import json
import jwt
import bcrypt
from datetime import datetime, timedelta
import os
from backend.db import get_db_connection
import logging

logger = logging.getLogger()

JWT_SECRET = os.environ.get('JWT_SECRET', 'fallback-secret')
JWT_ALGORITHM = 'HS256'

def auth_handler(event, context):
    path = event['requestContext']['http']['path']
    method = event['requestContext']['http']['method']
    
    if path == '/auth/register' and method == 'POST':
        return register_user(event)
    elif path in ['/auth/login', '/auth/token'] and method == 'POST':
        return login_user(event)
    elif path == '/auth/health' and method == 'GET':
        return {'statusCode': 200, 'body': json.dumps({'status': 'ok'})}
    else:
        return {'statusCode': 404, 'body': json.dumps({'error': 'Endpoint not found'})}

def register_user(event):
    try:
        body = json.loads(event['body'])
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')
        
        if not all([username, email, password]):
            return error_response('Missing required fields', 400)
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Verificar si usuario existe
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            return error_response('User already exists', 400)
        
        # Crear usuario
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password, role) VALUES (%s, %s, %s, %s) RETURNING id, username, email, role",
            (username, email, hashed_password, 'user')
        )
        user = cursor.fetchone()
        conn.commit()
        
        return success_response({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }, 201)
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return error_response('Registration failed', 500)

def login_user(event):
    try:
        body = json.loads(event['body'])
        username = body.get('username')
        password = body.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            "SELECT id, username, email, hashed_password, role FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
            return error_response('Invalid credentials', 401)
        
        # Generar JWT
        token_payload = {
            'sub': user['username'],
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return success_response({
            'access_token': token,
            'token_type': 'bearer',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        })
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return error_response('Login failed', 500)

def success_response(data, status_code=200):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }

def error_response(message, status_code):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': message})
    }