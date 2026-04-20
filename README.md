# NeonGrid-9

```
╔══════════════════════════════════════════════════════════════════╗
║  NEONGRID-9 :: LPIC-1 COMBAT TRAINING SYSTEM                     ║
║  Version 2.0  |  22 Kapitel — 500 Missionen                      ║
║                                                                  ║
║  "The system does not care who you are.                          ║
║   Only what you know."                                           ║
║                                             Powered By Chaoswerk ║
╚══════════════════════════════════════════════════════════════════╝
```

> Ein Cyberpunk-Terminal-Lernspiel für die LPIC-1-Zertifizierung.  
> Kein Browser. Kein GUI. Kein Bullshit. Nur Terminal.

---

## Schnellstart

```bash
python3 main.py
```

**Voraussetzungen:** Python 3.10+ · Keine externen Abhängigkeiten

---

## Statistiken

| Stat | Wert |
|---|---|
| Kapitel | 22 |
| Missionen | 500 |
| Max XP | 47 410 |
| LPIC-1 Domains | 101.x – 110.x |
| Fraktionen | 5 |
| Prüfungsmodus | 26 Blöcke / LPIC-1 komplett |

---

## Kapitelübersicht

| Ch | Titel | LPIC Topic | Missionen |
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
| 18 | EXAM PROTOCOL | ALL | 26 |
| 19 | GHOST PROTOCOL II | 102.6 | 18 |
| 20 | FIREWALL DOMINION | 109.4 | 21 |
| 21 | NETWORK SERVICES | 109.2 | 22 |
| 22 | STORAGE ADVANCED | 104.1 | 22 |

---

## LPIC-1 Coverage

| Domain | Thema | Kapitel |
|---|---|---|
| 101.1 | Hardware & BIOS | Ch01, Ch13 |
| 101.2 | Boot-Manager & GRUB2 | Ch02 |
| 101.3 | SysVinit & systemd | Ch03 |
| 102.4–6 | Pakete, Bibliotheken, Container | Ch12, Ch19 |
| 103.1–7 | Shell, Prozesse, Regex | Ch06, Ch07, Ch08 |
| 104.1–7 | Dateisysteme & Partitionen | Ch04, Ch22 |
| 105.1–2 | Shell-Env & Scripting | Ch17, Ch14 |
| 107.1–3 | User, Gruppen, Locale | Ch10, Ch16 |
| 108.1–2 | Logs, cron, MTA | Ch11 |
| 109.1–4 | Netzwerk, Firewall, Services | Ch09, Ch20, Ch21 |
| 110.1–3 | Security, VPN, Verschlüsselung | Ch15, Ch20 |

---

## Mission-Typen

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
| Kernel Syndicate | Kernel, Boot, Hardware | Ch01–03, Ch11 |
| Root Collective | Dateisysteme, User, Scripting | Ch04–05, Ch10, Ch14 |
| Net Runners | Netzwerk, Shell, Regex | Ch06, Ch08–09, Ch21 |
| Ghost Processors | Container, Kernel-Internals | Ch07, Ch13, Ch19 |
| Firewall Dominion | Security, Firewall, VPN | Ch15, Ch20 |

---

## Spielsystem

**Charakterentwicklung**
- XP sammeln durch Missionen und Quiz-Antworten
- Level 1–20 mit steigenden Anforderungen
- Gear-Rewards für besondere Leistungen (Boss-Missionen)
- Fraktions-Reputation durch chapter-spezifische Missionen

**Speichersystem**
- 3 Speicherslots (`~/.neongrid9_save_N.json`)
- Auto-Save nach jeder Mission
- Fortschritt wird kapitelweise gespeichert

**Prüfungsmodus (Kapitel 18)**
- 26 Exam-Blöcke mit LPIC-1-Stil Fragen
- Alle Domains 101–110 abgedeckt
- Boss: Simulierte LPIC-1-Prüfung

---

## Projektstruktur

```
neongrid9/
├── main.py                    # Game Loop, CHAPTERS, Menüs
├── engine/
│   ├── display.py             # ANSI-Terminal, Farben, Animationen
│   ├── mission_engine.py      # Mission/QuizQuestion Dataclasses, Runner
│   ├── player.py              # Player, Level, Gear, XP
│   └── save_system.py         # JSON Speicherslots
└── missions/
    ├── ch01_hardware.py       # 31 Missionen
    ├── ch02_boot.py           # 20 Missionen
    ├── ch03_init.py           # 32 Missionen
    ├── ch04_partitions.py     # 22 Missionen
    ├── ch05_permissions.py    # 20 Missionen
    ├── ch06_shell.py          # 20 Missionen
    ├── ch07_processes.py      # 20 Missionen
    ├── ch08_regex_vi.py       # 25 Missionen
    ├── ch09_network.py        # 20 Missionen
    ├── ch10_users.py          # 22 Missionen
    ├── ch11_logging.py        # 22 Missionen
    ├── ch12_packages.py       # 21 Missionen
    ├── ch13_kernel.py         # 25 Missionen
    ├── ch14_scripting.py      # 25 Missionen
    ├── ch15_security.py       # 22 Missionen
    ├── ch16_locale.py         # 22 Missionen
    ├── ch17_shellenv.py       # 22 Missionen
    ├── ch18_exam.py           # 26 Missionen
    ├── ch19_ghost_processors.py # 18 Missionen
    ├── ch20_firewall_dominion.py # 21 Missionen
    ├── ch21_network_services.py  # 22 Missionen
    └── ch22_storage_advanced.py  # 22 Missionen
```

---

## Entwicklung


---

*Powered By Chaoswerk*
