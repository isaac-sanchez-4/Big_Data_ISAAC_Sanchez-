@echo off
chcp 65001 >nul
echo ==========================================
echo    ARRANCANDO TUTOR INTELIGENTE DP-800
echo ==========================================

:: 0. Comprobar y arrancar Ollama de forma TOTALMENTE OCULTA con PowerShell
echo Verificando el estado de Ollama...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe" >nul
if "%ERRORLEVEL%"=="0" (
    echo [OK] Ollama ya está en ejecución.
) else (
    echo [AVISO] Ollama está detenido. Iniciándolo como proceso fantasma...
    powershell -Command "Start-Process -FilePath 'C:\Users\ISAAC\AppData\Local\Programs\Ollama\ollama.exe' -ArgumentList 'serve' -WindowStyle Hidden"
    echo Esperando 5 segundos a que Ollama cargue los modelos...
    ping 1.2.3.4 -n 1 -w 5000 >nul
)

:: 1. Activar el entorno virtual
echo Activando entorno virtual...
call .venv\Scripts\activate

:: 2. Iniciar FastAPI (Backend) en una ventana independiente
echo Iniciando Backend (FastAPI y Llama 3)...
start "Backend FastAPI" cmd /k "python -m uvicorn backend.api:app --reload --port 8000"

:: 3. Darle tiempo real a FastAPI para que cargue el modelo en memoria (8 segundos)
echo Esperando a que el motor de IA cargue por completo...
ping 1.2.3.4 -n 1 -w 8000 >nul

:: 4. Iniciar Streamlit (Frontend) cuando el backend ya está listo
echo Iniciando Frontend (Streamlit)...
start "Frontend Streamlit" cmd /k "streamlit run frontend/app.py"

echo ==========================================
echo ¡Todos los servicios iniciados con éxito!
echo ==========================================
pause