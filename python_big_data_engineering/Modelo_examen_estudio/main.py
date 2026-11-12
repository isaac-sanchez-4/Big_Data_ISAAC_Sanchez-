class Libro:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas


    def es_largo(self):
        return self.paginas > 300

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
mi_libro = Libro("Don Quijote", "Miguel de Cervantes", 500)

print(mi_libro.es_largo())
print(mi_libro)


class rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)

    def __str__(self):
        return f"Rectangulo de base {self.base} y altura {self.altura}"




cuadrado = rectangulo(2, 3)
print(cuadrado.area())
print(cuadrado.perimetro())
print(cuadrado)
