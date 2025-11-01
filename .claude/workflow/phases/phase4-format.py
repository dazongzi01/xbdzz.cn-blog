#!/usr/bin/env python3
"""
Phase 4: Format Optimization
Checks and optimizes article formatting
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import setup_logger, FileUtils, MarkdownUtils


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Phase 4: Format Optimization')
    parser.add_argument('--article', required=True, help='Article name')
    parser.add_argument('--work-dir', required=True, help='Working directory')
    parser.add_argument('--config', required=True, help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    return parser.parse_args()


def check_markdown_formatting(content, logger):
    """Check markdown formatting quality"""
    logger.info("Checking markdown formatting...")

    issues = []
    suggestions = []

    # Check heading structure
    headings = MarkdownUtils.extract_headings(content)
    if not headings:
        issues.append("No headings found in content")
    elif headings[0][0] != 1:
        issues.append("First heading should be H1 (# Title)")

    # Check for consistent heading levels
    heading_levels = [h[0] for h in headings]
    if heading_levels != sorted(set(heading_levels)):
        suggestions.append("Consider organizing headings in hierarchical order")

    # Check code blocks
    code_blocks = MarkdownUtils.extract_code_blocks(content)
    if len(code_blocks) > 0:
        logger.info(f"Found {len(code_blocks)} code blocks")
        for i, (lang, code) in enumerate(code_blocks, 1):
            if not lang:
                suggestions.append(f"Code block {i} should specify language for better highlighting")

    # Check links
    links = MarkdownUtils.extract_links(content)
    broken_link_count = 0
    for text, url in links:
        if url.startswith('#'):
            # Internal link - check if it references a valid heading
            pass
        logger.debug(f"Found link: [{text}]({url})")

    # Check images
    images = MarkdownUtils.extract_images(content)
    logger.info(f"Found {len(images)} images")

    # Check tables
    tables = MarkdownUtils.extract_tables(content)
    if tables:
        logger.info(f"Found {len(tables)} tables")

    # Check line length
    lines = content.split('\n')
    long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 120 and not line.strip().startswith('|')]
    if len(long_lines) > 5:
        suggestions.append(f"Consider breaking up long lines (found {len(long_lines)} lines > 120 chars)")

    # Check paragraph length
    paragraphs = content.split('\n\n')
    long_paragraphs = [i for i, p in enumerate(paragraphs, 1) if len(p) > 500 and not p.startswith('#')]
    if len(long_paragraphs) > 3:
        suggestions.append(f"Consider breaking up long paragraphs (found {len(long_paragraphs)} paragraphs > 500 chars)")

    # Check word count
    word_count = MarkdownUtils.get_word_count_estimate(content)

    return {
        'issues': issues,
        'suggestions': suggestions,
        'word_count': word_count,
        'heading_count': len(headings),
        'code_blocks': len(code_blocks),
        'links': len(links),
        'images': len(images),
        'tables': len(tables),
        'avg_line_length': sum(len(line) for line in lines) // len(lines) if lines else 0
    }


def create_optimization_checklist(article_name, config, format_check, logger):
    """Create format optimization checklist"""
    logger.info("Creating optimization checklist...")

    title = config.get('title', article_name)
    target_word_count = config.get('target_word_count', 5000)

    checklist = {
        'article_name': article_name,
        'title': title,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'format_check': format_check,
        'optimization_items': {
            'structure': [
                {'item': '标题层级正确 (H1 -> H2 -> H3)', 'status': 'pending', 'priority': 'high'},
                {'item': '有清晰的目录结构', 'status': 'pending', 'priority': 'high'},
                {'item': '各部分长度比例合理', 'status': 'pending', 'priority': 'medium'},
                {'item': '段落之间过渡顺畅', 'status': 'pending', 'priority': 'medium'}
            ],
            'typography': [
                {'item': '使用正确的标点符号', 'status': 'pending', 'priority': 'high'},
                {'item': '中英文间距正确', 'status': 'pending', 'priority': 'medium'},
                {'item': '没有多余的空行', 'status': 'pending', 'priority': 'low'},
                {'item': '缩进和格式一致', 'status': 'pending', 'priority': 'medium'}
            ],
            'content': [
                {'item': '所有观点都有支撑示例', 'status': 'pending', 'priority': 'high'},
                {'item': '没有重复内容', 'status': 'pending', 'priority': 'high'},
                {'item': '没有拼写错误', 'status': 'pending', 'priority': 'high'},
                {'item': '术语使用一致', 'status': 'pending', 'priority': 'medium'}
            ],
            'media': [
                {'item': '所有图片都已合适地插入', 'status': 'pending', 'priority': 'high'},
                {'item': '所有代码块都有语言标记', 'status': 'pending', 'priority': 'medium'},
                {'item': '表格格式正确', 'status': 'pending', 'priority': 'medium'},
                {'item': '所有链接都有效', 'status': 'pending', 'priority': 'high'}
            ],
            'readability': [
                {'item': f'字数在目标范围内 (~{target_word_count})', 'status': 'pending', 'priority': 'high'},
                {'item': '段落长度合理 (建议300-400字)', 'status': 'pending', 'priority': 'medium'},
                {'item': '句子长度合理', 'status': 'pending', 'priority': 'medium'},
                {'item': '使用清晰的列表和要点', 'status': 'pending', 'priority': 'medium'}
            ]
        }
    }

    return checklist


def generate_optimization_document(checklist, logger):
    """Generate optimization checklist document"""
    logger.info("Generating optimization document...")

    format_check = checklist['format_check']
    optimization = checklist['optimization_items']

    doc_lines = [
        f"# {checklist['title']} - 排版优化检查清单",
        "",
        f"**生成时间**: {checklist['created_at']}",
        "",
        "> 本清单用于检查和优化文章格式和排版",
        "",
        "---",
        "",
        "## 📊 当前格式检查结果",
        "",
        "### 基本统计",
        ""
    ]

    doc_lines.extend([
        f"- 字数: {format_check['word_count']} 字",
        f"- 标题数: {format_check['heading_count']}",
        f"- 代码块: {format_check['code_blocks']}",
        f"- 链接: {format_check['links']}",
        f"- 图片: {format_check['images']}",
        f"- 表格: {format_check['tables']}",
        f"- 平均行长: {format_check['avg_line_length']} 字符",
        ""
    ])

    if format_check['issues']:
        doc_lines.extend([
            "### 发现的问题",
            ""
        ])
        for issue in format_check['issues']:
            doc_lines.append(f"⚠️ {issue}")
        doc_lines.append("")

    if format_check['suggestions']:
        doc_lines.extend([
            "### 改进建议",
            ""
        ])
        for suggestion in format_check['suggestions']:
            doc_lines.append(f"💡 {suggestion}")
        doc_lines.append("")

    doc_lines.extend([
        "---",
        "",
        "## ✅ 优化检查清单",
        ""
    ])

    for category, items in optimization.items():
        doc_lines.extend([
            f"### {category.upper()}",
            ""
        ])

        for item in items:
            checkbox = "[ ]" if item['status'] == 'pending' else "[x]"
            priority_icon = "🔴" if item['priority'] == 'high' else ("🟡" if item['priority'] == 'medium' else "🟢")
            doc_lines.append(f"{checkbox} {priority_icon} {item['item']}")

        doc_lines.append("")

    doc_lines.extend([
        "---",
        "",
        "## 📋 具体优化建议",
        "",
        "### 1. 标题和结构优化",
        "",
        "- 确保 H1 标题只有一个（文章标题）",
        "- H2 标题用于主要章节",
        "- H3 标题用于小节",
        "- 避免跳过标题级别（如从 H1 直接到 H3）",
        "",
        "### 2. 文本优化",
        "",
        "- 移除多余的空行（最多两个连续空行）",
        "- 确保中英文之间有空格",
        "- 修复任何拼写或语法错误",
        "- 确保术语使用一致",
        "",
        "### 3. 列表和格式",
        "",
        "- 使用无序列表 (-) 或有序列表 (1.)",
        "- 列表项应该简洁（一行为佳）",
        "- 复杂内容使用块引用 (>) 突出显示",
        "- 代码行内用 `反引号` 包围",
        "",
        "### 4. 代码块",
        "",
        "- 所有代码块都要指定语言（如 ```python）",
        "- 代码应该有注释解释关键部分",
        "- 避免过长的代码示例（尽量不超过20行）",
        "",
        "### 5. 链接和图片",
        "",
        "- 链接使用描述性锚文本，而不是 'click here'",
        "- 外部链接应该在新窗口打开（如果支持）",
        "- 所有图片应该有 alt 文本",
        "- 图片应该在适当的位置（接近相关文本）",
        "",
        "### 6. 可读性",
        "",
        "- 保持段落长度在 300-400 字",
        "- 避免过长的句子（建议不超过 20 个词）",
        "- 使用短句和变化的句式保持兴趣",
        "- 重要概念使用 **加粗** 突出显示",
        "",
        "---",
        "",
        "## 🔧 优化工具和资源",
        "",
        "### 检查工具",
        "",
        "- **Markdown 验证**: 使用在线 Markdown 编辑器预览",
        "- **拼写检查**: 浏览器拼写检查或专用工具",
        "- **可读性检查**: Hemingway Editor 或类似工具",
        "",
        "### 本地预览",
        "",
        "- 使用 VitePress 本地预览最终效果",
        "- 检查在不同屏幕宽度下的显示效果",
        "- 确保所有链接在本地都能正常工作",
        "",
        "---",
        "",
        "## ✨ 完成清单",
        "",
        "- [ ] 所有基本统计检查完成",
        "- [ ] 所有问题都已修复",
        "- [ ] 所有建议都已采纳或明确拒绝",
        "- [ ] 格式检查清单全部完成",
        "- [ ] 本地预览检查通过",
        "- [ ] 准备进入 Phase 5: 发布检查",
        "",
        "---",
        "",
        f"**计划完成**: {datetime.utcnow().isoformat().split('T')[0]}",
        ""
    ])

    document = '\n'.join(doc_lines)
    return document


def main():
    """Main execution"""
    args = parse_arguments()

    # Setup logger
    log_file = Path(args.work_dir) / 'logs' / 'phase4.log'
    logger = setup_logger('phase4-format', str(log_file))

    try:
        logger.info("=" * 60)
        logger.info("Phase 4: Format Optimization - Starting")
        logger.info("=" * 60)

        # Read configuration
        config = FileUtils.read_json(args.config)
        logger.info(f"Article: {args.article}")

        # Read draft
        draft_file = Path(args.work_dir) / '02-draft.md'
        if not draft_file.exists():
            logger.error(f"Draft file not found: {draft_file}")
            return 1

        draft_content = FileUtils.read_file(str(draft_file))
        logger.info(f"Read draft: {len(draft_content)} characters")

        # Check formatting
        format_check = check_markdown_formatting(draft_content, logger)

        # Create checklist
        checklist = create_optimization_checklist(args.article, config, format_check, logger)

        # Generate document
        document = generate_optimization_document(checklist, logger)

        # Save checklist document
        checklist_file = Path(args.work_dir) / '04-checklist.md'
        FileUtils.write_file(str(checklist_file), document)
        logger.info(f"Checklist saved to {checklist_file}")

        # Save checklist JSON
        checklist_json_file = Path(args.work_dir) / '04-checklist.json'
        FileUtils.write_json(str(checklist_json_file), checklist)

        logger.info("Phase 4 completed successfully")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"Error in Phase 4: {str(e)}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == '__main__':
    sys.exit(main())
