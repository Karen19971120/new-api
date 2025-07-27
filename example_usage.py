#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿短视频脚本生成器 - 快速使用示例
"""

from generate_script import generate_script


# 示例1：基本使用
print("=== 示例1：基本使用 ===")
result = generate_script("宝宝夜醒频繁怎么办")
print(f"标题: {result['title']}")
print(f"脚本: {result['script']}")
print()

# 示例2：自定义主题
print("=== 示例2：自定义主题 ===")
custom_topic = "宝宝不爱吃饭"
result = generate_script(custom_topic)
print(f"主题: {custom_topic}")
print(f"标题: {result['title']}")
print(f"脚本: {result['script']}")
print()

# 示例3：批量生成
print("=== 示例3：批量生成 ===")
topics = ["宝宝便秘", "宝宝发烧", "宝宝湿疹"]
for topic in topics:
    result = generate_script(topic)
    print(f"主题: {topic}")
    print(f"标题: {result['title']}")
    print(f"字数: {len(result['script'])} 字符")
    print("-" * 30)

print("\n✅ 示例运行完成！")