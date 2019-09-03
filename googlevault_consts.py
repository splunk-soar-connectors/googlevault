# File: googlevault_consts.py
# Copyright (c) 2019 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

GOOGLE_SCOPE = 'https://www.googleapis.com/auth/ediscovery'
GSVAULT_INVALID_LIMIT = "Please provide non-zero positive integer in limit"
GSVAULT_TIME_FORMAT_ERROR = "Please provide date/time in '%Y-%m-%dT%H:%M:%SZ' format"
GSVAULT_TIME_RANGE_ERROR = "The given time range is incorrect"
GSVAULT_CORPUS_GROUPS_ERROR = "You have to provide either group_account_ids or org_unit_id for corpus type GROUPS "
GSVAULT_CORPUS_GROUPS_ERROR += "(If you want to create hold for search method ALL_GROUPS you have to provide org_unit_id of that groups" 
GSVAULT_CORPUS_GROUPS_ERROR += "and for search method GROUP_ACCOUNT you have to provide group_ids)"

GSVAULT_CORPUS_MAIL_DRIVE_HOLD_ERROR = "You have to provide either email_ids or org_unit_id for corpus type MAIL or DRIVE "
GSVAULT_CORPUS_MAIL_DRIVE_HOLD_ERROR += "(If you want to create hold for search method USER_ACCOUNT you have to provide email_ids of that users" 
GSVAULT_CORPUS_MAIL_DRIVE_HOLD_ERROR += "and for search method ORG_UNIT you have to provide org_unit_id)"

GSVAULT_CORPUS_MAIL_DRIVE_EXPORT_ERROR = "You have to provide either ORG_UNIT or ACCOUNT for corpus type MAIL or DRIVE"