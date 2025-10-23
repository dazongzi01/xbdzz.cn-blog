# CRMEB 文档爬虫

## 概述

这个爬虫工具用于自动化爬取 CRMEB 文档站点的所有内容，并保持原有的模块和目录结构。

## 功能特性

- ✅ 递归爬取所有文档页面
- ✅ 完整保留原始的模块和目录结构
- ✅ 自动提取文档标题、内容、链接
- ✅ HTML 到 Markdown 的智能转换
- ✅ 内容清洁和标准化处理
- ✅ 图片资源下载和本地化
- ✅ 生成详细的爬虫报告
- ✅ 结构索引生成

## 安装依赖

```bash
cd crawler
pip install -r requirements.txt
```

## 配置

编辑 `config.json` 配置爬虫参数：

```json
{
  "base_url": "https://doc.crmeb.com",
  "start_url": "https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961",
  "output_dir": "./output",
  "resources_dir": "./output/images",
  "concurrent_requests": 3,
  "request_timeout": 10,
  "delay_between_requests": 1
}
```

## 使用方法

### 1. 基本爬取

```bash
python spider.py
```

### 2. 自定义起始 URL

修改 `config.json` 中的 `start_url`，或使用命令行参数：

```bash
python spider.py --url "https://doc.crmeb.com/..."
```

## 工作流程

```
1. 加载配置 (config.json)
2. 从起始 URL 开始爬取
3. 解析页面结构和链接
4. 递归爬取所有链接
5. 转换 HTML 为 Markdown
6. 清洁和标准化内容
7. 下载图片资源
8. 生成结构索引
9. 输出报告
```

## 输出结构

爬取完成后，输出目录结构如下：

```
output/
├── images/               # 下载的图片资源
│   ├── module-name/
│   └── ...
├── structure.json        # 文档结构索引
├── crawl_report.json     # 爬虫报告
├── module-1/            # 模块 1
│   ├── chapter-1.md
│   ├── chapter-2.md
│   └── ...
├── module-2/            # 模块 2
│   └── ...
└── INDEX.md             # 全局索引
```

## 输出文件说明

### structure.json

完整的文档结构树，包含所有模块、章节和页面的关系。

```json
{
  "title": "根标题",
  "children": [
    {
      "title": "模块 1",
      "url": "...",
      "children": [
        {
          "title": "章节 1",
          "url": "...",
          "children": [...]
        }
      ]
    }
  ]
}
```

### crawl_report.json

爬虫执行的详细报告：

```json
{
  "total_visited": 100,
  "total_articles": 95,
  "failed_urls": [],
  "articles": [
    {
      "id": "unique_id",
      "title": "文章标题",
      "url": "原始 URL",
      "breadcrumb": [...],
      "content_length": 5000,
      "crawled_at": "2024-01-01 10:00:00"
    }
  ],
  "crawled_at": "2024-01-01 10:30:00"
}
```

## 常见问题

### 1. 爬虫无法访问网站

**原因**: 网站可能有反爬虫机制或防火墙。

**解决**:
- 增加 `delay_between_requests`
- 修改 `user_agent`
- 检查网站是否需要登录

### 2. 图片未下载

**原因**: 图片 URL 可能是相对路径或需要特殊处理。

**解决**:
- 检查 `base_url` 配置
- 查看爬虫日志中的错误信息

### 3. 某些页面转换后内容为空

**原因**: HTML 结构与解析器预期不符。

**解决**:
- 手动检查该页面的 HTML 结构
- 在 `parser.py` 中添加适配

## 进阶配置

### 自定义解析器

编辑 `parser.py` 的 `_extract_structure` 方法，支持不同的网站结构。

### 自定义清洁规则

编辑 `cleaner.py` 添加自定义的清洁规则。

## 贡献

有任何问题或建议？欢迎提交 Issue 或 PR！

## License

MIT
