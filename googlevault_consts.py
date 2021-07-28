# File: googlevault_consts.py
# Copyright (c) 2019-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

GOOGLE_SCOPE = 'https://www.googleapis.com/auth/ediscovery'
GOOGLE_ORGANIZATIONS_SCOPE = ['https://www.googleapis.com/auth/admin.directory.orgunit', 'https://www.googleapis.com/auth/admin.directory.orgunit.readonly']
GOOGLE_SCOPE_GROUP = 'https://www.googleapis.com/auth/admin.directory.group'
GOOGLE_SCOPE_GROUP_READONLY = 'https://www.googleapis.com/auth/admin.directory.group.readonly'
GOOGLE_SCOPE_MEMBER_READONLY = 'https://www.googleapis.com/auth/admin.directory.group.member.readonly'
GOOGLE_SCOPE_MEMBER = 'https://www.googleapis.com/auth/admin.directory.group.member'
GOOGLE_GROUPS_SCOPE = [GOOGLE_SCOPE_GROUP, GOOGLE_SCOPE_GROUP_READONLY, GOOGLE_SCOPE_MEMBER_READONLY, GOOGLE_SCOPE_MEMBER]
GSVAULT_INVALID_LIMIT = "Please provide non-zero positive integer in {param}]"
GSVAULT_TIME_FORMAT_ERROR = "Please provide date/time in '%Y-%m-%dT%H:%M:%SZ' format"
GSVAULT_TIME_RANGE_ERROR = "The given time range is incorrect"
GSVAULT_CORPUS_GROUPS_ERROR = "You have to provide either group_account_ids or org_unit_id for corpus type GROUPS "
GSVAULT_CORPUS_GROUPS_ERROR += "(If you want to create hold for search method ALL_GROUPS you have to provide org_unit_id of that groups"
GSVAULT_CORPUS_GROUPS_ERROR += "and for search method GROUP_ACCOUNT you have to provide group_ids)"

GSVAULT_CORPUS_MAIL_DRIVE_HOLD_ERROR = "You have to provide either email_ids or org_unit_id for corpus type MAIL or DRIVE "
GSVAULT_CORPUS_MAIL_DRIVE_HOLD_ERROR += "(If you want to create hold for search method USER_ACCOUNT you have to provide email_ids of that users"
GSVAULT_CORPUS_MAIL_DRIVE_HOLD_ERROR += "and for search method ORG_UNIT you have to provide org_unit_id)"

GSVAULT_CORPUS_MAIL_DRIVE_EXPORT_ERROR = "You have to provide either ORG_UNIT or ACCOUNT for corpus type MAIL"

CREATE_GOOGLE_VAULT_CLIENT = "Creating Google Vault client..."
TEST_CONNECTIVITY_FAILED = "Test Connectivity Failed"
MAKING_TEST_CALL_GOOGLE_VAULT = "Making test call to Google Vault for fetching the list of matters..."
TEST_CONNECTIVITY_PASSED = "Test Connectivity Passed"
ERROR_WHILE_LISTING_MATTERS = "Error while listing matters"
INVALID_INT = "Please provide a valid integer value in the {param}"
ERR_NEGATIVE_INT_PARAM = "Please provide a valid non-negative integer value in the {param}"
GOOGLE_VAULT_EXCEPTION = "Google vault exception: "
NO_DATA_FOUND = "No data found"

INVALID_ORI_UNI_ID = "Please provide valid org_unit_id for search method ORG_UNIT"
INVALID_USER_EMAILS = "Please provide valid list of user emails for search method ACCOUNT"
INVALID_USER_ID = "Please provide valid list of shared drive ids for search method TEAM_DRIVE"
INVALID_ACCOUNT_SELECT = "Please select ACCOUNT search method for corpus type GROUPS"
INVALID_UNPROCESSED_DATA = "UNPROCESSED_DATA data scope is not allowed for corpus type DRIVE"
INVALID_HELD_DATA = "TEAM_DRIVE search method is not allowed for corpus type DRIVE and data scope HELD_DATA"
INVALID_GROUP_ACC = "Please provide valid list of group account ID for search method GROUP_ACCOUNT"
INVALID_USER_ACCOUNT = "Please provide valid list of user emails for search method USER_ACCOUNT"

FAILED_CREATE_GVAULT = "Failed to create the Google Vault client"
SUCCESS_CREATED_M_H = "Successfully added held account to {hold_id} hold id for {matter_id} matter id"
