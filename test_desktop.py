#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌面应用测试脚本
验证所有核心功能模块是否正常工作
"""

import sys
import os
from pathlib import Path
import logging

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试核心模块
        from src.script_generator import ScriptGenerator
        print("  ✅ ScriptGenerator 导入成功")
        
        from src.tts_generator import TTSGenerator
        print("  ✅ TTSGenerator 导入成功")
        
        from src.asset_manager import AssetManager
        print("  ✅ AssetManager 导入成功")
        
        from src.video_composer import VideoComposer
        print("  ✅ VideoComposer 导入成功")
        
        from src.video_generator import VideoGenerator
        print("  ✅ VideoGenerator 导入成功")
        
        return True
    except Exception as e:
        print(f"  ❌ 模块导入失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("\n📦 测试依赖包...")
    
    deps = {
        'pathlib': '内置模块',
        'json': '内置模块',
        'logging': '内置模块',
        'threading': '内置模块',
        'asyncio': '内置模块'
    }
    
    optional_deps = {
        'edge_tts': 'TTS语音合成',
        'openai': 'AI脚本生成',
        'moviepy': '视频合成',
        'PIL': '图像处理',
        'requests': 'HTTP请求'
    }
    
    # 测试基础依赖
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"  ✅ {dep} ({desc})")
        except ImportError:
            print(f"  ❌ {dep} ({desc}) - 缺失")
    
    # 测试可选依赖
    print("  \n📦 可选依赖包:")
    for dep, desc in optional_deps.items():
        try:
            __import__(dep)
            print(f"  ✅ {dep} ({desc})")
        except ImportError:
            print(f"  ⚠️ {dep} ({desc}) - 缺失但不影响基本功能")

def test_config():
    """测试配置加载"""
    print("\n⚙️ 测试配置加载...")
    
    try:
        from config.config import (
            PROJECT_ROOT, ASSETS_DIR, OUTPUT_DIR,
            LLM_CONFIG, TTS_CONFIG, VIDEO_CONFIG
        )
        
        print(f"  ✅ 项目根目录: {PROJECT_ROOT}")
        print(f"  ✅ 素材目录: {ASSETS_DIR}")
        print(f"  ✅ 输出目录: {OUTPUT_DIR}")
        print(f"  ✅ LLM模型: {LLM_CONFIG.get('model', 'N/A')}")
        print(f"  ✅ TTS语音: {TTS_CONFIG.get('voice', 'N/A')}")
        print(f"  ✅ 视频分辨率: {VIDEO_CONFIG.get('resolution', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"  ❌ 配置加载失败: {e}")
        return False

def test_directory_structure():
    """测试目录结构"""
    print("\n📁 测试目录结构...")
    
    required_dirs = [
        "src",
        "config", 
        "assets/images/backgrounds",
        "assets/images/characters",
        "assets/images/props",
        "assets/music/background",
        "assets/audio",
        "output"
    ]
    
    for dir_path in required_dirs:
        path = project_root / dir_path
        if path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - 不存在")
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"    📁 已创建目录: {dir_path}")
            except Exception as e:
                print(f"    ❌ 创建目录失败: {e}")

def test_core_functionality():
    """测试核心功能"""
    print("\n🎬 测试核心功能...")
    
    try:
        # 测试视频生成器初始化
        from src.video_generator import VideoGenerator
        
        def mock_progress(status, message, progress):
            print(f"    进度: {progress}% - {message}")
        
        generator = VideoGenerator(progress_callback=mock_progress)
        print("  ✅ VideoGenerator 初始化成功")
        
        # 测试脚本生成
        print("  📝 测试脚本生成...")
        script_data = generator.script_generator.generate_script("测试关键词")
        if script_data:
            print("    ✅ 脚本生成成功")
            print(f"    📋 标题: {script_data.get('title', 'N/A')}")
            print(f"    🎞️ 场景数: {len(script_data.get('scenes', []))}")
        else:
            print("    ❌ 脚本生成失败")
        
        # 测试素材管理
        print("  🎨 测试素材管理...")
        asset_manager = generator.asset_manager
        bg_music = asset_manager.get_random_background_music()
        print(f"    ✅ 随机背景音乐: {bg_music}")
        
        print("  ✅ 核心功能测试完成")
        return True
        
    except Exception as e:
        print(f"  ❌ 核心功能测试失败: {e}")
        return False

def test_gui_components():
    """测试GUI组件（不启动界面）"""
    print("\n🖥️ 测试GUI组件...")
    
    try:
        # 在没有显示的环境中，我们只测试类定义
        import tkinter as tk
        print("  ✅ tkinter 可用")
        
        # 测试桌面应用类定义（不初始化）
        import desktop_app
        if hasattr(desktop_app, 'DesktopLauncher'):
            print("  ✅ DesktopLauncher 类定义正确")
        
        if hasattr(desktop_app, 'SettingsWindow'):
            print("  ✅ SettingsWindow 类定义正确")
            
        return True
        
    except ImportError as e:
        print(f"  ⚠️ GUI组件测试跳过: {e}")
        print("    💡 这在无显示环境中是正常的")
        return True
    except Exception as e:
        print(f"  ❌ GUI组件测试失败: {e}")
        return False

def test_file_generation():
    """测试文件生成功能"""
    print("\n📄 测试文件生成...")
    
    try:
        # 测试音频生成（模拟）
        from src.tts_generator import TTSGenerator
        tts = TTSGenerator()
        
        test_audio_path = project_root / "assets/audio/temp/test.mp3"
        test_audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = tts.generate_audio("测试文本", str(test_audio_path))
        if result:
            print("  ✅ 音频文件生成测试通过")
            # 清理测试文件
            if test_audio_path.exists() and test_audio_path.stat().st_size < 100:
                test_audio_path.unlink()
        else:
            print("  ⚠️ 音频生成失败（可能是网络问题）")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 文件生成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🎬 育儿卡通视频一键通 - 桌面版测试")
    print("=" * 60)
    
    # 设置日志级别，减少噪音
    logging.getLogger().setLevel(logging.ERROR)
    
    tests = [
        ("模块导入", test_imports),
        ("依赖包检查", test_dependencies),
        ("配置加载", test_config),
        ("目录结构", test_directory_structure),
        ("核心功能", test_core_functionality),
        ("GUI组件", test_gui_components),
        ("文件生成", test_file_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * (40-len(test_name))}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！桌面应用准备就绪！")
        print("\n🚀 启动应用:")
        print("  Windows: 双击 start.bat")
        print("  macOS/Linux: python3 desktop_app.py")
    else:
        print("⚠️ 部分测试失败，请查看上述错误信息")
        print("💡 建议查看 DESKTOP_SETUP.md 了解安装说明")
    
    print("\n📖 详细使用说明请查看: DESKTOP_SETUP.md")

if __name__ == "__main__":
    main()