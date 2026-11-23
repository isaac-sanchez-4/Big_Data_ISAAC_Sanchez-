# Smart Agro IoT — Plataforma de Datos End-to-End en Databricks

Proyecto integral de ingeniería de datos IoT agrícolas desarrollado sobre **Databricks** y **Unity Catalog**, alineado con los bloques de la certificación **Databricks DP-750 (A–G)**. Implementa una arquitectura **Medallion** completa (`Bronze → Silver → Gold`), ingesta incremental idempotente con `MERGE INTO`, auditoría de calidad de datos, gobierno RBAC, automatización mediante **Lakeflow Jobs** y una aplicación web en **Streamlit** con un asistente **Text-to-SQL** ejecutado en local mediante **Ollama**.

## Arquitectura del Proyecto

``` mermaid 
flowchart LR
    A[4 Fuentes JSONL<br/>Volumen Administrado] --> B[Bronze<br/>Ingesta Cruda Delta]
    B --> C[Silver<br/>Limpieza + MERGE INTO<br/>+ Calidad]
    C -->|36 inválidos| R[(calidad_rechazos_silver)]
    C -->|9.966 válidos| D[Gold<br/>4 Data Marts + OPTIMIZE]
    D --> E[App Streamlit<br/>Explorador + IA Text-to-SQL]
    F[Ollama Local<br/>qwen2.5-coder:32b] <--> E

    subgraph Gobernanza y Orquestación
        UC[Unity Catalog · RBAC<br/>admin / operarios / ai_assistant]
        LF[Lakeflow Job · Serverless<br/>Scheduled 09:30 AM]
    end

```

### Capas y componentes principales

* **Capa Bronze (`01_Bronce.ipynb`):** Ingesta cruda en formato Delta de cuatro fuentes `JSONL` (`sensor_readings`, `weather_readings`, `irrigation_events` y `alerts`) con trazabilidad (`fecha_ingesta`, `archivo_origen`) y documentación en catálogo (`COMMENT ON TABLE`).

* **Capa Silver (`02_Silver.ipynb`):** Desanidado de estructuras JSON (`measurements.*`), normalización de `timestamp`, deduplicación por `event_id`, validación de reglas de negocio (nulos y rangos físicos `[0, 100]`) y carga incremental idempotente mediante `MERGE INTO`. Los registros inválidos se aíslan en `calidad_rechazos_silver` con su motivo de rechazo.

* **Capa Gold (`03_Gold.ipynb`):** Construcción de 4 *Data Marts* de negocio (`gold_consumo_agua_parcela`, `gold_estres_suelo`, `gold_resumen_clima_diario`, `gold_resumen_alertas`) y mantenimiento con `OPTIMIZE` y evaluación mediante `DESCRIBE DETAIL`.

* **Gobierno y Seguridad (`04_Permisos.ipynb`):** Modelo RBAC en **Unity Catalog** bajo el principio de mínimo privilegio:

  * `admin`: `ALL PRIVILEGES` sobre `agro_catalog`.

  * `operarios`: `SELECT` exclusivo sobre las 4 tablas Gold y `REVOKE ALL` sobre Bronze, Silver y rechazos.

  * `ai_assistant`: `SELECT` exclusivo sobre Gold y `REVOKE INSERT, UPDATE, DELETE` a nivel de todo el catálogo.

* **Orquestación (Lakeflow Job):** Flujo secuencial `bronze → silver → gold` sobre cómputo *Serverless*, con programación diaria (`09:30 AM`) y validación de comportamiento ante fallo controlado y ejecución exitosa.

* **Capa de Consumo (`web/app.py`):** Aplicación web en **Streamlit** conectada vía `databricks-sql-connector` (con caché de 60s y credenciales en `st.secrets`), explorador de tablas filtrado por rol y chat **Text-to-SQL** con `qwen2.5-coder:32b` en local.

## Métricas y Validaciones Clave

| Dimensión | Evidencia / Resultado Verificado | 
| ----- | ----- | 
| **Calidad de datos (Silver)** | `10.002` registros en Bronze → `9.966` válidos en Silver y **`36` rechazos** trazados en `calidad_rechazos_silver`. | 
| **Idempotencia (`MERGE INTO`)** | Reejecución completa (`v9`): `6.154` filas origen, **`0` inserciones** (cero duplicados). | 
| **Carga incremental (Lote 2)** | Prueba controlada (`v11`): `2` filas origen → **`1` actualización + `1` inserción** registradas en `DESCRIBE HISTORY`. | 
| **Rendimiento (`OPTIMIZE`)** | Tiempo de consulta en Gold: **`0,632 s` → `0,5832 s`** (`numFiles = 1` en los 4 *Data Marts*). | 
| **Auditoría RBAC** | Verificado con `SHOW GRANTS` a nivel de catálogo, tabla Gold y tabla Bronze. | 

## Estructura del Repositorio

```
smart-agro-iot/
├── README.md
├── .gitignore
├── requirements.txt
├── notebooks/
│   ├── 01_Bronce.ipynb          # Ingesta cruda desde JSONL a tablas Delta Bronze
│   ├── 02_Silver.ipynb          # Desanidado, reglas de calidad, rechazos y MERGE INTO
│   ├── 03_Gold.ipynb            # 4 Data Marts de negocio, OPTIMIZE y DESCRIBE DETAIL
│   └── 04_Permisos.ipynb        # Políticas RBAC (GRANT / REVOKE) y auditoría SHOW GRANTS
├── web/
│   └── app.py                   # Interfaz Streamlit + Asistente IA Text-to-SQL (Ollama)
└── docs/
    ├── Documentacion_Smart_Agro_IoT.pdf
    └── Smart-Agro-IoT.pptx

```

## Instalación y Ejecución Local de la App (`web/app.py`)

### 1. Requisitos previos

* Python 3.10 o superior.

* Workspace de Databricks con el catálogo `agro_catalog.bronce` desplegado (ejecutando los notebooks `01` a `04`).

* [Ollama](https://ollama.com/) instalado en local con el modelo descargado:

  ```
  ollama pull qwen2.5-coder:32b
  
  ```

### 2. Clonar el repositorio e instalar dependencias

```
git clone <Link al proyecto>
cd smart-agro-iot

python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt

```

### 3. Configurar las credenciales de Databricks

Crea el archivo `web/.streamlit/secrets.toml` (excluido del repositorio mediante `.gitignore`) con tus datos de conexión del SQL Warehouse:

```
[databricks]
server_hostname = "tu-workspace.cloud.databricks.com"
http_path = "/sql/1.0/warehouses/tu-warehouse-id"
access_token = "dapiXXXXXXXXXXXXXXXXXXXXXXXX"

```

### 4. Lanzar la aplicación

```
streamlit run web/app.py

```

> **Nota sobre la simulación de roles en la interfaz:** Al desarrollarse sobre *Databricks Free Edition* con un único *Personal Access Token*, `app.py` simula el cambio de perfil (`Administrador` vs. `Trabajador (Operario)`) en la capa de interfaz replicando las políticas reales verificadas en Unity Catalog (`04_Permisos.ipynb`). En un entorno productivo, este selector se sustituiría por autenticación federada (Microsoft Entra ID) o *Service Principals* independientes por rol.

## Documentación y Demostración en Vivo

* **Documentación técnica completa:** [`docs/Documentacion_Smart_Agro_IoT.pdf`](docs/Documentacion_Smart_Agro_IoT.pdf)

* **Presentación del proyecto:** [`docs/Smart-Agro-IoT.pptx`](docs/Smart-Agro-IoT.pptx)

* **Vídeo demostrativo (App Streamlit + IA Text-to-SQL):** [`Video demo`](https://tajamar365-my.sharepoint.com/:v:/r/personal/isaac_sanchez_tajamar365_com/_layouts/15/stream.aspx?id=%2Fpersonal%2Fisaac_sanchez_tajamar365_com%2FDocuments%2Fvideo_demo_dp_750.mp4&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&share=cQpQxM5re0xIQKq3S4GkvfxCEgUBGNt4HPNYfM_L2shcZ4Chvg)
