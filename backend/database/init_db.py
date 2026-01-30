#!/usr/bin/env python3
"""
SolarArc Pro Database Initialization Script
功能：初始化数据库（创建表结构）
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


def create_database(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str
) -> bool:
    """创建数据库"""
    try:
        cmd = [
            'mysql',
            f'-h{host}',
            f'-P{port}',
            f'-u{user}',
            f'-p{password}',
            '-e', f'CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print_colored(f"错误: {result.stderr}", Colors.RED)
            return False

        return True
    except subprocess.TimeoutExpired:
        print_colored("错误: 创建数据库超时", Colors.RED)
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
        description='SolarArc Pro 数据库初始化脚本'
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
    print_colored("SolarArc Pro 数据库初始化脚本", Colors.BLUE)
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
    init_sql = sql_dir / '01_init_tables.sql'

    if not init_sql.exists():
        print_colored(f"错误: 找不到SQL文件 {init_sql}", Colors.RED)
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
    print(f"检查数据库 '{args.database}' 是否存在...")
    db_exists = check_database_exists(args.host, args.port, args.user, args.password, args.database)

    if not db_exists:
        print(f"数据库 '{args.database}' 不存在")
        print("正在创建数据库...")
        if not create_database(args.host, args.port, args.user, args.password, args.database):
            print_colored("✗ 创建数据库失败", Colors.RED)
            sys.exit(1)
        print_colored(f"✓ 数据库 '{args.database}' 创建成功", Colors.GREEN)
    else:
        print_colored(f"✓ 数据库 '{args.database}' 已存在", Colors.GREEN)
    print()

    # 询问是否继续
    if not args.yes:
        print_colored("警告：此操作将创建/覆盖数据库表结构", Colors.YELLOW)
        confirm = input("是否继续？(yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("操作已取消")
            sys.exit(0)

    # 执行初始化脚本
    print()
    print("正在执行初始化脚本...")

    # 使用标准输入方式执行SQL
    try:
        with open(init_sql, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        cmd = [
            'mysql',
            f'-h{args.host}',
            f'-P{args.port}',
            f'-u{args.user}',
            f'-p{args.password}',
            args.database
        ]

        result = subprocess.run(
            cmd,
            input=sql_content,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print_colored("✗ 初始化失败", Colors.RED)
            if result.stderr:
                print_colored(f"错误信息: {result.stderr}", Colors.RED)
            sys.exit(1)

    except subprocess.TimeoutExpired:
        print_colored("✗ 初始化超时", Colors.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"✗ 初始化失败: {e}", Colors.RED)
        sys.exit(1)

    print_colored("✓ 数据库表结构初始化完成", Colors.GREEN)
    print()
    print("下一步：")
    print("  运行 python seed_db.py 插入 demo 数据")

    print()
    print_colored("========================================", Colors.BLUE)
    print_colored("初始化完成！", Colors.BLUE)
    print_colored("========================================", Colors.BLUE)
    print()
    print("数据库已准备就绪，可以启动后端服务")
    print()
    print("命令提示：")
    print("  启动后端：cd .. && python start.py")
    print("  插入数据：python seed_db.py")


if __name__ == '__main__':
    main()
