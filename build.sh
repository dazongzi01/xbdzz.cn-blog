#!/bin/bash

###############################################################################
# VitePress 文档编译脚本
# 功能：编译 Markdown 文档成静态网站
#
# 使用方法：
#   ./build.sh              # 编译文档
#   ./build.sh --stats      # 编译并显示统计信息
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

# 打印函数
print_header() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    📦 VitePress 编译脚本"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
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

# 主程序
main() {
    print_header

    # 检查环境
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
    echo ""

    # 编译文档
    print_info "开始编译文档..."
    echo ""

    if npm run build:force; then
        echo ""
        print_success "编译完成！"
        echo ""

        # 显示统计信息（如果指定 --stats）
        if [ "${1:-}" = "--stats" ]; then
            echo -e "${YELLOW}📊 编译统计：${NC}"

            DIST_DIR="docs/.vitepress/dist"
            if [ -d "$DIST_DIR" ]; then
                HTML_COUNT=$(find "$DIST_DIR" -name "*.html" 2>/dev/null | wc -l)
                JS_COUNT=$(find "$DIST_DIR" -name "*.js" 2>/dev/null | wc -l)
                CSS_COUNT=$(find "$DIST_DIR" -name "*.css" 2>/dev/null | wc -l)
                IMG_COUNT=$(find "$DIST_DIR" \( -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.svg" \) 2>/dev/null | wc -l)
                TOTAL_SIZE=$(du -sh "$DIST_DIR" 2>/dev/null | cut -f1)
                TOTAL_FILES=$(find "$DIST_DIR" -type f 2>/dev/null | wc -l)

                echo "  HTML 文件:   $HTML_COUNT"
                echo "  JavaScript:  $JS_COUNT"
                echo "  CSS 文件:    $CSS_COUNT"
                echo "  图片文件:    $IMG_COUNT"
                echo "  总文件数:    $TOTAL_FILES"
                echo ""
                echo -e "${YELLOW}📈 大小统计：${NC}"
                echo "  总大小:      $TOTAL_SIZE"
                echo ""
            fi
        fi

        echo -e "${YELLOW}📁 输出目录：${NC}"
        echo "  docs/.vitepress/dist/"
        echo ""
        echo -e "${YELLOW}📝 后续步骤：${NC}"
        echo "  预览: npm run preview"
        echo "  部署: ./deploy.sh all"
        echo ""
    else
        print_error "编译失败！"
        exit 1
    fi
}

# 显示帮助
show_help() {
    echo -e "${CYAN}VitePress 文档编译脚本${NC}"
    echo ""
    echo "使用方法："
    echo "  ./build.sh              编译文档"
    echo "  ./build.sh --stats      编译并显示统计信息"
    echo "  ./build.sh --help       显示此帮助信息"
    echo ""
}

# 处理参数
case "${1:-build}" in
    --help|-h)
        show_help
        ;;
    build|--stats)
        main "$@"
        ;;
    *)
        print_error "未知选项: $1"
        show_help
        exit 1
        ;;
esac
