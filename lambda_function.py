# -*- coding: utf-8 -*-

from change_state import change_state

def lambda_handler(event, context):
    response = change_state(event)
    return {
        'statusCode': 200,
        'response': response
    }