# systemInformation

### Contact information for storage system.

Supported operations

Collection query , Instance query ,Modify

#### Attributes

| Attribute | Type | Description |
| --- | --- | --- |
| id | String | Unique identifier of the systemInformation instance. |
| contactFirstName | String | Contact first name for the storage system. |
| contactLastName | String | Contact last name for the storage system. |
| contactCompany | String | Contact company name for the storage system. |
| contactPhone | String | Phone number for the person who should be contacted by the |
|  |  | service provider for service issues. |
| contactEmail | String | Contact email address for the storage system. |
| locationName | String | The physical location of this system within the user's environment. |
|  |  | For example: Building C, lab 5, tile C25 |
| streetAddress | String | Street address for the storage system. |
| city | String | City where the storage system resides. |
| state | String | State where the storage system resides. |
| zipcode | String | Zip code or postal code where the storage system resides. -- eng |
|  |  | Zip Code is not currently supported by the ESRS VE system |
|  |  | information api |
| country | String | Country where the storage system resides. |
| siteld | String | The ID identifying the site where this system is installed. |
| contactMobilePhone | String | Mobile phone number for the person who should be contacted by |
|  |  | the service provider for service issues. |

### Query all members of the systemInformation collection

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI GET | /api/types/systemInformation/instances |
| None Request body arguments |  |
|  | 200 OK |
| Successful return status |  |
| Successful response body | JSON representation of all members of the systemInformation |
|  | collection. |

## Query a specific systemInformation instance

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | GET /api/instances/systemInformation/<id> |
|  | where <id> is the unique identifier of the systemInformation instance to query. |
| Request body arguments | None |
| Successful return status | 200 OK |
| Successful response body | JSON representation of a specific systemInformation instance. |

# Modify operation

Modify cotact and location information for the storage system displayed in Unisphere Central.

| Header | Accept: application/json |
| --- | --- |
|  | Content - Type: application/json |
| Method and URI | POST /api/instances/systemInformation/<id>/action/modify |
|  | where <id> is the unique identifier of the systemInformation instance. |
| Request body arguments | See the arquments table below. |
| Successful return status | 204 No Content, 202 Accepted (async response) |
| Successful response body | No body content. |

#### Arguments for the Modify operation

| Argument | In/ out | Type | Required? | Description |
| --- | --- | --- | --- | --- |
| contactFirstName | in | String | Optional |  |
| contactLastName | in | String | Optional |  |
| contactEmail | in | String | Optional |  |
| contactPhone | in | String | Optional |  |
| locationName | in | String | Optional |  |
| contactMobilePhone | in | String | Optional |  |
