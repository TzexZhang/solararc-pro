#!/usr/bin/env python3
"""
插入Demo数据脚本

用于向数据库插入测试数据

符合需求文档第四章的数据库设计

使用方法:
    python -m backend.database.insert_demo_data
    或
    cd backend/database
    python insert_demo_data.py
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta, date

# 添加项目根目录和backend目录到Python路径
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent  # 项目根目录
backend_dir = current_file.parent.parent  # backend目录

# 将backend目录添加到路径（这样可以导入app模块）
sys.path.insert(0, str(backend_dir))
# 将项目根目录添加到路径（为了支持模块运行方式）
sys.path.insert(0, str(project_root))

# 验证路径设置
if Path(backend_dir / "app").exists():
    print(f"✅ 找到app模块目录: {backend_dir / 'app'}")
else:
    print(f"❌ 错误: 无法找到app模块目录")
    print(f"   搜索路径: {backend_dir / 'app'}")
    sys.exit(1)

from sqlalchemy import select, func
from geoalchemy2 import WKTElement
from app.core.database import async_session_maker
from app.models.building import Building
from app.models.shadow_analysis import ShadowAnalysisCache
from app.models.solar_position import SolarPositionPrecalc
from app.models.user_settings import UserSettings
from app.utils.logger import logger


# Demo建筑数据
# 注意：WKT格式中坐标顺序为 纬度 经度 (latitude longitude)
DEMO_BUILDINGS = [
    {
        "name": "上海中心大厦",
        "building_type": "commercial",
        "total_height": 632.0,
        "floor_area": 420000.0,
        "floor_count": 127,
        "reflective_rate": 0.35,
        "footprint_wkt": "POLYGON((31.2336 121.5058, 31.2336 121.5068, 31.2346 121.5068, 31.2346 121.5058, 31.2336 121.5058))",
        "address": "上海市浦东新区陆家嘴银城中路501号",
        "district": "浦东新区",
        "city": "上海",
        "country": "China"
    },
    {
        "name": "环球金融中心",
        "building_type": "commercial",
        "total_height": 492.0,
        "floor_area": 381600.0,
        "floor_count": 101,
        "reflective_rate": 0.32,
        "footprint_wkt": "POLYGON((31.2328 121.5050, 31.2328 121.5060, 31.2338 121.5060, 31.2338 121.5050, 31.2328 121.5050))",
        "address": "上海市浦东新区世纪大道100号",
        "district": "浦东新区",
        "city": "上海",
        "country": "China"
    },
    {
        "name": "金茂大厦",
        "building_type": "commercial",
        "total_height": 420.5,
        "floor_area": 290000.0,
        "floor_count": 88,
        "reflective_rate": 0.30,
        "footprint_wkt": "POLYGON((31.2320 121.5042, 31.2320 121.5052, 31.2330 121.5052, 31.2330 121.5042, 31.2320 121.5042))",
        "address": "上海市浦东新区世纪大道88号",
        "district": "浦东新区",
        "city": "上海",
        "country": "China"
    },
    {
        "name": "北京中信大厦",
        "building_type": "commercial",
        "total_height": 528.0,
        "floor_area": 437000.0,
        "floor_count": 108,
        "reflective_rate": 0.33,
        "footprint_wkt": "POLYGON((39.9100 116.4300, 39.9100 116.4310, 39.9110 116.4310, 39.9110 116.4300, 39.9100 116.4300))",
        "address": "北京市朝阳区光华路CBD",
        "district": "朝阳区",
        "city": "北京",
        "country": "China"
    },
    {
        "name": "深圳平安国际金融中心",
        "building_type": "commercial",
        "total_height": 599.1,
        "floor_area": 460000.0,
        "floor_count": 115,
        "reflective_rate": 0.34,
        "footprint_wkt": "POLYGON((22.5330 114.0550, 22.5330 114.0560, 22.5340 114.0560, 22.5340 114.0550, 22.5330 114.0550))",
        "address": "深圳市福田区益田路5033号",
        "district": "福田区",
        "city": "深圳",
        "country": "China"
    },
    {
        "name": "广州周大福金融中心",
        "building_type": "commercial",
        "total_height": 530.0,
        "floor_area": 405000.0,
        "floor_count": 111,
        "reflective_rate": 0.31,
        "footprint_wkt": "POLYGON((23.1080 113.3250, 23.1080 113.3260, 23.1090 113.3260, 23.1090 113.3250, 23.1080 113.3250))",
        "address": "广州市天河区珠江新城花城大道",
        "district": "天河区",
        "city": "广州",
        "country": "China"
    },
    {
        "name": "成都绿地中心",
        "building_type": "commercial",
        "total_height": 468.0,
        "floor_area": 350000.0,
        "floor_count": 98,
        "reflective_rate": 0.30,
        "footprint_wkt": "POLYGON((30.5700 104.0650, 30.5700 104.0660, 30.5710 104.0660, 30.5710 104.0650, 30.5700 104.0650))",
        "address": "成都市锦江区东大街",
        "district": "锦江区",
        "city": "成都",
        "country": "China"
    },
    {
        "name": "武汉绿地中心",
        "building_type": "commercial",
        "total_height": 475.0,
        "floor_area": 360000.0,
        "floor_count": 97,
        "reflective_rate": 0.32,
        "footprint_wkt": "POLYGON((30.5900 114.3000, 30.5900 114.3010, 30.5910 114.3010, 30.5910 114.3000, 30.5900 114.3000))",
        "address": "武汉市武昌区和平大道",
        "district": "武昌区",
        "city": "武汉",
        "country": "China"
    }
]


async def clear_demo_data():
    """清除现有的demo数据"""
    try:
        async with async_session_maker() as session:
            # 删除所有阴影分析缓存记录
            await session.execute(ShadowAnalysisCache.__table__.delete())

            # 删除所有太阳位置预计算记录
            await session.execute(SolarPositionPrecalc.__table__.delete())

            # 删除所有用户配置记录
            await session.execute(UserSettings.__table__.delete())

            # 删除所有建筑记录
            await session.execute(Building.__table__.delete())

            await session.commit()
            logger.info("✅ 已清除现有的demo数据")

    except Exception as e:
        logger.error(f"❌ 清除demo数据失败: {str(e)}")
        raise


async def insert_buildings():
    """插入建筑数据"""
    try:
        async with async_session_maker() as session:
            buildings_to_create = []

            for building_data in DEMO_BUILDINGS:
                # 提取WKT格式的空间数据
                footprint_wkt = building_data.pop("footprint_wkt")

                # 创建Geometry对象
                building = Building(
                    **building_data,
                    footprint=WKTElement(footprint_wkt, srid=4326)
                )
                buildings_to_create.append(building)

            session.add_all(buildings_to_create)
            await session.commit()

            logger.info(f"✅ 成功插入 {len(buildings_to_create)} 条建筑数据")

            return buildings_to_create

    except Exception as e:
        logger.error(f"❌ 插入建筑数据失败: {str(e)}")
        raise


async def insert_shadow_analyses():
    """插入阴影分析缓存数据"""
    try:
        async with async_session_maker() as session:
            # 获取所有建筑
            result = await session.execute(select(Building))
            buildings = result.scalars().all()

            if not buildings:
                logger.warning("⚠️  没有找到建筑数据，跳过插入阴影分析缓存数据")
                return []

            shadow_analyses = []

            # 为每个建筑创建几天的阴影分析数据
            base_date = datetime.now().date()

            for building in buildings:
                # 从footprint中提取坐标（使用ST_AsText获取WKT）
                result = await session.execute(
                    select(func.ST_AsText(Building.footprint)).where(Building.id == building.id)
                )
                footprint_wkt = result.scalar()

                # 简单解析WKT获取中心点（实际应用中应使用ST_Centroid）
                # 注意：WKT格式为 纬度 经度
                # 这里简化处理，使用第一个坐标点
                coords = footprint_wkt.replace("POLYGON((", "").replace("))", "").split(",")[0].split()
                latitude = float(coords[0])  # 第一个值是纬度
                longitude = float(coords[1])  # 第二个值是经度

                # 为每个建筑创建3天的阴影分析数据
                for day_offset in range(3):
                    analysis_date = base_date + timedelta(days=day_offset)

                    # 每天创建几个时间点的数据
                    for hour in [8, 12, 16, 20]:
                        # 计算过期时间（7天后）
                        expires_at = datetime.now() + timedelta(days=7)

                        # 生成阴影多边形WKT（格式：纬度 经度）
                        shadow_wkt = f"POLYGON(({latitude + 0.001} {longitude + 0.001}, {latitude + 0.001} {longitude + 0.002}, {latitude + 0.002} {longitude + 0.002}, {latitude + 0.002} {longitude + 0.001}, {latitude + 0.001} {longitude + 0.001}))"

                        shadow_analysis = ShadowAnalysisCache(
                            building_id=building.id,
                            analysis_date=analysis_date,
                            analysis_hour=hour,
                            shadow_polygon=WKTElement(shadow_wkt, srid=4326),
                            shadow_area=15000.0 + (hour * 100),  # 模拟不同时间的阴影面积
                            expires_at=expires_at
                        )
                        shadow_analyses.append(shadow_analysis)

            session.add_all(shadow_analyses)
            await session.commit()

            logger.info(f"✅ 成功插入 {len(shadow_analyses)} 条阴影分析缓存数据")

            return shadow_analyses

    except Exception as e:
        logger.error(f"❌ 插入阴影分析缓存数据失败: {str(e)}")
        raise


async def insert_solar_positions():
    """插入太阳位置预计算数据（关键日期）"""
    try:
        async with async_session_maker() as session:
            solar_positions = []

            # 获取所有建筑的独特位置
            result = await session.execute(
                select(func.ST_AsText(Building.footprint), Building.city)
            )
            buildings = result.fetchall()

            if not buildings:
                logger.warning("⚠️  没有找到建筑数据，跳过插入太阳位置预计算数据")
                return []

            # 收集唯一的位置（避免重复）
            unique_locations = {}  # 使用字典去重：(lat, lng) -> (footprint_wkt, city)

            for footprint_wkt, city in buildings:
                # 解析坐标
                coords = footprint_wkt.replace("POLYGON((", "").replace("))", "").split(",")[0].split()
                latitude = float(coords[0])  # 第一个值是纬度
                longitude = float(coords[1])  # 第二个值是经度

                # 使用坐标作为key，确保每个位置只处理一次
                location_key = (round(latitude, 6), round(longitude, 6))
                if location_key not in unique_locations:
                    unique_locations[location_key] = (footprint_wkt, city)

            logger.info(f"✅ 找到 {len(unique_locations)} 个唯一位置")

            # 定义关键日期（2026年）
            key_dates = {
                "spring_equinox": date(2026, 3, 20),  # 春分
                "summer_solstice": date(2026, 6, 21),  # 夏至
                "autumn_equinox": date(2026, 9, 23),  # 秋分
                "winter_solstice": date(2026, 12, 22),  # 冬至
            }

            # 为每个唯一位置插入关键日期的太阳位置数据
            import math

            for (latitude, longitude), (footprint_wkt, city) in unique_locations.items():
                # 为每个关键日期插入每小时的数据
                for date_name, analysis_date in key_dates.items():
                    for hour in range(24):
                        # 模拟太阳位置数据（实际应用中应使用pvlib计算）
                        # 这里简化处理，使用近似公式

                        # 简化的太阳高度角计算（仅用于演示）
                        day_of_year = (analysis_date - date(analysis_date.year, 1, 1)).days
                        declination = 23.45 * math.sin(math.radians(360 / 365 * (day_of_year - 81)))
                        hour_angle = 15 * (hour - 12)
                        altitude_rad = math.asin(
                            math.sin(math.radians(latitude)) * math.sin(math.radians(declination)) +
                            math.cos(math.radians(latitude)) * math.cos(math.radians(declination)) *
                            math.cos(math.radians(hour_angle))
                        )
                        altitude = max(-90, min(90, altitude_rad * 180 / math.pi))

                        # 简化的太阳方位角计算
                        azimuth = (180 + hour_angle) % 360

                        solar_position = SolarPositionPrecalc(
                            latitude=latitude,
                            longitude=longitude,
                            date=analysis_date,
                            hour=hour,
                            altitude_angle=round(altitude, 6),
                            azimuth_angle=round(azimuth, 6)
                        )
                        solar_positions.append(solar_position)

            session.add_all(solar_positions)
            await session.commit()

            logger.info(f"✅ 成功插入 {len(solar_positions)} 条太阳位置预计算数据")

            return solar_positions

    except Exception as e:
        logger.error(f"❌ 插入太阳位置预计算数据失败: {str(e)}")
        raise


async def show_statistics():
    """显示数据统计信息"""
    try:
        async with async_session_maker() as session:
            # 统计建筑数量
            building_count = await session.execute(func.count(Building.id))
            building_count = building_count.scalar()

            # 统计阴影分析缓存数量
            shadow_count = await session.execute(func.count(ShadowAnalysisCache.id))
            shadow_count = shadow_count.scalar()

            # 统计太阳位置预计算数量
            solar_count = await session.execute(func.count(SolarPositionPrecalc.id))
            solar_count = solar_count.scalar()

            # 按城市统计建筑数量
            city_stats = await session.execute(
                select(Building.city, func.count(Building.id))
                .group_by(Building.city)
            )
            city_stats = city_stats.fetchall()

            logger.info("\n" + "=" * 60)
            logger.info("📊 数据统计")
            logger.info("=" * 60)
            logger.info(f"建筑总数: {building_count}")
            logger.info(f"阴影分析缓存记录总数: {shadow_count}")
            logger.info(f"太阳位置预计算记录总数: {solar_count}")
            logger.info("\n按城市统计:")
            for city, count in city_stats:
                logger.info(f"  - {city}: {count} 栋建筑")
            logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ 统计数据失败: {str(e)}")


async def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="插入Demo数据到数据库")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="清除现有数据后再插入"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("🚀 开始插入Demo数据...")
    logger.info("=" * 60)
    logger.info("📖 根据需求文档第四章设计插入测试数据")

    try:
        # 1. 清除现有数据（可选）
        if args.clear:
            logger.info("\n📝 步骤 1/4: 清除现有数据")
            await clear_demo_data()
        else:
            logger.info("\n📝 步骤 1/4: 检查现有数据")
            async with async_session_maker() as session:
                result = await session.execute(func.count(Building.id))
                count = result.scalar()
                if count > 0:
                    logger.warning(f"⚠️  数据库中已有 {count} 条建筑数据")
                    logger.warning("💡 如需清除现有数据，请使用 --clear 参数")
                else:
                    logger.info("✅ 数据库为空，可以插入新数据")

        # 2. 插入建筑数据
        logger.info("\n📝 步骤 2/4: 插入建筑数据")
        await insert_buildings()

        # 3. 插入阴影分析缓存数据
        logger.info("\n📝 步骤 3/4: 插入阴影分析缓存数据")
        await insert_shadow_analyses()

        # 4. 插入太阳位置预计算数据
        logger.info("\n📝 步骤 4/4: 插入太阳位置预计算数据")
        await insert_solar_positions()

        # 5. 显示统计信息
        await show_statistics()

        logger.info("\n" + "=" * 60)
        logger.info("🎉 Demo数据插入完成！")
        logger.info("=" * 60)
        logger.info("\n📚 插入的数据表:")
        logger.info("  - buildings: 建筑数据")
        logger.info("  - shadow_analysis_cache: 阴影分析缓存")
        logger.info("  - solar_positions_precalc: 太阳位置预计算（关键日期）")

    except Exception as e:
        logger.error("\n" + "=" * 60)
        logger.error(f"❌ 插入Demo数据失败: {str(e)}")
        logger.error("=" * 60)
        sys.exit(1)
    finally:
        # 确保数据库引擎被正确关闭
        try:
            from app.core.database import engine
            await engine.dispose()
        except:
            pass


if __name__ == "__main__":
    # 运行异步主函数
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⚠️  操作被用户中断")
        sys.exit(0)
