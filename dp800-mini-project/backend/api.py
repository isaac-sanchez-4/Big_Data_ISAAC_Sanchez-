import time
import json
import pyodbc
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import PromptTemplate

# CONFIGURACIÓN DE SQL SERVER 2025
SERVER = 'localhost\\SQLEXPRESS01'
DATABASE = 'DP800_TutorRAG'
CONNECTION_STRING = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"


# MODELOS DE DATOS
class Mensaje(BaseModel):
    rol: str
    contenido: str


class PeticionChat(BaseModel):
    pregunta: str
    historial: List[Mensaje]


class DocumentoSimulado:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata


def buscar_en_sql_server(query: str, top_k: int = 12):
    """
    Genera el vector con Ollama, mide el tiempo exacto de respuesta y recupera
    los fragmentos y números de página desde SQL Server 2025
    """
    t_inicio = time.perf_counter()

    embeddings_model = OllamaEmbeddings(model="nomic-embed-text")
    query_vector = embeddings_model.embed_query(query)

    vector_rounded = [round(float(val), 5) for val in query_vector]
    query_vector_str = "[" + ",".join(map(str, vector_rounded)) + "]"

    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    cursor.setinputsizes([
        (pyodbc.SQL_WVARCHAR, 0, 0),
        (pyodbc.SQL_INTEGER, 0, 0)
    ])

    cursor.execute("EXEC sp_BuscarFragmentosSimilares @QueryVector = ?, @TopK = ?", (query_vector_str, top_k))
    filas = cursor.fetchall()

    documentos_recuperados = []
    fuentes_metadata = []

    for fila in filas:
        # fila[2]=NombreArchivo, fila[3]=TextoChunk, fila[4]=NumeroPagina
        texto_limpio = fila[3].strip()
        distancia = round(float(fila[5]), 4) if len(fila) > 5 and fila[5] is not None else None

        doc = DocumentoSimulado(
            page_content=texto_limpio,
            metadata={"source": fila[2], "page": fila[4]}
        )
        documentos_recuperados.append(doc)
        fuentes_metadata.append({
            "archivo": fila[2],
            "pagina": fila[4],
            "distancia": distancia,
            "extracto": texto_limpio[:300].replace("\n", " ") + ("..." if len(texto_limpio) > 300 else "")
        })

    cursor.close()
    conn.close()

    tiempo_sql_ms = round((time.perf_counter() - t_inicio) * 1000, 2)
    return documentos_recuperados, fuentes_metadata, tiempo_sql_ms


# INICIALIZACIÓN DE LA API Y MOTORES
app = FastAPI(title="API Tutor Inteligente DP-800 - SQL Server 2025")

llm_estricto = None


@app.on_event("startup")
def cargar_motores():
    global llm_estricto
    llm_estricto = OllamaLLM(model="llama3", temperature=0.0)
    print("Motores de IA (Llama3) e Infraestructura SQL Server 2025 listos.")


@app.get("/")
def estado():
    return {"estado": "API activa en puerto 8000. Usa Streamlit en http://localhost:8501"}


# PROMPTS BLINDADOS (FORMATO EXAMEN DP-800)
template_estricto = """You are an official Microsoft Certified Expert examiner for the DP-800 certification. Analyze the user's question with absolute technical rigor and respond ENTIRELY IN ENGLISH.

STEP 1: DETECT THE QUESTION FORMAT CAREFULLY
- **TYPE 1 (Single-Choice Multiple Choice - A, B, C, D):** 
  * If the question asks to choose ONE correct option from a list of choices (A, B, C, D):
  * YOU MUST SELECT ONLY ONE OPTION. 
  * Mandatory output format:
    **[Exact Letter A, B, C, or D]. [Exact option text]**
    [Detailed technical justification explaining why this option is correct and why A, B, C, and D alternatives are discarded].

- **TYPE 2 (Multiple Statements / Yes-No per statement):** 
  * If the question presents numbered statements (1, 2, 3) requiring a Yes/No evaluation for each:
  * Mandatory output format:
    **1. [Yes / No]:** [Technical explanation]
    **2. [Yes / No]:** [Technical explanation]
    **3. [Yes / No]:** [Technical explanation]

STRICT TECHNICAL & EVIDENCE RULES:
- Base your answers strictly on the technical architecture of Azure SQL and SQL Server 2025.
- If it's a Type 1 question, NEVER use a "1. Yes / 2. No" list format. Pick the letter directly.

Retrieved context from documentation:
{context}

User's Question / Options:
{question}

Technical response in English:"""
prompt_verdad = PromptTemplate.from_template(template_estricto)


# ENDPOINT PRINCIPAL
@app.post("/chat")
async def endpoint_chat(peticion: PeticionChat):
    pregunta = peticion.pregunta
    historial = peticion.historial

    # 1. EL GUARDIA DE TRÁFICO
    prompt_guardia = f"""Actúa como un clasificador binario estricto para un tutor técnico de la certificación DP-800.
    Analiza la intención del usuario y clasifícala estrictamente en una de estas dos categorías:
    - 'CHAT': Si el usuario saluda, se despide, hace una pregunta personal, pide una historia de ficción, chatea o habla de temas ajenos a bases de datos o SQL Server.
    - 'BUSCAR': Si el usuario pregunta sobre SQL Server, Azure SQL, bases de datos, consultas T-SQL, índices, rendimiento, arquitectura de datos o pega un enunciado de examen/caso de estudio.

    Ejemplos:
    - "Hola, ¿qué tal?" -> CHAT
    - "Cuéntame un cuento de ciencia ficción" -> CHAT
    - "Gracias por la ayuda" -> CHAT
    - "¿Cómo optimizo un índice nonclustered?" -> BUSCAR
    - "You have an Azure SQL database..." -> BUSCAR

    TEXTO DEL USUARIO: "{pregunta}"
    Responde ÚNICAMENTE con la palabra CHAT o la palabra BUSCAR, sin explicaciones adicionales:"""

    intencion = llm_estricto.invoke(prompt_guardia).strip().upper()
    print(f"\n[TELEMETRÍA] Intención resuelta: {intencion}")

    # Enrutamiento directo basado puramente en la intención semántica
    if "CHAT" in intencion:
        def generar_chat():
            meta = json.dumps({
                "tipo": "chat",
                "fuentes": [],
                "tiempo_sql_ms": 0,
                "query_ejecutada": pregunta
            })
            yield f"<<<META_START>>>{meta}<<<META_END>>>"
            prompt_chat = f"Eres el Tutor Inteligente de la certificación DP-800. Responde en el idioma en el que te habla el usuario, de forma amigable y natural, a: '{pregunta}'"
            for chunk in llm_estricto.stream(prompt_chat):
                yield chunk.content if hasattr(chunk, 'content') else str(chunk)

        return StreamingResponse(generar_chat(), media_type="text/event-stream")

    intencion = llm_estricto.invoke(prompt_guardia).strip().upper()
    print(f"\n[TELEMETRÍA] Intención resuelta: {intencion}")

    if "CHAT" in intencion and len(pregunta.split()) < 6:
        def generar_chat():
            meta = json.dumps({
                "tipo": "chat",
                "fuentes": [],
                "tiempo_sql_ms": 0,
                "query_ejecutada": pregunta
            })
            yield f"<<<META_START>>>{meta}<<<META_END>>>"
            prompt_chat = f"Eres el Tutor Inteligente de la certificación DP-800. Responde en español de forma muy breve y cordial a: '{pregunta}'"
            for chunk in llm_estricto.stream(prompt_chat):
                yield chunk.content if hasattr(chunk, 'content') else str(chunk)

        return StreamingResponse(generar_chat(), media_type="text/event-stream")

    # 2. LA MEMORIA (CON AISLAMIENTO ENTRE PREGUNTAS DE EXAMEN)
    pregunta_a_buscar = pregunta
    if len(historial) > 1 and len(pregunta.split()) < 25:
        historial_str = "\n".join([f"{m.rol}: {m.contenido}" for m in historial[-2:]])
        prompt_memoria = f"""Resuelve pronombres ambiguos en la 'Nueva pregunta' solo si continúa el tema anterior. Si es una pregunta nueva o independiente, devuélvela intacta sin cambiar nada.
Historial:
{historial_str}
Nueva pregunta: "{pregunta}"
Pregunta resultante (solo la pregunta):"""
        pregunta_a_buscar = llm_estricto.invoke(prompt_memoria).strip()

    print(f"[TELEMETRÍA] Query en SQL Server 2025: {pregunta_a_buscar[:120]}...")

    # 3. RECUPERACIÓN VECTORIAL Y STREAMING
    documentos, fuentes, tiempo_sql_ms = buscar_en_sql_server(pregunta_a_buscar, top_k=8)
    contexto = "\n\n".join([doc.page_content for doc in documentos])

    # Pasamos la pregunta original íntegra al prompt final para no perder opciones ni declaraciones
    prompt_final = prompt_verdad.format(context=contexto, question=pregunta)

    def generar_respuesta():
        meta = json.dumps({
            "tipo": "rag",
            "fuentes": fuentes,
            "tiempo_sql_ms": tiempo_sql_ms,
            "query_ejecutada": pregunta_a_buscar
        })
        yield f"<<<META_START>>>{meta}<<<META_END>>>"

        for chunk in llm_estricto.stream(prompt_final):
            yield chunk.content if hasattr(chunk, 'content') else str(chunk)

    return StreamingResponse(generar_respuesta(), media_type="text/event-stream")