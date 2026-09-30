SELECT CASE 
           WHEN duracion_seg < 180 THEN 'Corta'
           WHEN duracion_seg BETWEEN 180 AND 240 THEN 'Media'
           ELSE 'Larga' 
       END AS categoria,
       COUNT(*) AS num_canciones,
       AVG(duracion_seg) AS duracion_media
FROM dbo.canciones
GROUP BY CASE 
             WHEN duracion_seg < 180 THEN 'Corta'
             WHEN duracion_seg BETWEEN 180 AND 240 THEN 'Media'
             ELSE 'Larga' 
         END
ORDER BY num_canciones DESC, categoria ASC;