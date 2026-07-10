"""Review queue and correction helpers."""

from __future__ import annotations


def review_reasons(row: dict[str, str], threshold: float = 0.75) -> list[str]:
    reasons: list[str] = []
    if float(row["category_confidence"]) < threshold:
        reasons.append("low category confidence")
    if float(row["priority_confidence"]) < threshold:
        reasons.append("low priority confidence")
    return reasons


def build_queue(predictions: list[dict[str, str]], threshold: float = 0.75) -> list[dict[str, object]]:
    queue: list[dict[str, object]] = []
    for row in predictions:
        reasons = review_reasons(row, threshold=threshold)
        if reasons:
            queue.append({**row, "review_reasons": "; ".join(reasons)})
    return queue


def apply_corrections(
    predictions: list[dict[str, str]],
    corrections: list[dict[str, str]],
) -> list[dict[str, object]]:
    corrections_by_id = {row["record_id"]: row for row in corrections}
    final_rows: list[dict[str, object]] = []

    for row in predictions:
        correction = corrections_by_id.get(row["record_id"])
        final_category = row["predicted_category"]
        final_priority = row["predicted_priority"]
        review_reason = ""
        reviewer_note = ""
        changed = False

        if correction:
            final_category = correction["final_category"]
            final_priority = correction["final_priority"]
            review_reason = correction["review_reason"]
            reviewer_note = correction["reviewer_note"]
            changed = (
                final_category != row["predicted_category"]
                or final_priority != row["predicted_priority"]
            )

        final_rows.append(
            {
                **row,
                "final_category": final_category,
                "final_priority": final_priority,
                "changed": str(changed),
                "review_reason": review_reason,
                "reviewer_note": reviewer_note,
            }
        )

    return final_rows


def summarize(final_rows: list[dict[str, str]]) -> dict[str, int]:
    changed_rows = [row for row in final_rows if row["changed"] == "True"]
    category_changes = [
        row for row in changed_rows if row["final_category"] != row["predicted_category"]
    ]
    priority_changes = [
        row for row in changed_rows if row["final_priority"] != row["predicted_priority"]
    ]
    return {
        "total_rows": len(final_rows),
        "changed_rows": len(changed_rows),
        "category_changes": len(category_changes),
        "priority_changes": len(priority_changes),
    }
