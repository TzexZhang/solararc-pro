# 前端Dockerfile - SolarArc Pro
# 多阶段构建，优化镜像大小

# ============================================
# 构建阶段
# ============================================
FROM node:18-alpine AS builder

# 设置标签
LABEL maintainer="SolarArc Pro Team"
LABEL description="SolarArc Pro Frontend - React + Vite"

# 设置工作目录
WORKDIR /build

# 安装构建依赖
RUN apk add --no-cache git python3 make g++

# 复制依赖文件
COPY package*.json ./

# 配置npm镜像（国内加速）
RUN npm config set registry https://registry.npmmirror.com

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# ============================================
# 生产阶段 - 使用Nginx
# ============================================
FROM nginx:alpine

# 安装curl（用于健康检查）
RUN apk add --no-cache curl

# 复制构建产物
COPY --from=builder /build/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 创建非root用户
RUN addgroup -g 1001 -S nginx-app && \
    adduser -S -D -H -u 1001 -h /usr/share/nginx/html -s /sbin/nologin -G nginx-app -g nginx-app nginx-app && \
    chown -R nginx-app:nginx-app /usr/share/nginx/html && \
    chown -R nginx-app:nginx-app /var/cache/nginx && \
    chown -R nginx-app:nginx-app /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx-app:nginx-app /var/run/nginx.pid

USER nginx-app

# 暴露端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

# 启动Nginx（前台运行）
CMD ["nginx", "-g", "daemon off;"]
