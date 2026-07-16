# 贡献指南

感谢你帮助建设面向中文学习者的 AI 产品知识库。贡献可以是内容纠错、案例、Demo、测试、图表或工程改进。

## 环境准备

安装 Git、uv 和 Python 3.13 或更高版本。克隆仓库后运行 uv sync --all-groups --frozen。不要把真实密钥写入仓库，外部服务配置使用环境变量和示例值。

## 分支与提交

从最新主分支创建 feat、fix 或 docs 前缀的功能分支。提交遵循 Conventional Commits，一次提交只表达一个可审查意图。不要复用已发布编号或无说明地重命名公开路径。

## 内容审查

确认中文表达清晰、术语符合规范、前置知识明确、案例具备边界、练习具有验收标准。规划内容必须标记成熟度，不得伪装成已完成正文。外部事实优先引用官方一手来源并记录检查日期。

## 代码审查

新功能先写失败测试，再实现最小行为。代码需符合 Python 或 TypeScript 规范，处理超时、错误、配置和敏感信息。Demo 必须提供运行、测试、输入、输出和故障排查说明。

## 本地验证

提交前运行 uv run ruff check scripts tests、uv run pytest -v、uv run python scripts/validate.py --root . 和 git diff --check。拉取请求正文应记录精确结果、影响范围、已知限制与后续工作。
