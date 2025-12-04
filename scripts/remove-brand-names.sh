#!/bin/bash

# 品牌名称批量清理脚本
# 用途：从所有文档中移除特定品牌名称

DOCS_DIR="docs"
BACKUP_DIR=".backup_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="brand_cleanup_$(date +%Y%m%d_%H%M%S).log"

echo "🚀 开始批量清理品牌名称..." | tee -a "$LOG_FILE"
echo "📁 文档目录: $DOCS_DIR" | tee -a "$LOG_FILE"
echo "💾 备份目录: $BACKUP_DIR" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 创建备份
echo "📦 创建备份..." | tee -a "$LOG_FILE"
mkdir -p "$BACKUP_DIR"
cp -r "$DOCS_DIR" "$BACKUP_DIR/"
echo "✅ 备份完成: $BACKUP_DIR/docs" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 统计信息
total_files=0
modified_files=0
total_replacements=0

# 查找所有 Markdown 文件
echo "🔍 扫描 Markdown 文件..." | tee -a "$LOG_FILE"
while IFS= read -r file; do
    total_files=$((total_files + 1))

    # 检查文件是否包含品牌名称
    if grep -q -i "crmeb" "$file"; then
        echo "📝 处理: $file" | tee -a "$LOG_FILE"

        # 计算替换次数
        before_count=$(grep -o -i "crmeb" "$file" | wc -l)

        # 执行替换（从最具体到最通用）
        sed -i '' \
            -e 's/CRMEB 多商户 Java 系统/多商户 Java 商城系统/g' \
            -e 's/CRMEB Java 多商户/Java 多商户商城系统/g' \
            -e 's/CRMEB-Java/Java商城系统/g' \
            -e 's/CRMEB 系统/商城系统/g' \
            -e 's/CRMEB 后台/管理后台/g' \
            -e 's/CRMEB 管理后台/系统管理后台/g' \
            -e 's/CRMEB 商城/商城平台/g' \
            -e 's/CRMEB 文档/系统文档/g' \
            -e 's/什么是 CRMEB？/系统简介/g' \
            -e 's/CRMEB 是/本系统是/g' \
            -e 's/选择 CRMEB/选择本系统/g' \
            -e 's/用 CRMEB/使用本系统/g' \
            -e 's/在 CRMEB/在系统/g' \
            -e 's/CRMEB 的/本系统的/g' \
            -e 's/CRMEB/本系统/g' \
            -e 's/CrmebAdminApplication/AdminApplication/g' \
            -e 's/CrmebApplication/Application/g' \
            -e 's/crmeb-admin/system-admin/g' \
            -e 's/crmeb-front/system-front/g' \
            -e 's/crmeb-java/shop-system/g' \
            -e 's/crmeb-shop/shop-site/g' \
            -e 's/crmeb-h5/h5-site/g' \
            -e 's/crmeb-files/shop-files/g' \
            -e 's/crmeb-prod-images/prod-images/g' \
            -e 's/crmeb-test-images/test-images/g' \
            -e 's/crmeb-prod-files/prod-files/g' \
            -e "s/CREATE USER 'crmeb'/CREATE USER 'dbuser'/g" \
            -e "s/'crmeb'@/'dbuser'@/g" \
            -e 's/username: crmeb/username: dbuser/g' \
            -e 's/mysql -u crmeb/mysql -u dbuser/g' \
            -e 's/ -u crmeb / -u dbuser /g' \
            -e 's/crmeb_db/shop_db/g' \
            -e 's/crmeb\.sql/database.sql/g' \
            -e 's/com\.crmeb/com.shop/g' \
            -e 's/Description=CRMEB/Description=Shop System/g' \
            -e 's/crmeb\.service/shop.service/g' \
            "$file"

        # 计算替换后的次数
        after_count=$(grep -o -i "crmeb" "$file" | wc -l)

        replacements=$((before_count - after_count))

        if [ $replacements -gt 0 ]; then
            modified_files=$((modified_files + 1))
            total_replacements=$((total_replacements + replacements))
            echo "   ✅ 替换了 $replacements 处" | tee -a "$LOG_FILE"
        else
            echo "   ⚠️  未发现可替换内容" | tee -a "$LOG_FILE"
        fi
    fi
done < <(find "$DOCS_DIR" -name "*.md" -type f)

echo "" | tee -a "$LOG_FILE"
echo "📊 统计摘要" | tee -a "$LOG_FILE"
echo "===================" | tee -a "$LOG_FILE"
echo "📁 扫描文件数: $total_files" | tee -a "$LOG_FILE"
echo "📝 修改文件数: $modified_files" | tee -a "$LOG_FILE"
echo "🔄 总替换次数: $total_replacements" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 最终验证
remaining=$(grep -r -i "crmeb" "$DOCS_DIR" --include="*.md" | wc -l)
if [ $remaining -eq 0 ]; then
    echo "✅ 完成！所有品牌名称已清理干净" | tee -a "$LOG_FILE"
else
    echo "⚠️  警告：仍有 $remaining 处品牌名称残留" | tee -a "$LOG_FILE"
    echo "   请查看详细日志：$LOG_FILE" | tee -a "$LOG_FILE"
    grep -r -i "crmeb" "$DOCS_DIR" --include="*.md" -n | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "💾 备份位置: $BACKUP_DIR" | tee -a "$LOG_FILE"
echo "📋 日志文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "如需恢复，执行：" | tee -a "$LOG_FILE"
echo "  rm -rf $DOCS_DIR && cp -r $BACKUP_DIR/docs $DOCS_DIR" | tee -a "$LOG_FILE"
