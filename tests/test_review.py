import unittest

from model_output_review.review import apply_corrections, build_queue, summarize


class ReviewTests(unittest.TestCase):
    def test_build_queue_uses_confidence_threshold(self):
        predictions = [
            {
                "record_id": "R-1",
                "category_confidence": "0.95",
                "priority_confidence": "0.55",
            },
            {
                "record_id": "R-2",
                "category_confidence": "0.91",
                "priority_confidence": "0.88",
            },
        ]

        queue = build_queue(predictions, threshold=0.75)

        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["record_id"], "R-1")

    def test_apply_corrections_preserves_prediction_context(self):
        predictions = [
            {
                "record_id": "R-1",
                "predicted_category": "A",
                "predicted_priority": "High",
            }
        ]
        corrections = [
            {
                "record_id": "R-1",
                "final_category": "B",
                "final_priority": "Normal",
                "review_reason": "low confidence",
                "reviewer_note": "changed after review",
            }
        ]

        final_rows = apply_corrections(predictions, corrections)

        self.assertEqual(final_rows[0]["predicted_category"], "A")
        self.assertEqual(final_rows[0]["final_category"], "B")
        self.assertEqual(final_rows[0]["changed"], "True")

    def test_summarize_counts_changes(self):
        summary = summarize(
            [
                {
                    "changed": "True",
                    "predicted_category": "A",
                    "final_category": "B",
                    "predicted_priority": "Normal",
                    "final_priority": "Normal",
                },
                {
                    "changed": "False",
                    "predicted_category": "A",
                    "final_category": "A",
                    "predicted_priority": "Normal",
                    "final_priority": "Normal",
                },
            ]
        )

        self.assertEqual(summary["changed_rows"], 1)
        self.assertEqual(summary["category_changes"], 1)
        self.assertEqual(summary["priority_changes"], 0)


if __name__ == "__main__":
    unittest.main()
