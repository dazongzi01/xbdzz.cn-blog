# 📋 工作流快速查阅表

> 完整文章自动化处理系统 - 快速参考指南

---

## ⚡ 最常用命令

### 一条命令处理一篇文章

```bash
bash run-full-workflow.sh <article-name>
```

### 实际例子

```bash
bash run-full-workflow.sh 00_简介
bash run-full-workflow.sh 01_安装搭建
bash run-full-workflow.sh 02_模块说明
```

---

## 📁 输出文件位置

所有文件保存在：`.claude/articles/<article-name>/`

### 您需要查看的文件（按优先级）

| 优先级 | 文件 | 用途 |
|--------|------|------|
| 🔴 最高 | **`02-draft.md`** | **最终文章（5000+字）** |
| 🟠 高 | `03-guidelines.md` | 配图制作指南 |
| 🟠 高 | `04-checklist.md` | 排版优化清单 |
| 🟡 中 | `05-final.md` | 发布前检查清单 |
| 🟢 参考 | `01-planning.md` | 规划分析文档 |

---

## 🎯 工作流做什么

```
输入: 744字符 (原始内容)
     ↓
[Phase 1] 内容规划 → 01-planning.md
     ↓
[Phase 2] 文章生成 → 02-draft.md (6,644字) ⭐
     ↓
[Phase 3] 配图指南 → 03-guidelines.md
     ↓
[Phase 4] 排版检查 → 04-checklist.md
     ↓
[Phase 5] 质量评分 → 05-final.md
     ↓
输出: 14个文件，168KB，完整的文章和所有辅助文档
```

---

## 💡 5个阶段详解

| 阶段 | 输入 | 输出 | 耗时 | 主要功能 |
|------|------|------|------|---------|
| Phase 1 | 原始内容 | 01-planning.md | 2min | 分析结构、确定受众、规划配图 |
| Phase 2 | 规划文档 | 02-draft.md | 5min | 生成5000+字完整文章 |
| Phase 3 | 初稿文章 | 03-guidelines.md | 1min | 提供配图尺寸和工具建议 |
| Phase 4 | 初稿文章 | 04-checklist.md | 1min | 检查排版、语法、表格 |
| Phase 5 | 初稿文章 | 05-final.md | 1min | 质量评分（0-100）、检查清单 |

---

## 🚀 快速开始步骤

### 步骤1：执行命令
```bash
cd /Users/dazongzi/ZBKJ/CODEMANGER/My_Doc
bash run-full-workflow.sh 00_简介
```

### 步骤2：等待完成
- 整个过程约15分钟
- 会看到每个Phase的进度输出

### 步骤3：查看结果
```bash
# 打开最终文章
open .claude/articles/00_简介/02-draft.md

# 打开配图指南
open .claude/articles/00_简介/03-guidelines.md

# 打开排版清单
open .claude/articles/00_简介/04-checklist.md
```

---

## 📞 其他有用的命令

### 查看工作流状态
```bash
bash workflow.sh status 00_简介
```

### 列出所有已处理的文章
```bash
bash workflow.sh list
```

### 查看工作流帮助
```bash
bash workflow.sh --help
```

### 执行单个Phase
```bash
bash workflow.sh phase 00_简介 1  # 执行Phase 1
bash workflow.sh phase 00_简介 2  # 执行Phase 2
bash workflow.sh phase 00_简介 3  # 执行Phase 3
bash workflow.sh phase 00_简介 4  # 执行Phase 4
bash workflow.sh phase 00_简介 5  # 执行Phase 5
```

---

## ✅ 发布前检查清单

按照 `05-final.md` 中的22项检查清单：

- [ ] 完成所有内容质量检查（8项）
- [ ] 完成所有排版格式检查（6项）
- [ ] 完成所有技术准确性检查（5项）
- [ ] 完成所有完整性检查（3项）

---

## 📊 内容成果数据

| 指标 | 数值 |
|------|------|
| 输入字符 | 744字 |
| 生成字符 | ~35,000字 |
| 倍增率 | **47倍** |
| 生成文件 | 14个 |
| 处理时间 | ~15分钟 |
| 输出大小 | 168KB |

---

## 🎨 配图建议

根据 `03-guidelines.md`，推荐配图5-6张：

| 序号 | 配图类型 | 用途 | 推荐工具 |
|------|---------|------|---------|
| 1 | 系统架构图 | 展示全貌 | Draw.io / Excalidraw |
| 2 | 对比表格 | 可视化对比 | Google Sheets / Excel |
| 3 | 功能模块导图 | 展示模块 | Mermaid / Xmind |
| 4 | 部署架构图 | 部署说明 | Visio / Lucidchart |
| 5 | 数据流程图 | 流程说明 | Mermaid / Draw.io |

---

## 💬 常见问题

### Q: 命令执行多久？
**A**: 约15分钟完成全部5个阶段

### Q: 输出文件在哪里？
**A**: `.claude/articles/<article-name>/` 目录下

### Q: 最重要的文件是哪个？
**A**: `02-draft.md` - 这是您要的最终文章

### Q: 怎么检查处理是否完成？
**A**: 执行 `bash workflow.sh status 00_简介` 查看状态

### Q: 可以中断后重新执行吗？
**A**: 可以，系统支持增量处理和恢复

### Q: 需要配置API密钥吗？
**A**: 不需要，零配置

---

## 🔗 相关文件

- 📖 完整文档：`README.md`
- 📊 工作流报告：`.claude/articles/<article-name>/WORKFLOW_COMPLETION_REPORT.md`
- 🎯 Phase脚本：`.claude/workflow/phases/`
- ⚙️ 配置文件：`.claude/workflow/config/`

---

## 🎉 总结

**您需要做的事情：**

1. ✅ 执行一条命令：`bash run-full-workflow.sh <article-name>`
2. ✅ 等待处理完成
3. ✅ 查看 `02-draft.md` 中的最终文章
4. ✅ 按照 `03-guidelines.md` 制作配图
5. ✅ 按照 `04-checklist.md` 优化排版
6. ✅ 按照 `05-final.md` 完成发布检查

**就这么简单！** 🚀

---

*最后更新：2025-11-01*
