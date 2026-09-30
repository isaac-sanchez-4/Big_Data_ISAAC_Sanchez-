SELECT R.fecha_hora,
		U.nombre_usuario,
		COALESCE(C.titulo, N'(Anuncio)') AS titulo,
		COALESCE(A.nombre, '-') AS artista
FROM dbo.reproducciones R
JOIN dbo.usuarios U ON R.usuario_id = U.usuario_id
LEFT JOIN dbo.canciones C ON R.cancion_id = C.cancion_id
LEFT JOIN dbo.artistas A ON C.artista_id = A.artista_id
WHERE r.fecha_hora >= '2026-09-16' AND r.fecha_hora < '2026-09-17'
ORDER BY r.fecha_hora ASC;