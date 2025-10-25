import json
import os
from auth.auth_controller import auth_handler
from api.api_controller import api_handler
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        path = event['requestContext']['http']['path']
        method = event['requestContext']['http']['method']
        
        logger.info(f"Processing {method} {path}")
        
        # Routing basado en paths
        if path.startswith('/auth') or path in ['/login', '/register']:
            return auth_handler(event, context)
        elif path.startswith('/api') or path.startswith('/destinations') or path.startswith('/reservations'):
            return api_handler(event, context)
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal server error'})
        }