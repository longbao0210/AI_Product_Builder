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


def test_validator_detects_markdown_and_secret_risks(tmp_path: Path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "catalog.json").write_text(
        json.dumps({"modules": [], "projects": [], "demos": []}), encoding="utf-8"
    )
    document = tmp_path / "README.md"
    document.write_text(
        "# 标题一\n\n# 标题二\n\n```mermaid\nflowchart LR\nA --> B\n\n"
        + "sk-proj-"
        + "a" * 32,
        encoding="utf-8",
    )

    errors = validate_repository(tmp_path)

    assert any("一级标题" in error for error in errors)
    assert any("Mermaid 围栏" in error for error in errors)
    assert any("疑似密钥" in error for error in errors)


def test_validator_rejects_invalid_demo_ids_and_status_conflicts(tmp_path: Path) -> None:
    catalog = {
        "modules": [
            {"id": "01", "slug": "Demo", "title": "演示", "status": "已完成"}
        ],
        "projects": [],
        "demos": [
            {
                "id": "1",
                "slug": "bad-id",
                "title": "错误编号",
                "module_id": "01",
                "stack": ["Python"],
                "status": "规划中",
            }
        ],
    }
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False), encoding="utf-8"
    )
    scaffold_repository(tmp_path)
    readme = tmp_path / "docs" / "01-Demo" / "README.md"
    readme.write_text("# 演示\n\n> 成熟度：规划中\n", encoding="utf-8")

    errors = validate_repository(tmp_path)

    assert any("Demo 编号" in error for error in errors)
    assert any("成熟度冲突" in error for error in errors)
