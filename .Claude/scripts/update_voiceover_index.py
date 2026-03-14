#!/usr/bin/env python3
"""
Update voiceover index with all processed reports
"""
import json
import os
import re
from datetime import datetime
from collections import defaultdict

PROCESSED_FILE = r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json"
OUTPUT_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"
INDEX_FILE = os.path.join(OUTPUT_DIR, "INDEX.md")

def load_processed():
    try:
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def categorize_report(filename):
    """Categorize report by content"""
    filename_lower = filename.lower()

    # Health/Medical
    if any(k in filename_lower for k in ['health', 'medical', 'doctor', 'cancer', 'hippocratic', 'deepscribe', 'ezra', 'huberman', 'rhonda', 'eagleman', 'brain', 'body', 'addiction', 'trauma', 'therapy', 'dopamine', 'serotonin', 'love', 'desire', 'movement', 'sauna', 'heat', 'cold', 'sleep', 'memory', 'attention', 'vitamin', 'micronutrient', 'longevity', 'youthful', 'vitality', 'aging', 'immune', 'genes', 'risk', 'morals']):
        return '观点/健康'

    # Science/Education
    if any(k in filename_lower for k in ['science', 'learn', 'understand', 'explain', 'physics', 'biology', 'chemistry', 'math', 'data happened', 'chris wig']):
        return '科普/科学'

    # Business/Investment
    if any(k in filename_lower for k in ['vc', 'venture', 'investment', 'investor', 'funding', 'startup', 'unicorn', 'decacorn', 'acquisition', 'exit', 'ipo', 'revenue', 'business', 'enterprise', 'b2b', 'gtm', 'plg', 'zirp', 'tomasz tunguz', 'firstmark', 'matt turck', 'theory ventures']):
        return '商业/投资'

    # Technology/Engineering
    if any(k in filename_lower for k in ['engineering', 'developer', 'code', 'programming', 'software', 'infrastructure', 'deploy', 'scale', 'testing', 'devops', 'cicd', 'github', 'cursor', 'vibe coding', 'openai', 'anthropic', 'claude', 'gpt', 'gemini', 'llm', 'diffblue', 'spur', 'fix tech debt', 'jenry howard', 'sharon zhou', 'lamini']):
        return '技术/工程'

    # AI/ML Research
    if any(k in filename_lower for k in ['agi', 'reasoning', 'inference', 'scaling', 'training', 'fine-tuning', 'rlhf', 'embeddings', 'vector', 'rag', 'retrieval', 'agent', 'multi-agent', 'verification', 'eval', 'benchmark', 'arc prize', 'imbue', 'poolside', 'nomic', 'ai2', 'olmo', 'state of llm', 'state of ai', 'sebastian raschka']):
        return '技术/科普'

    # Product/Design
    if any(k in filename_lower for k in ['product', 'design', 'ux', 'ui', 'user', 'experience', 'creativity', 'creative', 'adobe', 'firefly', 'photoshop', 'canva', 'captions', 'runway', 'synthesia', 'raspberry', 'fashion', 'video', 'image', 'vision', 'apple vision pro', 'hollywood', 'cris valenzuela']):
        return '技术/产品'

    # Data/Analytics
    if any(k in filename_lower for k in ['data', 'analytics', 'database', 'warehouse', 'lakehouse', 'snowflake', 'databricks', 'trino', 'iceberg', 'influxdb', 'espresso', 'sigma', 'dashboard', 'bi', 'visualization', 'grafana', 'datadog', 'monitoring', 'observability', 'textql', 'petabyte', 'pinecone', 'weaviate', 'vector database', 'understanding data engineering']):
        return '技术/产品'

    # Security/Safety
    if any(k in filename_lower for k in ['security', 'safety', 'guardrails', 'hallucination', 'red-team', 'robust', 'private', 'secure', 'credal', 'dust', 'hippocratic', 'patronus', 'haize']):
        return '技术/安全'

    # Open Source
    if any(k in filename_lower for k in ['open source', 'oss', 'mistral', 'nomic', 'huggingface', 'langchain', 'llamaindex']):
        return '技术/开源'

    # Personal Growth/Self-Improvement
    if any(k in filename_lower for k in ['habit', 'james clear', 'growth', 'ceo', 'leadership', 'management', 'career', 'how to grow', 'airtable', 'howie liu', 'daniel dines', 'morgante pell']):
        return '观点/个人成长'

    # Finance/Fintech
    if any(k in filename_lower for k in ['finance', 'financial', 'wall street', 'rogo', 'pigment', 'excel', 'spreadsheet', 'budgeting', 'ramp', 'intercom', 'ada', 'customer service', 'call center']):
        return '技术/金融'

    # E-commerce/Retail
    if any(k in filename_lower for k in ['commerce', 'shopify', 'stripe', 'agentic commerce', 'emily glassberg']):
        return '商业/业务'

    # Gaming/Metaverse
    if any(k in filename_lower for k in ['game', 'gaming', 'roblox', 'metaverse', 'xbox', 'playstation', 'nintendo']):
        return '技术/产品'

    # Networking/Cloud
    if any(k in filename_lower for k in ['cloud', 'serverless', 'compute', 'infrastructure', 'modal', 'zo computer']):
        return '技术/产品'

    # Search/Discovery
    if any(k in filename_lower for k in ['search', 'discovery', 'perplexity', 'you.com', 'glean', 'reinventing search', 'richard socher']):
        return '技术/产品'

    # Marketing/Growth
    if any(k in filename_lower for k in ['marketing', 'growth', 'seo', 'foursquare', 'location', 'innovation']):
        return '商业/业务'

    # Default
    return '技术/商业'

def main():
    print("Updating Voiceover Index...")

    processed = load_processed()

    # Get all reports with report_file
    reports = []
    for filepath, info in processed.items():
        if 'report_file' in info:
            reports.append(info)

    # Sort by date
    reports.sort(key=lambda x: x.get('timestamp', 0))

    # Categorize and count
    categorized = defaultdict(list)
    for report in reports:
        filename = os.path.basename(report['file_name'])
        category = categorize_report(filename)
        categorized[category].append(report)

    # Generate index entries
    index_entries = []
    for category in sorted(categorized.keys()):
        for report in categorized[category]:
            filename = os.path.basename(report['file_name'])
            clean_name = filename.replace('_20260313_', '_').replace('.md', '').replace('.md', '')
            clean_name = re.sub(r'_\d{6}$', '', clean_name)  # Remove trailing timestamp
            clean_name = clean_name.replace('_', ' ')

            # Format as wiki link
            link_name = clean_name.replace(' ', '_')
            date_str = datetime.fromtimestamp(report.get('timestamp', 0)).strftime('%Y-%m-%d')

            index_entries.append(f"| [[{link_name}_解读]] | {category} | 播客访谈 | {date_str} |")

    # Update INDEX.md
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the table section and replace it
    table_start = content.find('## 📋 解读列表')
    table_end = content.find('---', table_start + 1)

    if table_start > 0 and table_end > table_start:
        new_content = content[:table_start] + '## 📋 解读列表\n\n' + \
                     '| 标题 | 类型 | 平台 | 解读日期 |\n' + \
                     '|------|------|------|----------|\n' + \
                     '\n'.join(index_entries) + '\n\n' + \
                     content[table_end:]

        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Updated INDEX.md with {len(index_entries)} entries")
    else:
        print("Could not find table section in INDEX.md")

    # Update statistics
    stats = {}
    for category, reports in categorized.items():
        stats[category] = len(reports)

    stats_content = "## 📊 统计\n\n| 类型 | 数量 |\n|------|------|\n"
    for category in sorted(stats.keys(), key=lambda x: -stats[x]):
        stats_content += f"| {category} | {stats[category]} |\n"
    stats_content += f"| **总计** | **{len(reports)}** |\n"

    # Update stats section
    stats_start = content.find('## 📊 统计')
    stats_end = content.find('---', stats_start + 1)

    if stats_start > 0 and stats_end > stats_start:
        new_content = content[:stats_start] + stats_content + '\n\n' + content[stats_end:]

        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("Updated statistics section")

    print("\nCategory breakdown:")
    for category in sorted(stats.keys(), key=lambda x: -stats[x]):
        print(f"  {category}: {stats[category]}")

if __name__ == "__main__":
    main()
