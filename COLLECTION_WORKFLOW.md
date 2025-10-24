# 📚 采集工作流程指南

> 快速开始使用 TODO_CAIJI.md + smart_crawler.py 进行大批量采集

---

## 🎯 核心概念

### 文件结构
```
My_Doc/
├── TODO_CAIJI.md              ← 采集任务映射文件（你需要填写这个）
├── smart_crawler.py           ← 自动采集脚本（会自动运行）
├── smart_crawler_v2.py        ← v2 版本爬虫
├── smart_crawler_selenium.py  ← Selenium 版本（支持JavaScript）
└── docs/                      ← 采集结果输出目录
    ├── 01_快速开始/
    ├── 02_系统配置/
    ├── 03_商城功能/
    ├── 04_商户管理/
    ├── 05_交易订单/
    └── 06_API文档/
```

---

## 📋 使用步骤

### 步骤 1: 编辑 TODO_CAIJI.md

打开 `TODO_CAIJI.md` 文件，在对应模块下填写采集链接：

```markdown
## 📂 模块 1: Java 开发文档

### 1_快速开始
- 采集状态: [ ]
- 输出路径: `docs/01_快速开始/01_java快速开始.md`
- URL: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961
      ↑ 在这里填写采集链接

### 2_环境配置
- 采集状态: [ ]
- 输出路径: `docs/01_快速开始/02_环境配置.md`
- URL: https://doc.crmeb.com/...
```

**关键说明：**
- 保持格式不变（不要删除 `- ` 和 `-`）
- 一个链接对应一个任务
- 输出路径会自动生成 Markdown 文件

---

### 步骤 2: 运行采集脚本

#### 方式 A: 自动采集（推荐）
```bash
# 自动读取 TODO_CAIJI.md，采集所有填写了 URL 的任务
python3 smart_crawler.py
```

**做什么：**
1. ✅ 读取 `TODO_CAIJI.md` 中的所有 URL
2. ✅ 逐个访问并采集内容
3. ✅ 转换为 Markdown 格式
4. ✅ 保存到 `docs/` 对应目录
5. ✅ 自动更新任务状态为 `[✅]`

#### 方式 B: 使用 v2 版本爬虫
```bash
# v2 版本，功能更多，爬虫更稳定
python3 smart_crawler_v2.py
```

#### 方式 C: 使用 Selenium 爬虫（支持 JavaScript）
```bash
# 当目标网站使用了 JavaScript 动态加载时使用
python3 smart_crawler_selenium.py
```

---

### 步骤 3: 验证采集结果

采集完成后，检查结果：

```bash
# 查看采集的文件
ls -la docs/01_快速开始/
ls -la docs/02_系统配置/
# ... 等等

# 查看 TODO_CAIJI.md 中的状态
cat TODO_CAIJI.md | grep "采集状态"
```

**预期输出：**
```
- 采集状态: [✅]  ← 表示采集完成
```

---

## 📊 采集统计示例

采集前（空）：
```
| 模块 | 总任务数 | 已采集 | 采集率 |
|------|--------|--------|--------|
| 模块 1 | 3 | 0 | 0% |
| 总计 | 20 | 0 | 0% |
```

采集后（完成）：
```
| 模块 | 总任务数 | 已采集 | 采集率 |
|------|--------|--------|--------|
| 模块 1 | 3 | 3 | 100% |
| 模块 2 | 3 | 3 | 100% |
| ...   | ... | ... | ... |
| 总计 | 20 | 20 | 100% |
```

---

## 🔧 高级用法

### 采集特定模块
```bash
# 修改 smart_crawler.py，或在脚本中指定：
python3 smart_crawler.py --module "模块1"
```

### 采集特定 URL
```bash
python3 smart_crawler.py --url "https://example.com/doc"
```

### 批量采集多个源
```bash
# 编辑 TODO_CAIJI.md，添加多个来源的链接
# 例如：来自不同文档站点的链接
```

---

## ⚠️ 常见问题

### Q: 采集失败了怎么办？

**A:** 检查以下几点：

1. **URL 是否正确？**
   - 在浏览器中测试链接是否可以打开
   - 确保链接格式正确（以 `https://` 开头）

2. **网站是否有反爬虫？**
   - 尝试使用 Selenium 版本：`python3 smart_crawler_selenium.py`
   - 增加延迟时间

3. **网络连接？**
   - 检查网络连接
   - 尝试手动访问该 URL

### Q: 采集速度太慢怎么办？

**A:**
- 检查网络速度
- 在 `crawler/config.json` 中增加 `concurrent_requests` 值
- 减少 `delay_between_requests` 延迟

### Q: 如何修改输出目录？

**A:** 编辑 `TODO_CAIJI.md` 中的 `输出路径` 字段：
```markdown
- 输出路径: `docs/自定义目录/文件名.md`
```

### Q: 如何只采集某些任务？

**A:**
- 将不需要的任务的 URL 留空
- 或在 `采集状态` 中标记为 `[x]`（跳过）
- 只有有效的 URL 会被采集

---

## 📝 采集最佳实践

### 1. 批量采集前的准备
```bash
# 1. 编辑 TODO_CAIJI.md，填写所有 URL
# 2. 备份现有的采集结果（可选）
cp -r docs docs.backup

# 3. 运行采集
python3 smart_crawler.py

# 4. 检查结果
git status
git diff
```

### 2. 提交采集结果
```bash
# 1. 查看采集了什么
git status

# 2. 添加更改
git add -A

# 3. 提交
git commit -m "docs: collect new documentation

- Collected 20 documents from CRMEB
- Updated TODO_CAIJI.md status
- Added markdown files to docs/"

# 4. 推送（可选）
git push
```

### 3. 监控采集进度
```bash
# 实时查看进度
watch -n 1 "cat TODO_CAIJI.md | grep '\[✅\]' | wc -l"

# 查看完成百分比
grep -c "\[✅\]" TODO_CAIJI.md  # 已完成
grep -c "\[ \]" TODO_CAIJI.md   # 待采集
```

---

## 🚀 自动化采集（高级）

### 定时采集
```bash
# 使用 cron 定时运行采集脚本
crontab -e

# 每天晚上 8 点运行采集
0 20 * * * cd /Users/dazongzi/ZBKJ/CODEMANGER/My_Doc && python3 smart_crawler.py >> logs/collect.log 2>&1
```

### 采集后自动提交
```bash
# 创建自动化脚本 auto_collect.sh
#!/bin/bash
cd /Users/dazongzi/ZBKJ/CODEMANGER/My_Doc

# 运行采集
python3 smart_crawler.py

# 自动提交
git add TODO_CAIJI.md docs/
git commit -m "auto: daily collection $(date +%Y-%m-%d)"
git push
```

---

## 📚 支持的输入格式

### 支持的链接格式
- ✅ `https://doc.crmeb.com/...`
- ✅ `https://example.com/page`
- ✅ `http://example.com/...`
- ❌ `example.com/...`（必须包含协议）

### 支持的 HTML 内容
- ✅ 标准 HTML 文档
- ✅ Markdown 转 HTML
- ✅ 富文本内容
- ⚠️ JavaScript 动态加载（需要 Selenium 版本）

---

## 🎓 工作流程图

```
开始
  ↓
编辑 TODO_CAIJI.md（填写 URL）
  ↓
运行 python3 smart_crawler.py
  ↓
脚本读取 TODO_CAIJI.md
  ↓
逐个采集 URL 内容
  ↓
转换为 Markdown
  ↓
保存到 docs/ 目录
  ↓
更新 TODO_CAIJI.md 状态为 [✅]
  ↓
采集完成！
  ↓
运行 git add & git commit
  ↓
结束
```

---

## ✅ 检查清单

采集前：
- [ ] 编辑了 TODO_CAIJI.md，填写了所有需要采集的 URL
- [ ] 确认 URL 格式正确
- [ ] 网络连接正常
- [ ] 备份了现有文档

采集中：
- [ ] 脚本正在运行（可看到进度输出）
- [ ] 没有明显的错误信息

采集后：
- [ ] 检查了输出的 Markdown 文件
- [ ] 验证了 TODO_CAIJI.md 的状态更新
- [ ] 提交了更改到 Git
- [ ] 构建了文档网站（可选）

---

## 📞 获取帮助

查看脚本内的帮助信息：
```bash
python3 smart_crawler.py --help
python3 smart_crawler_v2.py --help
python3 smart_crawler_selenium.py --help
```

查看采集日志：
```bash
# 如果有日志文件
cat logs/collect.log
tail -f logs/collect.log
```

---

**最后更新:** 2025-10-24
**版本:** 1.0.0
**状态:** ✅ 就绪

一切都准备好了，可以开始大批量采集！🚀
