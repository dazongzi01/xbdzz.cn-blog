# 图片黑名单管理系统

## 📋 概述

本系统用于记录和管理不应该使用的图片文件，防止在文档编写过程中误用质量不合格的图片。

## 📂 文件说明

### 1. `.image-blacklist.json`
黑名单配置文件，记录所有被禁用的图片信息。

**字段说明：**
- `filename`: 图片文件名
- `deletedDate`: 删除日期
- `reason`: 删除原因
- `originalPath`: 原始路径
- `status`: 状态（deleted）

### 2. `scripts/check-image-blacklist.sh`
检查脚本，用于验证文档中是否引用了黑名单图片。

**用法：**
```bash
bash scripts/check-image-blacklist.sh
```

**返回值：**
- `0`: 检查通过，没有发现黑名单图片引用
- `1`: 检查失败，发现黑名单图片被引用

### 3. `scripts/image-usage-report.sh`
生成图片使用情况报告。

**用法：**
```bash
bash scripts/image-usage-report.sh
```

**输出内容：**
- 使用中的图片列表
- 未使用的图片列表
- 统计摘要

## 🔍 当前黑名单（9张）

已删除的不合格图片：
1. `84c3fb7843628de29b77a4ee9d596551.jpg`
2. `ai_guanwang.png`
3. `dark_logo.png`
4. `fb8012367dd2525ad8a00811c6255aae.jpg`
5. `icon_eyes.png`
6. `icon_picture.png`
7. `icon_sort.png`
8. `isSupport.png`
9. `no_portrait.png`

## 📊 当前图片统计（2025-12-04）

- ✅ **使用中**：9张
  - 8ec899e43d5733622f805fb931ce215c.png（圈层角色列表）
  - 2e708a76bd04c158daffabfe0673285b.png（新增圈层角色）
  - 8c5efbbc4df4917aae88963afdf60b60.png（圈层菜单配置）
  - 3c9c0b4950b986d46bfd14c2a59e5cfd.png（新增圈层）
  - 3bc424dc4f0025858ab161981ace466d.png（批量关联微页面）
  - 3ba76b01bb54f7bba106d1bec0d41225.png（添加圈层）
  - 7e892114688279d791032d0a5b07d706.png（圈层维护）
  - 42e862c3c7235773b6cbd022a557d368.png（归属商户）
  - 65f09acb7ddbea42c7226744c4da05f9.png（商户关联界面）

- ⚪ **未使用**：4张
  - 0b531278b30758295453b721132c0909.png
  - 6b001f1e5b4347844854990e34bc9253.png
  - a179e9cbb6ff141e51b94ac17b3bb181.png
  - f3d6341ec1d0dbf0abde32b0993a5ed8.png

- 🚫 **已禁用**：9张（见黑名单）

## 🚀 使用规则

### AI 助手规则

在采集或使用图片时：

1. **必须检查黑名单**：在使用任何图片前，先检查是否在黑名单中
2. **自动排除**：黑名单中的图片绝对不能使用
3. **及时更新**：发现新的不合格图片时，及时更新黑名单

### 手动操作规则

1. **删除图片后**：必须更新 `.image-blacklist.json`
2. **定期检查**：运行 `check-image-blacklist.sh` 确保没有误用
3. **生成报告**：运行 `image-usage-report.sh` 了解使用情况

## 📝 更新黑名单

当需要添加新的黑名单图片时：

1. 删除图片文件
2. 编辑 `.image-blacklist.json`
3. 添加新的条目：
   ```json
   {
     "filename": "图片文件名",
     "deletedDate": "删除日期",
     "reason": "删除原因",
     "originalPath": "原始路径",
     "status": "deleted"
   }
   ```
4. 更新 `statistics.totalBlacklisted` 计数
5. 运行检查脚本验证

## ✅ 验证流程

```bash
# 1. 检查黑名单图片是否被引用
bash scripts/check-image-blacklist.sh

# 2. 生成使用情况报告
bash scripts/image-usage-report.sh

# 3. 查看黑名单文件
cat .image-blacklist.json
```

## 🎯 最佳实践

1. **在采集图片前**：先查看黑名单，避免重复采集不合格图片
2. **在写文档时**：优先使用已验证的图片
3. **定期清理**：删除长期未使用的图片，保持目录整洁
4. **记录原因**：在黑名单中详细记录删除原因，方便后续参考

---

**最后更新**: 2025-12-04
**维护者**: AI 助手 + 用户
