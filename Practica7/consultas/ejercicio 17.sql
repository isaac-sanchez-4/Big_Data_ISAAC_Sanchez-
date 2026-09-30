select dispositivo,
		count(*) as reproducciones,
		sum(segundos_escuchados) as segundos,
		CAST(SUM(segundos_escuchados) / 60.0 AS decimal(10,1)) AS minutos
FROM dbo.reproducciones
GROUP BY dispositivo
ORDER BY reproducciones DESC;