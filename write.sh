#!/bin/bash

###############################################################################
# 文档写作命令 - 简化版
# 用法：
#   bash write.sh <article-name> [--dir <directory>]                              # 指定输出目录
#   bash write.sh <article-name> <file-path> [--dir <directory>]                 # 从本地文件生成
#   bash write.sh <article-name> <file1> <file2> [--dir <directory>]    # 合并多个文件
# 说明：
#   1. <article-name> - 文章名称（必须）
#   2. <files> - 输入文件列表（可选，不指定则不处理 HTML）
#   3. --dir <directory> - 输出目录（可选，不指定则根据文章名称前缀自动判断）
# 示例：
#   bash write.sh 02_搭建准备                                    # 自动输出到对应目录
#   bash write.sh 03_公众号 --dir 02_系统安装                   # 输出到指定目录
#   bash write.sh 03_公众号 file1.html file2.html --dir 02_系统安装
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
    echo -e "${BLUE}用法：bash write.sh <article-name> [files...] [--dir <directory>]${NC}"
    echo -e "${BLUE}示例1：bash write.sh 02_搭建准备${NC}"
    echo -e "${BLUE}示例2：bash write.sh 03_公众号 --dir 02_系统安装${NC}"
    echo -e "${BLUE}示例3：bash write.sh 03_公众号 file1.html file2.html --dir 02_系统安装${NC}"
    exit 1
fi

ARTICLE_NAME="$1"
shift
INPUT_FILES=()
OUTPUT_DIR=""

# 解析参数：分离输入文件和 --dir 选项
while [ $# -gt 0 ]; do
    if [ "$1" = "--dir" ]; then
        if [ $# -lt 2 ]; then
            echo -e "${RED}✗ 错误：--dir 选项需要指定目录${NC}"
            exit 1
        fi
        OUTPUT_DIR="$2"
        shift 2
    else
        INPUT_FILES+=("$1")
        shift
    fi
done

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    📄 文档自动写作处理                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📋 文章: ${YELLOW}${ARTICLE_NAME}${NC}"

# 如果提供了文件路径，先处理 HTML 和图片
if [ ${#INPUT_FILES[@]} -gt 0 ]; then
    # 验证所有文件都存在
    for file in "${INPUT_FILES[@]}"; do
        if [ ! -f "${file}" ]; then
            echo -e "${RED}✗ 错误：文件不存在: ${file}${NC}"
            exit 1
        fi
    done

    # 显示输入文件
    echo -e "${BLUE}📄 输入文件数: ${YELLOW}${#INPUT_FILES[@]}${NC}"
    for i in "${!INPUT_FILES[@]}"; do
        echo -e "${YELLOW}   $((i+1)). ${INPUT_FILES[$i]}${NC}"
    done
    echo ""

    # 处理多个文件 - 传递所有文件给 html-to-article.sh
    bash "${SCRIPT_DIR}/html-to-article.sh" "${ARTICLE_NAME}" "${OUTPUT_DIR}" "${INPUT_FILES[@]}"
    echo ""
fi

# 执行工作流生成完整文章
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# 执行简化版处理脚本生成文章
bash "${SCRIPT_DIR}/simple-process.sh" "${ARTICLE_NAME}" "${OUTPUT_DIR}"

echo ""
echo -e "${GREEN}✅ 完成！${NC}"
echo -e "${BLUE}📁 输出文件位置：${NC}"

# 判断最终输出目录
if [ -z "${OUTPUT_DIR}" ]; then
    # 未指定 --dir，根据文章名称前缀自动判断
    if [[ "${ARTICLE_NAME}" == 02_* ]]; then
        OUTPUT_DIR="02_系统安装"
    else
        OUTPUT_DIR="01_初步了解"
    fi
fi

echo -e "  ${GREEN}docs/${OUTPUT_DIR}/${ARTICLE_NAME}*.md${NC}"

echo ""
