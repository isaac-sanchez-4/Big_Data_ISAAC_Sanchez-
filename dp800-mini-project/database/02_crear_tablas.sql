-- Script 02: Creaci�n de Tablas 

USE DP800_TutorRAG;
GO

-- 1. M�dulos o �reas del Temario DP-800
CREATE TABLE Departamentos (
    DepartamentoID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL UNIQUE
);
GO

-- 2. Usuarios del sistema 
CREATE TABLE Usuarios (
    UsuarioID INT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(150) NOT NULL UNIQUE,
    HashedPassword NVARCHAR(255) NOT NULL,
    Rol NVARCHAR(50) DEFAULT 'Estudiante',
    DepartamentoID INT FOREIGN KEY REFERENCES Departamentos(DepartamentoID)
);
GO

-- 3. Documentos PDF cargados 
CREATE TABLE Documentos (
    DocumentoID INT IDENTITY(1,1) PRIMARY KEY,
    NombreArchivo NVARCHAR(255) NOT NULL,
    DepartamentoID INT FOREIGN KEY REFERENCES Departamentos(DepartamentoID),
    FechaSubida DATETIME DEFAULT GETDATE()
);
GO

-- 4. Fragmentos de texto (Chunks) con soporte VECTOR nativo de SQL Server 2025
-- Dimensiones = 384 (nomic-embed-text)
CREATE TABLE Fragmentos (
    FragmentoID INT IDENTITY(1,1) PRIMARY KEY,
    DocumentoID INT FOREIGN KEY REFERENCES Documentos(DocumentoID) ON DELETE CASCADE,
    TextoChunk NVARCHAR(MAX) NOT NULL,
    NumeroPagina INT,
    Embedding VECTOR(768) NOT NULL
);
GO

-- 5. Historial de preguntas y respuestas del tutor inteligente
CREATE TABLE Historial_Consultas (
    ConsultaID INT IDENTITY(1,1) PRIMARY KEY,
    UsuarioID INT FOREIGN KEY REFERENCES Usuarios(UsuarioID),
    Pregunta NVARCHAR(MAX) NOT NULL,
    RespuestaGenerada NVARCHAR(MAX) NOT NULL,
    FechaConsulta DATETIME DEFAULT GETDATE()
);
GO

PRINT 'Estructura de 5 tablas creada con �xito (incluyendo soporte VECTOR).';
GO