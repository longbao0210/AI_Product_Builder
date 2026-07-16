import json
import locale
import subprocess
import sys
from pathlib import Path

from scripts.knowledge_base.scaffold import MODULE_FILES, scaffold_repository


def test_scaffold_creates_required_files_without_overwrite(tmp_path: Path) -> None:
    catalog = {
        "modules": [
            {
                "id": "01",
                "slug": "Computer-Fundamentals",
                "title": "计算机基础",
                "status": "建设中",
            }
        ],
        "projects": [
            {"id": "01", "slug": "AI-Chat", "title": "AI 对话", "status": "规划中"}
        ],
        "demos": [
            {
                "id": "001",
                "slug": "hello-terminal",
                "title": "终端问候",
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


def test_scaffold_cli_runs_from_repository_root(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    catalog = {"modules": [], "projects": [], "demos": []}
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "catalog.json").write_text(
        json.dumps(catalog), encoding="utf-8"
    )
    result = subprocess.run(
        [sys.executable, "scripts/scaffold.py", "--root", str(tmp_path)],
        cwd=root,
        capture_output=True,
        text=True,
        encoding=locale.getpreferredencoding(False),
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "已创建" in result.stdout
