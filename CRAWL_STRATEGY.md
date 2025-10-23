# 文档爬虫策略报告

## 网站分析结果

### 网站技术栈

**URL**: https://doc.crmeb.com/crmebjavalandmer/CRMEBjava/25961

**技术框架**:
- 前端框架: Vue.js (Vue 2/3)
- UI 库: Element UI
- 构建工具: 使用组件化架构
- 渲染方式: **客户端动态渲染**（JavaScript 生成菜单和内容）

### 关键发现

1. **菜单是动态生成的**
   - 菜单项通过 Vue 组件 `menu-item` 渲染
   - 使用 Element UI 的 `el-menu` 和 `el-submenu` 组件
   - 静态 HTML 中看不到完整的菜单项目

2. **页面结构**
   - 顶部有菜单切换（logo 下方）
   - 左侧菜单导航栏（通过 JS 动态生成）
   - 中间是主要内容区域
   - 右侧可能是目录或辅助内容

3. **文档链接特点**
   - URL 格式: `/crmebjavalandmer/CRMEBjava/[数字ID]`
   - 例如: `/crmebjavalandmer/CRMEBjava/25961`
   - 通过改变尾部数字可以访问不同的文档

---

## 爬虫解决方案

### 方案对比

#### 方案 A: 简单爬虫 (spider.py, smart_spider.py)
**状态**: ❌ 不可行
**原因**:
- 菜单是 JavaScript 生成的
- 静态 HTML 请求看不到完整菜单
- 无法从静态 HTML 中提取所有文档链接

#### 方案 B: Selenium 爬虫 (selenium_spider.py) ⭐ **推荐**
**状态**: ✅ 可行
**优势**:
- 使用真正的浏览器引擎（Chrome/Safari/Firefox）
- 能够执行 JavaScript，等待页面完全加载
- 可以解析动态生成的菜单
- 可以提取渲染后的完整内容

**工作流程**:
```
1. 用浏览器打开首页
   ↓
2. 等待 JavaScript 加载完成
   ↓
3. 从渲染后的 DOM 中提取菜单链接
   ↓
4. 逐个访问每个菜单项
   ↓
5. 提取文档内容并转换为 Markdown
```

#### 方案 C: 打包工具分析
**状态**: ⏳ 备选
**方式**:
- 直接浏览器访问
- 打开开发者工具 (F12) Network 标签
- 查看 API 请求
- 可能存在 `/api/menu` 或类似的接口

---

## 推荐执行计划

### 第一步：准备 Selenium 环境

你需要安装 ChromeDriver 或使用系统自带的 Safari:

```bash
# macOS 上 Safari 驱动已内置
# 或者安装 ChromeDriver
brew install chromedriver
```

### 第二步：运行 Selenium 爬虫

```bash
cd crawler
python3 selenium_spider.py
```

### 第三步：检查输出

爬虫会生成:
- `output/menu.json` - 菜单结构
- `output/documents.json` - 文档列表
- `output/html/` - 每个文档的 HTML

### 第四步：转换为 Markdown

使用现有的 `parser.py` 和 `cleaner.py` 将 HTML 转换为 Markdown:

```bash
python3 convert_html_to_md.py
```

---

## 可能的挑战和解决方案

### 挑战 1: ChromeDriver 版本不匹配
**解决**: 使用 Safari WebDriver（macOS 内置）

### 挑战 2: 页面加载超时
**解决**: 增加 `wait_time` 参数或等待特定元素

### 挑战 3: 内容太多导致爬虫很慢
**解决**:
- 批量处理
- 多线程爬取
- 缓存已爬取的内容

### 挑战 4: 反爬虫机制
**解决**:
- 添加随机延迟
- 轮换 User-Agent
- 使用代理（如需要）

---

## 下一步行动

1. **确认 Selenium 环境**
   ```bash
   python3 -c "from selenium import webdriver; print('✓ Selenium 已安装')"
   ```

2. **测试爬虫**
   ```bash
   python3 crawler/selenium_spider.py
   ```

3. **如果成功**:
   - 扩大爬虫范围（从 10 个文档到全部）
   - 优化内容提取逻辑
   - 转换为 Markdown

4. **如果失败**:
   - 检查错误日志
   - 尝试 API 分析方案
   - 或手动获取菜单结构

---

## 备选方案：API 分析

如果 Selenium 方案也有问题，可以尝试：

1. 打开网站，按 F12 打开开发者工具
2. 切换到 Network 标签
3. 刷新页面，观察 XHR/Fetch 请求
4. 查看是否有 `/api/menu` 或类似的接口
5. 直接调用 API 获取菜单数据

---

## 工具清单

| 工具 | 功能 | 状态 |
|------|------|------|
| `discover.py` | 发现文档链接 | ⏳ 待改进 |
| `smart_spider.py` | 智能爬虫 | ⏳ 依赖菜单识别 |
| `selenium_spider.py` | Selenium 爬虫 | ✅ 推荐 |
| `parser.py` | HTML→Markdown | ✅ 已就绪 |
| `cleaner.py` | 内容清洁 | ✅ 已就绪 |

---

## 预期结果

按照以上计划，应该能够：

1. ✅ 自动识别所有文档菜单
2. ✅ 爬取每个文档的完整内容
3. ✅ 转换为标准 Markdown 格式
4. ✅ 保持原有的模块和目录结构
5. ✅ 生成 VitePress 可用的文档

**预期耗时**: 30-60 分钟（取决于文档数量和网络速度）

---

**报告生成**: 2024 年 10 月 23 日
**状态**: 准备执行 Selenium 爬虫方案
