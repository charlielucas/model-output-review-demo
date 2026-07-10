"""Command line entry points for the review workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from .io import read_csv, write_csv
from .review import apply_corrections, build_queue, summarize


ROOT = Path(__file__).resolve().parents[2]
PREDICTIONS_PATH = ROOT / "data" / "predictions.csv"
CORRECTIONS_PATH = ROOT / "data" / "corrections.csv"
QUEUE_PATH = ROOT / "examples" / "review_queue.csv"
FINAL_LABELS_PATH = ROOT / "examples" / "final_labels.csv"
REPORT_PATH = ROOT / "examples" / "review_report.md"


def queue(
    predictions_path: Path = PREDICTIONS_PATH,
    output_path: Path = QUEUE_PATH,
    threshold: float = 0.75,
) -> list[dict[str, object]]:
    rows = read_csv(predictions_path)
    review_rows = build_queue(rows, threshold=threshold)
    fieldnames = list(review_rows[0].keys()) if review_rows else []
    write_csv(output_path, review_rows, fieldnames)
    return review_rows


def apply(
    predictions_path: Path = PREDICTIONS_PATH,
    corrections_path: Path = CORRECTIONS_PATH,
    output_path: Path = FINAL_LABELS_PATH,
) -> list[dict[str, object]]:
    predictions = read_csv(predictions_path)
    corrections = read_csv(corrections_path)
    final_rows = apply_corrections(predictions, corrections)
    fieldnames = list(final_rows[0].keys()) if final_rows else []
    write_csv(output_path, final_rows, fieldnames)
    return final_rows


def report(final_labels_path: Path = FINAL_LABELS_PATH, output_path: Path = REPORT_PATH) -> str:
    final_rows = read_csv(final_labels_path)
    summary = summarize(final_rows)
    changed = [row for row in final_rows if row["changed"] == "True"]

    lines = [
        "# Review Report",
        "",
        f"- Total rows: {summary['total_rows']}",
        f"- Changed rows: {summary['changed_rows']}",
        f"- Category changes: {summary['category_changes']}",
        f"- Priority changes: {summary['priority_changes']}",
        "",
        "## Changed Records",
        "",
        "| record | predicted category | final category | predicted priority | final priority | reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in changed:
        lines.append(
            "| {record_id} | {predicted_category} | {final_category} | {predicted_priority} | {final_priority} | {review_reason} |".format(
                **row
            )
        )
    lines.append("")

    output = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Model output review workflow")
    parser.add_argument("command", choices=["queue", "apply", "report"])
    parser.add_argument("--predictions-path", type=Path, default=PREDICTIONS_PATH)
    parser.add_argument("--corrections-path", type=Path, default=CORRECTIONS_PATH)
    parser.add_argument("--queue-path", type=Path, default=QUEUE_PATH)
    parser.add_argument("--final-labels-path", type=Path, default=FINAL_LABELS_PATH)
    parser.add_argument("--report-path", type=Path, default=REPORT_PATH)
    parser.add_argument("--threshold", type=float, default=0.75)
    args = parser.parse_args()

    if args.command == "queue":
        rows = queue(
            predictions_path=args.predictions_path,
            output_path=args.queue_path,
            threshold=args.threshold,
        )
        print(f"Wrote {len(rows)} review rows to {args.queue_path}")
    elif args.command == "apply":
        rows = apply(
            predictions_path=args.predictions_path,
            corrections_path=args.corrections_path,
            output_path=args.final_labels_path,
        )
        print(f"Wrote {len(rows)} final rows to {args.final_labels_path}")
    elif args.command == "report":
        print(report(final_labels_path=args.final_labels_path, output_path=args.report_path))


if __name__ == "__main__":
    main()
