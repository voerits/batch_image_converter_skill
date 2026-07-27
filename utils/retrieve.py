import io
import sys
from pathlib import Path

import PIL.Image as Image
import numpy as np

def retrieve_file_lists(oripath: Path, formats: np.ndarray[str]) -> list[Path]:
    rglobs = oripath.rglob('*')
    file_list = []

    for p in list(rglobs):
        p_str = str(p)
        fm = p_str.strip().split('.')[-1]
        if fm in formats:
            file_list.append(p)

    return file_list

def retrieve_image(filepath: Path) -> io.BytesIO:
    img = Image.open(str(filepath))
    fm = filepath.name.strip().split('.')[-1]

    iobytes = io.BytesIO()
    img.save(iobytes, format = fm.upper())

    return iobytes

def make_new_folder(oripath: Path) -> Path:
    parent_dir = oripath.parent
    folder_name = oripath.name
    new_folder_name = folder_name + '_converted'

    Path.mkdir(parent_dir / new_folder_name)

    return parent_dir / new_folder_name
