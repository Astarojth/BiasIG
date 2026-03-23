This directory is reserved for the fine-tuned InternVL checkpoint used by the alignment pipeline.

Recommended local layout:

```text
model/
└── InternVL-4B-bench/
```

You can either:

- download the fine-tuned model here and let `3_align.py` discover it automatically
- or pass the Hugging Face repo ID directly with `--align-model BIGBench/InternVL-4B-bench`

The repository does not store model weights directly.
