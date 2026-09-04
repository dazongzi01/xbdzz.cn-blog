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
// 错：0.1 + 0.2 在浮点里不等于 0.3
int fen = (int)(yuan * 100);
```

金额只能用 `BigDecimal`。这条老生常谈，但真的还有人在犯。

**二、`setScale` 的舍入模式必须写出来。**

```java
public static int yuanToFen(BigDecimal yuan) {
    return yuan.multiply(new BigDecimal("100"))
               .setScale(0, RoundingMode.HALF_UP)   // 这个参数不能省
               .intValue();
}
```

不写舍入模式，遇到除不尽会直接抛 `ArithmeticException`。而且默认行为不是你想的那样——**明确写 `HALF_UP`，别赌**。

**三、分转元回来时，0 也要 `setScale(2)`。**

```java
public static BigDecimal fenToYuan(Integer fen) {
    if (fen == null) {
        return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);  // 不是直接 return ZERO
    }
    return new BigDecimal(fen).divide(new BigDecimal("100"), 2, RoundingMode.HALF_UP);
}
```

直接返回 `BigDecimal.ZERO`，序列化出去是 `0`；带了 `setScale(2)` 才是 `0.00`。

前端拿到 `0` 和 `0.00`，显示出来一个是「¥0」一个是「¥0.00」。**金额显示不一致，用户第一反应是你系统有问题。**

一个 `setScale(2)` 的事。

![签名-A](/blog/images/签名-A.png)
