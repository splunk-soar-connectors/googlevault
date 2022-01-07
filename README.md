[comment]: # "Auto-generated SOAR connector documentation"
# Google Vault

Publisher: Splunk  
Connector Version: 2\.0\.8  
Product Vendor: Google  
Product Name: Google Vault  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.0\.0  

This app supports the actions to perform eDiscovery and provide a compliance solution for G Suite, allowing customers to retain, hold, search, and export their data

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2019-2021 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
### Service Account

This app requires a pre-configured service account to operate. Please follow the procedure outlined
at [this link](https://support.google.com/a/answer/7378726?hl=en) to create a service account.  
The following APIs will need to be enabled:

-   AdminSDK
-   G Suite Vault API

At the end of the creation process, the admin console should ask you to save the config as a JSON
file. Copy the contents of the JSON file in the clipboard and paste it as the value of the "Contents
of Service Account JSON file" asset configuration parameter.

### Scopes

Once the service account has been created and APIs enabled, the next step is to configure scopes on
these APIs to allow the App to access them. Every action requires different scopes to operate, these
are listed in the action documentation.  
To enable scopes please complete the following steps:

-   Go to your G Suite domain's [Admin console.](http://admin.google.com/)
-   Select **Security** from the list of controls. If you don't see **Security** listed, select
    **More controls** from the gray bar at the bottom of the page, then select **Security** from the
    list of controls. If you can't see the controls, make sure you're signed in as an administrator
    for the domain.
-   Select **Show more** and then **Advanced settings** from the list of options.
-   Select **Manage API client access** in the **Authentication** section.
-   In the **Client Name** field enter the service account's **Client ID** . You can find your
    service account's client ID in the [Service accounts credentials
    page](https://console.developers.google.com/apis/credentials) or the service account JSON file
    (key named **client_id** ).
-   In the **One or More API Scopes** field enter the list of scopes that you wish to grant access
    to the App. For example, to enable all the scopes required by this app enter:
    https://www.googleapis.com/auth/ediscovery, https://www.googleapis.com/auth/ediscovery.readonly,
    https://www.googleapis.com/auth/admin.directory.orgunit,
    https://www.googleapis.com/auth/admin.directory.orgunit.readonly,
    https://www.googleapis.com/auth/admin.directory.group,
    https://www.googleapis.com/auth/admin.directory.group.readonly,
    https://www.googleapis.com/auth/admin.directory.group.member.readonly,
    https://www.googleapis.com/auth/admin.directory.group.member
-   Click **Authorize** .

### Notes

-   If the user provides Organization ID of the root level organization instead of the child
    organizations (in which export is to be created) in the action **create export** , API might
    throw an error **'Domain wide search is disabled'** or **'Select an organizational unit other
    than the root'** based on the configurations of the Google Vault.

### pyasn1

Copyright (c) 2005-2019, Ilya Etingof All rights reserved. Redistribution and use in source and
binary forms, with or without modification, are permitted provided that the following conditions are
met: \* Redistributions of source code must retain the above copyright notice, this list of
conditions and the following disclaimer. \* Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS
AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

### google-auth

This library simplifies using Google's various server-to-server authentication mechanisms to access
Google APIs. Apache License Version 2.0, January 2004. http://www.apache.org/licenses/

### google-api-python-client

This is the Python client library for Google's discovery based APIs. These client libraries are
officially supported by Google. However, the libraries are considered complete and are in
maintenance mode. This means that we will address critical bugs and security issues but will not add
any new features. Copyright 2014 Google Inc. All Rights Reserved. Licensed under the Apache License,
Version 2.0 (the "License"); you may not use this file except in compliance with the License. You
may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0

### oauth2client

This is a client library for accessing resources protected by OAuth 2.0. Apache License Version 2.0,
January 2004. http://www.apache.org/licenses/

### google-auth-oauthlib

This library provides oauthlib integration with google-auth. Apache License Version 2.0, January
2004. http://www.apache.org/licenses/


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Google Vault asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**login\_email** |  required  | string | Login email
**key\_json** |  required  | password | Contents of service account JSON file

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[list matters](#action-list-matters) - List all open, closed, and deleted matters  
[create matter](#action-create-matter) - Create a matter with OPEN state  
[get matter](#action-get-matter) - Fetch information for the given matter ID  
[close matter](#action-close-matter) - Move a matter to the CLOSED state  
[delete matter](#action-delete-matter) - Move a matter to the DELETED state  
[reopen matter](#action-reopen-matter) - Reopens a matter to move it from CLOSED to OPEN state  
[restore matter](#action-restore-matter) - Restores a matter to move it from DELETED to CLOSED state  
[list holds](#action-list-holds) - List all holds for the given matter ID  
[create hold](#action-create-hold) - Create a hold within the given matter ID  
[delete hold](#action-delete-hold) - Delete a hold  
[remove held account](#action-remove-held-account) - Remove held account from the given hold ID  
[add held account](#action-add-held-account) - Add held account to the given hold ID  
[list exports](#action-list-exports) - List all exports for the given matter ID  
[get export](#action-get-export) - Get information of an export from the given matter ID  
[create export](#action-create-export) - Perform a search based on the provided criteria and create an export for the search results  
[list organizations](#action-list-organizations) - List all organizations  
[list groups](#action-list-groups) - List all groups of a domain  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list matters'
List all open, closed, and deleted matters

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**state** |  optional  | Type of matters to be retrieved | string | 
**limit** |  optional  | Maximum number of matters to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.state | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.summary\.total\_matters\_returned | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create matter'
Create a matter with OPEN state

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Matter name | string | 
**description** |  required  | Matter description | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.description | string | 
action\_result\.parameter\.name | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.summary\.name | string | 
action\_result\.summary\.description | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get matter'
Fetch information for the given matter ID

Type: **investigate**  
Read only: **True**

There are two views of a matter\: BASIC \(default\) and FULL\. The FULL view adds matter permissions in addition to the data received in the BASIC view\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**view** |  optional  | View of matter | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.parameter\.view | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.matterPermissions\.\*\.accountId | string |  `gsvault user account id` 
action\_result\.data\.\*\.matterPermissions\.\*\.role | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'close matter'
Move a matter to the CLOSED state

Type: **generic**  
Read only: **False**

You can close the matter only if it is in the OPEN state\. If the matter is in the OPEN state and contains any holds, then, to close the matter all holds must be deleted\. For this, you have to checkmark the <b>Delete all holds</b> parameter and run the action\. If you keep the parameter unchecked and run the action, it will fail due to undeleted holds in the matter\. In that case, the user has to delete all the holds manually; run this action after that to close the matter\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**delete\_all\_holds** |  optional  | Delete all holds | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.delete\_all\_holds | boolean | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.matter\.description | string | 
action\_result\.data\.\*\.matter\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.matter\.name | string | 
action\_result\.data\.\*\.matter\.state | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete matter'
Move a matter to the DELETED state

Type: **generic**  
Read only: **False**

You can delete the matter only if it is in the CLOSED state\. If the matter is in the OPEN state and contains any holds, then, to delete it all holds must be deleted and the matter must be moved to the CLOSED state\. For this, you have to checkmark the 'Delete all holds' parameter and run the action\. By doing this, action will close the matter after deleting all the holds \(if any\) associated with it and move it to the DELETED state\. If you keep the parameter unchecked and run the action, it will fail due to the matter not being in the CLOSED state\. In that case, the user has to move the matter to the CLOSED state by manually deleting all the associated holds; run this action after that to delete the matter\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**delete\_all\_holds** |  optional  | Delete all holds | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.delete\_all\_holds | boolean | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'reopen matter'
Reopens a matter to move it from CLOSED to OPEN state

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.matter\.description | string | 
action\_result\.data\.\*\.matter\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.matter\.name | string | 
action\_result\.data\.\*\.matter\.state | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'restore matter'
Restores a matter to move it from DELETED to CLOSED state

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.state | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list holds'
List all holds for the given matter ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**limit** |  optional  | Maximum number of holds to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.accounts\.\*\.accountId | string |  `gsvault user account id`  `gsvault group account id` 
action\_result\.data\.\*\.accounts\.\*\.email | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
action\_result\.data\.\*\.accounts\.\*\.firstName | string | 
action\_result\.data\.\*\.accounts\.\*\.holdTime | string | 
action\_result\.data\.\*\.accounts\.\*\.lastName | string | 
action\_result\.data\.\*\.corpus | string | 
action\_result\.data\.\*\.holdId | string |  `gsvault hold id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.orgUnit\.holdTime | string | 
action\_result\.data\.\*\.orgUnit\.orgUnitId | string |  `gsvault org unit id` 
action\_result\.data\.\*\.query\.driveQuery\.includeSharedDriveFiles | boolean | 
action\_result\.data\.\*\.query\.driveQuery\.includeTeamDriveFiles | boolean | 
action\_result\.data\.\*\.query\.groupsQuery\.endTime | string | 
action\_result\.data\.\*\.query\.groupsQuery\.startTime | string | 
action\_result\.data\.\*\.query\.groupsQuery\.terms | string | 
action\_result\.data\.\*\.query\.mailQuery\.endTime | string | 
action\_result\.data\.\*\.query\.mailQuery\.startTime | string | 
action\_result\.data\.\*\.query\.mailQuery\.terms | string | 
action\_result\.data\.\*\.updateTime | string | 
action\_result\.summary\.total\_holds\_returned | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create hold'
Create a hold within the given matter ID

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Hold name | string | 
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**type** |  required  | Type of the hold | string | 
**search\_method** |  required  | Scope of search | string | 
**org\_unit\_id** |  optional  | Organization ID | string |  `gsvault org unit id` 
**user\_email\_ids** |  optional  | Comma\-separated list of user emails | string |  `gsvault user email ids`  `email` 
**group\_account\_ids** |  optional  | Comma\-separated list of group IDs | string |  `gsvault group account ids` 
**terms** |  optional  | Conditions to be met for a message to be covered by this hold | string | 
**start\_time** |  optional  | Start time \(%Y\-%m\-%dT%H\:%M\:%SZ\) | string | 
**end\_time** |  optional  | End time \(%Y\-%m\-%dT%H\:%M\:%SZ\) | string | 
**include\_shared\_drive\_files** |  optional  | Include files from associated shared drives | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.end\_time | string | 
action\_result\.parameter\.group\_account\_ids | string |  `gsvault group account ids` 
action\_result\.parameter\.include\_shared\_drive\_files | boolean | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.parameter\.name | string | 
action\_result\.parameter\.org\_unit\_id | string |  `gsvault org unit id` 
action\_result\.parameter\.search\_method | string | 
action\_result\.parameter\.start\_time | string | 
action\_result\.parameter\.terms | string | 
action\_result\.parameter\.type | string | 
action\_result\.parameter\.user\_email\_ids | string |  `gsvault user email ids`  `email` 
action\_result\.data\.\*\.accounts\.\*\.accountId | string |  `gsvault user account id`  `gsvault group account id` 
action\_result\.data\.\*\.accounts\.\*\.email | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
action\_result\.data\.\*\.accounts\.\*\.firstName | string | 
action\_result\.data\.\*\.accounts\.\*\.holdTime | string | 
action\_result\.data\.\*\.accounts\.\*\.lastName | string | 
action\_result\.data\.\*\.corpus | string | 
action\_result\.data\.\*\.holdId | string |  `gsvault hold id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.orgUnit\.holdTime | string | 
action\_result\.data\.\*\.orgUnit\.orgUnitId | string |  `gsvault org unit id` 
action\_result\.data\.\*\.query\.driveQuery\.includeSharedDriveFiles | boolean | 
action\_result\.data\.\*\.query\.driveQuery\.includeTeamDriveFiles | boolean | 
action\_result\.data\.\*\.query\.groupsQuery\.endTime | string | 
action\_result\.data\.\*\.query\.groupsQuery\.startTime | string | 
action\_result\.data\.\*\.query\.groupsQuery\.terms | string | 
action\_result\.data\.\*\.query\.mailQuery\.endTime | string | 
action\_result\.data\.\*\.query\.mailQuery\.startTime | string | 
action\_result\.data\.\*\.query\.mailQuery\.terms | string | 
action\_result\.data\.\*\.updateTime | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete hold'
Delete a hold

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**hold\_id** |  required  | Hold ID | string |  `gsvault hold id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.hold\_id | string |  `gsvault hold id` 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'remove held account'
Remove held account from the given hold ID

Type: **generic**  
Read only: **False**

A held account can only be removed from the given hold\_id if the search\_method of the hold is either USER\_ACCOUNT or GROUP\_ACCOUNT\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**hold\_id** |  required  | Hold ID | string |  `gsvault hold id` 
**account\_id** |  required  | User or group account ID | string |  `gsvault user account id`  `gsvault group account id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.account\_id | string |  `gsvault user account id`  `gsvault group account id` 
action\_result\.parameter\.hold\_id | string |  `gsvault hold id` 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'add held account'
Add held account to the given hold ID

Type: **generic**  
Read only: **False**

A held account can only be added to the given hold\_id if the search\_method of the hold is either USER\_ACCOUNT or GROUP\_ACCOUNT\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**hold\_id** |  required  | Hold ID | string |  `gsvault hold id` 
**account\_id** |  required  | User or group account ID | string |  `gsvault user account id`  `gsvault group account id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.account\_id | string |  `gsvault user account id`  `gsvault group account id` 
action\_result\.parameter\.hold\_id | string |  `gsvault hold id` 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.accountId | string |  `gsvault user account id`  `gsvault group account id` 
action\_result\.data\.\*\.email | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
action\_result\.data\.\*\.firstName | string | 
action\_result\.data\.\*\.holdTime | string | 
action\_result\.data\.\*\.lastName | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list exports'
List all exports for the given matter ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**limit** |  optional  | Maximum number of exports to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.bucketName | string | 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.md5Hash | string |  `md5` 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.objectName | string | 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.size | string | 
action\_result\.data\.\*\.createTime | string | 
action\_result\.data\.\*\.exportOptions\.driveOptions\.includeAccessInfo | boolean | 
action\_result\.data\.\*\.exportOptions\.groupsOptions\.exportFormat | string | 
action\_result\.data\.\*\.exportOptions\.mailOptions\.exportFormat | string | 
action\_result\.data\.\*\.exportOptions\.mailOptions\.showConfidentialModeContent | boolean | 
action\_result\.data\.\*\.exportOptions\.region | string | 
action\_result\.data\.\*\.id | string |  `gsvault export id` 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.query\.accountInfo\.emails | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
action\_result\.data\.\*\.query\.corpus | string | 
action\_result\.data\.\*\.query\.dataScope | string | 
action\_result\.data\.\*\.query\.driveOptions\.includeSharedDrives | boolean | 
action\_result\.data\.\*\.query\.driveOptions\.includeTeamDrives | boolean | 
action\_result\.data\.\*\.query\.driveOptions\.versionDate | string | 
action\_result\.data\.\*\.query\.endTime | string | 
action\_result\.data\.\*\.query\.mailOptions\.excludeDrafts | boolean | 
action\_result\.data\.\*\.query\.method | string | 
action\_result\.data\.\*\.query\.orgUnitInfo\.orgUnitId | string |  `gsvault org unit id` 
action\_result\.data\.\*\.query\.searchMethod | string | 
action\_result\.data\.\*\.query\.startTime | string | 
action\_result\.data\.\*\.query\.terms | string | 
action\_result\.data\.\*\.query\.timeZone | string | 
action\_result\.data\.\*\.requester\.displayName | string | 
action\_result\.data\.\*\.requester\.email | string |  `gsvault user email ids`  `email` 
action\_result\.data\.\*\.stats\.exportedArtifactCount | string | 
action\_result\.data\.\*\.stats\.sizeInBytes | string | 
action\_result\.data\.\*\.stats\.totalArtifactCount | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.summary\.total\_exports\_returned | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get export'
Get information of an export from the given matter ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**export\_id** |  required  | Export ID | string |  `gsvault export id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.export\_id | string |  `gsvault export id` 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.bucketName | string | 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.md5Hash | string |  `md5` 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.objectName | string | 
action\_result\.data\.\*\.cloudStorageSink\.files\.\*\.size | string | 
action\_result\.data\.\*\.createTime | string | 
action\_result\.data\.\*\.exportOptions\.driveOptions\.includeAccessInfo | boolean | 
action\_result\.data\.\*\.exportOptions\.mailOptions\.exportFormat | string | 
action\_result\.data\.\*\.exportOptions\.mailOptions\.showConfidentialModeContent | boolean | 
action\_result\.data\.\*\.exportOptions\.region | string | 
action\_result\.data\.\*\.id | string |  `gsvault export id` 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.query\.accountInfo\.emails | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
action\_result\.data\.\*\.query\.corpus | string | 
action\_result\.data\.\*\.query\.dataScope | string | 
action\_result\.data\.\*\.query\.driveOptions\.versionDate | string | 
action\_result\.data\.\*\.query\.endTime | string | 
action\_result\.data\.\*\.query\.method | string | 
action\_result\.data\.\*\.query\.searchMethod | string | 
action\_result\.data\.\*\.query\.startTime | string | 
action\_result\.data\.\*\.query\.terms | string | 
action\_result\.data\.\*\.query\.timeZone | string | 
action\_result\.data\.\*\.requester\.displayName | string | 
action\_result\.data\.\*\.requester\.email | string |  `gsvault user email ids`  `email` 
action\_result\.data\.\*\.stats\.exportedArtifactCount | string | 
action\_result\.data\.\*\.stats\.sizeInBytes | string | 
action\_result\.data\.\*\.stats\.totalArtifactCount | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create export'
Perform a search based on the provided criteria and create an export for the search results

Type: **generic**  
Read only: **False**

For ACCOUNT type search\_method, you have to provide a valid list of email\_ids\. For ORG\_UNIT type search\_method, provide valid org\_unit\_id\. For corpus type GROUPS, you have to select ACCOUNT search method and provide valid list of a group email\_ids\. The parameter export\_format is supported only for the corpus type MAIL and GROUPS\. The parameter exclude\_drafts is supported only for the corpus type MAIL\. The show\_confidential\_mode\_content parameter is supported only for the corpus type MAIL\. The parameters include\_access\_info and include\_shared\_drives are applicable only for the corpus type DRIVE\. UNPROCESSED\_DATA data\_scope is not supported for corpus type DRIVE\. The parameter version\_date is only applicable for the corpus type DRIVE\. If the corpus type is DRIVE and data scope is HELD\_DATA, search\_method TEAM\_DRIVE is not allowed\. Time zone is not applicable for the HELD\_DATA data\_scope\. Terms parameter is not applicable for the UNPROCESSED\_DATA data\_scope\. Google Vault selects the default data\_region based on the region assigned to the owner of the matter\. You can select one of the values from the United States\(US\) and Europe\(EUROPE\) to change the data\_region of the created export\. Exports are automatically deleted within 15 days of their creation\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Export name | string | 
**matter\_id** |  required  | Matter ID | string |  `gsvault matter id` 
**type** |  required  | Type of export | string | 
**data\_scope** |  required  | Scope of data to be exported | string | 
**search\_method** |  required  | Scope of search | string | 
**org\_unit\_id** |  optional  | Organization ID | string |  `gsvault org unit id` 
**email\_ids** |  optional  | Comma\-separated list of email IDs \(user or group\) | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
**shared\_drive\_ids** |  optional  | Comma\-separated list of shared drive IDs | string |  `gsvault shared drive ids` 
**start\_time** |  optional  | Start time \(%Y\-%m\-%dT%H\:%M\:%SZ\) | string | 
**end\_time** |  optional  | End time \(%Y\-%m\-%dT%H\:%M\:%SZ\) | string | 
**time\_zone** |  optional  | Time zone for the export | string | 
**terms** |  optional  | Terms | string | 
**version\_date** |  optional  | Version date \(%Y\-%m\-%dT%H\:%M\:%SZ\) | string | 
**data\_region** |  optional  | Data region | string | 
**exclude\_drafts** |  optional  | Exclude drafts | boolean | 
**export\_format** |  optional  | Export Format | string | 
**show\_confidential\_mode\_content** |  optional  | Show confidential mode content | boolean | 
**include\_shared\_drives** |  optional  | Include results from shared drives | boolean | 
**include\_access\_info** |  optional  | Include access level information for users with indirect access to files \(this may increase export duration\) | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.data\_region | string | 
action\_result\.parameter\.data\_scope | string | 
action\_result\.parameter\.email\_ids | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
action\_result\.parameter\.end\_time | string | 
action\_result\.parameter\.exclude\_drafts | boolean | 
action\_result\.parameter\.export\_format | string | 
action\_result\.parameter\.include\_access\_info | boolean | 
action\_result\.parameter\.include\_shared\_drives | boolean | 
action\_result\.parameter\.matter\_id | string |  `gsvault matter id` 
action\_result\.parameter\.name | string | 
action\_result\.parameter\.org\_unit\_id | string |  `gsvault org unit id` 
action\_result\.parameter\.search\_method | string | 
action\_result\.parameter\.shared\_drive\_ids | string |  `gsvault shared drive ids` 
action\_result\.parameter\.show\_confidential\_mode\_content | boolean | 
action\_result\.parameter\.start\_time | string | 
action\_result\.parameter\.terms | string | 
action\_result\.parameter\.time\_zone | string | 
action\_result\.parameter\.type | string | 
action\_result\.parameter\.version\_date | string | 
action\_result\.data\.\*\.createTime | string | 
action\_result\.data\.\*\.exportOptions\.driveOptions\.includeAccessInfo | boolean | 
action\_result\.data\.\*\.exportOptions\.groupsOptions\.exportFormat | string | 
action\_result\.data\.\*\.exportOptions\.mailOptions\.exportFormat | string | 
action\_result\.data\.\*\.exportOptions\.mailOptions\.showConfidentialModeContent | boolean | 
action\_result\.data\.\*\.exportOptions\.region | string | 
action\_result\.data\.\*\.id | string |  `gsvault export id` 
action\_result\.data\.\*\.matterId | string |  `gsvault matter id` 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.query\.accountInfo\.emails | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
action\_result\.data\.\*\.query\.corpus | string | 
action\_result\.data\.\*\.query\.dataScope | string | 
action\_result\.data\.\*\.query\.driveOptions\.includeSharedDrives | boolean | 
action\_result\.data\.\*\.query\.driveOptions\.includeTeamDrives | boolean | 
action\_result\.data\.\*\.query\.endTime | string | 
action\_result\.data\.\*\.query\.mailOptions\.excludeDrafts | boolean | 
action\_result\.data\.\*\.query\.method | string | 
action\_result\.data\.\*\.query\.orgUnitInfo\.orgUnitId | string |  `gsvault org unit id` 
action\_result\.data\.\*\.query\.searchMethod | string | 
action\_result\.data\.\*\.query\.sharedDriveInfo\.sharedDriveIds | string |  `gsvault shared drive ids` 
action\_result\.data\.\*\.query\.startTime | string | 
action\_result\.data\.\*\.query\.teamDriveInfo\.teamDriveIds | string | 
action\_result\.data\.\*\.query\.terms | string | 
action\_result\.data\.\*\.query\.timeZone | string | 
action\_result\.data\.\*\.requester\.displayName | string | 
action\_result\.data\.\*\.requester\.email | string |  `gsvault user email ids`  `email` 
action\_result\.data\.\*\.status | string | 
action\_result\.summary\.matter\_id | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list organizations'
List all organizations

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of organizations to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.etag | string | 
action\_result\.data\.\*\.kind | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.orgUnitId | string |  `gsvault org unit id` 
action\_result\.data\.\*\.orgUnitPath | string | 
action\_result\.data\.\*\.parentOrgUnitId | string |  `gsvault org unit id` 
action\_result\.data\.\*\.parentOrgUnitPath | string | 
action\_result\.summary\.total\_organization\_units\_returned | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list groups'
List all groups of a domain

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain name | string |  `domain` 
**limit** |  optional  | Maximum number of groups to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.domain | string |  `domain` 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.adminCreated | boolean | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.directMembersCount | string | 
action\_result\.data\.\*\.email | string |  `gsvault group email ids`  `email` 
action\_result\.data\.\*\.etag | string | 
action\_result\.data\.\*\.id | string |  `gsvault group account id` 
action\_result\.data\.\*\.kind | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.nonEditableAliases | string |  `email` 
action\_result\.summary\.total\_groups\_returned | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 