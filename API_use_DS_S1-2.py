# 会让模型输出结构化 JSON。

import os
import json
from openai import OpenAI

CONFIG_PATH = os.path.join(os.path.dirname(__file__),"config.json")

def parse_agent_response(content:str,required_keys:list):
    # === 第一层：JSON 语法校验 ===
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return{
            "success":False,
            "error_type":"invalid_json",
            "message":f"JSON 解析失败：{str(e)}",
            "raw_content":content # 保留原始内容，方便后续反馈给模型修正
        }
    # === 第二层：业务字段校验 ===
    missing_keys=[k for k in required_keys if k not in data]
    if missing_keys:
        return{
            "success":False,
            "error_type":"missing_keys",
            "message":f"缺少必需字段：{missing_keys}",
            "raw_content":content
        }
    # === 两层都通过 ===
    return{"success":True,"data":data}

try:
    with open(CONFIG_PATH,"r",encoding="utf-8") as f:
        config = json.load(f)

except FileNotFoundError:
    raise FileNotFoundError(
       f"❌ 未找到配置文件: {CONFIG_PATH}\n"
       "请在脚本同级目录创建 config.json，格式参考 README"
    )


api_key=config.get("deepseek_api_key")

if not api_key:
    raise ValueError("❌ config.json 中缺少 deepseek_api_key 字段！")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

system_prompt = """
The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

EXAMPLE INPUT: 
Which is the highest mountain in the world? Mount Everest.

EXAMPLE JSON OUTPUT:
{
    "question": "Which is the highest mountain in the world?",
    "answer": "Mount Everest"
}
"""

user_prompt = "Which is the longest river in the world? The Nile River."

messages=[{"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt},]

MAX_RETRIES = 3 # 放置无限循环

for attempt in range(MAX_RETRIES):

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        stream=False,
        response_format={'type': 'json_object'}
    )

    # 👇 新增：打印模型本次的原始返回内容
    raw_content = json.loads(response.choices[0].message.content)
    print(f"\n🤖 第 {attempt+1} 次模型原始输出:\n{raw_content}")

    result = parse_agent_response(
        content=response.choices[0].message.content,
        required_keys=["question", "answer","difficult"]
    )

    if result["success"]:
        print(f"✅ 第 {attempt+1} 次尝试成功:", result["data"])
        break

    # 👇 新增：打印具体的校验失败原因
    print(f"❌ 校验失败原因: {result['message']}")

    correction_msg=(
        f"你上一次输出的 JSON 有以下问题：{result['message']}\n"
        f"你的原始输出是：{result['raw_content']}\n"
        f"请根据以上错误信息修正后，重新输出合法的 JSON。"
    )

    messages.append({"role":"assistant","content":result["raw_content"]})
    print(f"📝 已追加 assistant 消息(原始错误输出):\n{result['raw_content']}")
    messages.append({"role":"user","content":correction_msg})
    print(f"💬 已追加 user 纠错指令:\n{correction_msg}")

    print(f"⚠️ 第 {attempt+1} 次尝试失败，正在让模型自我修正...")

else:
    # MAX_RETRIES 耗尽仍未成功
    print("❌ 达到最大重试次数，Agent 无法自行修正该问题")