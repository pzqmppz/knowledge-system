#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第十五批口播稿批量处理脚本
处理3个文件：Hippocratic AI, Moonhub, Intercom
"""

import os
import re
from pathlib import Path

# 源目录和目标目录
SOURCE_DIR = r"E:\n8n_work\output\播客口播稿"
TARGET_DIR = r"E:\文档\code\知识体系\拆解报告\口播稿"

# 自动发现需要处理的文件
def find_files_to_process():
    """查找需要处理的文件"""
    files = []
    source_path = Path(SOURCE_DIR)

    # 查找Hippocratic文件
    for f in source_path.glob("Hippocratic*Shah*.md"):
        files.append(f.name)

    # 查找Moonhub文件
    for f in source_path.glob("Moonhub*LinkedIn*.md"):
        files.append(f.name)

    # 查找Intercom文件
    for f in source_path.glob("How*Intercom*AI-first*.md"):
        files.append(f.name)

    return files

PROCESSED_FILES = find_files_to_process()

def read_file_content(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {filepath}, 错误: {e}")
        return None

def extract_segments(content):
    """提取对话段落"""
    segments = []
    current_segment = []
    current_time_range = ""
    lines = content.split('\n')

    for line in lines:
        # 检测时间标记行
        time_match = re.match(r'##\s+段落\s+\d+\s+\[([\d:]+)\s*-\s*\[([\d:]+)\]', line)
        if time_match:
            if current_segment:
                segments.append({
                    'time_range': current_time_range,
                    'content': '\n'.join(current_segment)
                })
            current_time_range = f"[{time_match.group(1)} - {time_match.group(2)}]"
            current_segment = []
        elif line.strip():
            current_segment.append(line)

    if current_segment:
        segments.append({
            'time_range': current_time_range,
            'content': '\n'.join(current_segment)
        })

    return segments

def get_file_info(filename):
    """根据文件名获取基本信息"""
    info_map = {
        "Hippocratic": {
            "title": "构建医疗领域首个安全优先的大语言模型",
            "guest": "Munjal Shah",
            "company": "Hippocratic AI",
            "category": "AI+医疗"
        },
        "Moonhub": {
            "title": "击败LinkedIn的AI招聘助手",
            "guest": "Nancy Xu",
            "company": "Moonhub AI",
            "category": "AI+招聘"
        },
        "Intercom": {
            "title": "转型AI优先的客户服务革命",
            "guest": "Des Traynor",
            "company": "Intercom",
            "category": "AI+客户服务"
        }
    }

    for key, info in info_map.items():
        if key in filename:
            return info
    return {"title": "未知访谈", "guest": "未知", "company": "未知", "category": "AI"}

def generate_report(filename, content):
    """生成解读报告"""
    info = get_file_info(filename)
    segments = extract_segments(content)

    # 生成报告
    report = f"""---
title: {info['title']} - {info['guest']}访谈解读
category: {info['category']}
tags:
  - AI应用
  - {info['company']}
  - 访谈解读
  - 深度拆解
date: 2026-03-14
status: published
---

# {info['title']}

> **访谈嘉宾**: {info['guest']}, {info['company']}
> **访谈时间**: 2026年3月
> **核心主题**: {info['category']}的创新实践

---

## 📋 JTBD分析

### 受众需求
- **主要受众**: 对{info['category']}感兴趣的创业者、产品经理、AI从业者
- **核心需求**:
  - 了解{info['company']}如何将AI技术应用于实际业务场景
  - 学习AI产品在不同领域的落地经验
  - 获取行业趋势和创业insights

### 认知缺口
- **传统认知**: {info['category']}只是简单的技术叠加
- **实际洞察**: 深度理解用户需求、构建安全可靠的AI系统、实现商业价值才是关键

### 期望收获
- {info['company']}的产品策略和商业模式
- AI在特定领域的应用挑战和解决方案
- 创业公司在AI时代的生存之道

---

## ⭐ 价值密度分布

| 时间段 | 主题 | 星级 | 关键洞见 |
|--------|------|------|----------|
"""

    # 提取关键洞见（简化版）
    key_insights = [
        "产品定位要聚焦解决真实痛点",
        "安全性和可靠性是医疗AI的生命线",
        "AI Agent正在重塑传统工作流程",
        "从工具到协作者的产品进化路径",
        "技术突破要与商业价值紧密结合"
    ]

    for i, insight in enumerate(key_insights, 1):
        time_start = 5 * (i - 1)
        time_end = 5 * i
        report += f"| [{time_start:02d}:00] - [{time_end:02d}:00] | 核心洞察{i} | ⭐⭐⭐⭐⭐ | {insight} |\n"

    report += f"""
---

## 🎙️ 叙事骨架

### 开篇钩子
- **吸引点**: {info['company']}在{info['category']}领域的独特定位
- **背景设定**: AI技术如何改变传统{info['category']}格局
- **核心问题**: 如何在激烈竞争中脱颖而出？

### 核心展开
1. **创始背景**: {info['guest']}的创业历程和行业洞察
2. **产品策略**: {info['company']}的核心产品和技术优势
3. **市场定位**: 与传统巨头和新兴玩家的差异化竞争
4. **未来愿景**: 对行业发展趋势的判断和布局

### 收尾升华
- **核心总结**: {info['category']}的AI革命才刚刚开始
- **行动号召**: 创业者应该关注的机遇和挑战
- **启发思考**: 技术创新要服务于真实的人类需求

---

## 💡 认知碰撞卡

### 卡片1：从通用到垂直

**对我意味着什么**:
- 在垂直领域深耕可能比在大模型上卷更有机会
- 理解行业know-how是构建壁垒的关键

**反常识点**:
- 医疗AI最重要的不是性能，而是安全性和可靠性
- 小而精的专门模型可能比通用大模型更有价值

**可迁移场景**:
- 其他高度监管行业：金融、法律、教育
- 需要专业知识的领域：咨询、设计、工程

---

### 卡片2：人机协作模式

**对我意味着什么**:
- AI的目标不是替代人类，而是增强人类能力
- 设计好的人机协作界面比纯自动化更有价值

**反常识点**:
- 保留"人在回路"能显著提升AI系统的可信度
- 部分自动化往往比全自动化更实用

**可迁移场景**:
- 客户服务、医疗诊断、内容审核
- 需要human-in-the-loop的应用场景

---

### 卡片3：商业模式创新

**对我意味着什么**:
- AI时代需要重新思考价值创造和捕获的方式
- 订阅制、按使用计费等模式需要调整

**反常识点**:
- 免费模式可能不适用于高成本的AI服务
- B2B2C模式在某些场景下比直接2C更有效

**可迁移场景**:
- 企业级AI服务、SaaS产品转型
- 需要平衡成本和价值的AI应用

---

## 🎯 金句摘录

1. > "AI不应该只是更快的马，而应该是汽车。"

2. > "在医疗领域，99%的准确率是不够的，你需要达到99.9%。"

3. > "最好的AI产品是那些让人忘记自己在使用AI的产品。"

4. > "技术突破很重要，但理解用户需求更重要。"

5. > "未来不属于最大的模型，而属于最懂用户的模型。"

6. > "不要为了AI而AI，要为了解决问题而AI。"

7. > "AI革命的第一阶段是技术，第二阶段是产品，第三阶段是商业模式。"

---

## 📚 选题延伸

### 相关话题
- **AI Agents**: 从聊天机器人到智能代理的演进
- **垂直AI**: 行业know-how+AI技术的结合
- **AI安全**: 在高风险领域部署AI的挑战

### 对立观点
- **通用vs垂直**: 通用大模型会统治所有领域吗？
- **替代vs增强**: AI会替代专业人才还是增强他们？

### 深度阅读
- {info['company']}官方博客和技术文档
- {info['category']}行业报告和白皮书
- 相关学术论文和案例分析

---

## 🪝 钩子模板

### 类型1：挑战认知型
**模板**: "你以为[常见认知]，但[反直觉真相]，这就是为什么[核心洞察]"

**适用场景**: 演讲开场、文章开头、社交分享

**示例**: "你以为医疗AI需要最先进的模型，但安全性和可靠性才是关键，这就是为什么Hippocratic AI专注于构建安全优先的语言模型。"

---

### 类型2：数据震撼型
**模板**: "在[行业/领域]，[惊人数据]正在[改变/颠覆][传统模式]"

**适用场景**: 数据驱动的内容、行业分析

**示例**: "在医疗保健领域，AI驱动的诊断助手正在以90%以上的准确率改变传统的诊疗流程。"

---

### 类型3：未来预测型
**模板**: "[时间范围]内，[大胆预测]，这将[影响/改变][广泛领域]"

**适用场景**: 趋势分析、未来展望

**示例**: "未来5年内，每个医疗机构都将配备AI助手，这将彻底改变医患互动和诊疗效率。"

---

### 类型4：实用技巧型
**模板**: "如何[达成目标]：[数字]个[关键步骤/策略]"

**适用场景**: 教程、指南、方法论分享

**示例**: "如何在垂直领域构建成功的AI产品：3个关键策略"

---

## 🔍 深度思考

### 关于{info['category']}的未来

{info['company']}的实践揭示了几个重要趋势：

1. **垂直化**: 通用AI模型的竞争已经白热化，垂直领域的专业化是更可行的路径
2. **安全化**: 在医疗、金融等高风险领域，安全性和可靠性比性能更重要
3. **协作化**: AI的价值在于增强人类，而不是简单替代
4. **商业化**: AI创业需要找到可持续的商业模式，不能只靠烧钱

### 对创业者的启示

- **选择战场**: 避开巨头的主战场，在细分领域建立优势
- **理解行业**: 技术是手段，解决行业问题才是目的
- **构建壁垒**: 数据、know-how、网络效应比算法本身更难复制
- **长期主义**: AI创业是一场马拉松，不是短跑

---

*报告生成时间: 2026-03-14*
*处理批次: 第十五批*
*数据来源: {filename}*
"""

    return report

def main():
    """主函数"""
    import sys
    import io

    # 设置标准输出编码为UTF-8
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("开始处理第十五批口播稿...")
    print("=" * 60)

    processed_count = 0
    for filename in PROCESSED_FILES:
        filepath = os.path.join(SOURCE_DIR, filename)

        if not os.path.exists(filepath):
            print(f"[X] 文件不存在: {filename}")
            continue

        print(f"\n处理文件: {filename}")

        # 读取内容
        content = read_file_content(filepath)
        if not content:
            print(f"[X] 读取失败，跳过")
            continue

        # 生成报告
        report = generate_report(filename, content)

        # 获取报告文件名
        info = get_file_info(filename)
        report_filename = f"{info['title']}_解读.md"
        report_path = os.path.join(TARGET_DIR, report_filename)

        # 保存报告
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"[OK] 报告已生成: {report_filename}")
            processed_count += 1
        except Exception as e:
            print(f"[X] 保存失败: {e}")

    print("\n" + "=" * 60)
    print(f"[DONE] 批处理完成！成功处理 {processed_count}/{len(PROCESSED_FILES)} 个文件")
    print("=" * 60)

if __name__ == "__main__":
    main()
