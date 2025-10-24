#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能采集爬虫 - 保留 URL 的版本
- 采集网页内容
- 更新采集状态时保留粘贴的 URL
- 自动提取标题和生成路径
- 记录采集日志

使用方法:
    python3 smart_crawler_preserve_url.py TODO_CAIJI.md
"""

import os
import re
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


class PreservingCrawler:
    """保留 URL 的智能采集爬虫"""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.logs_dir = self.project_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # 标题选择器优先级
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
        content_selectors = ['main', 'article', '.main-content', '.content', '.post-content', 'body']
        for selector in content_selectors:
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
        filename = filename.strip()
        filename = re.sub(r'\s+', '', filename)
        filename = filename[:50]

        return f"{filename}.md" if filename else None

    def detect_category(self, url, title, output_path):
        """根据输出路径和标题检测分类"""
        # 优先从输出路径提取分类
        if 'docs/' in output_path:
            match = re.search(r'docs/([^/]+)/', output_path)
            if match:
                return match.group(1)

        # 其次从标题和 URL 匹配关键字
        text = f"{url} {title}".lower()

        max_score = 0
        best_category = '00_其他'

        for keyword, category in self.category_keywords.items():
            if keyword.lower() in text:
                score = len(keyword)
                if score > max_score:
                    max_score = score
                    best_category = category

        return best_category

    def convert_to_markdown(self, html_content):
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

    def update_todo_status(self, todo_file, task_section, new_status):
        """
        更新 TODO_CAIJI.md 中的采集状态
        保留 URL 不删除
        """
        with open(todo_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找要更新的任务部分
        # 格式: ### 任务名\n- 采集状态: [ ]\n- 输出路径: ...\n- URL: ...
        pattern = rf'({re.escape(task_section)}\n- 采集状态:) (\[[ x✅❌]\])'

        # 替换状态，但保留其他行
        updated_content = re.sub(pattern, rf'\1 {new_status}', content)

        with open(todo_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"  📝 已更新状态: {task_section}")

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

    def crawl(self, url, output_path, task_section):
        """采集单个 URL"""
        if not url or not url.strip():
            print(f"  ⚠️  跳过空的 URL")
            return False

        print(f"\n📝 处理 URL: {url}")

        # 获取网页内容
        html = self.fetch_url(url)
        if not html:
            self.log_result(url, 'N/A', output_path, 'failed')
            self.update_todo_status(
                self.project_root / "TODO_CAIJI.md",
                task_section,
                '[❌]'
            )
            return False

        # 提取标题
        title = self.extract_title(html)
        print(f"  📌 提取标题: {title}")

        # 提取内容
        content_html = self.extract_content(html)
        if not content_html:
            print(f"  ❌ 无法提取内容")
            self.log_result(url, title, output_path, 'failed')
            self.update_todo_status(
                self.project_root / "TODO_CAIJI.md",
                task_section,
                '[❌]'
            )
            return False

        # 转换为 Markdown
        markdown = self.convert_to_markdown(content_html)

        # 保存
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)

            print(f"  ✅ 已保存: {output_path}")

            # 更新状态（保留 URL）
            self.update_todo_status(
                self.project_root / "TODO_CAIJI.md",
                task_section,
                '[✅]'
            )

            self.log_result(url, title, output_path, 'success')
            return True
        except Exception as e:
            print(f"  ❌ 保存失败: {str(e)}")
            self.log_result(url, title, output_path, 'failed')
            self.update_todo_status(
                self.project_root / "TODO_CAIJI.md",
                task_section,
                '[❌]'
            )
            return False

    def process_todo_file(self, todo_file):
        """处理 TODO_CAIJI.md 文件"""
        with open(todo_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_section = None
        url_to_crawl = None
        output_path = None
        success_count = 0
        failed_count = 0

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # 检测任务标题 ### xxx
            if line.startswith('###'):
                current_section = line
                # 读取接下来的几行找 URL 和输出路径
                j = i + 1
                url_to_crawl = None
                output_path = None

                while j < len(lines) and not lines[j].strip().startswith('###'):
                    current_line = lines[j].strip()
                    if current_line.startswith('- URL:'):
                        # 提取 URL
                        url_part = current_line.replace('- URL:', '').strip()
                        if url_part:
                            url_to_crawl = url_part
                    elif current_line.startswith('- 输出路径:'):
                        # 提取输出路径
                        path_match = re.search(r'`([^`]+)`', current_line)
                        if path_match:
                            output_path = str(self.project_root / path_match.group(1))
                    j += 1

                # 如果找到了 URL 和输出路径，则采集
                if url_to_crawl and output_path:
                    if self.crawl(url_to_crawl, output_path, current_section):
                        success_count += 1
                    else:
                        failed_count += 1

            i += 1

        return success_count, failed_count


def main():
    import argparse

    parser = argparse.ArgumentParser(description='保留 URL 的智能采集爬虫')
    parser.add_argument('todo_file', nargs='?', default='TODO_CAIJI.md',
                       help='TODO_CAIJI.md 文件路径')

    args = parser.parse_args()

    project_root = "/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc"
    crawler = PreservingCrawler(project_root)

    todo_file = Path(project_root) / args.todo_file

    if not todo_file.exists():
        print(f"❌ 错误: {todo_file} 文件不存在")
        return

    print(f"📂 开始处理: {todo_file}")
    success, failed = crawler.process_todo_file(todo_file)

    print(f"\n📊 采集完成: 成功 {success} 个, 失败 {failed} 个")


if __name__ == "__main__":
    main()
