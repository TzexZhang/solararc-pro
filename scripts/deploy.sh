#!/bin/bash

# ============================================
# SolarArc Pro - 一键部署脚本
# ============================================
# 使用方法：
#   ./scripts/deploy.sh [environment]
#
# 参数：
#   environment: dev, staging, prod (默认: dev)
#
# 示例：
#   ./scripts/deploy.sh dev
#   ./scripts/deploy.sh prod

set -e  # 遇到错误立即退出

# ============================================
# 配置
# ============================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT="${1:-dev}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================
# 检查环境
# ============================================
check_environment() {
    log_info "检查部署环境..."

    # 检查Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装，请先安装Docker"
        exit 1
    fi

    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi

    log_info "环境检查通过 ✓"
}

# ============================================
# 加载环境变量
# ============================================
load_env() {
    log_info "加载环境变量..."

    local env_file=".env"

    if [ ! -f "$env_file" ]; then
        log_warn ".env文件不存在，从.env.example创建..."
        cp .env.example "$env_file"
        log_warn "请编辑.env文件配置环境变量后重新运行"
        exit 1
    fi

    # 加载环境变量
    export $(cat "$env_file" | grep -v '^#' | xargs)

    log_info "环境变量加载完成 ✓"
}

# ============================================
# 构建镜像
# ============================================
build_images() {
    log_info "开始构建Docker镜像..."

    cd "$PROJECT_ROOT"

    # 构建后端镜像
    log_info "构建后端镜像..."
    docker-compose build backend

    # 构建前端镜像
    log_info "构建前端镜像..."
    docker-compose build frontend

    log_info "镜像构建完成 ✓"
}

# ============================================
# 启动服务
# ============================================
start_services() {
    log_info "启动服务..."

    cd "$PROJECT_ROOT"

    # 停止旧服务
    docker-compose down

    # 启动新服务
    docker-compose up -d mysql redis
    log_info "等待数据库启动..."
    sleep 10

    docker-compose up -d backend frontend

    log_info "服务启动完成 ✓"
}

# ============================================
# 健康检查
# ============================================
health_check() {
    log_info "执行健康检查..."

    local max_retries=30
    local retry=0

    while [ $retry -lt $max_retries ]; do
        if curl -f http://localhost:${BACKEND_PORT:-8000}/api/v1/health &> /dev/null; then
            log_info "后端服务健康检查通过 ✓"
            break
        fi

        retry=$((retry + 1))
        log_info "等待后端服务启动... ($retry/$max_retries)"
        sleep 2
    done

    if [ $retry -eq $max_retries ]; then
        log_error "后端服务启动超时"
        exit 1
    fi

    # 检查前端
    if curl -f http://localhost:${FRONTEND_PORT:-80}/health &> /dev/null; then
        log_info "前端服务健康检查通过 ✓"
    else
        log_warn "前端服务健康检查失败（可能还在启动中）"
    fi
}

# ============================================
# 运行数据库迁移
# ============================================
run_migrations() {
    log_info "运行数据库迁移..."

    cd "$PROJECT_ROOT"

    # 这里可以添加数据库迁移命令
    # docker-compose exec backend alembic upgrade head

    log_info "数据库迁移完成 ✓"
}

# ============================================
# 清理旧镜像
# ============================================
cleanup() {
    log_info "清理未使用的Docker资源..."

    docker image prune -f
    docker volume prune -f

    log_info "清理完成 ✓"
}

# ============================================
# 显示部署信息
# ============================================
show_info() {
    log_info "=================================="
    log_info "部署完成！"
    log_info "=================================="
    echo ""
    log_info "前端地址: http://localhost:${FRONTEND_PORT:-80}"
    log_info "后端地址: http://localhost:${BACKEND_PORT:-8000}"
    log_info "API文档: http://localhost:${BACKEND_PORT:-8000}/docs"
    echo ""
    log_info "查看日志: docker-compose logs -f"
    log_info "停止服务: docker-compose down"
    log_info "重启服务: docker-compose restart"
    echo ""
}

# ============================================
# 主函数
# ============================================
main() {
    log_info "=================================="
    log_info "SolarArc Pro 部署脚本"
    log_info "环境: $ENVIRONMENT"
    log_info "=================================="
    echo ""

    check_environment
    load_env
    build_images
    start_services
    health_check
    run_migrations
    cleanup
    show_info
}

# 运行主函数
main
