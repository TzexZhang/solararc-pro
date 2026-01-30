# SolarArc Pro - Frontend

高性能城市日照分析与视觉仿真平台 - 前端应用

## 技术栈

- **框架**: React 18.3 + TypeScript 5.0
- **构建工具**: Vite 5.0
- **UI 组件库**:
  - Ant Design 5.x (桌面端)
  - Ant Design Mobile 5.x (移动端)
- **地图与可视化**:
  - Mapbox GL JS v3
  - Deck.gl (3D 数据可视化)
  - ECharts (图表)
- **状态管理**: Zustand 4.x
- **路由**: React Router 6
- **HTTP 请求**: Axios + React Query
- **工具库**:
  - Day.js (日期处理)
  - Lodash-es (工具函数)
- **PWA**: Workbox

## 目录结构

```
frontend/
├── public/                      # 静态资源
├── src/
│   ├── main.tsx                 # 应用入口
│   ├── App.tsx                  # 根组件
│   ├── pages/                   # 页面组件
│   │   ├── HomePage.tsx         # 首页（地图+分析）
│   │   ├── LoginPage.tsx        # 登录页
│   │   ├── RegisterPage.tsx     # 注册页
│   │   ├── DashboardPage.tsx    # 仪表盘页
│   │   └── ReportsPage.tsx      # 分析报告页
│   ├── components/              # 通用组件
│   │   ├── layout/              # 布局组件
│   │   ├── map/                 # 地图相关组件
│   │   ├── charts/              # 图表组件
│   │   ├── auth/                # 认证组件
│   │   └── mobile/              # 移动端组件
│   ├── hooks/                   # 自定义 Hooks
│   ├── services/                # API 服务
│   ├── store/                   # 状态管理 (Zustand)
│   ├── types/                   # TypeScript 类型定义
│   ├── utils/                   # 工具函数
│   └── styles/                  # 全局样式
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── Dockerfile
└── nginx.conf
```

## 快速开始

### 环境要求

- Node.js >= 18.0.0
- npm >= 9.0.0

### 安装依赖

```bash
npm install
```

### 配置环境变量

复制 `.env.example` 到 `.env.local` 并配置：

```env
# API 配置
VITE_API_BASE_URL=http://localhost:8000/api/v1

# 地图配置
VITE_MAPBOX_TOKEN=your_mapbox_token_here
VITE_AMAP_KEY=your_amap_key_here

# 其他配置...
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## Docker 部署

### 构建镜像

```bash
docker build -t solararc-frontend .
```

### 运行容器

```bash
docker run -p 80:80 solararc-frontend
```

### 使用 Docker Compose

```bash
docker-compose up -d
```

## 主要功能

### 1. 用户认证
- 邮箱注册/登录
- 密码找回
- JWT Token 认证

### 2. 地图可视化
- 3D 建筑渲染
- 实时阴影显示
- 时间轴控制
- 视图模式切换

### 3. 日照分析
- 太阳位置计算
- 阴影分析
- 有效日照时长统计
- 建筑采光评估

### 4. 数据导出
- PDF 报告导出
- Excel 数据导出
- CSV 格式导出

### 5. 移动端适配
- 响应式布局
- 触摸手势支持
- PWA 离线功能

## 开发指南

### 状态管理

使用 Zustand 进行全局状态管理：

```typescript
import { useAuthStore } from '@/store'

const { user, login, logout } = useAuthStore()
```

### API 请求

使用封装的 HTTP 客户端：

```typescript
import { http } from '@/utils/request'

const data = await http.get('/api/endpoint')
```

### 自定义 Hooks

```typescript
import { useSolarPosition } from '@/hooks'

const { data, isLoading } = useSolarPosition()
```

### 路由

```typescript
import { useNavigate } from 'react-router-dom'

const navigate = useNavigate()
navigate('/path')
```

## 浏览器支持

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## 性能优化

- 代码分割 (React.lazy + Suspense)
- 组件懒加载
- 图片懒加载
- API 请求缓存 (React Query)
- Gzip 压缩
- 静态资源缓存

## PWA 支持

应用支持 PWA，可以：
- 离线访问
- 添加到主屏幕
- 接收推送通知

## 常见问题

### 1. 地图不显示

检查 Mapbox Token 是否正确配置：

```env
VITE_MAPBOX_TOKEN=pk.your_token_here
```

### 2. API 请求失败

确保后端服务已启动，并检查 `.env.local` 中的 API 地址配置。

### 3. 构建失败

清除缓存后重新构建：

```bash
rm -rf node_modules dist
npm install
npm run build
```

## 许可证

MIT License

## 联系方式

- GitHub: https://github.com/solararc-pro
- Email: support@solararc.pro
