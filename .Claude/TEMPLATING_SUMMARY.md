# Coze 工作流开发总结

## 问题与解决方案

### 核心问题

即使有规范文档和成功案例，大模型生成的 JSON 仍然需要多轮修改才能导入成功。

**根本原因**：
1. 规范是描述性的，不是可执行的
2. 隐式规则无法从文档中提取
3. 大模型会"创造"规范之外的结构

### 解决方案：模板化生成器

不依赖大模型"理解"规范，而是使用**代码生成器**直接生成正确结构。

---

## 关键发现

### HTTP 节点 bodyData 结构

这是最容易出错的地方，有两个完全不同的结构：

#### 1. EMPTY bodyType（GET 请求）

```json
{
  "bodyType": "EMPTY",
  "bodyData": {
    "binary": {
      "fileURL": {
        "type": "string",
        "value": {
          "type": "ref",
          "content": {
            "source": "block-output",
            "blockID": "",
            "name": ""
          }
          // ❌ 没有 rawMeta
        }
      }
    }
    // ❌ 没有 content
    // ❌ 没有 json
  }
}
```

#### 2. JSON bodyType（POST 请求）⚠️⚠️⚠️

```json
{
  "bodyType": "JSON",
  "bodyData": {
    "type": "ref",
    "content": {
      "source": "block-output",
      "blockID": "50100000",
      "name": "requestBody"
    },
    "rawMeta": {"type": 1},
    "binary": {
      "fileURL": {
        "type": "string",
        "value": {
          "type": "ref",
          "content": {
            "source": "block-output",
            "blockID": "",
            "name": ""
          },
          "rawMeta": {"type": 1}  // ✅ ⚠️ 必须在 value 对象内部！
        }
      }
    },
    "json": ""
  }
}
```

### 关键差异对照表

| 位置 | EMPTY | JSON |
|------|-------|------|
| `type` | 不需要 | `"ref"` |
| `content` (顶层) | ✅ 必须有 | ✅ 必须有 |
| `rawMeta` (顶层) | ✅ 必须有 | ✅ 必须有 |
| `json` | ✅ 必须有 | ✅ 必须有 |
| `binary.fileURL.value.rawMeta` | ✅ **必须有**（在 value 内） | ✅ **必须有**（在 value 内） |

---

## 使用模板生成器

### 位置

```
.claude/templates/
├── coze-workflow-builder.ts      # 核心生成器
└── example-interview-force-finish.ts  # 使用示例
```

### 使用步骤

1. **复制示例文件**
   ```bash
   cp .claude/templates/example-interview-force-finish.ts my-workflow.ts
   ```

2. **修改参数**
   - API 地址
   - 请求头
   - 代码逻辑

3. **生成工作流**
   ```bash
   npx tsx my-workflow.ts
   ```

### API 速查

```typescript
// 创建代码节点
createCodeNode({
  title: "节点标题",
  inputs: [
    {
      name: "inputName",
      type: "string",
      sourceNodeId: "sourceNodeId",
      sourceOutputName: "outputName"
    }
  ],
  code: "async function main({ params }: Args) { ... }",
  outputs: [{ name: "outputName", type: "string" }]
})

// 创建 HTTP 节点
createHTTPNode({
  title: "HTTP_请求标题",
  method: "POST",
  url: "https://api.example.com/endpoint",
  headers: [{ name: "Authorization", value: "Bearer xxx" }],
  bodyType: "JSON",
  bodySourceNodeId: "sourceNodeId",
  bodySourceOutputName: "outputName"
})

// 创建大模型节点
createLLMNode({
  title: "LLM_处理文本",
  prompt: "你的提示词",
  inputs: [...]
})

// 组装完整工作流
createWorkflow({
  startOutputs: [...],
  endInputs: [...],
  nodes: [node1, node2, node3]
})
```

---

## 验证清单

生成 JSON 后，快速验证：

- [ ] HTTP 节点的 `apiInfo` 只包含 `method` 和 `url`
- [ ] `body`、`headers` 等是 `inputs` 的直接子字段
- [ ] JSON bodyType 时，`binary.fileURL.value.rawMeta` 存在
- [ ] JSON bodyType 时，`content` 字段存在且正确引用源节点
- [ ] 所有节点的 `_temp` 字段完整

---

## 更新记录

| 日期 | 内容 |
|------|------|
| 2026-03-02 | 初始版本，从导入失败中提取规则 |
| 2026-03-02 | 发现 JSON bodyType 需要 `binary.fileURL.value.rawMeta` |
| 2026-03-02 | 创建模板生成器，替代"规范+大模型"模式 |
