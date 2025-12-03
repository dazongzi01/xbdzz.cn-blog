#!/bin/bash

###############################################################################
# HTML 转 Markdown 处理脚本（增强版 - 支持图片处理）
# 用法: bash html-to-article.sh <article-name> <output-dir> <input-files...>
#
# 功能：
# 1. 支持多种图片格式提取（img, figure+figcaption）
# 2. 保留图片说明（alt, title, figcaption）
# 3. 可选：下载图片到本地（设置 DOWNLOAD_IMAGES=true）
###############################################################################

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置选项
DOWNLOAD_IMAGES="${DOWNLOAD_IMAGES:-false}"  # 是否下载图片到本地
USE_PANDOC="${USE_PANDOC:-true}"             # 优先使用 pandoc（如果可用）

# 检查参数
if [ $# -lt 2 ]; then
    echo -e "${RED}✗ 错误：参数不足${NC}"
    echo -e "${BLUE}用法：bash html-to-article.sh <article-name> <output-dir> <input-files...>${NC}"
    echo -e "${BLUE}环境变量：${NC}"
    echo -e "${BLUE}  DOWNLOAD_IMAGES=true  # 下载图片到本地${NC}"
    echo -e "${BLUE}  USE_PANDOC=false      # 不使用 pandoc${NC}"
    exit 1
fi

ARTICLE_NAME="$1"
OUTPUT_DIR="$2"
shift 2
INPUT_FILES=("$@")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEMP_DIR="${SCRIPT_DIR}/.temp"
mkdir -p "${TEMP_DIR}"

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║              📄 HTML → Markdown 转换处理                     ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 判断输出目录
if [ -z "${OUTPUT_DIR}" ]; then
    if [[ "${ARTICLE_NAME}" == 02_* ]]; then
        OUTPUT_DIR="02_系统安装"
    else
        OUTPUT_DIR="01_初步了解"
    fi
fi

OUTPUT_PATH="${SCRIPT_DIR}/docs/${OUTPUT_DIR}"
mkdir -p "${OUTPUT_PATH}"

echo -e "${BLUE}📂 输出目录: ${YELLOW}docs/${OUTPUT_DIR}/${NC}"
echo ""

# 合并所有 HTML 文件内容
MERGED_HTML="${TEMP_DIR}/merged.html"
echo "" > "${MERGED_HTML}"

for file in "${INPUT_FILES[@]}"; do
    if [ ! -f "${file}" ]; then
        echo -e "${RED}✗ 文件不存在: ${file}${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ 读取文件: ${file}${NC}"

    # 移除 <style> 和 <script> 标签及其内容，保留 HTML 主体
    sed -E '/<style[^>]*>/,/<\/style>/d; /<script[^>]*>/,/<\/script>/d' "${file}" >> "${MERGED_HTML}"
    echo "" >> "${MERGED_HTML}"
done

# 判断是否使用 pandoc
TEMP_MD="${TEMP_DIR}/${ARTICLE_NAME}.md"
echo -e "${BLUE}🔄 转换中...${NC}"

HAS_PANDOC=false
if command -v pandoc &> /dev/null && [ "${USE_PANDOC}" = "true" ]; then
    HAS_PANDOC=true
    echo -e "${GREEN}✓ 使用 pandoc 进行转换（支持完整图片处理）${NC}"

    # 使用 pandoc 转换，自动处理图片
    pandoc -f html -t markdown "${MERGED_HTML}" -o "${TEMP_MD}" 2>/dev/null || {
        echo -e "${YELLOW}⚠ pandoc 转换失败，使用备用方法${NC}"
        HAS_PANDOC=false
    }
fi

# 如果没有 pandoc 或转换失败，使用增强的 sed 处理
if [ "${HAS_PANDOC}" = "false" ]; then
    echo -e "${YELLOW}⚠ 使用 sed 进行转换（基础图片支持）${NC}"

    # 创建临时文件用于多步处理
    TEMP_HTML="${TEMP_DIR}/temp.html"
    cp "${MERGED_HTML}" "${TEMP_HTML}"

    # 图片处理策略：按照特定顺序匹配，避免重复匹配
    # 注意：必须先处理更复杂的模式，再处理简单模式

    # 步骤1：标记所有图片标签（使用特殊占位符避免被误删）
    # 处理顺序：title+alt -> 只有alt -> 没有alt
    # 使用 @@@ 作为分隔符，避免与 URL 中的冒号和其他字符冲突

    # 1a. 处理带 title 的图片（src 和 alt 可能的顺序）
    sed -i '' -E 's#<img[[:space:]]+([^>]*[[:space:]])?src="([^"]*)"([^>]*[[:space:]])?alt="([^"]*)"([^>]*[[:space:]])?title="([^"]*)"[^>]*>#__IMG_TITLE__@@@\4@@@\2@@@\6#g' "${TEMP_HTML}"
    sed -i '' -E 's#<img[[:space:]]+([^>]*[[:space:]])?alt="([^"]*)"([^>]*[[:space:]])?src="([^"]*)"([^>]*[[:space:]])?title="([^"]*)"[^>]*>#__IMG_TITLE__@@@\2@@@\4@@@\6#g' "${TEMP_HTML}"

    # 1b. 处理只有 alt 的图片
    sed -i '' -E 's#<img[[:space:]]+([^>]*[[:space:]])?src="([^"]*)"([^>]*[[:space:]])?alt="([^"]*)"[^>]*>#__IMG_ALT__@@@\4@@@\2#g' "${TEMP_HTML}"
    sed -i '' -E 's#<img[[:space:]]+([^>]*[[:space:]])?alt="([^"]*)"([^>]*[[:space:]])?src="([^"]*)"[^>]*>#__IMG_ALT__@@@\2@@@\4#g' "${TEMP_HTML}"

    # 1c. 处理没有 alt 的图片
    sed -i '' -E 's#<img[[:space:]]+([^>]*[[:space:]])?src="([^"]*)"[^>]*>#__IMG_NOALT__@@@图片@@@\2#g' "${TEMP_HTML}"

    # 步骤2：转换其他 HTML 标签
    sed -E \
        -e 's/<h1[^>]*>(.*)<\/h1>/# \1/g' \
        -e 's/<h2[^>]*>(.*)<\/h2>/## \1/g' \
        -e 's/<h3[^>]*>(.*)<\/h3>/### \1/g' \
        -e 's/<h4[^>]*>(.*)<\/h4>/#### \1/g' \
        -e 's/<p[^>]*>(.*)<\/p>/\1\n/g' \
        -e 's/<strong[^>]*>(.*)<\/strong>/**\1**/g' \
        -e 's/<b[^>]*>(.*)<\/b>/**\1**/g' \
        -e 's/<em[^>]*>(.*)<\/em>/*\1*/g' \
        -e 's/<i[^>]*>(.*)<\/i>/*\1*/g' \
        -e 's/<code[^>]*>(.*)<\/code>/`\1`/g' \
        -e 's/<br[^>]*>/\n/g' \
        -e 's/<figcaption[^>]*>(.*)<\/figcaption>/*\1*/g' \
        -e 's/<[^>]*>//g' \
        "${TEMP_HTML}" > "${TEMP_MD}"

    # 步骤3：将占位符转换为 Markdown 格式
    # 使用 @@@ 作为分隔符解析
    sed -i '' -E 's#__IMG_TITLE__@@@([^@]*)@@@([^@]*)@@@([^_]*)#![\1](\2 "\3")#g' "${TEMP_MD}"
    sed -i '' -E 's#__IMG_ALT__@@@([^@]*)@@@([^_]*)#![\1](\2)#g' "${TEMP_MD}"
    sed -i '' -E 's#__IMG_NOALT__@@@([^@]*)@@@([^_]*)#![\1](\2)#g' "${TEMP_MD}"

    # 清理临时文件
    rm -f "${TEMP_HTML}"
fi

# 输出转换后的内容
OUTPUT_FILE="${OUTPUT_PATH}/${ARTICLE_NAME}.md"
cp "${TEMP_MD}" "${OUTPUT_FILE}"

# 统计图片数量
IMAGE_COUNT=$(grep -o '!\[.*\](.*)' "${OUTPUT_FILE}" | wc -l | tr -d ' ')
echo -e "${GREEN}✅ 转换完成${NC}"
echo -e "${BLUE}📊 找到图片: ${YELLOW}${IMAGE_COUNT} 张${NC}"

# 可选：下载图片到本地
if [ "${DOWNLOAD_IMAGES}" = "true" ] && [ "${IMAGE_COUNT}" -gt 0 ]; then
    echo ""
    echo -e "${CYAN}🔽 开始下载图片到本地...${NC}"

    # 创建图片目录
    IMAGES_DIR="${OUTPUT_PATH}/images"
    mkdir -p "${IMAGES_DIR}"

    # 提取所有图片 URL（只提取 URL，不包括 title 部分）
    # 格式: ![alt](url) 或 ![alt](url "title")
    grep -oE '!\[[^\]]*\]\([^)]+\)' "${OUTPUT_FILE}" | while IFS= read -r img_line; do
        # 提取括号内的内容
        url=$(echo "${img_line}" | sed -E 's/!\[[^\]]*\]\(([^ ")]+).*\)/\1/')

        # 跳过已经是本地路径的图片
        if [[ "${url}" =~ ^(http|https):// ]]; then
            # 提取文件名
            filename=$(basename "${url}" | sed 's/[?#].*//')

            # 如果文件名为空或无效，生成一个
            if [ -z "${filename}" ] || [[ ! "${filename}" =~ \. ]]; then
                filename="image_$(date +%s)_${RANDOM}.jpg"
            fi

            local_path="${IMAGES_DIR}/${filename}"

            # 下载图片
            if curl -sS -L -f "${url}" -o "${local_path}" 2>/dev/null; then
                echo -e "${GREEN}  ✓ 下载: ${filename}${NC}"

                # 更新 Markdown 文件中的路径
                relative_path="./images/${filename}"
                # 使用更精确的替换，只替换 URL 部分
                sed -i '' "s|${url}|${relative_path}|g" "${OUTPUT_FILE}"
            else
                echo -e "${YELLOW}  ⚠ 下载失败: ${url}${NC}"
            fi
        fi
    done

    echo -e "${GREEN}✅ 图片下载完成${NC}"
    echo -e "${BLUE}📁 图片目录: ${GREEN}${IMAGES_DIR}${NC}"
fi

echo ""
echo -e "${BLUE}📁 输出位置: ${GREEN}${OUTPUT_FILE}${NC}"
echo ""

# 显示使用提示
if [ "${DOWNLOAD_IMAGES}" != "true" ] && [ "${IMAGE_COUNT}" -gt 0 ]; then
    echo -e "${CYAN}💡 提示：${NC}"
    echo -e "${YELLOW}   如需下载图片到本地，请使用：${NC}"
    echo -e "${YELLOW}   DOWNLOAD_IMAGES=true bash html-to-article.sh ...${NC}"
    echo ""
fi

# 清理临时文件
rm -rf "${TEMP_DIR}"

exit 0
