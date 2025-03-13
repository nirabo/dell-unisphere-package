# API Test Report
Generated: Thu Mar 13 09:39:00 AM EET 2025

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
Got CSRF token: dd2acd94-b726-4a8f-8557-ffcc4be39904
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
    "id": "dd2acd94-b726-4a8f-8557-ffcc4be39904",
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

## Getting Candidate Software Versions

### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
### Response
```json
{
    "entries": [
        {
            "content": {
                "id": "candidate_default",
                "version": "5.4.0",
                "fullVersion": "Unity 5.4.0.0 (Release, Build 150, 2023-06-18 19:02:01, 5.4.0.0.5.150)",
                "revision": 150,
                "releaseDate": "2025-03-13T09:39:00.383081",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "id": "candidateSoftwareVersion_0"
        }
    ],
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
                "creationTime": "2025-02-11T09:38:55.933291",
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
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: dd2acd94-b726-4a8f-8557-ffcc4be39904"
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
10485760 bytes (10 MB, 10 MiB) copied, 0.0430455 s, 244 MB/s
File created: /home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin (10MB)
```

## Uploading Software Package

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" -u "admin:Password123!" -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: dd2acd94-b726-4a8f-8557-ffcc4be39904" -F "file=@/home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin"
```
### Response
```json
{
    "id": "file_8d0348fe-5666-4807-b9ad-53b02093cb35",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```

## prepare_software.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Preparing Software -d '-H "EMC-CSRF-TOKEN: dd2acd94-b726-4a8f-8557-ffcc4be39904"'
```
### Response
```json
{
    "id": "candidate_fa027c85-6f8c-4987-89f7-66210a64b82d",
    "status": "SUCCESS"
}
```

## create_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Creating Upgrade Session -d '-H "EMC-CSRF-TOKEN: dd2acd94-b726-4a8f-8557-ffcc4be39904"'
```
### Response
```json
{
    "id": "Upgrade_c51055d0-c5c3-4b96-8587-ac5fe5e18a10"
}
```

## resume_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Resuming Upgrade Session -d '-H "EMC-CSRF-TOKEN: dd2acd94-b726-4a8f-8557-ffcc4be39904"'
```
### Response
```json

```

## logout_response.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/loginSessionInfo/action/logout" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Logging Out -d '-H "EMC-CSRF-TOKEN: dd2acd94-b726-4a8f-8557-ffcc4be39904"'
```
### Response
```json
{
    "message": "Logged out successfully"
}
```

## Test Summary
