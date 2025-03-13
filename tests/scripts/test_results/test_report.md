# API Test Report
Generated: Thu Mar 13 11:31:25 AM EET 2025

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
    "updated": "2025-03-13T11:31:25.277Z",
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
            "updated": "2025-03-13T11:31:25.277Z"
        }
    ]
}
```

## Getting Login Session Info

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
Got CSRF token: 60c59121-a52a-4981-9025-2de6438dd084
### Response
```json
{
    "roles": [
        {
            "id": "administrator"
        }
    ],
    "domain": "local",
    "user": {
        "id": "user_admin"
    },
    "id": "60c59121-a52a-4981-9025-2de6438dd084",
    "idleTimeout": 3600,
    "isPasswordChangeRequired": false
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
    "updated": "2025-03-13T11:31:25.464Z",
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
            "updated": "2025-03-13T11:31:25.464Z"
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
            "updated": "2025-03-13T11:31:25.464Z"
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
            "updated": "2025-03-13T11:31:25.464Z"
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
    "updated": "2025-03-13T11:31:25.542Z",
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
                "releaseDate": "2025-03-13T11:31:14.303224",
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
                        "releaseDate": "2025-03-13T11:31:14.303226",
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
            "updated": "2025-03-13T11:31:25.542Z"
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
        "releaseDate": "2025-03-13T11:31:14.303224",
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
                "releaseDate": "2025-03-13T11:31:14.303226",
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
    "updated": "2025-03-13T11:31:25.608Z"
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
    "updated": "2025-03-13T11:31:25.677Z",
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
    "updated": "2025-03-13T11:31:25.746Z",
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
                "creationTime": "2025-02-11T11:31:14.303211",
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
            "updated": "2025-03-13T11:31:25.746Z"
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
    "updated": "2025-03-13T11:31:25.827Z",
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
            "updated": "2025-03-13T11:31:25.827Z"
        }
    ]
}
```

## Verifying Upgrade Eligibility

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 60c59121-a52a-4981-9025-2de6438dd084"
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
10485760 bytes (10 MB, 10 MiB) copied, 0.0471244 s, 223 MB/s
File created: /home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin (10MB)
```

## Uploading Software Package

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" -u "admin:Password123!" -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 60c59121-a52a-4981-9025-2de6438dd084" -F "file=@/home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin"
```
### Response
```json
{
    "id": "file_326c9837-f050-4f13-bf4a-a7b1e86fdb77",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```

## prepare_software.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Preparing Software -d '-H "EMC-CSRF-TOKEN: 60c59121-a52a-4981-9025-2de6438dd084"'
```
### Response
```json
{
    "id": "candidate_ce16ca88-73fb-4926-bb7d-dfb8e0583588",
    "status": "SUCCESS"
}
```

## create_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Creating Upgrade Session -d '-H "EMC-CSRF-TOKEN: 60c59121-a52a-4981-9025-2de6438dd084"'
```
### Response
```json
{
    "id": "Upgrade_dedb658a-5e89-4cc0-8d02-b3e637118a11"
}
```

## resume_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Resuming Upgrade Session -d '-H "EMC-CSRF-TOKEN: 60c59121-a52a-4981-9025-2de6438dd084"'
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
curl -s -k -L -X POST "http://localhost:8000/api/types/loginSessionInfo/action/logout" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Logging Out -d '-H "EMC-CSRF-TOKEN: 60c59121-a52a-4981-9025-2de6438dd084"'
```
### Response
```json
{
    "message": "Logged out successfully"
}
```

## Test Summary
