class RecursoComputacional:
    def __init__(self, id_recurso, nombre, fabricante, potencia_w, horas_uso):
        self.id_recurso = id_recurso
        self.nombre = nombre
        self.fabricante = fabricante
        self.potencia_w = potencia_w
        self.horas_uso = horas_uso

    def mostrar_informacion(self):
        print(f"Recurso: {self.id_recurso} - {self.nombre}")
        print(f"Fabricante: {self.fabricante}")

    def calcular_consumo(self):
        return (self.potencia_w * self.horas_uso) / 1000


class Ordenador(RecursoComputacional):
    def __init__(self, id_recurso, nombre, fabricante, potencia_w, horas_uso, procesador, ram_gb, sistema_operativo):
        super().__init__(id_recurso, nombre, fabricante, potencia_w, horas_uso)
        self.procesador = procesador
        self.ram_gb = ram_gb
        self.sistema_operativo = sistema_operativo

    def mostrar_informacion(self):
        print("Tipo: Ordenador")
        super().mostrar_informacion()
        print(f"Procesador: {self.procesador}")
        print(f"RAM: {self.ram_gb} GB")
        print(f"Sistema operativo: {self.sistema_operativo}")


class Servidor(RecursoComputacional):
    def __init__(self, id_recurso, nombre, fabricante, potencia_w, horas_uso, num_cpu, ram_gb, almacenamiento_tb):
        super().__init__(id_recurso, nombre, fabricante, potencia_w, horas_uso)
        self.num_cpu = num_cpu
        self.ram_gb = ram_gb
        self.almacenamiento_tb = almacenamiento_tb

    def mostrar_informacion(self):
        print("Tipo: Servidor")
        super().mostrar_informacion()
        print(f"Número de CPU: {self.num_cpu}")
        print(f"RAM: {self.ram_gb} GB")
        print(f"Almacenamiento: {self.almacenamiento_tb} TB")


class DispositivoEdge(RecursoComputacional):
    def __init__(self, id_recurso, nombre, fabricante, potencia_w, horas_uso, modelo_gpu, memoria_gpu_gb, tipo_inferencia):
        super().__init__(id_recurso, nombre, fabricante, potencia_w, horas_uso)
        self.modelo_gpu = modelo_gpu
        self.memoria_gpu_gb = memoria_gpu_gb
        self.tipo_inferencia = tipo_inferencia

    def mostrar_informacion(self):
        print("Tipo: Dispositivo Edge")
        super().mostrar_informacion()
        print(f"Modelo GPU: {self.modelo_gpu}")
        print(f"Memoria GPU: {self.memoria_gpu_gb} GB")
        print(f"Tipo de inferencia: {self.tipo_inferencia}")


# Objetos
recursos = [
    Ordenador("PC-01", "Estación ML 1", "Dell", 250, 50, "Intel Core i7", 32, "Windows 11"),
    Ordenador("PC-02", "Estación ML 2", "HP", 200, 40, "AMD Ryzen 7", 32, "Ubuntu 22.04"),
    Servidor("SRV-01", "Node BigData 1", "HPE", 600, 70, 2, 128, 4),
    Servidor("SRV-02", "Node BigData 2", "Dell", 700, 60, 4, 256, 8),
    DispositivoEdge("EDGE-01", "Jetson Nano 1", "NVIDIA", 15, 100, "Maxwell", 4, "Computer Vision"),
    DispositivoEdge("EDGE-02", "Jetson AGX", "NVIDIA", 30, 80, "Volta", 32, "NLP")
]

print("========== LABORATORIO BIG DATA ==========\n")
consumo_total = 0
max_consumo = -1
dispositivo_mayor = None
contador_pc, contador_srv, contador_edge = 0, 0, 0

for r in recursos:
    r.mostrar_informacion()
    consumo = r.calcular_consumo()
    print(f"Consumo acumulado: {consumo:.1f} kWh\n")
    
    consumo_total += consumo
    if consumo > max_consumo:
        max_consumo = consumo
        dispositivo_mayor = r.id_recurso

    if isinstance(r, Ordenador):
        contador_pc += 1
    elif isinstance(r, Servidor):
        contador_srv += 1
    elif isinstance(r, DispositivoEdge):
        contador_edge += 1

print("========== RESUMEN DEL LABORATORIO ==========")
print(f"Ordenadores: {contador_pc}")
print(f"Servidores: {contador_srv}")
print(f"Dispositivos Edge: {contador_edge}")
print(f"\nConsumo total: {consumo_total:.1f} kWh")
print(f"Dispositivo de mayor consumo: {dispositivo_mayor}")