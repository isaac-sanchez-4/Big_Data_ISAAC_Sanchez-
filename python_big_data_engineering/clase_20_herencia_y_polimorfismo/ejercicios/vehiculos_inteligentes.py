class Vehiculo:
    def __init__(self, matricula, modelo, **kwargs):
        self.matricula = matricula
        self.modelo = modelo
        super().__init__(**kwargs)

    def mostrar_informacion(self):
        print(f"Matrícula: {self.matricula}")
        print(f"Modelo: {self.modelo}")


class SistemaGPS:
    def __init__(self, latitud, longitud, **kwargs):
        self.latitud = latitud
        self.longitud = longitud
        super().__init__(**kwargs)

    def mostrar_ubicacion(self):
        print(f"Latitud: {self.latitud}")
        print(f"Longitud: {self.longitud}")


class SistemaConectividad:
    def __init__(self, direccion_ip, conectado, **kwargs):
        self.direccion_ip = direccion_ip
        self.conectado = conectado
        super().__init__(**kwargs)

    def mostrar_conexion(self):
        print(f"Dirección IP: {self.direccion_ip}")
        estado = "Conectado" if self.conectado else "Desconectado"
        print(f"Estado: {estado}")


class SistemaDiagnostico:
    def __init__(self, nivel_bateria, temperatura_motor, **kwargs):
        self.nivel_bateria = nivel_bateria
        self.temperatura_motor = temperatura_motor
        super().__init__(**kwargs)

    def mostrar_diagnostico(self):
        print(f"Nivel de batería: {self.nivel_bateria}%")
        print(f"Temperatura del motor: {self.temperatura_motor} °C")


class VehiculoInteligente(Vehiculo, SistemaGPS, SistemaConectividad, SistemaDiagnostico):
    def __init__(self, identificador_flota, **kwargs):
        self.identificador_flota = identificador_flota
        super().__init__(**kwargs)

    def mostrar_estado_completo(self):
        print("====================================")
        print("    ESTADO DEL VEHÍCULO INTELIGENTE")
        print("====================================\n")
        print(f"Identificador: {self.identificador_flota}\n")
        print("--- INFORMACIÓN DEL VEHÍCULO ---")
        self.mostrar_informacion()
        print("\n--- SISTEMA GPS ---")
        self.mostrar_ubicacion()
        print("\n--- CONECTIVIDAD ---")
        self.mostrar_conexion()
        print("\n--- DIAGNÓSTICO ---")
        self.mostrar_diagnostico()

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Identificador de flota: {self.identificador_flota}")


# Creación de objetos
vehiculo1 = VehiculoInteligente(
    identificador_flota="FLT-001",
    matricula="1234-ABC",
    modelo="Tesla Model 3",
    latitud=40.4168,
    longitud=-3.7038,
    direccion_ip="192.168.1.10",
    conectado=True,
    nivel_bateria=85,
    temperatura_motor=45
)

vehiculo2 = VehiculoInteligente(
    identificador_flota="FLT-002",
    matricula="5678-DEF",
    modelo="Mercedes eSprinter",
    latitud=41.3874,
    longitud=2.1686,
    direccion_ip="192.168.1.11",
    conectado=False,
    nivel_bateria=42,
    temperatura_motor=65
)

# Pruebas de métodos
vehiculo1.mostrar_estado_completo()
print("\n" + "="*40 + "\n")
vehiculo1.mostrar_informacion()

# Comprobación del MRO
print("\nMRO:", VehiculoInteligente.__mro__)