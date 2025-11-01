#!/usr/bin/env python3
"""
Phase 3: Illustration Guidelines
Generates detailed guidelines for creating illustrations
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
    parser = argparse.ArgumentParser(description='Phase 3: Illustration Guidelines')
    parser.add_argument('--article', required=True, help='Article name')
    parser.add_argument('--work-dir', required=True, help='Working directory')
    parser.add_argument('--config', required=True, help='Config file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    return parser.parse_args()


def analyze_draft_for_illustrations(draft_content, logger):
    """Analyze draft to identify illustration opportunities"""
    logger.info("Analyzing draft for illustration opportunities...")

    sections = MarkdownUtils.extract_sections(draft_content)
    images = MarkdownUtils.extract_images(draft_content)

    illustration_points = {
        '核心架构': 'Architecture Diagram',
        '业务流程': 'Process Flow Diagram',
        '模块详解': 'Module Structure Diagram',
        '对比分析': 'Comparison Table/Chart',
        '系统设计': 'System Design Diagram'
    }

    existing_images = len(images)
    logger.info(f"Found {existing_images} existing images in draft")

    return illustration_points, existing_images


def create_illustration_guidelines(article_name, config, draft_content, logger):
    """Create detailed illustration guidelines"""
    logger.info("Creating illustration guidelines...")

    title = config.get('title', article_name)
    required_illustrations = config.get('required_illustrations', 4)

    illustration_points, existing_images = analyze_draft_for_illustrations(draft_content, logger)

    guidelines = {
        'article_name': article_name,
        'title': title,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'total_illustrations_needed': required_illustrations,
        'existing_images': existing_images,
        'additional_needed': max(0, required_illustrations - existing_images),
        'illustrations': [
            {
                'number': 1,
                'section': '核心架构',
                'type': 'Architecture Diagram',
                'description': '系统总体架构图，展示各个组件的关系',
                'key_elements': [
                    '前端层',
                    '中间件',
                    '业务层',
                    '数据层',
                    '外部系统接口'
                ],
                'style': '简洁现代，使用蓝色/绿色配色',
                'tools_recommended': ['Figma', 'Draw.io', 'Lucidchart'],
                'file_format': 'PNG/SVG, 1200x800px minimum'
            },
            {
                'number': 2,
                'section': '业务流程',
                'type': 'Process Flow Diagram',
                'description': '完整的业务流程图，展示用户操作流程',
                'key_elements': [
                    '用户操作',
                    '系统处理',
                    '数据存储',
                    '结果输出'
                ],
                'style': '流程清晰，使用不同颜色区分不同阶段',
                'tools_recommended': ['Figma', 'Miro', 'Mermaid'],
                'file_format': 'PNG/SVG, 1400x900px minimum'
            },
            {
                'number': 3,
                'section': '模块详解',
                'type': 'Feature Overview',
                'description': '主要功能模块的可视化展示',
                'key_elements': [
                    '模块1: 功能说明',
                    '模块2: 功能说明',
                    '模块3: 功能说明'
                ],
                'style': '网格布局，每个模块一个图标或截图',
                'tools_recommended': ['Figma', 'Sketch', 'Adobe XD'],
                'file_format': 'PNG/SVG, 1200x600px minimum'
            },
            {
                'number': 4,
                'section': '对比分析',
                'type': 'Comparison Table/Chart',
                'description': '本方案与其他方案的功能对比图',
                'key_elements': [
                    '功能项目',
                    '本方案',
                    '竞品A',
                    '竞品B'
                ],
                'style': '清晰的表格或雷达图展示',
                'tools_recommended': ['Excel', 'Figma', 'Google Sheets'],
                'file_format': 'PNG/SVG, 1200x600px minimum'
            }
        ]
    }

    return guidelines


def generate_guidelines_document(guidelines, logger):
    """Generate illustration guidelines document"""
    logger.info("Generating guidelines document...")

    doc_lines = [
        f"# {guidelines['title']} - 配图制作指南",
        "",
        f"**生成时间**: {guidelines['created_at']}",
        "",
        "> 本文档为配图制作提供详细的指导和要求",
        "",
        "---",
        "",
        "## 📊 配图概览",
        "",
        f"- **总需求量**: {guidelines['total_illustrations_needed']} 张",
        f"- **已有图片**: {guidelines['existing_images']} 张",
        f"- **还需制作**: {guidelines['additional_needed']} 张",
        "",
        "---",
        "",
        "## 🎨 配图详细要求",
        ""
    ]

    for ill in guidelines['illustrations']:
        doc_lines.extend([
            f"### 配图 {ill['number']}: {ill['section']}",
            "",
            f"**类型**: {ill['type']}",
            f"**位置**: {ill['section']}部分",
            "",
            f"**描述**: {ill['description']}",
            "",
            "**关键要素**:",
            ""
        ])

        for element in ill['key_elements']:
            doc_lines.append(f"- {element}")

        doc_lines.extend([
            "",
            f"**推荐风格**: {ill['style']}",
            "",
            f"**推荐工具**: {', '.join(ill['tools_recommended'])}",
            "",
            f"**文件格式**: {ill['file_format']}",
            "",
            "---",
            ""
        ])

    doc_lines.extend([
        "## 🖼️ 制作要点",
        "",
        "### 通用要求",
        "",
        "1. **清晰度**",
        "   - 所有图片分辨率不低于 1200px（宽）",
        "   - 使用高质量的字体和图标",
        "   - 避免模糊、压缩过度",
        "",
        "2. **风格一致性**",
        "   - 所有图片使用统一的配色方案",
        "   - 统一的字体和图标风格",
        "   - 保持视觉层级一致",
        "",
        "3. **易读性**",
        "   - 文字大小合适（最小 12pt）",
        "   - 色彩对比度足够",
        "   - 避免过度装饰",
        "",
        "4. **文件格式**",
        "   - 优先使用 PNG 格式（透明背景）",
        "   - 也可使用 SVG 格式（矢量）",
        "   - 文件大小不超过 2MB",
        "",
        "---",
        "",
        "## 🎯 制作流程",
        "",
        "### 步骤 1: 准备",
        "- 收集参考资料和竞品图片",
        "- 确定配色方案和视觉风格",
        "- 准备设计工具和资源库",
        "",
        "### 步骤 2: 草图",
        "- 绘制初步草图",
        "- 确定布局和信息结构",
        "- 获得反馈意见",
        "",
        "### 步骤 3: 设计",
        "- 完成详细设计",
        "- 添加文字和细节",
        "- 检查清晰度和可读性",
        "",
        "### 步骤 4: 导出",
        "- 导出为指定格式",
        "- 检查文件大小和质量",
        "- 命名标准化",
        "",
        "---",
        "",
        "## 📋 检查清单",
        "",
        "制作完成后，请检查以下项目:",
        "",
        "- [ ] 所有4张图都已制作",
        "- [ ] 分辨率达到要求 (≥1200px)",
        "- [ ] 文件格式正确 (PNG/SVG)",
        "- [ ] 文件大小合理 (<2MB)",
        "- [ ] 配色方案统一",
        "- [ ] 字体风格一致",
        "- [ ] 文字清晰可读",
        "- [ ] 逻辑关系准确",
        "- [ ] 没有拼写错误",
        "- [ ] 图片已集中保存",
        "",
        "---",
        "",
        "## 💡 最佳实践",
        "",
        "1. **使用设计工具**",
        "   - Figma: 最推荐，功能强大，易于协作",
        "   - Draw.io: 流程图和架构图专家",
        "   - Lucidchart: 专业的图表工具",
        "",
        "2. **参考资源**",
        "   - 使用优质的图标库（如 Material Icons）",
        "   - 参考优秀的技术文章配图",
        "   - 保持简洁和专业风格",
        "",
        "3. **常见陷阱**",
        "   - 避免过度装饰，简洁为上",
        "   - 避免使用不相关的动画或特效",
        "   - 避免文字过多，关键信息为主",
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
    log_file = Path(args.work_dir) / 'logs' / 'phase3.log'
    logger = setup_logger('phase3-illustrations', str(log_file))

    try:
        logger.info("=" * 60)
        logger.info("Phase 3: Illustration Guidelines - Starting")
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

        # Create guidelines
        guidelines = create_illustration_guidelines(args.article, config, draft_content, logger)

        # Generate document
        document = generate_guidelines_document(guidelines, logger)

        # Save guidelines document
        guidelines_file = Path(args.work_dir) / '03-guidelines.md'
        FileUtils.write_file(str(guidelines_file), document)
        logger.info(f"Guidelines saved to {guidelines_file}")

        # Save guidelines JSON
        guidelines_json_file = Path(args.work_dir) / '03-guidelines.json'
        FileUtils.write_json(str(guidelines_json_file), guidelines)

        logger.info("Phase 3 completed successfully")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"Error in Phase 3: {str(e)}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == '__main__':
    sys.exit(main())
