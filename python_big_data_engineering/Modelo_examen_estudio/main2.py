class CuentaBancaria:
    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self.saldo = float(saldo)

    def ingresar(self, cantidad):
        if cantidad > 0:
            self.saldo += cantidad

    def retirar(self, cantidad):
        if cantidad > 0 and self.saldo >= cantidad:
            self.saldo -= cantidad
            return True
        return False

    def __str__(self):
        return f"Cuenta de {self.titular} con saldo {self.saldo} €"


# Ejemplo de uso
mi_cuenta = CuentaBancaria("Juan", 1000)
print(mi_cuenta)

mi_cuenta.ingresar(250.5)
print(mi_cuenta.retirar(500))
print(mi_cuenta.retirar(2000))
print(mi_cuenta)



class Alumno:
    def __init__(self, nombre):
        self.nombre = nombre
        self.calificaciones = []

    def agregar_calificacion(self, calificacion):
        self.calificaciones.append(calificacion)

    def calcular_media(self):
        if not self.calificaciones:
            return 0.0
        return sum(self.calificaciones) / len(self.calificaciones)
    def __str__(self):
        return f"Alumno: {self.nombre}, Calificaciones: {self.calificaciones}, Media: {self.calcular_media():.2f}"

alumno = Alumno("Pedro")
alumno.agregar_calificacion(8)
alumno.agregar_calificacion(9)

print(alumno)

alumno2 = Alumno("Pedro2")

print(alumno2)
