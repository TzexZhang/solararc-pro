"""测试密码hash是否正确"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 数据库中的hash
db_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkJbK3OpfbGC7Q.CjZXIoQKEBjTbN6c9yNU9q0C5q9HqW8"

# 测试密码
test_passwords = ["password123", "admin", "123456"]

print("测试数据库中的密码hash:")
for pwd in test_passwords:
    try:
        result = pwd_context.verify(pwd, db_hash)
        print(f"  密码: '{pwd}' -> {result}")
    except Exception as e:
        print(f"  密码: '{pwd}' -> 错误: {e}")

# 生成新的hash
print("\n生成新的hash:")
new_hash = pwd_context.hash("password123")
print(f"  password123 -> {new_hash}")
