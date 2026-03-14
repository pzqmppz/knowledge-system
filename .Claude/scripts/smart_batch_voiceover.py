#!/usr/bin/env python3
"""
Smart batch processing for podcast voiceover files.
Implements deduplication and topic filtering.
"""
import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib

# Configuration
SOURCE_DIR = r"E:\n8n_work\output\播客口播稿"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"
CLAUDE_CODE = r"C:\Users\YourUser\.claude\code"  # Adjust path as needed

# Target: Process 30-50 more unique topics
TARGET_NEW_REPORTS = 40

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

def extract_topic(filename):
    """Extract topic from filename for deduplication"""
    # Remove timestamp
    name = re.sub(r'_\d{8}_\d{6}\.md$', '', filename)
    # Remove special chars and lowercase
    name = re.sub(r'[^\w\s-]', ' ', name).lower().strip()
    # Extract key topic words
    words = name.split()
    # Remove common words
    stopwords = {'ai', 'ceo', 'the', 'and', 'or', 'for', 'with', 'on', 'in', 'at', 'of', 'to', 'from'}
    topic_words = [w for w in words if w not in stopwords and len(w) > 2]
    return ' '.join(topic_words[:5])  # First 5 meaningful words

def group_by_topic(files):
    """Group files by topic to find duplicates"""
    groups = defaultdict(list)
    for f in files:
        topic = extract_topic(f)
        groups[topic].append(f)
    return groups

def select_best_file(files):
    """Select the best file from duplicates (prefer larger size)"""
    best = None
    best_size = 0
    for f in files:
        filepath = os.path.join(SOURCE_DIR, f)
        try:
            size = os.path.getsize(filepath)
            if size > best_size:
                best_size = size
                best = f
        except:
            pass
    return best

def is_already_processed(filepath, processed):
    """Check if file or its duplicate is already processed"""
    # Direct check
    if filepath in processed:
        return True

    # Topic-based check
    topic = extract_topic(os.path.basename(filepath))
    for processed_file in processed.keys():
        if extract_topic(os.path.basename(processed_file)) == topic:
            return True

    return False

def get_unprocessed_files(processed):
    """Get list of unprocessed files with smart filtering"""
    all_files = []
    for f in os.listdir(SOURCE_DIR):
        if f.endswith('.md'):
            filepath = os.path.join(SOURCE_DIR, f)
            if not is_already_processed(filepath, processed):
                all_files.append(f)

    # Group by topic and select best
    groups = group_by_topic(all_files)
    selected = []
    for topic, files in groups.items():
        best = select_best_file(files)
        if best:
            selected.append(best)

    return selected

def process_file(filename):
    """Process a single file using voiceover-xray skill"""
    filepath = os.path.join(SOURCE_DIR, filename)

    try:
        # Read content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Create temp file with clean name
        temp_name = re.sub(r'_\d{8}_\d{6}\.md$', '.md', filename)
        temp_path = os.path.join(SOURCE_DIR, f"temp_{temp_name}")

        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Call voiceover-xray skill
        result = subprocess.run(
            ['claude', 'skill', 'voiceover-xray', temp_path],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Clean temp
        if os.path.exists(temp_path):
            os.remove(temp_path)

        if result.returncode == 0:
            return True, temp_name
        else:
            return False, result.stderr

    except Exception as e:
        return False, str(e)

def main():
    print("🎯 Smart Batch Voiceover Processor")
    print("=" * 50)

    # Load processed record
    processed = load_processed()
    print(f"📊 Already processed: {len(processed)} files")

    # Get unprocessed files
    unprocessed = get_unprocessed_files(processed)
    print(f"📋 Unprocessed unique topics: {len(unprocessed)} files")

    if not unprocessed:
        print("✅ All files processed!")
        return

    # Select files to process
    to_process = unprocessed[:TARGET_NEW_REPORTS]
    print(f"🎯 Planning to process: {len(to_process)} files")
    print()

    # Process files
    success_count = 0
    skip_count = 0

    for i, filename in enumerate(to_process, 1):
        filepath = os.path.join(SOURCE_DIR, filename)

        print(f"[{i}/{len(to_process)}] Processing: {filename[:60]}...")

        # Process the file
        success, result = process_file(filename)

        if success:
            # Mark as processed
            processed[filepath] = {
                "timestamp": int(datetime.now().timestamp()),
                "processed_at": datetime.now().isoformat(),
                "file_name": filename
            }
            success_count += 1
            print(f"  ✅ Success")
        else:
            skip_count += 1
            print(f"  ❌ Failed: {result[:100]}")

        # Save progress every 5 files
        if i % 5 == 0:
            save_processed(processed)
            print(f"  💾 Progress saved ({i}/{len(to_process)})")

        print()

    # Final save
    save_processed(processed)

    print("=" * 50)
    print("📈 Processing Complete!")
    print(f"  ✅ Successfully processed: {success_count}")
    print(f"  ❌ Skipped/Failed: {skip_count}")
    print(f"  📊 Total processed: {len(processed)}")

if __name__ == "__main__":
    main()
