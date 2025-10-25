import os
import psycopg2
from psycopg2.extras import RealDictCursor  # ✅ Importación correcta
import logging

logger = logging.getLogger()

def get_db_connection():
    """Conexión síncrona para Lambda"""
    try:
        connection = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            port=os.environ.get('DB_PORT', '5432')
        )
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise e

def execute_query(query, params=None):
    """Ejecutar query y retornar resultados como diccionarios"""
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:  # ✅ Ahora funciona
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                if query.strip().upper().startswith('INSERT'):
                    return cursor.fetchone()  # Para INSERT ... RETURNING
                return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()