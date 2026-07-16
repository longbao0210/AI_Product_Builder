# 首批企业级骨架与计算机基础模块实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立可公开发布的 AI Product Builder 企业级知识库骨架、治理与校验体系，并完整交付 `01-Computer-Fundamentals` 模块。

**Architecture:** Markdown 是课程内容的唯一事实来源，`config/*.json` 保存稳定的模块、项目和 Demo 清单，`scripts/knowledge_base/` 负责生成结构与执行静态校验。首批机械生成 40 个模块和 25 个项目的规范入口，人工编写全局文档与 01 模块完整正文，全部结果由 Python 标准库测试和仓库校验命令验收。

**Tech Stack:** Markdown、Mermaid、Python 3.13+、uv、pytest、Ruff、GitHub Actions、JSON Schema 风格配置。

## Global Constraints

- 所有知识库内容使用简体中文，面向中文初学者。
- Python 示例要求 Python 3.13 或更高版本，并使用 `uv` 管理依赖。
- Python Web API 使用 FastAPI 与 Pydantic v2。
- Web 示例使用 React、TypeScript、Tailwind CSS 与 Next.js。
- 小程序示例使用 Taro，并覆盖微信小程序平台约束。
- 模型示例覆盖 OpenAI SDK、Claude SDK 与 Gemini SDK。
- 容器化示例使用 Docker。
- Markdown、Mermaid、术语、命名、编号和代码风格必须全仓统一。
- 首批只将 `01-Computer-Fundamentals` 标记为“已完成”，其余模块和 Demo 必须如实标记成熟度。
- 默认分支为 `main`；实施在功能分支完成并通过 Pull Request 合并。

---

## 文件结构映射

```text
AI_Product_Builder/
├── .github/                  # 社区治理与 CI
├── assets/                   # 可复用静态资源
├── checklists/               # 学习、项目、发布、上线清单
├── config/                   # 模块、项目、Demo 单一事实来源清单
├── diagrams/                 # Mermaid 源文件与图表索引
├── docs/                     # 40 个编号课程模块
├── examples/                 # 200+ Demo 清单与后续实现
├── images/                   # 文档图片
├── learning-paths/           # 30/90/180/365 天学习计划
├── projects/                 # 25 个商业项目
├── prompts/                  # 提示词资产
├── resources/                # 跨模块资源
├── scripts/knowledge_base/   # 结构生成与校验包
├── standards/                # 全仓规范
├── templates/                # 文档和工程模板
└── tests/                    # 生成器与校验器测试
```

`config/catalog.json` 产生稳定目录名和成熟度；`scripts/knowledge_base/scaffold.py` 只创建缺失文件，绝不覆盖人工内容；`scripts/knowledge_base/validate.py` 汇总所有检查并返回非零退出码。生成器和校验器均通过 `Path` 接收仓库根目录，便于隔离测试。

---

### Task 1: 建立 Python 工具链与目录契约测试

**Files:**
- Create: `pyproject.toml`
- Create: `scripts/knowledge_base/__init__.py`
- Create: `scripts/knowledge_base/catalog.py`
- Create: `tests/test_catalog.py`
- Create: `config/catalog.json`

**Interfaces:**
- Consumes: 无。
- Produces: `load_catalog(root: Path) -> dict[str, object]`；后续生成器与校验器共享该接口。

- [ ] **Step 1: 写失败测试，锁定 40 个模块、25 个项目和 200 个 Demo**

```python
from pathlib import Path

from scripts.knowledge_base.catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_has_stable_counts_and_unique_ids() -> None:
    catalog = load_catalog(ROOT)
    modules = catalog["modules"]
    projects = catalog["projects"]
    demos = catalog["demos"]

    assert len(modules) == 40
    assert len(projects) == 25
    assert len(demos) >= 200
    assert len({item["id"] for item in modules}) == 40
    assert len({item["id"] for item in projects}) == 25
    assert len({item["id"] for item in demos}) == len(demos)
    assert modules[0]["slug"] == "Computer-Fundamentals"
    assert projects[-1]["slug"] == "AI-SaaS"
```

- [ ] **Step 2: 运行测试并确认因模块不存在而失败**

Run: `uv run pytest tests/test_catalog.py -v`

Expected: FAIL，包含 `ModuleNotFoundError: No module named 'scripts.knowledge_base.catalog'`。

- [ ] **Step 3: 建立工具链与清单加载接口**

```toml
[project]
name = "ai-product-builder-knowledge-base"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[dependency-groups]
dev = ["pytest>=8.4", "ruff>=0.12"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
target-version = "py313"
line-length = 100
```

```python
import json
from pathlib import Path
from typing import Any


def load_catalog(root: Path) -> dict[str, Any]:
    path = root / "config" / "catalog.json"
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)
```

`config/catalog.json` 使用三个数组：`modules` 项包含 `id`、`slug`、`title`、`status`；`projects` 项包含 `id`、`slug`、`title`、`status`；`demos` 项包含三位数 `id`、`slug`、`title`、`module_id`、`stack`、`status`。模块和项目严格使用设计规格给定顺序；Demo 001—200 按计算机、Python、Git、Linux、Web、AI、LLM、Prompt、Embedding、RAG、Agent、MCP、工作流、前后端、部署、安全、测试与产品主题分配。

- [ ] **Step 4: 运行测试和静态检查**

Run: `uv run pytest tests/test_catalog.py -v`

Expected: PASS，`1 passed`。

Run: `uv run ruff check scripts tests`

Expected: `All checks passed!`。

- [ ] **Step 5: 提交目录契约**

```bash
git add pyproject.toml config/catalog.json scripts/knowledge_base tests/test_catalog.py
git commit -m "build: define knowledge base catalog contract"
```

---

### Task 2: 实现非破坏式仓库骨架生成器

**Files:**
- Create: `scripts/knowledge_base/scaffold.py`
- Create: `tests/test_scaffold.py`
- Create: `scripts/scaffold.py`

**Interfaces:**
- Consumes: `load_catalog(root: Path) -> dict[str, object]`。
- Produces: `scaffold_repository(root: Path) -> list[Path]`，返回本次创建的文件；已存在文件保持不变。

- [ ] **Step 1: 写失败测试验证目录、必需文件与非覆盖行为**

```python
import json
from pathlib import Path

from scripts.knowledge_base.scaffold import MODULE_FILES, scaffold_repository


def test_scaffold_creates_required_files_without_overwrite(tmp_path: Path) -> None:
    catalog = {
        "modules": [{"id": "01", "slug": "Computer-Fundamentals", "title": "计算机基础", "status": "已完成"}],
        "projects": [{"id": "01", "slug": "AI-Chat", "title": "AI 对话", "status": "规划中"}],
        "demos": [{"id": "001", "slug": "hello-terminal", "title": "终端问候", "module_id": "01", "stack": ["Python"], "status": "规划中"}],
    }
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")

    created = scaffold_repository(tmp_path)
    module = tmp_path / "docs" / "01-Computer-Fundamentals"
    assert all((module / name).exists() for name in MODULE_FILES)
    assert (tmp_path / "projects" / "01-AI-Chat" / "README.md").exists()
    assert (tmp_path / "examples" / "README.md").exists()
    assert created

    marker = "人工维护内容\n"
    (module / "README.md").write_text(marker, encoding="utf-8")
    assert scaffold_repository(tmp_path) == []
    assert (module / "README.md").read_text(encoding="utf-8") == marker
```

- [ ] **Step 2: 运行测试并确认缺少生成器**

Run: `uv run pytest tests/test_scaffold.py -v`

Expected: FAIL，包含 `ModuleNotFoundError`。

- [ ] **Step 3: 实现生成器**

```python
from pathlib import Path

from .catalog import load_catalog


MODULE_FILES = (
    "README.md", "SUMMARY.md", "Glossary.md", "Resources.md", "FAQ.md",
    "Best-Practices.md", "Common-Mistakes.md", "Exercises.md", "Projects.md", "Interview.md",
)


def _write_once(path: Path, content: str, created: list[Path]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    created.append(path)


def scaffold_repository(root: Path) -> list[Path]:
    catalog = load_catalog(root)
    created: list[Path] = []
    for item in catalog["modules"]:
        folder = root / "docs" / f'{item["id"]}-{item["slug"]}'
        for filename in MODULE_FILES:
            title = filename.removesuffix(".md")
            content = f'# {item["id"]} {item["title"]} · {title}\n\n> 成熟度：{item["status"]}\n'
            _write_once(folder / filename, content, created)
    for item in catalog["projects"]:
        folder = root / "projects" / f'{item["id"]}-{item["slug"]}'
        content = f'# {item["id"]} {item["title"]}\n\n> 成熟度：{item["status"]}\n'
        _write_once(folder / "README.md", content, created)
    _write_once(root / "examples" / "README.md", "# Demo 索引\n", created)
    return created
```

顶层 `scripts/scaffold.py` 解析 `--root` 参数，调用 `scaffold_repository(Path(args.root).resolve())`，打印创建文件数；异常原样返回非零退出码。

- [ ] **Step 4: 验证测试并生成真实骨架**

Run: `uv run pytest tests/test_scaffold.py -v`

Expected: PASS。

Run: `uv run python scripts/scaffold.py --root .`

Expected: 输出创建文件数；`docs/` 出现 40 个模块目录，`projects/` 出现 25 个项目目录。

- [ ] **Step 5: 提交骨架生成器与生成结果**

```bash
git add scripts tests docs projects examples
git commit -m "feat: scaffold stable curriculum and project structure"
```

---

### Task 3: 建立结构与内容质量校验器

**Files:**
- Create: `scripts/knowledge_base/validate.py`
- Create: `scripts/validate.py`
- Create: `tests/test_validate.py`

**Interfaces:**
- Consumes: 清单与生成后的仓库树。
- Produces: `validate_repository(root: Path) -> list[str]`；空列表表示通过，每条字符串是可定位错误。

- [ ] **Step 1: 写失败测试覆盖缺失文件、占位符与断链**

```python
import json
from pathlib import Path

from scripts.knowledge_base.scaffold import scaffold_repository
from scripts.knowledge_base.validate import validate_repository


def test_validator_reports_actionable_errors(tmp_path: Path) -> None:
    catalog = {
        "modules": [{"id": "01", "slug": "Computer-Fundamentals", "title": "计算机基础", "status": "已完成"}],
        "projects": [],
        "demos": [],
    }
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
    scaffold_repository(tmp_path)
    readme = tmp_path / "docs" / "01-Computer-Fundamentals" / "README.md"
    readme.write_text("# 标题\n\n[坏链接](missing.md)\n", encoding="utf-8")
    (tmp_path / "docs" / "01-Computer-Fundamentals" / "FAQ.md").unlink()

    errors = validate_repository(tmp_path)

    assert any("FAQ.md" in error for error in errors)
    assert any("missing.md" in error for error in errors)
```

- [ ] **Step 2: 运行测试并确认缺少校验器**

Run: `uv run pytest tests/test_validate.py -v`

Expected: FAIL，包含 `ModuleNotFoundError`。

- [ ] **Step 3: 实现聚合校验器**

```python
import re
from pathlib import Path

from .catalog import load_catalog
from .scaffold import MODULE_FILES


LINK_RE = re.compile(r"\[[^]]+\]\((?!https?://|#|mailto:)([^)#]+)(?:#[^)]+)?\)")
FORBIDDEN = ("T" + "ODO", "T" + "BD")


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    catalog = load_catalog(root)
    for item in catalog["modules"]:
        folder = root / "docs" / f'{item["id"]}-{item["slug"]}'
        for filename in MODULE_FILES:
            path = folder / filename
            if not path.is_file():
                errors.append(f"缺少必需文件：{path.relative_to(root)}")
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"禁止占位符 {token}：{path.relative_to(root)}")
        for target in LINK_RE.findall(text):
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"失效链接 {target}：{path.relative_to(root)}")
    return sorted(set(errors))
```

顶层 `scripts/validate.py` 输出每个错误；有错误返回 `1`，无错误打印“知识库校验通过”并返回 `0`。

- [ ] **Step 4: 运行校验器测试**

Run: `uv run pytest tests/test_validate.py -v`

Expected: PASS。

- [ ] **Step 5: 提交校验器**

```bash
git add scripts tests
git commit -m "feat: validate repository structure and local links"
```

---

### Task 4: 编写全仓规范、模板和职责说明

**Files:**
- Create: `REPOSITORY_STRUCTURE.md`
- Create: `standards/README.md`
- Create: `standards/WRITING_STYLE.md`
- Create: `standards/TERMINOLOGY.md`
- Create: `standards/MARKDOWN_STYLE.md`
- Create: `standards/MERMAID_STYLE.md`
- Create: `standards/PYTHON_STYLE.md`
- Create: `standards/TYPESCRIPT_STYLE.md`
- Create: `standards/NAMING.md`
- Create: `standards/VERSIONS.md`
- Create: `templates/README.md`
- Create: `templates/learning-note.md`
- Create: `templates/project/README.md`
- Create: `templates/requirements-document.md`
- Create: `templates/prd.md`
- Create: `templates/design-document.md`
- Create: `templates/system-design.md`
- Create: `templates/api-document.md`
- Create: `templates/prompt.md`
- Create: `templates/mcp-server/README.md`
- Create: `templates/agent/README.md`

**Interfaces:**
- Consumes: 已批准设计规格。
- Produces: 人工作者和校验脚本共同遵循的单一规范来源。

- [ ] **Step 1: 写规范验收测试**

在 `tests/test_repository_docs.py` 中枚举上述文件，并断言每个文件存在、包含唯一 H1、正文不少于 200 个中文字符；`TERMINOLOGY.md` 必须包含“智能体（Agent）”“提示词（Prompt）”“嵌入（Embedding）”“工具调用（Tool Calling）”；`VERSIONS.md` 必须包含验证日期与官方来源列。

- [ ] **Step 2: 运行测试并确认文件缺失**

Run: `uv run pytest tests/test_repository_docs.py -v`

Expected: FAIL，首个错误指向 `REPOSITORY_STRUCTURE.md`。

- [ ] **Step 3: 编写规范与模板正文**

`REPOSITORY_STRUCTURE.md` 逐项解释顶层目录职责、允许内容、禁止内容和维护负责人角色。写作规范固定中文标点、标题层级、第二人称使用、代码前后说明和高风险提示；Mermaid 规范固定 `flowchart LR`、中文节点双引号、简洁配色和源文件归档；代码规范固定 Python 3.13 类型注解、Pydantic v2、TypeScript 严格模式、环境变量和错误处理；模板包含可删除的写作指引，但不得包含空标题或完成状态误导。

- [ ] **Step 4: 运行文档测试与仓库校验**

Run: `uv run pytest tests/test_repository_docs.py -v`

Expected: PASS。

Run: `uv run python scripts/validate.py --root .`

Expected: `知识库校验通过`。

- [ ] **Step 5: 提交规范与模板**

```bash
git add REPOSITORY_STRUCTURE.md standards templates tests/test_repository_docs.py
git commit -m "docs: establish repository standards and templates"
```

---

### Task 5: 编写全局入口、路线图和学习计划

**Files:**
- Create: `README.md`
- Create: `ROADMAP.md`
- Create: `LEARNING_PATH.md`
- Create: `learning-paths/README.md`
- Create: `learning-paths/30-days.md`
- Create: `learning-paths/90-days.md`
- Create: `learning-paths/180-days.md`
- Create: `learning-paths/365-days.md`
- Create: `CHANGELOG.md`
- Create: `LICENSE`

**Interfaces:**
- Consumes: `config/catalog.json`、术语与写作规范。
- Produces: 新学习者的统一入口和四套不冲突的学习节奏。

- [ ] **Step 1: 扩充文档测试**

断言根 README 包含项目介绍、学习价值、路线图、预计时间、最终能力、知识树、目录、学习方法、推荐顺序、实践方法和贡献入口；ROADMAP 包含 Beginner、Intermediate、Advanced、Expert、Master 五个阶段，且每阶段都有学习目标、知识、项目和能力；四套计划分别包含 30、90、180、365 个可识别的“第 N 天”条目。

- [ ] **Step 2: 运行测试确认全局文档尚不存在**

Run: `uv run pytest tests/test_repository_docs.py -v`

Expected: FAIL，报告缺少 `README.md`。

- [ ] **Step 3: 编写全局文档**

README 用 Mermaid 展示从基础到商业化的知识树，明确当前成熟度和推荐顺序；ROADMAP 将 40 个模块映射到五级能力；四套日程每天包含“学习、实践、验收”三项，压缩计划减少广度或项目深度但不跳过安全、测试和部署；LICENSE 使用 Apache License 2.0 官方全文；CHANGELOG 使用中文 Keep a Changelog 结构并登记首批建设内容。

- [ ] **Step 4: 验证文档数量、链接和计划天数**

Run: `uv run pytest tests/test_repository_docs.py -v`

Expected: PASS。

Run: `uv run python scripts/validate.py --root .`

Expected: `知识库校验通过`。

- [ ] **Step 5: 提交全局入口**

```bash
git add README.md ROADMAP.md LEARNING_PATH.md learning-paths CHANGELOG.md LICENSE tests
git commit -m "docs: add roadmap and structured learning paths"
```

---

### Task 6: 建立社区治理、清单、资源与 CI

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `SECURITY.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/ISSUE_TEMPLATE/content-error.yml`
- Create: `.github/ISSUE_TEMPLATE/feature-request.yml`
- Create: `.github/workflows/quality.yml`
- Create: `checklists/README.md`
- Create: `checklists/learning-checklist.md`
- Create: `checklists/project-checklist.md`
- Create: `checklists/release-checklist.md`
- Create: `checklists/production-checklist.md`
- Create: `resources/README.md`
- Create: `prompts/README.md`
- Create: `assets/README.md`
- Create: `images/README.md`
- Create: `diagrams/README.md`

**Interfaces:**
- Consumes: `uv run pytest`、`uv run ruff check`、`uv run python scripts/validate.py --root .`。
- Produces: 贡献流程、质量门禁和 CI 自动执行入口。

- [ ] **Step 1: 写治理文件测试**

断言贡献指南包含环境准备、分支、提交、内容审查、代码审查和验证命令；安全策略包含私密报告渠道说明但不编造邮箱；工作流按顺序安装 uv、Python 3.13、同步依赖、运行 Ruff、pytest 和知识库校验。

- [ ] **Step 2: 运行测试确认治理文件缺失**

Run: `uv run pytest tests/test_repository_docs.py -v`

Expected: FAIL，报告缺少 `CONTRIBUTING.md`。

- [ ] **Step 3: 编写治理文档和 CI**

CI 使用 `actions/checkout`、`astral-sh/setup-uv` 与 `actions/setup-python` 的当前稳定主版本标签；所有第三方 Action 在实施时查阅官方仓库并锁定已验证版本。安全报告通过 GitHub Private Vulnerability Reporting，引导贡献者不要在公开 Issue 中披露漏洞。四张清单使用可勾选项目并包含明确放行条件。

- [ ] **Step 4: 运行全套基础验证**

Run: `uv run ruff check scripts tests`

Expected: `All checks passed!`。

Run: `uv run pytest -v`

Expected: 全部 PASS。

Run: `uv run python scripts/validate.py --root .`

Expected: `知识库校验通过`。

- [ ] **Step 5: 提交治理与 CI**

```bash
git add CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md .github checklists resources prompts assets images diagrams tests
git commit -m "chore: add governance checklists and quality workflow"
```

---

### Task 7: 完善 40 个模块入口与 25 个项目规划

**Files:**
- Modify: `docs/02-Python/README.md` through `docs/40-Career/Interview.md`
- Modify: `projects/01-AI-Chat/README.md` through `projects/25-AI-SaaS/README.md`
- Create: `projects/README.md`
- Create: `examples/CATALOG.md`

**Interfaces:**
- Consumes: 清单、统一模板、课程依赖关系。
- Produces: 每个后续模块真实的范围、章节规划与验收标准；每个项目真实的产品范围和里程碑。

- [ ] **Step 1: 写成熟度与内容完整性测试**

遍历模块 02—40，断言十个固定文件均包含模块专属标题、成熟度“规划中”、前置知识、内容边界和验收标准，且不存在通用复制文案；遍历 25 个项目，断言 README 包含目标用户、核心问题、功能范围、技术栈、前置模块、里程碑、交付物和验收标准；Demo 目录表必须覆盖清单全部 ID。

- [ ] **Step 2: 运行测试并确认机械骨架内容不足**

Run: `uv run pytest tests/test_catalog_content.py -v`

Expected: FAIL，指出模块 02 缺少“前置知识”。

- [ ] **Step 3: 按模块与项目清单编写专属规划内容**

每个模块 README 给出 6—12 个编号章节题目及依赖，其他九个文件给出该主题的专属知识范围和后续填充规则；不得使用虚构完成状态。每个项目使用用户给定的 25 项顺序，将功能范围映射到真实课程前置条件，并定义从概念验证、最小可行产品、生产加固到上线复盘的里程碑。

- [ ] **Step 4: 验证全部索引和成熟度**

Run: `uv run pytest tests/test_catalog_content.py -v`

Expected: PASS。

Run: `uv run python scripts/validate.py --root .`

Expected: `知识库校验通过`。

- [ ] **Step 5: 提交规划索引**

```bash
git add docs projects examples tests/test_catalog_content.py
git commit -m "docs: map curriculum projects and demo catalog"
```

---

### Task 8: 完整编写 01-Computer-Fundamentals 模块

**Files:**
- Modify: `docs/01-Computer-Fundamentals/README.md`
- Modify: `docs/01-Computer-Fundamentals/SUMMARY.md`
- Modify: `docs/01-Computer-Fundamentals/Glossary.md`
- Modify: `docs/01-Computer-Fundamentals/Resources.md`
- Modify: `docs/01-Computer-Fundamentals/FAQ.md`
- Modify: `docs/01-Computer-Fundamentals/Best-Practices.md`
- Modify: `docs/01-Computer-Fundamentals/Common-Mistakes.md`
- Modify: `docs/01-Computer-Fundamentals/Exercises.md`
- Modify: `docs/01-Computer-Fundamentals/Projects.md`
- Modify: `docs/01-Computer-Fundamentals/Interview.md`
- Create: `docs/01-Computer-Fundamentals/01-Computer-and-Information.md`
- Create: `docs/01-Computer-Fundamentals/02-Hardware-and-Software.md`
- Create: `docs/01-Computer-Fundamentals/03-Operating-System-and-Process.md`
- Create: `docs/01-Computer-Fundamentals/04-File-System.md`
- Create: `docs/01-Computer-Fundamentals/05-Network-Fundamentals.md`
- Create: `docs/01-Computer-Fundamentals/06-Terminal-and-Environment.md`
- Create: `docs/01-Computer-Fundamentals/07-Data-and-Encoding.md`
- Create: `docs/01-Computer-Fundamentals/08-From-Source-to-Program.md`
- Create: `docs/01-Computer-Fundamentals/09-Development-Environment.md`
- Create: `docs/01-Computer-Fundamentals/10-Module-Project.md`

**Interfaces:**
- Consumes: 统一章节模板、术语规范、Mermaid 规范。
- Produces: 模块 01 完整学习闭环，并将“下一章”连接到模块 02。

- [ ] **Step 1: 写章节模板测试**

在 `tests/test_chapter_template.py` 中定义设计规格的 19 个二级标题（H1 标题不计），遍历十章并断言标题按固定顺序出现；每章至少包含一个 `flowchart`、一个架构图、一个 `sequenceDiagram`、一个可验证代码块、一个 Demo、练习验收、项目任务、最佳实践、错误、FAQ、总结和有效下一章链接。

- [ ] **Step 2: 运行测试确认章节缺失**

Run: `uv run pytest tests/test_chapter_template.py -v`

Expected: FAIL，报告缺少第一章文件。

- [ ] **Step 3: 按统一模板逐章编写完整内容**

十章从信息表示、软硬件、进程、文件系统、网络、终端、编码、程序执行、开发环境推进到综合项目。生活案例使用快递、图书馆、餐厅等中文读者熟悉场景；工作案例映射到 AI 产品故障诊断。代码示例只使用 Python 3.13 标准库或明确的终端命令，给出输入、预期输出和跨平台差异。综合项目构建“AI 产品运行环境体检器”，采集运行时、操作系统、编码、网络解析和磁盘信息，不采集敏感数据。

- [ ] **Step 4: 完善模块配套十文件**

模块 README 给出知识地图、预计 12—18 小时、前置条件、章节导航与完成标准；术语表覆盖二进制、CPU、内存、进程、线程、文件系统、路径、IP、DNS、端口、字符编码、解释器和环境变量；资源优先链接 Python、Microsoft、Linux Foundation、MDN、IETF 等官方一手资料并记录检查日期；练习、项目和面试文件均提供分级题目、验收或参考思路。

- [ ] **Step 5: 运行章节、链接和全仓测试**

Run: `uv run pytest tests/test_chapter_template.py -v`

Expected: PASS。

Run: `uv run pytest -v`

Expected: 全部 PASS。

Run: `uv run python scripts/validate.py --root .`

Expected: `知识库校验通过`。

- [ ] **Step 6: 提交模块 01**

```bash
git add docs/01-Computer-Fundamentals tests/test_chapter_template.py
git commit -m "docs: complete computer fundamentals module"
```

---

### Task 9: 增强 Mermaid、锚点、秘密与 Demo 元数据检查

**Files:**
- Modify: `scripts/knowledge_base/validate.py`
- Modify: `tests/test_validate.py`
- Create: `.gitignore`
- Create: `.env.example`

**Interfaces:**
- Consumes: 全仓 Markdown、Mermaid 代码块与 Demo 清单。
- Produces: 可在本地和 CI 复用的最终质量门禁。

- [ ] **Step 1: 为新规则写失败测试**

测试分别构造重复 H1、未闭合 Mermaid 围栏、真实密钥形态、Demo 缺少三位数 ID、已完成模块仍含“规划中”等输入，断言校验错误包含相对路径和规则名称；另写干净样例断言无错误。

- [ ] **Step 2: 运行测试确认规则尚未实现**

Run: `uv run pytest tests/test_validate.py -v`

Expected: FAIL，至少一个新规则未报告错误。

- [ ] **Step 3: 实现规则并保持函数单一职责**

将检查拆为 `check_structure`、`check_markdown`、`check_links`、`check_mermaid_fences`、`check_secrets`、`check_catalog_coverage`，每个函数签名为 `(root: Path, catalog: dict[str, object]) -> list[str]`；`validate_repository` 只聚合、去重和排序。秘密检查允许 `.env.example` 中的明显示例值，拒绝常见供应商真实令牌前缀和高熵硬编码值。

- [ ] **Step 4: 运行全部质量门禁**

Run: `uv run ruff check scripts tests`

Expected: `All checks passed!`。

Run: `uv run pytest -v`

Expected: 全部 PASS。

Run: `uv run python scripts/validate.py --root .`

Expected: `知识库校验通过`。

- [ ] **Step 5: 提交最终校验增强**

```bash
git add scripts tests .gitignore .env.example
git commit -m "test: enforce knowledge base quality gates"
```

---

### Task 10: 最终审计、版本记录与 Pull Request

**Files:**
- Modify: `CHANGELOG.md`
- Create: `docs/releases/0.1.0.md`
- Create: `reports/batch-01-validation.md`

**Interfaces:**
- Consumes: 所有首批交付和验证输出。
- Produces: 可审查的 `0.1.0` 首批发布说明与 Pull Request。

- [ ] **Step 1: 运行最终验证并记录精确结果**

Run: `uv sync --all-groups`

Expected: 依赖解析成功并生成或更新 `uv.lock`。

Run: `uv run ruff check scripts tests`

Expected: `All checks passed!`。

Run: `uv run pytest -v`

Expected: 全部 PASS；将测试数量和耗时写入验证报告。

Run: `uv run python scripts/validate.py --root .`

Expected: `知识库校验通过`。

Run: `git diff --check`

Expected: 无输出，退出码为 0。

- [ ] **Step 2: 审计交付数量**

统计并记录模块目录数、固定模块文件数、项目目录数、Demo 清单数、模块 01 章节数、Markdown 文件数、Mermaid 图数量和失效链接数。验收值分别不低于 40、400、25、200、10；失效链接必须为 0。

- [ ] **Step 3: 编写发布说明和验证报告**

`docs/releases/0.1.0.md` 说明已完成范围、成熟度边界、学习入口、验证命令和下一批 `02-Python`；`reports/batch-01-validation.md` 记录环境、命令、结果、数量审计和已知限制，不填写未经执行的结果。

- [ ] **Step 4: 提交发布资料**

```bash
git add CHANGELOG.md docs/releases/0.1.0.md reports/batch-01-validation.md uv.lock
git commit -m "docs: prepare batch one validation report"
```

- [ ] **Step 5: 推送功能分支并创建 Pull Request**

Run: `git status --short --branch`

Expected: 工作树干净，当前分支为首批功能分支。

推送分支后创建 Pull Request，标题为 `docs: 建立知识库骨架并完成计算机基础模块`；正文必须包含设计规格链接、交付范围、验证结果、成熟度说明和下一批计划。不得直接推送或合并到 `main`。

---

## 计划自审结果

- 规格覆盖：40 个模块骨架、25 个项目规划、200+ Demo 清单、四套学习计划、统一规范、模板、清单、CI、质量脚本和完整模块 01 均有对应任务。
- 占位符检查：计划未要求在成品正文保留未完成占位；后续内容统一使用可验证的“规划中”成熟度。
- 接口一致性：生成器与校验器均复用 `load_catalog(root)`；所有入口均接受仓库根路径；验证命令在本地和 CI 一致。
- 范围一致性：首批不伪造完成 02—40 模块或 200 个 Demo 实现，最终目标保持不变。
