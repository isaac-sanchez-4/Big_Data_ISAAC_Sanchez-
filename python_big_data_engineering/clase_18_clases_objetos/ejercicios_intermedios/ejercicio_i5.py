class EquipoProyecto:
    horas_empresa = 0
    equipos_creados = 0

    def __init__(self, nombre):
        self.nombre = nombre
        self.horas = 0
        self.miembros = []
        EquipoProyecto.equipos_creados += 1

    def incorporar(self, persona, horas):
        self.miembros.append(persona)
        self.horas += horas
        EquipoProyecto.horas_empresa += horas

    def __str__(self):
        return f"{self.nombre}:{self.miembros} · {self.horas} h"


datos = EquipoProyecto("Data Lake")
ml = EquipoProyecto("Churn ML")
datos.incorporar("Ana", 120)
datos.incorporar("Luis", 80)
ml.incorporar("Sara", 60)
print(datos)
print(ml)
print(EquipoProyecto.equipos_creados, EquipoProyecto.horas_empresa)
print(datos.miembros is ml.miembros)
print(vars(datos))