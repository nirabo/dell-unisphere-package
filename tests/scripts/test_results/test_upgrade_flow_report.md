# Dell Unisphere Mock API - Comprehensive Test Report
Generated on: Wed Mar 26 12:23:10 PM EET 2025


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
    "updated": "2025-03-26T12:23:10.814Z",
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
            "updated": "2025-03-26T12:23:10.814Z"
        }
    ]
}
```

## Getting Login Session Info
### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
Got CSRF token: 7a19c572-538d-4fb8-9bc2-b2d20f688957
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
        "id": "7a19c572-538d-4fb8-9bc2-b2d20f688957",
        "isPasswordChangeRequired": false
    },
    "links": [
        {
            "rel": "self",
            "href": "/7a19c572-538d-4fb8-9bc2-b2d20f688957"
        }
    ],
    "updated": "2025-03-26T12:23:10.875Z"
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
    "updated": "2025-03-26T12:23:11.074Z",
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
            "updated": "2025-03-26T12:23:11.074Z"
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
            "updated": "2025-03-26T12:23:11.074Z"
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
            "updated": "2025-03-26T12:23:11.074Z"
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
    "updated": "2025-03-26T12:23:11.149Z",
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
                "releaseDate": "2025-03-26T12:22:59.616940",
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
                        "releaseDate": "2025-03-26T12:22:59.616949",
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
            "updated": "2025-03-26T12:23:11.149Z"
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
        "releaseDate": "2025-03-26T12:22:59.616940",
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
                "releaseDate": "2025-03-26T12:22:59.616949",
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
    "updated": "2025-03-26T12:23:11.220Z"
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
    "updated": "2025-03-26T12:23:11.297Z",
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
    "updated": "2025-03-26T12:23:11.356Z",
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
    "updated": "2025-03-26T12:23:11.420Z",
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
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 06378f6d-1119-47ef-9d9b-b9aa03abd70e"
```
### Response
```json
{
    "updated": "2025-03-26T12:23:11.499864Z",
    "content": {
        "statusMessage": "",
        "overallStatus": false
    }
}
```

## Testing Complete Upgrade Flow
This test will create an upgrade session and monitor it until completion
Got CSRF token: d7bb04a3-0530-4f6a-965e-bedb361d4c73
### Step 1: Creating dummy upgrade file

## Creating dummy upgrade file
Creating a 10MB dummy file for testing software upload
```
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0434449 s, 241 MB/s
File created: ./tests/scripts/test_results/test_upgrade.bin (10MB)
```
### Step 2: Uploading software package
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: d7bb04a3-0530-4f6a-965e-bedb361d4c73" \
        -F "file=@./tests/scripts/test_results/test_upgrade.bin"
```
Response:
```json
{
    "id": "file_b0c7159f-b9c7-4636-b135-63cc4f2c42ac",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```
Uploaded software package: file_b0c7159f-b9c7-4636-b135-63cc4f2c42ac
### Step 3: Preparing software
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: d7bb04a3-0530-4f6a-965e-bedb361d4c73" \
        -H "Content-Type: application/json" \
        -d '{"filename":"file_b0c7159f-b9c7-4636-b135-63cc4f2c42ac"}'
```
Response:
```json
{
    "id": "candidate_36e4aa0f-08b9-4da8-a182-7bb7acb40bc3",
    "status": "SUCCESS"
}
```
### Step 4: Getting candidate software versions
Request:
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances"         -u "admin:Password123!"         -b cookie.jar         -H "X-EMC-REST-CLIENT: true"         -H "EMC-CSRF-TOKEN: d7bb04a3-0530-4f6a-965e-bedb361d4c73"
```
Response:
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-26T12:23:11.929Z",
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
                "id": "file_b0c7159f-b9c7-4636-b135-63cc4f2c42ac",
                "version": "5.4.0.0",
                "fullVersion": "Unity test_upgrade.bin",
                "revision": 0,
                "releaseDate": "2025-03-26T12:23:11.724639",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/file_b0c7159f-b9c7-4636-b135-63cc4f2c42ac"
                }
            ],
            "updated": "2025-03-26T12:23:11.929Z"
        },
        {
            "@base": "http://localhost:8000/api/instances/candidateSoftwareVersion",
            "content": {
                "id": "candidate_36e4aa0f-08b9-4da8-a182-7bb7acb40bc3",
                "version": "5.4.0",
                "fullVersion": "Unity 5.4.0.0 (Release, Build 150, 2023-06-18 19:02:01, 5.4.0.0.5.150)",
                "revision": 150,
                "releaseDate": "2025-03-26T12:23:11.870171",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/candidate_36e4aa0f-08b9-4da8-a182-7bb7acb40bc3"
                }
            ],
            "updated": "2025-03-26T12:23:11.929Z"
        }
    ]
}
```
Found candidate ID: file_b0c7159f-b9c7-4636-b135-63cc4f2c42ac
### Step 2: Creating upgrade session
### Step 3: Monitoring upgrade progress
Monitoring the upgrade session until completion

| Time | Status | Progress | Task States |
|------|--------|----------|------------|
| 12:23:12 | IN_PROGRESS | 0% | Preparing system: IN_PROGRESS,Performing health checks: PENDING,Preparing system software: PENDING,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:12
| Task | Status |
|------|--------|
| Preparing system | IN_PROGRESS |
| Performing health checks | PENDING |
| Preparing system software | PENDING |
| Waiting for reboot command | PENDING |
| Performing health checks | PENDING |
| Installing new software on peer SP | PENDING |
| Rebooting peer SP | PENDING |
| Restarting services on peer SP | PENDING |
| Installing new software on primary SP | PENDING |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:14 | IN_PROGRESS | 12% | Preparing system: COMPLETED,Performing health checks: IN_PROGRESS,Preparing system software: PENDING,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:14
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | IN_PROGRESS |
| Preparing system software | PENDING |
| Waiting for reboot command | PENDING |
| Performing health checks | PENDING |
| Installing new software on peer SP | PENDING |
| Rebooting peer SP | PENDING |
| Restarting services on peer SP | PENDING |
| Installing new software on primary SP | PENDING |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:16 | IN_PROGRESS | 18% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: IN_PROGRESS,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:16
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | IN_PROGRESS |
| Waiting for reboot command | PENDING |
| Performing health checks | PENDING |
| Installing new software on peer SP | PENDING |
| Rebooting peer SP | PENDING |
| Restarting services on peer SP | PENDING |
| Installing new software on primary SP | PENDING |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:23 | IN_PROGRESS | 40% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: IN_PROGRESS,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:23
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | IN_PROGRESS |
| Installing new software on peer SP | PENDING |
| Rebooting peer SP | PENDING |
| Restarting services on peer SP | PENDING |
| Installing new software on primary SP | PENDING |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:26 | IN_PROGRESS | 43% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: IN_PROGRESS,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:26
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | COMPLETED |
| Installing new software on peer SP | IN_PROGRESS |
| Rebooting peer SP | PENDING |
| Restarting services on peer SP | PENDING |
| Installing new software on primary SP | PENDING |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:32 | IN_PROGRESS | 50% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: IN_PROGRESS,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:32
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | COMPLETED |
| Installing new software on peer SP | COMPLETED |
| Rebooting peer SP | IN_PROGRESS |
| Restarting services on peer SP | PENDING |
| Installing new software on primary SP | PENDING |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:39 | IN_PROGRESS | 59% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: IN_PROGRESS,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:39
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | COMPLETED |
| Installing new software on peer SP | COMPLETED |
| Rebooting peer SP | COMPLETED |
| Restarting services on peer SP | IN_PROGRESS |
| Installing new software on primary SP | PENDING |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:42 | IN_PROGRESS | 66% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: IN_PROGRESS,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:42
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | COMPLETED |
| Installing new software on peer SP | COMPLETED |
| Rebooting peer SP | COMPLETED |
| Restarting services on peer SP | COMPLETED |
| Installing new software on primary SP | IN_PROGRESS |
| Rebooting the primary SP | PENDING |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:48 | IN_PROGRESS | 75% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: IN_PROGRESS,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 12:23:48
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | COMPLETED |
| Installing new software on peer SP | COMPLETED |
| Rebooting peer SP | COMPLETED |
| Restarting services on peer SP | COMPLETED |
| Installing new software on primary SP | COMPLETED |
| Rebooting the primary SP | IN_PROGRESS |
| Restarting services on primary SP | PENDING |
| Final tasks | PENDING |
| 12:23:55 | IN_PROGRESS | 83% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: COMPLETED,Restarting services on primary SP: IN_PROGRESS,Final tasks: PENDING |

#### Task State Changes at 12:23:55
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | COMPLETED |
| Installing new software on peer SP | COMPLETED |
| Rebooting peer SP | COMPLETED |
| Restarting services on peer SP | COMPLETED |
| Installing new software on primary SP | COMPLETED |
| Rebooting the primary SP | COMPLETED |
| Restarting services on primary SP | IN_PROGRESS |
| Final tasks | PENDING |
| 12:24:00 | COMPLETED | 100% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: COMPLETED,Restarting services on primary SP: COMPLETED,Final tasks: COMPLETED |

#### Task State Changes at 12:24:00
| Task | Status |
|------|--------|
| Preparing system | COMPLETED |
| Performing health checks | COMPLETED |
| Preparing system software | COMPLETED |
| Waiting for reboot command | COMPLETED |
| Performing health checks | COMPLETED |
| Installing new software on peer SP | COMPLETED |
| Rebooting peer SP | COMPLETED |
| Restarting services on peer SP | COMPLETED |
| Installing new software on primary SP | COMPLETED |
| Rebooting the primary SP | COMPLETED |
| Restarting services on primary SP | COMPLETED |
| Final tasks | COMPLETED |
**Success:** Upgrade completed successfully!
### Step 4: Getting final session details
Final Status Response:
```json
{
    "@base": "http://localhost:8000/api/instances/upgradeSession",
    "content": {
        "id": "Upgrade_5.4.0.0",
        "status": 2,
        "percentComplete": 100,
        "tasks": [
            {
                "status": 2,
                "type": 0,
                "caption": "Preparing system",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:03:30.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Performing health checks",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:02:10.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Preparing system software",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:16:10.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Waiting for reboot command",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:00:05.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Performing health checks",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:01:05.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Installing new software on peer SP",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:16:50.000"
            },
            {
                "status": 2,
                "type": 3,
                "caption": "Rebooting peer SP",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:14:15.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Restarting services on peer SP",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:05:00.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Installing new software on primary SP",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:13:30.000"
            },
            {
                "status": 2,
                "type": 3,
                "caption": "Rebooting the primary SP",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:13:55.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Restarting services on primary SP",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:05:10.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Final tasks",
                "creationTime": "2025-03-26T12:23:12.034776",
                "estRemainTime": "00:00:45.000"
            }
        ]
    },
    "links": [
        {
            "rel": "self",
            "href": "/Upgrade_5.4.0.0"
        }
    ],
    "updated": "2025-03-26T12:24:00.327Z"
}
```
### Task Completion Summary
| Task Name | Status | Duration |
|-----------|--------|----------|
