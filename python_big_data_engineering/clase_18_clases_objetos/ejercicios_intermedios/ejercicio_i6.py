class Precio:
    TASAS_A_EUR = {"EUR": 1.0, "USD": 0.92, "GBP": 1.17}

    def __init__(self, cantidad, divisa="EUR"):
        self.cantidad = round(cantidad, 2)
        self.divisa = divisa

    def en_euros(self):
        return self.cantidad * Precio.TASAS_A_EUR[self.divisa]

    def convertir_a(self, nueva_divisa):
        valor_euros = self.en_euros()
        nueva_cantidad = valor_euros / Precio.TASAS_A_EUR[nueva_divisa]
        return Precio(round(nueva_cantidad, 2), nueva_divisa)

    def __add__(self, otro):


        euros_propios = self.en_euros()
        euros_otro = otro.en_euros()
        total_euros = euros_propios + euros_otro
        cantidad_en_divisa_1 = total_euros / Precio.TASAS_A_EUR[self.divisa]
        return Precio(round(cantidad_en_divisa_1, 2), self.divisa)

    def __mul__(self, factor):
        return Precio(round(self.cantidad * factor, 2), self.divisa)

    def __eq__(self, otro):
        return round(self.en_euros(), 2) == round(otro.en_euros(), 2)

    def __lt__(self, otro):
        return self.en_euros() < otro.en_euros()

    def __float__(self):
        return round(self.en_euros(), 2)

    @classmethod
    def actualizar_tasa(cls, divisa, tasa):
        cls.TASAS_A_EUR[divisa] = tasa

    def __str__(self):
        return f"{self.cantidad:.2f} {self.divisa}"

    def __repr__(self):
        return f"Precio({self.cantidad}, '{self.divisa}')"


# Código de prueba
auriculares = Precio(59.90)
cable = Precio(12.50, "USD")
funda = Precio(15, "GBP")
print(auriculares + cable)
print(cable + auriculares)
print(funda.convertir_a("EUR"), funda.convertir_a("USD"))
print(cable * 3)
print(Precio(9.20) == Precio(10, "USD"), Precio(9.20) is Precio(10, "USD"))
catalogo = [auriculares, cable, funda]
print("Más barato:", min(catalogo), "| Más caro:", max(catalogo))
print("Total en EUR:", round(sum([float(p) for p in catalogo]), 2))
Precio.actualizar_tasa("USD", 0.95)
print(cable.convertir_a("EUR"), float(cable))

