DELETE FROM dbo.playlist_canciones
WHERE playlist_id = 2 AND cancion_id = 110;

DELETE FROM dbo.playlist_canciones WHERE playlist_id = 3;
DELETE FROM dbo.playlists WHERE playlist_id = 3;