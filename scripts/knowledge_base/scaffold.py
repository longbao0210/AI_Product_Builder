from pathlib import Path

from .catalog import load_catalog


MODULE_FILES = (
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

FILE_TITLES = {
    "README.md": "模块导读",
    "SUMMARY.md": "模块总结",
    "Glossary.md": "术语表",
    "Resources.md": "学习资源",
    "FAQ.md": "常见问题",
    "Best-Practices.md": "最佳实践",
    "Common-Mistakes.md": "常见错误",
    "Exercises.md": "练习",
    "Projects.md": "项目",
    "Interview.md": "面试准备",
}


def _write_once(path: Path, content: str, created: list[Path]) -> None:
    """仅创建不存在的文件，保护人工维护内容。"""
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    created.append(path)


def scaffold_repository(root: Path) -> list[Path]:
    """依据稳定清单创建课程、项目和 Demo 入口。"""
    catalog = load_catalog(root)
    created: list[Path] = []

    for item in catalog["modules"]:
        folder = root / "docs" / f'{item["id"]}-{item["slug"]}'
        for filename in MODULE_FILES:
            content = (
                f'# {item["id"]} {item["title"]} · {FILE_TITLES[filename]}\n\n'
                f'> 成熟度：{item["status"]}\n'
            )
            _write_once(folder / filename, content, created)

    for item in catalog["projects"]:
        folder = root / "projects" / f'{item["id"]}-{item["slug"]}'
        content = f'# {item["id"]} {item["title"]}\n\n> 成熟度：{item["status"]}\n'
        _write_once(folder / "README.md", content, created)

    _write_once(root / "examples" / "README.md", "# Demo 索引\n", created)
    return created
