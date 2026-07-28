# Usage Guide

This guide covers setup, command-line execution, manual workflows, reruns, output files, and troubleshooting for the Batch Image Converter for Codex.

## Requirements

- Python 3.9 or later
- [Pillow](https://pypi.org/project/pillow/)
- The Codex CLI, installed and authenticated
- A Codex environment capable of editing or generating image files and writing them to the workspace

Install Pillow:

```bash
python -m pip install Pillow
```

## Prepare the inputs

You need:

1. A folder containing the source images.
2. A UTF-8 text file containing the instruction to apply to every image.

For example:

```text
my_images/
prompt.txt
```

By default, the project processes `.jpg`, `.jpeg`, and `.png` files.

## Recommended workflow

Run a small test batch first. Review the results, adjust the instruction if necessary, and then process the remaining images.

### Linux or macOS

Test three images:

```bash
./skills/batch-image-converter/local/run_batch_converter.sh \
  --images /path/to/my_images \
  --prompt /path/to/prompt.txt \
  --execute \
  --limit 3
```

Process the remaining images:

```bash
./skills/batch-image-converter/local/run_batch_converter.sh \
  --images /path/to/my_images \
  --prompt /path/to/prompt.txt \
  --execute
```

### Windows PowerShell

Test three images:

```powershell
.\skills\batch-image-converter\local\run_batch_converter.ps1 `
  -ImagesPath "C:\path\to\my_images" `
  -PromptPath "C:\path\to\prompt.txt" `
  -Execute `
  -Limit 3
```

Process the remaining images:

```powershell
.\skills\batch-image-converter\local\run_batch_converter.ps1 `
  -ImagesPath "C:\path\to\my_images" `
  -PromptPath "C:\path\to\prompt.txt" `
  -Execute
```

## Run through a Codex prompt

From the repository root, you can ask Codex to run the workflow for you:

```text
Load the skill at ./skills/batch-image-converter as $batch-image-converter.
Convert the images in <path-to-image-folder> using the instruction in
<path-to-prompt-file>. Start with a test batch of 3 images, then process the
remaining images after the test outputs have been checked.
```

## Manual two-step workflow

The helper scripts combine two operations: creating a conversion manifest and executing its pending entries. You can run those operations separately when you need more control.

### Step 1: Build the conversion manifest

```bash
python main.py \
  --images /path/to/my_images \
  --prompt /path/to/prompt.txt \
  --imgformats JPG PNG JPEG
```

This creates a sibling output folder:

```text
my_images_converted/
```

It also creates the manifest:

```text
my_images_converted/_codex_conversion_manifest.jsonl
```

### Step 2: Process the manifest

Run a test batch of three pending entries:

```bash
python scripts/run_codex_batch.py \
  --manifest /path/to/my_images_converted/_codex_conversion_manifest.jsonl \
  --limit 3
```

Then process the remaining pending entries:

```bash
python scripts/run_codex_batch.py \
  --manifest /path/to/my_images_converted/_codex_conversion_manifest.jsonl
```

The executor calls `codex exec` once for each pending image, provides the source image and conversion instruction, and checks that a non-empty target file was created.

## Output structure

The output folder preserves the source image hierarchy and filenames. Non-image files are ignored.

```text
Source:
image_folder/
├── subfolder_1/
│   ├── subfolder_1a/
│   │   ├── image1.png
│   │   ├── image2.jpg
│   │   └── image3.jpeg
│   ├── notes.txt
│   └── image4.jpg
└── subfolder_2/
    ├── video.mp4
    └── image5.jpg

Output:
image_folder_converted/
├── subfolder_1/
│   ├── subfolder_1a/
│   │   ├── image1.png
│   │   ├── image2.jpg
│   │   └── image3.jpeg
│   └── image4.jpg
├── subfolder_2/
│   └── image5.jpg
└── _codex_conversion_manifest.jsonl
```

The output folder may also contain one log file for each attempted conversion:

```text
_codex_conversion_0001.log
_codex_conversion_0002.log
```

## Writing the conversion instruction

Clear and specific instructions generally produce more consistent results than broad requests.

Example `prompt.txt`:

```text
Convert the provided image into a simple cartoon illustration.

Requirements:
1. Keep only the main object from the original image.
2. Remove clutter, shadows, textures, props, labels, and the original background.
3. Draw the main object with clean, simplified black outlines.
4. Use bright, simple colors that make the object easy for a child to recognize.
5. Preserve the object's basic shape, orientation, and identifying features.
6. Center the object on a plain white background.
7. Do not add text, decorations, extra objects, or scenery.
8. Produce a 1280 × 1280 image.
```

Useful details to specify include:

- The intended visual style
- Objects to keep or remove
- Background requirements
- Colors and line treatment
- Text or decoration restrictions
- Output dimensions

## Manifest format

The manifest is a JSONL file containing one JSON object per image.

```json
{"source_path":"/images/item.jpg","target_path":"/images_converted/item.jpg","image_format":"jpg","instruction":"Use $batch-image-converter ...","status":"pending"}
```

Important fields include:

- `source_path`: path to the original image
- `target_path`: required output path
- `image_format`: expected output format
- `instruction`: full per-image conversion request
- `status`: `pending`, `completed`, `failed`, or `skipped_existing`
- `log_path`: log file for an attempted conversion, when available

## Rerunning images

Existing target images are skipped by default.

Use `--force` to rerun entries even when their output files already exist.

### Linux or macOS

```bash
./skills/batch-image-converter/local/run_batch_converter.sh \
  --images /path/to/my_images \
  --prompt /path/to/prompt.txt \
  --execute \
  --force
```

### Windows PowerShell

```powershell
.\skills\batch-image-converter\local\run_batch_converter.ps1 `
  -ImagesPath "C:\path\to\my_images" `
  -PromptPath "C:\path\to\prompt.txt" `
  -Execute `
  -Force
```

For a completely fresh run, remove or rename the existing `<image-folder>_converted` directory before rebuilding the manifest.

## Additional image formats

You can pass additional file extensions to `main.py` through `--imgformats`:

```bash
python main.py \
  --images /path/to/my_images \
  --prompt /path/to/prompt.txt \
  --imgformats JPG PNG JPEG WEBP
```

The current image-handling utilities are primarily designed around JPEG and PNG files, so test other formats before running a large batch.

## Troubleshooting

### The converted output folder already exists

`main.py` does not overwrite an existing output folder. Remove or rename that folder, or continue using its existing manifest.

### No images were found

Check that:

- The source path points to a directory.
- The image extensions are supported.
- Values passed to `--imgformats` match the file extensions.

### A conversion failed

The manifest entry is marked as `failed`. Check its `log_path` and review the corresponding Codex CLI output.

### Codex completed but no image was produced

An entry is marked as completed only when the target file exists and is non-empty. If the Codex environment cannot create image files, the entry remains failed and the attempt is recorded in its log.

### Results are inconsistent

AI-generated transformations can vary between images. Try the following:

- Make the instruction more specific.
- Run a small test batch before the full conversion.
- Rerun only unsatisfactory images.
- Add explicit requirements for composition, background, dimensions, and excluded elements.

## Processing considerations

The executor starts one Codex process per image. Processing time and usage therefore increase with the number of images in the manifest.

> This *usage.md* is generated by GPT-5.6 Sol