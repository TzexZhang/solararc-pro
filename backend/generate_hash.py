"""生成正确的密码hash并更新数据库"""
from passlib.context import CryptContext
import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成新的hash
password = "password123"
new_hash = pwd_context.hash(password)
print(f"新密码hash: {new_hash}")

# 连接数据库
conn = pymysql.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "root"),
    database=os.getenv("DB_NAME", "solararc_pro"),
    charset='utf8mb4'
)

try:
    cursor = conn.cursor()

    # 更新所有用户的密码hash
    sql = "UPDATE users SET password_hash = %s"
    cursor.execute(sql, (new_hash,))
    conn.commit()

    print(f"已更新 {cursor.rowcount} 个用户的密码hash")

    # 验证更新
    cursor.execute("SELECT email FROM users")
    users = cursor.fetchall()
    print("\n用户列表:")
    for (email,) in users:
        print(f"  - {email}")

finally:
    conn.close()

print("\n现在可以使用以下账户登录:")
print("  邮箱: admin@solararc.pro")
print("  密码: password123")
