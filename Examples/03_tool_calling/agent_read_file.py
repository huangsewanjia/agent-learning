# API_use_DS_S1-3.py
import os
import json
from tools import TOOLS, TOOL_FUNCTIONS
from openai import OpenAI

# ================= 配置加载 =================
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(ROOT, "config.json")

try:
    with open(CONFIG_PATH,'r',encoding='utf-8') as f:
        config=json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(
        f"❌ 未找到配置文件: {CONFIG_PATH}\n"
        f"请在项目根目录创建 config.json（可复制 config.example.json），详见 README"
    )

api_key = config.get("deepseek_api_key")

if not api_key:
    raise ValueError("❌ config.json 中缺少 deepseek_api_key 字段！")

client=OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ================= Agent 核心循环 =================
messages = [{"role": "user", "content": "阅读'五问理解'文件，总结这个文章的内容"}] # 发现带上后缀会更方便AI的定位，
print(f"User>\t {messages[0]['content']}")

while True:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOLS,
    )
    
    msg = response.choices[0].message
    
    # ✅ 1. 如果没有工具调用，说明模型已给出最终回答，打印并退出
    if not msg.tool_calls:
        print(f"Model>\t {msg.content}")
        break
        
    # ✅ 2. 将包含 tool_calls 的 assistant 消息追加到上下文
    messages.append(msg.model_dump())
    
    # ✅ 3. 遍历并执行所有工具调用
    for tool_call in msg.tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        print(f"Tool>\t Calling {func_name} with {args}")
        
        # 安全获取函数，避免 KeyError 导致程序崩溃
        func = TOOL_FUNCTIONS.get(func_name)
        if func:
            try:
                result = func(**args)
            except Exception as e:
                result = f"Execution Error: {str(e)}"
        else:
            result = f"Error: Unknown tool '{func_name}'"
            
        print(f"Tool>\t Result: {result}")
        
        # ✅ 4. 将工具执行结果追加到消息流，供下一轮模型读取
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })