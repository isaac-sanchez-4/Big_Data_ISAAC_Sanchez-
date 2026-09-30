SELECT nombre_usuario,
		fecha_alta,
		DATEDIFF(day ,fecha_alta,'2026-09-24') AS dias_antiguedad
from dbo.usuarios
	
Order by dias_antiguedad desc;