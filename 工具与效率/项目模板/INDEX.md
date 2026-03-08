---
title: "项目模板索引"
category: "工具与效率"
tags: ["模板", "项目初始化", "工程标准化"]
date: 2026-03-02
status: "completed"
---

# 项目模板

> 新项目初始化的标准模板集合

## 📋 模板文件

| 文件 | 说明 | 使用场景 |
|------|------|----------|
| [CLAUDE模板.md](./CLAUDE模板.md) | Claude Code 项目配置模板 | 所有使用 Claude Code 的项目 |
| [ENV模板.md](./ENV模板.md) | 环境变量配置模板 | 需要管理敏感信息的项目 |
| [CHANGELOG模板.md](./CHANGELOG模板.md) | 变更日志模板 | 跟踪代码与文档同步状态 |
| [项目初始化指南.md](./项目初始化指南.md) | 完整的项目初始化流程 | 新建项目时参考 |

## 🚀 快速开始

```bash
# 1. 复制模板到新项目
cp CLAUDE模板.md <your-project>/CLAUDE.md
cp ENV模板.md <your-project>/.env.example

# 2. 根据实际情况修改配置
vim CLAUDE.md
vim .env.example

# 3. 创建实际环境变量（不提交到 git）
cp .env.example .env
vim .env
```

## 📁 推荐项目结构

```
project/
├── CLAUDE.md              # Claude Code 配置（AI + 人类）
├── CHANGELOG.md           # 变更日志（跟踪文档同步状态）
├── .env.example           # 环境变量模板（提交）
├── .env                   # 实际配置（不提交）
├── README.md              # 项目说明
├── docs/
│   ├── PROJECT_INIT.md    # 项目初始化记录
│   ├── ARCHITECTURE.md    # 架构设计
│   └── DEPLOYMENT.md      # 部署方案
├── src/                   # 源代码
└── tests/                 # 测试代码
```

## 🔒 数据安全

- ✅ **提交**：CLAUDE.md、.env.example、docs/
- ❌ **不提交**：.env、密钥文件、临时配置
- 📝 **引用方式**：在 CLAUDE.md 中说明敏感信息的存放路径

## 📝 模板更新

最后更新：2026-03-02
