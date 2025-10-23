#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRMEB 文档发现工具 - 自动发现所有文档链接
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, List
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentDiscovery:
    """文档发现工具 - 自动识别菜单和文档链接"""

    def __init__(self, start_url: str):
        self.start_url = start_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

        self.discovered_urls: Set[str] = set()
        self.doc_structure = {}

    def fetch_page(self, url: str) -> str:
        """获取页面内容"""
        try:
            logger.info(f"正在获取: {url}")
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(f"HTTP {response.status_code}: {url}")
                return None
        except Exception as e:
            logger.error(f"获取失败: {url} - {str(e)}")
            return None

    def analyze_navigation(self, html: str, base_url: str) -> Dict:
        """分析导航菜单结构"""
        soup = BeautifulSoup(html, 'html.parser')

        # 寻找导航菜单（通常在 logo 下方）
        nav_selectors = [
            'nav', '.nav', '.navigation', '.sidebar', '.menu',
            'div[class*="nav"]', 'div[class*="menu"]', 'div[class*="sidebar"]'
        ]

        navigation = {}

        for selector in nav_selectors:
            nav_elem = soup.select_one(selector)
            if nav_elem:
                # 提取所有链接
                links = nav_elem.find_all('a', href=True)
                for link in links:
                    text = link.get_text(strip=True)
                    href = link.get('href', '')

                    if href and text:
                        full_url = urljoin(base_url, href)
                        # 检查是否是文档链接
                        if self._is_doc_url(full_url):
                            navigation[text] = full_url
                            logger.info(f"发现文档链接: {text} -> {full_url}")

        return navigation

    def _is_doc_url(self, url: str) -> bool:
        """检查是否是文档链接"""
        # 检查 URL 中的数字（文档 ID）
        return '/25' in url or '/26' in url or '/27' in url or any(c.isdigit() for c in url.split('/')[-1])

    def discover_all_documents(self) -> Dict:
        """发现所有文档"""
        logger.info("开始发现所有文档...")

        # 获取首页
        html = self.fetch_page(self.start_url)
        if not html:
            logger.error("无法获取首页")
            return {}

        # 分析导航
        navigation = self.analyze_navigation(html, self.start_url)

        logger.info(f"发现 {len(navigation)} 个文档链接")

        # 保存发现的结构
        result = {
            'start_url': self.start_url,
            'discovered_links': navigation,
            'total_count': len(navigation),
            'discovered_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        return result


def main():
    """主函数"""
    start_url = "https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961"

    discovery = DocumentDiscovery(start_url)
    result = discovery.discover_all_documents()

    # 保存结果
    output_file = Path('output') / 'discovered_documents.json'
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info(f"发现结果已保存到 {output_file}")
    logger.info(f"总共发现 {result['total_count']} 个文档")


if __name__ == '__main__':
    main()
