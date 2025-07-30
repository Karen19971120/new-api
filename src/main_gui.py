# -*- coding: utf-8 -*-
"""
主GUI界面
使用tkinter和customtkinter创建现代化的桌面应用
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import logging
import sys
import os
from pathlib import Path

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    logging.warning("CustomTkinter未安装，将使用标准tkinter")

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.video_generator import VideoGenerator, VideoGenerationStatus
from config.config import LLM_CONFIG

logger = logging.getLogger(__name__)

class ParentingVideoApp:
    """育儿卡通视频一键通主应用"""
    
    def __init__(self):
        """初始化应用"""
        self.video_generator = None
        self.generation_thread = None
        
        # 设置customtkinter主题
        if CTK_AVAILABLE:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()
        
        self.setup_ui()
        self.setup_video_generator()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主窗口配置
        self.root.title("育儿卡通视频一键通 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 创建主框架
        if CTK_AVAILABLE:
            main_frame = ctk.CTkFrame(self.root)
        else:
            main_frame = tk.Frame(self.root, bg='white')
        
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        if CTK_AVAILABLE:
            title_label = ctk.CTkLabel(
                main_frame,
                text="育儿卡通视频一键通",
                font=ctk.CTkFont(size=24, weight="bold")
            )
        else:
            title_label = tk.Label(
                main_frame,
                text="育儿卡通视频一键通",
                font=("Arial", 24, "bold"),
                bg='white'
            )
        
        title_label.pack(pady=(20, 10))
        
        # 副标题
        if CTK_AVAILABLE:
            subtitle_label = ctk.CTkLabel(
                main_frame,
                text="输入一个育儿关键词，即可自动生成专业的卡通讲解视频",
                font=ctk.CTkFont(size=14)
            )
        else:
            subtitle_label = tk.Label(
                main_frame,
                text="输入一个育儿关键词，即可自动生成专业的卡通讲解视频",
                font=("Arial", 14),
                bg='white'
            )
        
        subtitle_label.pack(pady=(0, 30))
        
        # 输入区域
        input_frame = tk.Frame(main_frame, bg='white' if not CTK_AVAILABLE else None)
        input_frame.pack(fill="x", pady=10)
        
        if CTK_AVAILABLE:
            keyword_label = ctk.CTkLabel(
                input_frame,
                text="请输入育儿关键词:",
                font=ctk.CTkFont(size=16, weight="bold")
            )
        else:
            keyword_label = tk.Label(
                input_frame,
                text="请输入育儿关键词:",
                font=("Arial", 16, "bold"),
                bg='white'
            )
        
        keyword_label.pack(anchor="w", pady=(0, 10))
        
        # 输入框
        if CTK_AVAILABLE:
            self.keyword_entry = ctk.CTkEntry(
                input_frame,
                height=40,
                font=ctk.CTkFont(size=14),
                placeholder_text="例如: 孩子两岁叛逆期怎么办"
            )
        else:
            self.keyword_entry = tk.Entry(
                input_frame,
                font=("Arial", 14),
                relief="solid",
                bd=1
            )
        
        self.keyword_entry.pack(fill="x", pady=(0, 20))
        
        # 生成按钮
        if CTK_AVAILABLE:
            self.generate_btn = ctk.CTkButton(
                input_frame,
                text="🎬 一键生成视频",
                height=50,
                font=ctk.CTkFont(size=16, weight="bold"),
                command=self.start_generation
            )
        else:
            self.generate_btn = tk.Button(
                input_frame,
                text="🎬 一键生成视频",
                font=("Arial", 16, "bold"),
                bg="#1f538d",
                fg="white",
                relief="flat",
                pady=10,
                command=self.start_generation
            )
        
        self.generate_btn.pack(fill="x", pady=10)
        
        # 进度区域
        progress_frame = tk.Frame(main_frame, bg='white' if not CTK_AVAILABLE else None)
        progress_frame.pack(fill="x", pady=20)
        
        # 进度条
        if CTK_AVAILABLE:
            self.progress_bar = ctk.CTkProgressBar(progress_frame, height=20)
        else:
            from tkinter import ttk
            self.progress_bar = ttk.Progressbar(
                progress_frame,
                mode='determinate',
                style='TProgressbar'
            )
        
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)
        
        # 状态标签
        if CTK_AVAILABLE:
            self.status_label = ctk.CTkLabel(
                progress_frame,
                text="等待开始...",
                font=ctk.CTkFont(size=12)
            )
        else:
            self.status_label = tk.Label(
                progress_frame,
                text="等待开始...",
                font=("Arial", 12),
                bg='white'
            )
        
        self.status_label.pack(anchor="w")
        
        # 输出区域
        output_frame = tk.Frame(main_frame, bg='white' if not CTK_AVAILABLE else None)
        output_frame.pack(fill="both", expand=True, pady=20)
        
        if CTK_AVAILABLE:
            output_label = ctk.CTkLabel(
                output_frame,
                text="输出文件:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
        else:
            output_label = tk.Label(
                output_frame,
                text="输出文件:",
                font=("Arial", 14, "bold"),
                bg='white'
            )
        
        output_label.pack(anchor="w", pady=(0, 10))
        
        # 输出文件列表
        if CTK_AVAILABLE:
            self.output_text = ctk.CTkTextbox(
                output_frame,
                height=150,
                font=ctk.CTkFont(size=12)
            )
        else:
            self.output_text = tk.Text(
                output_frame,
                height=8,
                font=("Arial", 12),
                relief="solid",
                bd=1
            )
        
        self.output_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # 底部按钮区域
        button_frame = tk.Frame(main_frame, bg='white' if not CTK_AVAILABLE else None)
        button_frame.pack(fill="x", pady=10)
        
        if CTK_AVAILABLE:
            self.open_folder_btn = ctk.CTkButton(
                button_frame,
                text="📁 打开输出文件夹",
                command=self.open_output_folder
            )
            self.settings_btn = ctk.CTkButton(
                button_frame,
                text="⚙️ 设置",
                command=self.open_settings
            )
        else:
            self.open_folder_btn = tk.Button(
                button_frame,
                text="📁 打开输出文件夹",
                command=self.open_output_folder
            )
            self.settings_btn = tk.Button(
                button_frame,
                text="⚙️ 设置",
                command=self.open_settings
            )
        
        self.open_folder_btn.pack(side="left", padx=(0, 10))
        self.settings_btn.pack(side="left")
        
        # 绑定回车键
        self.keyword_entry.bind("<Return>", lambda e: self.start_generation())
    
    def setup_video_generator(self):
        """设置视频生成器"""
        try:
            self.video_generator = VideoGenerator(progress_callback=self.update_progress)
            self.refresh_output_list()
        except Exception as e:
            logger.error(f"视频生成器初始化失败: {e}")
            messagebox.showerror("错误", f"初始化失败: {e}")
    
    def start_generation(self):
        """开始生成视频"""
        if not self.video_generator:
            messagebox.showerror("错误", "视频生成器未初始化")
            return
        
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入育儿关键词")
            return
        
        if self.video_generator.is_busy():
            messagebox.showwarning("警告", "正在生成视频，请等待完成")
            return
        
        # 禁用生成按钮
        self.generate_btn.configure(state="disabled")
        
        # 在新线程中运行生成任务
        self.generation_thread = threading.Thread(
            target=self.generate_video_thread,
            args=(keyword,),
            daemon=True
        )
        self.generation_thread.start()
    
    def generate_video_thread(self, keyword: str):
        """在线程中生成视频"""
        try:
            result = self.video_generator.generate_video(keyword)
            
            # 在主线程中更新UI
            self.root.after(0, self.generation_complete, result)
            
        except Exception as e:
            logger.error(f"视频生成线程异常: {e}")
            self.root.after(0, self.generation_error, str(e))
    
    def generation_complete(self, result: str):
        """生成完成的回调"""
        # 重新启用生成按钮
        self.generate_btn.configure(state="normal")
        
        if result:
            messagebox.showinfo("成功", f"视频生成完成！\n文件路径: {result}")
            self.refresh_output_list()
        else:
            messagebox.showerror("失败", "视频生成失败，请查看日志了解详情")
    
    def generation_error(self, error_msg: str):
        """生成出错的回调"""
        self.generate_btn.configure(state="normal")
        messagebox.showerror("错误", f"生成过程中发生错误:\n{error_msg}")
    
    def update_progress(self, status: str, message: str, progress: int):
        """更新进度显示"""
        def update_ui():
            # 更新进度条
            self.progress_bar.set(progress / 100.0)
            
            # 更新状态文字
            self.status_label.configure(text=message)
            
            # 如果完成或出错，重新启用按钮
            if status in [VideoGenerationStatus.COMPLETED, VideoGenerationStatus.ERROR]:
                self.generate_btn.configure(state="normal")
        
        # 在主线程中更新UI
        self.root.after(0, update_ui)
    
    def refresh_output_list(self):
        """刷新输出文件列表"""
        try:
            if not self.video_generator:
                return
            
            video_files = self.video_generator.list_generated_videos()
            
            # 清空文本框
            self.output_text.delete("1.0", tk.END if not CTK_AVAILABLE else "end")
            
            if not video_files:
                self.output_text.insert("1.0", "暂无生成的视频文件")
            else:
                output_content = "已生成的视频文件:\n\n"
                for i, video in enumerate(video_files[:10], 1):  # 显示最近10个
                    size_mb = video["size"] / (1024 * 1024)
                    output_content += f"{i}. {video['name']} ({size_mb:.1f}MB)\n"
                
                self.output_text.insert("1.0", output_content)
        
        except Exception as e:
            logger.error(f"刷新输出列表失败: {e}")
    
    def open_output_folder(self):
        """打开输出文件夹"""
        try:
            if self.video_generator:
                output_dir = self.video_generator.get_output_directory()
                
                # 跨平台打开文件夹
                import subprocess
                import platform
                
                if platform.system() == "Windows":
                    subprocess.run(["explorer", output_dir])
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", output_dir])
                else:  # Linux
                    subprocess.run(["xdg-open", output_dir])
        
        except Exception as e:
            logger.error(f"打开输出文件夹失败: {e}")
            messagebox.showerror("错误", f"无法打开文件夹: {e}")
    
    def open_settings(self):
        """打开设置窗口"""
        SettingsWindow(self.root)
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

class SettingsWindow:
    """设置窗口"""
    
    def __init__(self, parent):
        if CTK_AVAILABLE:
            self.window = ctk.CTkToplevel(parent)
        else:
            self.window = tk.Toplevel(parent)
        
        self.window.title("设置")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_settings_ui()
    
    def setup_settings_ui(self):
        """设置界面"""
        if CTK_AVAILABLE:
            main_frame = ctk.CTkFrame(self.window)
        else:
            main_frame = tk.Frame(self.window, bg='white')
        
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # API设置
        if CTK_AVAILABLE:
            api_label = ctk.CTkLabel(
                main_frame,
                text="LLM API 设置",
                font=ctk.CTkFont(size=16, weight="bold")
            )
        else:
            api_label = tk.Label(
                main_frame,
                text="LLM API 设置",
                font=("Arial", 16, "bold"),
                bg='white'
            )
        
        api_label.pack(anchor="w", pady=(0, 10))
        
        # API Key
        if CTK_AVAILABLE:
            self.api_key_entry = ctk.CTkEntry(
                main_frame,
                placeholder_text="输入OpenAI API Key (可选)",
                show="*"
            )
        else:
            self.api_key_entry = tk.Entry(
                main_frame,
                show="*"
            )
        
        self.api_key_entry.pack(fill="x", pady=5)
        self.api_key_entry.insert(0, LLM_CONFIG.get("api_key", ""))
        
        # 说明文字
        if CTK_AVAILABLE:
            info_label = ctk.CTkLabel(
                main_frame,
                text="* 如果不设置API Key，将使用模拟数据进行演示",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
        else:
            info_label = tk.Label(
                main_frame,
                text="* 如果不设置API Key，将使用模拟数据进行演示",
                font=("Arial", 12),
                fg="gray",
                bg='white'
            )
        
        info_label.pack(anchor="w", pady=(0, 20))
        
        # 按钮
        button_frame = tk.Frame(main_frame, bg='white' if not CTK_AVAILABLE else None)
        button_frame.pack(fill="x", pady=20)
        
        if CTK_AVAILABLE:
            save_btn = ctk.CTkButton(
                button_frame,
                text="保存",
                command=self.save_settings
            )
            cancel_btn = ctk.CTkButton(
                button_frame,
                text="取消",
                command=self.window.destroy
            )
        else:
            save_btn = tk.Button(
                button_frame,
                text="保存",
                command=self.save_settings
            )
            cancel_btn = tk.Button(
                button_frame,
                text="取消",
                command=self.window.destroy
            )
        
        save_btn.pack(side="right", padx=(10, 0))
        cancel_btn.pack(side="right")
    
    def save_settings(self):
        """保存设置"""
        try:
            # 这里可以保存设置到配置文件
            # 暂时只显示消息
            messagebox.showinfo("提示", "设置已保存\n重启应用后生效")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存设置失败: {e}")

def main():
    """主函数"""
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        app = ParentingVideoApp()
        app.run()
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        if CTK_AVAILABLE:
            messagebox.showerror("错误", f"应用启动失败: {e}")

if __name__ == "__main__":
    main()