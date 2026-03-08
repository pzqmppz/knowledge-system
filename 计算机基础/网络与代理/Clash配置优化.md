---
title: "Clash配置优化"
category: "计算机基础/网络与代理"
tags: ["Clash", "Clash Verge", "TUN模式", "配置优化", "实战"]
date: 2026-03-02
---

# Clash 配置优化

> 针对 Clash Verge + TUN 模式的实战优化指南

## 一、你的问题诊断

根据你的描述（Clash Verge + TUN 模式，国内网站访问慢），问题可能出在：

```
问题定位检查清单
│
├─ ❓ DNS 配置
│   ├─ 是否使用了国内 DoH？
│   ├─ fake-ip 模式是否合适？
│   └─ DNS 是否有泄露？
│
├─ ❓ 分流规则
│   ├─ 规则顺序是否正确？
│   ├─ 是否使用了规则集？
│   └─ 规则是否及时更新？
│
├─ ❓ TUN 模式配置
│   ├─ TUN 是否正确接管流量？
│   └─ 是否有 DNS 劫持？
│
└─ ❓ 代理节点
    ├─ 节点本身是否稳定？
    └─ 节点到国内的速度如何？
```

## 二、推荐配置模板

以下是针对你场景的优化配置，可以直接参考：

### 1. DNS 配置（核心）

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
  ipv6: false

  # 推荐 fake-ip 模式，更快
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16

  # 这些域名不用 fake-ip（避免问题）
  fake-ip-filter:
    - '*.lan'
    - '*.local'
    - '*.localhost'
    - localhost.ptlogin2.qq.com      # QQ 登录
    - '+.srv.nintendo.net'           # 任天堂
    - '+.stun.playstation.net'       # PlayStation
    - '+.msftconnecttest.com'        # 微软网络检测
    - '+.msftncsi.com'
    - '+.stun.*.*'                   # STUN 服务
    - '+.stun.*.*.*'
    - '+.stun.*.*.*.*'
    - lens.l.google.com              # Google STUN
    - 'stun.l.google.com'

  # 基础 DNS（用于解析 DoH 域名）
  default-nameserver:
    - 223.5.5.5
    - 119.29.29.29

  # 主 DNS（国内 DoH，优先）
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query

  # 备用 DNS（国外 DoH）
  fallback:
    - https://1.1.1.1/dns-query
    - https://dns.google/dns-query

  # 回退过滤：国内 IP 用国内 DNS 结果
  fallback-filter:
    geoip: true
    geoip-code: CN
    ipcidr:
      - 240.0.0.0/4
      - 0.0.0.0/32

  # 特定域名使用特定 DNS
  nameserver-policy:
    'geosite:cn': [https://doh.pub/dns-query]
    'geosite:category-games': [https://dns.alidns.com/dns-query]
```

### 2. TUN 模式配置

```yaml
tun:
  enable: true
  stack: system          # 或 gvisor（更稳定但稍慢）
  dns-hijack:
    - any:53
    - tcp://any:53
  auto-route: true       # 自动设置路由
  auto-detect-interface: true  # 自动检测出口网卡
```

### 3. 规则集配置

```yaml
rule-providers:
  # 拒绝广告
  reject:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt"
    path: ./ruleset/reject.yaml
    interval: 86400

  # 代理域名
  proxy:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt"
    path: ./ruleset/proxy.yaml
    interval: 86400

  # 直连域名
  direct:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt"
    path: ./ruleset/direct.yaml
    interval: 86400

  # 中国 IP
  cncidr:
    type: http
    behavior: ipcidr
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt"
    path: ./ruleset/cncidr.yaml
    interval: 86400

  # 私有网络
  private:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt"
    path: ./ruleset/private.yaml
    interval: 86400

rules:
  # 广告拦截
  - RULE-SET,reject,REJECT

  # 私有网络直连
  - RULE-SET,private,DIRECT

  # 代理域名
  - RULE-SET,proxy,PROXY

  # 直连域名
  - RULE-SET,direct,DIRECT

  # 中国 IP 直连
  - RULE-SET,cncidr,DIRECT
  - GEOIP,CN,DIRECT

  # 兜底：其他走代理
  - MATCH,PROXY
```

### 4. 策略组配置

```yaml
proxy-groups:
  # 主代理选择
  - name: PROXY
    type: select
    proxies:
      - 自动选择
      - 手动选择
      - DIRECT

  # 自动选择最快节点
  - name: 自动选择
    type: url-test
    proxies:
      - 节点1
      - 节点2
      # ... 你的节点
    url: 'http://www.gstatic.com/generate_204'
    interval: 300

  # 手动选择
  - name: 手动选择
    type: select
    proxies:
      - 节点1
      - 节点2
      # ... 你的节点
```

## 三、Clash Verge 特定设置

### 1. 界面设置

在 Clash Verge 中：

1. **设置 → 系统设置**
   - 开启「TUN 模式」
   - 开启「系统代理」（可选，TUN 模式下不需要）

2. **设置 → Clash 设置**
   - 开启「允许局域网连接」（如果需要）
   - 设置「外部控制」端口（默认 9090）

### 2. 配置文件管理

推荐使用「Merge」配置，而不是直接修改订阅：

1. 打开 Clash Verge
2. 点击「配置」→「新建」→「Merge」
3. 添加你的自定义配置（DNS、规则等）
4. 这样订阅更新不会覆盖你的修改

### Merge 配置示例

```yaml
# Merge 配置 - 只写你要覆盖的部分

dns:
  enable: true
  enhanced-mode: fake-ip
  # ... 上面的 DNS 配置

rule-providers:
  # ... 上面的 rule-providers 配置

rules:
  # ... 上面的 rules 配置

# 在规则最前面插入
prepend-rules:
  - DOMAIN-SUFFIX,example.com,DIRECT  # 你的自定义规则

# 在代理最前面插入
prepend-proxies:
  # 自定义代理节点

# 在策略组最前面插入
prepend-proxy-groups:
  # 自定义策略组
```

## 四、常见问题解决

### 问题 1：访问国内网站仍然很慢

**排查步骤：**

1. **检查连接日志**
   ```
   Clash Verge → 连接 → 查看该网站走的是什么规则
   ```

2. **检查 DNS 解析**
   ```bash
   nslookup 问题网站.com
   # 看返回的 IP 是国内还是国外
   ```

3. **临时关闭 TUN 模式测试**
   - 如果关闭后正常，说明是分流规则问题
   - 如果关闭后仍然慢，说明是网络本身问题

4. **检查是否是网站自身问题**
   - 某些网站会主动检测并限制代理 IP
   - 这是网站行为，你无法完全解决

### 问题 2：某些网站无法访问

1. **检查是否被广告规则拦截**
   ```
   暂时注释掉 reject 规则，看是否恢复正常
   ```

2. **检查 DNS 解析是否正常**
   ```bash
   nslookup 无法访问的网站.com
   ```

3. **尝试切换到 redir-host 模式**
   ```yaml
   dns:
     enhanced-mode: redir-host
   ```

### 问题 3：游戏/语音有问题

1. **把游戏相关域名加入 fake-ip-filter**
2. **或切换到 redir-host 模式**
3. **检查 UDP 是否正常**（某些代理节点不支持 UDP）

### 问题 4：规则更新后仍然有问题

1. **手动更新规则集**
   ```
   Clash Verge → 配置 → 更新规则集
   ```

2. **清除 DNS 缓存**
   ```bash
   # Windows
   ipconfig /flushdns

   # 在 Clash Verge 中重启内核
   ```

3. **清除浏览器缓存**
   ```
   Chrome: chrome://net-internals/#dns → Clear host cache
   ```

## 五、调试技巧

### 1. 开启详细日志

```yaml
log-level: debug
```

### 2. 查看连接详情

Clash Verge → 连接 → 点击具体连接查看：
- 匹配的规则
- 使用的策略组
- 实际的代理节点
- 连接耗时

### 3. 测试 DNS

```bash
# 使用 Clash 的 DNS 测试
nslookup baidu.com 127.0.0.1

# 对比使用公共 DNS
nslookup baidu.com 223.5.5.5
```

### 4. 测试代理延迟

```bash
# 直接 ping 国内网站
ping baidu.com

# 通过代理 curl
curl -x http://127.0.0.1:7890 https://www.baidu.com -w "Time: %{time_total}s\n"
```

## 六、终极建议

如果以上都优化了仍然有问题，可能是：

1. **代理节点质量问题**
   - 换一个更好的节点
   - 选择离中国更近的节点（香港、日本、新加坡）

2. **网站自身的限制**
   - 某些网站就是会限制代理 IP
   - 这是网站策略，无法完全绕过

3. **网络环境问题**
   - ISP 本身的网络质量
   - 高峰期网络拥堵

## 🎯 核心要点回顾

1. **DNS 配置是最重要的** - 先确保 DNS 正确
2. **使用 Merge 配置** - 不直接修改订阅
3. **使用规则集** - 比手动维护更全面
4. **善用日志功能** - 看清楚流量走向
5. **有些问题无法解决** - 网站主动限制代理 IP

## 相关链接

- [Clash Wiki](https://clash.wiki/)
- [Loyalsoldier 规则集](https://github.com/Loyalsoldier/clash-rules)
- [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev)
