---
title: "Redis 里刚 Pop，进程挂了钱已经收了"
description: "小程序已经是「支付成功」。积分页还是 0，券没到账，分账没触发。"
date: 2026-09-24
tags:
  - Redis
---

# Redis 里刚 Pop，进程挂了钱已经收了

小程序已经是「支付成功」。积分页还是 0，券没到账，分账没触发。

钱在回调里收完了。后面那一串被推进 Redis List，下一个任务 `rightPop`。
弹出来了，进程没了。

```java
redis.lPush("task:paid", orderNo);
String id = redis.rightPop("task:paid");
```

**`rightPop` 是取出并删除。** 没有 ACK。

这套代码里，处理函数抛异常会再 `lPush` 回去。单测 mock 一个 throw，
能看见消息回队，于是绿灯。

进程在 Pop 和 handle 之间被杀掉，catch 进不去，回队也不会发生。
日志可能还没写上。前端继续展示已支付——那是回调改的订单状态，
跟这条 List 不是同一个字段。

想补的话，用 `rightPopAndLeftPush`：

```java
// 弹出的同时放进「处理中」
String id = redis.rightPopAndLeftPush(
        "task:pending",
        "task:doing");
handle(id);
redis.lRemove("task:doing", 1, id);
```

崩溃时消息还在 `task:doing` 里，重启能捞。
还要写超时扫描、幂等、积压监控。

**写到第三个的时候，问自己：是不是在造一个残缺的 MQ。**

我的判断线：**丢了能靠对账补回来 → Redis List 够了；
丢了就是钱少了 → 落库扫表，或者老实上 MQ。**

测这条，不要只测 throw。把进程杀掉。

![签名-A](/blog/images/签名-A.png)
