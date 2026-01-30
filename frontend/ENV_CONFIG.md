# 环境变量配置说明

## 📁 配置文件

项目使用两个环境变量配置文件：

- **`.env.development`** - 开发环境配置
- **`.env.production`** - 生产环境配置

## 🚀 使用方式

### 开发环境

开发时自动使用 `.env.development` 中的配置：

```bash
npm run dev
```

### 生产环境

构建时自动使用 `.env.production` 中的配置：

```bash
npm run build
```

## 🔧 配置说明

### 已配置的密钥

- **Mapbox Access Token**: 已配置
- **高德地图 API Key**: 需要你自己配置（如果需要使用高德地图）

### 开发环境 (.env.development)

- API 地址: `http://127.0.0.1:8000/api/v1`
- 地图中心: 北京天安门
- 开发工具: 已启用

### 生产环境 (.env.production)

- API 地址: `https://api.solararc.pro/api/v1`（需要修改为实际地址）
- 地图中心: 北京天安门
- 开发工具: 已禁用

## ⚙️ 修改配置

### 修改 API 地址

**开发环境**: 编辑 `.env.development`
```bash
VITE_API_BASE_URL=http://your-api-server:8000/api/v1
```

**生产环境**: 编辑 `.env.production`
```bash
VITE_API_BASE_URL=https://your-domain.com/api/v1
```

### 配置高德地图 API Key

如果需要使用高德地图，编辑对应的 `.env.*` 文件：

```bash
VITE_AMAP_API_KEY=你的高德地图API密钥
```

获取方式：
1. 访问 https://lbs.amap.com/
2. 注册/登录
3. 创建应用 → 选择"Web端（JS API）"
4. 添加 Key → 复制密钥

## 💡 在代码中使用

```typescript
// 使用配置文件（推荐）
import { API_BASE_URL, MAP_CENTER, ENABLE_3D_BUILDINGS } from '@/config'

// 或直接使用环境变量
const apiUrl = import.meta.env.VITE_API_BASE_URL
```

## 📝 重要提示

1. **不要提交敏感信息**：.env.*.local 文件会被 .gitignore 忽略
2. **修改后需重启**：修改环境变量后需要重启开发服务器
3. **生产构建**：生产环境构建时会自动使用 .env.production 的配置
