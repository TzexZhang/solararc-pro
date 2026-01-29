#!/usr/bin/env python3
"""
数据库初始化脚本

用于创建数据库表结构

符合需求文档第四章的数据库设计

使用方法:
    python -m backend.database.init_db
    或
    cd backend/database
    python init_db.py
"""
import asyncio
import sys
from pathlib import Path

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

from sqlalchemy import text
from app.core.database import engine, Base
from app.utils.logger import logger
from app.config import settings


async def create_database():
    """创建数据库（如果不存在）"""
    try:
        # 从DATABASE_URL中提取数据库名称
        db_name = settings.DATABASE_URL.split('/')[-1].split('?')[0]

        # 创建连接到MySQL服务器（不指定数据库）
        server_url = settings.DATABASE_URL.rsplit('/', 1)[0]

        from sqlalchemy.ext.asyncio import create_async_engine
        server_engine = create_async_engine(
            server_url.replace("mysql+pymysql://", "mysql+aiomysql://"),
            echo=False,
        )

        async with server_engine.connect() as conn:
            # 检查数据库是否存在
            result = await conn.execute(
                text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{db_name}'")
            )

            if not result.fetchone():
                # 创建数据库
                await conn.execute(
                    text(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                )
                await conn.commit()
                logger.info(f"✅ 数据库 '{db_name}' 创建成功")
            else:
                logger.info(f"ℹ️  数据库 '{db_name}' 已存在")

        await server_engine.dispose()

    except Exception as e:
        logger.error(f"❌ 创建数据库失败: {str(e)}")
        raise


async def create_tables():
    """创建所有表"""
    try:
        async with engine.begin() as conn:
            # 导入所有模型以确保它们被注册
            from app.models import building, shadow_analysis, solar_position, user_settings

            # 创建所有表
            await conn.run_sync(Base.metadata.create_all)

            logger.info("✅ 数据库表创建成功")

            # 显示创建的表
            tables = list(Base.metadata.tables.keys())
            logger.info(f"📋 已创建的表: {', '.join(tables)}")

            # 创建空间索引（如果不存在）
            await create_spatial_indexes(conn)

    except Exception as e:
        logger.error(f"❌ 创建表失败: {str(e)}")
        raise


async def create_spatial_indexes(conn):
    """创建空间索引"""
    try:
        # 检查并创建 buildings 表的空间索引
        await conn.execute(text("""
            CREATE SPATIAL INDEX IF NOT EXISTS idx_footprint
            ON buildings(footprint)
        """))

        # 检查并创建 shadow_analysis_cache 表的空间索引
        await conn.execute(text("""
            CREATE SPATIAL INDEX IF NOT EXISTS idx_shadow_polygon
            ON shadow_analysis_cache(shadow_polygon)
        """))

        logger.info("✅ 空间索引创建成功")

    except Exception as e:
        logger.warning(f"⚠️  创建空间索引时出现警告: {str(e)}")


async def verify_tables():
    """验证表是否创建成功"""
    try:
        async with engine.connect() as conn:
            # 检查表是否存在
            result = await conn.execute(
                text("SHOW TABLES")
            )
            tables = [row[0] for row in result.fetchall()]

            logger.info(f"📊 当前数据库中的表: {', '.join(tables) if tables else '无'}")

            # 验证关键表
            required_tables = [
                'buildings',
                'shadow_analysis_cache',
                'solar_positions_precalc',
                'user_settings'
            ]
            missing_tables = [t for t in required_tables if t not in tables]

            if missing_tables:
                logger.warning(f"⚠️  缺少的表: {', '.join(missing_tables)}")
                return False
            else:
                logger.info("✅ 所有必需的表都已创建")

                # 验证空间索引
                await verify_spatial_indexes(conn)
                return True

    except Exception as e:
        logger.error(f"❌ 验证表失败: {str(e)}")
        return False


async def verify_spatial_indexes(conn):
    """验证空间索引"""
    try:
        # 检查 buildings 表的空间索引
        result = await conn.execute(text("""
            SHOW INDEX FROM buildings WHERE Key_name = 'idx_footprint'
        """))
        if result.fetchone():
            logger.info("✅ buildings.footprint 空间索引已创建")

        # 检查 shadow_analysis_cache 表的空间索引
        result = await conn.execute(text("""
            SHOW INDEX FROM shadow_analysis_cache WHERE Key_name = 'idx_shadow_polygon'
        """))
        if result.fetchone():
            logger.info("✅ shadow_analysis_cache.shadow_polygon 空间索引已创建")

    except Exception as e:
        logger.warning(f"⚠️  验证空间索引时出现警告: {str(e)}")


async def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🚀 开始初始化数据库...")
    logger.info("=" * 60)
    logger.info("📖 根据需求文档第四章设计创建数据库结构")

    try:
        # 1. 创建数据库
        logger.info("\n📝 步骤 1/3: 创建数据库")
        await create_database()

        # 2. 创建表
        logger.info("\n📝 步骤 2/3: 创建数据表")
        await create_tables()

        # 3. 验证表
        logger.info("\n📝 步骤 3/3: 验证表结构")
        success = await verify_tables()

        if success:
            logger.info("\n" + "=" * 60)
            logger.info("🎉 数据库初始化完成！")
            logger.info("=" * 60)
            logger.info("\n📚 数据库设计参考:")
            logger.info("  - buildings (建筑表): §4.2.1")
            logger.info("  - solar_positions_precalc (太阳位置预计算表): §4.2.2")
            logger.info("  - shadow_analysis_cache (阴影分析缓存表): §4.2.3")
            logger.info("  - user_settings (用户配置表): §4.2.4")
        else:
            logger.error("\n" + "=" * 60)
            logger.error("❌ 数据库初始化未完全成功")
            logger.error("=" * 60)
            sys.exit(1)

    except Exception as e:
        logger.error("\n" + "=" * 60)
        logger.error(f"❌ 数据库初始化失败: {str(e)}")
        logger.error("=" * 60)
        sys.exit(1)
    finally:
        # 确保数据库引擎被正确关闭
        try:
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
