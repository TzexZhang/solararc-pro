#!/usr/bin/env python3
"""
SolarArc Pro Database Seeding Script
功能：插入 demo 数据
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


def check_mysql_command() -> bool:
    """检查MySQL命令是否可用"""
    try:
        result = subprocess.run(['mysql', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def test_mysql_connection(
    host: str,
    port: int,
    user: str,
    password: str
) -> bool:
    """测试MySQL连接"""
    try:
        cmd = [
            'mysql',
            f'-h{host}',
            f'-P{port}',
            f'-u{user}',
            f'-p{password}',
            '-e', 'SELECT 1'
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def check_database_exists(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str
) -> bool:
    """检查数据库是否存在"""
    try:
        cmd = [
            'mysql',
            f'-h{host}',
            f'-P{port}',
            f'-u{user}',
            f'-p{password}',
            '-e', f'SHOW DATABASES LIKE "{database}"'
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return database in result.stdout
    except subprocess.TimeoutExpired:
        return False


def execute_sql_file(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    sql_file: Path
) -> bool:
    """执行SQL文件"""
    try:
        # 读取SQL文件并确保使用UTF-8编码
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 将SQL内容编码为UTF-8字节
        sql_bytes = sql_content.encode('utf-8')

        cmd = [
            'mysql',
            f'-h{host}',
            f'-P{port}',
            f'-u{user}',
            f'-p{password}',
            '--default-character-set=utf8mb4',
            database
        ]

        result = subprocess.run(
            cmd,
            input=sql_bytes,
            capture_output=True,
            timeout=60
        )

        if result.returncode != 0:
            stderr_output = result.stderr.decode('utf-8', errors='replace')
            print_colored(f"错误: {stderr_output}", Colors.RED)
            return False

        return True
    except subprocess.TimeoutExpired:
        print_colored("错误: 执行超时", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"错误: {e}", Colors.RED)
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='SolarArc Pro 数据库 Seeding 脚本'
    )
    parser.add_argument(
        '--host',
        default=os.getenv('DB_HOST', 'localhost'),
        help='MySQL主机地址'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=int(os.getenv('DB_PORT', '3306')),
        help='MySQL端口'
    )
    parser.add_argument(
        '--user',
        default=os.getenv('DB_USER', 'root'),
        help='MySQL用户名'
    )
    parser.add_argument(
        '--password',
        default=os.getenv('DB_PASSWORD', ''),
        help='MySQL密码'
    )
    parser.add_argument(
        '--database',
        default=os.getenv('DB_NAME', 'solararc_pro'),
        help='数据库名称'
    )
    parser.add_argument(
        '--yes',
        '-y',
        action='store_true',
        help='跳过确认提示'
    )

    args = parser.parse_args()

    # 打印标题
    print_colored("========================================", Colors.BLUE)
    print_colored("SolarArc Pro 数据库 Seeding 脚本", Colors.BLUE)
    print_colored("========================================", Colors.BLUE)
    print()

    # 打印配置信息
    print("数据库配置信息：")
    print(f"  主机: {args.host}")
    print(f"  端口: {args.port}")
    print(f"  用户: {args.user}")
    print(f"  数据库: {args.database}")
    print()

    # 获取SQL目录
    sql_dir = Path(__file__).parent
    seed_sql = sql_dir / '02_seed_data.sql'

    if not seed_sql.exists():
        print_colored(f"错误: 找不到SQL文件 {seed_sql}", Colors.RED)
        sys.exit(1)

    # 检查MySQL命令
    print("检查 MySQL 连接...")
    if not check_mysql_command():
        print_colored("错误: mysql 命令未找到，请先安装 MySQL", Colors.RED)
        sys.exit(1)

    # 测试连接
    if not test_mysql_connection(args.host, args.port, args.user, args.password):
        print_colored("错误: 无法连接到数据库，请检查配置信息", Colors.RED)
        print()
        print("请确认：")
        print("  1. MySQL 服务已启动")
        print("  2. 数据库用户名和密码正确")
        print(f"  3. 端口 {args.port} 可访问")
        sys.exit(1)

    print_colored("✓ MySQL 连接成功", Colors.GREEN)
    print()

    # 检查数据库是否存在
    print("检查数据库是否存在...")
    if not check_database_exists(args.host, args.port, args.user, args.password, args.database):
        print_colored(f"错误: 数据库 '{args.database}' 不存在", Colors.RED)
        print()
        print("请先运行 init_db.py 创建数据库表结构")
        sys.exit(1)

    print_colored("✓ 数据库存在", Colors.GREEN)
    print()

    # 询问是否继续
    if not args.yes:
        print_colored("警告：此操作将插入 demo 数据到数据库", Colors.YELLOW)
        confirm = input("是否继续？(yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("操作已取消")
            sys.exit(0)

    # 执行 seeding 脚本
    print()
    print("正在插入 demo 数据...")

    if not execute_sql_file(args.host, args.port, args.user, args.password, args.database, seed_sql):
        print_colored("✗ Seeding 失败", Colors.RED)
        sys.exit(1)

    print_colored("✓ Demo 数据插入成功", Colors.GREEN)
    print()
    print("Demo 用户信息：")
    print("  管理员: admin@solararc.pro (密码: password123)")
    print("  演示用户: demo@solararc.pro (密码: password123)")
    print("  测试用户: test@solararc.pro (密码: password123)")
    print()
    print("Demo 数据包括：")
    print("  - 3 个测试用户")
    print("  - 8 个示例建筑（北京朝阳区）")
    print("  - 2 个示例项目")
    print("  - 太阳位置数据（夏至/冬至）")
    print("  - 1 个示例分析报告")

    print()
    print_colored("========================================", Colors.BLUE)
    print_colored("Seeding 完成！", Colors.BLUE)
    print_colored("========================================", Colors.BLUE)
    print()
    print("数据库已包含 demo 数据，可以启动后端服务测试")
    print()
    print("命令提示：")
    print("  启动后端：cd .. && python start.py")
    print("  访问 API 文档: http://localhost:8000/api/docs")


if __name__ == '__main__':
    main()
