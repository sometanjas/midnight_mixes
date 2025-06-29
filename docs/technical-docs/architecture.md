---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Tatjana K.]

{: .no_toc }
# Architecture


<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

Dieses Repository enthält eine Flask-Anwendung, die eine API sowie serverseitig gerenderte Templates bereitstellt. Zusammen bilden sie einen Dienst zur Cocktailsuche.

## Codemap

- `/docs`
  - enthält statische Dokumentation und Design Decisions
- `/sql`
  - enthält vorbereitete Dateien, mit denen die Datenbank automatisch gefüllt wird
- `/static`
  - enthält statische Ressourcen
- `/templates`
  - enthält die Templates der Webseiten
- `app.py`
  - der Haupteinstiegspunkt der Anwendung, in dem sich alle APIs befinden
- `db.py`
  - enthält Funktionen zur Datenbankverbindung
- `forms.py`
  - definiert Formulare für eine Flask-Webanwendung
- `requirements.txt`
  - listet die Python-Abhängigkeiten auf, die zum Erstellen der Application erforderlich sind

## Cross-cutting concerns

Die Application erwartet eine vorhandene Datei `db.sqlite`, die die SQLite-Datenbank enthält, um korrekt zu funktionieren.
Die Application bietet außerdem eine Command-Line Interface Schnittstelle, um eine neue, mit Beispieldaten vorbefüllte Datenbank zu erstellen.
Dazu kann der Befehl `flask init-db` ausgeführt werden.