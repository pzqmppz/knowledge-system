#!/bin/bash
# 口播稿监听脚本启动器 (Linux/Mac)

set -e

echo "============================================"
echo "口播稿自动监听脚本"
echo "============================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python 3.7+"
    exit 1
fi

# 获取脚本所在目录
cd "$(dirname "$0")"

# 检查依赖是否安装
if ! python3 -c "import watchdog" &> /dev/null; then
    echo "正在安装依赖..."
    pip3 install -r watch_voiceover_requirements.txt
fi

# 运行监听脚本
echo "启动监听脚本..."
echo ""
python3 watch_voiceover.py
