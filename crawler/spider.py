#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRMEB 文档站点爬虫
目标: 完整保留原站点的模块和目录结构
"""

import os
import json
import time
import logging
from typing import Dict, List, Set, Optional, Tuple
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import hashlib

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CRMEBCrawler:
    """CRMEB 文档爬虫"""

    def __init__(self, config_path: str = 'config.json'):
        """初始化爬虫"""
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update(self.config.get('headers', {}))

        # 创建输出目录
        self.output_dir = Path(self.config['output_dir'])
        self.resources_dir = Path(self.config['resources_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.resources_dir.mkdir(parents=True, exist_ok=True)

        # 追踪已爬取的 URL
        self.visited_urls: Set[str] = set()
        self.failed_urls: List[Tuple[str, str]] = []

        # 文档树结构
        self.doc_tree: Dict = defaultdict(dict)
        self.articles: List[Dict] = []

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"配置文件不存在: {config_path}")
            raise

    def _fetch_page(self, url: str) -> Optional[str]:
        """获取页面内容"""
        if url in self.visited_urls:
            return None

        try:
            logger.info(f"正在爬取: {url}")
            response = self.session.get(
                url,
                timeout=self.config['request_timeout'],
                verify=False
            )
            response.encoding = 'utf-8'

            if response.status_code == 200:
                self.visited_urls.add(url)
                return response.text
            else:
                logger.warning(f"状态码异常: {url} - {response.status_code}")
                self.failed_urls.append((url, f"HTTP {response.status_code}"))
                return None

        except requests.RequestException as e:
            logger.error(f"请求失败: {url} - {str(e)}")
            self.failed_urls.append((url, str(e)))
            return None
        finally:
            time.sleep(self.config['delay_between_requests'])

    def _extract_structure(self, html: str, url: str) -> Dict:
        """提取文档结构（导航、模块、章节）"""
        soup = BeautifulSoup(html, 'html.parser')
        structure = {
            'url': url,
            'title': '',
            'breadcrumb': [],
            'navigation': [],
            'content': '',
            'children_urls': []
        }

        try:
            # 提取标题
            title_tag = soup.find('h1') or soup.find('title')
            if title_tag:
                structure['title'] = title_tag.get_text(strip=True)

            # 提取面包屑（用于确定位置）
            breadcrumb = soup.find('nav', class_='breadcrumb')
            if breadcrumb:
                items = breadcrumb.find_all('a')
                structure['breadcrumb'] = [
                    {'text': item.get_text(strip=True), 'url': item.get('href')}
                    for item in items
                ]

            # 提取导航菜单（左侧或顶部）
            nav = soup.find('nav', class_=['sidebar', 'navigation'])
            if nav:
                links = nav.find_all('a')
                structure['navigation'] = [
                    {
                        'text': link.get_text(strip=True),
                        'url': link.get('href'),
                        'class': link.get('class', [])
                    }
                    for link in links if link.get('href')
                ]

            # 提取主要内容
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                structure['content'] = str(main_content)

        except Exception as e:
            logger.error(f"提取结构失败: {url} - {str(e)}")

        return structure

    def _extract_all_links(self, html: str, base_url: str) -> Set[str]:
        """提取页面中的所有文档链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()

        for link in soup.find_all('a', href=True):
            href = link.get('href', '').strip()
            if not href or href.startswith('#'):
                continue

            # 转换为绝对 URL
            absolute_url = urljoin(base_url, href)

            # 只保留同域名的文档链接
            if self._is_valid_doc_url(absolute_url):
                links.add(absolute_url)

        return links

    def _is_valid_doc_url(self, url: str) -> bool:
        """检查是否是有效的文档链接"""
        parsed = urlparse(url)
        base_parsed = urlparse(self.config['base_url'])

        # 同域名检查
        if parsed.netloc != base_parsed.netloc:
            return False

        # 排除某些类型的链接
        exclude_patterns = ['.pdf', '.zip', '.exe', 'javascript:', 'mailto:']
        if any(url.lower().endswith(pattern) or pattern in url for pattern in exclude_patterns):
            return False

        return True

    def crawl(self, start_url: Optional[str] = None) -> None:
        """开始爬取"""
        start_url = start_url or self.config['start_url']
        to_crawl = [start_url]

        while to_crawl:
            url = to_crawl.pop(0)

            if url in self.visited_urls:
                continue

            html = self._fetch_page(url)
            if not html:
                continue

            # 提取结构
            structure = self._extract_structure(html, url)
            logger.info(f"✓ 成功: {structure['title']} ({url})")

            # 保存文档元信息
            self._save_article_metadata(url, structure)

            # 提取新链接
            new_links = self._extract_all_links(html, url)
            for link in new_links:
                if link not in self.visited_urls and link not in to_crawl:
                    to_crawl.append(link)

        # 生成报告
        self._generate_report()

    def _save_article_metadata(self, url: str, structure: Dict) -> None:
        """保存文章元信息"""
        article = {
            'id': hashlib.md5(url.encode()).hexdigest()[:12],
            'title': structure['title'],
            'url': url,
            'breadcrumb': structure['breadcrumb'],
            'content_length': len(structure['content']),
            'crawled_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.articles.append(article)

    def _generate_report(self) -> None:
        """生成爬虫运行报告"""
        report = {
            'total_visited': len(self.visited_urls),
            'total_articles': len(self.articles),
            'failed_urls': self.failed_urls,
            'articles': self.articles,
            'crawled_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # 保存为 JSON
        with open(self.output_dir / 'crawl_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"\n爬虫完成报告:")
        logger.info(f"  总爬取: {report['total_visited']} 页")
        logger.info(f"  文章数: {report['total_articles']}")
        logger.info(f"  失败: {len(report['failed_urls'])} 页")
        logger.info(f"  报告已保存到: {self.output_dir / 'crawl_report.json'}")


if __name__ == '__main__':
    try:
        crawler = CRMEBCrawler('config.json')
        logger.info("开始爬取 CRMEB 文档...")
        crawler.crawl()
        logger.info("爬虫任务完成！")
    except Exception as e:
        logger.error(f"爬虫异常退出: {str(e)}")
        raise
