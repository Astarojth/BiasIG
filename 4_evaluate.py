import argparse

from benchmark.config import align_result_file
from benchmark.evaluate import eta
from benchmark.evaluate import explicit
from benchmark.evaluate import implicit


def parse_args():
    parser = argparse.ArgumentParser(description="Compute BiasIG metrics from an alignment result JSON file.")
    parser.add_argument(
        "--model-name",
        default="lcm",
        help="Short name of the text-to-image model being evaluated.",
    )
    parser.add_argument(
        "--align-path",
        default=None,
        help="Path to the alignment JSON file. Defaults to ./aligned/<model-name>/align_<model-name>.json.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    align_path = args.align_path or str(align_result_file(args.model_name))
    eta(align_path, args.model_name)
    print("eta finished")
    explicit(align_path, args.model_name)
    print("explicit finished")
    implicit(align_path, args.model_name)
    print("implicit finished")
