from __future__ import annotations

from benchmark.config import resolve_align_model


def load_alignment_model(model_path: str | None = None):
    from transformers import AutoTokenizer, AutoModel
    import torch

    resolved_model_path = resolve_align_model(model_path)
    model = AutoModel.from_pretrained(
        resolved_model_path,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    ).eval().cuda()
    tokenizer = AutoTokenizer.from_pretrained(resolved_model_path, trust_remote_code=True)
    return model, tokenizer, resolved_model_path
