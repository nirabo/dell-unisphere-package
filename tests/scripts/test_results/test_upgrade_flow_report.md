# Dell Unisphere Mock API - Comprehensive Test Report
Generated on: Sat Mar 15 02:06:42 PM EET 2025


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
    "updated": "2025-03-15T14:06:42.076Z",
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
            "updated": "2025-03-15T14:06:42.076Z"
        }
    ]
}
```

## Getting Login Session Info
### Request
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/loginSessionInfo/instances" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
```
Got CSRF token: 549510d6-8091-42b3-913a-6d064048fdb3
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
        "id": "549510d6-8091-42b3-913a-6d064048fdb3",
        "isPasswordChangeRequired": false
    },
    "links": [
        {
            "rel": "self",
            "href": "/549510d6-8091-42b3-913a-6d064048fdb3"
        }
    ],
    "updated": "2025-03-15T14:06:42.139Z"
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
    "updated": "2025-03-15T14:06:42.335Z",
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
            "updated": "2025-03-15T14:06:42.335Z"
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
            "updated": "2025-03-15T14:06:42.335Z"
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
            "updated": "2025-03-15T14:06:42.335Z"
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
    "updated": "2025-03-15T14:06:42.413Z",
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
                "releaseDate": "2025-03-15T14:06:27.934947",
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
                        "releaseDate": "2025-03-15T14:06:27.934960",
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
            "updated": "2025-03-15T14:06:42.413Z"
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
        "releaseDate": "2025-03-15T14:06:27.934947",
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
                "releaseDate": "2025-03-15T14:06:27.934960",
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
    "updated": "2025-03-15T14:06:42.479Z"
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
    "updated": "2025-03-15T14:06:42.530Z",
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
    "updated": "2025-03-15T14:06:42.597Z",
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
    "updated": "2025-03-15T14:06:42.672Z",
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
curl -s -k -L -X POST "http://localhost:8000/api/types/upgradeSession/action/verifyUpgradeEligibility" -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: 00b5dfa7-8cc6-49e5-bb46-5c9f475fd0c5"
```
### Response
```json
{
    "eligible": true,
    "messages": [],
    "requiredPatches": [],
    "requiredHotfixes": []
}
```

## Testing Complete Upgrade Flow
This test will create an upgrade session and monitor it until completion
Got CSRF token: d7b466aa-bea6-47e6-8464-107adf22d77d
### Step 1: Creating dummy upgrade file

## Creating dummy upgrade file
Creating a 10MB dummy file for testing software upload
```
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0443167 s, 237 MB/s
File created: ./tests/scripts/test_results/test_upgrade.bin (10MB)
```
### Step 2: Uploading software package
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: d7b466aa-bea6-47e6-8464-107adf22d77d" \
        -F "file=@./tests/scripts/test_results/test_upgrade.bin"
```
Response:
```json
{
    "id": "file_c04e72c9-bf87-4b08-a08c-890de1317d74",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```
Uploaded software package: file_c04e72c9-bf87-4b08-a08c-890de1317d74
### Step 3: Preparing software
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: d7b466aa-bea6-47e6-8464-107adf22d77d" \
        -H "Content-Type: application/json" \
        -d '{"filename":"file_c04e72c9-bf87-4b08-a08c-890de1317d74"}'
```
Response:
```json
{
    "id": "candidate_f285cc52-5a69-4fa5-b058-83dc2b3fd3b2",
    "status": "SUCCESS"
}
```
### Step 4: Getting candidate software versions
Request:
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances"         -u "admin:Password123!"         -b cookie.jar         -H "X-EMC-REST-CLIENT: true"         -H "EMC-CSRF-TOKEN: d7b466aa-bea6-47e6-8464-107adf22d77d"
```
Response:
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-15T14:06:43.118Z",
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
                "id": "file_c04e72c9-bf87-4b08-a08c-890de1317d74",
                "version": "5.4.0.0",
                "fullVersion": "Unity test_upgrade.bin",
                "revision": 0,
                "releaseDate": "2025-03-15T14:06:42.948452",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/file_c04e72c9-bf87-4b08-a08c-890de1317d74"
                }
            ],
            "updated": "2025-03-15T14:06:43.118Z"
        },
        {
            "@base": "http://localhost:8000/api/instances/candidateSoftwareVersion",
            "content": {
                "id": "candidate_f285cc52-5a69-4fa5-b058-83dc2b3fd3b2",
                "version": "5.4.0",
                "fullVersion": "Unity 5.4.0.0 (Release, Build 150, 2023-06-18 19:02:01, 5.4.0.0.5.150)",
                "revision": 150,
                "releaseDate": "2025-03-15T14:06:43.070722",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/candidate_f285cc52-5a69-4fa5-b058-83dc2b3fd3b2"
                }
            ],
            "updated": "2025-03-15T14:06:43.118Z"
        }
    ]
}
```
Found candidate ID: file_c04e72c9-bf87-4b08-a08c-890de1317d74
### Step 2: Creating upgrade session
### Step 3: Monitoring upgrade progress
Monitoring the upgrade session until completion

| Time | Status | Progress | Task States |
|------|--------|----------|------------|
| 14:06:43 | IN_PROGRESS | 0% | Preparing system: IN_PROGRESS,Performing health checks: PENDING,Preparing system software: PENDING,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:06:43
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
| 14:06:45 | IN_PROGRESS | 12% | Preparing system: COMPLETED,Performing health checks: IN_PROGRESS,Preparing system software: PENDING,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:06:45
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
| 14:06:48 | IN_PROGRESS | 18% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: IN_PROGRESS,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:06:48
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
| 14:06:54 | IN_PROGRESS | 39% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: IN_PROGRESS,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:06:54
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
| 14:06:57 | IN_PROGRESS | 43% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: IN_PROGRESS,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:06:57
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
| 14:07:03 | IN_PROGRESS | 50% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: IN_PROGRESS,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:07:03
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
| 14:07:10 | IN_PROGRESS | 58% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: IN_PROGRESS,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:07:10
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
| 14:07:15 | IN_PROGRESS | 69% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: IN_PROGRESS,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:07:15
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
| 14:07:22 | IN_PROGRESS | 77% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: IN_PROGRESS,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 14:07:22
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
| 14:07:28 | IN_PROGRESS | 89% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: COMPLETED,Restarting services on primary SP: IN_PROGRESS,Final tasks: PENDING |

#### Task State Changes at 14:07:28
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
| 14:07:31 | COMPLETED | 100% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: COMPLETED,Restarting services on primary SP: COMPLETED,Final tasks: COMPLETED |

#### Task State Changes at 14:07:31
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
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:03:30.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Performing health checks",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:02:10.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Preparing system software",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:16:10.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Waiting for reboot command",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:00:05.000"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Performing health checks",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:01:05.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Installing new software on peer SP",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:16:50.000"
            },
            {
                "status": 2,
                "type": 3,
                "caption": "Rebooting peer SP",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:14:15.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Restarting services on peer SP",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:05:00.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Installing new software on primary SP",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:13:30.000"
            },
            {
                "status": 2,
                "type": 3,
                "caption": "Rebooting the primary SP",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:13:55.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Restarting services on primary SP",
                "creationTime": "2025-03-15T14:06:43.239288",
                "estRemainTime": "00:05:10.000"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Final tasks",
                "creationTime": "2025-03-15T14:06:43.239288",
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
    "updated": "2025-03-15T14:07:31.076Z"
}
```
### Task Completion Summary
| Task Name | Status | Duration |
|-----------|--------|----------|
