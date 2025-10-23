#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRMEB Selenium 爬虫 - 处理 JavaScript 渲染的内容
支持动态菜单加载
"""

import time
import logging
import json
from pathlib import Path
from typing import Dict, Set, List
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SeleniumCRMEBCrawler:
    """使用 Selenium 爬取动态渲染的文档"""

    def __init__(self, start_url: str, output_dir: str = './output'):
        self.start_url = start_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.visited_urls: Set[str] = set()
        self.documents: List[Dict] = []
        self.menu_items: Dict[str, str] = {}

        # 配置 Chrome 选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无界面模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("✓ Chrome WebDriver 已初始化")
        except Exception as e:
            logger.error(f"Chrome WebDriver 初始化失败: {e}")
            logger.info("尝试使用 Safari...")
            try:
                self.driver = webdriver.Safari()
                logger.info("✓ Safari WebDriver 已初始化")
            except Exception as e2:
                logger.error(f"Safari WebDriver 也失败: {e2}")
                raise

    def get_page_with_js(self, url: str, wait_selector: str = None, wait_time: int = 10) -> str:
        """使用 Selenium 获取渲染后的页面"""
        try:
            logger.info(f"使用 Selenium 加载: {url}")
            self.driver.get(url)

            # 等待页面加载
            if wait_selector:
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, wait_selector))
                )
            else:
                # 等待一般的加载完成
                time.sleep(5)

            # 获取渲染后的 HTML
            html = self.driver.page_source
            return html

        except Exception as e:
            logger.error(f"加载失败: {url} - {str(e)}")
            return None

    def extract_menu_from_rendered(self, html: str) -> Dict[str, str]:
        """从渲染后的 HTML 中提取菜单"""
        soup = BeautifulSoup(html, 'html.parser')
        menu_items = {}

        # 查找 Element UI 菜单项
        logger.info("尝试从 Element UI 菜单中提取...")

        # 寻找所有菜单项
        menu_selectors = [
            '.el-menu-item',
            '.el-submenu',
            '[role="menuitem"]',
            '[class*="menu"]'
        ]

        for selector in menu_selectors:
            elements = soup.select(selector)
            if elements:
                logger.info(f"找到 {len(elements)} 个 {selector} 元素")
                for elem in elements:
                    text = elem.get_text(strip=True)
                    # 查找元素内或元素下的链接
                    link = elem.find('a')
                    if link and link.get('href'):
                        href = link.get('href')
                        if text and href:
                            full_url = urljoin(self.start_url, href)
                            menu_items[text] = full_url
                            logger.info(f"✓ {text} -> {href}")

        # 如果上面没找到，查找所有可点击的元素
        if not menu_items:
            logger.info("尝试查找所有超链接...")
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                text = link.get_text(strip=True)
                href = link.get('href', '').strip()
                if text and href and len(text) > 2:  # 过滤掉太短的文本
                    full_url = urljoin(self.start_url, href)
                    if full_url not in menu_items.values():
                        menu_items[text] = full_url

        return menu_items

    def extract_content(self, html: str, url: str) -> Dict:
        """提取文档内容"""
        soup = BeautifulSoup(html, 'html.parser')

        # 提取标题
        title = ''
        for selector in ['h1', 'h2', '.title', '.doc-title', '[class*="title"]']:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                if len(title) > 3:
                    break

        if not title:
            title = soup.title.string if soup.title else "未知文档"

        # 提取内容
        content = ''
        for selector in ['main', 'article', '.content', '.doc-content', 'body']:
            elem = soup.select_one(selector)
            if elem:
                content = str(elem)
                break

        return {
            'title': title,
            'url': url,
            'content': content,
            'html': html
        }

    def crawl(self):
        """开始爬取"""
        try:
            logger.info("=" * 60)
            logger.info("CRMEB Selenium 爬虫启动")
            logger.info("=" * 60)

            # 加载首页
            logger.info("\n【步骤 1】加载首页并提取菜单...")
            html = self.get_page_with_js(self.start_url, wait_time=15)
            if not html:
                logger.error("无法加载首页")
                return

            # 提取菜单
            self.menu_items = self.extract_menu_from_rendered(html)
            logger.info(f"\n找到 {len(self.menu_items)} 个菜单项")

            # 保存菜单
            if self.menu_items:
                menu_file = self.output_dir / 'menu.json'
                with open(menu_file, 'w', encoding='utf-8') as f:
                    json.dump(self.menu_items, f, ensure_ascii=False, indent=2)
                logger.info(f"✓ 菜单已保存到 {menu_file}")

                # 爬取每个菜单项
                logger.info("\n【步骤 2】爬取菜单项...")
                for title, url in list(self.menu_items.items())[:10]:  # 先试10个
                    if url not in self.visited_urls:
                        logger.info(f"\n正在爬取: {title}")
                        html = self.get_page_with_js(url, wait_time=10)
                        if html:
                            doc = self.extract_content(html, url)
                            self.documents.append(doc)
                            self.visited_urls.add(url)

                # 保存文档
                logger.info("\n【步骤 3】保存文档...")
                self._save_documents()

        finally:
            self.driver.quit()
            logger.info("\n✓ WebDriver 已关闭")

    def _save_documents(self):
        """保存文档"""
        docs_file = self.output_dir / 'documents.json'
        with open(docs_file, 'w', encoding='utf-8') as f:
            simplified = [
                {
                    'title': doc['title'],
                    'url': doc['url'],
                }
                for doc in self.documents
            ]
            json.dump(simplified, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ {len(self.documents)} 个文档已保存")

        # 保存 HTML
        html_dir = self.output_dir / 'html'
        html_dir.mkdir(exist_ok=True)
        for i, doc in enumerate(self.documents):
            with open(html_dir / f"doc_{i}.html", 'w', encoding='utf-8') as f:
                f.write(doc['html'])

        logger.info(f"爬虫完成！\n总爬取: {len(self.visited_urls)} 页\n总文档: {len(self.documents)}")


def main():
    """主函数"""
    start_url = "https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961"

    crawler = SeleniumCRMEBCrawler(start_url)
    crawler.crawl()


if __name__ == '__main__':
    main()
