CREATE TABLE dbo.playlist_canciones (
    playlist_id    int          NOT NULL,
    cancion_id     int          NOT NULL,
    fecha_agregada datetime2(0) NOT NULL CONSTRAINT DF_plc_fecha_agregada DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_playlist_canciones PRIMARY KEY (playlist_id, cancion_id),
    CONSTRAINT FK_plc_playlists FOREIGN KEY (playlist_id) REFERENCES dbo.playlists (playlist_id),
    CONSTRAINT FK_plc_canciones FOREIGN KEY (cancion_id) REFERENCES dbo.canciones (cancion_id)
);