#!/usr/bin/env python3
"""
SolarArc Pro - Main Entry Point
这是后端应用的主入口文件
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 导入并运行应用
if __name__ == '__main__':
    import uvicorn
    from app.config import settings

    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║           SolarArc Pro Backend Server                ║
    ║           城市时空日照分析与可视化模拟平台           ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    print(f"🚀 启动服务器...")
    print(f"📍 环境: {settings.environment.upper()}")
    print(f"🌐 主机: {settings.api_host}")
    print(f"🔌 端口: {settings.api_port}")
    print(f"📚 API文档: http://{settings.api_host}:{settings.api_port}/api/docs")
    print(f"🏥 健康检查: http://{settings.api_host}:{settings.api_port}/health")
    print()

    try:
        uvicorn.run(
            "app.main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=(settings.environment == "development"),
            log_level=settings.log_level.lower()
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  服务器已停止")
    except Exception as e:
        print(f"\n\n❌ 启动失败: {e}")
        sys.exit(1)
