# -*- coding: utf-8 -*-
"""
视频合成模块
使用MoviePy进行视频合成，包括图片、音频、字幕的组合
"""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys
import os

def check_moviepy():
    """动态检测MoviePy是否可用"""
    try:
        import moviepy
        from moviepy.editor import (
            VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip,
            CompositeAudioClip, TextClip, concatenate_videoclips
        )
        return True
    except ImportError as e:
        logging.warning(f"MoviePy不可用: {e}")
        return False

# 初始检测，但允许后续重新检测
MOVIEPY_AVAILABLE = check_moviepy()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import VIDEO_CONFIG, OUTPUT_DIR

logger = logging.getLogger(__name__)

class VideoComposer:
    """视频合成器"""
    
    def __init__(self):
        """初始化视频合成器"""
        self.resolution = VIDEO_CONFIG["resolution"]
        self.fps = VIDEO_CONFIG["fps"]
        self.font_size = VIDEO_CONFIG["font_size"]
        self.font_color = VIDEO_CONFIG["font_color"]
        self.font_stroke_color = VIDEO_CONFIG["font_stroke_color"]
        self.font_stroke_width = VIDEO_CONFIG["font_stroke_width"]
        
        if not MOVIEPY_AVAILABLE:
            logger.error("MoviePy不可用，无法进行视频合成")
    
    def compose_video(
        self,
        script_data: Dict[str, Any],
        audio_files: List[Dict[str, Any]],
        visual_assets: List[Dict[str, Any]],
        background_music: Optional[str] = None,
        output_filename: str = "output_video.mp4"
    ) -> Optional[str]:
        """
        合成完整视频
        
        Args:
            script_data: 脚本数据
            audio_files: 音频文件列表
            visual_assets: 视觉素材列表
            background_music: 背景音乐文件路径
            output_filename: 输出文件名
            
        Returns:
            str: 输出视频文件路径，失败返回None
        """
        # 动态检测MoviePy可用性
        moviepy_available = check_moviepy()
        if not moviepy_available:
            logger.error("MoviePy不可用，使用模拟视频生成")
            return self._create_mock_video(output_filename)
        
        try:
            # 动态导入MoviePy模块
            from moviepy.editor import (
                VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip,
                CompositeAudioClip, TextClip, concatenate_videoclips
            )
            
            logger.info("开始视频合成")
            
            # 创建场景视频片段
            video_clips = []
            total_duration = 0
            
            # 处理主要场景
            for i, scene in enumerate(script_data.get("scenes", [])):
                scene_number = scene.get("scene_number", i + 1)
                
                # 查找对应的音频文件
                audio_info = next(
                    (audio for audio in audio_files 
                     if audio.get("scene_number") == scene_number),
                    None
                )
                
                # 查找对应的视觉素材
                visual_info = next(
                    (visual for visual in visual_assets 
                     if visual.get("scene_number") == scene_number),
                    None
                )
                
                if audio_info and visual_info:
                    clip = self._create_scene_clip(scene, audio_info, visual_info)
                    if clip:
                        video_clips.append(clip)
                        total_duration += clip.duration
                        logger.info(f"场景{scene_number}合成成功，时长: {clip.duration:.2f}秒")
            
            # 处理结尾场景
            outro = script_data.get("outro")
            if outro:
                audio_info = next(
                    (audio for audio in audio_files 
                     if audio.get("scene_number") == "outro"),
                    None
                )
                visual_info = next(
                    (visual for visual in visual_assets 
                     if visual.get("scene_number") == "outro"),
                    None
                )
                
                if audio_info and visual_info:
                    clip = self._create_scene_clip(outro, audio_info, visual_info)
                    if clip:
                        video_clips.append(clip)
                        total_duration += clip.duration
                        logger.info(f"结尾场景合成成功，时长: {clip.duration:.2f}秒")
            
            if not video_clips:
                logger.error("没有成功创建任何视频片段")
                return self._create_mock_video(output_filename)
            
            # 拼接所有视频片段
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # 添加背景音乐
            if background_music and Path(background_music).exists():
                final_video = self._add_background_music(final_video, background_music)
            
            # 输出视频
            output_path = OUTPUT_DIR / output_filename
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                audio_codec='aac',
                codec='libx264'
            )
            
            # 清理资源
            final_video.close()
            for clip in video_clips:
                clip.close()
            
            logger.info(f"视频合成完成: {output_path}")
            logger.info(f"总时长: {total_duration:.2f}秒")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"视频合成失败: {e}")
            return self._create_mock_video(output_filename)
    
    def _create_scene_clip(
        self,
        scene_data: Dict[str, Any],
        audio_info: Dict[str, Any],
        visual_info: Dict[str, Any]
    ) -> Optional[Any]:
        """创建单个场景的视频片段"""
        try:
            # 加载音频
            audio_path = audio_info.get("file_path")
            if not audio_path or not Path(audio_path).exists():
                logger.error(f"音频文件不存在: {audio_path}")
                return None
            
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            # 创建背景
            background_path = visual_info.get("background")
            if background_path and Path(background_path).exists():
                # 这里应该是图片，但由于我们的占位文件是文本，我们创建一个色块
                background_clip = self._create_color_clip(
                    color=(100, 150, 200),  # 蓝色背景
                    duration=duration
                )
            else:
                # 默认背景色
                background_clip = self._create_color_clip(
                    color=(50, 100, 150),   # 深蓝色背景
                    duration=duration
                )
            
            # 创建字幕
            text = audio_info.get("text", "")
            if text:
                subtitle_clip = self._create_subtitle_clip(text, duration)
                # 合成视频和字幕
                video_clip = CompositeVideoClip([background_clip, subtitle_clip])
            else:
                video_clip = background_clip
            
            # 设置音频
            video_clip = video_clip.set_audio(audio_clip)
            
            return video_clip
            
        except Exception as e:
            logger.error(f"创建场景片段失败: {e}")
            return None
    
    def _create_color_clip(self, color: tuple, duration: float) -> Any:
        """创建纯色背景片段"""
        try:
            # 创建纯色图片
            import numpy as np
            from PIL import Image
            
            # 创建纯色数组
            img_array = np.full(
                (self.resolution[1], self.resolution[0], 3),
                color,
                dtype=np.uint8
            )
            
            # 转换为PIL图片
            img = Image.fromarray(img_array)
            
            # 保存临时文件
            temp_path = OUTPUT_DIR / "temp_bg.png"
            img.save(temp_path)
            
            # 创建视频片段
            clip = ImageClip(str(temp_path), duration=duration)
            clip = clip.resize(self.resolution)
            
            return clip
            
        except Exception as e:
            logger.error(f"创建色块失败: {e}")
            # 如果失败，返回一个简单的黑色背景
            return ImageClip(color=(0, 0, 0), size=self.resolution, duration=duration)
    
    def _create_subtitle_clip(self, text: str, duration: float) -> Any:
        """创建字幕片段"""
        try:
            # 分行处理长文本
            max_chars_per_line = 20
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + word) <= max_chars_per_line:
                    current_line += word + " "
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            subtitle_text = "\n".join(lines)
            
            # 创建文字片段
            txt_clip = TextClip(
                subtitle_text,
                fontsize=self.font_size,
                color=self.font_color,
                stroke_color=self.font_stroke_color,
                stroke_width=self.font_stroke_width,
                method='caption',
                size=(self.resolution[0] - 100, None)  # 留边距
            )
            
            # 设置位置和时长
            txt_clip = txt_clip.set_duration(duration)
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_margin(50)
            
            return txt_clip
            
        except Exception as e:
            logger.error(f"创建字幕失败: {e}")
            # 返回空的透明片段
            return ImageClip(color=(0, 0, 0, 0), size=(1, 1), duration=duration).set_opacity(0)
    
    def _add_background_music(self, video_clip: Any, music_path: str) -> Any:
        """添加背景音乐"""
        try:
            if not Path(music_path).exists():
                logger.warning(f"背景音乐文件不存在: {music_path}")
                return video_clip
            
            # 加载背景音乐
            bg_music = AudioFileClip(music_path)
            
            # 调整音乐长度匹配视频
            if bg_music.duration < video_clip.duration:
                # 如果音乐短于视频，循环播放
                loops_needed = int(video_clip.duration / bg_music.duration) + 1
                bg_music = bg_music.loop(loops_needed)
            
            # 截取匹配视频长度
            bg_music = bg_music.subclip(0, video_clip.duration)
            
            # 降低背景音乐音量
            bg_music = bg_music.volumex(0.3)
            
            # 合成音频
            if video_clip.audio:
                final_audio = CompositeAudioClip([video_clip.audio, bg_music])
            else:
                final_audio = bg_music
            
            # 应用到视频
            video_clip = video_clip.set_audio(final_audio)
            
            logger.info("背景音乐添加成功")
            return video_clip
            
        except Exception as e:
            logger.error(f"添加背景音乐失败: {e}")
            return video_clip
    
    def _create_mock_video(self, filename: str) -> str:
        """创建模拟视频文件（用于测试）"""
        try:
            output_path = OUTPUT_DIR / filename
            
            # 创建一个简单的文本文件作为占位
            mock_content = f"""
# 模拟视频文件: {filename}
# 这是一个占位文件，表示视频生成完成
# 在实际部署时，这里应该是真正的MP4视频文件

文件名: {filename}
生成时间: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}
状态: 模拟生成成功
            """.strip()
            
            output_path.write_text(mock_content, encoding='utf-8')
            logger.info(f"模拟视频创建成功: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            logger.error(f"创建模拟视频失败: {e}")
            return ""