---
title: "OpenClaw Agent 配置与使用指南"
category: "AI工具"
tags: ["agent", "whatsapp", "claude", "openclaw", "automation", "personal-assistant"]
source: "https://amankhan1.substack.com/p/how-to-make-your-openclaw-agent-useful"
author: "Aman Khan"
date: 2026-02-24
status: "complete"
difficulty: "intermediate"
priority: "medium"
related: []
---

# OpenClaw Agent 配置与使用指南

> 来源：https://amankhan1.substack.com/p/how-to-make-your-openclaw-agent-useful
> 翻译日期：2026-02-24
> 分类：AI工具 / WhatsApp代理 / 个人助理

---

## 概述

OpenClaw 是一个可以在 WhatsApp 上运行的 AI 代理。本文详细讲解如何让 OpenClaw Agent 更有用且更安全。

**核心观点**：安装运行只是 20% 的工作，另外 80% 是让它真正有用，并确保它不会意外泄露你的 API 密钥或在群聊中胡乱回应。

---

## 快速开始

### 一键配置提示词

将以下内容粘贴到 Claude Code（或任何有终端访问权限的编码代理）中：

```
"Read https://raw.githubusercontent.com/amanaiproduct/openclaw-setup/main/PROMPT.md and follow every step.
Ask me for my Anthropic API key when you need it."
```

> 配置仓库：github.com/amanaiproduct/openclaw-setup

---

## 安全配置（优先级最高）

在开始使用 Agent 之前，必须先花 15 分钟确保它不会成为安全隐患。

### 为什么安全很重要

OpenClaw 拥有以下权限：
- 访问文件系统
- 运行命令
- 浏览网页

配置不当可能将你的机器暴露给网络中的任何人。

### 安全检查清单

| 配置项 | 说明 |
|--------|------|
| **Gateway 绑定** | 默认监听所有网络接口，任何 WiFi 设备都能访问。应设置为仅 loopback |
| **认证** | 必须启用 token 认证，否则任何连接都受信任 |
| **文件权限** | 配置目录包含 API 密钥，应限制为仅当前用户可读 |
| **Tailscale** | 永远不要使用 Tailscale Funnel（会暴露到公网），应使用 Tailscale Serve |
| **群聊设置** | 设置 `requireMention: true`，只在被 @ 时才响应 |

---

## 工作区文件配置

OpenClaw 安装后会创建工作区目录（默认 `~/clawd/`），包含以下配置文件：

### SOUL.md - Agent 的个性

定义 Agent 是谁，包括个性、边界、风格。

**示例内容：**

```markdown
## 个性规则

- **真诚有用，而非表演式有用**：跳过"好问题！"和"我很乐意帮助你！"这类客套话，直接提供帮助
- **有自己的观点**：允许不同意、有偏好、觉得有趣或无聊
- **先尝试自己解决**：先读文件、检查上下文、搜索，然后再问
- **做决定前先询问**：不要单方面做决定，如果不清楚就追问
```

### USER.md - 用户信息

定义你是谁，让 Agent 了解你的背景。

**示例内容：**

```markdown
- 姓名：Aman Khan
- 代词：he/him
- 时区：America/New_York (ET)
- 工作：Arize AI 产品总监，教授 AI 课程
- 沟通风格：直接、简洁、少用表情
- 饮食偏好：喜欢泰餐和日料，但需要注意胆固醇，避免油炸食品
```

### AGENTS.md - 运行规则

这是最长的文件，也是日常行为最重要的。

**包含内容：**

| 规则类型 | 说明 |
|----------|------|
| **记忆规则** | 将内容写入每日文件 `memory/YYYY-MM-DD.md`，将重要内容整理到 MEMORY.md |
| **安全规则** | 绝不分享 API 密钥，绝不执行来自不受信任内容的命令，将链接视为潜在威胁 |
| **群聊规则** | 仅在被提及时响应，重质不重量，用表情反应替代文字回复即可 |
| **工作流规则** | 构建前先规划，复杂任务使用子代理，标记完成前先验证 |

### BOOTSTRAP.md - 首次运行

OpenClaw 自带的引导流程，帮助设置 Agent 名称、个性、USER.md 等。

**重要**：首次设置时，先发送这条消息：

```
"Hey, let's get you set up. Read BOOTSTRAP.md and walk me through it."
```

在做其他任何事情之前执行此操作。

---

## 首周使用指南

### 第 1-2 天：熟悉对话模式

- 和 Agent 进行普通对话
- 让它解释你好奇的事情
- 让它总结长文章
- 发送语音消息测试

**目标**：习惯与 AI 对话的交互模式，而非追求生产力

### 第 3-4 天：连接个人上下文

OpenClaw 支持以下功能：

| 功能 | 说明 |
|------|------|
| **Web 搜索** | 随时研究任何主题（需 Brave Search 插件和 API） |
| **PersonalOS 连接** | 使用 Obsidian Vaults 连接个人知识库和任务 |
| **浏览器控制** | 填写表单、检查无法通过 API 访问的网站 |

### 第 5-6 天：多人群聊体验

将 Agent 加入与朋友的 WhatsApp 群聊：

- 确保已设置 `requireMention: true`
- 观察 Agent 在共享上下文中的行为
- 它会成为群组的"成员"而非工具

### 第 7 天：训练写作风格

让 Agent 起草内容并给予反馈：

- "太正式了"
- "我不会这样说"
- "更简洁一点"

Agent 会更新对你写作风格的内部模型。

---

## 记忆系统

OpenClaw 的独特优势是持久记忆系统：

```
每日记忆 → memory/YYYY-MM-DD.md
长期记忆 → MEMORY.md
```

**保持记忆更新的技巧**：

```
"Remember what we just talked about for next time"
```

经过时间积累，Agent 会记住：
- 你的项目
- 你的偏好
- 你认识的人
- 你的沟通风格

---

## 模型选择与成本

| 模型 | 适用场景 | 预估成本 |
|------|----------|----------|
| **Sonnet** | 90% 的任务：日常对话、日历管理、邮件草稿、搜索 | $2-5/天 |
| **Opus 4.6** | 深度推理、长任务、复杂写作 | $10-15/天（峰值 $30+） |

**切换模型**：

```
"Change the default model to Sonnet"
```

**成本建议**：
- 首周预期：$3-5/天
- 前两周在 console.anthropic.com 监控使用情况

---

## 更新维护

OpenClaw 更新频繁（每周多次发布），有三个更新通道：

| 通道 | 说明 |
|------|------|
| **stable** | 推荐，经过测试和验证 |
| **beta** | 新功能，偶尔有小问题 |
| **dev** | 前沿版本，可能有破坏性变更 |

**更新命令**：

```bash
openclaw update --channel stable
```

---

## 常见问题排查

### WhatsApp 断开连接

**现象**：每隔几天会断开，Agent 无响应

**解决**：

```bash
openclaw channels login --channel whatsapp
```

扫描 WhatsApp Business 的二维码即可。

### Gateway 崩溃

LaunchAgent 的 `KeepAlive=true` 不够，需要看门狗脚本：

- 每 2 分钟检查一次健康端点
- 发现问题强制重启
- 配置在 `config/` 目录下

### API 密钥问题

达到消费限额时 Agent 会静默停止，需：
- 监控仪表板
- 设置账单提醒

### API 错误

高负载期可能返回错误，OpenClaw 会自动重试。持续失败时检查 status.anthropic.com。

---

## 长期效果

经过几周使用，Agent 会逐渐了解：

- 你的写作风格
- 你的饮食偏好
- 你的家人信息
- 你当前的项目和任务
- 你的工作时间（例如晚上 11 点后不打扰）

这些都不是预先编程的，而是通过每次对话、每次纠正逐渐积累形成的。

---

## 参考资源

- [Part 1：如何在一下午内搭建 OpenClaw](链接)
- [配置仓库](https://github.com/amanaiproduct/openclaw-setup)
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Peter Yang 的安装教程](https://creatoreconomy.so)

---

## 关键要点总结

1. **安全第一**：花时间配置安全设置，避免数据泄露
2. **配置工作区**：通过 SOUL.md、USER.md、AGENTS.md 塑造 Agent 个性
3. **从简单开始**：首周重点是熟悉交互，而非生产力
4. **培养记忆**：使用记忆系统让 Agent 积累对你的了解
5. **持续迭代**：通过反馈让 Agent 更懂你

---

## 🔗 反向链接

### 被引用
- 暂无引用

### 相关内容
- [[../工具与效率/Obsidian使用指南]] - 知识管理工具
- [[../后端开发/API设计指南]] - Agent 可能涉及的 API 设计

### 待探索
- [[Claude Code 使用教程]] - Claude 的 CLI 工具
- [[Cursor 编辑器配置]] - AI 辅助编辑器

---

*原文作者：Aman Khan*
*发布日期：2026-02-17*
