# 🚀 VitePress 编译和部署指南

> 一键编译 → 打包 → 部署的完整脚本

## 📋 快速开始

### 1️⃣ 编译文档

```bash
./deploy.sh build
```

**输出：** `docs/.vitepress/dist/` 目录（静态网站文件）

### 2️⃣ 查看编译统计

```bash
./deploy.sh build --stats
```

**显示：**
- HTML 文件数
- JavaScript 文件数
- CSS 文件数
- 图片文件数
- 总文件数和大小

### 3️⃣ 打包部署文件

```bash
./deploy.sh package
```

**输出：** `deploy/vitepress-dist_YYYYMMDD_HHMMSS.tar.gz` 压缩包

### 4️⃣ 完整流程（推荐）

```bash
./deploy.sh all
```

**步骤：**
1. ✓ 编译文档
2. ✓ 显示统计
3. ✓ 打包部署文件

### 5️⃣ 上传到服务器

```bash
./deploy.sh deploy user@example.com /var/www/html
```

**步骤：**
1. ✓ 编译文档
2. ✓ 显示统计
3. ✓ 打包部署文件
4. ✓ 上传到服务器
5. ✓ 显示部署说明

---

## 🎯 完整的部署流程

### 场景 1: 本地构建，自己手动上传

```bash
# 第一步：完整编译和打包
./deploy.sh all

# 第二步：手动上传 deploy 目录下的包到服务器
# 或者通过其他方式（FTP、云存储等）上传

# 第三步：在服务器上解压并部署
# 参考下面的"服务器部署步骤"
```

### 场景 2: 完全自动化部署

```bash
# 一条命令搞定：编译 + 打包 + 上传
./deploy.sh deploy user@example.com /var/www/html
```

---

## 📦 服务器部署步骤

假设已经通过 `./deploy.sh deploy` 上传了包，或手动上传了 `vitepress-dist_*.tar.gz`：

### 步骤 1: 登录服务器

```bash
ssh user@example.com
```

### 步骤 2: 进入目标目录

```bash
cd /var/www/html
```

### 步骤 3: 解压部署包

```bash
tar -xzf vitepress-dist_20240101_120000.tar.gz
```

**结果：** 创建 `dist/` 目录，包含所有静态文件

### 步骤 4: 备份旧版本（可选）

```bash
# 如果之前有旧的网站文件
mv html html.backup
```

### 步骤 5: 移动新版本到位置

```bash
# 方案 A: 将 dist 目录内容移到当前位置
mv dist/* .

# 方案 B: 将 dist 目录改名为 html
mv dist html
```

### 步骤 6: 清理临时文件

```bash
rm vitepress-dist_20240101_120000.tar.gz
```

### 步骤 7: 验证部署

```bash
# 检查关键文件是否存在
ls -la index.html
ls -la assets/

# 查看文件数量
find . -type f | wc -l
```

---

## 🛠️ 脚本详解

### 可用命令

| 命令 | 说明 | 输出 |
|------|------|------|
| `build` | 编译文档 | `docs/.vitepress/dist/` |
| `build --stats` | 编译并显示统计 | 编译结果 + 文件统计 |
| `package` | 打包部署文件 | `deploy/*.tar.gz` |
| `all` | 编译 + 打包 | 完整的部署包 |
| `deploy <server> <path>` | 完整部署流程 | 上传到服务器 |
| `clean` | 清理构建文件 | 删除临时文件 |
| `help` | 显示帮助 | 命令列表 |

### 脚本功能

✅ **环境检查**
- 验证 Node.js 和 npm 已安装
- 检查 package.json 和 docs 目录

✅ **自动编译**
- 清理旧构建文件
- 运行 `npm run build:force`
- 生成静态网站

✅ **编译统计**
- HTML、JS、CSS、图片文件计数
- 总文件数和大小统计
- 构建目录路径显示

✅ **智能打包**
- 压缩成 tar.gz 格式
- 自动保留最近 5 个包
- 自动清理旧包

✅ **一键上传**
- 使用 scp 上传到服务器
- 自动生成部署说明
- 显示服务器部署步骤

✅ **彩色输出**
- 清晰的进度显示
- 错误和成功提示
- 易于阅读和理解

---

## 💡 使用场景

### 场景 A: 日常开发测试

```bash
# 每次编辑后快速验证
./deploy.sh build
```

### 场景 B: 定期构建

```bash
# 每天晚上自动打包（可用 cron）
./deploy.sh all
```

### 场景 C: 持续集成（CI/CD）

```bash
# 在 CI/CD 流程中使用
./deploy.sh build --stats
if [ $? -eq 0 ]; then
    ./deploy.sh package
fi
```

### 场景 D: 生产部署

```bash
# 完整的编译、打包、上传流程
./deploy.sh deploy user@prod-server.com /var/www/mydocs
```

---

## 🔧 自定义配置

### 修改部署目录

编辑 `deploy.sh`，找到配置部分：

```bash
DEPLOY_DIR="${SCRIPT_DIR}/deploy"  # 修改这里
```

### 修改保留包数量

找到这行：

```bash
ls -t "${DEPLOY_DIR}"/vitepress-dist_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm
```

`tail -n +6` 表示保留最近 5 个包，改为：
- `+4` - 保留最近 3 个
- `+11` - 保留最近 10 个

### 自定义包名称

修改：

```bash
PACKAGE_NAME="vitepress-dist_${TIMESTAMP}.tar.gz"
```

例如：

```bash
PACKAGE_NAME="my-docs_${TIMESTAMP}.tar.gz"
```

---

## 📊 部署包结构

打包后的 tar.gz 包含：

```
vitepress-dist_20240101_120000.tar.gz
└── dist/
    ├── index.html
    ├── assets/
    │   ├── *.js
    │   ├── *.css
    │   └── images/
    ├── 01_初步了解/
    │   └── *.html
    └── ...（其他页面）
```

解压后可以直接部署到 Web 服务器。

---

## ⚠️ 常见问题

### Q1: 编译失败怎么办？

**A:** 检查：
1. Node.js 和 npm 是否已安装
2. 运行 `npm install` 安装依赖
3. docs 目录中是否有 Markdown 文件

### Q2: scp 上传失败

**A:** 检查：
1. 服务器地址和用户名是否正确
2. 是否有 SSH 权限
3. 远程目录是否存在且有写权限

```bash
# 先测试 SSH 连接
ssh user@server.com "ls -la /var/www/html"
```

### Q3: 包太大怎么办？

**A:** 可以：
1. 清理不必要的文件（docs 目录）
2. 在构建时排除某些文件
3. 考虑使用 gzip 压缩（脚本已使用）

### Q4: 如何在服务器上自动更新？

**A:** 创建一个 shell 脚本在服务器上运行：

```bash
#!/bin/bash
cd /var/www/html
# 下载最新包（可以从你的存储位置）
wget https://your-storage.com/vitepress-dist_latest.tar.gz
tar -xzf vitepress-dist_latest.tar.gz
mv dist/* .
rm -rf dist vitepress-dist_latest.tar.gz
```

然后用 cron 定期运行。

---

## 🎯 最佳实践

✅ **编译后总是检查统计**
```bash
./deploy.sh build --stats
```

✅ **打包前确认无错误**
```bash
# 先编译，看是否有错误
./deploy.sh build
# 然后再打包
./deploy.sh package
```

✅ **保留历史包用于回滚**
```bash
# 脚本会自动保留最近 5 个包
./deploy.sh all
# 旧包在 deploy/ 目录中
```

✅ **在上传前在本地测试**
```bash
npm run preview  # 预览最终效果
```

✅ **部署后验证**
```bash
# 在服务器上检查
curl http://example.com
# 或用浏览器打开
```

---

## 📝 相关命令速查

```bash
# 开发时
npm run dev          # 实时预览
npm run build:force  # 手动编译

# 部署时
./deploy.sh build    # 编译
./deploy.sh all      # 编译+打包
./deploy.sh deploy server.com /path  # 完整部署

# 清理
./deploy.sh clean    # 清理构建文件
```

---

**现在你可以一键编译和部署了！** 🚀

