import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def load_manifest(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                entries.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
    return entries


def write_manifest(path: Path, entries: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def border_background_mask(arr: np.ndarray) -> np.ndarray:
    channels_min = arr.min(axis=2)
    channels_max = arr.max(axis=2)
    near_white = (channels_min >= 222) & ((channels_max - channels_min) <= 42)

    height, width = near_white.shape
    background = np.zeros((height, width), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        if near_white[0, x]:
            background[0, x] = True
            queue.append((0, x))
        if near_white[height - 1, x]:
            background[height - 1, x] = True
            queue.append((height - 1, x))

    for y in range(height):
        if near_white[y, 0]:
            background[y, 0] = True
            queue.append((y, 0))
        if near_white[y, width - 1]:
            background[y, width - 1] = True
            queue.append((y, width - 1))

    while queue:
        y, x = queue.popleft()
        for next_y, next_x in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if (
                0 <= next_y < height
                and 0 <= next_x < width
                and near_white[next_y, next_x]
                and not background[next_y, next_x]
            ):
                background[next_y, next_x] = True
                queue.append((next_y, next_x))

    return background


def cartoonify(source: Image.Image) -> Image.Image:
    original = ImageOps.exif_transpose(source).convert("RGB")
    original_arr = np.asarray(original)
    background = border_background_mask(original_arr)

    color = original.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.SMOOTH_MORE)
    color = ImageEnhance.Color(color).enhance(1.85)
    color = ImageEnhance.Contrast(color).enhance(1.18)
    color = ImageEnhance.Brightness(color).enhance(1.04)
    color = ImageOps.posterize(color, 4).filter(ImageFilter.ModeFilter(3))

    edges = original.convert("L").filter(ImageFilter.FIND_EDGES)
    edges = ImageOps.autocontrast(edges).filter(ImageFilter.MaxFilter(3))
    edge_arr = np.asarray(edges)

    object_mask = ~background
    if object_mask.any():
        threshold = int(np.percentile(edge_arr[object_mask], 70))
        threshold = max(36, min(96, threshold))
    else:
        threshold = 48

    expanded_object = Image.fromarray((object_mask.astype(np.uint8) * 255), "L").filter(
        ImageFilter.MaxFilter(5)
    )
    expanded_object_arr = np.asarray(expanded_object) > 0
    line_mask = (edge_arr >= threshold) & expanded_object_arr

    result = np.asarray(color).copy()
    result[background] = (255, 255, 255)
    result[line_mask] = (35, 35, 35)

    return Image.fromarray(result, "RGB")


def convert_entry(entry: dict[str, Any]) -> None:
    source_path = Path(entry["source_path"])
    target_path = Path(entry["target_path"])
    image_format = str(entry.get("image_format", target_path.suffix.lstrip("."))).lower()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source_path) as source:
        converted = cartoonify(source)

    if image_format in {"jpg", "jpeg"}:
        converted.save(target_path, "JPEG", quality=95, subsampling=0, optimize=True)
    elif image_format == "png":
        converted.save(target_path, "PNG", optimize=True)
    else:
        converted.save(target_path)

    if not target_path.exists() or target_path.stat().st_size == 0:
        raise RuntimeError(f"Target was not written: {target_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cartoonify every image in a Codex manifest.")
    parser.add_argument("--manifest", required=True, help="Path to _codex_conversion_manifest.jsonl")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    entries = load_manifest(manifest_path)

    failures = 0
    for index, entry in enumerate(entries, start=1):
        print(f"[{index}/{len(entries)}] {entry['source_path']}")
        try:
            convert_entry(entry)
        except Exception as exc:
            entry["status"] = "failed"
            entry["error"] = str(exc)
            failures += 1
            print(f"  failed: {exc}")
        else:
            entry["status"] = "completed"
            entry.pop("error", None)
            entry.pop("log_path", None)
        write_manifest(manifest_path, entries)

    print(f"Converted {len(entries) - failures} image(s); failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
