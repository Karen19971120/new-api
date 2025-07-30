#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿卡通视频一键通 - 桌面应用启动器
专为桌面环境优化的启动程序
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import logging
from pathlib import Path
import threading
import subprocess

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class DesktopLauncher:
    """桌面应用启动器"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("育儿卡通视频一键通")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 设置图标（如果有的话）
        try:
            # 可以设置应用图标
            # self.root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        self.setup_ui()
        self.check_dependencies()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = tk.Label(
            main_frame,
            text="🎬 育儿卡通视频一键通",
            font=("Arial", 24, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # 副标题
        subtitle_label = tk.Label(
            main_frame,
            text="一键生成专业的育儿知识短视频",
            font=("Arial", 14),
            bg='white',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # 功能说明
        features_frame = tk.LabelFrame(main_frame, text="✨ 核心功能", font=("Arial", 12, "bold"), bg='white')
        features_frame.pack(fill='x', pady=(0, 20))
        
        features = [
            "🤖 AI智能脚本生成",
            "🔊 高质量语音合成",
            "🎨 智能素材匹配",
            "🎬 自动视频合成",
            "📱 短视频平台适配"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                features_frame,
                text=feature,
                font=("Arial", 11),
                bg='white',
                anchor='w'
            )
            feature_label.pack(fill='x', padx=10, pady=2)
        
        # 输入区域
        input_frame = tk.LabelFrame(main_frame, text="🎯 开始使用", font=("Arial", 12, "bold"), bg='white')
        input_frame.pack(fill='x', pady=(0, 20))
        
        # 关键词输入
        tk.Label(
            input_frame,
            text="请输入育儿关键词：",
            font=("Arial", 11),
            bg='white'
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.keyword_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=50,
            relief='solid',
            bd=1
        )
        self.keyword_entry.pack(fill='x', padx=10, pady=(0, 10))
        self.keyword_entry.insert(0, "孩子不爱吃饭怎么办")  # 默认示例
        
        # 生成按钮
        self.generate_btn = tk.Button(
            input_frame,
            text="🚀 一键生成视频",
            font=("Arial", 14, "bold"),
            bg='#3498db',
            fg='white',
            relief='flat',
            pady=10,
            command=self.start_generation
        )
        self.generate_btn.pack(fill='x', padx=10, pady=(0, 15))
        
        # 进度区域
        progress_frame = tk.LabelFrame(main_frame, text="📊 生成进度", font=("Arial", 12, "bold"), bg='white')
        progress_frame.pack(fill='x', pady=(0, 20))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(fill='x', padx=10, pady=10)
        
        # 状态标签
        self.status_label = tk.Label(
            progress_frame,
            text="等待开始...",
            font=("Arial", 10),
            bg='white',
            fg='#27ae60'
        )
        self.status_label.pack(padx=10, pady=(0, 10))
        
        # 底部按钮
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        # 打开输出文件夹按钮
        self.open_folder_btn = tk.Button(
            button_frame,
            text="📁 打开输出文件夹",
            command=self.open_output_folder,
            bg='#95a5a6',
            fg='white',
            relief='flat'
        )
        self.open_folder_btn.pack(side='left')
        
        # 高级设置按钮
        self.settings_btn = tk.Button(
            button_frame,
            text="⚙️ 设置",
            command=self.open_settings,
            bg='#95a5a6',
            fg='white',
            relief='flat'
        )
        self.settings_btn.pack(side='left', padx=(10, 0))
        
        # 帮助按钮
        help_btn = tk.Button(
            button_frame,
            text="❓ 帮助",
            command=self.show_help,
            bg='#95a5a6',
            fg='white',
            relief='flat'
        )
        help_btn.pack(side='right')
    
    def check_dependencies(self):
        """检查依赖包"""
        self.status_label.config(text="正在检查依赖包...", fg='#f39c12')
        self.root.update()
        
        missing_deps = []
        
        try:
            import customtkinter
        except ImportError:
            missing_deps.append("customtkinter")
        
        try:
            import edge_tts
        except ImportError:
            missing_deps.append("edge-tts")
        
        try:
            import openai
        except ImportError:
            missing_deps.append("openai")
        
        try:
            import moviepy
        except ImportError:
            missing_deps.append("moviepy")
        
        if missing_deps:
            self.status_label.config(
                text=f"缺少依赖包: {', '.join(missing_deps)}",
                fg='#e74c3c'
            )
            
            result = messagebox.askyesno(
                "缺少依赖包",
                f"应用需要以下依赖包:\n{', '.join(missing_deps)}\n\n是否自动安装？"
            )
            
            if result:
                self.install_dependencies(missing_deps)
            else:
                messagebox.showwarning(
                    "警告",
                    "某些功能可能无法正常使用。\n建议手动安装依赖包。"
                )
        else:
            self.status_label.config(text="✅ 所有依赖包检查完成", fg='#27ae60')
    
    def install_dependencies(self, deps):
        """安装缺失的依赖包"""
        def install_thread():
            try:
                for dep in deps:
                    self.status_label.config(text=f"正在安装 {dep}...", fg='#f39c12')
                    self.root.update()
                    
                    # 使用pip安装
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", 
                        "--user", dep
                    ])
                
                self.status_label.config(text="✅ 依赖包安装完成", fg='#27ae60')
                messagebox.showinfo("成功", "依赖包安装完成！")
                
            except Exception as e:
                self.status_label.config(text="❌ 依赖包安装失败", fg='#e74c3c')
                messagebox.showerror("错误", f"依赖包安装失败:\n{e}")
        
        thread = threading.Thread(target=install_thread, daemon=True)
        thread.start()
    
    def start_generation(self):
        """开始生成视频"""
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入育儿关键词")
            return
        
        # 禁用生成按钮
        self.generate_btn.config(state='disabled')
        
        # 在新线程中运行生成任务
        thread = threading.Thread(
            target=self.generate_video_thread,
            args=(keyword,),
            daemon=True
        )
        thread.start()
    
    def generate_video_thread(self, keyword):
        """在线程中生成视频"""
        try:
            # 动态导入模块
            from src.video_generator import VideoGenerator
            
            def progress_callback(status, message, progress):
                # 在主线程中更新UI
                self.root.after(0, self.update_progress, message, progress)
            
            generator = VideoGenerator(progress_callback=progress_callback)
            
            # 开始生成
            result = generator.generate_video(keyword)
            
            # 完成回调
            self.root.after(0, self.generation_complete, result)
            
        except Exception as e:
            # 错误回调
            self.root.after(0, self.generation_error, str(e))
    
    def update_progress(self, message, progress):
        """更新进度显示"""
        self.progress_var.set(progress)
        self.status_label.config(text=message, fg='#3498db')
        self.root.update()
    
    def generation_complete(self, result):
        """生成完成的回调"""
        self.generate_btn.config(state='normal')
        
        if result and Path(result).exists():
            self.status_label.config(text="🎉 视频生成完成！", fg='#27ae60')
            
            # 询问是否打开文件
            response = messagebox.askyesno(
                "成功",
                f"视频生成完成！\n\n文件位置:\n{result}\n\n是否打开文件夹？"
            )
            
            if response:
                self.open_output_folder()
        else:
            self.status_label.config(text="❌ 视频生成失败", fg='#e74c3c')
            messagebox.showerror("失败", "视频生成失败，请查看控制台了解详情。")
    
    def generation_error(self, error_msg):
        """生成出错的回调"""
        self.generate_btn.config(state='normal')
        self.status_label.config(text="❌ 生成出错", fg='#e74c3c')
        messagebox.showerror("错误", f"生成过程中发生错误:\n{error_msg}")
    
    def open_output_folder(self):
        """打开输出文件夹"""
        try:
            output_dir = project_root / "output"
            output_dir.mkdir(exist_ok=True)
            
            # 跨平台打开文件夹
            import platform
            
            if platform.system() == "Windows":
                os.startfile(output_dir)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(output_dir)])
            else:  # Linux
                subprocess.run(["xdg-open", str(output_dir)])
                
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件夹:\n{e}")
    
    def open_settings(self):
        """打开设置窗口"""
        SettingsWindow(self.root)
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🎬 育儿卡通视频一键通 - 使用帮助

📋 使用步骤：
1. 在关键词输入框中输入育儿主题
2. 点击"一键生成视频"按钮
3. 等待生成完成（通常需要1-3分钟）
4. 在输出文件夹中查看生成的视频

🎯 关键词示例：
• 孩子不爱吃饭怎么办
• 宝宝睡眠问题
• 如何培养孩子专注力
• 两岁宝宝叛逆期
• 儿童情绪管理

💡 提示：
• 首次使用可能需要下载依赖包
• 生成的视频为竖屏格式，适合短视频平台
• 可以在设置中配置OpenAI API获得更好效果

❓ 如有问题，请查看README.md文档
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        
        text_widget = tk.Text(help_window, wrap='word', padx=20, pady=20)
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
        # 关闭按钮
        close_btn = tk.Button(
            help_window,
            text="关闭",
            command=help_window.destroy,
            bg='#95a5a6',
            fg='white',
            relief='flat'
        )
        close_btn.pack(pady=10)
    
    def run(self):
        """运行应用"""
        # 设置关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 居中显示
        self.center_window()
        
        # 运行主循环
        self.root.mainloop()
    
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取窗口尺寸
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"+{x}+{y}")
    
    def on_closing(self):
        """关闭应用时的处理"""
        if messagebox.askokcancel("退出", "确定要退出应用吗？"):
            self.root.destroy()

class SettingsWindow:
    """设置窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # API设置
        api_frame = tk.LabelFrame(main_frame, text="OpenAI API 设置", font=("Arial", 11, "bold"))
        api_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            api_frame,
            text="API Key (可选):",
            font=("Arial", 10)
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.api_key_entry = tk.Entry(
            api_frame,
            show="*",
            width=50,
            relief='solid',
            bd=1
        )
        self.api_key_entry.pack(fill='x', padx=10, pady=(0, 10))
        
        # 说明
        info_label = tk.Label(
            api_frame,
            text="设置API Key可获得更好的脚本生成效果\n不设置将使用模拟数据进行演示",
            font=("Arial", 9),
            fg='gray',
            justify='left'
        )
        info_label.pack(anchor='w', padx=10, pady=(0, 15))
        
        # 按钮
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="保存",
            command=self.save_settings,
            bg='#27ae60',
            fg='white',
            relief='flat'
        )
        save_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=self.window.destroy,
            bg='#95a5a6',
            fg='white',
            relief='flat'
        )
        cancel_btn.pack(side='right')
    
    def save_settings(self):
        """保存设置"""
        api_key = self.api_key_entry.get().strip()
        
        # 这里可以保存到配置文件
        # 暂时只显示消息
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            messagebox.showinfo("成功", "API Key已保存！\n重启应用后生效。")
        else:
            messagebox.showinfo("提示", "将使用模拟数据进行演示")
        
        self.window.destroy()

def main():
    """主函数"""
    try:
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # 创建并运行应用
        app = DesktopLauncher()
        app.run()
        
    except Exception as e:
        # 如果GUI启动失败，显示错误消息
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        messagebox.showerror(
            "启动失败",
            f"应用启动失败:\n{e}\n\n请检查Python环境和依赖包。"
        )
        
        root.destroy()

if __name__ == "__main__":
    main()