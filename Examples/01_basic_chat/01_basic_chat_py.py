# 学习使用LLM API 完成对话

import os
import json
from openai import OpenAI

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(ROOT, "config.json")

try:
    with open(CONFIG_PATH,"r",encoding="utf-8") as f:
        config = json.load(f)

except FileNotFoundError:
    raise FileNotFoundError(
       f"❌ 未找到配置文件: {CONFIG_PATH}\n"
        f"请在项目根目录创建 config.json（可复制 config.example.json），详见 README"
    )


api_key=config.get("deepseek_api_key")

if not api_key:
    raise ValueError("❌ config.json 中缺少 deepseek_api_key 字段！")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role":"system","content":"You are a helpful assistant"},
        {"role":"user","content":"Hello"},
    ],
    stream=False,
    extra_body={"thinking":{"type":"disabled"}}
)

print(response.choices[0].message.content)