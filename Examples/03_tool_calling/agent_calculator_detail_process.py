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

# ================= 可视化辅助函数 =================
def print_block(title, content, color_code="\033[0m"):
    """格式化打印区块，支持颜色高亮"""
    reset = "\033[0m"
    print(f"\n{color_code}{'='*20} {title} {'='*20}{reset}")
    if isinstance(content, (dict, list)):
        print(json.dumps(content, indent=2, ensure_ascii=False))
    else:
        print(content)
    print(f"{color_code}{'='*50}{reset}\n")

# ================= Agent 核心循环 =================
messages = [{"role": "user", "content": "计算 (12+8)*3.5"}]
MAX_ITERATIONS = 10

print_block("🚀 初始用户输入", messages[0]["content"], "\033[92m")

for step in range(1, MAX_ITERATIONS + 1):
    # ---------- 1. 展示发送给 LLM 的完整请求 ----------
    request_payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "tools": TOOLS  # 👈 这就是 LLM 用来做“路由判断”的菜单
    }
    print_block(f"📤 [Step {step}] 发送给 LLM 的完整 Payload", request_payload, "\033[94m")
    
    response = client.chat.completions.create(**request_payload)
    msg = response.choices[0].message
    
    # ---------- 2. 展示 LLM 返回的原始决策 ----------
    raw_response = {
        "content": msg.content,
        "tool_calls": [tc.model_dump() for tc in msg.tool_calls] if msg.tool_calls else None
    }
    print_block(f"📥 [Step {step}] LLM 返回的原始决策", raw_response, "\033[93m")
    
    # ---------- 3. 判断是否需要调用工具 ----------
    if not msg.tool_calls:
        print_block("✅ 最终答案生成", msg.content, "\033[92m")
        break
        
    # 将 assistant 的决策消息加入上下文
    messages.append(msg.model_dump())
    
    # ---------- 4. 本地工具执行与映射 ----------
    for tool_call in msg.tool_calls:
        func_name = tool_call.function.name
        raw_args = tool_call.function.arguments
        
        # 4.1 参数解析校验
        try:
            args = json.loads(raw_args)
            parse_status = f"✅ JSON 解析成功: {args}"
        except json.JSONDecodeError as e:
            parse_status = f"❌ JSON 解析失败: {e}"
            args = None
            
        print_block(f"🔧 工具执行: {func_name}", parse_status, "\033[95m")
        
        # 4.2 函数查找与执行
        if args is not None:
            func = TOOL_FUNCTIONS.get(func_name)
            if func:
                try:
                    result = func(**args)
                    exec_status = f"✅ 执行成功\n返回值: {result}"
                except Exception as e:
                    result = f"Execution Error: {str(e)}"
                    exec_status = f"❌ 执行异常: {result}"
            else:
                result = f"Unknown tool: {func_name}"
                exec_status = f"❌ 未找到工具: {result}"
                
            print_block(f"⚙️ {func_name} 执行结果", exec_status, "\033[95m")
        else:
            result = parse_status
            
        # ---------- 5. 组装回传消息 ----------
        tool_msg = {
            "role": "tool",
            "tool_call_id": tool_call.id,  # 👈 关键：ID 必须与 LLM 决策中的 ID 严格对应
            "content": str(result)
        }
        messages.append(tool_msg)
        print_block("🔄 已追加到上下文的 Tool Message", tool_msg, "\033[96m")

else:
    print_block("⚠️ 安全阀触发", f"达到最大迭代次数 {MAX_ITERATIONS}，强制停止", "\033[91m")