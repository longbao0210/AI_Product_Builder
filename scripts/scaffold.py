import argparse
from pathlib import Path

from knowledge_base.scaffold import scaffold_repository


def main() -> int:
    parser = argparse.ArgumentParser(description="创建 AI Product Builder 知识库骨架")
    parser.add_argument("--root", default=".", help="仓库根目录，默认为当前目录")
    args = parser.parse_args()

    created = scaffold_repository(Path(args.root).resolve())
    print(f"已创建 {len(created)} 个文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
