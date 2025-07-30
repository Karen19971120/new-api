#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
育儿卡通视频一键通 - 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="parenting-video-generator",
    version="1.0.0",
    author="育儿视频生成器团队",
    author_email="support@example.com",
    description="一款为零基础内容创作者设计的桌面软件，只需输入一个育儿关键词，即可自动生成适配短视频平台的卡通讲解风格视频。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/parenting-video-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "parenting-video=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/**/*", "config/*"],
    },
)