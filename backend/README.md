# SolarArc Pro Backend

高性能城市时空日照分析与视觉仿真平台 - FastAPI 后端服务

## 技术栈

- **Python 3.10+**
- **FastAPI 0.104+** - 高性能 Web 框架
- **SQLAlchemy 2.0+** - ORM
- **MySQL 8.0+** - 数据库
- **pvlib** - 太阳位置计算
- **shapely** - 空间几何计算
- **JWT** - 用户认证

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models/                 # SQLAlchemy 模型
│   ├── schemas/                # Pydantic schemas
│   ├── api/                    # API 路由
│   ├── services/               # 业务逻辑层
│   └── core/                   # 核心功能（JWT、密码加密等）
├── tests/                      # 测试
├── requirements.txt
├── Dockerfile
└── .env.example
```

## 快速开始

### 1. 环境要求

- Python 3.10+
- MySQL 8.0+
- pip

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 到 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接等：

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/solararc_pro
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

### 4. 初始化数据库

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE solararc_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 启动应用（会自动创建表）
uvicorn app.main:app --reload --port 8000
```

### 5. 访问 API 文档

启动后访问以下地址：

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## API 端点

### 认证相关 (`/api/v1/auth`)

- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `GET /me` - 获取当前用户信息
- `POST /logout` - 用户登出
- `PUT /change-password` - 修改密码
- `POST /forgot-password` - 请求密码重置
- `POST /reset-password` - 重置密码

### 建筑数据 (`/api/v1/buildings`)

- `GET /bbox` - 获取视野内的建筑列表
- `GET /{building_id}` - 获取单个建筑详情
- `POST /import` - 导入建筑数据
- `DELETE /{building_id}` - 删除建筑

### 太阳位置计算 (`/api/v1/solar`)

- `GET /position` - 计算太阳位置
- `GET /daily-positions` - 获取24小时太阳位置

### 阴影计算 (`/api/v1/shadows`)

- `POST /calculate` - 计算建筑阴影
- `POST /overlap` - 阴影重叠分析
- `GET /compare-extremes` - 冬夏至阴影对比

### 日照分析 (`/api/v1/analysis`)

- `POST /point-sunlight` - 点日照分析
- `POST /shadow-overlap` - 阴影重叠分析

### 分析报告 (`/api/v1/analysis/reports`)

- `POST /` - 创建分析报告
- `GET /` - 获取报告列表
- `GET /{report_id}` - 获取报告详情
- `GET /{report_id}/building-scores` - 获取建筑采光评分
- `GET /{report_id}/export` - 导出报告
- `DELETE /{report_id}` - 删除报告

## 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行测试
pytest tests/

# 运行特定测试
pytest tests/test_auth.py
pytest tests/test_solar.py
pytest tests/test_buildings.py
```

## Docker 部署

### 构建镜像

```bash
docker build -t solararc-backend .
```

### 运行容器

```bash
docker run -d \
  --name solararc-backend \
  -p 8000:8000 \
  -e DATABASE_URL=mysql+pymysql://root:password@host.docker.internal:3306/solararc_pro \
  -e SECRET_KEY=your-secret-key \
  solararc-backend
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://root:password@db:3306/solararc_pro
      - SECRET_KEY=your-secret-key
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=solararc_pro
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 生产环境部署

### 使用 Gunicorn

```bash
gunicorn app.main:app \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name api.solararc.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 开发指南

### 添加新的 API 端点

1. 在 `app/api/` 下创建新的路由文件
2. 在 `app/schemas/` 下定义 Pydantic schemas
3. 在 `app/services/` 下实现业务逻辑
4. 在 `app/main.py` 中注册路由

### 数据库迁移

```bash
# 使用 Alembic 进行数据库迁移
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | 数据库连接 URL | mysql+pymysql://root:password@localhost:3306/solararc_pro |
| `SECRET_KEY` | JWT 密钥 | - |
| `API_HOST` | API 监听地址 | 0.0.0.0 |
| `API_PORT` | API 监听端口 | 8000 |
| `CORS_ORIGINS` | 允许的 CORS 源 | http://localhost:5173 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 过期时间（分钟） | 10080 (7天) |

## 常见问题

### 1. 数据库连接失败

检查数据库是否启动，以及 `DATABASE_URL` 是否正确。

### 2. CORS 错误

在 `.env` 文件中添加前端域名到 `CORS_ORIGINS`。

### 3. pvlib 安装失败

确保安装了所需的系统依赖：

```bash
sudo apt-get install -y gcc libgeos-dev libproj-dev
```

## License

MIT License

## 联系方式

- 项目主页: [SolarArc Pro](https://github.com/yourusername/solararc-pro)
- 问题反馈: [Issues](https://github.com/yourusername/solararc-pro/issues)
