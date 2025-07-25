#!/bin/bash
# 育儿卡通视频一键通 - Linux启动脚本

echo "🚀 启动育儿卡通视频一键通..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

# 检查Python版本
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: Python版本过低 ($python_version)，需要Python 3.8或更高版本"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 检查依赖
echo "🔍 检查依赖包..."

if ! python3 -c "import customtkinter" 2>/dev/null; then
    echo "📦 安装缺失的依赖包..."
    if ! pip3 install -r requirements.txt; then
        echo "❌ 依赖安装失败，尝试使用备用方法..."
        pip3 install --user customtkinter edge-tts requests openai
    fi
fi

echo "✅ 依赖检查完成"

# 启动应用
echo "🎬 启动应用..."
python3 main.py

echo "👋 应用已关闭"