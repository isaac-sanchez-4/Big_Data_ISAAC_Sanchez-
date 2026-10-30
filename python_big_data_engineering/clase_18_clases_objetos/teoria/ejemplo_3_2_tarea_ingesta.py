# Crea una clase `TareaIngesta` que represente una tarea de carga de datos. El constructor debe recibir:
#
# - `nombre` y `origen` como **parámetros obligatorios**.
# - `formato` y `reintentos_max` como **parámetros opcionales**, con valores por defecto `"csv"` y `3`.
#
# Además, el constructor debe crear dos **atributos de estado** que **no se reciben como parámetro** y que toda tarea nueva tiene con el mismo valor inicial:
#
# - `estado`, con el valor `"pendiente"`.
# - `filas_cargadas`, con el valor `0`.
#
# Después, crea dos tareas:
#
# - `t1`: `"ventas_diarias"` desde `"sftp_tiendas"`, usando los valores por defecto.
# - `t2`: `"clics_web"` desde `"blob_logs"`, con formato `"json"` y `5` reintentos.
#
# Por último, recorre ambas tareas con un bucle `for` y muestra en una línea por tarea su nombre, formato, reintentos, estado y filas cargadas, alineando las columnas como en la salida esperada.

class TareaIngesta:
    def __init__(self, nombre, origen, formato="csv", reintentos_max=3):
        self.nombre = nombre
        self.origen = origen
        self.formato = formato
        self.reintentos_max = reintentos_max
        self.estado = "pendiente"
        self.filas_cargadas = 0

t1 = TareaIngesta("ventas_diarias", "sftp_tiendas")
t2 = TareaIngesta("clics_web", "blob_logs", formato="json", reintentos_max=5)

for tarea in [t1, t2]:
    print(f"{tarea.nombre:<15} formato={tarea.formato:<5} reintentos={tarea.reintentos_max} "
          f"estado={tarea.estado} filas={tarea.filas_cargadas}")