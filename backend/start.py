#!/usr/bin/env python3
"""
SolarArc Pro Backend Startup Script
功能：启动后端服务器
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Optional

# ANSI颜色代码
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_colored(message: str, color: str = Colors.NC):
    """打印彩色消息"""
    print(f"{color}{message}{Colors.NC}")


def check_python_version() -> bool:
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored(f"错误: Python 3.8+ required, found {version.major}.{version.minor}", Colors.RED)
        return False
    return True


def create_virtual_environment(venv_path: Path) -> bool:
    """创建虚拟环境"""
    try:
        print("创建虚拟环境...")
        subprocess.run(
            [sys.executable, '-m', 'venv', str(venv_path)],
            check=True,
            capture_output=True
        )
        print_colored("✓ 虚拟环境创建成功", Colors.GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"错误: 创建虚拟环境失败 - {e}", Colors.RED)
        return False


def install_dependencies(venv_path: Path, requirements_file: Path) -> bool:
    """安装依赖"""
    try:
        print("安装依赖包...")

        # 确定pip路径
        if os.name == 'nt':  # Windows
            pip_path = venv_path / 'Scripts' / 'pip'
        else:  # Linux/Mac
            pip_path = venv_path / 'bin' / 'pip'

        subprocess.run(
            [str(pip_path), 'install', '-r', str(requirements_file)],
            check=True,
            capture_output=True
        )
        print_colored("✓ 依赖包安装成功", Colors.GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"错误: 安装依赖失败 - {e}", Colors.RED)
        return False


def check_env_file(env_file: Path, env_example: Optional[Path]) -> bool:
    """检查.env文件"""
    if not env_file.exists():
        if env_example and env_example.exists():
            print_colored("创建 .env 文件从 .env.example...", Colors.YELLOW)
            import shutil
            shutil.copy(env_example, env_file)
            print_colored("✓ .env 文件已创建", Colors.GREEN)
            print_colored("请编辑 .env 文件配置您的环境变量", Colors.YELLOW)
            return False
        else:
            print_colored("错误: .env 文件不存在且没有 .env.example 模板", Colors.RED)
            return False
    return True


def start_server(
    venv_path: Path,
    host: str,
    port: int,
    reload: bool
) -> None:
    """启动FastAPI服务器"""
    try:
        print_colored("========================================", Colors.BLUE)
        print_colored("启动 FastAPI 服务器...", Colors.BLUE)
        print_colored("========================================", Colors.BLUE)
        print()

        # 确定uvicorn路径
        if os.name == 'nt':  # Windows
            uvicorn_path = venv_path / 'Scripts' / 'uvicorn'
        else:  # Linux/Mac
            uvicorn_path = venv_path / 'bin' / 'uvicorn'

        # 构建命令
        cmd = [
            str(uvicorn_path),
            'app.main:app',
            '--host', host,
            '--port', str(port)
        ]

        if reload:
            cmd.append('--reload')

        # 打印启动信息
        print(f"主机: {host}")
        print(f"端口: {port}")
        print(f"重载: {'是' if reload else '否'}")
        print()
        print_colored("API 文档: http://localhost:8000/api/docs", Colors.GREEN)
        print_colored("ReDoc 文档: http://localhost:8000/api/redoc", Colors.GREEN)
        print_colored("健康检查: http://localhost:8000/health", Colors.GREEN)
        print()
        print_colored("按 Ctrl+C 停止服务器", Colors.YELLOW)
        print_colored("========================================", Colors.BLUE)
        print()

        # 启动服务器
        subprocess.run(cmd)

    except KeyboardInterrupt:
        print()
        print_colored("服务器已停止", Colors.YELLOW)
    except Exception as e:
        print_colored(f"错误: 启动服务器失败 - {e}", Colors.RED)
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='SolarArc Pro 后端启动脚本'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='服务器监听地址（默认: 0.0.0.0）'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='服务器端口（默认: 8000）'
    )
    parser.add_argument(
        '--no-reload',
        action='store_true',
        help='禁用自动重载（生产环境）'
    )
    parser.add_argument(
        '--skip-deps',
        action='store_true',
        help='跳过依赖检查和安装'
    )

    args = parser.parse_args()

    # 打印标题
    print_colored("========================================", Colors.BLUE)
    print_colored("SolarArc Pro 后端启动脚本", Colors.BLUE)
    print_colored("========================================", Colors.BLUE)
    print()

    # 检查Python版本
    if not check_python_version():
        sys.exit(1)

    print_colored(f"✓ Python版本: {sys.version.split()[0]}", Colors.GREEN)
    print()

    # 获取项目路径
    project_root = Path(__file__).parent
    venv_path = project_root / '.venv'
    requirements_file = project_root / 'requirements.txt'
    env_file = project_root / '.env'
    env_example = project_root / '.env.example'

    # 检查/创建虚拟环境
    if not venv_path.exists():
        if not create_virtual_environment(venv_path):
            sys.exit(1)
        print()
    else:
        print_colored("✓ 虚拟环境已存在", Colors.GREEN)
        print()

    # 安装依赖
    if not args.skip_deps:
        if not install_dependencies(venv_path, requirements_file):
            sys.exit(1)
        print()

    # 检查.env文件
    if not check_env_file(env_file, env_example):
        print_colored("请配置 .env 文件后重新运行", Colors.YELLOW)
        sys.exit(1)

    print_colored("✓ 环境配置检查完成", Colors.GREEN)
    print()

    # 启动服务器
    start_server(
        venv_path=venv_path,
        host=args.host,
        port=args.port,
        reload=not args.no_reload
    )


if __name__ == '__main__':
    main()
