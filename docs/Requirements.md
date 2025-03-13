# Requirements

This document details the requirements for implementing the Dell Unisphere mock API for the purposes of development and testing of a software upgrade facility for Unity storage systems.

## System Requirements

### Functional Requirements

The system must implement the following requirements:

1. Every resource type must have a corresponding collection endpoint and instance endpoint.
  - Instance endpoint: `/api/instances/{resource_type}`
  - exception: `/files/upload`

2. Every resource endpoint response is wrapped in the following structure:

```json
{
    "id": "<id>",
    "base": "<base>",
    "updated": "<updated>",
    "links": ["<links>"],
    "content": ["<content>"]
}
```

where:
- `<id>` is the unique identifier of the resource instance.
- `<base>` is the base URL of the resource instance.
- `<updated>` is the last update time of the resource instance.
- `<links>` is an array of links to related resources.
- `<content>` is the content of the resource instance.

3. Every endpoint requires the following headers:

```http
X-EMC-REST-CLIENT: true
Authorization: Bearer <token>
```

where `<token>` is a valid authentication token - base64 encoded `user:pass` pair.

4. Every successfull GET endpoint shall return a valid cookie and CSRF token

5. Every endpoint must return a valid JSON response.

6. Every endpoint must return a valid HTTP status code.

7. Every POST, PUT, and DELETE endpoint require a valid CSRF token

8. Every POST, PUT, and DELETE endpoint require a valid session cookie

9. Once a valid session cookie and CSRF token are received, they shall be used for all subsequent requests
