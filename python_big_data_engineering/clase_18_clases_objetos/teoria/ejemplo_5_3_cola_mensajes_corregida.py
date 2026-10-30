"""`self.mensajes.append(...)` no crea un atributo nuevo: **modifica la lista de la clase**, que es la misma para todas las colas. Los mensajes de pagos aparecen en pedidos y viceversa. La corrección es crear la lista en el constructor, de modo que cada objeto tenga la suya:"""
class ColaMensajes:
    def __init__(self, topic):
        self.topic = topic
        self.mensajes = []     # atributo de instancia: una lista por cola

    def publicar(self, mensaje):
        self.mensajes.append(mensaje)

pedidos = ColaMensajes("pedidos")
pagos = ColaMensajes("pagos")
pedidos.publicar("pedido 501 creado")
pagos.publicar("pago 77 confirmado")

print(pedidos.topic, pedidos.mensajes)
print(pagos.topic, pagos.mensajes)
print(pedidos.mensajes is pagos.mensajes)