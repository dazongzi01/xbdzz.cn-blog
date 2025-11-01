#!/bin/bash

###############################################################################
# 文章完整工作流 - 一条命令搞定5个阶段
# 用法1: bash run-full-workflow.sh <article-name>
# 用法2: bash run-full-workflow.sh /path/to/file.md
# 示例1: bash run-full-workflow.sh 00_简介
# 示例2: bash run-full-workflow.sh /Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/docs/01_初步了解/00_简介.md
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
    echo -e "${RED}✗ 错误：缺少参数${NC}"
    echo -e "${BLUE}用法1：bash run-full-workflow.sh <article-name>${NC}"
    echo -e "${BLUE}用法2：bash run-full-workflow.sh /path/to/file.md${NC}"
    echo -e "${BLUE}示例1：bash run-full-workflow.sh 00_简介${NC}"
    echo -e "${BLUE}示例2：bash run-full-workflow.sh /Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/docs/01_初步了解/00_简介.md${NC}"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INPUT="$1"

# 判断是文件路径还是文章名称
if [[ "$INPUT" == /* ]] || [[ "$INPUT" == ./* ]]; then
    # 输入是文件路径
    if [ ! -f "$INPUT" ]; then
        echo -e "${RED}✗ 错误：文件不存在: $INPUT${NC}"
        exit 1
    fi
    # 提取文件名（不含扩展名）作为文章名称
    ARTICLE_NAME=$(basename "$INPUT" .md)
    # 复制文件到工作目录
    echo -e "${BLUE}ℹ 读取文件: $INPUT${NC}"
    mkdir -p "${SCRIPT_DIR}/.claude/articles/${ARTICLE_NAME}"
    cp "$INPUT" "${SCRIPT_DIR}/.claude/articles/${ARTICLE_NAME}/00-raw-input.md"
    echo -e "${GREEN}✓ 文件已准备${NC}"
else
    # 输入是文章名称
    ARTICLE_NAME="$INPUT"
fi

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  📄 文章完整工作流处理                        ║"
echo "║                  一条命令完成5个阶段                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📋 文章名称: ${YELLOW}${ARTICLE_NAME}${NC}"
echo ""

# Phase 1
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}[1/5] 执行 Phase 1: 内容规划与分析${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
bash "${SCRIPT_DIR}/workflow.sh" phase "${ARTICLE_NAME}" 1
echo -e "${GREEN}✓ Phase 1 完成${NC}\n"

# Phase 2
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}[2/5] 执行 Phase 2: 初稿内容生成${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
bash "${SCRIPT_DIR}/workflow.sh" phase "${ARTICLE_NAME}" 2
echo -e "${GREEN}✓ Phase 2 完成${NC}\n"

# Phase 3
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}[3/5] 执行 Phase 3: 配图制作指南${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
bash "${SCRIPT_DIR}/workflow.sh" phase "${ARTICLE_NAME}" 3
echo -e "${GREEN}✓ Phase 3 完成${NC}\n"

# Phase 4
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}[4/5] 执行 Phase 4: 排版优化检查${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
bash "${SCRIPT_DIR}/workflow.sh" phase "${ARTICLE_NAME}" 4
echo -e "${GREEN}✓ Phase 4 完成${NC}\n"

# Phase 5
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}[5/5] 执行 Phase 5: 发布前质检${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
bash "${SCRIPT_DIR}/workflow.sh" phase "${ARTICLE_NAME}" 5
echo -e "${GREEN}✓ Phase 5 完成${NC}\n"

# 最终状态
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ 所有5个阶段均已完成！${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 显示生成的文件
echo -e "${YELLOW}📁 生成的文件位置：${NC}"
echo -e "  ${BLUE}.claude/articles/${ARTICLE_NAME}/${NC}"
echo ""

echo -e "${YELLOW}📄 核心输出文件：${NC}"
echo -e "  ${GREEN}✓${NC} ${BLUE}02-draft.md${NC}              → 最终文章（主要输出）"
echo -e "  ${GREEN}✓${NC} ${BLUE}03-guidelines.md${NC}         → 配图制作指南"
echo -e "  ${GREEN}✓${NC} ${BLUE}04-checklist.md${NC}          → 排版优化检查清单"
echo -e "  ${GREEN}✓${NC} ${BLUE}05-final.md${NC}              → 发布前检查清单"
echo ""

echo -e "${YELLOW}📊 工作流统计：${NC}"
bash "${SCRIPT_DIR}/workflow.sh" status "${ARTICLE_NAME}"
echo ""

echo -e "${GREEN}🎉 工作流处理完成！${NC}"
echo -e "${BLUE}后续步骤：${NC}"
echo -e "  1. 查看 ${YELLOW}02-draft.md${NC} 了解完整文章内容"
echo -e "  2. 按照 ${YELLOW}03-guidelines.md${NC} 制作配图"
echo -e "  3. 参考 ${YELLOW}04-checklist.md${NC} 优化排版"
echo -e "  4. 按照 ${YELLOW}05-final.md${NC} 完成发布检查"
echo ""
