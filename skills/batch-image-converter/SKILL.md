---
name: batch-image-converter
description: Convert batches of images according to a shared user style or edit request while preserving the source folder's relative directory structure and filenames. Use when Codex is asked to process a folder of JPG, JPEG, or PNG images, read a generated image-conversion manifest, create converted image outputs, or perform repeated image style transformations such as cartoon-like, brighter, sky/background changes, or other visual edits across many files.
---

# Batch Image Converter

## Overview

Convert each listed source image into a real new image using the user's shared visual instruction. Save every output at the requested target path, preserving the relative folder structure and original filename.

## Workflow

1. Find the batch source.
   - If the user gives a manifest path, read it as JSONL.
   - If the user gives a folder and prompt instead, run the project script to create a manifest before converting images.

2. For each manifest entry:
   - Open `source_path`.
   - Use the available image generation or image editing tool to create a real converted image.
   - Apply `instruction` exactly, treating the user conversion request as applying to this image only.
   - Save the converted image to `target_path`.
   - Create parent directories when needed.
   - Keep the original filename and use `image_format` when the available image tool supports it.
   - Do not stop after creating folders, writing a manifest, or explaining the task.

3. Ignore non-image files. Do not copy unrelated files from the source tree.

4. Report completion with the number of converted images and the output folder.

## Manifest Format

The project script writes `_codex_conversion_manifest.jsonl`. Each line is one JSON object:

```json
{"source_path":"E:\\images\\item.jpg","target_path":"E:\\images_converted\\item.jpg","image_format":"jpg","instruction":"Use $batch-image-converter ...","status":"pending"}
```

Use `source_path`, `target_path`, `image_format`, and `instruction`. `status` is informational.

## Project Script

From the project root, create a manifest with:

```bash
python main.py --images <folder> --prompt <prompt-file> --imgformats JPG PNG JPEG
```

The script creates `<folder>_converted` beside the source folder and writes a manifest there. If the output folder already exists, stop and ask the user whether to remove it, rename it, or choose a different source folder.

## Codex Execution Script

After creating a manifest, run Codex once per pending image:

```bash
python scripts/run_codex_batch.py --manifest <folder>_converted/_codex_conversion_manifest.jsonl
```

Use `--limit N` for a small test batch before running every image. The executor attaches each `source_path` image to `codex exec`, asks Codex to create the target image, writes one log file per image, and updates each manifest entry status to `completed`, `failed`, or `skipped_existing`.

If Codex cannot create image files in the current environment, report that limitation and point to the failed entry's log. Do not silently mark the entry as complete unless `target_path` exists and is non-empty.

## Local Helper Scripts

Optional local wrappers live in `skills/batch-image-converter/local/`.

- Windows PowerShell: `skills/batch-image-converter/local/run_batch_converter.ps1`
- Linux/macOS Bash: `skills/batch-image-converter/local/run_batch_converter.sh`

Both helpers prepare the manifest from a source image folder and prompt file. Pass `-Execute` / `--execute` to run `scripts/run_codex_batch.py`, and use `-Limit N` / `--limit N` for a small test batch before processing every image.
