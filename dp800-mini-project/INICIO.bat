@echo off
echo ==========================================
echo    ARRANCANDO TUTOR INTELIGENTE DP-800
echo ==========================================

:: 1. Activar el entorno virtual
call .venv\Scripts\activate

:: 2. Iniciar FastAPI (Backend) en una ventana secundaria de comandos
echo Iniciando Backend (FastAPI)...
start cmd /k "python -m uvicorn backend.api:app --reload --port 8000"

:: 3. Esperar unos segundos a que cargue la API
timeout /t 3 /nobreak > nul

:: 4. Iniciar Streamlit (Frontend) en otra ventana secundaria
echo Iniciando Frontend (Streamlit)...
start cmd /k "streamlit run frontend/app.py"

echo ==========================================
echo ¡Servicios iniciados correctamente!
echo ==========================================
pause