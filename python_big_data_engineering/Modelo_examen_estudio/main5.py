import conversor
from conversor import celsius_to_fahrenheit, kg_a_libras

print(celsius_to_fahrenheit(25))
print(kg_a_libras(10))

def calcular_media(lista):
    return sum(lista) / len(lista) if lista else 0.0


def encontrar_maximo(lista):
    return max(lista)

if __name__ == "__main__":

    numeros = [10, 25, 8, 42, 15]

    media = calcular_media(numeros)
    maximo = encontrar_maximo(numeros)

    print(f"Lista de prueba: {numeros}")
    print(f"Media calculada: {media}")
    print(f"Valor máximo: {maximo}")