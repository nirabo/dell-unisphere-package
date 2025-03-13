# system

Information about general settings for the storage system.

### Supported operations

Collection query , Instance query ,Failback ,Modify

# Attributes

| Attribute | Type | Description |
| --- | --- | --- |
| id | String | Unique identifier of the system instance. |
| health | health | Health information for the system, as defined by the |
|  |  | health resource type. |
| name | String | System name. |
| model | String | System model name. |
| serialNumber | String | System product serial number. |
| uuidBase | unsigned Integer[32] | Base value used to generate UUIDs in the host |
|  |  | environment(e.g. OVMS host). |
| internalModel | String | Internal model name for the system. |
| platform | String | Hardware platform for the system. |
| isAllFlash | Boolean | Indicates whether sytem is all flash. |
| macAddress | String | MAC address of the management interface. |
| isEULAAccepted | Boolean | Indicates whether the End User License Agreement |
|  |  | (EULA) was accepted for an upgrade. Once the EULA |
|  |  | is accepted, users can upload product licenses and |
|  |  | configure the system, or both. Values are: |
|  |  | . true - EULA was accepted on the system. Once |
|  |  | you set this value, you cannot set it to false later on. |
|  |  | false - EULA was not accepted on the system. . |
| isUpgradeComplete | Boolean | Indicates whether an upgrade completed. Operations |
|  |  | that change the configuration of the system are not |
|  |  | allowed while an upgrade is in progress. |
|  |  | Values are: |
|  |  | . true - Upgrade completed. |
|  |  | . false - Upgrade did not complete. |
| isAutoFailbackEnabled | Boolean | Indicates whether the automatic failback of NAS |
|  |  | servers is enabled for the system. Values are: |
|  |  | . true - Automatic failback for NAS servers is |
|  |  | enabled. |
|  |  | . false - Automatic failback for NAS servers is |
|  |  | disabled. |
| currentPower | unsigned Integer[32(watts)] | Current amount of power used by the system. |
| avgPower | unsigned Integer[32(watts)] | Average amount of power used by the system. The |
|  |  | system uses a one hour window of 30-second samples |
|  |  | to determine this value. |
| supportedUpgradeModels | List< SPModelNameEnum> | List of all supported models for hardware upgrade. |
| isHemoteSysInterfaceAutoPair | Boolean |  |
|  |  | Indicates whether remote system interface automatic pairing is enabled for the system. When enabled, only |
|  |  | pingable replication interfaces between two Unity |
|  |  | systems are used by replication remote system. The |
|  |  | default value is true. Modify the value to false if it is |
|  |  | intended to use all replication interfaces for the replication remote system despite their connectivity. |
|  |  | Values are: |
|  |  | . true - Remote system interface automatic pairing is |
|  |  | enabled. |
|  |  | . false - Remote system interface automatic pairing |
|  |  | is disabled. |

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI GET | /api/types/system/instances |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of all members of the system collection. |

# Query a specific system instance

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | GET /api/instances/system/<id> |
|  | where <id> is the unique identifier of the system instance to query. |
| Or |  |
|  | GET /api/instances/system/name: < value> |
|  | where <value> is the name of the system instance to query. |
| Request body arguments None |  |
| Successful return status | 200 OK |
| Successful response body | JSON representation of a specific system instance. |

# Fallback operation

Immediately fall back the storage system to the other storage processor.

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST /api/instances/system/<id>/action/failback |
|  | where <id> is the unique identifier of the system instance. |
| Or |  |
|  | POST /api/instances/system/name: < value>/action/failback |
|  | where < value> is the name of the system instance. |
| Request body arguments | None |
| Successful return status | 204 No Content, 202 Accepted (async response) |
| Successful response body | No body content. |

# Modify operation

Modify the system configuration.

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST /api/instances/system/<id>/action/modify |
|  | where <id> is the unique identifier of the system instance. |
| Or |  |
|  | POST /api/instances/system/name: <value>/action/modify |
|  | where < value> is the name of the system instance. |
| Request body arguments | See the arquments table below. |
| Successful return status | 204 No Content, 202 Accepted (async response) |
| Successful response body | No body content. |

# Arguments for the Modify operation

| Arqument | In/ | Type | Required? | Description |
| --- | --- | --- | --- | --- |
|  | out |  |  |  |
| name | in | String | Optional | System name. |
| uuidBase | in | unsigned | Optional | Base value used to generate UUIDs in the host |
|  |  | Integer[32] |  | environment(e.g. OVMS host). This value should be |
|  |  |  |  | a non-negative number, and not greater than |
|  |  |  |  | 16385. OpenVMS requires an unique OVMS device |
|  |  |  |  | UUID for every device visible to an OVMS host, the |
|  |  |  |  | OVMS device UUID must also be consistent for any |
|  |  |  |  | given device across all nodes of an OVMS cluster. |
|  |  |  |  | Dell VNX and Unity systems create the OVMS |
|  |  |  |  | device UUID by appending the LUN number to the |
|  |  |  |  | configured Unity or VNX OVMS base UUID. In the |
|  |  |  |  | situation of multiple storage systems visible to the |
|  |  |  |  | same OVMS host(s) the storage systems must be |
|  |  |  |  | configured with unique values which avoid |
|  |  |  |  | conflicting OVMS device UUIDs. Unity and VNX |
|  |  |  |  | devices connected to multi-node OVMS clusters |
|  |  |  |  | should be configured into a consistency group to |
|  |  |  |  | ensure a consistent OVMS device UUID for the |
|  |  |  |  | same device across all OVMS cluster nodes. |

| isUpgradeCompleted | in | Boolean | Optional | Indicates whether to manually mark an upgrade |
| --- | --- | --- | --- | --- |
|  |  |  |  | process completed. This value is automatically set |
|  |  |  |  | to true by the upgrade provider at the end of the |
|  |  |  |  | upgrade process and back to false by the first GUI |
|  |  |  |  | request. |
|  |  |  |  | Values are: |
|  |  |  |  | . true - Mark the upgrade completed. |
|  |  |  |  | . false - Do not mark upgrade completed. |
|  |  |  |  | This attribute is required by the GUI to display the |
|  |  |  |  | upgrade details window on the first login after the |
|  |  |  |  | upgrade completes. It does not depend on the |
|  |  |  |  | session. The user who started an upgrade may not |
|  |  |  |  | see its results, if another user logged in earlier. |
| isEulaAccepted | in | Boolean | Optional | Indicates whether to accept the End User License |
|  |  |  |  | Agreement (EULA) for an upgrade. Once the EULA |
|  |  |  |  | is accepted, users can upload product licenses and |
|  |  |  |  | configure the system, or both. Values are: |
|  |  |  |  | . true - Accept the EULA .. |
|  |  |  |  | . false - Do not accept the EULA. |
| isAutoFailbackEnabled | in | Boolean | Optional | Indicates whether to enable the automatic failback |
|  |  |  |  | of NAS servers in the system. Values are: |
|  |  |  |  | . true - Enable the automatic failback of NAS |
|  |  |  |  | servers. |
|  |  |  |  | . false - Disable the automatic failback of NAS |
|  |  |  |  | servers. |
| isRemoteSysInterfaceAutoPair | in | Boolean | Optional | Indicates whether remote system interface |
|  |  |  |  | automatic pairing is enabled for the system. Values |
|  |  |  |  | are: |
|  |  |  |  | . true - Remote system interface automatic |
|  |  |  |  | pairing is enabled. |
|  |  |  |  | . false - Remote system interface automatic |
|  |  |  |  | pairing is disabled. |
