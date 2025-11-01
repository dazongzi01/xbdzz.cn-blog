# 📦 build.sh 脚本说明

## 🎯 功能

`build.sh` 是一个**自动化文档构建脚本**，用于：

1. **过滤未采集的文档** - 根据 `TODO_CAIJI.md` 配置，过滤掉未收集的文档
2. **构建 VitePress 文档** - 将 Markdown 文档编译成静态网站
3. **生成部署文件** - 输出到 `docs/.vitepress/dist` 目录

## 📋 脚本工作流程

```
步骤 1: 过滤未采集的文档
  ├─ 运行 Python 脚本 (scripts/filter-collected-docs.py)
  ├─ 读取 TODO_CAIJI.md 配置
  └─ 过滤掉未采集的 Markdown 文件

步骤 2: 构建文档
  ├─ 运行 npm run build:force
  ├─ VitePress 编译所有文档
  └─ 生成 HTML 静态文件
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
# 直接运行
./build.sh

# 或者用 bash 运行
bash build.sh
```

### 预期输出

```
======================================
   📦 文档构建脚本
======================================

[信息] 步骤 1/2: 正在过滤未采集的文档...
--------------------------------------
[成功] 文档过滤完成

--------------------------------------
[信息] 步骤 2/2: 正在构建文档...
--------------------------------------
[成功] 文档构建完成！

[信息] 构建输出目录: docs/.vitepress/dist
[信息] 生成的 HTML 文件数: 42

[信息] 预览构建结果:
  npm run preview

======================================
[成功] ✅ 构建流程已完成
======================================
```

## ⚠️ 当前问题

### 🔴 缺失的依赖文件

脚本依赖的文件**目前不存在**：

| 文件 | 用途 | 状态 |
|------|------|------|
| `scripts/filter-collected-docs.py` | Python 过滤脚本 | ❌ 不存在 |
| `TODO_CAIJI.md` | 采集配置文件 | ⚠️ 存在但可能不完整 |

### 🔧 后果

如果现在运行 `./build.sh`，会出现错误：

```
[错误] 找不到过滤脚本: scripts/filter-collected-docs.py
```

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

## 🎯 要使 build.sh 完全可用

需要：

1. **创建 Python 过滤脚本**
   ```bash
   mkdir -p scripts
   touch scripts/filter-collected-docs.py
   ```

2. **实现过滤逻辑**
   - 读取 `TODO_CAIJI.md`
   - 解析已采集的文档列表
   - 删除或隐藏未采集的文档

3. **更新 TODO_CAIJI.md**
   - 明确列出所有已采集的文档
   - 跟踪采集进度

## 💡 建议

### 短期（立即）
- 使用 `npm run dev` 进行开发
- 使用 `npm run build` 进行构建
- **暂不需要** `build.sh`

### 中期（本周）
- 如果需要文档过滤功能，创建 Python 脚本
- 完成 `scripts/` 目录结构
- 实现自动过滤逻辑

### 长期（持续）
- 完成 `build.sh` 的所有功能
- 集成 CI/CD 流程
- 自动化部署

## 🔄 当前推荐工作流

```bash
# 1. 开发时实时预览
npm run dev

# 2. 编辑完成后构建
npm run build:force

# 3. 预览最终结果
npm run preview

# 4. 提交到 git
git add . && git commit -m "message"
```

---

## 📌 总结

**build.sh 的用途：** 自动化文档构建和过滤

**当前状态：** ⚠️ 不完整（缺少过滤脚本）

**建议：** 暂时使用 npm 命令，未来需要时再完善 build.sh

