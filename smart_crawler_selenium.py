#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CRMEB 文档智能采集系统 - Selenium版本
- 使用Selenium渲染JavaScript
- 提取动态渲染后的内容
- 支持Vue.js应用采集
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class SeleniumDocumentCrawler:
    def __init__(self):
        self.base_path = Path("/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/docs")

        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        self.driver = None
        self.chrome_options = chrome_options

    def init_driver(self):
        """初始化Selenium WebDriver"""
        if self.driver is None:
            try:
                self.driver = webdriver.Chrome(options=self.chrome_options)
            except Exception as e:
                print(f"❌ 初始化Chrome驱动失败: {str(e)}")
                print("   请确保已安装ChromeDriver: brew install chromedriver")
                return False
        return True

    def fetch_url_with_selenium(self, url):
        """使用Selenium获取渲染后的页面内容"""
        try:
            if not self.init_driver():
                return None

            print(f"  🔄 正在获取: {url}")
            self.driver.get(url)

            # 等待内容加载
            wait = WebDriverWait(self.driver, 10)
            try:
                # 等待内容区域加载
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content")))
                time.sleep(2)  # 额外等待以确保Vue渲染完成
            except:
                print(f"  ⚠️  等待超时，使用当前加载的内容")

            # 获取渲染后的HTML
            html = self.driver.page_source
            return html

        except Exception as e:
            print(f"  ❌ 获取失败: {str(e)}")
            return None

    def fetch_url_fallback(self, url):
        """备用方案：使用requests获取"""
        try:
            print(f"  🔄 正在获取(备用): {url}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
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

        # 获取标题 - 优先使用h2"快速了解"之后的内容
        title = None

        # 方法1: 寻找"快速了解"之后的标题
        quick_learn = soup.find(string=re.compile('快速了解'))
        if quick_learn:
            # 找到其父元素后的下一个h2或h3
            parent = quick_learn.parent
            next_elem = parent.find_next(['h2', 'h3'])
            if next_elem:
                title = next_elem.get_text().strip()

        # 方法2: 查找所有h2/h3标题，跳过模板占位符
        if not title:
            for heading in soup.find_all(['h2', 'h3']):
                text = heading.get_text().strip()
                if text and not text.startswith('{{') and len(text) > 0:
                    title = text
                    break

        # 提取主要内容
        main_content = None
        for selector in ['.wiki-content', '.content', 'main', 'article']:
            main_content = soup.select_one(selector)
            if main_content:
                break

        if not main_content:
            main_content = soup.find('body') or soup

        return {
            'title': title,
            'content': str(main_content),
            'text': main_content.get_text()
        }

    def extract_key_points(self, soup_obj, text):
        """从内容中智能提取要点"""
        key_points = []

        # 方法1: 从h2/h3标题提取（跳过模板占位符）
        headings = []
        for tag in soup_obj.find_all(['h2', 'h3', 'h4']):
            text_content = tag.get_text().strip()
            if text_content and not text_content.startswith('{{') and len(text_content) > 0 and len(text_content) < 100:
                headings.append(text_content)

        # 方法2: 从列表项提取
        list_items = []
        for li in soup_obj.find_all('li'):
            text_content = li.get_text().strip()
            if text_content and not text_content.startswith('{{') and len(text_content) > 0 and len(text_content) < 100:
                list_items.append(text_content)

        # 方法3: 从段落提取关键句
        paragraphs = []
        for p in soup_obj.find_all('p'):
            text_content = p.get_text().strip()
            if text_content and not text_content.startswith('{{') and len(text_content) > 20 and len(text_content) < 150:
                # 如果是重要段落（包含关键词）
                if any(keyword in text_content for keyword in ['系统', '功能', '特性', '包含', '支持', '提供', '包括', '实现', '基于', '采用']):
                    paragraphs.append(text_content)

        # 合并要点
        key_points = headings[:6] if headings else []  # 最多6个标题
        key_points.extend(list_items[:6])  # 最多6个列表项
        key_points.extend(paragraphs[:3])  # 最多3个段落

        # 去重和清理
        key_points = list(dict.fromkeys(key_points))  # 去重
        key_points = [p for p in key_points if len(p) > 5 and not p.startswith('{{')]  # 过滤太短的和模板

        return key_points[:8]  # 返回最多8个要点

    def html_to_markdown(self, html_content, title):
        """将HTML转换为结构化Markdown"""
        soup = BeautifulSoup(html_content, 'html.parser')

        markdown = ""

        # 添加标题 - 使用提取的标题或文档名
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
        for element in soup.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol', 'pre', 'blockquote', 'table']):
            if element.name in ['h2', 'h3', 'h4']:
                level = int(element.name[1]) + 1
                text = element.get_text().strip()
                if text and not text.startswith('{{'):
                    markdown += f"{'#' * level} {text}\n\n"

            elif element.name == 'p':
                text = element.get_text().strip()
                if text and len(text) > 5 and not text.startswith('{{'):
                    markdown += f"{text}\n\n"

            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li', recursive=False):
                    text = li.get_text().strip()
                    if text and not text.startswith('{{'):
                        markdown += f"- {text}\n"
                markdown += "\n"

            elif element.name == 'pre':
                code = element.get_text()
                if not code.startswith('{{'):
                    markdown += f"```\n{code}\n```\n\n"

            elif element.name == 'blockquote':
                text = element.get_text().strip()
                if text and not text.startswith('{{'):
                    markdown += f"> {text}\n\n"

            elif element.name == 'table':
                markdown += "| 列1 | 列2 |\n|-----|-----|\n"
                for row in element.find_all('tr'):
                    cells = []
                    for cell in row.find_all(['td', 'th']):
                        cells.append(cell.get_text().strip())
                    if cells:
                        markdown += f"| {' | '.join(cells)} |\n"
                markdown += "\n"

        result = markdown.strip() or f"# {title or '文档'}\n\n暂无详细内容"
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

        # 尝试使用Selenium获取
        html = self.fetch_url_with_selenium(url)

        # 如果Selenium失败，使用备用方案
        if not html:
            html = self.fetch_url_fallback(url)

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

    def close(self):
        """关闭WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None


def parse_todo_caiji(filepath):
    """解析 TODO_CAIJI.md 文件并提取待采集的URL"""
    tasks = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式提取模块和URL信息
        pattern = r'-\s*\[([✅❌🔄 ])\]\s*\*\*([^*]+)\*\*.*?路径:\s*`(docs[^`]+)`.*?URL:\s*(https?[^\n]*)'

        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            status, title, path, url = match.groups()
            url = url.strip()

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
    print("=" * 70)
    print("🚀 CRMEB 文档智能采集系统 - Selenium 版本")
    print("=" * 70)

    crawler = SeleniumDocumentCrawler()

    try:
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

    finally:
        # 关闭WebDriver
        crawler.close()


if __name__ == "__main__":
    main()
