# Agent Learning

这是一个**从零手写 AI Agent** 的个人学习项目。为了帮助大家更好地理解 Agent 的底层运行机制，本项目**未使用任何第三方 Agent 框架**，而是直接基于 **DeepSeek API** 从最基础的 LLM 调用开始逐步构建。

项目包含完整的学习笔记与可运行示例，带你一步步实现从基础对话 → 结构化 JSON 输出 → 工具调用循环的完整演进过程。

## 学习路径

| 阶段 | 目录 | 入口脚本 | 学到什么 |
|------|------|----------|----------|
| 1 | `examples/01_basic_chat/` | `01_basic_chat_py.py` | 调用 DeepSeek API，完成一次基础对话 |
| 2 | `examples/02_structured_json/` | `02_structured_json_demo.py` | 强制 JSON 输出、字段校验、有限次自我纠错 |
| 3a | `examples/03_tool_calling/` | `agent_calculator.py` | Agent 工具调用主循环（计算器，简洁日志） |
| 3b | `examples/03_tool_calling/` | `agent_calculator_detail_process.py` | 完整 payload / tool message 可视化调试 |
| 3c | `examples/03_tool_calling/` | `agent_read_file.py` | 读文件工具 + 多轮推理 |

## 项目结构

```text
agent-learning/
├── config.example.json      # 配置模板（提交到 Git）
├── config.json              # 本地 API Key（已在 .gitignore，勿提交）
├── examples/
│   ├── 01_basic_chat/       # 阶段 1：基础对话
│   ├── 02_structured_json/  # 阶段 2：结构化 JSON + utils/
│   └── 03_tool_calling/     # 阶段 3：工具调用 + tools/
├── Test source/                # 示例用的本地文件（如 五问理解.md）
├── Notes/                   # 学习过程笔记（Cursor 对话导出等）
└── README.md

快速开始
安装依赖
```Bash
pip install openai
```
配置 API Key
在项目根目录（与 `config.example.json` 同级）：
```Bash
cp config.example.json config.json
# 编辑 config.json，填入 deepseek_api_key
```
## 配置说明

所有示例脚本通过固定相对路径定位项目根目录：从 `examples/<阶段>/` 向上两级读取 `config.json`。
将根目录中的`config.example.json` 改为 `config.json` 并填入 API Key。

## 核心概念

### 阶段 2：结构化输出与重试

- API 参数：`response_format={"type": "json_object"}`

- 校验：`utils/response_parser.parse_agent_response(content, required_keys)`

- 校验失败时，将错误输出与纠错指令追加到 messages，最多重试 `MAX_RETRIES` 次

### 阶段 3：工具调用循环

1. 将 `tools.TOOLS` 传给 API 的 `tools` 参数

2. 若 `message.tool_calls` 为空 → 输出最终答案并结束

3. 否则执行 `tools.TOOL_FUNCTIONS[name](**args)`

4. 以 `role: "tool"` \+ 对应 `tool_call_id` 写回 messages

5. 回到步骤 1

## 测试数据

- `Test source`：供 `agent_read_file.py` 读取

## License

见 [LICENSE]
