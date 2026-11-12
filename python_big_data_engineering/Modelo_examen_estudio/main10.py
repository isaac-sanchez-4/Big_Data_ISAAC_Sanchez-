from traceback import print_tb


def numeros(n):
    # 1. El caso base (el freno)
    if n == 0:
        return "yaaa"

    # 2. El paso recursivo (llamarse a sí misma cambiando n)
    return str(n) + " " + numeros(n - 1)
print(numeros(7))
"""
print(numeros(7))


with open("datos.txt", "r", encoding="utf-8") as f:
    for linea in f:
        print(linea.strip()) # .strip() quita los saltos de línea invisibles (\n)


with open("resultado.txt", "w", encoding="utf-8") as f:
    f.write("Hola, esto es el examen\n")

"""