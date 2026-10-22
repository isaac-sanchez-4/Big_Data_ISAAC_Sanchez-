-- Script 03: Procedimientos Almacenados para B�squeda Sem�ntica

USE DP800_TutorRAG;
GO

CREATE OR ALTER PROCEDURE sp_BuscarFragmentosSimilares
    @QueryVector NVARCHAR(MAX),  
    @TopK INT = 4               
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP (@TopK)
        f.FragmentoID,
        f.DocumentoID,
        d.NombreArchivo,
        f.TextoChunk,
        f.NumeroPagina,
        VECTOR_DISTANCE('cosine', f.Embedding, CAST(@QueryVector AS VECTOR(768))) AS DistanciaCoseno
    FROM Fragmentos f
    INNER JOIN Documentos d ON f.DocumentoID = d.DocumentoID
    ORDER BY DistanciaCoseno ASC;
END;
GO

PRINT 'Procedimiento almacenado sp_BuscarFragmentosSimilares creado correctamente.';
GO