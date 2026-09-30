SELECT us.nombre_usuario, 
       COUNT(*) AS reproducciones, 
       SUM(r.segundos_escuchados) AS segundos
FROM dbo.reproducciones r
JOIN dbo.usuarios us ON r.usuario_id = us.usuario_id
WHERE r.tipo_contenido = N'Canción'
GROUP BY us.nombre_usuario
HAVING COUNT(*) > 3 AND SUM(r.segundos_escuchados) > 800
ORDER BY segundos DESC;