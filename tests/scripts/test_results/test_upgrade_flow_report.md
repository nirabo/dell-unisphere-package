# Dell Unisphere Mock API - Upgrade Flow Test Report
Generated on: Sat Mar 15 01:24:54 PM EET 2025


## Checking if API is running
API is running at http://localhost:8000

## Testing Complete Upgrade Flow
This test will create an upgrade session and monitor it until completion
Got CSRF token: 3e937c1c-e8eb-485c-b1be-b1e9efb22f67
### Step 1: Creating dummy upgrade file

## Creating dummy upgrade file
Creating a 10MB dummy file for testing software upload
```
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0518394 s, 202 MB/s
File created: ./tests/scripts/test_results/test_upgrade.bin (10MB)
```
### Step 2: Uploading software package
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: 3e937c1c-e8eb-485c-b1be-b1e9efb22f67" \
        -F "file=@./tests/scripts/test_results/test_upgrade.bin"
```
Response:
```json
{
    "id": "file_2136b4ad-07f5-4352-ae91-62ec65c155bc",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```
Uploaded software package: file_2136b4ad-07f5-4352-ae91-62ec65c155bc
### Step 3: Preparing software
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: 3e937c1c-e8eb-485c-b1be-b1e9efb22f67" \
        -H "Content-Type: application/json" \
        -d '{"filename":"file_2136b4ad-07f5-4352-ae91-62ec65c155bc"}'
```
Response:
```json
{
    "id": "candidate_e62109f3-cd8c-4c78-b8f3-49520e683072",
    "status": "SUCCESS"
}
```
### Step 4: Getting candidate software versions
Request:
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances"         -u "admin:Password123!"         -b cookie.jar         -H "X-EMC-REST-CLIENT: true"         -H "EMC-CSRF-TOKEN: 3e937c1c-e8eb-485c-b1be-b1e9efb22f67"
```
Response:
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-15T13:24:54.768Z",
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
                "id": "file_2136b4ad-07f5-4352-ae91-62ec65c155bc",
                "version": "5.4.0.0",
                "fullVersion": "Unity test_upgrade.bin",
                "revision": 0,
                "releaseDate": "2025-03-15T13:24:54.561974",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/file_2136b4ad-07f5-4352-ae91-62ec65c155bc"
                }
            ],
            "updated": "2025-03-15T13:24:54.768Z"
        },
        {
            "@base": "http://localhost:8000/api/instances/candidateSoftwareVersion",
            "content": {
                "id": "candidate_e62109f3-cd8c-4c78-b8f3-49520e683072",
                "version": "5.4.0",
                "fullVersion": "Unity 5.4.0.0 (Release, Build 150, 2023-06-18 19:02:01, 5.4.0.0.5.150)",
                "revision": 150,
                "releaseDate": "2025-03-15T13:24:54.699161",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/candidate_e62109f3-cd8c-4c78-b8f3-49520e683072"
                }
            ],
            "updated": "2025-03-15T13:24:54.768Z"
        }
    ]
}
```
Found candidate ID: file_2136b4ad-07f5-4352-ae91-62ec65c155bc
### Step 2: Creating upgrade session
### Step 3: Monitoring upgrade progress
Monitoring the upgrade session until completion

| Time | Status | Progress | Task States |
|------|--------|----------|------------|
| 13:24:55 | IN_PROGRESS | 0% | Preparing system: IN_PROGRESS,Performing health checks: PENDING,Preparing system software: PENDING,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:24:55
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
| 13:24:59 | IN_PROGRESS | 11% | Preparing system: COMPLETED,Performing health checks: IN_PROGRESS,Preparing system software: PENDING,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:24:59
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
| 13:25:01 | IN_PROGRESS | 16% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: IN_PROGRESS,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:25:01
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
| 13:25:17 | IN_PROGRESS | 37% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: IN_PROGRESS,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:25:17
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
| 13:25:19 | IN_PROGRESS | 42% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: IN_PROGRESS,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:25:19
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
| 13:25:35 | IN_PROGRESS | 50% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: IN_PROGRESS,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:25:35
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
| 13:25:49 | IN_PROGRESS | 58% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: IN_PROGRESS,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:25:49
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
| 13:25:56 | IN_PROGRESS | 67% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: IN_PROGRESS,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:25:56
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
| 13:26:09 | IN_PROGRESS | 75% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: IN_PROGRESS,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 13:26:09
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
| 13:26:23 | IN_PROGRESS | 85% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: COMPLETED,Restarting services on primary SP: IN_PROGRESS,Final tasks: PENDING |

#### Task State Changes at 13:26:23
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
| 13:26:27 | IN_PROGRESS | 99% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: COMPLETED,Restarting services on primary SP: COMPLETED,Final tasks: IN_PROGRESS |

#### Task State Changes at 13:26:27
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
| Final tasks | IN_PROGRESS |
| 13:26:29 | COMPLETED | 100% | Preparing system: COMPLETED,Performing health checks: COMPLETED,Preparing system software: COMPLETED,Waiting for reboot command: COMPLETED,Performing health checks: COMPLETED,Installing new software on peer SP: COMPLETED,Rebooting peer SP: COMPLETED,Restarting services on peer SP: COMPLETED,Installing new software on primary SP: COMPLETED,Rebooting the primary SP: COMPLETED,Restarting services on primary SP: COMPLETED,Final tasks: COMPLETED |

#### Task State Changes at 13:26:29
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
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:03:30.000",
                "startTime": "2025-03-15T13:24:54.875255",
                "endTime": "2025-03-15T13:24:58.390747"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Performing health checks",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:02:10.000",
                "startTime": "2025-03-15T13:24:58.390979",
                "endTime": "2025-03-15T13:25:00.565350"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Preparing system software",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:16:10.000",
                "startTime": "2025-03-15T13:25:00.565574",
                "endTime": "2025-03-15T13:25:16.749399"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Waiting for reboot command",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:00:05.000",
                "startTime": "2025-03-15T13:25:16.749751",
                "endTime": "2025-03-15T13:25:16.852944"
            },
            {
                "status": 2,
                "type": 0,
                "caption": "Performing health checks",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:01:05.000",
                "startTime": "2025-03-15T13:25:16.853166",
                "endTime": "2025-03-15T13:25:17.946759"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Installing new software on peer SP",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:16:50.000",
                "startTime": "2025-03-15T13:25:17.946988",
                "endTime": "2025-03-15T13:25:34.802920"
            },
            {
                "status": 2,
                "type": 3,
                "caption": "Rebooting peer SP",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:14:15.000",
                "startTime": "2025-03-15T13:25:34.803208",
                "endTime": "2025-03-15T13:25:49.068227"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Restarting services on peer SP",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:05:00.000",
                "startTime": "2025-03-15T13:25:49.068537",
                "endTime": "2025-03-15T13:25:54.074721"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Installing new software on primary SP",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:13:30.000",
                "startTime": "2025-03-15T13:25:54.074942",
                "endTime": "2025-03-15T13:26:07.588298"
            },
            {
                "status": 2,
                "type": 3,
                "caption": "Rebooting the primary SP",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:13:55.000",
                "startTime": "2025-03-15T13:26:07.588444",
                "endTime": "2025-03-15T13:26:21.530810"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Restarting services on primary SP",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:05:10.000",
                "startTime": "2025-03-15T13:26:21.530954",
                "endTime": "2025-03-15T13:26:26.708508"
            },
            {
                "status": 2,
                "type": 2,
                "caption": "Final tasks",
                "creationTime": "2025-03-15T13:24:54.872466",
                "estRemainTime": "00:00:45.000",
                "startTime": "2025-03-15T13:26:26.708836",
                "endTime": "2025-03-15T13:26:27.462124"
            }
        ],
        "messages": [
            {
                "timestamp": "2025-03-15T13:24:54.875209",
                "message": "Starting task: Preparing system",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:24:54.875322",
                "message": "Starting task: Preparing system",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:24:58.390449",
                "message": "Completed task: Preparing system",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:24:58.390759",
                "message": "Completed task: Preparing system",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:24:58.390888",
                "message": "Starting task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:24:58.391174",
                "message": "Starting task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:00.565164",
                "message": "Completed task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:00.565360",
                "message": "Completed task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:00.565483",
                "message": "Starting task: Preparing system software",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:00.565795",
                "message": "Starting task: Preparing system software",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.749176",
                "message": "Completed task: Preparing system software",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.749410",
                "message": "Completed task: Preparing system software",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.749596",
                "message": "Starting task: Waiting for reboot command",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.750062",
                "message": "Starting task: Waiting for reboot command",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.852733",
                "message": "Completed task: Waiting for reboot command",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.852955",
                "message": "Completed task: Waiting for reboot command",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.853079",
                "message": "Starting task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:16.853364",
                "message": "Starting task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:17.946537",
                "message": "Completed task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:17.946769",
                "message": "Completed task: Performing health checks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:17.946893",
                "message": "Starting task: Installing new software on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:17.947188",
                "message": "Starting task: Installing new software on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:34.802740",
                "message": "Completed task: Installing new software on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:34.802928",
                "message": "Completed task: Installing new software on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:34.803088",
                "message": "Starting task: Rebooting peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:34.803521",
                "message": "Starting task: Rebooting peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:49.068010",
                "message": "Completed task: Rebooting peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:49.068239",
                "message": "Completed task: Rebooting peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:49.068428",
                "message": "Starting task: Restarting services on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:49.068815",
                "message": "Starting task: Restarting services on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:54.074507",
                "message": "Completed task: Restarting services on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:54.074730",
                "message": "Completed task: Restarting services on peer SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:54.074854",
                "message": "Starting task: Installing new software on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:25:54.075123",
                "message": "Starting task: Installing new software on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:07.588170",
                "message": "Completed task: Installing new software on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:07.588302",
                "message": "Completed task: Installing new software on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:07.588388",
                "message": "Starting task: Rebooting the primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:07.588546",
                "message": "Starting task: Rebooting the primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:21.530697",
                "message": "Completed task: Rebooting the primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:21.530814",
                "message": "Completed task: Rebooting the primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:21.530891",
                "message": "Starting task: Restarting services on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:21.531110",
                "message": "Starting task: Restarting services on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:26.708288",
                "message": "Completed task: Restarting services on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:26.708520",
                "message": "Completed task: Restarting services on primary SP",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:26.708721",
                "message": "Starting task: Final tasks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:26.709122",
                "message": "Starting task: Final tasks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:27.461940",
                "message": "Completed task: Final tasks",
                "severity": 0
            },
            {
                "timestamp": "2025-03-15T13:26:27.462132",
                "message": "Completed task: Final tasks",
                "severity": 0
            }
        ]
    },
    "links": [
        {
            "rel": "self",
            "href": "/Upgrade_5.4.0.0"
        }
    ],
    "updated": "2025-03-15T13:26:29.973Z"
}
```
### Task Completion Summary
| Task Name | Status | Duration |
|-----------|--------|----------|
