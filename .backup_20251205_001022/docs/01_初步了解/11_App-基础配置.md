# 📱 App 基础配置指南

现在你的后端、PC管理端、H5商城都已经上线了。接下来是为移动应用（App）做基础配置。无论是iOS还是Android，都需要从这一步开始。

这一步很重要，配置好了，才能顺利进行开发和打包！

---

## 🎯 理解App应用是什么

在CRMEB系统中，App指的是原生应用：

| 应用类型 | 技术 | 特点 |
|---------|------|------|
| **H5商城** | Vue + UniApp | 网页版，用浏览器打开 |
| **小程序** | UniApp | 微信小程序，在微信中打开 |
| **App应用** | UniApp | 原生应用，安装到手机上 |

**App的优势：**
- 💪 更好的性能（比H5快）
- 📱 原生应用体验（可以上架应用市场）
- 🔔 推送通知功能
- 📲 可以离线使用部分功能
- ⭐ 用户粘性更高

---

## 🎯 第一步：准备开发环境

### 前置要求

确保你已经装好了：

| 软件 | 用途 | 检查方法 |
|------|------|--------|
| Node.js | 构建工具 | `node -v` |
| npm | 包管理 | `npm -v` |
| Git | 版本控制 | `git --version` |
| HBuilderX | UniApp开发工具 | 下载并安装 |

如果没装，参考[服务器运行环境](/01_初步了解/06_服务器运行环境)中的安装步骤。

### 下载 HBuilderX

HBuilderX 是做 UniApp 开发的官方工具：

1. **打开官网** 👉 [HBuilderX 官方下载](https://www.dcloud.io/hbuilderx.html)
2. **选择版本**
   - Windows/Mac 都有版本
   - 选择"标准版"就够用了
3. **安装**
   - 解压或运行安装程序
   - 按照提示完成安装

💡 **小贴士：** HBuilderX是免费的，不需要破解或付费

### 配置 HBuilderX

安装完成后需要做一些配置：

1. **打开 HBuilderX**
2. **配置 Node.js 路径**
   - 菜单：工具 → 选项（或 HBuilderX → Preferences）
   - 找到"运行配置"或"Node.js"
   - 设置 Node.js 路径（通常自动识别）
3. **安装插件**（可选）
   - 在"插件市场"搜索 UniApp 相关插件
   - 安装有用的语言支持和代码提示

---

## 🎯 第二步：获取项目源代码

### 找到App项目文件

App项目通常在项目根目录的 `uniapp/` 或 `mobile/` 目录下：

```
你的项目/
├── admin/           # PC管理端
├── mobile/          # H5商城 + App（UniApp项目）
│   ├── src/
│   ├── pages/
│   ├── App.vue
│   └── package.json
└── crmeb-admin/     # Java后端
```

### 打开项目

1. **用 HBuilderX 打开 mobile 项目**
   - HBuilderX → 文件 → 打开项目
   - 选择 `mobile` 文件夹
2. **等待项目加载完成**
   - HBuilderX 会自动扫描项目结构
   - 可能需要 1-2 分钟

✅ **项目打开成功的标志：**
- 左边能看到项目的文件树
- 没有红色的错误提示

---

## 🎯 第三步：修改App基础配置

### 打开 manifest.json

这个文件是 App 的配置文件，很关键：

1. **在项目根目录找到** `manifest.json` 文件
2. **用 HBuilderX 打开它**

### 配置应用信息

这个文件分为几个部分。我们需要关注的是：

**1️⃣ 应用名称和ID**

```json
{
  "name": "你的App名称",
  "appid": "生成一个唯一ID"
}
```

- **应用名称**：用户在手机上看到的名字，比如"我的商城"
- **AppID**：UniApp 自动分配的唯一标识

💡 **小贴士：** 第一次打开manifest.json时，HBuilderX会自动为你生成AppID

**2️⃣ Android配置**

```json
"android": {
  "package": "com.example.myapp",
  "targetSdkVersion": 31,
  "minSdkVersion": 21
}
```

- **package**：包名，格式：`com.公司.应用名`，必须全小写
- **targetSdkVersion**：目标Android版本（31或以上）
- **minSdkVersion**：最低Android版本（通常21以上）

⚠️ **重要：** 包名一旦设定就很难改，要仔细想想！

**3️⃣ iOS配置**（如果要发iOS版本）

```json
"ios": {
  "dSYMs": true
}
```

这个保持默认就行，后续打包时还会有更多配置。

**4️⃣ 应用图标和启动图**

```json
"icon": {
  "width": 192,
  "height": 192,
  "path": "static/icon.png"
}
```

你需要准备：
- **应用图标**：192x192 像素的PNG图片
- **启动屏**：1080x1920 像素的PNG图片

📂 **文件位置：** 放在项目的 `static/` 文件夹下

### 配置API地址

App 需要知道后端服务器在哪里：

1. **找到** `src/config/` 或 `src/api/` 目录
2. **找到类似的配置文件**（比如 `env.js` 或 `config.js`）
3. **修改 API 地址**

```javascript
// src/config/api.js 或类似文件
export const API_URL = 'http://yoursite.com'  // 改成你的服务器地址
// 或者
export const API_URL = 'http://123.45.67.89:8000'
```

⚠️ **重点：**
- 用你实际的服务器地址替换
- 如果是 HTTPS，改成 `https://`
- 确保后端服务已经启动

---

## 🎯 第四步：安装依赖包

App 项目需要各种npm包才能运行：

### 打开终端

在 HBuilderX 中打开项目的终端：

1. **菜单**：终端 → 新建终端（或其他类似选项）
2. **或者**：用命令行进入项目目录

```bash
cd 你的项目/mobile
```

### 安装依赖

```bash
npm install
```

⏳ **等待 2-5 分钟**

如果网络慢，换淘宝镜像：

```bash
npm config set registry https://registry.npmmirror.com
npm install
```

✅ **安装成功**：看到 `added xxx packages`

💡 **小贴士：** 如果报错，试试：
```bash
rm -rf node_modules
npm install
```

---

## 🎯 第五步：验证基础配置

### 检查项目结构

确保项目有这些关键文件/文件夹：

```
mobile/
├── src/
│   ├── pages/           # 页面文件
│   ├── components/      # 组件
│   ├── api/             # API调用
│   ├── config/          # 配置文件
│   ├── App.vue          # 主应用文件
│   └── main.js          # 入口文件
├── static/              # 静态资源（图片、图标等）
├── manifest.json        # App配置（刚刚修改的）
├── package.json         # npm配置
└── README.md            # 项目说明
```

### 检查没有错误

在 HBuilderX 中查看：

1. **菜单**：查看 → 编辑器 → 问题（或类似）
2. 看有没有红色的错误（橙色警告可以先忽略）

❌ **如果有错误：**
- 检查 node_modules 有没有装好
- 检查API配置有没有改
- 检查图标文件有没有放在 static/ 文件夹

---

## ⚠️ 常见问题

### Q: manifest.json 在哪里找？

**A:** 就在项目根目录。HBuilderX 会在左边文件树顶部显示它。

### Q: 包名应该填什么？

**A:** 格式：`com.公司名.应用名`，全部小写

比如：
- `com.mycompany.myshop`
- `com.crmeb.shop`
- `cn.xxx.mall`

⚠️ **一旦设定就很难改，确保拼写正确！**

### Q: 应用图标和启动屏必须现在准备吗？

**A:** 可以先用默认的，后续再换。但最好现在就准备好：

**应用图标：** 192x192 PNG
**启动屏：** 1080x1920 PNG

如果没有，可以：
- 用设计工具（Photoshop、Figma）做
- 找免费在线设计工具（Canva等）
- 用AI生成（现在很方便）

### Q: API地址填错了怎么办？

**A:** 没关系，随时可以改：

1. **打开配置文件**（src/config/api.js等）
2. **修改URL**
3. **保存文件**
4. 重新运行/打包时会生效

---

## 📋 App基础配置检查清单

配置完成后，检查这些项目：

- [ ] HBuilderX 已安装
- [ ] Node.js 和 npm 已正确配置
- [ ] App 项目已在 HBuilderX 中打开
- [ ] manifest.json 已修改（应用名称、包名、AppID）
- [ ] Android 配置已设置
- [ ] API 地址已修改为服务器地址
- [ ] npm 依赖已安装（node_modules 文件夹存在）
- [ ] 没有红色错误提示
- [ ] 应用图标和启动屏已放在 static/ 文件夹（可选）

---

## 🎉 基础配置完成！

现在你的 App 项目已经：

1. ✅ 打开了正确的开发工具
2. ✅ 安装了所需的依赖
3. ✅ 配置了应用基本信息
4. ✅ 连接到了后端服务器

接下来的步骤：

1. [App开发调试](/01_初步了解/12_App-开发调试) - 在模拟器中测试App
2. [App打包配置](/01_初步了解/13_App-打包配置) - 为打包做准备
3. [App打包上线](/01_初步了解/14_App-打包上线) - 打包并发布到应用市场

💡 **小贴士：** 基础配置很重要，确保都按照步骤做好。后续的开发和打包都依赖这一步的配置！

祝你的 App 开发顺利！🚀

