#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本生成器功能
"""

import os
import sys
from generate_script import generate_script, ParentingScriptGenerator


def test_fallback_script():
    """测试备用脚本功能（不需要API密钥）"""
    print("=== 测试备用脚本功能 ===")
    
    # 测试已知主题
    test_topics = [
        "宝宝夜醒频繁",
        "宝宝挑食", 
        "宝宝哭闹",
        "宝宝发烧怎么办"  # 未知主题
    ]
    
    for topic in test_topics:
        print(f"\n主题: {topic}")
        try:
            result = generate_script(topic)
            print(f"标题: {result['title']}")
            print(f"脚本: {result['script'][:100]}...")  # 只显示前100个字符
        except Exception as e:
            print(f"错误: {e}")


def test_api_script():
    """测试API脚本生成功能（需要API密钥）"""
    print("\n=== 测试API脚本生成功能 ===")
    
    # 检查是否有API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("未设置OPENAI_API_KEY环境变量，跳过API测试")
        return
    
    test_topic = "宝宝便秘怎么办"
    print(f"测试主题: {test_topic}")
    
    try:
        result = generate_script(test_topic)
        print(f"标题: {result['title']}")
        print(f"脚本: {result['script']}")
        print(f"脚本长度: {len(result['script'])} 字符")
    except Exception as e:
        print(f"API调用失败: {e}")


def test_generator_class():
    """测试生成器类"""
    print("\n=== 测试生成器类 ===")
    
    try:
        generator = ParentingScriptGenerator()
        result = generator.generate_script("宝宝湿疹")
        print(f"标题: {result['title']}")
        print(f"脚本: {result['script'][:100]}...")
    except Exception as e:
        print(f"类测试失败: {e}")


def main():
    """主测试函数"""
    print("育儿短视频脚本生成器测试")
    print("=" * 50)
    
    # 测试备用脚本
    test_fallback_script()
    
    # 测试生成器类
    test_generator_class()
    
    # 测试API功能（如果有密钥）
    test_api_script()
    
    print("\n测试完成！")


if __name__ == "__main__":
    main()