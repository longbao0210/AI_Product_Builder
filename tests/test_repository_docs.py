import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STANDARD_AND_TEMPLATE_FILES = (
    "REPOSITORY_STRUCTURE.md",
    "standards/README.md",
    "standards/WRITING_STYLE.md",
    "standards/TERMINOLOGY.md",
    "standards/MARKDOWN_STYLE.md",
    "standards/MERMAID_STYLE.md",
    "standards/PYTHON_STYLE.md",
    "standards/TYPESCRIPT_STYLE.md",
    "standards/NAMING.md",
    "standards/VERSIONS.md",
    "templates/README.md",
    "templates/learning-note.md",
    "templates/project/README.md",
    "templates/requirements-document.md",
    "templates/prd.md",
    "templates/design-document.md",
    "templates/system-design.md",
    "templates/api-document.md",
    "templates/prompt.md",
    "templates/mcp-server/README.md",
    "templates/agent/README.md",
)


def test_standards_and_templates_are_substantial() -> None:
    for relative in STANDARD_AND_TEMPLATE_FILES:
        path = ROOT / relative
        assert path.is_file(), f"缺少文件：{relative}"
        text = path.read_text(encoding="utf-8")
        h1_count = sum(line.startswith("# ") for line in text.splitlines())
        chinese_characters = re.findall(r"[\u4e00-\u9fff]", text)
        assert h1_count == 1, f"{relative} 必须且只能有一个一级标题"
        assert len(chinese_characters) >= 200, f"{relative} 中文说明不足 200 字"


def test_terminology_and_version_policy_are_explicit() -> None:
    terminology = (ROOT / "standards" / "TERMINOLOGY.md").read_text(encoding="utf-8")
    for term in (
        "智能体（Agent）",
        "提示词（Prompt）",
        "嵌入（Embedding）",
        "工具调用（Tool Calling）",
    ):
        assert term in terminology

    versions = (ROOT / "standards" / "VERSIONS.md").read_text(encoding="utf-8")
    assert "验证日期" in versions
    assert "官方来源" in versions
