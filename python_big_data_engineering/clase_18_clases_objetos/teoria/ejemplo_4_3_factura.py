"""El departamento de facturación necesita generar facturas que calculen automáticamente su subtotal, sus impuestos y su total. Crea una clase `Factura` en la que **unos métodos reutilicen a otros** en lugar de repetir los mismos cálculos.

El constructor debe recibir:

- `numero` y `cliente` como **parámetros obligatorios**.
- `tipo_iva` como **parámetro opcional**, con valor por defecto `0.21`.

Además, debe crear el atributo `lineas` como una **lista vacía** propia de cada factura.

La clase debe tener estos **métodos**:

- `agregar_linea(concepto, cantidad, precio_unitario)`: añade a `lineas` un diccionario con las claves `"concepto"`, `"cantidad"` y `"precio"`.
- `subtotal()`: devuelve la suma de `cantidad × precio` de todas las líneas, redondeada a 2 decimales.
- `impuestos()`: devuelve el subtotal multiplicado por el tipo de IVA, redondeado a 2 decimales. **Debe llamar a `subtotal()`**, no repetir su cálculo.
- `total()`: devuelve la suma del subtotal y los impuestos, redondeada a 2 decimales. **Debe llamar a `subtotal()` e `impuestos()`**.
- `imprimir()`: muestra la factura con este formato:
    - Una cabecera con el número de factura y el cliente.
    - Una línea por concepto con su nombre, cantidad, precio unitario e importe, alineados en columnas.
    - Las líneas finales de `Subtotal`, `IVA 21%` y `TOTAL`, alineadas a la derecha.

Después:

1. Crea una factura con número `"F-2026-0412"` para el cliente `"Logística Iberia S.L."`, usando el IVA por defecto.
2. Añádele estas líneas:
    - `"Licencia ETL (usuario)"`: 3 unidades a 49.90
    - `"Soporte anual"`: 1 unidad a 1200.00
    - `"Formación (jornada)"`: 2 unidades a 350.00
3. Llama al método `imprimir()` para mostrar la factura completa.

Reflexiona: si mañana cambia la forma de calcular el subtotal (por ejemplo, para aplicar descuentos), ¿cuántos métodos tendrías que modificar?"""
class Factura:
    def __init__(self, numero, cliente, tipo_iva=0.21):
        self.numero = numero
        self.cliente = cliente
        self.tipo_iva = tipo_iva
        self.lineas = []

    def agregar_linea(self, concepto, cantidad, precio_unitario):
        self.lineas.append({"concepto": concepto, "cantidad": cantidad, "precio": precio_unitario})

    def subtotal(self):
        return round(sum([linea["cantidad"] * linea["precio"] for linea in self.lineas]), 2)

    def impuestos(self):
        return round(self.subtotal() * self.tipo_iva, 2)

    def total(self):
        return round(self.subtotal() + self.impuestos(), 2)

    def imprimir(self):
        print(f"Factura{self.numero} · Cliente:{self.cliente}")
        for linea in self.lineas:
            importe = linea["cantidad"] * linea["precio"]
            print(f"{linea['concepto']:<22}{linea['cantidad']:>3} x{linea['precio']:>8.2f} ={importe:>9.2f}")
        print(f"{'Subtotal':<38}{self.subtotal():>9.2f}")
        print(f"{'IVA ' + str(int(self.tipo_iva * 100)) + '%':<38}{self.impuestos():>9.2f}")
        print(f"{'TOTAL':<38}{self.total():>9.2f}")

factura = Factura("F-2026-0412", "Logística Iberia S.L.")
factura.agregar_linea("Licencia ETL (usuario)", 3, 49.90)
factura.agregar_linea("Soporte anual", 1, 1200.00)
factura.agregar_linea("Formación (jornada)", 2, 350.00)
factura.imprimir()