#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
播客口播稿批量处理脚本
自动处理所有未处理的播客口播稿文件
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

# 配置
SOURCE_DIR = r"E:\n8n_work\output\播客口播稿"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"

def load_processed_records():
    """加载已处理记录"""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed_record(file_path, report_path):
    """保存处理记录"""
    records = load_processed_records()
    records[file_path] = {
        "timestamp": int(datetime.now().timestamp()),
        "processed_at": datetime.now().isoformat(),
        "file_name": os.path.basename(file_path),
        "report_file": report_path
    }
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def get_all_files():
    """获取所有md文件"""
    source_path = Path(SOURCE_DIR)
    return list(source_path.glob("*.md"))

def get_unprocessed_files():
    """获取未处理的文件"""
    processed = load_processed_records()
    all_files = get_all_files()
    unprocessed = []

    for file_path in all_files:
        full_path = str(file_path)
        # 检查是否已处理（通过完整路径匹配）
        is_processed = any(
            processed_record.get("file_name") == file_path.name or
            full_path in processed
            for processed_record in processed.values()
        )
        if not is_processed:
            unprocessed.append(file_path)

    return unprocessed

def extract_topic_from_filename(filename):
    """从文件名提取主题"""
    # 移除时间戳和扩展名
    name = re.sub(r'_\d{8}_\d{6}\.md$', '', filename)
    # 移除特殊字符，保留中英文、数字、空格
    name = re.sub(r'[^\w\s\u4e00-\u9fff-]', ' ', name)
    # 替换下划线为空格
    name = name.replace('_', ' ')
    # 压缩多个空格
    name = ' '.join(name.split())
    return name

def categorize_by_topic(files):
    """按主题分类文件"""
    categories = {
        "AI_Infrastructure": [],
        "AI_Agents": [],
        "AI_Application": [],
        "Enterprise_AI": [],
        "AI_Research": [],
        "AI_Video": [],
        "AI_Coding": [],
        "Data_Database": [],
        "Health_Medicine": [],
        "VC_Business": [],
        "Customer_Service": [],
        "Other": []
    }

    topic_keywords = {
        "AI_Infrastructure": ["infrastructure", "compute", "deployment", "modal", "fireworks", "serverless"],
        "AI_Agents": ["agent", "autonomous", "workflow", "langchain", "basis", "imbue"],
        "AI_Application": ["application", "product", "experience", "user"],
        "Enterprise_AI": ["enterprise", "scaling", "organization", "team"],
        "AI_Research": ["research", "paper", "transformer", "openai", "anthropic", "model", "llm", "gpt"],
        "AI_Video": ["video", "runway", "captions", "synthesia", "fashion"],
        "AI_Coding": ["coding", "programming", "github", "cursor", "poolside", "diffblue"],
        "Data_Database": ["data", "database", "snowflake", "pinecone", "weaviate", "surreal", "motherduck", "trino", "influxdb"],
        "Health_Medicine": ["health", "medical", "doctor", "cancer", "therapy", "hippocratic"],
        "VC_Business": ["vc", "venture", "startup", "ceo", "fund", "investment"],
        "Customer_Service": ["customer", "service", "call", "center", "support", "intercom", "ada"]
    }

    for file_path in files:
        filename_lower = file_path.name.lower()
        categorized = False

        for category, keywords in topic_keywords.items():
            if any(keyword in filename_lower for keyword in keywords):
                categories[category].append(file_path)
                categorized = True
                break

        if not categorized:
            categories["Other"].append(file_path)

    return categories

def generate_report_summary():
    """生成处理摘要"""
    processed = load_processed_records()
    unprocessed = get_unprocessed_files()
    categories = categorize_by_topic(unprocessed)

    print("=" * 80)
    print("播客口播稿批量处理状态")
    print("=" * 80)
    print(f"总文件数: {len(get_all_files())}")
    print(f"已处理: {len(processed)}")
    print(f"未处理: {len(unprocessed)}")
    print()
    print("未处理文件分类:")
    print("-" * 80)

    for category, files in categories.items():
        if files:
            print(f"{category}: {len(files)} 个文件")

    print()
    print("=" * 80)

    # 返回需要处理的文件（每个主题取前2个）
    files_to_process = []
    for category, files in categories.items():
        if files:
            files_to_process.extend(files[:2])

    return files_to_process

if __name__ == "__main__":
    files_to_process = generate_report_summary()

    if files_to_process:
        print(f"\n准备处理 {len(files_to_process)} 个文件:")
        for i, f in enumerate(files_to_process[:10], 1):
            print(f"{i}. {f.name}")
        if len(files_to_process) > 10:
            print(f"... 还有 {len(files_to_process) - 10} 个文件")
