# Configuración Actual - Colombia Explora Cloud

## 🌐 URLs de Acceso
- **Frontend**: https://dnnn5lek64q8u.cloudfront.net
- **API Backend**: https://oxj71v1u44.execute-api.us-east-1.amazonaws.com/prod
- **S3 Website**: http://colombia-explora-frontend-prod.s3-website-us-east-1.amazonaws.com

## 🗄️ Base de Datos RDS
- **Endpoint**: colombia-explora-db-prod.cq9w2yq26aau.us-east-1.rds.amazonaws.com
- **Puerto**: 5432
- **Base de datos**: colombiaexploraprod
- **Usuario**: explora_user
- **Contraseña**: ExploraPass123!

## 🔧 Recursos Principales
- **CloudFormation Stack**: colombia-explora-prod
- **S3 Bucket**: colombia-explora-frontend-prod
- **Lambda Function**: colombia-explora-backend-prod
- **API Gateway**: colombia-explora-api-prod (oxj71v1u44)
- **CloudFront**: dnnn5lek64q8u.cloudfront.net

## 📊 Estado Actual
- **Stack Status**: CREATE_COMPLETE
- **RDS Status**: available
- **Lambda Status**: Active
- **Frontend**: Desplegado y accesible

# Ver estado del stack
aws cloudformation describe-stacks --stack-name colombia-explora-prod

# Probar API
curl https://oxj71v1u44.execute-api.us-east-1.amazonaws.com/prod/destinations

# Ver logs de Lambda
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/colombia-explora


# Comandos que NO tienen problemas de rutas
echo "=== 🔍 VERIFICACIÓN ALTERNATIVA ==="

# 1. Verificar Lambda directamente
echo "1. Estado de Lambda:"
aws lambda get-function --function-name colombia-explora-backend-prod --query 'Configuration.LastUpdateStatus' --output text

# 2. Ver CloudWatch alarms (no tiene problemas de ruta)
echo ""
echo "2. Alarmas CloudWatch:"
aws cloudwatch describe-alarms --alarm-name-prefix colombia-explora --query 'MetricAlarms[].{Alarm:AlarmName, State:StateValue}' --output table

# 3. Ver métricas recientes de Lambda
echo ""
echo "3. Métricas de Lambda:"
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=colombia-explora-backend-prod \
    --start-time $(date -u -d "1 hour ago" +%Y-%m-%dT%H:%M:%SZ) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
    --period 3600 \
    --statistics Sum \
    --query 'Datapoints[].{Timestamp:Timestamp, Invocations:Sum}' \
    --output table 2>/dev/null || echo "No hay métricas recientes"