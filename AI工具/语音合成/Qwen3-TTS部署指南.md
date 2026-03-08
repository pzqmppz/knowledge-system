# Qwen3-TTS 部署指南

> 基于 Qwen3-TTS 的语音合成和声音克隆本地部署
>
> 最后更新：2026-02-26

---

## 一、概述

Qwen3-TTS 是阿里开源的语音合成模型，支持多种生成模式：

| 模式 | 功能 | 适用场景 |
|------|------|----------|
| **Base (声音克隆)** | 上传参考音频，克隆音色 | 复制特定人的声音 |
| **Voice Design** | 通过自然语言描述音色 | "温柔女声"、"沉稳男声" |
| **CustomVoice** | 使用预设的9种音色 | 快速选择预设声音 |

---

## 二、模型部署

### 2.1 部署信息

| 项目 | Voice Design | Base (声音克隆) |
|------|--------------|-----------------|
| 模型名称 | Qwen3-TTS-12Hz-1.7B-VoiceDesign | Qwen3-TTS-12Hz-1.7B-Base |
| 模型大小 | 3.8GB | 3.6GB |
| GPU 显存 | ~4GB | ~4GB |
| 虚拟环境 | `E:\ai-deploy\qwen3-tts-env` | `E:\ai-deploy\qwen3-tts-base-env` |
| 模型目录 | `E:\ai-deploy\models\Qwen3-TTS` | `E:\ai-deploy\models\Qwen3-TTS-Base` |
| 服务端口 | **8003** | **8004** |

### 2.2 启动方式

```powershell
# Voice Design 模式
E:\ai-deploy\containers\start_qwen3tts.bat

# Base 声音克隆模式
E:\ai-deploy\containers\start_qwen3tts_base.bat
```

### 2.3 服务地址

| 服务 | Voice Design (8003) | Base (8004) |
|------|---------------------|-------------|
| Gradio UI | http://localhost:8003/ui | http://localhost:8004/ui |
| API 文档 | http://localhost:8003/docs | http://localhost:8004/docs |
| 健康检查 | http://localhost:8003/health | http://localhost:8004/health |

---

## 三、快速调用

### 3.1 Voice Design API（端口 8003）

通过自然语言描述音色：

```bash
# curl 调用
curl -X POST "http://localhost:8003/api/tts" \
  -F "text=你好，这是一个测试。" \
  -F "language=Chinese" \
  -F "instruct=用温柔的女声朗读" \
  --output output.wav
```

```python
# Python 调用
import requests

response = requests.post(
    "http://localhost:8003/api/tts",
    data={
        "text": "你好，这是一个测试。",
        "language": "Chinese",
        "instruct": "用温柔的女声朗读",
    }
)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

### 3.2 声音克隆 API（端口 8004）

上传参考音频，克隆其音色：

```bash
# curl 调用
curl -X POST "http://localhost:8004/api/tts-clone" \
  -F "text=这是要合成的文字内容" \
  -F "language=Chinese" \
  -F "ref_text=参考音频中的文字内容" \
  -F "reference_audio=@reference.wav" \
  --output output.wav
```

```python
# Python 调用
import requests

with open("reference.wav", "rb") as f:
    response = requests.post(
        "http://localhost:8004/api/tts-clone",
        data={
            "text": "这是要合成的文字内容",
            "language": "Chinese",
            "ref_text": "参考音频中的文字内容",
        },
        files={"reference_audio": f},
    )

with open("output.wav", "wb") as f:
    f.write(response.content)
```

### 3.3 参数说明

**Voice Design (8003)**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | ✅ | 要合成的文字 |
| language | string | ✅ | 语言（Chinese/English） |
| instruct | string | ✅ | 音色描述（如"温柔女声"） |

**声音克隆 (8004)**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | ✅ | 要合成的文字 |
| language | string | ✅ | 语言（Chinese/English） |
| ref_text | string | ✅ | 参考音频对应的文字 |
| reference_audio | file | ✅ | 参考音频文件（3-10秒） |

---

## 四、依赖版本

```txt
Python==3.10.11
PyTorch==2.5.1+cu121
qwen-tts==0.1.1
transformers==4.57.3
gradio==6.6.0
```

---

## 四、使用方法

### 4.1 Voice Design 模式（端口 8003）

通过自然语言描述想要的音色：

```python
from qwen_tts import Qwen3TTSModel
import torch

model = Qwen3TTSModel.from_pretrained(
    r"E:\ai-deploy\models\Qwen3-TTS",
    device_map="auto",
    torch_dtype=torch.float16,
)

wavs, sr = model.generate_voice_design(
    text="你好，这是一个测试。",
    language="Chinese",
    instruct="用温柔的女声朗读",
)
```

### 4.2 Base 声音克隆模式（端口 8004）

上传参考音频，克隆其音色：

```python
from qwen_tts import Qwen3TTSModel
import torch

model = Qwen3TTSModel.from_pretrained(
    r"E:\ai-deploy\models\Qwen3-TTS-Base",
    device_map="auto",
    torch_dtype=torch.float16,
)

wavs, sr = model.generate_voice_clone(
    text="这是要合成的文字内容",
    language="Chinese",
    ref_audio="reference.wav",      # 参考音频路径
    ref_text="参考音频中的文字内容",  # 参考音频对应的文字
    x_vector_only_mode=False,       # ICL 模式，质量更好
    max_new_tokens=2048,
    do_sample=True,
    top_k=50,
    top_p=1.0,
    temperature=0.9,
    repetition_penalty=1.05,
    subtalker_dosample=True,
    subtalker_top_k=50,
    subtalker_top_p=1.0,
    subtalker_temperature=0.9,
)
```

### 4.3 参考音频要求（声音克隆）

- **格式**：WAV、MP3 等常见格式
- **时长**：3-10秒最佳（更长也可以）
- **内容**：清晰的人声，无背景音乐
- **质量**：无噪音、无回声

---

## 五、API 调用

### 5.1 声音克隆 API (端口 8004)

**Python 调用**：
```python
import requests

url = "http://localhost:8004/api/tts-clone"

with open("reference.wav", "rb") as f:
    response = requests.post(
        url,
        data={
            "text": "你好，这是一个测试。",
            "language": "Chinese",
            "ref_text": "参考音频中的文字内容",
        },
        files={"reference_audio": f},
    )

with open("output.wav", "wb") as f:
    f.write(response.content)
```

**curl 调用**：
```bash
curl -X POST "http://localhost:8004/api/tts-clone" \
  -F "text=你好，这是一个测试。" \
  -F "language=Chinese" \
  -F "ref_text=参考音频中的文字内容" \
  -F "reference_audio=@reference.wav" \
  --output output.wav
```

---

## 六、常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| PyTorch 依赖冲突 | typing-extensions 版本问题 | 使用 cu121 版本 |
| 页面文件太小错误 | 系统内存不足 | 释放内存后重试 |
| 不支持 generate_custom_voice | 模型类型不匹配 | 使用对应模型的方法 |
| SoX 未找到 | 未安装音频工具 | `winget install sox` |
| pip MemoryError | pip 缓存损坏 | `pip cache purge` |
| `reference_audio` 参数错误 | 参数名错误 | 改为 `ref_audio` |
| `ref_text is required` | ICL 模式需要参考文本 | 添加 `ref_text` 参数 |
| 生成音频过短/不匹配 | 生成参数不正确 | 按官方示例调整参数 |

---

## 七、文件清单

| 文件 | 路径 |
|------|------|
| Voice Design 服务脚本 | `E:\ai-deploy\containers\qwen3_tts_server.py` |
| Voice Design 启动脚本 | `E:\ai-deploy\containers\start_qwen3tts.bat` |
| Base 服务脚本 | `E:\ai-deploy\containers\qwen3_tts_base_server.py` |
| Base 启动脚本 | `E:\ai-deploy\containers\start_qwen3tts_base.bat` |
| Voice Design 模型 | `E:\ai-deploy\models\Qwen3-TTS\` |
| Base 模型 | `E:\ai-deploy\models\Qwen3-TTS-Base\` |

---

## 八、模型对比

| 模型 | 端口 | 功能 | 方法 | 特点 |
|------|------|------|------|------|
| **Base** | 8004 | 声音克隆 | `generate_voice_clone()` | 克隆任意声音 |
| VoiceDesign | 8003 | 指令设计音色 | `generate_voice_design()` | 通过自然语言描述 |
| CustomVoice | - | 预设说话人 | `generate_custom_voice()` | 9种预设音色 |

---

*文档版本: 2.0*
*更新日期: 2026-02-26*
