#!/usr/bin/env python3
"""
批量处理口播稿文件
读取指定目录下的 .md 文件并执行 voiceover-xray 拆解
"""

import os
import sys
import json
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入 voiceover-xray skill
import importlib.util
spec = importlib.util.spec_from_file_location("voiceover_xray",
    Path(__file__).parent.parent / "skills" / "voiceover-xray.md")
# voiceover-xray 是一个 skill 文件，不是 Python 模块
# 我们需要手动执行其逻辑

def read_file_content(file_path: Path) -> str:
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return ""

def main():
    if len(sys.argv) < 2:
        print("用法: python batch_voiceover.py <文件路径>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        sys.exit(1)

    content = read_file_content(file_path)
    print(f"文件内容 ({len(content)} 字符):")
    print("=" * 60)
    print(content[:1000])  # 打印前 1000 字符
    print("=" * 60)

if __name__ == "__main__":
    main()
