class Mensaje:
    ROLES_VALIDOS = ("system", "user", "assistant")

    def __init__(self, rol, contenido):
        self.rol = rol
        self.contenido = contenido

    def tokens(self):
        return len(self.contenido.split())

    def a_dict(self):
        return {"role": self.rol, "content": self.contenido}

    def __str__(self):
        return f"[{self.rol}] {self.contenido}"


class Conversacion:
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens
        self.__mensajes = []

    def agregar(self, rol, contenido):
        if rol not in Mensaje.ROLES_VALIDOS:
            return False
        nuevo_mensaje = Mensaje(rol, contenido)
        self.__mensajes.append(nuevo_mensaje)
        self._recortar()
        return True

    def __iadd__(self, tupla):
        rol, contenido = tupla
        self.agregar(rol, contenido)
        return self

    def tokens_totales(self):
        return sum(m.tokens() for m in self.__mensajes)

    def _recortar(self):
        while self.tokens_totales() > self.max_tokens and len(self.__mensajes) > 1:
            # Buscar el mensaje más antiguo que no sea "system"
            for i, m in enumerate(self.__mensajes):
                if m.rol != "system":
                    self.__mensajes.pop(i)
                    break

    def __len__(self):
        return len(self.__mensajes)

    def __contains__(self, palabra):
        palabra_lower = palabra.lower()
        return any(palabra_lower in m.contenido.lower() for m in self.__mensajes)

    def para_api(self):
        return [m.a_dict() for m in self.__mensajes]

    def __str__(self):
        return "\n".join(str(m) for m in self.__mensajes)


# Código de prueba
conv = Conversacion(max_tokens=30)
conv += ("system", "Eres el asistente de siniestros de Seguros Brisamar")
conv += ("user", "Quiero dar un parte de mi coche")
conv += ("assistant", "Claro, ¿cuál es la matrícula del vehículo?")
print(conv.agregar("cliente", "Hola"))
print(len(conv), conv.tokens_totales())
conv += ("user", "Es la 4821 KLM y el golpe fue en un parking")
print(len(conv), conv.tokens_totales())
print(conv)
print("matrícula" in conv, "COCHE" in conv)
print(conv.para_api()[0])