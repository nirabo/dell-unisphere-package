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
- **Swagger UI**: Self-documenting API with authentication support
- **Test Scripts**: Comprehensive test scripts to verify API functionality

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
# Run the test script
make test
```

### Test Report

A comprehensive test report is available at [Test Report](tests/scripts/test_results/test_report.md). This report includes:

- API version information
- Test results for all major endpoints
- Sample requests and responses
- Coverage information

## API Documentation

Detailed API documentation is available in the `docs` directory:

- [Dell Unisphere REST API Documentation](docs/DellUnisphereRestAPI.md)
- [Requirements Documentation](docs/Requirements.md)

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

### File Upload

Handles software package uploads.

```
POST /upload/files/types/candidateSoftwareVersion
```

## Development

### Project Structure

```
dell-unisphere-package/
├── docs/                 # Documentation files
├── src/                  # Source code
│   └── dell_unisphere_package/
│       ├── controllers/  # Business logic
│       ├── models/       # Data models
│       ├── routes/       # API endpoints
│       ├── schemas/      # Pydantic schemas
│       └── main.py       # Application entry point
├── tests/                # Test files
│   ├── scripts/          # Test scripts
│   └── unit/             # Unit tests
├── Makefile              # Build and run commands
└── README.md             # This file
```

### Adding New Features

To add a new resource type:

1. Add the schema in `src/dell_unisphere_package/schemas/`
2. Add the storage model in `src/dell_unisphere_package/models/`
3. Create routes in `src/dell_unisphere_package/routes/`
4. Register the routes in `src/dell_unisphere_package/routes/__init__.py`
5. Update tests in `tests/scripts/test_api.sh`
6. Update documentation in `docs/`

## License

[License information]

## Disclaimer

This is a mock implementation for development and testing purposes only. It is not affiliated with or endorsed by Dell Technologies.
