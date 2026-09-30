CREATE TABLE dbo.playlists (
    playlist_id    int IDENTITY(1,1) NOT NULL,
    usuario_id     int               NOT NULL,
    nombre         nvarchar(100)     NOT NULL,
    es_publica     bit               NOT NULL CONSTRAINT DF_playlists_publica DEFAULT 0,
    fecha_creacion datetime2(0)      NOT NULL CONSTRAINT DF_playlists_fecha DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT PK_playlists PRIMARY KEY (playlist_id),
    CONSTRAINT FK_playlists_usuarios FOREIGN KEY (usuario_id) REFERENCES dbo.usuarios (usuario_id),
    CONSTRAINT UQ_playlists_usuario_nombre UNIQUE (usuario_id, nombre)
);