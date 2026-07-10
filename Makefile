PYTHON ?= python3

.PHONY: test demo queue apply report

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests

queue:
	PYTHONPATH=src $(PYTHON) -m model_output_review queue

apply:
	PYTHONPATH=src $(PYTHON) -m model_output_review apply

report:
	PYTHONPATH=src $(PYTHON) -m model_output_review report

demo: queue apply report
