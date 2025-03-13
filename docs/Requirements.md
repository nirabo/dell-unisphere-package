# Dell Unisphere Mock API Requirements

This document details the requirements for implementing the Dell Unisphere mock API for the purposes of development and testing of a software upgrade facility for Unity storage systems.

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

#### Software Upgrade Session

23. The API must implement the `softwareUpgradeSession` resource type with the following embedded resource types:
   - `upgradeMessage`
   - `upgradeTask`

24. The API must implement the following operations for the `softwareUpgradeSession` resource type:
   - Create
   - VerifyUpgradeEligibility
   - Resume

25. The API must implement the following enumerations:
   - `UpgradeSessionTypeEnum`
   - `UpgradeStatusEnum`
   - `UpgradeTypeEnum`

26. The `create_upgrade_session` endpoint must check for existing candidate software versions before creating a session.

27. The `resume_upgrade_session` endpoint must validate the session's existence and ensure it is in a paused state before resuming.

#### File Upload

28. The API must implement a file upload endpoint for candidate software versions:
   - `/upload/files/types/candidateSoftwareVersion`

29. The file upload endpoint must accept multipart/form-data with a file field.

30. The `prepare_software` function must only create a candidate software version when a file is uploaded.

### Non-Functional Requirements

31. The API must be implemented using FastAPI.

32. The API must use Pydantic for data validation and serialization.

33. The API must include a Swagger UI self-documentation page with authentication support.

34. The API must include a test script to verify functionality.

35. The API must closely mimic the behavior of the real Dell Unisphere API.

36. The API must provide robust error handling with clear feedback when operations fail.

37. The API must be accessible via HTTPS.

38. The API must support concurrent requests.

39. The API must maintain session state between requests.

40. The API must be containerizable for easy deployment.
