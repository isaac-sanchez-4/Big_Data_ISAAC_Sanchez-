"""Un equipo de calidad de datos define un **umbral máximo de nulos** que se aplica por defecto a todas las columnas, aunque algunas columnas concretas pueden tolerar más. En este ejercicio vas a comprobar qué ocurre cuando un objeto **"tapa"** un atributo de clase con uno propio.

Crea una clase `ReglaCalidad` con:

- Un **atributo de clase** `umbral_nulos` con el valor `0.05` (5 %).
- Un constructor que reciba el parámetro obligatorio `columna` y lo guarde como atributo de instancia.
- Un método `evaluar(nulos, total)` que:
    - Calcule el porcentaje de nulos como `nulos / total`.
    - Devuelva `"OK"` si ese porcentaje es menor o igual que `self.umbral_nulos`, y `"FALLO"` en caso contrario.
    - Devuelva un texto con el formato `<columna>:<porcentaje> nulos (umbral<umbral>) -><resultado>`, mostrando el porcentaje con un decimal y el umbral sin decimales.

Después:

1. Crea dos reglas: `r_email` para la columna `"email"` y `r_telefono` para la columna `"telefono"`.
2. Asigna **solo a `r_telefono`** un umbral propio de `0.20`, usando `r_telefono.umbral_nulos = 0.20`.
3. Evalúa `r_email` con 80 nulos sobre 1000 registros y `r_telefono` con 150 nulos sobre 1000 registros.
4. Muestra los atributos de cada objeto con `vars()`.
5. Cambia el umbral **en la clase** a `0.10`, usando `ReglaCalidad.umbral_nulos = 0.10`.
6. Vuelve a evaluar ambas reglas con los mismos datos del punto 3.

Antes de ejecutar, intenta predecir los resultados. Fíjate en la salida de `vars()`: ¿qué objeto tiene `umbral_nulos` como atributo propio? ¿Por qué el cambio del punto 5 afecta a una regla y no a la otra?"""
class ReglaCalidad:
    umbral_nulos = 0.05

    def __init__(self, columna):
        self.columna = columna

    def evaluar(self, nulos, total):
        ratio = nulos / total
        resultado = "OK" if ratio <= self.umbral_nulos else "FALLO"
        return f"{self.columna}:{ratio:.1%} nulos (umbral{self.umbral_nulos:.0%}) ->{resultado}"

r_email = ReglaCalidad("email")
r_telefono = ReglaCalidad("telefono")
r_telefono.umbral_nulos = 0.20

print(r_email.evaluar(80, 1000))
print(r_telefono.evaluar(150, 1000))
print(vars(r_email))
print(vars(r_telefono))

ReglaCalidad.umbral_nulos = 0.10
print(r_email.evaluar(80, 1000))
print(r_telefono.evaluar(150, 1000))