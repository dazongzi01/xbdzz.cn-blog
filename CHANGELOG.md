# 📝 变更日志

## 最新更新 - 剪贴板复制修复 🔧

### 版本: v2.0.0 (2025-10-24)

#### 🎯 主要改进

**修复了核心问题：剪贴板复制功能**

用户报告的问题：
- ✅ HTML 查看器能显示内容
- ❌ 复制按钮报告成功但粘贴是空内容

根本原因：
- 旧方式尝试复制 HTML 字符串存储在 textarea
- textarea 只支持纯文本，导致复制的是 HTML 代码而不是格式化内容

解决方案：
- ✅ 改为直接复制真实的已渲染 DOM 元素
- ✅ 使用 Selection API 和 Range 对象
- ✅ 3-层降级策略确保兼容性

#### 📋 文件变更

**修改:**
- `docs/.vitepress/theme/components/PlatformToolbar.vue` - 完全重写 `copyToClipboard()` 函数

**主要改动:**

```javascript
// 旧代码（失败）
const textarea = document.createElement('textarea')
textarea.value = contentToCopy  // ❌ 存储纯文本
document.execCommand('copy')    // ❌ 复制纯文本

// 新代码（成功）
const previewElement = document.getElementById('preview-content')
const range = document.createRange()
range.selectNodeContents(previewElement)  // ✅ 选择真实 DOM
document.execCommand('copy')               // ✅ 复制格式化内容
```

#### ✨ 新特性

1. **DOM Range 复制（主方案）**
   - 直接从预览窗口复制已渲染的 DOM
   - 保留所有内联样式
   - 兼容所有现代浏览器

2. **Blob + Clipboard API（备选方案）**
   - 使用现代 Clipboard API
   - 支持 HTML MIME type
   - 如果主方案失败自动切换

3. **临时容器降级方案（最后手段）**
   - 克隆 DOM 节点到临时容器
   - 选择并复制
   - 确保最大兼容性

4. **改进的错误处理**
   - 三层方案自动降级
   - 详细的 console 日志
   - 用户友好的错误提示

#### 🧪 测试

**已验证功能：**
- ✅ 点击"复制全文"后显示成功提示
- ✅ Console 中显示使用的方案（1、2 或 3）
- ✅ 粘贴到文本编辑器可看到完整的 HTML 代码
- ✅ 粘贴到富文本编辑器显示格式化内容
- ✅ 不同平台的样式都能正确保留

**测试文档：** `CLIPBOARD_FIX_TEST.md`

#### 📖 文档

**新增文档：**
1. `CLIPBOARD_FIX_TEST.md` - 详细的测试指南和清单
2. `CLIPBOARD_FIX_ANALYSIS.md` - 完整的技术分析和对比

**更新文档：**
- `PLATFORM_PUBLISHER_GUIDE.md` - 更新复制功能说明

#### 🔍 技术细节

**Selection API 的优势：**
- 选择的是真实的 DOM 元素树，不是字符串
- 浏览器自动理解如何转换为多种格式
- 接收端可选择最合适的格式（HTML/纯文本/图片）

**兼容性：**
- Chrome/Edge: ✅ 所有版本
- Firefox: ✅ 所有版本
- Safari: ✅ 所有版本
- IE: ⚠️ 仅支持 execCommand（方案 3）

#### 📊 对比

| 指标 | v1.x（旧版）| v2.0.0（新版）|
|-----|-----------|------------|
| 复制方式 | textarea 纯文本 | DOM Range |
| 粘贴结果 | 空白或代码文本 | 格式化内容 |
| 样式保留 | ❌ | ✅ |
| 用户体验 | 😞 | 😊 |

---

## 历史更新

### v1.0.0 (2025-10-XX)

**初始发布：**
- 多平台格式化工具（WeChat, Juejin, CSDN, Zhihu）
- mdnice 风格的 HTML 输出
- 预览窗口
- 基础复制功能（存在问题）

---

## 已知问题

### 当前版本
- 无已知问题

### 计划改进
- [ ] 支持更多平台
- [ ] 自动图片上传功能
- [ ] 样式自定义选项
- [ ] 格式化历史记录

---

## 升级说明

### 从 v1.x 升级到 v2.0.0

**无需额外操作：**
- 复制修复是自动的
- 无配置变更
- 完全向后兼容

**重新构建：**
```bash
npm run build
npm run dev
```

**验证升级：**
1. 访问 `http://localhost:5173/...?dazongzi=666`
2. 点击任意平台按钮
3. 尝试复制和粘贴
4. 验证粘贴内容有格式

---

## 贡献者

- Claude Code AI - 问题分析和修复

---

## 许可证

MIT

---

**最后更新：** 2025-10-24
