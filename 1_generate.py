import argparse

import benchmark
from benchmark.config import DEFAULT_DATA_DIR, DEFAULT_GENERATION_ENDPOINT, DEFAULT_WORKFLOW


def parse_args():
    parser = argparse.ArgumentParser(description="Generate images for the BiasIG prompt suite.")
    parser.add_argument(
        "--workflow",
        default=str(DEFAULT_WORKFLOW),
        help="Path to the ComfyUI workflow JSON file.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of full prompt-set generation iterations to run.",
    )
    parser.add_argument(
        "--data-path",
        default=str(DEFAULT_DATA_DIR),
        help="Path to the repository data directory.",
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_GENERATION_ENDPOINT,
        help="ComfyUI prompt endpoint.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    for _ in range(args.iterations):
        benchmark.generate_image(args.workflow, args.endpoint, args.data_path)
