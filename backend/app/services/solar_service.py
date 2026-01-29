"""
太阳位置计算服务

使用pvlib和astral库计算精确的太阳位置
"""
from datetime import datetime, date, time
from typing import Dict, List, Optional
import pytz
import numpy as np

try:
    from pvlib.solarposition import get_solarposition
    from pvlib.irradiance import disc
    PVLIB_AVAILABLE = True
except ImportError:
    PVLIB_AVAILABLE = False

from app.utils.logger import logger


class SolarService:
    """太阳位置计算服务"""

    def __init__(self):
        """初始化太阳位置计算服务"""
        if not PVLIB_AVAILABLE:
            logger.warning("pvlib未安装，太阳位置计算功能受限")

    async def calculate_solar_position(
        self,
        latitude: float,
        longitude: float,
        target_date: date,
        hour: int,
        minute: int = 0,
        timezone: str = "Asia/Shanghai",
    ) -> Dict:
        """
        计算指定时间、地点的太阳位置

        Args:
            latitude: 纬度
            longitude: 经度
            target_date: 目标日期
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
            timezone: 时区

        Returns:
            包含太阳位置信息的字典
        """
        try:
            if not PVLIB_AVAILABLE:
                # 使用简化算法（天文算法基础版）
                return await self._calculate_simple_solar_position(
                    latitude, longitude, target_date, hour, minute, timezone
                )

            # 创建时区
            tz = pytz.timezone(timezone)

            # 创建日期时间对象
            dt = datetime.combine(target_date, time(hour, minute))
            localized_dt = tz.localize(dt)

            # 使用pvlib计算太阳位置
            solpos = get_solarposition(
                time=localized_dt,
                latitude=latitude,
                longitude=longitude,
                temperature=20,  # 气温（摄氏度）
                pressure=101325,  # 气压（帕斯卡）
            )

            # 提取结果
            result = solpos.iloc[0]

            solar_altitude = float(result['elevation'])
            solar_azimuth = float(result['azimuth'])
            solar_zenith = float(result['zenith'])

            # 计算日出日落时间
            sunrise_sunset = self._calculate_sunrise_sunset_pvlib(
                latitude, longitude, target_date, timezone
            )

            return {
                "latitude": latitude,
                "longitude": longitude,
                "datetime": localized_dt.isoformat(),
                "solar_altitude": round(solar_altitude, 6),
                "solar_azimuth": round(solar_azimuth, 6),
                "solar_zenith": round(solar_zenith, 6),
                "sunrise_time": sunrise_sunset["sunrise"],
                "sunset_time": sunrise_sunset["sunset"],
                "day_length": sunrise_sunset["day_length"],
                "solar_noon": sunrise_sunset["solar_noon"],
                "timezone": timezone,
            }

        except Exception as e:
            logger.error(f"计算太阳位置失败: {str(e)}")
            raise

    async def calculate_daily_positions(
        self,
        latitude: float,
        longitude: float,
        target_date: date,
        timezone: str = "Asia/Shanghai",
    ) -> List[Dict]:
        """
        计算24小时的太阳位置

        Args:
            latitude: 纬度
            longitude: 经度
            target_date: 目标日期
            timezone: 时区

        Returns:
            包含24小时太阳位置的列表
        """
        try:
            positions = []

            for hour in range(24):
                position = await self.calculate_solar_position(
                    latitude=latitude,
                    longitude=longitude,
                    target_date=target_date,
                    hour=hour,
                    minute=0,
                    timezone=timezone,
                )

                positions.append({
                    "hour": hour,
                    "altitude": position["solar_altitude"],
                    "azimuth": position["solar_azimuth"],
                })

            return positions

        except Exception as e:
            logger.error(f"计算24小时太阳位置失败: {str(e)}")
            raise

    async def calculate_sunrise_sunset(
        self,
        latitude: float,
        longitude: float,
        target_date: date,
        timezone: str = "Asia/Shanghai",
    ) -> Dict:
        """
        计算日出日落时间

        Args:
            latitude: 纬度
            longitude: 经度
            target_date: 目标日期
            timezone: 时区

        Returns:
            包含日出日落时间的字典
        """
        try:
            # 使用pvlib计算
            if PVLIB_AVAILABLE:
                return self._calculate_sunrise_sunset_pvlib(
                    latitude, longitude, target_date, timezone
                )
            else:
                return await self._calculate_sunrise_sunset_simple(
                    latitude, longitude, target_date, timezone
                )

        except Exception as e:
            logger.error(f"计算日出日落失败: {str(e)}")
            raise

    async def calculate_key_dates_positions(
        self,
        latitude: float,
        longitude: float,
        year: int,
        hour: int = 12,
    ) -> Dict:
        """
        计算关键日期的太阳位置

        Args:
            latitude: 纬度
            longitude: 经度
            year: 年份
            hour: 小时（默认正午）

        Returns:
            包含春分、夏至、秋分、冬至太阳位置的字典
        """
        try:
            # 关键日期（北半球）
            key_dates = {
                "spring_equinox": f"{year}-03-20",  # 春分
                "summer_solstice": f"{year}-06-21",  # 夏至
                "autumn_equinox": f"{year}-09-23",  # 秋分
                "winter_solstice": f"{year}-12-22",  # 冬至
            }

            result = {}

            for name, date_str in key_dates.items():
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                position = await self.calculate_solar_position(
                    latitude=latitude,
                    longitude=longitude,
                    target_date=target_date,
                    hour=hour,
                    minute=0,
                )

                result[name] = {
                    "date": date_str,
                    "solar_altitude": position["solar_altitude"],
                    "solar_azimuth": position["solar_azimuth"],
                    "sunrise_time": position["sunrise_time"],
                    "sunset_time": position["sunset_time"],
                    "day_length": position["day_length"],
                }

            return result

        except Exception as e:
            logger.error(f"计算关键日期太阳位置失败: {str(e)}")
            raise

    def _calculate_sunrise_sunset_pvlib(
        self,
        latitude: float,
        longitude: float,
        target_date: date,
        timezone: str,
    ) -> Dict:
        """使用pvlib计算日出日落"""
        try:
            tz = pytz.timezone(timezone)

            # 计算一天中的太阳位置
            times = [
                tz.localize(datetime.combine(target_date, time(h, m)))
                for h in range(24) for m in range(0, 60, 15)
            ]

            solpos = get_solarposition(
                time=times,
                latitude=latitude,
                longitude=longitude,
            )

            # 找到日出和日落
            mask = solpos['elevation'] > 0
            if mask.any():
                sunrise_idx = mask.idxmax()
                sunset_idx = len(mask) - mask[::-1].idxmax() - 1

                sunrise_time = times[sunrise_idx].strftime("%H:%M:%S")
                sunset_time = times[sunset_idx].strftime("%H:%M:%S")

                # 计算日照时长
                day_length_hours = (sunset_idx - sunrise_idx) * 0.25  # 15分钟步长
                day_length = round(day_length_hours, 2)

                # 计算正午时间
                solar_noon_idx = len(times) // 2
                solar_noon = times[solar_noon_idx].strftime("%H:%M:%S")
            else:
                # 极地情况
                sunrise_time = "00:00:00"
                sunset_time = "23:59:59"
                day_length = 24.0
                solar_noon = "12:00:00"

            return {
                "sunrise": sunrise_time,
                "sunset": sunset_time,
                "day_length": day_length,
                "solar_noon": solar_noon,
            }

        except Exception as e:
            logger.error(f"pvlib计算日出日落失败: {str(e)}")
            # 返回默认值
            return {
                "sunrise": "06:00:00",
                "sunset": "18:00:00",
                "day_length": 12.0,
                "solar_noon": "12:00:00",
            }

    async def _calculate_simple_solar_position(
        self,
        latitude: float,
        longitude: float,
        target_date: date,
        hour: int,
        minute: int,
        timezone: str,
    ) -> Dict:
        """
        简化的太阳位置计算（不依赖pvlib）

        使用天文算法基础公式
        """
        try:
            # 这里实现简化的太阳位置计算算法
            # 实际项目中应使用pvlib获得更高精度

            # 简化的太阳高度角和方位角计算
            # （这里仅作示例，实际需要完整的SPS算法）

            import math

            # 年积日
            year_start = date(target_date.year, 1, 1)
            day_of_year = (target_date - year_start).days + 1

            # 简化的太阳赤纬角（度）
            declination = 23.45 * math.sin(math.radians(360 / 365 * (day_of_year - 81)))

            # 时角（度）
            hour_angle = 15 * (hour - 12) + minute / 4

            # 太阳高度角（度）
            lat_rad = math.radians(latitude)
            dec_rad = math.radians(declination)
            ha_rad = math.radians(hour_angle)

            altitude = math.asin(
                math.sin(lat_rad) * math.sin(dec_rad) +
                math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad)
            )
            solar_altitude = math.degrees(altitude)

            # 太阳方位角（度）
            azimuth = math.atan2(
                math.sin(ha_rad),
                math.cos(ha_rad) * math.sin(lat_rad) -
                math.tan(dec_rad) * math.cos(lat_rad)
            )
            solar_azimuth = (math.degrees(azimuth) + 180) % 360

            # 太阳天顶角
            solar_zenith = 90 - solar_altitude

            return {
                "latitude": latitude,
                "longitude": longitude,
                "datetime": f"{target_date} {hour:02d}:{minute:02d}",
                "solar_altitude": round(solar_altitude, 6),
                "solar_azimuth": round(solar_azimuth, 6),
                "solar_zenith": round(solar_zenith, 6),
                "sunrise_time": "06:00:00",
                "sunset_time": "18:00:00",
                "day_length": 12.0,
                "solar_noon": "12:00:00",
                "timezone": timezone,
                "note": "Simplified calculation (pvlib not installed)",
            }

        except Exception as e:
            logger.error(f"简化太阳位置计算失败: {str(e)}")
            raise

    async def _calculate_sunrise_sunset_simple(
        self,
        latitude: float,
        longitude: float,
        target_date: date,
        timezone: str,
    ) -> Dict:
        """简化的日出日落计算"""
        # 简化计算，返回近似值
        return {
            "sunrise": "06:00:00",
            "sunset": "18:00:00",
            "day_length": 12.0,
            "solar_noon": "12:00:00",
            "note": "Simplified calculation (pvlib not installed)",
        }
