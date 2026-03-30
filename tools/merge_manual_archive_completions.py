#!/usr/bin/env python3
"""Validate and merge manual archive completion records into a completed ledger."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUEUE = ROOT / "archived_specs" / "manual_archive_task_queue.json"
DEFAULT_COMPLETIONS = ROOT / "archived_specs" / "manual_archive_completion_template.csv"
DEFAULT_OUTPUT_CSV = ROOT / "archived_specs" / "manual_archive_completed_records.csv"
DEFAULT_OUTPUT_JSON = ROOT / "archived_specs" / "manual_archive_completed_records.json"

QUEUE_FIELDS = [
    "id",
    "model",
    "brand",
    "category",
    "official_source_url",
    "sample_status",
    "source_entry_type",
    "archive_capture_status",
    "priority",
    "manual_status",
]
LIST_FIELDS = {"manual_action_steps", "required_outputs"}
COMPLETION_FIELDS = [
    "browser_capture_state",
    "browser_pdf_path",
    "browser_screenshot_path",
    "wayback_url",
    "archive_today_url",
    "completed_by",
    "completed_date",
    "capture_note",
    "archive_note",
]
OUTPUT_FIELDS = QUEUE_FIELDS + ["manual_action_steps", "required_outputs"] + COMPLETION_FIELDS + [
    "browser_pdf_exists",
    "browser_screenshot_exists",
    "record_status",
    "validation_note",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE, help="Path to manual_archive_task_queue.json")
    parser.add_argument(
        "--completions",
        type=Path,
        default=DEFAULT_COMPLETIONS,
        help="Path to a filled-in completion CSV, usually based on the completion template",
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV, help="Merged completed-records CSV")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="Merged completed-records JSON")
    return parser.parse_args()


def load_queue(path: Path) -> list[dict]:
    payload = json.loads(path.read_text())
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError("Queue JSON does not contain a rows array")
    return rows


def load_completions(path: Path) -> dict[str, dict]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"id", *COMPLETION_FIELDS}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Completion CSV is missing required columns: {sorted(missing)}")
        records: dict[str, dict] = {}
        for row in reader:
            row_id = str(row["id"]).strip()
            if not row_id:
                raise ValueError("Completion CSV contains a row without an id")
            if row_id in records:
                raise ValueError(f"Duplicate completion row for id {row_id}")
            records[row_id] = row
    return records


def flatten_list_field(value: object) -> str:
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=True)
    return "" if value is None else str(value)


def resolve_path(raw: str) -> Path | None:
    text = (raw or "").strip()
    if not text:
        return None
    path = Path(text)
    return path if path.is_absolute() else (ROOT / path)


def completion_state(row: dict) -> str:
    value = (row.get("browser_capture_state") or "").strip().lower()
    if value not in {"captured", "partial", "blocked"}:
        raise ValueError(f"Row {row.get('id')} has invalid browser_capture_state: {value!r}")
    return value


def validate_artifacts(row_id: str, row: dict) -> tuple[bool, bool, str]:
    pdf_path = resolve_path(row.get("browser_pdf_path", ""))
    screenshot_path = resolve_path(row.get("browser_screenshot_path", ""))
    pdf_exists = bool(pdf_path and pdf_path.exists())
    screenshot_exists = bool(screenshot_path and screenshot_path.exists())
    state = completion_state(row)

    if state == "captured" and not (pdf_exists or screenshot_exists):
        raise FileNotFoundError(
            f"Row {row_id} is marked captured but neither browser PDF nor screenshot exists on disk"
        )
    if state in {"partial", "blocked"} and not (row.get("capture_note") or row.get("archive_note")):
        raise ValueError(
            f"Row {row_id} is {state} but has no capture_note or archive_note explaining the outcome"
        )

    if pdf_path and not pdf_exists:
        raise FileNotFoundError(f"Row {row_id} PDF path does not exist: {pdf_path}")
    if screenshot_path and not screenshot_exists:
        raise FileNotFoundError(f"Row {row_id} screenshot path does not exist: {screenshot_path}")

    return pdf_exists, screenshot_exists, state


def merge(queue_rows: list[dict], completion_rows: dict[str, dict]) -> list[dict]:
    merged: list[dict] = []
    queue_ids = {str(row["id"]) for row in queue_rows}
    completion_ids = set(completion_rows)

    missing = queue_ids - completion_ids
    extra = completion_ids - queue_ids
    if missing:
        raise ValueError(f"Missing completion rows for queue ids: {sorted(missing)}")
    if extra:
        raise ValueError(f"Completion CSV contains unknown ids: {sorted(extra)}")

    for row in queue_rows:
        row_id = str(row["id"])
        completion = completion_rows[row_id]
        pdf_exists, screenshot_exists, state = validate_artifacts(row_id, completion)

        merged_row = {field: row.get(field, "") for field in QUEUE_FIELDS}
        merged_row["manual_action_steps"] = flatten_list_field(row.get("manual_action_steps"))
        merged_row["required_outputs"] = flatten_list_field(row.get("required_outputs"))
        for field in COMPLETION_FIELDS:
            merged_row[field] = completion.get(field, "").strip()
        merged_row["browser_pdf_exists"] = "yes" if pdf_exists else "no"
        merged_row["browser_screenshot_exists"] = "yes" if screenshot_exists else "no"
        if state == "captured":
            merged_row["record_status"] = "completed"
            merged_row["validation_note"] = "browser capture complete"
        elif state == "partial":
            merged_row["record_status"] = "partial"
            merged_row["validation_note"] = "browser capture partial"
        else:
            merged_row["record_status"] = "blocked"
            merged_row["validation_note"] = "browser capture blocked"
        merged.append(merged_row)
    return merged


def write_outputs(rows: list[dict], output_csv: Path, output_json: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    output_json.write_text(json.dumps(rows, indent=2, ensure_ascii=True) + "\n")


def main() -> None:
    args = parse_args()
    queue_rows = load_queue(args.queue)
    completion_rows = load_completions(args.completions)
    merged_rows = merge(queue_rows, completion_rows)
    write_outputs(merged_rows, args.output_csv, args.output_json)


if __name__ == "__main__":
    main()
