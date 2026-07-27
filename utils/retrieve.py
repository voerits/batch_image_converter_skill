import io
from collections.abc import Iterable
from pathlib import Path

import PIL.Image as Image

PIL_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
}


def retrieve_file_lists(oripath: Path, formats: Iterable[str]) -> list[Path]:
    if not oripath.exists():
        raise FileNotFoundError(f"Image folder does not exist: {oripath}")
    if not oripath.is_dir():
        raise NotADirectoryError(f"Image path is not a folder: {oripath}")

    normalized_formats = {fmt.lower().lstrip(".") for fmt in formats}
    file_list: list[Path] = []

    for p in sorted(oripath.rglob("*")):
        if p.is_file() and p.suffix.lower().lstrip(".") in normalized_formats:
            file_list.append(p)

    return file_list


def retrieve_image(filepath: Path) -> io.BytesIO:
    img = Image.open(str(filepath))
    fm = filepath.suffix.lower().lstrip(".")

    iobytes = io.BytesIO()
    img.save(iobytes, format=PIL_FORMATS.get(fm, fm.upper()))
    iobytes.seek(0)

    return iobytes


def make_new_folder(oripath: Path) -> Path:
    parent_dir = oripath.parent
    folder_name = oripath.name
    new_folder_name = folder_name + "_converted"
    new_folder = parent_dir / new_folder_name

    try:
        new_folder.mkdir()
    except FileExistsError as exc:
        raise FileExistsError(f"Converted output folder already exists: {new_folder}") from exc

    return new_folder
