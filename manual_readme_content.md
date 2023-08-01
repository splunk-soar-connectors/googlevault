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
