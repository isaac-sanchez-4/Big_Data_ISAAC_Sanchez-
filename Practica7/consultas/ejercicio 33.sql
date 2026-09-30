INSERT INTO dbo.playlist_canciones (playlist_id, cancion_id)
VALUES (1, 103), (1, 104), (1, 113);

INSERT INTO dbo.playlist_canciones (playlist_id, cancion_id)
VALUES (2, 106), (2, 107), (2, 110);

INSERT INTO dbo.playlist_canciones (playlist_id, cancion_id)
SELECT 3, c.cancion_id
FROM dbo.canciones c
JOIN dbo.generos g ON c.genero_id = g.genero_id
WHERE g.nombre IN (N'House', N'Techno');