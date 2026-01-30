# SolarArc Pro Frontend 部署指南

## 项目概述

SolarArc Pro 是一个高性能城市日照分析与视觉仿真平台的前端应用,基于 React 18 + TypeScript + Vite 构建。

## 技术栈

- **React 18.3** - 前端框架
- **TypeScript 5.0** - 类型系统
- **Vite 5.0** - 构建工具
- **Ant Design 5.x** - UI 组件库(桌面端)
- **Ant Design Mobile 5.x** - 移动端 UI 组件
- **Mapbox GL JS** - 地图渲染
- **Deck.gl** - 3D 数据可视化
- **ECharts** - 数据可视化图表
- **Zustand** - 状态管理
- **React Query** - 数据请求与缓存
- **React Router 6** - 路由管理
- **Axios** - HTTP 客户端
- **Day.js** - 日期处理
- **TailwindCSS** - 样式框架
- **Workbox** - PWA 支持

## 项目结构

```
frontend/
├── public/                      # 静态资源
│   └── favicon.svg
├── src/
│   ├── components/              # 通用组件(20个组件)
│   │   ├── layout/              # 布局组件(Header, Sidebar, Footer)
│   │   ├── map/                 # 地图组件(MapView, Timeline, BuildingCard)
│   │   ├── charts/              # 图表组件(Dashboard, SunlightChart)
│   │   ├── auth/                # 认证组件(LoginForm, RegisterForm)
│   │   └── mobile/              # 移动端组件(BottomNav, FAB)
│   ├── pages/                   # 页面组件(5个页面)
│   │   ├── HomePage.tsx         # 首页
│   │   ├── LoginPage.tsx        # 登录页
│   │   ├── RegisterPage.tsx     # 注册页
│   │   ├── DashboardPage.tsx    # 仪表盘
│   │   └── ReportsPage.tsx      # 报告页
│   ├── hooks/                   # 自定义 Hooks(5个)
│   │   ├── useAuth.ts           # 认证钩子
│   │   ├── useSolarPosition.ts  # 太阳位置
│   │   ├── useBuildings.ts      # 建筑数据
│   │   ├── useShadows.ts        # 阴影计算
│   │   └── useReport.ts         # 分析报告
│   ├── services/                # API 服务(5个)
│   │   ├── authService.ts       # 认证服务
│   │   ├── buildingService.ts   # 建筑服务
│   │   ├── solarService.ts      # 太阳服务
│   │   ├── shadowService.ts     # 阴影服务
│   │   └── analysisService.ts   # 分析服务
│   ├── store/                   # 状态管理(Zustand)
│   │   ├── authStore.ts         # 认证状态
│   │   ├── mapStore.ts          # 地图状态
│   │   └── appStore.ts          # 应用状态
│   ├── types/                   # TypeScript 类型(5个文件)
│   │   ├── index.ts             # 类型导出
│   │   ├── common.ts            # 通用类型
│   │   ├── auth.ts              # 认证类型
│   │   ├── building.ts          # 建筑类型
│   │   ├── analysis.ts          # 分析类型
│   │   └── map.ts               # 地图类型
│   ├── utils/                   # 工具函数(5个)
│   │   ├── request.ts           # HTTP 请求封装
│   │   ├── storage.ts           # 本地存储
│   │   ├── format.ts            # 格式化函数
│   │   ├── geo.ts               # 地理坐标转换
│   │   └── index.ts             # 工具导出
│   ├── styles/                  # 样式文件
│   │   └── global.css           # 全局样式
│   ├── App.tsx                  # 根组件
│   ├── App.css                  # 根样式
│   └── main.tsx                 # 入口文件
├── index.html                   # HTML 模板
├── package.json                 # 项目配置
├── tsconfig.json                # TypeScript 配置
├── vite.config.ts               # Vite 配置
├── tailwind.config.js           # TailwindCSS 配置
├── postcss.config.js            # PostCSS 配置
├── Dockerfile                   # Docker 配置
├── nginx.conf                   # Nginx 配置
├── .env.example                 # 环境变量示例
├── .env.local.example           # 本地环境变量示例
├── .eslintrc.json               # ESLint 配置
├── .prettierrc                  # Prettier 配置
├── .dockerignore                # Docker 忽略文件
├── .gitignore                   # Git 忽略文件
├── README.md                    # 项目说明
└── DEPLOYMENT.md                # 部署指南(本文件)

统计信息:
- TypeScript/TSX 文件: 46 个
- 组件: 20 个
- 页面: 5 个
- Hooks: 5 个
- 服务: 5 个
- Stores: 3 个
- 类型文件: 5 个
- 工具函数: 5 个
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env.local

# 编辑 .env.local,配置以下关键参数:
# - VITE_API_BASE_URL: 后端 API 地址
# - VITE_MAPBOX_TOKEN: Mapbox Token
# - VITE_AMAP_KEY: 高德地图 Key(可选)
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问: http://localhost:3000

### 4. 构建生产版本

```bash
npm run build
```

构建产物在 `dist/` 目录

### 5. 预览生产构建

```bash
npm run preview
```

## Docker 部署

### 构建镜像

```bash
docker build -t solararc-frontend:latest .
```

### 运行容器

```bash
docker run -d -p 80:80 \
  -e VITE_API_BASE_URL=https://your-backend.com/api/v1 \
  --name solararc-frontend \
  solararc-frontend:latest
```

### Docker Compose 部署

```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "80:80"
    environment:
      - VITE_API_BASE_URL=http://backend:8000/api/v1
    restart: unless-stopped
```

## 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| VITE_API_BASE_URL | 后端 API 地址 | http://localhost:8000/api/v1 |
| VITE_MAPBOX_TOKEN | Mapbox Access Token | pk.xxx |
| VITE_AMAP_KEY | 高德地图 Key | xxx |
| VITE_MAP_CENTER_LNG | 默认中心经度 | 116.397428 |
| VITE_MAP_CENTER_LAT | 默认中心纬度 | 39.90923 |
| VITE_MAP_DEFAULT_ZOOM | 默认缩放级别 | 12 |
| VITE_ENABLE_ANALYSIS | 是否启用分析功能 | true |
| VITE_ENABLE_EXPORT | 是否启用导出功能 | true |

## 性能优化

### 代码分割

- 路由级别代码分割
- 组件懒加载
- 第三方库单独打包

### 缓存策略

- React Query 缓存 API 请求
- localStorage 持久化状态
- Service Worker 离线缓存

### 资源优化

- Gzip 压缩
- 图片懒加载
- 静态资源 CDN

## PWA 支持

应用支持 PWA,可以:

- 离线访问
- 添加到主屏幕
- 接收推送通知

Service Worker 会在生产构建时自动注册。

## 浏览器支持

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90
- 移动浏览器(iOS Safari, Chrome Mobile)

## 开发指南

### 添加新页面

1. 在 `src/pages/` 创建页面组件
2. 在 `src/App.tsx` 添加路由
3. 在 Sidebar 添加导航项

### 添加新 API

1. 在 `src/types/` 定义类型
2. 在 `src/services/` 添加服务方法
3. 创建自定义 Hook(可选)

### 添加全局状态

在 `src/store/` 创建 Zustand store:

```typescript
import { create } from 'zustand'

export const useMyStore = create((set) => ({
  data: null,
  setData: (data) => set({ data })
}))
```

## 故障排查

### 1. 地图不显示

检查 Mapbox Token 配置:

```bash
# .env.local
VITE_MAPBOX_TOKEN=pk.your_token_here
```

### 2. API 请求失败

- 确认后端服务已启动
- 检查 VITE_API_BASE_URL 配置
- 查看浏览器控制台网络请求

### 3. 构建失败

清除缓存重建:

```bash
rm -rf node_modules dist .vite
npm install
npm run build
```

### 4. 样式不生效

确认 TailwindCSS 配置:

```javascript
// tailwind.config.js
content: [
  "./index.html",
  "./src/**/*.{js,ts,jsx,tsx}",
]
```

## 生产部署

### Nginx 部署

1. 构建项目: `npm run build`
2. 将 `dist/` 目录内容复制到 Nginx 根目录
3. 配置 Nginx(参考 `nginx.conf`)

### Zeabur 部署

1. 连接 GitHub 仓库
2. 选择 frontend 目录
3. 配置环境变量
4. 自动部署

### 静态托管

可部署到:
- Vercel
- Netlify
- GitHub Pages
- 阿里云 OSS + CDN

## 维护建议

1. **定期更新依赖**:
   ```bash
   npm update
   ```

2. **代码检查**:
   ```bash
   npm run lint
   ```

3. **格式化代码**:
   ```bash
   npm run format
   ```

4. **类型检查**:
   ```bash
   npx tsc --noEmit
   ```

## 技术支持

- 文档: `docs/需求设计文档.md`
- GitHub Issues: https://github.com/solararc-pro/issues
- Email: support@solararc.pro

## 许可证

MIT License
