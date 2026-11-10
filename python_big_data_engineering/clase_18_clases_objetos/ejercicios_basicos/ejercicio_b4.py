class LlamadaLLM:
    PRECIOS = {
        "modelo-lite": (0.20, 0.80),
        "modelo-pro": (3.00, 12.00)
    }
    total_llamadas = 0

    def __init__(self, modelo, tokens_entrada, tokens_salida):
        self.modelo = modelo
        self.tokens_entrada = tokens_entrada
        self.tokens_salida = tokens_salida
        LlamadaLLM.total_llamadas += 1

    def tokens_totales(self):
        return self.tokens_entrada + self.tokens_salida

    def coste(self):
        precio_ent, precio_sal = LlamadaLLM.PRECIOS[self.modelo]
        coste_ent = (self.tokens_entrada / 1_000_000) * precio_ent
        coste_sal = (self.tokens_salida / 1_000_000) * precio_sal
        return round(coste_ent + coste_sal, 6)

    def __repr__(self):
        return f"LlamadaLLM({self.modelo}, {self.tokens_totales()} tokens, ${self.coste():g})"


# Código de prueba
llamadas = [
    LlamadaLLM("modelo-lite", 1200, 300),
    LlamadaLLM("modelo-pro", 1200, 300),
    LlamadaLLM("modelo-lite", 8000, 1500),
    LlamadaLLM("modelo-pro", 25000, 4000),
]
for llamada in llamadas:
    print(llamada)
print("Llamadas registradas:", LlamadaLLM.total_llamadas)
print(f"Coste total: ${round(sum([l.coste() for l in llamadas]), 6)}")
coste_pro = sum([l.coste() for l in llamadas if l.modelo == "modelo-pro"])
print("Peso de modelo-pro:", round(100 * coste_pro / sum([l.coste() for l in llamadas]), 1), "%")