DROP TABLE IF EXISTS dbo.playlist_canciones;
DROP TABLE IF EXISTS dbo.playlists;
DROP TABLE IF EXISTS dbo.sysdiagrams;


SELECT name 
FROM sys.tables
ORDER BY name ASC;