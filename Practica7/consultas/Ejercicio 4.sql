SELECT nombre_usuario, plan_suscripcion, fecha_alta
FROM dbo.usuarios
WHERE pais = 'ES'
ORDER BY fecha_alta ASC;