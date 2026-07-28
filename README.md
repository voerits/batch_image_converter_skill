# Batch Image Converter Skill for Codex

Convert a folder of images with one shared visual instruction while preserving the original filenames and directory structure.

This repository provides a Codex skill and helper scripts for preparing and running batch image transformations. Each supported image is processed individually, so the same instruction can be applied across an entire nested folder tree.

### Features

1. Apply one style or editing instruction, or more complex instructions, to a batch of images.

2. Preserve each image's relative path and filename.

3. Ignore non-image files instead of copying them into the output folder.

4. Very easy to set off. A simple sentence in your Codex terminal and everything is done.

### How to use it

Very easy! Prompt in your Codex terminal:

> *Load the skill at ./skills/batch-image-converter as $batch-image-converter. Convert the images in [path-to-image-folder] using the instruction in [path-to-prompt-file].*

And let your Codex run it! (^^) 

P.S., You can also make the prompt a little more complex, eg., by demanding a small-size test before formally running over the whole bunch, such as "*Start with a test batch of 3 images, then process the remaining images after the test outputs have been checked.*"

### Supported image formats

By default, the project processes:

```
.jpg
.jpeg
.png
```

Additional extensions can be supplied to 'main.py' through '--imgformats', although the current image-handling utilities are designed around JPEG and PNG files.

### Requirements

- Python 3.9 or later

- Pillow

- The Codex CLI, installed and authenticated

- A Codex environment capable of editing or generating image files and writing them to the workspace

Install the Python dependency:

```python -m pip install Pillow```

### Quick start

Clone the repository:

```
git clone https://github.com/voerits/batch_image_converter_skill.git
cd batch_image_converter_skill
```

Prepare:

- A folder containing the source images.

- A UTF-8 text file containing the conversion instruction.

Then ask Codex to run the skill from the repository root. Remember to provide your image folder path and prompt text file path.

For command-line examples, manual execution, reruns, manifest details, and troubleshooting, see **usage.md**.

### What it does

Given a folder containing images, it generates new images which have converted the original images' style as to user's illustrations. This conversion has the features below:

1. The output images are organized in a new folder, which preserves the same directory structure as the original image folder. The names of the sub-directories and image files are also preserved. However, the files other than image files are ignored and are not included in the output folder.

eg. 

original folder:

    image_folder/
        |____subfolder_1/
            |____subsubfolder_1/
                |____image1.png
                |____image2.jpg
                |____image3.jpeg              
            |____text1.txt
            |____image4.jpg
            |____subsubfolder_2/
                |____video.mp4
                |____image5.jpg
        |____subfolder_2/
            |____subsubfolder_3/
                |____subsubfolder_1/
                    |____image6.png
            |____image7.jpg

new folder:

    image_folder_converted/
        |____subfolder_1/
            |____subsubfolder_1/
                |____image1.png
                |____image2.jpg
                |____image3.jpeg
            |____image4.jpg
            |____subsubfolder_2/
                |____image5.jpg
        |____subfolder_2/
            |____subsubfolder_3/
                |____subsubfolder_1/
                    |____image6.png
            |____image7.jpg

2. The conversion is conducted by AI agent per image file. The requirement for the conversion is provided by user. 

eg.:

    Convert the provided image into a simple cartoon illustration.

    Requirements:
    1. Keep only the main object from the original image. Remove all other objects, clutter, shadows, textures, props, labels, backgrounds, and unnecessary details.
    2. Draw the main object with clean, simplified black outlines.
    3. Use bright, simple colors that make the object easy for a child to recognize and distinguish.
    4. Preserve the object’s basic shape, orientation, and key identifying features from the original image.
    5. Place the cartoon object centered on a plain white background.
    6. Do not add any text, decorations, extra objects, or scenery.
    7. Has a size of 1280 x 1280 pixels.


### Notes

AI image transformations may vary between files even when they use the same instruction. Review a small test batch first, then refine the prompt or rerun individual images when needed.

### Project structure
    .
    ├── main.py
    ├── scripts/
    │   └── run_codex_batch.py
    ├── skills/
    │   └── batch-image-converter/
    │       ├── SKILL.md
    │       ├── agents/
    │       └── local/
    │           ├── run_batch_converter.ps1
    │           └── run_batch_converter.sh
    └── utils/
        └── retrieve.py
        └── toagent.py
        └── generate.py

### License

This project is licensed under the MIT License.