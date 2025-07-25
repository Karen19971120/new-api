@echo off
chcp 65001 > nul
cls

echo ========================================
echo   🎬 育儿卡通视频一键通 - 快速安装
echo ========================================
echo.

:: 检查Python
echo 🔍 检查Python环境...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python，请先安装Python！
    echo 📥 下载地址: https://www.python.org/downloads/
    echo 💡 安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python环境检查通过
echo.

:: 创建项目文件夹
echo 📁 创建项目文件夹...
set "PROJECT_DIR=%USERPROFILE%\Desktop\育儿视频生成器"

if exist "%PROJECT_DIR%" (
    echo ⚠️ 项目文件夹已存在，将覆盖更新
) else (
    mkdir "%PROJECT_DIR%"
)

:: 创建子文件夹
mkdir "%PROJECT_DIR%\src" 2>nul
mkdir "%PROJECT_DIR%\config" 2>nul
mkdir "%PROJECT_DIR%\assets\images\backgrounds" 2>nul
mkdir "%PROJECT_DIR%\assets\images\characters" 2>nul
mkdir "%PROJECT_DIR%\assets\images\props" 2>nul
mkdir "%PROJECT_DIR%\assets\music\background" 2>nul
mkdir "%PROJECT_DIR%\assets\audio\temp" 2>nul
mkdir "%PROJECT_DIR%\output" 2>nul

echo ✅ 文件夹结构创建完成
echo.

:: 创建核心文件（这里应该是复制实际文件的逻辑）
echo 📄 创建项目文件...

:: 创建requirements.txt
echo # 育儿卡通视频一键通 - 依赖库 > "%PROJECT_DIR%\requirements.txt"
echo. >> "%PROJECT_DIR%\requirements.txt"
echo # GUI框架 >> "%PROJECT_DIR%\requirements.txt"
echo tkinter >> "%PROJECT_DIR%\requirements.txt"
echo. >> "%PROJECT_DIR%\requirements.txt"
echo # 视频处理 >> "%PROJECT_DIR%\requirements.txt"
echo moviepy==1.0.3 >> "%PROJECT_DIR%\requirements.txt"
echo Pillow==10.1.0 >> "%PROJECT_DIR%\requirements.txt"
echo numpy^>=1.21.0 >> "%PROJECT_DIR%\requirements.txt"
echo. >> "%PROJECT_DIR%\requirements.txt"
echo # 语音合成 >> "%PROJECT_DIR%\requirements.txt"
echo edge-tts==6.1.12 >> "%PROJECT_DIR%\requirements.txt"
echo. >> "%PROJECT_DIR%\requirements.txt"
echo # LLM API调用 >> "%PROJECT_DIR%\requirements.txt"
echo openai==1.3.8 >> "%PROJECT_DIR%\requirements.txt"
echo requests==2.31.0 >> "%PROJECT_DIR%\requirements.txt"
echo. >> "%PROJECT_DIR%\requirements.txt"
echo # 数据处理 >> "%PROJECT_DIR%\requirements.txt"
echo pydub==0.25.1 >> "%PROJECT_DIR%\requirements.txt"

:: 创建启动脚本
echo @echo off > "%PROJECT_DIR%\start.bat"
echo chcp 65001 ^> nul >> "%PROJECT_DIR%\start.bat"
echo echo 🚀 启动育儿卡通视频一键通... >> "%PROJECT_DIR%\start.bat"
echo python desktop_app.py >> "%PROJECT_DIR%\start.bat"
echo pause >> "%PROJECT_DIR%\start.bat"

:: 创建简单的说明文件
echo # 育儿卡通视频一键通 > "%PROJECT_DIR%\README.txt"
echo. >> "%PROJECT_DIR%\README.txt"
echo 使用说明: >> "%PROJECT_DIR%\README.txt"
echo 1. 双击 start.bat 启动应用 >> "%PROJECT_DIR%\README.txt"
echo 2. 输入育儿关键词 >> "%PROJECT_DIR%\README.txt"
echo 3. 点击生成视频 >> "%PROJECT_DIR%\README.txt"
echo 4. 查看output文件夹中的结果 >> "%PROJECT_DIR%\README.txt"

echo ✅ 基础文件创建完成
echo.

:: 安装依赖
echo 📦 安装Python依赖包...
cd /d "%PROJECT_DIR%"
python -m pip install --user -r requirements.txt

if %errorlevel% neq 0 (
    echo ⚠️ 依赖安装可能有问题，但可以继续
)

echo.
echo ========================================
echo           🎉 安装完成！
echo ========================================
echo.
echo 📍 项目位置: %PROJECT_DIR%
echo.
echo 📋 接下来的步骤:
echo 1. 📄 复制完整的项目文件到该文件夹
echo 2. 🚀 双击 start.bat 启动应用
echo 3. 🎬 开始创建育儿视频！
echo.
echo 💡 提示: 需要将完整的项目文件复制到以上目录
echo    包括 desktop_app.py 和 src/ 文件夹中的所有文件
echo.

:: 打开项目文件夹
echo 📂 打开项目文件夹...
explorer "%PROJECT_DIR%"

echo.
pause