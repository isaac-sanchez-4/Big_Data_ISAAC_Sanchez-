class Empleado:
    def __init__(self, id_empleado, nombre, salario_base, departamento):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.salario_base = salario_base
        self.departamento = departamento

    def mostrar_informacion(self):
        print(f"ID: {self.id_empleado}\nNombre: {self.nombre}\nDepartamento: {self.departamento}\nSalario base: {self.salario_base} €")


class Desarrollador(Empleado):
    def __init__(self, id_empleado, nombre, salario_base, departamento, lenguaje_principal, nivel):
        super().__init__(id_empleado, nombre, salario_base, departamento)
        self.lenguaje_principal = lenguaje_principal
        self.nivel = nivel

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Lenguaje principal: {self.lenguaje_principal}\nNivel: {self.nivel}\n")


class AnalistaDatos(Empleado):
    def __init__(self, id_empleado, nombre, salario_base, departamento, herramienta_bi, especialidad):
        super().__init__(id_empleado, nombre, salario_base, departamento)
        self.herramienta_bi = herramienta_bi
        self.especialidad = especialidad

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Herramienta BI: {self.herramienta_bi}\nEspecialidad: {self.especialidad}\n")


class AdministradorSistemas(Empleado):
    def __init__(self, id_empleado, nombre, salario_base, departamento, sistema_operativo, certificacion):
        super().__init__(id_empleado, nombre, salario_base, departamento)
        self.sistema_operativo = sistema_operativo
        self.certificacion = certificacion

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Sistema operativo: {self.sistema_operativo}\nCertificación: {self.certificacion}\n")


empleados = [
    Desarrollador("E001", "Ana López", 2800, "Desarrollo", "Python", "Senior"),
    Desarrollador("E002", "Marc Ruiz", 2400, "Desarrollo", "JavaScript", "Junior"),
    AnalistaDatos("E003", "Carlos Pérez", 2600, "Datos", "Power BI", "Análisis de ventas"),
    AnalistaDatos("E004", "Sofía Chen", 2750, "Datos", "Tableau", "Big Data"),
    AdministradorSistemas("E005", "Laura Gómez", 2900, "Infraestructura", "Linux", "AZ-104"),
    AdministradorSistemas("E006", "David Sanz", 3100, "Infraestructura", "Windows Server", "CCNA")
]

for emp in empleados:
    emp.mostrar_informacion()