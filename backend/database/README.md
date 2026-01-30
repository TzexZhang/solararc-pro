# SolarArc Pro 数据库脚本使用说明

## Windows 系统使用方法

### 方式一：使用批处理脚本（.bat）- 推荐给Windows用户

#### 1. 初始化数据库
双击运行 `init_db.bat` 或在命令行中执行：
```cmd
init_db.bat
```

**功能：**
- 检查MySQL连接
- 自动创建数据库（如果不存在）
- 创建所有数据库表结构

**环境变量配置（可选）：**
```cmd
set DB_HOST=localhost
set DB_PORT=3306
set DB_USER=root
set DB_PASSWORD=your_password
set DB_NAME=solararc_pro
```

#### 2. 插入Demo数据
数据库初始化完成后，双击运行 `seed_db.bat`：
```cmd
seed_db.bat
```

**功能：**
- 插入3个测试用户（admin/demo/test，密码：password123）
- 插入8个示例建筑（北京朝阳区）
- 插入2个示例项目
- 插入太阳位置数据
- 插入示例分析报告

#### 3. 启动后端服务
在 `backend` 目录下双击运行 `start.bat`：
```cmd
start.bat
```

**功能：**
- 自动创建虚拟环境（如果不存在）
- 安装依赖包
- 检查配置文件
- 启动FastAPI服务器

#### 4. 一键启动（推荐）
在 `backend` 目录下双击运行 `setup.bat`：
```cmd
setup.bat
```

**功能：**
- 自动执行数据库初始化
- 自动插入demo数据
- 自动启动后端服务

---

### 方式二：使用Python脚本

#### 1. 初始化数据库
```cmd
cd database
python init_db.py --yes
```

**命令行参数：**
- `--host`: MySQL主机地址（默认：localhost）
- `--port`: MySQL端口（默认：3306）
- `--user`: MySQL用户名（默认：root）
- `--password`: MySQL密码
- `--database`: 数据库名称（默认：solararc_pro）
- `--yes, -y`: 跳过确认提示

**示例：**
```cmd
python init_db.py --host localhost --port 3306 --user root --password your_password --yes
```

#### 2. 插入Demo数据
```cmd
python seed_db.py --yes
```

**命令行参数：**
- 同 `init_db.py`

---

## Demo 用户信息

数据库初始化后会创建以下测试用户：

| 邮箱 | 密码 | 角色 |
|------|------|------|
| admin@solararc.pro | password123 | 管理员 |
| demo@solararc.pro | password123 | 演示用户 |
| test@solararc.pro | password123 | 测试用户 |

---

## 环境要求

### 必需软件
- Python 3.8+
- MySQL 8.0+
- pip（Python包管理器）

### MySQL配置
确保MySQL服务已启动，并且：
- 端口可访问（默认3306）
- 用户有创建数据库和表的权限
- 支持utf8mb4字符集

---

## 常见问题

### 1. MySQL命令未找到
**错误：** `mysql 命令未找到`

**解决方法：**
- 将MySQL安装路径添加到系统PATH环境变量
- 例如：`C:\Program Files\MySQL\MySQL Server 8.0\bin`

### 2. 字符编码错误
**错误：** `Incorrect string value` 或中文乱码

**解决方法：**
- 脚本已自动添加 `--default-character-set=utf8mb4` 参数
- 确保MySQL配置支持utf8mb4

### 3. 数据库连接失败
**错误：** `Can't connect to MySQL server`

**解决方法：**
- 检查MySQL服务是否启动
- 验证用户名和密码
- 确认端口号正确

---

## 文件说明

### 批处理脚本（Windows）
- `init_db.bat` - 数据库初始化脚本
- `seed_db.bat` - Demo数据插入脚本
- `start.bat` - 后端启动脚本（位于backend目录）
- `setup.bat` - 一键启动脚本（位于backend目录）

### Python脚本（跨平台）
- `init_db.py` - 数据库初始化脚本
- `seed_db.py` - Demo数据插入脚本
- `start.py` - 后端启动脚本（位于backend目录）

### SQL文件
- `01_init_tables.sql` - 数据库表结构定义
- `02_seed_data.sql` - Demo数据插入语句

---

## 验证安装

### 1. 检查数据库表
```sql
USE solararc_pro;
SHOW TABLES;
```

应该显示9个表：
- users
- password_resets
- buildings
- solar_positions_precalc
- shadow_analysis_cache
- projects
- analysis_reports
- building_scores
- user_settings

### 2. 检查Demo数据
```sql
SELECT COUNT(*) FROM users;  -- 应该返回3
SELECT COUNT(*) FROM buildings;  -- 应该返回8
SELECT COUNT(*) FROM projects;  -- 应该返回2
```

### 3. 访问API文档
启动后端后，访问：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- 健康检查: http://localhost:8000/health

---

## 下一步

数据库初始化完成后：

1. **配置后端环境变量**
   - 编辑 `backend/.env` 文件
   - 设置数据库连接信息

2. **启动后端服务**
   ```cmd
   cd ..
   start.bat
   ```

3. **测试API**
   - 访问 http://localhost:8000/api/docs
   - 使用demo用户登录测试

---

## 技术支持

如遇问题，请检查：
1. Python和MySQL版本是否符合要求
2. MySQL服务是否正常运行
3. 环境变量配置是否正确
4. 防火墙是否允许连接

更多问题请参考项目主文档。
