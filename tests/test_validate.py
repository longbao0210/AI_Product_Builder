import json
from pathlib import Path

from scripts.knowledge_base.scaffold import scaffold_repository
from scripts.knowledge_base.validate import validate_repository


def test_validator_reports_missing_files_and_broken_links(tmp_path: Path) -> None:
    catalog = {
        "modules": [
            {
                "id": "01",
                "slug": "Computer-Fundamentals",
                "title": "计算机基础",
                "status": "建设中",
            }
        ],
        "projects": [],
        "demos": [],
    }
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False), encoding="utf-8"
    )
    scaffold_repository(tmp_path)
    readme = tmp_path / "docs" / "01-Computer-Fundamentals" / "README.md"
    readme.write_text("# 标题\n\n[坏链接](missing.md)\n", encoding="utf-8")
    (tmp_path / "docs" / "01-Computer-Fundamentals" / "FAQ.md").unlink()

    errors = validate_repository(tmp_path)

    assert any("FAQ.md" in error for error in errors)
    assert any("missing.md" in error for error in errors)


def test_validator_rejects_unfinished_markers(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "catalog.json").write_text(
        json.dumps({"modules": [], "projects": [], "demos": []}), encoding="utf-8"
    )
    document = tmp_path / "README.md"
    document.write_text("# 示例\n\nT" + "ODO：补充内容\n", encoding="utf-8")

    errors = validate_repository(tmp_path)

    assert any("禁止占位符" in error and "README.md" in error for error in errors)
