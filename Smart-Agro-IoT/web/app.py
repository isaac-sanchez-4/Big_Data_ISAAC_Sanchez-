import streamlit as st
import pandas as pd
from databricks import sql
import ollama

# ==========================================
# CONFIGURACION Y METADATOS (Unity Catalog)
# ==========================================
st.set_page_config(page_title="Smart Agro IoT", layout="wide")

# Definicion exacta de las tablas y columnas reales en Databricks
ESQUEMAS_DB = {
    # Capa Gold (Negocio - 4 Data Marts)
    "gold_consumo_agua_parcela": "Metricas agregadas de consumo de riego por parcela (columnas: plot_id, total_agua_consumida_litros, total_riegos_realizados, caudal_medio_l_min).",
    "gold_estres_suelo": "Metricas agregadas de suelo y baterias por parcela y cultivo (columnas: plot_id, crop, temperatura_suelo_maxima_c, temperatura_suelo_media_c, humedad_suelo_media_pct, bateria_max, bateria_media_pct).",
    "gold_resumen_clima_diario": "Resumen meteorologico diario agregado (columnas: fecha, temperatura_aire_maxima_c, temperatura_aire_media_c, humedad_aire_media_pct, precipitacion_total_mm, velocidad_viento_media_ms).",
    "gold_resumen_alertas": "Resumen de alertas e incidencias por parcela, tipo y severidad (columnas: plot_id, alert_code, severity, total_alertas, valor_medido_maximo, ultima_alerta_registrada).",

    # Capa Silver (Datos limpios y auditoria de calidad)
    "sensor_readings_silver": "Lecturas limpias de sensores de suelo (columnas: event_id, timestamp, device_id, plot_id, crop, sensor_depth_cm, battery_pct, device_status, soil_moisture_pct, soil_temperature_c, soil_ph, soil_ec_ds_m).",
    "weather_readings_silver": "Lecturas meteorologicas limpias (columnas: event_id, timestamp, device_id, battery_pct, device_status, air_temperature_c, air_humidity_pct, solar_radiation_w_m2, rainfall_mm, wind_speed_ms).",
    "irrigation_events_silver": "Eventos de riego limpios (columnas: event_id, timestamp, device_id, plot_id, irrigation_status, valve_status, water_flow_l_min, water_pressure_bar, water_volume_l, reason, battery_pct, device_status).",
    "alerts_silver": "Historial limpio de alertas operativas de sensores y riego (columnas: event_id, timestamp, device_id, plot_id, farm_id, event_type, alert_code, severity, measured_value, threshold_value, message).",
    "calidad_rechazos_silver": "Tabla de auditoria con registros rechazados por reglas de calidad como valores nulos o fuera de rango (columnas: event_id, timestamp, device_id, origen, motivo_rechazo, fecha_auditoria).",

    # Capa Bronze (Datos crudos)
    "sensor_readings_bronze": "Lecturas crudas de sensores (columnas: event_id, timestamp, device_id, plot_id, crop, sensor_depth_cm, battery_pct, device_status, measurements.soil_moisture_pct, measurements.soil_temperature_c, measurements.soil_ph, measurements.soil_ec_ds_m, fecha_ingesta, archivo_origen).",
    "weather_readings_bronze": "Datos climaticos crudos (columnas: event_id, timestamp, device_id, battery_pct, device_status, measurements.air_temperature_c, measurements.air_humidity_pct, measurements.solar_radiation_w_m2, measurements.rainfall_mm, measurements.wind_speed_ms, fecha_ingesta, archivo_origen).",
    "irrigation_events_bronze": "Eventos de riego crudos (columnas: event_id, timestamp, device_id, plot_id, irrigation_status, valve_status, water_flow_l_min, water_pressure_bar, water_volume_l, reason, battery_pct, device_status, fecha_ingesta, archivo_origen).",
    "alerts_bronze": "Alertas crudas del sistema IoT (columnas: event_id, timestamp, device_id, plot_id, farm_id, event_type, alert_code, severity, measured_value, threshold_value, message, fecha_ingesta, archivo_origen)."
}

# Asignacion de permisos por rol (RBAC)
PERMISOS = {
    "Administrador": list(ESQUEMAS_DB.keys()),
    "Trabajador (Operario)": [
        "gold_consumo_agua_parcela",
        "gold_estres_suelo",
        "gold_resumen_clima_diario",
        "gold_resumen_alertas"
    ]
}


# CONEXION A DATABRICKS
@st.cache_data(ttl=60, show_spinner=False)
def consultar_databricks(query: str) -> pd.DataFrame:
    try:
        connection = sql.connect(
            server_hostname=st.secrets["databricks"]["server_hostname"],
            http_path=st.secrets["databricks"]["http_path"],
            access_token=st.secrets["databricks"]["access_token"]
        )
        cursor = connection.cursor()
        cursor.execute(query)
        try:
            resultado = cursor.fetchall_arrow().to_pandas()
        except Exception:
            rows = cursor.fetchall()
            if rows:
                columns = [col[0] for col in cursor.description]
                resultado = pd.DataFrame([list(row) for row in rows], columns=columns)
            else:
                resultado = pd.DataFrame()
        cursor.close()
        connection.close()
        return resultado
    except Exception as e:
        return pd.DataFrame({"error_sql": [str(e)]})


# MOTOR IA TEXT-TO-SQL (QWEN CODER 32B)

def agente_text_to_sql(pregunta, tablas_permitidas):
    esquema_contexto = "\n".join([f"- {t}: {ESQUEMAS_DB[t]}" for t in tablas_permitidas])

    prompt_sistema = f"""Eres un ingeniero de datos experto en Databricks SQL.
Base de datos: `agro_catalog.bronce`.

TABLAS PERMITIDAS Y SUS COLUMNAS EXACTAS:
{esquema_contexto}

REGLAS ESTRICTAS:
1. Devuelve UNICAMENTE la consulta SQL pura. CERO explicaciones, CERO markdown (```sql).
2. USA SOLO LAS COLUMNAS DEFINIDAS ARRIBA. Nunca inventes nombres de columnas.
3. El FROM debe ser absoluto: FROM agro_catalog.bronce.nombre_tabla
4. Deduce sinonimos (ej. "gasto" = "consumo", "lluvia" = "precipitacion_total_mm" o "rainfall_mm", "parcela 1" = "P001").
5. Si el usuario solo envia un saludo (ej. "hola", "buenos dias") o una frase que no es una consulta de datos, devuelve exactamente la palabra: NO_SQL
6. Si el usuario pide datos de tablas a las que no tiene acceso en la lista superior, devuelve exactamente la palabra: BLOQUEADO
"""
    response = ollama.chat(model='qwen2.5-coder:32b', messages=[
        {'role': 'system', 'content': prompt_sistema},
        {'role': 'user', 'content': pregunta}
    ])

    sql_generado = response['message']['content'].strip()

    # Limpieza estricta de formato
    sql_generado = sql_generado.replace("```sql", "").replace("```", "").strip()
    if sql_generado.endswith(";"):
        sql_generado = sql_generado[:-1]

    return sql_generado


# ==========================================
# 1. BARRA LATERAL: RBAC Y UTILIDADES
# ==========================================
st.sidebar.title("Control de Acceso")
rol_usuario = st.sidebar.selectbox("Iniciando sesion como:", ["Administrador", "Trabajador (Operario)"])
tablas_accesibles_usuario = PERMISOS[rol_usuario]

st.sidebar.divider()
if st.sidebar.button("Limpiar historial de chat"):
    st.session_state.chat_history = []
    st.rerun()

# ==========================================
# 2. EXPLORADOR DE DATOS DINAMICO
# ==========================================
st.title(f"Panel de Control - {rol_usuario}")
st.subheader("Explorador de Tablas Autorizadas")

col_tabla, col_btn = st.columns([3, 1])
with col_tabla:
    tabla_seleccionada = st.selectbox("Selecciona una tabla para previsualizar:", tablas_accesibles_usuario)
with col_btn:
    st.write("")
    st.write("")
    btn_consultar = st.button("Consultar 100 registros")

if btn_consultar:
    with st.spinner(f"Consultando {tabla_seleccionada}..."):
        df = consultar_databricks(f"SELECT * FROM agro_catalog.bronce.{tabla_seleccionada} LIMIT 100")
        if "error_sql" in df.columns:
            st.error(f"Error de base de datos: {df['error_sql'].iloc[0]}")
        elif df.empty:
            st.info(f"La tabla {tabla_seleccionada} no contiene registros actualmente.")
        else:
            st.dataframe(df, use_container_width=True)

st.divider()

# ==========================================
# 3. CHATBOT IA INTEGRADO
# ==========================================
st.subheader("Asistente de Datos (Text-to-SQL)")

opciones_capa = ["Todas permitidas"]
if rol_usuario == "Administrador":
    opciones_capa.extend(["Solo Bronze", "Solo Silver", "Solo Gold"])
else:
    opciones_capa.append("Solo Gold")

filtro_capa = st.selectbox("Filtrar alcance de la IA (Capa Arquitectura):", opciones_capa)

if filtro_capa == "Todas permitidas":
    tablas_contexto_ia = tablas_accesibles_usuario
else:
    palabra_clave = filtro_capa.split(" ")[1].lower()
    tablas_contexto_ia = [t for t in tablas_accesibles_usuario if palabra_clave in t.lower()]

st.caption(f"Contexto actual de la IA: {', '.join(tablas_contexto_ia)}")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "df" in msg and not msg["df"].empty:
            st.dataframe(msg["df"])

if prompt := st.chat_input("Ej: Cual es el consumo medio de agua en las parcelas"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not tablas_contexto_ia:
            st.warning("No hay tablas disponibles en la capa seleccionada para tu rol.")
            st.session_state.chat_history.append(
                {"role": "assistant", "content": "No hay tablas disponibles para consultar."})
        else:
            with st.spinner("Analizando consulta..."):
                sql_query = agente_text_to_sql(prompt, tablas_contexto_ia)

            if "NO_SQL" in sql_query:
                msg_saludo = "Hola. Estoy conectado al catalogo de Databricks. Indica que metrica de riego, suelo, clima, alertas o calidad deseas consultar."
                st.info(msg_saludo)
                st.session_state.chat_history.append({"role": "assistant", "content": msg_saludo})

            elif "BLOQUEADO" in sql_query:
                st.error("La consulta requiere acceso a tablas fuera de tu alcance actual.")
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": "Operacion bloqueada por RBAC o filtro de capa."})

            else:
                st.code(sql_query, language="sql")

                with st.spinner("Ejecutando consulta en Databricks..."):
                    df_resultado = consultar_databricks(sql_query)

                    if "error_sql" in df_resultado.columns:
                        error_msg = df_resultado['error_sql'].iloc[0]
                        st.error(f"Error SQL: {error_msg}")
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": f"Fallo en ejecucion SQL: {error_msg}"})
                    elif df_resultado.empty:
                        msg_vacio = "La consulta se ejecuto correctamente, pero no devolvio ningun registro que cumpla la condicion."
                        st.info(msg_vacio)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"**Consulta ejecutada:**\n```sql\n{sql_query}\n```\n\n{msg_vacio}"
                        })
                    else:
                        st.dataframe(df_resultado)

                        with st.spinner("Redactando respuesta..."):
                            respuesta_humana = ollama.chat(model='qwen2.5-coder:32b', messages=[
                                {'role': 'system',
                                 'content': 'Eres un analista de datos. Resume este resultado de base de datos en 1 o 2 lineas. Se directo y tecnico sin anadir introducciones.'},
                                {'role': 'user',
                                 'content': f"Pregunta: {prompt}\nDatos devueltos:\n{df_resultado.to_string()}"}
                            ])
                            texto_final = respuesta_humana['message']['content']
                            st.markdown(texto_final)

                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": f"**Consulta ejecutada:**\n```sql\n{sql_query}\n```\n\n{texto_final}",
                                "df": df_resultado
                            })