SELECT COUNT(*) AS num_canciones,
       MIN(duracion_seg) AS duracion_min,
       MAX(duracion_seg) AS duracion_max,
       AVG(duracion_seg) AS media_entera,
       AVG(CAST(duracion_seg AS decimal(10,5))) AS media_decimal
FROM dbo.canciones;