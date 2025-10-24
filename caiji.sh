#!/bin/bash

# 文档采集自动化脚本
# 用法: ./caiji.sh

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
echo "   📋 文档采集自动化脚本"
echo "======================================"
echo ""

# 检查 Python3 是否安装
if ! command -v python3 &> /dev/null; then
    print_error "Python3 未安装，请先安装 Python3"
    exit 1
fi

print_info "Python 版本: $(python3 --version)"

# 检查采集脚本是否存在
if [ ! -f "smart_crawler_three_level.py" ]; then
    print_error "找不到 smart_crawler_three_level.py 脚本"
    exit 1
fi

# 检查任务配置文件是否存在
if [ ! -f "TODO_CAIJI.md" ]; then
    print_error "找不到 TODO_CAIJI.md 配置文件"
    exit 1
fi

# 显示待采集任务数量
print_info "正在读取采集任务..."
TOTAL_TASKS=$(grep -c "采集状态: \[ \]" TODO_CAIJI.md || true)
print_info "待采集任务数: ${TOTAL_TASKS}"

if [ "$TOTAL_TASKS" -eq 0 ]; then
    print_warning "没有待采集的任务"
    exit 0
fi

echo ""
print_info "开始执行采集任务..."
echo "--------------------------------------"

# 执行采集脚本
if python3 smart_crawler_three_level.py; then
    echo ""
    echo "--------------------------------------"
    print_success "采集任务执行完成！"

    # 显示采集结果统计
    COMPLETED=$(grep -c "采集状态: \[✅\]" TODO_CAIJI.md || true)
    FAILED=$(grep -c "采集状态: \[❌\]" TODO_CAIJI.md || true)

    echo ""
    print_info "采集统计:"
    echo "  - 成功: ${COMPLETED}"
    echo "  - 失败: ${FAILED}"
    echo "  - 待采集: $((TOTAL_TASKS - COMPLETED - FAILED))"

    # 显示输出目录
    if [ -d "docs" ]; then
        echo ""
        print_info "采集的文档保存在 docs/ 目录"
        print_info "目录结构:"
        tree docs -L 2 2>/dev/null || ls -R docs/
    fi
else
    echo ""
    print_error "采集任务执行失败！"
    exit 1
fi

echo ""
echo "======================================"
print_success "✅ 所有任务已完成"
echo "======================================"
echo ""
