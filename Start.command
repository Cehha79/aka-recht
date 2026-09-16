#!/bin/zsh
# AKA Recht starten: lokaler Dienst auf 127.0.0.1, Oberfläche im Standardbrowser.
RECHTSORDNER="${0:A:h}"
cd "$RECHTSORDNER" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 fehlt. Deine Unterlagen bleiben im Finder zugänglich."
  exit 1
fi
python3 "$RECHTSORDNER/06 Werkzeuge/dienst/server.py" "$@"
