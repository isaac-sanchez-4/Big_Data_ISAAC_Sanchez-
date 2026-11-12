inventario = [
    {"nombre": "Teclado mecánico", "categoria": "Periféricos", "stock": 45, "precio": 85.0},
    {"nombre": "Monitor 27\"", "categoria": "Pantallas", "stock": 8, "precio": 240.0},
    {"nombre": "Ratón inalámbrico", "categoria": "Periféricos", "stock": 120, "precio": 25.0},
    {"nombre": "Soportes VESA", "categoria": "Pantallas", "stock": 15, "precio": 35.0},
    {"nombre": "Cable HDMI 2m", "categoria": "Cables", "stock": 4, "precio": 12.0},
    {"nombre": "Hub USB-C", "categoria": "Periféricos", "stock": 6, "precio": 45.0}
]


def generar_informe_stock(lista_inventario):
    return {
        "stock_valorado": {
            p["nombre"]: p["stock"] * p["precio"]
            for p in lista_inventario
            if (p["stock"] * p["precio"]) > 500.0
        },
        "criticos": sorted([
            p["nombre"]
            for p in lista_inventario
            if p["stock"] < 10
        ]),
        "categorias_activas": {
            p["categoria"]
            for p in lista_inventario
            if p["stock"] > 0
        }
    }

informe = generar_informe_stock(inventario)
print(informe)
