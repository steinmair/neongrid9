# NeonGrid-9

```
╔══════════════════════════════════════════════════════════════════╗
║  NEONGRID-9 :: Linux KAMPFTRAINING-SYSTEM                       ║
║  Version 1.0  |  22 Kapitel — 501 Missionen                      ║
║                                                                  ║
║  "Das System kümmert sich nicht, wer du bist.                    ║
║   Nur, was du weißt."                                            ║
║                                             Powered By Chaoswerk ║
╚══════════════════════════════════════════════════════════════════╝
```

> Ein Cyberpunk-Terminal-Lernspiel für Linux-Systemadministration.  
> Kein Browser. Kein GUI. Kein Bullshit. Nur Terminal.

---

## 🚀 Schnellstart

```bash
python3 main.py
```

**Voraussetzungen:** Python 3.10+ · Keine externen Abhängigkeiten

---

## 📊 Statistiken

| Stat | Wert |
|---|---|
| Kapitel | 22 |
| Missionen | 501 |
| Boss-Missionen | 22 |
| Quiz-Fragen | 1.117 |
| Max XP | 51.540 |
| Linux Domains | 101.x – 110.x |
| Fraktionen | 5 |
| Prüfungsmodus | Kapitel 22 (Grand Finale) |
| Hint-Abdeckung | 88,6 % (444/501) |

---

## Kapitelübersicht

| Kp | Titel | Topic | Missionen |
|---|---|---|---|
| 01 | BOOT CAMP | 101.1 | 31 |
| 02 | DARK BOOT | 101.2 | 20 |
| 03 | GHOST PROTOCOL | 101.3 | 32 |
| 04 | PARTITION WARS | 104.1 | 22 |
| 05 | PERMISSION MATRIX | 104.5 | 20 |
| 06 | DATA STREAMS | 103.2 | 20 |
| 07 | GHOST PROCESS | 103.5 | 20 |
| 08 | REGEX PROTOCOL | 103.7 | 25 |
| 09 | NET PROTOCOL | 109.1 | 20 |
| 10 | USER MATRIX | 107.1 | 22 |
| 11 | SYSLOG MATRIX | 108.1 | 22 |
| 12 | INSTALL PROTOCOL | 102.4 | 21 |
| 13 | KERNEL FORGE | 101.1 | 25 |
| 14 | SCRIPT PROTOCOL | 105.2 | 25 |
| 15 | SECURITY PROTOCOL | 110.1 | 22 |
| 16 | LOCALE MATRIX | 107.3 | 22 |
| 17 | SHELL ENV | 105.1 | 22 |
| 18 | STORAGE ADVANCED | 104.1 | 22 |
| 19 | GHOST PROTOCOL II | 102.6 | 18 |
| 20 | FIREWALL DOMINION | 109.4 | 21 |
| 21 | NETWORK SERVICES | 109.2 | 22 |
| 22 | FINAL EXAM PROTOCOL | ALL | 27 |

---

## Linux-Abdeckung

| Domain | Thema | Kapitel |
|---|---|---|
| 101.1 | Hardware & BIOS | Kp01, Kp13 |
| 101.2 | Boot-Manager & GRUB2 | Kp02 |
| 101.3 | SysVinit & systemd | Kp03 |
| 102.4–6 | Pakete, Bibliotheken, Container | Kp12, Kp19 |
| 103.1–7 | Shell, Prozesse, Regex | Kp06, Kp07, Kp08 |
| 104.1–7 | Dateisysteme & Partitionen | Kp04, Kp18, Kp22 |
| 105.1–2 | Shell-Env & Scripting | Kp17, Kp14 |
| 107.1–3 | User, Gruppen, Locale | Kp10, Kp16 |
| 108.1–2 | Logs, cron, MTA | Kp11 |
| 109.1–4 | Netzwerk, Firewall, Services | Kp09, Kp20, Kp21 |
| 110.1–3 | Security, VPN, Verschlüsselung | Kp15, Kp20 |

---

## Missionstypen

| Typ | Beschreibung |
|---|---|
| `SCAN` | Konzept lernen & Befehl ausführen |
| `CONSTRUCT` | System konfigurieren & aufbauen |
| `INFILTRATE` | Sicherheitstests & Analyse |
| `DECODE` | Ausgaben & Logs interpretieren |
| `REPAIR` | Kaputte Systeme reparieren |
| `QUIZ` | Wissenstest mit mehreren Fragen |
| `BOSS` | Kapitel-Boss — alle Konzepte kombiniert |

---

## Fraktionen

| Fraktion | Thema | Präsenz |
|---|---|---|
| Kernel Syndicate | Kernel, Boot, Hardware | Kp01–03, Kp11 |
| Root Collective | Dateisysteme, User, Scripting | Kp04–05, Kp10, Kp14 |
| Net Runners | Netzwerk, Shell, Regex | Kp06, Kp08–09, Kp21 |
| Ghost Processors | Container, Kernel-Internals | Kp07, Kp13, Kp19 |
| Firewall Dominion | Security, Firewall, VPN | Kp15, Kp20 |

---

## Spielsystem

**Charakterentwicklung**
- XP sammeln durch Missionen und Quiz-Antworten
- Level 1–20 mit steigenden Anforderungen
- Gear-Rewards für besondere Leistungen (Boss-Missionen)
- Fraktions-Reputation durch kapitelspezifische Missionen

**Speichersystem**
- 3 Speicherslots (`~/.neongrid9_save_N.json`)
- Auto-Save nach jeder Mission
- Fortschritt wird kapitelweise gespeichert

**Prüfungsmodus (Kapitel 22 — GRAND FINALE)**
- 26 Exam-Blöcke mit Linux-Stil Fragen
- Alle Domains 101–110 komplett abgedeckt
- Boss: Simulierte Linux-Prüfung (Höhepunkt)

---

## 📚 Dokumentation

Neue Spieler sollten in dieser Reihenfolge lesen:
1. **[GAMEPLAY_GUIDE.md](GAMEPLAY_GUIDE.md)** — Wie man spielt, Missionstypen, Progression, Achievements
2. **[LINUX_TOPICS.md](LINUX_TOPICS.md)** — Kapitel zu Linux-Topics (101–110) zuordnen
3. **[TIPS_TRICKS.md](TIPS_TRICKS.md)** — Fortgeschrittene Strategien, Speedrun-Taktiken, Optimierung

---

## Spielstatus

**Version 1.0 — Produktionsreif** ✅

- ✅ Alle 501 Missionen vollständig implementiert
- ✅ 22 Kapitel mit kohärenter Story
- ✅ 18 Achievements mit funktionierenden Unlock-Triggern
- ✅ XP/Schwierigkeit ausbalanciert (kein Grinding nötig)
- ✅ 88,6 % Hint-Abdeckung (444/501 Missionen)
- ✅ Erweitertes Player-Profil mit detaillierten Statistiken
- ✅ Umfassende Dokumentation (50+ KB)
- ✅ Alle Tests bestanden (5/5 Test-Suite)
- ✅ Null Warnungen/Fehler

### Spielen

```bash
python3 main.py
```

### Test-Suite

```bash
python3 scripts/test_gameflow.py
```

---

## Installation & Verbreitung

### Systemanforderungen
- Python 3.10+
- Terminal/Befehlszeile
- ~50 MB Speicherplatz
- Keine externen Abhängigkeiten

### Schnelleinstieg

```bash
git clone <this-repo>
cd neongrid9
python3 main.py
```

### Geschätzte Spielzeit

- Einzelnes Kapitel: 25–35 Minuten
- Vollständiges Spiel (Kp01-22): 15–25 Stunden
- Speedrun (alle Kapitel): 4–5 Stunden
- Completionist (alle Achievements): 25–30 Stunden

---

## 📖 Lernpfade

### Zur Prüfungsvorbereitung

1. Lies **LINUX_TOPICS.md**, um die Abdeckung zu verstehen
2. Absolviere die Kapitel der Reihe nach (Kp01-22)
3. Konzentriere dich auf Kapitel, die Prüfungsdomains entsprechen
4. Nutze **TIPS_TRICKS.md** für Optimierungsstrategien
5. Referenziere Befehle für praktische Linux-Übungen

### Zum allgemeinen Linux-Lernen

1. Starten mit **GAMEPLAY_GUIDE.md**
2. Alle 22 Kapitel der Reihe nach spielen
3. Story-Narration lesen (sie lehren Konzepte)
4. Hints strategisch nutzen
5. Kapitel wiederholen zur Mastery

### Zum Speedrunning

1. Lies **TIPS_TRICKS.md** Speedrun-Sektion
2. Lerne Missionssmuster
3. Optimiere Quiz-Antworten
4. Verfolge persönliche Best-Zeiten
5. Ziel: < 30 min pro Kapitel

---

## Projektstruktur

```
neongrid9/
├── main.py                              # Einstiegspunkt, Game Loop
├── engine/
│   ├── display.py                      # Terminal UI, ANSI-Farben, Formatierung
│   ├── mission_engine.py                # Mission-System, Achievement-Trigger
│   ├── player.py                        # Player-Profil, XP, Leveling, Statistiken
│   ├── features.py                      # 18 Achievements, Hints, Fraktionen
│   ├── terminal_sim.py                  # Terminal-Simulator
│   └── save_system.py                   # Speichern/Laden-System
├── missions/
│   ├── ch01_hardware.py                 # 31 Missionen (Hardware-Grundlagen)
│   ├── ch02_boot.py                     # 20 Missionen (Boot-Prozess)
│   ├── ch03_init.py                     # 32 Missionen (Init-Systeme)
│   ├── ch04_partitions.py               # 22 Missionen (Partitionen/Festplatten)
│   ├── ch05_permissions.py              # 20 Missionen (Dateiberechtigungen)
│   ├── ch06_shell.py → ch22_exam.py     # Kapitel 6-22 (440 Missionen insgesamt)
└── Dokumentation/
    ├── README.md                        # Diese Datei
    ├── GAMEPLAY_GUIDE.md                # Spielanleitung (15 KB)
    ├── LINUX_TOPICS.md                  # Topic-Zuordnung (20 KB)
    └── TIPS_TRICKS.md                   # Fortgeschrittene Strategien (18 KB)
```

---

## Inhaltsstatistiken

| Metrik | Anzahl | Status |
|--------|--------|--------|
| Gesamt Missionen | 501 | ✅ Vollständig |
| Kapitel | 22 | ✅ Vollständig |
| Boss-Missionen | 22 | ✅ Vollständig |
| Quiz-Fragen | 1.117+ | ✅ Vollständig |
| Achievements | 18 | ✅ Vollständig |
| Fraktionen | 5 | ✅ Vollständig |
| Gear-Items | 20+ | ✅ Vollständig |
| Gesamt XP | 51.540 | ✅ Ausbalanciert |
| Hint-Abdeckung | 444/501 (88,6%) | ✅ Vollständig |

---

## Entwicklung & Tests

### Tests ausführen

```bash
python3 scripts/test_gameflow.py
```

### Test-Abdeckung

- ✅ Mission-Laden (501 Missionen)
- ✅ Player-Systeme (XP, Leveling, Achievements)
- ✅ Mission-Datenintegritä (Hints, Befehle, Format)
- ✅ Quiz-Fragen (Format, Antworten, Erklärungen)
- ✅ Kapitelzugriff (alle 22 Kapitel verifiziert)

**Ergebnis:** ✅ ALLE TESTS BESTANDEN (5/5)

### Eine Mission debuggen

```python
import sys
sys.path.insert(0, '/home/ande/neongrid9')
from missions.ch01_hardware import CHAPTER_1_MISSIONS
mission = CHAPTER_1_MISSIONS[0]
print(f"Mission: {mission.title}")
print(f"XP: {mission.xp}")
print(f"Hints: {mission.hints}")
```

---

## Lizenz & Zuschreibung

**NeonGrid-9** — Linux Cyberpunk Lernspiel

*Ein cyberpunk-inspiriertes Terminal-Lernspiel für Linux-Systemadministration.*

Mit pädagogischer Absicht erstellt: Komplexe Linux-Systemverwaltungskonzepte durch interaktives Gameplay zugänglich machen.

---

*Powered By Chaoswerk*  
*Produktionsreif* 🚀
