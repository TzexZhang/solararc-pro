"""重新生成并更新密码hash"""
import pymysql
import sys
import os

# 确保使用正确的bcrypt版本
try:
    from passlib.context import CryptContext
    print(f"Python版本: {sys.version}")

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    # 测试hash生成
    test_hash = pwd_context.hash("password123")
    print(f"测试hash成功: {test_hash[:30]}...")
    print(f"验证测试hash: {pwd_context.verify('password123', test_hash)}")

    # 生成新hash
    new_hash = pwd_context.hash("password123")
    print(f"\n新密码hash: {new_hash}")

    # 连接数据库
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='root',
        database='solararc_pro',
        charset='utf8mb4'
    )

    cursor = conn.cursor()

    # 更新所有用户的密码hash
    sql = "UPDATE users SET password_hash = %s"
    cursor.execute(sql, (new_hash,))
    conn.commit()

    print(f"\n已更新 {cursor.rowcount} 个用户的密码hash")

    # 验证更新
    cursor.execute('SELECT email, password_hash FROM users LIMIT 1')
    email, db_hash = cursor.fetchone()
    print(f'\n验证用户: {email}')
    print(f'验证密码: {pwd_context.verify("password123", db_hash)}')

    conn.close()
    print("\n✓ 密码hash更新成功！")
    print("现在请重启后端服务器，然后使用以下账户登录:")
    print("  邮箱: admin@solararc.pro")
    print("  密码: password123")

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
