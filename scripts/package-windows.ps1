Write-Host "📦 Empaquetando Lambda para Windows..." -ForegroundColor Green

# Configuración
$BackendPath = "backend"
$DeployPath = "deploy"
$ZipFile = "function.zip"

# Limpiar
Remove-Item "$DeployPath\$ZipFile" -ErrorAction SilentlyContinue

# Verificar que backend existe
if (-not (Test-Path $BackendPath)) {
    Write-Host "❌ Directorio backend no encontrado" -ForegroundColor Red
    exit 1
}

# Crear directorio deploy si no existe
New-Item -ItemType Directory -Force -Path $DeployPath

# Crear ZIP directamente
Write-Host "Creando $ZipFile..." -ForegroundColor Yellow
Compress-Archive -Path "$BackendPath\*" -DestinationPath "$DeployPath\$ZipFile" -Force

# Verificar
if (Test-Path "$DeployPath\$ZipFile") {
    $size = (Get-Item "$DeployPath\$ZipFile").Length / 1MB
    Write-Host "✅ ZIP creado: $DeployPath\$ZipFile ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "❌ Error creando ZIP" -ForegroundColor Red
}