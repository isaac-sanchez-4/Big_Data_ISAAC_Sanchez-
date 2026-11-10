class FranjaHoraria:
    def __init__(self, inicio, fin):
        self.__inicio_min = self._a_minutos(inicio)
        self.__fin_min = self._a_minutos(fin)
        self.inicio_str = inicio
        self.fin_str = fin

    def _a_minutos(self, texto):
        horas, minutos = map(int, texto.split(":"))
        return horas * 60 + minutos

    def __len__(self):
        return self.__fin_min - self.__inicio_min

    def __contains__(self, hora_texto):
        h_min = self._a_minutos(hora_texto)
        return self.__inicio_min <= h_min < self.__fin_min

    def solapa(self, otra):
        return max(self.__inicio_min, otra.__inicio_min) < min(self.__fin_min, otra.__fin_min)

    def __lt__(self, otra):
        return self.__inicio_min < otra.__inicio_min

    def __str__(self):
        return f"{self.inicio_str}-{self.fin_str}"


class Sala:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.__reservas = []

    def reservar(self, inicio, fin, responsable, asistentes):
        if asistentes > self.capacidad:
            return "RECHAZADA: aforo"
        
        nueva_franja = FranjaHoraria(inicio, fin)
        for franja, resp, asis in self.__reservas:
            if nueva_franja.solapa(franja):
                return f"RECHAZADA: solapa con {franja} ({resp})"
        
        self.__reservas.append((nueva_franja, responsable, asistentes))
        self.__reservas.sort(key=lambda x: x[0])
        return f"OK {nueva_franja}"

    def ocupada_a(self, hora):
        for franja, resp, asis in self.__reservas:
            if hora in franja:
                return resp
        return None

    def ocupacion(self, jornada_min=600):
        total_minutos_reservados = sum(len(franja) for franja, resp, asis in self.__reservas)
        pct = (total_minutos_reservados / jornada_min) * 100
        return round(pct, 1)

    def agenda(self):
        lineas = []
        for franja, resp, asis in self.__reservas:
            lineas.append(f"{franja} · {resp} ({asis} pers.)")
        return "\n".join(lineas)


# Código de prueba
sala = Sala("Atlas", 8)
print(sala.reservar("10:00", "11:30", "Ana", 6))
print(sala.reservar("09:00", "10:00", "Luis", 4))
print(sala.reservar("11:00", "12:00", "Marta", 5))
print(sala.reservar("12:00", "12:45", "Iker", 12))
print(sala.reservar("15:15", "16:00", "Iker", 7))
print(sala.agenda())
print(sala.ocupada_a("10:59"), sala.ocupada_a("11:30"), sala.ocupada_a("15:15"))
print("Ocupación:", sala.ocupacion(), "%")
f = FranjaHoraria("08:45", "09:20")
print(f, len(f), "09:20" in f)