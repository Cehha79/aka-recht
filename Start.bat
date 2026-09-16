@echo off
rem AKA Recht starten (Windows): Dienst auf 127.0.0.1, Oberflaeche im Browser. Ungeprueft, siehe README.
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3 fehlt. Bitte von python.org installieren, mit "Add python.exe to PATH".
  pause
  exit /b 1
)
python "%~dp0\06 Werkzeuge\dienst\server.py" %*
