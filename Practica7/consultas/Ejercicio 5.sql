SELECT titulo, duracion_seg, fecha_lanzamiento
FROM dbo.canciones
WHERE fecha_lanzamiento >= '2026-01-01' AND fecha_lanzamiento < '2027-01-01'
  AND duracion_seg BETWEEN 170 AND 200
ORDER BY fecha_lanzamiento ASC;