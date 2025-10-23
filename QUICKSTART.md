# 🚀 快速开始指南

## 5 分钟快速了解项目

### 项目是什么？

将你的 CRMEB 文档从 `doc.crmeb.com` 迁移到现代化的 VitePress 文档系统，同时配套一个强大的多平台发布工具，支持自动发布到微信公众号、掘金、CSDN、知乎等平台。

### 当前状态

✅ **已完成**：爬虫框架和工具开发
⏳ **等待中**：你的网站结构信息

### 完整的工作流程

```
你的文档站点
    ↓
爬虫自动爬取
    ↓
转换为 Markdown
    ↓
VitePress 文档站
    ↓
↙        ↓        ↘
微信    掘金    CSDN
公众号
```

---

## 马上开始

### 步骤 1：查看项目结构

打开这个目录，你会看到：

```
crmeb-docs-platform/
├── .claude/todos.md          ← 详细的任务清单（重要！）
├── README.md                 ← 项目概览
├── SETUP_GUIDE.md            ← 初始化指南
├── PROJECT_STATUS.md         ← 项目进度报告
├── ARCHITECTURE.md           ← 技术架构
├── QUICKSTART.md             ← 本文件
│
└── crawler/                  ← 爬虫工具
    ├── spider.py             (爬虫程序)
    ├── parser.py             (HTML 解析)
    ├── cleaner.py            (内容清洁)
    ├── config.json           (配置文件)
    ├── requirements.txt      (Python 依赖)
    └── README.md             (爬虫说明)
```

### 步骤 2：阅读关键文档

优先级顺序：

1. **`.claude/todos.md`** - 了解所有任务和当前进度
2. **`SETUP_GUIDE.md`** - 了解如何继续
3. **`README.md`** - 理解整个项目
4. **`ARCHITECTURE.md`** - 深入理解技术细节（可选）

### 步骤 3：提供你的网站信息

我需要你告诉我：

1. **网站的 HTML 结构**
   - 打开你的文档页面
   - 右键 → 查看源代码
   - 告诉我如何找到：
     - 标题在哪个 HTML 元素
     - 正文内容在哪个容器
     - 导航菜单的结构

2. **文档的组织结构**
   - 最顶层的模块有哪些？
   - 每个模块下有什么子章节？
   - 举例说明目录层级

3. **或者**：提供网站的截图或 HTML 片段

### 步骤 4：我会调整爬虫

基于你提供的信息，我会：
1. 更新爬虫的 HTML 选择器
2. 配置正确的链接识别规则
3. 测试爬虫
4. 生成所有文档的 Markdown 版本

### 步骤 5：搭建 VitePress 文档系统

- 创建优美的文档网站
- 配置 SEO
- 添加搜索功能
- 自定义主题

### 步骤 6：配置多平台发布工具

- 一键发布到多个平台
- 自动格式转换
- 样式适配

---

## 核心文件说明

### 爬虫工具 (crawler/)

**目的**：自动爬取你的文档并保持原有结构

**包含**：
- `spider.py` (500+ 行) - 网络爬虫
- `parser.py` (400+ 行) - HTML 解析和 Markdown 转换
- `cleaner.py` (350+ 行) - 内容清洁和标准化

**使用**：
```bash
cd crawler
pip install -r requirements.txt
python spider.py
```

**输出**：
```
output/
├── structure.json        # 文档树
├── crawl_report.json     # 爬虫报告
├── module-1/
│   ├── chapter-1.md
│   └── chapter-2.md
└── images/               # 下载的图片
```

---

## 常见问题

### Q: 爬虫会破坏我的网站吗？
A: 不会。爬虫只是读取公开的页面，它：
- 遵守 robots.txt
- 限制请求频率（每秒一个）
- 只下载文本和图片
- 不修改任何数据

### Q: 需要多长时间？
A:
- 如果网站有 100 页：约 2-3 分钟
- 准备工作和调整：1-2 小时
- 完整的迁移（包括 VitePress）：15-20 小时

### Q: 爬虫失败了怎么办？
A:
- 检查 `crawler/output/crawl_report.json` 中的错误
- 修改 `crawler/config.json` 中的参数
- 查看 `crawler/README.md` 的常见问题部分

### Q: 如何定制输出的文件名和路径？
A:
编辑 `crawler/cleaner.py` 中的 `PathNormalizer` 类。

### Q: 图片下载失败？
A:
检查图片 URL 是否正确，修改 `crawler/parser.py` 中的图片处理逻辑。

---

## 下一步检查清单

- [ ] 阅读 `.claude/todos.md`
- [ ] 阅读 `SETUP_GUIDE.md`
- [ ] 准备网站 HTML 信息或截图
- [ ] 告诉我网站的模块结构
- [ ] 我会调整爬虫并运行
- [ ] 继续搭建 VitePress
- [ ] 开发多平台发布工具
- [ ] 部署上线

---

## 技术栈一览

| 组件 | 技术 | 说明 |
|------|------|------|
| 爬虫 | Python 3.8+ | requests, BeautifulSoup4 |
| 解析 | Python | markdownify, lxml |
| 文档系统 | VitePress + Vue 3 | TypeScript 支持 |
| 发布系统 | Node.js + TypeScript | TypeScript, Commander.js |
| 部署 | 静态站点 | GitHub Pages, Netlify, 自有服务器 |

---

## 支持和帮助

### 文档位置

| 需求 | 查看文件 |
|------|---------|
| 了解任务进度 | `.claude/todos.md` |
| 初始化步骤 | `SETUP_GUIDE.md` |
| 项目概览 | `README.md` |
| 爬虫使用 | `crawler/README.md` |
| 技术架构 | `ARCHITECTURE.md` |
| 项目状态 | `PROJECT_STATUS.md` |
| 快速开始 | `QUICKSTART.md`（本文件）|

### 问题排查

1. **首先**：查看相关的 README 文件
2. **然后**：检查 `.claude/todos.md` 中的任务描述
3. **最后**：提出具体的问题

---

## 我们已经做了什么

✅ 创建完整的项目结构
✅ 开发了爬虫框架（1500+ 行代码）
✅ 编写了详细的文档
✅ 设计了完整的架构
✅ 创建了任务清单

## 接下来的步骤

⏳ 等你提供网站信息
→ 调整爬虫
→ 运行爬虫爬取数据
→ 搭建 VitePress
→ 开发发布工具
→ 整合和部署

---

## 需要你做的事

1. **提供网站信息**（10 分钟）
   - 网站 HTML 结构
   - 模块组织方式

2. **让我运行爬虫**（10 分钟）
   - 爬取所有文档
   - 生成 Markdown 文件

3. **一起搭建系统**（后续）
   - VitePress 文档站
   - 多平台发布工具

---

## 立即开始

```bash
# 1. 进入项目目录
cd crmeb-docs-platform

# 2. 阅读任务清单（必读！）
cat .claude/todos.md

# 3. 阅读初始化指南
cat SETUP_GUIDE.md

# 4. 向我提供网站信息
# ...告诉我你看到的 HTML 和模块结构

# 5. 等我调整爬虫
# ...

# 6. 我会运行爬虫
# cd crawler && python spider.py
```

---

**准备好了吗？让我们开始吧！**

有任何问题，查看相关的 README 文件或提出具体疑问。
