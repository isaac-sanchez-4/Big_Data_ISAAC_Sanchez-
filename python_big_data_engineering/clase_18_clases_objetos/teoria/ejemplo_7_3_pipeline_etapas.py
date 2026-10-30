"""
El equipo de datos ejecuta cada noche un *pipeline* que procesa las ventas de las tiendas. Un *pipeline* está formado por varias **etapas** que se ejecutan en orden. Modela este sistema mediante **composición**: un objeto `Pipeline` que contiene objetos `Etapa` como parte de sus atributos.

**Clase `Etapa`**

- Un constructor que reciba los parámetros obligatorios `nombre` y `duracion_seg`, y cree el atributo de estado `ejecutada` con el valor inicial `False`.
- Un método `ejecutar()` que marque la etapa como ejecutada y devuelva el texto  `OK <nombre> (<duracion_seg>s)`.

**Clase `Pipeline`**

- Un constructor que reciba el parámetro obligatorio `nombre` y cree el atributo `etapas` como una **lista vacía**.
- Un método `agregar_etapa(etapa)` que añada un objeto `Etapa` a la lista.
- Un método `duracion_total()` que devuelva la suma de la duración de todas sus etapas.
- Un método `ejecutar()` que:
    1. Muestre la cabecera `Pipeline '<nombre>' (<n> etapas)`.
    2. Ejecute cada etapa **en orden**, llamando a su propio método `ejecutar()`, y muestre el texto que devuelve.
    3. Muestre `Duración total: <segundos>s`, **usando el método `duracion_total()`**.

Después:

1. Crea un *pipeline* llamado `"ventas_nocturno"`.
2. Añádele estas cuatro etapas, en este orden:
    - `"extraer_ficheros_tiendas"`: 120 segundos
    - `"validar_esquema"`: 35 segundos
    - `"deduplicar_tickets"`: 48 segundos
    - `"publicar_zona_curated"`: 60 segundos
3. Muestra una lista con el estado `ejecutada` de cada etapa, usando una *list comprehension*.
4. Ejecuta el *pipeline*.
5. Vuelve a mostrar la lista con el estado `ejecutada` de cada etapa.

Reflexiona: ¿qué clase sabe cómo se ejecuta una etapa y cuál sabe en qué orden se ejecutan? ¿Por qué el estado de las etapas cambia aunque solo hayas llamado al método `ejecutar()` del *pipeline*?
"""
class Etapa:
    def __init__(self, nombre, duracion_seg):
        self.nombre = nombre
        self.duracion_seg = duracion_seg
        self.ejecutada = False

    def ejecutar(self):
        self.ejecutada = True
        return f"  OK{self.nombre} ({self.duracion_seg}s)"

class Pipeline:
    def __init__(self, nombre):
        self.nombre = nombre
        self.etapas = []

    def agregar_etapa(self, etapa):
        self.etapas.append(etapa)

    def duracion_total(self):
        return sum([etapa.duracion_seg for etapa in self.etapas])

    def ejecutar(self):
        print(f"Pipeline '{self.nombre}' ({len(self.etapas)} etapas)")
        for etapa in self.etapas:
            print(etapa.ejecutar())
        print(f"Duración total:{self.duracion_total()}s")

pipeline = Pipeline("ventas_nocturno")
pipeline.agregar_etapa(Etapa("extraer_ficheros_tiendas", 120))
pipeline.agregar_etapa(Etapa("validar_esquema", 35))
pipeline.agregar_etapa(Etapa("deduplicar_tickets", 48))
pipeline.agregar_etapa(Etapa("publicar_zona_curated", 60))

print([etapa.ejecutada for etapa in pipeline.etapas])
pipeline.ejecutar()
print([etapa.ejecutada for etapa in pipeline.etapas])