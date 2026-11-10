class ArchivoDatos:
    def __init__(self, nombre, tamano):
        self.nombre = nombre
        self.tamano = tamano

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Tamaño: {self.tamano} MB")

    def procesar(self):
        print("Procesamiento genérico de archivo")


class ArchivoCSV(ArchivoDatos):
    def procesar(self):
        print(f"Procesando archivo CSV: {self.nombre}")
        print("Leyendo registros separados por comas...")


class ArchivoJSON(ArchivoDatos):
    def procesar(self):
        print(f"Procesando archivo JSON: {self.nombre}")
        print("Extrayendo propiedades de los objetos JSON...")


class ArchivoTXT(ArchivoDatos):
    def procesar(self):
        print(f"Procesando archivo TXT: {self.nombre}")
        print("Leyendo líneas y realizando limpieza básica...")


class ArchivoXML(ArchivoDatos):
    def procesar(self):
        print(f"Procesando archivo XML: {self.nombre}")
        print("Analizando etiquetas y atributos XML...")


def ejecutar_procesamiento(archivo):
    archivo.mostrar_informacion()
    archivo.procesar()
    print()


# Creación de objetos e inclusión de XML
archivos = [
    ArchivoCSV("ventas.csv", 15),
    ArchivoJSON("sensores.json", 8),
    ArchivoTXT("logs.txt", 25),
    ArchivoXML("configuracion.xml", 5)
]

for arch in archivos:
    ejecutar_procesamiento(arch)