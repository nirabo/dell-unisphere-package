# Dell Unisphere Mock API Architecture

This document describes the software architecture of the Dell Unisphere Mock API project, including its components, design patterns, data flow, and deployment considerations.

## Table of Contents

1. [Architectural Overview](#architectural-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Authentication and Security](#authentication-and-security)
5. [API Design](#api-design)
6. [Persistence Layer](#persistence-layer)
7. [Error Handling](#error-handling)
8. [Testing Architecture](#testing-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Future Architectural Considerations](#future-architectural-considerations)

## Architectural Overview

The Dell Unisphere Mock API is built using a layered architecture pattern with FastAPI as the web framework. The application follows a clean architecture approach, separating concerns into distinct layers:

1. **Presentation Layer**: API routes and endpoints
2. **Business Logic Layer**: Controllers and services
3. **Data Access Layer**: Models and repositories
4. **Domain Layer**: Core business entities and schemas

### High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                      Client Applications                        │
└───────────────────────────────┬────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                         FastAPI Application                     │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   Middleware    │───▶│     Routers     │───▶│  Controllers  │ │
│  │  (Auth, CSRF)   │    │  (API Endpoints)│    │(Business Logic│ │
│  └─────────────────┘    └─────────────────┘    └──────────────┘ │
│                                                        │        │
│                                                        ▼        │
│                                               ┌──────────────┐  │
│                                               │    Models    │  │
│                                               │  (Data Store)│  │
│                                               └──────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Presentation Layer

The presentation layer is responsible for handling HTTP requests and responses. It uses FastAPI's routing system to define API endpoints.

#### Key Components:

- **Routes**: Defined in `src/dell_unisphere_package/routes/`
  - `auth.py`: Authentication-related endpoints
  - `system.py`: System information endpoints
  - `software.py`: Software version and upgrade endpoints
  - `upload.py`: File upload endpoints
  - `user.py`: User management endpoints

- **Middleware**: Defined in `src/dell_unisphere_package/middleware/`
  - `authentication.py`: HTTP Basic Authentication middleware
  - `csrf.py`: CSRF protection middleware

### Business Logic Layer

The business logic layer contains the application's core functionality and business rules.

#### Key Components:

- **Controllers**: Defined in `src/dell_unisphere_package/controllers/`
  - `auth_controller.py`: Authentication logic
  - `system_controller.py`: System information logic
  - `software_controller.py`: Software version and upgrade logic
  - `upload_controller.py`: File upload logic
  - `user_controller.py`: User management logic

- **Services**: Defined in `src/dell_unisphere_package/services/`
  - `auth_service.py`: Authentication services
  - `software_service.py`: Software management services

### Data Access Layer

The data access layer is responsible for data persistence and retrieval.

#### Key Components:

- **Models**: Defined in `src/dell_unisphere_package/models/`
  - `user.py`: User data model
  - `system.py`: System information model
  - `software.py`: Software version models
  - `upgrade.py`: Upgrade session models

- **Repositories**: Defined in `src/dell_unisphere_package/repositories/`
  - `user_repository.py`: User data access
  - `software_repository.py`: Software data access

### Domain Layer

The domain layer defines the core business entities and data schemas.

#### Key Components:

- **Schemas**: Defined in `src/dell_unisphere_package/schemas/`
  - `user.py`: User-related schemas
  - `system.py`: System information schemas
  - `software.py`: Software version schemas
  - `upgrade.py`: Upgrade session schemas
  - `common.py`: Common response schemas

## Data Flow

The data flow through the application follows this general pattern:

1. Client sends HTTP request to an API endpoint
2. Middleware processes the request (authentication, CSRF protection)
3. Router receives the request and forwards it to the appropriate controller
4. Controller processes the request, using services as needed
5. Services interact with repositories to access data
6. Repositories retrieve or modify data in the models
7. Controller formats the response using schemas
8. Router returns the HTTP response to the client

### Sequence Diagram for a Typical Request

```
┌──────┐          ┌────────────┐          ┌──────────┐          ┌────────┐          ┌──────┐
│Client│          │Middleware   │          │Router    │          │Controller│          │Model │
└──┬───┘          └─────┬──────┘          └────┬─────┘          └────┬───┘          └──┬───┘
   │                    │                      │                     │                  │
   │ HTTP Request       │                      │                     │                  │
   │──────────────────▶│                      │                     │                  │
   │                    │                      │                     │                  │
   │                    │ Authenticated Request│                     │                  │
   │                    │─────────────────────▶                     │                  │
   │                    │                      │                     │                  │
   │                    │                      │ Process Request     │                  │
   │                    │                      │────────────────────▶                  │
   │                    │                      │                     │                  │
   │                    │                      │                     │ Data Operation   │
   │                    │                      │                     │─────────────────▶
   │                    │                      │                     │                  │
   │                    │                      │                     │ Data Response    │
   │                    │                      │                     │◀─────────────────
   │                    │                      │                     │                  │
   │                    │                      │ Formatted Response  │                  │
   │                    │                      │◀────────────────────                  │
   │                    │                      │                     │                  │
   │ HTTP Response      │                      │                     │                  │
   │◀──────────────────                      │                     │                  │
   │                    │                      │                     │                  │
```

## Authentication and Security

The application implements multiple authentication mechanisms:

### HTTP Basic Authentication

- Implemented in the `get_current_user` function
- Uses username/password credentials
- Validates against stored user credentials

### Session-based Authentication with CSRF Protection

- Session management with secure cookies
- CSRF token generation and validation
- Token exemptions for specific endpoints (login, file upload)

### Security Components

- **Authentication Middleware**: Validates user credentials
- **CSRF Middleware**: Protects against cross-site request forgery
- **Password Hashing**: Secures stored passwords
- **Custom OpenAPI Schema**: Documents security requirements

## API Design

The API is designed to mimic the Dell EMC Unisphere REST API for Unity storage systems.

### API Structure

- RESTful design principles
- Resource-based URL structure
- Standard HTTP methods (GET, POST, PUT, DELETE)
- JSON response format

### Response Format

All API responses follow a consistent format:

```json
{
  "content": {
    // Response data
  },
  "error": {
    "errorCode": 0,
    "httpStatusCode": 200,
    "messages": []
  }
}
```

### API Versioning

- Version information included in system endpoints
- Version compatibility checks in upgrade endpoints

## Persistence Layer

The application uses in-memory data stores for simplicity, with the option to extend to persistent storage.

### Data Storage

- **In-Memory Collections**: Python dictionaries and lists
- **File Storage**: For uploaded software packages

### Data Models

- **User Model**: Stores user credentials and permissions
- **System Model**: Stores system information
- **Software Model**: Stores software version information
- **Upgrade Model**: Stores upgrade session information

## Error Handling

The application implements a comprehensive error handling strategy:

### Error Types

- **Validation Errors**: Input validation failures
- **Authentication Errors**: Authentication failures
- **Authorization Errors**: Permission issues
- **Resource Errors**: Missing or invalid resources
- **System Errors**: Internal server errors

### Error Response Format

```json
{
  "content": {},
  "error": {
    "errorCode": 123,
    "httpStatusCode": 400,
    "messages": ["Error message details"]
  }
}
```

## Testing Architecture

The testing architecture follows the test pyramid approach:

### Test Layers

1. **Unit Tests**: Test individual components in isolation
   - Located in `tests/unit/`
   - Focus on controllers, services, and utilities

2. **Integration Tests**: Test component interactions
   - Located in `tests/integration/`
   - Focus on API endpoints and data flow

3. **End-to-End Tests**: Test complete workflows
   - Located in `tests/e2e/`
   - Focus on user scenarios and use cases

### Test Infrastructure

- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **Test Fixtures**: Reusable test data and setups
- **Test Scripts**: Automated test execution

## Deployment Architecture

The application is designed for flexible deployment options:

### Development Environment

- Local development server
- In-memory data storage
- Debug mode enabled

### Production Environment

- ASGI server (Uvicorn)
- Optional reverse proxy (Nginx)
- Environment variable configuration

### CI/CD Pipeline

- GitHub Actions workflows
- Automated testing
- Package building and publishing
- Dependency management with astral uv and pip

## Future Architectural Considerations

### Scalability Enhancements

- Database integration for persistent storage
- Containerization with Docker
- Kubernetes orchestration
- Horizontal scaling capabilities

### Security Enhancements

- OAuth2 authentication
- Role-based access control (RBAC)
- API rate limiting
- Advanced logging and monitoring

### Feature Enhancements

- Additional Dell Unisphere API endpoints
- Real-time notifications
- Asynchronous task processing
- Event-driven architecture

---

This architecture document provides a comprehensive overview of the Dell Unisphere Mock API project's design and implementation. It serves as a guide for understanding the current architecture and planning future enhancements.
