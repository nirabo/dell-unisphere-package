# API Test Report
Generated: Thu Mar 13 08:35:15 AM EET 2025

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
    "updated": "2025-03-13T08:35:15.183312Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/basicSystemInfo",
            "updated": "2025-03-13T08:35:15.183312Z",
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
Got CSRF token: 9jmP2-y9XDR-XEzGHT8KV_W7E5g0oz37h-dc06_E3dU
### Response
```json
{
    "@base": "http://localhost:8000/api/types/loginSessionInfo/instances?per_page=2000",
    "updated": "2025-03-13T08:35:15.252761Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/loginSessionInfo",
            "updated": "2025-03-13T08:35:15.252761Z",
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
    "updated": "2025-03-13T08:35:15.396332Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/user",
            "updated": "2025-03-13T08:35:15.396332Z",
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
            "updated": "2025-03-13T08:35:15.396332Z",
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
            "updated": "2025-03-13T08:35:15.396332Z",
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
    "updated": "2025-03-13T08:35:15.457393Z",
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
    "updated": "2025-03-13T08:35:15.517849Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/upgradeSession",
            "updated": "2025-03-13T08:35:15.517849Z",
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
    "updated": "2025-03-13T08:35:15.581382Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "http://localhost:8000/api/instances/upgradeSession",
            "updated": "2025-03-13T08:35:15.581382Z",
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
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 9jmP2-y9XDR-XEzGHT8KV_W7E5g0oz37h-dc06_E3dU"
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
10485760 bytes (10 MB, 10 MiB) copied, 0.0473281 s, 222 MB/s
File created: /home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin (10MB)
```

## Uploading Software Package

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" -u "admin:Password123!" -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 9jmP2-y9XDR-XEzGHT8KV_W7E5g0oz37h-dc06_E3dU" -F "file=@/home/lpetrov/projects/sandbox/work/dell-unisphere-package/tests/scripts/test_results/test_upgrade.bin"
```
### Response
```json
{
    "id": "file_e67b1949-d1d2-4c59-bfef-7a953e9e4ee8",
    "filename": "test_upgrade.bin",
    "status": "UPLOADED"
}
```

## prepare_software.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Preparing Software -d '-H "EMC-CSRF-TOKEN: 9jmP2-y9XDR-XEzGHT8KV_W7E5g0oz37h-dc06_E3dU"'
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
        "created": "2025-03-13T08:35:15.957995Z"
    }
}
```

## create_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Creating Upgrade Session -d '-H "EMC-CSRF-TOKEN: 9jmP2-y9XDR-XEzGHT8KV_W7E5g0oz37h-dc06_E3dU"'
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
        "created": "2025-03-13T08:35:16.032183Z"
    }
}
```

## resume_upgrade_session.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/instances/upgradeSession/Upgrade_5.3.0.120/action/resume" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Resuming Upgrade Session -d '-H "EMC-CSRF-TOKEN: 9jmP2-y9XDR-XEzGHT8KV_W7E5g0oz37h-dc06_E3dU"'
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
        "created": "2025-03-13T08:35:16.096939Z"
    }
}
```

## logout_response.json

### Request
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/loginSessionInfo/action/logout" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" Logging Out -d '-H "EMC-CSRF-TOKEN: 9jmP2-y9XDR-XEzGHT8KV_W7E5g0oz37h-dc06_E3dU"'
```
### Response
```json
{
    "status": "LOGGED_OUT"
}
```

## Test Summary
