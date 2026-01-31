整理一个python开发的rules在`.cursor/rules/python-dev.mdc`文件中

- 建一个 @dev subagent 和 一个 @formatter subagent格式化

## dev subagent

- conda py312 开发/测试
- 类型注释(符合py 3.12的类型注释规范)
- 写完后交由subagent @formatter 格式化代码



## formatter subagent

- pylint 检查
- mypy 检查
- ruff 检查并格式化
