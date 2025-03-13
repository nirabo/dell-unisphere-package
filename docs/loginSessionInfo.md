## loginSessionInfo

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
| idieTimeout | unsigned Integer[ID(seconds)] | Number of seconds after last use until this session expires. |
| idPasswordChangeRequired | Boolean |  |

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
