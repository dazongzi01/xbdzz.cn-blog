#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CRMEB 文档智能采集系统 V2
- 自动提取文章核心要点
- 生成结构化Markdown
- 提高文档质量
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import json

class SmartDocumentCrawler:
    def __init__(self):
        self.base_path = Path("/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/docs")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_url(self, url):
        """获取URL内容"""
        try:
            print(f"  🔄 正在获取: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"  ❌ 获取失败: {str(e)}")
            return None

    def extract_content(self, html):
        """提取页面主要内容"""
        soup = BeautifulSoup(html, 'html.parser')

        # 移除脚本和样式
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        # 获取标题 - 跳过Vue模板占位符
        title = None
        for heading in soup.find_all(['h1', 'h2']):
            text = heading.get_text().strip()
            if text and len(text) > 0 and not text.startswith('{{'):
                title = text
                break

        # 如果没有找到标题，尝试从其他元素提取
        if not title:
            # 查找document title或meta标签
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
                # 清理title中的额外信息
                if ' - ' in title:
                    title = title.split(' - ')[0].strip()
                if ' | ' in title:
                    title = title.split(' | ')[0].strip()

        # 提取主要内容
        content_parts = []

        # 寻找主要内容区域
        main_content = None
        for selector in ['.wiki-content', '.content', 'main', 'article']:
            main_content = soup.select_one(selector)
            if main_content:
                break

        if not main_content:
            main_content = soup.find('body') or soup

        return {
            'title': title or '文档',
            'content': str(main_content),
            'text': main_content.get_text()
        }

    def extract_key_points(self, soup_obj, text):
        """从内容中智能提取要点"""
        key_points = []

        # 方法1: 从h2/h3标题提取
        headings = []
        for tag in soup_obj.find_all(['h2', 'h3', 'h4']):
            text_content = tag.get_text().strip()
            if text_content and len(text_content) > 0 and len(text_content) < 100:
                headings.append(text_content)

        # 方法2: 从列表项提取
        list_items = []
        for li in soup_obj.find_all('li'):
            text_content = li.get_text().strip()
            if text_content and len(text_content) > 0 and len(text_content) < 100:
                list_items.append(text_content)

        # 方法3: 从段落提取关键句（以"●"或"•"开头）
        paragraphs = []
        for p in soup_obj.find_all('p'):
            text_content = p.get_text().strip()
            if text_content and len(text_content) > 20 and len(text_content) < 150:
                # 如果是重要段落（包含关键词）
                if any(keyword in text_content for keyword in ['系统', '功能', '特性', '包含', '支持', '提供', '包括', '实现']):
                    paragraphs.append(text_content)

        # 合并要点
        key_points = headings[:6] if headings else []  # 最多6个标题
        key_points.extend(list_items[:6])  # 最多6个列表项
        key_points.extend(paragraphs[:3])  # 最多3个段落

        # 去重和清理
        key_points = list(dict.fromkeys(key_points))  # 去重
        key_points = [p for p in key_points if len(p) > 5]  # 过滤太短的

        return key_points[:8]  # 返回最多8个要点

    def html_to_markdown(self, html_content, title):
        """将HTML转换为结构化Markdown"""
        soup = BeautifulSoup(html_content, 'html.parser')

        markdown = ""

        # 添加标题
        if title and not title.startswith('{{'):
            markdown += f"# {title}\n\n"
        else:
            markdown += "# 文档\n\n"

        # 提取关键要点
        key_points = self.extract_key_points(soup, html_content)

        if key_points:
            markdown += "## 📋 核心内容\n\n"
            for point in key_points:
                markdown += f"- {point}\n"
            markdown += "\n"

        # 提取所有主要内容块
        markdown += "## 📖 详细内容\n\n"

        # 处理各类元素
        processed_text = set()  # 防止重复

        for element in soup.find_all(['p', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'pre', 'blockquote', 'table', 'div']):
            if element.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(element.name[1]) + 1
                text = element.get_text().strip()
                # 只提取不是模板占位符的标题
                if text and not text.startswith('{{') and not text.startswith('{') and len(text) > 0:
                    if text not in processed_text:
                        markdown += f"{'#' * level} {text}\n\n"
                        processed_text.add(text)

            elif element.name == 'p':
                text = element.get_text().strip()
                if text and len(text) > 5 and not text.startswith('{{') and not text.startswith('{'):
                    if text not in processed_text:
                        markdown += f"{text}\n\n"
                        processed_text.add(text)

            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li', recursive=False):
                    text = li.get_text().strip()
                    if text and not text.startswith('{{') and not text.startswith('{'):
                        if text not in processed_text:
                            markdown += f"- {text}\n"
                            processed_text.add(text)
                if markdown.strip() and not markdown.endswith('\n\n'):
                    markdown += "\n"

            elif element.name == 'pre':
                code = element.get_text()
                if code and not code.startswith('{{'):
                    markdown += f"```\n{code}\n```\n\n"

            elif element.name == 'blockquote':
                text = element.get_text().strip()
                if text and not text.startswith('{{'):
                    if text not in processed_text:
                        markdown += f"> {text}\n\n"
                        processed_text.add(text)

            elif element.name == 'table':
                markdown += "| 列1 | 列2 |\n|-----|-----|\n"
                for row in element.find_all('tr'):
                    cells = []
                    for cell in row.find_all(['td', 'th']):
                        cells.append(cell.get_text().strip())
                    if cells and not any(c.startswith('{{') for c in cells):
                        markdown += f"| {' | '.join(cells)} |\n"
                markdown += "\n"

        result = markdown.strip()
        if not result or result == "# 文档\n\n## 📋 核心内容\n\n## 📖 详细内容":
            result = f"# {title or '文档'}\n\n暂无详细内容"

        return result

    def save_document(self, filepath, content):
        """保存文档"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def crawl_url(self, module_path, doc_name, url):
        """采集单个URL"""
        if not url:
            return False

        print(f"\n📝 采集: {doc_name}")

        html = self.fetch_url(url)
        if not html:
            return False

        # 提取内容
        extracted = self.extract_content(html)

        # 转换为Markdown
        markdown = self.html_to_markdown(extracted['content'], extracted['title'] or doc_name)

        # 保存
        file_path = self.base_path / module_path / f"{doc_name}.md"
        saved_path = self.save_document(file_path, markdown)
        print(f"  ✅ 已保存: {saved_path}")

        return True


def parse_todo_caiji(filepath):
    """解析 TODO_CAIJI.md 文件并提取待采集的URL"""
    tasks = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式提取模块和URL信息
        # 格式: - [✅] **标题** - 路径: `docs/XX/YY.md` - URL: https://...
        pattern = r'-\s*\[([✅❌🔄 ])\]\s*\*\*([^*]+)\*\*.*?路径:\s*`(docs[^`]+)`.*?URL:\s*(https?[^\n]*)'

        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            status, title, path, url = match.groups()
            url = url.strip()

            # 只采集已标记为完成但还没有真正HTML内容的文件（[✅]标记的）
            # 或者尚未采集的文件（[ ]标记的）
            if url and url != '':
                module_path = path.split('/')[1]  # e.g. "01_快速开始"
                doc_name = path.split('/')[-1].replace('.md', '')  # e.g. "01_系统介绍"

                tasks.append({
                    'title': title,
                    'module_path': module_path,
                    'doc_name': doc_name,
                    'url': url.strip(),
                    'status': status
                })

    except Exception as e:
        print(f"❌ 解析TODO文件失败: {str(e)}")

    return tasks


def main():
    """主程序"""
    crawler = SmartDocumentCrawler()

    print("=" * 70)
    print("🚀 CRMEB 文档智能采集系统 V2 启动")
    print("=" * 70)

    # 读取 TODO_CAIJI.md 中的URL并采集
    todo_file = Path("/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/TODO_CAIJI.md")

    if not todo_file.exists():
        print(f"\n❌ 找不到 TODO_CAIJI.md 文件: {todo_file}")
        return

    tasks = parse_todo_caiji(todo_file)

    if not tasks:
        print("\n⚠️  没有找到待采集的URL")
        print("📖 请在 TODO_CAIJI.md 中添加URL")
        return

    print(f"\n📋 发现 {len(tasks)} 个待采集任务")

    # 采集每个URL
    success_count = 0
    failed_count = 0

    for task in tasks:
        print(f"\n{'=' * 70}")
        print(f"📝 任务: {task['title']}")
        print(f"   模块: {task['module_path']}")
        print(f"   文档: {task['doc_name']}")
        print(f"   URL: {task['url']}")

        if crawler.crawl_url(task['module_path'], task['doc_name'], task['url']):
            success_count += 1
            print(f"   ✅ 采集成功")
        else:
            failed_count += 1
            print(f"   ❌ 采集失败")

    print(f"\n{'=' * 70}")
    print(f"✅ 采集完成！")
    print(f"   成功: {success_count}/{len(tasks)}")
    print(f"   失败: {failed_count}/{len(tasks)}")
    print(f"   请运行 'npm run build' 来重新生成网站")
    print("=" * 70)


if __name__ == "__main__":
    main()
