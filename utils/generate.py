import io
import sys
from pathlib import Path

from PIL import Image

import toagent

def make_prompt(img_io: io.BytesIO, img_format: str, user_prompt: str) -> str:
    img_bytes = img_io.getvalue()

    prompt = "Convert an image file according to the illustrative demands: " + user_prompt + \
    "\n Image file is in binary format: " + img_bytes + "\n its original format is " + img_format + \
    "\n Return this image also in io.BytesIO loadable binary format, whose decode is also for " + img_format + " format." 

    return prompt

def save_image(img_bytes: bytes, img_format: str, save_path: Path):
    img_io = io.BytesIO(img_bytes)
    img = Image.open(img_io)

    img.save(save_path, format=img_format.upper())