SELECT E1.nombre as empleado, E1.puesto,
COALESCE(E2.nombre,'(sin jefe)') AS jefe
from dbo.empleados E1
LEFT JOIN dbo.empleados E2 ON E1.jefe_id= E2.empleado_id
ORDER BY E1.empleado_id	ASC;