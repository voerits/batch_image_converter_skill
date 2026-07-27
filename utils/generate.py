from __future__ import annotations

import io
from pathlib import Path
from typing import Any

from PIL import Image

from . import toagent

PIL_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
}


def make_prompt(image_path: Path, output_path: Path, img_format: str, user_prompt: str) -> str:
    return toagent.build_conversion_instruction(
        image_path=image_path,
        output_path=output_path,
        user_prompt=user_prompt,
        image_format=img_format,
    )


def build_manifest_entries(
    image_file_list: list[Path],
    source_root: Path,
    save_dir: Path,
    user_prompt: str,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    for img_fp in image_file_list:
        image_path_relative = img_fp.relative_to(source_root)
        save_path = save_dir / image_path_relative
        save_path.parent.mkdir(parents=True, exist_ok=True)
        img_format = img_fp.suffix.lower().lstrip(".")
        entries.append(
            toagent.build_manifest_entry(
                image_path=img_fp,
                output_path=save_path,
                user_prompt=user_prompt,
                image_format=img_format,
            )
        )

    return entries


def save_image(image_data: bytes | io.BytesIO | Image.Image, img_format: str, save_path: Path) -> None:
    save_path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(image_data, Image.Image):
        img = image_data
    elif isinstance(image_data, bytes):
        img = Image.open(io.BytesIO(image_data))
    else:
        image_data.seek(0)
        img = Image.open(image_data)

    normalized_format = img_format.lower().lstrip(".")
    img.save(save_path, format=PIL_FORMATS.get(normalized_format, normalized_format.upper()))
