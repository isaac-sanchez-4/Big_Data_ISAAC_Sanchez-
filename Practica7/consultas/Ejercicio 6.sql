SELECT nombre_usuario 
FROM dbo.usuarios
where nombre_usuario LIKE '%[_]%'
ORDER BY nombre_usuario ASC;