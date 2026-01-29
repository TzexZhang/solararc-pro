# SolarArc Pro - Zeabur 部署配置指南

## 目录
- [一、Zeabur平台介绍](#一zeabur平台介绍)
- [二、快速开始](#二快速开始)
- [三、项目配置文件](#三项目配置文件)
- [四、环境变量配置](#四环境变量配置)
- [五、部署步骤](#五部署步骤)
- [六、域名与HTTPS](#六域名与https)
- [七、监控与维护](#七监控与维护)
- [八、常见问题](#八常见问题)
- [九、成本优化](#九成本优化)

---

## 一、Zeabur平台介绍

### 1.1 为什么选择Zeabur？

Zeabur是专为国内开发者优化的PaaS平台，具有以下优势：

| 特性 | 说明 |
|------|------|
| 🇨🇳 **国内友好** | 服务器部署在国内（阿里云、腾讯云），访问速度快 |
| 💰 **免费额度** | 每月$5免费额度，适合中小型项目 |
| 🚀 **自动部署** | 连接GitHub，代码推送自动部署 |
| 🐳 **Docker支持** | 支持Dockerfile和docker-compose.yml |
| 🗄️ **内置数据库** | 一键创建MySQL、PostgreSQL、Redis |
| 🔒 **自动HTTPS** | 自动申请和续期SSL证书 |
| 📊 **实时监控** | CPU、内存、流量实时监控 |
| 🛠️ **中文界面** | 完整中文支持 |

### 1.2 免费额度详情

| 资源 | 免费额度 | 付费扩展 |
|------|----------|----------|
| CPU | 0.2 vCPU | ¥10/月起 |
| 内存 | 256MB | ¥10/月起 |
| 存储 | 1GB | 按量计费 |
| 带宽 | 50GB/月 | ¥0.8/GB |
| MySQL | 1个实例 | ¥15/月起 |
| PostgreSQL | 1个实例 | ¥15/月起 |

**适合场景**: 个人项目、演示环境、小型MVP产品

---

## 二、快速开始

### 2.1 前置要求

- GitHub账号（用于代码托管和自动部署）
- Zeabur账号（[zeabur.com](https://zeabur.com)）
- 可选：自定义域名（如 `solararc.yourdomain.com`）

### 2.2 注册Zeabur

1. 访问 [zeabur.com](https://zeabur.com)
2. 点击右上角 "Login"
3. 选择 "Sign in with GitHub"（推荐）
4. 首次登录会自动创建账号

### 2.3 创建项目

1. 登录后进入Dashboard
2. 点击 "Create New Project"
3. 输入项目名称：`solararc-pro`
4. 选择区域：`China` (推荐国内访问)
5. 点击 "Create"

---

## 三、项目配置文件

### 3.1 项目目录结构

```
solararc-pro/
├── backend/                 # 后端服务
│   ├── Dockerfile          # Docker镜像配置
│   ├── requirements.txt    # Python依赖
│   ├── .env.example        # 环境变量模板
│   └── app/                # 应用代码
│       ├── main.py         # FastAPI入口
│       ├── api/            # API路由
│       ├── models/         # 数据模型
│       └── utils/          # 工具函数
├── frontend/               # 前端服务
│   ├── Dockerfile          # Docker镜像配置
│   ├── package.json        # Node依赖
│   ├── nginx.conf          # Nginx配置
│   ├── .env.example        # 环境变量模板
│   └── src/                # 应用代码
├── zeabur.yml             # Zeabur配置（可选）
└── README.md              # 项目说明
```

### 3.2 Zeabur配置文件 (zeabur.yml)

创建 `zeabur.yml` 文件在项目根目录：

```yaml
# Zeabur部署配置
version: 1

# 数据库配置
databases:
  - name: solararc-mysql
    type: mysql
    version: "8.0"
    # 可选：设置密码
    # password: ${MYSQL_PASSWORD}

# 服务配置
services:
  # 后端服务
  - name: backend
    type: container
    source: ./backend
    dockerfile: Dockerfile
    # 端口配置
    ports:
      - port: 8000
        type: HTTP
        # 可选：自定义域名
        domain:
          - api.solararc.zeabur.app
    # 环境变量
    env:
      - DATABASE_URL=mysql://root:${MYSQL_PASSWORD}@solararc-mysql:3306/solararc_pro
      - PYTHON_ENV=production
      - LOG_LEVEL=INFO
      - TZ=Asia/Shanghai
    # 依赖服务
    depends_on:
      - solararc-mysql
    # 资源限制（可选）
    resources:
      cpu: 0.2
      memory: 256Mi

  # 前端服务
  - name: frontend
    type: container
    source: ./frontend
    dockerfile: Dockerfile
    ports:
      - port: 80
        type: HTTP
    env:
      - VITE_API_BASE_URL=https://backend.zeabur.app/api/v1
    domains:
      - solararc.zeabur.app
    # 资源限制（可选）
    resources:
      cpu: 0.1
      memory: 128Mi
```

---

## 四、环境变量配置

### 4.1 后端环境变量

在Zeabur控制台配置以下环境变量：

#### 必需变量
```env
# 数据库连接（Zeabur自动注入）
DATABASE_URL=${MYSQL_URL}

# 应用配置
APP_NAME=SolarArc Pro
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# 时区
TZ=Asia/Shanghai
```

#### 可选变量
```env
# 数据库连接池
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=5

# CORS配置
CORS_ORIGINS=https://solararc.zeabur.app,https://www.yourdomain.com

# 高德地图API（国内使用）
AMAP_API_KEY=your_amap_api_key

# 安全密钥
SECRET_KEY=your-secret-key-change-in-production

# 文件上传
MAX_UPLOAD_SIZE=10485760  # 10MB
```

### 4.2 前端环境变量

#### 必需变量
```env
# API地址
VITE_API_BASE_URL=https://your-backend.zeabur.app/api/v1

# 应用配置
VITE_APP_NAME=SolarArc Pro
VITE_APP_VERSION=1.0.0
```

#### 可选变量
```env
# 地图配置（高德地图）
VITE_AMAP_KEY=your_amap_key
VITE_MAP_CENTER_LNG=116.397428
VITE_MAP_CENTER_LAT=39.90923
VITE_MAP_DEFAULT_ZOOM=12

# 默认城市
VITE_DEFAULT_CITY=北京
VITE_DEFAULT_CITY_CODE=110000

# 功能开关
VITE_ENABLE_ANALYSIS=true
VITE_ENABLE_EXPORT=true
VITE_ENABLE_DEBUG=false
```

---

## 五、部署步骤

### 5.1 准备代码仓库

1. 在GitHub创建仓库（如果还没有）
2. 推送代码到GitHub：
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/solararc-pro.git
git push -u origin main
```

### 5.2 部署MySQL数据库

1. 进入Zeabur项目的 "Services" 页面
2. 点击 "New Service" → "Database" → "MySQL"
3. 配置数据库：
   - Name: `solararc-mysql`
   - Version: `8.0`
4. 点击 "Deploy"
5. 等待数据库创建完成（约1-2分钟）
6. 记录数据库连接信息（在服务详情页查看）

### 5.3 部署后端服务

#### 方式1: 使用zeabur.yml（推荐）

如果已创建 `zeabur.yml` 文件：

1. 在Zeabur项目页面点击 "Import from GitHub"
2. 选择你的GitHub仓库
3. Zeabur会自动识别配置文件
4. 确认配置，点击 "Deploy"

#### 方式2: 手动配置

1. 点击 "New Service" → "Git" → 选择你的仓库
2. 配置服务：
   - Service Name: `backend`
   - Root Directory: `/backend`
   - Dockerfile Path: `Dockerfile`
3. 配置环境变量（见4.1节）
4. 点击 "Deploy"
5. 等待部署完成（首次约3-5分钟）

### 5.4 部署前端服务

重复5.3步骤，配置前端服务：
- Service Name: `frontend`
- Root Directory: `/frontend`
- Dockerfile Path: `Dockerfile`
- 环境变量（见4.2节）

### 5.5 验证部署

1. 在Zeabur控制台查看所有服务状态（应为绿色✓）
2. 访问前端域名：`https://solararc.zeabur.app`
3. 测试API：`https://backend.zeabur.app/api/v1/health`

---

## 六、域名与HTTPS

### 6.1 使用默认域名

Zeabur自动提供 `.zeabur.app` 子域名：
- 前端：`https://solararc.zeabur.app`
- 后端：`https://solararc-backend.zeabur.app`

**自动HTTPS**: Zeabur自动为所有域名申请SSL证书。

### 6.2 配置自定义域名

#### 步骤1: 添加域名

1. 进入服务设置 → "Domains"
2. 点击 "Add Domain"
3. 输入自定义域名：`solararc.yourdomain.com`
4. 点击 "Add"

#### 步骤2: 配置DNS

在你的域名注册商（如阿里云、腾讯云）添加DNS记录：

| 类型 | 名称 | 值 | TTL |
|------|------|-----|-----|
| CNAME | solararc | cname.zeabur.app | 600 |
| CNAME | api | cname.zeabur.app | 600 |

#### 步骤3: 验证DNS

等待DNS生效（通常5-30分钟）：

```bash
# 检查DNS解析
nslookup solararc.yourdomain.com

# 应返回: cname.zeabur.app
```

#### 步骤4: HTTPS证书

Zeabur会自动申请Let's Encrypt证书，通常在DNS生效后5分钟内完成。

### 6.3 国内域名备案

如果使用 `.cn` 域名或需要在大陆提供长期服务，需要进行ICP备案：

1. 在域名注册商处备案
2. 备案通过后，在Zeabur中备案
3. 提交备案号给Zeabur客服

**建议**: 初期使用 `.com` 或 `.net` 域名，无需备案。

---

## 七、监控与维护

### 7.1 实时监控

在Zeabur Dashboard可以查看：

#### 服务状态
- CPU使用率
- 内存使用量
- 磁盘占用
- 网络流量

#### 日志查看
```bash
# 使用Zeabur CLI（需要安装）
zeabur logs backend --follow
zeabur logs frontend --tail 100
```

或在Web界面查看实时日志。

### 7.2 数据库监控

MySQL数据库监控指标：
- 连接数
- 查询QPS
- 慢查询日志
- 存储空间

### 7.3 告警设置（付费功能）

免费版仅支持基础监控，付费版可配置：
- CPU/内存告警
- 服务宕机告警
- 自定义Webhook

### 7.4 数据备份

#### 自动备份
Zeabur自动每天备份MySQL数据库，保留7天。

#### 手动备份
```bash
# 通过SSH连接
zeabur ssh backend

# 导出数据库
mysqldump -h solararc-mysql -u root -p solararc_pro > backup.sql

# 下载到本地
zeabur cp backend:/app/backup.sql ./backup.sql
```

#### 恢复数据
```bash
# 上传备份文件
zeabur cp ./backup.sql backend:/app/backup.sql

# 恢复数据库
zeabur ssh backend
mysql -h solararc-mysql -u root -p solararc_pro < backup.sql
```

---

## 八、常见问题

### 8.1 部署失败

#### 问题: Docker构建失败

**症状**: 构建日志显示错误

**解决**:
1. 检查Dockerfile语法
2. 确认依赖包版本兼容
3. 查看构建日志找到具体错误

#### 问题: 内存不足导致服务重启

**症状**: 服务频繁重启，日志显示 "OOMKilled"

**解决**:
1. 减少gunicorn worker数量：
```python
# backend/Dockerfile
CMD ["gunicorn", "main:app", "--workers", "1", "--threads", "2"]
```

2. 优化Python依赖，移除不必要的包

3. 升级到付费套餐（更多内存）

### 8.2 连接问题

#### 问题: 无法连接到数据库

**症状**: API返回500错误，日志显示数据库连接失败

**解决**:
1. 确认DATABASE_URL环境变量正确
2. 检查数据库服务是否运行
3. 确认网络连接（后端和数据库在同一VPC）

#### 问题: CORS错误

**症状**: 浏览器控制台显示CORS policy错误

**解决**:
1. 在后端CORS_ORIGINS添加前端域名
2. 确认前端API地址配置正确
3. 检查后端CORS中间件配置

### 8.3 性能问题

#### 问题: API响应慢

**解决**:
1. 启用数据库查询缓存
2. 优化N+1查询问题
3. 使用Redis缓存热点数据
4. 增加gunicorn worker数量

#### 问题: 前端加载慢

**解决**:
1. 启用Nginx Gzip压缩（已配置）
2. 使用CDN加速静态资源
3. 实现代码分割（Code Splitting）
4. 懒加载非关键组件

---

## 九、成本优化

### 9.1 免费额度优化策略

| 优化项 | 策略 | 节省 |
|--------|------|------|
| **CPU** | 减少worker数量，使用异步任务 | 50% |
| **内存** | 使用gunicorn预加载，清理缓存 | 30% |
| **带宽** | 启用Gzip，使用WebP格式 | 70% |
| **数据库** | 定期清理日志表，优化查询 | 20% |

### 9.2 超出免费额度的处理

#### 警告阈值
- CPU使用率 > 80%
- 内存使用率 > 90%
- 流量 > 40GB/月

#### 处理方案

**方案1: 优化代码（推荐）**
- 优化数据库查询
- 减少不必要的API调用
- 启用客户端缓存

**方案2: 升级套餐**

| 套餐 | 配置 | 价格 | 适合 |
|------|------|------|------|
| 免费版 | 0.2 vCPU, 256MB RAM | ¥0 | 演示/测试 |
| 基础版 | 0.5 vCPU, 512MB RAM | ¥10/月 | 个人项目 |
| 标准版 | 1 vCPU, 1GB RAM | ¥30/月 | 小型应用 |
| 专业版 | 2 vCPU, 2GB RAM | ¥80/月 | 生产环境 |

### 9.3 长期成本估算

假设日活1000用户的场景：

| 项目 | 免费版 | 标准版 | 专业版 |
|------|--------|--------|--------|
| 基础费用 | ¥0 | ¥30/月 | ¥80/月 |
| 额外流量 | ¥20/月 | ¥10/月 | ¥5/月 |
| 数据库 | ¥0 | ¥15/月 | ¥15/月 |
| **合计** | **¥20/月** | **¥55/月** | **¥100/月** |

**建议**: 初期使用免费版，用户量增长后再升级。

---

## 十、进阶配置

### 10.1 使用Redis缓存

创建Redis实例：

```yaml
databases:
  - name: solararc-redis
    type: redis
    version: "7.0"
```

后端集成Redis：

```python
# backend/app/cache.py
import redis
from typing import Optional

redis_client = redis.Redis(
    host='solararc-redis',
    port=6379,
    db=0,
    decode_responses=True
)

def cache_get(key: str) -> Optional[str]:
    return redis_client.get(key)

def cache_set(key: str, value: str, ttl: int = 3600):
    redis_client.setex(key, ttl, value)
```

### 10.2 定时任务

使用Celery执行定时任务：

```python
# backend/app/tasks.py
from celery import Celery

celery_app = Celery('solararc')
celery_app.config_from_object('celeryconfig')

@celery_app.task
def calculate_daily_shadows():
    """每天凌晨2点计算所有建筑阴影"""
    # ... 计算逻辑
    pass
```

配置定时任务：

```python
# backend/celeryconfig.py
from celery.schedules import crontab

beat_schedule = {
    'calculate-daily-shadows': {
        'task': 'tasks.calculate_daily_shadows',
        'schedule': crontab(hour=2, minute=0),
    },
}
```

### 10.3 多环境部署

配置开发/测试/生产环境：

```yaml
# zeabur.prod.yml (生产环境)
databases:
  - name: solararc-mysql-prod
    type: mysql

services:
  - name: backend-prod
    env:
      - ENV=production
    domains:
      - api.solararc.com

# zeabur.dev.yml (开发环境)
databases:
  - name: solararc-mysql-dev
    type: mysql

services:
  - name: backend-dev
    env:
      - ENV=development
    domains:
      - api-dev.solararc.zeabur.app
```

---

## 十一、故障排查清单

### 11.1 部署阶段检查

- [ ] Dockerfile语法正确
- [ ] 端口配置正确（后端8000，前端80）
- [ ] 环境变量已配置
- [ ] 依赖服务（数据库）已启动
- [ ] GitHub代码已推送到main分支

### 11.2 运行阶段检查

- [ ] 服务状态正常（绿色✓）
- [ ] 日志无错误信息
- [ ] CPU/内存未超限
- [ ] 数据库连接正常
- [ ] 域名DNS解析正确

### 11.3 性能检查

- [ ] API响应时间 < 500ms
- [ ] 前端首屏加载 < 3s
- [ ] 数据库查询 < 100ms
- [ ] 带宽使用合理

---

## 十二、参考资料

### 12.1 官方文档
- [Zeabur官方文档](https://zeabur.com/docs)
- [Zeabur CLI使用指南](https://zeabur.com/docs/cli)
- [Zeabur部署最佳实践](https://zeabur.com/docs/best-practices)

### 12.2 相关技术
- [Docker官方文档](https://docs.docker.com/)
- [FastAPI部署指南](https://fastapi.tiangolo.com/deployment/)
- [Vite生产构建](https://vitejs.dev/guide/build.html)
- [Nginx配置指南](https://nginx.org/en/docs/)

### 12.3 社区资源
- [Zeabur Discord社区](https://discord.gg/zeabur)
- [GitHub讨论区](https://github.com/zeabur/discussions)
- [Stack Overflow标签](https://stackoverflow.com/questions/tagged/zeabur)

---

## 十三、联系支持

如果遇到问题：

1. **查看文档**: [Zeabur Docs](https://zeabur.com/docs)
2. **社区支持**: [Discord](https://discord.gg/zeabur)
3. **提交Issue**: [GitHub Issues](https://github.com/zeabur/zeabur/issues)
4. **邮件支持**: support@zeabur.com（付费用户）

---

**文档版本**: v1.0
**更新日期**: 2026-01-29
**维护者**: SolarArc Pro 开发团队
