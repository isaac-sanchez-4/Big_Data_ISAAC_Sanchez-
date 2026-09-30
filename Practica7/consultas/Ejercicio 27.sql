SELECT 
    g.nombre AS genero, 
    COUNT(r.reproduccion_id) AS reproducciones_validas, 
    CAST(SUM(r.segundos_escuchados) / 60.0 AS DECIMAL(10,1)) AS minutos 
FROM dbo.generos g 
JOIN dbo.canciones c ON g.genero_id = c.genero_id 
JOIN dbo.reproducciones r ON c.cancion_id = r.cancion_id 
GROUP BY g.nombre 
HAVING COUNT(r.reproduccion_id) > 3 
ORDER BY reproducciones_validas DESC;
