class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # 1. Representación en texto (print y str)
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    # 2. Operadores de Comparación (__eq__ para == y __lt__ para <)
    def __eq__(self, otro):
        if not isinstance(otro, Vector):
            return False
        return self.x == otro.x and self.y == otro.y

    def __lt__(self, otro):
        # Comparamos por longitud/magnitud simple para el ejemplo
        return (self.x**2 + self.y**2) < (otro.x**2 + otro.y**2)

    # 3. Operadores Aritméticos (+, -, *)
    def __add__(self, otro):
        if isinstance(otro, Vector):
            return Vector(self.x + otro.x, self.y + otro.y)
        raise TypeError("Solo se puede sumar con otro Vector")

    def __sub__(self, otro):
        if isinstance(otro, Vector):
            return Vector(self.x - otro.x, self.y - otro.y)
        raise TypeError("Solo se puede restar con otro Vector")

    def __mul__(self, escalar):
        if isinstance(escalar, (int, float)):
            return Vector(self.x * escalar, self.y * escalar)
        raise TypeError("El multiplicador debe ser un número")


# ==========================================
# PRUEBAS DE FUNCIONAMIENTO
# ==========================================
if __name__ == "__main__":
    v1 = Vector(3.0, 4.0)
    v2 = Vector(1.0, 2.0)
    v3 = Vector(3.0, 4.0)

    # Probando __str__
    print("v1:", v1)  # Vector(3.0, 4.0)

    # Probando __eq__ (==)
    print("¿v1 == v3?:", v1 == v3)  # True

    # Probando __lt__ (<)
    print("¿v2 < v1?:", v2 < v1)  # True (porque v2 es más pequeño)

    # Probando __add__ (+)
    suma = v1 + v2
    print("v1 + v2 =", suma)  # Vector(4.0, 6.0)

    # Probando __sub__ (-)
    resta = v1 - v2
    print("v1 - v2 =", resta)  # Vector(2.0, 2.0)

    # Probando __mul__ (*)
    multi = v1 * 2
    print("v1 * 2 =", multi)  # Vector(6.0, 8.0)

from dataclasses import dataclass


# ==========================================
# 1. EJEMPLO CON @DATACLASS (La forma rápida)
# ==========================================
# Si usas dataclass, Python te autogenera el __init__, __eq__ y __str__ por ti.
@dataclass
class ItemInventario:
    nombre: str
    stock: int
    precio: float


# Si creas dos objetos iguales, al tener el __eq__ automático, darán True al compararlos:
# item1 = ItemInventario("Teclado", 10, 45.99)
# item2 = ItemInventario("Teclado", 10, 45.99)
# print(item1 == item2)  -> Devuelve True


# ==========================================================
# 2. EJEMPLO CLásico CON MÉTODOS MÁGICOS A MANO (__eq__, __str__, etc.)
# ==========================================================
class Rectangulo:
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    # El famoso __str__ para que el objeto se imprima bonito en texto
    def __str__(self):
        return f"Rectángulo de base {self.base} y altura {self.altura}"

    # El __eq__ que vimos para comparar si dos rectángulos son iguales por sus datos
    def __eq__(self, otro):
        if not isinstance(otro, Rectangulo):
            return False
        return self.base == otro.base and self.altura == otro.altura

    # El operador de suma (+) para sumar las áreas de dos rectángulos y crear uno nuevo
    def __add__(self, otro):
        if not isinstance(otro, Rectangulo):
            raise TypeError("Solo se puede sumar con otro Rectangulo")

        nueva_base = self.base + otro.base
        nueva_altura = self.altura + otro.altura
        return Rectangulo(nueva_base, nueva_altura)

    # Método normal de la clase
    def area(self):
        return self.base * self.altura


# ==========================
# PRUEBAS DE FUNCIONAMIENTO
# ==========================
if __name__ == "__main__":
    r1 = Rectangulo(5.0, 3.0)
    r2 = Rectangulo(5.0, 3.0)
    r3 = Rectangulo(2.0, 2.0)

    # 1. Probando __str__
    print(r1)  # Muestra: Rectángulo de base 5.0 y altura 3.0

    # 2. Probando __eq__ (Compara los datos internos, no la memoria)
    print("¿Son r1 y r2 iguales?", r1 == r2)  # True
    print("¿Son r1 y r3 iguales?", r1 == r3)  # False

    # 3. Probando __add__ (Sumar objetos con el signo +)
    r_suma = r1 + r3
    print("Rectángulo sumado:", r_suma)  # Rectángulo de base 7.0 y altura 5.0




"""

1. Operadores Matemáticos (Aritméticos)
Sirven para cuando haces operaciones entre objetos con símbolos como +, -, *, etc.

Suma (+): def __add__(self, otro):

Resta (-): def __sub__(self, otro):

Multiplicación (*): def __mul__(self, otro):

División (/): def __truediv__(self, otro):

División entera (//): def __floordiv__(self, otro):

Módulo / Resto (%): def __mod__(self, otro):

Potencia (**): def __pow__(self, otro):

2. Operadores de Asignación In-situ (Modificar el propio objeto)
Sirven cuando usas operadores como +=, -=, etc., que modifican el objeto actual en lugar de crear uno nuevo.

Suma e igual (+=): def __iadd__(self, otro): (calcula, modifica self y devuelve return self)

Resta e igual (-=): def __isub__(self, otro):

Multiplicación e igual (*=): def __imul__(self, otro):

3. Operadores de Comparación
Sirven para comparar objetos con <, >, ==, etc. (Python a veces deduce algunos si programas los inversos, pero estos son los oficiales):

Igualdad (==): def __eq__(self, otro):

Desigualdad (!=): def __ne__(self, otro):

Menor que (<): def __lt__(self, otro): (less than)

Menor o igual (<=): def __le__(self, otro): (less or equal)

Mayor que (>): def __gt__(self, otro): (greater than)

Mayor o igual (>=): def __ge__(self, otro): (greater or equal)

4. Otros métodos mágicos clásicos (Por si acaso)
Representación en texto para usuarios (__str__): Lo que se muestra al hacer print() o str().

Representación técnica para devs (__repr__): La forma oficial o de depuración del objeto.

Longitud (__len__): Permite usar len(objeto).

Pertenencia (__contains__): Permite usar el operador in (ej. item in mi_objeto).
"""