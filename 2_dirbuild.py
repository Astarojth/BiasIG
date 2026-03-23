import argparse
from pathlib import Path

from benchmark.generate import dir_build
from benchmark.config import arranged_dir, config_value, load_config


def parse_args():
    parser = argparse.ArgumentParser(description="Arrange generated BiasIG images into prompt-wise folders.")
    parser.add_argument(
        "--config",
        default=None,
        help="Optional YAML or JSON config file.",
    )
    parser.add_argument(
        "--model-name",
        default=None,
        help="Short name of the text-to-image model being evaluated.",
    )
    parser.add_argument(
        "--source-path",
        default=None,
        help="Directory containing the raw generated images.",
    )
    parser.add_argument(
        "--target-path",
        default=None,
        help="Directory to write arranged images to. Defaults to ./outputs/arranged/<model-name>.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    model_name = args.model_name or config_value(config, "model_name", default="lcm")
    source_path = args.source_path or config_value(config, "paths", "raw_output_dir")
    if not source_path:
        raise ValueError("A raw image source path is required. Provide --source-path or set paths.raw_output_dir in the config.")
    target_path = Path(
        args.target_path
        or config_value(config, "paths", "arranged_dir", default=str(arranged_dir(model_name)))
    )
    target_path.mkdir(parents=True, exist_ok=True)
    dir_build(source_path, str(target_path))
