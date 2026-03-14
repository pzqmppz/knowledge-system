---
title: "AI工具分类索引"
category: "AI工具"
tags: ["index", "AI工具"]
date: 2026-03-06
status: "updated"
---

# AI工具分类索引

> 最后更新：2026-03-06

## 📁 本分类包含

- **本地模型部署** - ASR、TTS 等本地 AI 模型
- **AI Agent** - 自动化代理和个人助理
- **AI 工作流** - 工作流自动化和集成
- **Prompt Engineering** - 提示词工程
- **代码生成** - AI 辅助代码生成工具
- **开发流程** - AI 辅助开发的最佳实践和流程

---

## 📂 子分类

| 分类 | 说明 | 文件数 |
|------|------|--------|
| [VIBE CODING](./VIBE%20CODING/) | AI 辅助开发流程文档（拆分版） | 11 |
| [语音识别 (ASR)](./语音识别/INDEX.md) | 本地语音识别模型 | 2 |
| [语音合成 (TTS)](./语音合成/INDEX.md) | 语音合成和声音克隆 | 1 |
| [Agent](./Agent/INDEX.md) | AI 代理和自动化 | 1 |

---

## 📄 根目录文件

### 部署框架

| 文件 | 标签 | 难度 | 日期 |
|------|------|------|------|
| [本地模型部署框架](./本地模型部署框架.md) | #部署框架 #模板 #脚本 #可复用 | beginner | 2026-02-26 |

### 工具指南

| 文件 | 标签 | 难度 | 日期 |
|------|------|------|------|
| [智谱AI输入法 - 产品介绍](./智谱AI输入法-产品介绍.md) | #语音输入 #指令理解 #VoiceCoding | beginner | 2026-03-09 |
| [Context7 深度指南](./CONTEXT7-深度指南.md) | #MCP #文档 #AI编程 #Claude-Code | beginner | 2026-03-06 |
| [VIBE CODING v2.0](./VIBE%20CODING%202.0.md) | #Claude-Code #开发流程 #AI编程 #SOP | beginner | 2026-03-06 |
| → [VIBE CODING/](./VIBE%20CODING/) | 拆分文档（11 个文件）| | |

### 项目部署报告

| 文件 | 标签 | 难度 | 日期 |
|------|------|------|------|
| [Dify本地部署指南](./Dify本地部署指南.md) | #部署 #Docker #LLM #工作流 | beginner | 2026-03-06 |
| [screenshot-to-code 部署报告](./screenshot-to-code部署报告.md) | #部署 #Docker #代码生成 #GLM | intermediate | 2026-03-04 |

---

## 🏷️ 标签索引

### 模型类型
- #ASR - 自动语音识别
- #TTS - 语音合成
- #声音克隆 - Voice Cloning
- #LLM - 大语言模型
- #工作流 - Workflow Automation

### 部署相关
- #Docker - 容器化部署
- #CUDA - GPU 计算
- #本地部署 - 本地模型

### Agent 相关
- #agent - AI 代理
- #automation - 自动化
- #personal-assistant - 个人助理

### 开发相关
- #Claude-Code - Anthropic Claude 代码编辑器
- #SOP - 标准操作流程
- #AI编程 - AI 辅助编程

---

## 🔗 相关链接

### 外部资源
- [HuggingFace](https://huggingface.co) - 模型托管平台
- [ModelScope](https://modelscope.cn) - 阿里模型平台
- [Claude API 文档](https://docs.anthropic.com)
- [Dify 官网](https://dify.ai) - LLM 应用开发平台

### 本站相关
- [工具与效率](../工具与效率/INDEX.md) - 传统工具与效率提升
- [后端开发](../后端开发/INDEX.md) - Agent 可能涉及的后端知识
- [编程项目/项目讨论](../编程项目/项目讨论/) - 项目讨论和方案设计

---

## 📊 部署模型汇总

| 模型 | 类型 | 端口 | 显存 | 状态 |
|------|------|------|------|------|
| WhisperX | ASR | 8000 | ~8GB | ✅ |
| Qwen3-ASR | ASR | 8001 | ~6GB | ✅ |
| Qwen3-TTS (VoiceDesign) | TTS | 8003 | ~4GB | ✅ |
| Qwen3-TTS (Base) | TTS | 8004 | ~4GB | ✅ |
| Screenshot-to-Code | 代码生成 | 5173/7001 | API | ✅ |
| Dify | 工作流平台 | 8090 | ~2GB | ✅ |

### 部署项目清单
| 项目 | 路径 | 说明 | 日期 |
|------|------|------|------|
| Dify | `E:\ai-deploy\dify\` | LLM 应用开发平台，支持工作流和 Agent | 2026-03-06 |
| Screenshot-to-Code | `E:\docker-projects\screenshot-to-code\` | 截图转代码工具，集成智谱 GLM-4.6V | 2026-03-04 |

---

*此文件由程序自动维护*
