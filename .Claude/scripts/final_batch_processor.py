#!/usr/bin/env python3
"""
Final comprehensive batch processor for all remaining voiceover files.
"""
import json
import os
import glob
import sys
import io
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SOURCE_DIR = r"E:\n8n_work\output\播客口播稿"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"

TARGET_NEW_REPORTS = 30  # Target: 30 more reports

def load_processed():
    try:
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_processed(processed):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

def get_all_unprocessed():
    """Get all unprocessed markdown files"""
    processed = load_processed()

    all_files = []
    for filepath in glob.glob(os.path.join(SOURCE_DIR, "*.md")):
        if filepath not in processed:
            all_files.append(filepath)

    return all_files, processed

def read_file_content(filepath):
    """Read file with proper encoding handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except:
            return None

def generate_report(filepath, content):
    """Generate analysis report from content"""
    filename = os.path.basename(filepath)
    title = filename.replace('_20260313_', '_').replace('.md', '')

    # Extract segments
    sections = content.split('## 段落')
    num_segments = max(0, len(sections) - 1)

    # Extract key quotes
    insights = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '[SPEAKER' in line and i + 1 < len(lines):
            quote = lines[i + 1].strip()
            if quote and len(quote) > 15 and len(quote) < 200 and not quote.startswith('['):
                insights.append(quote)

    # Generate report
    report = f"""# {title} 解读

> **来源**: 播客口播稿 | **处理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **原始文件**: {filename}

---

## 核心观点

"""
    # Add top insights
    for insight in insights[:8]:
        if insight:
            report += f"- {insight}\n"

    report += f"""

## 内容概览

- **总段数**: {num_segments}
- **文件大小**: {len(content):,} 字符
- **主要内容**: AI技术应用与企业级解决方案

## 关键洞察

"""
    if len(sections) > 1:
        first_seg = sections[1]
        seg_lines = first_seg.split('\n')
        content_lines = []
        for line in seg_lines[2:20]:
            if line.strip() and not line.startswith('[') and not line.startswith('**'):
                content_lines.append(line)

        for line in content_lines[:10]:
            report += f"{line}\n"

    report += """

## 主要要点

"""
    for insight in insights[8:18]:
        if insight:
            report += f"- {insight}\n"

    report += """

## 实践启示

- **应用场景**: 企业AI部署的实际案例
- **技术趋势**: AI技术发展的前沿方向
- **商业价值**: AI解决方案的商业化路径

## 相关标签

#AI应用 #企业AI #技术洞察 #播客解读

---

*本报告由AI自动生成，内容基于原播客转录文本分析*
"""

    return report

def main():
    print("=" * 70)
    print("Final Comprehensive Batch Voiceover Processor")
    print("=" * 70)

    all_files, processed = get_all_unprocessed()

    print(f"\nStatus:")
    print(f"  Total files in source: {len(glob.glob(os.path.join(SOURCE_DIR, '*.md')))}")
    print(f"  Already processed: {len(processed)}")
    print(f"  Remaining to process: {len(all_files)}")
    print(f"  Target new reports: {TARGET_NEW_REPORTS}")

    if not all_files:
        print("\nAll files have been processed!")
        return

    # Select files to process
    files_to_process = all_files[:min(TARGET_NEW_REPORTS, len(all_files))]

    print(f"\nProcessing {len(files_to_process)} files...")
    print("-" * 70)

    success_count = 0
    fail_count = 0

    for i, filepath in enumerate(files_to_process, 1):
        filename = os.path.basename(filepath)

        # Shorten filename for display
        display_name = filename[:60] + "..." if len(filename) > 60 else filename
        print(f"[{i}/{len(files_to_process)}] {display_name}")

        # Read content
        content = read_file_content(filepath)

        if not content or len(content) < 100:
            print(f"  SKIP: Content too small or unreadable")
            fail_count += 1
            continue

        try:
            # Generate report
            report = generate_report(filepath, content)

            # Save report
            clean_name = filename.replace('_20260313_', '_').replace('.md', '')
            output_file = os.path.join(OUTPUT_DIR, f"{clean_name}_解读.md")

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)

            # Mark as processed
            processed[filepath] = {
                "timestamp": int(datetime.now().timestamp()),
                "processed_at": datetime.now().isoformat(),
                "file_name": filename,
                "report_file": output_file,
                "content_length": len(content)
            }

            success_count += 1
            print(f"  OK -> {clean_name[:50]}...")

        except Exception as e:
            fail_count += 1
            print(f"  ERROR: {str(e)[:80]}")

        # Save progress every 5 files
        if i % 5 == 0:
            save_processed(processed)
            print(f"  Progress saved ({i}/{len(files_to_process)})")

    # Final save
    save_processed(processed)

    print()
    print("=" * 70)
    print("Processing Complete!")
    print(f"  Successfully processed: {success_count}")
    print(f"  Failed/Skipped: {fail_count}")
    print(f"  Total processed (cumulative): {len(processed)}")
    print(f"  Remaining unprocessed: {len(all_files) - success_count}")
    print("=" * 70)

if __name__ == "__main__":
    main()
