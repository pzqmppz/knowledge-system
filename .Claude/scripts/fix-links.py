#!/usr/bin/env python3
"""
知识链接同步脚本
自动更新因文件移动/重命名而失效的双向链接
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 配置
VAULT_PATH = Path(__file__).parent.parent.parent
LINK_MAP_FILE = Path(__file__).parent / "link-map.json"

def extract_wikilinks(content):
    """提取文本中的所有 wikilinks"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)

def build_link_index(vault_path):
    """建立文件索引：文件路径 -> 可能的链接名"""
    index = {}

    for md_file in vault_path.rglob("*.md"):
        # 跳过隐藏目录和 git-ignored 目录
        if any(part.startswith('.') for part in md_file.parts):
            continue

        relative_path = md_file.relative_to(vault_path)
        filename = md_file.stem

        # 记录多种可能的链接格式
        index[filename] = str(relative_path)
        index[str(relative_path)] = str(relative_path)
        index[str(relative_path.with_suffix(''))] = str(relative_path)

        # 记录带目录的格式
        if len(relative_path.parts) > 1:
            parent = str(relative_path.parent)
            index[f"{parent}/{filename}"] = str(relative_path)
            index[f"{parent}\\{filename}"] = str(relative_path)

    return index

def scan_broken_links(vault_path, link_index):
    """扫描所有失效链接"""
    broken = {}

    for md_file in vault_path.rglob("*.md"):
        if any(part.startswith('.') for part in md_file.parts):
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            links = extract_wikilinks(content)

        for link in links:
            # 处理别名格式 [[文件名|显示名]]
            link_target = link.split('|')[0].strip()

            # 检查链接是否有效
            if link_target not in link_index:
                if md_file not in broken:
                    broken[md_file] = []
                broken[md_file].append(link_target)

    return broken

def fix_links(vault_path, old_path, new_path, dry_run=True):
    """批量替换链接"""
    old_name = Path(old_path).stem
    new_name = Path(new_path).stem
    old_relative = str(Path(old_path).relative_to(vault_path))
    new_relative = str(Path(new_path).relative_to(vault_path))

    # 可能的旧链接格式
    old_patterns = [
        f"[[{old_name}]]",
        f"[[{old_relative}]]",
        f"[[{old_relative.with_suffix('')}]]",
    ]

    # 新链接格式
    new_link = f"[[{new_relative.with_suffix('')}]]"

    changed_files = []

    for md_file in vault_path.rglob("*.md"):
        if any(part.startswith('.') for part in md_file.parts):
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 替换所有旧链接格式
        for pattern in old_patterns:
            content = content.replace(pattern, new_link)

        if content != original_content:
            if not dry_run:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            changed_files.append(str(md_file.relative_to(vault_path)))

    return changed_files

def main():
    import argparse
    import sys

    # 修复 Windows 编码问题
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description='知识链接同步工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 扫描失效链接
    subparsers.add_parser('scan', help='扫描所有失效链接')

    # 修复链接
    fix_parser = subparsers.add_parser('fix', help='修复链接')
    fix_parser.add_argument('--old', required=True, help='旧路径')
    fix_parser.add_argument('--new', required=True, help='新路径')
    fix_parser.add_argument('--apply', action='store_true', help='实际执行修改')

    args = parser.parse_args()

    print(f"[知识库] 路径: {VAULT_PATH}")
    print()

    if args.command == 'scan':
        print("[扫描] 正在建立链接索引...")
        link_index = build_link_index(VAULT_PATH)
        print(f"[完成] 索引建立完成，共 {len(link_index)} 个文件")

        print("[扫描] 正在扫描失效链接...")
        broken = scan_broken_links(VAULT_PATH, link_index)

        if broken:
            print(f"\n[发现] {len(broken)} 个文件包含失效链接：\n")
            for file, links in broken.items():
                print(f"  FILE: {file.relative_to(VAULT_PATH)}")
                for link in links:
                    print(f"     -> [[{link}]]")
        else:
            print("[完成] 没有发现失效链接！")

    elif args.command == 'fix':
        old_path = Path(args.old).absolute()
        new_path = Path(args.new).absolute()

        if not old_path.exists():
            print(f"[错误] 旧路径不存在: {old_path}")
            return

        print(f"[修复] 链接更新")
        print(f"   旧路径: {old_path}")
        print(f"   新路径: {new_path}")
        print()

        changed = fix_links(VAULT_PATH, old_path, new_path, dry_run=not args.apply)

        if changed:
            print(f"[更新] 将修改 {len(changed)} 个文件：")
            for file in changed:
                print(f"   - {file}")

            if not args.apply:
                print()
                print("[预览] 这是预览模式，使用 --apply 参数实际执行修改")
            else:
                print()
                print("[完成] 链接已更新！")
        else:
            print("[信息] 没有找到需要更新的链接")

if __name__ == '__main__':
    main()
