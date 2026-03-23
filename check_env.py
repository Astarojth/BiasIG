import argparse
import importlib.util
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

from benchmark.config import REPO_ROOT, config_value, load_config, resolve_align_model


def parse_args():
    parser = argparse.ArgumentParser(description="Check whether the local environment is ready for BiasIG.")
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "configs" / "example.yaml"),
        help="Path to a YAML or JSON config file.",
    )
    return parser.parse_args()


def module_status(name: str) -> str:
    return "ok" if importlib.util.find_spec(name) else "missing"


def check_endpoint(endpoint: str) -> str:
    try:
        request = Request(endpoint, method="HEAD")
        urlopen(request, timeout=2)
        return "reachable"
    except URLError:
        return "unreachable"
    except Exception:
        return "unknown"


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)

    endpoint = config_value(config, "generation", "endpoint", default="http://127.0.0.1:8190/prompt")
    align_model = resolve_align_model(config_value(config, "alignment", "model"))
    raw_output_dir = config_value(config, "paths", "raw_output_dir")
    arranged_dir = config_value(config, "paths", "arranged_dir")
    aligned_dir = config_value(config, "paths", "aligned_dir")
    align_file = config_value(config, "paths", "align_file")
    workflow = config_value(config, "generation", "workflow")
    prompt_root = config_value(config, "generation", "prompt_root")

    print("BiasIG Environment Check")
    print("========================")
    print(f"repo_root: {REPO_ROOT}")
    print(f"python: {os.sys.executable}")
    print(f"config: {args.config}")
    print("")
    print("Dependencies")
    print(f"- transformers: {module_status('transformers')}")
    print(f"- torch: {module_status('torch')}")
    print(f"- torchvision: {module_status('torchvision')}")
    print(f"- scipy: {module_status('scipy')}")
    print(f"- yaml: {module_status('yaml')}")
    print("")
    print("Pipeline Inputs")
    print(f"- generation endpoint: {endpoint} ({check_endpoint(endpoint)})")
    print(f"- workflow: {workflow or '(not set)'} ({'ok' if workflow and Path(workflow).exists() else 'missing'})")
    print(f"- prompt root: {prompt_root or './data/prompt'}")
    print(f"- raw output dir: {raw_output_dir or '(not set)'}")
    print(f"- arranged dir: {arranged_dir or '(not set)'}")
    print(f"- aligned dir: {aligned_dir or '(not set)'}")
    print(f"- align file: {align_file or '(not set)'}")
    if Path(str(align_model)).exists():
        print(f"- alignment model: local path found at {align_model}")
    else:
        print(f"- alignment model: will resolve from {align_model}")
