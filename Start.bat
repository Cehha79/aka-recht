@echo off
rem AKA Recht starten (Windows): Dienst auf 127.0.0.1, Oberflaeche im Browser. Geprueft am 17.09.2026 auf Windows 11 mit Python 3.14.
rem Windows legt python.exe als Verweis auf den Microsoft Store an; "where python" findet diesen Koeder. Deshalb wird Python wirklich gestartet.
cd /d "%~dp0"
python --version >nul 2>nul
if errorlevel 1 (
  echo Python 3 fehlt oder "python" zeigt nur auf den Microsoft Store. Bitte von python.org installieren, mit "Add python.exe to PATH", dann dieses Fenster neu oeffnen.
  pause
  exit /b 1
)
rem KI-Konfigurationen (.mcp.json, .claude\settings.json, .codex\config.toml) auf "python" statt "python3" stellen; aendert nichts, wenn schon eingerichtet.
python "%~dp0\06 Werkzeuge\einrichten_windows.py"
if errorlevel 1 echo Hinweis: KI-Konfiguration nicht vollstaendig angepasst, siehe Meldung oben. Die Oberflaeche startet trotzdem.
python "%~dp0\06 Werkzeuge\dienst\server.py" %*
