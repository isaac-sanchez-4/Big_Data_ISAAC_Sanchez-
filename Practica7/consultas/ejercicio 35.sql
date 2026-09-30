UPDATE dbo.playlists
SET descripcion = N'Guitarras para la oficina'
WHERE playlist_id = 2;

UPDATE p
SET p.es_publica = 1
FROM dbo.playlists p
JOIN dbo.usuarios u ON p.usuario_id = u.usuario_id
WHERE u.plan_suscripcion = N'Premium';