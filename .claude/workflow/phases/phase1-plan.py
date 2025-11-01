#!/usr/bin/env python3
"""
Phase 1: Content Planning
Analyzes raw content and creates a detailed content plan
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
    parser = argparse.ArgumentParser(description='Phase 1: Content Planning')
    parser.add_argument('--article', required=True, help='Article name')
    parser.add_argument('--work-dir', required=True, help='Working directory')
    parser.add_argument('--config', required=True, help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    return parser.parse_args()


def analyze_raw_content(raw_content, config, logger):
    """Analyze raw content and extract structure"""
    logger.info("Analyzing raw content structure...")

    sections = MarkdownUtils.extract_sections(raw_content)
    headings = MarkdownUtils.extract_headings(raw_content)
    links = MarkdownUtils.extract_links(raw_content)
    images = MarkdownUtils.extract_images(raw_content)
    word_count = MarkdownUtils.get_word_count_estimate(raw_content)

    analysis = {
        'sections_count': len(sections),
        'headings_count': len(headings),
        'links_count': len(links),
        'images_count': len(images),
        'estimated_word_count': word_count,
        'main_sections': list(sections.keys())[:5],  # Top 5 sections
        'structure_quality': 'good' if len(headings) > 2 else 'needs_improvement'
    }

    logger.info(f"Found {len(sections)} sections and {len(headings)} headings")
    return analysis


def create_content_plan(article_name, config, analysis, raw_content, logger):
    """Create detailed content plan"""
    logger.info("Creating content plan...")

    audiences = config.get('audiences', ['技术人员', '运营人员', '产品经理'])
    title = config.get('title', article_name)
    style = config.get('writing_style', '俏皮有趣，专业准确')

    plan = {
        'article_name': article_name,
        'title': title,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'content_analysis': analysis,
        'audiences': audiences,
        'writing_style': style,
        'target_word_count': config.get('target_word_count', 5000),
        'required_illustrations': config.get('required_illustrations', 4),
        'outline': {
            '简介': {
                'description': '一句话定义，核心价值说明',
                'target_audience': 'all',
                'key_points': ['定义', '价值', '应用场景']
            },
            '特性概览': {
                'description': '列举主要特性和优势',
                'target_audience': ['技术人员', '产品经理'],
                'key_points': ['核心特性', '优势对比', '功能列表']
            },
            '核心架构': {
                'description': '详细说明系统架构和设计',
                'target_audience': ['技术人员'],
                'key_points': ['架构图', '模块划分', '技术栈']
            },
            '模块详解': {
                'description': '逐个解释主要模块功能',
                'target_audience': ['技术人员', '运营人员'],
                'key_points': ['模块功能', '使用场景', '配置说明']
            },
            '业务流程': {
                'description': '说明整个业务流程',
                'target_audience': ['运营人员', '产品经理'],
                'key_points': ['流程图', '关键步骤', '使用实例']
            },
            '对比分析': {
                'description': '与其他方案对比',
                'target_audience': ['产品经理', '决策者'],
                'key_points': ['功能对比', '优劣分析', '选择建议']
            },
            '应用场景': {
                'description': '具体应用场景和使用例子',
                'target_audience': 'all',
                'key_points': ['场景1', '场景2', '场景3']
            },
            '快速开始': {
                'description': '入门指南和基础配置',
                'target_audience': ['技术人员'],
                'key_points': ['环境要求', '安装步骤', '初始配置']
            },
            '常见问题': {
                'description': 'FAQ部分',
                'target_audience': 'all',
                'key_points': ['技术问题', '使用问题', '故障排除']
            },
            '最佳实践': {
                'description': '最佳实践和技巧',
                'target_audience': ['技术人员', '运营人员'],
                'key_points': ['性能优化', '安全建议', '扩展方法']
            }
        },
        'audience_segments': {
            '技术人员': {
                'focus': ['架构', '代码示例', '最佳实践'],
                'tone': '专业、准确、深入',
                'content_ratio': '40%'
            },
            '运营人员': {
                'focus': ['功能说明', '业务流程', '配置指南'],
                'tone': '清晰、实用、易理解',
                'content_ratio': '35%'
            },
            '产品经理': {
                'focus': ['特性对比', '业务价值', '应用场景'],
                'tone': '专业、有见地、战略性',
                'content_ratio': '25%'
            }
        },
        'key_messages': [
            f"什么是{title}",
            f"为什么需要{title}",
            f"{title}的核心优势",
            f"如何使用{title}",
            f"{title}的适用场景"
        ],
        'illustrations_plan': {
            'count': config.get('required_illustrations', 4),
            'types': ['架构图', '流程图', '功能截图', '对比表格'],
            'placement': {
                '核心架构': '架构图',
                '业务流程': '流程图',
                '模块详解': '功能截图',
                '对比分析': '对比表格'
            }
        },
        'estimated_timeline': {
            'phase2_draft': '4-8小时',
            'phase3_illustrations': '1小时',
            'phase4_format': '45分钟',
            'phase5_publish': '1小时',
            'total': '8-12小时'
        }
    }

    logger.info("Content plan created successfully")
    return plan


def generate_planning_document(plan, article_name, work_dir, logger):
    """Generate Phase 1 output document"""
    logger.info("Generating planning document...")

    doc_lines = [
        f"# {plan['title']} - 内容规划文档",
        "",
        f"**生成时间**: {plan['created_at']}",
        "",
        "---",
        "",
        "## 📋 内容分析",
        "",
        "### 分析结果",
        ""
    ]

    analysis = plan['content_analysis']
    doc_lines.extend([
        f"- **现有内容部分数**: {analysis['sections_count']}",
        f"- **标题数量**: {analysis['headings_count']}",
        f"- **参考链接**: {analysis['links_count']}",
        f"- **图片数量**: {analysis['images_count']}",
        f"- **预计字数**: 约 {analysis['estimated_word_count']} 字",
        f"- **结构质量**: {analysis['structure_quality']}",
        "",
        "---",
        "",
        "## 🎯 内容规划",
        "",
        f"**目标字数**: {plan['target_word_count']} 字",
        f"**所需插图**: {plan['required_illustrations']} 张",
        f"**写作风格**: {plan['writing_style']}",
        "",
        "### 目标受众",
        ""
    ])

    for audience, info in plan['audience_segments'].items():
        doc_lines.extend([
            f"#### {audience}",
            f"- **内容占比**: {info['content_ratio']}",
            f"- **语气**: {info['tone']}",
            f"- **关键关注**: {', '.join(info['focus'])}",
            ""
        ])

    doc_lines.extend([
        "---",
        "",
        "## 📑 内容大纲",
        ""
    ])

    for section_name, section_info in plan['outline'].items():
        doc_lines.extend([
            f"### {section_name}",
            f"**说明**: {section_info['description']}",
            f"**关键点**: {', '.join(section_info['key_points'])}",
            ""
        ])

    doc_lines.extend([
        "---",
        "",
        "## 🖼️ 配图规划",
        ""
    ])

    illustrations = plan['illustrations_plan']
    for placement, ill_type in illustrations['placement'].items():
        doc_lines.append(f"- **{placement}**: {ill_type}")

    doc_lines.extend([
        "",
        "---",
        "",
        "## ⏱️ 预计时间表",
        ""
    ])

    for phase, duration in plan['estimated_timeline'].items():
        doc_lines.append(f"- **{phase}**: {duration}")

    doc_lines.extend([
        "",
        "---",
        "",
        "## 💡 关键信息点",
        ""
    ])

    for i, msg in enumerate(plan['key_messages'], 1):
        doc_lines.append(f"{i}. {msg}")

    doc_lines.extend([
        "",
        "---",
        "",
        f"**计划完成**: {datetime.utcnow().isoformat().split('T')[0]}",
        ""
    ])

    document = '\n'.join(doc_lines)

    # Save planning document
    planning_file = Path(work_dir) / '01-planning.md'
    FileUtils.write_file(str(planning_file), document)

    # Save plan JSON
    plan_json_file = Path(work_dir) / '01-planning.json'
    FileUtils.write_json(str(plan_json_file), plan)

    logger.info(f"Planning document saved to {planning_file}")
    return document


def main():
    """Main execution"""
    args = parse_arguments()

    # Setup logger
    log_file = Path(args.work_dir) / 'logs' / 'phase1.log'
    logger = setup_logger('phase1-plan', str(log_file))

    try:
        logger.info("=" * 60)
        logger.info("Phase 1: Content Planning - Starting")
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

        # Analyze content
        analysis = analyze_raw_content(raw_content, config, logger)

        # Create content plan
        plan = create_content_plan(args.article, config, analysis, raw_content, logger)

        # Generate planning document
        generate_planning_document(plan, args.article, args.work_dir, logger)

        logger.info("Phase 1 completed successfully")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"Error in Phase 1: {str(e)}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == '__main__':
    sys.exit(main())
