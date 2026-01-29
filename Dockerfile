# SolarArc Pro - 多阶段构建Dockerfile
# 用于构建包含后端的完整项目

# ============================================
# 阶段1: 后端构建
# ============================================
FROM python:3.10-slim as backend-builder

# 设置工作目录
WORKDIR /app/backend

# 安装系统依赖（空间计算所需）
RUN apt-get update && apt-get install -y \
    gcc \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn


# ============================================
# 阶段2: 后端运行时
# ============================================
FROM python:3.10-slim as backend-runtime

# 设置工作目录
WORKDIR /app/backend

# 创建非root用户
RUN useradd -m -u 1000 appuser

# 从builder阶段复制虚拟环境和安装的包
COPY --from=backend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# 复制应用代码
COPY backend/app ./app
COPY backend/main.py .
COPY backend/start.py .

# 设置权限
RUN chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

# 启动命令
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker"]


# ============================================
# 如果需要前端，可以取消注释以下部分
# ============================================
#
# # ============================================
# # 阶段3: 前端构建
# # ============================================
# FROM node:18-alpine as frontend-builder
#
# WORKDIR /app/frontend
#
# # 安装npm依赖（使用国内镜像加速）
# RUN npm config set registry https://registry.npmmirror.com
#
# # 复制package文件
# COPY frontend/package*.json ./
#
# # 安装依赖
# RUN npm ci
#
# # 复制源代码
# COPY frontend/ . /app/
# COPY frontend/public ./public
# COPY frontend/src ./src
# COPY frontend/vite.config.ts .
# COPY frontend/index.html .
# COPY frontend/tsconfig.json .
#
# # 构建生产版本
# RUN npm run build
#
#
# # ============================================
# # 阶段4: Nginx服务器（提供前端静态文件和代理后端API）
# # ============================================
# FROM nginx:alpine as production
#
# # 从frontend构建阶段复制构建产物
# COPY --from=frontend-builder /app/dist /usr/share/nginx/html
#
# # 复制nginx配置
# COPY deployment/nginx.conf /etc/nginx/conf.d/default.conf
#
# EXPOSE 80
#
# CMD ["nginx", "-g", "daemon off;"]
