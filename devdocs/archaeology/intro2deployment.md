# NeonGrid-9 :: Einführung in Deployment & Infrastruktur

> Wie das Projekt heute läuft, was es braucht, und welche Optionen es gibt.

## Die kurze Version

**Es gibt kein Deployment.**

Das Projekt ist ein reines Python-Skript, das direkt aus dem Quellcode gestartet wird. Kein Docker, kein CI/CD, kein Build-Schritt, kein Paketmanager. Ein Entwickler klont das Repository und tippt `python3 main.py`. Das ist der gesamte "Deploy-Prozess".

Das ist keine Nachlässigkeit — es ist eine bewusste architektonische Entscheidung, die sich aus der Art des Programms ergibt.

---

## Warum es kein Deployment gibt

### 1. Zero Dependencies

Wenn du durch den gesamten Code gehst und nach externen Bibliotheken suchst, findest du **nichts**. Die Import-Liste des Projekts ist:

```python
import sys, os, time, json, re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from pathlib import Path
```

Alles aus der Python-Standardbibliothek. Kein `pip install`, kein `requirements.txt`, kein `setup.py`, kein `pyproject.toml`. Das bedeutet:

- Kein Dependency-Management nötig
- Kein virtueller Environment nötig
- Kein Paket-Repository nötig
- Kein Versionskonflikt möglich

### 2. Single-User, Single-Process

Das Spiel speichert seinen Zustand in JSON-Dateien im Home-Verzeichnis des Nutzers (`~/.neongrid9/save_slot1.json`). Es gibt keinen Server, keine Datenbank, keine gemeinsame Session. Es ist ein **lokaler Single-Player-Client**.

Ein Multiplayer- oder Server-Konzept würde die gesamte Architektur umwerfen. Solange das nicht geplant ist, braucht es keine Infrastruktur.

### 3. Terminal-nativ

Das Spiel rendert direkt auf `stdout` mit ANSI-Escape-Codes für Farben. Es braucht kein Browser-Fenster, kein GUI-Toolkit, kein Rendering-Backend. Jeder Computer mit einem Terminal-Emulator kann es darstellen — Windows Terminal, macOS Terminal, Linux Konsole, SSH-Session, VS Code integriertes Terminal.

---

## Was die Abwesenheit einer Dockerfile uns sagt

Es gibt keine `Dockerfile`, kein `docker-compose.yml`, kein `.dockerignore`. Das sagt drei Dinge:

1. **Das Ziel ist der Endnutzer, nicht ein Service.** Containerisierung macht Sinn für Server, Microservices oder isolierte Build-Umgebungen. Ein interaktives Terminal-Spiel profitiert nicht von einem Container — im Gegenteil: Ein Docker-Container würde dem Spieler ein unnötiges Konstrukt (`docker run -it neongrid9`) aufzwingen, ohne einen Vorteil zu bieten.

2. **Portabilität ist bereits gegeben.** Weil das Spiel nur Python 3.10+ und ein Terminal braucht, ist es bereits plattformübergreifend. Docker würde hier nur eine zusätzliche Schicht hinzufügen, die nichts löst.

3. **Kein State-Sharing nötig.** Container sind nützlich, um Zustand zu isolieren. Aber NeonGrid-9 *will* Zustand im Home-Verzeichnis persistieren. Ein Container, der bei jedem Start frisch ist, würde die Speicherstände zerstören, es sei denn, man mountet ein Volume — was wiederum die Einfachheit des Projekts untergräbt.

---

## Was wäre, wenn man es doch containerisieren wollte?

Falls jemand aus bildungstechnischen Gründen (z.B. ein vorkonfiguriertes Lern-Lab) eine Docker-Version bauen möchte, sähe das minimalistisch so aus:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
CMD ["python3", "main.py"]
```

Das wäre funktional vollständig. Man braucht keinen Multi-Stage-Build, kein `pip install`, keine Umgebungsvariablen, keinen Healthcheck. Man würde das Image bauen und mit einem interaktiven TTY starten:

```bash
docker build -t neongrid9 .
docker run -it --rm neongrid9
```

Das einzige, was man beachten müsste, ist das Speichern: Ohne ein gemountetes Volume wären die Spielstände nach Container-Exit weg. Man müsste also ergänzen:

```bash
docker run -it --rm -v "$HOME/.neongrid9:/root/.neongrid9" neongrid9
```

Aber das zeigt genau, warum es keine Dockerfile gibt: Das Projekt gewinnt durch Containerisierung nichts.

---

## Deployment-Szenarien, die *natürlich* passen

Auch ohne Docker oder CI/CD gibt es plausible Wege, wie dieses Projekt verteilt werden könnte:

### 1. Git-Clone (aktueller Zustand)

```bash
git clone <repo>
cd neongrid9
python3 main.py
```

Das ist die beabsichtigte Verteilungsmethode. Sie setzt voraus, dass der Nutzer Git und Python 3.10+ hat.

### 2. GitHub Releases mit Zip/Archive

Ein `git archive` oder ein GitHub-Release-Asset als `.zip`/`.tar.gz` würde das Spiel an Nutzer bringen, die kein Git installiert haben. Der Nutzer entpackt und startet.

### 3. System-Paketierung (Linux)

Weil es keine Abhängigkeiten gibt, lässt sich das Spiel leicht in ein System-Paket verpacken:

- **Debian/Ubuntu:** Ein `.deb`-Paket, das die Python-Dateien nach `/usr/share/games/neongrid9/` kopiert und einen Wrapper-Skript nach `/usr/bin/neongrid9` legt.
- **Arch Linux:** Ein `PKGBUILD`, das `git clone` oder ein Release-Tarball nutzt.
- **Fedora/RHEL:** Ein `.rpm`-Paket auf ähnliche Weise.

Der gesamte Build-Prozess wäre: Dateien kopieren, ausführbar machen, optional einen Desktop-Eintrag erstellen.

### 4. PyInstaller / cx_Freeze (Standalone-Binary)

Mit PyInstaller könnte man das Projekt in eine einzelne ausführbare Datei packen, die Python selbst mitbringt. Der Nutzer braucht dann überhaupt kein Python auf seinem System.

```bash
pyinstaller --onefile main.py
```

Das Ergebnis wäre eine ~5-15 MB große Datei, die auf dem Zielsystem direkt läuft. Für ein Lernspiel, das an Schulen oder in Trainingsumgebungen verteilt werden soll, wäre das eine sehr praktikable Option.

### 5. Nix / Homebrew

Für erfahrenere Nutzer könnte das Projekt als Nix-Package oder Homebrew-Formula verfügbar gemacht werden:

```bash
nix run github:owner/neongrid9
# oder
brew install neongrid9
```

Das wäre elegant, aber die Zielgruppe (Linux-Anfänger) nutzt diese Tools typischerweise nicht.

---

## Skalierbarkeit: Was bedeutet das hier?

Das Wort "Skalierbarkeit" hat in diesem Projekt eine andere Bedeutung als bei einem Web-Service.

### Horizontale Skalierung

Es gibt keine. Das Spiel ist ein Single-User-Prozess. Mehrere Instanzen können parallel laufen (jede mit eigenem Save-Slot), aber sie teilen keinen Zustand.

### Vertikale Skalierung

Auch nicht relevant. Der Speicherverbrauch liegt im niedrigen zweistelligen Megabyte-Bereich. Die CPU-Last ist vernachlässigbar (Textausgabe und User-Input-Warten). Es gibt keinen Algorithmus, der durch mehr CPU oder RAM schneller würde.

### "Content-Skalierbarkeit"

Das einzige, was "wächst", ist der Content. Die Architektur ist darauf vorbereitet:

- Neue Kapitel werden als neue Dateien in `missions/` hinzugefügt.
- Sie werden in `main.py` in die `CHAPTERS`-Liste importiert.
- Kein anderer Code muss angefasst werden.

Das bedeutet: Ein Content-Autor kann Kapitel 23, 24, 25 schreiben, ohne die Engine zu verstehen. Das ist die wahre Skalierbarkeit dieses Projekts — **horizontale Content-Erweiterung**, nicht horizontale Lastverteilung.

---

## Was eine CI/CD-Pipeline hier tun würde

Es gibt keine `.github/workflows/`, `.gitlab-ci.yml` oder Ähnliches. Das ist vernünftig, weil es aktuell nichts zu "bauen" gibt.

Falls das Projekt wachsen würde, wären diese CI/CD-Schritte sinnvoll:

1. **Linting:** `ruff check .` oder `flake8`
2. **Typprüfung:** `mypy engine/ missions/ main.py`
3. **Unit-Tests:** `pytest` für `save_system`, `player`, `features`
4. **Content-Audit:** Ein Skript, das prüft, ob alle Missionen die Pflichtfelder (`mission_id`, `title`, `quiz_questions`, `exam_tip`, etc.) haben.
5. **PyInstaller-Build:** Erzeugung einer `.exe` (Windows) und einer Linux-Binary bei jedem Release-Tag.

Aber für den aktuellen Stand (Version 1.0, rein lokal) wäre das Overhead.

---

## Zusammenfassung für Infrastruktur-Entwickler

| Aspekt | Realität |
|--------|----------|
| **Build-Prozess** | Keiner. `python3 main.py` reicht. |
| **Dependencies** | Zero. Pure stdlib. |
| **Container** | Nicht vorhanden. Nicht nötig. |
| **CI/CD** | Nicht vorhanden. Nicht nötig. |
| **Datenbank** | Keine. JSON-Dateien im Home-Verzeichnis. |
| **Server** | Keiner. Single-Player-Client. |
| **Netzwerk** | Keiner. Alles lokal. |
| **Skalierbarkeit** | Nicht anwendbar. |
| **Verteilung** | Git-Clone oder Zip-Download. |
| **Zielplattformen** | Alles mit Python 3.10+ und Terminal. |

Das Projekt ist architektonisch ein **Endnutzer-Tool**, kein Service. Wenn du als Infrastruktur-Entwickler hier ankommst und nach Kubernetes, Terraform oder Load-Balancern suchst — du bist an der falschen Stelle. Die Infrastruktur dieses Projekts ist die Python-Laufzeitumgebung auf dem Rechner des Spielers.
