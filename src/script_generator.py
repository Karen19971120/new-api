# -*- coding: utf-8 -*-
"""
脚本生成模块
负责调用LLM API生成结构化的育儿视频脚本
"""

import json
import openai
import logging
from typing import Dict, Any, Optional
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import LLM_CONFIG, SCRIPT_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class ScriptGenerator:
    """智能脚本生成器"""
    
    def __init__(self):
        """初始化脚本生成器"""
        self.client = None
        self._setup_openai_client()
    
    def _setup_openai_client(self):
        """设置OpenAI客户端"""
        try:
            if not LLM_CONFIG["api_key"]:
                logger.warning("未设置OpenAI API密钥，将使用模拟数据")
                return
            
            self.client = openai.OpenAI(
                api_key=LLM_CONFIG["api_key"],
                base_url=LLM_CONFIG["base_url"]
            )
            logger.info("OpenAI客户端初始化成功")
        except Exception as e:
            logger.error(f"OpenAI客户端初始化失败: {e}")
            self.client = None
    
    def generate_script(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        根据关键词生成视频脚本
        
        Args:
            keyword: 用户输入的关键词
            
        Returns:
            Dict: 生成的脚本数据，包含场景、配音等信息
        """
        try:
            logger.info(f"开始生成脚本，关键词: {keyword}")
            
            if not self.client:
                logger.warning("使用模拟脚本数据")
                return self._get_mock_script(keyword)
            
            # 构建提示词
            prompt = SCRIPT_PROMPT_TEMPLATE.format(keyword=keyword)
            
            # 调用LLM API
            response = self.client.chat.completions.create(
                model=LLM_CONFIG["model"],
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=LLM_CONFIG["max_tokens"],
                temperature=LLM_CONFIG["temperature"]
            )
            
            # 解析响应
            content = response.choices[0].message.content.strip()
            logger.info("LLM响应获取成功")
            
            # 解析JSON
            script_data = self._parse_script_response(content)
            
            if script_data:
                logger.info("脚本生成成功")
                return script_data
            else:
                logger.error("脚本解析失败，使用模拟数据")
                return self._get_mock_script(keyword)
                
        except Exception as e:
            logger.error(f"脚本生成失败: {e}")
            return self._get_mock_script(keyword)
    
    def _parse_script_response(self, content: str) -> Optional[Dict[str, Any]]:
        """解析LLM响应的JSON内容"""
        try:
            # 尝试提取JSON部分
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                script_data = json.loads(json_str)
                
                # 验证必要字段
                if self._validate_script_data(script_data):
                    return script_data
                    
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
        except Exception as e:
            logger.error(f"脚本数据解析失败: {e}")
            
        return None
    
    def _validate_script_data(self, data: Dict[str, Any]) -> bool:
        """验证脚本数据的完整性"""
        try:
            # 检查必要字段
            required_fields = ["title", "scenes"]
            for field in required_fields:
                if field not in data:
                    logger.error(f"缺少必要字段: {field}")
                    return False
            
            # 检查场景数据
            if not isinstance(data["scenes"], list) or len(data["scenes"]) == 0:
                logger.error("场景数据无效")
                return False
            
            # 检查每个场景的必要字段
            scene_fields = ["scene_number", "duration_hint", "visual_description", "voice_over_text"]
            for scene in data["scenes"]:
                for field in scene_fields:
                    if field not in scene:
                        logger.error(f"场景缺少必要字段: {field}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"脚本数据验证失败: {e}")
            return False
    
    def _get_mock_script(self, keyword: str) -> Dict[str, Any]:
        """获取模拟脚本数据（用于测试和无API情况）"""
        logger.info("使用模拟脚本数据")
        
        return {
            "title": f"关于{keyword}的育儿知识",
            "scenes": [
                {
                    "scene_number": 1,
                    "duration_hint": 5,
                    "visual_description": "卡通专家微笑地出现在屏幕中央，背景是明亮的咨询室。专家做大家好的手势。",
                    "voice_over_text": f"家长们好！今天我们来聊聊{keyword}这个话题。"
                },
                {
                    "scene_number": 2,
                    "duration_hint": 8,
                    "visual_description": "画面左侧是卡通专家，右侧出现一个大大的问号气泡。",
                    "voice_over_text": "这确实是很多家长都会遇到的问题，让我来为大家详细解答。"
                },
                {
                    "scene_number": 3,
                    "duration_hint": 10,
                    "visual_description": "画面切换，一个卡通妈妈蹲下身，微笑着和宝宝互动。",
                    "voice_over_text": "首先，我们要理解孩子的心理，保持耐心和爱心是最重要的。"
                },
                {
                    "scene_number": 4,
                    "duration_hint": 8,
                    "visual_description": "卡通专家再次出现，旁边有一个打勾的清单图标。",
                    "voice_over_text": "记住这个小贴士，相信对您会有帮助。"
                }
            ],
            "outro": {
                "visual_description": "卡通专家再次出现在屏幕中央，微笑着挥手。",
                "voice_over_text": "你学会了吗？关注我，每天分享一个育儿小妙招！"
            }
        }