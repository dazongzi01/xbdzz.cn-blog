# 🗺️ 文章写作自动化工作流系统 - 实现路线图

## 📋 项目总览

**项目名称**：文章写作自动化工作流系统
**状态**：✅ 系统设计完成，待实现
**目标**：完全自动化的文章写作流程，一键启动，多设备无差异

---

## ✅ 已完成的工作

### 1. 系统架构设计 ✅
- **文件**：`.claude/workflow-system-proposal.md`
- **内容**：
  - 完整的系统架构图
  - 5个阶段的详细说明
  - 技术栈选择和原因
  - 使用场景和示例

### 2. 主控制脚本 ✅
- **文件**：`workflow.sh`
- **大小**：13KB
- **功能**：
  - 8个核心命令
  - 完整的参数解析
  - 错误处理和恢复
  - 彩色终端输出
  - JSON配置和状态管理

### 3. 完整使用指南 ✅
- **文件**：`WORKFLOW_SYSTEM_GUIDE.md`
- **大小**：20KB
- **内容**：
  - 快速开始（5分钟）
  - 命令参考
  - 使用场景
  - 故障排除
  - 最佳实践

---

## ⏳ 待实现的工作

### Priority 1: 核心实现 (1-2周)

#### Phase 2: 初稿生成脚本 ⭐ 最关键
**文件**：`.claude/workflow/phases/phase2-draft.py`

**功能**：
```python
def phase2_draft(config, planning_doc):
    # 1. 加载规划和原始内容
    # 2. 加载文章模板
    # 3. 调用Claude API优化内容
    # 4. 填充模板和格式化
    # 5. 添加配图占位符
    # 6. 生成完整初稿
```

**预期输出**：
- `02-draft.md`（7600+字）
- 完整的Markdown格式
- 关键词标注
- 配图占位符

**实现方案**：
```python
# 伪代码
1. 初始化日志和进度显示
2. 读取并解析输入文件
3. 使用Claude API调用
   - 优化内容结构
   - 为不同受众讲解
   - 添加关键词和格式
4. 填充模板
5. 生成输出文件
6. 记录完成统计
```

#### Phase 5: 发布检查脚本
**文件**：`.claude/workflow/phases/phase5-publish.py`

**功能**：
- 质量分析
- 生成检查清单
- 计算质量评分
- 生成完成总结

#### 模板库
**位置**：`.claude/workflow/templates/`

**文件**：
- `article-template.md`（文章模板）
- `guide-template.md`（指南模板）
- `checklist-template.md`（检查清单模板）

#### 配置管理
**文件**：
- `.claude/workflow/config/default-config.json`
- `.claude/workflow/config/project-config.json`

---

### Priority 2: 完整功能 (2-3周)

#### Phase 1-4 脚本实现
- `phase1-plan.py`
- `phase3-illustrations.py`
- `phase4-format.py`

#### 工具库
**位置**：`.claude/workflow/utils/`

**模块**：
- `markdown-utils.py`（Markdown处理）
- `file-utils.py`（文件操作）
- `logger.py`（日志记录）
- `claude-api.py`（Claude API封装）

#### 状态管理系统
- 进度跟踪
- 自动恢复机制
- JSON配置管理

---

### Priority 3: 增强特性 (3-4周)

#### 实时进度显示
- 进度条
- 实时日志输出
- 时间估计

#### 自动检查和修复
- Markdown语法检查
- 链接有效性检查
- 自动修复功能

#### Git集成
- 自动提交
- 版本管理
- 变更跟踪

#### 报告生成
- HTML报告
- PDF导出
- 统计数据展示

---

## 📁 完整的目录结构

```
My_Doc/
│
├─ workflow.sh ✅
├─ WORKFLOW_SYSTEM_GUIDE.md ✅
├─ .claude/
│  ├─ workflow-system-proposal.md ✅
│  │
│  ├─ workflow/
│  │  ├─ workflow.sh (主脚本的备份/软链接)
│  │  │
│  │  ├─ phases/
│  │  │  ├─ phase1-plan.py ⏳
│  │  │  ├─ phase2-draft.py ⏳⭐
│  │  │  ├─ phase3-illustrations.py ⏳
│  │  │  ├─ phase4-format.py ⏳
│  │  │  └─ phase5-publish.py ⏳
│  │  │
│  │  ├─ templates/
│  │  │  ├─ article-template.md ⏳
│  │  │  ├─ guide-template.md ⏳
│  │  │  └─ checklist-template.md ⏳
│  │  │
│  │  ├─ config/
│  │  │  ├─ default-config.json ⏳
│  │  │  └─ project-config.json ⏳
│  │  │
│  │  └─ utils/
│  │     ├─ __init__.py
│  │     ├─ markdown-utils.py ⏳
│  │     ├─ file-utils.py ⏳
│  │     ├─ logger.py ⏳
│  │     └─ claude-api.py ⏳
│  │
│  ├─ articles/
│  │  └─ {article-name}/
│  │     ├─ config.json
│  │     ├─ status.json
│  │     ├─ 00-raw-input.md
│  │     ├─ 01-planning.md
│  │     ├─ 02-draft.md
│  │     ├─ 03-guidelines.md
│  │     ├─ 04-checklist.md
│  │     ├─ 05-final.md
│  │     ├─ SUMMARY.md
│  │     └─ logs/
│  │
│  ├─ settings.local.json ✅ (已存在)
│  └─ SYSTEM_IMPLEMENTATION_ROADMAP.md ✅ (本文件)
│
├─ docs/01_初步了解/
│  ├─ (现有文档)
│  └─ {article-name}.md (发布文件)
│
└─ (其他项目文件)

✅ = 已完成
⏳ = 待实现
```

---

## 🔄 实现步骤详解

### Step 1: 基础框架搭建 (Day 1)

```bash
# 创建目录结构
mkdir -p .claude/workflow/{phases,templates,config,utils}

# 创建__init__.py
touch .claude/workflow/__init__.py
touch .claude/workflow/utils/__init__.py

# 创建配置文件
# (从workflow-system-proposal.md中的示例复制)
```

### Step 2: 工具库实现 (Day 1-2)

**utils/logger.py**：日志记录
```python
import logging

class Logger:
    def __init__(self, name, log_file):
        self.logger = logging.getLogger(name)
        # 配置文件和终端输出

    def info(self, msg): ...
    def success(self, msg): ...
    def error(self, msg): ...
    def warn(self, msg): ...
```

**utils/file-utils.py**：文件操作
```python
def read_file(path): ...
def write_file(path, content): ...
def read_json(path): ...
def write_json(path, data): ...
```

**utils/markdown-utils.py**：Markdown处理
```python
def extract_headings(md): ...
def extract_code_blocks(md): ...
def add_placeholders(md, placeholders): ...
def count_words(md): ...
```

**utils/claude-api.py**：Claude API封装
```python
def call_claude(
    task: str,
    content: str,
    style: str,
    audiences: list
) -> str:
    """
    调用Claude API进行内容优化
    """
    # 构建prompt
    # 调用API
    # 返回结果
```

### Step 3: 模板库创建 (Day 2)

**templates/article-template.md**：
```markdown
# {{title}}

## 导语
> {{intro}}

## 目录导航
(自动生成)

## 一句话定义
{{definition}}

## 核心特性表
(自动生成)

## (其他章节)

...
```

### Step 4: Phase 2 实现 (Day 3-4) ⭐ 优先级最高

这是最关键的阶段，实现逻辑：

```python
# phase2-draft.py
import sys
import json
from pathlib import Path
from datetime import datetime

def phase2_draft(article_name, work_dir, config_file):
    """
    Phase 2: 初稿生成
    """
    # 1. 初始化
    logger = Logger("phase2", f"{work_dir}/logs/phase2.log")
    logger.info("开始 Phase 2: 初稿生成")

    # 2. 加载配置
    config = load_json(config_file)
    raw_input = read_file(f"{work_dir}/00-raw-input.md")
    planning = read_file(f"{work_dir}/01-planning.md")

    # 3. 加载模板
    template = read_file(TEMPLATES_DIR / "article-template.md")

    # 4. 处理内容（使用Claude API）
    draft = process_content_with_claude(
        raw_input=raw_input,
        planning=planning,
        template=template,
        config=config,
        logger=logger
    )

    # 5. 添加格式和优化
    draft = apply_formatting(draft, config)
    draft = add_illustration_placeholders(draft, planning)

    # 6. 统计信息
    word_count = count_words(draft)
    logger.success(f"初稿完成: {word_count} 字")

    # 7. 保存输出
    output_file = f"{work_dir}/02-draft.md"
    write_file(output_file, draft)

    # 8. 更新状态
    update_status(work_dir, "phase2", "completed", word_count)

    return draft

def process_content_with_claude(
    raw_input, planning, template, config, logger
):
    """
    使用Claude API优化和生成内容
    """
    logger.info("调用Claude API进行内容优化...")

    # 构建prompt
    prompt = f"""
    请帮我完成一篇文章的初稿。

    原始内容：
    {raw_input}

    规划文档：
    {planning}

    配置信息：
    - 标题：{config['title']}
    - 受众：{', '.join(config['audiences'])}
    - 风格：{config['writing_style']}
    - 字数目标：{config.get('target_word_count', 5000)}字

    请：
    1. 按照模板结构组织内容
    2. 为每个受众群体讲解
    3. 添加俏皮有趣的表达
    4. 使用**加粗**标注关键词
    5. 在需要配图的地方标记【配图：...】

    模板：
    {template}
    """

    # 调用Claude API
    response = call_claude_api(prompt)
    return response

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--article", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    phase2_draft(args.article, args.work_dir, args.config)
```

### Step 5: Phase 1, 3, 4, 5 实现 (Day 5-7)

每个阶段都遵循类似的结构：
1. 初始化日志
2. 加载输入
3. 处理逻辑（可能调用Claude API）
4. 生成输出
5. 更新状态

### Step 6: 测试和优化 (Day 8-10)

```bash
# 测试完整工作流
bash workflow.sh init test-article \
  --title "Test Article" \
  --audiences "开发者,运营者"

# 提供测试内容
cp sample-content.md .claude/articles/test-article/00-raw-input.md

# 运行完整工作流
bash workflow.sh run test-article --verbose

# 验证输出
ls -la .claude/articles/test-article/
cat .claude/articles/test-article/SUMMARY.md
```

---

## 📊 实现时间估计

| 任务 | 时间 | 优先级 |
|------|------|--------|
| 工具库实现 | 4小时 | 1 |
| Phase 2 实现 | 6小时 | 1 |
| Phase 5 实现 | 4小时 | 1 |
| 模板库创建 | 2小时 | 1 |
| Phase 1, 3, 4 | 12小时 | 2 |
| 完整测试 | 4小时 | 2 |
| 文档完善 | 2小时 | 2 |
| 增强特性 | 8小时 | 3 |
| **总计** | **42小时** | |

**分布**：
- 第1周：核心实现（20小时）✅
- 第2周：完整功能（16小时）✅
- 第3周：增强特性（8小时）✅

---

## 🧪 测试计划

### 单元测试

```python
# tests/test_phase2.py
def test_phase2_basic():
    """测试基本的初稿生成"""
    result = phase2_draft(...)
    assert len(result) > 5000
    assert "【配图" in result

def test_phase2_formatting():
    """测试格式化"""
    result = phase2_draft(...)
    assert result.count("#") > 0
    assert "**" in result
```

### 集成测试

```bash
# 测试完整工作流
bash test_workflow.sh

# 验证输出文件
bash test_output_files.sh

# 验证质量评分
bash test_quality_score.sh
```

### 多设备测试

- ✅ macOS
- ⏳ Windows (WSL)
- ⏳ Linux

---

## 📝 依赖管理

### Python 依赖

```txt
# requirements.txt
python >= 3.8
anthropic >= 0.7.0
python-dotenv >= 0.19.0
pyyaml >= 6.0
```

### 系统要求

- Bash 4.0+
- Python 3.8+
- 互联网连接（调用Claude API）
- Git（可选，用于版本控制）

---

## 🔐 API 密钥管理

**存储位置**：`~/.claude-code/config.json` 或环境变量

```bash
# 设置方式
export ANTHROPIC_API_KEY="your-key-here"

# 或创建.env文件
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

---

## 🚀 部署步骤

### 本地部署

```bash
# 1. 克隆或复制系统文件
cd My_Doc

# 2. 安装Python依赖
pip install -r .claude/workflow/requirements.txt

# 3. 配置API密钥
export ANTHROPIC_API_KEY="your-key"

# 4. 测试系统
bash workflow.sh --help

# 5. 创建第一篇文章
bash workflow.sh init my-first-article
```

### 云端部署（可选）

可以部署到：
- GitHub Actions
- GitLab CI
- Jenkins
- 自建服务器

---

## 📚 文档计划

### 待编写文档

- [ ] API参考文档
- [ ] 贡献指南
- [ ] 系统维护指南
- [ ] 常见问题解答
- [ ] 最佳实践指南

---

## 🎯 成功标准

### Phase 1: 核心系统完成

```
✅ workflow.sh 可以正常执行所有命令
✅ Phase 2 可以生成 5000+ 字的初稿
✅ 配置和状态正确管理
✅ 可以在不同设备上继续工作
✅ 所有日志正确记录
```

### Phase 2: 完整功能

```
✅ 所有5个阶段都能执行
✅ 可以从任何阶段继续
✅ 完整的错误恢复机制
✅ 自动生成质量评分
```

### Phase 3: 增强特性

```
✅ 实时进度显示
✅ 自动检查和修复
✅ Git集成
✅ 报告生成
```

---

## 🔗 相关文档

| 文档 | 位置 | 用途 |
|------|------|------|
| 系统设计 | `.claude/workflow-system-proposal.md` | 完整的架构设计 |
| 使用指南 | `WORKFLOW_SYSTEM_GUIDE.md` | 用户使用手册 |
| 本文档 | `.claude/SYSTEM_IMPLEMENTATION_ROADMAP.md` | 实现计划 |

---

## ✨ 总结

这个自动化工作流系统的实现分为三个阶段：

### 第1周：核心实现
- 工具库 + Phase 2 + Phase 5 + 模板
- 目标：完成最关键的初稿生成功能

### 第2周：完整功能
- 所有5个阶段脚本
- 状态管理和错误恢复
- 完整的测试

### 第3周：增强特性
- 实时进度、自动检查、Git集成
- 文档完善
- 多设备支持验证

---

## 🎉 预期成果

完成后，你将拥有：

✅ **一套完整的自动化系统**
- 5个阶段的自动处理
- 多设备无差异工作
- 完整的质量保证

✅ **可重复使用的工作流**
- 适用于所有新文章
- 保存所有过程
- 持续优化

✅ **企业级的内容管理**
- 版本控制
- 质量跟踪
- 完整的文档库

---

**开始实现吧！🚀**

根据这个路线图逐步实现，即可完成整个自动化系统。

预计3周内完成核心功能，4周内完成所有功能。
