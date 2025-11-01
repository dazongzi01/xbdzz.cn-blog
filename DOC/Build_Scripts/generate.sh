#!/bin/bash

###############################################################################
# 文章内容生成脚本 - 一条命令生成完整文章
# 用法: bash generate.sh /path/to/your/file.md
###############################################################################

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}✗ 错误：缺少文件路径${NC}"
    echo -e "${BLUE}用法：bash generate.sh /path/to/your/file.md${NC}"
    exit 1
fi

INPUT_FILE="$1"

# 检查文件是否存在
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}✗ 错误：文件不存在: $INPUT_FILE${NC}"
    exit 1
fi

# 检查必要的依赖
echo -e "${BLUE}ℹ 检查依赖...${NC}"

if ! python3 -c "import anthropic" 2>/dev/null; then
    echo -e "${YELLOW}⚠ 缺少 anthropic 包，正在安装...${NC}"
    pip3 install anthropic -q
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo -e "${RED}✗ 错误：未设置 ANTHROPIC_API_KEY 环境变量${NC}"
    echo -e "${BLUE}请先执行：export ANTHROPIC_API_KEY=\"sk-...\"${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 依赖检查完成${NC}"

# 获取文件名（不含扩展名）作为 article-name
ARTICLE_NAME=$(basename "$INPUT_FILE" .md)

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 初始化文章（如果还没有）
if [ ! -d "$SCRIPT_DIR/.claude/articles/$ARTICLE_NAME" ]; then
    echo -e "${BLUE}ℹ 初始化文章: $ARTICLE_NAME${NC}"
    bash workflow.sh init "$ARTICLE_NAME" --title "$ARTICLE_NAME"
fi

# 复制用户的输入文件到工作目录
cp "$INPUT_FILE" "$SCRIPT_DIR/.claude/articles/$ARTICLE_NAME/00-raw-input.md"
echo -e "${GREEN}✓ 已读取文件内容${NC}"

# 运行完整工作流
echo -e "${BLUE}ℹ 开始处理工作流...${NC}"
bash workflow.sh run "$ARTICLE_NAME"

echo -e ""
echo -e "${GREEN}✓ 完成！${NC}"
echo -e "${BLUE}ℹ 生成的文件位置：${NC}"
echo -e "  .claude/articles/$ARTICLE_NAME/"
echo -e ""
echo -e "${BLUE}ℹ 主要输出：${NC}"
echo -e "  - 02-draft.md      → 最终文章（5000+字）"
echo -e "  - 03-guidelines.md → 配图指南"
echo -e "  - 04-checklist.md  → 排版清单"
echo -e "  - 05-final.md      → 发布检查清单"
echo -e ""
