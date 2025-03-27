# Dell Unisphere Mock API

A mock implementation of the Dell EMC Unisphere REST API for Unity storage systems, designed for development and testing purposes without requiring access to actual Unity storage hardware.

## Overview

This package provides a FastAPI-based implementation of the Dell Unisphere API, focusing on the software upgrade functionality. It simulates the behavior of a real Unity storage system, allowing developers to test their applications against a realistic API without needing physical hardware.

## Features

- **Authentication**: HTTP Basic Authentication and session-based authentication with CSRF protection
- **API Resources**:
  - Basic System Information
  - Login Session Management
  - User Management
  - Candidate Software Versions
  - Installed Software Versions
  - Upgrade Sessions
  - File Upload for Software Packages
  - System Configuration for Mock Behavior Control
- **Parametric Testing**: Control API behavior for testing both success and failure scenarios
  - Configurable eligibility verification with success, failure, and auto modes
  - Randomized failure simulation with adjustable probability
  - Query parameter overrides for specific test cases
- **Swagger UI**: Self-documenting API with authentication support
- **Test Scripts**: Comprehensive test scripts to verify API functionality, including shell scripts and pytest integration tests

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd dell-unisphere-package

# Install dependencies using astral uv (recommended)
uv pip install -e .

# Or using standard pip
pip install -e .
```

## Usage

### Starting the Server

```bash
# Start the server using the Makefile
make run
```

The server will be available at http://localhost:8000 by default.

### API Documentation

Access the Swagger UI documentation at http://localhost:8000/docs

### Authentication

The API supports HTTP Basic Authentication with the following default credentials:

- Username: `admin`, Password: `Password123!`
- Username: `user`, Password: `Password123!`
- Username: `diagnose`, Password: `Password123!`

### Testing

```bash
# Run all tests with coverage
make test

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run only end-to-end tests
make test-e2e

# Generate HTML test report with coverage
make test-report
```

Our testing approach follows the [Test Pyramid](docs/TestStrategy.md) methodology with comprehensive unit, integration, and end-to-end tests.

### Parametric Testing

The mock API supports parametric testing of various scenarios through the system configuration endpoints. This is particularly useful for testing how client applications handle both success and failure responses.

#### Eligibility Testing Scripts

```bash
# Run the eligibility testing shell script
./tests/scripts/test_eligibility_modes.sh

# Run the eligibility testing integration tests
make test-integration PYTEST_ARGS="-v tests/integration/test_eligibility_modes.py"
```

The eligibility testing scripts demonstrate how to:

1. Switch between success, failure, and auto modes
2. Test with explicit parameter overrides
3. Verify randomized behavior in auto mode
4. Reset system configuration to default values

### Test Report and Coverage

A comprehensive test report is available at [Test Report](tests/scripts/test_results/test_report.md). This report includes:

- API version information
- Test results for all major endpoints
- Sample requests and responses
- Coverage information

Detailed coverage reports are generated in HTML format in the `tests/scripts/test_results/coverage` directory after running `make test-report`.

## Documentation

Comprehensive documentation is available in the `docs` directory:

### API Documentation
- [Dell Unisphere REST API Documentation](docs/DellUnisphereRestAPI.md) - Detailed specification of the Dell Unisphere REST API endpoints, request/response formats, and authentication mechanisms.

### Project Documentation
- [Architecture](docs/Architecture.md) - Detailed software architecture including component design, data flow, and deployment considerations.
- [Requirements Documentation](docs/Requirements.md) - Functional and non-functional requirements for the Dell Unisphere Mock API.
- [Test Strategy](docs/TestStrategy.md) - Comprehensive testing approach including unit, integration, and e2e tests organized according to the test pyramid approach.
- [Use Cases](docs/UseCases.md) - Common use case scenarios and workflows for interacting with the Dell Unisphere API.
- [Project Backlog](docs/Backlog.md) - Current development status, completed features, and planned enhancements.
- [Presentation](docs/presentation.md) - Comprehensive Marp presentation detailing the problem, solution, and results of the Dell Unisphere Mock API implementation, with a focus on the software upgrade process.

### Additional Resources
The API also provides interactive documentation through Swagger UI, available at http://localhost:8000/docs when the server is running.

## Implemented Resource Types

### Basic System Info

Provides basic information about the storage system.

```
GET /api/types/basicSystemInfo/instances
```

### Login Session Info

Manages user sessions and authentication.

```
GET /api/types/loginSessionInfo/instances
POST /api/types/loginSessionInfo/action/logout
```

### User

Manages user accounts and permissions.

```
GET /api/types/user/instances
```

### Candidate Software Version

Manages software versions available for upgrade.

```
GET /api/types/candidateSoftwareVersion/instances
POST /api/types/candidateSoftwareVersion/action/prepare
```

### Installed Software Version

Provides information about currently installed software.

```
GET /api/types/installedSoftwareVersion/instances
GET /api/instances/installedSoftwareVersion/{id}
```

### Upgrade Session

Manages software upgrade sessions.

```
GET /api/types/upgradeSession/instances
POST /api/types/upgradeSession/instances
POST /api/types/upgradeSession/action/verifyUpgradeEligibility
POST /api/instances/upgradeSession/{id}/action/resume
```

### System Configuration

Controls the behavior of the mock API for testing purposes.

```
GET /api/types/systemConfig/instances
POST /api/types/systemConfig/action/update
```

The system configuration endpoints allow you to control how the mock API behaves, particularly for testing different scenarios:

- **Eligibility Status**: Control whether eligibility verification succeeds or fails
  - `success`: Always returns success response
  - `failure`: Always returns failure response with error codes
  - `auto`: Randomly returns success or failure based on a configurable threshold
- **Failure Codes**: Customize the error codes returned in failure responses
- **Auto Failure Threshold**: Set the probability of failure in auto mode (0.0 to 1.0)

### File Upload

Handles software package uploads.

```
POST /upload/files/types/candidateSoftwareVersion
```

## Development

### Project Roadmap

The project is currently at version 0.2.0. For a detailed view of completed features and planned enhancements, see the [Project Backlog](docs/Backlog.md).

#### Current Status
- Core API functionality is implemented with proper authentication and response formatting
- Comprehensive test suite with unit, integration, and e2e tests
- CI/CD pipelines with GitHub Actions
- Support for both astral uv and standard pip package management

#### Next Steps
- Additional Dell Unisphere API endpoints
- Enhanced documentation and examples
- Improved test coverage
- Containerization

For more details on the development roadmap, refer to the [Project Backlog](docs/Backlog.md).

### Project Structure

```
dell-unisphere-package/
├── docs/                 # Documentation files
│   ├── Backlog.md        # Project roadmap and status
│   ├── TestStrategy.md   # Testing methodology
│   ├── UseCases.md       # API usage examples
│   └── Requirements.md   # Project requirements
├── src/                  # Source code
│   └── dell_unisphere_package/
│       ├── controllers/  # Business logic
│       ├── models/       # Data models
│       ├── routes/       # API endpoints
│       ├── schemas/      # Pydantic schemas
│       └── main.py       # Application entry point
├── tests/                # Test files
│   ├── e2e/              # End-to-end tests
│   ├── integration/      # Integration tests
│   ├── scripts/          # Test scripts
│   │   └── test_results/ # Test reports and coverage
│   └── unit/             # Unit tests
├── .github/workflows/    # GitHub Actions CI/CD
├── Makefile              # Build and run commands
└── README.md             # This file
```

### Adding New Features

To add a new resource type:

1. Add the schema in `src/dell_unisphere_package/schemas/`
2. Add the storage model in `src/dell_unisphere_package/models/`
3. Create routes in `src/dell_unisphere_package/routes/`
4. Register the routes in `src/dell_unisphere_package/routes/__init__.py`
5. Add tests following the [Test Strategy](docs/TestStrategy.md):
   - Unit tests in `tests/unit/`
   - Integration tests in `tests/integration/`
   - End-to-end tests in `tests/e2e/`
6. Update API test scripts in `tests/scripts/test_api.sh`
7. Update documentation in `docs/`
8. Update the [Project Backlog](docs/Backlog.md) to reflect the new feature

Ensure all new code maintains or improves the current test coverage levels. Run `make test-report` to generate coverage reports and verify your changes meet the project's quality standards.

## License

[License information]

## Disclaimer

This is a mock implementation for development and testing purposes only. It is not affiliated with or endorsed by Dell Technologies.
