# 综合项目：AI 产品运行环境体检器

## 学习目标

把前九章的系统知识组合为一个安全、可测试的环境体检器，能够检查 Python、操作系统、编码、路径、磁盘和本机名称解析。

## 为什么学

真实项目不会按章节出现故障。一个启动失败可能同时涉及版本、目录、配置与网络。综合项目训练你组织检查顺序、隔离失败并形成可交付报告。

## 适用场景

适用于本地开发初始化、CI 前置检查、容器启动探针和客服诊断。体检器只读取必要元数据，不自动修改系统，也不采集用户名、密钥或完整环境变量。

## 核心概念

核心是检查项、结果模型、调度器、报告器和退出码。每个检查独立返回状态与摘要，单项失败不能阻止其他检查；总体状态由明确规则聚合。

## 生活案例

出门前分别检查证件、天气、交通和设备电量。某一项失败会被记录并采取对应行动，不应让整张清单消失。计算机检查同样需要独立结果和清楚证据。

## 工作案例

AI 服务在新服务器启动前运行体检器，发现 Python 版本正确但磁盘空间不足。团队先扩容而不是更换模型，避免了错误方向和上线事故。

## 理论

可靠诊断遵循数据最小化、检查隔离、稳定模式和非零退出码。环境相关结果使用类型或范围验收，不能把某台电脑的具体数值写成永久预期。

## 流程图

~~~mermaid
flowchart LR
    A["读取允许列表"] --> B["执行独立检查"]
    B --> C["收集成功与失败"]
    C --> D["生成文本与 JSON"]
    D --> E["根据规则返回退出码"]
~~~

## 架构图

~~~mermaid
flowchart LR
    CLI["命令行入口"] --> RUN["调度器"]
    RUN --> PY["Python 检查"]
    RUN --> FS["文件与磁盘检查"]
    RUN --> NET["DNS 检查"]
    PY --> REPORT["报告器"]
    FS --> REPORT
    NET --> REPORT
~~~

## 时序图

~~~mermaid
sequenceDiagram
    participant U as 用户
    participant R as 调度器
    participant C as 检查项
    participant O as 报告器
    U->>R: 启动体检
    loop 每个检查
        R->>C: 执行
        C-->>R: 状态与摘要
    end
    R->>O: 汇总结果
    O-->>U: 报告与退出码
~~~

## 代码示例

```python
from pathlib import Path
import platform
import shutil
import socket
import sys

report = {
    "python": platform.python_version(),
    "platform": platform.system(),
    "encoding": sys.getdefaultencoding(),
    "localhost": socket.gethostbyname("localhost"),
    "free_gib": round(shutil.disk_usage(Path.cwd()).free / 2**30, 2),
}
for key, value in report.items():
    print(f"{key}: {value}")
```

预期输出：Python 版本、操作系统、UTF-8 编码、本机地址和可用磁盘；环境相关数值可以不同。

## Demo

保存为 main.py，使用 Python 3.13 运行。分别记录文本输出和 JSON 设计草图，再模拟一个独立检查失败，确认其余结果仍然存在。

## 练习

1. 为每个结果定义名称、状态、摘要和安全详情。
2. 将 Python 版本不足定义为失败。
3. 为 DNS 异常设计不影响其他检查的错误结果。

验收：测试覆盖正常、单项失败与总体退出码。

## 项目

完成环境体检器源码、pyproject.toml、uv.lock、README、测试和示例报告。增加文本与 JSON 输出，不执行修复命令。

## 最佳实践

- 使用允许列表读取系统信息。
- 每个检查只承担一个职责。
- 捕获具体异常并保留安全上下文。
- 环境相关断言使用范围与类型。
- 输出模式保持稳定以便自动化消费。

## 常见错误

- 单项异常导致整个报告中断。
- 打印全部环境变量造成秘密泄露。
- 把环境差异当作测试失败。
- 自动执行高权限修复，扩大副作用。

## FAQ

**问：体检器可以自动修复吗？**

答：首版不可以。诊断与修复权限不同，自动修复需要独立设计、确认与回滚。

**问：是否要连接外部模型？**

答：不需要。项目验证基础运行环境，应保持快速、确定和低风险。

## 总结

你已经把信息、硬件、进程、文件、网络、终端、编码、运行时和开发环境组合为可验证工具，并建立了进入 Python 模块所需的系统排错基础。

## 下一章

[下一模块：Python](../02-Python/README.md)
