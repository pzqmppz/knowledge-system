#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理播客口播稿文件
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 配置
SOURCE_DIR = Path(r"E:\n8n_work\output\播客口播稿")
OUTPUT_DIR = Path(r"E:\文档\code\知识体系\拆解报告\口播稿")
PROCESSED_FILE = Path(r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json")

# 优先级文件列表
PRIORITY_FILES = [
    ("Runway CEO - AI Video", "*Runway*025843.md"),
    ("Chasing Real AGI - ARC Prize", "*Chasing*044254.md"),
    ("Box CEO - Agents and Future of Work", "*Box*042946.md"),
    ("Writer CEO - Easy Button for GenAI", "*Writer*053435.md"),
    ("SurrealDB CEO", "*Surreal*054848.md"),
    ("AI Therapist", "*Therapist*022457.md"),
    ("Dashboards Are Dead - Sigma", "*Dashboards*042326.md"),
    ("AI Engineering Revolution - FirstMark", "*Engineering*032306.md"),
    ("Captions CEO - AI Video", "*Captions*054730.md"),
    ("Datadog CEO - AI at Datadog", "*Datadog*055240.md"),
]

def load_processed():
    """加载已处理记录"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed(processed):
    """保存已处理记录"""
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

def find_file(pattern):
    """根据模式查找文件"""
    files = list(SOURCE_DIR.glob(pattern))
    if files:
        return files[0]
    return None

def is_processed(file_path, processed):
    """检查文件是否已处理"""
    return str(file_path) in processed

def read_file_content(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}")
        return None

def main():
    """主函数"""
    processed = load_processed()
    to_process = []

    # 查找需要处理的文件
    for name, pattern in PRIORITY_FILES:
        file_path = find_file(pattern)
        if file_path and not is_processed(file_path, processed):
            to_process.append((name, file_path))

    print(f"找到 {len(to_process)} 个待处理文件")

    if len(to_process) == 0:
        print("所有文件都已处理完毕")
        return

    # 输出待处理文件列表
    for i, (name, path) in enumerate(to_process, 1):
        print(f"{i}. {name}", file=sys.stderr)
        print(f"   路径: {path}", file=sys.stderr)
        content = read_file_content(path)
        if content:
            print(f"   内容长度: {len(content)} 字符", file=sys.stderr)
            # 不打印预览，避免编码问题
        print(file=sys.stderr)

if __name__ == "__main__":
    main()
