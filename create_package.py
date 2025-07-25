#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿卡通视频一键通 - 项目打包脚本
将所有必要文件打包成压缩文件，方便分发
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_package():
    """创建项目压缩包"""
    
    # 定义需要打包的文件
    files_to_package = [
        # 核心启动文件
        "desktop_app.py",
        "start.bat", 
        "requirements.txt",
        
        # 核心模块
        "src/script_generator.py",
        "src/tts_generator.py",
        "src/asset_manager.py", 
        "src/video_composer.py",
        "src/video_generator.py",
        "src/main_gui.py",
        
        # 配置文件
        "config/config.py",
        
        # 文档
        "README.md",
        "DESKTOP_SETUP.md",
        "DESKTOP_COMPLETE.md",
        "DOWNLOAD_GUIDE.md",
        "FILE_LIST.md",
        
        # 测试工具
        "test_desktop.py",
        "demo.py",
        "test_app.py",
        
        # 构建工具
        "build_exe.py",
        "setup.py",
        "quick_install.bat",
    ]
    
    # 创建临时打包目录
    package_dir = Path("育儿视频生成器")
    
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    print("🏗️ 创建项目目录结构...")
    
    # 创建子目录
    (package_dir / "src").mkdir()
    (package_dir / "config").mkdir()
    (package_dir / "assets" / "images" / "backgrounds").mkdir(parents=True)
    (package_dir / "assets" / "images" / "characters").mkdir(parents=True)
    (package_dir / "assets" / "images" / "props").mkdir(parents=True)
    (package_dir / "assets" / "music" / "background").mkdir(parents=True)
    (package_dir / "assets" / "audio" / "temp").mkdir(parents=True)
    (package_dir / "output").mkdir()
    
    print("📄 复制项目文件...")
    
    # 复制文件
    copied_count = 0
    for file_path in files_to_package:
        source = Path(file_path)
        if source.exists():
            dest = package_dir / file_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            print(f"  ✅ {file_path}")
            copied_count += 1
        else:
            print(f"  ⚠️ 文件不存在: {file_path}")
    
    # 创建说明文件
    readme_content = """# 育儿卡通视频一键通

## 快速开始

### Windows用户
1. 双击 start.bat 启动应用
2. 等待依赖安装完成
3. 开始使用图形界面创建视频

### 其他系统
1. 安装Python 3.8+
2. 运行: pip install -r requirements.txt
3. 运行: python desktop_app.py

## 详细说明
请查看 DESKTOP_SETUP.md 文件获取详细的安装和使用说明。

## 文件说明
- desktop_app.py: 主桌面应用程序
- src/: 核心功能模块
- config/: 配置文件
- assets/: 素材文件夹（程序会自动创建示例文件）
- output/: 生成的视频输出文件夹

祝您使用愉快！
"""
    
    with open(package_dir / "使用说明.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"\n📦 创建压缩包...")
    
    # 创建ZIP压缩包
    zip_filename = "育儿卡通视频一键通.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                # 使用相对于package_dir的路径作为archive名称
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    # 获取压缩包大小
    zip_size = os.path.getsize(zip_filename) / 1024  # KB
    
    print("\n" + "="*60)
    print("🎉 打包完成！")
    print("="*60)
    print(f"📁 压缩包名称: {zip_filename}")
    print(f"📊 压缩包大小: {zip_size:.1f} KB")
    print(f"📄 包含文件数: {copied_count}")
    print(f"📍 当前位置: {Path.cwd() / zip_filename}")
    
    print("\n📋 压缩包内容:")
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        for name in sorted(zipf.namelist()):
            print(f"  📄 {name}")
    
    print("\n🚀 使用方法:")
    print("1. 下载压缩包到您的电脑")
    print("2. 解压到任意文件夹")
    print("3. 双击 start.bat (Windows) 或运行 python desktop_app.py")
    print("4. 开始创建育儿视频！")
    
    # 清理临时目录
    shutil.rmtree(package_dir)
    
    return zip_filename

if __name__ == "__main__":
    print("🎬 育儿卡通视频一键通 - 项目打包工具")
    print("="*60)
    
    try:
        zip_file = create_package()
        print(f"\n✅ 压缩包创建成功: {zip_file}")
    except Exception as e:
        print(f"\n❌ 打包失败: {e}")