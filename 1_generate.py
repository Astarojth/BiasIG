import argparse

import benchmark
from benchmark.config import (
    DEFAULT_DATA_DIR,
    DEFAULT_GENERATION_ENDPOINT,
    DEFAULT_WORKFLOW,
    config_value,
    load_config,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate images for the BiasIG prompt suite.")
    parser.add_argument(
        "--config",
        default=None,
        help="Optional YAML or JSON config file.",
    )
    parser.add_argument(
        "--workflow",
        default=None,
        help="Path to the ComfyUI workflow JSON file.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=None,
        help="Number of full prompt-set generation iterations to run.",
    )
    parser.add_argument(
        "--data-path",
        default=None,
        help="Path to the repository data directory.",
    )
    parser.add_argument(
        "--prompt-root",
        default=None,
        help="Optional root directory containing prompt subfolders. Overrides --data-path/prompt.",
    )
    parser.add_argument(
        "--endpoint",
        default=None,
        help="ComfyUI prompt endpoint.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    workflow = args.workflow or config_value(config, "generation", "workflow", default=str(DEFAULT_WORKFLOW))
    iterations = args.iterations or config_value(config, "generation", "iterations", default=1)
    data_path = args.data_path or config_value(config, "generation", "data_path", default=str(DEFAULT_DATA_DIR))
    prompt_root = args.prompt_root or config_value(config, "generation", "prompt_root")
    endpoint = args.endpoint or config_value(config, "generation", "endpoint", default=DEFAULT_GENERATION_ENDPOINT)

    for _ in range(iterations):
        benchmark.generate_image(workflow, endpoint, data_path=data_path, prompt_path=prompt_root)
