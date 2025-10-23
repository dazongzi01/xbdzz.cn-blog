#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 内容解析器 - 将 HTML 转换为标准 Markdown
"""

import logging
import re
from typing import Dict, List, Tuple
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup, NavigableString
import hashlib

logger = logging.getLogger(__name__)


class MarkdownParser:
    """HTML 到 Markdown 转换器"""

    def __init__(self, base_url: str = '', resource_dir: str = 'images'):
        self.base_url = base_url
        self.resource_dir = resource_dir
        self.images = []

    def html_to_markdown(self, html: str, title: str = '') -> str:
        """将 HTML 内容转换为 Markdown"""
        soup = BeautifulSoup(html, 'html.parser')

        # 移除脚本和样式
        for script in soup(['script', 'style', 'nav', 'footer']):
            script.decompose()

        markdown = ''

        # 添加标题
        if title:
            markdown += f'# {title}\n\n'

        # 处理主要内容
        for element in soup.children:
            if isinstance(element, NavigableString):
                text = str(element).strip()
                if text:
                    markdown += text + '\n\n'
            else:
                markdown += self._element_to_markdown(element) + '\n'

        return self._clean_markdown(markdown)

    def _element_to_markdown(self, element) -> str:
        """递归转换 HTML 元素为 Markdown"""
        if isinstance(element, NavigableString):
            return str(element)

        tag = element.name

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag[1])
            text = element.get_text(strip=True)
            return f"\n{'#' * level} {text}\n"

        elif tag == 'p':
            text = self._process_inline_elements(element)
            return f"{text}\n"

        elif tag in ['ul', 'ol']:
            return self._process_list(element, tag == 'ol')

        elif tag == 'li':
            text = self._process_inline_elements(element)
            return f"- {text}\n"

        elif tag == 'a':
            text = element.get_text(strip=True)
            href = element.get('href', '#')
            href = urljoin(self.base_url, href) if self.base_url else href
            return f'[{text}]({href})'

        elif tag == 'img':
            return self._process_image(element)

        elif tag in ['code', 'kbd']:
            return f"`{element.get_text()}`"

        elif tag == 'pre':
            code_block = element.find('code')
            if code_block:
                language = self._extract_language(code_block)
                code = code_block.get_text()
                return f"```{language}\n{code}\n```\n"
            return f"```\n{element.get_text()}\n```\n"

        elif tag == 'blockquote':
            text = self._process_inline_elements(element)
            return f"> {text}\n"

        elif tag == 'table':
            return self._process_table(element)

        elif tag in ['strong', 'b']:
            text = self._process_inline_elements(element)
            return f"**{text}**"

        elif tag in ['em', 'i']:
            text = self._process_inline_elements(element)
            return f"*{text}*"

        elif tag == 'br':
            return '\n'

        elif tag in ['div', 'section', 'article']:
            return self._process_container(element)

        else:
            return self._process_container(element)

    def _process_inline_elements(self, element) -> str:
        """处理内联元素"""
        text = ''
        for child in element.children:
            if isinstance(child, NavigableString):
                text += str(child).strip()
            else:
                text += self._element_to_markdown(child)
        return text

    def _process_list(self, element, ordered: bool = False) -> str:
        """处理列表"""
        items = element.find_all('li', recursive=False)
        markdown = '\n'

        for i, item in enumerate(items, 1):
            prefix = f"{i}. " if ordered else "- "
            text = self._process_inline_elements(item)
            markdown += f"{prefix}{text}\n"

        return markdown + '\n'

    def _process_image(self, img_element) -> str:
        """处理图片"""
        src = img_element.get('src', '')
        alt = img_element.get('alt', 'image')

        if src:
            # 转换为绝对 URL
            src = urljoin(self.base_url, src) if self.base_url else src
            self.images.append({'src': src, 'alt': alt})

            # 返回 Markdown 格式
            return f"![{alt}]({src})"

        return ''

    def _process_table(self, table_element) -> str:
        """处理表格"""
        rows = table_element.find_all('tr')
        if not rows:
            return ''

        markdown = '\n'

        # 处理表头
        headers = []
        for th in rows[0].find_all(['th', 'td']):
            headers.append(th.get_text(strip=True))

        if headers:
            markdown += '| ' + ' | '.join(headers) + ' |\n'
            markdown += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'

            # 处理表体
            for row in rows[1:]:
                cells = []
                for td in row.find_all('td'):
                    cells.append(td.get_text(strip=True))

                if cells:
                    markdown += '| ' + ' | '.join(cells) + ' |\n'

        return markdown + '\n'

    def _process_container(self, element) -> str:
        """处理容器元素"""
        markdown = ''
        for child in element.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:
                    markdown += text + '\n'
            else:
                markdown += self._element_to_markdown(child) + '\n'
        return markdown

    def _extract_language(self, code_element) -> str:
        """提取代码块语言"""
        class_attr = code_element.get('class', [])
        for cls in class_attr:
            if cls.startswith('language-'):
                return cls.replace('language-', '')
        return ''

    def _clean_markdown(self, markdown: str) -> str:
        """清洁 Markdown"""
        # 移除过多的空行
        markdown = re.sub(r'\n{4,}', '\n\n\n', markdown)

        # 移除行尾空格
        lines = [line.rstrip() for line in markdown.split('\n')]
        markdown = '\n'.join(lines)

        # 移除起始和结尾空白
        markdown = markdown.strip()

        return markdown


class DocumentStructureAnalyzer:
    """文档结构分析器 - 分析导航和模块关系"""

    @staticmethod
    def extract_breadcrumb(soup: BeautifulSoup) -> List[Dict]:
        """提取面包屑导航"""
        breadcrumbs = []

        # 尝试多个可能的选择器
        selectors = [
            'nav.breadcrumb',
            'div.breadcrumb',
            '.breadcrumb-nav',
            'ol.breadcrumb'
        ]

        for selector in selectors:
            breadcrumb_elem = soup.select_one(selector)
            if breadcrumb_elem:
                links = breadcrumb_elem.find_all('a')
                breadcrumbs = [
                    {
                        'text': link.get_text(strip=True),
                        'url': link.get('href', '')
                    }
                    for link in links
                ]
                break

        return breadcrumbs

    @staticmethod
    def extract_toc(soup: BeautifulSoup) -> List[Dict]:
        """提取目录"""
        toc = []

        # 查找导航菜单
        nav_selectors = ['nav.sidebar', 'nav.toc', '.doc-nav', '.sidebar']

        for selector in nav_selectors:
            nav = soup.select_one(selector)
            if nav:
                items = DocumentStructureAnalyzer._parse_nav_items(nav)
                toc.extend(items)
                break

        return toc

    @staticmethod
    def _parse_nav_items(nav_element, level: int = 0) -> List[Dict]:
        """递归解析导航项"""
        items = []

        for elem in nav_element.children:
            if isinstance(elem, NavigableString):
                continue

            if elem.name == 'a':
                items.append({
                    'text': elem.get_text(strip=True),
                    'url': elem.get('href', ''),
                    'level': level
                })

            elif elem.name in ['ul', 'ol']:
                items.extend(DocumentStructureAnalyzer._parse_nav_items(elem, level + 1))

        return items


if __name__ == '__main__':
    # 测试示例
    sample_html = '<h1>标题</h1><p>段落文本 <a href="#">链接</a></p>'
    parser = MarkdownParser()
    md = parser.html_to_markdown(sample_html, 'Test')
    print(md)
