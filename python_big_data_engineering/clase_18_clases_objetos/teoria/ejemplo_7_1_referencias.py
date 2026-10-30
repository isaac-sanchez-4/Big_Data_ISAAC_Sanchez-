"""
Un programa de fidelización gestiona los puntos que acumula cada cliente. En este ejercicio vas a comprobar que una variable **no contiene** el objeto, sino una **referencia** a él, y qué consecuencias tiene esto al asignar variables y al pasar objetos a funciones.

Crea una clase `ClienteFidelidad` con:

- Un constructor que reciba `id_cliente` como **parámetro obligatorio** y `puntos` como **parámetro opcional**, con valor por defecto `0`.
- Un método `sumar_puntos(cantidad)` que añada `cantidad` a los puntos del cliente.

Crea también una **función** (fuera de la clase) llamada `aplicar_bono_bienvenida(cliente)` que reciba un cliente y le sume 200 puntos usando su método `sumar_puntos`.

Después, realiza estas tres pruebas:

**Prueba 1: asignar un objeto a otra variable**

1. Crea un cliente `original` con id `"C-88"` y 100 puntos.
2. Haz `alias = original`.
3. Suma 50 puntos a través de `alias`.
4. Muestra los puntos de `original` y comprueba con `is` si `alias` y `original` son el mismo objeto.

**Prueba 2: dos objetos con los mismos datos**

1. Crea un cliente `otro` con id `"C-88"` y 150 puntos.
2. Comprueba con `is` si `otro` y `original` son el mismo objeto.
3. Comprueba con `==` si sus puntos son iguales.

**Prueba 3: pasar un objeto a una función**

1. Llama a `aplicar_bono_bienvenida(otro)`.
2. Muestra los puntos de `otro` y los de `original`.

Antes de ejecutar, intenta predecir la salida. ¿Por qué el cambio hecho a través de `alias` se ve en `original`? ¿Por qué `otro` y `original` no son el mismo objeto si tienen el mismo id y los mismos puntos? ¿Por qué la función modifica el objeto que recibe, aunque no devuelva nada?
"""
class ClienteFidelidad:
    def __init__(self, id_cliente, puntos=0):
        self.id_cliente = id_cliente
        self.puntos = puntos

    def sumar_puntos(self, cantidad):
        self.puntos += cantidad

def aplicar_bono_bienvenida(cliente):
    cliente.sumar_puntos(200)

original = ClienteFidelidad("C-88", 100)
alias = original
alias.sumar_puntos(50)
print(original.puntos)
print(alias is original)

otro = ClienteFidelidad("C-88", 150)
print(otro is original)
print(otro.puntos == original.puntos)

aplicar_bono_bienvenida(otro)
print(otro.puntos)
print(original.puntos)