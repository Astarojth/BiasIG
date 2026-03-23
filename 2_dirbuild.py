import argparse
from pathlib import Path

from benchmark.generate import dir_build
from benchmark.config import arranged_dir


def parse_args():
    parser = argparse.ArgumentParser(description="Arrange generated BiasIG images into prompt-wise folders.")
    parser.add_argument(
        "--model-name",
        default="lcm",
        help="Short name of the text-to-image model being evaluated.",
    )
    parser.add_argument(
        "--source-path",
        required=True,
        help="Directory containing the raw generated images.",
    )
    parser.add_argument(
        "--target-path",
        default=None,
        help="Directory to write arranged images to. Defaults to ./arranged/<model-name>.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    target_path = Path(args.target_path) if args.target_path else arranged_dir(args.model_name)
    target_path.mkdir(parents=True, exist_ok=True)
    dir_build(args.source_path, str(target_path))
