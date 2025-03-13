# Makefile for Dell Unisphere Mock API

# Variables
PYTHON := python
UV := uv
APP_MODULE := dell_unisphere_package.main:app
TEST_DIR := tests
COVERAGE_REPORT := coverage.xml
DOCS_DIR := docs

# Default target
all: install test lint

# Install dependencies
install:
	$(UV) sync

# Run tests and generate coverage report
test:
	$(UV) run pytest $(TEST_DIR) --cov=src --cov-report=xml:$(COVERAGE_REPORT)
	@echo "Test results written to $(COVERAGE_REPORT)"

# Run the FastAPI server
run:
	$(UV) run $(PYTHON) -m uvicorn $(APP_MODULE) --reload

# Lint and format code
lint:
	$(UV) run pre-commit run --all

# Generate documentation
docs:
	@echo "Updating documentation..."
	@# Add documentation generation commands here as needed

# Clean up build artifacts
clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache
	rm -f $(COVERAGE_REPORT)

# Phony targets
.PHONY: all install test run lint docs clean
