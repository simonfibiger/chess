@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe python -m venv .venv
if errorlevel 1 goto end
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto end
.venv\Scripts\python.exe server.py --host 0.0.0.0
:end
pause
