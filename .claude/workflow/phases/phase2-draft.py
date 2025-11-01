#!/usr/bin/env python3
"""
Phase 2: Initial Draft Generation
Uses Claude API to generate comprehensive article draft
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import setup_logger, FileUtils, MarkdownUtils, ClaudeAPI


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Phase 2: Initial Draft Generation')
    parser.add_argument('--article', required=True, help='Article name')
    parser.add_argument('--work-dir', required=True, help='Working directory')
    parser.add_argument('--config', required=True, help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    return parser.parse_args()


def prepare_draft_prompt(raw_content, config, plan, logger):
    """Prepare comprehensive draft generation prompt"""
    logger.info("Preparing draft generation prompt...")

    title = config.get('title', 'Article')
    audiences = config.get('audiences', [])
    style = config.get('writing_style', '专业准确')
    word_count = config.get('target_word_count', 5000)

    audiences_str = '\n'.join([f"  - {a}" for a in audiences])

    prompt = f"""请为以下主题生成一篇高质量的技术文章初稿：

**文章标题**: {title}

**目标受众**:
{audiences_str}

**写作风格**: {style}，俏皮有趣，容易理解

**目标字数**: 约 {word_count} 字

**用户提供的原始内容/大纲**:
```
{raw_content}
```

**内容结构要求** (请按以下结构组织):

1. **简介** (150-200字)
   - 一句话定义
   - 核心价值说明
   - 为什么重要

2. **特性概览** (300-400字)
   - 主要特性列表
   - 核心优势说明
   - 对比简述

3. **核心架构** (400-500字)
   - 系统架构说明
   - 技术栈概述
   - 模块划分

4. **模块详解** (600-800字)
   - 逐个说明主要模块
   - 模块功能和作用
   - 配置和使用方法

5. **业务流程** (300-400字)
   - 整体流程说明
   - 关键步骤描述
   - 实际应用示例

6. **对比分析** (400-500字)
   - 与其他方案对比
   - 优劣势分析
   - 选择建议

7. **应用场景** (300-400字)
   - 3个具体应用场景
   - 每个场景的描述
   - 场景适用性分析

8. **快速开始** (200-300字)
   - 环境要求
   - 安装步骤
   - 基础配置

9. **常见问题** (200-300字)
   - 5-10个常见问题
   - 简洁的答案

10. **最佳实践** (200-300字)
    - 性能优化建议
    - 安全建议
    - 常见陷阱避免

**特殊要求**:

1. **多受众适配**:
   - 对技术人员: 包含技术细节、代码示例、最佳实践
   - 对运营人员: 强调功能说明、业务价值、使用方法
   - 对产品经理: 突出特性对比、业务价值、应用场景

2. **内容质量**:
   - 使用清晰的标题和子标题
   - 每个观点都有具体例子或说明
   - 使用表格对比关键概念
   - 包含实际使用场景

3. **格式要求**:
   - 使用 Markdown 格式
   - 适当使用 **加粗** 和 *斜体*
   - 使用 > 引用重要内容
   - 使用代码块展示配置或代码示例
   - 使用列表组织信息

4. **语言要求**:
   - 专业但易理解
   - 避免过度复杂的术语
   - 使用类比帮助理解
   - 保持俏皮有趣的语气

请生成完整的文章初稿，确保：
- 内容准确、完整、有见地
- 适合多个受众阅读
- 可以直接用于发布（需要配图）
- 字数在 {word_count} 字左右
"""

    return prompt


def generate_draft_with_claude(prompt, logger):
    """Call Claude API to generate draft"""
    logger.info("Calling Claude API to generate draft...")

    try:
        api = ClaudeAPI()

        system_prompt = """你是一个顶级的技术文章编写专家，具有以下特点：
- 能够用简单易懂的方式解释复杂的技术概念
- 能够为多个不同背景的受众编写内容
- 文笔流畅，内容有趣且专业
- 重视实际应用和具体例子
- 能够构建清晰的逻辑结构

请按照要求生成高质量的技术文章初稿。"""

        draft = api.call_api(
            prompt=prompt,
            system=system_prompt,
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.7
        )

        logger.info(f"Draft generated successfully ({len(draft)} characters)")
        return draft

    except Exception as e:
        logger.error(f"Error calling Claude API: {str(e)}")
        raise


def optimize_draft(draft, audiences, logger):
    """Post-process and optimize the draft"""
    logger.info("Optimizing draft...")

    # Sanitize markdown
    draft = MarkdownUtils.sanitize_markdown(draft)

    # Calculate word count
    word_count = MarkdownUtils.get_word_count_estimate(draft)
    logger.info(f"Draft word count estimate: {word_count}")

    # Extract and validate structure
    headings = MarkdownUtils.extract_headings(draft)
    logger.info(f"Found {len(headings)} headings in draft")

    return draft


def generate_draft_document(article_name, raw_content, config, plan, logger):
    """Generate Phase 2 output (draft)"""
    logger.info("Generating initial draft...")

    try:
        # Prepare prompt
        prompt = prepare_draft_prompt(raw_content, config, plan, logger)

        # Generate draft using Claude
        draft = generate_draft_with_claude(prompt, logger)

        # Optimize draft
        draft = optimize_draft(draft, config.get('audiences', []), logger)

        # Calculate word count (no footer added - keep document clean)
        word_count = MarkdownUtils.get_word_count_estimate(draft)

        # Save draft
        draft_file = Path(config.get('work_dir', '.')) / '02-draft.md' if 'work_dir' in config else Path('.') / '02-draft.md'

        # Since config doesn't have work_dir passed directly, use sys.argv approach
        # But we'll handle this differently - the parent should pass work_dir

        return draft, word_count

    except Exception as e:
        logger.error(f"Error generating draft: {str(e)}")
        raise


def main():
    """Main execution"""
    args = parse_arguments()

    # Setup logger
    log_file = Path(args.work_dir) / 'logs' / 'phase2.log'
    logger = setup_logger('phase2-draft', str(log_file))

    try:
        logger.info("=" * 60)
        logger.info("Phase 2: Initial Draft Generation - Starting")
        logger.info("=" * 60)

        # Read configuration
        config = FileUtils.read_json(args.config)
        logger.info(f"Article: {args.article}")
        logger.info(f"Title: {config.get('title', args.article)}")

        # Read raw content
        raw_input_file = Path(args.work_dir) / '00-raw-input.md'
        if not raw_input_file.exists():
            logger.error(f"Raw input file not found: {raw_input_file}")
            return 1

        raw_content = FileUtils.read_file(str(raw_input_file))
        logger.info(f"Read raw content: {len(raw_content)} characters")

        # Read planning document if it exists
        plan = {}
        plan_file = Path(args.work_dir) / '01-planning.json'
        if plan_file.exists():
            plan = FileUtils.read_json(str(plan_file))
            logger.info("Read planning document from Phase 1")

        # Generate draft
        logger.info("Starting draft generation with Claude API...")
        prompt = prepare_draft_prompt(raw_content, config, plan, logger)

        draft = generate_draft_with_claude(prompt, logger)

        # Optimize and save
        draft = optimize_draft(draft, config.get('audiences', []), logger)

        word_count = MarkdownUtils.get_word_count_estimate(draft)

        # No metadata footer - keep document clean
        final_draft = draft

        # Save draft
        draft_file = Path(args.work_dir) / '02-draft.md'
        FileUtils.write_file(str(draft_file), final_draft)
        logger.info(f"Draft saved to {draft_file}")

        # Save draft metadata
        draft_meta = {
            'article_name': args.article,
            'title': config.get('title', args.article),
            'word_count': word_count,
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'model': 'claude-3-5-sonnet-20241022',
            'audiences': config.get('audiences', []),
            'target_word_count': config.get('target_word_count', 5000)
        }

        meta_file = Path(args.work_dir) / '02-draft.json'
        FileUtils.write_json(str(meta_file), draft_meta)

        logger.info("Phase 2 completed successfully")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"Error in Phase 2: {str(e)}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == '__main__':
    sys.exit(main())
