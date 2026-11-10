# Ejemplo 1: Reproductores multimedia
class ReproductorMP3:
    def reproducir(self):
        return "Reproduciendo archivo de música MP3..."

class ReproductorVideo:
    def reproducir(self):
        return "Reproduciendo archivo de video MP4..."

def iniciar_reproduccion(dispositivo):
    print(dispositivo.reproducir())

mp3 = ReproductorMP3()
mp4 = ReproductorVideo()

iniciar_reproduccion(mp3)
iniciar_reproduccion(mp4)


# Ejemplo 2: Pasarela de pagos
class TarjetaCredito:
    def procesar_pago(self, cantidad):
        print(f"Pagando {cantidad}€ con Tarjeta de Crédito.")

class PayPal:
    def procesar_pago(self, cantidad):
        print(f"Pagando {cantidad}€ a través de cuenta PayPal.")

def realizar_checkout(metodo_pago, total):
    metodo_pago.procesar_pago(total)

realizar_checkout(TarjetaCredito(), 150)
realizar_checkout(PayPal(), 45.99)