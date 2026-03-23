import argparse

from benchmark.config import aligned_dir, arranged_dir, resolve_align_model


def parse_args():
    parser = argparse.ArgumentParser(description="Run BiasIG multimodal alignment on arranged images.")
    parser.add_argument(
        "--model-name",
        default="lcm",
        help="Short name of the text-to-image model being evaluated.",
    )
    parser.add_argument(
        "--image-path",
        default=None,
        help="Directory containing arranged prompt-wise images. Defaults to ./arranged/<model-name>.",
    )
    parser.add_argument(
        "--output-path",
        default=None,
        help="Directory for alignment outputs. Defaults to ./aligned/<model-name>.",
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
    image_path = args.image_path or str(arranged_dir(args.model_name))
    output_path = args.output_path or str(aligned_dir(args.model_name))
    align_model = resolve_align_model(args.align_model)
    process_all_subdirs_multi(image_path, output_path, args.model_name, align_model)
    print("finished")
