class Incidencia:
    def __init__(self, numero, empleado, descripcion):
        self.numero = numero
        self.empleado = empleado
        self.descripcion = descripcion

    def mostrar_informacion(self):
        print(f"Incidencia: {self.numero}")
        print(f"Empleado: {self.empleado}")
        print(f"Descripción: {self.descripcion}")

    def resolver(self):
        print("Solución: revisión general de la incidencia")


class GestionPrioridad:
    def __init__(self, prioridad):
        self.prioridad = prioridad

    def mostrar_prioridad(self):
        if self.prioridad == "alta":
            print("Prioridad: ALTA - atención urgente")
        elif self.prioridad == "media":
            print("Prioridad: MEDIA - atención normal")
        else:
            print("Prioridad: BAJA - atención no urgente")


class TicketSoporte(Incidencia, GestionPrioridad):
    def __init__(self, numero, empleado, descripcion, prioridad):
        Incidencia.__init__(self, numero, empleado, descripcion)
        GestionPrioridad.__init__(self, prioridad)

    def mostrar_detalles(self):
        self.mostrar_informacion()
        self.mostrar_prioridad()


class TicketHardware(TicketSoporte):
    def resolver(self):
        print("Solución: revisar componentes físicos")

    def mostrar_detalles(self):
        super().mostrar_detalles()
        self.resolver()
        print("Incidencia registrada")


class TicketSoftware(TicketSoporte):
    def resolver(self):
        print("Solución: comprobar y actualizar la aplicación")

    def mostrar_detalles(self):
        super().mostrar_detalles()
        self.resolver()
        print("Incidencia registrada")


class TicketRedes(TicketSoporte):
    def resolver(self):
        print("Solución: verificar la conexión de red")

    def mostrar_detalles(self):
        super().mostrar_detalles()
        self.resolver()
        print("Incidencia registrada")


class TicketSeguridad(TicketSoporte):
    def resolver(self):
        print("Solución: comprobar accesos y cambiar credenciales")

    def mostrar_detalles(self):
        super().mostrar_detalles()
        self.resolver()
        print("Incidencia registrada")


def atender_incidencia(ticket):
    print("-----------------------------")
    ticket.mostrar_detalles()


# Creación de objetos originales + ampliación
tickets = [
    TicketHardware(101, "Ana", "El ordenador no enciende", "alta"),
    TicketSoftware(102, "Luis", "La aplicación se bloquea", "media"),
    TicketRedes(103, "Marta", "No hay conexión a Internet", "alta"),
    TicketSoftware(104, "Pedro", "No puedo actualizar el programa", "baja"),
    TicketSeguridad(105, "Sara", "Se ha detectado un acceso sospechoso", "alta")
]

for t in tickets:
    atender_incidencia(t)
