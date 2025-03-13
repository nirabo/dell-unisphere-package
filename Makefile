# Makefile for Dell Unisphere Mock API

# Variables
PYTHON := python
UV := uv
PIP := pip
APP_MODULE := dell_unisphere_package.main:app
TEST_DIR := tests
COVERAGE_REPORT := coverage.xml
DOCS_DIR := docs
TEST_REPORT_DIR := tests/scripts/test_results

# Check if uv is available, otherwise use pip
ifeq ($(shell which uv >/dev/null 2>&1; echo $$?), 0)
	PKG_MANAGER := uv
else
	PKG_MANAGER := pip
endif

# Default target
all: install test lint

# Install dependencies
install:
ifeq ($(PKG_MANAGER), uv)
	$(UV) sync
else
	$(PIP) install -e .
endif

# Run all tests and generate coverage report
test:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run python -m pytest $(TEST_DIR) --cov=src --cov-report=xml:$(COVERAGE_REPORT) --cov-report=term
else
	$(PYTHON) -m pytest $(TEST_DIR) --cov=src --cov-report=xml:$(COVERAGE_REPORT) --cov-report=term
endif
	@echo "Test results written to $(COVERAGE_REPORT)"

# Run unit tests only
test-unit:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run python -m pytest $(TEST_DIR)/unit -v -m unit
else
	$(PYTHON) -m pytest $(TEST_DIR)/unit -v -m unit
endif

# Run integration tests only
test-integration:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run python -m pytest $(TEST_DIR)/integration -v -m integration
else
	$(PYTHON) -m pytest $(TEST_DIR)/integration -v -m integration
endif

# Run end-to-end tests only
test-e2e:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run python -m pytest $(TEST_DIR)/e2e -v -m e2e
else
	$(PYTHON) -m pytest $(TEST_DIR)/e2e -v -m e2e
endif

# Run security tests only
test-security:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run python -m pytest $(TEST_DIR) -v -m security
else
	$(PYTHON) -m pytest $(TEST_DIR) -v -m security
endif

# Run error handling tests only
test-error:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run python -m pytest $(TEST_DIR) -v -m error
else
	$(PYTHON) -m pytest $(TEST_DIR) -v -m error
endif

# Generate HTML test report
test-report:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run python -m pytest $(TEST_DIR) --cov=src --cov-report=html:$(TEST_REPORT_DIR)/coverage --html=$(TEST_REPORT_DIR)/pytest_report.html
else
	$(PYTHON) -m pytest $(TEST_DIR) --cov=src --cov-report=html:$(TEST_REPORT_DIR)/coverage --html=$(TEST_REPORT_DIR)/pytest_report.html
endif
	@echo "HTML test reports generated in $(TEST_REPORT_DIR)"

# Run the FastAPI server
run:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run $(PYTHON) -m uvicorn $(APP_MODULE) --reload
else
	$(PYTHON) -m uvicorn $(APP_MODULE) --reload
endif

# Lint and format code
lint:
ifeq ($(PKG_MANAGER), uv)
	$(UV) run pre-commit run --all
else
	$(PYTHON) -m pre_commit run --all
endif

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
