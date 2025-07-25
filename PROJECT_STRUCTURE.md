# 🎬 育儿卡通视频一键通 - 项目结构

```
育儿卡通视频一键通/
├── 📁 主要文件
│   ├── main.py                 # 应用程序主入口
│   ├── README.md               # 项目说明文档
│   ├── requirements.txt        # Python依赖库
│   ├── setup.py               # 安装脚本
│   ├── test_app.py            # 功能测试脚本
│   ├── start.sh               # Linux启动脚本
│   └── start.bat              # Windows启动脚本
│
├── 📁 src/                    # 核心源代码
│   ├── main_gui.py            # 主GUI界面
│   ├── script_generator.py    # 脚本生成模块
│   ├── tts_generator.py       # TTS语音合成模块
│   ├── asset_manager.py       # 素材管理模块
│   ├── video_composer.py      # 视频合成模块
│   └── video_generator.py     # 视频生成控制器
│
├── 📁 config/                 # 配置文件
│   └── config.py              # 主配置文件
│
├── 📁 assets/                 # 素材资源
│   ├── 📁 images/             # 图片素材
│   │   ├── backgrounds/       # 背景图片
│   │   │   ├── consultation_room.png
│   │   │   ├── home.png
│   │   │   ├── playground.png
│   │   │   └── bedroom.png
│   │   ├── characters/        # 角色图片
│   │   │   ├── expert_happy.png
│   │   │   ├── expert_explaining.png
│   │   │   ├── expert_thinking.png
│   │   │   ├── mom_happy.png
│   │   │   ├── mom_worried.png
│   │   │   ├── baby_crying.png
│   │   │   ├── baby_happy.png
│   │   │   └── baby_playing.png
│   │   └── props/             # 道具图片
│   │       ├── question_mark.png
│   │       ├── checkmark.png
│   │       ├── heart.png
│   │       ├── clothes_red.png
│   │       ├── clothes_blue.png
│   │       └── toy.png
│   └── 📁 music/              # 音乐资源
│       └── background/        # 背景音乐
│           ├── warm_family.mp3
│           ├── happy_children.mp3
│           ├── gentle_guidance.mp3
│           └── peaceful_moments.mp3
│
└── 📁 output/                 # 输出目录
    └── (生成的视频文件)
```

## 📋 模块说明

### 🎯 核心模块

1. **ScriptGenerator** (`src/script_generator.py`)
   - 功能：调用LLM API生成结构化的育儿视频脚本
   - 输入：用户关键词
   - 输出：JSON格式的视频脚本

2. **TTSGenerator** (`src/tts_generator.py`)
   - 功能：使用edge-tts生成高质量中文语音
   - 输入：脚本文本
   - 输出：MP3音频文件

3. **AssetManager** (`src/asset_manager.py`)
   - 功能：智能匹配和管理图片、音乐素材
   - 输入：视觉描述文本
   - 输出：匹配的素材文件路径

4. **VideoComposer** (`src/video_composer.py`)
   - 功能：使用MoviePy合成最终视频
   - 输入：音频、图片、字幕数据
   - 输出：MP4视频文件

5. **VideoGenerator** (`src/video_generator.py`)
   - 功能：协调各模块完成整个视频生成流程
   - 输入：关键词
   - 输出：完整的视频文件

### 🖥️ 用户界面

6. **MainGUI** (`src/main_gui.py`)
   - 功能：现代化的桌面应用界面
   - 框架：Tkinter + CustomTkinter
   - 特性：进度显示、状态反馈、文件管理

### ⚙️ 配置系统

7. **Config** (`config/config.py`)
   - 功能：统一的配置管理
   - 内容：API设置、素材路径、视频参数等

## 🚀 使用流程

1. **启动应用**：运行 `python main.py` 或双击启动脚本
2. **输入关键词**：在界面中输入育儿相关关键词
3. **一键生成**：点击生成按钮，等待处理完成
4. **获取成果**：在output目录中找到生成的MP4视频

## 🔧 技术栈

- **编程语言**：Python 3.8+
- **GUI框架**：Tkinter + CustomTkinter
- **视频处理**：MoviePy
- **语音合成**：edge-tts (微软Edge TTS)
- **LLM集成**：OpenAI API
- **图像处理**：Pillow
- **音频处理**：pydub

## 📦 依赖管理

所有依赖库都定义在 `requirements.txt` 中，使用以下命令安装：

```bash
pip install -r requirements.txt
```

## 🎨 素材系统

应用采用模块化的素材管理系统：

- **背景图片**：不同场景的背景
- **角色图片**：专家、妈妈、宝宝等角色
- **道具图片**：问号、对勾、爱心等辅助元素
- **背景音乐**：温馨、轻快的背景音乐

用户可以通过替换 `assets/` 目录中的文件来自定义素材。