"""Un equipo de integración necesita una cola de mensajes independiente para cada *topic* (por ejemplo, `"pedidos"` y `"pagos"`). Un desarrollador ha definido la lista de mensajes **como atributo de clase** por error. En este ejercicio vas a reproducir el fallo y descubrir por qué ocurre.

Crea una clase `ColaMensajes` con:

- Un **atributo de clase** `mensajes` con una **lista vacía**.
- Un constructor que reciba el parámetro obligatorio `topic` y lo guarde como atributo de instancia.
- Un método `publicar(mensaje)` que añada el mensaje a `self.mensajes` usando `append()`.

Después:

1. Crea dos colas: `pedidos` con el *topic* `"pedidos"` y `pagos` con el *topic* `"pagos"`.
2. Publica `"pedido 501 creado"` en la cola `pedidos`.
3. Publica `"pago 77 confirmado"` en la cola `pagos`.
4. Muestra el *topic* y los mensajes de cada cola.
5. Comprueba con el operador `is` si `pedidos.mensajes` y `pagos.mensajes` son el mismo objeto.

Observa la salida: ¿contiene cada cola solo sus propios mensajes? ¿Por qué `append()` no crea una lista nueva en el objeto, como sí ocurría al asignar `umbral_nulos` en el ejemplo anterior?

Por último, **corrige la clase** para que cada cola tenga su propia lista de mensajes y comprueba que la salida es la correcta."""
class ColaMensajes:
    mensajes = []          # atributo de clase mutable: compartido por todas las colas

    def __init__(self, topic):
        self.topic = topic

    def publicar(self, mensaje):
        self.mensajes.append(mensaje)

pedidos = ColaMensajes("pedidos")
pagos = ColaMensajes("pagos")
pedidos.publicar("pedido 501 creado")
pagos.publicar("pago 77 confirmado")

print(pedidos.topic, pedidos.mensajes)
print(pagos.topic, pagos.mensajes)
print(pedidos.mensajes is pagos.mensajes)