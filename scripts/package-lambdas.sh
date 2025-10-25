#!/bin/bash

echo "📦 Empaquetando funciones Lambda..."

cd backend

# Limpiar empaquetado anterior
rm -rf package
rm -f ../deploy/function.zip

# Crear directorio temporal
mkdir -p package

# Instalar dependencias
echo "Instalando dependencias Python..."
pip install -r requirements.txt -t package/

# Copiar código
echo "Copiando código fuente..."
cp *.py package/
cp -r auth/ package/
cp -r api/ package/

# Crear archivo ZIP
echo "Creando ZIP..."
cd package
zip -r9 ../function.zip .
cd ..

# Mover a directorio de deploy
mv function.zip ../deploy/

# Limpiar
rm -rf package

echo "✅ Lambda empaquetada en: ../deploy/function.zip"
ls -lh ../deploy/function.zip