from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HF_ALIGN_MODEL = "BIGBench/InternVL-4B-bench"
DEFAULT_LOCAL_ALIGN_MODEL = REPO_ROOT / "model" / "InternVL-4B-bench"
DEFAULT_WORKFLOW = REPO_ROOT / "data" / "workflow" / "lcm_sdxl.json"
DEFAULT_DATA_DIR = REPO_ROOT / "data"
DEFAULT_GENERATION_ENDPOINT = "http://127.0.0.1:8190/prompt"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "outputs"


def repo_path(*parts: str) -> Path:
    return REPO_ROOT.joinpath(*parts)


def output_root() -> Path:
    return Path(os.getenv("BIASIG_OUTPUT_ROOT", str(DEFAULT_OUTPUT_ROOT)))


def raw_dir(model_name: str) -> Path:
    return output_root() / "raw" / model_name


def resolve_align_model(model_path: str | None = None) -> str:
    if model_path:
        return model_path

    env_model = os.getenv("BIASIG_ALIGN_MODEL")
    if env_model:
        return env_model

    if DEFAULT_LOCAL_ALIGN_MODEL.exists():
        return str(DEFAULT_LOCAL_ALIGN_MODEL)

    return DEFAULT_HF_ALIGN_MODEL


def arranged_dir(model_name: str) -> Path:
    return output_root() / "arranged" / model_name


def aligned_dir(model_name: str) -> Path:
    return output_root() / "aligned" / model_name


def align_result_file(model_name: str) -> Path:
    return aligned_dir(model_name) / f"align_{model_name}.json"


def result_dir(model_name: str) -> Path:
    return output_root() / "results" / model_name


def load_config(config_path: str | None) -> dict[str, Any]:
    if not config_path:
        return {}

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        if path.suffix.lower() == ".json":
            return json.load(file)
        try:
            import yaml
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "PyYAML is required to load YAML config files. Install it or use a JSON config."
            ) from exc
        return yaml.safe_load(file) or {}


def config_value(config: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = config
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current
