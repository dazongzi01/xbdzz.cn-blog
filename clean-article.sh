#!/bin/bash
# 清理文档中的CSS和JS代码

FILE="$1"
TEMP_FILE="${FILE}.tmp"

# 使用 awk 清理
awk '
/^```/ { in_code=!in_code; print; next }
in_code { print; next }
/^\s*(\/\*|\.semi-|@keyframes|position:|background|width:|height:|--semi-|rgba|transform|transition|animation)/ { next }
/^\s*[{}]\s*$/ { next }
{ print }
' "${FILE}" > "${TEMP_FILE}" && mv "${TEMP_FILE}" "${FILE}" && echo "✅ 清理完成"
