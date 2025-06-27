-- Cognitive Memory System - Database Setup

-- Extensión requerida para vectores
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla principal de unidades de memoria
CREATE TABLE IF NOT EXISTS memory_units (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    cognitive_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tokens INTEGER,
    
    -- Índices para performance
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at DESC),
    INDEX idx_cognitive_score (cognitive_score DESC)
);

-- Índice para búsqueda vectorial optimizada
CREATE INDEX idx_embedding ON memory_units 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Tabla de sesiones (opcional para analytics)
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    total_interactions INTEGER DEFAULT 0,
    avg_cognitive_score FLOAT
);

-- Tabla de patrones detectados por MAHOUT
CREATE TABLE IF NOT EXISTS cognitive_patterns (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    pattern_type VARCHAR(100),
    pattern_data JSONB,
    strength FLOAT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at
CREATE TRIGGER update_sessions_updated_at 
    BEFORE UPDATE ON sessions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Vista para analytics
CREATE OR REPLACE VIEW session_analytics AS
SELECT 
    s.id as session_id,
    s.created_at,
    s.total_interactions,
    s.avg_cognitive_score,
    COUNT(DISTINCT p.pattern_type) as unique_patterns,
    AVG(p.strength) as avg_pattern_strength
FROM sessions s
LEFT JOIN cognitive_patterns p ON s.id = p.session_id
GROUP BY s.id, s.created_at, s.total_interactions, s.avg_cognitive_score;

-- Permisos básicos
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cognitive_app;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cognitive_app;

-- Verificar instalación
SELECT version();
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
