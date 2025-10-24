#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能采集爬虫 - 自动提取标题和生成路径
- 从网页 HTML 中自动提取标题
- 根据标题、URL 和关键字自动生成输出路径
- 支持多种选择器（h1, title, meta 等）
- 自动分类和创建目录

使用方法:
    python3 smart_crawler_auto.py --url "https://example.com/doc"
"""

import os
import re
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from datetime import datetime


class AutoPathCrawler:
    """智能采集爬虫，支持自动路径生成"""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.logs_dir = self.project_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # 标题选择器优先级（从高到低）
        self.title_selectors = [
            'div.title h1',
            'h1.title',
            'div.page-title h1',
            '.main-title h1',
            'h1',
            'title',
            'meta[property="og:title"]',
            'meta[name="description"]'
        ]

        # 内容选择器
        self.content_selectors = [
            'main',
            'article',
            '.main-content',
            '.content',
            '.post-content',
            'body'
        ]

        # 分类关键字映射
        self.category_keywords = {
            '快速开始': '01_快速开始',
            '入门': '01_快速开始',
            'quick': '01_快速开始',
            'start': '01_快速开始',

            '配置': '02_系统配置',
            'config': '02_系统配置',
            'setup': '02_系统配置',
            'install': '02_系统配置',

            '商城': '03_商城功能',
            '商品': '03_商城功能',
            'shop': '03_商城功能',
            'store': '03_商城功能',

            '商户': '04_商户管理',
            'merchant': '04_商户管理',
            'seller': '04_商户管理',

            '订单': '05_交易订单',
            'order': '05_交易订单',
            'transaction': '05_交易订单',

            'api': '06_API文档',
            '接口': '06_API文档',
            '文档': '06_API文档',
        }

    def fetch_url(self, url):
        """获取 URL 内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            print(f"  🔄 正在获取: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"  ❌ 获取失败: {str(e)}")
            return None

    def extract_title(self, html_content):
        """从 HTML 中提取标题"""
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # 尝试各个选择器
        for selector in self.title_selectors:
            try:
                if selector.startswith('meta'):
                    element = soup.select_one(selector)
                    if element:
                        title = element.get('content') or element.get('value')
                        if title:
                            return title.strip()
                else:
                    element = soup.select_one(selector)
                    if element and element.get_text(strip=True):
                        return element.get_text(strip=True)
            except:
                continue

        return None

    def extract_content(self, html_content):
        """从 HTML 中提取主要内容"""
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # 移除脚本和样式
        for tag in soup(['script', 'style', 'meta', 'link']):
            tag.decompose()

        # 尝试各个内容选择器
        for selector in self.content_selectors:
            element = soup.select_one(selector)
            if element:
                return str(element)

        return str(soup)

    def generate_filename(self, title):
        """从标题生成文件名"""
        if not title:
            return None

        # 移除特殊字符
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        # 移除前后空白
        filename = filename.strip()
        # 替换多个空格为单个
        filename = re.sub(r'\s+', '', filename)
        # 限制长度
        filename = filename[:50]

        return f"{filename}.md" if filename else None

    def detect_category(self, url, title):
        """根据 URL 和标题检测分类"""
        # 组合 URL 和标题用于关键字匹配
        text = f"{url} {title}".lower()

        # 匹配关键字找出分类
        max_score = 0
        best_category = '00_其他'

        for keyword, category in self.category_keywords.items():
            if keyword.lower() in text:
                score = len(keyword)  # 更长的匹配优先级更高
                if score > max_score:
                    max_score = score
                    best_category = category

        return best_category

    def generate_output_path(self, url, title):
        """自动生成输出路径"""
        if not title:
            title = "untitled"

        # 检测分类
        category = self.detect_category(url, title)

        # 生成文件名
        filename = self.generate_filename(title)
        if not filename:
            filename = "document.md"

        # 组合路径
        output_path = self.docs_dir / category / filename

        return str(output_path), category, filename

    def convert_to_markdown(self, html_content, base_url):
        """将 HTML 转换为 Markdown"""
        try:
            from markdownify import markdownify as md
            markdown = md(html_content)
            return markdown.strip()
        except:
            # 如果没有 markdownify，使用简单转换
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            return text.strip()

    def save_document(self, filepath, content):
        """保存文档到指定路径"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✅ 已保存: {filepath}")
        return True

    def log_result(self, url, title, output_path, status):
        """记录采集结果"""
        log_file = self.logs_dir / f"collect_{datetime.now().strftime('%Y%m%d')}.log"

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'title': title,
            'output_path': output_path,
            'status': status
        }

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def crawl(self, url):
        """采集单个 URL"""
        print(f"\n📝 处理 URL: {url}")

        # 获取网页内容
        html = self.fetch_url(url)
        if not html:
            self.log_result(url, 'N/A', 'N/A', 'failed')
            return False

        # 提取标题
        title = self.extract_title(html)
        print(f"  📌 提取标题: {title}")

        # 生成输出路径
        output_path, category, filename = self.generate_output_path(url, title)
        print(f"  📁 输出路径: {output_path}")
        print(f"  🏷️  分类: {category}")
        print(f"  📄 文件名: {filename}")

        # 提取内容
        content_html = self.extract_content(html)
        if not content_html:
            print(f"  ❌ 无法提取内容")
            self.log_result(url, title, output_path, 'failed')
            return False

        # 转换为 Markdown
        markdown = self.convert_to_markdown(content_html, url)

        # 保存
        if self.save_document(output_path, markdown):
            self.log_result(url, title, output_path, 'success')
            return True
        else:
            self.log_result(url, title, output_path, 'failed')
            return False

    def generate_report(self):
        """生成采集报告"""
        report_file = self.logs_dir / f"report_{datetime.now().strftime('%Y%m%d')}.md"

        # 统计结果
        docs = {}
        for root, dirs, files in os.walk(self.docs_dir):
            for file in files:
                if file.endswith('.md'):
                    rel_path = Path(root).relative_to(self.docs_dir)
                    if str(rel_path) not in docs:
                        docs[str(rel_path)] = []
                    docs[str(rel_path)].append(file)

        # 生成报告
        report = "# 采集报告\n\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += "## 采集结果\n\n"

        total_files = 0
        for category, files in sorted(docs.items()):
            report += f"### {category}\n"
            for file in files:
                report += f"- {file}\n"
                total_files += 1

        report += f"\n**总计: {total_files} 个文件**\n"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n📊 报告已生成: {report_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='智能采集爬虫 - 自动提取标题和生成路径')
    parser.add_argument('--url', type=str, help='要采集的 URL')
    parser.add_argument('--file', type=str, help='包含 URL 的文件')
    parser.add_argument('--report', action='store_true', help='生成采集报告')

    args = parser.parse_args()

    project_root = "/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc"
    crawler = AutoPathCrawler(project_root)

    if args.report:
        crawler.generate_report()
        return

    if args.url:
        crawler.crawl(args.url)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]

        success = 0
        failed = 0
        for url in urls:
            if crawler.crawl(url):
                success += 1
            else:
                failed += 1

        print(f"\n📊 采集完成: 成功 {success} 个, 失败 {failed} 个")
        crawler.generate_report()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
