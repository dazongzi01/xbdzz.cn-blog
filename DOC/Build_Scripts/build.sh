#!/bin/bash

# 文档构建脚本 - 自动过滤未采集的文档
# 用法: ./build.sh

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[信息]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[成功]${NC} $1"
}

print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

# 打印标题
echo ""
echo "======================================"
echo "   📦 文档构建脚本"
echo "======================================"
echo ""

# 检查 Python3 是否安装
if ! command -v python3 &> /dev/null; then
    print_error "Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    print_error "Node.js 未安装，请先安装 Node.js"
    exit 1
fi

# 检查过滤脚本是否存在
if [ ! -f "scripts/filter-collected-docs.py" ]; then
    print_error "找不到过滤脚本: scripts/filter-collected-docs.py"
    exit 1
fi

# 检查 TODO 配置文件是否存在
if [ ! -f "TODO_CAIJI.md" ]; then
    print_error "找不到 TODO_CAIJI.md 配置文件"
    exit 1
fi

# 第一步：过滤未采集的文档
print_info "步骤 1/2: 正在过滤未采集的文档..."
echo "--------------------------------------"

if python3 scripts/filter-collected-docs.py; then
    print_success "文档过滤完成"
else
    print_error "文档过滤失败"
    exit 1
fi

echo ""
echo "--------------------------------------"

# 第二步：构建文档
print_info "步骤 2/2: 正在构建文档..."
echo "--------------------------------------"

if npm run build:force; then
    echo ""
    echo "--------------------------------------"
    print_success "文档构建完成！"

    # 显示构建输出目录
    if [ -d "docs/.vitepress/dist" ]; then
        echo ""
        print_info "构建输出目录: docs/.vitepress/dist"

        # 统计文件数量
        HTML_COUNT=$(find docs/.vitepress/dist -name "*.html" | wc -l)
        print_info "生成的 HTML 文件数: ${HTML_COUNT}"
    fi

    echo ""
    print_info "预览构建结果:"
    echo "  npm run preview"
else
    echo ""
    print_error "文档构建失败！"
    exit 1
fi

echo ""
echo "======================================"
print_success "✅ 构建流程已完成"
echo "======================================"
echo ""
