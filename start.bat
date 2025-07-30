@echo off
chcp 65001 > nul
:: 育儿卡通视频一键通 - Windows启动脚本

echo 🚀 启动育儿卡通视频一键通...

:: 检查Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8或更高版本
    echo 📥 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python检查通过

:: 检查依赖
echo 🔍 检查依赖包...

python -c "import tkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 缺少tkinter，请重新安装Python并确保包含tkinter
    pause
    exit /b 1
)

:: 启动桌面应用
echo 🎬 启动桌面应用...
python desktop_app.py

echo 👋 应用已关闭
pause