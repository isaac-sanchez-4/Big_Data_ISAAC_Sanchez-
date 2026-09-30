SELECT COUNT(*) AS total_filas,
       COUNT(cancion_id) AS con_cancion,
       COUNT(DISTINCT cancion_id) AS canciones_distintas,
       COUNT(DISTINCT usuario_id) AS usuarios_distintos
FROM dbo.reproducciones;