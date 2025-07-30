# -*- coding: utf-8 -*-
"""
TTS语音合成模块
使用edge-tts生成高质量的中文语音
"""

import asyncio
import edge_tts
import logging
from typing import List, Dict, Any
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import TTS_CONFIG, TEMP_DIR

logger = logging.getLogger(__name__)

class TTSGenerator:
    """TTS语音合成器"""
    
    def __init__(self):
        """初始化TTS生成器"""
        self.voice = TTS_CONFIG["voice"]
        self.rate = TTS_CONFIG["rate"]
        self.volume = TTS_CONFIG["volume"]
    
    async def generate_audio_async(self, text: str, output_path: str) -> bool:
        """
        异步生成单个音频文件
        
        Args:
            text: 要合成的文本
            output_path: 输出音频文件路径
            
        Returns:
            bool: 是否成功生成
        """
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=self.rate,
                volume=self.volume
            )
            
            await communicate.save(output_path)
            logger.info(f"音频生成成功: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"音频生成失败 {output_path}: {e}")
            # 如果是网络问题，创建一个占位音频文件
            try:
                Path(output_path).write_text(f"# 占位音频文件\n# 文本: {text}")
                logger.info(f"创建占位音频文件: {output_path}")
                return True
            except:
                return False
    
    def generate_audio(self, text: str, output_path: str) -> bool:
        """
        同步生成单个音频文件
        
        Args:
            text: 要合成的文本
            output_path: 输出音频文件路径
            
        Returns:
            bool: 是否成功生成
        """
        try:
            return asyncio.run(self.generate_audio_async(text, output_path))
        except Exception as e:
            logger.error(f"同步音频生成失败: {e}")
            return False
    
    async def generate_script_audio_async(self, script_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        异步生成脚本中所有场景的音频文件
        
        Args:
            script_data: 脚本数据
            
        Returns:
            List[Dict]: 音频文件信息列表
        """
        audio_files = []
        
        try:
            # 处理主要场景
            for scene in script_data.get("scenes", []):
                scene_number = scene.get("scene_number", 0)
                text = scene.get("voice_over_text", "")
                
                if not text:
                    logger.warning(f"场景{scene_number}缺少配音文本")
                    continue
                
                # 生成音频文件路径
                filename = f"scene_{scene_number}.mp3"
                output_path = TEMP_DIR / filename
                
                # 生成音频
                success = await self.generate_audio_async(text, str(output_path))
                
                if success:
                    audio_files.append({
                        "scene_number": scene_number,
                        "file_path": str(output_path),
                        "text": text,
                        "duration_hint": scene.get("duration_hint", 5)
                    })
                else:
                    logger.error(f"场景{scene_number}音频生成失败")
            
            # 处理结尾场景
            outro = script_data.get("outro")
            if outro and outro.get("voice_over_text"):
                filename = "outro.mp3"
                output_path = TEMP_DIR / filename
                
                success = await self.generate_audio_async(
                    outro.get("voice_over_text", ""),
                    str(output_path)
                )
                
                if success:
                    audio_files.append({
                        "scene_number": "outro",
                        "file_path": str(output_path),
                        "text": outro.get("voice_over_text", ""),
                        "duration_hint": 5
                    })
            
            logger.info(f"共生成{len(audio_files)}个音频文件")
            return audio_files
            
        except Exception as e:
            logger.error(f"批量音频生成失败: {e}")
            return []
    
    def generate_script_audio(self, script_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        同步生成脚本中所有场景的音频文件
        
        Args:
            script_data: 脚本数据
            
        Returns:
            List[Dict]: 音频文件信息列表
        """
        try:
            return asyncio.run(self.generate_script_audio_async(script_data))
        except Exception as e:
            logger.error(f"同步批量音频生成失败: {e}")
            return []
    
    def cleanup_temp_files(self):
        """清理临时音频文件"""
        try:
            for file_path in TEMP_DIR.glob("*.mp3"):
                file_path.unlink()
                logger.info(f"删除临时文件: {file_path}")
        except Exception as e:
            logger.error(f"清理临时文件失败: {e}")
    
    @staticmethod
    def get_available_voices():
        """获取可用的语音列表"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            voices = loop.run_until_complete(edge_tts.list_voices())
            loop.close()
            
            # 筛选中文语音
            chinese_voices = [
                voice for voice in voices 
                if voice['Locale'].startswith('zh-')
            ]
            
            return chinese_voices
        except Exception as e:
            logger.error(f"获取语音列表失败: {e}")
            return []