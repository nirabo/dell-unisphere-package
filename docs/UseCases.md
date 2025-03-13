# Dell Unisphere Mock API Use Cases

This document outlines the primary use cases for the Dell Unisphere Mock API, providing detailed workflows and interaction patterns for developers and testers. These use cases are derived from the API documentation and requirements.

## Table of Contents

- [Authentication and Session Management](#authentication-and-session-management)
- [System Information Retrieval](#system-information-retrieval)
- [Software Version Management](#software-version-management)
- [Software Upgrade Workflow](#software-upgrade-workflow)
- [User Management](#user-management)

## Authentication and Session Management

### UC-1: User Authentication

**Description**: A user authenticates with the API to establish a session.

**Actors**: Client Application, API Server

**Preconditions**:
- The API server is running
- The user has valid credentials

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: GET /api/types/loginSessionInfo/instances
    Note over Client,API: HTTP Basic Auth with credentials
    API->>Client: 200 OK with session info and cookies
    Note over Client,API: Client stores EMC-CSRF-TOKEN

    Client->>API: Subsequent API requests with token
    API->>Client: Protected resources
```

**Postconditions**:
- The user is authenticated
- The client has a valid session cookie and CSRF token
- The client can make authenticated requests

### UC-2: User Logout

**Description**: A user terminates their active session.

**Actors**: Client Application, API Server

**Preconditions**:
- The user has an active authenticated session

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: POST /api/types/loginSessionInfo/action/logout
    Note over Client,API: Includes session cookie and CSRF token
    API->>Client: 200 OK
    Note over API: Session is invalidated
```

**Postconditions**:
- The user's session is terminated
- The session cookie is invalidated

## System Information Retrieval

### UC-3: Retrieve Basic System Information

**Description**: A client retrieves basic information about the storage system without authentication.

**Actors**: Client Application, API Server

**Preconditions**:
- The API server is running

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: GET /api/types/basicSystemInfo/instances
    API->>Client: 200 OK with system information
    Note over Client: Client processes system info
```

**Postconditions**:
- The client has basic system information (model, name, software version)

## Software Version Management

### UC-4: List Installed Software Versions

**Description**: A user retrieves information about currently installed software.

**Actors**: Client Application, API Server

**Preconditions**:
- The user is authenticated

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: GET /api/types/installedSoftwareVersion/instances
    Note over Client,API: Includes authentication
    API->>Client: 200 OK with installed software versions

    Client->>API: GET /api/instances/installedSoftwareVersion/{id}
    Note over Client,API: Optional detailed query for specific version
    API->>Client: 200 OK with detailed version information
```

**Postconditions**:
- The client has information about installed software versions

### UC-5: List Candidate Software Versions

**Description**: A user retrieves information about software versions available for upgrade.

**Actors**: Client Application, API Server

**Preconditions**:
- The user is authenticated

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: GET /api/types/candidateSoftwareVersion/instances
    Note over Client,API: Includes authentication
    API->>Client: 200 OK with candidate software versions
```

**Postconditions**:
- The client has information about available software versions for upgrade

## Software Upgrade Workflow

### UC-6: Complete Software Upgrade Process

**Description**: A user uploads a new software package and performs a system upgrade.

**Actors**: Client Application, API Server

**Preconditions**:
- The user is authenticated with administrative privileges
- A new software package is available for upload

**Flow**:

```mermaid
flowchart TD
    A[Start] --> B[Upload Software Package]
    B --> C[Prepare Software]
    C --> D[Verify Upgrade Eligibility]
    D --> E{Eligible?}
    E -->|Yes| F[Create Upgrade Session]
    E -->|No| Z[End with Error]
    F --> G[Monitor Upgrade Progress]
    G --> H{Upgrade Paused?}
    H -->|Yes| I[Resume Upgrade]
    H -->|No| J[Wait for Completion]
    I --> J
    J --> K{Upgrade Complete?}
    K -->|Yes| Y[End Successfully]
    K -->|No| G
```

**Detailed Sequence**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: POST /upload/files/types/candidateSoftwareVersion
    Note over Client,API: Multipart form with file
    API->>Client: 200 OK with file info

    Client->>API: POST /api/types/candidateSoftwareVersion/action/prepare
    API->>Client: 200 OK

    Client->>API: POST /api/types/upgradeSession/action/verifyUpgradeEligibility
    API->>Client: 200 OK with eligibility status

    Client->>API: POST /api/types/upgradeSession/instances
    API->>Client: 200 OK with session info

    loop Until Complete
        Client->>API: GET /api/types/upgradeSession/instances
        API->>Client: 200 OK with session status

        alt If Paused
            Client->>API: POST /api/instances/upgradeSession/{id}/action/resume
            API->>Client: 200 OK
        end
    end
```

**Postconditions**:
- The new software is installed
- The system is running the updated software version

### UC-7: Upload Software Package

**Description**: A user uploads a new software package to the system.

**Actors**: Client Application, API Server

**Preconditions**:
- The user is authenticated with appropriate privileges
- The user has a valid software package file

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: POST /upload/files/types/candidateSoftwareVersion
    Note over Client,API: Multipart form with file
    API->>Client: 200 OK with file info

    Client->>API: POST /api/types/candidateSoftwareVersion/action/prepare
    API->>Client: 200 OK with candidate version info
```

**Postconditions**:
- The software package is uploaded and prepared
- A new candidate software version is available

## User Management

### UC-8: List Users

**Description**: An administrator retrieves information about system users.

**Actors**: Administrator, API Server

**Preconditions**:
- The administrator is authenticated

**Flow**:

```mermaid
sequenceDiagram
    participant Admin as Administrator
    participant API as Dell Unisphere API

    Admin->>API: GET /api/types/user/instances
    Note over Admin,API: Includes authentication
    API->>Admin: 200 OK with user information
```

**Postconditions**:
- The administrator has information about system users

## Integration Use Cases

### UC-9: Automated Upgrade Testing

**Description**: A CI/CD pipeline tests the complete upgrade workflow.

**Actors**: CI/CD System, API Server

**Preconditions**:
- The API server is running
- Test credentials are available
- Test software package is available

**Flow**:

```mermaid
flowchart LR
    A[CI/CD Trigger] --> B[Authentication]
    B --> C[Upload Package]
    C --> D[Create Upgrade Session]
    D --> E[Monitor Upgrade]
    E --> F[Verify Success]
    F --> G[Report Results]
```

**Postconditions**:
- The upgrade workflow is validated
- Test results are recorded

### UC-10: Client Application Development

**Description**: A developer uses the mock API to build and test a client application.

**Actors**: Developer, Client Application, API Server

**Preconditions**:
- The API server is running
- Development environment is set up

**Flow**:

```mermaid
flowchart TD
    A[Start Development] --> B[Connect to Mock API]
    B --> C[Implement Authentication]
    C --> D[Implement Core Features]
    D --> E[Test Error Handling]
    E --> F[Integration Testing]
    F --> G[Performance Testing]
    G --> H[Documentation]
```

**Postconditions**:
- The client application is developed and tested
- The application can interact with the real Dell Unisphere API

## Error Handling Use Cases

### UC-11: Handle Authentication Failures

**Description**: The system properly handles authentication failures.

**Actors**: Client Application, API Server

**Preconditions**:
- The API server is running

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: GET /api/types/loginSessionInfo/instances
    Note over Client,API: Invalid credentials
    API->>Client: 401 Unauthorized
    Note over Client: Client handles error

    Client->>API: GET /api/types/user/instances
    Note over Client,API: Missing authentication
    API->>Client: 401 Unauthorized
    Note over Client: Client handles error
```

**Postconditions**:
- The system properly rejects unauthorized access
- The client receives appropriate error messages

### UC-12: Handle Invalid Operations

**Description**: The system properly handles invalid operations.

**Actors**: Client Application, API Server

**Preconditions**:
- The user is authenticated

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API

    Client->>API: POST /api/types/upgradeSession/instances
    Note over Client,API: No candidate versions available
    API->>Client: 400 Bad Request
    Note over Client: Client handles error

    Client->>API: POST /api/instances/upgradeSession/{invalid_id}/action/resume
    API->>Client: 404 Not Found
    Note over Client: Client handles error
```

**Postconditions**:
- The system properly rejects invalid operations
- The client receives appropriate error messages

## Security Use Cases

### UC-13: CSRF Protection

**Description**: The system protects against Cross-Site Request Forgery attacks.

**Actors**: Client Application, API Server, Potential Attacker

**Preconditions**:
- The user is authenticated

**Flow**:

```mermaid
sequenceDiagram
    participant Client as Client Application
    participant API as Dell Unisphere API
    participant Attacker as Malicious Site

    Client->>API: GET /api/types/loginSessionInfo/instances
    API->>Client: 200 OK with CSRF token

    Attacker->>Client: Trick user into submitting form
    Client->>API: POST request without CSRF token
    API->>Client: 403 Forbidden
    Note over API: Request rejected
```

**Postconditions**:
- The system rejects requests without valid CSRF tokens
- The user is protected from CSRF attacks
