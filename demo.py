#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿卡通视频一键通 - 功能演示脚本
无需GUI，直接展示核心功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_script_generation():
    """演示脚本生成功能"""
    print("🎬 演示脚本生成功能")
    print("-" * 40)
    
    try:
        from src.script_generator import ScriptGenerator
        
        generator = ScriptGenerator()
        script = generator.generate_script("孩子不爱吃饭")
        
        if script:
            print(f"✅ 脚本生成成功！")
            print(f"📝 标题: {script.get('title', 'N/A')}")
            print(f"🎞️ 场景数量: {len(script.get('scenes', []))}")
            
            # 显示第一个场景的内容
            if script.get('scenes'):
                first_scene = script['scenes'][0]
                print(f"\n第一个场景示例:")
                print(f"  💬 配音文案: {first_scene.get('voice_over_text', 'N/A')[:100]}...")
                print(f"  🎨 视觉描述: {first_scene.get('visual_description', 'N/A')[:100]}...")
        else:
            print("❌ 脚本生成失败")
            
    except Exception as e:
        print(f"❌ 脚本生成演示失败: {e}")

def demo_tts_generation():
    """演示TTS功能"""
    print("\n🔊 演示TTS语音合成功能")
    print("-" * 40)
    
    try:
        from src.tts_generator import TTSGenerator
        from config.config import TEMP_DIR
        
        generator = TTSGenerator()
        
        # 生成一段测试音频
        test_text = "大家好，欢迎使用育儿卡通视频一键通！"
        output_path = TEMP_DIR / "demo_audio.mp3"
        
        success = generator.generate_audio(test_text, str(output_path))
        
        if success:
            print(f"✅ 语音合成成功！")
            print(f"📁 音频文件: {output_path}")
            print(f"📝 合成文本: {test_text}")
        else:
            print("❌ 语音合成失败")
            
    except Exception as e:
        print(f"❌ TTS演示失败: {e}")

def demo_asset_matching():
    """演示素材匹配功能"""
    print("\n🎨 演示素材匹配功能")
    print("-" * 40)
    
    try:
        from src.asset_manager import AssetManager
        
        manager = AssetManager()
        
        # 测试不同的视觉描述
        test_descriptions = [
            "卡通专家微笑地出现在屏幕中央，背景是明亮的咨询室",
            "画面左侧是卡通专家，右侧出现一个大大的问号气泡",
            "一个卡通妈妈蹲下身，微笑着和宝宝互动，温馨的家庭背景"
        ]
        
        for i, description in enumerate(test_descriptions, 1):
            print(f"\n测试场景 {i}:")
            print(f"  📝 描述: {description[:60]}...")
            
            assets = manager.match_visual_assets(description)
            
            print(f"  🖼️ 背景素材: {Path(assets.get('background', 'N/A')).name if assets.get('background') else 'N/A'}")
            print(f"  👥 角色素材数量: {len(assets.get('characters', []))}")
            print(f"  🎯 道具素材数量: {len(assets.get('props', []))}")
        
        # 测试背景音乐
        music = manager.get_random_background_music()
        if music:
            print(f"\n🎵 随机背景音乐: {Path(music).name}")
        else:
            print(f"\n🎵 随机背景音乐: 未找到")
            
    except Exception as e:
        print(f"❌ 素材匹配演示失败: {e}")

def demo_video_generation():
    """演示完整视频生成流程"""
    print("\n🎬 演示完整视频生成流程")
    print("-" * 40)
    
    try:
        from src.video_generator import VideoGenerator
        
        def progress_callback(status, message, progress):
            print(f"  📊 [{progress:3d}%] {message}")
        
        generator = VideoGenerator(progress_callback=progress_callback)
        
        print("🚀 开始生成演示视频...")
        print("💡 由于使用模拟数据，生成的是演示文件")
        
        # 使用一个简单的关键词进行演示
        video_path = generator.generate_video("宝宝睡眠问题")
        
        if video_path:
            print(f"\n✅ 视频生成完成！")
            print(f"📁 输出文件: {video_path}")
            print(f"📂 输出目录: {generator.get_output_directory()}")
            
            # 显示生成的文件信息
            if Path(video_path).exists():
                file_size = Path(video_path).stat().st_size
                print(f"📊 文件大小: {file_size} 字节")
        else:
            print("❌ 视频生成失败")
            
    except Exception as e:
        print(f"❌ 视频生成演示失败: {e}")

def show_project_info():
    """显示项目信息"""
    print("🎬 育儿卡通视频一键通 - 功能演示")
    print("=" * 50)
    print("📋 产品简介:")
    print("   一款为零基础内容创作者设计的桌面软件")
    print("   只需输入一个育儿关键词，即可自动生成")
    print("   适配短视频平台的卡通讲解风格视频")
    print()
    print("🔧 技术特色:")
    print("   ✓ AI智能脚本生成")
    print("   ✓ 高质量TTS语音合成")
    print("   ✓ 智能素材匹配")
    print("   ✓ 自动视频合成")
    print("   ✓ 现代化GUI界面")
    print()

def main():
    """主演示函数"""
    show_project_info()
    
    # 运行各项功能演示
    demo_script_generation()
    demo_tts_generation()
    demo_asset_matching()
    demo_video_generation()
    
    print("\n" + "=" * 50)
    print("🎉 演示完成！")
    print("💡 要使用完整功能，请运行: python main.py")
    print("📖 更多信息请查看: README.md")

if __name__ == "__main__":
    main()