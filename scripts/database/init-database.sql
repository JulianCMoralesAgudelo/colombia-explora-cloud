-- ==================== COLOMBIA EXPLORA - ESQUEMA DE BASE DE DATOS ====================
-- Ejecutar después del despliegue en RDS PostgreSQL

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de destinos turísticos
CREATE TABLE IF NOT EXISTS destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    region VARCHAR(255),
    price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    destination_id INTEGER REFERENCES destinations(id) ON DELETE CASCADE,
    people INTEGER NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuario administrador por defecto
-- Contraseña: admin123 (debes generar el hash bcrypt real)
INSERT INTO users (username, email, hashed_password, role) 
VALUES (
    'admin', 
    'admin@colombiaexplora.com', 
    '$2b$12$LQv3c1yqBWVHx5GyaRqXFOg5sCgRgRZRZRZRZRZRZRZRZRZRZRZRZ', 
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- Datos de ejemplo para destinos
INSERT INTO destinations (name, description, region, price) VALUES
('Valle del Cocora', 'Hermoso valle con palmas de cera gigantes', 'Quindío', 120000.00),
('Termales de Santa Rosa', 'Aguas termales relajantes', 'Risaralda', 80000.00),
('Parque del Café', 'Parque temático sobre la cultura cafetera', 'Quindío', 95000.00),
('Salento', 'Pueblo colorido con arquitectura tradicional', 'Quindío', 70000.00)
ON CONFLICT (name) DO NOTHING;

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_reservations_user_id ON reservations(user_id);
CREATE INDEX IF NOT EXISTS idx_reservations_destination_id ON reservations(destination_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);