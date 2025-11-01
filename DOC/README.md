# 📚 文档和脚本总索引

这个文件夹包含所有项目的文档、工具脚本和配置指南，按功能模块组织。

> **💡 提示**：常用脚本 `build.sh`, `write.sh`, `generate.sh`, `deploy.sh` 都有**根目录副本**，可以直接在根目录运行，无需进入 `DOC/` 文件夹。这些脚本在本文件夹中也有完整源文件供备份和查看。

---

## 📁 目录结构

### 🚀 [Deployment](./Deployment) - 部署相关

编译、打包和部署到服务器的完整方案。

| 文件 | 说明 |
|------|------|
| **deploy.sh** | 自动化部署脚本（编译→打包→上传） |
| **DEPLOY_GUIDE.md** | 详细部署指南和最佳实践 |

**快速开始**：
```bash
./DOC/Deployment/deploy.sh build        # 编译
./DOC/Deployment/deploy.sh all          # 编译+打包
./DOC/Deployment/deploy.sh deploy user@server.com /path  # 完整部署
```

---

### 🛠️ [Build_Scripts](./Build_Scripts) - 构建和工作流

文档构建、生成和完整工作流脚本。

| 文件 | 说明 |
|------|------|
| **BUILD_SCRIPT_GUIDE.md** | build.sh 脚本说明 |
| **build.sh** | 文档构建脚本 |
| **generate.sh** | 文档生成器 |
| **write.sh** | 自动写作脚本 |
| **workflow.sh** | 基础工作流 |
| **run-full-workflow.sh** | 完整工作流执行脚本 |

**相关命令**：
```bash
npm run dev              # 开发预览
npm run build:force      # 强制编译
npm run preview          # 预览构建结果
```

---

### 📢 [Platform_Publishing](./Platform_Publishing) - 多平台发布

将文章发布到微信、掘金、CSDN、知乎等平台的工具和指南。

| 文件 | 说明 |
|------|------|
| **PLATFORM_PUBLISHER_GUIDE.md** | 详细发布指南 |
| **PLATFORM_PUBLISHER_QUICK_START.md** | 快速开始指南 |

**使用方法**：
1. 在文档URL后加 `?dazongzi=666` 激活工具栏
2. 选择目标平台预览效果
3. 点击"复制全文"一键复制

**示例**：
```
http://localhost:5173/01_初步了解/01_快速了解?dazongzi=666
```

---

### 📋 [Content_Rules](./Content_Rules) - 内容规范和格式规则

跨平台内容格式规范和检查清单。

| 文件 | 说明 |
|------|------|
| **CROSS_PLATFORM_FORMAT_RULES.md** | 4大格式规则和详细说明 |
| **FORMAT_RULES_SUMMARY.md** | 规则快速总结 |

**4大核心规则**：
1. 流程图 → 纯文本描述
2. ASCII表格 → Markdown表格
3. 多级列表 → 标准列表
4. 架构图 → 分层文字描述

---

### 🐛 [Bug_Fixes](./Bug_Fixes) - 已修复的问题和调整

项目进行中修复的问题、CSS调整和相关文档。

| 文件 | 说明 |
|------|------|
| **COPY_BUTTON_FIX_SUMMARY.md** | 复制按钮修复总结 |
| **COPY_BUTTON_VERIFICATION.md** | 复制按钮验证过程 |
| **CSS_LAYOUT_FIXES.md** | CSS布局修复说明 |
| **README_FIX.md** | README修复记录 |

这些是已完成的工作文档，供参考。

---

### 📊 [System_Status](./System_Status) - 系统状态和总结

项目整体状态和历史总结。

| 文件 | 说明 |
|------|------|
| **SYSTEM_STATUS.md** | 当前系统状态 |
| **MASTER_SUMMARY.md** | 工作总结和里程碑 |

---

## 🎯 快速参考

### 常见任务

| 任务 | 命令 | 位置 |
|------|------|------|
| **开发预览** | `npm run dev` | 根目录 |
| **编译构建** | `npm run build:force` | 根目录 |
| **自动部署** | `./deploy.sh all` | 根目录 |
| **发布到平台** | 添加 `?dazongzi=666` | 文档URL |
| **查看部署指南** | `./DOC/Deployment/DEPLOY_GUIDE.md` | 本目录 |
| **查看发布指南** | `./DOC/Platform_Publishing/PLATFORM_PUBLISHER_GUIDE.md` | 本目录 |

### 工作流程

```
1. 写文章
   └─ 参考：docs/01_初步了解/

2. 本地测试
   └─ npm run dev

3. 编译构建
   └─ npm run build:force

4. 发布到多平台（可选）
   └─ 添加 ?dazongzi=666 参数，选择平台复制

5. 部署到服务器
   └─ ./DOC/Deployment/deploy.sh deploy user@server /path
```

---

## 📖 文件索引

需要找特定文档？

- **部署问题** → `DOC/Deployment/DEPLOY_GUIDE.md`
- **发布问题** → `DOC/Platform_Publishing/PLATFORM_PUBLISHER_GUIDE.md`
- **格式问题** → `DOC/Content_Rules/CROSS_PLATFORM_FORMAT_RULES.md`
- **脚本帮助** → `DOC/Build_Scripts/BUILD_SCRIPT_GUIDE.md`
- **往期问题** → `DOC/Bug_Fixes/` 或 `DOC/System_Status/`

---

**主README文档**：[../README.md](../README.md)
