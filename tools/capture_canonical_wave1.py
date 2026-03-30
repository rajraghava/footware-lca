#!/usr/bin/env python3
"""Capture local HTML, PDF, and screenshots for canonical Phase 1 rows."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "archived_specs" / "canonical_40_archive_index.csv"
QUEUE_PATH = ROOT / "archived_specs" / "canonical_40_high_priority_queue.csv"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--selection-mode",
        choices=["queue_rank_range", "index_filter"],
        default="queue_rank_range",
    )
    parser.add_argument("--start-rank", type=int, default=1)
    parser.add_argument("--end-rank", type=int, default=5)
    parser.add_argument("--upgrade-priority", default="")
    parser.add_argument("--require-tier", default="")
    parser.add_argument("--only-pending", action="store_true")
    parser.add_argument(
        "--log-path",
        default="archived_specs/canonical_capture_log.csv",
        help="Repo-relative CSV path for the capture log.",
    )
    return parser.parse_args()


def run_capture(url: str, html_path: Path, pdf_path: Path, screenshot_path: Path) -> tuple[str, str]:
    errors: list[str] = []

    try:
        html_result = subprocess.run(
            [str(CHROME), "--headless=new", "--no-sandbox", "--disable-gpu", "--dump-dom", url],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if html_result.returncode == 0 and html_result.stdout.strip():
            html_path.write_text(html_result.stdout, encoding="utf-8")
        else:
            errors.append(f"html:{html_result.returncode}")
    except subprocess.TimeoutExpired:
        errors.append("html:timeout")

    try:
        pdf_result = subprocess.run(
            [
                str(CHROME),
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=45,
        )
        if pdf_result.returncode != 0 or not pdf_path.exists():
            errors.append(f"pdf:{pdf_result.returncode}")
    except subprocess.TimeoutExpired:
        errors.append("pdf:timeout")

    try:
        screenshot_result = subprocess.run(
            [
                str(CHROME),
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--window-size=1440,2400",
                f"--screenshot={screenshot_path}",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=45,
        )
        if screenshot_result.returncode != 0 or not screenshot_path.exists():
            errors.append(f"screenshot:{screenshot_result.returncode}")
    except subprocess.TimeoutExpired:
        errors.append("screenshot:timeout")

    status = "captured_cleanly" if not errors else "capture_attempt_incomplete"
    return status, ";".join(errors)


def relpath(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def select_rows(index: pd.DataFrame, queue: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    if args.selection_mode == "queue_rank_range":
        queue["_queue_rank_num"] = pd.to_numeric(queue["Queue_Rank"], errors="coerce")
        return queue[queue["_queue_rank_num"].between(args.start_rank, args.end_rank, inclusive="both")].copy()

    selected = index.copy()
    if args.upgrade_priority:
        selected = selected[selected["Upgrade_Priority"] == args.upgrade_priority]
    if args.require_tier:
        selected = selected[selected["Evidence_Tier_Final"] == args.require_tier]
    if args.only_pending:
        selected = selected[selected["Capture_Status"] != "captured_cleanly"]
    return selected.copy()


def main() -> None:
    args = parse_args()
    index = pd.read_csv(INDEX_PATH, dtype=str).fillna("")
    queue = pd.read_csv(QUEUE_PATH, dtype=str).fillna("")
    selected = select_rows(index, queue, args)
    progress_report = ROOT / args.log_path

    log_rows: list[dict[str, str]] = []
    for row in selected.to_dict(orient="records"):
        html_path = ROOT / row["Planned_HTML_Path"]
        pdf_path = ROOT / row["Planned_PDF_Path"]
        screenshot_path = ROOT / row["Planned_Screenshot_Path"]
        html_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        status, errors = run_capture(row["Resolved_URL"], html_path, pdf_path, screenshot_path)

        mask = index["Model"] == row["Model"]
        if html_path.exists():
            index.loc[mask, "Existing_HTML_Artifact"] = relpath(html_path)
        if pdf_path.exists():
            index.loc[mask, "Existing_PDF_Artifact"] = relpath(pdf_path)
        if screenshot_path.exists():
            index.loc[mask, "Existing_Screenshot_Artifact"] = relpath(screenshot_path)
        index.loc[mask, "Capture_Status"] = status
        note_prefix = index.loc[mask, "Notes"].iloc[0]
        if status == "captured_cleanly":
            note_prefix = note_prefix.replace("Local capture still pending.", "").strip()
            capture_note = "Local HTML/PDF/screenshot capture completed."
        else:
            capture_note = f"Capture errors: {errors}"
        index.loc[mask, "Notes"] = f"{note_prefix} {capture_note}".strip()

        log_rows.append(
            {
                "Model": row["Model"],
                "Resolved_URL": row["Resolved_URL"],
                "HTML_Path": relpath(html_path) if html_path.exists() else "",
                "PDF_Path": relpath(pdf_path) if pdf_path.exists() else "",
                "Screenshot_Path": relpath(screenshot_path) if screenshot_path.exists() else "",
                "Capture_Status": status,
                "Errors": errors,
            }
        )

    index.to_csv(INDEX_PATH, index=False)
    updated_queue = index[index["Upgrade_Priority"] == "high"].copy()
    updated_queue["_queue_rank_sort"] = pd.to_numeric(updated_queue["Queue_Rank"], errors="coerce")
    updated_queue = updated_queue.sort_values(["_queue_rank_sort", "Model"], na_position="last").drop(columns=["_queue_rank_sort"])
    updated_queue.to_csv(QUEUE_PATH, index=False)

    with progress_report.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Model", "Resolved_URL", "HTML_Path", "PDF_Path", "Screenshot_Path", "Capture_Status", "Errors"],
        )
        writer.writeheader()
        writer.writerows(log_rows)


if __name__ == "__main__":
    main()
