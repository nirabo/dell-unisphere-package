### candidateSoftwareVersion

Information about system software upgrades and language packs uploaded to the storage system and available to install

Embedded resource types

nameValuePai

#### Supported operations

Collection query , Instance query ,Prepare

# Attributes

| Attribute | Type | Description |
| --- | --- | --- |
| id | String | Unique identifier of the candidateSoftwareVersion instance. |
| version | String | Version of the candidate software. |
| fullVersion | String | Full Version of the candidate software. |
| revision | unsigned Integer[32] | Revision number of the candidate software. |
| releaseDate | DateTime | Release date of the candidate software. |
| type | Upgrade TypeEnum | Type of the candidate software. |
| rebootRequired | Boolean | Package requires reboot of bo5th SPs, one at a time, with |
|  |  | services remaining available. |
| canPauseBeforeReboot | Boolean | Package can utilize the 'pause' feature allowing the user to |
|  |  | choose their disruptive window. |

# Attributes for nameValuePair

List of name value pairs used to embed additional data in an object.

| Attribute | Type | Description |
| --- | --- | --- |
| name | String | Candidate description name. |
| value | String | Candidate description value. |

Query all members of the candidateSoftwareVersion collection

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | GET /api/types/candidateSoftwareVersion/instances |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of all members of the candidateSoftwareVersion |
|  | collection. |

Query a specific candidateSoftwareVersion instance

|  | Content - Type: application/json |
| --- | --- |
| Method and URI | GET /api/instances/candidateSoftwareVersion/<id> |
|  | where <id> is the unique identifier of the candidateSoftwareVersion instance to query. |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of a specific candidateSoftwareVersion |
|  | instance. |

# Prepare operation

Prepare the automated downloaded software image. Create a candidate version given a filename of the automated downloaded software image on the storage syttem.

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST api/types/candidateSoftwareVersion/action/prepare |
| Request body arguments | See the arquments table below. |
| Successful return status | 200 OK, 202 Accepted (async response) |
| Successful response body | JSON representation of the returned attributes. |

## Arguments for the Prepare operation

| Argument | In/ | Type | Required? | Description |
| --- | --- | --- | --- | --- |
|  | out |  |  |  |
| filename | in | String | Required | Filename of the automated downloaded software image |
|  |  |  |  | to change into candidate version. |
| id | out | candidateSoftwareVersion | N/A |  |
