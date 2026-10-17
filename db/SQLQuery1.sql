-- =============================================================================
-- BASE DE DATOS: PasteleriaUSPG
-- Sistema Experto de Recomendación y Personalización de Pasteles
-- =============================================================================

-- 1. Crear Base de Datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'PasteleriaUSPG')
BEGIN
    CREATE DATABASE PasteleriaUSPG;
END
GO

USE PasteleriaUSPG;
GO

-- 2. Eliminar tablas previas si existen (para poder re-ejecutar sin errores)
IF OBJECT_ID('HistorialRecomendaciones', 'U') IS NOT NULL DROP TABLE HistorialRecomendaciones;
IF OBJECT_ID('CatalogoIngredientes', 'U') IS NOT NULL DROP TABLE CatalogoIngredientes;
IF OBJECT_ID('Usuarios', 'U') IS NOT NULL DROP TABLE Usuarios;
GO

-- -----------------------------------------------------------------------------
-- TABLA 1: Usuarios (Nuevos, recurrentes y sus preferencias fijas)
-- -----------------------------------------------------------------------------
CREATE TABLE Usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    correo NVARCHAR(150) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    restriccion_predeterminada NVARCHAR(50) NOT NULL DEFAULT 'ninguna', -- 'ninguna', 'sin-lactosa'
    perfil_favorito NVARCHAR(50) NULL,                                 -- 'citrico-ligero', 'chocolatoso-denso', etc.
    fecha_registro DATETIME DEFAULT GETDATE(),
    activo BIT DEFAULT 1
);
GO

-- -----------------------------------------------------------------------------
-- TABLA 2: CatalogoIngredientes (Base ontológica administrable)
-- -----------------------------------------------------------------------------
CREATE TABLE CatalogoIngredientes (
    id_ingrediente INT IDENTITY(1,1) PRIMARY KEY,
    tipo NVARCHAR(30) NOT NULL,        -- 'bizcocho', 'relleno', 'cobertura'
    nombre NVARCHAR(50) NOT NULL UNIQUE,
    categoria NVARCHAR(50) NOT NULL,   -- 'citrico', 'amargo', 'dulce', 'frutal', 'cremoso', 'ligera', 'densa', 'vegetal'
    densidad NVARCHAR(20) NOT NULL DEFAULT 'ligera', -- 'ligera', 'densa'
    contiene_lactosa CHAR(2) NOT NULL DEFAULT 'no',  -- 'si', 'no'
    disponible BIT DEFAULT 1
);
GO

-- -----------------------------------------------------------------------------
-- TABLA 3: HistorialRecomendaciones (Trazabilidad y memoria de inferencia)
-- -----------------------------------------------------------------------------
CREATE TABLE HistorialRecomendaciones (
    id_recomendacion INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NULL FOREIGN KEY REFERENCES Usuarios(id_usuario) ON DELETE SET NULL,
    modo NVARCHAR(30) NOT NULL,                -- 'filtro-general', 'individual'
    restriccion NVARCHAR(30) NOT NULL,         -- 'ninguna', 'sin-lactosa'
    perfil_solicitado NVARCHAR(50) NULL,
    bizcocho_final NVARCHAR(50) NULL,
    relleno_final NVARCHAR(50) NULL,
    cobertura_final NVARCHAR(50) NULL,
    estado NVARCHAR(30) NOT NULL,              -- 'viable', 'incompatible', 'incompleto'
    tipo_receta NVARCHAR(30) NOT NULL,         -- 'exacta', 'ajustada', 'error'
    mensaje NVARCHAR(500) NOT NULL,
    justificacion NVARCHAR(MAX) NOT NULL,
    regla_activada NVARCHAR(100) NOT NULL,     -- Regla CLIPS disparada
    fecha_consulta DATETIME DEFAULT GETDATE()
);
GO

-- -----------------------------------------------------------------------------
-- CARGA INICIAL DE DATOS (SEEDING): Catálogo Oficial de PasteleríaUSPG
-- -----------------------------------------------------------------------------

-- Bizcochos
INSERT INTO CatalogoIngredientes (tipo, nombre, categoria, densidad, contiene_lactosa) VALUES
('bizcocho', 'limon', 'citrico', 'ligera', 'no'),
('bizcocho', 'chocolate-humedo', 'amargo', 'densa', 'no'),
('bizcocho', 'vainilla', 'dulce', 'ligera', 'no'),
('bizcocho', 'zanahoria', 'dulce', 'densa', 'no'),
('bizcocho', 'vainilla-vegetal', 'dulce', 'ligera', 'no');

-- Rellenos
INSERT INTO CatalogoIngredientes (tipo, nombre, categoria, densidad, contiene_lactosa) VALUES
('relleno', 'maracuya', 'frutal', 'ligera', 'no'),
('relleno', 'frutos-rojos', 'frutal', 'ligera', 'no'),
('relleno', 'tres-leches', 'cremoso', 'ligera', 'si'),
('relleno', 'dulce-de-leche', 'cremoso', 'ligera', 'si'),
('relleno', 'mermelada-cereza', 'frutal', 'ligera', 'no');

-- Coberturas
INSERT INTO CatalogoIngredientes (tipo, nombre, categoria, densidad, contiene_lactosa) VALUES
('cobertura', 'merengue-italiano', 'ligera', 'ligera', 'no'),
('cobertura', 'chantilly', 'ligera', 'ligera', 'si'),
('cobertura', 'ganache', 'densa', 'densa', 'no'),
('cobertura', 'crema-vegetal', 'vegetal', 'ligera', 'no');

-- Usuarios iniciales de prueba
INSERT INTO Usuarios (nombre, correo, password_hash, restriccion_predeterminada, perfil_favorito) VALUES
('Luis Avila', 'leavilab@alumno.uspg.edu.gt', 'hash_pass_123', 'sin-lactosa', 'frutal-saludable'),
('Dylan Telon', 'datelonz@alumno.uspg.edu.gt', 'hash_pass_456', 'ninguna', 'chocolatoso-denso'),
('Maria Pacheco', 'mdpachecol@alumno.uspg.edu.gt', 'hash_pass_789', 'ninguna', 'citrico-ligero');
GO

-- -----------------------------------------------------------------------------
-- CONSULTA DE VERIFICACIÓN
-- -----------------------------------------------------------------------------
SELECT 'Catalogo cargado con exito:' AS Estado, COUNT(*) AS TotalIngredientes FROM CatalogoIngredientes;
SELECT * FROM CatalogoIngredientes;
SELECT * FROM Usuarios;
SELECT * FROM dbo.HistorialRecomendaciones;
GO