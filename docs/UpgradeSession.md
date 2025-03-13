## UpgradeSessionTypeEnum

| Value | Enumeration |
| :-- | :-- |
| 0 | Upgrade |
| 1 | Health_Check |
| 2 | Storageprocessor_Upgrade |
| 3 | Offline_Storageprocessor_Upgrade |

## UpgradeStatusEnum
Current status of the associated upgrade session.

| Value | Enumeration | Description |
| :--: | :-- | :-- |
| 0 | Upgrade_Not_Started | Upgrade session was not started. |
| 1 | Upgrade_in_Progress | Upgrade session is in the process of upgrading the system <br> software, language pack, or drive firmware. |

| 2 | Upgrade_Completed | Upgrade session completed successfully. |
| :-- | :-- | :-- |
| 3 | Upgrade_Failed | Upgrade session did not complete successfully. |
| 4 | Upgrade_Failed_Lock | Upgrade session failed, and the system is in a locked state. |
| 5 | Upgrade_Cancelled | Upgrade session was cancelled. |
| 6 | Upgrade_Paused | Upgrade session is paused. |
| 7 | Upgrade_Adminseledged | Upgrade session was acknowledged. |
| 8 | Upgrade_Waiting_For_User | Upgrade session is waiting for user action to continue the <br> upgrade |
| 9 | Upgrade_Paused_Lock | Upgrade session is paused past the point of cancellation. |

## UpgradeTypeEnum

| Value | Enumeration |
| :-- | :-- |
| 0 | Software |
| 1 | Firmware |
| 2 | LanguagePack |

## softwareUpgradeSession

Information about a storage system upgrade session.

Create an upgrade session to upprade the system software or view existing upprade sessions. The upgrade sessions installs an uporade candidate file ryslem. Download the hast Support website. Use the CLI to upload the upgrade candidate to the system before creating the upgrade session. For information, see theUnisphere CLI User Guide.

The latest software upgrade candidate contains all available hot fixes. If you have applied hot fixes to your system, the hot fixes are included in the latest upgrade candidate.

Note: All system components must be healthy prior to upgrading the system software. If any system components are degraded, the software update will fail

### Embedded resource types

upgradeMessage, upgradeTask

# Supported operations

Collection query, Instance query, Create, VerifyUpgradeEligibility, Resume

### Attributes

| Attribute | Type | Description |
| --- | --- | --- |
| id | String | Unique identifier for the softwareUpgradeSession instance. |
| type | UpgradeSessionTypeEnum | Type of software to upgrade. |
| candidate | candidateSoftwareVersion | Candidate software to install in the upgrade session, as defined by |
|  |  | the candidateSoftwareVersion resource type. |
| caption | String | Caption for this upgrade session. |
| status | UpgradeStatusEnum | Status of the current upgrade session. |
| messages | List < upgradeMessage> | List of upgrade messages. |
| creationTime | DateTime | Date and time when the upgrade session was started. |
| elapsedTime | Date Time[Interval] | Amount of time for which the upgrade session was running. |
| percentComplete | unsigned Integer[16(percent)] | Percentage of the upgrade that is completed. |
|  | [0.. 100] |  |
| tasks | List < upgrade Task> | Current upgrade activity in the upgrade session, as defined by the |
|  |  | upgradeTask resource type. |

### Attributes for upgradeMessage

A message occurrence. This is also the message object returned in the body of non-2xx return code REST responses.

| Attribute | Type | Description |
| --- | --- | --- |
| errorCode | String | Error code for this message. |
| messages | List<localizedMessage> | List of localized messages. |
| severity | SeverityEnum | Severity level associated with this message. |
| httpStatus | unsigned Integer[32] | HTTP status code for this message. |

Attributes for upgradeTask

| Attribute | Type | Description |
| --- | --- | --- |
| caption | String | Caption for this task. |
| creationTime | DateTime | Date and time when the upgrade task was started. |
| status | UpgradeStatusEnum | Current status of the upgrade activity. |
| type | UpgradeSessionTypeEnum | Upgrade session type. |
| estRemainTime | DateTime[Interval] | Estimated time remaining for the upgrade task. |

#### Query all members of the softwareUpgradeSession collection

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | GET api/types/softwareUpgradeSession/instances |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of all members of the softwareUpgradeSession collection. |

#### Query a specific softwareUpgradeSession instance

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | GET /api/instances/softwareUpgradeSession/<id> |
|  | where <id> is the unique identifier of the softwareUpgradeSession instance to query. |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of a specific softwareUpgradeSession instance. |

# Create operation

Start a session to upgrade the system software with an uploaded upgrade candidate

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST /api/types/softwareUpgradeSession/instances |
| Request body arguments | See the arquments table below. |
| Successful return status | 201 Created |
| Successful response body | JSON representation of the <id> attribute |

# Arguments for the Create operation

| Arqument | In/ | Type | Required? | Description |
| --- | --- | --- | --- | --- |
|  | out |  |  |  |
| candidate | in | candidateSoftwareVersion | Optional | Candidate software to install in the upgrade |
|  |  |  |  | session, as defined by the |
|  |  |  |  | candidateSoftwareVersion resource type. |
| selectedModel | in | SPModelNameEnum | Optional |  |
| pauseBeforeReboot | in | Boolean | Optional | Flag to tell that session should stop after the |
|  |  |  |  | "preinstall" tasks and before first SP reboot. |
| id | out | softwareUpgradeSession | N/A | The new upgrade session. |

# VerifyUpgradeEligibility operation

Validate that the system is in a healthy state. This is required for an upgrade is started. You can use this operation to peration to perdion to perdion to perdion no perfo

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST |
|  | /api/types/softwareUpgradeSession/action/verifyUpgradeEligibility |
| Request body arguments | See the arquments table below. |
| Successful return status | 200 OK, 202 Accepted (async response) |
| Successful response body | JSON representation of the returned attributes. |

### Arguments for the VerifyUpgradeEligibility operation

| Arqument | In/ | Type | Required? | Description |
| --- | --- | --- | --- | --- |
|  | out |  |  |  |
| messages | out | List < upgradeMessage> | N/A | List of embedded upgradeMessage which contain the info |
|  |  |  |  | of message's identifier, localized text, severity and so on. |

# Resume operation

Resume a session that is currently in paused, failed, or failed_lock state.

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI POST | /api/instances/softwareUpgradeSession/<id>/action/resume |
|  | where <id> is the unique identifier of the softwareUpgradeSession instance. |
| Request body arguments None |  |
| Successful return status | 204 No Content |
| Successful response body | No body content. |
