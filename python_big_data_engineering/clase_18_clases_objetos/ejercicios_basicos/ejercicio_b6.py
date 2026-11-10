class PesoEnvio:
    def __init__(self, gramos):
        self.gramos = gramos if gramos > 0 else 0

    def __add__(self, otro):
        return PesoEnvio(self.gramos + otro.gramos)

    def __eq__(self, otro):
        return self.gramos == otro.gramos

    def __lt__(self, otro):
        return self.gramos < otro.gramos

    def __str__(self):
        if self.gramos >= 1000:
            return f"{self.gramos / 1000:.2f} kg"
        return f"{self.gramos} g"

    def __repr__(self):
        return f"PesoEnvio({self.gramos})"


# Código de prueba
paquetes = [PesoEnvio(850), PesoEnvio(1250), PesoEnvio(400), PesoEnvio(-30), PesoEnvio(2300)]
print(paquetes[0] + paquetes[2])
print(paquetes[0] + paquetes[1])
pale = PesoEnvio(0)
for p in paquetes:
    pale = pale + p
print("Palé:", pale)
print(sorted(paquetes))
print("Más pesado:", max(paquetes))
print(PesoEnvio(1250) == paquetes[1], PesoEnvio(1250) is paquetes[1])