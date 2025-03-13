# API Test Report
Generated: Thu Mar 13 11:15:10 AM EET 2025

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
    "entries": [
        {
            "content": {
                "id": "0",
                "model": "Unity 380F",
                "name": "CKM01204905476",
                "softwareVersion": "5.3.0",
                "softwareFullVersion": "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)",
                "apiVersion": "13.0",
                "earliestApiVersion": "4.0"
            },
            "id": "basicSystemInfo_0"
        }
    ],
    "base": "http://localhost:8000/api"
}
```

## Getting Login Session Info

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
Got CSRF token: d2c5e39f-8aa2-4941-845c-8374b21e52c9
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
    "id": "d2c5e39f-8aa2-4941-845c-8374b21e52c9",
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
    "entries": [
        {
            "content": {
                "id": "user_admin"
            },
            "id": "user_0"
        },
        {
            "content": {
                "id": "user_user"
            },
            "id": "user_1"
        },
        {
            "content": {
                "id": "user_diagnose"
            },
            "id": "user_2"
        }
    ],
    "base": "http://localhost:8000/api"
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
    "entries": [
        {
            "content": {
                "id": "0",
                "version": "5.3.0",
                "revision": 120,
                "releaseDate": "2025-03-13T11:04:40.663380",
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
                        "releaseDate": "2025-03-13T11:04:40.663383",
                        "upgradedeDriveCount": 24,
                        "estimatedTime": 30,
                        "isNewVersion": false
                    }
                ]
            },
            "id": "installedSoftwareVersion_0"
        }
    ],
    "base": "http://localhost:8000/api"
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
    "content": {
        "id": "0",
        "version": "5.3.0",
        "revision": 120,
        "releaseDate": "2025-03-13T11:04:40.663380",
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
                "releaseDate": "2025-03-13T11:04:40.663383",
                "upgradedeDriveCount": 24,
                "estimatedTime": 30,
                "isNewVersion": false
            }
        ]
    },
    "id": "0"
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
    "entries": [],
    "base": "http://localhost:8000/api"
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
    "entries": [
        {
            "content": {
                "id": "Upgrade_4.3.0.1499782821",
                "type": 0,
                "candidate": "candidate_default",
                "caption": "Upgrade_4.3.0.1499782821",
                "status": 2,
                "messages": [],
                "creationTime": "2025-02-11T11:04:40.663365",
                "elapsedTime": "PT2H30M",
                "percentComplete": 100,
                "tasks": []
            },
            "id": "upgradeSession_0"
        }
    ],
    "base": "http://localhost:8000/api"
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
    "entries": [
        {
            "content": {
                "status": 2,
                "caption": "Upgrade_4.3.0.1499782821",
                "percentComplete": 100,
                "tasks": []
            },
            "id": "upgradeSession_0"
        }
    ],
    "base": "http://localhost:8000/api"
}
```

## Verifying Upgrade Eligibility

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: d2c5e39f-8aa2-4941-845c-8374b21e52c9"
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
10485760 bytes (10 MB, 10 MiB) copied, 0.0262606 s, 399 MB/s
File created: /home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin (10MB)
```

## Uploading Software Package

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" -u "admin:Password123!" -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: d2c5e39f-8aa2-4941-845c-8374b21e52c9" -F "file=@/home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin"
```
### Response
```json
{
    "id": "file_e700ccd5-b548-4a08-a19d-f140f71b4761",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```

## prepare_software.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Preparing Software -d '-H "EMC-CSRF-TOKEN: d2c5e39f-8aa2-4941-845c-8374b21e52c9"'
```
### Response
```json
{
    "id": "candidate_a65f359d-140a-47c6-a80b-07f8e5f9318c",
    "status": "SUCCESS"
}
```

## create_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Creating Upgrade Session -d '-H "EMC-CSRF-TOKEN: d2c5e39f-8aa2-4941-845c-8374b21e52c9"'
```
### Response
```json
{
    "id": "Upgrade_a5bbe0cf-d40a-4a33-890b-cc76494fddf1"
}
```

## resume_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Resuming Upgrade Session -d '-H "EMC-CSRF-TOKEN: d2c5e39f-8aa2-4941-845c-8374b21e52c9"'
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
curl -s -k -L -X POST "http://localhost:8000/api/types/loginSessionInfo/action/logout" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Logging Out -d '-H "EMC-CSRF-TOKEN: d2c5e39f-8aa2-4941-845c-8374b21e52c9"'
```
### Response
```json
{
    "message": "Logged out successfully"
}
```

## Test Summary
