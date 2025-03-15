# Dell Unisphere Mock API - Upgrade Flow Test Report
Generated on: Sat Mar 15 11:40:38 AM EET 2025


## Checking if API is running
API is running at http://localhost:8000

## Testing Complete Upgrade Flow
This test will create an upgrade session and monitor it until completion
Got CSRF token: 56e36540-eeeb-4c6c-9d8a-bbc6249a75b4
### Step 1: Creating dummy upgrade file

## Creating dummy upgrade file
Creating a 10MB dummy file for testing software upload
```
10+0 records in
10+0 records out
10485760 bytes (10 MB, 10 MiB) copied, 0.0421071 s, 249 MB/s
File created: ./tests/scripts/test_results/test_upgrade.bin (10MB)
```
### Step 2: Uploading software package
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/upload/files/types/candidateSoftwareVersion" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: 56e36540-eeeb-4c6c-9d8a-bbc6249a75b4" \
        -F "file=@./tests/scripts/test_results/test_upgrade.bin"
```
Response:
```json
{
    "id": "file_43c234dc-6a38-4a7a-8d43-bd063d3c97b8",
    "filename": "test_upgrade.bin",
    "size": 10485760
}
```
Uploaded software package: file_43c234dc-6a38-4a7a-8d43-bd063d3c97b8
### Step 3: Preparing software
Request:
```bash
curl -s -k -L -X POST "http://localhost:8000/api/types/candidateSoftwareVersion/action/prepare" \
        -u "admin:Password123!" \
        -b cookie.jar \
        -H "X-EMC-REST-CLIENT: true" \
        -H "EMC-CSRF-TOKEN: 56e36540-eeeb-4c6c-9d8a-bbc6249a75b4" \
        -H "Content-Type: application/json" \
        -d '{"filename":"file_43c234dc-6a38-4a7a-8d43-bd063d3c97b8"}'
```
Response:
```json
{
    "id": "candidate_6bcf5f22-a544-4c5a-8d50-c15a997f3046",
    "status": "SUCCESS"
}
```
### Step 4: Getting candidate software versions
Request:
```bash
curl -s -k -L -X GET "http://localhost:8000/api/types/candidateSoftwareVersion/instances"         -u "admin:Password123!"         -b cookie.jar         -H "X-EMC-REST-CLIENT: true"         -H "EMC-CSRF-TOKEN: 56e36540-eeeb-4c6c-9d8a-bbc6249a75b4"
```
Response:
```json
{
    "@base": "http://localhost:8000/api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-03-15T11:40:39.323Z",
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
                "id": "file_43c234dc-6a38-4a7a-8d43-bd063d3c97b8",
                "version": "5.4.0.0",
                "fullVersion": "Unity test_upgrade.bin",
                "revision": 0,
                "releaseDate": "2025-03-15T11:40:39.135471",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/file_43c234dc-6a38-4a7a-8d43-bd063d3c97b8"
                }
            ],
            "updated": "2025-03-15T11:40:39.323Z"
        },
        {
            "@base": "http://localhost:8000/api/instances/candidateSoftwareVersion",
            "content": {
                "id": "candidate_6bcf5f22-a544-4c5a-8d50-c15a997f3046",
                "version": "5.4.0",
                "fullVersion": "Unity 5.4.0.0 (Release, Build 150, 2023-06-18 19:02:01, 5.4.0.0.5.150)",
                "revision": 150,
                "releaseDate": "2025-03-15T11:40:39.251634",
                "type": "SOFTWARE",
                "rebootRequired": true,
                "canPauseBeforeReboot": true
            },
            "links": [
                {
                    "rel": "self",
                    "href": "/candidate_6bcf5f22-a544-4c5a-8d50-c15a997f3046"
                }
            ],
            "updated": "2025-03-15T11:40:39.323Z"
        }
    ]
}
```
Found candidate ID: file_43c234dc-6a38-4a7a-8d43-bd063d3c97b8
### Step 2: Creating upgrade session
### Step 3: Monitoring upgrade progress
Monitoring the upgrade session until completion

| Time | Status | Progress | Task States |
|------|--------|----------|------------|
| 11:40:39 | PENDING | 0% | Preparing system: PENDING,Performing health checks: PENDING,Preparing system software: PENDING,Waiting for reboot command: PENDING,Performing health checks: PENDING,Installing new software on peer SP: PENDING,Rebooting peer SP: PENDING,Restarting services on peer SP: PENDING,Installing new software on primary SP: PENDING,Rebooting the primary SP: PENDING,Restarting services on primary SP: PENDING,Final tasks: PENDING |

#### Task State Changes at 11:40:39
| Task | Status |
|------|--------|
| Preparing system | PENDING |
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
