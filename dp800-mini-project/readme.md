# Tutor inteligente RAG para DP-800

Aplicación local de preguntas y respuestas para preparar la certificación DP-800. Combina recuperación aumentada por generación (RAG), SQL Server con búsqueda vectorial y Ollama para responder en español usando el contenido de `documentos/DP800.pdf`.

## Arquitectura

- **Frontend:** Streamlit en `frontend/app.py`, con chat, streaming y telemetría de las fuentes recuperadas.
- **Backend:** FastAPI en `backend/api.py`. Genera el embedding de la pregunta, recupera fragmentos desde SQL Server y consulta Llama 3.
- **Base de datos:** SQL Server con vectores `VECTOR(768)` y el procedimiento `sp_BuscarFragmentosSimilares`.
- **Modelos locales:** Ollama con `nomic-embed-text` para embeddings y `llama3` para generar respuestas.

## Estructura

```text
dp800-mini-project/
├── ai/INGESTA.py                # Carga el PDF, crea fragmentos y genera embeddings
├── backend/api.py               # API FastAPI y recuperación RAG
├── database/                    # Scripts SQL, que deben ejecutarse en orden
├── documentos/DP800.pdf         # Documento utilizado como fuente
├── frontend/app.py              # Interfaz Streamlit
├── docs/Mini proyecto dp.docx   # Memoria del proyecto
├── INICIO.bat                   # Arranque automático en Windows
└── readme.md                    # Este documento
```

## Requisitos

- Windows y Python 3.10 o superior.
- SQL Server 2025 (o una versión compatible con el tipo `VECTOR`) y ODBC Driver 17 for SQL Server.
- Ollama instalado y ejecutándose.
- Un entorno virtual en `.venv` si se utiliza `INICIO.bat`.

Descarga los modelos necesarios:

```powershell
ollama pull llama3
ollama pull nomic-embed-text
```

Instala las dependencias del proyecto en el entorno virtual:

```powershell
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` contiene las dependencias de FastAPI, Streamlit, SQL Server, PyMuPDF y LangChain utilizadas por la aplicación.

## Configuración de SQL Server

Los scripts de `database/` deben ejecutarse en este orden:

1. `01_crear_bbdd.sql`
2. `02_crear_tablas.sql`
3. `03_procedimiento.sql`

> **Advertencia:** `01_crear_bbdd.sql` elimina y vuelve a crear `DP800_TutorRAG` si ya existe. No lo ejecutes sobre una base de datos con información que quieras conservar.

La aplicación está configurada actualmente para la instancia `localhost\SQLEXPRESS01` y la base de datos `DP800_TutorRAG`, usando autenticación de Windows. Si tu servidor es diferente, actualiza `SERVER`, `DATABASE` y `CONNECTION_STRING` en `backend/api.py` y `ai/INGESTA.py`.

## Ingesta del documento

La ingesta solo es necesaria cuando se crea o actualiza la base de datos. Comprueba que el PDF esté en `documentos/DP800.pdf` y ejecuta desde la raíz del proyecto:

```powershell
python ai/INGESTA.py
```

El script divide el documento en fragmentos, genera un embedding de 768 dimensiones para cada uno y los guarda en SQL Server.

## Ejecución

### Inicio automático en Windows

Con el entorno virtual creado y Ollama en ejecución, ejecuta:

```powershell
INICIO.bat
```

El script abre FastAPI en `http://localhost:8000` y Streamlit en `http://localhost:8501`.

### Inicio manual

En dos terminales abiertas en la raíz del proyecto:

```powershell
python -m uvicorn backend.api:app --reload --port 8000
```

```powershell
streamlit run frontend/app.py
```

Puedes comprobar el estado de la API en `http://localhost:8000/` y abrir la interfaz en `http://localhost:8501`.

## Solución de problemas

- **No se puede conectar con SQL Server:** comprueba que el servicio esté iniciado, que exista la instancia `localhost\SQLEXPRESS01`, que esté instalado ODBC Driver 17 y que la base de datos se haya creado ejecutando los scripts en orden.
- **No se puede conectar con Ollama:** inicia Ollama y verifica los modelos con `ollama list`. Si faltan, ejecuta los comandos `ollama pull` de la sección de requisitos.
- **La ingesta no encuentra el PDF:** ejecuta `python ai/INGESTA.py` desde la raíz del proyecto y confirma que el archivo esté en `documentos/DP800.pdf`.
- **El frontend indica que FastAPI no responde:** inicia primero el backend con Uvicorn y comprueba `http://localhost:8000/` antes de abrir Streamlit.
- **La búsqueda no devuelve resultados:** revisa que la ingesta haya terminado correctamente y que la tabla `Fragmentos` contenga datos.

## Limitaciones actuales

- La configuración de conexión está definida directamente en `backend/api.py` y `ai/INGESTA.py`.
- La aplicación está pensada para uso local y no incluye autenticación de usuarios.
- El script `01_crear_bbdd.sql` recrea la base de datos; realiza una copia de seguridad antes de usarlo en un entorno con datos.

## Funcionalidades

- Recuperación de fragmentos mediante embeddings y búsqueda vectorial en SQL Server.
- Respuestas en streaming desde FastAPI hacia Streamlit.
- Historial de conversación con reescritura de preguntas breves y ambiguas.
- Telemetría de la consulta SQL, distancia de los resultados y páginas del PDF utilizadas.