#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建Windows可执行文件的脚本
使用PyInstaller将Python应用打包成exe文件
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安装成功")
    except Exception as e:
        print(f"❌ PyInstaller 安装失败: {e}")
        return False
    return True

def build_executable():
    """构建可执行文件"""
    try:
        # PyInstaller命令
        cmd = [
            "pyinstaller",
            "--onefile",                    # 打包成单个文件
            "--windowed",                   # 不显示控制台窗口
            "--name", "育儿视频生成器",        # 可执行文件名称
            "--icon", "icon.ico",           # 图标文件（如果存在）
            "--add-data", "assets;assets",  # 包含素材文件夹
            "--add-data", "config;config",  # 包含配置文件夹
            "--hidden-import", "tkinter",
            "--hidden-import", "customtkinter",
            "--hidden-import", "edge_tts",
            "--hidden-import", "openai",
            "--hidden-import", "moviepy",
            "--hidden-import", "PIL",
            "desktop_app.py"                # 主程序文件
        ]
        
        print("🔨 开始构建可执行文件...")
        print(f"命令: {' '.join(cmd)}")
        
        subprocess.check_call(cmd)
        
        print("✅ 可执行文件构建成功！")
        print("📁 文件位置: dist/育儿视频生成器.exe")
        
    except Exception as e:
        print(f"❌ 构建失败: {e}")
        return False
    
    return True

def create_installer_script():
    """创建安装脚本"""
    installer_script = """
@echo off
echo 🚀 育儿卡通视频一键通 - 安装程序
echo =======================================

:: 创建安装目录
set "INSTALL_DIR=%USERPROFILE%\\育儿视频生成器"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 复制文件
echo 📂 正在复制文件...
copy "育儿视频生成器.exe" "%INSTALL_DIR%\\"
xcopy /E /I "assets" "%INSTALL_DIR%\\assets"
xcopy /E /I "config" "%INSTALL_DIR%\\config"

:: 创建桌面快捷方式
echo 🔗 创建桌面快捷方式...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\育儿视频生成器.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\育儿视频生成器.exe'; $Shortcut.Save()"

:: 创建开始菜单快捷方式
echo 📝 创建开始菜单快捷方式...
set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\\育儿视频生成器.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\育儿视频生成器.exe'; $Shortcut.Save()"

echo ✅ 安装完成！
echo 📱 您可以在桌面或开始菜单找到"育儿视频生成器"
pause
    """
    
    with open("install.bat", "w", encoding="gbk") as f:
        f.write(installer_script)
    
    print("✅ 安装脚本创建成功: install.bat")

def main():
    """主函数"""
    print("🎬 育儿卡通视频一键通 - 构建工具")
    print("=" * 50)
    
    # 检查是否在Windows系统
    if os.name != 'nt':
        print("❌ 此脚本仅支持Windows系统")
        return
    
    # 检查主程序文件是否存在
    if not Path("desktop_app.py").exists():
        print("❌ 找不到主程序文件 desktop_app.py")
        return
    
    # 安装PyInstaller
    print("1. 安装PyInstaller...")
    if not install_pyinstaller():
        return
    
    # 构建可执行文件
    print("\n2. 构建可执行文件...")
    if not build_executable():
        return
    
    # 创建安装脚本
    print("\n3. 创建安装脚本...")
    create_installer_script()
    
    print("\n" + "=" * 50)
    print("🎉 构建完成！")
    print("\n📋 使用说明:")
    print("1. 可执行文件: dist/育儿视频生成器.exe")
    print("2. 安装脚本: install.bat")
    print("3. 运行install.bat可以将程序安装到系统中")
    
if __name__ == "__main__":
    main()