select us.nombre_usuario, us.plan_suscripcion, us.fecha_alta
from dbo.usuarios us 
LEFT JOIN dbo.reproducciones re on us.usuario_id = re.usuario_id
where re.reproduccion_id is null;