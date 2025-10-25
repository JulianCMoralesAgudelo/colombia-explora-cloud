#!/bin/bash

echo "🏔️ Colombia Explora - Health Check"
echo "==================================="

# Configuración
STACK_NAME="colombia-explora-prod"
AWS_REGION="us-east-1"

# Obtener outputs del stack
echo "📡 Obteniendo información del stack..."
API_URL=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`ApiGatewayURL`].OutputValue' --output text 2>/dev/null || echo "NOT_FOUND")
S3_BUCKET=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' --output text 2>/dev/null || echo "NOT_FOUND")

echo "🌐 API Gateway: $API_URL"
echo "📁 S3 Bucket: $S3_BUCKET"

# Verificar Lambda
echo ""
echo "🔍 Verificando Lambda..."
LAMBDA_NAME="colombia-explora-backend-prod"
LAMBDA_STATUS=$(aws lambda get-function --function-name $LAMBDA_NAME --query 'Configuration.LastUpdateStatus' --output text 2>/dev/null || echo "NOT_FOUND")

if [ "$LAMBDA_STATUS" == "Successful" ]; then
    echo "✅ Lambda: HEALTHY ($LAMBDA_STATUS)"
else
    echo "❌ Lambda: UNHEALTHY ($LAMBDA_STATUS)"
fi

# Test de conectividad API
echo ""
echo "🔍 Testeando API..."
if [ "$API_URL" != "NOT_FOUND" ]; then
    API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health 2>/dev/null || echo "000")
    
    if [ "$API_RESPONSE" == "200" ]; then
        echo "✅ API: HEALTHY (HTTP $API_RESPONSE)"
    else
        echo "❌ API: UNHEALTHY (HTTP $API_RESPONSE)"
    fi
else
    echo "❌ API: NOT DEPLOYED"
fi

echo ""
echo "==================================="
echo "🏔️ Health Check completado!"