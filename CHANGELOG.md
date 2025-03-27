# Changelog

All notable changes to the Dell Unisphere Mock API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-03-26

### Added
- New system configuration endpoints for controlling mock behavior:
  - `GET /api/types/systemConfig/instances`: Returns the current system configuration
  - `POST /api/types/systemConfig/action/update`: Updates the system configuration
- Parametric testing capabilities for eligibility endpoint:
  - Added support for success, failure, and auto (randomized) modes
  - Configurable failure probability in auto mode
  - Explicit parameter override via `fail` query parameter
- Comprehensive test scripts:
  - Shell script for manual testing of eligibility modes
  - Pytest integration tests with parameterized test cases

### Changed
- Enhanced `verify_upgrade_eligibility` endpoint to match real system schema
- Improved test coverage for eligibility verification
- Updated system configuration model with eligibility status control

### Fixed
- Consistent response format for eligibility verification
- Proper error handling in system configuration updates

## [0.2.0] - 2025-03-15

### Added
- Initial implementation of upgrade functionality
- Basic authentication with CSRF protection
- API endpoints for system information
- Software version management
- Upgrade session creation and monitoring

## [0.1.0] - 2025-03-01

### Added
- Project initialization
- FastAPI server setup
- Basic project structure
