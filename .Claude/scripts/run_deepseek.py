#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from openai import OpenAI

# Load skill
skill_path = Path(__file__).parent.parent / "skills" / "voiceover-xray.md"
with open(skill_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "---" and i > 0:
            start_idx = i + 1
            break
    skill_prompt = "".join(lines[start_idx:])

# Load file
file_path = Path(__file__).parent.parent.parent / "拆解报告" / "口播稿" / "营销增长与SEO优化全攻略（版本一）.md"
with open(file_path, "r", encoding="utf-8") as f:
    file_content = f.read()

# Call DeepSeek API
client = OpenAI(
    api_key="sk-f7123abf43ce4ae48be7549b3af862f6",
    base_url="https://api.deepseek.com"
)

full_prompt = f"""{skill_prompt}

请分析以下口播稿内容：

---
{file_content}
---
"""

print("调用 DeepSeek API...")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个专业的内容分析助手，擅长深度拆解口播稿的传播结构和知识价值。"},
        {"role": "user", "content": full_prompt}
    ],
    temperature=0.7,
    max_tokens=8000
)

result = response.choices[0].message.content

# Save result
output_path = Path(__file__).parent.parent.parent / "拆解报告" / "口播稿" / "营销增长与SEO优化全攻略（版本一）-DeepSeek解读.md"
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result)

print(f"结果已保存到: {output_path}")
print(f"\n--- DeepSeek 分析结果预览 ---\n")
print(result[:2000] + "..." if len(result) > 2000 else result)
