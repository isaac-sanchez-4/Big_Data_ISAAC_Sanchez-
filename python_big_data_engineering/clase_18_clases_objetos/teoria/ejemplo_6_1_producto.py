"""Una tienda online necesita representar los productos de su catálogo de forma legible, tanto para mostrarlos a los usuarios como para depurarlos en el código. Crea una clase `Producto` que defina **dos representaciones en texto** distintas mediante los métodos especiales `__str__` y `__repr__`.

El constructor debe recibir los parámetros obligatorios `sku`, `nombre` y `precio`, y guardarlos como atributos de instancia.

Además, la clase debe tener dos **métodos especiales**:

- `__str__()`: devuelve una representación **pensada para el usuario**, con el formato `<nombre> (<sku>) - <precio> €`, mostrando el precio con 2 decimales.
- `__repr__()`: devuelve una representación **pensada para el desarrollador**, con el formato `Producto(sku='<sku>', nombre='<nombre>', precio=<precio>)`.

Después:

1. Crea un producto `p` con SKU `"SKU-4471"`, nombre `"Auriculares BT"` y precio `59.9`.
2. Muestra el producto de cuatro formas distintas:
    - Con `print(p)`.
    - Con `print(str(p))`.
    - Con `print(repr(p))`.
    - Dentro de una f-string: `f"Producto destacado: {p}"`.
3. Crea una lista `catalogo` que contenga `p` y un segundo producto con SKU `"SKU-1020"`, nombre `"Cargador USB-C"` y precio `19.95`.
4. Muestra la lista completa con `print(catalogo)`.

Observa la salida: ¿qué método usa Python en cada uno de los casos del punto 2? ¿Y cuál usa al imprimir la lista del punto 4? ¿Qué se mostraría si la clase no definiera `__repr__`?"""
class Producto:
    def __init__(self, sku, nombre, precio):
        self.sku = sku
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} ({self.sku}) -{self.precio:.2f} €"

    def __repr__(self):
        return f"Producto(sku='{self.sku}', nombre='{self.nombre}', precio={self.precio})"

p = Producto("SKU-4471", "Auriculares BT", 59.9)

print(p)
print(str(p))
print(repr(p))
print(f"Producto destacado:{p}")

catalogo = [p, Producto("SKU-1020", "Cargador USB-C", 19.95)]
print(catalogo)