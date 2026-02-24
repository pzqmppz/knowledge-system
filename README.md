# 知识体系

> 日常学习知识点记录库 - 人机双可读

## 项目说明

本项目采用 **VS Code + Markdown** 架构，旨在构建一个既方便人类阅读又便于程序解析的知识管理系统。

- 人读：VS Code 编辑、Markdown 预览、Obsidian 可视化
- 机读：YAML Frontmatter 元数据、统一命名规范、程序友好结构

---

## 快速开始

### 保存知识点

告诉我以下信息即可快速保存：

```
"帮我保存一个 [分类] 的知识点：[简短描述]"
```

**示例**：
- "帮我保存一个前端的知识点：React 性能优化技巧"
- "保存一个算法笔记：快速排序的实现"
- "保存这篇链接内容：https://example.com/article"

我会自动：
1. 创建带元数据的文件
2. 保存并格式化内容
3. 更新索引和标签
4. 创建相关链接

---

## 项目统计

| 分类 | 文件数 | 最后更新 |
|------|--------|----------|
| 前端开发 | 0 | - |
| 后端开发 | 0 | - |
| 数据库 | 0 | - |
| 算法与数据结构 | 0 | - |
| 系统设计 | 0 | - |
| DevOps运维 | 0 | - |
| 计算机基础 | 0 | - |
| AI工具 | 1 | 2026-02-24 |
| 工具与效率 | 0 | - |
| 软技能 | 0 | - |
| 游戏开发 | 0 | - |
| 编程项目 | 4 | 2026-02-24 |
| 其他 | 0 | - |
| **总计** | **5** | 2026-02-24 |

---

## 目录结构

### 📁 前端开发
- HTML/CSS/JavaScript
- 框架 (React, Vue, Next.js 等)
- 状态管理
- 构建工具
- 性能优化

### 📁 后端开发
- 服务端语言 (Node.js, Python, Go 等)
- API 设计
- 微服务架构
- 认证授权
- 后端性能

### 📁 数据库
- 关系型数据库 (MySQL, PostgreSQL)
- NoSQL (MongoDB, Redis)
- 数据库设计
- 查询优化
- ORM

### 📁 算法与数据结构
- 常见算法
- 数据结构
- LeetCode 解题
- 复杂度分析

### 📁 系统设计
- 架构设计
- 分布式系统
- 缓存策略
- 消息队列
- 高可用/高并发

### 📁 DevOps运维
- 容器化 (Docker, Kubernetes)
- CI/CD
- 监控与日志
- 云服务

### 📁 计算机基础
- 操作系统
- 计算机网络
- 数据结构原理
- 编译原理

### 📁 AI工具
- AI 编程助手 (Claude, ChatGPT, Cursor 等)
- AI 代理/Agent (OpenClaw, Custom Agents)
- AI 工作流自动化
- Prompt Engineering
- AI 辅助开发实践

### 📁 工具与效率
- Git 使用
- IDE/编辑器技巧
- 命令行工具
- 自动化脚本（非 AI）

### 📁 软技能
- 沟通协作
- 项目管理
- 学习方法
- 职业规划

### 📁 游戏开发
- 游戏设计想法
- 引擎与工具 (Unity, Unreal, Godot)
- 游戏编程
- 美术资源
- 音效音乐
- 项目管理

### 📁 编程项目
- 项目讨论 💡
- 进行中 🚧
- 已完成 ✅

### 📁 其他
- 暂未分类的知识点

### 📦 box 临时仓库
- 书库 - 原始书籍文件
- 论文 - 学术论文 PDF
- 文章 - 网页文章存档
- 项目 - GitHub 项目源码

> **说明**：box/ 存储原始素材（不上传 Git），拆解后的核心知识点归档到各分类目录

---

## 项目配置

### 系统配置

| 文件 | 说明 |
|------|------|
| [`.knowledge/config.yaml`](.knowledge/config.yaml) | 全局配置，供程序读取知识体系结构 |
| [`.knowledge/METADATA_SPEC.md`](.knowledge/METADATA_SPEC.md) | 元数据规范文档 |
| [`.knowledge/GRAPH_SPEC.md`](.knowledge/GRAPH_SPEC.md) | 知识图谱规范文档 |
| [`.knowledge/OPERATIONS_MANUAL.md`](.knowledge/OPERATIONS_MANUAL.md) | 操作准则 (SOP) |
| [`.knowledge/BOOK_SPEC.md`](.knowledge/BOOK_SPEC.md) | 书籍处理规范 |
| [`.knowledge/GITHUB_SPEC.md`](.knowledge/GITHUB_SPEC.md) | GitHub 项目分析规范 |

### 索引文件

| 文件 | 说明 |
|------|------|
| [`INDEX.md`](INDEX.md) | 全局索引，统计概览和最近更新 |
| [`TAGS.md`](TAGS.md) | 标签字典，按字母索引 |

---

## 使用 Obsidian 可视化

### 1. 安装 Obsidian
下载：https://obsidian.md

### 2. 打开知识体系
1. 打开 Obsidian
2. 点击 "打开文件夹作为仓库"
3. 选择 `e:\文档\code\知识体系` 目录

### 3. 查看知识图谱
按 `Ctrl/Cmd + G` 或点击左侧的 **关系图谱** 图标

### 4. 使用功能
| 功能 | 快捷键 | 说明 |
|------|--------|------|
| 关系图谱 | `Ctrl/Cmd + G` | 查看知识连接可视化 |
| 反向链接 | `Ctrl/Cmd + Shift + E` | 查看哪些文件引用了当前文件 |
| 大纲视图 | `Ctrl/Cmd + Shift + O` | 查看文档大纲 |
| 搜索 | `Ctrl/Cmd + Shift + F` | 全局搜索 |

### 5. 推荐插件
在 `设置 -> 社区插件` 中安装：
- **Graph Analysis** - 更强大的图谱分析
- **Dataview** - 查询和索引数据
- **Excalidraw** - 绘制图表

---

## 使用说明

在日常对话中，告诉我是哪个领域的知识点，我会帮你：
1. 自动归类到对应目录
2. 创建格式化的笔记文件
3. 添加统一的 YAML Frontmatter 元数据
4. 保持内容的结构化和可检索性

---

*创建日期: 2026-02-24*
*最后更新: 2026-02-24*
*下次审核: 2026-03-24*
