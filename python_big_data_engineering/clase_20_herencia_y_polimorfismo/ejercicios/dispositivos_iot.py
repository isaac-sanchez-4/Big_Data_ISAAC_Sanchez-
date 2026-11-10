class DispositivoIoT:
    def __init__(self, device_id, nombre, ubicacion, valor, unidad):
        self.device_id = device_id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.valor = valor
        self.unidad = unidad

    def mostrar_informacion(self):
        print(f"ID: {self.device_id}")
        print(f"Nombre: {self.nombre}")
        print(f"Ubicación: {self.ubicacion}")
        print(f"Valor: {self.valor} {self.unidad}")


class SensorHumedad(DispositivoIoT):
    def __init__(self, device_id, nombre, ubicacion, valor, unidad, profundidad, calibracion):
        super().__init__(device_id, nombre, ubicacion, valor, unidad)
        self.profundidad = profundidad
        self.calibracion = calibracion

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Profundidad: {self.profundidad} cm")
        print(f"Calibración: {self.calibracion}")
        print("Categoría: Sensor de humedad")


class SensorTemperatura(DispositivoIoT):
    def __init__(self, device_id, nombre, ubicacion, valor, unidad, altitud, precision):
        super().__init__(device_id, nombre, ubicacion, valor, unidad)
        self.altitud = altitud
        self.precision = precision

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Altitud: {self.altitud} m")
        print(f"Precisión: {self.precision} {self.unidad}")
        print("Categoría: Sensor de temperatura")


class SensorViento(DispositivoIoT):
    def __init__(self, device_id, nombre, ubicacion, valor, unidad, orientacion, velocidad_maxima):
        super().__init__(device_id, nombre, ubicacion, valor, unidad)
        self.orientacion = orientacion
        self.velocidad_maxima = velocidad_maxima

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Orientación: {self.orientacion}")
        print(f"Velocidad máxima: {self.velocidad_maxima} {self.unidad}")
        print("Categoría: Sensor de viento")


class SensorTanque(DispositivoIoT):
    def __init__(self, device_id, nombre, ubicacion, valor, unidad, capacidad, nivel_bateria):
        super().__init__(device_id, nombre, ubicacion, valor, unidad)
        self.capacidad = capacidad
        self.nivel_bateria = nivel_bateria

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"Capacidad: {self.capacidad} L")
        print(f"Nivel de batería: {self.nivel_bateria}%")
        print("Categoría: Sensor de tanque")


# Creación de objetos (2 por cada clase hija)
dispositivos = [
    SensorHumedad("DEV001", "Sensor suelo 1", "Parcela A", 45, "%", 30, "Automática"),
    SensorHumedad("DEV002", "Sensor suelo 2", "Parcela B", 50, "%", 25, "Manual"),
    SensorTemperatura("DEV003", "Sensor amb 1", "Parcela B", 26, "°C", 650, 0.5),
    SensorTemperatura("DEV004", "Sensor amb 2", "Parcela C", 22, "°C", 700, 0.2),
    SensorViento("DEV005", "Anemómetro 1", "Parcela C", 18, "km/h", "Norte", 80),
    SensorViento("DEV006", "Anemómetro 2", "Parcela A", 12, "km/h", "Sur", 65),
    SensorTanque("DEV007", "Tanque 1", "Parcela A", 75, "%", 5000, 90),
    SensorTanque("DEV008", "Tanque 2", "Parcela B", 40, "%", 3000, 45)
]

for d in dispositivos:
    d.mostrar_informacion()
    if isinstance(d, SensorHumedad):
        print("-> Alerta: Control de riego activo")
    print("-" * 40)

# Comprobación de vars() en el primer objeto
print("Atributos limpios de DEV001:", vars(dispositivos[0]))