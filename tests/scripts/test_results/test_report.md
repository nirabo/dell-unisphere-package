# API Test Report
Generated: Sat Mar 15 12:07:50 PM EET 2025

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
    "updated": "2025-03-15T12:07:50.488Z",
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
            "updated": "2025-03-15T12:07:50.488Z"
        }
    ]
}
```

## Getting Login Session Info

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
Got CSRF token: e636d6c9-0148-40b6-a6e7-494a404148d2
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
        "id": "e636d6c9-0148-40b6-a6e7-494a404148d2",
        "isPasswordChangeRequired": false
    },
    "links": [
        {
            "rel": "self",
            "href": "/e636d6c9-0148-40b6-a6e7-494a404148d2"
        }
    ],
    "updated": "2025-03-15T12:07:50.554Z"
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
    "updated": "2025-03-15T12:07:50.721Z",
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
            "updated": "2025-03-15T12:07:50.721Z"
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
            "updated": "2025-03-15T12:07:50.721Z"
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
            "updated": "2025-03-15T12:07:50.721Z"
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
    "updated": "2025-03-15T12:07:50.797Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/installedSoftwareVersion",
            "content": {
                "id": "0",
                "version": "5.3.0",
                "revision": 120,
                "releaseDate": "2025-03-15T12:05:34.080526",
                "fullVersion": "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)",
                "languages": [
                    {
                        "name": "English",
                        "version": "5.3.0"
                    },
                    {
                        "name": "Chinese",
                        "version": "5.3.0"
                    }
                ],
                "hotFixes": [
                    "HF1",
                    "HF2"
                ],
                "packageVersions": [
                    {
                        "name": "Base",
                        "version": "5.3.0"
                    },
                    {
                        "name": "Management",
                        "version": "5.3.0"
                    }
                ],
                "driveFirmware": [
                    {
                        "name": "Drive Firmware Package 1",
                        "version": "1.2.3",
                        "releaseDate": "2025-03-15T12:05:34.080528",
                        "upgradedeDriveCount": 24,
                        "estimatedTime": 30,
                        "isNewVersion": false
                    }
                ]
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/0"
                }
            ],
            "updated": "2025-03-15T12:07:50.797Z"
        }
    ]
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
    "@base": "http://localhost:8000/api/instances/installedSoftwareVersion",
    "content": {
        "id": "0",
        "version": "5.3.0",
        "revision": 120,
        "releaseDate": "2025-03-15T12:05:34.080526",
        "fullVersion": "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)",
        "languages": [
            {
                "name": "English",
                "version": "5.3.0"
            },
            {
                "name": "Chinese",
                "version": "5.3.0"
            }
        ],
        "hotFixes": [
            "HF1",
            "HF2"
        ],
        "packageVersions": [
            {
                "name": "Base",
                "version": "5.3.0"
            },
            {
                "name": "Management",
                "version": "5.3.0"
            }
        ],
        "driveFirmware": [
            {
                "name": "Drive Firmware Package 1",
                "version": "1.2.3",
                "releaseDate": "2025-03-15T12:05:34.080528",
                "upgradedeDriveCount": 24,
                "estimatedTime": 30,
                "isNewVersion": false
            }
        ]
    },
    "links": [
        {
            "rel": "self",
            "href": "/0"
        }
    ],
    "updated": "2025-03-15T12:07:50.874Z"
}
```

## Testing Complete Upgrade Flow

## Testing Complete Upgrade Flow
This test will create an upgrade session and monitor it until completion
### Step 1: Getting candidate software versions
Request:
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances"         -u "admin:Password123!"         -b cookie.jar         -H "X-EMC-REST-CLIENT: true"         -H "EMC-CSRF-TOKEN: e636d6c9-0148-40b6-a6e7-494a404148d2"
```
Response:
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-15T12:07:50.944Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": []
}
```
**Error:** No candidate software versions found

## Getting Candidate Software Versions

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-15T12:07:51.011Z",
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
    "updated": "2025-03-15T12:07:51.084Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/upgradeSession",
            "content": {
                "id": "Upgrade_4.3.0.1499782821",
                "type": 0,
                "candidate": "candidate_default",
                "caption": "Upgrade_4.3.0.1499782821",
                "status": 2,
                "messages": [],
                "creationTime": "2025-02-13T12:05:34.080508",
                "elapsedTime": "PT2H30M",
                "percentComplete": 100,
                "tasks": []
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/Upgrade_4.3.0.1499782821"
                }
            ],
            "updated": "2025-03-15T12:07:51.084Z"
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
    "updated": "2025-03-15T12:07:51.146Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/upgradeSession",
            "content": {
                "status": 2,
                "caption": "Upgrade_4.3.0.1499782821",
                "percentComplete": 100,
                "tasks": []
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/0"
                }
            ],
            "updated": "2025-03-15T12:07:51.146Z"
        }
    ]
}
```

## Verifying Upgrade Eligibility

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: e636d6c9-0148-40b6-a6e7-494a404148d2"
```
### Response
```json
{
    "detail": "Not Found"
}
```

## Creating dummy upgrade file

## Creating dummy upgrade file
Creating a 10MB dummy file for testing software upload
```
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0450695 s, 233 MB/s
File created: /home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin (10MB)
```

## Uploading Software Package

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" -u "admin:Password123!" -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: e636d6c9-0148-40b6-a6e7-494a404148d2" -F "file=@/home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin"
```
### Response
```json
{
    "id": "file_818e5c4d-72d4-42dd-97c9-0d3f15d3165b",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```

## prepare_software.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Preparing Software -d '-H "EMC-CSRF-TOKEN: e636d6c9-0148-40b6-a6e7-494a404148d2"'
```
### Response
```json
{
    "id": "candidate_a2f05c44-9fe9-40b3-8e6f-621b086e0731",
    "status": "SUCCESS"
}
```

## create_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Creating Upgrade Session -d '-H "EMC-CSRF-TOKEN: e636d6c9-0148-40b6-a6e7-494a404148d2"'
```
### Response
```json
{
    "id": "Upgrade_5.4.0.0"
}
```

## resume_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Resuming Upgrade Session -d '-H "EMC-CSRF-TOKEN: e636d6c9-0148-40b6-a6e7-494a404148d2"'
```
### Response
```json
{
    "status": "SUCCESS"
}
```

## logout_response.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/loginSessionInfo/action/logout" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Logging Out -d '-H "EMC-CSRF-TOKEN: e636d6c9-0148-40b6-a6e7-494a404148d2"'
```
### Response
```json
{
    "message": "Logged out successfully"
}
```

## Test Summary
