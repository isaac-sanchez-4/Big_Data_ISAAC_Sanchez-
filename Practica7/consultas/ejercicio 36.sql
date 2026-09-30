SELECT p.playlist_id, 
       u.nombre_usuario, 
       p.nombre, 
       p.es_publica,
       COUNT(pc.cancion_id) AS num_canciones
FROM dbo.playlists p
JOIN dbo.usuarios u ON p.usuario_id = u.usuario_id
LEFT JOIN dbo.playlist_canciones pc ON p.playlist_id = pc.playlist_id
GROUP BY p.playlist_id, u.nombre_usuario, p.nombre, p.es_publica
ORDER BY p.playlist_id ASC;