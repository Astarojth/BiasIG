import argparse
import subprocess
import sys
from pathlib import Path

from benchmark.config import load_config, config_value, REPO_ROOT


def parse_args():
    parser = argparse.ArgumentParser(description="Run BiasIG pipeline stages from a single command.")
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "configs" / "example.yaml"),
        help="Path to a YAML or JSON config file.",
    )
    parser.add_argument(
        "--stage",
        choices=["generate", "arrange", "align", "evaluate", "all"],
        default="all",
        help="Pipeline stage to run.",
    )
    return parser.parse_args()


def script_path(name: str) -> str:
    return str(REPO_ROOT / name)


def run_step(script_name: str, config_path: str):
    command = [sys.executable, script_path(script_name), "--config", config_path]
    print(f"[BiasIG] Running: {' '.join(command)}")
    subprocess.run(command, check=True)


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)

    if args.stage == "generate":
        run_step("1_generate.py", args.config)
    elif args.stage == "arrange":
        run_step("2_dirbuild.py", args.config)
    elif args.stage == "align":
        run_step("3_align.py", args.config)
    elif args.stage == "evaluate":
        run_step("4_evaluate.py", args.config)
    else:
        raw_dir = config_value(config, "paths", "raw_output_dir")
        if not raw_dir:
            raise ValueError(
                "The 'all' stage requires paths.raw_output_dir in the config so arranged images can be built from generated files."
            )
        for step in ["1_generate.py", "2_dirbuild.py", "3_align.py", "4_evaluate.py"]:
            run_step(step, args.config)
