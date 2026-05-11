-- Script SQL para creación de base de datos (PostgreSQL/SQLite compatible)
-- Nota: SQLAlchemy crea esto automáticamente al iniciar la app.

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL, -- 'viajero', 'guia', 'admin'
    telefono VARCHAR(20),
    ciudad VARCHAR(100),
    estado BOOLEAN DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Usuario Administrador Inicial
-- La contraseña 'Admin123!' hasheada con bcrypt sería diferente cada vez, 
-- pero el código de app.py se encarga de crearla correctamente.
