#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿短视频脚本生成器演示
"""

from generate_script import generate_script


def main():
    """主演示函数"""
    print("🎬 育儿短视频脚本生成器演示")
    print("=" * 50)
    
    # 演示主题列表
    demo_topics = [
        "宝宝夜醒频繁怎么办",
        "宝宝挑食怎么解决", 
        "宝宝哭闹不止",
        "宝宝便秘怎么办",
        "宝宝发烧护理",
        "宝宝湿疹处理"
    ]
    
    print(f"📝 将生成 {len(demo_topics)} 个育儿主题的脚本\n")
    
    for i, topic in enumerate(demo_topics, 1):
        print(f"🎯 主题 {i}: {topic}")
        print("-" * 30)
        
        try:
            result = generate_script(topic)
            
            print(f"📌 标题: {result['title']}")
            print(f"📄 脚本: {result['script']}")
            print(f"📊 字数: {len(result['script'])} 字符")
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
        
        print("\n" + "="*50 + "\n")
    
    print("✅ 演示完成！")
    print("\n💡 使用提示:")
    print("1. 设置 OPENAI_API_KEY 环境变量可以使用AI生成更个性化的内容")
    print("2. 生成的脚本适合配音使用，长度控制在300字以内")
    print("3. 内容仅供参考，具体育儿建议请咨询专业医生")


if __name__ == "__main__":
    main()