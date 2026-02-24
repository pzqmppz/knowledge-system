---
title: "知识图谱规范"
category: "system"
tags: ["knowledge-graph", "relationships", "specification"]
date: 2026-02-24
status: "complete"
---

# 知识图谱规范

> 本文档定义知识体系中的关系链接和图谱可视化规范

---

## 双向链接语法

### 基本语法

使用 Obsidian 风格的双向链接（兼容标准 Markdown 扩展）：

```markdown
# 链接到其他文件
查看 [[OpenClaw-Agent配置指南]] 了解更多

# 带别名的链接
参见 [[OpenClaw-Agent配置指南|OpenClaw 教程]]

# 链接到标题
[[文件名#章节标题]]

# 链接到其他分类的文件
[[../后端开发/API设计指南]]
```

### 嵌入语法

```markdown
# 嵌入整个文件
![[OpenClaw-Agent配置指南]]

# 嵌入特定章节
![[OpenClaw-Agent配置指南##安全配置]]

# 嵌入代码块
![[OpenClaw-Agent配置指南##一键配置提示词]]
```

---

## 关系类型定义

### 1. 前置知识 (prerequisite)

```markdown
**前置知识**：[[JavaScript基础]]、[[异步编程概念]]
```

表示理解当前内容需要先掌握的知识。

### 2. 相关内容 (related)

```markdown
**相关内容**：[[React状态管理]]、[[Vue响应式原理]]
```

表示主题相关、可以对比学习的内容。

### 3. 实践应用 (applies-to)

```markdown
**应用场景**：[[电商项目实战]]、[[博客系统开发]]
```

表示理论知识在实际项目中的应用。

### 4. 扩展阅读 (extends)

```markdown
**深入阅读**：[[分布式系统设计模式]]、[[微服务架构最佳实践]]
```

表示更深入或更高级的内容。

### 5. 问题解决 (solves)

```markdown
**解决问题**：[[如何解决API跨域问题]]、[[性能优化实战]]
```

表示内容解决的问题或场景。

---

## 元数据中的关系

使用 `related` 字段定义强关联关系：

```yaml
---
related:
  - "前端开发/React状态管理.md"
  - "后端开发/API设计指南.md"
  - "系统设计/缓存策略.md"
---
```

---

## 标签关系系统

### 层级标签

使用 `/` 表示层级关系：

```
#ai/agent           → AI 领域下的 Agent
#ai/prompt          → AI 领域下的 Prompt
#frontend/react     → 前端下的 React
#backend/api        → 后端下的 API
```

### 属性标签

使用 `:` 表示属性：

```
#status:learning    → 正在学习中
#status:learned     → 已掌握
#priority:high      → 高优先级
#source:article     → 来源：文章
```

---

## 反向链接索引

在每个文件末尾维护反向链接区域：

```markdown
---

## 🔗 反向链接

### 被引用
- [[API设计指南]] - 在 RESTful 设计章节中引用
- [[性能优化实战]] - 在缓存策略章节中引用

### 相关讨论
- [[如何选择合适的数据库]] - 相关讨论
```

---

## Obsidian 兼容性

### 推荐插件

| 插件 | 用途 |
|------|------|
| Graph Analysis | 可视化知识图谱 |
| Dataview | 查询和索引数据 |
| Breadcrumbs | 层级关系可视化 |
| Excalidraw | 绘制图表和概念图 |

### 本地配置

在项目根目录创建 `.obsidian/config`：

```json
{
  "pluginsEnabled": [
    "graph",
    "dataview",
    "backlinks"
  ],
  "graph": {
    "localForce": 300,
    "repelForce": 300
  }
}
```

---

## 程序解析关系

### 解析链接

```python
import re

def extract_links(content):
    """提取所有双向链接"""
    # [[链接]]
    pattern = r'\[\[([^\]]+)\]\]'
    links = re.findall(pattern, content)
    return links

def parse_link(link):
    """解析链接"""
    if '|' in link:
        target, alias = link.split('|', 1)
    else:
        target, alias = link, link
    if '#' in target:
        file, anchor = target.split('#', 1)
    else:
        file, anchor = target, None
    return {
        'file': file.strip(),
        'alias': alias.strip(),
        'anchor': anchor
    }
```

### 构建图谱

```python
import networkx as nx

def build_graph(files):
    """构建知识图谱"""
    G = nx.DiGraph()

    for file_path, content in files.items():
        # 添加节点
        G.add_node(file_path, metadata=parse_metadata(content))

        # 添加边
        for link in extract_links(content):
            target = resolve_link(link, file_path)
            if target:
                G.add_edge(file_path, target, type='link')

    return G
```

---

## 图谱可视化建议

### 节点样式

| 节点类型 | 颜色 | 形状 |
|----------|------|------|
| 核心概念 | 红色 | 圆形 |
| 基础知识 | 蓝色 | 方形 |
| 实践应用 | 绿色 | 菱形 |
| 工具/资源 | 灰色 | 三角形 |

### 边样式

| 关系类型 | 样式 | 箭头 |
|----------|------|------|
| 前置知识 | 虚线 | 空心 |
| 相关内容 | 实线 | 无 |
| 应用场景 | 点线 | 实心 |
| 扩展阅读 | 双线 | 空心 |

---

*版本: 1.0*
*最后更新: 2026-02-24*
