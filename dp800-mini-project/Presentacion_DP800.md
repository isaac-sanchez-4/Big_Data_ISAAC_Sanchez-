---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #ffffff
---

# CERTIFICACIÓN OFICIAL MICROSOFT DP-800
## Tutor Inteligente RAG con SQL Server 2025
**Asistente técnico local de alta velocidad para resolución de escenarios de examen.**

*Autor: Isaac Sánchez García · Big Data & IA*

---

<!-- class: default -->

## 01 · CONTEXTO Y PROBLEMÁTICA
### El Desafío en la Preparación Técnica

* **Volúmenes Masivos:** Guías oficiales superiores a 400 páginas.
* **Alucinaciones LLM:** Modelos genéricos sin contexto actualizado.
* **Precisión de Examen:** Rigor estricto en opciones múltiples.

---

## 02 · DISEÑO TECNOLÓGICO
### Arquitectura Desacoplada 100% Local

1. **01 · FRONTEND (Streamlit):** 
   Chat interactivo con telemetría desplegable.
2. **02 · BACKEND (FastAPI):** 
   Control de intenciones en streaming.
3. **03 · DATOS (SQL Server 2025):** 
   Búsqueda vectorial nativa `VECTOR(768)`.
4. **04 · MODELOS IA (Ollama Local):** 
   Llama 3 determinista sin coste.

---

## 03 · MOTOR RELACIONAL E IA
### Búsqueda Vectorial Nativa en SQL Server

```sql
-- Procedimiento sp_BuscarFragmentosSimilares
SELECT TOP (@TopK)
    d.NombreArchivo, f.TextoChunk, f.NumeroPagina,
    VECTOR_DISTANCE('cosine', f.Embedding, CAST(@QueryVector AS VECTOR(768))) AS Distancia
FROM Fragmentos f
INNER JOIN Documentos d ON f.DocumentoID = d.DocumentoID
ORDER BY Distancia ASC;

```

* **Soporte `VECTOR(768)`:** Almacenamiento nativo de embeddings `nomic-embed-text`.
* **Función `VECTOR_DISTANCE`:** Similitud coseno calculada dentro del motor.
* **Trazabilidad Documental:** Retorno exacto de página y archivo PDF.

---

## 04 · INGENIERÍA DE SOFTWARE

### Retos y Soluciones Implementadas

**Contaminación de Contexto (Alucinaciones en Opciones)**

* *Problema:* El historial previo alteraba nuevas búsquedas.
* *Solución (Query Rewriter):* Aislamiento estricto al cambiar de tema para búsquedas limpias.

**Confusión de Formato**

* *Problema:* Confusión de opciones de test con código SQL.
* *Solución (Prompt Blindado):* Reglas de examinador oficial Microsoft con evaluación estructurada (A/B/C/D o Sí/No).

---

## 05 · RESULTADOS EN PRODUCCIÓN

### Transparencia y Telemetría en Tiempo Real

* **⚡ 982.75 ms:** Latencia de búsqueda vectorial en SQL Server 2025 (Top 8 fragmentos).
* **✅ Verificación exitosa:** Comprobado en caso práctico `IncidentDescription`, recuperando las páginas 357, 359, 360, 361 y 363 con una distancia coseno de `0.3044`.

---

## 06 · CIERRE DEL PROYECTO

### Conclusiones y Valor de la Solución

* **Nivel 3 Avanzado Superado:** Fusión de base de datos relacional transaccional con IA vectorial nativa.
* **Privacidad y Coste Cero:** Ejecución 100% local con Ollama y despliegue en un clic mediante `INICIO.bat`.
* **Alta Versatilidad:** Adaptable a cualquier otra certificación técnica reemplazando el archivo PDF.

---

# ¡Muchas gracias por su atención!

**Turno de preguntas y demostración práctica en vivo.**

*Isaac Sánchez García · Tutor Inteligente RAG DP-800*

```eof
