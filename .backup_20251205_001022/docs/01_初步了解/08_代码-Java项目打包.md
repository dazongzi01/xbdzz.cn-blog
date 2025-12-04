# 📦 Java项目打包和部署指南

现在你的网站框架已经搭好了。接下来需要把你的 Java 项目打包成可以运行的 JAR 文件，然后上传到服务器。

这一步是真正让项目"活"起来的关键！

---

## 🎯 理解 JAR 文件是什么

JAR（Java Archive）文件就是一个"打包好的 Java 应用"。

**类比：**
- 你的源代码 = 建筑的"设计图"
- JAR 文件 = 建筑的"成品"

用户不需要源代码，只需要 JAR 文件，一条命令就能启动项目。

---

## 🎯 第一步：确认项目配置

在打包之前，检查你的项目配置。

### 检查 application.yml 或 application.properties

找到项目根目录下的配置文件：
- `src/main/resources/application.yml` 或
- `src/main/resources/application.properties`

**需要检查的配置：**

```yaml
spring:
  application:
    name: crmeb-admin

  datasource:
    url: jdbc:mysql://localhost:3306/crmeb_db?useSSL=false&serverTimezone=Asia/Shanghai
    username: crmeb
    password: 你的数据库密码
    driver-class-name: com.mysql.cj.jdbc.Driver

  jpa:
    hibernate:
      ddl-auto: update

  redis:
    host: localhost
    port: 6379
    password: 你的redis密码
    timeout: 1800000

server:
  port: 8000
  servlet:
    context-path: /
```

⚠️ **重点检查：**
- **MySQL 连接地址** - `localhost:3306` 是对的（本地）
- **MySQL 用户名和密码** - 必须和服务器上的一样
- **Redis 连接** - 同样需要密码
- **项目端口** - 通常是 8000

💡 **小贴士：** 如果本地和服务器的配置不同，考虑用环境变量或多个配置文件。

### 检查 pom.xml（Maven 项目）

找 `<packaging>` 标签，确保是 `jar`：

```xml
<packaging>jar</packaging>
```

如果是 `war`，改成 `jar`。

---

## 🎯 第二步：本地打包

最好在本地先打包一次，确保没有问题。

### 使用 IDE（推荐）

**如果用 IntelliJ IDEA：**

1. 右键项目名称
2. 选择"Open Module Settings"或"Project Structure"
3. 找到"Artifacts"
4. 点"+"添加新的 JAR 构建
5. 配置好后点"Build" → "Build Artifacts"
6. 看到"Build successful"就成功了
7. JAR 文件通常在 `target/` 目录

**如果用 Eclipse：**

1. 右键项目名称
2. 选择"Export..."
3. 选择"JAR file"
4. 配置输出位置
5. 点"Finish"

### 使用命令行（推荐）

打开项目根目录的命令行，运行：

```bash
mvn clean package
```

这会：
1. 清理之前的编译（`clean`）
2. 编译源代码
3. 运行测试
4. 打包成 JAR 文件（`package`）

⏳ **等待 1-5 分钟**（取决于你的项目大小和网络）

✅ 看到 `BUILD SUCCESS` 说明成功了！

JAR 文件会出现在 `target/` 目录，通常叫 `crmeb-admin-xxx.jar`

### 本地测试运行（可选）

在本地试试能否运行：

```bash
java -jar target/crmeb-admin-xxx.jar
```

如果看到项目启动日志，说明 JAR 包没有问题。

⚠️ **注意：** 本地运行需要 MySQL 和 Redis 也在运行

---

## 🎯 第三步：上传 JAR 文件到服务器

现在你有了 JAR 文件，需要上传到服务器。

### 方法1️⃣：用宝塔文件管理器（简单）

1. 登录宝塔
2. 左边菜单 → "文件"
3. 进入你的项目目录，比如 `/www/wwwroot/crmeb/`
4. 点"上传"
5. 选择你的 JAR 文件
6. 等待上传完成

### 方法2️⃣：用 SFTP 工具（推荐）

用 FileZilla 或 WinSCP：

1. 打开 SFTP 工具
2. 输入服务器 IP、用户名、密码
3. 连接到服务器
4. 导航到 `/www/wwwroot/crmeb/` 目录
5. 从本地拖拽 JAR 文件到服务器目录
6. 等待上传完成

### 方法3️⃣：用 Git（推荐）

如果项目在 Git 仓库：

```bash
cd /www/wwwroot/crmeb/
git clone 你的仓库地址 .
mvn clean package
```

直接在服务器编译，省去上传大文件的步骤。

💡 **小贴士：** 如果你的 JAR 文件很大（几百 MB），建议用 Git 方式在服务器编译。

---

## 🎯 第四步：启动 Java 项目

上传完成后，SSH 连接到服务器，启动项目。

### 简单启动（测试用）

```bash
cd /www/wwwroot/crmeb/
java -jar crmeb-admin-xxx.jar
```

你会看到项目启动日志显示（Spring Boot 标志和启动信息）。

**启动过程中会显示：**
1. Spring Boot 项目启动的 ASCII 艺术
2. 日志行：`Starting CrmebAdminApplication on server`
3. 数据库连接日志
4. 最终显示：`Started CrmebAdminApplication`

⏳ **等待项目完全启动**（通常 10-30 秒）

✅ 看到 `Started CrmebAdminApplication` 说明启动成功了！此时项目已经就绪。

⚠️ **注意：** 这样启动的问题是，关闭终端连接后项目会停止。

### 后台启动（推荐）

使用 `nohup` 让项目在后台运行：

```bash
nohup java -jar crmeb-admin-xxx.jar > app.log 2>&1 &
```

解释：
- `nohup` - 后台运行
- `> app.log` - 日志输出到 app.log 文件
- `2>&1` - 错误日志也输出到同一个文件
- `&` - 在后台运行

✅ 这样项目会一直运行，即使关闭终端也不会停止。

### 查看启动日志

```bash
tail -f /www/wwwroot/crmeb/app.log
```

查看项目是否成功启动。按 `Ctrl+C` 退出查看。

### 验证项目是否启动成功

```bash
ps aux | grep java
```

如果看到你的 java 进程，说明项目已启动。

或者在浏览器访问：

```
http://你的服务器IP:8000/
```

如果看到项目首页或 API 响应，说明成功了！

⚠️ **如果访问不了：**

1. 检查防火墙有没有开放 8000 端口
2. 查看 app.log 有没有错误信息
3. 确认 MySQL 和 Redis 连接正常

---

## 🎯 第五步：配置开机自启（可选）

万一服务器重启了，你的项目应该能自动启动。

### 方法1️⃣：用宝塔计划任务（简单）

1. 在宝塔左边菜单点"计划任务"
2. 点"添加任务"
3. 选择"Shell 脚本"
4. 填写启动命令：

```bash
cd /www/wwwroot/crmeb/ && nohup java -jar crmeb-admin-xxx.jar > app.log 2>&1 &
```

5. 选择"重启后执行"
6. 点"添加"

💡 **小贴士：** 这样服务器重启后，项目会自动启动。

### 方法2️⃣：用 Systemd（推荐）

创建一个 Systemd 服务文件：

```bash
sudo nano /etc/systemd/system/crmeb.service
```

填写内容：

```ini
[Unit]
Description=CRMEB Admin Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/www/wwwroot/crmeb/
ExecStart=/usr/bin/java -jar /www/wwwroot/crmeb/crmeb-admin-xxx.jar
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

保存后运行：

```bash
sudo systemctl daemon-reload
sudo systemctl enable crmeb
sudo systemctl start crmeb
```

验证是否启动：

```bash
sudo systemctl status crmeb
```

---

## ⚠️ 常见问题速查

### Q: 启动时报错"Address already in use"？

**A:** 说明 8000 端口已经被占用了。

解决：

1. **改端口**
   - 在 `application.yml` 改成其他端口，比如 8001
   - 重新打包

2. **杀死占用端口的进程**
   ```bash
   lsof -i :8000
   kill -9 进程ID
   ```

3. **查看是不是之前的项目还在运行**
   ```bash
   ps aux | grep java
   kill 旧进程的ID
   ```

### Q: 启动时报错"Connection refused"?

**A:** 说明连接数据库或 Redis 失败了。

检查：

1. **MySQL 在运行吗？**
   ```bash
   ps aux | grep mysql
   ```

2. **Redis 在运行吗？**
   ```bash
   ps aux | grep redis
   ```

3. **用户名和密码对不对？**
   - 在宝塔检查 MySQL 用户
   - 在宝塔检查 Redis 密码

4. **防火墙有没有拦住？**
   - 宝塔防火墙要放行 3306（MySQL）和 6379（Redis）

### Q: 启动很慢或一直卡在某个地方？

**A:** 可能是：

1. **网络不好** - 项目在下载依赖
2. **服务器配置低** - 内存或 CPU 不足
3. **数据库有问题** - 初始化数据库很慢

解决：

1. 等等，给项目充足的启动时间（可能需要 1-2 分钟）
2. 查看 app.log 看具体在做什么
3. 如果一直不动，Ctrl+C 停止，检查日志找错误

### Q: 数据库连接失败怎么办？

**A:** 常见原因和解决：

1. **密码错了**
   - 在宝塔 MySQL 管理里重置密码
   - 更新 application.yml 里的密码

2. **用户不存在**
   - 在宝塔创建 MySQL 用户 `crmeb`
   - 赋予数据库权限

3. **数据库不存在**
   - 在宝塔创建数据库 `crmeb_db`
   - 导入初始化脚本

```bash
mysql -u crmeb -p crmeb_db < init.sql
```

### Q: 项目启动了但访问不了？

**A:** 排查顺序：

1. **反向代理配置对不对？**
   - 宝塔网站设置中检查反向代理
   - 确保指向 `http://127.0.0.1:8000`

2. **防火墙有没有开放 80/443？**
   - 宝塔防火墙要开放 80 和 443

3. **Nginx 有没有启动？**
   - 在宝塔点 Nginx → "重启"

4. **API 路径对不对？**
   - 试试访问 `http://IP:8000/api/...`
   - 看是否能直接访问（不通过 Nginx）

---

## 📋 Java 项目部署检查清单

部署完成后，检查这些项目：

- [ ] 项目配置文件已正确修改（数据库、Redis）
- [ ] JAR 文件已成功打包
- [ ] JAR 文件已上传到服务器
- [ ] 项目已启动，日志无错误
- [ ] 能通过 `http://IP:8000` 访问
- [ ] 反向代理已配置，能通过域名访问
- [ ] 数据库初始化成功
- [ ] 开机自启已配置

---

## 🎉 你的 Java 项目已经上线了！

现在：

1. ✅ Java 后端已启动
2. ✅ 可以通过反向代理访问
3. ✅ 可以通过域名 HTTPS 访问

接下来需要：

1. 部署 PC 管理端（参考[管理端打包](/01_初步了解/09_代码-管理端打包)）
2. 部署 H5 商城（参考[H5打包](/01_初步了解/10_代码H5打包)）
3. 初始化数据
4. 配置业务相关的功能

祝你的项目顺利上线！🚀

