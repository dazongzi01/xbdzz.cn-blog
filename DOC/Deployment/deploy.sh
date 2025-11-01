#!/bin/bash

###############################################################################
# VitePress 文档编译和部署脚本
# 功能：编译 Markdown 文档 → 生成静态站点 → 打包部署文件
#
# 使用方法：
#   1. 基本编译：./deploy.sh build
#   2. 编译并显示统计：./deploy.sh build --stats
#   3. 打包部署文件：./deploy.sh package
#   4. 完整流程（编译+打包）：./deploy.sh all
#   5. 清理构建文件：./deploy.sh clean
#   6. 编译 + 打包 + 上传：./deploy.sh deploy [server] [path]
#      示例：./deploy.sh deploy user@example.com /var/www/html
#
###############################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="${SCRIPT_DIR}/docs"
DIST_DIR="${DOCS_DIR}/.vitepress/dist"
DEPLOY_DIR="${SCRIPT_DIR}/deploy"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PACKAGE_NAME="vitepress-dist_${TIMESTAMP}.tar.gz"
PACKAGE_PATH="${DEPLOY_DIR}/${PACKAGE_NAME}"

# 打印函数
print_header() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    $1"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_section() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 检查环境
check_environment() {
    print_section "检查环境"

    if ! command -v node &> /dev/null; then
        print_error "Node.js 未安装"
        exit 1
    fi
    print_success "Node.js $(node --version)"

    if ! command -v npm &> /dev/null; then
        print_error "npm 未安装"
        exit 1
    fi
    print_success "npm $(npm --version)"

    if [ ! -f "${SCRIPT_DIR}/package.json" ]; then
        print_error "找不到 package.json"
        exit 1
    fi
    print_success "package.json 存在"

    if [ ! -d "${DOCS_DIR}" ]; then
        print_error "找不到 docs 目录"
        exit 1
    fi
    print_success "docs 目录存在"
    echo ""
}

# 编译文档
build_docs() {
    print_section "编译 VitePress 文档"

    if [ -d "${DIST_DIR}" ]; then
        print_info "清理旧的构建文件..."
        rm -rf "${DIST_DIR}"
    fi

    cd "${SCRIPT_DIR}"

    print_info "运行 npm run build:force..."
    if npm run build:force; then
        print_success "编译完成"
    else
        print_error "编译失败"
        exit 1
    fi
    echo ""
}

# 显示编译统计
show_stats() {
    print_section "编译统计"

    if [ ! -d "${DIST_DIR}" ]; then
        print_error "找不到构建目录: ${DIST_DIR}"
        return 1
    fi

    # 计算文件统计
    HTML_COUNT=$(find "${DIST_DIR}" -name "*.html" 2>/dev/null | wc -l)
    JS_COUNT=$(find "${DIST_DIR}" -name "*.js" 2>/dev/null | wc -l)
    CSS_COUNT=$(find "${DIST_DIR}" -name "*.css" 2>/dev/null | wc -l)
    IMG_COUNT=$(find "${DIST_DIR}" \( -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.svg" \) 2>/dev/null | wc -l)
    TOTAL_SIZE=$(du -sh "${DIST_DIR}" 2>/dev/null | cut -f1)
    TOTAL_FILES=$(find "${DIST_DIR}" -type f 2>/dev/null | wc -l)

    echo -e "${YELLOW}📊 文件统计：${NC}"
    echo "  HTML 文件:  ${HTML_COUNT}"
    echo "  JavaScript: ${JS_COUNT}"
    echo "  CSS 文件:   ${CSS_COUNT}"
    echo "   图片文件:   ${IMG_COUNT}"
    echo "   总文件数:   ${TOTAL_FILES}"
    echo ""
    echo -e "${YELLOW}📈 大小统计：${NC}"
    echo "  总大小:     ${TOTAL_SIZE}"
    echo ""
    echo -e "${YELLOW}📁 构建目录：${NC}"
    echo "  ${DIST_DIR}"
    echo ""
}

# 打包部署文件
package_dist() {
    print_section "打包部署文件"

    if [ ! -d "${DIST_DIR}" ]; then
        print_error "找不到构建目录，请先运行编译"
        exit 1
    fi

    # 创建 deploy 目录
    mkdir -p "${DEPLOY_DIR}"

    # 保留最近5个包
    print_info "清理旧的部署包（保留最近5个）..."
    ls -t "${DEPLOY_DIR}"/vitepress-dist_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm

    # 打包
    print_info "创建部署包: ${PACKAGE_NAME}"
    cd "${DOCS_DIR}/.vitepress"
    tar -czf "${PACKAGE_PATH}" dist/

    if [ -f "${PACKAGE_PATH}" ]; then
        PACKAGE_SIZE=$(du -h "${PACKAGE_PATH}" | cut -f1)
        print_success "打包完成"
        echo ""
        echo -e "${YELLOW}📦 部署包信息：${NC}"
        echo "  文件名: ${PACKAGE_NAME}"
        echo "  大小:   ${PACKAGE_SIZE}"
        echo "  路径:   ${PACKAGE_PATH}"
        echo ""
    else
        print_error "打包失败"
        exit 1
    fi
}

# 上传到服务器
upload_to_server() {
    local SERVER=$1
    local REMOTE_PATH=$2

    if [ -z "${SERVER}" ] || [ -z "${REMOTE_PATH}" ]; then
        print_error "服务器地址和路径不能为空"
        echo "使用方法: ./deploy.sh deploy user@server.com /var/www/html"
        exit 1
    fi

    print_section "上传到服务器"

    if [ ! -f "${PACKAGE_PATH}" ]; then
        print_error "找不到部署包，请先运行打包"
        exit 1
    fi

    print_info "上传包到服务器..."
    print_info "服务器: ${SERVER}"
    print_info "目标路径: ${REMOTE_PATH}"
    echo ""

    if scp "${PACKAGE_PATH}" "${SERVER}:${REMOTE_PATH}/${PACKAGE_NAME}"; then
        print_success "上传完成"
        echo ""

        echo -e "${YELLOW}📝 部署到服务器的步骤：${NC}"
        echo ""
        echo "1. 登录服务器:"
        echo "   ssh ${SERVER}"
        echo ""
        echo "2. 进入目标目录:"
        echo "   cd ${REMOTE_PATH}"
        echo ""
        echo "3. 解压部署包:"
        echo "   tar -xzf ${PACKAGE_NAME}"
        echo ""
        echo "4. （可选）备份旧版本:"
        echo "   mv dist dist.backup"
        echo ""
        echo "5. 移动新版本到位置:"
        echo "   mv dist /* ."
        echo ""
        echo "6. 清理临时文件:"
        echo "   rm ${PACKAGE_NAME}"
        echo ""
    else
        print_error "上传失败，请检查网络和权限"
        exit 1
    fi
}

# 清理构建文件
clean_build() {
    print_section "清理构建文件"

    if [ -d "${DIST_DIR}" ]; then
        print_info "删除构建目录: ${DIST_DIR}"
        rm -rf "${DIST_DIR}"
        print_success "构建目录已删除"
    fi

    if [ -d "${DEPLOY_DIR}" ]; then
        read -p "是否删除 deploy 目录中的所有包? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "${DEPLOY_DIR}"
            print_success "deploy 目录已删除"
        fi
    fi
    echo ""
}

# 显示帮助
show_help() {
    echo -e "${CYAN}VitePress 文档编译和部署脚本${NC}"
    echo ""
    echo "使用方法："
    echo "  ./deploy.sh <command> [options]"
    echo ""
    echo "命令："
    echo "  build              编译文档"
    echo "  build --stats      编译并显示统计信息"
    echo "  package            打包部署文件"
    echo "  all                编译 + 打包"
    echo "  deploy <server> <path>"
    echo "                     编译 + 打包 + 上传到服务器"
    echo "  clean              清理构建文件"
    echo "  help               显示此帮助信息"
    echo ""
    echo "示例："
    echo "  # 基本编译"
    echo "  ./deploy.sh build"
    echo ""
    echo "  # 编译并显示统计"
    echo "  ./deploy.sh build --stats"
    echo ""
    echo "  # 完整流程"
    echo "  ./deploy.sh all"
    echo ""
    echo "  # 上传到服务器"
    echo "  ./deploy.sh deploy user@example.com /var/www/html"
    echo ""
}

# 主程序
main() {
    local COMMAND=${1:-help}

    case "${COMMAND}" in
        build)
            check_environment
            build_docs
            if [ "${2:-}" = "--stats" ]; then
                show_stats
            fi
            print_header "编译完成！"
            echo -e "${YELLOW}构建目录：${NC} ${DIST_DIR}"
            echo ""
            ;;
        package)
            check_environment
            package_dist
            print_header "打包完成！"
            echo ""
            ;;
        all)
            check_environment
            build_docs
            show_stats
            package_dist
            print_header "编译和打包完成！"
            echo ""
            ;;
        deploy)
            check_environment
            build_docs
            show_stats
            package_dist
            upload_to_server "$2" "$3"
            print_header "部署完成！"
            echo ""
            ;;
        clean)
            clean_build
            print_header "清理完成！"
            echo ""
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: ${COMMAND}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主程序
main "$@"
