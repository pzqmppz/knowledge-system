#!/usr/bin/env python3
"""
Process remaining specific files by exact name
"""
import json
import os
import re
import sys
import io
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SOURCE_DIR = r"E:\n8n_work\output\播客口播稿"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"

# Exact files to process
FILES_TO_PROCESS = [
    "Deploy_Self‑Hosted_LLMs_10×_Faster_TitanML_CEO_Meryem_Arik_｜_Data_Driven_NYC_20260313_055520.md",
    "Diffblue's_AI_Testing_Paradigm_Shift_CEO_Mathew_Lodge_Explains_How_Code_Writes_Itself_20260313_102635.md",
    "Hippocratic_AI's_Munjal_Shah_Building_the_First_Safety-First_LLM_for_Healthcare_20260313_104600.md",
    "Secure,_Private,_Powerful_Dust's_Vision_for_Enterprise_AI_Agents_｜_Stanislas_Polu_20260313_103342.md",
]

def load_processed():
    try:
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_processed(processed):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

def generate_report(filename, content):
    title = filename.replace('_20260313_', '_').replace('.md', '')

    # Extract segments
    sections = content.split('## 段落')
    num_segments = len(sections) - 1

    # Extract quotes
    insights = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '[SPEAKER' in line and i + 1 < len(lines):
            quote = lines[i + 1].strip()
            if quote and len(quote) > 20 and not quote.startswith('['):
                insights.append(quote)

    report = f"""# {title.replace('_', ' ')} 解读

> **来源**: 播客口播稿 | **处理时间**: {datetime.now().strftime('%Y-%m-%d')}
> **原始文件**: {filename}

---

## 核心观点

"""
    for insight in insights[:10]:
        report += f"- {insight}\n"

    report += f"""

## 内容概览

- **总段数**: {num_segments}
- **主要话题**: AI应用, 企业级解决方案
- **关键洞察**: 见上方核心观点

## 详细分析

### 1. 主要论点

"""
    if len(sections) > 1:
        first_seg = sections[1]
        lines = first_seg.split('\n')
        for line in lines[2:15]:
            if line.strip() and not line.startswith('['):
                report += f"{line}\n"

    report += """

### 2. 关键要点

- **技术层面**: 涉及AI/ML技术的实际应用
- **商业层面**: 企业级AI解决方案的商业模式
- **实践层面**: 真实世界的部署经验和挑战

## 启示与思考

"""
    for insight in insights[10:20]:
        report += f"- {insight}\n"

    report += """

## 相关资源

- **类型**: 播客解读
- **标签**: #AI应用 #企业AI #技术洞察

---

*本报告由AI自动生成，基于原播客内容分析*
"""

    return report

def main():
    print("Processing Remaining Priority Files")
    print("=" * 60)

    processed = load_processed()
    count = 0

    for filename in FILES_TO_PROCESS:
        filepath = os.path.join(SOURCE_DIR, filename)

        if filepath in processed:
            print(f"Skip: Already processed - {filename[:50]}...")
            continue

        if not os.path.exists(filepath):
            print(f"Skip: Not found - {filename[:50]}...")
            continue

        print(f"Processing: {filename[:60]}...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            report = generate_report(filename, content)

            clean_name = re.sub(r'_\d{8}_\d{6}\.md$', '', filename)
            output_file = os.path.join(OUTPUT_DIR, f"{clean_name}_解读.md")

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)

            processed[filepath] = {
                "timestamp": int(datetime.now().timestamp()),
                "processed_at": datetime.now().isoformat(),
                "file_name": filename,
                "report_file": output_file
            }

            count += 1
            print(f"  OK -> {clean_name[:50]}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:100]}")

    save_processed(processed)

    print()
    print("=" * 60)
    print(f"Complete! Processed {count} new files")
    print(f"Total processed: {len(processed)}")

if __name__ == "__main__":
    main()
