# 📝 文章自动化工作流系统

## 🚀 如何使用

### 1️⃣ 初始化文章
```bash
bash workflow.sh init {article-name} --title "文章标题" --audiences "技术人员,运营人员"
```

**示例**：
```bash
bash workflow.sh init my-article --title "Python 教程" --audiences "开发者"
```

### 2️⃣ 添加你的内容
编辑生成的文件：
```
./articles/{article-name}/00-raw-input.md
```

粘贴你的原始内容、大纲或笔记

### 3️⃣ 运行自动工作流
```bash
bash workflow.sh run {article-name}
```

系统会自动执行：
1. Phase 1: 内容规划（1小时）
2. Phase 2: 初稿生成（4-8小时）
3. Phase 3: 配图指南（1小时）
4. Phase 4: 排版优化（45分钟）
5. Phase 5: 发布检查（1小时）

### 4️⃣ 查看进度
```bash
bash workflow.sh status {article-name}
```

### 5️⃣ 发布文章
```bash
bash workflow.sh publish {article-name}
```

---

## 📁 生成的文件位置

```
./articles/{article-name}/
├─ 00-raw-input.md          你的原始内容
├─ 01-planning.md           规划文档
├─ 02-draft.md              初稿文章（5000+字）
├─ 03-guidelines.md         配图指南
├─ 04-checklist.md          排版清单
├─ 05-final.md              发布清单
├─ SUMMARY.md               完成总结
├─ config.json              配置
├─ status.json              进度
└─ logs/                    日志文件
```

---

## 🔧 其他常用命令

```bash
# 查看所有文章
bash workflow.sh list

# 只运行特定阶段（1-5）
bash workflow.sh phase {article-name} 2

# 从中断处继续
bash workflow.sh resume {article-name}

# 显示帮助
bash workflow.sh --help
```

---

## ⚙️ 必要配置

**使用 Phase 2（初稿生成）需要设置 API 密钥**：

```bash
export ANTHROPIC_API_KEY="sk-..."
```

---

## 📊 工作流说明

| 阶段 | 说明 | 输出 |
|-----|------|------|
| Phase 1 | 分析内容结构、规划内容 | 01-planning.md |
| Phase 2 | 使用Claude生成完整初稿 | 02-draft.md |
| Phase 3 | 生成配图制作指南 | 03-guidelines.md |
| Phase 4 | 检查排版、生成优化清单 | 04-checklist.md |
| Phase 5 | 质量评分、生成发布清单 | 05-final.md |

---

## ✨ 核心特性

✅ 完全自动化
✅ 多受众优化（技术人员、运营人员、产品经理）
✅ 支持中断和恢复
✅ Mac/Windows/Linux 兼容
✅ 70项质量检查
✅ 自动生成所有辅助文档

---

## 🎯 快速示例

```bash
# 初始化
bash workflow.sh init markdown-guide --title "Markdown 完全指南" --audiences "开发者,写手"

# 编辑内容
# vim ./articles/markdown-guide/00-raw-input.md

# 运行工作流
bash workflow.sh run markdown-guide

# 查看初稿
cat ./articles/markdown-guide/02-draft.md

# 发布
bash workflow.sh publish markdown-guide
```

---

**需要帮助？运行**: `bash workflow.sh --help`
