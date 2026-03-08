---
title: "CLAUDE.md 项目配置模板"
category: "工具与效率"
tags: ["模板", "Claude-Code", "项目配置"]
date: 2026-03-02
status: "completed"
---

# CLAUDE.md 项目配置模板

> 将此文件复制为项目根目录的 `CLAUDE.md`，并填入实际信息

---

## 🤖 Claude 会话启动声明

**重要：在开始任何工作之前，Claude 必须：**

1. ✅ 完整阅读本 CLAUDE.md 文件
2. ✅ 阅读 CHANGELOG.md 了解最新变更
3. ✅ 确认信息优先级：**代码 > 文档**
4. ✅ 遇到不确定时，先验证代码再行动

**工作原则：**
- 代码即真理，文档仅供参考
- 发现文档与代码不一致时，以代码为准
- 需要修改代码前，先阅读现有代码理解现状
- 完成变更后，提醒用户更新 CHANGELOG

---

## 项目信息

```yaml
项目名称: [填写项目名称]
项目类型: [Web应用 / CLI工具 / 库 / API服务]
开发阶段: [初始化 / 开发中 / 测试中 / 生产中]
技术栈: [主要技术栈，如: React + Node.js + PostgreSQL]
```

---

## ⚠️ 信息优先级（重要）

> 本项目可能存在文档与代码不完全同步的情况，请按以下优先级获取信息：

### 信息可信度层级

| 优先级 | 信息源 | 可信度 | 说明 |
|--------|--------|--------|------|
| **1** | **实际代码** | 🔴 最高 | 代码即真理，一切以实际代码为准 |
| **2** | CLAUDE.md | 🟠 高 | 本文件，应保持最新 |
| **3** | CHANGELOG.md | 🟡 中 | 变更记录，了解演进历史 |
| **4** | docs/*.md | 🟢 低 | 架构/设计文档，可能滞后 |
| **5** | 早期 PRD | 🔵 很低 | 仅作历史参考，现状可能完全不同 |

### 快速验证方法

当文档信息不一致时，优先验证代码：

| 信息类型 | 快速验证方式 | 优先查看文件 |
|----------|--------------|--------------|
| 项目架构 | 查看 src/ 目录结构 | `ls -la src/` |
| API 路由 | 查看路由定义 | `src/routes/*.ts` |
| 数据模型 | 查看模型定义 | `src/models/*.ts` |
| 配置信息 | 查看配置文件 | `package.json`, `.env.example` |
| 依赖版本 | 查看依赖声明 | `package.json`, `go.mod` |

### 文档状态同步

```yaml
# 当前代码版本
code_version: [从 package.json / git tag 获取]

# 文档最后同步版本
doc_sync_version: [手动维护]

# 差距说明
sync_gap: |
  - v0.6.1: 添加了用户认证模块（代码已更新，文档待更新）
  - v0.6.2: 修复了数据库连接池问题（无需更新文档）
  - v0.6.3: API 路由重构（docs/API.md 需要更新）
```

### Claude 工作原则

```yaml
决策原则: "代码优先，文档参考"

工作流程:
  1. 首先阅读 CLAUDE.md 了解项目概况
  2. 阅读 CHANGELOG.md 了解最新变更
  3. 需要具体细节时，直接阅读相关代码文件
  4. 如需查阅文档，优先查看文档顶部的时间戳
  5. 发现文档与代码不一致时，以代码为准
  6. 可在变更时提醒用户更新相关文档

强制验证步骤:
  修改代码前:
    - 必须先阅读现有代码
    - 必须确认当前实现
    - 不能仅依赖文档描述

  参考文档时:
    - 检查文档时间戳
    - 对比 CHANGELOG 确认是否过期
    - 过期文档必须用代码验证

异常处理:
  - 如果文档时间戳超过 7 天，自动降低信任度
  - 如果 CHANGELOG 有未同步的变更，优先参考代码
  - 疑惑时直接询问用户："文档与代码不一致，以哪个为准？"
  - 不确定时，主动阅读代码确认，不要猜测
```

---

## 仓库信息

| 项目 | 地址 |
|------|------|
| GitHub 仓库 | `[github.com/username/repo]` |
| 文档仓库 | `[如有独立文档仓库]` |
| Issue 跟踪 | `[GitHub Issues / Jira / 其他]` |

---

## Claude Code 配置

### 首选模型
```yaml
默认模型: glm-4.7
复杂任务模型: claude-opus-4-6
快速任务模型: claude-haiku-4-5
```

### 必需 Skills
```yaml
开发阶段:
  - tdd                     # 测试驱动开发
  - security-review         # 安全审查
  - simplify                # 代码简化

文档阶段:
  - obsidian-markdown       # Obsidian Markdown

部署阶段:
  - e2e                     # 端到端测试
```

---

## 敏感信息指引

> 以下信息不存放在代码仓库中，仅说明存放位置

### 本地密钥文件
```bash
# SSH 密钥
~/.ssh/[project_name]_key

# API 密钥
~/.config/[project_name]/api_keys.json

# 云服务凭证
~/.aws/credentials (profile: [project_name])
```

### 环境变量
```bash
# 实际配置文件位置
.env

# 模板文件位置
.env.example

# 加载方式
# Claude Code 读取 .env.example 了解结构
# 实际值从 .env 或本地文件读取
```

### 服务器连接
```yaml
开发服务器:
  地址: [dev.example.com]
  连接方式: [SSH 配置文件中的 Host 别名]
  配置文件: ~/.ssh/config

生产服务器:
  部署方式: [GitHub Actions / 手动部署 / 其他]
  详细配置: docs/DEPLOYMENT.md
```

---

## 开发命令

### 本地开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 代码检查
npm run lint

# 运行测试
npm test
```

### 数据库
```bash
# 启动本地数据库
docker-compose up -d postgres

# 运行迁移
npm run migrate

# 填充测试数据
npm run seed
```

### 构建
```bash
# 生产构建
npm run build

# 预览构建结果
npm run preview
```

### 部署
```bash
# 部署到开发环境
npm run deploy:dev

# 部署到生产环境
npm run deploy:prod
```

---

## 项目结构

```
project/
├── CLAUDE.md              # 本文件
├── .env.example           # 环境变量模板
├── README.md              # 项目说明
├── docs/
│   ├── PROJECT_INIT.md    # 项目初始化记录
│   ├── ARCHITECTURE.md    # 架构设计
│   ├── API.md             # API 文档
│   └── DEPLOYMENT.md      # 部署方案
├── src/                   # 源代码
├── tests/                 # 测试代码
└── scripts/               # 构建和部署脚本
```

---

## 开发规范

### Git 工作流
```yaml
分支策略: [GitFlow / Trunk-Based / 其他]
主分支: main/master
开发分支: develop
特性分支: feature/xxx
修复分支: fix/xxx
```

### Commit 规范
```
feat: 新功能
fix: 修复 Bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具
```

---

## AI 辅助开发指引

### 使用场景
1. **新功能开发**：使用 `/plan` 先规划，再用 `tdd` 技能开发
2. **Bug 修复**：先阅读相关代码，再提出修复方案
3. **代码审查**：使用 `code-review` 技能检查 PR
4. **部署准备**：使用 `security-review` 检查安全问题

### 禁止操作
- ❌ 不要提交 .env 文件
- ❌ 不要在代码中硬编码密钥
- ❌ 不要跳过测试直接部署
- ❌ 不要修改已发布的 API 接口

---

*模板版本: 1.0.0 | 最后更新: 2026-03-02*
