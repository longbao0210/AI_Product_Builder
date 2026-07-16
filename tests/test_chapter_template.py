from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "01-Computer-Fundamentals"
CHAPTERS = (
    "01-Computer-and-Information.md",
    "02-Hardware-and-Software.md",
    "03-Operating-System-and-Process.md",
    "04-File-System.md",
    "05-Network-Fundamentals.md",
    "06-Terminal-and-Environment.md",
    "07-Data-and-Encoding.md",
    "08-From-Source-to-Program.md",
    "09-Development-Environment.md",
    "10-Module-Project.md",
)
SECTIONS = (
    "学习目标",
    "为什么学",
    "适用场景",
    "核心概念",
    "生活案例",
    "工作案例",
    "理论",
    "流程图",
    "架构图",
    "时序图",
    "代码示例",
    "Demo",
    "练习",
    "项目",
    "最佳实践",
    "常见错误",
    "FAQ",
    "总结",
    "下一章",
)


def test_computer_fundamentals_chapters_follow_the_template() -> None:
    for filename in CHAPTERS:
        path = MODULE / filename
        assert path.is_file(), f"缺少章节：{filename}"
        text = path.read_text(encoding="utf-8")
        positions = [text.index(f"## {section}") for section in SECTIONS]
        assert positions == sorted(positions), f"章节标题顺序错误：{filename}"
        assert text.count("flowchart ") >= 2
        assert "sequenceDiagram" in text
        assert "```python" in text
        assert "预期输出" in text
        assert "](" in text[text.index("## 下一章") :]


def test_computer_fundamentals_module_files_are_complete() -> None:
    required = (
        "README.md",
        "SUMMARY.md",
        "Glossary.md",
        "Resources.md",
        "FAQ.md",
        "Best-Practices.md",
        "Common-Mistakes.md",
        "Exercises.md",
        "Projects.md",
        "Interview.md",
    )
    for filename in required:
        text = (MODULE / filename).read_text(encoding="utf-8")
        assert "成熟度：已完成" in text
        assert len(text) >= 800, f"模块配套文件内容不足：{filename}"
