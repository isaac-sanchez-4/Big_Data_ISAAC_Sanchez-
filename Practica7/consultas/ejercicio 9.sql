SELECT TOP (2) WITH TIES reproduccion_id, usuario_id, cancion_id, segundos_escuchados
FROM dbo.reproducciones
ORDER BY segundos_escuchados DESC;