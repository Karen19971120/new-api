# 📥 育儿卡通视频一键通 - 下载安装指南

## 🎯 下载方式

由于我们在开发环境中，有几种方式可以将这个完整的桌面应用下载到您的电脑：

### 方式一：手动下载文件（推荐）

如果您可以访问这些文件，可以逐个复制保存以下核心文件：

#### 📁 必需文件清单

**🚀 启动文件**
- `desktop_app.py` - 主桌面应用程序
- `start.bat` - Windows一键启动脚本
- `requirements.txt` - 依赖包列表

**🧠 核心模块 (src/文件夹)**
- `src/script_generator.py`
- `src/tts_generator.py` 
- `src/asset_manager.py`
- `src/video_composer.py`
- `src/video_generator.py`
- `src/main_gui.py`

**⚙️ 配置文件 (config/文件夹)**
- `config/config.py`

**📖 说明文档**
- `README.md`
- `DESKTOP_SETUP.md`
- `DESKTOP_COMPLETE.md`

**🧪 测试工具（可选）**
- `test_desktop.py`
- `demo.py`

### 方式二：创建安装包（如果支持）

让我为您创建一个自解压的安装脚本：

#### Windows 安装包内容
```
育儿视频生成器/
├── desktop_app.py          # 主程序
├── start.bat              # 启动脚本
├── install.bat            # 安装脚本
├── requirements.txt       # 依赖列表
├── src/                   # 核心模块
├── config/               # 配置文件
├── assets/               # 素材文件夹（空）
└── docs/                 # 说明文档
```

## 🔧 安装步骤

### 第一步：准备Python环境

**Windows用户：**
1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.8 或更高版本
3. 安装时**务必勾选** "Add Python to PATH"
4. 安装完成后重启电脑

**验证安装：**
```bash
# 打开命令提示符（cmd），运行：
python --version
# 应该显示 Python 3.x.x
```

### 第二步：下载项目文件

**方法A：逐个保存文件**
1. 复制每个文件的内容
2. 在您的电脑上创建对应的文件和文件夹结构
3. 将内容粘贴保存

**方法B：使用Git（如果有）**
```bash
# 如果文件在Git仓库中
git clone [仓库地址]
```

### 第三步：创建项目文件夹

在您的电脑上创建以下文件夹结构：
```
育儿视频生成器/
├── desktop_app.py
├── start.bat
├── requirements.txt
├── src/
│   ├── script_generator.py
│   ├── tts_generator.py
│   ├── asset_manager.py
│   ├── video_composer.py
│   ├── video_generator.py
│   └── main_gui.py
├── config/
│   └── config.py
├── assets/
│   ├── images/
│   │   ├── backgrounds/
│   │   ├── characters/
│   │   └── props/
│   ├── music/
│   │   └── background/
│   └── audio/
│       └── temp/
└── output/
```

### 第四步：一键启动

**Windows用户：**
```
双击 start.bat 文件
```

**其他系统：**
```bash
cd 育儿视频生成器
python desktop_app.py
```

## 📦 快速安装脚本

我为您创建了一个自动安装脚本：
```