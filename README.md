# BiasIG: Benchmarking Multi-dimensional Social Biases in Text-to-Image Models

<p align="center">
  <img src="https://img.shields.io/badge/Accepted-IJCNN%202026-0f766e?style=flat-square" alt="Accepted by IJCNN 2026">
  <img src="https://img.shields.io/badge/Task-Text--to--Image%20Bias%20Benchmark-c2410c?style=flat-square" alt="Text-to-Image Bias Benchmark">
  <img src="https://img.shields.io/badge/Scope-47%2C040%20Prompts-1d4ed8?style=flat-square" alt="47040 prompts">
</p>

<p align="center">
  <strong>🧭 A benchmark for auditing social bias in text-to-image models across acquired attributes, protected attributes, manifestation, and visibility.</strong>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-highlights">Highlights</a> •
  <a href="#-benchmark-composition">Composition</a> •
  <a href="#-evaluation-pipeline">Pipeline</a> •
  <a href="#-quick-start">Quick Start</a>
</p>

> BiasIG is built for researchers who want a more structured and diagnosis-oriented view of fairness in text-to-image generation, rather than a single coarse score.

## 🌟 Overview

BiasIG provides a unified benchmark for evaluating multi-dimensional social bias in text-to-image generation. The repository includes:

- A 47,040-prompt benchmark covering occupations, characteristics, and social relations
- Ground-truth statistics and weighting files for quantitative evaluation
- ComfyUI workflow templates for model generation
- An automated alignment pipeline based on a fine-tuned InternVL backbone
- Evaluation code for implicit bias, explicit bias, and manifestation analysis

BiasIG is designed to support both benchmark reproduction and follow-up research on bias diagnosis and mitigation in generative models.

The alignment backbone can be loaded from either:

- a local directory at `./model/InternVL-4B-bench`
- or the public Hugging Face repository `BIGBench/InternVL-4B-bench`

## ✨ Highlights

- **🧩 4D definition system.** Bias is organized along acquired attributes, protected attributes, manifestation, and visibility.
- **📦 Large prompt suite.** The benchmark contains 47,040 prompts spanning implicit and explicit evaluation settings.
- **🤖 Automated evaluation.** A fine-tuned multimodal model is used to align generated images with demographic attributes at scale.
- **📈 Unified metrics.** The repository includes code for implicit bias, explicit bias, and manifestation-factor evaluation.

## 🧮 Benchmark Composition

The current release contains:

- **4,280 implicit prompts**
  - 3,580 occupation prompts
  - 480 characteristic prompts
  - 220 social-relation prompts
- **42,760 explicit prompts**
  - 32,220 occupation prompts
  - 4,320 characteristic prompts
  - 6,220 social-relation prompts

This totals **47,040 prompts**.

| Category | Count |
| --- | ---: |
| Implicit prompts | 4,280 |
| Explicit prompts | 42,760 |
| Total prompts | 47,040 |

<p align="center">
  <img src="assets/figures/prompt_portion.png" alt="Prompt composition in BiasIG" width="78%">
</p>

## 🛠️ Evaluation Pipeline

BiasIG follows a four-stage pipeline:

1. Generate images from the benchmark prompt set with a target text-to-image model.
2. Rearrange generated images into prompt-wise directories.
3. Run multimodal alignment with the fine-tuned InternVL backbone.
4. Compute implicit bias, explicit bias, and manifestation scores.

<p align="center">
  <img src="assets/figures/architecture.png" alt="BiasIG evaluation pipeline" width="92%">
</p>

## 📊 Main Results

BiasIG was used in the paper to evaluate 8 mainstream text-to-image models and 3 debiasing methods.

<p align="center">
  <img src="assets/figures/model_groups_comparison.png" alt="BiasIG benchmark results across model groups" width="92%">
</p>

<p align="center">
  <img src="assets/figures/debiasing.png" alt="BiasIG debiasing comparison" width="70%">
</p>

## 🗂️ Repository Structure

```text
BiasIG/
├── 1_generate.py
├── 2_dirbuild.py
├── 3_align.py
├── 4_evaluate.py
├── assets/
│   └── figures/
├── benchmark/
│   ├── config.py
│   ├── evaluate/
│   ├── generate/
│   └── internViT_pkg/
├── data/
│   ├── prompt/
│   ├── truth/
│   └── workflow/
├── model/
├── result/
├── tools/
├── requirements.txt
└── LICENSE
```

## 🚀 Quick Start

### 1. Environment

```bash
conda create -n biasig python=3.11
conda activate biasig
pip install -r requirements.txt
```

### 2. Prepare the alignment model

BiasIG now supports two alignment model setups:

- **Local model directory:** place the fine-tuned checkpoint at `./model/InternVL-4B-bench`
- **Direct Hugging Face loading:** use `BIGBench/InternVL-4B-bench`

If you want to rely on the local directory layout, see `model/Readme.md`.

### 3. Generate benchmark images

```bash
python 1_generate.py \
  --workflow ./data/workflow/sdxl.json \
  --iterations 1 \
  --endpoint http://127.0.0.1:8190/prompt
```

### 4. Rearrange outputs by prompt

```bash
python 2_dirbuild.py \
  --model-name sdxl \
  --source-path /path/to/raw/generated/images
```

### 5. Align images with demographic labels

```bash
python 3_align.py \
  --model-name sdxl \
  --align-model BIGBench/InternVL-4B-bench
```

If you have already downloaded the fine-tuned model into `./model/InternVL-4B-bench`, you can omit `--align-model` and the script will use the local checkpoint automatically.

### 6. Compute benchmark metrics

```bash
python 4_evaluate.py --model-name sdxl
```

## 📝 Notes

- `data/prompt/` contains the released benchmark prompt files.
- `data/truth/` contains released reference statistics and weighting files.
- `data/workflow/` contains example workflow templates for supported generation setups.
- `tools/` contains helper scripts used to maintain prompt files and benchmark metadata.
- Alignment outputs are written to `./aligned/<model-name>/align_<model-name>.json`.

## ⚖️ License

This project is released under the MIT License.
