#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容清洁器 - 清洗和标准化 Markdown 内容
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class MarkdownCleaner:
    """Markdown 清洁和标准化工具"""

    # 正则表达式模式
    PATTERNS = {
        'multiple_newlines': re.compile(r'\n{4,}'),
        'trailing_spaces': re.compile(r' +$', re.MULTILINE),
        'leading_spaces': re.compile(r'^ +', re.MULTILINE),
        'html_entities': {
            '&nbsp;': ' ',
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&quot;': '"',
            '&apos;': "'",
            '&copy;': '©',
            '&reg;': '®',
            '&times;': '×',
            '&divide;': '÷',
        },
        'empty_links': re.compile(r'\[\s*\]\s*\(\s*\)'),
        'broken_headings': re.compile(r'^#+\s*$', re.MULTILINE),
    }

    @classmethod
    def clean_content(cls, content: str) -> str:
        """执行完整的清洁流程"""
        if not content:
            return ''

        content = cls.remove_html_entities(content)
        content = cls.fix_spacing(content)
        content = cls.remove_empty_elements(content)
        content = cls.standardize_formatting(content)
        content = cls.fix_code_blocks(content)
        content = cls.fix_lists(content)
        content = cls.ensure_proper_spacing(content)

        return content.strip()

    @classmethod
    def remove_html_entities(cls, content: str) -> str:
        """移除 HTML 实体"""
        for entity, replacement in cls.PATTERNS['html_entities'].items():
            content = content.replace(entity, replacement)
        return content

    @classmethod
    def fix_spacing(cls, content: str) -> str:
        """修复间距问题"""
        # 移除过多的空行
        content = cls.PATTERNS['multiple_newlines'].sub('\n\n\n', content)

        # 移除行尾空格
        content = cls.PATTERNS['trailing_spaces'].sub('', content)

        # 修复标题周围的空格
        content = re.sub(r'\n\s*#+\s+', '\n\n# ', content)

        return content

    @classmethod
    def remove_empty_elements(cls, content: str) -> str:
        """移除空元素"""
        # 移除空链接
        content = cls.PATTERNS['empty_links'].sub('', content)

        # 移除空标题
        content = cls.PATTERNS['broken_headings'].sub('', content)

        # 移除只包含空格的行
        lines = content.split('\n')
        lines = [line for line in lines if line.strip()]
        content = '\n'.join(lines)

        return content

    @classmethod
    def standardize_formatting(cls, content: str) -> str:
        """标准化格式"""
        # 标准化强调样式
        content = re.sub(r'__([^_]+)__', r'**\1**', content)  # __ -> **
        content = re.sub(r'_([^_]+)_', r'*\1*', content)  # _ -> *

        # 标准化代码块语言标识
        content = re.sub(r'```(\w+)?', lambda m: '```' + (m.group(1) or ''), content)

        return content

    @classmethod
    def fix_code_blocks(cls, content: str) -> str:
        """修复代码块"""
        # 确保代码块前后有空行
        content = re.sub(r'\n```', '\n\n```', content)
        content = re.sub(r'```\n', '```\n\n', content)

        # 修复未闭合的代码块
        code_blocks = re.findall(r'^```', content, re.MULTILINE)
        if len(code_blocks) % 2 != 0:
            logger.warning("检测到未闭合的代码块")
            content += '\n```'

        return content

    @classmethod
    def fix_lists(cls, content: str) -> str:
        """修复列表格式"""
        lines = content.split('\n')
        fixed_lines = []
        in_list = False

        for i, line in enumerate(lines):
            # 检查是否是列表项
            if re.match(r'^\s*[-*+]\s', line):
                in_list = True

                # 标准化列表项缩进
                match = re.match(r'^(\s*)[-*+]\s(.+)$', line)
                if match:
                    indent = match.group(1)
                    content_part = match.group(2)
                    fixed_lines.append(f"{indent}- {content_part}")
                else:
                    fixed_lines.append(line)

            elif re.match(r'^\s*\d+\.\s', line):
                in_list = True
                fixed_lines.append(line)

            elif in_list and not line.strip():
                fixed_lines.append(line)
                in_list = False

            elif in_list and not re.match(r'^\s*', line):
                in_list = False
                fixed_lines.append(line)

            else:
                fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    @classmethod
    def ensure_proper_spacing(cls, content: str) -> str:
        """确保适当的间距"""
        lines = content.split('\n')
        result = []

        for i, line in enumerate(lines):
            result.append(line)

            # 标题后添加空行
            if line.startswith('#'):
                if i + 1 < len(lines) and lines[i + 1].strip():
                    result.append('')

        return '\n'.join(result)

    @classmethod
    def validate_content(cls, content: str) -> Dict[str, any]:
        """验证内容质量"""
        issues = []

        # 检查是否为空
        if not content.strip():
            issues.append('内容为空')

        # 检查标题
        if not re.search(r'^#+\s+', content, re.MULTILINE):
            issues.append('缺少标题')

        # 检查链接格式
        broken_links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', content)
        for text, url in broken_links:
            if not text or not url:
                issues.append(f'链接格式错误: [{text}]({url})')

        # 检查代码块
        code_count = content.count('```')
        if code_count % 2 != 0:
            issues.append(f'代码块数量不匹配 (找到 {code_count} 个)')

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'content_length': len(content),
            'line_count': len(content.split('\n'))
        }


class PathNormalizer:
    """路径标准化工具"""

    @staticmethod
    def normalize_file_path(title: str, url: str = '') -> str:
        """
        根据标题和 URL 生成标准化的文件路径
        结构: module/chapter/section.md
        """
        # 移除特殊字符
        safe_title = re.sub(r'[^\w\s-]', '', title)

        # 转换为小写，用连字符连接
        safe_title = safe_title.lower().strip().replace(' ', '-')

        # 移除连续的连字符
        safe_title = re.sub(r'-+', '-', safe_title)

        return f"{safe_title}.md"

    @staticmethod
    def extract_hierarchy_from_url(url: str) -> Dict[str, str]:
        """从 URL 提取层级信息"""
        # 这需要根据实际的 URL 结构调整
        # 示例: /module/chapter/25961 -> {'module': 'module', 'chapter': 'chapter', 'page_id': '25961'}
        parts = url.strip('/').split('/')
        return {
            'raw_parts': parts,
            'page_id': parts[-1] if parts else ''
        }

    @staticmethod
    def build_file_path(breadcrumb: List[Dict], title: str) -> str:
        """根据面包屑和标题构建文件路径"""
        if not breadcrumb:
            # 降级处理
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = safe_title.lower().strip().replace(' ', '-')
            return f"{safe_title}.md"

        # 使用面包屑构建路径
        path_parts = [item['text'] for item in breadcrumb[:-1]]
        path_parts.append(title)

        # 清理路径部分
        path_parts = [
            re.sub(r'[^\w\s-]', '', p).lower().strip().replace(' ', '-')
            for p in path_parts
        ]

        # 移除空部分
        path_parts = [p for p in path_parts if p]

        return '/'.join(path_parts) + '.md'


if __name__ == '__main__':
    # 测试示例
    sample = '''
    # 标题

    这是一个段落，有___多___个__空__行。

    &nbsp;&nbsp;&nbsp;

    ```python
    print("hello")
    ```

    - 列表项 1
    - 列表项 2

    '''

    cleaned = MarkdownCleaner.clean_content(sample)
    print("清洁后的内容:")
    print(cleaned)
    print("\n验证结果:")
    print(MarkdownCleaner.validate_content(cleaned))
