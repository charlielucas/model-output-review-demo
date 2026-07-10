# Model Output Review

A small Python project for reviewing model predictions and applying human corrections.

The data is synthetic. It is not employer data, customer data, or a real labeling queue.

## What It Does

The workflow starts with model predictions, builds a review queue, applies reviewer corrections, and writes a short summary of what changed.

It is meant to show the part of ML work that sits after prediction:

- keep model confidence with each row
- route uncertain rows for review
- apply correction decisions from a reviewer
- preserve the original prediction next to the final label
- summarize changes by field and reason

## Quick Start

Use Python 3.9 or newer.

```bash
PYTHONPATH=src python3 -m model_output_review queue
PYTHONPATH=src python3 -m model_output_review apply
PYTHONPATH=src python3 -m model_output_review report
```

Or use the Makefile:

```bash
make test
make demo
```

## Outputs

- `examples/review_queue.csv`
- `examples/final_labels.csv`
- `examples/review_report.md`

## Design Notes

This repo is intentionally simple. It treats review as a data quality workflow: keep enough context to understand the prediction, change only the rows that need a decision, and leave an audit trail.

## Known Limits

- The input data is small and synthetic.
- The review decisions are pre-filled for the demo.
- There is no web UI.
- The rules are meant to be easy to inspect, not exhaustive.
