class PlantillaPrompt:
    def __init__(self, rol, tarea, formato_salida="texto libre"):
        self.rol = rol
        self.tarea = tarea
        self.formato_salida = formato_salida
        self.restricciones = []

    def agregar_restriccion(self, texto):
        self.restricciones.append(texto)

    def construir(self, entrada):
        lineas = [
            f"Actúa como {self.rol}.",
            f"Tarea: {self.tarea}"
        ]
        if self.restricciones:
            lineas.append("Restricciones:")
            for r in self.restricciones:
                lineas.append(f"- {r}")
        lineas.append(f"Formato de salida: {self.formato_salida}")
        lineas.append(f'Entrada: """{entrada}"""')
        return "\n".join(lineas)

    def __repr__(self):
        return f"PlantillaPrompt(rol='{self.rol}', restricciones={len(self.restricciones)})"


# Código de prueba
clasificador = PlantillaPrompt(
    "analista de experiencia de cliente",
    "clasifica el sentimiento de la reseña como POSITIVO, NEUTRO o NEGATIVO",
    "JSON con las claves sentimiento y motivo",
)
clasificador.agregar_restriccion("No inventes información que no aparezca en la reseña")
clasificador.agregar_restriccion("El motivo debe tener como máximo 15 palabras")
print(repr(clasificador))
print(clasificador.construir("El portátil llegó en 24 h pero la batería dura la mitad de lo anunciado."))
print("---")
resumen = PlantillaPrompt("redactor técnico", "resume la incidencia en una frase")
print(resumen.construir("El TPV de la tienda 14 no imprime tickets desde las 10:00."))