#!/bin/sh
# AKA Recht starten (Linux und macOS ohne Finder-Doppelklick): Dienst auf 127.0.0.1, Oberfläche im Browser.
RECHTSORDNER="$(cd "$(dirname "$0")" && pwd)"
cd "$RECHTSORDNER" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 fehlt. Deine Unterlagen bleiben im Dateimanager zugänglich."
  exit 1
fi
exec python3 "$RECHTSORDNER/06 Werkzeuge/dienst/server.py" "$@"
