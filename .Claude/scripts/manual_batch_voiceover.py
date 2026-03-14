#!/usr/bin/env python3
"""
Manual batch processor for voiceover files.
Reads files and invokes voiceover-xray skill for each.
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Configuration
SOURCE_DIR = r"E:\n8n_work\output\播客口播稿"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"

# Topics to prioritize (unique, high-value)
PRIORITY_TOPICS = [
    "Hippocratic",  # Medical AI
    "TensorZero",   # Feedback loops
    "Rogo",         # Finance AI
    "TextQL",       # Enterprise data
    "Raspberry AI", # Fashion AI
    "Synthesia",    # AI video
    "TitanML",      # LLM deployment
    "Patronus AI",  # LLM monitoring
    "Modal",        # AI infrastructure
    "Dust",         # Enterprise assistants
    "Diffblue",     # AI testing
    "Celonis",      # Process mining
    "Ezra",         # Cancer detection
    "Intercom",     # Customer service
    "ZoomInfo",     # Sales intelligence
    "Notion",       # Knowledge work
    "Hebbia",       # Knowledge work AI
    "Fortune",      # AI mastering
    "VC perspective", # Investment view
    "FirstMark",    # VC insights
    "Huberman",     # Health optimization
    "James Clear",  # Habits
    "Dorian Yates", # Muscle building
    "Dr Alex Marson", # Cancer immune system
    "Dr Rhonda Patrick", # Micronutrients
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

def get_priority_files(processed):
    """Get files matching priority topics that aren't processed"""
    priority_files = []

    for filename in os.listdir(SOURCE_DIR):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(SOURCE_DIR, filename)
        if filepath in processed:
            continue

        # Check if matches priority topic
        for topic in PRIORITY_TOPICS:
            if topic.lower() in filename.lower():
                priority_files.append((topic, filename))
                break

    return priority_files

def main():
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("Target: Manual Batch Voiceover Processor")
    print("=" * 60)

    processed = load_processed()
    print(f"📊 Already processed: {len(processed)} files")
    print()

    # Get priority files
    priority_files = get_priority_files(processed)

    if not priority_files:
        print("ℹ️  No priority files found to process")
        print("📋 Listing all unprocessed files...")

        all_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.md')]
        unprocessed = [f for f in all_files if os.path.join(SOURCE_DIR, f) not in processed]

        print(f"\n📋 Unprocessed files: {len(unprocessed)}")
        for i, f in enumerate(unprocessed[:30], 1):
            print(f"  {i}. {f[:70]}")
        return

    print(f"🎯 Found {len(priority_files)} priority files to process:")
    for topic, filename in priority_files[:10]:
        print(f"  - [{topic}] {filename[:60]}")
    print()

    # Generate processing commands
    print("📝 Processing commands:")
    print("=" * 60)

    for topic, filename in priority_files[:40]:  # Max 40 files
        filepath = os.path.join(SOURCE_DIR, filename)
        clean_name = filename.replace('_20260313_', '_').replace('.md', '')

        print(f"# Topic: {topic}")
        print(f"# File: {filename}")
        print(f"/voiceover-xray \"{filepath}\"")
        print()

if __name__ == "__main__":
    main()
