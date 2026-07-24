@echo off
REM MarkBridge — Windows build script
REM Generates: dist\MarkBridge.exe (standalone, no Python required)
REM Run from repo root: scripts\markitdown-app\build.bat

echo Building MarkBridge for Windows...

pip install pyinstaller --quiet

pyinstaller ^
  --name MarkBridge ^
  --onefile ^
  --windowed ^
  --icon scripts\markitdown-app\icon.ico ^
  --add-data "scripts\markitdown-app;markitdown-app" ^
  --hidden-import customtkinter ^
  --hidden-import watchdog ^
  --hidden-import pystray ^
  --hidden-import markitdown ^
  scripts\markitdown-app\main.py

echo.
if exist dist\MarkBridge.exe (
  echo [OK] dist\MarkBridge.exe criado com sucesso.
  echo Copia para qualquer PC Windows — nao necessita de Python instalado.
) else (
  echo [ERRO] Build falhou. Verifica os logs acima.
)
