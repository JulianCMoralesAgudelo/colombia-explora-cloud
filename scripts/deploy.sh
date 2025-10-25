#!/bin/bash

set -e

echo "🚀 Deploying Colombia Explora to AWS..."

# Configuración
PROJECT_NAME="colombia-explora"
ENVIRONMENT="prod"
AWS_REGION="us-east-1"
STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Función para imprimir con color
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar prerequisitos
check_prerequisites() {
    echo "🔍 Checking prerequisites..."
    
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI not found. Please install it first."
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        print_error "jq not found. Please install it first."
        exit 1
    fi
    
    # Verificar que estamos autenticados en AWS
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS not authenticated. Please run 'aws configure' first."
        exit 1
    fi
    
    print_status "Prerequisites satisfied"
}

# Empaquetar Lambda function
package_lambda() {
    echo "📦 Packaging Lambda function..."
    
    cd backend
    
    # Crear directorio para package
    mkdir -p package
    
    # Instalar dependencias
    pip install -r requirements.txt -t package/
    
    # Copiar código
    cp *.py package/
    cp -r auth/ package/
    cp -r api/ package/
    
    # Crear ZIP
    cd package
    zip -r ../function.zip .
    cd ..
    
    # Mover ZIP a directorio de deploy
    mkdir -p ../deploy
    mv function.zip ../deploy/
    
    cd ..
    
    print_status "Lambda packaged successfully"
}

# Desplegar CloudFormation
deploy_infrastructure() {
    echo "🏗️ Deploying CloudFormation stack..."
    
    # Parámetros para CloudFormation
    PARAMETERS="ParameterKey=ProjectName,ParameterValue=${PROJECT_NAME} \
                ParameterKey=Environment,ParameterValue=${ENVIRONMENT} \
                ParameterKey=DBUsername,ParameterValue=explora_user \
                ParameterKey=DBPassword,ParameterValue=ExploraPass123! \
                ParameterKey=JWTSecret,ParameterValue=MySuperSecretJWTKeyForColombiaExplora2024"
    
    # Crear o actualizar stack
    if aws cloudformation describe-stacks --stack-name $STACK_NAME &> /dev/null; then
        print_warning "Stack exists, updating..."
        aws cloudformation update-stack \
            --stack-name $STACK_NAME \
            --template-body file://cloudformation/colombia-explora-cloud.yaml \
            --parameters $PARAMETERS \
            --capabilities CAPABILITY_IAM
    else
        print_status "Creating new stack..."
        aws cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://cloudformation/colombia-explora-cloud.yaml \
            --parameters $PARAMETERS \
            --capabilities CAPABILITY_IAM
    fi
    
    # Esperar a que el stack se complete
    echo "⏳ Waiting for stack to complete..."
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
    
    print_status "CloudFormation stack deployed successfully"
}

# Obtener outputs del stack
get_stack_outputs() {
    echo "📡 Getting stack outputs..."
    
    OUTPUTS=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs')
    
    API_GATEWAY_URL=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="ApiGatewayURL") | .OutputValue' | cut -d'/' -f3)
    S3_BUCKET=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="S3BucketName") | .OutputValue')
    
    export API_GATEWAY_URL
    export S3_BUCKET
    
    print_status "Stack outputs retrieved"
}

# Actualizar Lambda function
update_lambda() {
    echo "🔁 Updating Lambda function..."
    
    aws lambda update-function-code \
        --function-name "${PROJECT_NAME}-backend-${ENVIRONMENT}" \
        --zip-file fileb://deploy/function.zip
    
    print_status "Lambda function updated"
}

# Desplegar frontend a S3
deploy_frontend() {
    echo "🎨 Deploying frontend to S3..."
    
    # Build del frontend con las URLs correctas
    cd frontend
    API_GATEWAY_URL=$API_GATEWAY_URL AWS_REGION=$AWS_REGION npm run build:aws
    cd ..
    
    # Sincronizar con S3
    aws s3 sync frontend/dist/browser/ s3://$S3_BUCKET --delete
    
    # Invalidar cache de CloudFront
    DISTRIBUTION_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?Origins.Items[0].DomainName=='$S3_BUCKET.s3.$AWS_REGION.amazonaws.com'].Id" --output text)
    
    if [ ! -z "$DISTRIBUTION_ID" ]; then
        aws cloudfront create-invalidation \
            --distribution-id $DISTRIBUTION_ID \
            --paths "/*"
    fi
    
    print_status "Frontend deployed to S3"
}

# Ejecutar despliegue completo
main() {
    echo "🏔️ Starting Colombia Explora Deployment"
    echo "========================================="
    
    check_prerequisites
    package_lambda
    deploy_infrastructure
    get_stack_outputs
    update_lambda
    deploy_frontend
    
    # Mostrar URLs finales
    echo ""
    echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
    echo "========================================="
    echo "🌐 Frontend URL: https://$(aws cloudfront list-distributions --query "DistributionList.Items[?Origins.Items[0].DomainName=='$S3_BUCKET.s3.$AWS_REGION.amazonaws.com'].DomainName" --output text)"
    echo "🔗 API Gateway: https://$API_GATEWAY_URL"
    echo "📊 CloudWatch: https://$AWS_REGION.console.aws.amazon.com/cloudwatch/home"
    echo ""
}

# Ejecutar despliegue
main "$@"