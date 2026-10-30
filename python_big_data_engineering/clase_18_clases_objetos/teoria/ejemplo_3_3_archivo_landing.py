"""
Cuando llega un fichero a la zona *landing*, el equipo de datos necesita extraer automáticamente información derivada de su ruta y su tamaño.

> La **zona *landing*** (zona de aterrizaje o de llegada) es el primer área de almacenamiento de un *data lake* o de una plataforma de datos: el lugar donde se depositan los ficheros **tal como llegan de los sistemas de origen**, sin transformar ni validar.
>

Crea una clase `ArchivoLanding` cuyo constructor reciba dos **parámetros obligatorios**:

- `ruta`: ruta completa del fichero.
- `tamano_bytes`: tamaño del fichero en bytes.

Además de guardar ambos valores, el constructor debe crear cuatro **atributos calculados** a partir de ellos, sin recibirlos como parámetro:

- `nombre`: el nombre del fichero, es decir, la última parte de la ruta tras la última `/`.
- `extension`: la extensión del fichero, obtenida a partir de `nombre` y convertida a minúsculas.
- `tamano_mb`: el tamaño en megabytes, redondeado a 2 decimales (1 MB = 1024 × 1024 bytes).
- `es_grande`: `True` si el fichero supera los 100 MB y `False` en caso contrario.

Ten en cuenta que algunos atributos dependen de otros, así que piensa en qué orden debes crearlos.

Después, crea un objeto `archivo` con la ruta `"/landing/ventas/2026/10/ventas_tienda_07.CSV"` y un tamaño de `157_286_400` bytes, y muestra por pantalla su nombre, extensión, tamaño en MB y si es grande.
"""
class ArchivoLanding:
    def __init__(self, ruta, tamano_bytes):
        self.ruta = ruta
        self.tamano_bytes = tamano_bytes
        self.nombre = ruta.split("/")[-1]
        self.extension = self.nombre.split(".")[-1].lower()
        self.tamano_mb = round(tamano_bytes / (1024 * 1024), 2)
        self.es_grande = self.tamano_mb > 100

archivo = ArchivoLanding("/landing/ventas/2026/10/ventas_tienda_07.CSV", 157_286_400)

print(archivo.nombre)
print(archivo.extension)
print(archivo.tamano_mb)
print(archivo.es_grande)