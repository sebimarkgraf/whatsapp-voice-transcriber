
all: docs test

.PHONY: docs test

docs:
	@echo "Generating documentation"
	pdm run pdoc -d google -o docs/ whatsapp_transcribe
	@echo "Documentation generated in docs/"

test:
	pdm run python -m pytest --cov=whatsapp_transcribe tests/
