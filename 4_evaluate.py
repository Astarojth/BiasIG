import argparse

from benchmark.config import align_result_file, config_value, load_config
from benchmark.evaluate import eta
from benchmark.evaluate import explicit
from benchmark.evaluate import implicit


def parse_args():
    parser = argparse.ArgumentParser(description="Compute BiasIG metrics from an alignment result JSON file.")
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
        "--align-path",
        default=None,
        help="Path to the alignment JSON file. Defaults to ./outputs/aligned/<model-name>/align_<model-name>.json.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    model_name = args.model_name or config_value(config, "model_name", default="lcm")
    align_path = args.align_path or config_value(config, "paths", "align_file", default=str(align_result_file(model_name)))
    eta(align_path, model_name)
    print("eta finished")
    explicit(align_path, model_name)
    print("explicit finished")
    implicit(align_path, model_name)
    print("implicit finished")
