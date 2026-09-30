SELECT a.nombre AS artista, 
       COUNT(r.reproduccion_id) AS reproducciones
FROM dbo.artistas a
LEFT JOIN dbo.canciones c ON a.artista_id = c.artista_id
LEFT JOIN dbo.reproducciones r ON c.cancion_id = r.cancion_id
GROUP BY a.nombre
ORDER BY reproducciones DESC, a.nombre ASC;