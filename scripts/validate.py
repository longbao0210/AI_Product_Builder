import argparse
from pathlib import Path

from knowledge_base.validate import validate_repository


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 AI Product Builder 知识库")
    parser.add_argument("--root", default=".", help="仓库根目录，默认为当前目录")
    args = parser.parse_args()

    errors = validate_repository(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print("知识库校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
