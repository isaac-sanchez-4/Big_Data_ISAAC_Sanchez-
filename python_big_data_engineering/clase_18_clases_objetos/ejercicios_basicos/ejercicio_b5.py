class Climatizador:
    TEMP_MIN = 18
    TEMP_MAX = 27

    def __init__(self, sala, consigna_inicial):
        self.sala = sala
        self.__consigna = self._limitar(consigna_inicial)
        self._historial = [self.__consigna]

    def _limitar(self, valor):
        if valor < Climatizador.TEMP_MIN:
            return Climatizador.TEMP_MIN
        if valor > Climatizador.TEMP_MAX:
            return Climatizador.TEMP_MAX
        return valor

    def ajustar(self, grados):
        nueva = self._limitar(self.__consigna + grados)
        self.__consigna = nueva
        self._historial.append(nueva)
        return nueva

    def consigna(self):
        return self.__consigna

    def __str__(self):
        cambios = len(self._historial) - 1
        return f"Sala {self.sala} · {self.__consigna} °C · {cambios} cambios"


# Código de prueba
sala_a = Climatizador("A", 22)
sala_b = Climatizador("B", 31)
print(sala_a.ajustar(-3), sala_a.ajustar(-4), sala_a.ajustar(6))
print(sala_a)
print(sala_b)
print(sala_a._historial)
print(vars(sala_b))
print(hasattr(sala_a, "__consigna"), hasattr(sala_a, "_Climatizador__consigna"))

