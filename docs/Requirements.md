# Dell Unisphere Mock API Requirements

This document details the requirements for implementing the Dell Unisphere mock API for the purposes of development and testing of a software upgrade facility for Unity storage systems. The mock API provides a realistic simulation of the Dell Unisphere API to enable development and testing without requiring access to actual Unity storage hardware.

## System Requirements

### Functional Requirements

The system must implement the following requirements:

#### API Structure and Response Format

1. Every resource type must have a corresponding collection endpoint and instance endpoint.
   - Collection endpoint: `/api/types/{resource_type}/instances`
   - Instance endpoint: `/api/instances/{resource_type}/{id}`
   - Special case for file uploads: `/upload/files/types/{resource_type}`

2. Every resource collection response must be wrapped in the following structure:

```json
{
    "@base": "https://{host}/api/types/{resource_type}/instances?per_page=2000",
    "updated": "{timestamp}",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "https://{host}/api/instances/{resource_type}",
            "updated": "{timestamp}",
            "links": [
                {
                    "rel": "self",
                    "href": "/{id}"
                }
            ],
            "content": {
                "id": "{id}",
                // Additional resource-specific fields
            }
        }
    ]
}
```

3. Every resource instance response must be wrapped in the following structure:

```json
{
    "@base": "https://{host}/api/instances/{resource_type}",
    "updated": "{timestamp}",
    "links": [
        {
            "rel": "self",
            "href": "/{id}"
        }
    ],
    "content": {
        "id": "{id}",
        // Additional resource-specific fields
    }
}
```

#### Authentication and Security

4. The API must support HTTP Basic Authentication with the following header:

```http
Authorization: Basic {base64_encoded_credentials}
```

where `{base64_encoded_credentials}` is a base64 encoded `username:password` pair.

5. Every endpoint requires the following header:

```http
X-EMC-REST-CLIENT: true
```

6. Every successful GET endpoint must return a valid cookie and CSRF token in the response headers:

```http
Set-Cookie: mod_sec_emc={cookie_value}; path=/; secure; HttpOnly
EMC-CSRF-TOKEN: {csrf_token}
```

7. Every POST, PUT, and DELETE endpoint requires a valid CSRF token in the request header:

```http
EMC-CSRF-TOKEN: {csrf_token}
```

8. Every POST, PUT, and DELETE endpoint requires a valid session cookie in the request header:

```http
Cookie: mod_sec_emc={cookie_value}
```

9. Once a valid session cookie and CSRF token are received, they must be used for all subsequent requests.

10. The API must implement CSRF protection with exemptions for login and file upload endpoints.

#### Response Requirements

11. Every endpoint must return a valid JSON response.

12. Every endpoint must return an appropriate HTTP status code:
   - 200 OK: Successful GET, PUT, or POST request
   - 201 Created: Successful resource creation
   - 202 Accepted: Request accepted for processing (async operations)
   - 204 No Content: Successful DELETE request
   - 400 Bad Request: Invalid request parameters
   - 401 Unauthorized: Missing or invalid authentication
   - 403 Forbidden: Insufficient permissions
   - 404 Not Found: Resource not found
   - 500 Internal Server Error: Server-side error

13. Error responses must follow this format:

```json
{
    "error": {
        "errorCode": {numeric_code},
        "httpStatusCode": {http_status_code},
        "messages": [
            {
                "en-US": "{error_message}"
            }
        ],
        "created": "{timestamp}"
    }
}
```

### Resource Type Requirements

#### Basic System Info

14. The API must implement the `basicSystemInfo` resource type with the following attributes:
   - `id`: String
   - `model`: String
   - `name`: String
   - `softwareVersion`: String
   - `softwareFullVersion`: String
   - `apiVersion`: String
   - `earliestApiVersion`: String

15. The `basicSystemInfo` endpoint must be accessible without authentication.

#### Login Session Info

16. The API must implement the `loginSessionInfo` resource type with the following attributes:
   - `id`: String
   - `roles`: Array of role objects
   - `domain`: String
   - `user`: User object reference
   - `idleTimeout`: Integer (seconds)
   - `isPasswordChangeRequired`: Boolean

17. The API must implement a logout operation for the `loginSessionInfo` resource type.

#### User

18. The API must implement the `user` resource type with appropriate attributes.

19. The API must support Create, Modify, and Delete operations for the `user` resource type.

#### Candidate Software Version

20. The API must implement the `candidateSoftwareVersion` resource type with appropriate attributes.

21. The API must implement a Prepare operation for the `candidateSoftwareVersion` resource type.

22. The candidate software versions store must be empty upon initialization.

23. The API must enforce a single-candidate policy for software upgrades:
    - Only one candidate software version can exist in the system at any time
    - When a new candidate is uploaded, it must replace any existing candidate
    - After a successful upgrade, the candidate software version must be automatically removed
    - The system must handle concurrent upload attempts appropriately to maintain the single-candidate invariant

    **Rationale**: This requirement ensures that the mock API accurately reflects the behavior of the actual Dell Unisphere system, where only one upgrade candidate can exist at a time. This prevents confusion about which version would be used for an upgrade and simplifies the upgrade workflow.

#### Software Upgrade Session

23. The API must implement the `softwareUpgradeSession` resource type with the following embedded resource types:
   - `upgradeMessage`
   - `upgradeTask`

   **Rationale**: These embedded resource types are essential for providing detailed information about upgrade progress and any issues encountered during the upgrade process. This structure mirrors the actual Dell Unisphere API, ensuring that client applications can be tested against realistic data structures.

24. The API must implement the following operations for the `softwareUpgradeSession` resource type:
   - Create: Allows the creation of a new upgrade session
   - VerifyUpgradeEligibility: Validates that the system can be upgraded
   - Resume: Continues a paused upgrade session

   **Rationale**: These operations represent the core functionality needed to manage the software upgrade lifecycle. The ability to create, verify, and resume upgrade sessions is critical for testing the complete upgrade workflow, including handling interruptions and validations.

25. The API must implement the following enumerations:
   - `UpgradeSessionTypeEnum`: Defines the type of upgrade (e.g., UPGRADE, INSTALL)
   - `UpgradeStatusEnum`: Tracks the status of the upgrade (e.g., PENDING, IN_PROGRESS, COMPLETED)
   - `UpgradeTypeEnum`: Specifies what is being upgraded (e.g., SOFTWARE, LANGUAGE_PACK)

   **Rationale**: These enumerations provide standardized values for critical upgrade parameters, ensuring consistency in the API and enabling proper state management throughout the upgrade process. They allow client applications to make decisions based on well-defined states.

26. The `create_upgrade_session` endpoint must check for existing candidate software versions before creating a session.

   **Rationale**: This validation prevents the creation of invalid upgrade sessions when no software is available to upgrade to, avoiding wasted resources and providing immediate feedback to users about prerequisites for upgrades.

27. The `resume_upgrade_session` endpoint must validate the session's existence and ensure it is in a paused state before resuming.

   **Rationale**: This validation maintains the integrity of the upgrade process by preventing attempts to resume non-existent or already completed/failed sessions, which could lead to unpredictable system behavior.

#### File Upload

28. The API must implement a file upload endpoint for candidate software versions:
   - `/upload/files/types/candidateSoftwareVersion`

   **Rationale**: A dedicated endpoint for file uploads provides a clear interface for clients to upload software packages, following the structure of the real Dell Unisphere API and ensuring compatibility with existing tools and workflows.

29. The file upload endpoint must accept multipart/form-data with a file field.

   **Rationale**: The multipart/form-data format is the standard for file uploads in HTTP applications, allowing binary data to be transferred efficiently along with metadata, ensuring compatibility with a wide range of client tools.

30. The `prepare_software` function must only create a candidate software version when a file is uploaded.

   **Rationale**: This requirement ensures data integrity by preventing the creation of invalid candidate software versions without corresponding files, maintaining a consistent relationship between uploaded files and software version records.

#### Installed Software Version

31. The API must implement the `installedSoftwareVersion` resource type with the following attributes:
   - `id`: String identifier for the installed software version
   - `version`: String representing the version number
   - `revision`: Integer representing the revision number
   - `releaseDate`: DateTime when the software was released
   - `fullVersion`: String with complete version information
   - `languages`: Array of installed language packs
   - `hotFixes`: Array of installed hotfixes
   - `packageVersions`: Array of installed package versions
   - `driveFirmware`: Array of drive firmware packages

   **Rationale**: These attributes provide comprehensive information about the currently installed software, which is essential for determining upgrade eligibility and tracking the system's software state. This information helps users make informed decisions about whether and when to upgrade.

32. The API must implement the following embedded resource types for `installedSoftwareVersion`:
   - `firmwarePackage`: Contains information about drive firmware packages
   - `installedSoftwareVersionLanguage`: Contains information about installed language packs
   - `installedSoftwareVersionPackages`: Contains information about installed software packages

   **Rationale**: These embedded resource types provide structured access to detailed components of the installed software, enabling fine-grained queries and updates. This structure mirrors the actual Dell Unisphere API, ensuring that client applications can be tested against realistic data structures.

33. The API must support the following operations for the `installedSoftwareVersion` resource type:
   - Collection query: Retrieve all installed software versions
   - Instance query: Retrieve a specific installed software version by ID

   **Rationale**: These operations allow clients to access both overview and detailed information about installed software, supporting different use cases from system monitoring to detailed analysis of specific versions.

### Non-Functional Requirements

34. The API must be implemented using FastAPI.

   **Rationale**: FastAPI provides a modern, high-performance framework with automatic OpenAPI documentation generation, type checking, and asynchronous support, making it ideal for creating a mock API that can handle concurrent requests efficiently.

35. The API must use Pydantic for data validation and serialization.

   **Rationale**: Pydantic provides robust data validation, serialization, and documentation capabilities that integrate seamlessly with FastAPI, ensuring that API inputs and outputs conform to expected schemas and reducing the risk of data-related errors.

36. The API must include a Swagger UI self-documentation page with authentication support.

   **Rationale**: Integrated API documentation through Swagger UI provides developers with an interactive way to explore and test the API, reducing the learning curve and improving developer productivity. Authentication support in the documentation ensures that all API features can be tested directly from the UI.

37. The API must include a test script to verify functionality.

   **Rationale**: An automated test script provides a quick way to verify that the entire API is functioning correctly, serving as both a validation tool and a demonstration of how to use the API.

38. The API must closely mimic the behavior of the real Dell Unisphere API.

   **Rationale**: By accurately simulating the behavior of the real API, the mock API enables developers to build and test applications that will work seamlessly with actual Dell Unisphere systems, reducing integration issues when moving to production environments.

39. The API must provide robust error handling with clear feedback when operations fail.

   **Rationale**: Detailed error messages help developers quickly identify and fix issues in their client applications, improving the development experience and reducing debugging time. Consistent error formats also allow client applications to handle errors programmatically.

40. The API must be accessible via HTTPS.

   **Rationale**: HTTPS support ensures secure communication between clients and the API, protecting sensitive information and mimicking the security requirements of the real Dell Unisphere API, which is critical for testing authentication and authorization flows.

41. The API must support concurrent requests.

   **Rationale**: Support for concurrent requests allows the API to handle multiple clients simultaneously, providing a more realistic testing environment and ensuring that client applications can be tested for race conditions and concurrency issues.

42. The API must maintain session state between requests.

   **Rationale**: Session state management is crucial for implementing authentication and authorization features that persist across multiple requests, enabling realistic testing of multi-step workflows and user sessions.

43. The API must be containerizable for easy deployment.

   **Rationale**: Container support simplifies deployment across different environments, ensures consistency between development and testing setups, and allows the API to be easily integrated into CI/CD pipelines for automated testing.
