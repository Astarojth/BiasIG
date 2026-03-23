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
  <a href="#-extensibility">Extensibility</a> •
  <a href="#-automation">Automation</a> •
  <a href="#-demo">Demo</a> •
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
- **🔧 Extensible by design.** Prompt files, truth statistics, workflow templates, and evaluator configuration can all be updated for future benchmark extensions.
- **⚙️ Config-driven workflow.** The main pipeline now supports YAML/JSON configuration, environment checks, and a single-command runner.

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

## 🔧 Extensibility

BiasIG is intended to be maintainable and extensible rather than frozen as a one-off release.

You can extend or update the benchmark in several ways:

- **Prompt updates.** Add or revise benchmark prompts under `data/prompt/`.
- **Ground-truth updates.** Update released statistics and weighting files under `data/truth/`.
- **Workflow updates.** Add new generation backbones or workflow templates under `data/workflow/`.
- **Evaluator updates.** Swap the alignment model with `--align-model` or the `BIASIG_ALIGN_MODEL` environment variable.
- **Benchmark maintenance tools.** Use the helper scripts in `tools/` when you need to regenerate or maintain prompt- and weight-related assets.

This also means the repository supports future additions such as new demographic axes, new prompt families, new model workflows, and updated evaluation backbones.

## ⚙️ Automation

BiasIG now supports a more automated workflow on top of the individual 1-4 scripts.

- `configs/example.yaml` provides a standard end-to-end configuration.
- `check_env.py` validates dependencies, endpoint reachability, and alignment-model resolution.
- `run_pipeline.py` can run `generate`, `arrange`, `align`, `evaluate`, or `all`.
- Standardized outputs are written under `./outputs/`.

Recommended layout:

```text
outputs/
├── raw/<model_name>/
├── arranged/<model_name>/
├── aligned/<model_name>/
└── results/<model_name>/
```

## 🧪 Demo

A minimal demo prompt subset is included under `demo/prompt/` together with `configs/demo.yaml`.

This demo is useful for:

- smoke-testing the pipeline
- validating your environment before a full benchmark run
- checking that your generation, alignment, and evaluation paths are wired correctly

## 🗂️ Repository Structure

```text
BiasIG/
├── 1_generate.py
├── 2_dirbuild.py
├── 3_align.py
├── 4_evaluate.py
├── assets/
│   └── figures/
├── check_env.py
├── configs/
│   ├── demo.yaml
│   └── example.yaml
├── benchmark/
│   ├── config.py
│   ├── evaluate/
│   ├── generate/
│   └── internViT_pkg/
├── data/
│   ├── prompt/
│   ├── truth/
│   └── workflow/
├── demo/
│   └── prompt/
├── model/
├── run_pipeline.py
├── tools/
├── requirements.txt
└── LICENSE
```

## 🚀 Quick Start

### Recommended Path

If you want the shortest route to a successful run, use this sequence:

1. Prepare `configs/example.yaml`
2. Run `python check_env.py --config ./configs/example.yaml`
3. Make sure your ComfyUI workflow writes generated images into `paths.raw_output_dir`
4. Run `python run_pipeline.py --config ./configs/example.yaml --stage all`

### 1. Environment

```bash
conda create -n biasig python=3.11
conda activate biasig
pip install -r requirements.txt
```

### 2. Run an environment check

```bash
python check_env.py --config ./configs/example.yaml
```

### 3. Prepare the alignment model

BiasIG now supports two alignment model setups:

- **Local model directory:** place the fine-tuned checkpoint at `./model/InternVL-4B-bench`
- **Direct Hugging Face loading:** use `BIGBench/InternVL-4B-bench`

If you want to rely on the local directory layout, see `model/Readme.md`.

### 4. Generate benchmark images

```bash
python 1_generate.py \
  --config ./configs/example.yaml
```

### 5. Rearrange outputs by prompt

```bash
python 2_dirbuild.py \
  --config ./configs/example.yaml
```

### 6. Align images with demographic labels

```bash
python 3_align.py \
  --config ./configs/example.yaml
```

If you have already downloaded the fine-tuned model into `./model/InternVL-4B-bench`, you can omit `--align-model` and the script will use the local checkpoint automatically.

### 7. Compute benchmark metrics

```bash
python 4_evaluate.py --config ./configs/example.yaml
```

### 8. Run the full pipeline from one command

```bash
python run_pipeline.py --config ./configs/example.yaml --stage all
```

`--stage all` expects your generation workflow to write raw images into the `paths.raw_output_dir` configured in the file. This is the key link between ComfyUI generation and the later arrange/align/evaluate stages.

### 9. Try the minimal demo

```bash
python check_env.py --config ./configs/demo.yaml
python run_pipeline.py --config ./configs/demo.yaml --stage generate
```

### Advanced Usage

If you prefer to run stages separately, all four main scripts still support direct CLI usage as well as `--config`-driven execution.

## 📝 Notes

- `data/prompt/` contains the released benchmark prompt files.
- `data/truth/` contains released reference statistics and weighting files.
- `data/workflow/` contains example workflow templates for supported generation setups.
- `configs/` contains reusable pipeline configurations.
- `demo/prompt/` contains a small prompt subset for fast smoke tests.
- `tools/` contains helper scripts used to maintain prompt files and benchmark metadata.
- Alignment outputs are written to `./outputs/aligned/<model-name>/align_<model-name>.json`.
- Evaluation outputs are written to `./outputs/results/<model-name>/`.
- `run_pipeline.py` now performs stage-level dependency checks and will fail early if expected inputs are missing.

## ⚖️ License

This project is released under the MIT License.
