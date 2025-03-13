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
|             | HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"<br><html><br/><body><br/><form <br="" enctype="multipart/form-data" method="post">action="https://<ip_address>/upload/file/types/<br/>candidateSoftwareVersion"&gt;<br/><input name="filename&gt;" type="file"/><br/><input type="submit"/><br/></ip_address></form><br/></body><br/></html> |

A successful upload request returns 200 OK HTTP status code. If the request does not succeed, the server returns a 4*nn* or 5*nn* HTTP status code in the response header and a message entity in the response body.
