# 📦 build.sh 脚本说明

## 🎯 功能

`build.sh` 是一个**VitePress 文档编译脚本**，用于：

1. **编译 Markdown 文档** - 将所有 Markdown 文件编译成静态网站
2. **生成静态文件** - 输出到 `docs/.vitepress/dist` 目录
3. **显示编译统计** - 可选显示 HTML、JS、CSS、图片等文件统计

## 📋 脚本工作流程

```
步骤: 构建文档
  ├─ 检查 Node.js 和 npm 环境
  ├─ 运行 npm run build:force
  ├─ VitePress 编译所有文档
  ├─ 生成 HTML 静态文件
  └─ 显示统计信息（可选）
```

## 🚀 使用方法

### 前置条件

脚本需要以下环境：

```bash
✓ Python3 - 用于过滤脚本
✓ Node.js - 用于 npm 命令
✓ npm 依赖 - 已在 package.json 中配置
```

### 基本使用

```bash
# 直接编译
./build.sh

# 编译并显示统计
./build.sh --stats

# 显示帮助
./build.sh --help
```

### 预期输出

```
╔════════════════════════════════════════════════════════════════╗
║                    📦 VitePress 编译脚本
╚════════════════════════════════════════════════════════════════╝

✓ Node.js v18.x.x
✓ npm 8.x.x

ℹ 开始编译文档...

✓ 编译完成！

📊 编译统计：
  HTML 文件:   45
  JavaScript:  12
  CSS 文件:    8
  图片文件:    20
  总文件数:    95

📈 大小统计：
  总大小:      2.5M

📁 输出目录：
  docs/.vitepress/dist/

📝 后续步骤：
  预览: npm run preview
  部署: ./deploy.sh all
```

## ✅ 更新说明

脚本已经过修复和优化：

| 功能 | 状态 |
|------|------|
| 编译文档 | ✅ 正常工作 |
| 显示统计 | ✅ 支持 --stats 选项 |
| 环境检查 | ✅ 检查 Node.js 和 npm |
| 彩色输出 | ✅ 清晰的进度显示 |

所有依赖文件都已存在，脚本可以正常执行。

## 📝 相关文件说明

### 其他构建脚本

你项目中还有其他构建脚本：

| 脚本 | 用途 |
|------|------|
| `generate.sh` | 生成器脚本 |
| `workflow.sh` | 完整工作流脚本 |
| `run-full-workflow.sh` | 运行完整工作流 |
| `write.sh` | 文档写入脚本 |

### 直接构建方式（当前可用）

如果 `build.sh` 不可用，可以直接使用 npm 命令：

```bash
# 开发模式（实时预览）
npm run dev

# 生产构建
npm run build

# 强制构建（清除缓存）
npm run build:force

# 预览构建结果
npm run preview
```

## 🎯 常见用法

### 编译文档
```bash
./build.sh
```
直接编译所有 Markdown 文件成静态网站。

### 编译并查看统计
```bash
./build.sh --stats
```
编译后显示生成的 HTML、JS、CSS、图片数量和总大小。

### 完整工作流
```bash
# 1. 开发时实时预览
npm run dev

# 2. 编辑完成后编译
./build.sh --stats

# 3. 预览最终结果
npm run preview

# 4. 部署到服务器
./deploy.sh all

# 5. 提交到 git
git add . && git commit -m "message"
```

---

## 📌 总结

**build.sh 的用途：** VitePress 文档编译脚本

**当前状态：** ✅ 完全可用

**功能：**
- 编译 Markdown 文档成静态网站
- 支持 --stats 选项显示编译统计
- 环境检查和彩色输出
- 提示后续步骤（预览、部署）

