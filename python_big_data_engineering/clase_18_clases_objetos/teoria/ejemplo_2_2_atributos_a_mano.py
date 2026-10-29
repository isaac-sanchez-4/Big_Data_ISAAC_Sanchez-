# En Python, a un objeto se le pueden añadir atributos en cualquier momento con la notación `objeto.atributo = valor`. En este ejercicio vas a comprobar qué problema genera hacerlo así.
#
# Partiendo de la clase vacía `Pedido`:
#
# 1. Crea un objeto `pedido_a` y asígnale **a mano** dos atributos: `codigo` con el valor `"PED-1001"` e `importe` con el valor `149.90`.
# 2. Crea un objeto `pedido_b` y asígnale **solo** el atributo `codigo` con el valor `"PED-1002"`.
#
# Después, muestra por pantalla:
#
# 1. El código y el importe de `pedido_a`.
# 2. El código de `pedido_b`.
# 3. Si `pedido_a` tiene el atributo `importe`, usando `hasattr()`.
# 4. Si `pedido_b` tiene el atributo `importe`, usando `hasattr()`.
# 5. Todos los atributos de `pedido_a` y de `pedido_b`, usando `vars()`.
#
# Observa la salida: ¿tienen ambos pedidos la misma estructura? ¿Qué pasaría si intentaras mostrar `pedido_b.importe`?

class Pedido:
    pass

pedido_a = Pedido()
pedido_a.codigo = "PED-1001"
pedido_a.importe = 149.90

pedido_b = Pedido()
pedido_b.codigo = "PED-1002"

print(pedido_a.codigo, pedido_a.importe)
print(pedido_b.codigo)
print(hasattr(pedido_a, "importe"))
print(hasattr(pedido_b, "importe"))
print(vars(pedido_a))
print(vars(pedido_b))