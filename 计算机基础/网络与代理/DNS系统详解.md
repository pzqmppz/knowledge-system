---
title: "DNS系统详解"
category: "计算机基础/网络与代理"
tags: ["DNS", "DNS泄露", "DoH", "DNS污染", "Clash DNS"]
date: 2026-03-02
---

# DNS系统详解

> DNS 是代理问题中最容易被忽视，却又最关键的环节

## 一、DNS 是什么

DNS（Domain Name System）是把**域名翻译成 IP 地址**的系统。

```
你输入：www.baidu.com
    ↓
DNS 查询
    ↓
返回：110.242.68.3（百度的 IP）
    ↓
浏览器连接 110.242.68.3
```

## 二、DNS 解析的完整链路

```
┌────────────────────────────────────────────────────────────────┐
│                        DNS 解析链路                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. 浏览器缓存                                                  │
│     │ (chrome://net-internals/#dns)                           │
│     ↓ 没有缓存                                                 │
│                                                                │
│  2. 系统缓存                                                    │
│     │ (Windows: ipconfig /displaydns)                         │
│     ↓ 没有缓存                                                 │
│                                                                │
│  3. hosts 文件                                                  │
│     │ (C:\Windows\System32\drivers\etc\hosts)                 │
│     ↓ 没有记录                                                 │
│                                                                │
│  4. 本地 DNS 服务器（通常是路由器或 ISP 分配的）                   │
│     │                                                          │
│     ↓ 没有缓存或缓存过期                                        │
│                                                                │
│  5. 递归查询（本地 DNS 服务器帮你查）                            │
│     │                                                          │
│     ├─→ 根域名服务器（.）                                       │
│     │       │                                                  │
│     │       ↓ 告诉我 .com 的服务器                              │
│     │                                                          │
│     ├─→ 顶级域名服务器（.com）                                   │
│     │       │                                                  │
│     │       ↓ 告诉我 baidu.com 的服务器                         │
│     │                                                          │
│     └─→ 权威域名服务器（baidu.com）                              │
│             │                                                  │
│             ↓ 返回 www.baidu.com 的 IP                         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## 三、为什么 DNS 在代理中如此重要

### 问题 1：DNS 泄露

```
你想要的效果：
浏览器 → Clash DNS → 代理服务器 DNS → 目标网站
        （DNS 也走代理，不泄露真实 IP）

实际可能发生的情况：
浏览器 → 系统 DNS（ISP） → 目标网站
        （DNS 没走代理，ISP 知道你访问了什么）
```

**DNS 泄露的后果：**
- ISP 知道你访问了哪些网站
- **国内网站的 DNS 可能返回海外 CDN 的 IP**（因为 DNS 服务器在海外）
- 网站通过 DNS 解析结果判断你的"位置"

### 问题 2：DNS 返回错误的 IP

这是你遇到的核心问题之一：

```
场景：你在日本代理服务器上查询 baidu.com 的 IP

情况 A（理想）：
DNS 返回中国境内的百度服务器 IP
→ 直连访问，速度快

情况 B（实际可能发生）：
DNS 服务器根据"请求来源 IP"（日本）
返回"离日本最近的百度节点"（可能是日本或香港的 CDN）
→ 这个节点可能容量有限或路由不佳
→ 访问变慢
```

### 问题 3：DNS 污染

```
某些 DNS 查询会被"劫持"，返回错误的 IP

你查询：google.com
污染的 DNS 返回：某个不存在的 IP 或虚假 IP
→ 无法访问
```

## 四、Clash 中的 DNS 配置

Clash 的 DNS 配置非常关键，直接影响分流效果：

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53

  # IPv6 配置
  ipv6: false

  # 增强模式 - 用于 TUN 模式
  enhanced-mode: fake-ip  # 或 redir-host

  # fake-ip 范围
  fake-ip-range: 198.18.0.1/16

  # fake-ip 过滤（这些域名不用 fake-ip）
  fake-ip-filter:
    - '*.lan'
    - localhost.ptlogin2.qq.com
    - '+.srv.nintendo.net'
    - '+.stun.playstation.net'
    - '+.msftconnecttest.com'
    - '+.msftncsi.com'

  # 域名服务器
  default-nameserver:
    - 223.5.5.5      # 阿里 DNS（用于解析下面的 doh 域名）
    - 119.29.29.29   # 腾讯 DNS

  # 分流 DNS 配置
  nameserver:
    - https://doh.pub/dns-query           # 腾讯 DoH
    - https://dns.alidns.com/dns-query    # 阿里 DoH

  # 回退 DNS（当上面失败时使用）
  fallback:
    - https://1.1.1.1/dns-query           # Cloudflare DoH
    - https://dns.google/dns-query        # Google DoH

  # 回退过滤器（决定什么时候用 fallback）
  fallback-filter:
    geoip: true
    geoip-code: CN
    ipcidr:
      - 240.0.0.0/4
      - 0.0.0.0/32
```

### fake-ip 模式 vs redir-host 模式

| 特性 | fake-ip | redir-host |
|------|---------|------------|
| 原理 | 返回假 IP，实际连接时再解析 | 立即解析真实 IP |
| 速度 | 更快（减少 DNS 查询） | 较慢 |
| 规则匹配 | 基于域名 | 基于 IP |
| 兼容性 | 某些应用可能出问题 | 兼容性好 |
| 游戏/PT | 可能有问题 | 推荐 |

**你的情况建议：**
- 如果主要浏览网页：用 `fake-ip`
- 如果玩游戏或遇到奇怪的问题：用 `redir-host`

## 五、DNS 问题诊断方法

### 1. 检查当前使用的 DNS

```bash
# Windows
nslookup baidu.com

# 查看返回的 IP 和使用的 DNS 服务器
```

### 2. 对比不同 DNS 的解析结果

```bash
# 使用阿里 DNS 查询
nslookup baidu.com 223.5.5.5

# 使用 Google DNS 查询
nslookup baidu.com 8.8.8.8

# 使用 Cloudflare DNS 查询
nslookup baidu.com 1.1.1.1

# 对比返回的 IP 是否相同
```

### 3. 检查 DNS 泄露

访问：https://dnsleak.com/

如果显示的服务器位置和你预期的不一致，说明有 DNS 泄露。

### 4. 在 Clash 中开启 DNS 日志

```yaml
# 在配置文件中添加
dns:
  enable: true
  # ...
log-level: debug
```

然后查看 Clash Verge 的日志，看 DNS 查询的实际过程。

## 六、常见 DNS 问题与解决

### 问题 1：国内网站解析到海外 IP

**原因：** DNS 请求走了代理，海外 DNS 服务器返回海外 CDN IP

**解决：**
```yaml
dns:
  nameserver:
    - https://doh.pub/dns-query      # 国内 DNS
    - https://dns.alidns.com/dns-query

  # 关键：确保国内域名使用国内 DNS
  nameserver-policy:
    'geosite:cn': [https://doh.pub/dns-query]
    'geosite:category-games': [https://dns.alidns.com/dns-query]
```

### 问题 2：某些网站无法解析

**原因：** DNS 服务器被污染或无法访问

**解决：** 使用 DoH（DNS over HTTPS）加密 DNS 查询

### 问题 3：游戏/语音软件有问题

**原因：** fake-ip 模式与某些应用不兼容

**解决：**
```yaml
dns:
  enhanced-mode: redir-host
  # 或者把问题域名加入 fake-ip-filter
  fake-ip-filter:
    - '+.stun.*.*'
    - '+.stun.*.*.*'
    - '+.stun.*.*.*.*'
    - '+.stun.*.*.*.*.*'
```

## 🎯 核心要点回顾

1. **DNS 决定了你的流量最终连接到哪个 IP**
2. **DNS 查询的来源 IP 会影响返回的 IP 地址**（CDN 就近原则）
3. **fake-ip 模式更快，但有兼容性问题**
4. **使用国内 DoH 可以避免 DNS 污染，同时获得正确的国内 IP**
5. **DNS 配置是 Clash 分流生效的前提**

## 下一步

- [[分流规则设计]] - 如何让正确的流量走正确的路
- [[Clash配置优化]] - 综合优化你的配置
