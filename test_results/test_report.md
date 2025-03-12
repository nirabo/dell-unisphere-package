# API Test Report
Generated: Wed Mar 12 05:20:24 PM EET 2025

---


## Checking if API is running

API is running at http://localhost:8000

## Getting Basic System Info

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/basicSystemInfo/instances" -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/basicSystemInfo/instances?per_page=2000",
    "updated": "2025-03-12T17:20:24.735441Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/basicSystemInfo",
            "updated": "2025-03-12T17:20:24.735441Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/0"
                }
            ],
            "content": {
                "id": "0"
            }
        }
    ]
}
```

## Getting Login Session Info

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
Got CSRF token: 0HqiSO4vn0xEvn0lT2aXnkoLO-BhlA3RZqcAR-a3TgI
### Response
```json
{
    "@base": "http://localhost:8000/api/types/loginSessionInfo/instances?per_page=2000",
    "updated": "2025-03-12T17:20:24.813806Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/loginSessionInfo",
            "updated": "2025-03-12T17:20:24.813806Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/user"
                }
            ],
            "content": {
                "id": "user"
            }
        }
    ]
}
```

## Getting Auth Token

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/auth" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "detail": "Not Found"
}
```

## Getting User Info

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/user/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/user/instances?per_page=2000",
    "updated": "2025-03-12T17:20:24.957742Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/user",
            "updated": "2025-03-12T17:20:24.957742Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/user_admin"
                }
            ],
            "content": {
                "id": "user_admin"
            }
        },
        {
            "@base": "http://localhost:8000/api/instances/user",
            "updated": "2025-03-12T17:20:24.957742Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/user_user"
                }
            ],
            "content": {
                "id": "user_user"
            }
        },
        {
            "@base": "http://localhost:8000/api/instances/user",
            "updated": "2025-03-12T17:20:24.957742Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/user_diagnose"
                }
            ],
            "content": {
                "id": "user_diagnose"
            }
        }
    ]
}
```

## Getting Candidate Software Versions

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-12T17:20:25.042223Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": []
}
```

## Getting Upgrade Sessions

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/upgradeSession/instances?per_page=2000",
    "updated": "2025-03-12T17:20:25.125687Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/upgradeSession",
            "updated": "2025-03-12T17:20:25.125687Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/Upgrade_4.3.0.1499782821"
                }
            ],
            "content": {
                "id": "Upgrade_4.3.0.1499782821"
            }
        }
    ]
}
```

## Getting Upgrade Sessions with Fields

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/upgradeSession/instances?fields=status,caption,percentComplete,tasks" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/upgradeSession/instances?per_page=2000",
    "updated": "2025-03-12T17:20:25.185368Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/upgradeSession",
            "updated": "2025-03-12T17:20:25.185368Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/Upgrade_4.3.0.1499782821"
                }
            ],
            "content": {
                "id": "Upgrade_4.3.0.1499782821"
            }
        }
    ]
}
```

## Verifying Upgrade Eligibility

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 0HqiSO4vn0xEvn0lT2aXnkoLO-BhlA3RZqcAR-a3TgI"
```
### Response
```json
{
    "isEligible": true,
    "messages": []
}
```

## Creating dummy upgrade file

## Creating dummy upgrade file
Creating a 10MB dummy file for testing software upload
```
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0417487 s, 251 MB/s
File created: test_upgrade.bin (10MB)
```

## Uploading Software Package

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" -u "admin:Password123!" -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 0HqiSO4vn0xEvn0lT2aXnkoLO-BhlA3RZqcAR-a3TgI" -F "file=@test_upgrade.bin"
```
### Response
```json
{
    "id": "file_1ad3c17f-016e-4530-a20a-744776d3c0e4",
    "filename": "test_upgrade.bin",
    "status": "UPLOADED"
}
```

## prepare_software.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Preparing Software -d '-H "EMC-CSRF-TOKEN: 0HqiSO4vn0xEvn0lT2aXnkoLO-BhlA3RZqcAR-a3TgI"'
```
### Response
```json
{
    "error": {
        "errorCode": 131149829,
        "httpStatusCode": 403,
        "messages": [
            {
                "en-US": "Invalid CSRF token"
            }
        ],
        "created": "2025-03-12T17:20:25.538739Z"
    }
}
```

## create_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Creating Upgrade Session -d '-H "EMC-CSRF-TOKEN: 0HqiSO4vn0xEvn0lT2aXnkoLO-BhlA3RZqcAR-a3TgI"'
```
### Response
```json
{
    "error": {
        "errorCode": 131149829,
        "httpStatusCode": 403,
        "messages": [
            {
                "en-US": "Invalid CSRF token"
            }
        ],
        "created": "2025-03-12T17:20:25.601624Z"
    }
}
```

## resume_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Resuming Upgrade Session -d '-H "EMC-CSRF-TOKEN: 0HqiSO4vn0xEvn0lT2aXnkoLO-BhlA3RZqcAR-a3TgI"'
```
### Response
```json
{
    "error": {
        "errorCode": 131149829,
        "httpStatusCode": 403,
        "messages": [
            {
                "en-US": "Invalid CSRF token"
            }
        ],
        "created": "2025-03-12T17:20:25.667151Z"
    }
}
```

## logout_response.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/loginSessionInfo/action/logout" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Logging Out -d '-H "EMC-CSRF-TOKEN: 0HqiSO4vn0xEvn0lT2aXnkoLO-BhlA3RZqcAR-a3TgI"'
```
### Response
```json
{
    "status": "LOGGED_OUT"
}
```

## Test Summary

