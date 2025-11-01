#!/usr/bin/env python3
"""
Phase 5: Publishing Checklist
Final quality check before publishing
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
    parser = argparse.ArgumentParser(description='Phase 5: Publishing Checklist')
    parser.add_argument('--article', required=True, help='Article name')
    parser.add_argument('--work-dir', required=True, help='Working directory')
    parser.add_argument('--config', required=True, help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    return parser.parse_args()


def perform_quality_checks(content, logger):
    """Perform comprehensive quality checks"""
    logger.info("Performing quality checks...")

    checks = {
        'completeness': {},
        'accuracy': {},
        'readability': {},
        'format': {},
        'seo': {}
    }

    # Completeness checks
    headings = MarkdownUtils.extract_headings(content)
    checks['completeness']['has_title'] = len(headings) > 0
    checks['completeness']['has_sections'] = len(headings) > 3
    checks['completeness']['word_count'] = MarkdownUtils.get_word_count_estimate(content)

    # Accuracy checks
    links = MarkdownUtils.extract_links(content)
    checks['accuracy']['internal_links'] = sum(1 for _, url in links if url.startswith('#'))
    checks['accuracy']['external_links'] = sum(1 for _, url in links if url.startswith('http'))
    checks['accuracy']['has_references'] = len(links) > 0

    # Readability checks
    sections = MarkdownUtils.extract_sections(content)
    checks['readability']['section_count'] = len(sections)
    checks['readability']['avg_section_length'] = sum(len(s) for s in sections.values()) // len(sections) if sections else 0

    images = MarkdownUtils.extract_images(content)
    checks['readability']['image_count'] = len(images)

    tables = MarkdownUtils.extract_tables(content)
    checks['readability']['table_count'] = len(tables)

    code_blocks = MarkdownUtils.extract_code_blocks(content)
    checks['readability']['code_block_count'] = len(code_blocks)

    # Format checks
    lines = content.split('\n')
    checks['format']['line_count'] = len(lines)
    checks['format']['has_empty_lines'] = any(not line.strip() for line in lines)
    checks['format']['consistent_spacing'] = True

    # SEO checks
    title = MarkdownUtils.extract_title(content)
    checks['seo']['has_title'] = len(title) > 0
    checks['seo']['title_length'] = len(title)
    checks['seo']['has_keywords'] = 'Python' in content or 'JavaScript' in content or 'API' in content or '架构' in content

    return checks


def generate_quality_score(checks, logger):
    """Calculate quality score based on checks"""
    logger.info("Calculating quality score...")

    score_components = {
        'completeness': 0,
        'accuracy': 0,
        'readability': 0,
        'format': 0,
        'seo': 0
    }

    # Completeness score
    completeness = checks['completeness']
    if completeness['has_title']:
        score_components['completeness'] += 20
    if completeness['has_sections']:
        score_components['completeness'] += 20
    if 3000 <= completeness['word_count'] <= 10000:
        score_components['completeness'] += 20

    # Accuracy score
    accuracy = checks['accuracy']
    if accuracy['has_references']:
        score_components['accuracy'] += 20
    if accuracy['internal_links'] > 0 or accuracy['external_links'] > 0:
        score_components['accuracy'] += 20

    # Readability score
    readability = checks['readability']
    if readability['section_count'] >= 5:
        score_components['readability'] += 15
    if readability['image_count'] >= 3:
        score_components['readability'] += 15
    if readability['avg_section_length'] >= 300:
        score_components['readability'] += 10

    # Format score
    format_check = checks['format']
    if format_check['line_count'] > 100:
        score_components['format'] += 20
    if format_check['has_empty_lines']:
        score_components['format'] += 15

    # SEO score
    seo = checks['seo']
    if seo['has_title']:
        score_components['seo'] += 15
    if 10 <= seo['title_length'] <= 60:
        score_components['seo'] += 15
    if seo['has_keywords']:
        score_components['seo'] += 20

    overall_score = min(100, sum(score_components.values()) // 5)
    return overall_score, score_components


def create_final_checklist(article_name, config, checks, quality_score, logger):
    """Create final publishing checklist"""
    logger.info("Creating final publishing checklist...")

    title = config.get('title', article_name)

    checklist_items = [
        # Content quality
        {
            'category': 'Content Quality',
            'items': [
                {'task': 'Title is clear and descriptive', 'required': True},
                {'task': 'Content is accurate and well-researched', 'required': True},
                {'task': 'No spelling or grammar errors', 'required': True},
                {'task': 'Consistent terminology throughout', 'required': True},
                {'task': 'All statements have supporting evidence or examples', 'required': True},
                {'task': 'No misleading or outdated information', 'required': True},
                {'task': 'Content flows logically from section to section', 'required': True},
                {'task': 'Key concepts are clearly defined', 'required': True},
                {'task': 'Examples are relevant and helpful', 'required': True},
                {'task': 'Technical accuracy verified', 'required': True}
            ]
        },
        # Structure and Organization
        {
            'category': 'Structure and Organization',
            'items': [
                {'task': 'Article has clear H1 title', 'required': True},
                {'task': 'Proper heading hierarchy (H1 > H2 > H3)', 'required': True},
                {'task': 'Introduction sets up the topic well', 'required': True},
                {'task': 'Body is well-organized with logical sections', 'required': True},
                {'task': 'Conclusion summarizes key points', 'required': True},
                {'task': 'Transitions between sections are smooth', 'required': True},
                {'task': 'Table of contents (if needed) is accurate', 'required': False}
            ]
        },
        # Formatting and Style
        {
            'category': 'Formatting and Style',
            'items': [
                {'task': 'Markdown is valid and renders correctly', 'required': True},
                {'task': 'No excessive use of bold or italic', 'required': True},
                {'task': 'Lists are properly formatted and consistent', 'required': True},
                {'task': 'Code blocks have language specified', 'required': True},
                {'task': 'Tables are properly formatted', 'required': True},
                {'task': 'Quotes are properly formatted', 'required': True},
                {'task': 'Font size and spacing are appropriate', 'required': True},
                {'task': 'No double spaces or unusual whitespace', 'required': True}
            ]
        },
        # Images and Media
        {
            'category': 'Images and Media',
            'items': [
                {'task': 'All required images are present', 'required': True},
                {'task': 'Images are high quality and clear', 'required': True},
                {'task': 'Images are properly sized and optimized', 'required': True},
                {'task': 'Images have descriptive alt text', 'required': True},
                {'task': 'Image captions are clear and helpful', 'required': True},
                {'task': 'Videos or interactive content works properly', 'required': False},
                {'task': 'All media files are accessible', 'required': True}
            ]
        },
        # Links and References
        {
            'category': 'Links and References',
            'items': [
                {'task': 'All internal links are correct and working', 'required': True},
                {'task': 'All external links are current and valid', 'required': True},
                {'task': 'Link anchor text is descriptive', 'required': True},
                {'task': 'References are properly cited', 'required': True},
                {'task': 'No broken or redirected links', 'required': True},
                {'task': 'External links open in appropriate context', 'required': False}
            ]
        },
        # Audience Alignment
        {
            'category': 'Audience Alignment',
            'items': [
                {'task': 'Content is appropriate for target audience', 'required': True},
                {'task': 'Technical level is suitable for audience', 'required': True},
                {'task': 'Jargon is explained or avoided', 'required': True},
                {'task': 'Examples are relevant to audience', 'required': True},
                {'task': 'Tone is appropriate and engaging', 'required': True},
                {'task': 'Content addresses audience pain points', 'required': True}
            ]
        },
        # SEO and Metadata
        {
            'category': 'SEO and Metadata',
            'items': [
                {'task': 'Title is SEO-friendly and descriptive', 'required': True},
                {'task': 'Keywords are naturally incorporated', 'required': True},
                {'task': 'Meta description is compelling (if applicable)', 'required': False},
                {'task': 'Headings include relevant keywords', 'required': True},
                {'task': 'URL is descriptive and SEO-friendly', 'required': True},
                {'task': 'Article is categorized correctly', 'required': True}
            ]
        },
        # Final Checks
        {
            'category': 'Final Checks',
            'items': [
                {'task': 'Proofread for typos and errors', 'required': True},
                {'task': 'Run through spell checker', 'required': True},
                {'task': 'Preview in actual publishing format', 'required': True},
                {'task': 'Test all interactive elements', 'required': True},
                {'task': 'Verify on mobile devices', 'required': False},
                {'task': 'Get feedback from peer review', 'required': True},
                {'task': 'All feedback has been addressed', 'required': True}
            ]
        }
    ]

    return {
        'article_name': article_name,
        'title': title,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'quality_checks': checks,
        'quality_score': quality_score,
        'checklist_items': checklist_items
    }


def generate_final_document(checklist, logger):
    """Generate final publishing checklist document"""
    logger.info("Generating final publishing document...")

    doc_lines = [
        f"# {checklist['title']} - 发布前最终检查清单",
        "",
        f"**生成时间**: {checklist['created_at']}",
        "",
        "> 本清单用于确保文章在发布前满足所有质量要求",
        "",
        "---",
        "",
        "## 📊 质量评分",
        ""
    ]

    # Quality score display
    quality_score = checklist['quality_score']
    score_bar = "█" * (quality_score // 10) + "░" * ((100 - quality_score) // 10)
    doc_lines.extend([
        f"**总体评分**: {quality_score}/100",
        f"**评分进度**: {score_bar}",
        "",
        "评分说明:",
        "- 90-100: 优秀（可以直接发布）",
        "- 80-89: 良好（建议小幅调整）",
        "- 70-79: 中等（建议重要部分调整）",
        "- 60-69: 一般（建议较大调整）",
        "- 低于 60: 不合格（建议重新审视）",
        "",
        "---",
        "",
        "## ✅ 检查清单",
        ""
    ])

    total_items = 0
    for category in checklist['checklist_items']:
        doc_lines.extend([
            f"### {category['category']}",
            ""
        ])

        for item in category['items']:
            checkbox = "[ ]"
            required = "(必需)" if item['required'] else "(可选)"
            doc_lines.append(f"{checkbox} {item['task']} {required}")
            total_items += 1

        doc_lines.append("")

    doc_lines.extend([
        "---",
        "",
        "## 📋 检查统计",
        ""
    ])

    checks = checklist['quality_checks']
    doc_lines.extend([
        f"**文章统计**:",
        f"- 字数: {checks['completeness']['word_count']} 字",
        f"- 标题数: {checks['readability']['section_count']} 个",
        f"- 图片: {checks['readability']['image_count']} 张",
        f"- 表格: {checks['readability']['table_count']} 个",
        f"- 代码块: {checks['readability']['code_block_count']} 个",
        f"- 链接: {checks['accuracy']['internal_links'] + checks['accuracy']['external_links']} 个",
        "",
        "---",
        "",
        "## 🎯 发布前准备",
        "",
        "### 步骤 1: 最终审查",
        "",
        "- [ ] 完整阅读一遍全文",
        "- [ ] 检查所有格式是否正确",
        "- [ ] 验证所有链接和图片",
        "- [ ] 检查移动端显示效果",
        "",
        "### 步骤 2: 内容优化",
        "",
        "- [ ] 确认没有过时信息",
        "- [ ] 验证所有代码示例的准确性",
        "- [ ] 确保所有参考资源仍然有效",
        "- [ ] 更新任何相关的统计数据",
        "",
        "### 步骤 3: 元数据准备",
        "",
        "- [ ] 准备文章的 slug/URL",
        "- [ ] 准备文章的摘要或描述",
        "- [ ] 选择相关的标签和分类",
        "- [ ] 准备社交媒体分享内容",
        "",
        "### 步骤 4: 发布配置",
        "",
        "- [ ] 检查发布日期和时间",
        "- [ ] 检查作者信息",
        "- [ ] 配置发布权限",
        "- [ ] 准备发布后的推广策略",
        "",
        "---",
        "",
        "## 🚀 发布后任务",
        "",
        "- [ ] 验证文章已正确发布",
        "- [ ] 检查所有链接在实时环境中的工作情况",
        "- [ ] 监控评论和反馈",
        "- [ ] 根据反馈进行必要的更新",
        "- [ ] 分享到相关平台",
        "- [ ] 追踪文章的浏览量和互动",
        "",
        "---",
        "",
        "## 💡 发布建议",
        "",
        "1. **最佳发布时间**: 周二至周四上午 10-11 点",
        "2. **社交媒体分享**: 准备多个变体的分享文案",
        "3. **内部通知**: 通知相关团队成员",
        "4. **外部宣传**: 考虑在社区和论坛中分享",
        "5. **后续更新**: 准备定期更新计划",
        "",
        "---",
        "",
        "## 📝 编辑备注",
        "",
        "**关键反馈**:",
        "",
        "- 没有关键反馈（编辑时请填写）",
        "",
        "**改进建议**:",
        "",
        "- 没有改进建议（编辑时请填写）",
        "",
        "---",
        "",
        f"**计划完成**: {datetime.utcnow().isoformat().split('T')[0]}",
        "",
        "**准备发布**: ❌ (完成所有检查后将变为 ✅)",
        ""
    ])

    document = '\n'.join(doc_lines)
    return document


def main():
    """Main execution"""
    args = parse_arguments()

    # Setup logger
    log_file = Path(args.work_dir) / 'logs' / 'phase5.log'
    logger = setup_logger('phase5-publish', str(log_file))

    try:
        logger.info("=" * 60)
        logger.info("Phase 5: Publishing Checklist - Starting")
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

        # Perform quality checks
        checks = perform_quality_checks(draft_content, logger)

        # Calculate quality score
        quality_score, score_components = generate_quality_score(checks, logger)
        logger.info(f"Quality score: {quality_score}/100")

        # Create checklist
        checklist = create_final_checklist(args.article, config, checks, quality_score, logger)

        # Generate document
        document = generate_final_document(checklist, logger)

        # Save final checklist document
        final_file = Path(args.work_dir) / '05-final.md'
        FileUtils.write_file(str(final_file), document)
        logger.info(f"Final checklist saved to {final_file}")

        # Save checklist JSON
        checklist_json_file = Path(args.work_dir) / '05-final.json'
        FileUtils.write_json(str(checklist_json_file), checklist)

        # Create summary
        summary = {
            'article_name': args.article,
            'title': config.get('title', args.article),
            'completion_date': datetime.utcnow().isoformat() + 'Z',
            'quality_score': quality_score,
            'all_phases_complete': True,
            'ready_for_publish': quality_score >= 70,
            'recommendations': [
                "内容已准备好进行最终审查",
                f"质量评分: {quality_score}/100",
                "请按照发布前检查清单进行最终验证",
                "完成所有清单项后可以发布"
            ]
        }

        # Save summary
        summary_file = Path(args.work_dir) / 'SUMMARY.md'
        summary_text = f"""# {config.get('title', args.article)} - 完成总结

**完成时间**: {summary['completion_date']}

## 📊 完成统计

- **质量评分**: {summary['quality_score']}/100
- **所有阶段**: ✅ 完成
- **发布就绪**: {'✅ 可以发布' if summary['ready_for_publish'] else '⚠️ 需要优化后再发布'}

## 📝 建议

{chr(10).join([f"- {rec}" for rec in summary['recommendations']])}

## 📂 输出文件

- `01-planning.md` - 内容规划文档
- `02-draft.md` - 初稿内容（{checks['completeness']['word_count']} 字）
- `03-guidelines.md` - 配图制作指南
- `04-checklist.md` - 排版优化检查清单
- `05-final.md` - 发布检查清单

## 🚀 后续步骤

1. 按照 `05-final.md` 中的检查清单进行最终验证
2. 准备配图（参考 `03-guidelines.md`）
3. 优化排版（参考 `04-checklist.md`）
4. 完成所有检查后发布

---

**系统自动生成** | {datetime.utcnow().isoformat()}
"""
        FileUtils.write_file(str(summary_file), summary_text)

        logger.info("Phase 5 completed successfully")
        logger.info(f"Quality Score: {quality_score}/100")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"Error in Phase 5: {str(e)}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == '__main__':
    sys.exit(main())
