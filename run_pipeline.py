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


def require_path(path_value: str | None, message: str) -> Path:
    if not path_value:
        raise ValueError(message)
    return Path(path_value)


def require_existing_dir(path_value: str | None, message: str) -> Path:
    path = require_path(path_value, message)
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"{message} Current value: {path}")
    return path


def require_existing_file(path_value: str | None, message: str) -> Path:
    path = require_path(path_value, message)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"{message} Current value: {path}")
    return path


def validate_stage_inputs(config: dict, stage: str):
    raw_dir = config_value(config, "paths", "raw_output_dir")
    arranged = config_value(config, "paths", "arranged_dir")
    aligned = config_value(config, "paths", "aligned_dir")
    align_file = config_value(config, "paths", "align_file")

    if stage == "generate":
        require_path(
            raw_dir,
            "Config must define paths.raw_output_dir so generated images have a known target location.",
        )
    elif stage == "arrange":
        require_existing_dir(
            raw_dir,
            "Arrange stage requires paths.raw_output_dir to exist and contain generated images.",
        )
    elif stage == "align":
        require_existing_dir(
            arranged,
            "Align stage requires paths.arranged_dir to exist. Run arrange first or update the config.",
        )
    elif stage == "evaluate":
        require_existing_file(
            align_file,
            "Evaluate stage requires paths.align_file to exist. Run align first or update the config.",
        )


def print_stage_summary(config: dict):
    print("[BiasIG] Pipeline Summary")
    print(f"  model_name      : {config_value(config, 'model_name', default='(unset)')}")
    print(f"  workflow        : {config_value(config, 'generation', 'workflow', default='(unset)')}")
    print(f"  prompt_root     : {config_value(config, 'generation', 'prompt_root', default='./data/prompt')}")
    print(f"  raw_output_dir  : {config_value(config, 'paths', 'raw_output_dir', default='(unset)')}")
    print(f"  arranged_dir    : {config_value(config, 'paths', 'arranged_dir', default='(unset)')}")
    print(f"  aligned_dir     : {config_value(config, 'paths', 'aligned_dir', default='(unset)')}")
    print(f"  align_file      : {config_value(config, 'paths', 'align_file', default='(unset)')}")
    print("")


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    print_stage_summary(config)

    if args.stage == "generate":
        validate_stage_inputs(config, "generate")
        run_step("1_generate.py", args.config)
    elif args.stage == "arrange":
        validate_stage_inputs(config, "arrange")
        run_step("2_dirbuild.py", args.config)
    elif args.stage == "align":
        validate_stage_inputs(config, "align")
        run_step("3_align.py", args.config)
    elif args.stage == "evaluate":
        validate_stage_inputs(config, "evaluate")
        run_step("4_evaluate.py", args.config)
    else:
        validate_stage_inputs(config, "generate")
        run_step("1_generate.py", args.config)
        validate_stage_inputs(config, "arrange")
        run_step("2_dirbuild.py", args.config)
        validate_stage_inputs(config, "align")
        run_step("3_align.py", args.config)
        validate_stage_inputs(config, "evaluate")
        run_step("4_evaluate.py", args.config)
