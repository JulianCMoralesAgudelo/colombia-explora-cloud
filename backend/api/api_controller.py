import json
import jwt
from datetime import datetime
import os
from db import get_db_connection
import logging

logger = logging.getLogger()

JWT_SECRET = os.environ.get('JWT_SECRET', 'fallback-secret')

def api_handler(event, context):
    path = event['requestContext']['http']['path']
    method = event['requestContext']['http']['method']
    
    # Verificar autenticación para endpoints protegidos
    if path != '/api/destinations' or method != 'GET':
        auth_header = event.get('headers', {}).get('authorization', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response('Authentication required', 401)
        
        token = auth_header[7:]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user_role = payload.get('role')
        except jwt.ExpiredSignatureError:
            return error_response('Token expired', 401)
        except jwt.InvalidTokenError:
            return error_response('Invalid token', 401)
    else:
        user_id = None
        user_role = None
    
    # Routing de endpoints
    if path == '/api/destinations' and method == 'GET':
        return get_destinations()
    elif path == '/api/destinations' and method == 'POST':
        if user_role != 'admin':
            return error_response('Admin access required', 403)
        return create_destination(event)
    elif path.startswith('/api/destinations/') and method == 'PATCH':
        if user_role != 'admin':
            return error_response('Admin access required', 403)
        destination_id = path.split('/')[-1]
        return update_destination(event, destination_id)
    elif path.startswith('/api/destinations/') and method == 'DELETE':
        if user_role != 'admin':
            return error_response('Admin access required', 403)
        destination_id = path.split('/')[-1]
        return delete_destination(destination_id)
    elif path == '/api/reservations' and method == 'GET':
        return get_user_reservations(user_id)
    elif path == '/api/reservations' and method == 'POST':
        return create_reservation(event, user_id)
    elif path == '/api/health' and method == 'GET':
        return success_response({'status': 'ok'})
    else:
        return error_response('Endpoint not found', 404)

def get_destinations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, name, description, region, price, created_at 
            FROM destinations 
            ORDER BY created_at DESC
        """)
        destinations = cursor.fetchall()
        
        # Convertir Decimal a float para JSON
        for dest in destinations:
            if dest['price']:
                dest['price'] = float(dest['price'])
        
        return success_response(destinations)
        
    except Exception as e:
        logger.error(f"Get destinations error: {e}")
        return error_response('Failed to fetch destinations', 500)

def create_destination(event):
    try:
        body = json.loads(event['body'])
        name = body.get('name')
        description = body.get('description')
        region = body.get('region')
        price = body.get('price')
        
        if not all([name, region, price]):
            return error_response('Missing required fields', 400)
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            INSERT INTO destinations (name, description, region, price) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id, name, description, region, price, created_at
        """, (name, description, region, price))
        
        destination = cursor.fetchone()
        conn.commit()
        
        if destination['price']:
            destination['price'] = float(destination['price'])
        
        return success_response(destination, 201)
        
    except Exception as e:
        logger.error(f"Create destination error: {e}")
        return error_response('Failed to create destination', 500)

def update_destination(event, destination_id):
    try:
        body = json.loads(event['body'])
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Verificar que el destino existe
        cursor.execute("SELECT id FROM destinations WHERE id = %s", (destination_id,))
        if not cursor.fetchone():
            return error_response('Destination not found', 404)
        
        update_fields = []
        update_values = []
        
        if 'name' in body:
            update_fields.append("name = %s")
            update_values.append(body['name'])
        if 'description' in body:
            update_fields.append("description = %s")
            update_values.append(body['description'])
        if 'region' in body:
            update_fields.append("region = %s")
            update_values.append(body['region'])
        if 'price' in body:
            update_fields.append("price = %s")
            update_values.append(body['price'])
        
        if not update_fields:
            return error_response('No fields to update', 400)
        
        update_values.append(destination_id)
        
        query = f"""
            UPDATE destinations 
            SET {', '.join(update_fields)} 
            WHERE id = %s 
            RETURNING id, name, description, region, price, created_at
        """
        
        cursor.execute(query, update_values)
        destination = cursor.fetchone()
        conn.commit()
        
        if destination['price']:
            destination['price'] = float(destination['price'])
        
        return success_response(destination)
        
    except Exception as e:
        logger.error(f"Update destination error: {e}")
        return error_response('Failed to update destination', 500)

def delete_destination(destination_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Verificar que el destino existe
        cursor.execute("SELECT id FROM destinations WHERE id = %s", (destination_id,))
        if not cursor.fetchone():
            return error_response('Destination not found', 404)
        
        cursor.execute("DELETE FROM destinations WHERE id = %s", (destination_id,))
        conn.commit()
        
        return success_response({'message': 'Destination deleted successfully'})
        
    except Exception as e:
        logger.error(f"Delete destination error: {e}")
        return error_response('Failed to delete destination', 500)

def get_user_reservations(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT r.id, r.people, r.check_in, r.check_out, r.total_price, r.created_at,
                   d.name as destination_name, d.region, d.price as destination_price
            FROM reservations r
            JOIN destinations d ON r.destination_id = d.id
            WHERE r.user_id = %s
            ORDER BY r.created_at DESC
        """, (user_id,))
        
        reservations = cursor.fetchall()
        
        # Convertir Decimal a float
        for res in reservations:
            if res['total_price']:
                res['total_price'] = float(res['total_price'])
            if res['destination_price']:
                res['destination_price'] = float(res['destination_price'])
        
        return success_response(reservations)
        
    except Exception as e:
        logger.error(f"Get reservations error: {e}")
        return error_response('Failed to fetch reservations', 500)

def create_reservation(event, user_id):
    try:
        body = json.loads(event['body'])
        destination_id = body.get('destination_id')
        people = body.get('people')
        check_in = body.get('check_in')
        check_out = body.get('check_out')
        
        if not all([destination_id, people, check_in, check_out]):
            return error_response('Missing required fields', 400)
        
        # Validar fechas
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        
        if check_out_date <= check_in_date:
            return error_response('Check-out date must be after check-in date', 400)
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Obtener precio del destino
        cursor.execute("SELECT price FROM destinations WHERE id = %s", (destination_id,))
        destination = cursor.fetchone()
        
        if not destination:
            return error_response('Destination not found', 404)
        
        # Calcular precio total
        days = (check_out_date - check_in_date).days
        total_price = float(destination['price']) * people * days
        
        # Crear reserva
        cursor.execute("""
            INSERT INTO reservations (user_id, destination_id, people, check_in, check_out, total_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, user_id, destination_id, people, check_in, check_out, total_price, created_at
        """, (user_id, destination_id, people, check_in, check_out, total_price))
        
        reservation = cursor.fetchone()
        conn.commit()
        
        reservation['total_price'] = float(reservation['total_price'])
        
        return success_response(reservation, 201)
        
    except Exception as e:
        logger.error(f"Create reservation error: {e}")
        return error_response('Failed to create reservation', 500)

def success_response(data, status_code=200):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(data)
    }

def error_response(message, status_code):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps({'error': message})
    }