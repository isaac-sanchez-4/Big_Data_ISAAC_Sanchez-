precios = [12.5, 65.0, 45.0, 120.0, 30.5, 85.0]


es_caro = lambda precio: precio >= 50.0

# Ejemplos de uso
print(es_caro(65.0))  # True
print(es_caro(50.0))  # True
print(es_caro(12.5))  # False

solo_caros = list(filter(es_caro, precios))
print(solo_caros)

precios_con_descuento = list(map(lambda precio: precio * 0.8, solo_caros))
print(precios_con_descuento)


def cuenta_atras(n):
    if n <= 0:
        return "yaaa"
    return f"{n} {cuenta_atras(n - 1)}"

print(cuenta_atras(5))
print(cuenta_atras(10))