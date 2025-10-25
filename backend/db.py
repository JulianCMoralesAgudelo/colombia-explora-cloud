import os
import asyncpg
from sqlmodel import SQLModel
import psycopg2
from psycopg2.extras import RealDictCursor
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

async def get_async_db():
    """Conexión asíncrona (si se necesita)"""
    return await asyncpg.create_pool(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=os.environ.get('DB_PORT', '5432')
    )