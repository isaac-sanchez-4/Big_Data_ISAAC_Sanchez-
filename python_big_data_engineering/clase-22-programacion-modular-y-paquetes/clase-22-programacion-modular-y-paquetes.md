# 📋Clase 22 - Programación modular y paquetes

# Sesión 1:  Programación modular

> En las clases 18, 19 y 20 se trabajó la **programación orientada a objetos** y en la Clase 21 la **programación funcional**. Todos los ejemplos cabían en un solo archivo.
Los programas reales, en cambio, tienen miles de líneas, los escriben varias personas y reutilizan código entre proyectos. Esta clase enseña a **repartir un programa en varios archivos y carpetas** que se importan entre sí: la **programación modular**.

---

![Imagen](images/clase-22-programacion-modular-y-paquetes/image-001.png)

---

## Sección 1. ¿Qué es la programación modular?

### Definición

> La **programación modular** consiste en dividir un programa en **piezas independientes**, llamadas **módulos**, cada una responsable de **una tarea concreta**. Las piezas se conectan entre sí **importándose**.

---

| Término | Significado en Python |
| --- | --- |
| **Módulo** | Un archivo `.py`. Su nombre es el del archivo sin la extensión: `tarifas.py` es el módulo `tarifas` |
| **Importar** | Pedirle a Python que cargue un módulo para usar lo que contiene (variables, funciones, clases) |
| **Paquete** | Una carpeta que agrupa varios módulos relacionados (Sección 7) |
| **Biblioteca** o **librería** | Conjunto de módulos y paquetes listos para usar: la **biblioteca estándar** viene con Python; las **externas** se instalan con `pip` |
| **Espacio de nombres** | El «apellido» de cada nombre: `tarifas.coste_envio` y `aduanas.coste_envio` son dos funciones distintas aunque se llamen igual |

---

> Las tres piezas encajan unas dentro de otras: una **librería** contiene **paquetes**, y cada paquete contiene **módulos**.

![Imagen](images/clase-22-programacion-modular-y-paquetes/image-002.png)

---

> Cuando se desarrolla un programa en Python, normalmente se reparte en varios archivos: algunos se convierten en **módulos**, otros se agrupan en **paquetes** y uno de ellos es el **punto de entrada** (*entry point*) o **programa principal** (*main*). Es buena práctica llamar `main.py` a ese archivo.

---

> Ventajas de dividir el programa en módulos:
1. **Reutilización**: una función escrita una vez en un módulo se importa en todos los programas que la necesiten.
2. **Mantenimiento**: si cambia una regla (por ejemplo, una tarifa), se modifica en **un solo sitio**.
3. **Legibilidad**: archivos cortos, cada uno con un propósito claro.
4. **Trabajo en equipo**: cada persona trabaja en un módulo sin pisar el código de las demás.
5. **Pruebas**: cada módulo se puede probar por separado.

---

### Sintaxis

```plain text
mi_programa/
├── main.py          ← punto de entrada: importa y coordina
├── tarifas.py       ← módulo: reglas de precios
└── clientes.py      ← módulo: gestión de clientes

```

---

```python
# main.py
# Importar módulos
import tarifas
import clientes

# Función propia del programa principal
def procesar_envio(peso):
    print("=== PROCESAMIENTO DE ENVÍO ===")

    # Utilizar una función del módulo clientes
    clientes.mostrar_cliente()

    # Utilizar una función del módulo tarifas
    coste = tarifas.coste_envio(peso)

    # Obtener descuento del cliente
    descuento = clientes.obtener_descuento()

    # Aplicar descuento
    total = tarifas.aplicar_descuento(coste, descuento)

    print("------------------------------")
    print("Peso:", peso, "kg")
    print("Coste inicial:", coste, "€")
    print("Descuento:", descuento, "%")
    print("Total a pagar:", round(total, 2), "€")

# Llamar a la función principal
procesar_envio(2.0)
```

---

### Ejemplo 1.1 · Del script único al primer módulo

> Una empresa de paquetería calcula el coste de cada envío con una tarifa base, un precio por kilo y un recargo para los envíos urgentes. Hasta ahora todo estaba en un único archivo, `monolito.py`.
El departamento de atención al cliente y el de facturación necesitan **la misma función** de cálculo. En lugar de copiarla en cada programa, se saca a un módulo `tarifas.py`, y `main.py` lo importa.

---

> 📁 `ejemplo_1_1_primer_modulo/`

```plain text
ejemplo_1_1_primer_modulo/
├── monolito.py
├── tarifas.py
└── main.py
```

---

**Antes: ****`monolito.py`** (todo en un archivo)

```python
TARIFA_BASE = 3.50
PRECIO_POR_KG = 0.80
RECARGO_URGENTE = 0.25


def coste_envio(peso_kg, urgente=False):
    coste = TARIFA_BASE + peso_kg * PRECIO_POR_KG
    if urgente:
        coste = coste * (1 + RECARGO_URGENTE)
    return round(coste, 2)


pedidos = [("A-101", 2.0, False), ("A-102", 7.5, True), ("A-103", 0.5, False)]
for codigo, peso, urgente in pedidos:
    print(f"{codigo}:{coste_envio(peso, urgente)} €")
```

---

**Después: ****`tarifas.py`** (el módulo, solo con las reglas de negocio)

```python
"""Tarifas de envío de la empresa de paquetería."""

TARIFA_BASE = 3.50
PRECIO_POR_KG = 0.80
RECARGO_URGENTE = 0.25


def coste_envio(peso_kg, urgente=False):
    coste = TARIFA_BASE + peso_kg * PRECIO_POR_KG
    if urgente:
        coste = coste * (1 + RECARGO_URGENTE)
    return round(coste, 2)
```

---

**Después: ****`main.py`** (el programa que lo usa)

```python
import tarifas

pedidos = [("A-101", 2.0, False), ("A-102", 7.5, True), ("A-103", 0.5, False)]
for codigo, peso, urgente in pedidos:
    print(f"{codigo}:{tarifas.coste_envio(peso, urgente)} €")

print("Tarifa base:", tarifas.TARIFA_BASE)
```

---

**Ejecución:**

```powershell
python monolito.py
python main.py
```

**Salida esperada de ****`monolito.py`****:**

```plain text
A-101: 5.1 €
A-102: 11.88 €
A-103: 3.9 €
```

---

**Salida esperada de ****`main.py`****:**

```plain text
A-101: 5.1 €
A-102: 11.88 €
A-103: 3.9 €
Tarifa base: 3.5
```

---

**Highlights:**

1. `import tarifas` se escribe **sin** la extensión `.py`. Python busca el archivo `tarifas.py`, en este caso en la misma carpeta que `main.py`.
2. Todo lo que está definido en el módulo se usa con la forma **`modulo.nombre`**: `tarifas.coste_envio()`, `tarifas.TARIFA_BASE`.
3. El resultado es idéntico: modularizar **no cambia lo que hace** el programa, cambia **cómo está organizado**.
4. Si mañana sube la tarifa base, se cambia en `tarifas.py` y **todos** los programas que lo importan reciben el cambio.
5. La cadena entre comillas triples de la primera línea es el **docstring del módulo**: describe para qué sirve el archivo.
---

## Sección 2. Crear e importar módulos

### Definición

> Cualquier archivo `.py` es un módulo y puede contener **variables**, **funciones** y **clases**. Hay cuatro formas de importarlo:

---

| Forma | Qué hace | Cómo se usa después |
| --- | --- | --- |
| `import modulo` | Carga el módulo completo | `modulo.funcion()` |
| `import modulo as alias` | Igual, pero con un nombre más corto | `alias.funcion()` |
| `from modulo import nombre` | Trae **solo** ese nombre al programa | `funcion()` directamente |
| `from modulo import nombre as alias` | Trae ese nombre con otro nombre | `alias()` |

---

> Existe una quinta forma, **`from modulo import *`**, que trae **todos** los nombres públicos del módulo. **No se recomienda**: no se sabe qué nombres entran y puede sobrescribir otros sin avisar.

Un módulo importado es un **objeto** de la clase `module`. Como cualquier objeto, tiene atributos:

| Atributo | Contenido |
| --- | --- |
| `modulo.__name__` | Nombre del módulo |
| `modulo.__doc__` | Su docstring |
| `modulo.__file__` | Ruta del archivo `.py` |
| `dir(modulo)` | Lista de todos los nombres que contiene |

---

```python
import pyspark

# 1. Nombre del paquete
print(pyspark.__name__)

# 2. Documentación del paquete
print(pyspark.__doc__)

# 3. Ubicación del archivo
print(pyspark.__file__)

# 4. Contenido del paquete
print(dir(pyspark))
# ['Accumulator', 'AccumulatorParam', 'Any', 'BarrierTaskContext', 'BarrierTaskInfo', 'BasicProfiler', 'Broadcast', 'CPickleSerializer', 'Callable', 'HiveContext', 'InheritableThread', 'MarshalSerializer', 'Profiler', 'RDD', 'RDDBarrier', 'Row', 'SQLContext', 'SparkConf', 'SparkContext', 'SparkFiles', 'SparkJobInfo', 'SparkStageInfo', 'StatusTracker', 'StorageLevel', 'TaskContext', 'TypeVar', 'Union', '_F', '_NoValue', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '__version__', '_globals', 'accumulators', 'broadcast', 'cast', 'cloudpickle', 'conf', 'context', 'core', 'errors', 'files', 'find_spark_home', 'inheritable_thread_target', 'is_remote_only', 'java_gateway', 'join', 'keyword_only', 'logger', 'loose_version', 'profiler', 'rdd', 'rddsampler', 'resource', 'resultiterable', 'serializers', 'shuffle', 'since', 'sql', 'statcounter', 'status', 'storagelevel', 'sys', 'taskcontext', 'traceback_utils', 'util', 'version', 'wraps']
```

---

### Analogía

> Pedir herramientas a un **almacén de bricolaje**:
- `import ferreteria` es traerte **la caja de herramientas entera**: para usar el martillo dices «el martillo **de la caja**» (`ferreteria.martillo`).
- `from ferreteria import martillo` es coger **solo el martillo** y dejarlo en tu mesa: lo usas directamente.
- `from ferreteria import *` es **vaciar la caja entera sobre tu mesa**: tienes todo a mano, pero si ya tenías un martillo propio, ya no sabes cuál es cuál.

---

>
La diferencia principal entre `import ferreteria` y `from ferreteria import *` está en **cómo accedes a las funciones, variables y clases del módulo y cómo se incorporan a tu espacio de nombres (*****namespace*****)**.

Vamos a verlo con un ejemplo sencillo.

```plain text
# ferreteria.py

iva = 0.21

def calcular_precio(precio):
    return precio * (1 + iva)

def mostrar_producto(nombre):
    print(f"Producto: {nombre}")
```

Importa el módulo como un objeto y permite acceder a sus componentes utilizando su nombre.

```plain text
import ferreteria

print(ferreteria.iva)

precio = ferreteria.calcular_precio(100)
print(precio)

ferreteria.mostrar_producto("Martillo")
```

**Ventajas:**

- Sabes de qué módulo procede cada función o variable.
- Evitas conflictos entre nombres de diferentes módulos.
- Es más fácil mantener y comprender el código.
Importa directamente al espacio de nombres actual todos los nombres públicos exportados por el módulo.

```plain text
from ferreteria import *

print(iva)

precio = calcular_precio(100)
print(precio)

mostrar_producto("Martillo")
```

**Desventajas:**

- No queda claro de dónde procede cada función o variable.
- Puede sobrescribir nombres que ya existían.
- Dificulta la lectura y el mantenimiento del código.
Por defecto, `import *` no importa nombres que comienzan por `_`, salvo que el módulo defina `__all__` para controlar explícitamente qué nombres exporta.

| Característica | `import ferreteria` | `from ferreteria import *` |
| --- | --- | --- |
| Importa el módulo como objeto accesible | Sí | No directamente |
| Acceso a funciones | `ferreteria.calcular_precio()` | `calcular_precio()` |
| Acceso a variables | `ferreteria.iva` | `iva` |
| Riesgo de conflictos | Bajo | Alto |
| Recomendado | Sí | Generalmente no |

---

### Sintaxis

```python
import modulo
import modulo as alias
from modulo import nombre1, nombre2
from modulo import nombre as alias
from modulo import *                   # desaconsejado

modulo.__name__
dir(modulo)
```

---

### Ejemplo 2.1 · Primer contacto: un módulo con una función y una clase

> Crear un módulo es tan sencillo como crear un script: basta con escribir funciones o clases en un archivo `.py`. Se crea el módulo `saludos.py` con una función `saludar()` y una clase `Saludo` cuyo `__init__` muestra un mensaje. Desde `main.py`, **en la misma carpeta**, se usan de las dos formas básicas: importando el módulo completo y con `from ... import`.

---

> 📁 `ejemplo_2_1_modulo_saludos/`

```plain text
ejemplo_2_1_modulo_saludos/
├── saludos.py
└── main.py
```

---

**`saludos.py`**

```python
def saludar():
    print("Hola, te estoy saludando desde la función saludar() "
          "del módulo saludos")


class Saludo:
    def __init__(self):
        print("Hola, te estoy saludando desde el __init__ "
              "de la clase Saludo")
    
    def saludar_persona(self, nombre):
        print(f"Hola {nombre}, desde la clase Saludo")
```

---

**`main.py`**

```python
# Forma 1: importar el módulo completo

import saludos

# Llamar a la función del módulo
saludos.saludar()

# Crear un objeto de la clase
objeto = saludos.Saludo()

# Llamar al método del objeto
objeto.saludar_persona("Ana")
```

```python
# Forma 2: importar solo la función y la clase

from saludos import Saludo

objeto = Saludo()

objeto.saludar_persona("Ana")
```

---

### Ejemplo 2.2 · Un módulo de funciones financieras

> El departamento de ventas de una cadena de electrodomésticos usa siempre los mismos cálculos: precio con IVA, aplicar un descuento y calcular el margen de beneficio. Se agrupan en un módulo `finanzas.py` de **funciones puras** (Clase 21) y constantes.
Desde `main.py` se inspecciona el módulo como objeto y se usan sus funciones, incluso como argumento de `map()`.

---

> 📁 `ejemplo_2_2_modulo_finanzas/`

```plain text
ejemplo_2_2_modulo_finanzas/
├── finanzas.py
└── main.py
```

---

**`finanzas.py`**

```python
"""Funciones financieras del departamento de ventas."""

IVA_GENERAL = 0.21
IVA_REDUCIDO = 0.10


def con_iva(importe, tipo=IVA_GENERAL):
    return round(importe * (1 + tipo), 2)


def aplicar_descuento(importe, porcentaje):
    return round(importe * (1 - porcentaje / 100), 2)


def margen(precio_venta, coste):
    return round((precio_venta - coste) / precio_venta * 100, 1)
```

---

**`main.py`**

```python
import finanzas

print(type(finanzas))
print(finanzas.__name__)
print(finanzas.__doc__)
print([nombre for nombre in dir(finanzas) if not nombre.startswith("_")])

print(finanzas.con_iva(100))
print(finanzas.con_iva(100, finanzas.IVA_REDUCIDO))
print(finanzas.aplicar_descuento(250, 15))
print(finanzas.margen(150, 90), "%")

precios = [120.0, 45.5, 80.0]
print(list(map(finanzas.con_iva, precios)))
```

**Salida esperada:**

```plain text
<class 'module'>
finanzas
Funciones financieras del departamento de ventas.
['IVA_GENERAL', 'IVA_REDUCIDO', 'aplicar_descuento', 'con_iva', 'margen']
121.0
110.0
212.5
40.0 %
[145.2, 55.05, 96.8]
```

---

**Highlights:**

>
1. `type(finanzas)` confirma que un módulo es un **objeto** de la clase `module`, igual que en la Clase 19 se vio que todo en Python es un objeto.
2. `dir()` devuelve todos los nombres del módulo. Se filtran los que empiezan por `_` (atributos internos como `__name__` o `__file__`) para ver solo lo que ha escrito el programador.
3. Las constantes del módulo se escriben en **MAYÚSCULAS** por convención: indican que no deben modificarse.
4. `map(finanzas.con_iva, precios)` pasa la función del módulo **sin paréntesis**, como cualquier función (Clase 21). Una función no deja de ser un objeto por estar en otro archivo.

---

### Ejemplo 2.3 · Las formas de importar y el conflicto de nombres

> La empresa de paquetería tiene dos módulos de tarifas, uno para envíos nacionales y otro para internacionales. **Los dos** tienen una función que se llama `calcular_coste()`. Se prueban las cuatro formas de importar y se provoca a propósito un **conflicto de nombres**.

---

> 📁 `ejemplo_2_3_formas_de_importar/`

```plain text
ejemplo_2_3_formas_de_importar/
├── envios_nacionales.py
├── envios_internacionales.py
└── main.py
```

---

**`envios_nacionales.py`**

```python
"""Tarifas para envíos dentro de España."""

ZONA = "nacional"


def calcular_coste(peso_kg):
    return round(4.00 + peso_kg * 0.60, 2)
```

---

**`envios_internacionales.py`**

```python
"""Tarifas para envíos fuera de España."""

ZONA = "internacional"


def calcular_coste(peso_kg):
    return round(12.00 + peso_kg * 2.50, 2)
```

---

**`main.py`**

```python
# 1. import modulo
import envios_nacionales
print("1.", envios_nacionales.ZONA, envios_nacionales.calcular_coste(4))

# 2. import modulo as alias
import envios_internacionales as intl
print("2.", intl.ZONA, intl.calcular_coste(4))

# 3. from modulo import nombre
from envios_nacionales import calcular_coste
print("3.", calcular_coste(4))

# 4. from modulo import nombre as alias
from envios_internacionales import calcular_coste as coste_intl
print("4.", coste_intl(4))

# 5. Conflicto: se importa otro nombre igual al que ya existía
from envios_internacionales import calcular_coste
print("5.", calcular_coste(4))
print("   ¿De qué módulo viene ahora?", calcular_coste.__module__)
```

**Salida esperada:**

```plain text
1. nacional 6.4
2. internacional 22.0
3. 6.4
4. 22.0
5. 22.0
   ¿De qué módulo viene ahora? envios_internacionales
```

---

**Highlights:**

>
1. Con `import modulo` (formas 1 y 2) **no hay conflicto posible**: el nombre del módulo actúa como apellido y distingue las dos funciones `calcular_coste`.
2. Con `from ... import` (formas 3 y 4) la función se usa sin prefijo. Es más corto, pero se pierde la información de **dónde viene**.
3. En el paso 5, el segundo `from ... import calcular_coste` **sobrescribe sin avisar** el nombre del paso 3. Es el mismo problema que con `from modulo import *`, pero multiplicado por todos los nombres del módulo.
4. Toda función guarda en `__module__` el nombre del módulo donde se definió. Sirve para depurar este tipo de errores.
5. Las importaciones van normalmente **al principio** del archivo. Aquí se reparten por el código solo para comparar las formas una a una.

---

### Ejemplo 2.4 · Un módulo de utilidades con comprehensions y lambdas

> El equipo de datos de una tienda online exporta del CRM la lista de clientes con nombres, emails y ciudades escritos de cualquier manera, y con algún cliente duplicado. Se crea el módulo `limpieza.py` con funciones puras que resuelven cada tarea con un tipo distinto de **comprehension**:

---

| Función | Qué hace | Herramienta |
| --- | --- | --- |
| `normalizar()` | Limpia espacios, mayúsculas y minúsculas | Comprehension de **lista** |
| `dominios()` | Dominios de email distintos | Comprehension de **set** |
| `indexar_por_email()` | Diccionario `email → cliente` | Comprehension de **diccionario** |
| `gasto_por_ciudad()` | Gasto total de cada ciudad | Comprehension de diccionario + expresión generadora |
| `ordenar()` | Ordena según un criterio | Diccionario `ORDENES` de **lambdas** |

---

`main.py` importa el módulo con un alias y, además, la constante `ORDENES`.

> 📁 `ejemplo_2_4_modulo_comprehensions/`

```plain text
ejemplo_2_4_modulo_comprehensions/
├── limpieza.py
└── main.py
```

---

**`limpieza.py`**

```python
"""Utilidades para limpiar y organizar los datos de clientes del CRM."""

ORDENES = {
    "nombre": lambda c: c["nombre"],
    "gasto": lambda c: c["gasto"],
}


def normalizar(clientes):
    return [
        {
            "nombre": c["nombre"].strip().title(),
            "email": c["email"].strip().lower(),
            "ciudad": c["ciudad"].strip().title(),
            "gasto": c["gasto"],
        }
        for c in clientes
    ]


def dominios(clientes):
    return {c["email"].split("@")[1] for c in clientes}


def indexar_por_email(clientes):
    return {c["email"]: c for c in clientes}


def gasto_por_ciudad(clientes):
    ciudades = sorted({c["ciudad"] for c in clientes})
    return {
        ciudad: round(sum(c["gasto"] for c in clientes if c["ciudad"] == ciudad), 2)
        for ciudad in ciudades
    }


def ordenar(clientes, criterio, descendente=False):
    return sorted(clientes, key=ORDENES[criterio], reverse=descendente)
```

---

**`main.py`**

```python
import limpieza as lp
from limpieza import ORDENES

crudos = [
    {"nombre": "  ana lópez", "email": "ANA@Gmail.com ", "ciudad": "madrid", "gasto": 320.5},
    {"nombre": "LUIS PÉREZ ", "email": "luis@empresa.es", "ciudad": " Sevilla", "gasto": 89.9},
    {"nombre": "marta ruiz", "email": "marta@gmail.com", "ciudad": "Madrid ", "gasto": 145.0},
    {"nombre": "ana lópez", "email": "ana@gmail.com", "ciudad": "madrid", "gasto": 60.0},
]

clientes = lp.normalizar(crudos)
print([c["nombre"] for c in clientes])
print("Dominios:", sorted(lp.dominios(clientes)))

indice = lp.indexar_por_email(clientes)
print(len(clientes), "registros ->", len(indice), "emails distintos")
print("Gasto por ciudad:", lp.gasto_por_ciudad(clientes))

mejores = lp.ordenar(clientes, "gasto", descendente=True)
print("Por gasto:", [(c["nombre"], c["gasto"]) for c in mejores[:2]])
print("Criterios disponibles:", list(ORDENES))
```

**Salida esperada:**

```plain text
['Ana López', 'Luis Pérez', 'Marta Ruiz', 'Ana López']
Dominios: ['empresa.es', 'gmail.com']
4 registros -> 3 emails distintos
Gasto por ciudad: {'Madrid': 525.5, 'Sevilla': 89.9}
Por gasto: [('Ana López', 320.5), ('Marta Ruiz', 145.0)]
Criterios disponibles: ['nombre', 'gasto']
```

---

**Highlights:**

>
1. Las cuatro funciones son **puras**: reciben la lista y devuelven datos nuevos sin modificar `crudos` (Clase 21).
2. `dominios()` devuelve un **set**, así que `gmail.com` aparece una sola vez aunque lo usen tres clientes. Se ordena con `sorted()` para mostrarlo siempre igual, porque un set no tiene orden.
3. En `indexar_por_email()`, los dos registros de Ana tienen el mismo email tras normalizar. En un diccionario las claves no se repiten, así que **el último registro sustituye al primero**: hay 4 registros pero 3 emails distintos. Al deduplicar así hay que decidir conscientemente cuál se conserva.
4. `gasto_por_ciudad()` combina una comprehension de diccionario con una expresión generadora dentro de `sum()`. Madrid suma los tres registros: 320,5 + 145 + 60.
5. El módulo exporta tanto **funciones** como un **diccionario de lambdas**. Desde fuera se puede consultar qué criterios hay (`list(ORDENES)`) sin leer el código del módulo.
6. `import limpieza as lp` y `from limpieza import ORDENES` conviven sin problema: son dos formas de acceder al mismo módulo.

---

## Sección 3. Qué ocurre al importar un módulo

### Definición

> Cuando Python ejecuta `import modulo` por **primera vez** en un programa:

6. **Busca** el archivo `modulo.py` (Sección 6 explica dónde).
7. **Ejecuta todo su código**, de arriba abajo. Las líneas `def` y `class` crean funciones y clases; un `print()` suelto se ejecuta de verdad.
8. Crea un **objeto módulo** con todos los nombres resultantes.
9. Lo guarda en un diccionario llamado **`sys.modules`**, que funciona como caché de módulos ya cargados.  
- Si después se vuelve a importar el mismo módulo, **desde cualquier archivo del programa**, Python lo encuentra en `sys.modules` y **no lo vuelve a ejecutar**: entrega el mismo objeto.
- Consecuencias:
> • Un módulo se ejecuta **una sola vez** por programa.
• Todos los archivos que importan un módulo **comparten el mismo objeto**. Si uno modifica un dato mutable del módulo (por ejemplo, un diccionario), los demás ven el cambio.
Además, Python guarda una versión compilada del módulo en la carpeta **`__pycache__/`** (archivos `.pyc`) para cargarlo más rápido la próxima vez. Esa carpeta se crea sola, se puede borrar sin problema y **no se sube a Git**.
10. **Busca** el archivo `modulo.py` (Sección 6 explica dónde).
11. **Ejecuta todo su código**, de arriba abajo. Las líneas `def` y `class` crean funciones y clases; un `print()` suelto se ejecuta de verdad.
12. Crea un **objeto módulo** con todos los nombres resultantes.
13. Lo guarda en un diccionario llamado **`sys.modules`**, que funciona como caché de módulos ya cargados.
- Un módulo se ejecuta **una sola vez** por programa.
- Todos los archivos que importan un módulo **comparten el mismo objeto**. Si uno modifica un dato mutable del módulo (por ejemplo, un diccionario), los demás ven el cambio.
14. Lo guarda en un diccionario llamado **`sys.modules`**, que funciona como caché de módulos ya cargados.
---

### Sintaxis

```python
import sys

"nombre_modulo" in sys.modules        # ¿ya se ha cargado?
sys.modules["nombre_modulo"]          # el objeto módulo guardado en la caché
modulo_a.modulo_b is modulo_b         # True: es el mismo objeto
```

---

### Ejemplo 3.1 · Un módulo de configuración compartido

> Una aplicación de informes financieros tiene un módulo `configuracion.py` con la moneda y el número de decimales con que se muestran los importes. El módulo `informes.py` lo importa para formatear cantidades, y `main.py` importa ambos.
Se añade un `print()` en `configuracion.py` para ver **cuántas veces** se ejecuta su código y se comprueba que un cambio en la configuración hecho desde `main.py` se nota en `informes.py`.

---

> 📁 `ejemplo_3_1_que_pasa_al_importar/`

```plain text
ejemplo_3_1_que_pasa_al_importar/
├── configuracion.py
├── informes.py
└── main.py
```

---

**`configuracion.py`**

```python
print("  [cargando el módulo configuracion]")

CONFIG = {"moneda": "EUR", "decimales": 2}
```

---

**`informes.py`**

```python
import configuracion


def formatear(importe):
    decimales = configuracion.CONFIG["decimales"]
    moneda = configuracion.CONFIG["moneda"]
    return f"{importe:.{decimales}f}{moneda}"
```

---

**`main.py`**

```python
import sys

print("Inicio del programa")
import configuracion
import configuracion            # segunda vez: no se vuelve a ejecutar
import informes                 # informes también importa configuracion
print("Fin de los import")

print("¿Está en sys.modules?", "configuracion" in sys.modules)
print("¿Es el mismo objeto?", informes.configuracion is configuracion)

print(informes.formatear(1234.7))
configuracion.CONFIG["moneda"] = "USD"
configuracion.CONFIG["decimales"] = 0
print(informes.formatear(1234.7))
```

**Salida esperada:**

```plain text
Inicio del programa
  [cargando el módulo configuracion]
Fin de los import
¿Está en sys.modules? True
¿Es el mismo objeto? True
1234.70 EUR
1235 USD
```

---

**Highlights:**

>
1. El mensaje `[cargando el módulo configuracion]` aparece **una sola vez**, aunque el módulo se importa tres veces (dos en `main.py` y una dentro de `informes.py`).
2. `informes.configuracion is configuracion` es `True`: `main.py` e `informes.py` trabajan con **el mismo objeto módulo**, no con copias.
3. Por eso, al cambiar `CONFIG` desde `main.py`, `informes.formatear()` usa la moneda y los decimales nuevos.
4. Esta característica es útil para compartir configuración, pero peligrosa si se abusa: cualquier archivo puede cambiar un dato que otros usan. Es el mismo problema de las **funciones impuras** de la Clase 21.
5. Después de ejecutar el ejemplo aparece una carpeta `__pycache__/` junto a los módulos. Es normal.
6. Poner un `print()` suelto en un módulo solo tiene sentido para este experimento. En la práctica, un módulo **no debe ejecutar nada** al importarse, solo definir cosas. La Sección 4 explica cómo conseguirlo.

---

### Ejemplo 3.2 · Un objeto compartido por todos los módulos

> Una tienda online quiere un **registro de auditoría** único en el que todos los departamentos anoten lo que hacen: pagos, envíos… Como un módulo se ejecuta **una sola vez**, si el módulo `auditoria.py` crea un objeto al importarse, **todos** los módulos que lo importen recibirán **el mismo objeto**.
- `auditoria.py`: la clase `RegistroAuditoria` y una instancia única, `registro`.
- `pagos.py` y `envios.py`: importan `registro` y anotan en él cada operación.
- `main.py`: ejecuta operaciones y consulta el registro.

---

> 📁 `ejemplo_3_2_objeto_compartido/`

```plain text
ejemplo_3_2_objeto_compartido/
├── auditoria.py
├── pagos.py
├── envios.py
└── main.py
```

---

**`auditoria.py`**

```python
"""Registro de auditoría compartido por todo el programa."""


class RegistroAuditoria:
    def __init__(self):
        self._eventos = []

    def anotar(self, origen, mensaje):
        self._eventos.append((len(self._eventos) + 1, origen, mensaje))

    def filtrar(self, origen):
        return [evento for evento in self._eventos if evento[1] == origen]

    def __len__(self):
        return len(self._eventos)

    def __iter__(self):
        for evento in self._eventos:
            yield evento


registro = RegistroAuditoria()          # instancia única, creada al importar el módulo
```

---

**`pagos.py`**

```python
"""Cobros a clientes."""

from auditoria import registro


def cobrar(cliente, importe):
    registro.anotar("pagos", f"cobro de{importe} € a{cliente}")
    return round(importe, 2)
```

---

**`envios.py`**

```python
"""Preparación de envíos."""

from auditoria import registro


def preparar_envio(cliente, articulos):
    registro.anotar("envios", f"{len(articulos)} artículos para{cliente}")
    return sorted(articulos, key=lambda articulo: articulo.lower())
```

---

**`main.py`**

```python
import auditoria
import pagos
from auditoria import registro
from envios import preparar_envio

pagos.cobrar("Bodegas Sol", 245.0)
print(preparar_envio("Bodegas Sol", ["vino tinto", "Cava", "aceite"]))
pagos.cobrar("Talleres Norte", 99.9)

print("Eventos registrados:", len(registro))
for numero, origen, mensaje in registro:
    print(f"{numero}. [{origen}]{mensaje}")

print("Solo pagos:", len(registro.filtrar("pagos")))
print("¿Mismo objeto en todos los módulos?", registro is auditoria.registro is pagos.registro)
```

**Salida esperada:**

```plain text
['aceite', 'Cava', 'vino tinto']
Eventos registrados: 3
  1. [pagos] cobro de 245.0 € a Bodegas Sol
  2. [envios] 3 artículos para Bodegas Sol
  3. [pagos] cobro de 99.9 € a Talleres Norte
Solo pagos: 2
¿Mismo objeto en todos los módulos? True
```

---

**Highlights:**

>
1. La línea `registro = RegistroAuditoria()` se ejecuta **una sola vez**, la primera vez que algún archivo importa `auditoria`. Los demás imports reciben el objeto ya creado desde `sys.modules`.
2. `pagos.py` y `envios.py` anotan en **el mismo registro** sin conocerse entre sí: por eso los eventos salen numerados del 1 al 3 en el orden en que ocurrieron.
3. La comparación encadenada `a is b is c` confirma que `main.py`, `auditoria` y `pagos` apuntan al mismo objeto.
4. `__iter__` es un **generador** y `filtrar()` usa una **comprehension**: la clase permite recorrer y consultar los eventos sin dar acceso a la lista interna `_eventos`.
5. En `envios.py`, `key=lambda articulo: articulo.lower()` ordena sin distinguir mayúsculas. Sin la lambda, `Cava` saldría primero porque las mayúsculas van antes que las minúsculas.
6. Este patrón (un módulo que crea un objeto único y compartido) se usa mucho para registros (*logs*), configuraciones y conexiones. Es la forma más sencilla en Python de tener **una sola instancia** de una clase en todo el programa.

---

## Sección 4. `__name__` y el patrón `if __name__ == "__main__":`

### Definición

> Todo módulo tiene una variable especial **`__name__`** que Python rellena automáticamente:

| Cómo se usa el archivo | Valor de `__name__` |
| --- | --- |
| Se **ejecuta directamente**: `python validaciones.py` | `"__main__"` |
| Se **importa** desde otro archivo: `import validaciones` | `"validaciones"` (el nombre del módulo) |

---

Esto permite escribir un bloque de código que **solo se ejecuta cuando el archivo se lanza directamente**, y que se ignora cuando se importa:

```python
if __name__ == "__main__":
    # pruebas o programa principal
```

---

Usos habituales:

15. Añadir **pruebas rápidas** al final de un módulo, para comprobarlo de forma aislada sin que esas pruebas molesten al importarlo.
16. Marcar el **punto de entrada** de un programa en su `main.py`, normalmente llamando a una función `main()`.
---

### Analogía.

Un **actor** de una compañía de teatro. Cuando ensaya **solo en su casa**, recita su papel completo de principio a fin para comprobar que se lo sabe. Cuando actúa **dentro de la obra**, no recita de golpe todo su papel: espera a que el director le dé paso en cada escena. El actor es el mismo, pero se comporta distinto según si «lo ejecutan» solo o «lo importan» en la obra.

---

### Sintaxis

```python
# mi_modulo.py
def funcion_util():
    ...

if __name__ == "__main__":
    print(funcion_util())       # solo con: python mi_modulo.py
```

---

```python
# main.py
def main():
    ...                         # programa principal

if __name__ == "__main__":
    main()
```

---

### Ejemplo 4.1 · Un módulo de validaciones con pruebas propias

> El equipo de datos de una distribuidora mayorista recibe fichas de clientes con códigos postales y teléfonos escritos de muchas formas. Se crea un módulo `validaciones.py` con dos funciones:
- `es_codigo_postal_valido(cp)`: 5 dígitos y las dos primeras cifras entre 01 y 52 (las provincias españolas).
- `normalizar_telefono(telefono)`: deja solo los dígitos y devuelve el número con el prefijo `+34`, o `None` si no tiene al menos 9 cifras.
El módulo incluye pruebas rápidas dentro de `if __name__ == "__main__":`. Se ejecuta de dos formas: **directamente** y **importado** desde `main.py`.

---

> 📁 `ejemplo_4_1_name_main/`

```plain text
ejemplo_4_1_name_main/
├── validaciones.py
└── main.py
```

---

**`validaciones.py`**

```python
"""Validaciones de los datos de clientes."""

print(f"  [validaciones.py] __name__ ={__name__!r}")


def es_codigo_postal_valido(cp):
    return len(cp) == 5 and cp.isdigit() and 1 <= int(cp[:2]) <= 52


def normalizar_telefono(telefono):
    digitos = "".join(c for c in telefono if c.isdigit())
    if len(digitos) < 9:
        return None
    return "+34" + digitos[-9:]


if __name__ == "__main__":
    print("  Pruebas rápidas del módulo:")
    print("  ", es_codigo_postal_valido("28013"), es_codigo_postal_valido("99001"))
    print("  ", normalizar_telefono("612 34 56 78"), normalizar_telefono("123"))
```

---

**`main.py`**

```python
import validaciones

print(f"[main.py] __name__ ={__name__!r}")

clientes = [
    ("Ferretería Ruiz", "28013", "91-555-12-34"),
    ("Bodegas Sol", "99001", "600 11 22 33"),
    ("Talleres Norte", "48001", "944 000"),
]

validos = [
    (nombre, validaciones.normalizar_telefono(telefono))
    for nombre, cp, telefono in clientes
    if validaciones.es_codigo_postal_valido(cp)
]
print(validos)
```

---

**Ejecución 1: el módulo directamente**

```powershell
python validaciones.py
```

**Salida esperada:**

```plain text
  [validaciones.py] __name__ = '__main__'
  Pruebas rápidas del módulo:
   True False
   +34612345678 None
```

---

**Ejecución 2: el programa que lo importa**

```powershell
python main.py
```

**Salida esperada:**

```plain text
  [validaciones.py] __name__ = 'validaciones'
[main.py] __name__ = '__main__'
[('Ferretería Ruiz', '+34915551234'), ('Talleres Norte', None)]
```

---

**Highlights:**

>
1. El **mismo archivo** `validaciones.py` tiene un `__name__` distinto según cómo se use: `'__main__'` al ejecutarlo y `'validaciones'` al importarlo.
2. Al importarlo desde `main.py`, las pruebas del bloque `if` **no se ejecutan**. El módulo solo aporta sus funciones.
3. El archivo que se lanza con `python` siempre es el `'__main__'` del programa: en la ejecución 2 lo es `main.py`.
4. `Bodegas Sol` se descarta porque su código postal empieza por `99`. `Talleres Norte` pasa el filtro, pero su teléfono tiene solo 6 cifras y queda como `None`: un dato pendiente de revisar.
5. El `print()` suelto de la línea 3 está solo para ver el valor de `__name__`. En un módulo real se quitaría.

---

### Ejemplo 4.2 · Un módulo con una clase y sus propias pruebas

> El departamento financiero de una empresa exportadora convierte sus facturas en euros a otras divisas. Se crea el módulo `conversor.py` con la clase `ConversorDivisas`:
- `convertir()`: convierte un importe a una divisa.
- `convertir_lote()`: convierte una lista de importes, con una comprehension de **lista**.
- `tabla()`: muestra cuánto vale un importe en todas las divisas, con una comprehension de **diccionario**.
Al final del módulo, dentro de `if __name__ == "__main__":`, hay unas pruebas rápidas que comparan cada resultado con el valor esperado. `main.py` importa la clase y la usa con las facturas del día, combinándola con comprehensions, `zip()`, `filter()` y una `lambda`.

---

> 📁 `ejemplo_4_2_clase_con_pruebas/`

```plain text
ejemplo_4_2_clase_con_pruebas/
├── conversor.py
└── main.py
```

---

**`conversor.py`**

```python
"""Conversión de importes en euros a otras divisas."""


class ConversorDivisas:
    def __init__(self, tasas):
        self.tasas = tasas                      # {divisa: unidades por 1 €}

    def convertir(self, importe_eur, divisa):
        return round(importe_eur * self.tasas[divisa], 2)

    def convertir_lote(self, importes_eur, divisa):
        return [self.convertir(importe, divisa) for importe in importes_eur]

    def tabla(self, importe_eur):
        return {divisa: self.convertir(importe_eur, divisa) for divisa in self.tasas}


if __name__ == "__main__":
    prueba = ConversorDivisas({"USD": 1.10, "GBP": 0.85})
    print("Prueba convertir:", prueba.convertir(100, "USD") == 110.0)
    print("Prueba lote:     ", prueba.convertir_lote([10, 20], "GBP") == [8.5, 17.0])
    print("Prueba tabla:    ", prueba.tabla(100) == {"USD": 110.0, "GBP": 85.0})
```

---

**`main.py`**

```python
from conversor import ConversorDivisas

tasas_hoy = {"USD": 1.08, "GBP": 0.86, "JPY": 162.5}
conversor = ConversorDivisas(tasas_hoy)

facturas = [("F-01", 1200.0), ("F-02", 349.9), ("F-03", 75.0)]

print("100 € equivalen a:", conversor.tabla(100))

en_usd = conversor.convertir_lote([importe for _, importe in facturas], "USD")
print("Facturas en USD:", en_usd)

grandes_gbp = {numero: conversor.convertir(importe, "GBP")
               for numero, importe in facturas if importe > 100}
print("Mayores de 100 € en GBP:", grandes_gbp)

numeros = [numero for numero, _ in facturas]
superan_300_usd = list(filter(lambda par: par[1] > 300, zip(numeros, en_usd)))
print("Superan 300 USD:", superan_300_usd)
```

---

**Ejecución 1: el módulo directamente**

```powershell
python conversor.py
```

**Salida esperada:**

```plain text
Prueba convertir: True
Prueba lote:      True
Prueba tabla:     True
```

---

**Ejecución 2: el programa que lo importa**

```powershell
python main.py
```

**Salida esperada:**

```plain text
100 € equivalen a: {'USD': 108.0, 'GBP': 86.0, 'JPY': 16250.0}
Facturas en USD: [1296.0, 377.89, 81.0]
Mayores de 100 € en GBP: {'F-01': 1032.0, 'F-02': 300.91}
Superan 300 USD: [('F-01', 1296.0), ('F-02', 377.89)]
```

---

**Highlights:**

>
1. Las pruebas usan **tasas inventadas y fáciles de calcular** (1,10 y 0,85), distintas de las de `main.py`. Así se comprueba la lógica de la clase con números que se pueden verificar de cabeza.
2. Al importar `conversor` desde `main.py`, las pruebas **no se ejecutan** y la salida queda limpia.
3. Cada prueba compara el resultado con el esperado y muestra `True` o `False`. Si algún día se modifica la clase y una prueba muestra `False`, se detecta el error antes de usar el módulo en otro programa.
4. Dentro de la clase, `convertir_lote()` y `tabla()` **reutilizan** `convertir()` en lugar de repetir la fórmula: si cambia el redondeo, se cambia en un solo método.
5. En `main.py`, `zip(numeros, en_usd)` empareja cada número de factura con su importe en dólares, y `filter()` con una `lambda` se queda con los pares que superan 300 USD.

---

## Sección 5. Módulos con clases y funciones

### Definición

> Un módulo puede contener **clases**, igual que funciones. Al organizar un programa orientado a objetos en módulos, se suele seguir este reparto:

| Módulo | Contenido típico |
| --- | --- |
| `modelos.py` | Las clases que representan los **datos** del negocio (`Producto`, `Cliente`, `Venta`…) y su jerarquía de herencia |
| `servicios.py`, `inventario.py`… | Clases o funciones que **trabajan con** esos modelos |
| `reglas.py`, `politicas.py`, `utilidades.py`… | **Funciones puras** con reglas de negocio y cálculos |
| `main.py` | El punto de entrada: crea los objetos y coordina |

---

Reglas importantes:

>
- Para usar una clase de otro módulo se importa como cualquier otro nombre: `from modelos import Producto`.
- Una clase **derivada** puede estar en un módulo distinto de su clase **base**: basta con importar la base.
- `isinstance()` funciona con clases importadas, y reconoce también a las derivadas (Clase 20).
- La programación modular **combina** bien con la orientada a objetos y con la funcional: las clases organizan los datos, las funciones puras organizan las reglas y los módulos organizan los archivos.

---

### Analogía.

> En una **fábrica de muebles**, el departamento de diseño guarda los **planos** de cada mueble (las clases), el taller tiene las **máquinas** que cortan y montan siguiendo esos planos (los servicios) y la oficina técnica mantiene el **manual de normas** de calidad (las funciones puras). Ningún departamento guarda copias de los planos de otro: cuando el taller necesita uno, lo **pide** a diseño.

---

### Sintaxis

```python
# modelos.py
class Base:
    ...

class Derivada(Base):
    ...
```

---

```python
# servicios.py
from modelos import Base

class Gestor:
    def agregar(self, obj):
        if not isinstance(obj, Base):
            raise TypeError(...)
```

---

```python
# main.py
from modelos import Base, Derivada
from servicios import Gestor
```

---

### Ejemplo 5.1 · Inventario de un almacén repartido en módulos

> Una cadena de supermercados gestiona el inventario de sus almacenes. El programa se reparte en dos módulos:
- `modelos.py`: la clase `Producto` y su derivada `ProductoPerecedero`, que vende con un **30 % de descuento** los productos a los que les quedan **3 días o menos** para caducar.
- `inventario.py`: la clase `Inventario`, que guarda los productos y ofrece consultas. Usa herramientas de la Clase 21: `filter()`, expresiones generadoras, `sorted()` con `key` y un generador en `__iter__`.
`main.py` importa ambos módulos, crea el inventario y lo consulta.

---

> 📁 `ejemplo_5_1_modulos_con_clases/`

```plain text
ejemplo_5_1_modulos_con_clases/
├── modelos.py
├── inventario.py
└── main.py
```

---

**`modelos.py`**

```python
"""Clases del catálogo de productos."""


class Producto:
    def __init__(self, sku, nombre, precio, stock):
        self.sku = sku
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @property
    def valor_stock(self):
        return round(self.precio * self.stock, 2)

    def precio_venta(self):
        return self.precio

    def __repr__(self):
        return f"{type(self).__name__}({self.sku!r},{self.nombre!r})"


class ProductoPerecedero(Producto):
    def __init__(self, sku, nombre, precio, stock, dias_para_caducar):
        super().__init__(sku, nombre, precio, stock)
        self.dias_para_caducar = dias_para_caducar

    def precio_venta(self):
        if self.dias_para_caducar <= 3:
            return round(self.precio * 0.70, 2)
        return self.precio
```

---

**`inventario.py`**

```python
"""Gestión del inventario de un almacén."""

from modelos import Producto


class Inventario:
    CRITERIOS = {
        "precio": lambda p: p.precio_venta(),
        "stock": lambda p: p.stock,
        "valor": lambda p: p.valor_stock,
    }

    def __init__(self):
        self._productos = []

    def agregar(self, producto):
        if not isinstance(producto, Producto):
            raise TypeError("Solo se admiten objetos Producto")
        self._productos.append(producto)

    def __len__(self):
        return len(self._productos)

    def __iter__(self):
        for producto in self._productos:
            yield producto

    def bajo_stock(self, umbral):
        return list(filter(lambda p: p.stock < umbral, self._productos))

    def valor_total(self):
        return round(sum(p.valor_stock for p in self._productos), 2)

    def ordenar_por(self, criterio, descendente=False):
        return sorted(self._productos, key=self.CRITERIOS[criterio], reverse=descendente)
```

---

**`main.py`**

```python
from modelos import Producto, ProductoPerecedero
from inventario import Inventario

almacen = Inventario()
almacen.agregar(Producto("SKU-01", "Aceite 1L", 6.40, 120))
almacen.agregar(ProductoPerecedero("SKU-02", "Yogur pack 4", 2.20, 15, dias_para_caducar=2))
almacen.agregar(Producto("SKU-03", "Arroz 1kg", 1.35, 8))
almacen.agregar(ProductoPerecedero("SKU-04", "Queso curado", 9.90, 30, dias_para_caducar=40))

print("Productos en almacén:", len(almacen))
for p in almacen:
    print(f"{p.nombre:<14} precio venta:{p.precio_venta():>5}")

print("Bajo stock (<20):", almacen.bajo_stock(20))
print("Valor total:", almacen.valor_total())
print("Por valor:", [p.sku for p in almacen.ordenar_por("valor", descendente=True)])

try:
    almacen.agregar("Leche")
except TypeError as error:
    print("TypeError:", error)
```

**Salida esperada:**

```plain text
Productos en almacén: 4
  Aceite 1L      precio venta:   6.4
  Yogur pack 4   precio venta:  1.54
  Arroz 1kg      precio venta:  1.35
  Queso curado   precio venta:   9.9
Bajo stock (<20): [ProductoPerecedero('SKU-02', 'Yogur pack 4'), Producto('SKU-03', 'Arroz 1kg')]
Valor total: 1108.8
Por valor: ['SKU-01', 'SKU-04', 'SKU-02', 'SKU-03']
TypeError: Solo se admiten objetos Producto
```

---

**Highlights:**

>
1. `inventario.py` importa `Producto` desde `modelos.py` para poder comprobar los tipos con `isinstance()`. Un `ProductoPerecedero` también pasa la comprobación porque **es un** `Producto` (Clase 20).
2. `main.py` importa de **dos** módulos. Cada archivo tiene una responsabilidad: `modelos.py` sabe **qué es** un producto; `inventario.py` sabe **cómo gestionar** muchos.
3. El bucle `for` llama al precio de venta de cada objeto y cada clase responde con su versión: es **polimorfismo**, aunque las clases estén en otro archivo.
4. `__iter__` es un **generador** (Clase 21): permite recorrer el inventario con `for` sin dar acceso directo a la lista interna `_productos`.
5. El diccionario `CRITERIOS` guarda **lambdas** como valores: añadir un criterio nuevo de ordenación es añadir una entrada, sin tocar `ordenar_por()`.

---

### Ejemplo 5.2 · Un módulo de reglas funcionales usado por una clase

> Una tienda online de material deportivo cambia de **política de precios** según la campaña: precio normal, rebajas, Black Friday u outlet. El equipo decide separar las reglas de la lógica:
- `politicas_precio.py`: **solo funciones puras**. Incluye una función que **fabrica** descuentos (clausura, Clase 21) y una función `componer()` que encadena varias políticas usando `reduce()`. Al final, un diccionario `POLITICAS` con las campañas disponibles.
- `tarificador.py`: la clase `Tarificador`, que **recibe una política** (una función) y la aplica a un catálogo.
Así, marketing puede añadir campañas en `politicas_precio.py` sin tocar la clase.

---

> 📁 `ejemplo_5_2_clases_y_funciones/`

```plain text
ejemplo_5_2_clases_y_funciones/
├── politicas_precio.py
├── tarificador.py
└── main.py
```

---

**`politicas_precio.py`**

```python
"""Políticas de precio: funciones puras que reciben un precio y devuelven otro."""

from functools import reduce


def precio_normal(precio):
    return precio


def redondeo_comercial(precio):
    return int(precio) + 0.99


def crear_descuento(porcentaje):
    def descontar(precio):
        return round(precio * (1 - porcentaje / 100), 2)
    return descontar


def componer(*politicas):
    return lambda precio: reduce(lambda acumulado, f: f(acumulado), politicas, precio)


POLITICAS = {
    "normal": precio_normal,
    "rebajas": crear_descuento(20),
    "black_friday": crear_descuento(35),
    "outlet": componer(crear_descuento(40), redondeo_comercial),
}
```

---

**`tarificador.py`**

```python
"""Clase que aplica una política de precios a un catálogo."""

from politicas_precio import POLITICAS, precio_normal


class Tarificador:
    def __init__(self, politica=precio_normal):
        self.politica = politica

    def cambiar_politica(self, nombre):
        self.politica = POLITICAS[nombre]

    def tarifar(self, catalogo):
        return {producto: self.politica(precio) for producto, precio in catalogo.items()}
```

---

**`main.py`**

```python
from tarificador import Tarificador
from politicas_precio import POLITICAS, crear_descuento

catalogo = {"Zapatillas": 89.90, "Mochila": 45.00, "Gorra": 19.50}

caja = Tarificador()
print("Normal:      ", caja.tarifar(catalogo))

caja.cambiar_politica("black_friday")
print("Black Friday:", caja.tarifar(catalogo))

caja.cambiar_politica("outlet")
print("Outlet:      ", caja.tarifar(catalogo))

caja.politica = crear_descuento(10)               # política creada al momento
print("Socios -10%: ", caja.tarifar(catalogo))

print("Políticas disponibles:", list(POLITICAS))
```

**Salida esperada:**

```plain text
Normal:       {'Zapatillas': 89.9, 'Mochila': 45.0, 'Gorra': 19.5}
Black Friday: {'Zapatillas': 58.44, 'Mochila': 29.25, 'Gorra': 12.68}
Outlet:       {'Zapatillas': 53.99, 'Mochila': 27.99, 'Gorra': 11.99}
Socios -10%:  {'Zapatillas': 80.91, 'Mochila': 40.5, 'Gorra': 17.55}
Políticas disponibles: ['normal', 'rebajas', 'black_friday', 'outlet']
```

---

**Highlights:**

>
1. Un módulo puede **importar otros módulos**: `politicas_precio.py` importa `reduce` de la biblioteca estándar y `tarificador.py` importa `politicas_precio.py`. Se forma una cadena de dependencias.
2. El atributo `politica` de la clase guarda **una función**. Cambiar de campaña es asignar otra función: la clase no sabe ni le importa cómo se calcula el precio.
3. `componer(crear_descuento(40), redondeo_comercial)` crea una política nueva encadenando dos: primero descuenta un 40 % y después redondea a `,99`. `reduce()` pasa el precio por cada función en orden.
4. El diccionario `POLITICAS` se crea **al importar** el módulo, una sola vez (Sección 3).
5. La regla de diseño es: **lo que cambia a menudo** (las reglas de negocio) va en su propio módulo, separado de **lo que cambia poco** (la clase que las aplica).

---

## Sección 6. Dónde busca Python los módulos

### Definición

> Al ejecutar `import nombre`, Python busca el módulo **en orden** en una lista de carpetas guardada en **`sys.path`**. Usa el **primero** que encuentra:
1. **La carpeta del script que se está ejecutando** (`sys.path[0]`). Por eso `main.py` encuentra los módulos de su misma carpeta, y por eso **un módulo guardado en otra carpeta no se encuentra** con un simple `import`. La solución ordenada es agrupar los módulos en **paquetes** (Sección 7) colocados junto al `main.py`.
2. Las carpetas de la **biblioteca estándar** de Python.
3. La carpeta **`site-packages`** del entorno virtual activo, donde `pip` instala las librerías externas.

---

Errores típicos al importar:

| Error | Causa habitual |
| --- | --- |
| `ModuleNotFoundError: No module named 'x'` | El archivo no existe, el nombre está mal escrito, se ejecuta desde otra carpeta, o la librería externa no está instalada en el `.venv` activo |
| `ImportError: cannot import name 'y' from 'x'` | El módulo existe, pero no contiene el nombre `y` |
| `AttributeError: module 'x' has no attribute 'y'` | Igual que el anterior, usando `x.y`. Muy a menudo: **un archivo propio tiene el mismo nombre que un módulo estándar** y lo está tapando |

---

> ⚠️ **Nunca** llames a tus archivos como módulos de Python o de librerías: `random.py`, `math.py`, `statistics.py`, `json.py`, `csv.py`, `datetime.py`, `pandas.py`… Como la carpeta del script se mira **primero**, tu archivo «tapa» al módulo original.

---

### Analogía 

Cuando buscas unas **llaves**, miras primero en el **bolsillo**, después en el **recibidor** y por último en el **cajón de la cocina**. Te quedas con las primeras que encuentras. Si en el bolsillo llevas unas llaves que se parecen a las de casa pero son de la oficina, **nunca llegarás al recibidor**, y la puerta de casa no se abrirá.

---

### Sintaxis

```python
import sys

sys.path              # lista de carpetas donde se buscan módulos, en orden
sys.path[0]           # la carpeta del script que se está ejecutando

modulo.__file__       # ruta del archivo desde el que se cargó el módulo
```

---

### Ejemplo 6.1 · Un archivo que tapa a un módulo estándar

> Un analista quería probar el módulo `random` para hacer un sorteo entre clientes y, sin pensarlo, llamó a su archivo de pruebas **`random.py`**. Después, en otro archivo de la misma carpeta, intenta usar el `random` de Python.
Se inspecciona `sys.path`, se comprueba **de dónde** se ha cargado `random` y se provoca también un `ModuleNotFoundError`.

---

> 📁 `ejemplo_6_1_donde_busca_python/`

```plain text
ejemplo_6_1_donde_busca_python/
├── random.py        ← ¡nombre peligroso!
└── main.py
```

---

**`random.py`**

```python
# Archivo creado por error con el mismo nombre que un módulo estándar
def sorteo():
    return "Esto NO es el módulo random de Python"
```

---

**`main.py`**

```python
import os
import sys

print("Primera ruta de búsqueda:", os.path.basename(sys.path[0]))
print("Número de rutas > 1:", len(sys.path) > 1)

import random
print("random se ha cargado desde:", os.path.basename(random.__file__))
try:
    print(random.randint(1, 6))
except AttributeError as error:
    print("AttributeError:", error)

try:
    import tarifas_2027
except ModuleNotFoundError as error:
    print("ModuleNotFoundError:", error)
```

**Salida esperada:**

```plain text
Primera ruta de búsqueda: ejemplo_6_1_donde_busca_python
Número de rutas > 1: True
random se ha cargado desde: random.py
AttributeError: module 'random' has no attribute 'randint'
ModuleNotFoundError: No module named 'tarifas_2027'
```

---

> En Python 3.13 o posterior, el mensaje del `AttributeError` añade una sugerencia: renombrar el archivo porque tapa al módulo estándar.

---

**Highlights:**

>
1. `os.path.basename()` se queda solo con el último trozo de una ruta. Se usa para no mostrar la ruta completa, que es distinta en cada ordenador.
2. `sys.path[0]` es la carpeta del ejemplo: Python mira ahí **antes** que en la biblioteca estándar.
3. `random.__file__` delata el problema: se ha cargado **nuestro** `random.py`, que no tiene `randint()`.
4. La solución es **renombrar el archivo** (por ejemplo, `prueba_sorteo.py`) y **borrar la carpeta ****`__pycache__/`** que se creó con el nombre antiguo.
5. Cuando aparezca un `ModuleNotFoundError` con una librería externa, lo primero es comprobar que la terminal muestra `(.venv)`: si el entorno virtual no está activo, Python no mira en su `site-packages`.

---

# Sesión 2: Paquetes

## Sección 7. Definición de Paquete en Python

> Un **paquete** es una **carpeta que contiene módulos** y que Python trata como una unidad. Cuando el número de módulos crece, hace falta poner orden: agruparlos por funcionalidad o según la aplicación donde se usan. Python aprovecha para ello la **estructura de carpetas** del sistema operativo.

---

Ventajas de usar paquetes:

17. **Agrupan** distintos módulos bajo un mismo nombre y permiten crear **jerarquías** de módulos, subpaquetes y submódulos.
18. Permiten **distribuir** el código como una librería instalable, de forma que otros programas lo usen igual que un módulo estándar.
- La carpeta lleva un archivo especial **`__init__.py`**. Puede estar vacío. Marca la carpeta como paquete y se **ejecuta automáticamente** la primera vez que se importa algo del paquete.
- Los módulos de un paquete se importan con **puntos**, como una ruta: `paquete.modulo`.
- Un paquete puede contener otros paquetes (**subpaquetes**), cada uno con su propio `__init__.py`: `paquete.subpaquete.modulo`. La jerarquía puede crecer tanto como se necesite.
---

---

![Imagen](images/clase-22-programacion-modular-y-paquetes/image-003.png)

---

En la imagen, `app` es una carpeta normal con dos módulos, mientras que `paquete` y `paquete/subpaquete` son paquetes porque contienen `__init__.py`. El `modulo3.py` se importaría como `paquete.subpaquete.modulo3`.

---

**Imports absolutos y relativos**

| Tipo | Ejemplo | Cuándo se usa |
| --- | --- | --- |
| **Absoluto** | `from facturacion.modelos import Cliente` | Desde fuera del paquete (por ejemplo, en `main.py`). Siempre funciona |
| **Relativo** | `from .modelos import Cliente` | Desde **dentro** del paquete, para importar un módulo hermano. El punto significa «este mismo paquete» |

---

Los imports relativos solo funcionan cuando el módulo se usa **como parte del paquete**. Si se ejecuta directamente un archivo que los contiene (`python facturacion/factura.py`), Python lanza un `ImportError`.

### **El ****`__init__.py`**** como recepción del paquete**

En `__init__.py` se pueden importar las clases y funciones principales del paquete para que quien lo use escriba `from facturacion import Factura` en lugar de `from facturacion.factura import Factura`. También se suelen definir:

- `__version__`: la versión del paquete.
- `__all__`: la lista de nombres públicos, que es lo que se importa con `from paquete import *`.
---

### Sintaxis

```plain text
main.py
mi_paquete/
├── __init__.py
├── modulo_a.py
├── modulo_b.py
└── subpaquete/
    ├── __init__.py
    └── modulo_c.py
```

```python
# Imports absolutos (desde fuera del paquete)
import mi_paquete.modulo_a
import mi_paquete.modulo_a as ma
from mi_paquete.modulo_a import ClaseA
from mi_paquete import ClaseA           # si __init__.py la importa
from mi_paquete.subpaquete.modulo_c import funcion_c

# Imports relativos (desde dentro del paquete)
from .modulo_a import ClaseA            # módulo hermano
from . import modulo_a                  # el módulo completo

# __init__.py
from .modulo_a import ClaseA
__version__ = "1.0.0"
__all__ = ["ClaseA"]
```

---

### Ejemplo 7.1 · Un primer paquete de logística

> Una empresa de transporte agrupa su código de flota en un paquete `logistica` con dos módulos:
- `vehiculos.py`: la clase `Vehiculo` y sus derivadas `Furgoneta` y `Camion`, cada una con su coste por kilómetro.
- `rutas.py`: funciones puras para calcular la distancia y el coste de una ruta. Reciben cualquier vehículo y le piden su coste por kilómetro (polimorfismo).

El `__init__.py` está **vacío**. Desde `main.py` se importan los módulos del paquete de varias formas.

---

> 📁 `ejemplo_7_1_primer_paquete/`

```plain text
ejemplo_7_1_primer_paquete/
├── logistica/
│   ├── __init__.py      (vacío)
│   ├── vehiculos.py
│   └── rutas.py
└── main.py
```

---

Para crear el `__init__.py` vacío desde la terminal:

```powershell
New-Item logistica\__init__.py -ItemType File
```

---

**`logistica/vehiculos.py`**

```python
"""Vehículos de la flota."""


class Vehiculo:
    def __init__(self, matricula, capacidad_kg):
        self.matricula = matricula
        self.capacidad_kg = capacidad_kg

    def coste_por_km(self):
        return 0.0

    def puede_cargar(self, kg):
        return kg <= self.capacidad_kg

    def __str__(self):
        return f"{type(self).__name__}{self.matricula}"


class Furgoneta(Vehiculo):
    def coste_por_km(self):
        return 0.35


class Camion(Vehiculo):
    def coste_por_km(self):
        return 0.90
```

---

**`logistica/rutas.py`**

```python
"""Cálculos sobre rutas de reparto (funciones puras)."""


def distancia_total(tramos_km):
    return round(sum(tramos_km), 1)


def coste_ruta(vehiculo, tramos_km):
    return round(vehiculo.coste_por_km() * distancia_total(tramos_km), 2)
```

---

**`main.py`**

```python
import logistica
import logistica.rutas as rutas
from logistica.vehiculos import Furgoneta, Camion

flota = [Furgoneta("1234-KLM", 1200), Camion("5678-PQR", 18000)]
tramos = [120, 85.5, 40]
carga_kg = 3500

print("Distancia:", rutas.distancia_total(tramos), "km")
for vehiculo in flota:
    print(f"{vehiculo} ->{rutas.coste_ruta(vehiculo, tramos)} €")

aptos = [v.matricula for v in flota if v.puede_cargar(carga_kg)]
print(f"Aptos para{carga_kg} kg:", aptos)

print(type(logistica))
print(logistica.__name__, "|", rutas.__name__, "|", Furgoneta.__module__)
```

**Salida esperada:**

```plain text
Distancia: 245.5 km
  Furgoneta 1234-KLM -> 85.92 €
  Camion 5678-PQR -> 220.95 €
Aptos para 3500 kg: ['5678-PQR']
<class 'module'>
logistica | logistica.rutas | logistica.vehiculos
```

---

**Highlights:**

>
1. `logistica.vehiculos` se lee como una ruta: «el módulo `vehiculos` del paquete `logistica`».
2. Un paquete importado también es un objeto `module`. Su nombre completo aparece en `__name__` y en el `__module__` de sus clases: `logistica.vehiculos`.
3. `rutas.py` **no importa** `vehiculos.py`: no le hace falta. Solo llama a `coste_por_km()`, y cualquier objeto que tenga ese método sirve (polimorfismo).
4. El alias `import logistica.rutas as rutas` evita escribir `logistica.rutas.coste_ruta(...)` cada vez.

---

### Ejemplo 7.2 · Subpaquetes

> Se amplía el módulo de saludos del Ejemplo 2.1. Ahora el código se organiza en un paquete `paquete` con **dos subpaquetes**: `hola`, con el módulo `saludos.py`, y `adios`, con el módulo `despedidas.py`. Cada carpeta lleva su `__init__.py` **vacío**. Desde `main.py` se importa una función de un subpaquete y una clase del otro.

---

> 📁 `ejemplo_7_2_subpaquetes/`

```plain text
ejemplo_7_2_subpaquetes/
├── main.py
└── paquete/
    ├── __init__.py
    ├── hola/
    │   ├── __init__.py
    │   └── saludos.py
    └── adios/
        ├── __init__.py
        └── despedidas.py
```

---

**`paquete/hola/saludos.py`**

```python
def saludar():
    print("Hola, te estoy saludando desde la función saludar() "
          "del módulo saludos")


class Saludo:
    def __init__(self):
        print("Hola, te estoy saludando desde el __init__ "
              "de la clase Saludo")
```

---

**`paquete/adios/despedidas.py`**

```python
def despedir():
    print("Adiós, me estoy despidiendo desde la función despedir() "
          "del módulo despedidas")


class Despedida:
    def __init__(self):
        print("Adiós, me estoy despidiendo desde el __init__ "
              "de la clase Despedida")
```

---

**`main.py`**

```python
from paquete.hola.saludos import saludar
from paquete.adios.despedidas import Despedida

saludar()
Despedida()
```

**Salida esperada:**

```plain text
Hola, te estoy saludando desde la función saludar() del módulo saludos
Adiós, me estoy despidiendo desde el __init__ de la clase Despedida
```

---

**Highlights:**

>
1. La ruta del import sigue la ruta de carpetas: `paquete.hola.saludos` es el archivo `paquete/hola/saludos.py`.
2. Cada nivel de la jerarquía tiene su `__init__.py`, aunque esté vacío. Así queda claro qué carpetas son paquetes.
3. `main.py` está **al lado** de la carpeta `paquete`: por eso Python la encuentra (Sección 6).
4. Solo se importa lo que se usa: la función `despedir()` y la clase `Saludo` existen, pero `main.py` no las necesita.

---

### Ejemplo 7.3 · El `__init__.py` como recepción e imports relativos

> Una empresa de suministros para hostelería tiene un paquete `facturacion` con tres módulos que se usan entre sí:
- `modelos.py`: las clases `Cliente` y `LineaFactura`.
- `calculos.py`: funciones puras para la base imponible, el IVA y un **descuento por volumen** por tramos (5 % desde 1 000 € y 10 % desde 5 000 €), calculado con `reduce()`.
- `factura.py`: la clase `Factura`, que importa los otros dos módulos con **imports relativos**.
El `__init__.py` expone las clases principales, la versión del paquete y la lista `__all__`, de forma que `main.py` solo necesita `from facturacion import Cliente, Factura`.

---

> 📁 `ejemplo_7_3_init_e_imports_relativos/`

```plain text
ejemplo_7_3_init_e_imports_relativos/
├── facturacion/
│   ├── __init__.py
│   ├── modelos.py
│   ├── calculos.py
│   └── factura.py
└── main.py
```

---

**`facturacion/modelos.py`**

```python
"""Clases de datos de la facturación."""


class Cliente:
    def __init__(self, nif, nombre, tipo_iva=0.21):
        self.nif = nif
        self.nombre = nombre
        self.tipo_iva = tipo_iva


class LineaFactura:
    def __init__(self, concepto, unidades, precio_unitario):
        self.concepto = concepto
        self.unidades = unidades
        self.precio_unitario = precio_unitario

    @property
    def importe(self):
        return round(self.unidades * self.precio_unitario, 2)
```

---

**`facturacion/calculos.py`**

```python
"""Funciones puras para calcular importes."""

from functools import reduce

TRAMOS_DESCUENTO = [(1000, 0.05), (5000, 0.10)]       # (base mínima, porcentaje)


def base_imponible(lineas):
    return round(sum(linea.importe for linea in lineas), 2)


def descuento_por_volumen(base):
    porcentaje = reduce(
        lambda actual, tramo: tramo[1] if base >= tramo[0] else actual,
        TRAMOS_DESCUENTO,
        0.0,
    )
    return round(base * porcentaje, 2)


def cuota_iva(base, tipo):
    return round(base * tipo, 2)
```

---

**`facturacion/factura.py`**

```python
"""La clase Factura, que usa los otros módulos del paquete."""

from .modelos import Cliente, LineaFactura
from .calculos import base_imponible, descuento_por_volumen, cuota_iva


class Factura:
    _contador = 0

    def __init__(self, cliente):
        if not isinstance(cliente, Cliente):
            raise TypeError("Se esperaba un Cliente")
        Factura._contador += 1
        self.numero = f"F-{Factura._contador:04d}"
        self.cliente = cliente
        self.lineas = []

    def agregar_linea(self, concepto, unidades, precio_unitario):
        self.lineas.append(LineaFactura(concepto, unidades, precio_unitario))
        return self                                   # permite encadenar llamadas

    def total(self):
        base = base_imponible(self.lineas)
        base_neta = round(base - descuento_por_volumen(base), 2)
        return round(base_neta + cuota_iva(base_neta, self.cliente.tipo_iva), 2)

    def __str__(self):
        return f"{self.numero} |{self.cliente.nombre} | líneas:{len(self.lineas)} | total:{self.total()} €"
```

---

**`facturacion/__init__.py`**

```python
"""Paquete de facturación de la empresa."""

from .modelos import Cliente, LineaFactura
from .factura import Factura

__version__ = "1.0.0"
__all__ = ["Cliente", "LineaFactura", "Factura"]
```

---

**`main.py`**

```python
import facturacion
from facturacion import Cliente, Factura

print("Versión del paquete:", facturacion.__version__)

hosteleria = Cliente("B12345678", "Hostelería Levante SL")
panaderia = Cliente("A87654321", "Panadería Ortiz", tipo_iva=0.10)

f1 = (Factura(hosteleria)
      .agregar_linea("Cafetera industrial", 2, 950.00)
      .agregar_linea("Molinillo", 1, 320.00)
      .agregar_linea("Mantenimiento anual", 1, 180.00))
f2 = Factura(panaderia).agregar_linea("Amasadora", 1, 640.00)

for factura in [f1, f2]:
    print(factura)

print(facturacion.__all__)
print(Factura.__module__)
```

**Salida esperada:**

```plain text
Versión del paquete: 1.0.0
F-0001 | Hostelería Levante SL | líneas: 3 | total: 2758.8 €
F-0002 | Panadería Ortiz | líneas: 1 | total: 704.0 €
['Cliente', 'LineaFactura', 'Factura']
facturacion.factura
```

---

**Prueba adicional:** desde la carpeta del ejemplo, ejecuta directamente el módulo que contiene imports relativos:

```powershell
python facturacion\factura.py
```

**Salida esperada (última línea del error):**

```plain text
ImportError: attempted relative import with no known parent package
```

---

**Highlights:**

>
1. Gracias al `__init__.py`, `main.py` importa `Factura` desde `facturacion` sin saber en qué módulo interno está. Si mañana `Factura` se mueve a otro archivo del paquete, `main.py` **no cambia**.
2. Aun así, `Factura.__module__` revela su ubicación real: `facturacion.factura`.
3. Cálculo de `F-0001`: base 2 400 € → descuento del 5 % (120 €) → base neta 2 280 € → IVA del 21 % (478,80 €) → **2 758,80 €**. `F-0002` no llega a 1 000 €, así que no tiene descuento y lleva IVA del 10 %.
4. Dentro del paquete, `factura.py` usa `from .modelos import ...`. El punto significa «el paquete en el que estoy», así que el código no depende del nombre de la carpeta.
5. El `ImportError` de la prueba adicional ocurre porque, al ejecutar `factura.py` directamente, Python no sabe que pertenece a un paquete. Los módulos internos de un paquete **se importan, no se ejecutan**: el punto de entrada es `main.py`.
6. `agregar_linea()` devuelve `self`, lo que permite **encadenar** varias llamadas en una sola expresión. Los paréntesis alrededor de `f1 = (...)` permiten repartirla en varias líneas.

---

## Sección 8. La biblioteca estándar: módulos que ya vienen con Python

### Definición

> Python incluye cientos de módulos listos para usar, sin instalar nada: la **biblioteca estándar**. Se importan exactamente igual que los módulos propios. Algunos de los más usados en ingeniería de datos:

---

| Módulo | Para qué sirve | Ejemplos |
| --- | --- | --- |
| `math` | Funciones matemáticas | `math.ceil()`, `math.floor()`, `math.sqrt()` |
| `statistics` | Estadística básica | `statistics.mean()`, `statistics.median()`, `statistics.stdev()` |
| `collections` | Estructuras de datos especializadas | `Counter` (contar), `defaultdict`, `namedtuple` |
| `datetime` | Fechas y horas | `date`, `datetime`, `timedelta` |
| `functools` | Herramientas para funciones | `reduce()`, `partial()` |
| `itertools` | Herramientas para iteradores | `chain()`, `islice()`, `groupby()` |
| `random` | Números aleatorios | `random.randint()`, `random.choice()` |
| `os`, `sys` | Sistema operativo e intérprete | `os.path`, `sys.path` |

---

Las librerías **externas** (pandas, PySpark…) no vienen con Python: las publica la comunidad, se instalan con `pip install` dentro del `.venv` y se anotan en `requirements.txt`, como se hizo en la Clase 18. Una vez instaladas, se importan con la misma sintaxis.

Dónde consultarlas:

- Biblioteca estándar: [The Python Standard Library](https://docs.python.org/3/library/index.html) (también [en español](https://docs.python.org/es/3/library/index.html)).
- Librerías de terceros: [PyPI · The Python Package Index](https://pypi.org/).
---

### Sintaxis

```python
import math
import statistics
from collections import Counter
from datetime import date, timedelta
from functools import partial

partial(funcion, argumento=valor)     # nueva función con ese argumento ya fijado
```

---

### Ejemplo 8.1 · El cierre semanal de una cafetería

> Una cadena de cafeterías analiza los tickets de un local para preparar el pedido semanal. Se resuelven cinco tareas, cada una con un módulo distinto de la biblioteca estándar:
1. Los **dos productos más vendidos** (`collections.Counter`).
2. El **ticket medio** y la **mediana** (`statistics`).
3. Cuántos **sacos de café de 2 kg** pedir si se consumen 7,3 kg a la semana (`math.ceil`, que redondea hacia arriba).
4. La **fecha del próximo pedido**, una semana después del último (`datetime`).
5. Una función de IVA con el **tipo de hostelería (10 %) ya fijado**, a partir de una función general (`functools.partial`).

---

> 📁 `ejemplo_8_1_biblioteca_estandar/`

```plain text
ejemplo_8_1_biblioteca_estandar/
└── main.py
```

---

**`main.py`**

```python
import math
import statistics
from collections import Counter
from datetime import date, timedelta
from functools import partial

tickets = [("café", 1.40), ("tostada", 2.10), ("café", 1.40), ("zumo", 2.80),
           ("café", 1.40), ("tostada", 2.10), ("croissant", 1.80)]

# collections: contar sin escribir el bucle
mas_vendidos = Counter(producto for producto, _ in tickets)
print("Más vendidos:", mas_vendidos.most_common(2))

# statistics: medidas estadísticas
importes = [precio for _, precio in tickets]
print("Ticket medio:", round(statistics.mean(importes), 2),
      "| mediana:", statistics.median(importes))

# math: funciones matemáticas
consumo_kg, saco_kg = 7.3, 2
print("Sacos de café a pedir:", math.ceil(consumo_kg / saco_kg))

# datetime: fechas
ultimo_pedido = date(2026, 11, 10)
proximo_pedido = ultimo_pedido + timedelta(days=7)
print("Próximo pedido:", proximo_pedido.isoformat())

# functools: fijar argumentos de una función ya existente
def con_iva(importe, tipo):
    return round(importe * (1 + tipo), 2)

con_iva_hosteleria = partial(con_iva, tipo=0.10)
print("Con IVA del 10 %:", list(map(con_iva_hosteleria, [1.40, 2.10, 2.80])))
```

**Salida esperada:**

```plain text
Más vendidos: [('café', 3), ('tostada', 2)]
Ticket medio: 1.86 | mediana: 1.8
Sacos de café a pedir: 4
Próximo pedido: 2026-11-17
Con IVA del 10 %: [1.54, 2.31, 3.08]
```

---

**Highlights:**

>
1. `Counter` recibe una expresión generadora (Clase 21) y cuenta cuántas veces aparece cada producto. `most_common(2)` devuelve los dos primeros como pares `(producto, veces)`.
2. `math.ceil(3.65)` da `4`: aunque sobre algo de café, no se puede pedir medio saco.
3. Sumar un `timedelta` a una `date` da otra fecha: Python se encarga de los cambios de mes y de año.
4. `partial()` es una alternativa a las clausuras de la Clase 21: crea una función nueva a partir de otra, con algún argumento ya fijado. `con_iva_hosteleria` solo necesita el importe, así que encaja directamente en `map()`.
5. Antes de escribir una función de utilidad, conviene comprobar si la biblioteca estándar ya la tiene.

---

## Sección 9. Un proyecto modular completo: pipeline ETL

### Definición

> Un **pipeline ETL** (*Extract, Transform, Load*) es el proceso típico de la ingeniería de datos:
1. **Extracción**: leer los datos en bruto de su origen.
2. **Transformación**: limpiar, validar y convertir los datos.
3. **Carga**: guardar el resultado donde se va a consultar.
Cada etapa es una responsabilidad distinta, así que encaja de forma natural en **un módulo por etapa**, agrupados en un paquete.

---

**Buenas prácticas de organización**

| Práctica | Por qué |
| --- | --- |
| **Un módulo, una responsabilidad** | Si el nombre de un módulo necesita un «y» (`clientes_y_facturas.py`), probablemente son dos módulos |
| Nombres de módulos en **minúsculas con guiones bajos** (`snake_case`), sin espacios ni tildes | Son nombres de variables para Python: `import mis datos` no es válido |
| Imports **al principio** del archivo, en tres bloques separados por una línea en blanco: 1) biblioteca estándar, 2) librerías externas, 3) módulos propios | Es lo que recomienda la guía PEP 8: de un vistazo se ve de qué depende el archivo |
| Evitar `from modulo import *` | No se sabe qué nombres entran ni de dónde vienen |
| Los módulos **solo definen**; el código que se ejecuta va en `main()` bajo `if __name__ == "__main__":` | Importar un módulo no debe tener efectos inesperados |
| Evitar **imports circulares** (A importa B y B importa A) | Python puede encontrarse un módulo a medio cargar y lanzar `ImportError`. Suele indicar que hay que sacar lo común a un tercer módulo |
| Nombres internos con **un guion bajo** (`_es_decimal`) | Convención de la Clase 19: indica que es un detalle interno del módulo y no forma parte de lo que ofrece |

---

### Sintaxis

> La estructura habitual del programa principal (`main.py`) es: primero los imports, ordenados en tres bloques; después el código propio (funciones y clases); y al final el punto de entrada real, protegido con `if __name__ == "__main__":`.

---

Estructura del programa principal

![Imagen](images/clase-22-programacion-modular-y-paquetes/image-004.png)

---

Aplicada a un archivo real:

```python
"""Docstring del módulo: qué hace este archivo."""

# 1. Biblioteca estándar
import math
from datetime import date

# 2. Librerías externas (instaladas con pip)
# import pandas as pd

# 3. Módulos propios
from mi_paquete import mi_funcion


def main():
    ...


if __name__ == "__main__":
    main()
```

---

### Ejemplo 9.1 · Pipeline de ventas de una cadena de tiendas

> Una cadena de tiendas de café e infusiones recibe cada noche las ventas de sus locales en un texto con formato CSV. Los datos llegan **sucios**: espacios sobrantes, mayúsculas mezcladas y algunas filas con las unidades escritas en letra o vacías.

Se construye el paquete `pipeline_ventas` con un módulo por responsabilidad:

---

| Módulo | Responsabilidad | Técnica principal |
| --- | --- | --- |
| `modelos.py` | Clase `Venta` | OOP |
| `extraccion.py` | Entregar las líneas de datos una a una | Generador |
| `transformacion.py` | Limpiar, validar y convertir a objetos `Venta` | Funciones puras + `map()` / `filter()` |
| `carga.py` | Guardar las ventas y responder consultas | Clase `AlmacenVentas` |
| `orquestador.py` | Unir las tres etapas | Composición de funciones |
| `__init__.py` | Exponer solo `ejecutar_pipeline()` | `__all__` |

`main.py` solo ejecuta el pipeline y muestra los resultados.

---

> 📁 `ejemplo_9_1_pipeline_modular/`

```plain text
ejemplo_9_1_pipeline_modular/
├── pipeline_ventas/
│   ├── __init__.py
│   ├── modelos.py
│   ├── extraccion.py
│   ├── transformacion.py
│   ├── carga.py
│   └── orquestador.py
└── main.py
```

---

**`pipeline_ventas/modelos.py`**

```python
"""Clases de datos del pipeline."""


class Venta:
    def __init__(self, tienda, producto, unidades, precio):
        self.tienda = tienda
        self.producto = producto
        self.unidades = unidades
        self.precio = precio

    @property
    def importe(self):
        return round(self.unidades * self.precio, 2)

    def __repr__(self):
        return f"Venta({self.tienda},{self.producto},{self.importe})"
```

---

**`pipeline_ventas/extraccion.py`**

```python
"""Extracción: lee los registros en bruto sin cargarlos todos a la vez."""


def leer_registros(texto):
    lineas = texto.strip().split("\n")
    for linea in lineas[1:]:                  # se salta la cabecera
        yield linea
```

---

**`pipeline_ventas/transformacion.py`**

```python
"""Transformación: funciones puras que limpian y convierten los registros."""

from .modelos import Venta


def parsear(linea):
    return [campo.strip() for campo in linea.split(",")]


def _es_decimal(texto):
    try:
        float(texto)
        return True
    except ValueError:
        return False


def es_valido(campos):
    return len(campos) == 4 and campos[2].isdigit() and _es_decimal(campos[3])


def a_venta(campos):
    tienda, producto, unidades, precio = campos
    return Venta(tienda.title(), producto.lower(), int(unidades), float(precio))


def transformar(lineas):
    campos = map(parsear, lineas)
    validos = filter(es_valido, campos)
    return map(a_venta, validos)
```

---

**`pipeline_ventas/carga.py`**

```python
"""Carga: almacena las ventas y ofrece consultas."""


class AlmacenVentas:
    def __init__(self):
        self._ventas = []

    def cargar(self, ventas):
        for venta in ventas:
            self._ventas.append(venta)

    def __len__(self):
        return len(self._ventas)

    def total_por_tienda(self):
        totales = {}
        for venta in self._ventas:
            totales[venta.tienda] = round(totales.get(venta.tienda, 0) + venta.importe, 2)
        return totales

    def top_productos(self, n):
        totales = {}
        for venta in self._ventas:
            totales[venta.producto] = round(totales.get(venta.producto, 0) + venta.importe, 2)
        return sorted(totales.items(), key=lambda par: par[1], reverse=True)[:n]
```

---

**`pipeline_ventas/orquestador.py`**

```python
"""Orquestador: une las tres etapas del pipeline."""

from .extraccion import leer_registros
from .transformacion import transformar
from .carga import AlmacenVentas


def ejecutar_pipeline(texto):
    almacen = AlmacenVentas()
    almacen.cargar(transformar(leer_registros(texto)))
    return almacen
```

---

**`pipeline_ventas/__init__.py`**

```python
"""Pipeline ETL de ventas: extracción, transformación y carga."""

from .orquestador import ejecutar_pipeline

__all__ = ["ejecutar_pipeline"]
```

---

**`main.py`**

```python
"""Punto de entrada del pipeline de ventas."""

from pipeline_ventas import ejecutar_pipeline

DATOS = """tienda,producto,unidades,precio
madrid, Café Molido ,3,4.50
barcelona,té verde,2,3.20
madrid,café molido,1,4.50
valencia,cacao,dos,2.80
barcelona,Café Molido,4,4.50
sevilla,té verde,,3.20
valencia,cacao,5,2.80
"""


def main():
    almacen = ejecutar_pipeline(DATOS)
    print("Ventas cargadas:", len(almacen))
    print("Total por tienda:", almacen.total_por_tienda())
    print("Top 2 productos:", almacen.top_productos(2))


if __name__ == "__main__":
    main()
```

**Salida esperada:**

```plain text
Ventas cargadas: 5
Total por tienda: {'Madrid': 18.0, 'Barcelona': 24.4, 'Valencia': 14.0}
Top 2 productos: [('café molido', 36.0), ('cacao', 14.0)]
```

---

**Highlights:**

>
1. De 7 filas se cargan 5: la de Valencia con unidades `dos` y la de Sevilla con unidades vacías no pasan `es_valido()`. Por eso Sevilla no aparece en los totales.
2. `" Café Molido "`, `"café molido"` y `"Café Molido"` acaban siendo el mismo producto gracias a `strip()` y `lower()` en la transformación.
3. Toda la cadena es **perezosa** (Clase 21): `leer_registros()` es un generador y `transformar()` devuelve un `map`. Ninguna línea se procesa hasta que `AlmacenVentas.cargar()` recorre el resultado, y nunca se guarda una lista intermedia.
4. `main.py` **no conoce** las etapas internas: solo importa `ejecutar_pipeline`. Se podría cambiar por completo cómo se transforman los datos sin tocar `main.py`.
5. `_es_decimal()` lleva guion bajo porque es un detalle interno de `transformacion.py`. Fíjate en que el `__init__.py` tampoco lo expone.
6. Cada módulo se puede probar por separado. Por ejemplo, `transformacion.parsear(" madrid ,cacao,5,2.80")` se comprueba sin necesitar ni la extracción ni la carga.
7. Esta misma estructura (un paquete con extracción, transformación y carga, y un `main.py` que lo lanza) es la que se usará en los proyectos de datos del máster, cambiando el texto de ejemplo por ficheros, bases de datos o Spark.

---

# Ejemplo 9.2 : del notebook a producción

En la clase se dijo que en ingeniería de datos **todo el código de producción es modular**: un pipeline se reparte en módulos de **extracción**, **transformación** y **carga**. Este ejemplo lo muestra de principio a fin: se parte de un análisis hecho en un **notebook de Jupyter** (`.ipynb`) y se convierte, paso a paso, en un **proyecto modular** listo para ejecutarse en producción. 

---

## Sección 1. El punto de partida: un notebook

### Contexto

> **FrescoYa** es un supermercado online que reparte en Madrid, Sevilla y Valencia. Una analista de datos ha preparado en un notebook el **informe diario de ventas por ciudad**:
1. Lee los pedidos del día, que llegan en formato CSV.
2. Descarta los pedidos con el importe vacío o mal escrito.
3. Descarta los pedidos cancelados.
4. Calcula el importe de cada pedido con un **21 % de IVA**.
5. Suma las ventas por ciudad, de mayor a menor.

---

El notebook funciona, y el informe gusta tanto que la dirección pide que se **ejecute automáticamente cada noche**. Es el momento de llevarlo a producción.

> En un proyecto real, los pedidos llegarían de un fichero, una base de datos o una API. Aquí se escriben en un texto dentro del código para que el ejemplo se pueda ejecutar sin nada más.

---

### El notebook `informe_ventas.ipynb`

Un notebook se ejecuta **celda a celda**, y cada celda muestra su salida debajo.

**Celda [1]** · Cargar los datos

```python
datos = """id,cliente,ciudad,importe,estado
P001, Ana López ,madrid,45.50,entregado
P002,Luis Pérez,Sevilla,12.00,cancelado
P003,Marta Ruiz,MADRID,30.25,entregado
P004,Jorge Gil,valencia,,entregado
P005,Elena Sanz,sevilla,80.00,entregado
P006,Pablo Ríos,Valencia,22.40,en reparto
P007,Sara Mora,madrid,abc,entregado"""
lineas = datos.split("\n")[1:]
print("Pedidos leídos:", len(lineas))
```

```plain text
Pedidos leídos: 7
```

**Celda [2]** · Limpiar y descartar errores

```python
filas = []
rechazados = []
for l in lineas:
    c = [x.strip() for x in l.split(",")]
    try:
        imp = float(c[3])
        filas.append([c[0], c[1].title(), c[2].title(), imp, c[4].lower()])
    except ValueError:
        rechazados.append(c[0])
print("Rechazados por datos erróneos:", rechazados)
```

```plain text
Rechazados por datos erróneos: ['P004', 'P007']
```

**Celda [3]** · Quitar cancelados y calcular el IVA

```python
cancelados = [f[0] for f in filas if f[4] == "cancelado"]
filas = [f for f in filas if f[4] != "cancelado"]
for f in filas:
    f.append(round(f[3] * 1.21, 2))
print("Pedidos cancelados:", cancelados)
print("Pedidos procesados:", len(filas))
```

```plain text
Pedidos cancelados: ['P002']
Pedidos procesados: 4
```

**Celda [4]** · Agregar por ciudad

```python
resumen = {}
for f in filas:
    resumen[f[2]] = round(resumen.get(f[2], 0) + f[5], 2)
resumen = dict(sorted(resumen.items(), key=lambda x: x[1], reverse=True))
```

**Celda [5]** · Mostrar el informe

```python
print("Ventas con IVA por ciudad:")
for ciudad, total in resumen.items():
    print(f"  {ciudad:<9}{total:>8.2f} €")
```

```plain text
Ventas con IVA por ciudad:
  Sevilla     96.80 €
  Madrid      91.65 €
  Valencia    27.10 €
```

---

## Sección 2. Por qué este notebook no puede ir a producción tal cual

> El notebook es perfecto para **explorar** datos y probar ideas. Pero tiene problemas cuando el código se tiene que ejecutar solo, todas las noches y durante años:

| Problema en el notebook | Dónde se ve | Consecuencia en producción |
| --- | --- | --- |
| **Depende del orden de ejecución** | La celda 4 usa `f[5]`, una columna que solo existe si antes se ejecutó la celda 3. Si se salta, falla con `IndexError`; si se repite la 3, cada pedido acumula columnas de IVA duplicadas | Resultados o errores distintos según quién lo ejecute y cómo |
| **Todo son variables globales** | `filas`, `resumen` y `rechazados` viven en el notebook y cualquier celda puede cambiarlas | Errores difíciles de encontrar (son funciones impuras, Clase 21) |
| **Números «mágicos» repartidos** | El `1.21` del IVA y el texto `"cancelado"` están escritos dentro del código | Si cambia el IVA, hay que buscarlo celda a celda |
| **Datos sin estructura** | Un pedido es una lista: `f[2]` es la ciudad y `f[5]` el total con IVA | Nadie recuerda qué es `f[5]`, y añadir un campo descoloca todos los índices |
| **Nada se puede reutilizar** | La limpieza solo existe dentro de este notebook | Otro informe que necesite limpiar pedidos tiene que copiar y pegar |
| **No se puede probar por partes** | La validación está mezclada con la lectura y la limpieza | No se puede comprobar una regla sin ejecutarlo todo |
| **Difícil de automatizar** | Un `.ipynb` está pensado para abrirse y ejecutarse a mano | Las herramientas de automatización lanzan programas `.py` con un punto de entrada claro |

---

## Sección 3. Paso a paso de la conversión

| Paso | Qué se hace | Dónde acaba |
| --- | --- | --- |
| 1 | Identificar las **etapas** del notebook: qué celdas extraen, cuáles transforman y cuáles cargan | Un módulo por etapa |
| 2 | Sacar los números y textos fijos a un **módulo de configuración** | `config.py` |
| 3 | Sustituir las listas por posiciones (`f[2]`, `f[5]`) por una **clase** con atributos con nombre | `modelos.py` |
| 4 | Convertir las celdas de limpieza en **funciones puras** que reciben datos y devuelven datos nuevos | `transformacion.py` |
| 5 | Llevar la agregación a una **clase** que guarda los pedidos y responde consultas | `carga.py` |
| 6 | Escribir una función que una las etapas **siempre en el mismo orden** | `orquestador.py` |
| 7 | Agrupar todo en un **paquete** y exponer solo lo necesario | `etl/__init__.py` |
| 8 | Crear el **punto de entrada** con `main()` y `if __name__ == "__main__":` | `main.py` |
| 9 | Comprobar que la versión modular da **exactamente la misma salida** que el notebook | Ejecución final |

Correspondencia entre celdas y módulos:

| Celda del notebook | Módulo de producción |
| --- | --- |
| Celda 1: cargar los datos | `extraccion.py` |
| Celda 2: limpiar y descartar errores | `transformacion.py` → `parsear()`, `es_valido()`, `a_pedido()` |
| Celda 3: quitar cancelados y calcular el IVA | `transformacion.py` → `transformar()` y `modelos.py` → `Pedido.total_con_iva` |
| Celda 4: agregar por ciudad | `carga.py` → `ResumenVentas.por_ciudad()` |
| Celda 5: mostrar el informe | `main.py` → `mostrar_informe()` |
| El `1.21` y el texto `"cancelado"` | `config.py` |

---

## Sección 4. El proyecto modular

### Estructura

```plain text
pedidos_etl/
├── main.py                ← punto de entrada
└── etl/                   ← paquete del pipeline
    ├── __init__.py
    ├── config.py          ← reglas de negocio configurables
    ├── modelos.py         ← clase Pedido
    ├── extraccion.py      ← E: obtener los datos
    ├── transformacion.py  ← T: limpiar, validar y convertir
    ├── carga.py           ← L: guardar y resumir
    └── orquestador.py     ← une E, T y L
```

---

### `etl/config.py`

```python
"""Parámetros del pipeline. Si cambia una regla de negocio, se cambia aquí."""

IVA = 0.21
ESTADO_CANCELADO = "cancelado"
```

### `etl/modelos.py`

```python
"""Clases de datos del pipeline."""

from .config import IVA


class Pedido:
    def __init__(self, id_pedido, cliente, ciudad, importe, estado):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.ciudad = ciudad
        self.importe = importe
        self.estado = estado

    @property
    def total_con_iva(self):
        return round(self.importe * (1 + IVA), 2)

    def __repr__(self):
        return f"Pedido({self.id_pedido}, {self.ciudad}, {self.total_con_iva})"
```

### `etl/extraccion.py`

```python
"""Extracción: obtiene las líneas de datos en bruto, sin la cabecera."""


def leer_lineas(texto):
    return texto.strip().split("\n")[1:]
```

### `etl/transformacion.py`

```python
"""Transformación: funciones puras que limpian, validan y convierten los datos."""

from .config import ESTADO_CANCELADO
from .modelos import Pedido


def parsear(linea):
    return [campo.strip() for campo in linea.split(",")]


def es_valido(campos):
    if len(campos) != 5:
        return False
    try:
        float(campos[3])
        return True
    except ValueError:
        return False


def a_pedido(campos):
    id_pedido, cliente, ciudad, importe, estado = campos
    return Pedido(id_pedido, cliente.title(), ciudad.title(), float(importe), estado.lower())


def transformar(lineas):
    registros = list(map(parsear, lineas))
    rechazados = [r[0] for r in registros if not es_valido(r)]
    pedidos = [a_pedido(r) for r in registros if es_valido(r)]
    cancelados = [p.id_pedido for p in pedidos if p.estado == ESTADO_CANCELADO]
    activos = list(filter(lambda p: p.estado != ESTADO_CANCELADO, pedidos))
    return activos, rechazados, cancelados
```

### `etl/carga.py`

```python
"""Carga: guarda los pedidos procesados y genera el resumen."""


class ResumenVentas:
    def __init__(self):
        self._pedidos = []

    def cargar(self, pedidos):
        self._pedidos.extend(pedidos)

    def __len__(self):
        return len(self._pedidos)

    def por_ciudad(self):
        totales = {}
        for pedido in self._pedidos:
            totales[pedido.ciudad] = round(totales.get(pedido.ciudad, 0) + pedido.total_con_iva, 2)
        return dict(sorted(totales.items(), key=lambda par: par[1], reverse=True))
```

### `etl/orquestador.py`

```python
"""Orquestador: une las tres etapas del pipeline en el orden correcto."""

from .extraccion import leer_lineas
from .transformacion import transformar
from .carga import ResumenVentas


def ejecutar_pipeline(texto):
    lineas = leer_lineas(texto)
    activos, rechazados, cancelados = transformar(lineas)
    resumen = ResumenVentas()
    resumen.cargar(activos)
    return {
        "leidos": len(lineas),
        "rechazados": rechazados,
        "cancelados": cancelados,
        "resumen": resumen,
    }
```

### `etl/__init__.py`

```python
"""Pipeline ETL de pedidos online: extracción, transformación y carga."""

from .orquestador import ejecutar_pipeline

__all__ = ["ejecutar_pipeline"]
```

### `main.py`

```python
"""Punto de entrada del pipeline de pedidos."""

from etl import ejecutar_pipeline

# En producción, estos datos llegarían de un fichero, una base de datos o una API
DATOS = """id,cliente,ciudad,importe,estado
P001, Ana López ,madrid,45.50,entregado
P002,Luis Pérez,Sevilla,12.00,cancelado
P003,Marta Ruiz,MADRID,30.25,entregado
P004,Jorge Gil,valencia,,entregado
P005,Elena Sanz,sevilla,80.00,entregado
P006,Pablo Ríos,Valencia,22.40,en reparto
P007,Sara Mora,madrid,abc,entregado"""


def mostrar_informe(resultado):
    print("Pedidos leídos:", resultado["leidos"])
    print("Rechazados por datos erróneos:", resultado["rechazados"])
    print("Pedidos cancelados:", resultado["cancelados"])
    print("Pedidos procesados:", len(resultado["resumen"]))
    print("Ventas con IVA por ciudad:")
    for ciudad, total in resultado["resumen"].por_ciudad().items():
        print(f"  {ciudad:<9}{total:>8.2f} €")


def main():
    resultado = ejecutar_pipeline(DATOS)
    mostrar_informe(resultado)


if __name__ == "__main__":
    main()
```

---

### Ejecución

```powershell
cd pedidos_etl
python main.py
```

**Salida esperada:**

```plain text
Pedidos leídos: 7
Rechazados por datos erróneos: ['P004', 'P007']
Pedidos cancelados: ['P002']
Pedidos procesados: 4
Ventas con IVA por ciudad:
  Sevilla     96.80 €
  Madrid      91.65 €
  Valencia    27.10 €
```

Es **exactamente la misma salida** que la del notebook. Modularizar no cambia lo que hace el programa: cambia cómo está organizado.

---

### Highlights:

>
1. **Cada etapa en su módulo.** `extraccion.py`, `transformacion.py` y `carga.py` son la E, la T y la L del pipeline. Si mañana los pedidos llegan de una base de datos en lugar de un texto, solo cambia `extraccion.py`.
2. **Las reglas de negocio en un solo sitio.** El IVA está en `config.py` y lo usa la clase `Pedido`. Si cambia, se modifica una línea.
3. **Una clase en lugar de posiciones.** `pedido.ciudad` y `pedido.total_con_iva` se entienden solos; `f[2]` y `f[5]` no. Además, el total con IVA es una `@property` que **se calcula** cuando se pide: no es una columna que se añade a mano y que puede faltar o duplicarse según el orden de las celdas.
4. **Funciones puras en la transformación.** `parsear()`, `es_valido()` y `a_pedido()` no modifican nada fuera de ellas. `transformar()` las combina con `map()`, comprehensions y `filter()` con una `lambda`.
5. **El orden lo fija el código.** En el notebook, el orden dependía de quién pulsaba las celdas. En producción lo fija `ejecutar_pipeline()`, y siempre es el mismo.
6. **Una sola puerta de entrada.** `main.py` solo importa `ejecutar_pipeline` y no necesita saber cómo está hecho el pipeline por dentro.
7. **Listo para automatizar.** Programar la ejecución nocturna consiste en lanzar `python main.py`. Gracias a `if __name__ == "__main__":`, el paquete también se puede importar desde otros programas sin que se ejecute nada.
8. **Mejoras en un único sitio.** Al separar `es_valido()`, se ha añadido una comprobación que el notebook no tenía: que cada línea tenga exactamente 5 campos (Sección 5). Con estos datos la salida no cambia, pero el pipeline es más robusto.

---

## Sección 5. Probar una pieza por separado

> Una ventaja directa de la versión modular es que cada función se puede probar **sin ejecutar el pipeline completo**. Por ejemplo: ¿qué pasa si alguien escribe el importe con **coma decimal**? Con una coma de más, la línea se parte en 6 campos en lugar de 5.

Desde la carpeta `pedidos_etl`, en un archivo de pruebas o en la consola de Python:

```python
from etl.transformacion import parsear, es_valido

print(es_valido(parsear("P010,Rosa Vidal,bilbao,19.95,entregado")))
print(es_valido(parsear("P009,Rosa Vidal,bilbao,9,95,entregado")))
print(es_valido(parsear("P011,Iván Paz,bilbao,,entregado")))
```

**Salida esperada:**

```plain text
True
False
False
```

En el notebook, la línea de `P009` habría pasado la validación: tomaría `9` como importe y `95` como estado, sin dar ningún error, y el pedido se sumaría con un importe equivocado. Encontrar ese fallo habría obligado a revisar todas las celdas.

---

## Sección 6. ¿Y el notebook? Sigue siendo útil

> El notebook **no se tira**: sigue siendo la mejor herramienta para explorar datos, probar ideas y hacer gráficos. Lo que cambia es su papel:

|  | Notebook (`.ipynb`) | Proyecto modular (`.py`) |
| --- | --- | --- |
| Para qué | Explorar, analizar, prototipar | Ejecutar en producción de forma automática y repetible |
| Quién lo ejecuta | Una persona, celda a celda | Un programador de tareas, siempre igual |
| Dónde viven las reglas | Repartidas por las celdas | En módulos con nombre, en un solo sitio |
| Cómo se reutiliza | Copiando y pegando | Importando |

La práctica habitual en los equipos de datos es que, una vez existe el paquete, **el notebook lo importa** en lugar de repetir el código. Si el notebook está en la carpeta `pedidos_etl`, una celda podría ser:

```python
from etl import ejecutar_pipeline

resultado = ejecutar_pipeline(datos)
resultado["resumen"].por_ciudad()
```

Así, el análisis del notebook y el proceso de producción usan **las mismas reglas**, y un cambio en el paquete llega a los dos.

---

## Sección 7. Lo que viene después

> Más adelante en el máster, los pipelines trabajarán con volúmenes de datos mucho mayores y con herramientas específicas de Big Data. La organización será **la misma** que en este ejemplo:
- Un **paquete** con un módulo por etapa.
- Las **reglas de negocio** en configuración.
- La **transformación** como funciones que reciben datos y devuelven datos nuevos.
- Un **orquestador** que une las etapas y un **`main.py`** como punto de entrada.
Cambiará **qué hay dentro** de cada módulo, no **cómo se organizan**. Por eso aprender a modularizar ahora con Python puro es la base de todo lo que viene.

