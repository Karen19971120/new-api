# -*- coding: utf-8 -*-
"""
育儿卡通视频一键通 - 配置文件
包含所有可配置的参数和API设置
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 目录配置
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
AUDIO_DIR = ASSETS_DIR / "audio"
MUSIC_DIR = ASSETS_DIR / "music"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMP_DIR = AUDIO_DIR / "temp"

# 确保目录存在
for dir_path in [ASSETS_DIR, IMAGES_DIR, AUDIO_DIR, MUSIC_DIR, OUTPUT_DIR, TEMP_DIR]:
    dir_path.mkdir(exist_ok=True)

# LLM API 配置
LLM_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY", ""),
    "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "model": "gpt-3.5-turbo",
    "max_tokens": 2000,
    "temperature": 0.7
}

# TTS 配置
TTS_CONFIG = {
    "voice": "zh-CN-XiaoxiaoNeural",  # 微软Edge中文童音
    "rate": "+0%",                    # 语速
    "volume": "+0%"                   # 音量
}

# 视频配置
VIDEO_CONFIG = {
    "resolution": (720, 1280),        # 竖屏尺寸 (适合短视频平台)
    "fps": 24,                        # 帧率
    "audio_fade_in": 0.1,            # 音频淡入时间(秒)
    "audio_fade_out": 0.1,           # 音频淡出时间(秒)
    "font_size": 36,                 # 字幕字体大小
    "font_color": "white",           # 字幕颜色
    "font_stroke_color": "black",    # 字幕描边颜色
    "font_stroke_width": 2,          # 字幕描边宽度
    "subtitle_position": ("center", "bottom"),  # 字幕位置
    "subtitle_margin": 50,           # 字幕底部边距
}

# 素材库配置
ASSET_CATEGORIES = {
    "backgrounds": {
        "consultation_room": "咨询室背景",
        "home": "家庭背景", 
        "playground": "游乐场背景",
        "bedroom": "卧室背景"
    },
    "characters": {
        "expert_happy": "专家开心",
        "expert_explaining": "专家讲解",
        "expert_thinking": "专家思考", 
        "mom_happy": "妈妈开心",
        "mom_worried": "妈妈担心",
        "baby_crying": "宝宝哭泣",
        "baby_happy": "宝宝开心",
        "baby_playing": "宝宝玩耍"
    },
    "props": {
        "question_mark": "问号",
        "checkmark": "打勾",
        "heart": "爱心",
        "clothes_red": "红色衣服",
        "clothes_blue": "蓝色衣服",
        "toy": "玩具"
    }
}

# 提示词模板
SCRIPT_PROMPT_TEMPLATE = """
你是一个专业的育儿短视频脚本编写专家。请根据用户提供的关键词，生成一个适合短视频平台(抖音、小红书等)的育儿知识讲解脚本。

要求：
1. 视频总时长控制在30-60秒
2. 内容要专业、实用、易懂
3. 语言风格要亲切、温暖，适合父母群体
4. 结构要清晰：开场引入 -> 知识点讲解 -> 结尾总结
5. 每个场景要有明确的视觉描述，方便匹配素材

用户关键词：{keyword}

请严格按照以下JSON格式输出：

{{
  "title": "视频标题",
  "scenes": [
    {{
      "scene_number": 1,
      "duration_hint": 5,
      "visual_description": "详细的画面描述，包含背景、角色、动作等",
      "voice_over_text": "这个场景的配音文案"
    }},
    {{
      "scene_number": 2,
      "duration_hint": 8,
      "visual_description": "详细的画面描述",
      "voice_over_text": "这个场景的配音文案"
    }}
  ],
  "outro": {{
    "visual_description": "结尾画面描述",
    "voice_over_text": "结尾配音文案"
  }}
}}

注意：
- visual_description要尽量使用以下关键词：专家开心、专家讲解、妈妈开心、妈妈担心、宝宝哭泣、宝宝开心、咨询室、家庭背景、问号、打勾等
- voice_over_text要自然流畅，适合语音播放
- 每个场景的时长建议5-12秒
"""

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "filename": PROJECT_ROOT / "logs" / "app.log"
}

# 确保日志目录存在
(PROJECT_ROOT / "logs").mkdir(exist_ok=True)