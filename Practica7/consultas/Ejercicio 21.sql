SELECT a.nombre as artista,
c.titulo,
g.nombre as genero 

from dbo.canciones c 
join dbo.artistas a on c.artista_id = a.artista_id
join dbo.generos g on c.genero_id = g.genero_id
where a.pais ='ES'
ORDER BY a.nombre ASC, c.titulo ASC;