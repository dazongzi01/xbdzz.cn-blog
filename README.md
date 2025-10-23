# CRMEB 文档平台完整解决方案

一个完整的文档迁移、优化和多平台发布系统。

## 🎯 项目目标

将 CRMEB 现有的文档系统（doc.crmeb.com）迁移到现代化的 VitePress 文档框架，并建立一个智能多平台发布系统，支持自动发布到：

- 📱 微信公众号
- 🔗 掘金
- 📝 CSDN
- 💬 知乎
- 📺 视频内容管理

## 📂 项目结构

```
crmeb-docs-platform/
│
├── .claude/
│   └── todos.md                    # 详细的分步任务清单（标记进度）
│
├── crawler/                        # 文档爬虫工具
│   ├── spider.py                   # 主爬虫程序
│   ├── parser.py                   # HTML 解析和 Markdown 转换
│   ├── cleaner.py                  # 内容清洁和标准化
│   ├── config.json                 # 爬虫配置
│   ├── requirements.txt            # Python 依赖
│   ├── README.md                   # 爬虫使用说明
│   └── output/                     # 爬虫输出目录
│       ├── structure.json          # 文档结构树
│       ├── crawl_report.json       # 爬虫报告
│       └── [modules]/              # 模块目录
│
├── docs/                           # VitePress 文档系统
│   ├── .vitepress/
│   │   ├── config.ts               # 配置文件
│   │   ├── theme/                  # 自定义主题
│   │   └── public/                 # 静态资源
│   ├── index.md                    # 首页
│   ├── api/                        # API 文档
│   ├── guide/                      # 使用指南
│   └── images/                     # 本地图片
│
├── publisher/                      # 多平台发布系统
│   ├── src/
│   │   ├── core/                   # 核心功能
│   │   │   ├── converter.ts        # Markdown 转换引擎
│   │   │   ├── publisher.ts        # 发布管理器
│   │   │   └── tracker.ts          # 版本追踪
│   │   ├── platforms/              # 平台适配器
│   │   │   ├── wechat.ts           # 微信公众号
│   │   │   ├── juejin.ts           # 掘金
│   │   │   ├── csdn.ts             # CSDN
│   │   │   └── zhihu.ts            # 知乎
│   │   ├── templates/              # 样式模板
│   │   │   ├── wechat.css
│   │   │   ├── juejin.css
│   │   │   └── ...
│   │   └── cli.ts                  # CLI 工具
│   ├── package.json
│   └── README.md
│
├── database/                       # 元数据存储
│   ├── articles.json               # 文章索引
│   ├── publish-status.json         # 发布状态
│   └── structure.json              # 文档结构
│
├── scripts/                        # 自动化脚本
│   ├── crawl.sh                    # 爬虫脚本
│   ├── build.sh                    # 构建脚本
│   ├── publish.sh                  # 发布脚本
│   └── update.sh                   # 更新脚本
│
├── SETUP_GUIDE.md                  # 初始化指南
├── README.md                       # 本文件
└── .gitignore

```

## 🚀 快速开始

### 前提条件

- Python 3.8+
- Node.js 16+ & npm
- Git

### 初始化步骤

#### 1. 克隆项目并进入目录

```bash
cd crmeb-docs-platform
```

#### 2. 设置爬虫环境

```bash
cd crawler
pip install -r requirements.txt
```

#### 3. 配置爬虫参数

编辑 `crawler/config.json`：

```json
{
  "base_url": "https://doc.crmeb.com",
  "start_url": "https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961"
}
```

#### 4. 运行爬虫

```bash
python spider.py
```

输出会保存在 `crawler/output/` 目录中

#### 5. 设置 VitePress 文档系统

```bash
cd ../docs
npm install
npm run dev
```

访问 http://localhost:5173 预览文档

## 📋 四个主要阶段

### 阶段 1️⃣：文档爬取与数据处理

- ✅ 分析原站点结构
- ✅ 开发 Python 爬虫（完成基础框架）
- ✅ 保留原有的模块和目录结构
- ✅ 内容清洁和标准化
- ✅ 图片资源下载
- ⏳ **等待**：网站结构信息

### 阶段 2️⃣：VitePress 文档系统搭建

- ⏳ 初始化 VitePress 项目
- ⏳ 配置主题和导航
- ⏳ 迁移爬虫输出的 Markdown 文件
- ⏳ SEO 优化
- ⏳ 搜索功能集成
- ⏳ 视频嵌入组件

### 阶段 3️⃣：多平台发布系统

- ⏳ 格式转换引擎
- ⏳ 平台适配器（微信、掘金、CSDN、知乎）
- ⏳ 样式模板系统
- ⏳ CLI 工具开发
- ⏳ 自动化发布
- ⏳ 版本管理

### 阶段 4️⃣：整合、测试与部署

- ⏳ 端到端测试
- ⏳ 工作流脚本
- ⏳ 文档完善
- ⏳ CI/CD 配置
- ⏳ 部署到生产环境

## 💡 核心功能

### 🕷️ 智能爬虫

```bash
python crawler/spider.py
```

- 递归爬取所有文档页面
- 完全保留原有的目录结构
- 自动转换 HTML 为 Markdown
- 下载图片资源
- 生成详细报告

### 📚 VitePress 文档站

- 现代化的文档界面
- 强大的搜索功能
- 完整的 SEO 支持
- 响应式设计
- 深色/浅色主题切换

### 📤 多平台发布

```bash
# 转换文档
npm run convert docs/guide/module-1.md --platform wechat

# 预览效果
npm run preview docs/guide/module-1.md --platform juejin

# 发布到多个平台
npm run publish docs/guide/module-1.md --platforms juejin,csdn
```

- 一键转换到各平台格式
- 批量发布管理
- 版本追踪
- 样式自定义

## 📊 任务管理

所有任务进度记录在 `.claude/todos.md`，采用 Markdown 检查列表格式：

```markdown
### 阶段一：文档爬取
- [x] 任务已完成
- [ ] 任务待进行
```

## 🔧 常用命令

### 爬虫

```bash
cd crawler
python spider.py                    # 运行爬虫
python spider.py --help            # 查看帮助
```

### 文档系统

```bash
cd docs
npm install                         # 安装依赖
npm run dev                         # 开发模式
npm run build                       # 构建生产版本
npm run preview                     # 预览构建结果
```

### 发布系统

```bash
cd publisher
npm install                         # 安装依赖
npm run build                       # 构建
npm run publish --help              # 查看发布命令帮助
```

## 📝 文档

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 详细的初始化指南
- [crawler/README.md](crawler/README.md) - 爬虫使用说明
- [.claude/todos.md](.claude/todos.md) - 完整的任务清单（推荐）

## 🤝 贡献

任何问题或建议都欢迎！

## 📄 License

MIT

---

## 下一步

1. **查看 SETUP_GUIDE.md** - 获取详细的初始化步骤
2. **查看 .claude/todos.md** - 了解所有任务和进度
3. **提供网站结构信息** - 帮助我定制爬虫
4. **开始爬虫工作** - 获取所有文档内容

## 联系

有任何问题，请查阅相应的 README 文件或提交 Issue。
