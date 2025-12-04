#!/bin/bash

# 图片黑名单检查脚本
# 用途：检查文档中是否引用了黑名单中的图片

BLACKLIST_FILE=".image-blacklist.json"
DOCS_DIR="docs"

echo "🔍 检查文档中的图片引用..."
echo ""

# 提取黑名单中的文件名（macOS 兼容的方式）
blacklisted_images=$(grep -o '"filename": *"[^"]*"' "$BLACKLIST_FILE" | sed 's/"filename": *"//;s/"//')

found_issues=0

# 检查每个黑名单图片
while IFS= read -r image; do
    if [ -z "$image" ]; then
        continue
    fi

    # 只在 .md 文件中搜索该图片的引用
    matches=$(grep -r "$image" "$DOCS_DIR"/**/*.md 2>/dev/null)

    if [ ! -z "$matches" ]; then
        echo "⚠️  警告：发现黑名单图片引用 - $image"
        echo "$matches"
        echo ""
        found_issues=$((found_issues + 1))
    fi
done <<< "$blacklisted_images"

if [ $found_issues -eq 0 ]; then
    echo "✅ 检查完成：没有发现黑名单图片的引用"
else
    echo "❌ 发现 $found_issues 个黑名单图片仍被引用"
    exit 1
fi
