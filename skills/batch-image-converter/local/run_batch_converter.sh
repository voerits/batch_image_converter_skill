#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "$script_dir/../../.." && pwd)"

images_path="assets/image_objects"
prompt_path="assets/prompt.txt"
execute=false
limit=0
force=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --images)
            images_path="$2"
            shift 2
            ;;
        --prompt)
            prompt_path="$2"
            shift 2
            ;;
        --execute)
            execute=true
            shift
            ;;
        --limit)
            limit="$2"
            shift 2
            ;;
        --force)
            force=true
            shift
            ;;
        -h|--help)
            cat <<'EOF'
Usage: ./skills/batch-image-converter/local/run_batch_converter.sh [options]

Options:
  --images PATH   Source image folder. Defaults to assets/image_objects.
  --prompt PATH   Prompt text file. Defaults to assets/prompt.txt.
  --execute       Run Codex for each manifest entry after preparing the manifest.
  --limit N       Process only the first N pending entries when executing.
  --force         Re-run entries even when the target file already exists.
  -h, --help      Show this help.
EOF
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 2
            ;;
    esac
done

cd "$project_root"

if [[ ! -d "$images_path" ]]; then
    echo "Image folder does not exist: $images_path" >&2
    exit 1
fi

if [[ ! -f "$prompt_path" ]]; then
    echo "Prompt file does not exist: $prompt_path" >&2
    exit 1
fi

images_path="${images_path%/}"
output_path="${images_path}_converted"
manifest_path="$output_path/_codex_conversion_manifest.jsonl"

if [[ -f "$manifest_path" ]]; then
    echo "Using existing manifest:"
    echo "$manifest_path"
else
    python main.py \
        --images "$images_path" \
        --prompt "$prompt_path" \
        --imgformats JPG PNG JPEG
fi

echo
echo "Manifest prepared at:"
echo "$manifest_path"
echo

if [[ "$execute" == true ]]; then
    args=(scripts/run_codex_batch.py --manifest "$manifest_path")

    if [[ "$limit" -gt 0 ]]; then
        args+=(--limit "$limit")
    fi

    if [[ "$force" == true ]]; then
        args+=(--force)
    fi

    python "${args[@]}"
else
    echo "To ask Codex to generate real converted images for every entry, run:"
    echo "./skills/batch-image-converter/local/run_batch_converter.sh --execute"
    echo
    echo "For a small first test, run:"
    echo "./skills/batch-image-converter/local/run_batch_converter.sh --execute --limit 3"
fi
