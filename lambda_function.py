# -*- coding: utf-8 -*-

from change_state import change_state

def lambda_handler(event, context):
    status_code = change_state(event)
    return {
        'statusCode': status_code,
    }