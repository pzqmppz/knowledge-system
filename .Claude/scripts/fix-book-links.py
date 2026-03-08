#!/usr/bin/env python3
"""
修复书籍拆解报告之间的互相引用
将 [[书名]] 修复为 [[书名-拆解报告]]
"""

import re
from pathlib import Path

# 书籍列表（从 拆解报告/书籍/ 目录获取）
BOOKS = [
    "The Beginning of Infinity",
    "Apple in China",
    "Breakneck",
    "High Output Management",
    "从0到1",
    "从零构建大模型",
    "创业维艰",
    "别闹了，费曼先生",
    "原则",
    "反脆弱",
    "孙子兵法",
    "弗兰克尔自传",
    "思考快与慢",
    "沉思录",
    "理性乐观派",
    "穷查理宝典",
]

VAULT_PATH = Path(__file__).parent.parent.parent
REPORTS_DIR = VAULT_PATH / "拆解报告" / "书籍"

def fix_links():
    """修复书籍报告中的链接"""
    changed_count = 0
    file_count = 0

    for md_file in REPORTS_DIR.glob("*.md"):
        if not md_file.is_file():
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 修复每个书名的链接
        for book in BOOKS:
            # 匹配 [[书名]] 但不匹配 [[书名-拆解报告]] 或 [[书名|...]]
            # 使用负向后查找和负向前瞻
            pattern = rf'\[\[{re.escape(book)}(?![\-|])\]\]'
            replacement = f'[[{book}-拆解报告]]'
            content = re.sub(pattern, replacement, content)

        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)

            file_count += 1
            changes = content.count('-拆解报告') - original_content.count('-拆解报告')
            changed_count += changes
            print(f"[Fixed] {md_file.name}: {changes} links")

    print()
    print(f"[Summary] {file_count} files updated, {changed_count} links fixed")

if __name__ == '__main__':
    print("[Fix] Starting book link fix...")
    fix_links()
    print("[Done] Fix complete!")
