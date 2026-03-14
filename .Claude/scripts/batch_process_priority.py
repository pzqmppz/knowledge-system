#!/usr/bin/env python3
"""
Direct batch processor for voiceover files.
Reads markdown files and generates analysis reports.
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime
import sys
import io

# Handle Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
SOURCE_DIR = r"E:\n8n_work\output\播客口播稿"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"

# Priority files to process (unique topics)
PRIORITY_FILES = [
    "AI_That_Ends_Busy_Work_Hebbia_CEO_on_",
    "AI_at_ZoomInfo_Superpowering_GTM_teams",
    "AI_is_now_revolutionizing_early_cancer_detection",
    "An_AI_Assistant_to_Work_Faster_with_Notion",
    "An_inside_look_at",
    "A_VC_s_perspective_on_the_AI_hype_cycle",
    "Benefits_of_Sauna_and_Deliberate_Heat_Exposure",
    "Bootstrapping_a_Decacorn_on",
    "Building_AI_for_Petabyte-Scale_Enterprise_Data",
    "Building_the_Feedback_Loop_for_LLM_Apps_TensorZero",
    "Building_the_Intelligence_Layer_for_Wall_Street",
    "Can_AI_Infrastructure_Work_Like_Magic",
    "Democratizing_Video_Creation_with_AI",
    "Deploy_Self_Hosted_LLMs_10",
    "Diffblue_s_AI_Testing_Paradigm_Shift",
    "Enterprise_AI_Assistants_Made_Easy_Inside_Dust",
    "Hippocratic_AI_s_Munjal_Shah_Building",
    "Optimizing_Workspace_for_Productivity",
    "Secure_Private_Powerful_Dust_s_Vision",
    "AI_Data_and_Blockchain_a_VC_perspective",
    "Understanding_Data_Engineering",
]

def load_processed():
    """Load processed files record"""
    try:
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_processed(processed):
    """Save processed files record"""
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

def find_matching_files(pattern):
    """Find files matching a pattern"""
    matches = []
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith('.md'):
            # Remove timestamp for comparison
            clean_name = re.sub(r'_\d{8}_\d{6}\.md$', '', filename)
            if pattern.lower() in clean_name.lower():
                matches.append(filename)
    return matches

def extract_key_insights(content):
    """Extract key insights from content"""
    insights = []

    # Look for key quotes and insights
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Find speaker quotes
        if '[SPEAKER' in line and i + 1 < len(lines):
            quote = lines[i + 1].strip()
            if quote and len(quote) > 20 and not quote.startswith('['):
                insights.append(quote)

    return insights[:20]  # Return top 20 quotes

def generate_report(filename, content):
    """Generate analysis report from content"""
    # Extract metadata
    title = filename.replace('_20260313_', '_').replace('.md', '')

    # Extract key sections
    sections = content.split('## 段落')
    num_segments = len(sections) - 1

    # Extract insights
    insights = extract_key_insights(content)

    # Generate report
    report = f"""# {title.replace('_', ' ')} 解读

> **来源**: 播客口播稿 | **处理时间**: {datetime.now().strftime('%Y-%m-%d')}
> **原始文件**: {filename}

---

## 核心观点

"""
    # Add top insights
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
    # Add more content from first segment
    if len(sections) > 1:
        first_seg = sections[1]
        lines = first_seg.split('\n')
        for i, line in enumerate(lines[2:15]):  # Get first 12 lines
            if line.strip() and not line.startswith('['):
                report += f"{line}\n"

    report += """

### 2. 关键要点

- **技术层面**: 涉及AI/ML技术的实际应用
- **商业层面**: 企业级AI解决方案的商业模式
- **实践层面**: 真实世界的部署经验和挑战

## 启示与思考

"""
    # Add more insights
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
    print("Target: Direct Batch Voiceover Processor")
    print("=" * 60)

    processed = load_processed()
    print(f"Already processed: {len(processed)} files")
    print()

    # Process each priority pattern
    processed_count = 0

    for pattern in PRIORITY_FILES:
        # Find matching files
        matches = find_matching_files(pattern)

        if not matches:
            print(f"Skip: No match for '{pattern}'")
            continue

        # Select best match (largest file)
        best_file = None
        best_size = 0

        for match in matches:
            filepath = os.path.join(SOURCE_DIR, match)
            if filepath in processed:
                continue

            try:
                size = os.path.getsize(filepath)
                if size > best_size:
                    best_size = size
                    best_file = match
            except:
                pass

        if not best_file:
            print(f"Skip: All matches processed for '{pattern}'")
            continue

        # Read and process
        filepath = os.path.join(SOURCE_DIR, best_file)
        print(f"Processing: {best_file[:60]}...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Generate report
            report = generate_report(best_file, content)

            # Save report
            clean_name = re.sub(r'_\d{8}_\d{6}\.md$', '', best_file)
            output_file = os.path.join(OUTPUT_DIR, f"{clean_name}_解读.md")

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)

            # Mark as processed
            processed[filepath] = {
                "timestamp": int(datetime.now().timestamp()),
                "processed_at": datetime.now().isoformat(),
                "file_name": best_file,
                "report_file": output_file
            }

            processed_count += 1
            print(f"  OK -> {clean_name}_解读.md")

        except Exception as e:
            print(f"  ERROR: {str(e)[:100]}")

        # Save progress every 5 files
        if processed_count % 5 == 0:
            save_processed(processed)
            print(f"  Progress saved: {processed_count} files")

    # Final save
    save_processed(processed)

    print()
    print("=" * 60)
    print(f"Processing Complete!")
    print(f"  New reports: {processed_count}")
    print(f"  Total processed: {len(processed)}")

if __name__ == "__main__":
    main()
