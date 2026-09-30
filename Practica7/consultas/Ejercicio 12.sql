-- Versión 1
SELECT nombre,
       CONCAT(nombre, ' (', pais, ')') AS etiqueta,
       LEN(nombre) AS longitud
FROM dbo.artistas
ORDER BY nombre ASC;

-- Versión 2
SELECT nombre,
       nombre || ' (' || pais || ')' AS etiqueta,
       LEN(nombre) AS longitud
FROM dbo.artistas
ORDER BY nombre ASC;