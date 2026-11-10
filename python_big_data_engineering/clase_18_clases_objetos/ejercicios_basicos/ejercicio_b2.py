class ConexionBD:
    MAX_CONEXIONES = 3
    abiertas = 0

    def __init__(self, servidor):
        self.servidor = servidor
        self.activa = False

    def abrir(self):
        if self.activa:
            return "ya estaba abierta"
        if ConexionBD.abiertas >= ConexionBD.MAX_CONEXIONES:
            return "rechazada: límite alcanzado"
        
        self.activa = True
        ConexionBD.abiertas += 1
        return "abierta"

    def cerrar(self):
        if self.activa:
            self.activa = False
            ConexionBD.abiertas -= 1
            return "cerrada"
        return "no estaba abierta"

    @classmethod
    def estado_pool(cls):
        return f"{cls.abiertas}/{cls.MAX_CONEXIONES} conexiones en uso"


# Código de prueba
etl_ventas = ConexionBD("pg-prod-01")
etl_stock = ConexionBD("pg-prod-01")
etl_crm = ConexionBD("pg-prod-01")
etl_logs = ConexionBD("pg-prod-01")
print(etl_ventas.abrir(), "|", etl_stock.abrir(), "|", etl_crm.abrir())
print(etl_logs.abrir())
print(etl_ventas.abrir())
print(ConexionBD.estado_pool())
print(etl_stock.cerrar())
print(etl_logs.abrir())
print(etl_stock.cerrar())
print(ConexionBD.estado_pool())