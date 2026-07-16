import re
from pathlib import Path

from .catalog import load_catalog
from .scaffold import MODULE_FILES


LINK_RE = re.compile(r"\[[^]]+\]\((?!https?://|#|mailto:)([^)#]+)(?:#[^)]+)?\)")
FORBIDDEN = ("T" + "ODO", "T" + "BD")
EXCLUDED_PARTS = {".git", ".worktrees", ".venv", ".tools", ".pytest_cache"}


def _iter_markdown(root: Path):
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        if relative.parts[:2] == ("docs", "superpowers"):
            continue
        yield path


def validate_repository(root: Path) -> list[str]:
    """返回可定位的知识库错误；空列表表示通过。"""
    errors: list[str] = []
    catalog = load_catalog(root)

    for item in catalog["modules"]:
        folder = root / "docs" / f'{item["id"]}-{item["slug"]}'
        for filename in MODULE_FILES:
            path = folder / filename
            if not path.is_file():
                errors.append(f"缺少必需文件：{path.relative_to(root)}")

    for path in _iter_markdown(root):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"禁止占位符 {token}：{relative}")
        for target in LINK_RE.findall(text):
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"失效链接 {target}：{relative}")

    return sorted(set(errors))
