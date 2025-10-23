# CRMEB 文档平台完整任务清单

## 📊 项目概述
- 目标：将现有 doc.crmeb.com 文档迁移到 VitePress，并实现多平台发布系统
- 原则：完全保持原站点的模块和目录结构
- 周期：4 个阶段，逐步完成和标记

---

## 🎯 阶段一：文档爬取与数据处理

### 1.1 分析原站点结构
- [ ] 访问 https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961
- [ ] 分析导航结构（模块、章节、小节）
- [ ] 识别文档的 URL 模式和层级关系
- [ ] 记录原始目录树到 database/structure.json
- [ ] 文档：创建 crawler/ANALYSIS.md 记录发现

### 1.2 开发 Python 爬虫
- [ ] 创建 crawler/requirements.txt
- [ ] 编写 crawler/spider.py（主爬虫）
  - 递归爬取所有文档页面
  - 识别和跟踪导航结构
  - 保持原有模块分组
- [ ] 编写 crawler/parser.py（内容解析）
  - 提取页面标题
  - 提取正文内容
  - 解析文档中的链接
- [ ] 编写 crawler/cleaner.py（内容清洗）
  - 移除 HTML 标签
  - 统一 Markdown 格式
  - 处理特殊符号和编码
- [ ] 创建 crawler/config.json（配置文件）
  - 目标 URL
  - 存储策略
  - 并发参数

### 1.3 数据存储与组织
- [ ] 在 crawler/output 中创建完整的目录树（按原站点结构）
- [ ] 每个文档保存为独立的 .md 文件
- [ ] 创建 crawler/output/structure.json 记录完整的层级关系
- [ ] 记录每个文档的元信息（原始 URL、标题、位置、关联资源等）

### 1.4 处理资源文件
- [ ] 识别文档中的所有图片链接
- [ ] 下载图片到本地：crawler/output/images/[模块]/
- [ ] 更新 Markdown 中的图片路径
- [ ] 处理其他资源（PDF、代码文件等）

### 1.5 生成索引和验证
- [ ] 创建 crawler/output/INDEX.md（全局索引）
- [ ] 生成 database/articles.json（文章元信息表）
  ```json
  {
    "articles": [
      {
        "id": "unique_id",
        "title": "文章标题",
        "module": "模块名",
        "path": "相对路径",
        "url": "原始URL",
        "children": []
      }
    ]
  }
  ```
- [ ] 验证爬取的完整性
- [ ] 生成爬虫运行报告（crawler/REPORT.md）

---

## 🎯 阶段二：VitePress 文档站建设

### 2.1 项目初始化
- [ ] npm init in docs/
- [ ] 安装 VitePress: npm install vitepress vue
- [ ] 创建初始文件结构
- [ ] 创建 docs/.vitepress/config.ts

### 2.2 配置主题和导航
- [ ] 根据 database/structure.json 生成导航配置
- [ ] 配置 docs/.vitepress/sidebar.ts（侧边栏）
  - 按原始模块组织
  - 支持多级嵌套
- [ ] 配置 docs/.vitepress/nav.ts（顶部导航）
- [ ] 自定义主题颜色和品牌

### 2.3 迁移文档内容
- [ ] 复制 crawler/output 中的 Markdown 文件到 docs/
- [ ] 保持原有的目录结构
- [ ] 检查并修复路径和链接
- [ ] 验证图片引用正确

### 2.4 SEO 优化
- [ ] 配置 meta 标签和描述
- [ ] 生成 sitemap
- [ ] 配置 robots.txt
- [ ] 添加 OpenGraph 元数据
- [ ] 实现结构化数据 (JSON-LD)

### 2.5 功能特性
- [ ] 配置全文搜索（algolia 或 mini-search）
- [ ] 创建视频嵌入组件（docs/.vitepress/theme/VideoPlayer.vue）
- [ ] 配置代码高亮主题
- [ ] 实现首页自定义
- [ ] 添加面包屑导航

### 2.6 构建和测试
- [ ] npm run build
- [ ] npm run preview（本地预览）
- [ ] 检查所有页面是否正常渲染
- [ ] 性能优化（图片压缩、代码分割等）

---

## 🎯 阶段三：多平台发布系统

### 3.1 项目初始化
- [ ] npm init in publisher/
- [ ] 安装依赖: typescript, commander, prettier 等
- [ ] 创建 tsconfig.json
- [ ] 创建项目文件结构

### 3.2 格式转换引擎
- [ ] 创建 publisher/src/core/converter.ts
  - 基础 Markdown 解析
  - AST 构建和遍历
- [ ] 创建平台适配器基类: publisher/src/platforms/base.ts
- [ ] 实现微信公众号适配器: publisher/src/platforms/wechat.ts
  - 处理代码块样式
  - 处理引用样式
  - 处理表格转换
  - 生成富文本 HTML
- [ ] 实现掘金适配器: publisher/src/platforms/juejin.ts
- [ ] 实现 CSDN 适配器: publisher/src/platforms/csdn.ts
- [ ] 实现知乎适配器: publisher/src/platforms/zhihu.ts

### 3.3 样式模板系统
- [ ] 创建 publisher/templates/ 目录
- [ ] 微信公众号样式: publisher/templates/wechat.css
  - 代码块样式
  - 引用样式
  - 标题样式
  - 链接样式
- [ ] 其他平台样式模板
- [ ] 创建模板管理器: publisher/src/core/template-manager.ts

### 3.4 状态管理和追踪
- [ ] 创建 publisher/src/core/tracker.ts
  - 记录发布状态
  - 版本管理
  - 更新追踪
- [ ] 更新 database/publish-status.json 结构
- [ ] 实现发布历史记录

### 3.5 CLI 工具开发
- [ ] 创建 publisher/src/cli.ts
- [ ] 实现命令：
  - `publish [file]` - 发布单篇文章
  - `convert [file] --platform [name]` - 格式转换
  - `preview [file] --platform [name]` - 预览
  - `batch [dir]` - 批量发布
  - `status` - 查看发布状态
  - `update [file]` - 更新已发布的文章
  - `link-video [file] --url [video-url]` - 关联视频

### 3.6 自动化发布集成
- [ ] 掘金 API 集成: publisher/src/api/juejin.ts
- [ ] CSDN API 集成（如果可用）
- [ ] 公众号发布流程（生成富文本）
- [ ] 知乎发布流程（API 或手动）

---

## 🎯 阶段四：整合、测试与部署

### 4.1 工作流脚本
- [ ] 创建 scripts/crawl.sh（爬虫脚本）
- [ ] 创建 scripts/build.sh（构建脚本）
- [ ] 创建 scripts/publish.sh（发布脚本）
- [ ] 创建 scripts/update.sh（更新脚本）

### 4.2 端到端测试
- [ ] 测试爬虫工作流
  - 完整爬取
  - 目录结构验证
  - 资源完整性验证
- [ ] 测试文档构建
  - 本地预览
  - 所有页面加载
  - 链接有效性
  - SEO 验证
- [ ] 测试发布流程
  - 格式转换正确性
  - 各平台样式渲染
  - 自动发布功能

### 4.3 文档完善
- [ ] 创建 README.md（项目概述）
- [ ] 创建 crawler/README.md（爬虫使用说明）
- [ ] 创建 publisher/README.md（发布系统使用说明）
- [ ] 创建 WORKFLOW.md（完整工作流说明）
- [ ] 创建最佳实践指南

### 4.4 部署配置
- [ ] 配置 VitePress 构建输出
- [ ] 部署到 GitHub Pages 或自有服务器
- [ ] 配置 CI/CD（GitHub Actions）
- [ ] 设置自动构建触发器

### 4.5 维护和监控
- [ ] 设置监控告警
- [ ] 创建维护计划
- [ ] 记录常见问题和解决方案

---

## ✅ 检查清单

### 最终验证
- [ ] 所有源文档都已成功迁移
- [ ] VitePress 站点正常运行，无 404 或错误
- [ ] 所有图片和资源都正确加载
- [ ] SEO 优化已实施
- [ ] 发布系统可以一键转换和发布到多个平台
- [ ] 文档完整，使用者可以快速上手
- [ ] 整个工作流可以自动化执行

---

## 📝 进度统计

- 总任务数: 待计算
- 已完成:
- 进行中:
- 未开始:

---

## 🔗 关键资源

- 原始文档: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/
- VitePress 文档: https://vitepress.dev/
- 爬虫最佳实践: 待补充
- 各平台 API 文档: 待补充
