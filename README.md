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
| Missionen | 501 |
| Boss-Missionen | 22 |
| Quiz-Fragen | 1 117 |
| Max XP | 47 610 |
| LPIC-1 Domains | 101.x – 110.x |
| Fraktionen | 5 |
| Prüfungsmodus | 27 Blöcke / LPIC-1 komplett |
| Quiz-Abdeckung | 100 % (501/501) |

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
| 18 | EXAM PROTOCOL | ALL | 27 |
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

## 📚 Documentation

New players should read in this order:
1. **[GAMEPLAY_GUIDE.md](GAMEPLAY_GUIDE.md)** — How to play, mission types, progression, achievements
2. **[LPIC_1_MAPPING.md](LPIC_1_MAPPING.md)** — Map chapters to LPIC-1 exam topics (101 & 102)
3. **[TIPS_TRICKS.md](TIPS_TRICKS.md)** — Advanced strategies, speedrun tactics, optimization

For development status:
- **[PERFECTION_COMPLETE.md](PERFECTION_COMPLETE.md)** — Final implementation report & checklist
- **[PERFECTION_ROADMAP.md](PERFECTION_ROADMAP.md)** — Implementation guide & strategy

---

## 🎮 Game Status

**Version 1.0 — Production Ready** ✅

- ✅ All 501 missions fully implemented
- ✅ 22 chapters complete with coherent story
- ✅ 18 achievements with working unlock triggers
- ✅ XP/difficulty balanced (no grinding)
- ✅ 88.6% hint coverage (444/501 missions)
- ✅ Enhanced player profile with detailed statistics
- ✅ Comprehensive documentation (50+ KB)
- ✅ All tests passing (5/5 test suite)
- ✅ Zero warnings/errors

### How to Play
```bash
python3 main.py
```

### Test Suite
```bash
python3 scripts/test_gameflow.py
```

---

## 🚀 Installation & Distribution

### System Requirements
- Python 3.8+
- Terminal/command line
- ~50 MB disk space
- No external dependencies

### Quick Start
```bash
git clone <this-repo>
cd neongrid9
python3 main.py
```

### Estimated Playtime
- Single chapter: 25-35 minutes
- Full game (ch01-22): 15-25 hours
- Speedrun (all chapters): 4-5 hours
- Completionist (all achievements): 25-30 hours

---

## 📖 Learning Path

### For LPIC-1 Exam Prep
1. Read **LPIC_1_MAPPING.md** to understand exam coverage
2. Complete chapters sequentially (Ch01-22)
3. Focus on chapters matching exam domains
4. Use **TIPS_TRICKS.md** for optimization strategies
5. Reference commands section for real Linux practice

### For General Linux Learning
1. Start with **GAMEPLAY_GUIDE.md**
2. Play through all 22 chapters in order
3. Read story narratives (they teach concepts)
4. Use hints strategically to learn
5. Repeat chapters for mastery

### For Speedrunning
1. Read **TIPS_TRICKS.md** speedrun section
2. Learn mission patterns
3. Optimize quiz answers
4. Track personal best times
5. Target: < 30 min per chapter

---

## 🏗️ Project Structure (Detailed)

```
neongrid9/
├── main.py                              # Entry point, game loop
├── engine/
│   ├── display.py                      # Terminal UI, ANSI colors, formatting
│   ├── mission_engine.py                # Mission system, QuizQuestion, achievement triggers
│   ├── player.py                        # Player profile, XP, leveling, stats (6 new fields)
│   ├── features.py                      # Achievements (18 total), hints, factions
│   ├── terminal_sim.py                  # Terminal simulator
│   └── save_system.py                   # Save/load persistence
├── missions/
│   ├── ch01_hardware.py                 # 31 missions (Hardware basics)
│   ├── ch02_boot.py                     # 20 missions (Boot process)
│   ├── ch03_init.py                     # 32 missions (Init systems)
│   ├── ch04_partitions.py               # 22 missions (Partitions/disks)
│   ├── ch05_permissions.py              # 20 missions (File permissions)
│   ├── ch06_shell.py → ch22_storage...  # Chapters 6-22 (440 missions total)
└── Documentation/
    ├── README.md                        # This file
    ├── GAMEPLAY_GUIDE.md                # How to play (15 KB)
    ├── LPIC_1_MAPPING.md                # Exam mapping (20 KB)
    ├── TIPS_TRICKS.md                   # Advanced strategies (18 KB)
    ├── PERFECTION_ROADMAP.md            # Implementation guide
    └── PERFECTION_COMPLETE.md           # Final status report
```

---

## 📊 Content Statistics

| Metric | Count | Status |
|--------|-------|--------|
| Total Missions | 501 | ✅ Complete |
| Chapters | 22 | ✅ Complete |
| Boss Missions | 22 | ✅ Complete |
| Quiz Questions | 1,117+ | ✅ Complete |
| Achievements | 18 | ✅ Complete |
| Factions | 5 | ✅ Complete |
| Gear Items | 20+ | ✅ Complete |
| Total XP | 51,540 | ✅ Balanced |
| Hint Coverage | 444/501 (88.6%) | ✅ Complete |

---

## 🧪 Development & Testing

### Running Tests
```bash
python3 scripts/test_gameflow.py
```

### Test Coverage
- ✅ Mission loading (501 missions)
- ✅ Player systems (XP, leveling, achievements)
- ✅ Mission data integrity (hints, commands, format)
- ✅ Quiz questions (format, answers, explanations)
- ✅ Chapter access (all 22 chapters verified)

**Result:** ✅ ALL TESTS PASSED (5/5)

### Debugging a Mission
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

## 📄 License & Attribution

**NeonGrid-9** - LPIC-1 Cyberpunk Learning Game

*A cyberpunk-themed terminal learning game for LPIC-1 certification exam prep.*

Created with pedagogical intent: making complex Linux system administration concepts accessible through interactive gameplay.

---

*Powered By Chaoswerk*  
*Ready to Ship* 🚀
