from pathlib import Path

from scripts.knowledge_base.catalog import load_catalog


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_has_stable_counts_and_unique_ids() -> None:
    catalog = load_catalog(ROOT)
    modules = catalog["modules"]
    projects = catalog["projects"]
    demos = catalog["demos"]

    assert len(modules) == 40
    assert len(projects) == 25
    assert len(demos) >= 200
    assert len({item["id"] for item in modules}) == 40
    assert len({item["id"] for item in projects}) == 25
    assert len({item["id"] for item in demos}) == len(demos)
    assert modules[0]["slug"] == "Computer-Fundamentals"
    assert projects[-1]["slug"] == "AI-SaaS"
