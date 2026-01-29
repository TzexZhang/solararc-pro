"""
阴影计算服务

使用Shadow Volume算法计算建筑阴影
"""
from datetime import datetime, date
from typing import Dict, List, Optional
import numpy as np

try:
    from shapely.geometry import Polygon, Point, mapping
    from shapely.ops import unary_union
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

from app.utils.logger import logger
from app.services.solar_service import SolarService


class ShadowService:
    """阴影计算服务"""

    def __init__(self):
        """初始化阴影计算服务"""
        self.solar_service = SolarService()
        if not SHAPELY_AVAILABLE:
            logger.warning("Shapely未安装，阴影计算功能受限")

    async def calculate_shadows(
        self,
        building_ids: List[int],
        target_date: date,
        hour: int,
        minute: int = 0,
    ) -> Dict:
        """
        计算建筑阴影

        Args:
            building_ids: 建筑ID列表
            target_date: 目标日期
            hour: 小时
            minute: 分钟

        Returns:
            包含阴影数据的字典
        """
        try:
            import time
            start_time = time.time()

            # 获取建筑信息（这里需要从数据库获取，暂时使用模拟数据）
            buildings = await self._get_buildings_by_ids(building_ids)

            # 计算太阳位置
            # 使用第一个建筑的坐标作为太阳位置计算点
            if buildings:
                sample_building = buildings[0]
                # 从建筑底面提取中心点坐标
                footprint = sample_building.get("footprint")
                center_lng = footprint.get("coordinates")[0][0][0] if footprint else 116.397428
                center_lat = footprint.get("coordinates")[0][0][1] if footprint else 39.90923

                solar_position = await self.solar_service.calculate_solar_position(
                    latitude=center_lat,
                    longitude=center_lng,
                    target_date=target_date,
                    hour=hour,
                    minute=minute,
                )

                solar_altitude = solar_position["solar_altitude"]
                solar_azimuth = solar_position["solar_azimuth"]
            else:
                # 默认值
                solar_altitude = 45.0
                solar_azimuth = 180.0

            # 计算每个建筑的阴影
            shadows = []
            for building in buildings:
                shadow = await self._calculate_single_shadow(
                    building=building,
                    solar_altitude=solar_altitude,
                    solar_azimuth=solar_azimuth,
                )
                shadows.append(shadow)

            calculation_time = (time.time() - start_time) * 1000  # 毫秒

            return {
                "shadows": shadows,
                "solar_position": {
                    "altitude": solar_altitude,
                    "azimuth": solar_azimuth,
                },
                "calculation_time_ms": round(calculation_time, 2),
            }

        except Exception as e:
            logger.error(f"计算阴影失败: {str(e)}")
            raise

    async def compare_extreme_shadows(
        self,
        building_id: int,
        hour: int = 12,
    ) -> Dict:
        """
        对比极端日期的阴影

        Args:
            building_id: 建筑ID
            hour: 小时（默认正午）

        Returns:
            冬至日和夏至日阴影对比
        """
        try:
            # 获取建筑信息
            buildings = await self._get_buildings_by_ids([building_id])
            if not buildings:
                raise ValueError(f"建筑ID {building_id} 不存在")

            building = buildings[0]

            # 提取建筑坐标
            footprint = building.get("footprint")
            center_lng = footprint.get("coordinates")[0][0][0] if footprint else 116.397428
            center_lat = footprint.get("coordinates")[0][0][1] if footprint else 39.90923

            # 计算冬至日和夏至日的阴影
            current_year = datetime.now().year

            # 冬至日（12月22日，阴影最长）
            winter_shadow = await self._calculate_shadow_for_date(
                building=building,
                latitude=center_lat,
                longitude=center_lng,
                date_str=f"{current_year}-12-22",
                hour=hour,
            )

            # 夏至日（6月21日，阴影最短）
            summer_shadow = await self._calculate_shadow_for_date(
                building=building,
                latitude=center_lat,
                longitude=center_lng,
                date_str=f"{current_year}-06-21",
                hour=hour,
            )

            # 计算阴影长度系数
            winter_coefficient = winter_shadow.get("shadow_length_coefficient", 1.0)
            summer_coefficient = summer_shadow.get("shadow_length_coefficient", 1.0)
            ratio = winter_coefficient / summer_coefficient if summer_coefficient > 0 else 0

            return {
                "winter_solstice": {
                    "date": f"{current_year}-12-22",
                    "shadow_polygon": winter_shadow.get("shadow_polygon"),
                    "shadow_area": winter_shadow.get("shadow_area", 0),
                    "shadow_length_coefficient": winter_coefficient,
                    "solar_altitude": winter_shadow.get("solar_altitude", 0),
                },
                "summer_solstice": {
                    "date": f"{current_year}-06-21",
                    "shadow_polygon": summer_shadow.get("shadow_polygon"),
                    "shadow_area": summer_shadow.get("shadow_area", 0),
                    "shadow_length_coefficient": summer_coefficient,
                    "solar_altitude": summer_shadow.get("solar_altitude", 0),
                },
                "ratio": round(ratio, 3),
            }

        except Exception as e:
            logger.error(f"对比极端阴影失败: {str(e)}")
            raise

    async def generate_shadow_animation(
        self,
        building_id: int,
        target_date: date,
        start_hour: int = 6,
        end_hour: int = 18,
        step_minutes: int = 15,
    ) -> List[Dict]:
        """
        生成阴影动画帧

        Args:
            building_id: 建筑ID
            target_date: 目标日期
            start_hour: 开始小时
            end_hour: 结束小时
            step_minutes: 时间步长（分钟）

        Returns:
            动画帧列表
        """
        try:
            frames = []

            current_hour = start_hour
            current_minute = 0

            while current_hour < end_hour or (current_hour == end_hour and current_minute == 0):
                # 计算该时刻的阴影
                shadow_data = await self.calculate_shadows(
                    building_ids=[building_id],
                    target_date=target_date,
                    hour=current_hour,
                    minute=current_minute,
                )

                # 提取第一个（唯一）建筑的阴影
                if shadow_data.get("shadows"):
                    frame = {
                        "time": f"{current_hour:02d}:{current_minute:02d}",
                        "hour": current_hour,
                        "minute": current_minute,
                        "shadow": shadow_data["shadows"][0] if shadow_data["shadows"] else None,
                        "solar_altitude": shadow_data["solar_position"]["altitude"],
                        "solar_azimuth": shadow_data["solar_position"]["azimuth"],
                    }
                    frames.append(frame)

                # 推进时间
                current_minute += step_minutes
                if current_minute >= 60:
                    current_minute -= 60
                    current_hour += 1

            return frames

        except Exception as e:
            logger.error(f"生成阴影动画失败: {str(e)}")
            raise

    async def clear_cache(self, building_id: Optional[int] = None) -> int:
        """
        清空阴影缓存

        Args:
            building_id: 建筑ID，None表示清空所有

        Returns:
            删除的缓存数量
        """
        # 这里实现缓存清理逻辑
        # 实际项目中可以从Redis或数据库中删除缓存
        logger.info(f"清空阴影缓存: building_id={building_id}")
        return 0

    async def _get_buildings_by_ids(self, building_ids: List[int]) -> List[Dict]:
        """
        从数据库获取建筑信息

        Args:
            building_ids: 建筑ID列表

        Returns:
            建筑信息列表
        """
        # 这里应该是从数据库查询，暂时返回模拟数据
        # TODO: 实现数据库查询逻辑

        buildings = []
        for bid in building_ids:
            # 模拟建筑数据
            buildings.append({
                "id": bid,
                "name": f"建筑{bid}",
                "height": 100.0,
                "footprint": {
                    "type": "Polygon",
                    "coordinates": [[
                        [116.397428 + bid * 0.001, 39.90923],
                        [116.398428 + bid * 0.001, 39.90923],
                        [116.398428 + bid * 0.001, 39.91023],
                        [116.397428 + bid * 0.001, 39.91023],
                        [116.397428 + bid * 0.001, 39.90923],
                    ]],
                },
            })

        return buildings

    async def _calculate_single_shadow(
        self,
        building: Dict,
        solar_altitude: float,
        solar_azimuth: float,
    ) -> Dict:
        """
        计算单个建筑的阴影

        Args:
            building: 建筑信息
            solar_altitude: 太阳高度角
            solar_azimuth: 太阳方位角

        Returns:
            阴影数据
        """
        try:
            if not SHAPELY_AVAILABLE:
                # 返回模拟数据
                return {
                    "building_id": building.get("id"),
                    "shadow_polygon": None,
                    "shadow_area": 0,
                    "note": "Shapely not installed",
                }

            # 提取建筑信息
            building_id = building.get("id")
            height = building.get("height", 100)
            footprint_data = building.get("footprint")

            if not footprint_data:
                return {
                    "building_id": building_id,
                    "shadow_polygon": None,
                    "shadow_area": 0,
                }

            # 创建Shapely多边形
            footprint = Polygon(footprint_data["coordinates"][0])

            # 计算阴影（Shadow Volume算法）
            shadow = await self._project_shadow(
                footprint=footprint,
                height=height,
                solar_altitude=solar_altitude,
                solar_azimuth=solar_azimuth,
            )

            # 计算阴影面积
            shadow_area = shadow.area if shadow else 0

            # 计算阴影长度系数
            shadow_length_coefficient = self._calculate_shadow_coefficient(
                height=height,
                solar_altitude=solar_altitude,
            )

            return {
                "building_id": building_id,
                "shadow_polygon": mapping(shadow) if shadow else None,
                "shadow_area": round(shadow_area, 2),
                "shadow_length_coefficient": round(shadow_length_coefficient, 3),
            }

        except Exception as e:
            logger.error(f"计算单个建筑阴影失败: {str(e)}")
            return {
                "building_id": building.get("id"),
                "shadow_polygon": None,
                "shadow_area": 0,
                "error": str(e),
            }

    async def _project_shadow(
        self,
        footprint: Polygon,
        height: float,
        solar_altitude: float,
        solar_azimuth: float,
    ) -> Optional[Polygon]:
        """
        使用Shadow Volume算法投影阴影

        Args:
            footprint: 建筑底面多边形
            height: 建筑高度
            solar_altitude: 太阳高度角
            solar_azimuth: 太阳方位角

        Returns:
            阴影多边形
        """
        try:
            # 转换为弧度
            alt_rad = np.radians(solar_altitude)
            az_rad = np.radians(solar_azimuth)

            # 计算阴影长度
            # 阴影长度 = 建筑高度 / tan(太阳高度角)
            if solar_altitude <= 0:
                # 太阳在地平线以下，无阴影
                return None

            shadow_length = height / np.tan(alt_rad)

            # 计算阴影方向（太阳方位角的反方向）
            shadow_direction = az_rad + np.pi  # 反方向

            # 计算阴影偏移
            dx = shadow_length * np.cos(shadow_direction)
            dy = shadow_length * np.sin(shadow_direction)

            # 提取多边形顶点
            coords = list(footprint.exterior.coords)

            # 计算阴影多边形（连接建筑顶点和阴影顶点）
            shadow_coords = []
            for x, y in coords:
                # 原始顶点
                shadow_coords.append((x, y))
                # 阴影顶点
                shadow_coords.append((x + dx, y + dy))

            # 创建阴影多边形
            shadow_polygon = Polygon(shadow_coords)

            return shadow_polygon

        except Exception as e:
            logger.error(f"投影阴影失败: {str(e)}")
            return None

    def _calculate_shadow_coefficient(
        self,
        height: float,
        solar_altitude: float,
    ) -> float:
        """
        计算阴影长度系数

        Args:
            height: 建筑高度
            solar_altitude: 太阳高度角

        Returns:
            阴影长度系数
        """
        if solar_altitude <= 0:
            return float('inf')

        shadow_length = height / np.tan(np.radians(solar_altitude))
        coefficient = shadow_length / height if height > 0 else 0

        return coefficient

    async def _calculate_shadow_for_date(
        self,
        building: Dict,
        latitude: float,
        longitude: float,
        date_str: str,
        hour: int,
    ) -> Dict:
        """
        计算指定日期的阴影

        Args:
            building: 建筑信息
            latitude: 纬度
            longitude: 经度
            date_str: 日期字符串
            hour: 小时

        Returns:
            阴影数据
        """
        try:
            # 解析日期
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # 计算太阳位置
            solar_position = await self.solar_service.calculate_solar_position(
                latitude=latitude,
                longitude=longitude,
                target_date=target_date,
                hour=hour,
                minute=0,
            )

            # 计算阴影
            shadow = await self._calculate_single_shadow(
                building=building,
                solar_altitude=solar_position["solar_altitude"],
                solar_azimuth=solar_position["solar_azimuth"],
            )

            shadow["solar_altitude"] = solar_position["solar_altitude"]
            shadow["solar_azimuth"] = solar_position["solar_azimuth"]

            return shadow

        except Exception as e:
            logger.error(f"计算指定日期阴影失败: {str(e)}")
            return {
                "building_id": building.get("id"),
                "shadow_polygon": None,
                "shadow_area": 0,
                "solar_altitude": 0,
                "solar_azimuth": 0,
            }
