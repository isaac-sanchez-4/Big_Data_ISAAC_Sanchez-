class CuotaEquipo:
    peticiones_rechazadas = 0

    def __init__(self, equipo, limite_tokens):
        self.equipo = equipo
        self.limite_tokens = limite_tokens
        self.__consumos = []

    def consumido(self):
        return sum(tokens for caso, tokens in self.__consumos)

    def restante(self):
        return self.limite_tokens - self.consumido()

    def registrar(self, caso_uso, tokens):
        if tokens <= self.restante():
            self.__consumos.append((caso_uso, tokens))
            return True
        else:
            CuotaEquipo.peticiones_rechazadas += 1
            return False

    def porcentaje(self):
        if self.limite_tokens == 0:
            return 0.0
        return round((self.consumido() / self.limite_tokens) * 100, 1)

    def top_caso_uso(self):
        if not self.__consumos:
            return None
        totales_por_caso = {}
        for caso, tokens in self.__consumos:
            totales_por_caso[caso] = totales_por_caso.get(caso, 0) + tokens
        return max(totales_por_caso, key=totales_por_caso.get)

    def __bool__(self):
        return self.restante() > 0

    def __lt__(self, otro):
        return self.porcentaje() < otro.porcentaje()

    def __str__(self):
        pct = self.porcentaje()
        bloques_llenos = int(pct // 10)
        barra = "#" * bloques_llenos + "." * (10 - bloques_llenos)
        return f"{self.equipo:<10} [{barra}] {pct:.1f} %"


# Código de prueba
marketing = CuotaEquipo("Marketing", 50_000)
legal = CuotaEquipo("Legal", 20_000)
soporte = CuotaEquipo("Soporte", 80_000)
marketing.registrar("copys campaña", 18_000)
marketing.registrar("traducciones", 9_000)
marketing.registrar("copys campaña", 5_000)
legal.registrar("resumen contratos", 15_000)
print(legal.registrar("resumen contratos", 6_000))
print(legal.registrar("cláusulas", 5_000))
soporte.registrar("respuestas tickets", 12_000)
panel = sorted([marketing, legal, soporte])
panel.reverse()
for cuota in panel:
    print(cuota)
print("Restante Legal:", legal.restante(), "| ¿Puede seguir?", bool(legal))
print("Top Marketing:", marketing.top_caso_uso())
print("Rechazadas en total:", CuotaEquipo.peticiones_rechazadas)
print(CuotaEquipo("I+D", 10_000).top_caso_uso())