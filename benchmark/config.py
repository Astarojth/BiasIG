from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HF_ALIGN_MODEL = "BIGBench/InternVL-4B-bench"
DEFAULT_LOCAL_ALIGN_MODEL = REPO_ROOT / "model" / "InternVL-4B-bench"
DEFAULT_WORKFLOW = REPO_ROOT / "data" / "workflow" / "lcm_sdxl.json"
DEFAULT_DATA_DIR = REPO_ROOT / "data"
DEFAULT_GENERATION_ENDPOINT = "http://127.0.0.1:8190/prompt"


def repo_path(*parts: str) -> Path:
    return REPO_ROOT.joinpath(*parts)


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
    return repo_path("arranged", model_name)


def aligned_dir(model_name: str) -> Path:
    return repo_path("aligned", model_name)


def align_result_file(model_name: str) -> Path:
    return aligned_dir(model_name) / f"align_{model_name}.json"


def result_dir(model_name: str) -> Path:
    return repo_path("result", model_name)
