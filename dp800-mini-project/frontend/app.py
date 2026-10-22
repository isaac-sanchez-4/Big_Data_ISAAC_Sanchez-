import streamlit as st
import requests
import json
import time

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Tutor Inteligente DP-800",
    page_icon="",
    layout="centered"
)

st.title("Tutor DP-800")
st.caption("Asistente RAG conectado a SQL Server 2025 Vector Search & Llama 3")

API_URL = "http://localhost:8000/chat"


def dibujar_desplegable_telemetria(telemetria_dict):
    """
    Dibuja un  desplegable con toda la telemetría y las fuentes del PDf
    """
    if not telemetria_dict or telemetria_dict.get("tipo") != "rag":
        return

    t_sql = telemetria_dict.get("tiempo_sql_ms", 0)
    t_total = telemetria_dict.get("tiempo_total_s", 0)
    fuentes = telemetria_dict.get("fuentes", [])
    query_sql = telemetria_dict.get("query_ejecutada", "")

    paginas_unicas = sorted(list(set(str(f["pagina"]) for f in fuentes)))
    resumen_titulo = f"Telemetría y Fuentes SQL Server ({t_sql} ms | {len(fuentes)} fragmentos | Págs: {', '.join(paginas_unicas[:5])})"

    with st.expander(resumen_titulo, expanded=False):
        tab_metricas, tab_fuentes = st.tabs(["Telemetría de Ejecución", f"Fragmentos del PDF ({len(fuentes)})"])

        with tab_metricas:
            col1, col2, col3 = st.columns(3)
            col1.metric("Búsqueda SQL Server", f"{t_sql} ms")
            col2.metric("Tiempo Total (RAG+LLM)", f"{t_total} s")
            col3.metric("Vectores Recuperados", f"Top {len(fuentes)}")
            st.markdown("**Consulta vectorial procesada:**")
            st.code(query_sql, language="text")

        with tab_fuentes:
            for idx, f in enumerate(fuentes, 1):
                dist_txt = f" — Distancia Coseno: `{f['distancia']}`" if f.get("distancia") is not None else ""
                st.markdown(f"**Fragmento #{idx}** | 📄 `{f['archivo']}` (Página **{f['pagina']}**){dist_txt}")
                st.caption(f["extracto"])
                if idx < len(fuentes):
                    st.divider()


# BARRA LATERAL
with st.sidebar:
    st.header("Panel de Control")
    if st.button("Nueva Sesión / Limpiar Chat", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

    st.divider()
    st.markdown("### Arquitectura Activa")
    st.markdown("- **Base de Datos:** `SQL Server 2025`")
    st.markdown("- **Tipo Nativo:** `VECTOR(768)`")
    st.markdown("- **Embeddings:** `nomic-embed-text`")
    st.markdown("- **LLM:** `Llama 3 (Temp 0.0)`")

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Renderizar historial de conversación
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])
        if mensaje.get("telemetria_data"):
            dibujar_desplegable_telemetria(mensaje["telemetria_data"])

# ENTRADA DEL USUARIO Y STREAMING EN VIVO
if pregunta := st.chat_input("Escribe una pregunta técnica o pega un escenario del examen DP-800..."):
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

    with st.chat_message("assistant"):
        historial_limpio = [
            {"rol": m["rol"], "contenido": m["contenido"]}
            for m in st.session_state.mensajes[:-1]
        ]
        payload = {
            "pregunta": pregunta,
            "historial": historial_limpio
        }

        t_inicio_total = time.perf_counter()
        contenedor_meta = {"data": None}

        try:
            respuesta_http = requests.post(API_URL, json=payload, stream=True)
            respuesta_http.raise_for_status()

            def generador_limpio():
                buffer = ""
                meta_lista = False

                for chunk in respuesta_http.iter_content(chunk_size=512, decode_unicode=True):
                    if not chunk:
                        continue

                    if not meta_lista:
                        buffer += chunk
                        if "<<<META_END>>>" in buffer:
                            partes = buffer.split("<<<META_END>>>", 1)
                            json_raw = partes[0].replace("<<<META_START>>>", "").strip()
                            try:
                                contenedor_meta["data"] = json.loads(json_raw)
                            except Exception:
                                contenedor_meta["data"] = None

                            meta_lista = True
                            if partes[1]:
                                yield partes[1]
                    else:
                        yield chunk

            texto_final = st.write_stream(generador_limpio())
            tiempo_total_s = round(time.perf_counter() - t_inicio_total, 2)

            datos_telemetria = contenedor_meta["data"]
            if datos_telemetria:
                datos_telemetria["tiempo_total_s"] = tiempo_total_s
                dibujar_desplegable_telemetria(datos_telemetria)

            st.session_state.mensajes.append({
                "rol": "assistant",
                "contenido": texto_final,
                "telemetria_data": datos_telemetria
            })

        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar con FastAPI en `http://localhost:8000`. Verifica que Uvicorn esté activo.")