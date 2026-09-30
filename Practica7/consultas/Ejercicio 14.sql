SELECT reproduccion_id,
		CAST( fecha_hora as date ) as fecha,
		CAST (fecha_hora as time(0)) as hora,
		segundos_escuchados

FROM dbo.reproducciones

where usuario_id = 3

order by fecha ASC,hora ASC;