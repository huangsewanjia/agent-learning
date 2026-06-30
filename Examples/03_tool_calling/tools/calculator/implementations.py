from .validators import validate_calculator_expression

def calculator(expression: str) -> str:
    """安全计算器：先校验再执行"""
    is_valid, error_msg = validate_calculator_expression(expression)
    if not is_valid:
        return f"❌ 参数校验失败：{error_msg}"
    
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except ZeroDivisionError:
        return "❌ 计算错误：除数不能为零"
    except Exception as e:
        return f"❌ 计算异常：{str(e)}"