# 📋 文章写作自动化工作流系统 - 方案设计

## 🎯 目标

用户只需：
1. 提供一份 `.md` 文件和配置参数
2. 执行一条命令：`bash workflow.sh article-name`
3. 系统自动执行5个阶段，生成完整的文章和所有辅助文件
4. 每个阶段都有检查点，可以中断/继续

---

## 📦 推荐方案：混合型自动化系统

### 架构设计

```
My_Doc/
├─ .claude/
│  ├─ workflow/                    ← 核心工作流目录
│  │  ├─ workflow.sh              ← 主控制脚本（入口）
│  │  ├─ phases/                  ← 各阶段处理脚本
│  │  │  ├─ phase1-plan.py        ← 内容规划
│  │  │  ├─ phase2-draft.py       ← 初稿生成
│  │  │  ├─ phase3-illustrations.py ← 配图指南生成
│  │  │  ├─ phase4-format.py      ← 排版优化
│  │  │  └─ phase5-publish.py     ← 发布检查
│  │  ├─ templates/               ← 模板库
│  │  │  ├─ article-template.md   ← 文章模板
│  │  │  ├─ guide-template.md     ← 指南模板
│  │  │  └─ checklist-template.md ← 检查清单模板
│  │  ├─ config/                  ← 配置文件
│  │  │  ├─ default-config.json   ← 默认配置
│  │  │  └─ project-config.json   ← 项目级配置
│  │  └─ utils/                   ← 工具库
│  │     ├─ markdown-utils.py     ← Markdown处理
│  │     ├─ file-utils.py         ← 文件操作
│  │     └─ logger.py             ← 日志记录
│  │
│  ├─ articles/                    ← 文章工作目录
│  │  └─ {article-name}/          ← 每篇文章的工作目录
│  │     ├─ config.json           ← 文章配置
│  │     ├─ 00-raw-input.md       ← 原始输入
│  │     ├─ 01-planning.md        ← 规划输出
│  │     ├─ 02-draft.md           ← 初稿输出
│  │     ├─ 03-guidelines.md      ← 指南输出
│  │     ├─ 04-checklist.md       ← 检查清单输出
│  │     ├─ 05-final.md           ← 最终输出
│  │     ├─ logs/                 ← 执行日志
│  │     └─ status.json           ← 进度状态
│  │
│  └─ settings.json               ← Claude Code配置
│
├─ docs/01_初步了解/
│  └─ {article-name}.md           ← 最终发布文件（从03-final拷贝）
│
├─ workflow.sh                     ← 顶层快捷脚本
└─ README.md
```

---

## 🔄 工作流程详解

### 入口脚本：`workflow.sh`

```bash
#!/bin/bash

# 使用方式：
# bash workflow.sh init {article-name}          # 初始化新文章
# bash workflow.sh run {article-name}            # 运行所有阶段
# bash workflow.sh phase {article-name} {N}      # 运行特定阶段
# bash workflow.sh resume {article-name}         # 从中断处继续
# bash workflow.sh status {article-name}         # 查看进度
# bash workflow.sh publish {article-name}        # 最终发布

主要职责：
1. 参数校验和解析
2. 读取配置文件
3. 调用Python阶段脚本
4. 管理进度状态
5. 生成执行报告
```

---

## 🐍 阶段脚本设计

### Phase 1: `phase1-plan.py` - 内容规划

**输入**：
```json
{
  "article_name": "crmeb-intro",
  "title": "CRMEB Java多商户商城系统简介",
  "raw_content": "用户提供的原始内容或大纲",
  "target_audiences": ["技术人员", "运营人员", "产品经理"],
  "content_structure": ["导语", "核心特性", "架构", "功能", "对比", "场景", "快速开始", "FAQ"],
  "writing_style": "俏皮有趣，专业准确"
}
```

**输出**：
- 详细的规划文档 (`01-planning.md`)
  - 受众分析
  - 内容框架
  - 字数估算
  - 关键要点清单
  - 配图规划

**示例代码框架**：
```python
def phase1_plan(config, input_file):
    """
    第一阶段：内容规划
    输出：规划文档和配置
    """
    # 1. 读取用户输入
    raw_content = read_markdown(input_file)

    # 2. 分析内容结构
    structure = analyze_structure(raw_content)

    # 3. 为每个受众生成关键点
    for audience in config['target_audiences']:
        generate_audience_focus(audience, structure)

    # 4. 规划配图位置
    illustrations = plan_illustrations(structure)

    # 5. 生成规划文档
    planning_doc = generate_planning_doc(structure, illustrations)

    # 6. 保存输出
    save_output(planning_doc, f"01-planning.md")

    return planning_doc
```

---

### Phase 2: `phase2-draft.py` - 初稿生成

**输入**：
- Phase 1 的规划文档
- 用户提供的原始内容

**输出**：
- 完整的初稿文章 (`02-draft.md`)
  - 完整的Markdown结构
  - 配图占位符
  - 关键词标注
  - 段落分隔合理

**处理逻辑**：
```python
def phase2_draft(config, planning_doc):
    """
    第二阶段：初稿编写
    """
    # 1. 加载规划文档
    plan = load_planning(planning_doc)

    # 2. 读取用户原始内容
    raw_content = read_markdown(config['raw_input'])

    # 3. 用模板生成初稿框架
    draft = load_template("article-template.md")

    # 4. 填充各个章节
    for section in plan['sections']:
        content = extract_section_content(raw_content, section)
        filled = fill_template_section(draft, section, content)
        enrich_content(filled)  # 补充关键词标注、格式

    # 5. 调用Claude API进行内容优化和扩展
    optimized = call_claude_api(
        task="optimize_article",
        content=filled,
        style=config['writing_style'],
        audiences=config['target_audiences']
    )

    # 6. 添加配图占位符
    with_placeholders = add_illustration_placeholders(optimized, plan['illustrations'])

    # 7. 保存输出
    save_output(with_placeholders, "02-draft.md")

    return with_placeholders
```

---

### Phase 3: `phase3-illustrations.py` - 配图指南生成

**输入**：
- 初稿文档
- 规划文档中的配图列表

**输出**：
- 配图制作指南 (`03-guidelines.md`)
  - 每张配图的制作步骤
  - 工具选择和使用教程
  - 质量标准
  - 文件夹结构说明

**处理逻辑**：
```python
def phase3_illustrations(config, draft_doc, planning_doc):
    """
    第三阶段：配图制作指南生成
    """
    # 1. 解析初稿中的配图占位符
    illustrations = extract_illustration_placeholders(draft_doc)

    # 2. 为每张配图选择最适合的工具
    for ill in illustrations:
        tool = select_best_tool(ill['type'], ill['complexity'])
        ill['tool'] = tool

    # 3. 生成配图指南
    guide = generate_illustration_guide(illustrations)

    # 4. 添加工具教程
    guide = add_tool_tutorials(guide, set(tool for tool in illustrations))

    # 5. 添加质量标准和文件夹结构
    guide = add_standards_and_structure(guide)

    # 6. 保存输出
    save_output(guide, "03-guidelines.md")

    return guide
```

---

### Phase 4: `phase4-format.py` - 排版优化

**输入**：
- 初稿文档
- 项目的排版标准配置

**输出**：
- 排版检查清单 (`04-checklist.md`)
  - 标题层级检查
  - 文本格式检查
  - 列表和表格检查
  - 代码块检查
  - 本地预览步骤

**处理逻辑**：
```python
def phase4_format(config, draft_doc):
    """
    第四阶段：排版优化检查清单生成
    """
    # 1. 分析初稿的排版结构
    analysis = analyze_formatting(draft_doc)

    # 2. 对比排版标准
    issues = find_formatting_issues(analysis, config['formatting_standards'])

    # 3. 生成检查清单
    checklist = generate_formatting_checklist(draft_doc)

    # 4. 添加修复建议
    checklist = add_fixing_suggestions(checklist, issues)

    # 5. 添加本地预览说明
    checklist = add_preview_instructions(checklist)

    # 6. 保存输出
    save_output(checklist, "04-checklist.md")

    return checklist
```

---

### Phase 5: `phase5-publish.py` - 发布检查清单

**输入**：
- 完成优化后的初稿
- 发布标准配置

**输出**：
- 最终发布检查清单 (`05-final.md`)
  - 70项发布前检查
  - 质量评分
  - 发布前3小时清单
  - 发布后跟踪指标

**处理逻辑**：
```python
def phase5_publish(config, final_draft):
    """
    第五阶段：最终发布检查清单
    """
    # 1. 分析最终文章质量
    quality_analysis = analyze_article_quality(final_draft)

    # 2. 生成完整的发布检查清单
    checklist = generate_publishing_checklist(final_draft)

    # 3. 计算质量评分
    score = calculate_quality_score(quality_analysis)

    # 4. 添加质量评分
    checklist = add_quality_score(checklist, score)

    # 5. 添加发布后跟踪指标
    checklist = add_tracking_metrics(checklist)

    # 6. 生成最终总结
    summary = generate_summary(quality_analysis, score)

    # 7. 保存输出
    save_output(checklist, "05-final.md")
    save_output(summary, "SUMMARY.md")

    return checklist, summary
```

---

## 📊 进度状态管理

每篇文章有一个 `status.json` 文件：

```json
{
  "article_name": "crmeb-intro",
  "title": "CRMEB Java多商户商城系统简介",
  "created_at": "2024-11-01T10:00:00Z",
  "updated_at": "2024-11-01T15:30:00Z",

  "phases": {
    "phase1": {
      "status": "completed",
      "completed_at": "2024-11-01T10:30:00Z",
      "duration_minutes": 30,
      "output": "01-planning.md"
    },
    "phase2": {
      "status": "completed",
      "completed_at": "2024-11-01T13:00:00Z",
      "duration_minutes": 150,
      "output": "02-draft.md",
      "word_count": 7600
    },
    "phase3": {
      "status": "completed",
      "completed_at": "2024-11-01T14:00:00Z",
      "duration_minutes": 60,
      "output": "03-guidelines.md"
    },
    "phase4": {
      "status": "pending",
      "started_at": null,
      "output": "04-checklist.md"
    },
    "phase5": {
      "status": "pending",
      "output": "05-final.md"
    }
  },

  "quality_score": null,
  "published": false,
  "logs": "logs/execution.log"
}
```

---

## 💻 使用示例

### 场景1：快速启动新文章

```bash
# 1. 初始化新文章
bash workflow.sh init crmeb-intro \
  --title "CRMEB Java多商户商城系统简介" \
  --audiences "技术人员,运营人员,产品经理"

# 2. 准备原始内容
# 编辑 .claude/articles/crmeb-intro/00-raw-input.md

# 3. 执行完整工作流
bash workflow.sh run crmeb-intro

# 输出：
# ✅ Phase 1: 内容规划 (30分钟) ✓
# ✅ Phase 2: 初稿编写 (2.5小时) ✓
# ✅ Phase 3: 配图指南 (1小时) ✓
# ✅ Phase 4: 排版优化 (45分钟) ✓
# ✅ Phase 5: 发布检查 (1小时) ✓
#
# 📊 最终评分: ⭐⭐⭐⭐⭐ (96%)
# 📄 最终文件: docs/01_初步了解/crmeb-intro.md
```

### 场景2：单独执行某个阶段

```bash
# 只运行Phase 2 (初稿编写)
bash workflow.sh phase crmeb-intro 2

# 或运行Phase 2-4
bash workflow.sh phase crmeb-intro 2:4
```

### 场景3：查看进度和恢复

```bash
# 查看当前进度
bash workflow.sh status crmeb-intro

# 输出：
# 文章: CRMEB Java多商户商城系统简介
# 进度: Phase 3 完成 (3/5)
# 预计剩余时间: 2小时45分钟
#
# Phase 1: ✅ 完成 (30分钟)
# Phase 2: ✅ 完成 (2.5小时)
# Phase 3: ✅ 完成 (1小时)
# Phase 4: ⏳ 待进行
# Phase 5: ⏳ 待进行

# 从中断处继续
bash workflow.sh resume crmeb-intro
```

### 场景4：多设备无差异工作

```bash
# 在Mac上开始
cd My_Doc
bash workflow.sh init my-article --title "..."
bash workflow.sh phase my-article 1:3

# 在Windows/Linux上继续（只需复制项目文件夹）
cd My_Doc
bash workflow.sh status my-article
bash workflow.sh resume my-article

# 完全相同的输出和结果！
```

---

## 🔧 配置管理

### 全局配置 (`default-config.json`)

```json
{
  "default_audiences": ["技术人员", "运营人员", "产品经理"],
  "default_writing_style": "俏皮有趣，专业准确",
  "default_word_count_per_section": 800,
  "formatting_standards": {
    "max_heading_level": 3,
    "max_paragraph_length": 4,
    "max_table_columns": 5,
    "max_code_block_lines": 30
  },
  "quality_standards": {
    "min_quality_score": 85,
    "required_illustrations": 4,
    "required_sections": ["导语", "快速开始", "FAQ"]
  },
  "tools": {
    "illustration_tools": {
      "architecture": "excalidraw",
      "flowchart": "mermaid",
      "comparison": "markdown",
      "data": "excel"
    },
    "preview": "vitepress",
    "markdown_linter": "markdownlint"
  },
  "output_paths": {
    "final_article": "docs/01_初步了解/",
    "work_directory": ".claude/articles/",
    "templates_directory": ".claude/workflow/templates/"
  }
}
```

### 项目级配置 (`project-config.json`)

```json
{
  "project_name": "My_Doc",
  "project_description": "多层级方案对比写作系统",
  "documentation_root": "docs/01_初步了解/",
  "vitepress_port": 5174,
  "git_enabled": true,
  "auto_commit": false,
  "notification_enabled": true
}
```

---

## 📝 工作目录结构示例

运行后的文件组织：

```
.claude/articles/crmeb-intro/
├─ config.json                    # 文章配置
├─ status.json                    # 进度状态
├─ 00-raw-input.md               # 用户输入
├─ 01-planning.md                # Phase 1 输出：规划文档
├─ 02-draft.md                   # Phase 2 输出：完整初稿
├─ 03-guidelines.md              # Phase 3 输出：配图指南
├─ 04-checklist.md               # Phase 4 输出：排版检查清单
├─ 05-final.md                   # Phase 5 输出：发布检查清单
├─ logs/
│  ├─ phase1.log                 # Phase 1 执行日志
│  ├─ phase2.log                 # Phase 2 执行日志
│  ├─ phase3.log                 # Phase 3 执行日志
│  ├─ phase4.log                 # Phase 4 执行日志
│  ├─ phase5.log                 # Phase 5 执行日志
│  └─ execution.log              # 完整执行日志
└─ SUMMARY.md                    # 最终完成总结

docs/01_初步了解/
└─ crmeb-intro.md               # 最终发布文件
```

---

## 🎯 额外特性

### 1. 实时进度显示

```bash
bash workflow.sh run crmeb-intro --verbose

# 输出实时进度：
# [████░░░░░░░░░░░░░░] 20%  Phase 1 正在进行...
#    ├─ 分析内容结构 ✓
#    ├─ 分析目标受众 ✓
#    └─ 规划配图位置 ⏳
```

### 2. 并行处理支持

```bash
# 同时处理多篇文章（Phase独立的情况下）
bash workflow.sh run article1 &
bash workflow.sh run article2 &
wait
```

### 3. 自动检查和修复

```bash
bash workflow.sh validate crmeb-intro

# 检查：
# ✓ Markdown语法正确
# ✓ 所有链接有效
# ✗ 配图占位符未填充 (可自动填充)
# ✓ 代码块语言标注完整
```

### 4. 版本控制

```bash
bash workflow.sh version crmeb-intro

# 输出：
# 版本历史：
# v0.3 - 2024-11-01 15:30 - Phase 5完成
# v0.2 - 2024-11-01 14:00 - Phase 3完成
# v0.1 - 2024-11-01 10:00 - 创建
```

### 5. 报告生成

```bash
bash workflow.sh report crmeb-intro

# 生成完整的HTML报告，包含：
# - 进度统计
# - 质量评分详解
# - 每个阶段的输出
# - 问题和建议
```

---

## 🛠️ 技术栈建议

| 组件 | 技术 | 原因 |
|------|------|------|
| **主控制脚本** | Bash | 跨平台，无依赖 |
| **阶段脚本** | Python 3 | 强大的文本处理和API调用 |
| **API集成** | Claude API | 智能内容生成和优化 |
| **Markdown处理** | `python-markdown`, `pymdown-extensions` | 完整的Markdown解析 |
| **数据管理** | JSON | 轻量级配置和状态管理 |
| **日志** | Python logging | 结构化日志记录 |
| **Git集成** | GitPython | 自动版本控制 |

---

## 💡 为什么这个设计很强大

### 1. **完全自动化** ✅
- 用户只需提供原始内容和参数
- 系统自动生成所有5个阶段的输出

### 2. **多设备无差异** ✅
- 所有逻辑用Python，跨Mac/Windows/Linux
- 配置和状态用JSON，易于迁移
- 任何设备上执行同样的命令，得到同样的结果

### 3. **灵活可控** ✅
- 可以运行完整流程，也可以跳过某些阶段
- 可以从中断处恢复
- 每个阶段都有日志和输出

### 4. **可扩展** ✅
- 易于添加新的阶段
- 易于修改配置
- 易于集成其他工具

### 5. **高质量保证** ✅
- 每个阶段都有检查清单
- 自动质量评分
- 可追踪的完整日志

---

## 🚀 下一步实现建议

### 优先级1（核心）
- [ ] `workflow.sh` 主控制脚本
- [ ] `phase2-draft.py` （最关键的阶段）
- [ ] `phase5-publish.py` （质量检查）
- [ ] 配置管理系统

### 优先级2（完整性）
- [ ] 所有5个阶段脚本
- [ ] 进度状态管理
- [ ] 日志系统

### 优先级3（增强）
- [ ] 实时进度显示
- [ ] 自动检查和修复
- [ ] 报告生成

---

## ✨ 总结

这个设计能够：

✅ **完全符合你的需求**
- 一条命令启动整个工作流
- 多设备无差异
- 自动处理所有细节

✅ **超越基本需求**
- 可以恢复中断的工作
- 完整的日志和报告
- 灵活的阶段控制

✅ **为未来扩展**
- 易于添加新功能
- 易于修改流程
- 易于集成新工具

---

**要我立即开始实现这个系统吗？我可以：**
1. 先实现核心部分（workflow.sh + phase2-draft.py）
2. 然后补充其他阶段
3. 最后添加高级特性

你想从哪里开始？
