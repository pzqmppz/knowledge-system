# Context7 深度指南

> 将最新的技术文档注入 AI 上下文，解决模型训练数据滞后问题

---

## 目录

- [什么是 Context7](#什么是-context7)
- [核心问题与解决方案](#核心问题与解决方案)
- [工作原理](#工作原理)
- [安装与配置](#安装与配置)
- [使用方法](#使用方法)
- [支持的库与生态](#支持的库与生态)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 什么是 Context7

**Context7** 是由 **Upstash** 团队开发的基于 **MCP（Model Context Protocol）** 的文档服务工具，专门解决大语言模型（LLMs）训练数据滞后导致的代码生成问题。

### 核心定位

```
┌─────────────────────────────────────────────────────────┐
│  Context7 = AI 编程助手的"实时文档外挂"                    │
│                                                         │
│  不是替代 AI，而是为 AI 提供最新、准确的上下文信息          │
└─────────────────────────────────────────────────────────┘
```

### 关键特性

| 特性 | 说明 |
|------|------|
| **实时文档获取** | 从官方源（GitHub、npm、官方文档网站）拉取最新文档 |
| **版本特定** | 根据目标库的版本匹配相应文档，避免版本不一致问题 |
| **MCP 集成** | 通过 Model Context Protocol 与主流 AI 工具无缝集成 |
| **减少幻觉** | 降低 AI 生成不存在 API 或过时代码的可能性 |
| **广泛支持** | 已索引超过 **68,000+** 个流行库 |
| **免费使用** | 个人用户每天可免费查询 **50 次** |

---

## 核心问题与解决方案

### AI 编程的三大痛点

```
痛点 1: 训练数据滞后
├─ GPT-4 训练数据截止 2023 年
├─ 框架快速迭代（Next.js、React 每年多次更新）
└─ AI 无法获取新版本的 API 变更

痛点 2: 幻觉 API
├─ 小众库容易产生虚构的 API
├─ 过时的参数和废弃方法
└─ 代码看起来对，但跑不通

痛点 3: 文档复制困境
├─ 手动复制文档超出 token 限制
├─ AI 无法获取完整上下文
└─ 建议不够准确，需要反复验证
```

### Context7 的解决方案

```
┌─────────────────────────────────────────────────────────┐
│  传统提示工程                     Context7 上下文工程      │
├─────────────────────────────────────────────────────────┤
│  依赖模型训练数据        →        动态获取最新官方文档      │
│  每次提示需重新设计      →        一次配置，持续生效        │
│  局限于提示词长度        →        可扩展至数千 token       │
└─────────────────────────────────────────────────────────┘
```

---

## 工作原理

### 数据处理流程

```
官方文档源
    │
    ↓
┌─────────────────────────────────────────────────────────┐
│  1. 解析 (Parse)                                        │
│     从文档中提取代码片段和示例                            │
└─────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────┐
│  2. 丰富 (Enrich)                                       │
│     使用 LLMs 添加简短解释和元数据                        │
└─────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────┐
│  3. 向量化 (Vectorize)                                  │
│     嵌入内容以便进行语义搜索                              │
└─────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────┐
│  4. 重新排名 (Rerank)                                   │
│     使用自定义算法对结果进行相关性评分                     │
└─────────────────────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────────────────────┐
│  5. 缓存 (Cache)                                        │
│     通过 Redis 提供请求，获得最佳性能                     │
└─────────────────────────────────────────────────────────┘
```

### MCP 协议集成

Context7 通过 MCP 协议暴露两个核心接口：

| 接口 | 功能 | 使用场景 |
|------|------|----------|
| `resolve-library-id` | 解析库名称，找到具体的包 | 模糊搜索库（如输入 "next" 找到 Next.js） |
| `get-library-docs` | 获取指定包的文档内容 | 获取特定版本的官方文档和代码示例 |

---

## 安装与配置

### 前置要求

- **Node.js** >= v18.0.0
- 已安装支持 MCP 的 AI 工具（Claude Code、Cursor、Windsurf 等）

### Claude Code 配置

#### 方法一：命令行安装

```bash
# 添加 Context7 MCP 服务器
claude mcp add context7 --transport http --url https://context7.upstash.io/mcp

# 验证是否成功
claude mcp list
```

#### 方法二：配置文件安装

编辑 `~/.claude.json`（Windows: `%USERPROFILE%\.claude.json`）：

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://context7.upstash.io/mcp"
    }
  }
}
```

### Cursor 配置

#### 方法一：界面配置

1. 打开 `Settings` → `Cursor Settings` → `MCP`
2. 点击 `Add new global MCP server`
3. 添加配置

#### 方法二：配置文件

编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### Windsurf 配置

编辑 `~/.windsurfmcp.json`：

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### Claude Desktop 配置

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或
`%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

---

## 使用方法

### 基本使用模式

在提示词末尾添加 **`use context7`**：

```
创建一个使用 Next.js App Router 的登录页面组件。use context7
```

### Claude Code 中的使用

#### 方法一：显式声明

```
请使用 Context7 的 /vercel/next.js 库查询最新文档后，回答：
如何在 Next.js 15 中使用 Server Actions？
```

#### 方法二：关键词触发

```
创建一个使用 React 18 的 createRoot API 的项目。use context7
```

### 实际效果对比

#### 不使用 Context7

```javascript
// AI 生成的过时代码（基于 Next.js 12）
import ReactDOM from 'react-dom';
ReactDOM.render(<App />, document.getElementById('root'));
```

#### 使用 Context7

```javascript
// 基于最新文档生成的正确代码（Next.js 15 + React 18）
import { createRoot } from 'react-dom/client';
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
```

---

## 支持的库与生态

### 数据规模

截至 2026 年，Context7 已索引：

| 指标 | 数量 |
|------|------|
| 索引库总数 | **68,716+** |
| 代码片段数 | **数百万** |
| 代码示例最多的库 | n8n (25,321+ 片段) |
| 覆盖语言 | JavaScript, Python, Go, Rust, PHP 等 |

### 主流支持的技术栈

```
前端框架
├─ Next.js (/vercel/next.js)
├─ React (/facebook/react)
├─ Vue (/vuejs/core)
└─ Svelte (/sveltejs/svelte)

后端框架
├─ FastAPI (/tiangolo/fastapi)
├─ Django (/django/django)
├─ Express (/expressjs/express)
└─ NestJS (/nestjs/nest)

数据库
├─ Prisma (/prisma/prisma)
├─ Drizzle ORM (/drizzle-team/drizzle-orm)
└─ PostgreSQL (/postgres/postgres)

工具库
├─ Tailwind CSS (/tailwindlabs/tailwindcss)
├─ Shadcn UI (/shadcn-ui/ui)
└─ Vercel AI SDK (/vercel/ai-sdk-kit)

自动化工具
└─ n8n (/n8n-io/n8n)
```

---

## 最佳实践

### 1. 明确指定版本

```
❌ 模糊：如何使用 Next.js 的路由？

✅ 明确：如何在 Next.js 15.3 中使用 App Router？use context7
```

### 2. 结合具体场景

```
❌ 泛泛：给我一个 React 组件示例

✅ 具体：创建一个带有表单验证的登录组件，
        使用 React Hook Form 和 Zod。use context7
```

### 3. 利用库名称解析

```
# 查询 n8n 相关文档
请使用 Context7 的 /llmstxt/n8n_io_llms-full_txt 库，
查询如何在 Code 节点中访问上一个节点的数据
```

### 4. 多库联合查询

```
创建一个项目，使用以下技术栈：
- Next.js 15 App Router
- Prisma ORM
- Tailwind CSS
- Shadcn UI 组件

请分别使用 Context7 查询各库的最新文档后生成代码
```

---

## 常见问题

### Q1: Context7 是免费的吗？

**A:** 个人用户完全免费，每天可查询 **50 次**。团队和企业可能需要付费计划。

### Q2: Context7 能离线使用吗？

**A:** 不能。Context7 是基于 HTTP 的 MCP 服务，需要网络连接。

### Q3: 如何知道查询的是哪个版本？

**A:** Context7 会自动根据项目依赖识别版本，或使用你明确指定的版本（如 `next.js@15`）。

### Q4: 支持私有库吗？

**A:** 目前主要支持公共开源库。私有库支持可能在未来的企业版本中提供。

### Q5: 与官方文档有什么区别？

**A:** Context7 不替代官方文档，而是：
- 提取官方文档的核心代码片段
- 清理冗余内容，保留关键信息
- 通过语义搜索快速定位相关内容
- 直接注入 AI 上下文，避免手动复制

### Q6: 为什么 Claude Code 已经有 Context7 插件？

**A:** Context7 有两种使用方式：
1. **MCP 服务器**：通过配置使用（本文介绍的方式）
2. **Claude Code 插件**：通过 `/plugins` 命令安装

两者本质相同，都是调用 Context7 的 API。

---

## 相关资源

### 官方资源

- **官网**: https://context7.io
- **GitHub**: https://github.com/upstash/context7
- **MCP 协议**: https://modelcontextprotocol.io

### 社区资源

- **Claude Code 文档**: https://docs.anthropic.com/claude-code
- **Cursor MCP 文档**: https://cursor.sh/docs/mcp
- **MCP 生态**: https://smithery.ai

---

## 附录：配置示例

### 完整的 Claude Code 配置示例

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://context7.upstash.io/mcp"
    },
    "web-reader": {
      "type": "http",
      "url": "https://open.bigmodel.cn/api/mcp/web_reader/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### 常用库名称速查表

| 技术栈 | Context7 Library ID |
|--------|---------------------|
| Next.js | `/vercel/next.js` |
| React | `/facebook/react` |
| Vue | `/vuejs/core` |
| FastAPI | `/tiangolo/fastapi` |
| Prisma | `/prisma/prisma` |
| n8n（完整版） | `/llmstxt/n8n_io_llms-full_txt` |
| n8n（精简版） | `/n8n-io/n8n-docs` |
| Tailwind CSS | `/tailwindlabs/tailwindcss` |

---

*最后更新: 2026-03-06*
