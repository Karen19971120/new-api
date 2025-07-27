# 育儿短视频脚本生成器

## 功能介绍

`generate_script.py` 是一个使用 GPT API 生成育儿短视频脚本的 Python 模块。脚本以卡通宝宝"小泡泡"的第一人称视角进行叙述，内容风格感性可爱且科学严谨。

## 特性

- 🎭 以可爱的卡通宝宝"小泡泡"第一人称叙述
- 📝 生成包含标题和脚本正文的完整内容
- ⏰ 控制在 30-60 秒语速（约 300 字内）
- 🔬 内容科学严谨，提供实用的育儿建议
- 💖 语言风格感性可爱，富有亲和力
- 🔧 支持本地模型和自定义 API 端点

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 设置 API 密钥

```bash
export OPENAI_API_KEY="your-api-key-here"
```

或者在代码中直接传入：

```python
from generate_script import generate_parenting_script

result = generate_parenting_script(
    "宝宝夜醒频繁怎么办",
    api_key="your-api-key-here"
)
```

### 2. 基本用法

```python
from generate_script import generate_parenting_script

# 生成脚本
result = generate_parenting_script("宝宝夜醒频繁怎么办")

print("标题:", result["title"])
print("脚本:", result["script"])
```

### 3. 使用本地模型

```python
from generate_script import generate_parenting_script

# 使用本地 Ollama 等模型
result = generate_parenting_script(
    "如何培养宝宝的睡眠习惯",
    base_url="http://localhost:11434/v1"
)
```

### 4. 类方式使用

```python
from generate_script import ScriptGenerator

generator = ScriptGenerator(api_key="your-key")
result = generator.generate_script("宝宝不爱吃饭怎么办")
```

## 输入参数

- **topic** (str): 育儿主题关键词，如"宝宝夜醒频繁怎么办"
- **api_key** (str, 可选): OpenAI API 密钥
- **base_url** (str, 可选): 自定义 API 端点，支持本地模型

## 输出格式

```python
{
    "title": "吸引人的短视频标题",
    "script": "以小泡泡第一人称叙述的脚本内容（约300字）"
}
```

## 示例主题

- "宝宝夜醒频繁怎么办"
- "如何培养宝宝的睡眠习惯"
- "宝宝不爱吃饭怎么办"
- "如何和宝宝建立亲子关系"
- "宝宝学走路的注意事项"

## 错误处理

脚本包含完善的错误处理机制：
- API 调用失败时自动生成备用脚本
- JSON 解析失败时手动提取内容
- 提供友好的错误提示信息

## 环境变量

- `OPENAI_API_KEY`: OpenAI API 密钥
- `OPENAI_BASE_URL`: 自定义 API 基础 URL（可选）

## 注意事项

1. 确保有稳定的网络连接（除非使用本地模型）
2. API 调用可能产生费用，请合理使用
3. 生成的内容仅供参考，具体育儿问题请咨询专业医生