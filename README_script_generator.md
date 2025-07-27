# 育儿短视频脚本生成器

## 功能描述

这个Python模块可以根据用户提供的主题关键词，自动生成以卡通宝宝"小泡泡"第一人称视角的育儿短视频脚本。

## 主要特性

- 🎭 以卡通宝宝"小泡泡"的第一人称进行叙述
- 📝 自动生成标题和脚本正文
- 🎯 内容风格感性可爱又不失科学严谨
- ⏱️ 长度控制在30-60秒语速（约300字内）
- 🔧 支持GPT API和本地模型
- 🛡️ 包含错误处理和备用脚本

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基本使用

```python
from generate_script import generate_script

# 设置API密钥（也可以通过环境变量设置）
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# 生成脚本
result = generate_script("宝宝夜醒频繁怎么办")
print(f"标题: {result['title']}")
print(f"脚本: {result['script']}")
```

### 2. 使用自定义API配置

```python
from generate_script import generate_script

result = generate_script(
    topic="宝宝挑食",
    api_key="your-api-key",
    api_base="https://your-api-endpoint.com/v1"
)
```

### 3. 使用类的方式

```python
from generate_script import ParentingScriptGenerator

generator = ParentingScriptGenerator(
    api_key="your-api-key",
    api_base="https://api.openai.com/v1"
)

result = generator.generate_script("宝宝哭闹")
```

## 输出格式

脚本生成器返回一个字典，包含以下字段：

```python
{
    "title": "短视频标题",
    "script": "完整的脚本内容"
}
```

## 示例输出

### 主题：宝宝夜醒频繁怎么办

**标题：** 小泡泡教你解决宝宝夜醒问题

**脚本：** 嗨，我是小泡泡！很多爸爸妈妈都问我，为什么宝宝晚上总是醒呢？其实啊，这是很正常的！小宝宝的睡眠周期比大人短，而且他们还在适应这个世界。我的建议是：1. 建立固定的睡前仪式，比如洗澡、讲故事；2. 保持房间安静和黑暗；3. 不要一哭就立即抱起，可以轻轻拍拍安抚。记住，每个宝宝都是独特的，要有耐心哦！

## 环境变量配置

你可以通过设置环境变量来配置API：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 错误处理

- 如果API调用失败，系统会自动使用备用脚本
- 备用脚本包含常见育儿主题的预设内容
- 所有错误都会记录到日志中

## 支持的育儿主题

系统内置了以下主题的备用脚本：
- 宝宝夜醒频繁
- 宝宝挑食
- 宝宝哭闹

对于其他主题，系统会生成通用的脚本内容。

## 注意事项

1. 确保你有有效的GPT API密钥
2. 网络连接正常以访问API
3. 脚本内容仅供参考，具体育儿建议请咨询专业医生
4. 生成的脚本适合配音使用，长度控制在300字以内

## 许可证

本项目遵循MIT许可证。