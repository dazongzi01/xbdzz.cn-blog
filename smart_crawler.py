#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CRMEB 文档智能采集系统
- 读取 TODO_CAIJI.md
- 解析待采集任务
- 自动采集和转换
- 更新任务状态
- 同步VitePress配置
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

class DocumentCrawler:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.todo_file = self.project_root / "TODO_CAIJI.md"
        self.config_file = self.docs_dir / ".vitepress" / "config.ts"

    def parse_todo_file(self):
        """解析TODO_CAIJI.md文件"""
        if not self.todo_file.exists():
            print("❌ TODO_CAIJI.md 文件不存在")
            return {}

        with open(self.todo_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析模块和任务
        tasks = {}
        current_module = None

        for line in content.split('\n'):
            # 匹配模块
            module_match = re.match(r'^## 📂 模块 (\d+): (.+)$', line)
            if module_match:
                module_num = module_match.group(1)
                module_name = module_match.group(2)
                current_module = f"{module_num}_{module_name.replace(' ', '')}"
                if current_module not in tasks:
                    tasks[current_module] = []
                continue

            # 匹配任务URL
            if line.strip().startswith('- URL:') and current_module:
                url = line.split(':', 1)[1].strip()
                if url and not url.startswith('['):
                    # 获取上一个任务信息
                    if tasks[current_module]:
                        tasks[current_module][-1]['url'] = url

            # 匹配任务标题和路径
            title_match = re.match(r'### (\d+_\w+)', line)
            if title_match and current_module:
                path_match = None
                status = "[ ]"  # 默认未采集

                tasks[current_module].append({
                    'section': title_match.group(1),
                    'status': status,
                    'url': '',
                    'path': ''
                })

        return tasks

    def fetch_url(self, url):
        """获取URL内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"❌ 获取 {url} 失败: {str(e)}")
            return None

    def convert_to_markdown(self, html_content, base_url):
        """将HTML转换为Markdown"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # 移除脚本和样式
        for tag in soup(['script', 'style']):
            tag.decompose()

        # 转换HTML为Markdown
        markdown = md(str(soup))

        # 处理图片URL
        markdown = self._process_image_urls(markdown, base_url)

        return markdown.strip()

    def _process_image_urls(self, markdown, base_url):
        """处理相对图片URL"""
        def replace_url(match):
            url = match.group(1)
            if not url.startswith(('http://', 'https://', '/')):
                url = urljoin(base_url, url)
            return f"![{match.group(0)}]({url})"

        markdown = re.sub(r'!\[(.*?)\]\((.*?)\)',
                         lambda m: f"![{m.group(1)}]({urljoin(base_url, m.group(2))})",
                         markdown)
        return markdown

    def save_document(self, filepath, content):
        """保存文档到指定路径"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 已保存: {filepath}")

    def update_vitepress_config(self):
        """自动更新VitePress配置"""
        print("🔄 更新VitePress配置...")
        # TODO: 实现配置更新逻辑
        pass

    def update_todo_status(self, module, section, status, note=''):
        """更新TODO文件中的任务状态"""
        with open(self.todo_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 更新状态标记
        pattern = f"- \\[.\\] \\*\\*{section}\\*\\*"
        replacement = f"- [{status}] **{section}**"

        content = re.sub(pattern, replacement, content)

        with open(self.todo_file, 'w', encoding='utf-8') as f:
            f.write(content)

    def run(self):
        """主采集流程"""
        print("=" * 60)
        print("🚀 CRMEB 文档采集系统启动")
        print("=" * 60)

        tasks = self.parse_todo_file()

        if not tasks:
            print("❌ 没有找到待采集任务")
            return

        total_tasks = sum(len(v) for v in tasks.values())
        completed = 0

        for module, module_tasks in tasks.items():
            print(f"\n📂 处理模块: {module}")

            for task in module_tasks:
                if not task.get('url'):
                    print(f"  ⏭️  跳过 {task['section']}: 无URL")
                    continue

                print(f"  🔄 采集 {task['section']}...")

                # 采集内容
                html = self.fetch_url(task['url'])
                if not html:
                    print(f"    ❌ 采集失败")
                    continue

                # 转换为Markdown
                markdown = self.convert_to_markdown(html, task['url'])

                # 保存
                self.save_document(task['path'], markdown)

                # 更新状态
                self.update_todo_status(module, task['section'], '✅', '采集完成')
                completed += 1

        print(f"\n📊 采集完成: {completed}/{total_tasks}")
        print("=" * 60)


def main():
    project_root = "/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc"
    crawler = DocumentCrawler(project_root)
    crawler.run()


if __name__ == "__main__":
    main()
