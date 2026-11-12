ventas = [
    {"id": 1, "categoria": "tecnología", "producto": "ratón", "precio": 25.50, "cantidad": 3},
    {"id": 2, "categoria": "hogar", "producto": "lámpara", "precio": 45.00, "cantidad": 1},
    {"id": 3, "categoria": "tecnología", "producto": "teclado", "precio": 60.00, "cantidad": 2},
    {"id": 4, "categoria": "ropa", "producto": "camisa", "precio": 30.00, "cantidad": 4},
    {"id": 5, "categoria": "hogar", "producto": "alfombra", "precio": 80.00, "cantidad": 1},
    {"id": 6, "categoria": "tecnología", "producto": "monitor", "precio": 150.00, "cantidad": 1}
]

def analizar_ventas(lista_ventas):
    resumen ={}
    for venta in lista_ventas:
        categoria = venta["categoria"]
        producto = venta["producto"]
        ingreso = venta["precio"] * venta["cantidad"]

        if categoria not in resumen:
            resumen[categoria] = {
                "ingresos_totales": 0,
                "productos_vendidos": set()
            }

        resumen[categoria]["ingresos_totales"] += ingreso
        resumen[categoria]["productos_vendidos"].add(producto)

    return resumen


resultado = analizar_ventas(ventas)
print(resultado)