#!/bin/bash

echo "🏔️ Building Colombia Explora Frontend for AWS S3..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build for production
echo "🔨 Building Angular application..."
npm run build -- --configuration production

# Create S3 deployment package
echo "📁 Preparing S3 deployment..."
mkdir -p ../deploy/s3
cp -r dist/browser/* ../deploy/s3/

# Create config file for API Gateway URLs
cat > ../deploy/s3/assets/config.js << EOL
// Configuración dinámica para AWS
window.API_GATEWAY_URL = "${API_GATEWAY_URL}";
window.AWS_REGION = "${AWS_REGION}";
EOL

echo "✅ Frontend build completed!"
echo "📁 Files ready in: ../deploy/s3/"
echo "🌐 Upload to S3 with: aws s3 sync ../deploy/s3/ s3://your-bucket-name --delete"