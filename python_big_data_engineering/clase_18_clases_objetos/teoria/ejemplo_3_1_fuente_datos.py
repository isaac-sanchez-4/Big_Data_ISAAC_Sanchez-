# El equipo de datos quiere registrar las fuentes de las que se alimenta su *data lake*. Crea una clase `FuenteDatos` cuyo constructor reciba tres **parámetros obligatorios** y los guarde como atributos del objeto:
#
# - `nombre`: identificador de la fuente.
# - `tipo`: forma de acceso a los datos (por ejemplo, `"api"` o `"fichero"`).
# - `ubicacion`: URL o ruta donde se encuentran los datos.
#
# Después, crea dos fuentes:
#
# - `crm`: `"crm_clientes"`, de tipo `"api"`, ubicada en `"https://api.crm.empresa.com/v2"`.
# - `erp`: `"erp_facturas"`, de tipo `"fichero"`, ubicada en `"/landing/erp/facturas/"`.
#
# Por último:
#
# 1. Muestra el nombre, tipo y ubicación de cada fuente en una línea, separados por `|`.
# 2. Usa la función `vars()` sobre `erp` para mostrar todos sus atributos en forma de diccionario.

class FuenteDatos:
    def __init__(self, nombre, tipo, ubicacion):
        self.nombre = nombre
        self.tipo = tipo
        self.ubicacion = ubicacion

crm = FuenteDatos("crm_clientes", "api", "https://api.crm.empresa.com/v2")
erp = FuenteDatos("erp_facturas", "fichero", "/landing/erp/facturas/")

print(crm.nombre, "|", crm.tipo, "|", crm.ubicacion)
print(erp.nombre, "|", erp.tipo, "|", erp.ubicacion)
print(vars(erp))