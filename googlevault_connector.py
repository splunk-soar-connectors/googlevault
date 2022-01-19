# File: googlevault_connector.py
#
# Copyright (c) 2019-2022 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
import datetime
import json
import os

import phantom.app as phantom
import phantom.utils as ph_utils
import requests
from google.oauth2 import service_account
from googleapiclient import discovery
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from googlevault_consts import *

init_path = '{}/dependencies/google/__init__.py'.format(  # noqa
    os.path.dirname(os.path.abspath(__file__))  # noqa
)  # noqa
try:
    open(init_path, 'a+').close()  # noqa
except Exception:  # noqa
    pass  # noqa


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class GoogleVaultConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(GoogleVaultConnector, self).__init__()

        self._state = None
        self._login_email = None
        self._key_dict = None

    def _create_client(self, action_result, scopes):
        credentials = None

        try:
            credentials = service_account.Credentials.from_service_account_info(self._key_dict, scopes=scopes)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Unable to create load the key json", e), None

        if self._login_email:
            try:
                credentials = credentials.with_subject(self._login_email)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Failed to create delegated credentials", e), None

        try:
            if self.get_action_identifier() in ['list_organizations', 'list_groups']:
                client = discovery.build('admin', 'directory_v1', credentials=credentials)
            else:
                client = discovery.build('vault', 'v1', credentials=credentials)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Unable to create client", e), None

        return phantom.APP_SUCCESS, client

    def _validate_integer(self, action_result, parameter, key, allow_zero=False):
        try:
            if not float(parameter).is_integer():
                action_result.set_status(phantom.APP_ERROR, INVALID_INT.format(param=key))
                return None

            parameter = int(parameter)
        except Exception as e:
            self.debug_print(GOOGLE_VAULT_EXCEPTION, e)
            action_result.set_status(phantom.APP_ERROR, INVALID_INT.format(param=key))
            return None

        if parameter < 0:
            action_result.set_status(phantom.APP_ERROR, ERR_NEGATIVE_INT_PARAM.format(param=key))
            return None

        if not allow_zero and parameter == 0:
            action_result.set_status(phantom.APP_ERROR, GSVAULT_INVALID_LIMIT.format(param=key))
            return None

        return parameter

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]
        self.save_progress(CREATE_GOOGLE_VAULT_CLIENT)

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.save_progress(TEST_CONNECTIVITY_FAILED)
            return ret_val

        self.save_progress(MAKING_TEST_CALL_GOOGLE_VAULT)
        try:
            client.matters().list(pageSize=10).execute()
        except Exception as e:
            self.save_progress(TEST_CONNECTIVITY_FAILED)
            return action_result.set_status(phantom.APP_ERROR, ERROR_WHILE_LISTING_MATTERS, e)

        self.save_progress(TEST_CONNECTIVITY_PASSED)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_matters(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        view = param.get("state")

        limit = self._validate_integer(action_result, param.get("limit", DEFAULT_LIMIT), 'limit', allow_zero=False)

        if limit is None:
            return action_result.get_status()
        try:
            matters = self._paginator(client, limit=limit, view=view)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, ERROR_WHILE_LISTING_MATTERS, e)

        if not matters:
            return action_result.set_status(phantom.APP_ERROR, NO_DATA_FOUND)

        for matter in matters:
            action_result.add_data(matter)

        num_matters = len(matters)
        action_result.update_summary({'total_matters_returned': num_matters})

        return action_result.set_status(phantom.APP_SUCCESS, 'Successfully retrieved {} matter{}'.format(
            num_matters, '' if num_matters == 1 else 's'))

    def _handle_list_organizations(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = GOOGLE_ORGANIZATIONS_SCOPE

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        limit = self._validate_integer(action_result, param.get("limit", DEFAULT_LIMIT), 'limit', allow_zero=False)

        if limit is None:
            return action_result.get_status()
        try:
            org_units = self._paginator(client, limit=limit)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while listing organization units", e)

        if not org_units:
            return action_result.set_status(phantom.APP_ERROR, NO_DATA_FOUND)

        for org_unit in org_units:
            action_result.add_data(org_unit)

        num_org_units = len(org_units)
        action_result.update_summary({'total_organization_units_returned': num_org_units})

        return action_result.set_status(phantom.APP_SUCCESS, 'Successfully retrieved {} organization unit{}'.format(
            num_org_units, '' if num_org_units == 1 else 's'))

    def _handle_list_groups(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = GOOGLE_GROUPS_SCOPE

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        domain = param["domain"]
        limit = self._validate_integer(action_result, param.get("limit", DEFAULT_LIMIT), 'limit', allow_zero=False)

        if limit is None:
            return action_result.get_status()
        try:
            groups = self._paginator(client, limit=limit, domain=domain)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while listing groups for the given domain '{}'".format(domain), e)

        if not groups:
            return action_result.set_status(phantom.APP_ERROR, NO_DATA_FOUND)

        for group in groups:
            action_result.add_data(group)

        num_groups = len(groups)
        action_result.update_summary({'total_groups_returned': num_groups})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved {} group{} for the domain '{}'".format(
            num_groups, '' if num_groups == 1 else 's', domain))

    def _handle_create_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val
        name = param["name"]
        description = param["description"]
        matter_content = {
            'name': name,
            'description': description,
        }
        try:
            matter = client.matters().create(body=matter_content).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while creating matter", e)

        action_result.add_data(matter)
        action_result.update_summary({'name': name, 'description': description})
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created matter")

    def _handle_get_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]
        matter_id = param["matter_id"]
        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        ret_val, matter = self._get_single_matter(action_result, client, matter_id=matter_id, view=param.get("view", "BASIC"))

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        action_result.add_data(matter)
        action_result.update_summary({'matter_id': matter_id})
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully fetched matter")

    def _get_single_matter(self, action_result, client, matter_id, view="BASIC"):

        try:
            response = client.matters().get(matterId=matter_id, view=view).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while fetching matter", e), None

        return phantom.APP_SUCCESS, response

    def _handle_close_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        delete_flag = param.get("delete_all_holds", True)
        matter_id = param["matter_id"]

        ret_val, flag, state = self._check_matter_state(action_result, client, matter_id=matter_id, state_for_check="OPEN")

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if not flag:
            return action_result.set_status(phantom.APP_ERROR, "Matter already exists in {} state".format(state))

        if not delete_flag:
            try:
                matter = client.matters().close(matterId=matter_id).execute()
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Error while closing matter", e)
        else:
            ret_val, matter = self._close_single_matter(action_result, client, matter_id=matter_id)

            if phantom.is_fail(ret_val):
                return action_result.get_status()

        action_result.add_data(matter)
        action_result.update_summary({'matter_id': matter_id})
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully closed matter")

    def _close_single_matter(self, action_result, client, matter_id):

        ret_val = self._check_for_hold(action_result, client, matter_id=matter_id)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        try:
            response = client.matters().close(matterId=matter_id).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while closing matter", e)

        return phantom.APP_SUCCESS, response

    def _check_for_hold(self, action_result, client, matter_id):

        holds = self._paginator(client, matter_id=matter_id, hold_flag=True)

        if not holds:
            return phantom.APP_SUCCESS

        ret_val = self._delete_all_holds(action_result, client, matter_id, holds)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        return phantom.APP_SUCCESS

    def _delete_all_holds(self, action_result, client, matter_id, holds):

        for hold in holds:
            hold_id = hold.get("holdId")
            if hold_id:
                ret_val, result = self._delete_single_hold(action_result, client, matter_id, hold_id)
                if phantom.is_fail(ret_val):
                    return action_result.get_status()

        return phantom.APP_SUCCESS

    def _check_matter_state(self, action_result, client, matter_id, state_for_check=None):

        flag = False
        state = None

        ret_val, matter = self._get_single_matter(action_result, client, matter_id=matter_id)

        if phantom.is_fail(ret_val):
            return action_result.get_status(), flag, state

        state = matter.get("state")
        if state and state == state_for_check:
            flag = True

        return phantom.APP_SUCCESS, flag, state

    def _handle_delete_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        delete_flag = param.get("delete_all_holds", True)
        matter_id = param["matter_id"]

        ret_val, flag, state = self._check_matter_state(action_result, client, matter_id=matter_id, state_for_check="DELETED")

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if flag:
            return action_result.set_status(phantom.APP_ERROR, "Matter already exists in {} state".format(state))

        if state == "OPEN":
            if delete_flag:
                ret_val, matter = self._close_single_matter(action_result, client, matter_id=matter_id)

                if phantom.is_fail(ret_val):
                    return action_result.get_status()

        try:
            matter = client.matters().delete(matterId=matter_id).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while deleting matter", e)

        action_result.add_data(matter)
        action_result.update_summary({'matter_id': matter_id})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully deleted matter")

    def _handle_restore_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]
        matter_id = param["matter_id"]
        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        try:
            matter = client.matters().undelete(matterId=matter_id).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while restoring matter", e)

        action_result.add_data(matter)
        action_result.update_summary({'matter_id': matter_id})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully restored matter")

    def _handle_reopen_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]
        matter_id = param["matter_id"]
        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        try:
            matter = client.matters().reopen(matterId=matter_id).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while reopening matter", e)

        action_result.add_data(matter)
        action_result.update_summary({'matter_id': matter_id})
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully reopened matter")

    def _update_wanted_hold(self, wanted_hold, search_method, emails, ids, org_unit_id):

        def update_hold(key, value):
            wanted_hold.update({key: value})

        org_unit = {'orgUnitId': org_unit_id}
        if search_method == "ORG_UNIT":
            update_hold("orgUnit", org_unit)

        elif search_method == "USER_ACCOUNT":
            accounts = [{"email": email} for email in emails]
            update_hold("accounts", accounts)

        elif search_method == "ALL_GROUPS":
            update_hold("orgUnit", org_unit)

        elif search_method == "GROUP_ACCOUNT":
            accounts = [{"accountId": ac_id} for ac_id in ids]
            update_hold("accounts", accounts)

    def _validate_search_corpus_hold(self, action_result, search_method, corpus, emails_to_search, org_unit_id, group_account_ids):
        if corpus == "GROUPS" and search_method not in ["GROUP_ACCOUNT", "ALL_GROUPS"]:
            return action_result.set_status(phantom.APP_ERROR, GSVAULT_CORPUS_GROUPS_ERROR)

        if corpus in ["MAIL", "DRIVE"] and search_method not in ["ORG_UNIT", "USER_ACCOUNT"]:
            return action_result.set_status(phantom.APP_ERROR, GSVAULT_CORPUS_MAIL_DRIVE_HOLD_ERROR)

        if search_method == "ORG_UNIT" and not org_unit_id:
            return action_result.set_status(phantom.APP_ERROR, INVALID_ORI_UNI_ID)

        if search_method == "USER_ACCOUNT" and not emails_to_search:
            return action_result.set_status(phantom.APP_ERROR, INVALID_USER_ACCOUNT)

        if search_method == "ALL_GROUPS" and not org_unit_id:
            return action_result.set_status(phantom.APP_ERROR, INVALID_ORI_UNI_ID)

        if search_method == "GROUP_ACCOUNT" and not group_account_ids:
            return action_result.set_status(phantom.APP_ERROR, INVALID_GROUP_ACC)

        return phantom.APP_SUCCESS

    def _handle_create_hold(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        name = param['name']
        corpus = param['type']
        search_method = param.get('search_method')
        terms = param.get("terms")
        end_time = param.get("end_time")
        start_time = param.get("start_time")
        org_unit_id = param.get("org_unit_id")
        emails_to_search = param.get("user_email_ids")
        group_account_ids = param.get("group_account_ids")
        include_shared_drive_files = param.get("include_shared_drive_files", DEFAULT_BOOL_STATE)
        matter_id = param["matter_id"]

        is_valid = self._validate_search_corpus_hold(action_result, search_method, corpus, emails_to_search, org_unit_id, group_account_ids)
        if phantom.is_fail(is_valid):
            return action_result.get_status()

        emails = ids = list()
        if search_method == "USER_ACCOUNT":
            if emails_to_search:
                emails = [x.strip() for x in emails_to_search.split(",")]
                emails = list(filter(None, emails))

                if not emails:
                    return action_result.set_status(phantom.APP_ERROR, INVALID_USER_ACCOUNT)

        elif search_method == "GROUP_ACCOUNT":
            if group_account_ids:
                ids = [x.strip() for x in group_account_ids.split(",")]
                ids = list(filter(None, ids))

                if not ids:
                    return action_result.set_status(phantom.APP_ERROR, GSVAULT_CORPUS_GROUPS_ERROR)

        wanted_hold = {
            'name': name,
            'corpus': corpus
        }

        self._update_wanted_hold(wanted_hold, search_method, emails, ids, org_unit_id)

        if corpus == "DRIVE":
            drive_query = dict()

            if include_shared_drive_files:
                drive_query.update({"includeSharedDriveFiles": include_shared_drive_files})

            if drive_query:
                wanted_hold.update({"query": {"driveQuery": drive_query}})

        elif corpus == "MAIL" or corpus == "GROUPS":
            query = dict()
            ret_val = self._validate_time_range(action_result, start_time=start_time, end_time=end_time)

            if phantom.is_fail(ret_val):
                return action_result.get_status()

            if start_time:
                query.update({"startTime": start_time})
            if end_time:
                query.update({"endTime": end_time})
            if terms:
                query.update({"terms": terms})

            if query:
                if corpus == "MAIL":
                    wanted_hold.update({"query": {"mailQuery": query}})
                elif corpus == "GROUPS":
                    wanted_hold.update({"query": {"groupsQuery": query}})

        try:
            hold = client.matters().holds().create(matterId=matter_id, body=wanted_hold).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while creating hold", e)

        action_result.add_data(hold)
        action_result.update_summary({'matter_id': matter_id})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created hold")

    def _validate_time_range(self, action_result, start_time=None, end_time=None, version_date=None):
        # validation for start time and end time
        start = end = None
        try:
            if start_time:
                start = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
            if end_time:
                end = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
            if version_date:
                datetime.datetime.strptime(version_date, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, GSVAULT_TIME_FORMAT_ERROR)

        # validation for incorrect time span
        if start_time and end_time:
            now = datetime.datetime.now()
            if start >= end or start > now:
                return action_result.set_status(phantom.APP_ERROR, GSVAULT_TIME_RANGE_ERROR)

        return phantom.APP_SUCCESS

    def _handle_delete_hold(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]
        matter_id = param["matter_id"]
        hold_id = param["hold_id"]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        ret_val, result = self._delete_single_hold(action_result, client, matter_id, hold_id)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        action_result.add_data(result)
        action_result.update_summary({'matter_id': matter_id})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully deleted hold")

    def _delete_single_hold(self, action_result, client, matter_id, hold_id):

        try:
            response = client.matters().holds().delete(matterId=matter_id, holdId=hold_id).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while deleting hold", e), None

        return phantom.APP_SUCCESS, response

    def _handle_add_held_account(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        account_id = param["account_id"]
        matter_id = param["matter_id"]
        hold_id = param["hold_id"]

        held_account = {'accountId': account_id}

        try:
            result = client.matters().holds().accounts().create(matterId=matter_id, holdId=hold_id, body=held_account).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while adding held account to hold for given matter ID", e)

        action_result.add_data(result)
        action_result.update_summary({'matter_id': matter_id})

        message = SUCCESS_ADDED_HELD_ACCOUNT.format(hold_id=hold_id, matter_id=matter_id)
        return action_result.set_status(phantom.APP_SUCCESS, message)

    def _handle_remove_held_account(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]
        account_id = param["account_id"]
        matter_id = param["matter_id"]
        hold_id = param["hold_id"]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        try:
            result = client.matters().holds().accounts().delete(matterId=matter_id, holdId=hold_id, accountId=account_id).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while removing held account to hold for given matter ID", e)

        action_result.add_data(result)
        action_result.update_summary({'hold_id': hold_id, 'matter_id': matter_id})

        message = SUCCESS_REMOVED_HELD_ACCOUNT.format(hold_id=hold_id, matter_id=matter_id)
        return action_result.set_status(phantom.APP_SUCCESS, message)

    def _handle_list_holds(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        matter_id = param["matter_id"]

        limit = self._validate_integer(action_result, param.get("limit", DEFAULT_LIMIT), 'limit', allow_zero=False)

        if limit is None:
            return action_result.get_status()
        try:
            holds = self._paginator(client, limit=limit, matter_id=matter_id)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while listing holds", e)

        if not holds:
            return action_result.set_status(phantom.APP_ERROR, "No data found")

        for hold in holds:
            action_result.add_data(hold)

        num_holds = len(holds)
        action_result.update_summary({'total_holds_returned': num_holds})

        return action_result.set_status(phantom.APP_SUCCESS, 'Successfully retrieved {} hold{}'.format(num_holds, '' if num_holds == 1 else 's'))

    def _handle_list_exports(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        matter_id = param["matter_id"]

        limit = self._validate_integer(action_result, param.get("limit", DEFAULT_LIMIT), 'limit', allow_zero=False)

        if limit is None:
            return action_result.get_status()
        try:
            exports = self._paginator(client, limit=limit, matter_id=matter_id)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while listing exports", e)

        if not exports:
            return action_result.set_status(phantom.APP_ERROR, "No data found")

        for export in exports:
            action_result.add_data(export)

        num_exports = len(exports)
        action_result.update_summary({'total_exports_returned': num_exports})

        return action_result.set_status(phantom.APP_SUCCESS, 'Successfully retrieved {} export{}'.format(
            num_exports, '' if num_exports == 1 else 's'))

    def _paginator(self, client, limit=None, view=None, matter_id=None, hold_flag=False, domain=None):
        """
        This action is used to create an iterator that will paginate through responses from called methods.

        :param method_name: Name of method whose response is to be paginated
        :param action_result: Object of ActionResult class
        :param **kwargs: Dictionary of Input parameters
        """

        list_items = list()
        page_token = None
        action_id = self.get_action_identifier()

        kwargs = {}

        if action_id == "list_organizations":
            kwargs['customerId'] = 'my_customer'
        elif action_id == "list_groups":
            kwargs['domain'] = domain

        if view:
            kwargs.update({"state": view})

        if matter_id:
            kwargs.update({"matterId": matter_id})

        while True:
            if page_token:
                kwargs.update({"pageToken": page_token})
            response = None
            if action_id == "list_matters":
                response = client.matters().list(**kwargs).execute()
                if response.get("matters"):
                    list_items.extend(response.get("matters"))

            elif action_id == "list_organizations":
                response = client.orgunits().list(**kwargs).execute()
                if response.get("organizationUnits"):
                    list_items.extend(response.get("organizationUnits"))

            elif action_id == "list_groups":
                response = client.groups().list(**kwargs).execute()
                if response.get("groups"):
                    list_items.extend(response.get("groups"))

            elif action_id == "list_holds" or hold_flag:
                response = client.matters().holds().list(**kwargs).execute()
                if response.get("holds"):
                    list_items.extend(response.get("holds"))

            elif action_id == "list_exports":
                response = client.matters().exports().list(**kwargs).execute()
                if response.get("exports"):
                    list_items.extend(response.get("exports"))

            if limit and len(list_items) >= limit:
                return list_items[:limit]

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return list_items

    def _vaidate_search_corpus(self, action_result, search_method, corpus, org_unit_id, emails_to_search, shared_drive_ids, data_scope):
        if corpus == "MAIL":
            if search_method not in ["ORG_UNIT", "ACCOUNT"]:
                return action_result.set_status(phantom.APP_ERROR, GSVAULT_CORPUS_MAIL_DRIVE_EXPORT_ERROR)

        if search_method == "ORG_UNIT" and not org_unit_id:
            return action_result.set_status(phantom.APP_ERROR, INVALID_ORI_UNI_ID)

        if search_method == "ACCOUNT" and not emails_to_search:
            return action_result.set_status(phantom.APP_ERROR, INVALID_USER_EMAILS)

        if search_method == "TEAM_DRIVE" and not shared_drive_ids:
            return action_result.set_status(phantom.APP_ERROR, INVALID_USER_ID)

        if corpus == "GROUPS" and search_method != "ACCOUNT":
            return action_result.set_status(phantom.APP_ERROR, INVALID_ACCOUNT_SELECT)

        if corpus == "DRIVE" and data_scope == "UNPROCESSED_DATA":
            return action_result.set_status(phantom.APP_ERROR, INVALID_UNPROCESSED_DATA)

        if corpus == "DRIVE" and data_scope == "HELD_DATA" and search_method == "TEAM_DRIVE":
            return action_result.set_status(phantom.APP_ERROR, INVALID_HELD_DATA)

        return phantom.APP_SUCCESS

    def _update_query(self, query, search_method, data_scope, timezone, ids, emails, terms, start_time, end_time, org_unit_id):
        if start_time:
            query.update({"startTime": start_time})
        if end_time:
            query.update({"endTime": end_time})

        if data_scope != "HELD_DATA":
            if timezone:
                query.update({"timeZone": timezone})

        if data_scope != "UNPROCESSED_DATA":
            if terms:
                query.update({"terms": terms})

        if search_method == "ORG_UNIT":
            org_dict = {
                "orgUnitInfo": {
                    "org_unit_id": org_unit_id
                }
            }
            query.update(org_dict)

        if search_method == "ACCOUNT":
            account_dict = {
                "accountInfo": {
                    "emails": emails
                }
            }
            query.update(account_dict)

        if search_method == "TEAM_DRIVE":
            drive_dict = {
                "sharedDriveInfo": {
                    "sharedDriveIds": ids
                }
            }
            query.update(drive_dict)

    def _handle_create_export(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        name = param['name']
        corpus = param['type']
        data_scope = param['data_scope']
        search_method = param['search_method']

        terms = param.get("terms")
        end_time = param.get("end_time")
        timezone = param.get("time_zone")
        start_time = param.get("start_time")
        data_region = param.get("data_region")
        org_unit_id = param.get("org_unit_id")
        version_date = param.get("version_date")
        emails_to_search = param.get("email_ids")
        shared_drive_ids = param.get("shared_drive_ids")
        export_format = param.get("export_format")

        exclude_drafts = param.get("exclude_drafts", DEFAULT_BOOL_STATE)
        include_access_info = param.get("include_access_info", DEFAULT_BOOL_STATE)
        include_shared_drives = param.get("include_shared_drives", DEFAULT_BOOL_STATE)
        show_confidential_mode_content = param.get("show_confidential_mode_content", DEFAULT_BOOL_STATE)
        matter_id = param["matter_id"]

        is_valid = self._vaidate_search_corpus(action_result, search_method, corpus, org_unit_id, emails_to_search, shared_drive_ids, data_scope)
        if phantom.is_fail(is_valid):
            return action_result.get_status()

        query = {
            'corpus': corpus,
            'dataScope': data_scope,
            'searchMethod': search_method
        }

        emails = ids = list()
        if search_method == "ACCOUNT":
            if emails_to_search:
                emails = [x.strip() for x in emails_to_search.split(",")]
                emails = list(filter(None, emails))

                if not emails:
                    return action_result.set_status(phantom.APP_ERROR, INVALID_USER_EMAILS)

        elif search_method == "TEAM_DRIVE":
            if shared_drive_ids:
                ids = [x.strip() for x in shared_drive_ids.split(",")]
                ids = list(filter(None, ids))

                if not ids:
                    return action_result.set_status(phantom.APP_ERROR, INVALID_USER_ID)

        ret_val = self._validate_time_range(action_result, start_time=start_time, end_time=end_time)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        self._update_query(query, search_method, data_scope, timezone, ids, emails, terms, start_time, end_time, org_unit_id)

        wanted_export = {
            'name': name
        }

        export_options = dict()

        if corpus == "MAIL":
            mail_export_options = dict()

            if export_format:
                mail_export_options.update({"exportFormat": export_format})
            if show_confidential_mode_content:
                mail_export_options.update({"showConfidentialModeContent": show_confidential_mode_content})

            if mail_export_options:
                export_options.update({"mailOptions": mail_export_options})

            if exclude_drafts:
                query.update({"mailOptions": {"excludeDrafts": exclude_drafts}})

        elif corpus == "DRIVE":
            drive_options = dict()

            if include_access_info:
                export_options.update({"driveOptions": {'includeAccessInfo': include_access_info}})

            if version_date:
                ret_val = self._validate_time_range(action_result, version_date=version_date)

                if phantom.is_fail(ret_val):
                    return action_result.get_status()

                drive_options.update({"versionDate": version_date})

            if include_shared_drives:
                drive_options.update({'includeSharedDrives': include_shared_drives})

            if drive_options:
                query.update({"driveOptions": drive_options})

        elif corpus == "GROUPS":
            if export_format:
                export_options.update({"groupsOptions": {"exportFormat": export_format}})

        if data_region:
            export_options.update({"region": data_region})

        wanted_export.update({"query": query})

        if export_options:
            wanted_export.update({"exportOptions": export_options})

        try:
            export = client.matters().exports().create(matterId=matter_id, body=wanted_export).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while creating export", e)

        action_result.add_data(export)
        action_result.update_summary({'matter_id': matter_id})

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created export")

    def _handle_get_export(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)
        matter_id = param["matter_id"]
        export_id = param["export_id"]

        if phantom.is_fail(ret_val):
            self.debug_print(FAILED_CREATE_GVAULT)
            return ret_val

        try:
            result = client.matters().exports().get(matterId=matter_id, exportId=export_id).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while fetching export", e)

        action_result.add_data(result)
        action_result.update_summary({'matter_id': matter_id})
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully fetched export")

    def handle_action(self, param):
        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", action_id)

        # Dictionary mapping each action with its corresponding actions
        supported_actions = {
            'list_matters': self._handle_list_matters,
            'create_matter': self._handle_create_matter,
            'get_matter': self._handle_get_matter,
            'delete_matter': self._handle_delete_matter,
            'restore_matter': self._handle_restore_matter,
            'reopen_matter': self._handle_reopen_matter,
            'close_matter': self._handle_close_matter,
            'create_export': self._handle_create_export,
            'test_connectivity': self._handle_test_connectivity,
            'get_export': self._handle_get_export,
            'list_exports': self._handle_list_exports,
            'create_hold': self._handle_create_hold,
            'list_holds': self._handle_list_holds,
            'delete_hold': self._handle_delete_hold,
            'add_held_account': self._handle_add_held_account,
            'remove_held_account': self._handle_remove_held_account,
            'list_organizations': self._handle_list_organizations,
            'list_groups': self._handle_list_groups
        }

        try:
            run_action = supported_actions[action_id]
        except Exception:
            raise ValueError('action %r is not supported' % action_id)

        return run_action(param)

    def initialize(self):

        config = self.get_config()
        self._state = self.load_state()
        key_json = config['key_json']

        try:
            key_dict = json.loads(key_json)
        except Exception as e:
            return self.set_status(phantom.APP_ERROR, "Unable to load the key json", e)

        self._key_dict = key_dict

        login_email = config['login_email']

        if not ph_utils.is_email(login_email):
            return self.set_status(phantom.APP_ERROR, "Asset config 'login_email' failed validation")

        self._login_email = login_email

        return phantom.APP_SUCCESS

    def finalize(self):

        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import argparse
    import sys

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:
        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        login_url = BaseConnector._get_phantom_base_url() + "login"
        try:
            print("Accessing the Login page")
            r = requests.get(login_url, verify=True, timeout=DEFAULT_TIMEOUT)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=True, data=data, headers=headers, timeout=DEFAULT_TIMEOUT)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = GoogleVaultConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
