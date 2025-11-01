#!/bin/bash

###############################################################################
# 文档写作命令 - 简化版
# 用法：bash write.sh <article-name>
# 说明：
#   1. 在 Claude 中提供您的文档内容
#   2. 内容会自动保存到 .claude/work/<article-name>/00-raw-input.md
#   3. 执行此命令处理文档：bash write.sh <article-name>
#   4. 最终文章自动输出到 docs/01_初步了解/
###############################################################################

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}✗ 错误：缺少文章名称${NC}"
    echo -e "${BLUE}用法：bash write.sh <article-name>${NC}"
    echo -e "${BLUE}示例：bash write.sh 00_简介${NC}"
    exit 1
fi

ARTICLE_NAME="$1"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    📄 文档自动写作处理                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📋 文章: ${YELLOW}${ARTICLE_NAME}${NC}"
echo ""

# 执行工作流
bash "${SCRIPT_DIR}/workflow.sh" process "${ARTICLE_NAME}"

echo ""
echo -e "${GREEN}✅ 完成！${NC}"
echo -e "${BLUE}📁 输出文件位置：${NC}"
echo -e "  ${GREEN}docs/01_初步了解/${ARTICLE_NAME}*.md${NC}"
echo ""
