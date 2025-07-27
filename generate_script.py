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

输入参数：
- topic: str，用户自定义的内容主题关键词

输出结果：
- dict:
  - title: str，短视频标题
  - script: str，脚本正文内容（建议配音用）
"""

import os
import json
from typing import Dict, Optional
import logging

# 尝试导入requests，如果没有则使用urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.parse
    import urllib.error
    HAS_REQUESTS = False

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParentingScriptGenerator:
    """育儿短视频脚本生成器"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        """
        初始化脚本生成器
        
        Args:
            api_key: GPT API密钥，如果为None则从环境变量获取
            api_base: API基础URL，如果为None则使用默认OpenAI API
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or "https://api.openai.com/v1"
        self.use_api = bool(self.api_key)
    
    def generate_script(self, topic: str) -> Dict[str, str]:
        """
        生成育儿短视频脚本
        
        Args:
            topic: 用户自定义的内容主题关键词
            
        Returns:
            包含标题和脚本的字典
        """
        # 如果没有API密钥，直接使用备用脚本
        if not self.use_api:
            logger.info("未提供API密钥，使用备用脚本")
            return self._generate_fallback_script(topic)
        
        try:
            # 构建提示词
            prompt = self._build_prompt(topic)
            
            # 调用GPT API
            response = self._call_gpt_api(prompt)
            
            # 解析响应
            result = self._parse_response(response)
            
            return result
            
        except Exception as e:
            logger.error(f"生成脚本时发生错误: {e}")
            return self._generate_fallback_script(topic)
    
    def _build_prompt(self, topic: str) -> str:
        """构建GPT提示词"""
        return f"""
请以卡通宝宝"小泡泡"的第一人称视角，为以下育儿主题生成一个短视频脚本。

主题：{topic}

要求：
1. 内容风格要感性可爱又不失科学严谨
2. 以"小泡泡"的身份说话，语气要活泼可爱
3. 脚本长度控制在30-60秒语速（约300字内）
4. 包含实用的育儿建议和科学知识
5. 语言要通俗易懂，适合家长理解

请按以下JSON格式返回：
{{
    "title": "短视频标题（吸引人且符合主题）",
    "script": "完整的脚本内容，包含开场白、主要内容、结尾等"
}}

注意：
- 标题要简洁有力，吸引点击
- 脚本要自然流畅，适合配音
- 内容要有实用价值，帮助家长解决问题
"""
    
    def _call_gpt_api(self, prompt: str) -> str:
        """调用GPT API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的育儿内容创作者，擅长创作以卡通宝宝视角的育儿短视频脚本。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        if HAS_REQUESTS:
            # 使用requests库
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"API调用失败: {response.status_code} - {response.text}")
            
            return response.json()["choices"][0]["message"]["content"]
        else:
            # 使用urllib库
            import urllib.request
            import urllib.parse
            
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                f"{self.api_base}/chat/completions",
                data=json_data,
                headers=headers,
                method='POST'
            )
            
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    response_data = json.loads(response.read().decode('utf-8'))
                    return response_data["choices"][0]["message"]["content"]
            except urllib.error.HTTPError as e:
                raise Exception(f"API调用失败: {e.code} - {e.read().decode('utf-8')}")
            except urllib.error.URLError as e:
                raise Exception(f"网络错误: {e.reason}")
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """解析GPT响应"""
        try:
            # 尝试直接解析JSON
            result = json.loads(response)
            return {
                "title": result.get("title", ""),
                "script": result.get("script", "")
            }
        except json.JSONDecodeError:
            # 如果JSON解析失败，尝试提取内容
            logger.warning("JSON解析失败，尝试提取内容")
            return self._extract_content_from_text(response)
    
    def _extract_content_from_text(self, text: str) -> Dict[str, str]:
        """从文本中提取标题和脚本内容"""
        lines = text.strip().split('\n')
        title = ""
        script = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('"title"') or line.startswith("'title'"):
                title = line.split(':', 1)[1].strip().strip('",\'')
            elif line.startswith('"script"') or line.startswith("'script'"):
                script = line.split(':', 1)[1].strip().strip('",\'')
        
        return {
            "title": title or "育儿小贴士",
            "script": script or text
        }
    
    def _generate_fallback_script(self, topic: str) -> Dict[str, str]:
        """生成备用脚本（当API调用失败时）"""
        fallback_scripts = {
            "宝宝夜醒频繁": {
                "title": "小泡泡教你解决宝宝夜醒问题",
                "script": "嗨，我是小泡泡！很多爸爸妈妈都问我，为什么宝宝晚上总是醒呢？其实啊，这是很正常的！小宝宝的睡眠周期比大人短，而且他们还在适应这个世界。我的建议是：1. 建立固定的睡前仪式，比如洗澡、讲故事；2. 保持房间安静和黑暗；3. 不要一哭就立即抱起，可以轻轻拍拍安抚。记住，每个宝宝都是独特的，要有耐心哦！"
            },
            "宝宝挑食": {
                "title": "小泡泡的挑食解决秘籍",
                "script": "大家好，我是小泡泡！听说很多宝宝都有挑食的问题呢。其实挑食是很常见的，爸爸妈妈不要太担心！我的小建议：1. 把食物做成有趣的形状，比如小动物造型；2. 让宝宝参与做饭过程，他们会更有兴趣；3. 不要强迫，可以尝试10-15次，宝宝才会接受新食物；4. 以身作则，爸爸妈妈也要多吃蔬菜水果哦！"
            },
            "宝宝哭闹": {
                "title": "小泡泡解读宝宝哭闹密码",
                "script": "嗨，我是小泡泡！宝宝哭闹是他们的语言，不是任性哦！当我们哭的时候，可能是在说：我饿了、我困了、我不舒服、我想要抱抱。爸爸妈妈要学会观察我们的表情和动作。我的小贴士：1. 先检查基本需求（尿布、饥饿、温度）；2. 用温柔的声音安抚；3. 轻轻摇晃或抱着走动；4. 播放轻柔的音乐。记住，耐心和爱是最好的良药！"
            }
        }
        
        # 尝试匹配主题
        for key, script in fallback_scripts.items():
            if key in topic or topic in key:
                return script
        
        # 如果没有匹配，返回通用脚本
        return {
            "title": f"小泡泡的{topic}小贴士",
            "script": f"嗨，我是小泡泡！今天要和大家聊聊{topic}这个话题。作为一个小宝宝，我想告诉爸爸妈妈们，每个宝宝都是独特的，我们需要你们的理解和耐心。关于{topic}，我的建议是：多观察、多陪伴、多沟通。记住，爱是最好的教育方式！"
        }


def generate_script(topic: str, api_key: Optional[str] = None, api_base: Optional[str] = None) -> Dict[str, str]:
    """
    便捷函数：生成育儿短视频脚本
    
    Args:
        topic: 用户自定义的内容主题关键词
        api_key: GPT API密钥（可选）
        api_base: API基础URL（可选）
        
    Returns:
        包含标题和脚本的字典
    """
    generator = ParentingScriptGenerator(api_key, api_base)
    return generator.generate_script(topic)


# 示例使用
if __name__ == "__main__":
    # 示例1：使用环境变量中的API密钥
    try:
        result = generate_script("宝宝夜醒频繁怎么办")
        print("=== 生成的脚本 ===")
        print(f"标题: {result['title']}")
        print(f"脚本: {result['script']}")
    except Exception as e:
        print(f"生成失败: {e}")
    
    # 示例2：使用自定义API配置
    # result = generate_script("宝宝挑食", api_key="your-api-key", api_base="https://your-api-endpoint.com/v1")