 ```
 
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

```