[comment]: # "Auto-generated SOAR connector documentation"
# Google Vault

Publisher: Splunk  
Connector Version: 2.1.1  
Product Vendor: Google  
Product Name: Google Vault  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.3.5  

This app supports the actions to perform eDiscovery and provide a compliance solution for G Suite, allowing customers to retain, hold, search, and export their data

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2023 Splunk Inc."
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
    **Show More** , then select **Security** from the list of controls. If you can't see the
    controls, make sure you're signed in as an administrator for the domain.
-   Select **API controls** in the **Access and data control** section.
-   Select **MANAGE DOMAIN WIDE DELEGATIONS** in the **Domain wide delegation** section.
-   Select **Add new** in the API clients section
-   In the **Client Name** field enter the service account's **Client ID** . You can find your
    service account's client ID in the [Service accounts credentials
    page](https://console.developers.google.com/apis/credentials) or the service account JSON file
    (key named **client_id** ).
-   In the **One or More API Scopes** field enter the list of scopes that you wish to grant access
    to the App. For example, to enable all the scopes required by this app enter:
    https://www.googleapis.com/auth/ediscovery, https://www.googleapis.com/auth/ediscovery.readonly,
    https://www.googleapis.com/auth/admin.directory.orgunit.readonly,
    https://www.googleapis.com/auth/admin.directory.group.readonly
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
**login_email** |  required  | string | Login email
**key_json** |  required  | password | Contents of service account JSON file

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

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery.readonly</li></ul>.

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list matters'
List all open, closed, and deleted matters

Type: **investigate**  
Read only: **True**

Action uses the Admin SDK API to get a list of matters. Requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery.readonly</li></ul><br>The action will limit the number of matters returned to <b>limit</b> or (if not specified) 100.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**state** |  optional  | Type of matters to be retrieved | string | 
**limit** |  optional  | Maximum number of matters to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   500 
action_result.parameter.state | string |  |   OPEN 
action_result.data.\*.description | string |  |   Matter Description 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   0016f2e2-bc61-4119-89fe-6ba600663138 
action_result.data.\*.name | string |  |   Matter Name 109 
action_result.data.\*.state | string |  |   OPEN 
action_result.summary.total_matters_returned | numeric |  |   113 
action_result.message | string |  |   Successfully retrieved 113 matters 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'create matter'
Create a matter with OPEN state

Type: **generic**  
Read only: **False**

Action uses the Admin SDK API to create a matter. Requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Matter name | string | 
**description** |  required  | Matter description | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.description | string |  |   test value 2 
action_result.parameter.name | string |  |   test value 2 
action_result.data.\*.description | string |  |   test value 2 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.data.\*.name | string |  |   test value 2 
action_result.data.\*.state | string |  |   OPEN 
action_result.summary.name | string |  |   matter_name 
action_result.summary.description | string |  |   matter is being created for test purpose 
action_result.message | string |  |   Successfully created matter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get matter'
Fetch information for the given matter ID

Type: **investigate**  
Read only: **True**

There are two views of a matter: BASIC (default) and FULL. The FULL view adds matter permissions in addition to the data received in the BASIC view. Requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery.readonly</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**view** |  optional  | View of matter | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   72829eb1-2818-4a8b-a8db-cb8139d99fe0 
action_result.parameter.view | string |  |   FULL 
action_result.data.\*.description | string |  |   Matter Description 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   72829eb1-2818-4a8b-a8db-cb8139d99fe0 
action_result.data.\*.matterPermissions.\*.accountId | string |  `gsvault user account id`  |   108620176647363363111 
action_result.data.\*.matterPermissions.\*.role | string |  |   OWNER 
action_result.data.\*.name | string |  |   Matter Name 124 
action_result.data.\*.state | string |  |   OPEN 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully fetched matter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'close matter'
Move a matter to the CLOSED state

Type: **generic**  
Read only: **False**

You can close the matter only if it is in the OPEN state. If the matter is in the OPEN state and contains any holds, then, to close the matter all holds must be deleted. For this, you have to checkmark the <b>Delete all holds</b> parameter and run the action. If you keep the parameter unchecked and run the action, it will fail due to undeleted holds in the matter. In that case, the user has to delete all the holds manually; run this action after that to close the matter.<br>Requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**delete_all_holds** |  optional  | Delete all holds | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.delete_all_holds | boolean |  |   True  False 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.data.\*.matter.description | string |  |   test value 2 
action_result.data.\*.matter.matterId | string |  `gsvault matter id`  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.data.\*.matter.name | string |  |   test value 2 
action_result.data.\*.matter.state | string |  |   CLOSED 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully closed matter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'delete matter'
Move a matter to the DELETED state

Type: **generic**  
Read only: **False**

You can delete the matter only if it is in the CLOSED state. If the matter is in the OPEN state and contains any holds, then, to delete it all holds must be deleted and the matter must be moved to the CLOSED state. For this, you have to checkmark the 'Delete all holds' parameter and run the action. By doing this, action will close the matter after deleting all the holds (if any) associated with it and move it to the DELETED state. If you keep the parameter unchecked and run the action, it will fail due to the matter not being in the CLOSED state. In that case, the user has to move the matter to the CLOSED state by manually deleting all the associated holds; run this action after that to delete the matter.<br>Requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**delete_all_holds** |  optional  | Delete all holds | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.delete_all_holds | boolean |  |   True  False 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.data.\*.description | string |  |   test value 2 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.data.\*.name | string |  |   test value 2 
action_result.data.\*.state | string |  |   DELETED 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully deleted matter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'reopen matter'
Reopens a matter to move it from CLOSED to OPEN state

Type: **generic**  
Read only: **False**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   6d546bd6-b7e8-4404-b691-5a30f2bbf336 
action_result.data.\*.matter.description | string |  |   Matter Description 
action_result.data.\*.matter.matterId | string |  `gsvault matter id`  |   6d546bd6-b7e8-4404-b691-5a30f2bbf336 
action_result.data.\*.matter.name | string |  |   Matter Name 26 
action_result.data.\*.matter.state | string |  |   OPEN 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully reopened matter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'restore matter'
Restores a matter to move it from DELETED to CLOSED state

Type: **generic**  
Read only: **False**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.data.\*.description | string |  |   test value 2 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.data.\*.name | string |  |   test value 2 
action_result.data.\*.state | string |  |   CLOSED 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully restored matter 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list holds'
List all holds for the given matter ID

Type: **investigate**  
Read only: **True**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery.readonly</li></ul><br>The action will limit the number of holds returned to <b>limit</b> or (if not specified) 100.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**limit** |  optional  | Maximum number of holds to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   500 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   ac1c7c68-0b1f-4973-add2-bdf4f472ed6b 
action_result.data.\*.accounts.\*.accountId | string |  `gsvault user account id`  `gsvault group account id`  |   117361455879836884540 
action_result.data.\*.accounts.\*.email | string |  `gsvault user email ids`  `gsvault group email ids`  `email`  |   test2@testvalue.com 
action_result.data.\*.accounts.\*.firstName | string |  |   Test First Name 
action_result.data.\*.accounts.\*.holdTime | string |  |   2019-08-23T10:21:53.693Z 
action_result.data.\*.accounts.\*.lastName | string |  |   Test Last Name 
action_result.data.\*.corpus | string |  |   DRIVE 
action_result.data.\*.holdId | string |  `gsvault hold id`  |   3z8qrdt23cpfix 
action_result.data.\*.name | string |  |   My First drive Accounts Hold 
action_result.data.\*.orgUnit.holdTime | string |  |   2019-08-23T12:51:47.955Z 
action_result.data.\*.orgUnit.orgUnitId | string |  `gsvault org unit id`  |   id:03z8qrdt2kekpq1 
action_result.data.\*.query.driveQuery.includeSharedDriveFiles | boolean |  |   True  False 
action_result.data.\*.query.driveQuery.includeTeamDriveFiles | boolean |  |   True  False 
action_result.data.\*.query.groupsQuery.endTime | string |  |   2019-09-22T00:00:00Z 
action_result.data.\*.query.groupsQuery.startTime | string |  |   2019-09-04T00:00:00Z 
action_result.data.\*.query.groupsQuery.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.data.\*.query.mailQuery.endTime | string |  |   2019-09-04T00:00:00Z 
action_result.data.\*.query.mailQuery.startTime | string |  |   2019-09-04T00:00:00Z 
action_result.data.\*.query.mailQuery.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.data.\*.updateTime | string |  |   2019-08-23T10:21:52.734Z 
action_result.summary.total_holds_returned | numeric |  |   3 
action_result.message | string |  |   Successfully retrieved 3 holds 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'create hold'
Create a hold within the given matter ID

Type: **generic**  
Read only: **False**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Hold name | string | 
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**type** |  required  | Type of the hold | string | 
**search_method** |  required  | Scope of search | string | 
**org_unit_id** |  optional  | Organization ID | string |  `gsvault org unit id` 
**user_email_ids** |  optional  | Comma-separated list of user emails | string |  `gsvault user email ids`  `email` 
**group_account_ids** |  optional  | Comma-separated list of group IDs | string |  `gsvault group account ids` 
**terms** |  optional  | Conditions to be met for a message to be covered by this hold | string | 
**start_time** |  optional  | Start time (%Y-%m-%dT%H:%M:%SZ) | string | 
**end_time** |  optional  | End time (%Y-%m-%dT%H:%M:%SZ) | string | 
**include_shared_drive_files** |  optional  | Include files from associated shared drives | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.end_time | string |  |   2017-09-23T00:00:00Z 
action_result.parameter.group_account_ids | string |  `gsvault group account ids`  |   01302m9240iv47j 
action_result.parameter.include_shared_drive_files | boolean |  |   True  False 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   9236e87e-631a-49fc-a8c2-dfb8a34e4d24 
action_result.parameter.name | string |  |   test_hold_value_1 
action_result.parameter.org_unit_id | string |  `gsvault org unit id`  |   id:03z8qrdt2kekpq1 
action_result.parameter.search_method | string |  |   USER_ACCOUNT 
action_result.parameter.start_time | string |  |   2017-03-16T00:00:00Z 
action_result.parameter.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.parameter.type | string |  |   DRIVE 
action_result.parameter.user_email_ids | string |  `gsvault user email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.accounts.\*.accountId | string |  `gsvault user account id`  `gsvault group account id`  |   100113397046722686289 
action_result.data.\*.accounts.\*.email | string |  `gsvault user email ids`  `gsvault group email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.accounts.\*.firstName | string |  |   Test First Name 
action_result.data.\*.accounts.\*.holdTime | string |  |   2019-08-30T12:20:43Z 
action_result.data.\*.accounts.\*.lastName | string |  |   Test Last Name 
action_result.data.\*.corpus | string |  |   MAIL 
action_result.data.\*.holdId | string |  `gsvault hold id`  |   3z8qrdt3jtsioc 
action_result.data.\*.name | string |  |   test_hold_value_1 
action_result.data.\*.orgUnit.holdTime | string |  |   2019-08-30T12:20:16.451Z 
action_result.data.\*.orgUnit.orgUnitId | string |  `gsvault org unit id`  |   id:03z8qrdt2kekpq1 
action_result.data.\*.query.driveQuery.includeSharedDriveFiles | boolean |  |   True  False 
action_result.data.\*.query.driveQuery.includeTeamDriveFiles | boolean |  |   True  False 
action_result.data.\*.query.groupsQuery.endTime | string |  |   2019-08-30T00:00:00Z 
action_result.data.\*.query.groupsQuery.startTime | string |  |   2019-07-30T00:00:00Z 
action_result.data.\*.query.groupsQuery.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.data.\*.query.mailQuery.endTime | string |  |   2017-09-23T00:00:00Z 
action_result.data.\*.query.mailQuery.startTime | string |  |   2017-03-16T00:00:00Z 
action_result.data.\*.query.mailQuery.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.data.\*.updateTime | string |  |   2019-08-30T12:20:43.644Z 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully created hold 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'delete hold'
Delete a hold

Type: **generic**  
Read only: **False**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**hold_id** |  required  | Hold ID | string |  `gsvault hold id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.hold_id | string |  `gsvault hold id`  |   3z8qrdt0sr3fto 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   72829eb1-2818-4a8b-a8db-cb8139d99fe0 
action_result.data | string |  |  
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully deleted hold 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'remove held account'
Remove held account from the given hold ID

Type: **generic**  
Read only: **False**

A held account can only be removed from the given hold_id if the search_method of the hold is either USER_ACCOUNT or GROUP_ACCOUNT.<br>Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**hold_id** |  required  | Hold ID | string |  `gsvault hold id` 
**account_id** |  required  | User or group account ID | string |  `gsvault user account id`  `gsvault group account id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.account_id | string |  `gsvault user account id`  `gsvault group account id`  |   108620176647363363111 
action_result.parameter.hold_id | string |  `gsvault hold id`  |   3z8qrdt111pgr8 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   209366a8-eadc-4687-8d23-190afdfb12ba 
action_result.data | string |  |  
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.summary.hold_id | string |  |   1g17sx82yv5sqg 
action_result.message | string |  |   Successfully removed held account to 3z8qrdt111pgr8 hold id for 209366a8-eadc-4687-8d23-190afdfb12ba matter id 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'add held account'
Add held account to the given hold ID

Type: **generic**  
Read only: **False**

A held account can only be added to the given hold_id if the search_method of the hold is either USER_ACCOUNT or GROUP_ACCOUNT.<br>Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**hold_id** |  required  | Hold ID | string |  `gsvault hold id` 
**account_id** |  required  | User or group account ID | string |  `gsvault user account id`  `gsvault group account id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.account_id | string |  `gsvault user account id`  `gsvault group account id`  |   108620176647363363111 
action_result.parameter.hold_id | string |  `gsvault hold id`  |   3z8qrdt111pgr8 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   209366a8-eadc-4687-8d23-190afdfb12ba 
action_result.data.\*.accountId | string |  `gsvault user account id`  `gsvault group account id`  |   108620176647363363111 
action_result.data.\*.email | string |  `gsvault user email ids`  `gsvault group email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.firstName | string |  |   Test First Name 
action_result.data.\*.holdTime | string |  |   2019-08-26T16:04:49.943Z 
action_result.data.\*.lastName | string |  |   Test Last Name 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully added held account to 3z8qrdt111pgr8 hold id for 209366a8-eadc-4687-8d23-190afdfb12ba matter id 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list exports'
List all exports for the given matter ID

Type: **investigate**  
Read only: **True**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery.readonly</li></ul><br>The action will limit the number of exports returned to <b>limit</b> or (if not specified) 100.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**limit** |  optional  | Maximum number of exports to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   500 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   1db9d451-f68c-4b7c-bbb8-2dec2adc46a1 
action_result.data.\*.cloudStorageSink.files.\*.bucketName | string |  |   a6c13d2c-029f-4df3-9e95-1584897bac98 
action_result.data.\*.cloudStorageSink.files.\*.md5Hash | string |  `md5`  |   373afbad464a2f048cf77ce059b64c59 
action_result.data.\*.cloudStorageSink.files.\*.objectName | string |  |   1db9d451-f68c-4b7c-bbb8-2dec2adc46a1/exportly-f0624c45-c1f4-4c54-ade5-51f6ac08d134/my_first_export-1.zip 
action_result.data.\*.cloudStorageSink.files.\*.size | string |  |   3900 
action_result.data.\*.createTime | string |  |   2019-08-26T15:19:41.857Z 
action_result.data.\*.exportOptions.driveOptions.includeAccessInfo | boolean |  |   True  False 
action_result.data.\*.exportOptions.groupsOptions.exportFormat | string |  |   PST 
action_result.data.\*.exportOptions.mailOptions.exportFormat | string |  |   MBOX 
action_result.data.\*.exportOptions.mailOptions.showConfidentialModeContent | boolean |  |   True  False 
action_result.data.\*.exportOptions.region | string |  |   ANY 
action_result.data.\*.id | string |  `gsvault export id`  |   exportly-f0624c45-c1f4-4c54-ade5-51f6ac08d134 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   1db9d451-f68c-4b7c-bbb8-2dec2adc46a1 
action_result.data.\*.name | string |  |   my first export 
action_result.data.\*.query.accountInfo.emails | string |  `gsvault user email ids`  `gsvault group email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.query.corpus | string |  |   MAIL 
action_result.data.\*.query.dataScope | string |  |   ALL_DATA 
action_result.data.\*.query.driveOptions.includeSharedDrives | boolean |  |   True  False 
action_result.data.\*.query.driveOptions.includeTeamDrives | boolean |  |   True  False 
action_result.data.\*.query.driveOptions.versionDate | string |  |   2019-08-08T00:00:00Z 
action_result.data.\*.query.endTime | string |  |   2018-08-29T00:00:00Z 
action_result.data.\*.query.mailOptions.excludeDrafts | boolean |  |   True  False 
action_result.data.\*.query.method | string |  |   ACCOUNT 
action_result.data.\*.query.orgUnitInfo.orgUnitId | string |  `gsvault org unit id`  |   id:03ph8a2z1mtle0f 
action_result.data.\*.query.searchMethod | string |  |   ACCOUNT 
action_result.data.\*.query.startTime | string |  |   2018-08-01T00:00:00Z 
action_result.data.\*.query.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.data.\*.query.timeZone | string |  |   Etc/GMT 
action_result.data.\*.requester.displayName | string |  |   Test Display Name 
action_result.data.\*.requester.email | string |  `gsvault user email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.stats.exportedArtifactCount | string |  |   2 
action_result.data.\*.stats.sizeInBytes | string |  |   6756 
action_result.data.\*.stats.totalArtifactCount | string |  |   2 
action_result.data.\*.status | string |  |   COMPLETED 
action_result.summary.total_exports_returned | numeric |  |   2 
action_result.message | string |  |   Successfully retrieved 2 exports 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'get export'
Get information of an export from the given matter ID

Type: **investigate**  
Read only: **True**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery.readonly</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**export_id** |  required  | Export ID | string |  `gsvault export id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.export_id | string |  `gsvault export id`  |   exportly-fac2824a-35f7-4429-8f2d-74cbe30983ad 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   1db9d451-f68c-4b7c-bbb8-2dec2adc46a1 
action_result.data.\*.cloudStorageSink.files.\*.bucketName | string |  |   a6c13d2c-029f-4df3-9e95-1584897bac98 
action_result.data.\*.cloudStorageSink.files.\*.md5Hash | string |  `md5`  |   ff6eafd106f782eb7e84a777f088ba4e 
action_result.data.\*.cloudStorageSink.files.\*.objectName | string |  |   1db9d451-f68c-4b7c-bbb8-2dec2adc46a1/exportly-fac2824a-35f7-4429-8f2d-74cbe30983ad/my_second_export-1.zip 
action_result.data.\*.cloudStorageSink.files.\*.size | string |  |   13775 
action_result.data.\*.createTime | string |  |   2019-08-26T15:22:05.329Z 
action_result.data.\*.exportOptions.driveOptions.includeAccessInfo | boolean |  |   True  False 
action_result.data.\*.exportOptions.mailOptions.exportFormat | string |  |   MBOX 
action_result.data.\*.exportOptions.mailOptions.showConfidentialModeContent | boolean |  |   True  False 
action_result.data.\*.exportOptions.region | string |  |   ANY 
action_result.data.\*.id | string |  `gsvault export id`  |   exportly-fac2824a-35f7-4429-8f2d-74cbe30983ad 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   1db9d451-f68c-4b7c-bbb8-2dec2adc46a1 
action_result.data.\*.name | string |  |   my second export 
action_result.data.\*.query.accountInfo.emails | string |  `gsvault user email ids`  `gsvault group email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.query.corpus | string |  |   MAIL 
action_result.data.\*.query.dataScope | string |  |   ALL_DATA 
action_result.data.\*.query.driveOptions.versionDate | string |  |   2019-08-08T00:00:00Z 
action_result.data.\*.query.endTime | string |  |   2018-08-29T00:00:00Z 
action_result.data.\*.query.method | string |  |   ACCOUNT 
action_result.data.\*.query.searchMethod | string |  |   ACCOUNT 
action_result.data.\*.query.startTime | string |  |   2018-08-01T00:00:00Z 
action_result.data.\*.query.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.data.\*.query.timeZone | string |  |   Etc/GMT 
action_result.data.\*.requester.displayName | string |  |   Test Display Name 
action_result.data.\*.requester.email | string |  `gsvault user email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.stats.exportedArtifactCount | string |  |   8 
action_result.data.\*.stats.sizeInBytes | string |  |   24840 
action_result.data.\*.stats.totalArtifactCount | string |  |   8 
action_result.data.\*.status | string |  |   COMPLETED 
action_result.data.\*.query.orgUnitInfo.orgUnitId | string |  |   id:557asv0g70 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully fetched export 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'create export'
Perform a search based on the provided criteria and create an export for the search results

Type: **generic**  
Read only: **False**

For ACCOUNT type search_method, you have to provide a valid list of email_ids. For ORG_UNIT type search_method, provide valid org_unit_id. For corpus type GROUPS, you have to select ACCOUNT search method and provide valid list of a group email_ids. The parameter export_format is supported only for the corpus type MAIL and GROUPS. The parameter exclude_drafts is supported only for the corpus type MAIL. The show_confidential_mode_content parameter is supported only for the corpus type MAIL. The parameters include_access_info and include_shared_drives are applicable only for the corpus type DRIVE. UNPROCESSED_DATA data_scope is not supported for corpus type DRIVE. The parameter version_date is only applicable for the corpus type DRIVE. If the corpus type is DRIVE and data scope is HELD_DATA, search_method TEAM_DRIVE is not allowed. Time zone is not applicable for the HELD_DATA data_scope. Terms parameter is not applicable for the UNPROCESSED_DATA data_scope. Google Vault selects the default data_region based on the region assigned to the owner of the matter. You can select one of the values from the United States(US) and Europe(EUROPE) to change the data_region of the created export. Exports are automatically deleted within 15 days of their creation.<br>Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/ediscovery</li></ul>.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Export name | string | 
**matter_id** |  required  | Matter ID | string |  `gsvault matter id` 
**type** |  required  | Type of export | string | 
**data_scope** |  required  | Scope of data to be exported | string | 
**search_method** |  required  | Scope of search | string | 
**org_unit_id** |  optional  | Organization ID | string |  `gsvault org unit id` 
**email_ids** |  optional  | Comma-separated list of email IDs (user or group) | string |  `gsvault user email ids`  `gsvault group email ids`  `email` 
**shared_drive_ids** |  optional  | Comma-separated list of shared drive IDs | string |  `gsvault shared drive ids` 
**start_time** |  optional  | Start time (%Y-%m-%dT%H:%M:%SZ) | string | 
**end_time** |  optional  | End time (%Y-%m-%dT%H:%M:%SZ) | string | 
**time_zone** |  optional  | Time zone for the export | string | 
**terms** |  optional  | Terms | string | 
**version_date** |  optional  | Version date (%Y-%m-%dT%H:%M:%SZ) | string | 
**data_region** |  optional  | Data region | string | 
**exclude_drafts** |  optional  | Exclude drafts | boolean | 
**export_format** |  optional  | Export format | string | 
**show_confidential_mode_content** |  optional  | Show confidential mode content | boolean | 
**include_shared_drives** |  optional  | Include results from shared drives | boolean | 
**include_access_info** |  optional  | Include access level information for users with indirect access to files (this may increase export duration) | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.data_region | string |  |   US 
action_result.parameter.data_scope | string |  |   ALL_DATA 
action_result.parameter.email_ids | string |  `gsvault user email ids`  `gsvault group email ids`  `email`  |   testgroup@testvalue.com 
action_result.parameter.end_time | string |  |   2019-08-01T00:00:00Z 
action_result.parameter.exclude_drafts | boolean |  |   False  True 
action_result.parameter.export_format | string |  |   MBOX 
action_result.parameter.include_access_info | boolean |  |   False  True 
action_result.parameter.include_shared_drives | boolean |  |   False  True 
action_result.parameter.matter_id | string |  `gsvault matter id`  |   d2545a66-36ca-48dd-8fe1-44f790b72d05 
action_result.parameter.name | string |  |   test_export_group 
action_result.parameter.org_unit_id | string |  `gsvault org unit id`  |   id:03ph8a2z1mtle0f 
action_result.parameter.search_method | string |  |   ACCOUNT 
action_result.parameter.shared_drive_ids | string |  `gsvault shared drive ids`  |   0AMcc3KDZbSb2Uk9PVA,0AN4HRsxrp9juUk9PVA 
action_result.parameter.show_confidential_mode_content | boolean |  |   False  True 
action_result.parameter.start_time | string |  |   2019-07-01T00:00:00Z 
action_result.parameter.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.parameter.time_zone | string |  |   Etc/GMT-13 
action_result.parameter.type | string |  |   DRIVE 
action_result.parameter.version_date | string |  |   2019-07-01T00:00:00Z 
action_result.data.\*.createTime | string |  |   2019-09-04T16:11:36.252Z 
action_result.data.\*.exportOptions.driveOptions.includeAccessInfo | boolean |  |   True  False 
action_result.data.\*.exportOptions.groupsOptions.exportFormat | string |  |   MBOX 
action_result.data.\*.exportOptions.mailOptions.exportFormat | string |  |   MBOX 
action_result.data.\*.exportOptions.mailOptions.showConfidentialModeContent | boolean |  |   True  False 
action_result.data.\*.exportOptions.region | string |  |   US 
action_result.data.\*.id | string |  `gsvault export id`  |   exportly-781551ad-c2cb-4efc-8d53-4f5f6146ffdf 
action_result.data.\*.matterId | string |  `gsvault matter id`  |   d2545a66-36ca-48dd-8fe1-44f790b72d05 
action_result.data.\*.name | string |  |   test_export_group 
action_result.data.\*.query.accountInfo.emails | string |  `gsvault user email ids`  `gsvault group email ids`  `email`  |   testgroup@testvalue.com 
action_result.data.\*.query.corpus | string |  |   GROUPS 
action_result.data.\*.query.dataScope | string |  |   ALL_DATA 
action_result.data.\*.query.driveOptions.includeSharedDrives | boolean |  |   True  False 
action_result.data.\*.query.driveOptions.includeTeamDrives | boolean |  |   True  False 
action_result.data.\*.query.endTime | string |  |   2019-08-01T00:00:00Z 
action_result.data.\*.query.mailOptions.excludeDrafts | boolean |  |   True  False 
action_result.data.\*.query.method | string |  |   ORG_UNIT 
action_result.data.\*.query.orgUnitInfo.orgUnitId | string |  `gsvault org unit id`  |   id:03ph8a2z1mtle0f 
action_result.data.\*.query.searchMethod | string |  |   ACCOUNT 
action_result.data.\*.query.sharedDriveInfo.sharedDriveIds | string |  `gsvault shared drive ids`  |   0AN4HRsxrp9juUk9PVA 
action_result.data.\*.query.startTime | string |  |   2019-07-01T00:00:00Z 
action_result.data.\*.query.teamDriveInfo.teamDriveIds | string |  |   0AN4HRsxrp9juUk9PVA 
action_result.data.\*.query.terms | string |  |   has:attachment is:sent -label:drafts 
action_result.data.\*.query.timeZone | string |  |   Etc/GMT-13 
action_result.data.\*.requester.displayName | string |  |   Test Test 
action_result.data.\*.requester.email | string |  `gsvault user email ids`  `email`  |   test@testvalue.com 
action_result.data.\*.status | string |  |   IN_PROGRESS 
action_result.summary.matter_id | string |  |   9360993f-1cd6-4709-81e3-457ff0a0b4ba 
action_result.message | string |  |   Successfully created export 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list organizations'
List all organizations

Type: **investigate**  
Read only: **True**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/admin.directory.orgunit.readonly</li></ul><br>The action will limit the number of organizations returned to <b>limit</b> or (if not specified) 100.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**limit** |  optional  | Maximum number of organizations to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.limit | numeric |  |   100 
action_result.data.\*.description | string |  |   test.com 
action_result.data.\*.etag | string |  |   "f-A4wQx02aM-7Cegj6o2Lk8/RjBTZYgkNFkXC95y28MFhk3MTRQ" 
action_result.data.\*.kind | string |  |   admin#directory#orgUnit 
action_result.data.\*.name | string |  |   test.com 
action_result.data.\*.orgUnitId | string |  `gsvault org unit id`  |   id:03ph8a2z1mtle0f 
action_result.data.\*.orgUnitPath | string |  |   /test.com 
action_result.data.\*.parentOrgUnitId | string |  `gsvault org unit id`  |   id:03z8qrdt2kekpq1 
action_result.data.\*.parentOrgUnitPath | string |  |   / 
action_result.summary.total_organization_units_returned | numeric |  |   1 
action_result.message | string |  |   Successfully retrieved 1 organization unit 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list groups'
List all groups of a domain

Type: **investigate**  
Read only: **True**

Action requires authorization with the following scope:<ul><li>https://www.googleapis.com/auth/admin.directory.group.readonly</li></ul><br>The action will limit the number of groups returned to <b>limit</b> or (if not specified) 100.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**domain** |  required  | Domain name | string |  `domain` 
**limit** |  optional  | Maximum number of groups to return | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.domain | string |  `domain`  |   test.com 
action_result.parameter.limit | numeric |  |   100 
action_result.data.\*.adminCreated | boolean |  |   True  False 
action_result.data.\*.description | string |  |   This is for testing Purpose 
action_result.data.\*.directMembersCount | string |  |   0 
action_result.data.\*.email | string |  `gsvault group email ids`  `email`  |   testgroup@testdomain.com 
action_result.data.\*.etag | string |  |   "f-A4wQx02aM-7Cegj6o2Lk8/khBiJGjhnDQr0c_dCHzV0wULDBY" 
action_result.data.\*.id | string |  `gsvault group account id`  |   01302m9240iv47j 
action_result.data.\*.kind | string |  |   admin#directory#group 
action_result.data.\*.name | string |  |   testgroup 
action_result.data.\*.nonEditableAliases | string |  `email`  |   testing_group@testdomain.com.test-a.com 
action_result.summary.total_groups_returned | numeric |  |   5 
action_result.message | string |  |   Successfully retrieved 5 groups for the domain 'test.com' 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 