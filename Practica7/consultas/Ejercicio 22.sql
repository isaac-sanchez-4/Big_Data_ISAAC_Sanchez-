SELECT r.fecha_hora, 
       u.nombre_usuario, 
       c.titulo, 
       a.nombre AS artista
FROM dbo.reproducciones r
JOIN dbo.usuarios u ON r.usuario_id = u.usuario_id
JOIN dbo.canciones c ON r.cancion_id = c.cancion_id
JOIN dbo.artistas a ON c.artista_id = a.artista_id
WHERE r.fecha_hora >= '2026-09-16' AND r.fecha_hora < '2026-09-17'
ORDER BY R.fecha_hora ASC;