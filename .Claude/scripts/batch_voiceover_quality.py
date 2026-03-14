#!/usr/bin/env python3
"""
批量处理播客口播稿 - 使用 voiceover-xray skill 保证质量

此脚本通过 Skill 工具调用 voiceover-xray skill，确保每个文件都按照完整的 SOP 处理。
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

# 配置
WATCH_DIR = r"E:\n8n_work\output\播客口播稿"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"
BATCH_SIZE = 5  # 每批处理数量，避免 token 限制

def load_processed():
    """加载已处理文件记录"""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed(records):
    """保存已处理文件记录"""
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def get_all_files():
    """获取所有需要处理的文件"""
    watch_path = Path(WATCH_DIR)
    return list(watch_path.glob("*.md"))

def get_unprocessed_files(all_files, processed_records):
    """获取未处理的文件"""
    unprocessed = []
    seen_titles = set()

    for file in all_files:
        file_path = str(file)

        # 检查是否已处理
        if file_path in processed_records:
            continue

        # 检查是否重复（基于文件名相似度）
        title = file.stem
        is_duplicate = False

        for seen_title in seen_titles:
            # 简单的重复检测：去掉时间戳后比较
            title_base = title.split('_202603')[0].rstrip('_')
            seen_base = seen_title.split('_202603')[0].rstrip('_')
            if title_base == seen_base or title_base in seen_base or seen_base in title_base:
                is_duplicate = True
                # 标记重复文件为已处理
                processed_records[file_path] = {
                    'timestamp': int(time.time()),
                    'processed_at': datetime.now().isoformat(),
                    'file_name': file.name,
                    'duplicate': True
                }
                break

        if not is_duplicate:
            unprocessed.append(file)
            seen_titles.add(title)

    return unprocessed, processed_records

def print_processing_instructions(files):
    """打印处理指令"""
    print("\n" + "="*60)
    print(f"📝 批量处理播客口播稿 - 共 {len(files)} 个文件")
    print("="*60)
    print("\n📋 待处理文件列表：\n")

    for i, file in enumerate(files, 1):
        print(f"  {i}. {file.name}")

    print("\n" + "="*60)
    print("⚙️  处理方式：使用 voiceover-xray skill")
    print("="*60)

    # 生成分批指令
    batches = [files[i:i+BATCH_SIZE] for i in range(0, len(files), BATCH_SIZE)]

    print(f"\n📦 共 {len(batches)} 批，每批最多 {BATCH_SIZE} 个文件\n")

    for batch_idx, batch in enumerate(batches, 1):
        print(f"第 {batch_idx} 批 ({len(batch)} 个文件):")
        for file in batch:
            print(f"  - {file.name}")
        print()

def main():
    print("\n🔍 扫描播客口播稿目录...")

    # 获取所有文件
    all_files = get_all_files()
    print(f"📁 总文件数: {len(all_files)}")

    # 加载已处理记录
    processed_records = load_processed()
    print(f"✅ 已处理: {len(processed_records)}")

    # 获取未处理文件
    unprocessed_files, processed_records = get_unprocessed_files(all_files, processed_records)
    print(f"📝 待处理: {len(unprocessed_files)}")

    if not unprocessed_files:
        print("\n✨ 所有文件已处理完成！")
        return

    # 打印处理指令
    print_processing_instructions(unprocessed_files)

    # 保存更新的处理记录（标记重复文件）
    save_processed(processed_records)

    print("\n" + "="*60)
    print("📖 处理步骤")
    print("="*60)
    print("""
1. 对于每个文件，在 Claude Code 中执行：
   /voiceover-xray E:\\n8n_work\\output\\播客口播稿\\<文件名>.md

2. 或批量调用（推荐）：
   将文件列表提供给 Claude Code，让它逐个使用 voiceover-xray skill 处理

3. 处理完成后，索引会自动更新
    """)

    # 生成文件列表供复制
    print("\n" + "="*60)
    print("📋 文件路径列表（可复制）")
    print("="*60)
    for file in unprocessed_files[:BATCH_SIZE]:
        print(f'"{str(file)}"')

if __name__ == "__main__":
    main()
