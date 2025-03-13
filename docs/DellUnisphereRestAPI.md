# Dell Unisphere REST API Documentation

This document presents a curated subset of the complete Dell Unisphere REST API documentation, specifically tailored for the development of a mock server. This mock server is designed to facilitate the design, development, and testing of our client application, which aims to enable software updates for the server itself.

## Overview

This document provides a comprehensive overview of the Dell Unisphere REST API, including its endpoints, request/response formats, and usage examples.

<!-- TOC -->

- [Dell Unisphere REST API Documentation](#dell-unisphere-rest-api-documentation)
    - [Overview](#overview)
    - [Basic System Info](#basic-system-info)
        - [Supported Operations](#supported-operations)
        - [Attributes](#attributes)
        - [Query all members of the basicSystemInfo collection](#query-all-members-of-the-basicsysteminfo-collection)
        - [Query a specific basicSystemInfo instance](#query-a-specific-basicsysteminfo-instance)
    - [Authentication and Authorization](#authentication-and-authorization)
    - [Example - Get CSRF token](#example---get-csrf-token)
            - [This is the response:](#this-is-the-response)
            - [Now, we could use the token to send POST or DELETE request:](#now-we-could-use-the-token-to-send-post-or-delete-request)
    - [How to get attributes of resource](#how-to-get-attributes-of-resource)
    - [Example - Get attributes of pool](#example---get-attributes-of-pool)
    - [Unity will return all the attribute names of pooleturn all the attribute names of pool:](#unity-will-return-all-the-attribute-names-of-pooleturn-all-the-attribute-names-of-pool)
    - [System](#system)
        - [Supported operations](#supported-operations)
        - [Attributes](#attributes)
        - [Query a specific system instance](#query-a-specific-system-instance)
        - [Fallback operation](#fallback-operation)
        - [Modify operation](#modify-operation)
            - [Arguments for the Modify operation](#arguments-for-the-modify-operation)
    - [InstalledSoftwareVersion](#installedsoftwareversion)
        - [Embedded resource types](#embedded-resource-types)
    - [Supported operations](#supported-operations)
        - [Attributes](#attributes)
        - [Attributes for firmwarePackage](#attributes-for-firmwarepackage)
        - [Attributes for installedSoftwareVersionLanguage](#attributes-for-installedsoftwareversionlanguage)
        - [Attributes for installedSoftwareVersionPackages](#attributes-for-installedsoftwareversionpackages)
        - [Query all members of the installedSoftwareVersion collection](#query-all-members-of-the-installedsoftwareversion-collection)
        - [Query a specific installedSoftwareVersion instance](#query-a-specific-installedsoftwareversion-instance)
    - [Login Session Info](#login-session-info)
    - [Supported operations](#supported-operations)
- [Query all members of the loginSessionInfo collection](#query-all-members-of-the-loginsessioninfo-collection)
    - [Logout operation](#logout-operation)
    - [User](#user)
    - [Supported operations](#supported-operations)
    - [Create operation](#create-operation)
- [Modify operation](#modify-operation)
    - [Candidate Software Version](#candidate-software-version)
            - [Supported operations](#supported-operations)
- [Attributes](#attributes)
- [Attributes for nameValuePair](#attributes-for-namevaluepair)
- [Prepare operation](#prepare-operation)
    - [Arguments for the Prepare operation](#arguments-for-the-prepare-operation)
    - [UpgradeSessionTypeEnum](#upgradesessiontypeenum)
    - [UpgradeStatusEnum](#upgradestatusenum)
    - [UpgradeTypeEnum](#upgradetypeenum)
    - [Software Upgrade Session](#software-upgrade-session)
        - [Embedded resource types](#embedded-resource-types)
        - [Supported operations](#supported-operations)
        - [Attributes](#attributes)
            - [Attributes for upgradeMessage](#attributes-for-upgrademessage)
            - [Attributes for upgradeTask](#attributes-for-upgradetask)
            - [Query all members of the softwareUpgradeSession collection](#query-all-members-of-the-softwareupgradesession-collection)
            - [Query a specific softwareUpgradeSession instance](#query-a-specific-softwareupgradesession-instance)
        - [Create operation](#create-operation)
            - [Arguments for the Create operation](#arguments-for-the-create-operation)
        - [VerifyUpgradeEligibility operation](#verifyupgradeeligibility-operation)
            - [Arguments for the VerifyUpgradeEligibility operation](#arguments-for-the-verifyupgradeeligibility-operation)
        - [Resume operation](#resume-operation)
    - [Uploading upgrade candidates and language packs](#uploading-upgrade-candidates-and-language-packs)
        - [Syntax](#syntax)
    - [Appendix A: Example Response](#appendix-a-example-response)
        - [Typical Response Structure](#typical-response-structure)
        - [Explanation of Each Field](#explanation-of-each-field)
        - [Example in Context: /api/types/basicSystemInfo/instances](#example-in-context-apitypesbasicsysteminfoinstances)
        - [Key Takeaways](#key-takeaways)
    - [Appendix B: Example Cookie](#appendix-b-example-cookie)
        - [Example Cookie Value](#example-cookie-value)
        - [Explanation of Cookie Components](#explanation-of-cookie-components)
        - [Additional Context](#additional-context)
    - [Appendix C: Real API Interaction Record](#appendix-c-real-api-interaction-record)

<!-- /TOC -->

## Basic System Info

Provides unauthenticated access to system model, system name, software version, and API version information. This is a singleton resource type.

### Supported Operations

Collection query, Instance query

### Attributes

| Attribute | Type | Description |
| --- | --- | --- |
| id | String | Unique identifier of the basicSystemInfo instance. |
| model | String | Model name of this storage system. This value comes from the |
|  |  | model attribute of the system resource. |
| name | String | Name of this storage system. This value comes from the name |
|  |  | attribute of the system resource. |
| softwareVersion | String | Software version of this storage system. This value comes from the version attribute of the installedSoftwareVersion resource. |
| softwareFullVersion | String | Software full version of this storage system. This value comes from |
|  |  | the fullversion attribute of the installedSoftwareVersion resource. |
| apiVersion | String | Latest version of the REST API that this storage system supports. |
| earliestApiVersion | String | Earliest version of the REST API that this storage system supports. |

### Query all members of the basicSystemInfo collection

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | GET /api/types/basicSystemInfo/instances |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of all members of the basicSystemInfo |
|  | collection. |

### Query a specific basicSystemInfo instance

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | GET /api/instances/basicSystemInfo/<id> |
|  | where <id> is the unique identifier of the basicSystemInfo instance to query. |
|  | Or |
|  | GET /api/instances/basicSystemInfo/name: < value> |
|  | where < value> is the name of the basicSystemInfo instance to query. |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of a specific basicSystemInfo instance. |

## Authentication and Authorization

To make a Unity REST API request, there is something we need to know:

- Every Unity REST API request must be authenticated, except the query of basicSystemInfo resource type
- The Unity REST API uses the standard HTTP Basic authentication mechanism to authenticate the REST requests
- Header X-EMC-REST-CLIENT: true is required for logging into Unity REST API server
- Header EMC-CSRF-TOKEN is required for POST and DELETE requests
- The following headers should also be included:
	- Accept: application/json: to indicate the format of the response content is JSON
	- Content-type: application/json: to indicate the format of the request body is JSON, it is required if there is a request body

To get CSRF token, we could make a basic GET request and get the token from the response headers.

## Example - Get CSRF token

In this case, we learn how to get CSRF token for POST/DELETE request usage.

First, we send a GET request, in this case, we make a collection query for resource "user":

```bash

curl --include --insecure --location \
     --user admin:Password123! \
     --cookie cookie.txt \
     --header "Accept: application/json" \
     --header "Content-Type: application/json" \
     --header "X-EMC-REST-CLIENT: true" \
     "https://10.245.83.44/api/types/user/instances"

```

#### This is the response:

```bash
HTTP/1.1 200 OK
Date: Thu, 27 Aug 2020 01:39:17 GMT
Server: Apache
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=63072000; includeSubdomains;
Set-Cookie: mod_sec_emc=value3&1&value1&iqVsJ%2BQSevmw8FNGWoI%2FkWOzydl0oqhuJNaWfLy3oiq7iwH7fH
            ckEcjlZ2GBo5fg%0A&value2&eaae0856a499fcc3b91408224a7307abc203b6684401cf1b912098778c5
            79548; path=/; secure; HttpOnly
EMC-CSRF-TOKEN: A+QAtubhfNa0S6dkPyusYCuuHWnuFfzx7GteLQNEm8KOQgQHe0t90Vp0B09E6V7AwMo90iC0ee5EV
                GR0LQrWQcDLs3zLAD1vRThgPyPZWkY=
Pragma: no-cache
Cache-Control: no-cache, no-store, max-age=0
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Content-Language: en-US
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: application/json; version=1.0;charset=UTF-8


{
  "@base": "https://10.245.83.44/api/types/user/instances? per_page=2000",
  "updated": "2020-08-27T01:39:17.471Z",
  "links": [
    {
      "rel": "self",
      "href": "&page=1"
    }
  ],
  "entries": [
    {
      "@base": "https://10.245.83.44/api/instances/user",
      "updated": "2020-08-27T01:39:17.471Z",
      "links": [
        {
          "rel": "self",
          "href": "/user_admin"
        }
      ],
      "content": {
        "id": "user_admin"
      }
    }
  ]
}
```

We could get CSRF token from the headers of response, in this case, the CSRF token is `dNrzcvqLkkzcWDNK1O1XBIUzsbldshcss5Jt+mye16D9GuRU+dFTgZN1zGJ1E/ jYm6Slo531D9JUdffuY4ViI+aL+MLsIXJ2cwS3T1t24fI=`.

#### Now, we could use the token to send POST or DELETE request:

```bash

curl --include --insecure --location \
     --user admin:Password123! \
     --cookie cookie.txt \
     --cookie-jar cookie.txt \
     --header "Accept: application/json" \
     --header "Content-Type: application/json" \
     --header "X-EMC-REST-CLIENT: true" \
     --header "EMC-CSRF-TOKEN: A+QAtubhfNa0S6dkPyusYCuuHWnuFfzx7GteLQNEm8KOQgQHe0t90Vp0B09E6V7AwMo90iC0ee5EVGR0LQrWQcDLs3zLAD1vRThgPyPZWkY=" \
     --request DELETE \
     https://10.245.83.44:443/api/instances/storageResource/sv_19166

```

## How to get attributes of resource

As we discussed in the frst call, felds=id,name parameter is specifed in request URI to tell Unity which attributes we need. But actually most of the resources have a bunch of attributes, not only id and name.

In order to get all attributes of a resource, we could send a GET request to get the resource types.

## Example - Get attributes of pool

In this case, we learn how to get all attributes of pool.

We send a GET request to get pool types with felds=attributes.name parameter specifed:


```bash
curl -i -k -L \
 -u admin:Password123! \
 -c cookie.txt \
 -H "Accept: application/json" \
 -H "Content-Type: application/json" \
 -H "X-EMC-REST-CLIENT: true" \
 "https://10.245.83.44/api/types/pool?compact=True&felds=attributes.name"
```
## Unity will return all the attribute names of pooleturn all the attribute names of pool:


```json
{
  "content": {
    "name": "pool",
    "attributes": [
      {
        "name": "dataReductionRatio"
      },
      {
        "name": "snapSpaceHarvestLowThreshold"
      },
      {
        "name": "sizeUsed"
      },
      {
        "name": "hasCompressionEnabledLuns"
      },
      {
        "name": "poolSpaceHarvestLowThreshold"
      },
      {
        "name": "sizePreallocated"
      },
      {
        "name": "snapSizeSubscribed"
      },
      {
        "name": "sizeFree"
      },
      {
        "name": "health"
      }
    ]
  }
}
```


## System

Information about general settings for the storage system.

### Supported operations

Collection query, Instance query, Fallback, Modify

### Attributes

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

### Query a specific system instance

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

### Fallback operation

Immediately fall back the storage system to the other storage processor.

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST /api/instances/system/<id>/action/fallback |
|  | where <id> is the unique identifier of the system instance. |
| Or |  |
|  | POST /api/instances/system/name: < value>/action/failback |
|  | where < value> is the name of the system instance. |
| Request body arguments | None |
| Successful return status | 204 No Content, 202 Accepted (async response) |
| Successful response body | No body content. |

### Modify operation

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

#### Arguments for the Modify operation

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


## InstalledSoftwareVersion

Information about installed system software and language packs in the VAlite system.
### Embedded resource types
firmwarePackage, installedSoftwareVersionLanguage, installedSoftwareVersionPackages

## Supported operations
Collection query, instance query


### Attributes

| Attribute | Type | Description |
| :-- | :-- | :-- |
| id | String | Unique identifier of the installedSoftwareVersion instance. |
| version | String | Version of the installed software. |
| revision | unsigned Integer[00] | Revision number of the installed software. |
| releaseDate | DateTime | Release date of the installed software. |
| \nVersion | String | Full Version of the installed software. |
| languages | List: installedSoftwareVersionLanguage | List of language pack information included in this release. |
| hotFuse | List::String: | List of installed hotFuses for the installed software instance. |
| packageVersions | List::installedSoftwareVersionPackages: | List of relevant package names and the version number of the package. |
| driveFirmware | List::firmwarePackage: | The drive firmware package is part of the installed software bundle which is used to upgrade disk firmware after software upgrade is completed. |

### Attributes for firmwarePackage
The drive firmware package is part of CIC bundle List the detail of the drive firmware package

| Attribute | Type | Description |
| :-- | :-- | :-- |
| name | String | Name of drive firmware package. |
| version | String | Version of drive firmware package. |
| releaseDate | DateTime | Release date of drive firmware package. |
| upgradedeDriveCount | unsigned Integer[10244es] | The number of upgradede drives in the array. |
| estimatedTime | unsigned Integer[10244utes] | Time estimation to upgrade drive firmware in minutes. |
| \nNewVersion | Boolean | Indicates whether the drive firmware package is newer than the installed one. |

### Attributes for installedSoftwareVersionLanguage
List the language pack information (name, version) installed in the release

| Attribute | Type | Description |
| :-- | :-- | :-- |
| name | String | Name of the installed software language. |
| version | String | Version of the installed software language. |

### Attributes for installedSoftwareVersionPackages
List of relevant package information (name, version) installed in the release

| Attribute | Type | Description |
| :-- | :-- | :-- |
| name | String | Name of the installed software package. |
| version | String | Version of the installed software package. |

### Query all members of the installedSoftwareVersion collection

| Header | Accept: application/json <br> Content-Type: application/json |
| :-- | :-- |
| Method and URI | GET /api/types/installedSoftwareVersion/insurance |
| Request body arguments | None |
| Successful return status | 25\% OK |
| Successful response body | JSON representation of all members of the installedSoftwareVersion <br> collection. |

### Query a specific installedSoftwareVersion instance

| Header | Accept: application/json <br> Content-Type: application/json |
| :-- | :-- |
| Method and URI | GET /api/instances/installedSoftwareVersion/vid= <br> where rid is the unique identifier of the installedSoftwareVersion instance to query. |
| Request body arguments | None |
| Successful return status | $230 \mathrm{~V} \mathrm{~K}$ |
| Successful response body | DIDB representation of a specific installedSoftwareVersion <br> instance |

## Login Session Info

Information about a REST API login session.

## Supported operations

Collector query, Instance query, Logout
Attributes

| Attribute | Type | Description |
| :-- | :-- | :-- |
| id | String | Unique identifier of the loginSessionInfo instance. |
| domain | String | Domain of the user logged into this session. |
| user | user | Information about the user logged into this session, as <br> defined by the user resource type. |
| index | List index | List of roles for the user logged into this session, as <br> defined by the role resource type. |
| idleTimeout | unsigned Integer[ID(seconds)] | Number of seconds after last use until this session expires. |
| isPasswordChangeRequired | Boolean | Indicates if the user needs to change their password. |

![img-7.jpeg](img-7.jpeg)

# Query all members of the loginSessionInfo collection

| Header | Accept: application/json <br> Content-Type: application/json |
| :-- | :-- |
| Method and URI | GET /api/types/ingin/sessionInfo/instances |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of all members of the loginSessionInfo <br> collection. |

Query a specific loginSessionInfo instance

| Header | Accept: application/json <br> Content-Type: application/json |
| :-- | :-- |
| Method and URI | GET/api/instances/ingin/sessionInfo/vid- <br> where <sb> is the unique identifier of the loginSessionInfo instance to query. |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of a specific loginSessionInfo instance. |

## Logout operation

Log out of the session.

| Header | Accept: application/json <br> Content-Type: application/json |
| :-- | :-- |
| Method and URI | POST /api/types/loginSessionInfo/action/logout |
| Request body arguments | See the arguments table below. |
| Successful return status | 200 OK |
| Successful response body | JSON representation of the returned attributes. |

Arguments for the Logout operation

| Argument | $\mathbf{b c}$ <br> out | Type | Required? | Description |
| :-- | :-- | :-- | :-- | :-- |
| localCleanupOnly | $\mathrm{in}$ | Boolean | Optimal | Indicates whether to log out of all REST API sessions authenticated <br> by the Token Granting Token (TGT) with which this session was <br> established. |
|  |  |  |  | Values are: |
|  |  |  |  | - true - Log out of this session only. |
|  |  |  |  | - false - Log out of all sessions. |
| logoutOK | out | String | N/A | Indicates successful logout |


## User

Information about local users, including their roles, and how they are authenticated.

## Supported operations

Collection query, Instance query, Create_Delete _Modify
Attributes

| Attribute | Type | Description |
| :-- | :-- | :-- |
| id | String | Unique identifier of the user instance. |
| name | String | Name of the user. |
| role | role | User role as defined by the role resource type. |

Query all members of the user collection

| Header | Accept: application/json <br> Content-Type: application/json |
| :-- | :-- |
| Method and URI | GET /api/types/user/instances |
| Request body arguments | None |
| Successful return status | 220 OR |
| Successful response body | JSON representation of all members of the user collection.. |

Query a specific user instance

| Header | Accept: application/json <br> Content-Type: application/json |
| :--: | :--: |
| Method and URI | GET /api/instances/user/<id> where:idb: is the unique identifier of the user instance to query. |
|  | Or |
|  | GET /api/instances/user/name><value> where:value: is the name of the user instance to query. |
| Request body arguments | None |
| Successful return status | 220 OR |
| Successful response body | JSON representation of a specific user instance. |

## Create operation

Create a local user. When you create a local user, the system automatically creates a rolefilapping resource for that user, based on the value of the role attribute.

Use the nis6happing resource type to create authentication for LDAP users and LDAP groups, as described in the associated help topic.

| Header | Accept: application/json <br> Content-Type: application/json |
| :-- | :-- |
| Method and URI | W  /api/types/user/outances |
| Request body arguments | See the arguments table below. |
| Successful return status | 201 Created, 202 Accepted (async response) |
| Successful response body | 2000 representation of the <id> attribute |

Arguments for the Create operation

| Argument | In/ out | Type | Required? | Description |
| :--: | :--: | :--: | :--: | :--: |
| id | out | user | N/A | Unique identifier for the new user. |
| name | In | String | Required | User name. |
| role | In | String | Required | User role. |
| password | In | String | Required | Initial password for the user. <br> The value must match all of following regex expressions <br> $\cdot$ "(?/="id)/?\"[\#]\}(?\"\[w]\}?\="[\#-c]\}?\="[\#-Z]\} \text { (R-M)\$ }$ |

Delete operation
Delete a local user. When you delete a local user, the system also deletes the nis6happing resource associated with the user.

| Header | Accept: application/json <br> Content-Type: application/json |
| :--: | :--: |
| Method and URI | DELETE /api/outances/user/<id> where <id> is the unique identifier of the user instance to delete. |
|  | Or |
|  | DELETE /api/instances/user/name:<value> <br> where <value> is the name of the user instance to delete. |
| Request body arguments | Note |
| Successful return status | 204 No Content, 202 Accepted (async response) |
| Successful response body | No body content.. |

# Modify operation

Change the local user's password or/and role.
Use the nis6happing resource type to change the access pre/enges for LDAP users and LDAP groups, as described in the associated help topic.

| Header | Accept: application/json <br> Content-Type: application/json |
| :--: | :--: |
| Method and URI | W 消 //api/outances/user/<id>/action/modify <br> where <id> is the unique identifier of the user instance. |
|  | Or |
|  | POPT /api/outances/user/cases->value>/action/modify <br> where <value> is the name of the user instance. |
| Request body arguments | See the arguments table below. |
| Successful return status | 204 No Content, 202 Accepted (async response) |
| Successful response body | No body content.. |

## Candidate Software Version

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
| 7 | Upgrade_Acknowledged | Upgrade session was acknowledged. |
| 8 | Upgrade_Waiting_For_User | Upgrade session is waiting for user action to continue the <br> upgrade |
| 9 | Upgrade_Paused_Lock | Upgrade session is paused past the point of cancellation. |

## UpgradeTypeEnum

| Value | Enumeration |
| :-- | :-- |
| 0 | Software |
| 1 | Firmware |
| 2 | LanguagePack |

## Software Upgrade Session

Information about a storage system upgrade session.

Create an upgrade session to upprade the system software or view existing upprade sessions. The upgrade sessions installs an uporade candidate file ryslem. Download the hast Support website. Use the CLI to upload the upgrade candidate to the system before creating the upgrade session. For information, see theUnisphere CLI User Guide.

The latest software upgrade candidate contains all available hot fixes. If you have applied hot fixes to your system, the hot fixes are included in the latest upgrade candidate.

Note: All system components must be healthy prior to upgrading the system software. If any system components are degraded, the software update will fail

### Embedded resource types

upgradeMessage, upgradeTask

### Supported operations

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

#### Attributes for upgradeMessage

A message occurrence. This is also the message object returned in the body of non-2xx return code REST responses.

| Attribute | Type | Description |
| --- | --- | --- |
| errorCode | String | Error code for this message. |
| messages | List<localizedMessage> | List of localized messages. |
| severity | SeverityEnum | Severity level associated with this message. |
| httpStatus | unsigned Integer[32] | HTTP status code for this message. |

#### Attributes for upgradeTask

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

### Create operation

Start a session to upgrade the system software with an uploaded upgrade candidate

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST /api/types/softwareUpgradeSession/instances |
| Request body arguments | See the arquments table below. |
| Successful return status | 201 Created |
| Successful response body | JSON representation of the <id> attribute |

#### Arguments for the Create operation

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

### VerifyUpgradeEligibility operation

Validate that the system is in a healthy state. This is required for an upgrade is started. You can use this operation to peration to perdion to perdion to perdion no perfo

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST |
|  | /api/types/softwareUpgradeSession/action/verifyUpgradeEligibility |
| Request body arguments | See the arguments table below. |
| Successful return status | 200 OK, 202 Accepted (async response) |
| Successful response body | JSON representation of the returned attributes. |

#### Arguments for the VerifyUpgradeEligibility operation

| Arqument | In/ | Type | Required? | Description |
| --- | --- | --- | --- | --- |
|  | out |  |  |  |
| messages | out | List < upgradeMessage> | N/A | List of embedded upgradeMessage which contain the info |
|  |  |  |  | of message's identifier, localized text, severity and so on. |

### Resume operation

Resume a session that is currently in paused, failed, or failed_lock state.

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI POST | /api/instances/softwareUpgradeSession/<id>/action/resume |
|  | where <id> is the unique identifier of the softwareUpgradeSession instance. |
| Request body arguments None |  |
| Successful return status | 204 No Content |
| Successful response body | No body content. |

## **Uploading upgrade candidates and language packs**

You can upload upgrade candidates (software or firmware) and language packs to the storage system to make them available to install. To install an uploaded file, create a new candidateSoftwareVersion instance.

**NOTE:** When you upload an upgrade candidate file onto the storage system, it replaces the previous version. There can only be one upgrade candidate on the system at a time.

For information about the candidateSoftwareVersion resource type, see the *Unisphere Management REST API Reference Guide*.

### Syntax

To upload a system software upgrade candidate or language pack file, use the following components:

| Headers     | Accept: application/json<br>Content-Type: application/json<br>X-EMC-REST-CLIENT: true<br>EMC-CSRF-TOKEN: <token></token>                                                                                                                                                                                                                          |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Operation   | POST                                                                                                                                                                                                                                                                                                                                              |
| URI pattern | /upload/files/types/candidateSoftwareVersion                                                                                                                                                                                                                                                                                                      |
| Body        | Empty.                                                                                                                                                                                                                                                                                                                                            |
| Usage       | You must post the upgrade file using a multipart/form-data format as if from a simple web page form, like<br>that shown in the following example:                                                                                                                                                                                                 |
|             | ```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<body>
<form enctype="multipart/form-data" method="post" action="https://<ip_address>/upload/files/types/candidateSoftwareVersion">
<input name="file" type="file"/>
<input type="submit"/>
</form>
</body>
</html>
``` |

A successful upload request returns 200 OK HTTP status code. If the request does not succeed, the server returns a 4*nn* or 5*nn* HTTP status code in the response header and a message entity in the response body.


## Appendix A: Example Response

In Dell Unity REST API, the JSON responses typically follow a specific structure that includes metadata, links, and entries. This structure is consistent across many endpoints and is designed to provide both the requested data and navigational links for pagination or related resources.

### Typical Response Structure

```json
{
    "@base": "https://127.0.0.1:8000/api/types/user/instances?per_page=2000",
    "updated": "2020-08-27T01:39:17.471Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "https://127.0.0.1:8000/api/instances/user",
            "content": {
                "id": "user_admin"
            },
            "links": [
                {
                    "href": "/user_admin",
                    "rel": "self"
                }
            ],
            "updated": "2020-08-27T01:39:17.471Z"
        }
    ]
}
```

### Explanation of Each Field

1. **`@base`**:
   - This field provides the base URL for the resource type being queried.
   - It often includes query parameters like `per_page` to indicate how many items are returned per page.

2. **`updated`**:
   - A timestamp indicating when the resource was last updated.

3. **`links`**:
   - Contains navigation links, such as:
     - `rel`: Indicates the relationship of the link (e.g., `self` for the current resource).
     - `href`: The URL or relative path to access the resource or additional pages.

4. **`entries`**:
   - A list of individual resources (or objects) returned by the query.
   - Each entry includes:
     - **`@base`**: The base URL for this specific instance.
     - **`content`**: Contains the actual data fields for this resource (e.g., `id`, `name`, etc.).
     - **`links`**: Navigation links specific to this object, such as its `self` link.
     - **`updated`**: A timestamp for when this specific object was last updated.

### Example in Context: `/api/types/basicSystemInfo/instances`

For an endpoint like `/api/types/basicSystemInfo/instances`, the response would follow a similar structure but with fields relevant to system information. For example:

```json
{
    "@base": "https://127.0.0.1:8000/api/types/basicSystemInfo/instances?per_page=2000",
    "updated": "2025-01-23T12:00:00.000Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "https://127.0.0.1:8000/api/instances/basicSystemInfo",
            "content": {
                "id": "system_1",
                "name": "UnityStorage01",
                "model": "Unity 300F",
                "serialNumber": "SN123456789",
                "firmwareVersion": "5.2.0",
                "status": "online"
            },
            "links": [
                {
                    "href": "/system_1",
                    "rel": "self"
                }
            ],
            "updated": "2025-01-23T12:00:00.000Z"
        }
    ]
}
```

### Key Takeaways
- The response is always wrapped in metadata (`@base`, `updated`, `links`) and contains an array of `entries`.
- The actual data resides within the `content` field inside each entry.
- Pagination and navigation are handled via `links`.

This consistent structure makes it easier to parse and navigate through Dell Unity REST API responses programmatically!


## Appendix B: Example Cookie

### Example Cookie Value
```plaintext
mod_sec_emc=OLFzMrMXiCenpFdYZ167MoRvVSOc8Dm-vaMpdcJmmak; HttpOnly; Path=/; SameSite=lax; Secure
```

### Explanation of Cookie Components
- **`mod_sec_emc`**: This is the name of the cookie, which is often used for session management.
- **`OLFzMrMXiCenpFdYZ167MoRvVSOc8Dm-vaMpdcJmmak`**: This is the actual value of the cookie, which is a unique identifier for the session.
- **`HttpOnly`**: This attribute indicates that the cookie is not accessible via JavaScript, enhancing security.
- **`Path=/`**: This specifies that the cookie is valid for all paths on the domain.
- **`SameSite=lax`**: This attribute helps prevent CSRF attacks by controlling how cookies are sent with cross-site requests.
- **`Secure`**: This attribute ensures that the cookie is only sent over HTTPS connections.

### Additional Context
The Dell EMC Unity API uses cookie-based authentication, meaning that cookies are essential for maintaining sessions and authenticating requests. When making API calls, you may encounter multiple cookies, including session identifiers and CSRF tokens, which are critical for secure interactions with the API [6][7].

## Appendix C: Real API Interaction Record

 ```bash

 [root@mDA11 ~]# curl -s -k -L -X GET ${HOST}/api/types/basicSystemInfo/instances | python3 -m json.tool
{
    "@base": "${HOST}api/types/basicSystemInfo/instances?per_page=2000",
    "updated": "2025-02-28T08:20:38.636Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "${HOST}api/instances/basicSystemInfo",
            "updated": "2025-02-28T08:20:38.636Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/0"
                }
            ],
            "content": {
                "id": "0",
                "model": "Unity 380F",
                "name": "CKM01204905476",
                "softwareVersion": "5.3.0",
                "softwareFullVersion": "Unity 5.3.0.0 (Release, Build 120, 2023-03-18 19:02:01, 5.3.0.0.5.120)",
                "apiVersion": "13.0",
                "earliestApiVersion": "4.0"
            }
        }
    ]
}

[root@mDA11 ~]# curl -s -k -L -X GET ${HOST}/api/types/loginSessionInfo/instances -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true"
{"@base":"${HOST}api/types/loginSessionInfo/instances?per_page=2000","updated":"2025-02-28T08:23:01.645Z","links":[{"rel":"self","href":"&page=1"}],"entries":[{"@base":"${HOST}api/instances/loginSessionInfo","updated":"2025-02-28T08:23:01.645Z","links":[{"rel":"self","href":"/user"}],"content":{"roles":[{"id":"administrator"}],"domain":"local","user":{"id":"user_user"},"id":"user","idleTimeout":3600,"isPasswordChangeRequired":false}}]}[root@mDA11 ~]# curl -s -k -L -X GET ${HOST}/api/types/loginSessionInfo/instances -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" | python3 -m json.tool
{
    "@base": "${HOST}api/types/loginSessionInfo/instances?per_page=2000",
    "updated": "2025-02-28T08:23:13.307Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "${HOST}api/instances/loginSessionInfo",
            "updated": "2025-02-28T08:23:13.307Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/user"
                }
            ],
            "content": {
                "roles": [
                    {
                        "id": "administrator"
                    }
                ],
                "domain": "local",
                "user": {
                    "id": "user_user"
                },
                "id": "user",
                "idleTimeout": 3600,
                "isPasswordChangeRequired": false
            }
        }
    ]
}

[root@mDA11 ~]# curl -s -k -L -X GET ${HOST}/api/types/users/instances -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" | python3 -m json.tool
{
    "error": {
        "errorCode": 131149829,
        "httpStatusCode": 404,
        "messages": [
            {
                "en-US": "The requested resource does not exist. (Error Code:0x7d13005)"
            }
        ],
        "created": "2025-02-28T08:23:58.041Z"
    }
}
[root@mDA11 ~]# curl -s -k -L -X GET ${HOST}/api/types/user/instances -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" | python3 -m json.tool
{
    "@base": "${HOST}api/types/user/instances?per_page=2000",
    "updated": "2025-02-28T08:24:24.181Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "${HOST}api/instances/user",
            "updated": "2025-02-28T08:24:24.181Z",
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
            "@base": "${HOST}api/instances/user",
            "updated": "2025-02-28T08:24:24.181Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/user_diagnose"
                }
            ],
            "content": {
                "id": "user_diagnose"
            }
        },
        {
            "@base": "${HOST}api/instances/user",
            "updated": "2025-02-28T08:24:24.181Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/user_user"
                }
            ],
            "content": {
                "id": "user_user"
            }
        }
    ]
}

}
[root@mDA11 ~]# curl -s -k -L -X GET ${HOST}/api/types/candidateSoftwareVersion/instances -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" | python3 -m json.tool
{
    "@base": "${HOST}api/types/candidateSoftwareVersion/instances?per_page=2000",
    "updated": "2025-02-28T08:25:49.047Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": []
}
[root@mDA11 ~]# curl -s -k -L -X GET ${HOST}/api/types/upgradeSession/instances -u "admin:Password123!" -c cookie.jar -H "X-EMC-REST-CLIENT: true" | python3 -m json.tool
{
    "@base": "${HOST}api/types/upgradeSession/instances?per_page=2000",
    "updated": "2025-02-28T08:26:02.006Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "${HOST}api/instances/upgradeSession",
            "updated": "2025-02-28T08:26:02.006Z",
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

{
    "@base": "${HOST}api/types/upgradeSession/instances?fields=status,caption,percentComplete,tasks&per_page=2000",
    "updated": "2025-02-28T11:10:17.533Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
                "content": {
                "id": "Upgrade_5.3.0.120",
                "status": 1,
                "caption": "Upgrade_5.3.0.120",
                "percentComplete": 16,
                "tasks": [
                    {
                        "status": 2,
                        "type": 0,
                        "caption": "Preparing system",
                        "creationTime": "2025-02-28T11:03:58.832Z",
                        "estRemainTime": "00:03:30.000"
                    },
                    {
                        "status": 2,
                        "type": 0,
                        "caption": "Performing health checks",
                        "creationTime": "2025-02-28T11:05:03.082Z",
                        "estRemainTime": "00:01:10.000"
                    },
                    {
                        "status": 1,
                        "type": 0,
                        "caption": "Preparing system software",
                        "creationTime": "2025-02-28T11:10:16.391Z",
                        "estRemainTime": "00:16:10.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Waiting for reboot command",
                        "creationTime": "2025-02-28T11:01:54.381Z",
                        "estRemainTime": "00:00:05.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Performing health checks",
                        "creationTime": "2025-02-28T11:01:54.381Z",
                        "estRemainTime": "00:01:05.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Installing new software on peer SP",
                        "creationTime": "2025-02-28T11:01:54.381Z",
                        "estRemainTime": "00:16:50.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Rebooting peer SP",
                        "creationTime": "2025-02-28T11:01:54.381Z",
                        "estRemainTime": "00:14:15.000"
                    },
                                       {
                        "status": 0,
                        "type": 0,
                        "caption": "Restarting services on peer SP",
                        "creationTime": "2025-02-28T11:01:54.382Z",
                        "estRemainTime": "00:05:00.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Installing new software on primary SP",
                        "creationTime": "2025-02-28T11:01:54.382Z",
                        "estRemainTime": "00:13:30.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Rebooting the primary SP",
                        "creationTime": "2025-02-28T11:01:54.382Z",
                        "estRemainTime": "00:13:55.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Restarting services on primary SP",
                        "creationTime": "2025-02-28T11:01:54.382Z",
                        "estRemainTime": "00:05:10.000"
                    },
                    {
                        "status": 0,
                        "type": 0,
                        "caption": "Final tasks",
                        "creationTime": "2025-02-28T11:01:54.382Z",
                        "estRemainTime": "00:00:45.000"
                    }
                ]
            }
        }
    ]
}

   31  (2025-02-28 10:22:04 CET) time curl -s -k -L -X POST ${HOST}/api/types/upgradeSession/action/verifyUpgradeEligibility -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: d2nFivGgU8EiztUJ6IlsFwStrS+s59RxdKTX1mqvuFnOUz2fiwy1slHlItOu9ET003xOjsJFX+E9UE6jFxck4Ffo/Km9AJj13dsyt/7PkZQ=" -v

   59  (2025-02-28 11:16:45 CET) time uemcli -d 146.106.142.250 -u user -p Password123! -upload -f /sdev_shared/swint/WLT_SWINT/EXE5000/SICSv3/NAS/Unity-5.3.0.0.5.120.tgz.bin.gpg upgrade -sslPolicy accept

      26  (2025-02-28 10:02:42 CET) time curl -s -k -L -X POST ${HOST}/upload/files/types/candidateSoftwareVersion -b cookie.jar -H "X-EMC-REST-CLIENT: true" -H "EMC-CSRF-TOKEN: d2nFivGgU8EiztUJ6IlsFwStrS+s59RxdKTX1mqvuFnOUz2fiwy1slHlItOu9ET003xOjsJFX+E9UE6jFxck4Ffo/Km9AJj13dsyt/7PkZQ=" -H "multipart/form-data" -F filename=@/sdev_shared/swint/WLT_SWINT/EXE5000/SICSv3/NAS/Unity-5.3.0.0.5.120.tgz.bin.gpg

curl -s -k -L -X 'GET' '${HOST}/api/types/installedSoftwareVersion/instances?fields=driveFirmware' -u "admin:Password123!@" -c cookie.jar -H 'X-EMC-REST-CLIENT: true' -H "Accept: application/json" -H "Content-Type: application/json"   | python3 -m json.tool
{
    "@base": "${HOST}/api/types/installedSoftwareVersion/instances?fields=driveFirmware&per_page=2000",
    "updated": "2025-03-13T09:49:22.072Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "${HOST}/api/instances/installedSoftwareVersion",
            "updated": "2025-03-13T09:49:22.072Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/5.3.0.0.5.120"
                }
            ],
            "content": {
                "id": "5.3.0.0.5.120",
                "driveFirmware": [
                    {
                        "name": "Unity-Drive-Firmware-V20-2022-06-13.tgz.bin.gpg",
                        "version": "4.3.0.1499782821",
                        "releaseDate": "2022-06-13T23:24:01.000Z",
                        "upgradableDriveCount": 0,
                        "estimatedTime": 0,
                        "isNewerVersion": false
                    }
                ]
            }
        }
    ]
}

curl -s -k -L -X 'GET' 'https://146.106.142.250/api/types/loginSessionInfo/instances' -u "admin:Password123!" -c cookie.jar -H 'X-EMC-REST-CLIENT: true' -H "Accept: application/json" -H "Content-Type: application/json"   | python3 -m json.tool
{
    "@base": "$HOST/api/types/loginSessionInfo/instances?per_page=2000",
    "updated": "2025-03-13T10:15:38.600Z",
    "links": [
        {
            "rel": "self",
            "href": "&page=1"
        }
    ],
    "entries": [
        {
            "@base": "$HOST/api/instances/loginSessionInfo",
            "updated": "2025-03-13T10:15:38.600Z",
            "links": [
                {
                    "rel": "self",
                    "href": "/admin"
                }
            ],
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
                "id": "admin",
                "isPasswordChangeRequired": false
            }
        }
    ]
}

```
