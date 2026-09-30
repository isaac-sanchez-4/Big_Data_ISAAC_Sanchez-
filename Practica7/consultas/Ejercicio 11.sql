select	titulo,
		duracion_seg,
		CASE 
			WHEN duracion_seg < 180 THEN 'Corta'
			when duracion_seg BETWEEN 180 AND 240 THEN 'Media'
			ELSE 'Larga'
	END AS categoria 
FROM dbo.canciones 
WHERE artista_id = 5 
ORDER BY titulo ASC;