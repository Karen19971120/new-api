#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块名称：generate_script.py

功能：
- 使用 GPT API（或本地模型）生成一个育儿短视频脚本；
- 以卡通宝宝"小泡泡"的第一人称进行叙述；
- 输出应包含：标题、脚本正文；
- 内容风格感性可爱又不失科学严谨；
- 长度控制在 30~60 秒语速（约 300 字内）；
- 输入可以是你给定的"主题"关键词，如"宝宝夜醒频繁怎么办"。
"""

import os
import json
import requests
from typing import Dict, Optional
from openai import OpenAI


class ScriptGenerator:
    """育儿短视频脚本生成器"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化脚本生成器
        
        Args:
            api_key: OpenAI API密钥，如果不提供将从环境变量OPENAI_API_KEY获取
            base_url: API基础URL，支持本地模型或其他兼容API
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        self.client = None
        
        # 尝试初始化OpenAI客户端
        if self.api_key:
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except Exception as e:
                print(f"警告：OpenAI客户端初始化失败: {e}")
                print("将使用备用脚本生成功能")
        else:
            print("未检测到API密钥，将使用备用脚本生成功能")
    
    def generate_script(self, topic: str) -> Dict[str, str]:
        """
        生成育儿短视频脚本
        
        Args:
            topic: 内容主题关键词，例如"宝宝夜醒频繁怎么办"
            
        Returns:
            dict: 包含title和script的字典
                - title: str，短视频标题
                - script: str，脚本正文内容
        """
        
        # 构建提示词
        system_prompt = """你是一个专业的育儿内容创作者，需要以卡通宝宝"小泡泡"的第一人称视角来创作育儿短视频脚本。

角色设定：
- 你是小泡泡，一个可爱的卡通宝宝
- 说话风格：天真可爱，但又很有智慧
- 经常使用"泡泡觉得..."、"小泡泡发现..."这样的表达
- 语言亲和力强，让家长感到温馨

内容要求：
1. 标题要吸引人，突出解决问题的价值
2. 脚本要科学严谨，给出实用的育儿建议
3. 语言要感性可爱，符合小泡泡的人设
4. 控制在300字以内，适合30-60秒的语速
5. 结构清晰：问题引入 → 原因分析 → 解决方案 → 温馨提醒

请返回JSON格式，包含title和script两个字段。"""

        user_prompt = f"请为主题\"{topic}\"创作一个育儿短视频脚本。"
        
        # 如果没有可用的客户端，直接使用备用脚本
        if not self.client:
            return self._generate_fallback_script(topic)
        
        try:
            # 调用GPT API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # 解析响应
            content = response.choices[0].message.content.strip()
            
            # 尝试解析JSON
            try:
                result = json.loads(content)
                if isinstance(result, dict) and 'title' in result and 'script' in result:
                    return result
            except json.JSONDecodeError:
                pass
            
            # 如果JSON解析失败，尝试手动提取
            return self._extract_content_manually(content)
            
        except Exception as e:
            # 如果API调用失败，返回默认内容
            print(f"API调用失败: {e}")
            print("使用备用脚本生成功能")
            return self._generate_fallback_script(topic)
    
    def _extract_content_manually(self, content: str) -> Dict[str, str]:
        """手动提取标题和脚本内容"""
        lines = content.split('\n')
        title = ""
        script = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('标题') or line.startswith('title'):
                title = line.split('：', 1)[-1].split(':', 1)[-1].strip().strip('"')
            elif line.startswith('脚本') or line.startswith('script'):
                script = line.split('：', 1)[-1].split(':', 1)[-1].strip().strip('"')
        
        if not title or not script:
            # 如果没能正确提取，使用整个内容作为脚本
            if not title:
                title = f"小泡泡的育儿小贴士"
            if not script:
                script = content
        
        return {"title": title, "script": script}
    
    def _generate_fallback_script(self, topic: str) -> Dict[str, str]:
        """生成备用脚本（当API调用失败时）"""
        title = f"小泡泡教你：{topic}"
        
        script = f"""大家好，我是小泡泡！今天泡泡想和爸爸妈妈们聊聊{topic}这个话题呢～

小泡泡发现，很多爸爸妈妈都会遇到这样的困扰。其实呀，这是很正常的现象哦！

泡泡觉得，首先要了解原因，然后找到合适的解决方法。每个宝宝都是独特的小天使，需要爸爸妈妈的耐心和爱心～

记住哦，育儿路上没有标准答案，只要用心陪伴，宝宝一定会健康快乐地成长的！

小泡泡今天就分享到这里啦，如果对大家有帮助的话，记得点赞关注哦～拜拜！"""
        
        return {"title": title, "script": script}


def generate_parenting_script(topic: str, api_key: Optional[str] = None, base_url: Optional[str] = None) -> Dict[str, str]:
    """
    生成育儿短视频脚本的便捷函数
    
    Args:
        topic: 内容主题关键词
        api_key: OpenAI API密钥（可选）
        base_url: API基础URL（可选）
        
    Returns:
        dict: 包含title和script的字典
    """
    generator = ScriptGenerator(api_key=api_key, base_url=base_url)
    return generator.generate_script(topic)


# 示例用法
if __name__ == "__main__":
    # 示例1：基本用法
    try:
        result = generate_parenting_script("宝宝夜醒频繁怎么办")
        print("标题:", result["title"])
        print("\n脚本:")
        print(result["script"])
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"生成脚本时出错: {e}")
    
    # 示例2：使用自定义API
    try:
        # 可以指定本地模型API
        # result = generate_parenting_script(
        #     "宝宝不爱吃饭怎么办",
        #     base_url="http://localhost:11434/v1"  # 例如ollama本地API
        # )
        
        # 或者使用其他主题
        result = generate_parenting_script("如何培养宝宝的睡眠习惯")
        print("标题:", result["title"])
        print("\n脚本:")
        print(result["script"])
    except Exception as e:
        print(f"生成脚本时出错: {e}")