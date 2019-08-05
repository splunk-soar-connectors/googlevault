# -----------------------------------------
# Google Vault App
# -----------------------------------------

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

from googlevault_consts import *

import requests
import json

from googleapiclient.discovery import build
from httplib2 import http
from oauth2client import file, client tools



class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class GoogleVaultConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(GoogleVaultConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def _create_client(self):
        config = self.get_config()
        SCOPES = 'https://www.googleapis.com/auth/ediscovery'
        service_account_json = json.loads(config['key_json'])
        credentials = service_account_json.Credentials.from_service_account_info(service_account_json)

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            credentials = tools.run_flow(flow, store)
        client = build('vault', 'v1', http=creds.authorize(Http()))

        return client

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Creating Google Vault client...")
        try:
            client = self._create_client()
        except Exception as e:
            self.save_progress("Test Connectivity Failed")
            return action_result.set_status(phantom.APP_ERROR, "Error creating client", e)

        self.save_progress("Making test call to Google Vault...")
        try:
            results = service.matters().list(pageSize=10).execute()
            matters = results.get('matters', [])
        except Exception as e:
            self.save_progress("Test Connectivity Failed")
            return action_result.set_status(phantom.APP_ERROR, "Error listing Matters", e)

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_delete_hold(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        matterid = param['matterid']
        holdid = param['holdid']

        # make rest call
        ret_val, response = self._make_rest_call('/v1/matters/{matterId}/holds/{holdId}', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        action_result.add_data(response)

        summary = action_result.update_summary({})
        summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_remove_heldaccounts(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        matterid = param['matterid']
        holdid = param['holdid']
        accountids = param['accountids']

        ret_val, response = self._make_rest_call('/v1/matters/{matterId}/holds/{holdId}:removeHeldAccounts', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)


    def _handle_get_export(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        matterid = param['matterid']
        exportid = param['exportid']

        ret_val, response = self._make_rest_call('/v1/matters/{matterId}/exports/{exportId}', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_create_export(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        matterid = param['matterid']

        ret_val, response = self._make_rest_call('/v1/matters/{matterId}/exports', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        action_result.add_data(response)

        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_add_heldaccounts(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        matterid = param['matterid']
        holdid = param['holdid']
        emails = param['emails']

        ret_val, response = self._make_rest_call('/v1/matters/{matterId}/holds/{holdId}:addHeldAccounts', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_create_hold(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        matterid = param['matterid']

        ret_val, response = self._make_rest_call('/vi/matters/{matterId}/holds', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_matter(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        # required_parameter = param['required_parameter']

        ret_val, response = self._make_rest_call('/vi/matters/list', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        action_result.add_data(response)

        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_create_matter(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Required values can be accessed directly
        name = param['name']
        description = param['description']

        # Optional values should use the .get() function
        # optional_parameter = param.get('optional_parameter', 'default_value')

        # make rest call
        ret_val, response = self._make_rest_call('/v1/matters/create', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        # Now post process the data,  uncomment code as you deem fit

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'delete_hold':
            ret_val = self._handle_delete_hold(param)

        elif action_id == 'remove_heldaccounts':
            ret_val = self._handle_remove_heldaccounts(param)

        elif action_id == 'get_export':
            ret_val = self._handle_get_export(param)

        elif action_id == 'create_export':
            ret_val = self._handle_create_export(param)

        elif action_id == 'add_heldaccounts':
            ret_val = self._handle_add_heldaccounts(param)

        elif action_id == 'create_hold':
            ret_val = self._handle_create_hold(param)

        elif action_id == 'list_matter':
            ret_val = self._handle_list_matter(param)

        elif action_id == 'create_matter':
            ret_val = self._handle_create_matter(param)

        return ret_val

    def initialize(self):

        self._state = self.load_state()
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