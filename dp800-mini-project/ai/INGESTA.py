import os
import pyodbc
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings

# CONFIGURACIÓN DE SQL SERVER 2025
SERVER = 'localhost\\SQLEXPRESS01'
DATABASE = 'DP800_TutorRAG'
CONNECTION_STRING = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"

ruta_pdf = "documentos/DP800.pdf"

if not os.path.exists(ruta_pdf):
    print(f"Error: No se encuentra el archivo en '{ruta_pdf}'")
    exit()

print("Cargando PDF...")
loader = PyMuPDFLoader(ruta_pdf)
documentos_originales = loader.load()

print("Aplicando Chunking...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
trozos = splitter.split_documents(documentos_originales)

print("generando Embeddings con Ollama (nomic-embed-text)...")
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

# Conectamos a SQL Server 2025
conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()

# 1. Registramos el documento principal en la ddbb
nombre_archivo = os.path.basename(ruta_pdf)
cursor.execute("INSERT INTO Documentos (NombreArchivo) OUTPUT INSERTED.DocumentoID VALUES (?)", (nombre_archivo,))
documento_id = cursor.fetchone()[0]
conn.commit()

# Forzamos a pyodbc a enviar los textos largos como NVARCHAR(MAX) en lugar de ntext
cursor.setinputsizes([
    (pyodbc.SQL_INTEGER, 0, 0),
    (pyodbc.SQL_WVARCHAR, 0, 0),
    (pyodbc.SQL_INTEGER, 0, 0),
    (pyodbc.SQL_WVARCHAR, 0, 0)
])

print(f"Insertando {len(trozos)} fragmentos y vectores (768 dims) en SQL Server 2025...")

for i, trozo in enumerate(trozos):
    # Generamos el vector de 768 dimensiones
    vector = embeddings_model.embed_query(trozo.page_content)

    # Redondeamos a 5 decimales para aligerar el string JSON
    vector_rounded = [round(float(val), 5) for val in vector]
    vector_str = "[" + ",".join(map(str, vector_rounded)) + "]"

    pagina = trozo.metadata.get("page", 1)

    cursor.execute("""
        INSERT INTO Fragmentos (DocumentoID, TextoChunk, NumeroPagina, Embedding)
        VALUES (?, ?, ?, CAST(? AS VECTOR(768)))
    """, (documento_id, trozo.page_content, pagina, vector_str))

conn.commit()
cursor.close()
conn.close()

print("Ingesta completada con éxito en SQL Server 2025.")