
all: docs test format lint

.PHONY: docs test format lint

docs:
	@echo "Generating documentation"
	pdm run pdoc -d google -o docs/ whatsapp_transcribe
	@echo "Documentation generated in docs/"

test:
	pdm run python -m pytest --cov=whatsapp_transcribe tests/

format:
	pdm run ruff format .

lint:
	pdm run ruff check --fix .
