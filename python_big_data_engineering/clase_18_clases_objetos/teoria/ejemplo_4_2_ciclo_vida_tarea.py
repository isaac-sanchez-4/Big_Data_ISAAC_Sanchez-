"""Una tarea de ingesta pasa por distintos estados a lo largo de su vida: `"pendiente"` → `"en_ejecucion"` → `"completada"`. Crea una clase `TareaIngesta` cuyos **métodos protejan sus propias reglas**, de forma que la tarea no permita acciones que no correspondan a su estado actual.

El constructor debe recibir el parámetro obligatorio `nombre` y crear dos atributos de estado con valor inicial fijo:

- `estado`, con el valor `"pendiente"`.
- `filas_cargadas`, con el valor `0`.

La clase debe tener tres **métodos**:

- `iniciar()`: solo puede ejecutarse si la tarea está `"pendiente"`. En ese caso, cambia el estado a `"en_ejecucion"` y muestra `[nombre] Iniciada`. Si no, muestra `[nombre] No se puede iniciar: estado actual '<estado>'` y no cambia nada.
- `cargar(filas)`: solo puede ejecutarse si la tarea está `"en_ejecucion"`. En ese caso, suma `filas` a `filas_cargadas` y muestra `[nombre] +<filas> filas (acumulado:<filas_cargadas>)`. Si no, muestra `[nombre] Carga rechazada: la tarea no está en ejecución` y no suma nada.
- `finalizar()`: si la tarea está `"en_ejecucion"`, cambia el estado a `"completada"`. En cualquier caso, muestra `[nombre] Estado final:<estado> con<filas_cargadas> filas`.

Después, crea una tarea llamada `"ventas_diarias"` y ejecuta, **en este orden**, las siguientes llamadas:

1. `cargar(500)`
2. `iniciar()`
3. `cargar(12000)`
4. `cargar(8500)`
5. `iniciar()`
6. `finalizar()`

Antes de ejecutar el código, intenta predecir qué mensaje mostrará cada llamada. ¿Cuántas filas se habrán cargado al final? ¿Por qué no cuentan las 500 de la primera llamada?"""
class TareaIngesta:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "pendiente"
        self.filas_cargadas = 0

    def iniciar(self):
        if self.estado != "pendiente":
            print(f"[{self.nombre}] No se puede iniciar: estado actual '{self.estado}'")
            return
        self.estado = "en_ejecucion"
        print(f"[{self.nombre}] Iniciada")

    def cargar(self, filas):
        if self.estado != "en_ejecucion":
            print(f"[{self.nombre}] Carga rechazada: la tarea no está en ejecución")
            return
        self.filas_cargadas += filas
        print(f"[{self.nombre}] +{filas} filas (acumulado:{self.filas_cargadas})")

    def finalizar(self):
        if self.estado == "en_ejecucion":
            self.estado = "completada"
        print(f"[{self.nombre}] Estado final:{self.estado} con{self.filas_cargadas} filas")

tarea = TareaIngesta("ventas_diarias")
tarea.cargar(500)
tarea.iniciar()
tarea.cargar(12000)
tarea.cargar(8500)
tarea.iniciar()
tarea.finalizar()