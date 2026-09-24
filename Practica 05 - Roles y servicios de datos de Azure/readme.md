# Caso Práctico — Plataforma de Datos: Grupo Alimenta

Este documento contiene la resolución del caso práctico de diseño arquitectónico y estratégico para la plataforma de datos del **Grupo Alimenta**, cubriendo desde la ingesta de datos hasta la explotación analítica y aplicación de Inteligencia Artificial.

## objetivos del proyecto

* **Clasificación de fuentes:** Análisis de orígenes de datos transaccionales (OLTP), streaming (IoT) y ficheros (Batch).
* **Arquitectura Medallion:** Diseño de capas lógicas (Bronze, Silver, Gold) utilizando el ecosistema de Azure y Databricks.
* **Modelado Dimensional:** Creación de un esquema en estrella optimizado para el análisis de ventas y roturas de stock.
* **Roles y Gobierno:** Asignación de responsabilidades dentro del equipo de datos, definición de métricas de calidad y gestión de privacidad (PII) apoyada en Azure Purview.
* **Analítica Avanzada e IA:** Estrategia para modelos de Machine Learning (previsión de demanda) y asistentes virtuales impulsados por IA generativa.

## Stack Tecnológico Propuesto

* **Almacenamiento & Data Lake:** Azure Data Lake Storage Gen2 (Delta Lake).
* **Procesamiento & Computación:** Azure Databricks (Apache Spark) / Azure Data Factory.
* **Orígenes de Datos:** Azure SQL Database, Azure Cosmos DB, IoT, SFTP, APIs.
* **Explotación:** Power BI (DirectQuery/Import).
* **Gobierno de Datos:** Azure Purview.

## Estructura de entrega

* `Practica_05_ISAAC_Sanchez.pdf`: Documento principal con las respuestas.
* `Practica_05_ISAAC_Sanchez.md`: Exportación del informe en formato md para su lectura y evaluación.

---
**Autor:** Isaac Sánchez
