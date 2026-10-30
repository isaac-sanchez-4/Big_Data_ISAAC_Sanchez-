"""El equipo de plataforma necesita que todos los eventos de log de sus *pipelines* se muestren con un **formato homogéneo**, sin tener que repetir el formato en cada `print`. Crea una clase `EventoLog` que defina cómo se representa cada evento mediante los métodos especiales `__str__` y `__repr__`.

El constructor debe recibir los parámetros obligatorios `timestamp`, `nivel`, `servicio` y `mensaje`, y guardarlos como atributos de instancia.

Además, la clase debe tener dos **métodos especiales**:

- `__str__()`: devuelve una línea de log con el formato `<timestamp> [<nivel>] <servicio> | <mensaje>`, donde el nivel ocupa un ancho fijo de 5 caracteres y el servicio de 12, ambos alineados a la izquierda, para que todas las líneas queden en columna.
- `__repr__()`: devuelve una representación resumida con el formato `EventoLog('<timestamp>', '<nivel>', '<servicio>')`.

Después:

1. Crea una lista `eventos` con estos cuatro eventos:
    - `"2026-10-26 02:00:01"`, `"INFO"`, `"ingesta"`, `"Inicio de carga de ventas"`
    - `"2026-10-26 02:03:47"`, `"WARN"`, `"ingesta"`, `"Fichero tienda_12 llega vacío"`
    - `"2026-10-26 02:05:10"`, `"ERROR"`, `"transform"`, `"Columna 'importe' con texto no numérico"`
    - `"2026-10-26 02:09:33"`, `"INFO"`, `"carga"`, `"Lote publicado en zona curated"`
2. Recorre la lista con un bucle `for` y muestra cada evento con `print(evento)`.
3. Crea una lista `errores` que contenga solo los eventos de nivel `"ERROR"`, usando una *list comprehension* que filtre por el atributo `nivel`.
4. Muestra la lista `errores` con `print()`.

Observa la salida: ¿por qué las líneas del punto 2 y la lista del punto 4 se muestran con formatos distintos?"""
class EventoLog:
    def __init__(self, timestamp, nivel, servicio, mensaje):
        self.timestamp = timestamp
        self.nivel = nivel
        self.servicio = servicio
        self.mensaje = mensaje

    def __str__(self):
        return f"{self.timestamp} [{self.nivel:<5}]{self.servicio:<12} |{self.mensaje}"

    def __repr__(self):
        return f"EventoLog('{self.timestamp}', '{self.nivel}', '{self.servicio}')"

eventos = [
    EventoLog("2026-10-26 02:00:01", "INFO", "ingesta", "Inicio de carga de ventas"),
    EventoLog("2026-10-26 02:03:47", "WARN", "ingesta", "Fichero tienda_12 llega vacío"),
    EventoLog("2026-10-26 02:05:10", "ERROR", "transform", "Columna 'importe' con texto no numérico"),
    EventoLog("2026-10-26 02:09:33", "INFO", "carga", "Lote publicado en zona curated"),
]

for evento in eventos:
    print(evento)

errores = [e for e in eventos if e.nivel == "ERROR"]
print(errores)