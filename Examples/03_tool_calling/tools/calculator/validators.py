import re

def validate_calculator_expression(expr: str) -> tuple[bool, str]:
    """白名单校验：只允许数字、运算符、括号、小数点、空格"""
    # 去除首尾空格后检查是否为空
    expr = expr.strip()
    if not expr:
        return False, "表达式不能为空"
    
    # 白名单正则：匹配合法字符
    if not re.fullmatch(r'[0-9+\-*/().\s]+', expr):
        return False, "表达式包含非法字符"
    
    # 额外检查：防止连续运算符（如 "1++2"）
    if re.search(r'[+\-*/]{2,}', expr):
        return False, "表达式包含连续运算符"
    
    return True, ""