# 保留 URL 的采集脚本使用指南

> 采集时保留 URL 链接，只更新采集状态

---

## 问题描述

在采集文档时，需要：
1. ✅ 保留 `- URL:` 字段中粘贴的链接
2. ✅ 只更新 `- 采集状态:` 字段
3. ✅ 不删除任何已有的 URL

---

## 解决方案

### 脚本文件

**smart_crawler_preserve_url.py** - 专门设计来保留 URL 的采集脚本

### 工作原理

```
TODO_CAIJI.md
    ↓
读取所有任务（模块 → 章节 → 任务）
    ↓
提取 URL 和输出路径
    ↓
采集网页内容
    ↓
转换为 Markdown
    ↓
保存文件
    ↓
更新状态（只改变采集状态，保留 URL）
    ↓
记录日志
```

---

## 使用步骤

### 第 1 步：填写 URL

在 TODO_CAIJI.md 中找到对应的任务，粘贴 URL：

```markdown
## 📂 模块 1: Java 开发文档

### 1_快速开始
- 采集状态: [ ]
- 输出路径: `docs/01_快速开始/01_java快速开始.md`
- URL: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961
        ↑ 在这里粘贴链接
```

### 第 2 步：运行采集脚本

```bash
python3 smart_crawler_preserve_url.py
```

或指定文件：

```bash
python3 smart_crawler_preserve_url.py TODO_CAIJI.md
```

### 第 3 步：验证结果

采集完成后，URL 会被保留，只有状态会改变：

```markdown
### 1_快速开始
- 采集状态: [✅]           ← 状态已更新
- 输出路径: `docs/01_快速开始/01_java快速开始.md`
- URL: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961
        ↑ URL 保留完整！
```

---

## 采集状态标记

| 标记 | 含义 | 说明 |
|------|------|------|
| `[ ]` | 未采集 | 没有 URL 或尚未采集 |
| `[✅]` | 采集成功 | 已成功采集并保存 |
| `[❌]` | 采集失败 | 采集过程中出错 |
| `[x]` | 已采集 | 标记为已处理（跳过） |

---

## 脚本功能

### 核心特性

1. **保留 URL**
   - 采集状态更新时不删除 URL
   - 使用正则表达式精确定位状态字段

2. **自动识别任务**
   - 读取 `### 任务标题` 格式
   - 提取 `- URL:` 字段
   - 识别 `- 输出路径:` 字段

3. **错误处理**
   - URL 为空时跳过
   - 网络错误时标记为 `[❌]`
   - 内容提取失败时标记为 `[❌]`

4. **详细日志**
   - 每次采集都记录到日志文件
   - 日志位置：`logs/collect_YYYYMMDD.log`
   - 包含时间戳、URL、状态等信息

---

## 脚本输出示例

```
📂 开始处理: TODO_CAIJI.md

📝 处理 URL: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961
  🔄 正在获取: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961
  📌 提取标题: 快速了解 CRMEB
  ✅ 已保存: /path/to/docs/01_快速开始/01_java快速开始.md
  📝 已更新状态: ### 1_快速开始

📝 处理 URL: https://doc.crmeb.com/...
  ...

📊 采集完成: 成功 3 个, 失败 0 个
```

---

## 日志文件说明

采集日志保存在 `logs/` 目录：

```json
{
  "timestamp": "2025-10-24T21:30:45.123456",
  "url": "https://doc.crmeb.com/...",
  "title": "快速了解",
  "output_path": "/path/to/docs/01_快速开始/快速了解.md",
  "status": "success"
}
```

---

## 高级用法

### 批量采集多个模块

1. 在 TODO_CAIJI.md 中填写多个模块的 URL
2. 一次运行脚本采集所有任务
3. 脚本自动为每个任务更新状态

### 只采集特定任务

1. 在 TODO_CAIJI.md 中只填写需要采集的 URL
2. 其他任务的 URL 留空
3. 脚本会自动跳过空的 URL

### 重新采集

如果需要重新采集：

1. 更改状态为 `[ ]`（未采集）
2. 确保 URL 还在
3. 再次运行脚本

---

## 故障排查

### Q: URL 被删除了？

**A:** 这表示使用的是旧版脚本。请确认使用的是 `smart_crawler_preserve_url.py`

```bash
python3 smart_crawler_preserve_url.py
```

### Q: 状态没有更新？

**A:** 检查以下几点：

1. 采集是否成功（查看控制台输出）
2. 检查日志文件：`logs/collect_YYYYMMDD.log`
3. 确认 TODO_CAIJI.md 格式正确

### Q: 采集失败，状态变成 [❌]

**A:** 原因可能是：

1. **URL 无效** - 在浏览器中测试链接
2. **网络问题** - 检查网络连接
3. **内容格式** - 网站可能使用了 JavaScript 动态加载

解决方案：
- 检查 URL 是否正确
- 重试采集（重新运行脚本）
- 尝试使用 Selenium 版本爬虫

---

## 与其他脚本的区别

| 脚本 | 保留 URL | 自动路径 | 自动分类 | 用途 |
|------|---------|---------|---------|------|
| smart_crawler_preserve_url.py | ✅ | ❌ | ❌ | 使用 TODO_CAIJI.md 采集 |
| smart_crawler_auto.py | ❌ | ✅ | ✅ | 自动生成所有配置 |
| smart_crawler.py | ❌ | ❌ | ❌ | 标准采集脚本 |

---

## 完整工作流

```bash
# 1. 编辑 TODO_CAIJI.md，填写 URL
nano TODO_CAIJI.md

# 2. 运行采集脚本
python3 smart_crawler_preserve_url.py

# 3. 查看采集结果
ls -la docs/01_快速开始/

# 4. 查看日志
tail -20 logs/collect_20251024.log

# 5. 验证 TODO_CAIJI.md
grep "采集状态" TODO_CAIJI.md

# 6. 提交更改
git add TODO_CAIJI.md docs/
git commit -m "docs: collect new content"
git push
```

---

## 常见问题集合

### 能同时采集多个源吗？

可以！在 TODO_CAIJI.md 中为不同的任务填写来自不同网站的 URL，脚本会一次性采集所有的。

### 采集后 URL 为什么还在？

这就是设计的目的！保留 URL 以便：
- 后续重新采集时使用
- 对比原始链接和本地文件
- 追踪文档的来源

### 能自定义输出路径吗？

可以！直接编辑 TODO_CAIJI.md 中的 `- 输出路径:` 字段即可。

---

## 脚本版本

| 版本 | 功能 | 保留 URL |
|------|------|---------|
| preserve_url | 基础采集 | ✅ YES |
| auto | 自动配置 | ❌ NO |
| v2 | 增强功能 | ❌ NO |
| selenium | 动态网站 | ❌ NO |

---

**推荐使用**: `smart_crawler_preserve_url.py` 配合 `TODO_CAIJI.md` 进行大批量采集！

最后更新：2025-10-24
