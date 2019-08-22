# File: googlevault_connector.py
# Copyright (c) 2019 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.


# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
import phantom.utils as ph_utils

from googlevault_consts import *
import os
init_path = '{}/dependencies/google/__init__.py'.format(  # noqa
    os.path.dirname(os.path.abspath(__file__))  # noqa
)  # noqa
try:
    open(init_path, 'a+').close()  # noqa
except:  # noqa
    pass  # noqa


import requests
import json

from googleapiclient import discovery
from google.oauth2 import service_account


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

        if (self._login_email):
            try:
                credentials = credentials.with_subject(self._login_email)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "Failed to create delegated credentials", e), None

        self.debug_print("credentials: {}".format(credentials))
        client = discovery.build('vault', 'v1', credentials=credentials)

        return phantom.APP_SUCCESS, client

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]
        self.save_progress("Creating Google Vault client...")

        ret_val, client = self._create_client(action_result, scopes)
        self.debug_print("Services: {}".format(client))

        if phantom.is_fail(ret_val):
            self.save_progress("Test Connectivity Failed")
            return ret_val

        self.save_progress("Making test call to Google Vault...")
        try:
            results = client.matters().list(pageSize=10).execute()
            self.debug_print("Results: {}".format(results))
        except Exception as e:
            self.save_progress("Test Connectivity Failed")
            return action_result.set_status(phantom.APP_ERROR, "Error listing Matters", e)

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_matters(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print("Failed to create Google Vault client")
            return ret_val

        view = param.get("view").upper() if param.get("view") else None

        limit = param.get("limit")
        if (limit and not str(limit).isdigit()) or limit == 0:
            return action_result.set_status(phantom.APP_ERROR, GSVAULT_INVALID_LIMIT)
        try:
            matters = self._paginator(view, limit, client)
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while listing Matters", e)

        if not matters:
            return action_result.set_status(phantom.APP_ERROR, "No data found")

        for matter in matters:
            action_result.add_data(matter)

        num_matters = len(matters)
        action_result.update_summary({'total_matters_returned': num_matters})

        return action_result.set_status(phantom.APP_SUCCESS, 'Successfully retrieved {} matter{}'.format(num_matters, '' if num_matters == 1 else 's'))

    def _handle_create_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print("Failed to create Google Vault client")
            return ret_val

        matter_content = {
            'name': param.get("name"),
            'description': param.get("description"),
        }
        try:
            matter = client.matters().create(body=matter_content).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while creating matter", e)

        action_result.add_data(matter)
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created matter")

    def _handle_close_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print("Failed to create Google Vault client")
            return ret_val

        try:
            matter = client.matters().close(matterId=param.get("matter_id")).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while closing matter", e)

        action_result.add_data(matter)
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully closed matter")

    def _handle_delete_matter(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        scopes = [GOOGLE_SCOPE]

        ret_val, client = self._create_client(action_result, scopes)

        if phantom.is_fail(ret_val):
            self.debug_print("Failed to create Google Vault client")
            return ret_val

        try:
            matter = client.matters().delete(matterId=param.get("matter_id")).execute()
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR, "Error while deleting matter", e)

        action_result.add_data(matter)
        return action_result.set_status(phantom.APP_SUCCESS, "Successfully deleted matter")

    def _paginator(self, view, limit, client):
        """
        This action is used to create an iterator that will paginate through responses from called methods.

        :param method_name: Name of method whose response is to be paginated
        :param action_result: Object of ActionResult class
        :param **kwargs: Dictionary of Input parameters
        """

        list_items = list()
        page_token = None

        kwargs = {}

        if view:
            kwargs.update({"state": view})

        while True:
            if page_token:
                kwargs.update({"pageToken": page_token})
                response = client.matters().list(**kwargs).execute()
            else:
                response = client.matters().list(**kwargs).execute()

            if response.get("matters"):
                list_items.extend(response.get("matters"))

            if limit and len(list_items) >= limit:
                return list_items[:limit]

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        return list_items

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        if action_id == 'list_matters':
            ret_val = self._handle_list_matters(param)
        if action_id == 'create_matter':
            ret_val = self._handle_create_matter(param)
        if action_id == 'delete_matter':
            ret_val = self._handle_delete_matter(param)
        if action_id == 'close_matter':
            ret_val = self._handle_close_matter(param)

        return ret_val

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

        if (not ph_utils.is_email(login_email)):
            return self.set_status(phantom.APP_ERROR, "Asset config 'login_email' failed validation")

        self._login_email = login_email

        return phantom.APP_SUCCESS

    def finalize(self):

        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            print ("Accessing the Login page")
            r = requests.get("https://127.0.0.1/login", verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = 'https://127.0.0.1/login'

            print ("Logging into Platform to get the session id")
            r2 = requests.post("https://127.0.0.1/login", verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print ("Unable to get session id from the platfrom. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = GoogleVaultConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
