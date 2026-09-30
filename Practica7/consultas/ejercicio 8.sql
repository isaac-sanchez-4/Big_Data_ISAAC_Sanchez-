SELECT reproduccion_id, usuario_id, fecha_hora
FROM dbo.reproducciones
WHERE cancion_id IS NULL;