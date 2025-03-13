# Makefile for Dell Unisphere Mock API

# Variables
PYTHON := python
UV := uv
APP_MODULE := dell_unisphere_package.main:app
TEST_DIR := tests
COVERAGE_REPORT := coverage.xml
DOCS_DIR := docs
TEST_REPORT_DIR := tests/scripts/test_results

# Default target
all: install test lint

# Install dependencies
install:
	$(UV) sync

# Run all tests and generate coverage report
test:
	$(UV) run pytest $(TEST_DIR) --cov=src --cov-report=xml:$(COVERAGE_REPORT) --cov-report=term
	@echo "Test results written to $(COVERAGE_REPORT)"

# Run unit tests only
test-unit:
	$(UV) run pytest $(TEST_DIR)/unit -v -m unit

# Run integration tests only
test-integration:
	$(UV) run pytest $(TEST_DIR)/integration -v -m integration

# Run end-to-end tests only
test-e2e:
	$(UV) run pytest $(TEST_DIR)/e2e -v -m e2e

# Run security tests only
test-security:
	$(UV) run pytest $(TEST_DIR) -v -m security

# Run error handling tests only
test-error:
	$(UV) run pytest $(TEST_DIR) -v -m error

# Generate HTML test report
test-report:
	$(UV) run pytest $(TEST_DIR) --cov=src --cov-report=html:$(TEST_REPORT_DIR)/coverage --html=$(TEST_REPORT_DIR)/pytest_report.html
	@echo "HTML test reports generated in $(TEST_REPORT_DIR)"

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
	rm -rf $(TEST_REPORT_DIR)/coverage
	rm -f $(TEST_REPORT_DIR)/pytest_report.html

# Phony targets
.PHONY: all install test test-unit test-integration test-e2e test-security test-error test-report run lint docs clean
