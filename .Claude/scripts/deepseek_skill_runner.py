#!/usr/bin/env python3
"""
使用 DeepSeek API 运行项目的 skill 进行模型效果对比
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 安装依赖：pip install openai
from openai import OpenAI

# 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def load_skill(skill_name: str) -> str:
    """加载 skill 文件内容"""
    skill_path = PROJECT_ROOT / ".Claude" / "skills" / f"{skill_name}.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill 文件不存在: {skill_path}")

    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取 skill 的核心 prompt（跳过 frontmatter）
    lines = content.split("\n")
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "---" and i > 0:
            start_idx = i + 1
            break

    return "\n".join(lines[start_idx:])


def load_file_content(file_path: str) -> str:
    """加载要分析的文件内容"""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        raise FileNotFoundError(f"文件不存在: {full_path}")

    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


def run_deepseek(skill_prompt: str, file_content: str, model: str = "deepseek-chat"):
    """运行 DeepSeek API"""
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

    full_prompt = f"""{skill_prompt}

请分析以下口播稿内容：

---
{file_content}
---
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个专业的内容分析助手，擅长深度拆解口播稿的传播结构和知识价值。"},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
        max_tokens=8000
    )

    return response.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        print("用法: python deepseek_skill_runner.py <skill名称> <文件路径>")
        print("示例: python deepseek_skill_runner.py voiceover-xray '拆解报告/口播稿/营销增长与SEO优化全攻略（版本一）.md'")
        sys.exit(1)

    skill_name = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else None

    # 加载 skill
    print(f"📦 加载 skill: {skill_name}")
    skill_prompt = load_skill(skill_name)

    # 准备输入
    if file_path:
        print(f"📄 加载文件: {file_path}")
        file_content = load_file_content(file_path)
    else:
        print("📝 请输入要分析的内容（按 Ctrl+D 结束输入）：")
        file_content = sys.stdin.read()

    # 运行 DeepSeek
    print(f"🤖 调用 DeepSeek API...")
    result = run_deepseek(skill_prompt, file_content)

    # 输出结果
    print("\n" + "="*60)
    print("📊 DeepSeek 分析结果：")
    print("="*60 + "\n")
    print(result)

    # 可选：保存结果
    output_path = PROJECT_ROOT / "拆解报告" / "口播稿" / f"{Path(file_path).stem}-DeepSeek解读.md" if file_path else None
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n💾 结果已保存到: {output_path}")


if __name__ == "__main__":
    main()
