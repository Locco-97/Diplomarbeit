# Zusammenfassung
Um das neue Python Projekt zu nutzen müssen folgende Schritte durchgeführt werden:

### Virtual Environment erstellen (optional)
- Git Bash öffnen im Ornder Diplomarbeit (kontrollieren mit Befehl `pwd`)
- Environment Manager installieren: `pip install virtualenv`
- Environment erstellen: `python -m venv .venv`
- Environment aktivieren: `./.venv/Scripts/activate`

### Requirements installieren
- Git Bash öffnen im Ornder Diplomarbeit (kontrollieren mit Befehl `pwd`)
- Befehl ausführen: `pip install -r requirements.txt`

### Ausführbare Datei erstellen
- Git Bash öffnen im Ornder Diplomarbeit (kontrollieren mit Befehl `pwd`)
- Datei generieren: `pyinstaller --onefile kurzschlussanalyzer.py --add-data "kurzschlussanalyzer/images/*.png;kurzschlussanalyzer/images/" --noconsole --icon="kurzschlussanalyzer/images/blt.ico"`

- Datei wird unter dem Ordner *Dist* abgelegt. 