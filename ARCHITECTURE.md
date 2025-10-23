# 项目技术架构

## 系统设计概览

```
┌─────────────────────────────────────────────────────────────────┐
│                      CRMEB 文档平台系统架构                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   数据源         │
│ doc.crmeb.com    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│          爬虫系统 (Crawler)              │
│  ┌─────────────────────────────────┐   │
│  │ spider.py                       │   │
│  │ • URL 管理                      │   │
│  │ • 递归爬取                      │   │
│  │ • 链接提取                      │   │
│  │ • 错误处理                      │   │
│  └──────────┬──────────────────────┘   │
│             │                          │
│  ┌──────────▼──────────┐              │
│  │  parser.py          │              │
│  │ • HTML 解析         │              │
│  │ • MD 转换           │              │
│  │ • 结构提取          │              │
│  └──────────┬──────────┘              │
│             │                          │
│  ┌──────────▼──────────┐              │
│  │  cleaner.py         │              │
│  │ • 格式清洁          │              │
│  │ • 标准化            │              │
│  │ • 验证              │              │
│  └──────────┬──────────┘              │
└─────────────┼──────────────────────────┘
              │
              ▼
    ┌─────────────────────┐
    │  Markdown 文件      │
    │  + structure.json   │
    │  + 图片资源         │
    │  + 元数据           │
    └─────────┬───────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│     VitePress 文档系统 (Docs)           │
│  ┌─────────────────────────────────┐   │
│  │ config.ts - 全局配置            │   │
│  │ • 导航菜单                      │   │
│  │ • 侧边栏                        │   │
│  │ • SEO                           │   │
│  │ • 搜索配置                      │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ theme/ - 自定义主题            │   │
│  │ • 样式                          │   │
│  │ • 组件                          │   │
│  │ • 布局                          │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Markdown 文档                   │   │
│  │ (从爬虫输出)                    │   │
│  └─────────────────────────────────┘   │
└──────────────────┬───────────────────────┘
                   │
                   ▼
            ┌──────────────┐
            │ 静态网站     │
            │ • HTML 文件  │
            │ • JS        │
            │ • CSS       │
            └──────┬───────┘
                   │
                   ▼
        ┌────────────────────┐
        │  部署到 CDN/服务器 │
        │  • GitHub Pages    │
        │  • Netlify         │
        │  • 自有服务器      │
        └────────────────────┘
              │
              ├──────────────────────┐
              ▼                      ▼
        ┌──────────────┐      ┌──────────────┐
        │   VitePress  │      │   多平台     │
        │   文档站点   │      │   发布系统   │
        └──────────────┘      │              │
                              │ Converter:   │
                              │ • MD->微信   │
                              │ • MD->掘金   │
                              │ • MD->CSDN   │
                              │ • MD->知乎   │
                              │              │
                              │ Publishers:  │
                              │ • API 集成   │
                              │ • 自动发布   │
                              │ • 版本追踪   │
                              │              │
                              │ Templates:   │
                              │ • 样式库     │
                              │ • 预览       │
                              │              │
                              └──────────────┘
                                    │
                         ┌──────────┼──────────┬──────────┐
                         ▼          ▼          ▼          ▼
                    ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
                    │微信公众│ │ 掘金   │ │ CSDN   │ │ 知乎   │
                    │  号   │ │        │ │        │ │        │
                    └────────┘ └────────┘ └────────┘ └────────┘
```

## 数据流

### 1. 爬虫系统 (Crawler)

```
Config.json
    │
    ▼
Spider.py (网络爬虫)
    ├─ 请求管理
    ├─ URL 队列
    ├─ 链接提取
    └─ 错误处理
    │
    ▼
Parser.py (内容解析)
    ├─ HTML 选择器
    ├─ 元数据提取
    ├─ 结构识别
    └─ Markdown 转换
    │
    ▼
Cleaner.py (内容清洁)
    ├─ 格式修复
    ├─ 标准化
    ├─ 验证
    └─ 输出
    │
    ▼
Output/
    ├─ structure.json (文档树)
    ├─ crawl_report.json (报告)
    ├─ module-1/
    │   ├─ chapter-1.md
    │   └─ chapter-2.md
    └─ images/
        └─ [下载的图片]
```

### 2. VitePress 文档系统

```
Output/ (爬虫输出)
    │
    ▼
docs/
    ├─ .vitepress/
    │   ├─ config.ts (导入 structure.json)
    │   └─ theme/
    │
    ├─ index.md (首页)
    ├─ module-1/
    │   ├─ chapter-1.md
    │   └─ chapter-2.md
    └─ images/ (爬虫图片)
    │
    ▼
npm run build
    │
    ▼
.vitepress/dist/ (静态站点)
```

### 3. 多平台发布系统

```
docs/module-1/chapter-1.md
    │
    ▼
Publisher CLI
    │
    ├─ Converter.ts (格式转换)
    │   ├─ 解析 Markdown
    │   ├─ 构建 AST
    │   └─ 生成目标格式
    │
    ├─ Platforms/ (平台适配)
    │   ├─ wechat.ts
    │   ├─ juejin.ts
    │   ├─ csdn.ts
    │   └─ zhihu.ts
    │
    ├─ Templates/ (样式模板)
    │   └─ platform-specific.css
    │
    └─ Tracker.ts (状态追踪)
        └─ publish-status.json

    ▼
[平台输出格式]
    ├─ 微信公众号 (HTML + CSS)
    ├─ 掘金 (JSON API)
    ├─ CSDN (HTML + 元数据)
    └─ 知乎 (JSON + 元数据)
```

## 核心模块详解

### 爬虫系统 (spider.py)

```python
CRMEBCrawler
├─ __init__(config_path)
│   └─ 加载配置，初始化会话
│
├─ _fetch_page(url)
│   └─ 获取页面，处理错误
│
├─ _extract_structure(html, url)
│   ├─ 提取标题、面包屑
│   ├─ 解析导航菜单
│   └─ 提取主要内容
│
├─ _extract_all_links(html, base_url)
│   └─ 提取所有有效链接
│
├─ _is_valid_doc_url(url)
│   └─ 验证 URL 合法性
│
├─ crawl(start_url)
│   ├─ BFS 遍历所有页面
│   └─ 保存元数据
│
└─ _generate_report()
    └─ 生成爬虫报告
```

### 解析系统 (parser.py)

```python
MarkdownParser
├─ html_to_markdown(html, title)
│   └─ 完整的 HTML 到 MD 转换
│
├─ _element_to_markdown(element)
│   ├─ 标题 (h1-h6)
│   ├─ 段落 (p)
│   ├─ 列表 (ul, ol)
│   ├─ 表格 (table)
│   ├─ 代码块 (pre, code)
│   ├─ 图片 (img)
│   ├─ 链接 (a)
│   └─ 其他元素
│
├─ _process_*() 系列方法
│   ├─ _process_list()
│   ├─ _process_table()
│   ├─ _process_image()
│   └─ _process_code_block()
│
└─ _clean_markdown()
    └─ 后期处理
```

### 清洁系统 (cleaner.py)

```python
MarkdownCleaner
├─ clean_content(content)
│   └─ 完整的清洁流程
│
├─ remove_html_entities()
│   └─ 替换 HTML 实体
│
├─ fix_spacing()
│   ├─ 修复空行
│   └─ 修复缩进
│
├─ standardize_formatting()
│   ├─ 标准化强调
│   └─ 标准化代码块
│
├─ fix_lists() 和 fix_code_blocks()
│   └─ 特定格式修复
│
└─ validate_content()
    └─ 内容质量检查

PathNormalizer
├─ normalize_file_path()
│   └─ 文件名标准化
│
├─ extract_hierarchy_from_url()
│   └─ 从 URL 提取层级
│
└─ build_file_path()
    └─ 构建完整文件路径
```

## 文件和数据格式

### structure.json (文档树结构)

```json
{
  "title": "CRMEB Java 文档",
  "url": "https://...",
  "children": [
    {
      "title": "模块名",
      "url": "https://...",
      "level": 1,
      "children": [
        {
          "title": "章节名",
          "url": "https://...",
          "level": 2,
          "children": [...]
        }
      ]
    }
  ]
}
```

### crawl_report.json (爬虫报告)

```json
{
  "total_visited": 100,
  "total_articles": 95,
  "failed_urls": [...],
  "articles": [
    {
      "id": "abc123",
      "title": "文章标题",
      "url": "原始URL",
      "breadcrumb": [...],
      "content_length": 5000,
      "crawled_at": "2024-01-01 10:00:00"
    }
  ],
  "crawled_at": "2024-01-01 10:30:00"
}
```

### articles.json (文章索引)

```json
{
  "articles": [
    {
      "id": "unique_id",
      "title": "文章标题",
      "module": "模块名",
      "path": "module/chapter/article.md",
      "url": "原始URL",
      "children": [],
      "meta": {
        "description": "文章描述",
        "keywords": ["关键词"],
        "updated_at": "2024-01-01T10:00:00Z"
      }
    }
  ]
}
```

## 配置管理

### config.json (爬虫配置)

```json
{
  "base_url": "https://doc.crmeb.com",
  "start_url": "https://doc.crmeb.com/path/to/docs",
  "output_dir": "./output",
  "resources_dir": "./output/images",
  "concurrent_requests": 3,
  "request_timeout": 10,
  "retry_times": 3,
  "user_agent": "Custom User Agent",
  "headers": {
    "Accept": "text/html,...",
    "Accept-Language": "zh-CN,zh;q=0.9"
  },
  "respect_robots_txt": true,
  "delay_between_requests": 1
}
```

## 错误处理策略

### 1. 爬虫错误
- 网络错误：自动重试（最多 3 次）
- HTTP 错误：记录并继续
- 解析错误：记录源 HTML 用于调试

### 2. 解析错误
- 未找到选择器：降级处理
- HTML 格式错误：使用 lxml 容错模式
- 编码问题：自动检测和转换

### 3. 清洁错误
- 验证失败：记录日志并返回原内容
- 路径冲突：自动重命名

## 性能考虑

### 1. 网络请求
- 并发请求：可配置（默认 3）
- 请求超时：10 秒
- 延迟控制：每次请求间隔 1 秒
- 连接池：重用 session

### 2. 内存管理
- 流式处理：按行读取大文件
- 及时释放：爬取完成后清理缓存

### 3. 磁盘 I/O
- 批量写入：减少 I/O 操作
- 压缩存储：图片原地保存（可选）

## 安全考虑

1. **User-Agent 欺骗**：可配置，尊重 robots.txt
2. **请求频率控制**：避免过于频繁的请求
3. **数据验证**：严格验证输入和输出
4. **错误日志**：不泄露敏感信息

## 扩展性设计

### 支持新的网站结构

修改以下文件：
1. `config.json` - 调整 URL 和请求参数
2. `parser.py` - 修改 HTML 选择器
3. `cleaner.py` - 添加特定的清洁规则

### 支持新的输出格式

在 `publisher/src/platforms/` 中添加新的适配器。

### 支持新的数据源

创建新的 Crawler 子类，实现特定的爬取逻辑。

---

本设计文档确保系统的模块化、可维护性和可扩展性。
