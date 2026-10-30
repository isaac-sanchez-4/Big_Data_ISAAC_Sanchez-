"""
Una empresa de paquetería necesita analizar los envíos del día. Crea una clase `Envio` y procesa una **lista de objetos** de esa clase para obtener distintos indicadores.

La clase `Envio` debe tener:

- Un constructor que reciba los parámetros obligatorios `id_envio`, `destino`, `peso_kg` y `entregado` (un booleano), y los guarde como atributos de instancia.
- Un método especial `__repr__()` que devuelva el texto `Envio(<id_envio>, <destino>, <peso_kg> kg)`.

Crea también una **función** (fuera de la clase) llamada `obtener_peso(envio)` que reciba un envío y devuelva su peso.

Después, crea una lista `envios` con estos cinco envíos:

| id_envio | destino | peso_kg | entregado |
| --- | --- | --- | --- |
| E-01 | Madrid | 2.5 | True |
| E-02 | Sevilla | 14.0 | False |
| E-03 | Madrid | 0.8 | True |
| E-04 | Bilbao | 7.2 | False |
| E-05 | Sevilla | 3.1 | True |

Y calcula los siguientes indicadores:

1. `peso_total`: la suma del peso de todos los envíos, usando `sum()` con una *list comprehension*.
2. `pendientes`: una lista con los **identificadores** de los envíos que aún no se han entregado, usando una *list comprehension* con condición.
3. `envios_por_destino`: un diccionario que cuente cuántos envíos hay para cada destino, recorriendo la lista con un bucle `for` y usando el método `get()` del diccionario.
4. `mas_pesados`: los 2 envíos más pesados, usando `sorted()` con la función `obtener_peso` como `key`, en orden descendente.

Por último, muestra los cuatro indicadores por pantalla, con el peso total redondeado a 2 decimales y seguido de `kg`.

Fíjate en el punto 4: ¿por qué se pasa `obtener_peso` sin paréntesis? ¿Qué método de la clase usa Python para mostrar la lista `mas_pesados`?
"""
class Envio:
    def __init__(self, id_envio, destino, peso_kg, entregado):
        self.id_envio = id_envio
        self.destino = destino
        self.peso_kg = peso_kg
        self.entregado = entregado

    def __repr__(self):
        return f"Envio({self.id_envio},{self.destino},{self.peso_kg} kg)"

def obtener_peso(envio):
    return envio.peso_kg

envios = [
    Envio("E-01", "Madrid", 2.5, True),
    Envio("E-02", "Sevilla", 14.0, False),
    Envio("E-03", "Madrid", 0.8, True),
    Envio("E-04", "Bilbao", 7.2, False),
    Envio("E-05", "Sevilla", 3.1, True),
]

peso_total = sum([e.peso_kg for e in envios])
pendientes = [e.id_envio for e in envios if not e.entregado]

envios_por_destino = {}
for e in envios:
    envios_por_destino[e.destino] = envios_por_destino.get(e.destino, 0) + 1

mas_pesados = sorted(envios, key=obtener_peso, reverse=True)[:2]

print("Peso total:", round(peso_total, 2), "kg")
print("Pendientes:", pendientes)
print("Envíos por destino:", envios_por_destino)
print("Los 2 más pesados:", mas_pesados)