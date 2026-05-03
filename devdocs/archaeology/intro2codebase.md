# NeonGrid-9 :: Einführung in die Code-Architektur

> Für neue Entwickler: Wie das Projekt strukturiert ist, ohne in jede Datei abzutauchen.

## Kernphilosophie

Das Projekt ist ein **zustandsbasierter, textbasierter Lern-Client**.
Es gibt keinen Server, keine Datenbank und kein Netzwerk. Alles läuft lokal in einem Python-Prozess, der den Terminal-Bildschirm als Canvas nutzt.

Die Architektur folgt einem einfachen Prinzip:

**Daten + Engine = Spiel**

- **Daten** = 22 Kapitel mit Missionen, Quizfragen und ASCII-Art.
- **Engine** = Ein Satz von Python-Modulen, die diese Daten in ein interaktives Erlebnis verwandeln.

---

## Die drei Hauptschichten

Wenn du das Projekt zum ersten Mal siehst, denke an drei klar getrennte Schichten:

### 1. Daten-Schicht (`missions/`)

Hier lebt der *Content*. Jedes Kapitel ist eine eigene Python-Datei, die eine Liste von `Mission`-Objekten exportiert. Eine Mission enthält:

- Story-Texte, Erklärungen, Syntax-Beispiele
- Terminal-Aufgaben (erwartete Befehle)
- Quizfragen mit Optionen und Erklärungen
- Belohnungen (XP, Gear, Fraktions-Reputation)

**Wichtig:** Diese Dateien enthalten fast keine Logik. Sie sind reine Datenstrukturen. Das macht es sehr einfach, neue Kapitel hinzuzufügen oder bestehende zu bearbeiten, ohne den Rest der Engine zu berühren.

### 2. Engine-Schicht (`engine/`)

Dies ist das *Herzstück*. Sie besteht aus fünf Modulen mit klar definierten Verantwortlichkeiten:

| Modul | Aufgabe |
|-------|---------|
| `mission_engine.py` | Führt eine einzelne Mission aus (Story → Erklärung → Terminal → Quiz → Belohnung) |
| `player.py` | Hält den Spieler-Zustand (XP, Level, Inventar, Fortschritt) |
| `display.py` | Rendert alles auf den Bildschirm (Farben, Boxen, ASCII-Art, Prompts) |
| `terminal_sim.py` | Simuliert Linux-Befehle, ohne echte Prozesse zu starten |
| `save_system.py` | Serialisiert den Spieler-Zustand als JSON in `~/.neongrid9/` |
| `features.py` | Helfer für Hints, Achievements und Fraktions-Level |

### 3. Steuerungs-Schicht (`main.py`)

Das ist der *Dirigent*. Er initialisiert die Engine, zeigt die Menüs an und leitet den Spieler durch den Hauptzyklus:

```
Main Menu → (Neues Spiel / Laden) → Game Hub → Kapitel → Mission → Speichern
```

`main.py` ist auch der Ort, an dem alle 22 Kapitel importiert und in einer großen `CHAPTERS`-Liste registriert werden.

---

## Die zentrale Abstraktion: `MissionRunner`

Die wichtigste Klasse für das Verständnis des Spielablaufs ist `MissionRunner` in `engine/mission_engine.py`.

Sie implementiert eine **State Machine** für den Lern-Fluss:

```
START
  │
  ▼
[Header anzeigen] ──► [ASCII-Art] ──► [Story]
  │
  ▼
[Erklärung] ──► [Syntax] ──► [Beispiel]
  │
  ▼
[Terminal-Aufgabe]  ←── Der Spieler tippt Befehle
  │
  ▼
[Quiz]  ←── Der Spieler beantwortet Fragen
  │
  ▼
[XP berechnen] ──► [Level-Up prüfen] ──► [Achievements prüfen]
  │
  ▼
ENDE (Speichern)
```

`MissionRunner` hält eine Referenz auf ein `Player`-Objekt. Nach jedem Schritt aktualisiert es dessen Zustand. Das ist der primäre **Datenfluss**: Die Mission gibt Inhalte vor, der Spieler interagiert, und das Ergebnis fließt zurück in den `Player`.

---

## Spieler-Zustand und XP-Fluss

`Player` (in `engine/player.py`) ist ein reiner Dataclass-Container. Er speichert:

- **Identität:** Name, XP, Level, Titel
- **Fortschritt:** Abgeschlossene Missionen (als `Set[str]`), Quiz-Genauigkeit pro Kapitel
- **Besitz:** Inventar (Gear-IDs), Fraktions-Reputation
- **Statistiken:** Gesamtspielzeit, Boss-Kills, verwendete Hinweise

Der XP-Fluss folgt einem klaren Muster:

```
Mission wird abgeschlossen
    │
    ▼
Basis-XP der Mission (z.B. 40)
    + Quiz-Bonus (z.B. +30 für 2 richtige Fragen)
    = Roh-XP
    │
    ▼
Player.add_xp(Roh-XP)
    │
    ▼
Level-Skalierungsbonus (z.B. +10% ab Level 5)
    │
    ▼
Persistenz: save_system speichert Player.to_dict() als JSON
```

Achievements und Gear-Boni werden *nach* der XP-Vergabe geprüft und können ihrerseits wieder XP auslösen (Kaskadeneffekt).

---

## Design Patterns auf hoher Ebene

### 1. Singleton State (`GameState`)

`main.py` definiert eine globale Instanz `GAME = GameState()`. Diese existiert genau einmal pro Prozess und koordiniert:

- Den aktiven Spieler (`GAME.player`)
- Den aktiven Save-Slot (`GAME.save_slot`)
- Ob das Spiel läuft (`GAME.running`)

Das ist kein klassisches Singleton-Pattern (mit verstecktem Konstruktor), aber es folgt derselben Absicht: Es gibt eine einzige Quelle der Wahrheit für den Spielzustand.

### 2. Command Pattern (Terminal-Simulation)

`engine/terminal_sim.py` nutzt ein großes Dictionary namens `SIMULATED_OUTPUTS`:

```python
SIMULATED_OUTPUTS = {
    "lspci": "...",          # vorgefertigte Ausgabe
    "lsusb -t": "...",       # vorgefertigte Ausgabe
    ...
}
```

Wenn der Spieler einen Befehl tippt, wird er nicht an eine echte Shell weitergegeben. Stattdessen wird der Befehls-String als Schlüssel in dieses Dictionary geschlagen, und die vorgefertigte Antwort wird gedruckt.

Das ist ein **Command Pattern** in seiner einfachsten Form: Ein String repräsentiert einen Befehl, und ein Lookup liefert das Ergebnis.

### 3. Observer Pattern (Achievements)

Achievements werden nicht bei jeder Aktion einzeln geprüft. Stattdessen gibt es einen zentralen Checkpoint: **Nach Abschluss jeder Mission** ruft `MissionRunner` eine Reihe von Prüffunktionen auf:

- Hat der Spieler 100 Missionen abgeschlossen? → Achievement `quest_marathon`
- Hat der Spieler 5 Bosse besiegt? → Achievement `five_bosses`
- Ist der Spieler Level 10? → Achievement `level_ten`

Das Achievement-System *beobachtet* den Zustandswechsel des Spielers und reagiert darauf.

### 4. Strategy Pattern (Mission Types)

Missionen haben unterschiedliche Typen (`SCAN`, `INFILTRATE`, `BOSS`, `QUIZ`, etc.). Intern verzweigt `MissionRunner.run()` basierend auf `mission.mtype`:

- `BOSS` → Ruft `_run_boss()` auf (mehrere Phasen, höhere Schwierigkeit)
- `QUIZ` → Überspringt den Terminal-Teil, zeigt nur Quiz
- `SCAN`/`INFILTRATE` → Voller Fluss mit Terminal-Simulation

Das ist ein einfaches **Strategy Pattern**: Je nach Typ wird ein anderer Algorithmus gewählt, um die Mission auszuführen.

### 5. Template Method (Mission Execution)

Trotz der Typ-Unterschiede folgen fast alle Missionen demselben *Template*:

```
Header → Story → Erklärung → (Terminal) → Quiz → Ergebnis
```

`MissionRunner.run()` ist die Template-Methode, die diesen Ablauf erzwingt. Die konkreten Schritte (z.B. ob ein Terminal-Task existiert) variieren je nach Mission, aber die Reihenfolge ist immer gleich.

---

## Datenfluss-Pfade (die wichtigsten)

### Pfad A: Neues Spiel starten

```
main.py:main_menu()
    │
    ▼
new_game_menu()  →  Erstellt Player(name="Ghost")
    │
    ▼
GameState.player = Player
    │
    ▼
show_story_prologue()  →  typewrite()-Animation
    │
    ▼
game_hub()  →  Zeigt Fortschritt aller Kapitel
```

### Pfad B: Eine Mission spielen

```
game_hub()
    │
    ▼
chapter_menu(ch_id)
    │
    ▼
MissionRunner.run(mission)
    │
    ├──► engine/display.py  →  Zeigt Story, Farben, ASCII
    │
    ├──► engine/terminal_sim.py  →  Spieler tippt Befehl, Sim gibt Ausgabe
    │
    ├──► _run_quiz()  →  Spieler wählt A/B/C/D, Erklärung wird gezeigt
    │
    └──► Player.add_xp()  →  Level-Up? Achievements?
    │
    ▼
GameState.auto_save(player)  →  JSON nach ~/.neongrid9/
```

### Pfad C: Prüfungssimulation (Timed Exam)

```
game_hub() → timed_exam_mode()
    │
    ▼
Sammelt 60 Quizfragen aus ch22_exam.py
    │
    ▼
Zeigt Frage + Live-Timer (90 Minuten)
    │
    ▼
Spieler antwortet → Ergebnis wird sofort geprüft
    │
    ▼
Am Ende: Berechnet Linux-Score (0-800), zeigt Pass/Fail
```

### Pfad D: Laden eines Spielstands

```
main.py:load_game_menu()
    │
    ▼
save_system.load_game(slot)  →  Liest JSON
    │
    ▼
Player.from_dict(data)  →  Rekonstruiert Player-Objekt
    │
    ▼
GameState.player = Player
```

---

## Was das über die Code-Qualität sagt

- **Klare Trennung:** Daten (`missions/`), Logik (`engine/`) und Steuerung (`main.py`) sind physisch getrennt.
- **Keine externen Abhängigkeiten:** Das Spiel nutzt nur die Python-Standardbibliothek. Kein pip, kein Framework, keine UI-Widgets. Das reduziert die Komplexität drastisch.
- **Immutability bei Content:** Missionen und Quizfragen sind als `dataclass` definiert und werden zur Laufzeit nicht verändert. Der einzige mutable Zustand ist `Player`.
- **Deterministisch:** Da keine Netzwerk- oder Dateisystem-Operationen außerhalb der Speicherstände passieren, ist das Verhalten vorhersehbar und leicht zu testen.

---

## Zusammenfassung für den Einstieg

Wenn du als neuer Entwickler in dieses Projekt kommst:

1. **Lies `engine/mission_engine.py`** — Das ist der Dreh- und Angelpunkt. Wenn du verstehst, wie `MissionRunner.run()` arbeitet, verstehst du 80% des Spiels.
2. **Schaue in `missions/ch01_hardware.py`** — So sehen die Rohdaten aus. Pure Python-Datenstrukturen.
3. **Öffne `main.py` ab Zeile 390** — `game_hub()` und `chapter_menu()` zeigen, wie die Navigation zwischen Kapiteln und Missionen funktioniert.
4. **Alles andere ist Dekoration:** `display.py` macht es hübsch, `terminal_sim.py` macht es sicher, `save_system.py` macht es persistent.

Das Projekt ist im Kern ein sehr eleganter **Daten-getriebener Zustandsautomat** mit einer Cyberpunk-Verpackung.
