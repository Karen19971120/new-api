#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿卡通视频一键通 - 主入口文件
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置环境变量，确保能找到配置文件
os.environ.setdefault('PARENTING_VIDEO_ROOT', str(project_root))

if __name__ == "__main__":
    try:
        from src.main_gui import main
        main()
    except ImportError as e:
        print(f"导入模块失败: {e}")
        print("请确保已安装所有依赖库，运行: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"应用启动失败: {e}")
        sys.exit(1)