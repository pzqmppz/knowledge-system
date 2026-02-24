# 知识体系元数据规范

> 此文档定义了知识体系中所有文件应遵循的元数据格式，确保人机双可读。

---

## 元数据格式

所有 `.md` 文件必须在文件开头使用 **YAML Frontmatter** 格式添加元数据：

```yaml
---
title: "文件标题"
category: "分类名称"
tags: ["标签1", "标签2", "标签3"]
source: "来源链接或描述"
author: "作者（可选）"
date: YYYY-MM-DD
status: "complete|draft|updating|archived"
difficulty: "beginner|intermediate|advanced|expert"
priority: "low|medium|high|critical"
related: ["相关文件1.md", "相关文件2.md"]
---

# 文档正文开始...
```

---

## 字段说明

### 必填字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `title` | string | 文档标题 | `"OpenClaw Agent 配置指南"` |
| `category` | string | 所属分类（需匹配 config.yaml 中的分类） | `"AI工具"` |
| `date` | date | 创建或最后更新日期 | `"2026-02-24"` |

### 可选字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `tags` | array | 标签列表，用于分类和搜索 | `["agent", "whatsapp", "claude"]` |
| `source` | string | 来源链接或描述 | `"https://example.com/article"` |
| `author` | string | 作者 | `"Aman Khan"` |
| `status` | string | 文档状态 | `draft`, `complete`, `updating`, `archived` |
| `difficulty` | string | 难度等级 | `beginner`, `intermediate`, `advanced`, `expert` |
| `priority` | string | 优先级 | `low`, `medium`, `high`, `critical` |
| `related` | array | 相关文档（支持相对路径或文件名） | `["文件1.md", "../分类/文件2.md"]` |

---

## 状态值 (status)

| 值 | 说明 |
|----|------|
| `draft` | 草稿 - 内容尚未完成 |
| `complete` | 完成 - 内容已完善 |
| `updating` | 更新中 - 内容正在修改 |
| `archived` | 已归档 - 内容过时但保留 |

## 难度等级 (difficulty)

| 值 | 说明 |
|----|------|
| `beginner` | 入门 - 基础概念，适合初学者 |
| `intermediate` | 中级 - 需要一定基础 |
| `advanced` | 高级 - 深入内容 |
| `expert` | 专家 - 专业级别 |

## 优先级 (priority)

| 值 | 说明 |
|----|------|
| `low` | 低 - 备查资料 |
| `medium` | 中 - 常用内容 |
| `high` | 高 - 重要内容 |
| `critical` | 紧急 - 核心内容 |

---

## 示例文件

### 完整示例

```yaml
---
title: "OpenClaw Agent 配置指南"
category: "AI工具"
tags: ["agent", "whatsapp", "claude", "openclaw", "automation"]
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
```

### 最小示例

```yaml
---
title: "快速排序算法"
category: "算法与数据结构"
date: 2026-02-24
---

# 快速排序
...
```

---

## 程序读取指南

### 解析步骤

1. 读取文件内容
2. 检测 `---` 分隔符
3. 解析 YAML 格式的元数据
4. 根据元数据进行分类、索引、搜索

### Python 示例

```python
import yaml
import re

def parse_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    return None, content

# 使用
metadata, body = parse_metadata("AI工具/OpenClaw-Agent配置指南.md")
print(metadata['category'])  # 输出: AI工具
print(metadata['tags'])      # 输出: ['agent', 'whatsapp', 'claude', ...]
```

---

## 标签命名建议

### 分类标签
- 按技术：`#javascript`, `#python`, `#docker`
- 按概念：`#algorithm`, `#design-pattern`, `#security`

### 来源标签
- `#article` - 文章
- `#book` - 书籍
- `#paper` - 论文
- `#video` - 视频
- `#practice` - 实践经验
- `#qa` - 问答

### 状态标签
- `#todo` - 待学习
- `#learning` - 学习中
- `#learned` - 已掌握

---

*版本: 1.0*
*最后更新: 2026-02-24*
