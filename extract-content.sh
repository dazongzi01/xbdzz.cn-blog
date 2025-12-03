#!/bin/bash
# 从HTML中提取markdown-body内容

FILE=$1
OUTPUT=$2

# 提取markdown-body区域的内容，移除style和script
sed -n '/<div class="markdown-body/,/<\/div>/p' "$FILE" | \
  sed '/<style/,/<\/style>/d; /<script/,/<\/script>/d' > "$OUTPUT"

echo "✅ 已提取: $OUTPUT"
