#!/bin/bash

echo "🗄️  Configurando base de datos Colombia Explora..."

# Configuración
DB_HOST="localhost"
DB_NAME="colombia_explora"
DB_USER="explora_user"
DB_PASSWORD="ExploraPass123!"

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
until pg_isready -h $DB_HOST -p 5432 -U $DB_USER; do
  sleep 1
done

# Ejecutar script SQL
echo "📝 Ejecutando esquema de base de datos..."
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f scripts/database/init-database.sql

echo "✅ Base de datos configurada exitosamente!"