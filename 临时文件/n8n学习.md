### n8n 系统学习资料推荐

n8n 是一个开源的工作流自动化工具，适合构建复杂的自动化任务。下面我为你整理了一个系统的学习路径，从基础到进阶。你可以从官方文档和教程入手，这些资源是结构化的，结合视频和实践案例，能帮助你逐步掌握。考虑到你在中国的位置，我优先推荐了有中文支持的资源，以避免语言障碍和访问问题（n8n 官网可能需要科学上网）。

#### 1. **基础入门（适合零基础用户）**
   - **官方学习路径**：n8n 官方提供了一个结构化的学习路径，包括教程、课程和逐步指南。从安装开始，逐步覆盖核心概念如节点、工作流和数据处理。建议从这里起步，花1-2周时间跟随练习。
   - **初级课程（Level One）**：聚焦于 n8n 的界面导航、数据结构、表达式和数据转换。适合新手，包含文本和视频形式。
   - **快速上手教程视频**：YouTube 上有官方的 "n8n Quick Start Tutorial: Build Your First Workflow"，时长约20分钟，教你构建第一个工作流，包括触发器、动作和数据处理。

#### 2. **进阶学习（构建复杂工作流）**
   - **视频课程系列**：n8n 的 YouTube 频道有初级和高级课程播放列表。初级覆盖基础，高级涉及复杂节点、企业功能和 AI 集成。
   - **零到英雄完整课程**：一个6小时+的 YouTube 教程，从节点和架构基础到部署高级系统，包含真实案例。
   - **n8n Learning Hub**：一个 curated 资源中心，包含教程、模板和社区见解，适合探索独特用例。
   - **社区资源**：Reddit 的 r/n8n 子版块有用户分享的最佳免费资源，包括指南、速成课程和整合案例。

#### 3. **中文学习资源（更适合中国用户）**
   - **n8n 中文教程社区**：一个专为中文用户设计的网站，提供从安装部署到制作第一个工作流的完整指南，包括 Telegram 机器人和深度研究案例。内容以低代码实践为主，面向非程序员。
   - **GitHub 中文教程手册**：eleven-h/n8n 项目，提供高质量的中文教程和实战手册。覆盖核心概念、环境部署、节点详解、调试和进阶技巧，附带案例和截图。适合系统学习，按4周路线规划。
   - **视频教程系列**：Bilibili 或 YouTube 上有 "學會n8n 為你省下80% 時間！" 系列，EP.1 教你构建 AI 助理工作流，包括 Google 日历整合和 RSS 处理。简单易懂，适合初学者。
   - **手把手完整教学**："n8n 手把手完整教學" YouTube 视频，从基础到进阶，涵盖 AI workflow 和 Agent 应用，包括 Schema、JSON 和 Expression 编写。
   - **本地部署和汉化教程**：Zhihu 上有 "5分钟搞定！n8n 本地部署+ 汉化教程"，教你用 Docker 安装并汉化界面。 另外，Cnblogs 有 "1分钟安装N8N-2.0中文版"，包括解除组件限制。
   - **实战案例视频**："最强开源AI工作流n8n" YouTube 教程，包含本地部署和5个实战案例，GitHub 上有工作流下载。

学习建议：先用本地部署（Docker 或自托管）避免网络问题，然后从中文社区起步，结合官方英文资源深化。n8n 有活跃的社区（如 GitHub 和论坛），可以分享工作流求反馈。

### 更适合中国本地化的产品和教程

n8n 是德国开源产品，不是中国本土的，在中国使用可能需翻墙访问部分集成（如 Google 服务）。 如果你寻求更本地化的选项（支持国内云服务、合规性强、无需翻墙），以下是推荐的替代品。这些工具类似 n8n，支持工作流自动化，但更易在中国部署和集成本土服务（如阿里云、腾讯云、微信等）。我优先选择了开源或有中文支持的：

#### 推荐本地化替代产品
| 产品名称 | 描述 | 为什么适合中国 | 学习教程推荐 |
|----------|------|---------------|-------------|
| **Node-RED** | 开源可视化编程工具，由 IBM 开发，用于 IoT 和自动化工作流。支持自托管，节点丰富。 | 完全开源，无需翻墙；有大量中文社区支持；易集成国内 API 如阿里云函数。 | - 官方文档（有中文翻译）：node-red.org/docs<br>- Bilibili 教程："Node-RED 入门教程" 系列，简单拖拽构建工作流。 |
| **Activepieces** | 开源自动化平台，类似 n8n，但更注重无代码界面和 AI 集成。 | 自托管友好；支持国内部署；社区活跃，有中文用户分享。 | - GitHub 仓库：activepieces/activepieces<br>- 中文教程：Zhihu 或 CSDN 上搜索 "Activepieces 中文教程"，包含入门和案例。 |
| **Flowise** | 开源 AI 工作流工具，专注于 LLM 和 Agent 构建。 | 轻量级，自托管；易与中国 AI 服务（如百度文心一言）集成。 | - 官方：flowiseai.com<br>- YouTube/Bilibili："Flowise AI 教程"，从安装到构建 Agent。 |
| **阿里云函数计算 (FC)** | 阿里云的 Serverless 平台，支持工作流自动化。 | 中国本土产品，高速稳定；集成阿里生态（如 OSS、API Gateway）；无需翻墙。 | - 官方文档：aliyun.com/product/fc（全中文）<br>- 教程：阿里云大学课程 "函数计算入门"，免费视频。 |
| **腾讯云自动化工具 (SCF + API Gateway)** | 腾讯的 Serverless 函数服务，支持触发器和工作流。 | 国内优化；集成微信、QQ 等；合规性强。 | - 官方：cloud.tencent.com/product/scf（中文）<br>- 教程：腾讯云社区 "Serverless 工作流教程"。 |

#### 为什么这些更本地化？
- **网络与合规**：n8n 可能依赖国际服务，而这些替代支持国内镜像或云部署，避免访问限制。
- **社区支持**：Node-RED 和 Activepieces 有中文 GitHub 叉和教程，易上手。
- **成本**：开源选项免费，自托管；云产品如阿里/腾讯有免费额度。

如果你坚持用 n8n，推荐自托管版本，并用中文汉化教程。如果需要特定场景（如 AI 集成），告诉我，我可以帮你细化资源。


工作流案例：
https://github.com/Zie619/n8n-workflows

扫描你的项目，发现所有隐藏的 AI 组件：
https://github.com/Trusera/ai-bom
AI-BOM 是什么
AI Bill of Materials（AI 物料清单） —— 扫描你的项目，发现所有隐藏的 AI 组件

一条命令，自动发现项目中的 AI Agent、模型、API、密钥等

核心功能
扫描目标	能发现什么
LLM SDK	OpenAI、Anthropic、Google AI、Mistral、Ollama 等
Agent 框架	LangChain、CrewAI、AutoGen、LlamaIndex 等
模型引用	gpt-4o、claude-3-5-sonnet、gemini-1.5-pro 等
API Keys	sk-、sk-ant-、hf_* 等硬编码密钥
n8n 工作流	AI Agent 节点、MCP 客户端、Webhook 触发器等
MCP Servers	Model Context Protocol 配置
模型文件	.gguf、.safetensors、.onnx、.pt 等
🔥 对你特别有用的功能
n8n 工作流扫描

# 扫描 n8n 工作流 JSON 文件
ai-bom scan ./workflows/

# 扫描本地 n8n 实例
ai-bom scan . --n8n-local

# 扫描运行中的 n8n（通过 API）
ai-bom scan . --n8n-url http://localhost:5678 --n8n-api-key YOUR_KEY
能检测出：

AI Agent 节点
MCP 客户端连接
无认证的 Webhook 触发器
危险的工具组合
工作流中硬编码的凭证
n8n Community Node
它还提供了一个 n8n 社区节点，可以直接在 n8n 里扫描所有工作流：


Settings → Community Nodes → 搜索 n8n-nodes-trusera
快速上手

# 安装
pipx install ai-bom

# 扫描当前项目
ai-bom scan .

# 输出 CycloneDX SBOM（合规报告）
ai-bom scan . -f cyclonedx -o ai-bom.cdx.json

# 生成 HTML 报告
ai-bom scan . -f html -o report.html