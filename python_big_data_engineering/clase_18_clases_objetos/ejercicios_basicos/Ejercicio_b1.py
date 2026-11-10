class Empleado:
    def __init__(self, nombre, departamento, salario_bruto):
        self.nombre = nombre
        self.departamento = departamento
        self.salario_bruto = salario_bruto
        self.proyectos = []

    def asignar_proyecto(self, proyecto):
        if proyecto not in self.proyectos:
            self.proyectos.append(proyecto)

    def salario_neto_mensual(self, retencion=0.15):
        salario_neto_anual = self.salario_bruto * (1 - retencion)
        return round(salario_neto_anual / 14, 2)

    def __str__(self):
        return f"{self.nombre} ({self.departamento}) · {len(self.proyectos)} proyectos"


# Código de prueba
lucia = Empleado("Lucía Ortega", "Data Platform", 42000)
mario = Empleado("Mario Gil", "BI", 35000)
lucia.asignar_proyecto("Migración a Lakehouse")
lucia.asignar_proyecto("Catálogo de datos")
lucia.asignar_proyecto("Migración a Lakehouse")
print(lucia)
print(mario)
print(lucia.proyectos)
print(lucia.salario_neto_mensual())
print(lucia.salario_neto_mensual(0.20))
print(mario.salario_neto_mensual())