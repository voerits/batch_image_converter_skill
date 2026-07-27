import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

DEFAULT_MANIFEST_NAME = "_codex_conversion_manifest.jsonl"


def build_conversion_instruction(
    image_path: Path,
    output_path: Path,
    user_prompt: str,
    image_format: str,
) -> str:
    source = Path(image_path).resolve()
    target = Path(output_path).resolve()
    normalized_format = image_format.lower().lstrip(".")
    cleaned_prompt = user_prompt.strip()

    return (
        f'Use $batch-image-converter to convert the source image "{source}" and '
        f'save the converted result at "{target}". Apply this conversion request: '
        f"{cleaned_prompt} Output requirements: preserve the main subject and "
        f"composition, save as {normalized_format.upper()} when supported, keep "
        "the target file name unchanged, and create parent directories if needed."
    )


def build_manifest_entry(
    image_path: Path,
    output_path: Path,
    user_prompt: str,
    image_format: str,
) -> dict[str, Any]:
    return {
        "source_path": str(Path(image_path).resolve()),
        "target_path": str(Path(output_path).resolve()),
        "image_format": image_format.lower().lstrip("."),
        "instruction": build_conversion_instruction(
            image_path=image_path,
            output_path=output_path,
            user_prompt=user_prompt,
            image_format=image_format,
        ),
        "status": "pending",
    }


def write_conversion_manifest(
    entries: Iterable[Mapping[str, Any]],
    manifest_path: Path,
) -> Path:
    output_path = Path(manifest_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as manifest_file:
        for entry in entries:
            manifest_file.write(json.dumps(dict(entry), ensure_ascii=False) + "\n")

    return output_path


def convert_by_agent(
    entries: Iterable[Mapping[str, Any]],
    manifest_path: Path,
) -> Path:
    return write_conversion_manifest(entries, manifest_path)
