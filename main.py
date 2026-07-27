import argparse
from pathlib import Path

import utils.generate as generate
import utils.retrieve as retrieve
import utils.toagent as toagent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Codex conversion manifest for a folder of images."
    )

    parser.add_argument("--images", type=str, default="./assets/images")
    parser.add_argument("--prompt", type=str, default="./assets/prompt.txt")
    parser.add_argument("--imgformats", nargs="+", type=str, default=["JPG", "PNG", "JPEG"])

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    path_img = Path(args.images).expanduser().resolve()
    prompt_file = Path(args.prompt).expanduser().resolve()
    img_formats = [x.lower().lstrip(".") for x in args.imgformats]

    image_file_list = retrieve.retrieve_file_lists(path_img, img_formats)

    prompt = prompt_file.read_text(encoding="utf-8").strip()

    print(f"User prompt: {prompt}")

    try:
        save_dir = retrieve.make_new_folder(path_img)
    except FileExistsError as exc:
        raise SystemExit(f"Error: {exc}") from exc
    entries = generate.build_manifest_entries(image_file_list, path_img, save_dir, prompt)
    manifest_path = save_dir / toagent.DEFAULT_MANIFEST_NAME
    toagent.convert_by_agent(entries, manifest_path)

    print(f"Found {len(entries)} image(s).")
    print(f"Created converted output folder: {save_dir}")
    print(f"Wrote Codex conversion manifest: {manifest_path}")
    print(f"Next step: ask Codex to use $batch-image-converter with {manifest_path}")


if __name__ == "__main__":
    main()

