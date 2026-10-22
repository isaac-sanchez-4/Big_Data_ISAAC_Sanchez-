-- Script 01: Creación de la Base de Datos

USE master;
GO

IF EXISTS (SELECT * FROM sys.databases WHERE name = N'DP800_TutorRAG')
BEGIN
    ALTER DATABASE DP800_TutorRAG SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DP800_TutorRAG;
END
GO

CREATE DATABASE DP800_TutorRAG;
GO

USE DP800_TutorRAG;
GO

PRINT 'Base de datos DP800_TutorRAG creada correctamente.';
GO