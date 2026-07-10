import tempfile
import unittest
from pathlib import Path

from model_output_review.cli import CORRECTIONS_PATH, PREDICTIONS_PATH, apply, queue, report


class CliTests(unittest.TestCase):
    def test_workflow_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            queue_path = tmp_path / "queue.csv"
            final_path = tmp_path / "final.csv"
            report_path = tmp_path / "report.md"

            queue(output_path=queue_path)
            apply(output_path=final_path)
            output = report(final_labels_path=final_path, output_path=report_path)

            self.assertTrue(queue_path.exists())
            self.assertTrue(final_path.exists())
            self.assertTrue(report_path.exists())
            self.assertIn("Changed rows", output)


if __name__ == "__main__":
    unittest.main()
