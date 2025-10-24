# 🤖 智能自动采集爬虫使用指南

> 从网页中自动提取标题和关键字，智能生成输出路径和分类

---

## ✨ 核心功能

### 1️⃣ 自动提取网页标题
从网页 HTML 中智能提取标题：
- 尝试多个选择器：`<div class="title"><h1>` → `<title>` → `meta` 标签
- 自动清理和格式化标题
- 支持多语言标题

```html
<!-- 支持的标题格式 -->
<div class="title"><h1>快速了解</h1></div>      ✅
<h1 class="title">快速开始</h1>                  ✅
<title>Python 快速入门</title>                    ✅
<meta property="og:title" content="API文档">     ✅
```

### 2️⃣ 智能分类和路径生成
根据 URL 和标题自动识别分类和生成路径：

| 关键字 | 输出目录 |
|--------|---------|
| 快速开始、入门、quick、start | `01_快速开始/` |
| 配置、config、setup、install | `02_系统配置/` |
| 商城、商品、shop、store | `03_商城功能/` |
| 商户、merchant、seller | `04_商户管理/` |
| 订单、order、transaction | `05_交易订单/` |
| API、接口、文档 | `06_API文档/` |

### 3️⃣ 自动生成文件名
从标题自动生成清晰的文件名：

```
网页标题: "快速了解 CRMEB"
生成文件名: "快速了解CRMEB.md"

网页标题: "系统配置与安装"
生成文件名: "系统配置与安装.md"
```

### 4️⃣ 完整的日志和报告
记录每次采集的详细信息：
- 采集时间戳
- 源 URL
- 提取的标题
- 输出路径
- 采集状态（成功/失败）

生成采集报告：
```
# 采集报告

## 01_快速开始
- 快速了解CRMEB.md
- 环境安装指南.md
- 项目结构说明.md

## 02_系统配置
- 数据库配置.md
- 缓存设置.md
...
```

---

## 🚀 快速开始

### 方式 1: 采集单个 URL（推荐）

```bash
# 采集单个页面，自动提取标题和生成路径
python3 smart_crawler_auto.py --url "https://doc.crmeb.com/..."

# 输出示例：
# 📝 处理 URL: https://doc.crmeb.com/...
# 📌 提取标题: 快速了解
# 📁 输出路径: /Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/docs/01_快速开始/快速了解.md
# 🏷️  分类: 01_快速开始
# 📄 文件名: 快速了解.md
# ✅ 已保存: ...
```

### 方式 2: 批量采集（从文件读取 URL）

```bash
# 1. 创建 urls.txt 文件，每行一个 URL
cat > urls.txt << 'EOF'
https://doc.crmeb.com/crmebjava/CRMEBjava/25961
https://doc.crmeb.com/crmebjava/CRMEBjava/25962
https://doc.crmeb.com/crmebjava/CRMEBjava/25963
EOF

# 2. 批量采集
python3 smart_crawler_auto.py --file urls.txt

# 3. 查看采集报告
python3 smart_crawler_auto.py --report
```

### 方式 3: 与 TODO_CAIJI.md 配合

```bash
# 1. 在 TODO_CAIJI.md 中只填写 URL（不用填路径）
## 📂 模块 1: Java 开发文档

### 1_快速开始
- URL: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961

# 2. 创建脚本来提取 URL 并采集
python3 << 'EOF'
import re
from smart_crawler_auto import AutoPathCrawler

# 读取 TODO_CAIJI.md
with open('TODO_CAIJI.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取所有 URL
urls = re.findall(r'- URL:\s*(https?://\S+)', content)

# 采集
crawler = AutoPathCrawler('/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc')
for url in urls:
    if url.strip():
        crawler.crawl(url)

# 生成报告
crawler.generate_report()
EOF
```

---

## 📊 工作流程

```
输入: URL 列表
  ↓
[智能采集爬虫]
  ↓
1️⃣ 获取网页 HTML
  ↓
2️⃣ 提取标题（多选择器）
   - <div class="title"><h1> ✅
   - <title> ✅
   - <meta> ✅
  ↓
3️⃣ 自动分类
   - 匹配关键字
   - 确定输出目录
   - 01_快速开始/
   - 02_系统配置/
   - ...
  ↓
4️⃣ 生成文件名
   - 从标题提取
   - 清理特殊字符
   - xxx.md
  ↓
5️⃣ 提取内容
   - HTML → Markdown
  ↓
6️⃣ 保存文件
   - docs/01_快速开始/xxx.md
  ↓
7️⃣ 记录日志
   - logs/collect_20251024.log
  ↓
输出: 采集的 Markdown 文件 + 采集报告
```

---

## 🎯 完整示例

### 输入
```
URL: https://doc.crmeb.com/crmebjava/CRMEBjava/25961
网页 HTML 包含: <div class="title"><h1>快速了解</h1></div>
```

### 自动处理过程
```
1. 获取网页内容 ✅
2. 提取标题 → "快速了解"
3. 匹配关键字 → "快速" 匹配 "快速开始"
4. 确定分类 → "01_快速开始"
5. 生成文件名 → "快速了解.md"
6. 提取网页内容并转换为 Markdown
7. 保存文件 → docs/01_快速开始/快速了解.md
```

### 输出
```
📁 docs/
   └── 01_快速开始/
       └── 快速了解.md          (自动生成，无需手动设置路径)
```

---

## 🔧 高级配置

### 自定义分类关键字

编辑 `smart_crawler_auto.py` 中的 `category_keywords` 字典：

```python
self.category_keywords = {
    '快速开始': '01_快速开始',
    '自定义关键字': '07_自定义分类',
    # 添加更多...
}
```

### 自定义选择器

修改标题选择器优先级：

```python
self.title_selectors = [
    'div.custom-title',      # 你的自定义选择器
    'div.title h1',          # 官方选择器
    'h1',
    'title',
]
```

### 自定义内容提取

修改内容选择器：

```python
self.content_selectors = [
    '.custom-content',
    'main',
    'article',
]
```

---

## 📝 输出文件说明

### 采集日志
```
logs/collect_20251024.log

格式:
{
  "timestamp": "2025-10-24T15:30:45.123456",
  "url": "https://doc.crmeb.com/...",
  "title": "快速了解",
  "output_path": "/path/to/docs/01_快速开始/快速了解.md",
  "status": "success"
}
```

### 采集报告
```
reports/report_20251024.md

# 采集报告

生成时间: 2025-10-24 15:30:45

## 采集结果

### 01_快速开始
- 快速了解.md
- 环境安装.md

### 02_系统配置
- 数据库配置.md

总计: 3 个文件
```

---

## 🐛 故障排查

### Q: 标题提取不出来
**A:**
1. 检查网页是否真的包含标题
2. 在浏览器中右键 → "查看网页源代码"，查找标题元素
3. 如果标题在 JavaScript 中加载，使用 Selenium 版本

### Q: 分类不正确
**A:**
1. 检查关键字匹配规则
2. 编辑 `category_keywords` 添加或调整关键字
3. 查看日志文件确认匹配的关键字

### Q: 文件名包含奇怪字符
**A:**
特殊字符已自动清理（`< > : " / \ | ? *`），可以自定义清理规则

### Q: 采集的内容格式不对
**A:**
1. 修改 `content_selectors` 选择正确的内容区域
2. 使用浏览器开发者工具 (F12) 找到正确的选择器

---

## 💡 使用建议

1. **小批量测试**
   - 先用 1-2 个 URL 测试
   - 检查输出是否正确
   - 调整配置后再大批量采集

2. **定期检查日志**
   - 查看采集报告
   - 确认所有文件都已保存
   - 检查是否有失败的采集

3. **版本控制**
   - 采集后运行 `git add` 和 `git commit`
   - 保存采集记录
   ```bash
   git add docs/
   git commit -m "docs: auto-collected $(date +%Y-%m-%d) content"
   ```

4. **定期维护**
   - 清理重复文件
   - 更新分类关键字
   - 优化选择器配置

---

## 📚 相关文件

- `smart_crawler_auto.py` - 智能采集爬虫主程序
- `TODO_CAIJI.md` - 采集任务映射（只需填 URL）
- `logs/` - 采集日志目录
- `docs/` - 采集结果输出目录

---

## 🎓 工作流对比

### 旧方式（手动填路径）
```
URL + 手动输出路径 → 采集 → 保存
```
❌ 需要手动设计路径
❌ 容易出错
❌ 路径不一致

### 新方式（自动生成路径）
```
URL → [智能爬虫] → 自动提取标题 → 自动分类 → 自动生成路径 → 自动保存
```
✅ 完全自动化
✅ 零手动配置
✅ 路径统一规范
✅ 一致性强

---

**最后更新:** 2025-10-24
**版本:** 1.0.0
**状态:** ✅ 生产就绪

一切都自动化了！让采集变得简单高效！🚀
