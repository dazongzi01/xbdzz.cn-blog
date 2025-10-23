#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRMEB 智能爬虫 - 自动按模块采集所有文档
支持通过 URL 数字变化来获取不同文档内容
"""

import os
import json
import time
import logging
import re
from typing import Dict, List, Set, Tuple
from urllib.parse import urljoin, urlparse
from pathlib import Path
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SmartCRMEBCrawler:
    """
    智能 CRMEB 爬虫
    自动发现菜单，按模块采集文档
    """

    def __init__(self, start_url: str, output_dir: str = './output'):
        self.start_url = start_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })

        self.visited_urls: Set[str] = set()
        self.failed_urls: List[Tuple[str, str]] = []
        self.menu_items: Dict[str, str] = {}
        self.documents: List[Dict] = []

    def fetch_page(self, url: str) -> str:
        """获取页面内容"""
        if url in self.visited_urls:
            logger.debug(f"已访问: {url}")
            return None

        try:
            logger.info(f"正在获取: {url}")
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                self.visited_urls.add(url)
                time.sleep(1)  # 延迟，避免被封
                return response.text
            else:
                logger.warning(f"HTTP {response.status_code}: {url}")
                self.failed_urls.append((url, f"HTTP {response.status_code}"))
                return None

        except Exception as e:
            logger.error(f"获取失败: {url} - {str(e)}")
            self.failed_urls.append((url, str(e)))
            return None

    def extract_doc_id(self, url: str) -> str:
        """从 URL 中提取文档 ID"""
        # 格式: .../25961 或类似
        match = re.search(r'/(\d{5,})(?:/|$)', url)
        if match:
            return match.group(1)
        return None

    def extract_menu_items(self, html: str) -> Dict[str, str]:
        """从页面中提取菜单项"""
        soup = BeautifulSoup(html, 'html.parser')
        menu_items = {}

        # 寻找所有可能的菜单容器
        menu_selectors = [
            'nav', '.nav', '.navigation', '.sidebar',
            'div[class*="menu"]', 'div[class*="nav"]',
            '.doc-menu', '.left-menu', '.side-menu'
        ]

        for selector in menu_selectors:
            elements = soup.select(selector)
            for elem in elements:
                links = elem.find_all('a', href=True)
                for link in links:
                    text = link.get_text(strip=True)
                    href = link.get('href', '')

                    if text and href:
                        # 尝试转换为绝对 URL
                        full_url = urljoin(self.start_url, href)

                        # 检查是否是文档链接（包含数字 ID）
                        if re.search(r'/\d{5,}', full_url):
                            menu_items[text] = full_url
                            logger.info(f"✓ 找到菜单项: {text}")

        return menu_items

    def extract_content(self, html: str, url: str) -> Dict:
        """提取文档内容"""
        soup = BeautifulSoup(html, 'html.parser')

        # 提取标题
        title = ''
        title_selectors = ['h1', 'h2', '.doc-title', '.page-title', '[class*="title"]']
        for selector in title_selectors:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                break

        if not title:
            title = f"未知文档-{self.extract_doc_id(url)}"

        # 提取主要内容
        content = ''
        content_selectors = ['main', 'article', '.doc-content', '.content', '.main-content']
        for selector in content_selectors:
            elem = soup.select_one(selector)
            if elem:
                content = str(elem)
                break

        if not content:
            content = str(soup.find('body'))

        return {
            'title': title,
            'url': url,
            'doc_id': self.extract_doc_id(url),
            'content': content,
            'html': html
        }

    def extract_all_links(self, html: str) -> Set[str]:
        """从页面中提取所有文档链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()

        for link in soup.find_all('a', href=True):
            href = link.get('href', '').strip()
            if href and not href.startswith('#'):
                full_url = urljoin(self.start_url, href)

                # 检查是否是同域文档链接
                if self._is_valid_doc_url(full_url):
                    links.add(full_url)

        return links

    def _is_valid_doc_url(self, url: str) -> bool:
        """检查是否是有效的文档 URL"""
        # 必须是同域
        parsed = urlparse(url)
        base_parsed = urlparse(self.start_url)

        if parsed.netloc != base_parsed.netloc:
            return False

        # 必须包含数字 ID
        if not re.search(r'/\d{5,}', url):
            return False

        return True

    def crawl_with_menu(self):
        """使用菜单进行智能爬取"""
        logger.info("=" * 60)
        logger.info("开始使用菜单进行智能爬取")
        logger.info("=" * 60)

        # 第一步：获取首页并提取菜单
        logger.info("\n【步骤 1】获取首页并解析菜单...")
        html = self.fetch_page(self.start_url)
        if not html:
            logger.error("无法获取首页")
            return

        self.menu_items = self.extract_menu_items(html)
        logger.info(f"\n找到 {len(self.menu_items)} 个菜单项")

        if not self.menu_items:
            logger.warning("未找到任何菜单项，尝试直接爬取...")
            self._crawl_recursive(self.start_url)
            return

        # 第二步：为每个菜单项爬取文档
        logger.info("\n【步骤 2】逐个爬取菜单项...")
        for title, url in self.menu_items.items():
            logger.info(f"\n正在爬取: {title}")
            logger.info(f"URL: {url}")

            html = self.fetch_page(url)
            if html:
                # 提取内容
                doc_info = self.extract_content(html, url)
                self.documents.append(doc_info)

                # 从当前文档继续提取链接
                new_links = self.extract_all_links(html)
                for new_url in new_links:
                    if new_url not in self.visited_urls:
                        self._crawl_recursive(new_url)

        # 保存结果
        self._save_results()

    def _crawl_recursive(self, start_url: str, max_depth: int = 3, current_depth: int = 0):
        """递归爬取"""
        if current_depth >= max_depth:
            return

        if start_url in self.visited_urls:
            return

        html = self.fetch_page(start_url)
        if not html:
            return

        # 提取和保存内容
        doc_info = self.extract_content(html, start_url)
        self.documents.append(doc_info)

        # 提取新链接并继续爬取
        new_links = self.extract_all_links(html)
        for new_url in new_links:
            if new_url not in self.visited_urls:
                self._crawl_recursive(new_url, max_depth, current_depth + 1)

    def _save_results(self):
        """保存爬取结果"""
        logger.info("\n【步骤 3】保存结果...")

        # 保存菜单
        menu_file = self.output_dir / 'menu.json'
        with open(menu_file, 'w', encoding='utf-8') as f:
            json.dump(self.menu_items, f, ensure_ascii=False, indent=2)
        logger.info(f"✓ 菜单已保存到 {menu_file}")

        # 保存文档
        docs_file = self.output_dir / 'documents.json'
        with open(docs_file, 'w', encoding='utf-8') as f:
            # 只保存元信息，不保存完整 HTML（太大）
            simplified = [
                {
                    'title': doc['title'],
                    'url': doc['url'],
                    'doc_id': doc['doc_id'],
                }
                for doc in self.documents
            ]
            json.dump(simplified, f, ensure_ascii=False, indent=2)
        logger.info(f"✓ 文档列表已保存到 {docs_file}")

        # 保存完整HTML（用于后续处理）
        html_dir = self.output_dir / 'html'
        html_dir.mkdir(exist_ok=True)
        for doc in self.documents:
            doc_id = doc['doc_id']
            if doc_id:
                html_file = html_dir / f"{doc_id}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(doc['html'])

        # 保存报告
        report = {
            'start_url': self.start_url,
            'total_visited': len(self.visited_urls),
            'total_documents': len(self.documents),
            'menu_items': len(self.menu_items),
            'failed_urls': self.failed_urls,
            'crawled_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        report_file = self.output_dir / 'crawl_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ 报告已保存到 {report_file}")
        logger.info(f"\n爬虫完成！")
        logger.info(f"  总访问: {report['total_visited']} 页")
        logger.info(f"  总文档: {report['total_documents']} 篇")
        logger.info(f"  菜单项: {report['menu_items']} 个")
        logger.info(f"  失败: {len(report['failed_urls'])} 个")


def main():
    """主函数"""
    start_url = "https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961"

    logger.info("CRMEB 智能爬虫启动")
    logger.info(f"目标 URL: {start_url}\n")

    crawler = SmartCRMEBCrawler(start_url)
    crawler.crawl_with_menu()


if __name__ == '__main__':
    main()
