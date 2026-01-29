# SolarArc Pro

> 高性能城市时空日照分析与视觉仿真平台

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

## 📋 项目简介

SolarArc Pro 是一个为城市规划师、建筑师和开发商设计的高精度日照分析工具。通过科学算法计算建筑阴影、评估采光权，为城市建设决策提供数据支持。

### ✨ 核心功能

- ☀️ **高精度太阳位置计算** - 使用pvlib库，误差控制在角度秒级
- 🌑 **实时阴影计算** - Shadow Volume算法，支持复杂建筑形状
- 📊 **日照分析** - 有效日照时长统计、阴影重叠分析
- 🗺️ **多坐标系支持** - WGS84/GCJ-02/BD09相互转换
- 🎨 **3D可视化** - 基于Mapbox GL JS + Deck.gl的高性能渲染
- 📅 **时间轴动画** - 24小时日照变化动画演示
- 🇨🇳 **国内优化** - 高德地图、中国时区、中文界面

### 🎯 适用场景

- 城市规划日照评估
- 建筑设计采光分析
- 房地产开发可行性研究
- 采光权纠纷分析
- 科研教学演示

---

## 🏗️ 技术栈

### 后端
- **Python 3.10+** - 核心语言
- **FastAPI** - 高性能Web框架
- **MySQL 8.0** - 关系型数据库（空间索引）
- **pvlib** - 太阳位置算法库
- **Shapely** - 空间几何计算
- **SQLAlchemy** - ORM框架

### 前端
- **React 18** - UI框架
- **TypeScript** - 类型系统
- **Vite** - 构建工具
- **Mapbox GL JS** - 地图渲染
- **Deck.gl** - 3D数据可视化
- **Zustand** - 状态管理
- **Ant Design** - UI组件库

### 部署
- **Zeabur** - 推荐部署平台（国内访问快）
- **Docker** - 容器化部署
- **GitHub Actions** - CI/CD自动化

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+ (或使用Zeabur托管数据库)
- Git

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/solararc-pro.git
cd solararc-pro
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库等信息

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

后端API文档: http://localhost:8000/docs

### 3. 前端设置

```bash
# 新开一个终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env.local
# 编辑.env.local文件，配置API地址等

# 启动开发服务器
npm run dev
```

前端地址: http://localhost:5173

### 4. 使用Docker快速启动

```bash
# 配置环境变量
cp .env.example .env
# 编辑.env文件

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 📦 部署到Zeabur

Zeabur是国内访问速度最快的PaaS平台之一，完全支持本项目。

### 快速部署

1. **注册Zeabur**
   - 访问 [zeabur.com](https://zeabur.com)
   - 使用GitHub登录

2. **创建项目**
   - 点击 "New Project"
   - 选择 "Import from GitHub"
   - 选择你的仓库

3. **配置服务**
   - Zeabur会自动识别 `zeabur.yml` 配置
   - 配置环境变量（数据库连接、API密钥等）
   - 部署MySQL数据库
   - 部署后端服务
   - 部署前端服务

4. **访问应用**
   - 前端: `https://your-project.zeabur.app`
   - 后端: `https://your-backend.zeabur.app`

详细部署指南请查看: [Zeabur部署配置指南.md](./docs/Zeabur部署配置指南.md)

---

## 📖 项目结构

```
solararc-pro/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic Schema
│   │   ├── services/       # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   └── main.py         # 应用入口
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── services/       # API服务
│   │   ├── store/          # 状态管理
│   │   ├── router/         # 路由配置
│   │   └── main.tsx        # 应用入口
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── docs/                   # 文档
│   ├── 需求设计文档.md
│   ├── Zeabur部署配置指南.md
│   └── 配置文件说明.md
│
├── scripts/                # 脚本
│   └── deploy.sh
│
├── docker-compose.yml      # Docker编排
├── zeabur.yml             # Zeabur配置
└── README.md
```

---

## 🔧 配置说明

### 环境变量

#### 后端环境变量 (`backend/.env`)
```env
# 数据库
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/solararc_pro

# API配置
APP_NAME=SolarArc Pro
APP_ENV=development
DEBUG=false
LOG_LEVEL=INFO

# 地图API
AMAP_API_KEY=your_amap_api_key

# 安全
SECRET_KEY=your-secret-key-change-in-production
```

#### 前端环境变量 (`frontend/.env.local`)
```env
# API地址
VITE_API_BASE_URL=http://localhost:8000/api/v1

# 高德地图
VITE_AMAP_KEY=your_amap_key
VITE_MAP_CENTER_LNG=116.397428
VITE_MAP_CENTER_LAT=39.90923

# 默认城市
VITE_DEFAULT_CITY=北京
```

### 获取高德地图API Key

1. 访问 [高德开放平台](https://console.amap.com/dev/key/app)
2. 注册并登录
3. 创建应用，选择 "Web端(JS API)"
4. 获取Key并配置到环境变量

---

## 📚 API文档

后端API文档自动生成，访问以下地址查看：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要API端点

#### 建筑数据
- `GET /api/v1/buildings/` - 获取建筑列表
- `GET /api/v1/buildings/{id}` - 获取建筑详情
- `POST /api/v1/buildings/` - 创建建筑
- `POST /api/v1/buildings/import` - 导入建筑数据

#### 太阳位置
- `GET /api/v1/solar/position` - 计算太阳位置
- `GET /api/v1/solar/daily-positions` - 获取24小时太阳位置
- `GET /api/v1/solar/sunrise-sunset` - 获取日出日落时间

#### 阴影计算
- `POST /api/v1/shadows/calculate` - 计算建筑阴影
- `GET /api/v1/shadows/compare-extremes` - 对比极端日期阴影
- `GET /api/v1/shadows/animation` - 获取阴影动画数据

#### 日照分析
- `POST /api/v1/analysis/point-sunlight` - 点日照分析
- `POST /api/v1/analysis/shadow-overlap` - 阴影重叠分析

#### 坐标转换
- `POST /api/v1/coords/transform` - 坐标转换
- `GET /api/v1/coords/detect/{lat}/{lng}` - 检测坐标系

---

## 🛠️ 开发指南

### 后端开发

```bash
# 运行测试
cd backend
pytest

# 代码格式化
black app/
flake8 app/

# 类型检查
mypy app/
```

### 前端开发

```bash
# 代码检查
cd frontend
npm run lint

# 类型检查
npm run type-check

# 构建生产版本
npm run build
```

### 数据库迁移

```bash
cd backend

# 创建迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

---

## 📈 性能优化

### 后端优化
- 使用数据库连接池
- 空间索引加速查询
- Redis缓存热点数据
- 异步任务处理

### 前端优化
- 代码分割（Code Splitting）
- 组件懒加载
- 图像压缩和WebP格式
- CDN加速静态资源

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 📞 联系方式

- 项目主页: [https://github.com/yourusername/solararc-pro](https://github.com/yourusername/solararc-pro)
- 问题反馈: [GitHub Issues](https://github.com/yourusername/solararc-pro/issues)
- 邮箱: support@solararc.pro

---

## 🙏 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com/)
- [pvlib](https://pvlib-python.readthedocs.io/)
- [Shapely](https://shapely.readthedocs.io/)
- [React](https://react.dev/)
- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js)
- [Deck.gl](https://deck.gl/)
- [Ant Design](https://ant.design/)
- [Zeabur](https://zeabur.com/)

---

## 📝 更新日志

### v1.0.0 (2026-01-29)
- ✨ 初始版本发布
- ☀️ 太阳位置计算功能
- 🌑 阴影计算功能
- 📊 日照分析功能
- 🗺️ 3D地图可视化
- 🇨🇳 国内地图支持

---

**SolarArc Pro** - 让日照分析更简单、更精准 🌞
