import argparse

from benchmark.config import aligned_dir, arranged_dir, resolve_align_model, config_value, load_config


def parse_args():
    parser = argparse.ArgumentParser(description="Run BiasIG multimodal alignment on arranged images.")
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
        "--image-path",
        default=None,
        help="Directory containing arranged prompt-wise images. Defaults to ./outputs/arranged/<model-name>.",
    )
    parser.add_argument(
        "--output-path",
        default=None,
        help="Directory for alignment outputs. Defaults to ./outputs/aligned/<model-name>.",
    )
    parser.add_argument(
        "--align-model",
        default=None,
        help="Local path or Hugging Face repo ID of the fine-tuned InternVL alignment model.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    from benchmark.internViT_pkg import process_all_subdirs_multi

    args = parse_args()
    config = load_config(args.config)
    model_name = args.model_name or config_value(config, "model_name", default="lcm")
    image_path = args.image_path or config_value(config, "paths", "arranged_dir", default=str(arranged_dir(model_name)))
    output_path = args.output_path or config_value(config, "paths", "aligned_dir", default=str(aligned_dir(model_name)))
    align_model = resolve_align_model(args.align_model or config_value(config, "alignment", "model"))
    process_all_subdirs_multi(image_path, output_path, model_name, align_model)
    print("finished")
