"""Un proceso de ingesta agrupa los tickets de venta de cada día en **lotes**. Crea una clase `LoteDatos` que permita ir añadiendo registros a un lote y consultar información sobre ellos.  El constructor debe recibir el parámetro obligatorio `id_lote` y crear el atributo `registros` como una **lista vacía** propia de cada lote.

Además, la clase debe tener tres **métodos**:

- `agregar(registro)`: añade un registro (un diccionario) a la lista `registros`.
- `total_registros()`: devuelve cuántos registros tiene el lote.
- `importe_total()`: devuelve la suma del campo `"importe"` de todos los registros, redondeada a 2 decimales.

Después:

1. Crea un objeto `lote` con el identificador `"L-2026-10-26-01"`.
2. Añádele estos tres registros usando el método `agregar`:
    - `{"ticket": "T1", "importe": 23.50}`
    - `{"ticket": "T2", "importe": 8.75}`
    - `{"ticket": "T3", "importe": 112.00}`
3. Muestra por pantalla el identificador del lote, el número de registros y el importe total.
4. Vuelve a mostrar el número de registros, pero esta vez llamando al método **desde la clase** y pasando el objeto como argumento: `LoteDatos.total_registros(lote)`.

Compara los resultados de los puntos 3 y 4: ¿Qué te dice esto sobre el papel de `self`?"""
class LoteDatos:
    def __init__(self, id_lote):
        self.id_lote = id_lote
        self.registros = []

    def agregar(self, registro):
        self.registros.append(registro)

    def total_registros(self):
        return len(self.registros)

    def importe_total(self):
        total = 0
        for registro in self.registros:
            total += registro["importe"]
        return round(total, 2)

lote = LoteDatos("L-2026-10-26-01")
lote.agregar({"ticket": "T1", "importe": 23.50})
lote.agregar({"ticket": "T2", "importe": 8.75})
lote.agregar({"ticket": "T3", "importe": 112.00})

print(lote.id_lote)
print(lote.total_registros())
print(lote.importe_total())
print(LoteDatos.total_registros(lote))