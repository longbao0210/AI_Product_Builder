"""AI Product Builder 知识库质量门禁。"""

import re
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from .catalog import load_catalog
from .scaffold import MODULE_FILES


Catalog = dict[str, Any]
Check = Callable[[Path, Catalog], list[str]]

LINK_RE = re.compile(r"\[[^]]+\]\((?!https?://|#|mailto:)([^)#]+)(?:#[^)]+)?\)")
SECRET_RE = re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")
FORBIDDEN = ("T" + "ODO", "T" + "BD")
EXCLUDED_PARTS = {".git", ".worktrees", ".venv", ".tools", ".pytest_cache"}


def _iter_markdown(root: Path) -> Iterator[Path]:
    """遍历纳入发布质量检查的 Markdown 文件。"""
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        if relative.parts[:2] == ("docs", "superpowers"):
            continue
        yield path


def check_structure(root: Path, catalog: Catalog) -> list[str]:
    """检查模块固定文件是否完整。"""
    errors: list[str] = []
    for item in catalog["modules"]:
        folder = root / "docs" / f'{item["id"]}-{item["slug"]}'
        for filename in MODULE_FILES:
            path = folder / filename
            if not path.is_file():
                errors.append(f"缺少必需文件：{path.relative_to(root)}")
    return errors


def check_markdown(root: Path, catalog: Catalog) -> list[str]:
    """检查标题结构、禁用占位符与模块成熟度声明。"""
    errors: list[str] = []
    for path in _iter_markdown(root):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        h1_count = sum(line.startswith("# ") for line in text.splitlines())
        if h1_count != 1:
            errors.append(f"一级标题数量应为 1，实际为 {h1_count}：{relative}")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"禁止占位符 {token}：{relative}")

    for item in catalog["modules"]:
        readme = root / "docs" / f'{item["id"]}-{item["slug"]}' / "README.md"
        if not readme.is_file():
            continue
        expected = f'> 成熟度：{item["status"]}'
        if expected not in readme.read_text(encoding="utf-8"):
            errors.append(
                f"成熟度冲突：{readme.relative_to(root)} 应声明“{expected}”"
            )
    return errors


def check_links(root: Path, catalog: Catalog) -> list[str]:
    """检查仓库内相对链接目标是否存在。"""
    del catalog
    errors: list[str] = []
    for path in _iter_markdown(root):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        for target in LINK_RE.findall(text):
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"失效链接 {target}：{relative}")
    return errors


def check_mermaid_fences(root: Path, catalog: Catalog) -> list[str]:
    """检查 Mermaid 代码围栏是否成对闭合。"""
    del catalog
    errors: list[str] = []
    for path in _iter_markdown(root):
        opening_fence: str | None = None
        opening_line = 0
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.strip()
            if opening_fence is None and stripped in {"```mermaid", "~~~mermaid"}:
                opening_fence = stripped[:3]
                opening_line = line_number
            elif opening_fence is not None and stripped == opening_fence:
                opening_fence = None
        if opening_fence is not None:
            errors.append(
                f"Mermaid 围栏未闭合（始于第 {opening_line} 行）：{path.relative_to(root)}"
            )
    return errors


def check_secrets(root: Path, catalog: Catalog) -> list[str]:
    """检查文档中疑似被提交的 API 密钥。"""
    del catalog
    errors: list[str] = []
    for path in _iter_markdown(root):
        if SECRET_RE.search(path.read_text(encoding="utf-8")):
            errors.append(f"发现疑似密钥：{path.relative_to(root)}")
    return errors


def check_catalog_coverage(root: Path, catalog: Catalog) -> list[str]:
    """检查目录编号格式以及跨集合引用。"""
    del root
    errors: list[str] = []
    module_ids = {item["id"] for item in catalog["modules"]}

    for item in catalog["modules"]:
        if not re.fullmatch(r"\d{2}", item["id"]):
            errors.append(f'模块编号必须为两位数字：{item["id"]}')
    for item in catalog["projects"]:
        if not re.fullmatch(r"\d{2}", item["id"]):
            errors.append(f'项目编号必须为两位数字：{item["id"]}')
    for item in catalog["demos"]:
        if not re.fullmatch(r"\d{3}", item["id"]):
            errors.append(f'Demo 编号必须为三位数字：{item["id"]}')
        if item["module_id"] not in module_ids:
            errors.append(
                f'Demo {item["id"]} 引用了不存在的模块：{item["module_id"]}'
            )
    return errors


CHECKS: tuple[Check, ...] = (
    check_structure,
    check_markdown,
    check_links,
    check_mermaid_fences,
    check_secrets,
    check_catalog_coverage,
)


def validate_repository(root: Path) -> list[str]:
    """返回可定位的知识库错误；空列表表示通过。"""
    catalog = load_catalog(root)
    errors = [error for check in CHECKS for error in check(root, catalog)]
    return sorted(set(errors))
