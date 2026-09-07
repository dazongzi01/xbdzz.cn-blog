---
title: "元转分，少写一个参数就少一分钱"
description: "接支付绕不开元和分的转换。微信收分，你的库里存元。"
date: 2026-09-04
tags:
  - 支付
---

# 元转分，少写一个参数就少一分钱

接支付绕不开元和分的转换。微信收分，你的库里存元。

看着简单，三个地方容易漏。

**一、别用 double。**

```java
// 常见写法，也是错的写法
int fen = (int)(yuan * 100);
```

「浮点不精确」这话听腻了，但很少有人知道到底有多不准。我扫了一遍
0.01 到 10000.00 之间全部一百万个两位小数金额，拿这个写法和
`BigDecimal` 的结果对：

```
扫描区间: 0.01 ~ 10000.00 元
算错的:   65624 个
出错率:   6.5624%
第一个:   0.29 元 → 应为 29 分，算出 28 分
累计少收: 65624 分
```

**每 15 个金额里就有 1 个会少收一分钱**，而且从 0.29 元就开始了——
不是什么边界大数，是日常价格。

扫描的代码就是上面那两行加个循环，你可以自己跑一遍。

金额只能用 `BigDecimal`。

**二、`setScale` 的舍入模式必须写出来。**

```java
public static int yuanToFen(BigDecimal y) {
    return y.multiply(HUNDRED)
            // 这个参数不能省
            .setScale(0, HALF_UP)
            .intValue();
}
```

不写舍入模式，遇到除不尽会直接抛 `ArithmeticException`。而且默认行为不是你想的那样——**明确写 `HALF_UP`，别赌**。

**三、分转元回来时，0 也要 `setScale(2)`。**

```java
static BigDecimal toYuan(Integer fen) {
    if (fen == null) {
        // 不是直接 return ZERO
        return ZERO.setScale(2, HALF_UP);
    }
    return new BigDecimal(fen)
            .divide(HUNDRED, 2, HALF_UP);
}
```

直接返回 `BigDecimal.ZERO`，序列化出去是 `0`；带了 `setScale(2)` 才是 `0.00`。

前端拿到 `0` 和 `0.00`，显示出来一个是「¥0」一个是「¥0.00」。**金额显示不一致，用户第一反应是你系统有问题。**

一个 `setScale(2)` 的事。

![签名-A](/blog/images/签名-A.png)
