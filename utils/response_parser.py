import json

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