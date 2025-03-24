# Dell Unisphere Mock API - Comprehensive Test Report
Generated on: Mon Mar 24 08:08:23 AM EET 2025


## Checking if API is running
API is running at http://localhost:8000

## Running General API Tests
This section tests various API endpoints to ensure they are functioning correctly

## Getting Basic System Info
### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/basicSystemInfo/instances" -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/basicSystemInfo/instances?per_page=2000",
    "updated": "2025-03-24T08:08:23.301Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/basicSystemInfo",
            "content": {
                "id": "0",
                "model": "Unity 380F",
                "name": "CKM01204905476",
                "softwareVersion": "5.3.0",
                "softwareFullVersion": "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)",
                "apiVersion": "13.0",
                "earliestApiVersion": "4.0"
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/0"
                }
            ],
            "updated": "2025-03-24T08:08:23.301Z"
        }
    ]
}
```

## Getting Login Session Info
### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
Got CSRF token: a694e19e-4e7d-438d-bc3d-4e0c794c5704
### Response
```json
{
    "@base": "http://localhost:8000/api/instances/loginSessionInfo",
    "content": {
        "domain": "local",
        "idleTimeout": 3600,
        "roles": [
            {
                "id": "administrator"
            }
        ],
        "user": {
            "id": "user_admin"
        },
        "id": "a694e19e-4e7d-438d-bc3d-4e0c794c5704",
        "isPasswordChangeRequired": false
    },
    "links": [
        {
            "rel": "self",
            "href": "/a694e19e-4e7d-438d-bc3d-4e0c794c5704"
        }
    ],
    "updated": "2025-03-24T08:08:23.361Z"
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
    "updated": "2025-03-24T08:08:23.527Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/user",
            "content": {
                "id": "user_admin"
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/0"
                }
            ],
            "updated": "2025-03-24T08:08:23.527Z"
        },
        {
            "@base": "http://localhost:8000/api/instances/user",
            "content": {
                "id": "user_user"
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/1"
                }
            ],
            "updated": "2025-03-24T08:08:23.527Z"
        },
        {
            "@base": "http://localhost:8000/api/instances/user",
            "content": {
                "id": "user_diagnose"
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/2"
                }
            ],
            "updated": "2025-03-24T08:08:23.527Z"
        }
    ]
}
```

## Getting Installed Software Versions
### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/installedSoftwareVersion/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/installedSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-24T08:08:23.603Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": []
}
```

## Getting Specific Installed Software Version
### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/instances/installedSoftwareVersion/0" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "detail": "Installed software version not found"
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
    "updated": "2025-03-24T08:08:23.733Z",
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
    "updated": "2025-03-24T08:08:23.795Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": []
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
    "updated": "2025-03-24T08:08:23.873Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": []
}
```

## Verifying Upgrade Eligibility
### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 0c2e8e3a-e5d1-4ec9-a1f4-0da94407b77a"
```
### Response
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body"
            ],
            "msg": "Field required",
            "input": null
        }
    ]
}
```

## Testing Complete Upgrade Flow
This test will create an upgrade session and monitor it until completion
Got CSRF token: ad4e666c-8c89-4460-83cf-bb54b1de9770
### Step 1: Creating dummy upgrade file

## Creating dummy upgrade file
Creating a 10MB dummy file for testing software upload
```
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.040995 s, 256 MB/s
File created: ./tests/scripts/test_results/test_upgrade.bin (10MB)
```
### Step 2: Uploading software package
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: ad4e666c-8c89-4460-83cf-bb54b1de9770" \
        -F "file=@./tests/scripts/test_results/test_upgrade.bin"
```
Response:
```json
{
    "id": "file_55284666-0118-4a54-bc4e-76903dcea37f",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```
Uploaded software package: file_55284666-0118-4a54-bc4e-76903dcea37f
### Step 3: Preparing software
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: ad4e666c-8c89-4460-83cf-bb54b1de9770" \
        -H "Content-Type: application/json" \
        -d '{"filename":"file_55284666-0118-4a54-bc4e-76903dcea37f"}'
```
Response:
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-24T08:08:24.336Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/candidateSoftwareVersion",
            "content": {
                "status": "PREPARED",
                "filename": "file_55284666-0118-4a54-bc4e-76903dcea37f"
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/0"
                }
            ],
            "updated": "2025-03-24T08:08:24.336Z"
        }
    ]
}
```
### Step 4: Getting candidate software versions
Request:
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances"         -u "admin:Password123!"         -b cookie.jar         -H "X-EMC-REST-CLIENT: true"         -H "EMC-CSRF-TOKEN: ad4e666c-8c89-4460-83cf-bb54b1de9770"
```
Response:
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-24T08:08:24.396Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/candidateSoftwareVersion",
            "content": {
                "id": "file_55284666-0118-4a54-bc4e-76903dcea37f",
                "version": "5.4.0.0",
                "fullVersion": "Unity test_upgrade.bin",
                "revision": 0,
                "releaseDate": "2025-03-24T08:08:24.190066",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/file_55284666-0118-4a54-bc4e-76903dcea37f"
                }
            ],
            "updated": "2025-03-24T08:08:24.396Z"
        }
    ]
}
```
Found candidate ID: file_55284666-0118-4a54-bc4e-76903dcea37f
### Step 2: Creating upgrade session
**Error:** Failed to extract session ID
