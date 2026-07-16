from pathlib import Path

from scripts.knowledge_base.catalog import load_catalog
from scripts.knowledge_base.scaffold import MODULE_FILES


ROOT = Path(__file__).resolve().parents[1]


def test_planned_modules_have_specific_scope_and_acceptance() -> None:
    catalog = load_catalog(ROOT)
    for item in catalog["modules"][1:]:
        folder = ROOT / "docs" / f'{item["id"]}-{item["slug"]}'
        for filename in MODULE_FILES:
            text = (folder / filename).read_text(encoding="utf-8")
            assert item["title"] in text
            assert "成熟度：规划中" in text
            assert "前置知识" in text
            assert "内容边界" in text
            assert "验收标准" in text
        readme = (folder / "README.md").read_text(encoding="utf-8")
        assert readme.count(".md)") >= 6


def test_projects_have_product_and_delivery_contracts() -> None:
    catalog = load_catalog(ROOT)
    for item in catalog["projects"]:
        path = ROOT / "projects" / f'{item["id"]}-{item["slug"]}' / "README.md"
        text = path.read_text(encoding="utf-8")
        for heading in (
            "目标用户",
            "核心问题",
            "功能范围",
            "技术栈",
            "前置模块",
            "里程碑",
            "交付物",
            "验收标准",
        ):
            assert f"## {heading}" in text


def test_demo_catalog_covers_every_stable_id() -> None:
    catalog = load_catalog(ROOT)
    text = (ROOT / "examples" / "CATALOG.md").read_text(encoding="utf-8")
    for item in catalog["demos"]:
        assert f'| {item["id"]} |' in text
