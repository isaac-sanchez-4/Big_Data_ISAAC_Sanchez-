def agrupar_por_longitud(lista_palabras):
    resultado = {}

    for palabra in lista_palabras:
        longitud = len(palabra)
        if longitud not in resultado:
            resultado[longitud] = []
        if palabra not in resultado[longitud]:
            resultado[longitud].append(palabra)

    for longitud in resultado:
        resultado[longitud].sort()

    return resultado


palabras = ["sol", "casa", "sol", "perro", "gato", "luz", "árbol", "casa","pollazo"]
print(agrupar_por_longitud(palabras))
