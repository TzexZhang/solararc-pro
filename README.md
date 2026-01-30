# SolarArc Pro

> 高性能城市时空日照分析与视觉仿真平台 - 完整的前后端分离架构

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.0+-blue.svg)

## 📋 项目简介

SolarArc Pro 是一个功能完整的城市日照分析平台，包含用户认证、高精度太阳位置计算、3D建筑阴影渲染、可视化分析统计等核心功能。

### ✨ 核心功能

#### 🔐 用户认证系统
- 邮箱注册/登录
- JWT Token 认证
- 密码加密存储（bcrypt）
- 找回密码功能
- 账户安全保护

#### ☀️ 太阳位置计算
- 天文级 SPA 算法（pvlib）
- 角度秒级精度
- 支持 1900-2100 年任意日期
- 全球经纬度支持
- 日出日落时间计算

#### 🌑 3D 建筑与阴影渲染
- Shadow Volume 算法
- 复杂多边形支持
- 阴影重叠分析
- 冬至/夏至对比
- 实时阴影计算

#### 📊 可视化分析统计
- 日照统计图表（24小时曲线、月度对比）
- 太阳轨迹可视化
- 阴影热力图
- 建筑采光评分
- PDF/Excel 报告导出

#### 📱 移动端适配
- 响应式布局
- 触摸手势支持
- PWA 离线功能
- 移动端专属 UI

### 🎯 技术亮点

- **UUID 主键** - 所有表使用 VARCHAR(36) UUID
- **JWT 认证** - 无状态认证机制
- **空间索引** - MySQL 8.0 SPATIAL INDEX
- **前端缓存** - React Query + Zustand
- **PWA 支持** - Service Worker 离线缓存
- **Docker 部署** - 一键容器化部署

---

## 🏗️ 技术架构

### 后端技术栈
- **Python 3.10+** - 核心语言
- **FastAPI 0.104+** - 高性能 Web 框架
- **SQLAlchemy 2.0+** - ORM 框架（异步支持）
- **MySQL 8.0+** - 数据库（空间索引）
- **PyJWT 2.8+** - JWT 认证
- **passlib 1.7+** - 密码加密
- **pvlib 0.10+** - 太阳位置算法
- **shapely 2.0+** - 空间几何计算
- **reportlab** - PDF 报告生成
- **openpyxl** - Excel 处理

### 前端技术栈
- **React 18.3+** - UI 框架
- **TypeScript 5.0+** - 类型系统
- **Vite 5.0+** - 构建工具
- **Ant Design 5.x** - 桌面端 UI 组件
- **Ant Design Mobile** - 移动端 UI 组件
- **Mapbox GL JS / MapLibre GL** - 地图渲染
- **Deck.gl** - 3D 数据可视化
- **ECharts** - 数据可视化图表
- **Zustand** - 状态管理（轻量级）
- **React Router 6** - 路由管理
- **Axios** - HTTP 请求
- **Workbox** - PWA 支持

---

## 📁 项目结构

```
solararc-pro/
├── backend/                          # 后端服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI 应用入口
│   │   ├── config.py                # 配置管理
│   │   ├── database.py              # 数据库连接
│   │   ├── models/                  # SQLAlchemy 模型（UUID主键）
│   │   │   ├── user.py             # 用户、密码重置表
│   │   │   ├── building.py         # 建筑表
│   │   │   ├── solar_position.py   # 太阳位置预计算
│   │   │   ├── shadow_analysis.py  # 阴影缓存
│   │   │   ├── project.py          # 用户项目
│   │   │   ├── analysis_report.py  # 分析报告
│   │   │   └── building_score.py   # 建筑采光评分
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── api/                     # API 路由
│   │   │   ├── auth.py             # 认证 API（注册/登录/找回密码）
│   │   │   ├── buildings.py        # 建筑 CRUD API
│   │   │   ├── solar.py            # 太阳位置计算 API
│   │   │   ├── shadows.py          # 阴影计算 API
│   │   │   ├── analysis.py         # 日照分析 API
│   │   │   └── reports.py          # 可视化分析报告 API
│   │   ├── services/                # 业务逻辑层
│   │   │   ├── auth_service.py     # 认证服务（JWT、密码加密）
│   │   │   ├── solar_service.py    # 太阳位置计算
│   │   │   ├── shadow_service.py    # 阴影计算
│   │   │   └── report_service.py    # 报告生成服务
│   │   └── core/                    # 核心功能
│   │       ├── security.py         # JWT、密码加密
│   │       ├── deps.py             # 依赖注入
│   │       └── utils.py            # 工具函数
│   ├── tests/                      # 测试文件
│   ├── requirements.txt            # Python 依赖
│   ├── .env.example               # 环境变量模板
│   ├── Dockerfile                 # Docker 镜像
│   └── README.md
│
├── frontend/                        # 前端应用
│   ├── src/
│   │   ├── main.tsx               # 入口文件
│   │   ├── App.tsx                # 根组件
│   │   ├── pages/                 # 页面组件
│   │   │   ├── HomePage.tsx       # 首页（地图+分析）
│   │   │   ├── LoginPage.tsx      # 登录页
│   │   │   ├── RegisterPage.tsx   # 注册页
│   │   │   ├── DashboardPage.tsx  # 仪表盘页
│   │   │   └── ReportsPage.tsx    # 分析报告页
│   │   ├── components/            # 通用组件
│   │   │   ├── layout/            # 布局组件
│   │   │   ├── map/               # 地图组件
│   │   │   ├── charts/            # 图表组件
│   │   │   ├── auth/              # 认证组件
│   │   │   └── mobile/            # 移动端组件
│   │   ├── hooks/                 # 自定义 Hooks
│   │   │   ├── useAuth.ts         # 认证钩子
│   │   │   ├── useSolarPosition.ts
│   │   │   ├── useBuildings.ts
│   │   │   ├── useShadows.ts
│   │   │   └── useReport.ts
│   │   ├── services/              # API 服务
│   │   ├── store/                 # Zustand 状态管理
│   │   ├── types/                 # TypeScript 类型
│   │   └── utils/                # 工具函数
│   ├── package.json
│   ├── vite.config.ts             # Vite + PWA 配置
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── Dockerfile
│   ├── nginx.conf                 # Nginx 配置
│   └── README.md
│
├── docs/                           # 文档
│   ├── 需求设计文档.md              # 完整需求文档（v2.1）
│   └── 需求.md                     # 原始需求文档
│
├── docker-compose.yml              # Docker 编排
├── .gitignore
└── README.md                       # 本文件
```

---

## 🚀 快速开始

### 方式一：Docker 快速启动（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/solararc-pro.git
cd solararc-pro

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库密码、JWT 密钥等

# 3. 启动所有服务（MySQL + 后端 + 前端）
docker-compose up -d

# 4. 查看日志
docker-compose logs -f

# 5. 访问应用
# 前端: http://localhost
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 方式二：本地开发

#### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# Windows 激活
venv\Scripts\activate
# Linux/Mac 激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

#### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env.local
# 编辑 .env.local 文件

# 启动开发服务器
npm run dev
```

访问：http://localhost:5173

---

## 🔧 配置说明

### 后端环境变量 (backend/.env)

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://solararc_user:solararc_password@localhost:3306/solararc_pro
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=5

# API 配置
API_HOST=0.0.0.0
API_PORT=8000
APP_NAME=SolarArc Pro
DEBUG=true

# JWT 认证配置
SECRET_KEY=your-secret-key-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS 配置
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# 邮件服务（生产环境配置）
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=noreply@solararc.pro

# 高德地图（可选）
AMAP_API_KEY=your_amap_api_key
```

### 前端环境变量 (frontend/.env.local)

```env
# API 地址
VITE_API_BASE_URL=http://localhost:8000/api/v1

# 地图配置
VITE_MAP_STYLE=mapbox://styles/mapbox/streets-v11
VITE_MAP_CENTER_LNG=116.397428
VITE_MAP_CENTER_LAT=39.90923
VITE_MAP_DEFAULT_ZOOM=12

# 高德地图（国内使用）
VITE_AMAP_KEY=your_amap_key

# 默认城市
VITE_DEFAULT_CITY=北京
VITE_DEFAULT_CITY_CODE=110000

# 功能开关
VITE_ENABLE_ANALYSIS=true
VITE_ENABLE_EXPORT=true
VITE_ENABLE_PWA=true
```

---

## 📚 API 文档

后端启动后，访问以下地址查看完整的 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 核心 API 端点

#### 认证 API (`/api/v1/auth/*`)
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `GET /me` - 获取当前用户信息
- `POST /logout` - 退出登录
- `PUT /change-password` - 修改密码
- `POST /forgot-password` - 发送重置邮件
- `POST /reset-password` - 重置密码

#### 建筑 API (`/api/v1/buildings/*`)
- `GET /bbox` - 获取视野内建筑
- `GET /{id}` - 获取建筑详情
- `POST /import` - 导入建筑数据

#### 太阳位置 API (`/api/v1/solar/*`)
- `GET /position` - 计算太阳位置
- `GET /daily-positions` - 24小时太阳位置

#### 阴影 API (`/api/v1/shadows/*`)
- `POST /calculate` - 计算阴影
- `GET /compare-extremes` - 极端日期对比

#### 分析 API (`/api/v1/analysis/*`)
- `POST /point-sunlight` - 点日照分析
- `POST /shadow-overlap` - 阴影重叠分析

#### 报告 API (`/api/v1/analysis/reports/*`)
- `POST /` - 创建分析报告
- `GET /` - 报告列表
- `GET /{id}` - 报告详情
- `GET /{id}/building-scores` - 建筑评分
- `GET /{id}/export` - 导出报告
- `DELETE /{id}` - 删除报告

---

## 🗄️ 数据库设计

所有表使用 **VARCHAR(36) UUID** 作为主键：

### 核心表

1. **users** - 用户表
2. **password_resets** - 密码重置表
3. **buildings** - 建筑表（含空间数据）
4. **solar_positions_precalc** - 太阳位置预计算
5. **shadow_analysis_cache** - 阴影计算缓存
6. **projects** - 用户项目
7. **analysis_reports** - 分析报告
8. **building_scores** - 建筑采光评分
9. **user_settings** - 用户配置

详细设计请查看：[需求设计文档.md](./docs/需求设计文档.md)

---

## 📱 功能特性

### 用户认证
- ✅ 邮箱注册/登录
- ✅ JWT Token 认证
- ✅ 密码加密（bcrypt）
- ✅ 找回密码（邮件）
- ✅ 账户锁定保护

### 太阳计算
- ✅ SPA 算法（pvlib）
- ✅ 全球经纬度支持
- ✅ 1900-2100 年日期范围
- ✅ 时区处理
- ✅ 日出日落计算

### 阴影分析
- ✅ Shadow Volume 算法
- ✅ 复杂多边形支持
- ✅ 阴影重叠分析
- ✅ 冬至/夏至对比
- ✅ 空间索引优化

### 可视化
- ✅ 3D 建筑渲染
- ✅ 实时阴影显示
- ✅ 24小时时间轴
- ✅ 日照曲线图表
- ✅ 阴影热力图
- ✅ 建筑采光雷达图

### 移动端
- ✅ 响应式布局
- ✅ 触摸手势支持
- ✅ PWA 离线功能
- ✅ 移动端专属 UI

### 数据导出
- ✅ PDF 报告
- ✅ Excel 数据
- ✅ CSV 导出
- ✅ GeoJSON 数据

---

## 🎯 生产部署

### Docker 部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Zeabur 部署

详见需求设计文档第七章：部署方案

---

## 🧪 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

---

## 📄 开源协议

本项目采用 **MIT License** 开源协议。

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
- [ECharts](https://echarts.apache.org/)

---

## 📞 联系方式

- 问题反馈: [GitHub Issues](https://github.com/yourusername/solararc-pro/issues)

---

**SolarArc Pro** - 让日照分析更简单、更精准 🌞
