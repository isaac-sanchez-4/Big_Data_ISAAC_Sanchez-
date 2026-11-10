class ReglaCalidad:
    def __init__(self, columna, tipo, obligatoria=True, minimo=None):
        self.columna = columna
        self.tipo = tipo
        self.obligatoria = obligatoria
        self.minimo = minimo

    def comprobar(self, registro):
        if self.columna not in registro or registro[self.columna] is None:
            if self.obligatoria:
                return f"{self.columna}: falta"
            return None
        
        valor = registro[self.columna]
        if type(valor).__name__ != self.tipo:
            return f"{self.columna}: se esperaba {self.tipo}"
        
        if self.minimo is not None and valor < self.minimo:
            return f"{self.columna}: menor que {self.minimo}"
        
        return None

    def __repr__(self):
        opcional_str = "?" if not self.obligatoria else ""
        minimo_str = f">={self.minimo}" if self.minimo is not None else ""
        return f"Regla({self.columna}:{self.tipo}{minimo_str}{opcional_str})"


class ValidadorLote:
    def __init__(self, nombre):
        self.nombre = nombre
        self.__reglas = []
        self.validos = []
        self.rechazadas = []

    def __iadd__(self, regla):
        self.__reglas.append(regla)
        return self

    def __len__(self):
        return len(self.__reglas)

    def validar(self, registro):
        errores = []
        for regla in self.__reglas:
            err = regla.comprobar(registro)
            if err:
                errores.append(err)
        return errores

    def procesar(self, lote):
        self.validos = []
        self.rechazadas = []
        for reg in lote:
            errs = self.validar(reg)
            if not errs:
                self.validos.append(reg)
            else:
                self.rechazadas.append((reg, errs))

    def tasa_calidad(self):
        total = len(self.validos) + len(self.rechazadas)
        if total == 0:
            return 100.0
        return round((len(self.validos) / total) * 100, 1)

    def __str__(self):
        total = len(self.validos) + len(self.rechazadas)
        lineas = [
            f"Validador {self.nombre} · {len(self)} reglas",
            f"Válidos: {len(self.validos)} | Rechazados: {len(self.rechazadas)} | Calidad: {self.tasa_calidad()} %"
        ]
        for reg, errs in self.rechazadas:
            id_ped = reg.get("id_pedido", "N/A")
            lineas.append(f"- {id_ped}: {'; '.join(errs)}")
        return "\n".join(lineas)


# Código de prueba
validador = ValidadorLote("pedidos_silver")
validador += ReglaCalidad("id_pedido", "int")
validador += ReglaCalidad("cliente", "str")
validador += ReglaCalidad("importe", "float", minimo=0.01)
validador += ReglaCalidad("unidades", "int", minimo=1)
validador += ReglaCalidad("cupon", "str", obligatoria=False)
lote = [
    {"id_pedido": 5001, "cliente": "C-17", "importe": 89.9, "unidades": 2},
    {"id_pedido": 5002, "cliente": "C-03", "importe": "45,00", "unidades": 1},
    {"id_pedido": 5003, "importe": 12.5, "unidades": 0, "cupon": "BF26"},
    {"id_pedido": 5004, "cliente": "C-17", "importe": 230.0, "unidades": 4, "cupon": "BF26"},
    {"id_pedido": 5005, "cliente": "C-88", "importe": -5.0, "unidades": 1, "cupon": 10},
]
validador.procesar(lote)
print(validador)
print([r["id_pedido"] for r in validador.validos])
print(ReglaCalidad("importe", "float", minimo=0.01), ReglaCalidad("cupon", "str", obligatoria=False))