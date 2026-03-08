---
title: "本地 AI 模型部署指南"
category: "AI工具"
tags: ["Docker", "CUDA", "vLLM", "模型部署", "本地部署", "GPU", "容器化"]
source: "日常对话整理"
date: 2026-02-25
status: "complete"
difficulty: "intermediate"
priority: "high"
related: ["../DevOps运维/Docker入门.md"]
---

# Qwen3-ASR 部署指南

> 阿里 Qwen3 语音识别模型本地部署
>
> 最后更新：2026-02-25

---

## 快速调用

### 服务信息

| 项目 | 配置 |
|------|------|
| 服务端口 | **8001** |
| Gradio UI | http://localhost:8001/ui |
| API 文档 | http://localhost:8001/docs |
| 健康检查 | http://localhost:8001/health |

### API 调用示例

**curl 调用**：
```bash
curl -X POST "http://localhost:8001/api/transcribe" \
  -F "file=@audio.mp3" \
  -F "language=zh"
```

**Python 调用**：
```python
import requests

url = "http://localhost:8001/api/transcribe"

with open("audio.mp3", "rb") as f:
    response = requests.post(
        url,
        files={"file": f},
        data={"language": "zh"}
    )

result = response.json()
print(result["text"])  # 转录文本
```

### 返回格式

```json
{
  "text": "完整的转录文本",
  "segments": [
    {"start": 0.0, "end": 2.5, "text": "第一句话"},
    {"start": 2.5, "end": 5.0, "text": "第二句话"}
  ]
}
```

---

## 一、技术栈层次关系

从下到上的依赖关系：

```
┌─────────────────────────────────────────────────────────────────┐
│                        你的电脑/服务器                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Docker (容器平台)                       │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │              vLLM (推理引擎框架)                      │  │  │
│  │  │   高性能推理、显存管理、并发处理                        │  │  │
│  │  │  ┌────────────────────────────────────────────────┐  │  │  │
│  │  │  │         AI 模型 (Qwen3-ASR/TTS 等)              │  │  │  │
│  │  │  │   模型权重 + tokenizer + 配置文件                │  │  │  │
│  │  │  └────────────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              CUDA + NVIDIA 驱动 (GPU 基础)                 │  │
│  │           让程序能够使用显卡进行计算                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    NVIDIA 显卡硬件                         │  │
│  │                  (RTX 3060/4070/4090 等)                   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. 组件比喻理解

| 组件 | 比喻 | 作用 |
|------|------|------|
| [[Docker]] | 集装箱/虚拟房间 | 提供独立环境，不管你电脑装什么，容器里都有自己的操作系统和软件 |
| [[CUDA]] | 显卡驱动 + 工具箱 | 让程序能和显卡说话，指挥显卡干活 |
| vLLM | 高性能发动机 | 专门优化的大模型推理引擎，让模型跑得快、省显存 |
| 模型权重 | 大脑知识 | 具体的 AI 模型，包含训练好的参数 |

## 3. 数据处理流程

```
用户上传音频/文本
       ↓
   [浏览器]
       ↓
HTTP 请求 → localhost:8000
       ↓
┌──────────────────────────────────────────────┐
│  Docker 容器                                  │
│  ┌────────────────────────────────────────┐  │
│  │ vLLM 推理引擎                           │  │
│  │  1. 接收输入                            │  │
│  │  2. 预处理                              │  │
│  │  3. 调用模型                            │  │
│  └──────────┬─────────────────────────────┘  │
│             ↓                                 │
│  ┌────────────────────────────────────────┐  │
│  │ AI 模型                                 │  │
│  │  1. 加载模型权重到 GPU 显存             │  │
│  │  2. CUDA 执行矩阵运算                   │  │
│  │  3. 输出结果                            │  │
│  └────────────────────────────────────────┘  │
└──────────────┬───────────────────────────────┘
               ↓
         [NVIDIA 显卡]
         执行并行计算
               ↓
          返回结果
               ↓
         [浏览器显示]
```

## 4. 多模型部署复用层级

部署多个 AI 模型时，哪些可以复用，哪些需要独立：

```
┌─────────────────────────────────────────────────────────────────────┐
│                     主机层面（完全复用）                              │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  ✅ NVIDIA 显卡硬件          ← 一次购买，永久使用               │  │
│  │  ✅ NVIDIA 驱动              ← 装一次就行                      │  │
│  │  ✅ CUDA Toolkit             ← 完全复用                        │  │
│  │  ✅ Docker                   ← 一个守护进程管理多容器           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────┐   ┌─────────────────────────┐        │
│  │  🔄 容器1: ASR 服务      │   │  🔄 容器2: TTS 服务      │        │
│  │  ├─ vLLM/推理引擎        │   │  ├─ vLLM/推理引擎        │        │
│  │  ├─ 模型权重             │   │  ├─ 模型权重             │        │
│  │  └─ 端口: 8000          │   │  └─ 端口: 8001          │        │
│  └─────────────────────────┘   └─────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
```

| 层级 | 组件 | 是否复用 | 说明 |
|------|------|----------|------|
| 硬件 | NVIDIA 显卡 | ✅ 完全复用 | 一张卡跑多个模型 |
| 驱动 | NVIDIA Driver | ✅ 完全复用 | 主机装一次 |
| 运行时 | CUDA Toolkit | ✅ 完全复用 | 主机层面 |
| 平台 | [[Docker]] | ✅ 完全复用 | 一个守护进程管理多容器 |
| 容器 | Docker 容器 | ❌ 每个模型独立 | 隔离环境 |
| 引擎 | vLLM/推理框架 | ❌ 通常独立 | 每个容器里一份 |
| 模型 | 权重文件 | ❌ 每个模型独立 | 不同模型不同权重 |

## 5. 推荐的本地目录结构

```
E:\ai-deploy\                          # AI 部署专用根目录
│
├── models\                            # 所有模型权重（最占空间）
│   ├── qwen3-asr\                     # ASR 模型
│   │   ├── config.json
│   │   ├── model.safetensors
│   │   └── tokenizer.json
│   ├── qwen3-tts\                     # TTS 模型
│   │   └── ...
│   └── whisper-large\                 # 其他模型
│       └── ...
│
├── containers\                        # Docker 配置
│   ├── docker-compose.yml             # 编排文件
│   ├── asr\
│   │   ├── Dockerfile
│   │   └── config.yaml
│   └── tts\
│       ├── Dockerfile
│       └── config.yaml
│
├── scripts\                           # 启动脚本
│   ├── start-asr.sh
│   ├── start-tts.sh
│   └── stop-all.sh
│
├── data\                              # 输入输出数据
│   ├── input\                         # 待处理文件
│   └── output\                        # 处理结果
│
├── cache\                             # 缓存（可随时删除）
│   └── huggingface\
│
└── logs\                              # 日志
    ├── asr.log
    └── tts.log
```

### Docker 数据位置

```
E:\Docker\                             # Docker WSL 数据
└── DockerDesktopWSL\
    ├── disk\docker_data.vhdx          # 镜像、容器数据
    └── main\ext4.vhdx                 # 系统数据
```

### 目录设计原则

| 原则 | 说明 |
|------|------|
| **模型集中存放** | `models/` 单独管理，方便备份和复用 |
| **容器挂载模型** | [[Docker]] 用 `-v` 挂载，不把模型打包进镜像 |
| **数据分离** | 输入输出文件不混在模型目录里 |
| **缓存可删** | `cache/` 随时可清，不影响运行 |

## 6. 常见问题与解决方案

### 镜像只有空壳

**问题**：拉取的官方镜像（如 `qwenllm/qwen3-asr:latest`）只有 [[CUDA]] 基础环境，没有 vLLM 和模型文件。

```
你拉取的镜像:
┌──────────────────┐
│   Docker 容器     │
│  ┌────────────┐  │
│  │  CUDA 环境  │  ❌ 没有 vLLM
│  │  (空壳子)   │  ❌ 没有模型文件
│  └────────────┘  │
└──────────────────┘
```

**解决方案**：

| 方案 | 说明 | 复杂度 |
|------|------|--------|
| A | 找包含一切的完整镜像 | ⭐ 简单 |
| B | 用 vLLM 镜像 + 自动下载模型 | ⭐⭐ 中等 |
| C | 自己构建完整镜像 | ⭐⭐⭐ 复杂 |

### Docker 数据迁移

**Windows Docker Desktop 数据迁移步骤**：

1. 关闭 Docker Desktop
2. 复制数据到新位置
3. 重命名原目录为备份
4. 创建目录连接（Junction）：
   ```powershell
   New-Item -ItemType Junction -Path 'C:\Users\...\Docker\wsl' -Target 'E:\Docker\DockerDesktopWSL'
   ```
5. 启动 Docker Desktop 验证
6. 删除备份目录

## 7. Docker 挂载示例

```yaml
# docker-compose.yml
services:
  asr:
    image: vllm/vllm-openai:latest
    ports:
      - "8000:8000"
    volumes:
      - ../models:/models           # 挂载模型目录
      - ../data:/data               # 挂载数据目录
    environment:
      - MODEL_PATH=/models/qwen3-asr
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

```bash
# 命令行启动示例
# ASR 容器
docker run --gpus all -p 8000:8000 vllm/vllm-openai:latest \
  --model Qwen/Qwen3-ASR

# TTS 容器（新增，不同端口）
docker run --gpus all -p 8001:8000 vllm/vllm-openai:latest \
  --model Qwen/Qwen3-TTS
```

## 8. 相关资源

### 外部链接
- [vLLM 官方文档](https://docs.vllm.ai/)
- [Qwen 模型仓库](https://huggingface.co/Qwen)
- [Docker Desktop 文档](https://docs.docker.com/desktop/)
- [NVIDIA CUDA 安装指南](https://docs.nvidia.com/cuda/)

---

## 🔗 反向链接

### 前置知识
- [[Docker]] - 容器化基础
- [[CUDA]] - GPU 计算基础

### 相关内容
- [[OpenClaw-Agent配置指南]] - AI Agent 配置

### 应用场景
- 本地部署 Qwen3-ASR 语音识别模型
- 本地部署 Qwen3-TTS 语音合成模型

---

## 9. 实战案例：Qwen3-ASR Docker 部署

### 9.1 项目概述

**目标**：使用 Docker 部署 Qwen3-ASR 语音识别模型，提供 Web 界面和 REST API

**技术栈**：
- 基础镜像：`nvidia/cuda:12.1.0-runtime-ubuntu22.04`
- Python：3.10（Ubuntu 默认版本，兼容性最好）
- 深度学习：PyTorch 2.5.1 (CUDA 12.1)
- 模型：qwen-asr 0.0.6
- Web 界面：Gradio 6.6.0 + FastAPI 0.133.0

**最终目录结构**：
```
E:\ai-deploy\
├── models/qwen3-asr/          # 模型文件 (4.4GB)
├── containers/                 # Docker 配置
│   ├── Dockerfile             # 镜像定义
│   ├── docker-compose.yml     # 服务编排
│   ├── requirements.txt        # Python 依赖
│   ├── server.py              # Web 服务
│   ├── start.bat              # 启动脚本
│   └── stop.bat               # 停止脚本
├── data/                       # 输入输出
├── cache/                      # 缓存
└── logs/                       # 日志
```

### 9.2 遇到的问题与解决方案

#### 问题 1：Python 3.12 兼容性问题

**错误现象**：
```
ModuleNotFoundError: No module named 'distutils'
update-alternatives: --install needs <link> <name> <path> <priority>
```

**原因分析**：
- Python 3.12 移除了内置的 `distutils` 模块
- `update-alternatives` 命令参数不完整
- `python3.12-distutils` 包在 deadsnakes PPA 中不存在

**解决方案**：改用 Python 3.10（Ubuntu 22.04 默认版本）

```dockerfile
# ❌ 错误做法
RUN apt-get install -y python3.12 python3.12-venv
RUN update-alternatives --install /usr/bin/python3 python --slave

# ✅ 正确做法
RUN apt-get install -y python3 python3-pip python3-venv
```

#### 问题 2：qwen-asr 包版本不存在

**错误现象**：
```
ERROR: Could not find a version that satisfies the requirement qwen-asr>=0.1.0
ERROR: No matching distribution found for qwen-asr>=0.1.0
(available versions: 0.0.1, 0.0.2, 0.0.3, 0.0.4, 0.0.5, 0.0.6)
```

**解决方案**：修正 `requirements.txt`
```diff
- qwen-asr>=0.1.0
+ qwen-asr>=0.0.6
```

#### 问题 3：Docker 构建上下文路径错误

**错误现象**：
```
ERROR: lstat /scripts: no such file or directory
```

**原因**：`server.py` 在 `containers/` 目录，不在 `scripts/` 子目录

**解决方案**：
```dockerfile
# ❌ 错误
COPY scripts/*.py /app/

# ✅ 正确
COPY server.py /app/
```

#### 问题 4：模型路径错误

**错误现象**：
```
ValueError: Unrecognized model in /app/models. Should have a `model_type` key in its config.json
```

**原因**：模型实际在 `/app/models/qwen3-asr/` 子目录

**解决方案**：
```python
# ❌ 错误
MODEL_PATH = "/app/models"

# ✅ 正确
MODEL_PATH = "/app/models/qwen3-asr"
```

#### 问题 5：Gradio 挂载覆盖 API 路由

**错误现象**：访问根路径显示 JSON，看不到 Gradio 界面

**原因**：Gradio 挂载在根路径 `/` 覆盖了 FastAPI 路由

**解决方案**：将 Gradio 挂载到 `/ui`，根路径重定向
```python
# ✅ 正确做法
@app.get("/")
async def root():
    return RedirectResponse(url="/ui")

# Gradio 挂载到子路径
gr.mount_gradio_app(app, demo, path="/ui")
```

#### 问题 6：Docker 镜像源 403 错误

**错误现象**：
```
ERROR: unexpected status: 403 Forbidden
from mirror: https://docker.1panel.live/v2/...
```

**原因**：Docker 配置的镜像源返回 403

**解决方案**：直接拉取官方镜像绕过镜像缓存
```bash
docker pull nvidia/cuda:12.1.0-runtime-ubuntu22.04
docker-compose build
```

### 9.3 完整配置文件

#### Dockerfile

```dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 安装 Python 3.10 和 pip
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip3 install --upgrade pip setuptools wheel

# 安装 PyTorch (CUDA 12.1)
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 复制依赖文件
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /app

# 复制服务脚本
COPY server.py /app/

# 创建目录
RUN mkdir -p /app/data /app/cache /app/logs

EXPOSE 7860

CMD ["python3", "-u", "server.py"]
```

#### requirements.txt

```txt
# 核心依赖
torch>=2.0.0
transformers>=4.57.0
qwen-asr>=0.0.6

# Web 服务
gradio>=4.0.0
uvicorn[standard]>=0.24.0
fastapi>=0.104.0

# 音频处理
soundfile>=0.12.0
numpy>=1.24.0

# 工具库
pydantic>=2.0.0
python-multipart>=0.0.6

# 兼容性
setuptools>=65.0.0
wheel>=0.40.0
```

#### docker-compose.yml

```yaml
services:
  qwen3-asr:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: qwen3-asr
    ports:
      - "7860:7860"
    volumes:
      - E:/ai-deploy/models:/app/models:ro
      - E:/ai-deploy/data:/app/data
      - E:/ai-deploy/cache:/app/cache
      - E:/ai-deploy/logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped
    shm_size: '4gb'
    runtime: nvidia
```

### 9.4 服务访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| Gradio 界面 | http://localhost:7860/ui | Web 可视化界面 |
| API 文档 | http://localhost:7860/docs | Swagger 文档 |
| 健康检查 | http://localhost:7860/health | 服务状态检查 |
| API 识别 | http://localhost:7860/api/transcribe | POST 上传音频 |

### 9.5 经验总结

#### Python 版本选择

| 版本 | 推荐场景 | 说明 |
|------|----------|------|
| Python 3.10 | ✅ Docker 部署 | Ubuntu 默认，兼容性最好 |
| Python 3.12 | ❌ 不推荐 | distutils 已移除，生态不成熟 |

#### 模型路径规范

```python
# 挂载点
volumes:
  - E:/ai-deploy/models:/app/models:ro

# 容器内路径
MODEL_PATH = "/app/models/qwen3-asr"  # 注意子目录
```

#### Gradio + FastAPI 集成

```python
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
import gradio as gr

# 使用 lifespan 替代 on_event（FastAPI 新版）
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()  # 启动时加载
    yield

app = FastAPI(lifespan=lifespan)

# 根路径重定向到 UI
@app.get("/")
async def root():
    return RedirectResponse(url="/ui")

# Gradio 挂载到子路径
demo = create_gradio_interface()
gr.mount_gradio_app(app, demo, path="/ui")
```

### 9.6 启动停止脚本

**start.bat**：
```batch
@echo off
echo ============================================================
echo Qwen3-ASR Docker 部署脚本
echo ============================================================
echo.

REM 检查 Docker 是否运行
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker 未运行，请先启动 Docker Desktop
    pause
    exit /b 1
)

cd /d E:\ai-deploy\containers
echo [INFO] 正在启动容器...
docker-compose up -d
echo.
echo [OK] 服务已启动!
echo   - Gradio 界面: http://localhost:7860/ui
echo   - API 文档: http://localhost:7860/docs
pause
```

**stop.bat**：
```batch
@echo off
echo ============================================================
echo Qwen3-ASR Docker 停止脚本
echo ============================================================
echo.

cd /d E:\ai-deploy\containers
echo [INFO] 正在停止容器...
docker-compose down
echo.
echo [OK] 服务已停止!
pause
```
qwen3-asr模型地址：https://modelscope.cn/models/Qwen/Qwen3-ASR-1.7B
fun-asr模型地址：https://modelscope.cn/models/FunAudioLLM/Fun-ASR-Nano-2512
WhisperX 模型地址：https://github.com/m-bain/whisperX
---
问题：识别错误: CUDA driver error: out of memory