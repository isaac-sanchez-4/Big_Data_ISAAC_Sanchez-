# Un sistema de gestión de pedidos necesita empezar definiendo el tipo `Pedido`, aunque todavía no tenga atributos ni comportamiento. Crea una clase `Pedido` **vacía**, usando `pass` como cuerpo.
#
# Después, crea dos objetos de esa clase: `pedido_a` y `pedido_b`.
#
# Por último, muestra por pantalla:
#
# 1. El tipo de `pedido_a`, usando `type()`.
# 2. Solo el nombre de la clase de `pedido_a`, usando el atributo `__name__` sobre el resultado de `type()`.
# 3. Si `pedido_a` es una instancia de `Pedido`, usando `isinstance()`.
# 4. Si el texto `"PED-1001"` es una instancia de `Pedido`, usando `isinstance()`.
# 5. Si `pedido_a` y `pedido_b` son el mismo objeto, usando el operador `is`.
class Pedido:
    pass

pedido_a = Pedido()
pedido_b = Pedido()

print(type(pedido_a))
print(type(pedido_a).__name__)
print(isinstance(pedido_a, Pedido))
print(isinstance("PED-1001", Pedido))
print(pedido_a is pedido_b)