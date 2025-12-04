#!/bin/bash

# 图片使用情况报告脚本
# 用途：生成图片使用情况的详细报告

IMAGES_DIR="docs/03_使用手册/images"
DOCS_DIR="docs/03_使用手册"
BLACKLIST_FILE=".image-blacklist.json"

echo "📊 图片使用情况报告"
echo "===================="
echo ""

# 统计总图片数
total_images=$(ls -1 "$IMAGES_DIR" 2>/dev/null | wc -l)
echo "📁 图片目录：$IMAGES_DIR"
echo "📈 总图片数：$total_images"
echo ""

# 统计黑名单数量
if [ -f "$BLACKLIST_FILE" ]; then
    blacklist_count=$(grep -c '"filename"' "$BLACKLIST_FILE")
    echo "🚫 黑名单数量：$blacklist_count"
else
    echo "🚫 黑名单数量：0（黑名单文件不存在）"
fi
echo ""

echo "使用中的图片："
echo "---------------"

# 查找所有被引用的图片
used_count=0
for image in "$IMAGES_DIR"/*; do
    filename=$(basename "$image")
    if grep -r "$filename" "$DOCS_DIR"/*.md &>/dev/null; then
        matches=$(grep -r "$filename" "$DOCS_DIR"/*.md | wc -l)
        echo "✅ $filename (引用 $matches 次)"
        used_count=$((used_count + 1))
    fi
done
echo ""

echo "未使用的图片："
echo "---------------"

unused_count=0
for image in "$IMAGES_DIR"/*; do
    filename=$(basename "$image")
    if ! grep -r "$filename" "$DOCS_DIR"/*.md &>/dev/null; then
        size=$(ls -lh "$image" | awk '{print $5}')
        echo "⚪ $filename ($size)"
        unused_count=$((unused_count + 1))
    fi
done

echo ""
echo "统计摘要："
echo "--------"
echo "✅ 使用中：$used_count 张"
echo "⚪ 未使用：$unused_count 张"
echo "📁 总计：$total_images 张"
