from main import Libro

class empleado :
    def __init__(self,nombre,sueldo_base):
        self.nombre = nombre
        self.sueldo_base = sueldo_base

    def calcular_sueldo(self):
        return self.sueldo_base


class gerente(empleado):
    def __init__(self,nombre,sueldo_base,incentivo):
        super().__init__(nombre,sueldo_base)
        self.incentivo = incentivo

    def calcular_sueldo(self):
        return  super().calcular_sueldo() + self.incentivo


emp = empleado("Ana",1500)
ger = gerente("Carlos",2000,500)


print(f"Sueldo empleado: {emp.calcular_sueldo()} €")
print(f"Sueldo gerente: {ger.calcular_sueldo()} €")


class biblioteca :
    def __init__(self):
        self.libros = []

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def mostrar_libros(self):
        return [libro.titulo for libro in self.libros if libro.es_largo()]

mi_biblio = biblioteca()
print(mi_biblio.mostrar_libros())

libro1 = Libro("Don Quijote", "Miguel de Cervantes", 500)
libro2 = Libro("El Principito", "Antoine de Saint-Exupéry", 96)
libro3 = Libro("Cien años de soledad", "Gabriel García Márquez",4852)

mi_biblio.agregar_libro(libro1)
mi_biblio.agregar_libro(libro2)
mi_biblio.agregar_libro(libro3)
print(mi_biblio.mostrar_libros())
print(libro1.es_largo())
