# API Test Report
Generated: Thu Mar 13 10:08:15 AM EET 2025

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
Got CSRF token: 89eaf445-2660-4937-a341-032b98f76631
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
    "id": "89eaf445-2660-4937-a341-032b98f76631",
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
                "creationTime": "2025-02-11T10:08:08.693351",
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
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 89eaf445-2660-4937-a341-032b98f76631"
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
10485760 bytes (10 MB, 10 MiB) copied, 0.0289619 s, 362 MB/s
File created: /home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin (10MB)
```

## Uploading Software Package

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" -u "admin:Password123!" -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 89eaf445-2660-4937-a341-032b98f76631" -F "file=@/home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin"
```
### Response
```json
{
    "id": "file_736009d9-b092-41ac-8dbc-9086ff3f6d5d",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```

## prepare_software.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Preparing Software -d '-H "EMC-CSRF-TOKEN: 89eaf445-2660-4937-a341-032b98f76631"'
```
### Response
```json
{
    "id": "candidate_7775bed9-dac4-4ec4-8d2b-e4c030c183c1",
    "status": "SUCCESS"
}
```

## create_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Creating Upgrade Session -d '-H "EMC-CSRF-TOKEN: 89eaf445-2660-4937-a341-032b98f76631"'
```
### Response
```json
{
    "id": "Upgrade_048d7479-964d-4802-8724-5fd412155cad"
}
```

## resume_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Resuming Upgrade Session -d '-H "EMC-CSRF-TOKEN: 89eaf445-2660-4937-a341-032b98f76631"'
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
curl -s -k -L -X POST "http://localhost:8000/api/types/loginSessionInfo/action/logout" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Logging Out -d '-H "EMC-CSRF-TOKEN: 89eaf445-2660-4937-a341-032b98f76631"'
```
### Response
```json
{
    "message": "Logged out successfully"
}
```

## Test Summary
