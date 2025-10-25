🏔️ Colombia Explora - Arquitectura Serverless en AWS
Migración completa de la aplicación Colombia Explora a una arquitectura serverless en AWS usando CloudFormation.

🎯 Arquitectura
text
Usuario → CloudFront → S3 (Frontend Angular) → API Gateway → Lambda (Python) → RDS (Postgres)
                                                                             ↓ 
                                                                     CloudWatch / SNS
📋 Características
✅ Frontend Angular hospedado en S3 + CloudFront

✅ Backend Python como funciones Lambda

✅ Base de datos PostgreSQL en RDS

✅ Infraestructura como código con CloudFormation

✅ Monitoreo y alertas con CloudWatch + SNS

✅ Despliegue automatizado con scripts bash

✅ Escalabilidad automática con Lambda y RDS

✅ Alta disponibilidad en múltiples AZs

🚀 Despliegue Rápido
Prerrequisitos
bash
# AWS CLI configurado
aws configure

# Dependencias del sistema
sudo apt-get install jq zip  # Linux
brew install jq              # macOS
Despliegue Completo
bash
# 1. Clonar repositorio
git clone <repository-url>
cd colombia-explora-cloud

# 2. Dar permisos de ejecución
chmod +x scripts/*.sh

# 3. Desplegar todo
./scripts/deploy.sh
📁 Estructura del Proyecto
text
colombia-explora-cloud/
├── backend/           # Código Lambda (Python)
├── frontend/          # Angular app
├── cloudformation/    # Template IaC
├── scripts/           # Automatización
└── deploy/           # Archivos temporales
🔧 Configuración Manual
1. Variables de Entorno para Desarrollo
typescript
// En frontend/src/environments/environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000',
  authUrl: 'http://localhost:8001'
};
2. Parámetros CloudFormation
Editar scripts/deploy.sh:

bash
PROJECT_NAME="colombia-explora"
ENVIRONMENT="prod"
AWS_REGION="us-east-1"
DB_PASSWORD="TuPasswordSeguro123!"
JWT_SECRET="TuJWTSecretSuperSeguro"
🌐 URLs después del Despliegue
Frontend: https://[cloudfront-domain].cloudfront.net

API: https://[api-gateway].execute-api.[region].amazonaws.com/prod

Base de datos: [rds-endpoint]:5432

📊 Monitoreo
CloudWatch Dashboards
Lambda Metrics: Invocations, Errors, Duration

RDS Metrics: CPU, Connections, Storage

API Gateway: Latency, 4XX/5XX errors

Alertas SNS
Lambda errors > 0

RDS CPU > 80%

API Gateway 5XX errors

RDS almacenamiento < 15% libre

🔒 Seguridad
JWT Tokens para autenticación

IAM Roles para permisos mínimos

Security Groups para RDS

CloudFront con HTTPS

Secrets en Parameter Store para credenciales

🗃️ Base de Datos
Esquema Inicial
sql
-- Ejecutar después del despliegue en RDS
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    region VARCHAR(255),
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    destination_id INTEGER REFERENCES destinations(id),
    people INTEGER NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
🛠️ Desarrollo
Backend Local
bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Frontend Local
bash
cd frontend
npm install
npm start
📈 Escalabilidad
Lambda: Escala automáticamente hasta 1000 ejecuciones concurrentes

RDS: Puede escalar a instancias más grandes

CloudFront: Distribución global

S3: Almacenamiento ilimitado

💰 Costos Estimados
Servicio	Costo Mensual (USD)
Lambda	~$5-20
RDS (t3.micro)	~$15
S3	~$1-5
CloudFront	~$5-15
Total	~$26-55
🐛 Troubleshooting
Error: Lambda no puede conectar a RDS
bash
# Verificar Security Groups
aws ec2 describe-security-groups --group-ids [sg-id]
Frontend no carga desde S3
bash
# Verificar política del bucket
aws s3api get-bucket-policy --bucket [bucket-name]
🔄 Comandos Útiles
bash
# Ver estado del stack
aws cloudformation describe-stacks --stack-name colombia-explora-prod

# Actualizar solo backend
./scripts/deploy-backend.sh

# Health check
./scripts/health-check.sh
📞 Soporte
CloudWatch Logs: Buscar /aws/lambda/colombia-explora-backend-prod

Issues: [GitHub Issues]

Documentación: Esta documentación

Desarrollado con ❤️ para el Eje Cafetero Colombiano 🇨🇴🏔️

🔍 Mejoras realizadas:
✅ Formato corregido - Los code blocks ahora se muestran correctamente

✅ Contenido faltante agregado - Base de datos, desarrollo, troubleshooting

✅ Estructura mejorada - Secciones más organizadas

✅ Información práctica - Comandos útiles y costos

✅ Arquitectura visual - Diagrama formateado correctamente