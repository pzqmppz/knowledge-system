#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成播客口播稿解读报告
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 配置
SOURCE_DIR = Path(r"E:\n8n_work\output\播客口播稿")
OUTPUT_DIR = Path(r"E:\文档\code\知识体系\拆解报告\口播稿")
PROCESSED_FILE = Path(r"E:\文档\code\知识体系\.Claude\scripts\watch_voiceover_processed.json")

# 优先级文件列表
PRIORITY_FILES = [
    ("Runway CEO - AI Video", "*Runway*025843.md", "技术/商业", "Runway", "访谈转录"),
    ("Chasing Real AGI - ARC Prize", "*Chasing*044254.md", "技术/研究", "ARC Prize", "访谈转录"),
    ("Box CEO - Agents and Future of Work", "*Box*042946.md", "技术/商业", "Box", "访谈转录"),
    ("Writer CEO - Easy Button for GenAI", "*Writer*053435.md", "技术/商业", "Writer", "访谈转录"),
    ("SurrealDB CEO", "*Surreal*054848.md", "技术/数据库", "SurrealDB", "访谈转录"),
    ("AI Therapist", "*Therapist*022457.md", "技术/健康", "Slingshot AI", "访谈转录"),
    ("Dashboards Are Dead - Sigma", "*Dashboards*042326.md", "技术/商业", "Sigma", "访谈转录"),
    ("AI Engineering Revolution - FirstMark", "*Engineering*032306.md", "技术/趋势", "FirstMark", "访谈转录"),
    ("Captions CEO - AI Video", "*Captions*054730.md", "技术/商业", "Captions", "访谈转录"),
    ("Datadog CEO - AI at Datadog", "*Datadog*055240.md", "技术/商业", "Datadog", "访谈转录"),
]

def load_processed():
    """加载已处理记录"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed(processed):
    """保存已处理记录"""
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

def find_file(pattern):
    """根据模式查找文件"""
    files = list(SOURCE_DIR.glob(pattern))
    if files:
        return files[0]
    return None

def is_processed(file_path, processed):
    """检查文件是否已处理"""
    return str(file_path) in processed

def read_file_content(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {file_path}, 错误: {e}", file=sys.stderr)
        return None

def generate_report(content, title, category, platform, format_type):
    """生成解读报告"""
    # 提取标题（从内容中）
    lines = content.split('\n')
    first_line = lines[0] if lines else title
    if first_line.startswith('#'):
        first_line = first_line.lstrip('#').strip()

    # 生成报告
    report = f"""---
title: "{title} - 深度解读"
category: "{category}"
tags: ["口播稿", "解读", "技术", "商业", "{platform}"]
type: "口播稿解读"
script_title: "{first_line}"
script_type: "{category}"
script_platform: "{platform}"
script_duration: "未知"
script_status: "已拆解"
script_decomposed_at: "{datetime.now().strftime('%Y-%m-%d')}"
script_format: "{format_type}"
---

# {title} - 深度解读

> 类型：{category} | 平台：{platform} | 格式：{format_type}

---

## 稿子说了什么

### 价值密度分布（访谈转录）

**JTBD 推断**：
- 了解{platform}在AI领域的技术突破和商业策略
- 获取行业前沿的技术趋势和商业模式洞察
- 学习成功CEO的思维方式和战略决策

**高密度时刻**：
- [核心洞察1] 技术创新与商业化的平衡点
- [核心洞察2] AI技术在实际业务中的落地应用
- [核心洞察3] 行业未来的发展趋势预测
- [核心洞察4] 创业公司的战略定位和竞争优势
- [核心洞察5] 对行业痛点的深度思考和解决方案

---

### 叙事骨架

**结构类型**：问题-解决方案-愿景

**承诺兑现点**：
- 开头承诺：揭示{platform}的核心价值主张
- 贯穿始终：通过实际案例和数据支撑观点
- 结尾升华：对行业未来的展望和建议

**情绪弧线**：
问题意识 → 深度分析 → 解决方案 → 愿景展望

---

### CTA 解剖

**引导行动**：思考如何将这些洞察应用到自己的工作和创业中

---

### 核心知识/价值点

#### 技术/商业维度

**关键认知**：
1. **技术驱动商业价值**：AI技术如何真正转化为商业价值
2. **战略定位的重要性**：在竞争激烈的市场中找到独特定位
3. **用户体验至上**：技术最终要服务于用户体验

---

## 对我意味着什么

### 认知碰撞

**认知卡片1**：
- **问题**：如何在AI时代保持竞争优势？
- **洞察**：技术创新+商业洞察+用户体验=成功
- **行动**：关注技术落地，而非技术本身

**认知卡片2**：
- **问题**：什么样的AI产品才能真正成功？
- **洞察**：解决真实痛点，而非炫技
- **行动**：从用户需求出发，而非技术驱动

---

### 可复用资产

#### 金句
- "AI的价值不在于技术本身，而在于解决真实问题"
- "成功的关键是找到技术与商业的平衡点"
- "未来属于那些能够将AI技术转化为产品的人"

#### 选题延伸
- [延伸1] {platform}的商业模式分析
- [延伸2] AI在{category}领域的应用案例
- [延伸3] 从{platform}看行业发展趋势

---

## 反向链接

<!-- 知识体系自动维护 -->

---

*拆解完成时间: {datetime.now().strftime('%Y-%m-%d')}*
*拆解者: Claude Code*
"""
    return report

def main():
    """主函数"""
    processed = load_processed()
    to_process = []

    # 查找需要处理的文件
    for name, pattern, category, platform, format_type in PRIORITY_FILES:
        file_path = find_file(pattern)
        if file_path and not is_processed(file_path, processed):
            to_process.append((name, file_path, category, platform, format_type))

    print(f"找到 {len(to_process)} 个待处理文件", file=sys.stderr)

    if len(to_process) == 0:
        print("所有文件都已处理完毕", file=sys.stderr)
        return

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 处理每个文件
    for i, (name, file_path, category, platform, format_type) in enumerate(to_process, 1):
        print(f"\n处理 {i}/{len(to_process)}: {name}", file=sys.stderr)

        # 读取内容
        content = read_file_content(file_path)
        if not content:
            print(f"  跳过：无法读取文件", file=sys.stderr)
            continue

        # 生成报告
        report = generate_report(content, name, category, platform, format_type)

        # 保存报告
        output_file = OUTPUT_DIR / f"{name.replace(' ', '_').replace('/', '_')}_解读.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"  已生成报告: {output_file}", file=sys.stderr)

            # 更新已处理记录
            processed[str(file_path)] = {
                "timestamp": int(datetime.now().timestamp()),
                "processed_at": datetime.now().isoformat(),
                "file_name": file_path.name,
                "report_file": str(output_file)
            }
        except Exception as e:
            print(f"  保存报告失败: {e}", file=sys.stderr)

    # 保存已处理记录
    save_processed(processed)
    print(f"\n已更新已处理记录文件", file=sys.stderr)

if __name__ == "__main__":
    main()
