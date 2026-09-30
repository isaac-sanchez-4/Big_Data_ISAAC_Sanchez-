SELECT u.plan_suscripcion, 
       r.tipo_contenido, 
       COUNT(*) AS reproducciones
FROM reproducciones r 
join dbo.usuarios u on r.usuario_id = u.usuario_id
group by u.plan_suscripcion , r.tipo_contenido
order by u.plan_suscripcion ASC, r.tipo_contenido ASC;