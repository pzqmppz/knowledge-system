# Screenshot-to-Code 本地部署结项报告

> **部署日期**: 2026-03-04
> **项目**: screenshot-to-code
> **仓库**: https://github.com/abi/screenshot-to-code

---

## 一、项目概述

### 1.1 项目简介
screenshot-to-code 是一个使用 AI 将截图、设计稿和 Figma 设计转换为代码的工具。

### 1.2 技术栈
| 组件 | 技术 | 端口 |
|-----|------|------|
| 前端 | React + Vite + TypeScript | 5173 |
| 后端 | FastAPI + Python 3.12 | 7001 |
| 容器 | Docker Compose | - |

### 1.3 支持的代码输出
- HTML + Tailwind
- HTML + CSS
- React + Tailwind
- Vue + Tailwind
- Bootstrap
- Ionic + Tailwind
- SVG

---

## 二、部署环境

### 2.1 硬件配置
- **GPU**: NVIDIA 高端配置
- **系统**: Windows 10/11
- **Docker**: Docker Desktop 29.2.1+

### 2.2 部署路径
```
E:\docker-projects\screenshot-to-code\
├── backend/          # 后端代码
├── frontend/         # 前端代码
├── docker-compose.yml
└── .env             # 环境变量配置
```

---

## 三、环境变量配置

### 3.1 .env 文件内容
```bash
# GLM-5 API 配置 (智谱 AI)
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/

# 后端端口 (默认 7001)
BACKEND_PORT=7001
```

### 3.2 环境变量说明
| 变量 | 说明 | 必填 |
|-----|------|------|
| OPENAI_API_KEY | AI 模型 API Key | 是 |
| OPENAI_BASE_URL | API 基础地址 | 智谱 AI 必填 |
| BACKEND_PORT | 后端服务端口 | 否 |
| ANTHROPIC_API_KEY | Claude API Key | 否 |
| GEMINI_API_KEY | Gemini API Key | 否 |

---

## 四、部署命令

### 4.1 初始部署
```bash
# 1. 克隆项目
cd /e/docker-projects
git clone https://github.com/abi/screenshot-to-code.git
cd screenshot-to-code

# 2. 创建 .env 文件
echo "OPENAI_API_KEY=your_key" > .env
echo "OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/" >> .env

# 3. 启动服务
docker-compose up -d --build
```

### 4.2 常用运维命令
```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps

# 重新构建并启动
docker-compose up -d --build
```

---

## 五、自定义修改

### 5.1 智谱 AI GLM 集成

为支持智谱 AI 的 GLM 模型，进行了以下修改：

#### 后端修改
**文件**: `backend/llm.py`
```python
# 添加 GLM 模型枚举
class Llm(Enum):
    GLM_4_6V = "glm-4.6v"  # 智谱 GLM 视觉模型

# 模型提供商映射
MODEL_PROVIDER: dict[Llm, str] = {
    Llm.GLM_4_6V: "glm",
}

# GLM 模型配置
GLM_MODEL_CONFIG: dict[Llm, dict[str, str]] = {
    Llm.GLM_4_6V: {"api_name": "glm-4.6v"},
}
```

**文件**: `backend/agent/providers/glm.py` (新建)
- 创建 GLM Provider，使用 OpenAI 兼容的 Chat Completions API
- 支持流式输出和工具调用

**文件**: `backend/agent/providers/factory.py`
- 添加 GLM 模型的工厂支持

**文件**: `backend/routes/generate_code.py`
- 添加智谱 API 检测逻辑
- 当 `OPENAI_BASE_URL` 包含 "bigmodel" 或 "zhipu" 时，自动使用 GLM 模型

#### 前端修改
**文件**: `frontend/src/lib/models.ts`
```typescript
export enum CodeGenerationModel {
  GLM_4_6V = "glm-4.6v",
}

export const CODE_GENERATION_MODEL_DESCRIPTIONS = {
  "glm-4.6v": {
    name: "GLM-4.6V (Zhipu AI)",
    inBeta: false,
  },
};
```

### 5.2 修改文件清单
| 文件 | 修改类型 | 说明 |
|-----|---------|------|
| backend/llm.py | 修改 | 添加 GLM 模型定义 |
| backend/agent/providers/glm.py | 新建 | GLM Provider 实现 |
| backend/agent/providers/factory.py | 修改 | 添加 GLM 工厂支持 |
| backend/routes/generate_code.py | 修改 | 添加智谱 API 检测 |
| frontend/src/lib/models.ts | 修改 | 添加 GLM 前端模型 |

---

## 六、遇到的问题与解决方案

### 6.1 问题 1: 404 Not Found (/v4/responses)
**错误信息**:
```
Error code: 404 - {'path': '/v4/responses'}
```

**原因**:
- screenshot-to-code 使用 OpenAI 的新 Responses API (`/v4/responses`)
- 智谱 AI 只支持传统的 Chat Completions API (`/chat/completions`)

**解决方案**:
- 创建独立的 GLM Provider，使用 Chat Completions API
- 添加智谱 API 自动检测逻辑

### 6.2 问题 2: 模型选择错误
**原因**:
- 默认模型选择逻辑只识别 OpenAI API，无法区分智谱 API
- 即使配置了智谱 API，仍选择 GPT 模型

**解决方案**:
- 修改 `generate_code.py` 中的模型选择逻辑
- 添加 `openai_base_url` 参数传递
- 检测 URL 包含 "bigmodel" 或 "zhipu" 时使用 GLM 模型

### 6.3 问题 3: 模型名称不匹配
**原因**:
- 初始配置使用 `glm-4v-plus`，但智谱 API 的正确模型名是 `glm-4.6v`

**解决方案**:
- 更新所有相关配置，使用正确的模型名称 `glm-4.6v`

---

## 七、访问与使用

### 7.1 访问地址
- **本地访问**: http://localhost:5173
- **后端 API**: http://localhost:7001

### 7.2 使用流程
1. 打开浏览器访问 http://localhost:5173
2. 上传截图或设计稿
3. 选择技术栈（HTML+Tailwind、React 等）
4. 点击生成，等待 AI 处理
5. 查看生成的代码，可进行微调

### 7.3 API 测试
```bash
# 健康检查
curl http://localhost:7001/

# 详细健康状态
curl http://localhost:7001/health
```

---

## 八、服务验证清单

### 8.1 部署后验证
- [ ] Docker 服务运行正常
- [ ] 前端可以访问 http://localhost:5173
- [ ] 后端健康检查通过
- [ ] .env 配置正确加载
- [ ] 日志显示正确的模型选择
- [ ] 截图生成代码功能正常

### 8.2 日志检查要点
**正常日志应包含**:
```
Using openAiApiKey from environment variable
Using openAiBaseURL from environment variable
Detected Zhipu AI (GLM) API, using GLM models
Variant models:
Variant 1: glm-4.6v
```

---

## 九、故障排查

### 9.1 常见错误
| 错误 | 原因 | 解决方案 |
|-----|------|----------|
| 404 /v4/responses | API 不兼容 | 检查 GLM Provider 是否正确配置 |
| 模型选择为 GPT | API 检测失败 | 确认 OPENAI_BASE_URL 包含 "bigmodel" |
| 连接拒绝 | Docker 未启动 | 启动 Docker Desktop |
| API Key 错误 | Key 无效 | 检查智谱 AI 控制台 |

### 9.2 调试命令
```bash
# 查看后端日志
docker logs screenshot-to-code-backend-1 -f

# 查看前端日志
docker logs screenshot-to-code-frontend-1 -f

# 检查容器环境变量
docker exec screenshot-to-code-backend-1 env | grep OPENAI

# 进入容器调试
docker exec -it screenshot-to-code-backend-1 bash
```

---

## 十、后续优化建议

### 10.1 功能增强
- [ ] 支持更多智谱 AI 模型（如 glm-4-plus、glm-4-flash 等）
- [ ] 添加模型选择 UI，让用户手动选择
- [ ] 支持多模型对比生成

### 10.2 性能优化
- [ ] 添加请求缓存
- [ ] 支持本地模型（Ollama）
- [ ] 优化图片预处理

### 10.3 监控与日志
- [ ] 添加 API 调用统计
- [ ] 实现错误追踪
- [ ] 添加使用量监控

---

## 十一、相关资源

### 11.1 官方文档
- GitHub: https://github.com/abi/screenshot-to-code
- 智谱 AI: https://open.bigmodel.cn/

### 11.2 本地部署框架
- 部署框架文档: `[AI工具/本地模型部署框架.md](E:\文档\code\知识体系\AI工具\本地模型部署框架.md)`

---

**报告生成时间**: 2026-03-04
**部署状态**: ✅ 成功
**维护人员**: Claude Code + User
