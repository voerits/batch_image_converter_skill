import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_manifest(manifest_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    with manifest_path.open("r", encoding="utf-8") as manifest_file:
        for line_number, line in enumerate(manifest_file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                entries.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on manifest line {line_number}: {exc}") from exc

    return entries


def write_manifest(manifest_path: Path, entries: list[dict[str, Any]]) -> None:
    with manifest_path.open("w", encoding="utf-8") as manifest_file:
        for entry in entries:
            manifest_file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def build_codex_prompt(entry: dict[str, Any], skill_path: Path) -> str:
    return f"""Use the Codex skill at \"{skill_path}\" as $batch-image-converter.

Convert the attached source image into a real output image file.

Source image: {entry["source_path"]}
Target path: {entry["target_path"]}
Target format: {entry["image_format"]}

Conversion instruction:
{entry["instruction"]}

Important:
- Actually create the converted image file at the target path.
- Preserve the main object and composition from the source image.
- Apply the user's visual conversion request.
- Create parent directories if needed.
- Do not stop after writing a manifest or explanation.
- In your final response, say only whether the target image file was created.
"""


def run_codex_for_entry(
    entry: dict[str, Any],
    skill_path: Path,
    project_root: Path,
    extra_codex_args: list[str],
) -> subprocess.CompletedProcess[str]:
    source_path = Path(entry["source_path"])
    target_path = Path(entry["target_path"])
    target_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_codex_prompt(entry, skill_path)

    command = [
        "codex",
        "exec",
        "-C",
        str(project_root),
        "--sandbox",
        "workspace-write",
        "--image",
        str(source_path),
        *extra_codex_args,
    ]

    return subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Codex once per image in a batch conversion manifest."
    )
    parser.add_argument("--manifest", required=True, help="Path to _codex_conversion_manifest.jsonl")
    parser.add_argument(
        "--project-root",
        default=".",
        help="Repository root passed to codex exec with -C.",
    )
    parser.add_argument(
        "--skill-path",
        default="skills/batch-image-converter",
        help="Path to the batch-image-converter skill folder.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only process the first N pending entries.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-run entries even when the target file already exists.",
    )
    parser.add_argument(
        "--codex-arg",
        action="append",
        default=[],
        help="Extra argument to pass to codex exec. Repeat for multiple arguments.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    project_root = Path(args.project_root).expanduser().resolve()
    skill_path = Path(args.skill_path).expanduser().resolve()

    entries = load_manifest(manifest_path)
    processed = 0
    failures = 0

    for index, entry in enumerate(entries, start=1):
        target_path = Path(entry["target_path"])
        if target_path.exists() and not args.force:
            entry["status"] = "skipped_existing"
            continue

        if args.limit is not None and processed >= args.limit:
            break

        print(f"[{index}/{len(entries)}] Converting {entry['source_path']}")
        result = run_codex_for_entry(entry, skill_path, project_root, args.codex_arg)
        processed += 1

        log_path = manifest_path.parent / f"_codex_conversion_{index:04d}.log"
        log_path.write_text(
            "STDOUT:\n"
            + (result.stdout or "")
            + "\nSTDERR:\n"
            + (result.stderr or ""),
            encoding="utf-8",
        )

        if result.returncode == 0 and target_path.exists() and target_path.stat().st_size > 0:
            entry["status"] = "completed"
        else:
            entry["status"] = "failed"
            entry["log_path"] = str(log_path)
            failures += 1
            print(f"  failed; see {log_path}", file=sys.stderr)

        write_manifest(manifest_path, entries)

    print(f"Processed {processed} entr{'y' if processed == 1 else 'ies'}; failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
