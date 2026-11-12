from functools import reduce
class ProductoTienda:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = float(precio)

    def precio_final(self):
        return self.precio

    def __str__(self):
        return f"{self.nombre} - {self.precio_final():.2f} €"


class ProductoUrgente(ProductoTienda):
    def __init__(self, nombre, precio, recargo_urgencia):
        super().__init__(nombre, precio)
        self.recargo_urgencia = float(recargo_urgencia)

    def precio_final(self):
        return super().precio_final() + self.recargo_urgencia


class ProductoPromocion(ProductoTienda):
    def __init__(self, nombre, precio, descuento):
        super().__init__(nombre, precio)
        self.descuento = float(descuento)

    def precio_final(self):
        return super().precio_final() * (1 - self.descuento)


transacciones = [
    {"cliente": "Lucía", "item": ProductoTienda("Cable HDMI", 15.0), "cantidad": 2},
    {"cliente": "Carlos", "item": ProductoUrgente("Reparación placa", 120.0, 30.0), "cantidad": 1},
    {"cliente": "Ana", "item": ProductoPromocion("Antivirus", 40.0, 0.20), "cantidad": 1},
    {"cliente": "Lucía", "item": ProductoTienda("Ratón USB", 25.0), "cantidad": 1},
    {"cliente": "Marcos", "item": ProductoUrgente("Recuperación datos", 80.0, 20.0), "cantidad": 1}
]


lista_importes = list(map(lambda x: x["item"].precio_final() * x["cantidad"],transacciones))
print(lista_importes)

transacciones_urgentes = filter(lambda x: isinstance(x["item"], ProductoUrgente), transacciones)

nonbres = list(map(lambda x: x["item"].nombre, transacciones_urgentes))

print(nonbres)

factura_total = reduce(lambda acumulado,importe: acumulado + importe, lista_importes, 0.0)
print(f"{factura_total:.2f}")


def contar_total_articulos(transacciones):
    if not transacciones:
        return 0
    return transacciones[0]["cantidad"] + contar_total_articulos(transacciones[1:])

total_articulos = contar_total_articulos(transacciones)

print(f"Total de artículos vendidos: {total_articulos}")

