"""Una cadena logística monitoriza la temperatura de sus almacenes mediante sensores. Crea una clase `Sensor` que combine **atributos de clase**, compartidos por todos los sensores, con **atributos de instancia**, propios de cada uno.

La clase debe definir, **fuera del constructor**, dos atributos de clase:

- `unidad`, con el valor `"°C"`: es la misma para todos los sensores.
- `total_sensores`, con el valor `0`: servirá para contar cuántos sensores se han creado.

El constructor debe recibir los parámetros obligatorios `codigo` y `ubicacion`, guardarlos como atributos de instancia e **incrementar en 1** el contador `total_sensores` de la clase cada vez que se cree un sensor.

Además, la clase debe tener el método `describir(valor)`, que devuelva un texto con el formato `<codigo> (<ubicacion>):<valor><unidad>`.

Después:

1. Crea tres sensores:
    - `s1`: `"TMP-01"` en `"Cámara frigorífica A"`.
    - `s2`: `"TMP-02"` en `"Cámara frigorífica B"`.
    - `s3`: `"TMP-03"` en `"Muelle de carga"`.
2. Muestra la descripción de `s1` con una lectura de `18.4` y la de `s3` con una lectura de `12.1`.
3. Muestra el número de sensores registrados accediendo al contador **desde la clase**: `Sensor.total_sensores`.
4. Muestra de nuevo el contador, pero esta vez accediendo **desde un objeto**: `s2.total_sensores`.

Reflexiona: ¿por qué en el constructor se incrementa `Sensor.total_sensores` y no `self.total_sensores`? ¿Por qué `self.unidad` funciona dentro de `describir` si `unidad` nunca se asignó al objeto?"""
class Sensor:
    unidad = "°C"
    total_sensores = 0

    def __init__(self, codigo, ubicacion):
        self.codigo = codigo
        self.ubicacion = ubicacion
        Sensor.total_sensores += 1

    def describir(self, valor):
        return f"{self.codigo} ({self.ubicacion}):{valor}{self.unidad}"

s1 = Sensor("TMP-01", "Cámara frigorífica A")
s2 = Sensor("TMP-02", "Cámara frigorífica B")
s3 = Sensor("TMP-03", "Muelle de carga")

print(s1.describir(-18.4))
print(s3.describir(12.1))
print("Sensores registrados:", Sensor.total_sensores)
print(s2.total_sensores)