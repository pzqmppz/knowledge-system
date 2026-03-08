# Coze 工作流配置指南

> **用途**: Coze 工作流剪贴板格式标准规范
> **适用人员**: 所有需要配置Coze 工作流的开发人员
> **更新时间**: 2026-02-28

---

## 一、剪贴板格式结构

```json
{
  "type": "coze-workflow-clipboard-data",
  "source": {
    "workflowId": "",
    "flowMode": 0,
    "spaceId": "7491691397280874533",
    "isDouyin": false,
    "host": "www.coze.cn"
  },
  "bounds": { "x": -4100, "y": -400, "width": 5000, "height": 600 },
  "json": {
    "nodes": [...],
    "edges": [...]
  }
}
```

---

## 二、`_temp` 字段 ⚠️ 极其重要！

### 2.1 哪些节点需要？

**所有主要节点都必须有**：
- ✅ 开始 (type 1)
- ✅ 结束 (type 2)
- ✅ 大模型 (type 3)
- ✅ 代码 (type 5)
- ✅ HTTP 请求 (type 45)
- ✅ JSON 序列化/反序列化 (type 58/59)

### 2.2 各节点 `_temp` 参数

| 节点类型 | height | mainColor |
|---------|--------|-----------|
| 开始/结束 | 130 | `#5C62FF` |
| HTTP 请求 | 200 | `#3071F2` |
| 大模型 | 200 | `#00D4AA` |
| 代码节点 | 150 | `#00B2B2` |
| JSON 处理 | 120 | `#F2B600` |

### 2.3 完整示例

```json
{
  "id": "100001",
  "type": "1",
  "meta": { "position": { "x": -3400, "y": -200 } },
  "data": {
    "nodeMeta": {
      "title": "开始",
      "description": "工作流的起始节点",
      "icon": "...",
      "mainColor": "#5C62FF"
    },
    "outputs": [
      { "type": "string", "name": "input1", "required": true }
    ],
    "trigger_parameters": []
  },
  "_temp": {
    "bounds": { "x": -3400, "y": -200, "width": 360, "height": 130 },
    "externalData": {
      "icon": "...",
      "description": "工作流的起始节点",
      "title": "开始",
      "mainColor": "#5C62FF"
    }
  }
}
```

> **⚠️ 重要**：`_temp` 中的 `bounds` 位置应与节点的 `meta.position` 一致！

---

## 三、HTTP 请求节点配置 (Type 45) ⚠️⚠️⚠️

> **极其重要**：HTTP 节点格式非常严格，缺少任何字段都会导致导入后点击节点报错！
> 错误信息：`TypeError: (t.doc || "").split is not a function`

### 3.0 完整 HTTP 节点示例（GET 请求）

> ⚠️ **极其重要**：`body`、`headers`、`params`、`auth`、`setting`、`settingOnError` 必须是 `inputs` 的**直接子字段**，而不是嵌套在 `apiInfo` 内部！

```json
{
  "id": "450001",
  "type": "45",
  "meta": { "position": { "x": -2400, "y": -200 } },
  "data": {
    "nodeMeta": {
      "description": "发送 HTTP 请求获取数据",
      "icon": "https://lf3-static.bytednsdoc.com/obj/eden-cn/dvsmryvd_avi_dvsm/ljhwZthlaukjlkulzlp/icon/icon-HTTP.png",
      "mainColor": "#3071F2",
      "subTitle": "HTTP 请求",
      "title": "HTTP_查询岗位列表"
    },
    "inputParameters": [],
    "inputs": {
      "apiInfo": {
        "method": "GET",
        "url": "http://111.231.51.9/api/open/jobs"
      },
      "body": {
        "bodyType": "EMPTY",
        "bodyData": {
          "binary": {
            "fileURL": {
              "type": "string",
              "value": {
                "type": "ref",
                "content": { "source": "block-output", "blockID": "", "name": "" }
              }
            }
          }
        }
      },
      "headers": [
        {
          "name": "X-API-Key",
          "input": {
            "type": "string",
            "value": {
              "type": "literal",
              "content": "wehan_open_api_key_2026",
              "rawMeta": { "type": 1 }
            }
          }
        }
      ],
      "params": [],
      "auth": {
        "authType": "BEARER_AUTH",
        "authData": { "customData": { "addTo": "header" } },
        "authOpen": false
      },
      "setting": { "timeout": 60, "retryTimes": 2 },
      "settingOnError": {}
    },
    "outputs": [
      { "type": "string", "name": "body" },
      { "type": "integer", "name": "statusCode" },
      { "type": "string", "name": "headers" }
    ]
  },
  "_temp": {
    "bounds": { "x": -2600, "y": -200, "width": 360, "height": 200 },
    "externalData": {
      "icon": "https://lf3-static.bytednsdoc.com/obj/eden-cn/dvsmryvd_avi_dvsm/ljhwZthlaukjlkulzlp/icon/icon-HTTP.png",
      "description": "发送 HTTP 请求获取数据",
      "title": "HTTP_查询岗位列表",
      "mainColor": "#3071F2"
    }
  }
}
```

### 3.0.1 inputs 结构 ⚠️⚠️⚠️ 最常见的错误！

**正确结构**（headers 保留）：
```json
"inputs": {
  "apiInfo": {
    "method": "GET",
    "url": "http://..."
  },
  "body": {...},
  "headers": [...],      // ✅ inputs 的直接子字段
  "params": [],
  "auth": {...},
  "setting": {...},
  "settingOnError": {}
}
```

**错误结构**（headers 丢失）：
```json
"inputs": {
  "apiInfo": {
    "method": "GET",
    "url": "http://...",
    "body": {...},
    "headers": [...],    // ❌ 嵌套在 apiInfo 内部，导入后会丢失！
    "params": [],
    "auth": {...},
    "setting": {...},
    "settingOnError": {}
  }
}
```

### 3.1 必须存在的字段清单 ⚠️

| 字段路径 | 说明 | 常见错误 |
|---------|------|---------|
| `inputs.apiInfo` | **只包含 method 和 url** | ❌ 将其他字段嵌套在 apiInfo 内部 |
| `inputs.body` | 请求体配置 | ❌ 嵌套在 apiInfo 内部 |
| `inputs.headers` | 请求头配置 | ❌ 嵌套在 apiInfo 内部（**会丢失**） |
| `inputs.params` | URL 参数 | ❌ 嵌套在 apiInfo 内部 |
| `inputs.auth` | 认证配置 | ❌ 嵌套在 apiInfo 内部 |
| `inputs.setting` | 超时重试配置 | ❌ 嵌套在 apiInfo 内部 |
| `inputs.settingOnError` | 错误处理配置 | ❌ 嵌套在 apiInfo 内部 |
| `url` | **直接字符串**，不是对象 | ❌ `{"type": "literal", "content": "..."}` |
| `bodyData.binary` | 文件上传占位 | ❌ 缺失 |
| `bodyData.content` | **必须存在**，可为空对象 | ❌ 缺失（导致 split 报错）|
| `bodyData.json` | **必须存在**，可为空字符串 | ❌ 缺失 |
| `bodyData.rawMeta` | **必须存在** | ❌ 缺失 |
| `outputs[].type` | **body 是 string 不是 object** | ❌ `"type": "object"` |

### 3.2 bodyData 完整结构（GET 请求）

```json
"bodyData": {
  "binary": {
    "fileURL": {
      "type": "string",
      "value": {
        "type": "ref",
        "content": { "source": "block-output", "blockID": "", "name": "" },
        "rawMeta": { "type": 1 }
      }
    }
  },
  "content": { "source": "block-output", "blockID": "", "name": "" },
  "json": "",
  "rawMeta": { "type": 1 }
}
```

> ⚠️ **极其重要**：`binary`、`content`、`json`、`rawMeta` 四个字段**必须同时存在**！
> 缺少任何一个都会导致：`TypeError: (t.doc || "").split is not a function`

### 3.3 outputs 格式 ⚠️

```json
"outputs": [
  { "type": "string", "name": "body" },
  { "type": "integer", "name": "statusCode" },
  { "type": "string", "name": "headers" }
]
```

> **注意**：`body` 的类型是 `string`，不是 `object`！
> 后续代码节点需要 `JSON.parse(body)` 来解析

### 3.4 Headers 格式

```json
"headers": [
  {
    "name": "X-API-Key",
    "input": {
      "type": "string",
      "value": {
        "type": "literal",
        "content": "wehan_open_api_key_2026",
        "rawMeta": { "type": 1 }
      }
    }
  }
]
```

### 3.5 POST 请求 bodyData

```json
"body": {
  "bodyType": "JSON",
  "bodyData": {
    "type": "ref",
    "content": { "source": "block-output", "blockID": "500002", "name": "requestBodyJson" },
    "rawMeta": { "type": 1 },
    "binary": {
      "fileURL": {
        "type": "string",
        "value": {
          "type": "ref",
          "content": { "source": "block-output", "blockID": "", "name": "" },
          "rawMeta": { "type": 1 }
        }
      }
    },
    "json": "{\n  \"userId\": \"...\"\n}"
  }
}
```

---

## 四、变量引用格式

### 4.1 引用节点输出

```json
{
  "type": "ref",
  "content": {
    "source": "block-output",
    "blockID": "节点ID",
    "name": "字段名"
  },
  "rawMeta": { "type": 1 }
}
```

### 4.2 字面量

```json
{
  "type": "literal",
  "content": "固定值",
  "rawMeta": { "type": 1 }
}
```

### 4.3 rawMeta 类型值

| rawMeta.type | 数据类型 |
|-------------|---------|
| 1 | string |
| 2 | integer |
| 3 | float |
| 4 | boolean |

---

## 五、边 (Edges) 结构

```json
{
  "edges": [
    { "sourceNodeID": "100001", "targetNodeID": "450001" },
    { "sourceNodeID": "450001", "targetNodeID": "590001" }
  ]
}
```

---

## 六、常见问题排查 ⭐

### 6.1 导入后节点丢失

| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| 只有部分节点显示 | 缺少 `_temp` | 为所有节点添加 `_temp` 字段 |

### 6.2 HTTP 节点问题 ⚠️⚠️⚠️

| 问题 | 错误信息 | 原因 | 解决方案 |
|-----|---------|------|---------|
| **请求头丢失** ⚠️ | `"headers": []` | **inputs 结构错误**：headers 嵌套在 apiInfo 内部 | **headers 必须是 inputs 直接子字段** |
| **点击节点报错** | `TypeError: (t.doc \|\| "").split is not a function` | bodyData 缺少 `content` 或 `rawMeta` | 添加完整 bodyData 结构 |
| 请求头格式错误 | - | 旧格式 `{"key": ..., "value": ...}` | 改用 `{"name": ..., "input": ...}` |
| 请求体显示为空 | - | bodyData 缺少 `binary` 或 `json` | 必须同时包含四个字段 |
| 403 Forbidden | - | API Key 不匹配 | 检查 `X-API-Key` 是否正确 |
| url 解析失败 | - | url 使用了对象格式 | 改为直接字符串 `"url": "http://..."` |
| outputs 类型错误 | - | body 使用了 object 类型 | 改为 string，代码中 JSON.parse |

---

## 七、测试数据

### 测试岗位 ID

```bash
# 前端开发工程师
job_id: cmm5o5b8q000ezguj2h8ofvyj

# 后端开发工程师
job_id: cmm5o5b8q000fzguje6mp40ro

# AI算法工程师
job_id: cmm5o5b8r000gzguj0kl94ol3
```

### 测试用户 ID

```bash
# C端虚拟用户
user_id: test_user_c_001
```

### API Key 配置

| 环境 | API Key |
|-----|---------|
| 本地开发 | `wehan_dev_test_2026` |
| 生产环境 | `wehan_open_api_key_2026` |

---

## 八、版本更新记录

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| v8.0 | 2026-03-02 | **极其重要**：发现 inputs 结构问题！`body`/`headers`/`params`/`auth`/`setting` 必须是 inputs 直接子字段，不能嵌套在 apiInfo 内部！新增案例 6 |
| v7.0 | 2026-03-02 | 发现 apiInfo 字段顺序问题，`body` 必须在 `headers` 之前 |
| v6.0 | 2026-03-02 | 补充 HTTP 节点完整格式，添加 `content`/`rawMeta`/`auth`/`setting` 必填字段说明 |
| v3.2 | 2026-02-28 | 添加选择器说明、扩展常见错误分类 |
| v3.1 | 2026-02-28 | 修正插件/循环/批处理节点配置 |
| v3.0 | 2026-02-28 | 添加完整节点 ID 命名规范 |
| v2.0 | 2026-02-28 | 添加会话管理、消息管理节点 |
| v1.0 | 2026-02-28 | 初始版本 |

---

## 九、常见修复案例

### 案例 1：导入后只有部分节点显示

**问题**：只有代码节点显示，其他节点全部丢失

**原因**：缺少 `_temp` 字段

**解决方案**：为所有节点添加 `_temp` 字段

### 案例 2：HTTP 请求头丢失

**问题**：导入后请求头配置丢失

**原因**：使用旧格式 `{"key": ..., "value": ...}`

**解决方案**：改用 `{"name": ..., "input": {...}}`

### 案例 3：HTTP 请求体显示为空

**问题**：bodyData 在 Coze UI 中显示为空

**原因**：缺少 `binary` 或 `json` 字段

**解决方案**：同时添加 `binary` 和 `json` 字段

### 案例 4：点击 HTTP 节点报错 ⚠️ 最常见！

**问题**：导入成功，但点击 HTTP 节点时报错
```
TypeError: (t.doc || "").split is not a function
```

**原因**：bodyData 结构不完整，缺少以下字段之一：
- `content`
- `rawMeta`

**错误示例**：
```json
"bodyData": {
  "binary": {...},
  "json": ""
}
```

**正确示例**：
```json
"bodyData": {
  "binary": {
    "fileURL": {
      "type": "string",
      "value": {
        "type": "ref",
        "content": { "source": "block-output", "blockID": "", "name": "" },
        "rawMeta": { "type": 1 }
      }
    }
  },
  "content": { "source": "block-output", "blockID": "", "name": "" },
  "json": "",
  "rawMeta": { "type": 1 }
}
```

**解决方案**：确保 bodyData 包含完整的 4 个字段：`binary`、`content`、`json`、`rawMeta`

### 案例 5：HTTP 节点 outputs 类型错误

**问题**：代码节点接收到的 body 是字符串，导致直接访问属性报错

**原因**：outputs 中 body 类型写成了 object

**错误示例**：
```json
"outputs": [
  { "type": "object", "name": "body", "schema": [] }
]
```

**正确示例**：
```json
"outputs": [
  { "type": "string", "name": "body" }
]
```

**代码节点处理**：
```javascript
// body 是字符串，需要先 parse
const responseBody = JSON.parse(params.responseBody);
const data = responseBody.data;
```

### 案例 6：HTTP 请求头丢失（inputs 结构错误）⚠️⚠️⚠️ 最常见！

**问题**：导入后 HTTP 节点的 headers 变成空数组 `[]`

**原因**：`inputs` 结构错误，将 `headers`、`body`、`auth` 等字段嵌套在 `apiInfo` 内部

**错误示例**：
```json
"inputs": {
  "apiInfo": {
    "method": "GET",
    "url": "http://...",
    "headers": [...],    // ❌ 嵌套在 apiInfo 内部
    "body": {...},
    "auth": {...},
    ...
  }
}
```

**正确示例**：
```json
"inputs": {
  "apiInfo": {
    "method": "GET",
    "url": "http://..."
    // ✅ apiInfo 只包含 method 和 url
  },
  "headers": [...],      // ✅ inputs 的直接子字段
  "body": {...},
  "params": [],
  "auth": {...},
  "setting": {...},
  "settingOnError": {}
}
```

**解决方案**：
1. `apiInfo` 只包含 `method` 和 `url` 两个字段
2. `body`、`headers`、`params`、`auth`、`setting`、`settingOnError` 必须是 `inputs` 的**直接子字段**

---

*文档版本: 8.0 | 更新时间: 2026-03-02*
