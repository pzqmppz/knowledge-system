# WhisperX 本地部署指南

> 基于 RTX 4070 SUPER (12GB) + Windows 11 + 国内网络环境
>
> 最后更新：2026-02-26（含部署复盘修正）

---

## 一、概述

### 1.1 WhisperX 是什么

WhisperX 是基于 OpenAI Whisper 的增强版语音识别工具，提供：
- ⚡ 批处理推理（70x 实时速度）
- 🎯 字级时间戳（wav2vec2 对齐）
- 👥 说话人分离（pyannote）
- 🗣️ VAD 预处理（减少幻觉）

### 1.2 部署目标

| 目标 | 说明 |
|------|------|
| 语音识别 | 支持中文长音频（1小时+）转录 |
| 说话人分离 | 自动区分不同说话人 |
| API 服务 | 提供 REST API 供 n8n 调用 |
| Web UI | 提供 Gradio 界面方便测试 |

### 1.3 费用说明

| 项目 | 费用 |
|------|------|
| WhisperX | 完全免费（本地运行） |
| HuggingFace Token | 免费（仅需注册账号） |
| 对比 OpenAI API | $0.006/分钟 |

---

## 二、快速调用

> 已部署完成后，直接使用以下方式调用
双击运行：E:\ai-deploy\containers\start_whisperx.bat
服务地址：http://localhost:8001/ui  

### 2.1 服务地址

| 服务 | 地址 |
|------|------|
| API 文档 | http://localhost:8000/docs |
| 健康检查 | http://localhost:8000/ |
| Gradio UI | http://localhost:8000/ui |

### 2.2 API 调用示例

**curl 调用**：
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@audio.mp3" \
  -F "language=zh" \
  -F "min_speakers=2" \
  -F "max_speakers=5"
```

**Python 调用**：
```python
import requests

url = "http://localhost:8000/transcribe"
files = {"file": open("audio.mp3", "rb")}
data = {"language": "zh", "min_speakers": 2, "max_speakers": 5}

response = requests.post(url, files=files, data=data)
result = response.json()

for segment in result["result"]["segments"]:
    print(f"[{segment['speaker']}] {segment['text']}")
```

### 2.3 返回格式

```json
{
  "success": true,
  "result": {
    "segments": [
      {
        "start": 0.0,
        "end": 3.5,
        "text": "大家好，欢迎参加今天的会议。",
        "speaker": "SPEAKER_00"
      }
    ]
  }
}
```

### 2.4 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| file | file | 必填 | 音频文件（支持 mp3/wav/m4a 等） |
| language | string | zh | 语言代码（zh/en/ja 等） |
| min_speakers | int | None | 最小说话人数 |
| max_speakers | int | None | 最大说话人数 |

---

## 三、环境要求

### 3.1 硬件要求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| GPU | RTX 3060 (12GB) | RTX 4070+ (12GB) |
| 内存 | 16GB | 32GB |
| 硬盘 | 20GB | 50GB（含模型） |

### 3.2 软件要求

| 项目 | 版本要求 | 备注 |
|------|----------|------|
| Windows | 10/11 | - |
| NVIDIA 驱动 | >= 525 | `nvidia-smi` 查看 |
| CUDA | 12.1+ | 与 PyTorch 版本匹配 |
| Python | 3.10 | 推荐 3.10，避免 3.12 |
| FFmpeg | 任意版本 | 音频处理 |

### 3.3 验证命令

```powershell
# 检查 NVIDIA 驱动
nvidia-smi

# 检查 CUDA
nvcc --version

# 检查 Python
python --version
```

---

## 三、部署流程

### 3.1 流程概览

| 阶段 | 内容 | 预估时间 |
|------|------|----------|
| 1. 环境准备 | 创建虚拟环境、配置镜像 | 5 分钟 |
| 2. 安装依赖 | PyTorch、WhisperX | 15 分钟 |
| 3. 模型准备 | 下载模型、配置 Token | 20 分钟 |
| 4. 服务部署 | 创建 API 服务 | 10 分钟 |
| 5. 功能验证 | 测试各功能 | 5 分钟 |

---

### 3.2 阶段一：环境准备

#### Step 1.1：配置 pip 镜像

```powershell
# 使用阿里云镜像（清华源可能有 SSL 问题）
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

#### Step 1.2：创建虚拟环境

```powershell
# 使用 venv
python -m venv whisperx-env
.\whisperx-env\Scripts\activate

# 或使用 conda
conda create -n whisperx python=3.10 -y
conda activate whisperx
```

#### Step 1.3：配置 HF 镜像（国内必须）

```powershell
# 永久生效
[Environment]::SetEnvironmentVariable("HF_ENDPOINT", "https://hf-mirror.com", "User")

# 当前会话立即生效
$env:HF_ENDPOINT="https://hf-mirror.com"
```

---

### 3.3 阶段二：安装依赖

#### Step 2.1：安装 PyTorch

> ⚠️ **注意**：whisperx 3.8.1 要求 `torch~=2.8.0`，旧版本不兼容

```powershell
# 推荐方案：从官方源安装
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128

# 备选方案：清华源
pip install torch torchaudio --index-url https://mirrors.tuna.tsinghua.edu.cn/pytorch/whl/cu128
```

**验证安装**：
```python
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, Version: {torch.__version__}')"
# 预期输出: CUDA: True, Version: 2.8.0+cu128
```

#### Step 2.2：安装 WhisperX

```powershell
pip install whisperx
pip install fastapi uvicorn python-multipart gradio pandas
```

---

### 3.4 阶段三：模型准备

#### Step 3.1：获取 HuggingFace Token

1. 访问 https://huggingface.co/settings/tokens
2. 创建新 Token（只需勾选 **Read** 权限）
3. 访问以下页面接受用户协议：
   - https://huggingface.co/pyannote/speaker-diarization-3.1
   - https://huggingface.co/pyannote/segmentation-3.0

#### Step 3.2：下载模型

创建 `download_models.py`：

```python
import torch

# ============ 重要：解决 PyTorch 2.6+ weights_only 问题 ============
_original_torch_load = torch.load

def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)

torch.load = _patched_load

import whisperx
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
MODEL_ROOT = r"E:\ai-deploy\models"

# 下载 Whisper 模型
print("Downloading Whisper large-v3...")
model = whisperx.load_model("large-v3", device="cuda", compute_type="float16", download_root=MODEL_ROOT)

# 下载中文对齐模型
print("Downloading Chinese alignment model...")
align_model, metadata = whisperx.load_align_model(language_code="zh", device="cuda", model_dir=MODEL_ROOT)

print("All models downloaded!")
```

```powershell
python download_models.py
```

#### Step 3.3：模型目录结构

```
E:\ai-deploy\models\
├── models--Systran--faster-whisper-large-v3\          # 主模型 (~2.9GB)
└── models--jonatasgrosman--wav2vec2-large-xlsr-53-chinese-zh-CN\  # 对齐模型 (~2.4GB)

C:\Users\<用户>\.cache\huggingface\hub\
├── models--pyannote--segmentation-3.0\               # (~5.7MB)
└── models--pyannote--speaker-diarization-3.1\        # 说话人分离模型
```

---

### 3.5 阶段四：服务部署

#### Step 4.1：创建服务脚本

创建 `whisperx_server.py`：

```python
import torch

# ============ 修正1: PyTorch weights_only 问题 ============
_original_torch_load = torch.load

def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)

torch.load = _patched_load

import whisperx
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import gc
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 配置
HF_TOKEN = "hf_xxx"  # 替换为你的 token
MODEL_ROOT = r"E:\ai-deploy\models"
device = "cuda" if torch.cuda.is_available() else "cpu"

# 缓存
align_models = {}

# 加载主模型
print("Loading Whisper model...")
model = whisperx.load_model("large-v3", device, compute_type="float16", download_root=MODEL_ROOT)

# FastAPI 应用
app = FastAPI(title="WhisperX API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form(default="zh"),
    min_speakers: int = Form(default=None),
    max_speakers: int = Form(default=None)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # 1. 转录
        audio = whisperx.load_audio(tmp_path)
        result = model.transcribe(audio, language=language)

        # 2. 对齐
        if language not in align_models:
            align_models[language] = whisperx.load_align_model(
                language_code=language, device=device, model_dir=MODEL_ROOT
            )
        align_model, align_metadata = align_models[language]
        result = whisperx.align(result["segments"], align_model, align_metadata, audio, device)

        # 3. 说话人分离
        diarize_pipeline = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=device)

        # ============ 修正2-4: pyannote 4.x 适配 ============
        audio_tensor = torch.from_numpy(audio).unsqueeze(0).float()
        audio_dict = {"waveform": audio_tensor, "sample_rate": 16000}
        diarize_output = diarize_pipeline(audio_dict, min_speakers=min_speakers, max_speakers=max_speakers)

        # 提取 Annotation
        if hasattr(diarize_output, 'speaker_diarization'):
            diarize_segments = diarize_output.speaker_diarization
        else:
            diarize_segments = diarize_output

        # 转换为 DataFrame
        diarize_df = pd.DataFrame([
            {'start': turn.start, 'end': turn.end, 'speaker': speaker}
            for turn, _, speaker in diarize_segments.itertracks(yield_label=True)
        ])

        result = whisperx.assign_word_speakers(diarize_df, result)
        return {"success": True, "result": result}

    finally:
        os.unlink(tmp_path)
        gc.collect()
        torch.cuda.empty_cache()

@app.get("/")
def root():
    return {"status": "ok", "service": "WhisperX API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Step 4.2：启动服务

```powershell
python whisperx_server.py
```

访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/

---

### 3.6 阶段五：功能验证

```powershell
# 测试 API
curl -X POST "http://localhost:8000/transcribe" -F "file=@test.mp3" -F "language=zh"
```

---

## 四、常见问题与解决方案

### 4.1 安装阶段问题

#### 问题1：pip 镜像 SSL 错误

**症状**：`SSLError: SSL module is not available`

**解决方案**：
```powershell
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
```

---

#### 问题2：PyTorch 版本冲突

**症状**：whisperx 3.8.1 要求 `torch~=2.8.0`

**解决方案**：
```powershell
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
```

---

### 4.2 模型加载问题

#### 问题3：weights_only 安全模式

**症状**：`Unsupported global: GLOBAL omegaconf.listconfig.ListConfig`

**原因**：PyTorch 2.6+ 默认启用 `weights_only=True`

**解决方案**（在 import whisperx 之前）：
```python
import torch
_original_torch_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)
torch.load = _patched_load
```

---

#### 问题4：模型下载超时

**症状**：`ConnectionError` / `ReadTimeout`

**解决方案**：
```powershell
# 确保 HF 镜像已配置
$env:HF_ENDPOINT="https://hf-mirror.com"
```

---

### 4.3 说话人分离问题

#### 问题5：pyannote 4.x API 变更

**症状**：
- `'DiarizeOutput' object has no attribute 'itertracks'`
- `'Annotation' object has no attribute 'iterrows'`

**原因**：pyannote 4.x API 与 3.x 不兼容

**解决方案**：
```python
import pandas as pd

# 1. 转换音频格式
audio_tensor = torch.from_numpy(audio).unsqueeze(0).float()
audio_dict = {"waveform": audio_tensor, "sample_rate": 16000}
diarize_output = diarize_pipeline(audio_dict)

# 2. 提取 Annotation
if hasattr(diarize_output, 'speaker_diarization'):
    diarize_segments = diarize_output.speaker_diarization
else:
    diarize_segments = diarize_output

# 3. 转换为 DataFrame
diarize_df = pd.DataFrame([
    {'start': turn.start, 'end': turn.end, 'speaker': speaker}
    for turn, _, speaker in diarize_segments.itertracks(yield_label=True)
])

result = whisperx.assign_word_speakers(diarize_df, result)
```

---

#### 问题6：HF Token 未配置

**症状**：`ValueError: HF_TOKEN not provided`

**解决方案**：
1. 确认已获取 HF Token（Read 权限）
2. 确认已接受 pyannote 模型用户协议
3. 在代码中配置：`HF_TOKEN = "hf_xxx"`

---

### 4.4 运行时问题

#### 问题7：CUDA Out of Memory

**症状**：`RuntimeError: CUDA out of memory`

**解决方案**：
```python
# 方案A：降低精度
model = whisperx.load_model("large-v3", device, compute_type="int8")

# 方案B：使用小模型
model = whisperx.load_model("medium", device, compute_type="float16")
```

---

#### 问题8：音频格式不支持

**症状**：`Audio file could not be read`

**解决方案**：
```powershell
# 安装 ffmpeg
winget install ffmpeg

# 或转换格式
ffmpeg -i input.m4a -ar 16000 -ac 1 output.wav
```

---

## 五、依赖版本记录

### 5.1 验证可用版本（2026-02-26）

```txt
torch==2.8.0+cu128
torchaudio==2.8.0+cu128
whisperx==3.8.1
pyannote.audio==4.0.4
pyannote.core==6.0.1
pyannote.pipeline==4.0.0
gradio==6.6.0
fastapi==0.115.12
pandas>=1.5.0
```

### 5.2 安装命令

```powershell
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install whisperx fastapi uvicorn python-multipart gradio pandas
```

---

## 六、部署记录

| 日期 | 操作 | 结果 | 备注 |
|------|------|------|------|
| 2026-02-26 | 阶段一：环境准备 | ✅ | 阿里云镜像 |
| 2026-02-26 | 阶段二：安装依赖 | ✅ | PyTorch 2.8.0+cu128 |
| 2026-02-26 | 阶段三：模型准备 | ✅ | 含 pyannote 模型 |
| 2026-02-26 | 阶段四：服务部署 | ✅ | FastAPI + 说话人分离 |
| 2026-02-26 | 阶段五：功能验证 | ✅ | 全部通过 |

---

## 七、附录

### 7.1 调试技巧

```python
# 查看对象类型和属性
print(f"类型: {type(obj)}")
print(f"属性: {[m for m in dir(obj) if not m.startswith('_')]}")

# 阅读源码
import inspect
print(inspect.signature(func))

# 调试日志
print(f"[DEBUG] xxx", flush=True)
```

### 7.2 相关链接

- [WhisperX GitHub](https://github.com/m-bain/whisperX)
- [HuggingFace Token](https://huggingface.co/settings/tokens)
- [pyannote 模型](https://huggingface.co/pyannote/speaker-diarization-3.1)
- [HF 镜像](https://hf-mirror.com)

---

*版本: 2.0*
*更新日期: 2026-02-26*
