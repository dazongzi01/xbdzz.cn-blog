# wxJava 框架配置指南

> 本文档详细介绍 CRMEB-Java 多商户 V1.9+ 版本中 wxJava 框架的配置方法和迁移说明

---

## 📋 目录

- [版本说明](#版本说明)
- [配置变更概述](#配置变更概述)
- [wxJava 配置详解](#wxjava-配置详解)
- [迁移指南](#迁移指南)
- [配置示例](#配置示例)
- [常见问题](#常见问题)
- [最佳实践](#最佳实践)

---

## 💡 版本说明

### 什么是 wxJava？

**wxJava** 是微信开发 Java SDK，支持：
- 微信小程序
- 微信公众号
- 微信开放平台
- 微信企业号/企业微信
- 微信支付

### 版本变更

| 版本 | 配置方式 | 说明 |
|------|----------|------|
| **V1.9 之前** | 后台UI配置 | 在管理后台页面填写微信配置参数 |
| **V1.9+** | YAML配置文件 | 所有微信相关配置统一在 application.yml 中 |

**⚠️ 重要变更：**

从 V1.9 版本开始，CRMEB-Java 将微信相关的所有内容切换为使用 **wxJava 框架**实现，配置方式从后台页面配置改为 YAML 文件配置。

---

## 🔄 配置变更概述

### 后台UI变更

**说白了，就是原来在后台页面配置的地方，现在都被移除了，改到代码配置文件里配置。**

### 小程序配置变更

**旧版本（V1.9 之前）：**
```
平台端设置 → 平台设置 → 应用配置 → 小程序配置
（这里原来有AppID、Secret等参数）

平台端设置 → 平台设置 → 支付/充值 → 小程序支付配置
（这里原来有支付相关配置）
```

**新版本（V1.9+）：**
```
UI界面：参数已全部删除
配置位置：application.yml 文件中的 wx.miniapp 和 wx.pay.ma 节点
```

### 公众号配置变更

**旧版本（V1.9 之前）：**
```
平台端设置 → 平台设置 → 应用配置 → 公众号配置
（这里原来有AppID、Secret等参数）

平台端设置 → 平台设置 → 支付/充值 → 公众号支付配置
（这里原来有支付相关配置）
```

**新版本（V1.9+）：**
```
UI界面：参数已全部删除
配置位置：application.yml 文件中的 wx.mp 和 wx.pay.mp 节点
```

### 微信 APP 配置变更

**旧版本（V1.9 之前）：**
```
平台端设置 → 平台设置 → 应用配置 → 微信APP配置
（这里原来有AppID等参数）

平台端设置 → 平台设置 → 支付/充值 → 微信APP支付
（这里原来有支付相关配置）
```

**新版本（V1.9+）：**
```
UI界面：表单已全部删除
配置位置：application.yml 文件中的 wx.pay.app 节点
```

### 变更对比表

| 模块 | 旧配置位置 | 新配置位置 | 状态 |
|------|-----------|-----------|------|
| **小程序基础配置** | 后台UI | wx.miniapp | ✅ 已迁移 |
| **小程序支付配置** | 后台UI | wx.pay.ma | ✅ 已迁移 |
| **公众号基础配置** | 后台UI | wx.mp | ✅ 已迁移 |
| **公众号支付配置** | 后台UI | wx.pay.mp | ✅ 已迁移 |
| **APP支付配置** | 后台UI | wx.pay.app | ✅ 已迁移 |
| **开放平台配置** | 无 | wx.open | 🆕 新增 |

---

## ⚙️ wxJava 配置详解

### 配置文件位置

**文件路径：**
```
/src/main/resources/application.yml
```

或根据环境使用：
```
application-dev.yml   # 开发环境
application-test.yml  # 测试环境
application-prod.yml  # 生产环境
```

### 完整配置结构

```yaml
wx:
  miniapp:    # 小程序配置
  mp:         # 公众号配置
  open:       # 开放平台配置
  pay:        # 支付配置
    mp:       # 公众号支付
    ma:       # 小程序支付
    app:      # APP支付
```

---

## 📱 小程序配置（miniapp）

### 基础配置

```yaml
wx:
  miniapp:
    useRedis: true              # 是否使用 Redis 存储 token
    redisConfig:
      host: 127.0.0.1           # Redis 地址
      port: 6379                # Redis 端口
      password:                 # Redis 密码（无密码留空）
      timeout: 30000            # 连接超时时间（毫秒）
      database: 13              # Redis 数据库编号
    configs:
      - appid: wxabcd1234567890         # 小程序 AppID
        secret: abc123def456ghi789      # 小程序 AppSecret
        token: myToken123               # 消息服务器配置的 Token
        aesKey: abcdefghijk12345678901234567890ABCD  # EncodingAESKey
        msgDataFormat: JSON             # 消息数据格式
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **useRedis** | Boolean | 是 | 是否使用 Redis 存储 access_token |
| **redisConfig.host** | String | 是（useRedis=true时） | Redis 服务器地址 |
| **redisConfig.port** | Integer | 是 | Redis 端口，默认 6379 |
| **redisConfig.password** | String | 否 | Redis 密码，无密码可留空 |
| **redisConfig.timeout** | Integer | 否 | 连接超时，默认 30000ms |
| **redisConfig.database** | Integer | 否 | 数据库编号，默认 13 |
| **appid** | String | 是 | 微信小程序的 AppID |
| **secret** | String | 是 | 微信小程序的 AppSecret |
| **token** | String | 否 | 消息服务器配置的 Token（如需接收回调） |
| **aesKey** | String | 否 | 消息加密密钥（如启用消息加密） |
| **msgDataFormat** | String | 否 | 消息格式：JSON 或 XML，默认 JSON |

### 如何获取配置参数？

**AppID 和 AppSecret：**
```
1. 登录微信公众平台：https://mp.weixin.qq.com
2. 开发 → 开发管理 → 开发设置
3. 查看"开发者ID"
   - AppID（小程序ID）
   - AppSecret（小程序密钥，需要管理员扫码重置后查看）
```

**Token 和 EncodingAESKey：**
```
1. 开发 → 开发管理 → 开发设置 → 消息推送
2. 点击"启用"或"修改配置"
3. 自定义或随机生成 Token 和 EncodingAESKey
```

---

## 📢 公众号配置（mp）

### 基础配置

```yaml
wx:
  mp:
    useRedis: true              # 是否使用 Redis 存储 token
    redisConfig:
      host: 127.0.0.1           # Redis 地址
      port: 6379                # Redis 端口
      password:                 # Redis 密码
      timeout: 30000            # 连接超时时间（毫秒）
      database: 13              # Redis 数据库编号
    configs:
      - appid: wxABCD1234567890         # 公众号 AppID
        secret: abc123def456ghi789      # 公众号 AppSecret
        token: myMpToken123             # 消息服务器配置的 Token
        aesKey: abcdefghijk12345678901234567890ABCD  # EncodingAESKey
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **useRedis** | Boolean | 是 | 是否使用 Redis 存储 access_token |
| **redisConfig** | Object | 是（useRedis=true时） | Redis 配置，同小程序配置 |
| **appid** | String | 是 | 微信公众号的 AppID |
| **secret** | String | 是 | 微信公众号的 AppSecret |
| **token** | String | 否 | 消息服务器配置的 Token |
| **aesKey** | String | 否 | 消息加密密钥 |

### 如何获取配置参数？

**AppID 和 AppSecret：**
```
1. 登录微信公众平台：https://mp.weixin.qq.com
2. 开发 → 基本配置
3. 查看"公众号开发信息"
   - AppID（公众号开发者ID）
   - AppSecret（公众号开发者密码，需要管理员扫码查看）
```

---

## 🌐 开放平台配置（open）

### 应用场景

**开放平台配置主要用于：**
- PC 网站扫码登录
- 移动应用（APP）接入
- 第三方平台开发

**通俗讲：** 如果你的商城有 PC 端，用户需要通过微信扫码登录，就需要配置这个。

### 基础配置

```yaml
wx:
  open:
    useRedis: true                          # 是否使用 Redis
    componentAppId: wxopenXXXXXXXXXXXX      # 开放平台 AppID
    componentSecret: abc123def456ghi789     # 开放平台 AppSecret
    componentToken: myOpenToken123          # 消息服务器 Token
    componentAesKey: abcdefghijk12345678901234567890ABCD  # EncodingAESKey
    redisConfig:
      host: 127.0.0.1
      port: 6379
      password:
      timeout: 30000
      database: 13
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **useRedis** | Boolean | 是 | 是否使用 Redis 存储 |
| **componentAppId** | String | 是 | 微信开放平台的 AppID |
| **componentSecret** | String | 是 | 微信开放平台的 AppSecret |
| **componentToken** | String | 否 | 消息服务器配置的 Token |
| **componentAesKey** | String | 否 | 消息加密密钥 |
| **redisConfig** | Object | 是（useRedis=true时） | Redis 配置 |

### 如何获取配置参数？

**创建网站应用：**
```
1. 登录微信开放平台：https://open.weixin.qq.com
2. 管理中心 → 网站应用 → 创建网站应用
3. 填写应用信息，等待审核通过
4. 审核通过后，进入应用详情
5. 查看 AppID 和 AppSecret
```

---

## 💰 支付配置（pay）

### 配置结构

支付配置分为三个部分：

```yaml
wx:
  pay:
    mp:   # 公众号支付（JSAPI支付）
    ma:   # 小程序支付
    app:  # APP支付
```

### 公众号支付配置（pay.mp）

```yaml
wx:
  pay:
    mp:
      appId: wxABCD1234567890                    # 公众号 AppID
      mchId: 1234567890                          # 微信支付商户号
      mchKey: ABCDEFGHIJK1234567890ABCDEFGH      # 商户密钥（API密钥）
      keyPath: classpath:certs/apiclient_cert.p12  # p12证书路径
      # V3 版本支付配置（推荐）
      apiV3Key: ABCDEFGHIJK1234567890ABCDEFGH    # API v3 密钥
      certSerialNo: 1A2B3C4D5E6F7890             # 证书序列号
      privateCertPath: classpath:certs/apiclient_cert.pem    # 私钥证书路径
      privateKeyPath: classpath:certs/apiclient_key.pem      # 私钥文件路径
      publicKeyPath: classpath:certs/pub_key.pem             # 公钥文件路径
      publicKeyId: WXPAYID1234567890             # 微信支付公钥ID
```

### 小程序支付配置（pay.ma）

```yaml
wx:
  pay:
    ma:
      appId: wxabcd1234567890                    # 小程序 AppID
      mchId: 1234567890                          # 微信支付商户号
      mchKey: ABCDEFGHIJK1234567890ABCDEFGH      # 商户密钥（API密钥）
      keyPath: classpath:certs/apiclient_cert.p12  # p12证书路径
      # V3 版本支付配置（推荐）
      apiV3Key: ABCDEFGHIJK1234567890ABCDEFGH    # API v3 密钥
      certSerialNo: 1A2B3C4D5E6F7890             # 证书序列号
      privateCertPath: classpath:certs/apiclient_cert.pem
      privateKeyPath: classpath:certs/apiclient_key.pem
      publicKeyPath: classpath:certs/pub_key.pem
      publicKeyId: WXPAYID1234567890
```

### APP 支付配置（pay.app）

```yaml
wx:
  pay:
    app:
      appId: wxAPP1234567890                     # APP AppID
      mchId: 1234567890                          # 微信支付商户号
      mchKey: ABCDEFGHIJK1234567890ABCDEFGH      # 商户密钥
      keyPath: classpath:certs/apiclient_cert.p12
      # V3 版本配置
      apiV3Key: ABCDEFGHIJK1234567890ABCDEFGH
      certSerialNo: 1A2B3C4D5E6F7890
      privateCertPath: classpath:certs/apiclient_cert.pem
      privateKeyPath: classpath:certs/apiclient_key.pem
      publicKeyPath: classpath:certs/pub_key.pem
      publicKeyId: WXPAYID1234567890
```

### 支付配置参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **appId** | String | 是 | 应用的 AppID（公众号/小程序/APP） |
| **mchId** | String | 是 | 微信支付商户号 |
| **mchKey** | String | 是 | 商户密钥（API密钥）32位 |
| **keyPath** | String | V2必填 | p12证书文件路径 |
| **apiV3Key** | String | V3必填 | API v3 密钥（32位） |
| **certSerialNo** | String | V3必填 | 商户证书序列号 |
| **privateCertPath** | String | V3必填 | apiclient_cert.pem 证书路径 |
| **privateKeyPath** | String | V3必填 | apiclient_key.pem 私钥路径 |
| **publicKeyPath** | String | V3可选 | 微信支付公钥 pub_key.pem 路径 |
| **publicKeyId** | String | V3可选 | 微信支付公钥ID |

### 证书文件说明

**V2 版本证书：**
- `apiclient_cert.p12` - 商户证书（用于退款、企业付款等）

**V3 版本证书：**
- `apiclient_cert.pem` - 商户证书（PEM格式）
- `apiclient_key.pem` - 商户私钥
- `pub_key.pem` - 微信支付公钥（可选）

**证书存放位置：**
```
/src/main/resources/certs/
├── apiclient_cert.p12
├── apiclient_cert.pem
├── apiclient_key.pem
└── pub_key.pem
```

**路径配置方式：**
```yaml
# 绝对路径
keyPath: /Users/myapp/certs/apiclient_cert.p12

# 类路径（推荐）
keyPath: classpath:certs/apiclient_cert.p12
```

### 如何获取支付配置参数？

**商户号和商户密钥：**
```
1. 登录微信支付商户平台：https://pay.weixin.qq.com
2. 账户中心 → API安全 → 设置API密钥
3. 查看商户号：账户中心 → 商户信息
```

**下载证书：**
```
1. 微信支付商户平台
2. 账户中心 → API安全 → 申请API证书
3. 下载证书文件（apiclient_cert.p12）
4. V3证书：申请API证书v3版本
```

**API v3 密钥：**
```
1. 微信支付商户平台
2. 账户中心 → API安全 → 设置APIv3密钥
3. 设置32位密钥（自定义）
```

**证书序列号：**
```
# 使用 OpenSSL 查看
openssl x509 -in apiclient_cert.pem -noout -serial

# 输出示例
serial=1A2B3C4D5E6F7890
```

---

## 📝 配置示例

### 最小化配置（仅小程序）

```yaml
wx:
  miniapp:
    useRedis: true
    redisConfig:
      host: 127.0.0.1
      port: 6379
      password:
      timeout: 30000
      database: 13
    configs:
      - appid: wxabcd1234567890
        secret: abc123def456ghi789
        token: myToken
        aesKey: myAesKey1234567890123456789012
        msgDataFormat: JSON

  pay:
    ma:
      appId: wxabcd1234567890
      mchId: 1234567890
      mchKey: ABCDEFGHIJK1234567890ABCDEFGH
      apiV3Key: ABCDEFGHIJK1234567890ABCDEFGH
      certSerialNo: 1A2B3C4D5E6F7890
      privateCertPath: classpath:certs/apiclient_cert.pem
      privateKeyPath: classpath:certs/apiclient_key.pem
```

### 完整配置（所有功能）

```yaml
wx:
  # 小程序配置
  miniapp:
    useRedis: true
    redisConfig:
      host: 127.0.0.1
      port: 6379
      password: redis123
      timeout: 30000
      database: 13
    configs:
      - appid: wxabcd1234567890
        secret: abc123def456ghi789
        token: miniappToken123
        aesKey: myAesKey1234567890123456789012
        msgDataFormat: JSON

  # 公众号配置
  mp:
    useRedis: true
    redisConfig:
      host: 127.0.0.1
      port: 6379
      password: redis123
      timeout: 30000
      database: 13
    configs:
      - appid: wxABCD1234567890
        secret: xyz789uvw456rst123
        token: mpToken123
        aesKey: mpAesKey1234567890123456789012

  # 开放平台配置（PC扫码登录）
  open:
    useRedis: true
    componentAppId: wxopenXXXXXXXXXXXX
    componentSecret: open123secret456
    componentToken: openToken123
    componentAesKey: openAesKey1234567890123456789
    redisConfig:
      host: 127.0.0.1
      port: 6379
      password: redis123
      timeout: 30000
      database: 13

  # 支付配置
  pay:
    # 公众号支付
    mp:
      appId: wxABCD1234567890
      mchId: 1234567890
      mchKey: MPKEY1234567890ABCDEFGHIJK123
      apiV3Key: MPV3KEY1234567890ABCDEFGHIJK
      certSerialNo: 1A2B3C4D5E6F7890AABBCCDD
      privateCertPath: classpath:certs/mp/apiclient_cert.pem
      privateKeyPath: classpath:certs/mp/apiclient_key.pem
      publicKeyPath: classpath:certs/mp/pub_key.pem
      publicKeyId: WXPAYID1234567890

    # 小程序支付
    ma:
      appId: wxabcd1234567890
      mchId: 1234567890
      mchKey: MAKEY1234567890ABCDEFGHIJK123
      apiV3Key: MAV3KEY1234567890ABCDEFGHIJK
      certSerialNo: 1A2B3C4D5E6F7890AABBCCDD
      privateCertPath: classpath:certs/ma/apiclient_cert.pem
      privateKeyPath: classpath:certs/ma/apiclient_key.pem
      publicKeyPath: classpath:certs/ma/pub_key.pem
      publicKeyId: WXPAYID1234567890

    # APP 支付
    app:
      appId: wxAPP1234567890
      mchId: 1234567890
      mchKey: APPKEY1234567890ABCDEFGHIJK12
      apiV3Key: APPV3KEY1234567890ABCDEFGHIJ
      certSerialNo: 1A2B3C4D5E6F7890AABBCCDD
      privateCertPath: classpath:certs/app/apiclient_cert.pem
      privateKeyPath: classpath:certs/app/apiclient_key.pem
      publicKeyPath: classpath:certs/app/pub_key.pem
      publicKeyId: WXPAYID1234567890
```

---

## 🔄 迁移指南

### 从旧版本迁移步骤

**步骤 1：备份现有配置**

```
1. 登录 CRMEB 管理后台
2. 平台设置 → 应用配置
3. 截图或记录所有微信相关配置参数：
   - 小程序 AppID、Secret
   - 公众号 AppID、Secret
   - 支付商户号、商户密钥等
```

**步骤 2：下载证书文件**

```
1. 微信支付商户平台下载证书
2. 保存到项目 /src/main/resources/certs/ 目录
```

**步骤 3：修改 application.yml**

```
1. 打开 application.yml 文件
2. 按照上述配置示例填写 wx 节点配置
3. 确保所有参数正确填写
```

**步骤 4：启动项目测试**

```
1. 启动 CRMEB-Java 项目
2. 查看启动日志，确认无配置错误
3. 测试小程序/公众号功能
4. 测试支付功能
```

### 配置检查清单

```
[ ] 小程序 AppID 和 Secret 已填写
[ ] 公众号 AppID 和 Secret 已填写
[ ] Redis 连接配置正确
[ ] 商户号已正确填写
[ ] 商户密钥（mchKey）已填写
[ ] API v3 密钥已填写
[ ] 证书文件已上传到正确位置
[ ] 证书路径配置正确
[ ] 证书序列号已填写
[ ] 已重启项目并查看日志
```

---

## ❓ 常见问题

### 1. 配置后启动报错"Redis连接失败"

**错误信息：**
```
Unable to connect to Redis; nested exception is io.lettuce.core.RedisConnectionException
```

**原因：**
- Redis 服务未启动
- Redis 地址或端口配置错误
- Redis 密码错误
- 防火墙阻止连接

**解决方法：**
```bash
# 检查 Redis 是否运行
redis-cli ping
# 应返回 PONG

# 检查配置
wx:
  miniapp:
    redisConfig:
      host: 127.0.0.1  # 确认地址正确
      port: 6379       # 确认端口正确
      password:        # 确认密码正确（无密码留空）
```

### 2. 支付时报错"商户密钥配置错误"

**可能原因：**
- mchKey 填写错误
- mchKey 包含多余空格
- 使用了旧的商户密钥

**解决方法：**
```
1. 登录微信支付商户平台
2. 账户中心 → API安全 → API密钥
3. 重新设置密钥（32位）
4. 更新 application.yml 中的 mchKey
5. 确保无多余空格或换行
```

### 3. V3 支付报错"证书序列号错误"

**错误信息：**
```
The certificate serial number is invalid
```

**解决方法：**

**查看证书序列号：**
```bash
# 使用 OpenSSL
openssl x509 -in apiclient_cert.pem -noout -serial

# 输出类似
serial=1A2B3C4D5E6F7890AABBCCDD

# 复制序列号，去掉 "serial="
certSerialNo: 1A2B3C4D5E6F7890AABBCCDD
```

### 4. 证书文件找不到

**错误信息：**
```
FileNotFoundException: class path resource [certs/apiclient_cert.pem] cannot be opened
```

**原因：**
- 证书文件未上传
- 文件路径配置错误
- 文件名大小写错误

**解决方法：**
```
1. 确认证书文件存在于项目中
   位置：/src/main/resources/certs/

2. 检查配置路径
   privateCertPath: classpath:certs/apiclient_cert.pem

3. 注意文件名大小写（Linux区分大小写）

4. 打包后检查 jar 包中是否包含证书
   jar -tf your-app.jar | grep certs
```

### 5. 小程序登录失败

**可能原因：**
- AppID 或 AppSecret 错误
- Redis 存储 access_token 失败
- 网络问题无法访问微信接口

**排查步骤：**
```
1. 检查配置
   wx:
     miniapp:
       configs:
         - appid: wxabcd1234567890  # 确认正确
           secret: abc123...         # 确认正确

2. 检查日志
   查看是否有微信接口调用错误

3. 测试 Redis 连接
   确认能正常读写 Redis

4. 检查服务器网络
   curl https://api.weixin.qq.com
```

### 6. 公众号回调失败

**问题：**
用户关注公众号后，系统没有收到回调通知

**原因：**
- Token 或 AesKey 配置错误
- 回调地址配置错误
- 服务器无法被外网访问

**解决方法：**
```
1. 确认配置正确
   wx:
     mp:
       configs:
         - token: myToken123      # 与公众平台设置一致
           aesKey: myAesKey...    # 与公众平台设置一致

2. 配置回调地址
   微信公众平台 → 基本配置 → 服务器配置
   URL: https://yourdomain.com/wechat/portal
   Token: 与 application.yml 中的 token 一致
   EncodingAESKey: 与 aesKey 一致

3. 确保服务器可外网访问
   使用外网环境测试 curl https://yourdomain.com/wechat/portal
```

### 7. 多个小程序/公众号配置

**问题：**
如何配置多个小程序或多个公众号？

**答案：**

wxJava 支持多账号配置：

```yaml
wx:
  miniapp:
    useRedis: true
    redisConfig:
      host: 127.0.0.1
      port: 6379
      database: 13
    configs:
      - appid: wxminiapp1          # 小程序1
        secret: secret1
        token: token1
        aesKey: aesKey1
      - appid: wxminiapp2          # 小程序2
        secret: secret2
        token: token2
        aesKey: aesKey2

  mp:
    useRedis: true
    redisConfig:
      host: 127.0.0.1
      port: 6379
      database: 13
    configs:
      - appid: wxmp1               # 公众号1
        secret: secret1
      - appid: wxmp2               # 公众号2
        secret: secret2
```

**注意：** CRMEB 商户版目前默认支持单个应用配置，多账号需要代码适配。

---

## 🎯 最佳实践

### 1. 配置安全

**敏感信息保护：**
```yaml
# ❌ 错误：直接写在配置文件
wx:
  miniapp:
    configs:
      - appid: wxabcd1234567890
        secret: mysecret123  # 不安全

# ✅ 推荐：使用环境变量
wx:
  miniapp:
    configs:
      - appid: ${WX_MINIAPP_APPID}
        secret: ${WX_MINIAPP_SECRET}
```

**环境变量配置：**
```bash
# Linux/Mac
export WX_MINIAPP_APPID=wxabcd1234567890
export WX_MINIAPP_SECRET=abc123def456

# Windows
set WX_MINIAPP_APPID=wxabcd1234567890
set WX_MINIAPP_SECRET=abc123def456
```

**或使用配置中心：**
- Nacos
- Apollo
- Spring Cloud Config

### 2. Redis 优化

**为什么要用 Redis？**
- 存储 access_token（2小时有效期）
- 避免频繁调用微信接口获取 token
- 分布式部署时共享 token

**Redis 配置建议：**
```yaml
wx:
  miniapp:
    useRedis: true
    redisConfig:
      host: 127.0.0.1
      port: 6379
      password: strongPassword123
      timeout: 10000        # 超时时间不要太长
      database: 13          # 使用独立数据库
      # 连接池配置（可选）
      maxActive: 8
      maxIdle: 8
      minIdle: 0
```

### 3. 证书管理

**证书存放：**
```
/src/main/resources/certs/
├── mp/                # 公众号证书
│   ├── apiclient_cert.pem
│   └── apiclient_key.pem
├── ma/                # 小程序证书
│   ├── apiclient_cert.pem
│   └── apiclient_key.pem
└── app/               # APP证书
    ├── apiclient_cert.pem
    └── apiclient_key.pem
```

**证书权限：**
```bash
# 设置证书文件只读
chmod 400 certs/*/apiclient_*.pem
```

**证书更新：**
- 微信支付证书有效期 5 年
- 到期前 1 个月更新证书
- 更新后重启服务

### 4. 日志配置

**启用 wxJava 日志：**
```yaml
logging:
  level:
    com.github.binarywang.wxpay: DEBUG
    me.chanjar.weixin: DEBUG
```

**生产环境调整为 INFO：**
```yaml
logging:
  level:
    com.github.binarywang.wxpay: INFO
    me.chanjar.weixin: INFO
```

### 5. 环境隔离

**开发环境：**
```yaml
# application-dev.yml
wx:
  miniapp:
    configs:
      - appid: wx_dev_appid
        secret: dev_secret
  pay:
    ma:
      mchId: dev_mch_id
      # 使用沙箱环境
      useSandbox: true
```

**生产环境：**
```yaml
# application-prod.yml
wx:
  miniapp:
    configs:
      - appid: wx_prod_appid
        secret: prod_secret
  pay:
    ma:
      mchId: prod_mch_id
      useSandbox: false
```

### 6. 容错处理

**接口调用重试：**
```yaml
wx:
  miniapp:
    # 开启请求重试
    retrySleepMillis: 1000  # 重试间隔
    maxRetryTimes: 3         # 最大重试次数
```

**超时配置：**
```yaml
wx:
  miniapp:
    httpClientType: HTTPCLIENT  # 使用 HttpClient
    httpProxyHost:              # 代理配置（如需要）
    httpProxyPort:
    httpProxyUsername:
    httpProxyPassword:
```

---

## 📊 总结

### 配置流程回顾

```
1️⃣ 从后台UI备份旧配置参数
2️⃣ 下载微信支付证书文件
3️⃣ 上传证书到 /src/main/resources/certs/
4️⃣ 修改 application.yml 添加 wx 配置
5️⃣ 配置 Redis 连接信息
6️⃣ 启动项目查看日志
7️⃣ 测试小程序/公众号功能
8️⃣ 测试支付功能
```

### 关键配置对照表

| 功能 | 配置节点 | 必填参数 |
|------|---------|---------|
| **小程序基础** | wx.miniapp | appid, secret |
| **小程序支付** | wx.pay.ma | appId, mchId, mchKey/apiV3Key |
| **公众号基础** | wx.mp | appid, secret |
| **公众号支付** | wx.pay.mp | appId, mchId, mchKey/apiV3Key |
| **开放平台** | wx.open | componentAppId, componentSecret |
| **APP 支付** | wx.pay.app | appId, mchId, mchKey/apiV3Key |

### 注意事项总结

**🔴 必须做到：**
- ✅ 妥善保管 AppSecret 和商户密钥
- ✅ 使用环境变量保护敏感配置
- ✅ 启用 Redis 存储 access_token
- ✅ 正确配置证书文件路径
- ✅ 区分开发和生产环境配置

**⚠️ 常见错误：**
- ❌ AppID 和 AppSecret 填写错误
- ❌ 商户密钥包含空格或换行
- ❌ 证书文件路径配置错误
- ❌ Redis 连接配置错误
- ❌ V2 和 V3 配置混用

---

## 🔗 相关文档

- [微信公众号支付配置](./03_微信公众号支付配置指南.md)
- [微信小程序配置指南](./04_微信小程序配置指南.md)
- [微信小程序支付配置](./05_微信小程序支付配置.md)

---

## 📚 参考资源

**官方文档：**
- [wxJava 官方文档](https://github.com/Wechat-Group/WxJava)
- [微信公众平台](https://mp.weixin.qq.com)
- [微信开放平台](https://open.weixin.qq.com)
- [微信支付商户平台](https://pay.weixin.qq.com)

**工具推荐：**
- [wxJava Demo](https://github.com/Wechat-Group/WxJava/tree/develop/weixin-java-mp-demo)
- [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

---
