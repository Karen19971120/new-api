#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿卡通视频一键通 - 功能测试脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_import():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from src.script_generator import ScriptGenerator
        print("✅ ScriptGenerator 导入成功")
    except Exception as e:
        print(f"❌ ScriptGenerator 导入失败: {e}")
    
    try:
        from src.tts_generator import TTSGenerator
        print("✅ TTSGenerator 导入成功")
    except Exception as e:
        print(f"❌ TTSGenerator 导入失败: {e}")
    
    try:
        from src.asset_manager import AssetManager
        print("✅ AssetManager 导入成功")
    except Exception as e:
        print(f"❌ AssetManager 导入失败: {e}")
    
    try:
        from src.video_composer import VideoComposer
        print("✅ VideoComposer 导入成功")
    except Exception as e:
        print(f"❌ VideoComposer 导入失败: {e}")
    
    try:
        from src.video_generator import VideoGenerator
        print("✅ VideoGenerator 导入成功")
    except Exception as e:
        print(f"❌ VideoGenerator 导入失败: {e}")

def test_config():
    """测试配置加载"""
    print("\n⚙️ 测试配置加载...")
    
    try:
        from config.config import (
            PROJECT_ROOT, ASSETS_DIR, OUTPUT_DIR,
            LLM_CONFIG, TTS_CONFIG, VIDEO_CONFIG
        )
        print("✅ 配置文件加载成功")
        print(f"   项目根目录: {PROJECT_ROOT}")
        print(f"   素材目录: {ASSETS_DIR}")
        print(f"   输出目录: {OUTPUT_DIR}")
        print(f"   LLM模型: {LLM_CONFIG.get('model', 'N/A')}")
        print(f"   TTS语音: {TTS_CONFIG.get('voice', 'N/A')}")
        print(f"   视频分辨率: {VIDEO_CONFIG.get('resolution', 'N/A')}")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")

def test_script_generation():
    """测试脚本生成"""
    print("\n📝 测试脚本生成...")
    
    try:
        from src.script_generator import ScriptGenerator
        
        generator = ScriptGenerator()
        script = generator.generate_script("孩子不爱吃饭")
        
        if script:
            print("✅ 脚本生成成功")
            print(f"   标题: {script.get('title', 'N/A')}")
            print(f"   场景数量: {len(script.get('scenes', []))}")
            
            if script.get('scenes'):
                first_scene = script['scenes'][0]
                print(f"   第一个场景文案: {first_scene.get('voice_over_text', 'N/A')[:50]}...")
        else:
            print("❌ 脚本生成失败")
            
    except Exception as e:
        print(f"❌ 脚本生成测试失败: {e}")

def test_asset_manager():
    """测试素材管理"""
    print("\n🎨 测试素材管理...")
    
    try:
        from src.asset_manager import AssetManager
        
        manager = AssetManager()
        assets = manager.match_visual_assets("卡通专家微笑地出现在屏幕中央，背景是明亮的咨询室")
        
        print("✅ 素材匹配成功")
        print(f"   背景素材: {assets.get('background', 'N/A')}")
        print(f"   角色素材数量: {len(assets.get('characters', []))}")
        print(f"   道具素材数量: {len(assets.get('props', []))}")
        
        # 测试背景音乐
        music = manager.get_random_background_music()
        if music:
            print(f"   背景音乐: {music}")
        else:
            print("   背景音乐: 未找到")
            
    except Exception as e:
        print(f"❌ 素材管理测试失败: {e}")

def test_directory_structure():
    """测试目录结构"""
    print("\n📁 测试目录结构...")
    
    try:
        from config.config import ASSETS_DIR, OUTPUT_DIR
        
        # 检查关键目录
        dirs_to_check = [
            ASSETS_DIR / "images" / "backgrounds",
            ASSETS_DIR / "images" / "characters", 
            ASSETS_DIR / "images" / "props",
            ASSETS_DIR / "music" / "background",
            OUTPUT_DIR
        ]
        
        for dir_path in dirs_to_check:
            if dir_path.exists():
                print(f"✅ {dir_path.name} 目录存在")
            else:
                print(f"❌ {dir_path.name} 目录不存在")
                
    except Exception as e:
        print(f"❌ 目录结构测试失败: {e}")

def test_video_generator_init():
    """测试视频生成器初始化"""
    print("\n🎬 测试视频生成器初始化...")
    
    try:
        from src.video_generator import VideoGenerator
        
        def progress_callback(status, message, progress):
            print(f"   状态: {status} - {message} ({progress}%)")
        
        generator = VideoGenerator(progress_callback=progress_callback)
        print("✅ 视频生成器初始化成功")
        print(f"   当前状态: {generator.get_status()}")
        print(f"   输出目录: {generator.get_output_directory()}")
        
    except Exception as e:
        print(f"❌ 视频生成器初始化失败: {e}")

def main():
    """主测试函数"""
    print("🚀 育儿卡通视频一键通 - 功能测试")
    print("=" * 50)
    
    # 运行各项测试
    test_import()
    test_config()
    test_directory_structure()
    test_script_generation()
    test_asset_manager()
    test_video_generator_init()
    
    print("\n" + "=" * 50)
    print("✨ 测试完成！如果看到较多✅标志，说明应用基本功能正常。")
    print("💡 现在可以运行 `python main.py` 启动GUI应用了！")

if __name__ == "__main__":
    main()