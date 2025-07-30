# -*- coding: utf-8 -*-
"""
素材管理模块
负责匹配和管理图片、音乐等素材资源
"""

import logging
import random
from typing import Dict, List, Optional
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import IMAGES_DIR, MUSIC_DIR, ASSET_CATEGORIES

logger = logging.getLogger(__name__)

class AssetManager:
    """素材资源管理器"""
    
    def __init__(self):
        """初始化素材管理器"""
        self.images_dir = IMAGES_DIR
        self.music_dir = MUSIC_DIR
        self.asset_categories = ASSET_CATEGORIES
        self._create_sample_assets()
    
    def _create_sample_assets(self):
        """创建示例素材（占位图片）"""
        try:
            # 创建基础目录结构
            backgrounds_dir = self.images_dir / "backgrounds"
            characters_dir = self.images_dir / "characters"
            props_dir = self.images_dir / "props"
            
            backgrounds_dir.mkdir(exist_ok=True)
            characters_dir.mkdir(exist_ok=True)
            props_dir.mkdir(exist_ok=True)
            
            # 创建示例图片文件（空文件作为占位）
            sample_files = {
                "backgrounds": [
                    "consultation_room.png",
                    "home.png",
                    "playground.png", 
                    "bedroom.png"
                ],
                "characters": [
                    "expert_happy.png",
                    "expert_explaining.png",
                    "expert_thinking.png",
                    "mom_happy.png",
                    "mom_worried.png",
                    "baby_crying.png",
                    "baby_happy.png",
                    "baby_playing.png"
                ],
                "props": [
                    "question_mark.png",
                    "checkmark.png",
                    "heart.png",
                    "clothes_red.png",
                    "clothes_blue.png",
                    "toy.png"
                ]
            }
            
            for category, files in sample_files.items():
                category_dir = self.images_dir / category
                for filename in files:
                    file_path = category_dir / filename
                    if not file_path.exists():
                        # 创建简单的占位内容
                        file_path.write_text(f"# 占位图片: {filename}")
                        logger.info(f"创建占位图片: {file_path}")
            
            # 创建示例背景音乐
            music_bg_dir = self.music_dir / "background"
            music_bg_dir.mkdir(exist_ok=True)
            
            sample_music = [
                "warm_family.mp3",
                "happy_children.mp3",
                "gentle_guidance.mp3",
                "peaceful_moments.mp3"
            ]
            
            for music_file in sample_music:
                file_path = music_bg_dir / music_file
                if not file_path.exists():
                    file_path.write_text(f"# 占位音乐: {music_file}")
                    logger.info(f"创建占位音乐: {file_path}")
                    
        except Exception as e:
            logger.error(f"创建示例素材失败: {e}")
    
    def match_visual_assets(self, visual_description: str) -> Dict[str, Optional[str]]:
        """
        根据视觉描述匹配合适的素材
        
        Args:
            visual_description: 视觉描述文本
            
        Returns:
            Dict: 匹配的素材文件路径
        """
        matched_assets = {
            "background": None,
            "characters": [],
            "props": []
        }
        
        try:
            description_lower = visual_description.lower()
            
            # 匹配背景
            for asset_key, asset_name in self.asset_categories["backgrounds"].items():
                keywords = self._get_background_keywords(asset_key)
                if any(keyword in description_lower for keyword in keywords):
                    background_path = self.images_dir / "backgrounds" / f"{asset_key}.png"
                    if background_path.exists():
                        matched_assets["background"] = str(background_path)
                        logger.info(f"匹配背景: {asset_name} -> {background_path}")
                        break
            
            # 如果没有匹配到背景，使用默认背景
            if not matched_assets["background"]:
                default_bg = self.images_dir / "backgrounds" / "consultation_room.png"
                if default_bg.exists():
                    matched_assets["background"] = str(default_bg)
            
            # 匹配角色
            for asset_key, asset_name in self.asset_categories["characters"].items():
                keywords = self._get_character_keywords(asset_key)
                if any(keyword in description_lower for keyword in keywords):
                    character_path = self.images_dir / "characters" / f"{asset_key}.png"
                    if character_path.exists():
                        matched_assets["characters"].append(str(character_path))
                        logger.info(f"匹配角色: {asset_name} -> {character_path}")
            
            # 匹配道具
            for asset_key, asset_name in self.asset_categories["props"].items():
                keywords = self._get_props_keywords(asset_key)
                if any(keyword in description_lower for keyword in keywords):
                    prop_path = self.images_dir / "props" / f"{asset_key}.png"
                    if prop_path.exists():
                        matched_assets["props"].append(str(prop_path))
                        logger.info(f"匹配道具: {asset_name} -> {prop_path}")
            
            return matched_assets
            
        except Exception as e:
            logger.error(f"素材匹配失败: {e}")
            return matched_assets
    
    def _get_background_keywords(self, asset_key: str) -> List[str]:
        """获取背景素材的关键词"""
        keyword_mapping = {
            "consultation_room": ["咨询室", "办公室", "专业", "诊所"],
            "home": ["家庭", "家里", "客厅", "房间", "温馨"],
            "playground": ["游乐场", "户外", "玩耍", "运动"],
            "bedroom": ["卧室", "床", "睡觉", "休息"]
        }
        return keyword_mapping.get(asset_key, [])
    
    def _get_character_keywords(self, asset_key: str) -> List[str]:
        """获取角色素材的关键词"""
        keyword_mapping = {
            "expert_happy": ["专家开心", "专家微笑", "专家愉快"],
            "expert_explaining": ["专家讲解", "专家说话", "专家解释"],
            "expert_thinking": ["专家思考", "专家沉思"],
            "mom_happy": ["妈妈开心", "妈妈微笑", "母亲愉快"],
            "mom_worried": ["妈妈担心", "妈妈焦虑", "母亲忧虑"],
            "baby_crying": ["宝宝哭泣", "孩子哭", "婴儿哭闹"],
            "baby_happy": ["宝宝开心", "孩子高兴", "婴儿笑"],
            "baby_playing": ["宝宝玩耍", "孩子玩", "婴儿游戏"]
        }
        return keyword_mapping.get(asset_key, [])
    
    def _get_props_keywords(self, asset_key: str) -> List[str]:
        """获取道具素材的关键词"""
        keyword_mapping = {
            "question_mark": ["问号", "疑问", "问题"],
            "checkmark": ["打勾", "对勾", "正确", "完成"],
            "heart": ["爱心", "心形", "喜爱"],
            "clothes_red": ["红色衣服", "红衣"],
            "clothes_blue": ["蓝色衣服", "蓝衣"],
            "toy": ["玩具", "游戏"]
        }
        return keyword_mapping.get(asset_key, [])
    
    def get_random_background_music(self) -> Optional[str]:
        """获取随机背景音乐"""
        try:
            music_files = list((self.music_dir / "background").glob("*.mp3"))
            if music_files:
                selected_music = random.choice(music_files)
                logger.info(f"选择背景音乐: {selected_music}")
                return str(selected_music)
            else:
                logger.warning("没有找到背景音乐文件")
                return None
        except Exception as e:
            logger.error(f"获取背景音乐失败: {e}")
            return None
    
    def get_asset_info(self, asset_path: str) -> Dict:
        """获取素材信息"""
        try:
            path = Path(asset_path)
            if path.exists():
                return {
                    "name": path.name,
                    "size": path.stat().st_size,
                    "exists": True
                }
            else:
                return {
                    "name": path.name,
                    "size": 0,
                    "exists": False
                }
        except Exception as e:
            logger.error(f"获取素材信息失败: {e}")
            return {"name": "", "size": 0, "exists": False}