import json
from pathlib import Path
from typing import Any


def load_catalog(root: Path) -> dict[str, Any]:
    """读取仓库中的稳定内容清单。"""
    path = root / "config" / "catalog.json"
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)
