# -*- coding: utf-8 -*-
"""
视频生成控制器
协调脚本生成、TTS、素材匹配、视频合成等各个模块
"""

import logging
import time
from typing import Dict, Any, Optional, Callable
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.script_generator import ScriptGenerator
from src.tts_generator import TTSGenerator
from src.asset_manager import AssetManager
from src.video_composer import VideoComposer
from config.config import OUTPUT_DIR

logger = logging.getLogger(__name__)

class VideoGenerationStatus:
    """视频生成状态枚举"""
    IDLE = "idle"
    GENERATING_SCRIPT = "generating_script"
    GENERATING_AUDIO = "generating_audio"
    MATCHING_ASSETS = "matching_assets"
    COMPOSING_VIDEO = "composing_video"
    COMPLETED = "completed"
    ERROR = "error"

class VideoGenerator:
    """视频生成控制器"""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """
        初始化视频生成器
        
        Args:
            progress_callback: 进度回调函数，接收(status, message, progress)参数
        """
        self.progress_callback = progress_callback
        self.status = VideoGenerationStatus.IDLE
        
        # 初始化各个模块
        self.script_generator = ScriptGenerator()
        self.tts_generator = TTSGenerator()
        self.asset_manager = AssetManager()
        self.video_composer = VideoComposer()
        
        logger.info("视频生成器初始化完成")
    
    def generate_video(self, keyword: str) -> Optional[str]:
        """
        一键生成视频的主流程
        
        Args:
            keyword: 用户输入的关键词
            
        Returns:
            str: 生成的视频文件路径，失败返回None
        """
        try:
            start_time = time.time()
            logger.info(f"开始生成视频，关键词: {keyword}")
            
            # 第1步：生成脚本
            self._update_progress(VideoGenerationStatus.GENERATING_SCRIPT, "正在生成脚本...", 10)
            script_data = self.script_generator.generate_script(keyword)
            
            if not script_data:
                self._update_progress(VideoGenerationStatus.ERROR, "脚本生成失败", 0)
                return None
            
            logger.info(f"脚本生成成功，标题: {script_data.get('title', 'Unknown')}")
            
            # 第2步：生成音频
            self._update_progress(VideoGenerationStatus.GENERATING_AUDIO, "正在生成语音...", 30)
            audio_files = self.tts_generator.generate_script_audio(script_data)
            
            if not audio_files:
                self._update_progress(VideoGenerationStatus.ERROR, "语音生成失败", 0)
                return None
            
            logger.info(f"语音生成成功，共{len(audio_files)}个音频文件")
            
            # 第3步：匹配素材
            self._update_progress(VideoGenerationStatus.MATCHING_ASSETS, "正在匹配素材...", 50)
            visual_assets = self._match_all_visual_assets(script_data)
            
            if not visual_assets:
                self._update_progress(VideoGenerationStatus.ERROR, "素材匹配失败", 0)
                return None
            
            logger.info(f"素材匹配成功，共{len(visual_assets)}个场景")
            
            # 第4步：获取背景音乐
            background_music = self.asset_manager.get_random_background_music()
            
            # 第5步：合成视频
            self._update_progress(VideoGenerationStatus.COMPOSING_VIDEO, "正在合成视频...", 80)
            output_filename = self._generate_output_filename(keyword)
            video_path = self.video_composer.compose_video(
                script_data=script_data,
                audio_files=audio_files,
                visual_assets=visual_assets,
                background_music=background_music,
                output_filename=output_filename
            )
            
            if not video_path:
                self._update_progress(VideoGenerationStatus.ERROR, "视频合成失败", 0)
                return None
            
            # 第6步：清理临时文件
            self.tts_generator.cleanup_temp_files()
            
            # 完成
            end_time = time.time()
            duration = end_time - start_time
            success_message = f"视频生成完成！耗时: {duration:.1f}秒"
            
            self._update_progress(VideoGenerationStatus.COMPLETED, success_message, 100)
            logger.info(f"视频生成完成: {video_path}")
            logger.info(f"总耗时: {duration:.2f}秒")
            
            return video_path
            
        except Exception as e:
            error_message = f"视频生成过程中发生错误: {str(e)}"
            logger.error(error_message)
            self._update_progress(VideoGenerationStatus.ERROR, error_message, 0)
            return None
    
    def _match_all_visual_assets(self, script_data: Dict[str, Any]) -> list:
        """匹配所有场景的视觉素材"""
        visual_assets = []
        
        try:
            # 处理主要场景
            for scene in script_data.get("scenes", []):
                scene_number = scene.get("scene_number")
                visual_description = scene.get("visual_description", "")
                
                matched_assets = self.asset_manager.match_visual_assets(visual_description)
                
                visual_assets.append({
                    "scene_number": scene_number,
                    "background": matched_assets.get("background"),
                    "characters": matched_assets.get("characters", []),
                    "props": matched_assets.get("props", [])
                })
            
            # 处理结尾场景
            outro = script_data.get("outro")
            if outro:
                visual_description = outro.get("visual_description", "")
                matched_assets = self.asset_manager.match_visual_assets(visual_description)
                
                visual_assets.append({
                    "scene_number": "outro",
                    "background": matched_assets.get("background"),
                    "characters": matched_assets.get("characters", []),
                    "props": matched_assets.get("props", [])
                })
            
            return visual_assets
            
        except Exception as e:
            logger.error(f"素材匹配失败: {e}")
            return []
    
    def _generate_output_filename(self, keyword: str) -> str:
        """生成输出文件名"""
        try:
            # 清理关键词，移除特殊字符
            clean_keyword = "".join(c for c in keyword if c.isalnum() or c in "._- ")
            clean_keyword = clean_keyword.strip()
            
            if not clean_keyword:
                clean_keyword = "育儿视频"
            
            # 添加时间戳避免重名
            timestamp = int(time.time())
            filename = f"{clean_keyword}_{timestamp}.mp4"
            
            return filename
            
        except Exception as e:
            logger.error(f"生成文件名失败: {e}")
            return "output_video.mp4"
    
    def _update_progress(self, status: str, message: str, progress: int):
        """更新进度状态"""
        self.status = status
        
        if self.progress_callback:
            try:
                self.progress_callback(status, message, progress)
            except Exception as e:
                logger.error(f"进度回调失败: {e}")
        
        logger.info(f"状态更新: {status} - {message} ({progress}%)")
    
    def get_status(self) -> str:
        """获取当前状态"""
        return self.status
    
    def is_busy(self) -> bool:
        """检查是否正在生成视频"""
        return self.status not in [VideoGenerationStatus.IDLE, VideoGenerationStatus.COMPLETED, VideoGenerationStatus.ERROR]
    
    def reset(self):
        """重置状态"""
        self.status = VideoGenerationStatus.IDLE
        logger.info("视频生成器状态已重置")
    
    def get_output_directory(self) -> str:
        """获取输出目录路径"""
        return str(OUTPUT_DIR)
    
    def list_generated_videos(self) -> list:
        """列出已生成的视频文件"""
        try:
            video_files = []
            
            for file_path in OUTPUT_DIR.glob("*.mp4"):
                if file_path.is_file():
                    video_files.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "created": file_path.stat().st_ctime
                    })
            
            # 按创建时间排序，最新的在前
            video_files.sort(key=lambda x: x["created"], reverse=True)
            
            return video_files
            
        except Exception as e:
            logger.error(f"列出视频文件失败: {e}")
            return []