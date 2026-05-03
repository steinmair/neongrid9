# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. **It is also a complete specification for recreating the entire NeonGrid-9 project from scratch.**

---

## Quick Start (Existing Project)

```bash
python3 main.py
```

No external dependencies. Requires Python 3.10+.

---

## Complete Project Specification

### Overview

**NeonGrid-9** is a cyberpunk-themed terminal learning game for LPIC-1 Linux system administration certification.

**Stats:**
- 22 chapters (numbered 1–22)
- 501 total missions (22 per chapter on average: 1 intro + 20 regular + 1 boss)
- 1117 quiz questions with explanations
- 5 factions with reputation systems
- 19 achievements with unlock conditions
- 22 boss missions (chapter finales)
- Levels 1–20 with cumulative XP threshold
- 3 save slots (persistent JSON)
- Terminal simulator with 40+ Linux commands
- Story-driven gameplay with 5 unique faction speakers

**Completeness:** 100% content-complete (2026-04-21 audit). All 501 missions have: quiz_questions, why_important, exam_tip, memory_tip, story_transitions, ascii_art.

---

## Project Structure & File Organization

```
neongrid9/
├── main.py                          # Entry point, game loop, UI
├── CLAUDE.md                        # This file
├── README.md                        # Player documentation
├── GAMEPLAY_GUIDE.md                # Mission types, progression, achievements
├── LINUX_TOPICS.md                  # LPIC domain mapping (101–110)
├── TIPS_TRICKS.md                   # Speedrun strategies, optimization
├── LICENSE                          # MIT
├── .gitignore                       # Python artifacts, save files
│
├── engine/
│   ├── __init__.py                  # (empty)
│   ├── mission_engine.py            # Mission, QuizQuestion dataclasses; MissionRunner
│   ├── display.py                   # ANSI colors (C class), UI functions, typewriter, fast mode
│   ├── player.py                    # Player dataclass, LEVELS (1-20), GEAR_CATALOG, AchievementTracker
│   ├── features.py                  # HintRequest, Achievement, Hint system, Faction system
│   ├── terminal_sim.py              # Terminal simulator + CommandRegistry
│   ├── save_system.py               # Legacy JSON save/load (deprecated, see storage.py)
│   ├── storage.py                   # SaveRepository Protocol, JsonFileRepository, InMemoryRepository
│   ├── save_migrations.py           # v1 → v2 save migration logic
│   ├── renderer.py                  # Renderer Protocol, TerminalRenderer, NullRenderer
│   ├── achievement_engine.py        # Declarative AchievementRule + AchievementEngine
│   ├── menu_builder.py              # MenuBuilder fluent API
│   └── chapter_registry.py          # ChapterRegistry with recap metadata
│
└── missions/
    ├── __init__.py                  # (empty)
    ├── ch01_hardware.py              # CHAPTER_1_MISSIONS: 31 missions
    ├── ch02_boot.py                  # CHAPTER_2_MISSIONS: 20 missions
    ├── ch03_init.py                  # CHAPTER_3_MISSIONS: 32 missions
    ├── ch04_partitions.py            # CHAPTER_4_MISSIONS: 22 missions
    ├── ch05_permissions.py           # CHAPTER_5_MISSIONS: 20 missions
    ├── ch06_shell.py                 # CHAPTER_6_MISSIONS: 20 missions
    ├── ch07_processes.py             # CHAPTER_7_MISSIONS: 20 missions
    ├── ch08_regex_vi.py              # CHAPTER_8_MISSIONS: 25 missions
    ├── ch09_network.py               # CHAPTER_9_MISSIONS: 20 missions
    ├── ch10_users.py                 # CHAPTER_10_MISSIONS: 22 missions
    ├── ch11_logging.py               # CHAPTER_11_MISSIONS: 22 missions
    ├── ch12_packages.py              # CHAPTER_12_MISSIONS: 21 missions
    ├── ch13_kernel.py                # CHAPTER_13_MISSIONS: 25 missions
    ├── ch14_scripting.py             # CHAPTER_14_MISSIONS: 25 missions
    ├── ch15_security.py              # CHAPTER_15_MISSIONS: 22 missions
    ├── ch16_locale.py                # CHAPTER_16_MISSIONS: 22 missions
    ├── ch17_shellenv.py              # CHAPTER_17_MISSIONS: 22 missions
    ├── ch18_storage.py               # CHAPTER_18_MISSIONS: 22 missions
    ├── ch19_ghost_processors.py      # CHAPTER_19_MISSIONS: 18 missions
    ├── ch20_firewall_dominion.py     # CHAPTER_20_MISSIONS: 21 missions
    ├── ch21_network_services.py      # CHAPTER_21_MISSIONS: 22 missions
    └── ch22_final_exam.py            # CHAPTER_22_MISSIONS: 27 missions (Grand Finale)
```

---

## Core Data Structures

### Mission Dataclass

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Mission:
    # Identification
    mission_id: str                 # "1.01", "1.02", ..., "22.22"
    title: str                      # "Erste Signale — Was ist Hardware?"
    mtype: str                      # SCAN | INFILTRATE | DECODE | CONSTRUCT | REPAIR | QUIZ | BOSS
    xp: int                         # Base XP reward (30-225 range)
    chapter: int                    # 1-22

    # Visuals & Story
    ascii_art: str = ""             # Neon ASCII art (displayed on mission start)
    story_transitions: List[str] = field(default_factory=list)  # 4 transition lines between sections
    
    # Narrative Content
    story: str = ""                 # Introductory narrative
    speaker: str = "SYSTEM"         # Character name (ZARA Z3R0, RUST, PHANTOM, CIPHER, LYRA-7, EXAMINATOR, SYSTEM)
    why_important: str = ""         # LPIC exam domain relevance
    explanation: str = ""           # Concept explanation, technical details
    syntax: str = ""                # Command syntax (if applicable)
    example: str = ""               # Example output/demonstration
    
    # Task/Terminal
    task_description: str = ""      # What player must accomplish
    expected_commands: List[str] = field(default_factory=list)  # Valid command patterns player can try
    hint_text: str = ""             # Single-line hint (legacy; use hints list)
    hints: List[str] = field(default_factory=list)  # [free_hint, 20xp_hint, 50xp_final_answer]
    simulated_commands: List[str] = field(default_factory=list)  # Commands shown in example output

    # Quiz
    quiz_questions: List['QuizQuestion'] = field(default_factory=list)  # 1-5 questions per mission

    # Exam & Study
    exam_tip: str = ""              # Exam prep note (e.g., "Remember: LPIC-1 domain 103.1")
    memory_tip: str = ""            # Mnemonic or memory aid

    # Boss-Specific
    boss_name: str = ""             # Boss character name (e.g., "ZARA THE REAPER")
    boss_desc: str = ""             # Boss narrative and challenge description

    # Rewards
    gear_reward: Optional[str] = None  # Gear item ID from GEAR_CATALOG
    faction_reward: Optional[tuple] = None  # (faction_name: str, amount: int)
```

### QuizQuestion Dataclass

```python
@dataclass
class QuizQuestion:
    question: str                   # The question text
    options: List[str]              # ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
    correct: str                    # "A", "B", "C", or "D" (string, not index)
    explanation: str                # Why this is correct (for learning)
    xp_value: int = 15              # XP awarded for correct answer
```

---

## Chapter Definition

Each chapter file exports `CHAPTER_N_MISSIONS` list. **Example structure:**

```python
# missions/ch01_hardware.py
from engine.mission_engine import Mission, QuizQuestion

CHAPTER_1_MISSIONS = [
    # Mission 1.01 — Chapter Intro
    Mission(
        mission_id='1.01',
        title='Erste Signale — Was ist Hardware?',
        mtype='SCAN',
        xp=30,
        chapter=1,
        speaker='ZARA Z3R0',
        story='Ich hab dich bewusstlos im Sector-7-Slum gefunden...',
        why_important='Linux prüft dich auf Hardware-Grundlagen.',
        explanation='Linux erkennt Hardware automatisch beim Boot.',
        # ... rest of fields
    ),
    # Mission 1.02 — Regular mission
    Mission(...),
    # ...
    # Mission 1.22 — Boss mission
    Mission(
        mission_id='1.22',
        mtype='BOSS',
        title='ZARA THE REAPER',
        boss_name='ZARA THE REAPER',
        boss_desc='...',
        quiz_questions=[...],  # 5 expert questions
        xp=225,
        # ...
    ),
]
```

**Chapter Patterns:**
- **.01** — Intro (SCAN, 30-35 XP, story context, 1-3 quiz questions)
- **.02–.21** — Regular missions (mixed types, 40-70 XP, 1-5 quiz questions each)
- **.22** — Boss mission (BOSS type, 220-240 XP, 5 expert quiz questions, faction narrative climax)

---

## Mission Types & Execution Flow

### SCAN
- **Purpose:** Learn concept + execute single command
- **Flow:** Story → Explanation → Task → Validate command → Quiz
- **Terminal:** Single command execution; validates against `expected_commands`

### INFILTRATE
- **Purpose:** Security testing; multi-step terminal tasks
- **Flow:** Story → Explanation → Task → Terminal simulator (REPL) → Quiz
- **Terminal:** Multi-command execution; runs full terminal simulator

### DECODE
- **Purpose:** Interpret output/logs; analysis focus
- **Flow:** Story → Explanation → Example output → Quiz → Explanation
- **Terminal:** No terminal task; pure quiz-based learning

### CONSTRUCT
- **Purpose:** Build/configure system; multi-step construction
- **Flow:** Story → Explanation → Task → Terminal simulator → Quiz
- **Terminal:** Full REPL; validates multi-step configuration

### REPAIR
- **Purpose:** Diagnose and fix broken systems
- **Flow:** Story → Broken state description → Task → Terminal simulator → Quiz
- **Terminal:** Full REPL; validates repair steps

### QUIZ
- **Purpose:** Assess knowledge without terminal task
- **Flow:** Story → Explanation → Quiz (3-5 questions)
- **Terminal:** No terminal; pure quiz assessment

### BOSS
- **Purpose:** Chapter synthesis; all concepts combined
- **Flow:** Story → Boss intro ASCII art → Task summary → Terminal (if applicable) → Quiz (5 expert questions) → Boss outro → XP + gear reward
- **Terminal:** Varies; may include INFILTRATE/CONSTRUCT logic
- **Special:** Awards gear_reward; triggers faction_reward; achievement checks

---

## Chapter Catalog

| ID | Title | Topic | Missions | Focus |
|----|-------|-------|----------|-------|
| 1 | BOOT CAMP | 101.1 | 31 | Hardware & BIOS/UEFI |
| 2 | DARK BOOT | 101.2 | 20 | Boot-Manager & GRUB2 |
| 3 | GHOST PROTOCOL | 101.3 | 32 | SysVinit, systemd & Runlevels |
| 4 | PARTITION WARS | 104.1 | 22 | Partitioning & Filesystems |
| 5 | PERMISSION MATRIX | 104.5 | 20 | File Permissions, Links & FHS |
| 6 | DATA STREAMS | 103.2 | 20 | Shell, Pipes, Redirects & Text Filters |
| 7 | GHOST PROCESS | 103.5 | 20 | Processes, Signals & Priorities |
| 8 | REGEX PROTOCOL | 103.7 | 25 | Regular Expressions & vi Editor |
| 9 | NET PROTOCOL | 109.1 | 20 | TCP/IP, ip, ss, DNS, SSH & Firewall |
| 10 | USER MATRIX | 107.1 | 22 | Users, Groups, sudo & PAM |
| 11 | SYSLOG MATRIX | 108.1 | 22 | Logs, Time Services, cron & at |
| 12 | INSTALL PROTOCOL | 102.4 | 21 | dpkg, apt, rpm, yum/dnf & zypper |
| 13 | KERNEL FORGE | 101.1 | 25 | Modules, /proc, sysctl, udev & dmesg |
| 14 | SCRIPT PROTOCOL | 105.2 | 25 | Bash Scripting: Variables, Loops, Functions |
| 15 | SECURITY PROTOCOL | 110.1 | 22 | SUID, SSH Hardening, GPG, fail2ban, sudo & LUKS |
| 16 | LOCALE MATRIX | 107.3 | 22 | Locale, Timezones, X11, CUPS & Desktop |
| 17 | SHELL ENV | 105.1 | 22 | Startup Files, PATH, Aliases, History & PS1 |
| 18 | STORAGE ADVANCED | 104.1/104.3 | 22 | RAID, LVM, Quotas, iSCSI & btrfs |
| 19 | GHOST PROTOCOL II | 102.6/103.6 | 18 | Container & Virtualization |
| 20 | FIREWALL DOMINION | 109.4/110.1 | 21 | iptables, nftables, VPN & Network Security |
| 21 | NETWORK SERVICES | 109.2/109.4 | 22 | NFS, Samba, DHCP, DNS, LDAP & Network Services |
| 22 | FINAL EXAM PROTOCOL | ALL | 27 | Linux Certification Exam — All Topics (Grand Finale) |

---

## Player & Progression System

### Player Dataclass

```python
@dataclass
class Player:
    name: str
    xp: int = 0                            # Total accumulated XP
    level: int = 1                         # Calculated from XP
    current_chapter: int = 1               # Chapter in progress
    completed_missions: Set[str] = field(default_factory=set)  # {"1.01", "1.02", ...}
    achievements: Dict[str, bool] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)  # Gear item IDs
    factions: Dict[str, int] = field(default_factory=dict)  # {faction: reputation_points}
    chapter_times: Dict[int, float] = field(default_factory=dict)  # {ch: seconds}
    quiz_accuracy: Dict[int, tuple] = field(default_factory=dict)  # {ch: (correct, total)}
```

### Leveling System

```python
LEVELS = [
    (1,  "Newbie Hacker",       0),       # Level 1: 0 XP
    (2,  "Script Kiddie",       500),     # Level 2: 500 XP total
    (3,  "Terminal User",       1500),    # Level 3: 1500 XP total
    (4,  "Shell Dweller",       3000),
    (5,  "Pipe Runner",         5000),
    (6,  "Process Wrangler",    7500),
    (7,  "Filesystem Ghost",    10500),
    (8,  "Package Smuggler",    14000),
    (9,  "Daemon Whisperer",    18000),
    (10, "Net Runner",          22500),
    (11, "Kernel Adept",        27500),
    (12, "Root Initiate",       33000),
    (13, "System Breaker",      39000),
    (14, "Shell Architect",     45500),
    (15, "Certified Ghost",     52500),
    (16, "Kernel Architect",    60000),
    (17, "System Overlord",     68000),
    (18, "Net Phantom",         77000),
    (19, "Root Prophet",        87000),
    (20, "Linux Ghost",         98000),
]
```

**XP Calculation:**
- Mission base XP: 30-225 (varies by type)
- Quiz bonus: +15 per question (if correct)
- Hint penalty: -20 XP (STANDARD hint used), -50 XP (FINAL hint used)
- Gear boost: Some gear items grant +15% XP on specific mission types

**Max Total XP:** ~51,540 (all 501 missions + quizzes completed)

---

## Gear Catalog

```python
GEAR_CATALOG = {
    # Starter gear (auto-given)
    "basic_terminal": {
        "name": "Basic Terminal",
        "desc": "Your first interface. Rusty, but functional.",
        "rarity": "common",
        "tier": 1,
        "boost": "starter",
    },
    
    # Chapter boss drops (uncommon tier 2)
    "hardware_scanner": {
        "name": "Hardware Scanner",
        "desc": "Reveals hidden hints on hardware & package tasks.",
        "rarity": "uncommon",
        "tier": 2,
        "boost": "hw_hints",
        "source": "Boss Drop: Ch01, 09, 12",
    },
    
    # Elite gear (rare tier 3)
    "ghost_mask": {
        "name": "Ghost Mask",
        "desc": "+20% XP on all quiz missions.",
        "rarity": "rare",
        "tier": 3,
        "boost": "quiz_xp",
        "source": "Boss Drop: Ch15",
    },
    
    # Legendary (one per playthrough)
    "linux_badge": {
        "name": "Linux Badge",
        "desc": "+5% on ALL XP gains. Prestige item.",
        "rarity": "legendary",
        "tier": 4,
        "boost": "all_xp",
        "source": "Boss Drop: Ch18",
    },
}
```

**Rarity Levels:** common < uncommon < rare < legendary

---

## Factions

5 factions with narrative presence and reputation:

```python
FACTIONS = [
    "Kernel Syndicate",      # Hardware, boot, kernel focus (Ch01-03, 13)
    "Root Collective",       # Filesystem, user, admin focus (Ch04-05, 10)
    "Net Runners",           # Networking, shell, regex focus (Ch06, 08-09)
    "Ghost Processors",      # Container, virtualization focus (Ch19)
    "Firewall Dominion",     # Security, firewall focus (Ch15, 20)
]
```

**Reputation Mechanics:**
- Each mission awards faction_reward: (faction_name, points)
- Reputation displays in player profile
- Max reputation: 100 per faction
- No mechanical gameplay impact (narrative/flavor only)

---

## Achievement System (engine/achievement_engine.py)

40+ achievements (19 base + 22 chapter completion + dynamic) with declarative unlock conditions:

```python
# engine/achievement_engine.py
class AchievementEngine:
    RULES = [
        AchievementRule('first_mission',       lambda m, p: len(p.completed_missions) == 1),
        AchievementRule('boss_defeated',       lambda m, p: m.mtype == "BOSS" and p.bosses_defeated >= 1),
        AchievementRule('five_bosses',       lambda m, p: p.bosses_defeated >= 5),
        AchievementRule('all_bosses',          lambda m, p: p.bosses_defeated >= 22),
        AchievementRule('chapter_1_complete',  lambda m, p: len([x for x in p.completed_missions if x.startswith("1.")]) >= 31),
        AchievementRule('quest_marathon',      lambda m, p: len(p.completed_missions) >= 100),
        AchievementRule('chapter_master',      lambda m, p: _chapters_fully_complete(p) >= 5),
        AchievementRule('level_ten',           lambda m, p: p.level >= 10),
        AchievementRule('gear_collector',      lambda m, p: len(p.inventory) >= 10),
        AchievementRule('all_factions',        lambda m, p: all(calculate_level(rep) >= 2 for rep in p.reputation.values())),
        AchievementRule('perfect_quiz',        lambda m, p: p.last_mission_all_quiz_correct),
        AchievementRule('perfect_streak',      lambda m, p: p.consecutive_correct_quiz >= 10),
        AchievementRule('no_hints',            lambda m, p: p.last_mission_hints_used == 0 and bool(m.expected_commands)),
        AchievementRule('faction_max',         lambda m, p: any(rep >= 100 for rep in p.reputation.values())),
        # ... plus 22 dynamically generated chapter_N_complete rules
    ]
```

**Unlock Triggers:**
- `first_mission`: After mission 1.01
- `chapter_*_complete`: After final mission of chapter
- `boss_defeated`: After any boss mission
- `all_bosses`: After mission 22.22
- `exam_mastered`: After all Ch22 blocks
- `perfect_quiz`: All quiz questions correct in one mission
- `speedrun`: Complete chapter in <1 hour
- `lore_collector`: Read all story sections in chapter
- `faction_max`: Reach 100 reputation in any faction

---

## Hint System

3-tier hint system:

```python
class HintLevel(Enum):
    FREE = 0              # No XP cost
    STANDARD = 1          # -20 XP cost
    FINAL = 2             # -50 XP cost (reveals answer)
```

**Hints list per mission:**
```python
hints = [
    "Free hint (general guidance)",
    "20 XP hint (more specific)",
    "50 XP final hint (reveals answer pattern)",
]
```

Player can request any hint level. XP cost is deducted immediately. Choosing higher tiers doesn't prevent lower tier hints.

---

## Terminal Simulator (engine/terminal_sim.py)

4457-line terminal emulator supporting ~40 Linux commands. Commands are registered in a `CommandRegistry` class for extensibility and testability.

**CommandRegistry API:**
```python
reg = CommandRegistry()
reg.register("lspci", output_string)
found, output = reg.get_output("lspci -v")  # exact, prefix, or base match
```

**Supported Commands (partial list):**

**Supported Commands (partial list):**
- **File ops:** `ls`, `cat`, `touch`, `mkdir`, `rm`, `cp`, `mv`, `find`, `locate`
- **Text:** `grep`, `sed`, `awk`, `cut`, `sort`, `uniq`, `tr`, `head`, `tail`, `wc`
- **User/Perms:** `whoami`, `id`, `chmod`, `chown`, `useradd`, `userdel`, `passwd`, `sudo`
- **Process:** `ps`, `kill`, `top`, `jobs`, `bg`, `fg`, `nice`, `renice`, `systemctl`
- **Network:** `ping`, `ifconfig`, `ip`, `ss`, `netstat`, `curl`, `wget`, `ssh`, `scp`
- **System:** `uname`, `lsblk`, `df`, `du`, `mount`, `umount`, `fdisk`, `parted`
- **Package:** `apt`, `yum`, `dpkg`, `rpm`, `pacman`, `zypper`
- **Misc:** `man`, `which`, `history`, `export`, `echo`, `pwd`, `cd`

**Validation Logic:**
- Matches player input against `expected_commands` list (substring matching, case-insensitive)
- Returns simulated output based on command and context
- Maintains fake filesystem state for multi-step missions

**Output Format:**
```
$ command --flag
output
additional lines
$
```

---

## Save System (engine/storage.py + engine/save_migrations.py)

**3 independent save slots:** `~/.neongrid9/save_slot1.json`, `.../save_slot2.json`, `.../save_slot3.json`

**Protocols:** `SaveRepository` with two implementations:
- `JsonFileRepository` — writes to `~/.neongrid9/`
- `InMemoryRepository` — RAM-only, for unit tests

**Save File Format (JSON, v2):**
```json
{
  "_version": 2,
  "name": "GhostRunner",
  "xp": 15000,
  "level": 8,
  "level_title": "Package Smuggler",
  "completed_missions": ["1.01", "1.02", "1.03", ...],
  "failed_missions": {},
  "inventory": ["basic_terminal", "hardware_scanner"],
  "reputation": {
    "Kernel Syndicate": 50,
    "Root Collective": 75
  },
  "achievements": ["first_mission", "chapter_1_complete"],
  "total_quizzes": 45,
  "correct_first_try": 38,
  "bosses_defeated": 3,
  "secrets_found": 0,
  "days_played": 1,
  "streak": 0,
  "chapter_quiz_stats": {"1": {"asked": 10, "correct": 8}},
  "chapter_completion_time": {"1": 1500.5},
  "boss_kill_times": {},
  "total_playtime": 3600,
  "speaker_stats": {"ZARA Z3R0": 12},
  "hints_used": 2,
  "missions_per_chapter": {"1": 31},
  "consecutive_correct_quiz": 5
}
```

**Migration:** v1 saves (no `_version` key) are automatically migrated to v2 by `save_migrations.migrate_v1_to_v2()`, which populates missing fields with sensible defaults.

**Auto-Save:** After every mission completion
**Load:** Restores player state exactly as saved
**New Game:** Creates player with name, starting XP=0, level=1, empty achievements

---

## Game Loop & UI Flow

### main.py Structure

```python
def main():
    # 1. Boot sequence (first run only)
    if first_run:
        show_boot_sequence()
    
    while True:
        choice = main_menu()  # "1) New Game", "2) Load", "3) Manage Saves", "4) About", "q) Quit"
        
        if choice == "1":
            new_game_menu()  # Create new player
            game_hub()        # Main gameplay loop
        elif choice == "2":
            load_game_menu()  # Load from slot
            game_hub()
        elif choice == "3":
            manage_saves_menu()
        elif choice == "4":
            about_screen()
        elif choice in ("q", "quit", "exit"):
            exit()

def game_hub():
    """Main gameplay loop."""
    while GAME.running:
        ch_id, missions, topic, title, subtitle = current_chapter()
        
        print(f"[{ch_id}] {title}")
        
        for mission in missions:
            if mission.mission_id in player.completed_missions and mission.mtype != "BOSS":
                # Offer replay
                if prompt_yesno("Replay mission?"):
                    runner.run(mission)
            else:
                runner.run(mission)
                check_achievements()
                GAME.auto_save(player)
        
        # Chapter complete
        player.current_chapter += 1
```

### Display System (engine/display.py)

**ANSI Color Class:**
```python
class C:
    RESET = "\033[0m"
    NEON = "\033[38;5;51m"      # Bright cyan
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    DANGER = "\033[91m"
    SUCCESS = "\033[92m"
```

**UI Functions:**
```python
def clear():                          # Clear screen
def typewrite(text, delay=0.02):      # Slow char-by-char output
def slow_print(text):                 # Slower print with pauses
def show_ascii_art(art):              # Display ASCII art
def show_story(story, speaker):       # Display narrative
def show_code(code):                  # Code block with syntax highlight
def show_transition(text):            # Story transition
def mission_header(id, title, xp, type):  # Mission start screen
def level_up_screen(level, name):     # Celebration screen
def xp_bar(current, max):             # XP progress bar
def prompt_continue():                # Press [Enter]
def prompt_input(prompt):             # Get player input
def prompt_yesno(question):           # Yes/No choice
def show_success(msg):                # Green success message
def show_error(msg):                  # Red error message
def show_warn(msg):                   # Yellow warning message
def show_exam_tip(tip):               # Blue exam tip
def show_memory_tip(tip):             # Memory aid display
def show_hint(hint):                  # Hint display
def box(text, width=80):              # Draw box around text
```

---

## Mission Execution (engine/mission_engine.py)

### MissionRunner.run(mission) Flow

```python
def run(self, mission: Mission) -> bool:
    # 1. Handle replay (if already completed)
    if mission_completed and mtype != "BOSS":
        return replay_mission()
    
    # 2. Boss special handling
    if mission.mtype == "BOSS":
        return run_boss()
    
    # 3. Display header + story
    clear()
    mission_header(mission.mission_id, mission.title, mission.xp, mission.mtype)
    
    # 4. ASCII art
    if mission.ascii_art:
        show_ascii_art(mission.ascii_art)
    
    # 5. Story + transition
    show_story(mission.story, mission.speaker)
    show_transition(mission.story_transitions[0])
    
    # 6. Explanation phase
    show_info(mission.explanation)
    show_transition(mission.story_transitions[1])
    
    # 7. Syntax/Example (if applicable)
    if mission.syntax:
        show_code(mission.syntax)
    if mission.example:
        show_code(mission.example)
    show_transition(mission.story_transitions[2])
    
    # 8. Terminal task (non-QUIZ only)
    if mission.mtype in ["SCAN", "INFILTRATE", "CONSTRUCT", "REPAIR"]:
        show_info(mission.task_description)
        success = run_terminal(mission.expected_commands)
        if not success:
            return False
    
    show_transition(mission.story_transitions[3])
    
    # 9. Quiz
    correct = 0
    for q in mission.quiz_questions:
        if run_quiz_question(q):
            correct += 1
            xp_gained += q.xp_value
    
    # 10. Show results
    show_exam_tip(mission.exam_tip)
    show_memory_tip(mission.memory_tip)
    show_xp_gain(xp_gained)
    
    # 11. Apply rewards
    player.xp += xp_gained
    player.completed_missions.add(mission.mission_id)
    
    if mission.gear_reward:
        player.inventory.append(mission.gear_reward)
        show_success(f"Gear unlocked: {GEAR_CATALOG[mission.gear_reward]['name']}")
    
    if mission.faction_reward:
        faction, amount = mission.faction_reward
        player.factions[faction] = player.factions.get(faction, 0) + amount
    
    # 12. Check level up
    old_level = player.level
    player.level = calculate_level(player.xp, LEVELS)
    if player.level > old_level:
        level_up_screen(player.level, LEVELS[player.level-1][1])
    
    # 13. Check achievements
    check_achievement_triggers(mission)
    
    return True
```

### Terminal Task (run_terminal)

```python
def run_terminal(expected_commands: List[str]) -> bool:
    """REPL for player command execution."""
    from engine.terminal_sim import run_terminal
    
    correct_count = 0
    attempts = 0
    max_attempts = 5
    
    while correct_count < len(expected_commands) and attempts < max_attempts:
        cmd = prompt_input("$ ")
        
        # Check against expected commands (substring match)
        matched = any(exp.lower() in cmd.lower() for exp in expected_commands)
        
        if matched:
            # Simulate output
            output = terminal_sim.execute(cmd)
            print(output)
            correct_count += 1
        else:
            # Offer hint or retry
            show_error("Command not recognized. Try again or request a hint.")
            attempts += 1
    
    if correct_count < len(expected_commands):
        show_error("Mission failed. You can replay it.")
        return False
    
    show_success("Task completed!")
    return True
```

---

## Creating a Complete New Project

### 1. Project Initialization

```bash
mkdir neongrid9
cd neongrid9
git init
python3 -m venv venv
source venv/bin/activate
```

### 2. Create Directory Structure

```bash
mkdir engine missions
touch engine/__init__.py missions/__init__.py
```

### 3. Create Core Modules

#### engine/display.py (324 lines)
- ANSI color class `C` with 12+ colors
- UI functions: `clear()`, `typewrite()`, `mission_header()`, etc.
- All printing logic centralized here

#### engine/mission_engine.py (514 lines)
- `Mission` dataclass (20+ fields)
- `QuizQuestion` dataclass (5 fields)
- `MissionRunner` class with `run()` method
- Mission type dispatch logic
- Achievement/XP trigger logic

#### engine/player.py (392 lines)
- `Player` dataclass (8 fields)
- `LEVELS` list (15 tuples: level, title, xp_threshold)
- `GEAR_CATALOG` dict (20+ gear items)
- `AchievementTracker` class
- XP/level calculation functions

#### engine/features.py (276 lines)
- `HintRequest` dataclass + `HintLevel` enum
- `Achievement` dataclass
- `ACHIEVEMENTS` dict (19 achievements)
- `FactionStatus` tracking
- Hint/achievement/faction display functions

#### engine/terminal_sim.py (4457 lines)
- `TerminalSimulator` class
- Command dispatch table (40+ commands)
- Fake filesystem state
- Output simulation for each command
- Validation logic

#### engine/save_system.py (72 lines)
- `save_game(player, slot)` → JSON
- `load_game(slot)` → Player
- `slot_info(slot)` → metadata
- `delete_save(slot)` → delete JSON

### 4. Create Mission Files

#### missions/ch01_hardware.py (800+ lines)
```python
from engine.mission_engine import Mission, QuizQuestion

CHAPTER_1_MISSIONS = [
    Mission(
        mission_id='1.01',
        title='Erste Signale — Was ist Hardware?',
        mtype='SCAN',
        xp=30,
        chapter=1,
        speaker='ZARA Z3R0',
        story='...',
        why_important='...',
        explanation='...',
        ascii_art='''...''',
        story_transitions=[...],
        quiz_questions=[
            QuizQuestion(
                question='...',
                options=['A) ...', 'B) ...', 'C) ...', 'D) ...'],
                correct='A',
                explanation='...',
                xp_value=15,
            ),
        ],
        exam_tip='...',
        memory_tip='...',
        expected_commands=['...'],
        task_description='...',
        hints=['free', '20xp', '50xp'],
    ),
    # 30 more missions...
]
```

Repeat for ch02–ch22 (22 files total).

### 5. Create main.py (1374 lines)

```python
#!/usr/bin/env python3
"""NeonGrid-9 :: Linux COMBAT TRAINING SYSTEM"""

import sys, os, time, random
from engine.display import C, clear, ...
from engine.player import Player, LEVELS, GEAR_CATALOG
from engine.save_system import save_game, load_game, slot_info, delete_save
from engine.mission_engine import MissionRunner
from missions.ch01_hardware import CHAPTER_1_MISSIONS
from missions.ch02_boot import CHAPTER_2_MISSIONS
# ... import all 22 chapters

CHAPTERS = [
    (1, CHAPTER_1_MISSIONS, "101.1", "BOOT CAMP", "Hardware & BIOS/UEFI"),
    (2, CHAPTER_2_MISSIONS, "101.2", "DARK BOOT", "Boot-Manager & GRUB2"),
    # ... all 22 chapters
]

class GameState:
    def __init__(self):
        self.player = None
        self.save_slot = 1
        self.current_chapter = 1
        self.running = True
    
    def save(self):
        if self.player:
            save_game(self.player, self.save_slot)
    
    def auto_save(self, player):
        save_game(player, self.save_slot)

GAME = GameState()

def main():
    first_run = not any(os.path.exists(os.path.expanduser(f"~/.neongrid9/save_slot{i}.json")) for i in [1,2,3])
    if first_run:
        show_boot_sequence()
    
    while True:
        choice = main_menu()
        if choice == "1":
            new_game_menu()
            GAME.running = True
            game_hub()
        elif choice == "2":
            load_game_menu()
            GAME.running = True
            game_hub()
        # ...

def game_hub():
    """Main gameplay loop."""
    # ... chapter selection, mission execution, etc.

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(C.YELLOW + "\n  Interrupted.\n" + C.RESET)
        if GAME.player:
            GAME.save()
        sys.exit(0)
```

### 6. Create Documentation Files

- **README.md** — Project overview, stats, chapter table, gameplay guide links
- **GAMEPLAY_GUIDE.md** — Mission types, progression, achievements (player-facing)
- **LINUX_TOPICS.md** — LPIC domain mapping (player-facing)
- **TIPS_TRICKS.md** — Speedrun strategies, optimization (player-facing)

### 7. Create Git Infrastructure

**.gitignore:**
```
__pycache__/
*.pyc
.pytest_cache/
venv/
.venv/
~/.neongrid9_save_*.json
.DS_Store
```

**LICENSE:** MIT

**.git/config:**
```
[user]
    name = Steinmair
    email = steinmair23@gmail.com
```

---

## Development Guidelines

### Code Style
- **Python 3.10+** only
- **Dataclasses** for all data (no class-based methods for missions)
- **Type hints** on all function signatures
- **No external dependencies** (pure stdlib only)
- **Imports organized:** stdlib, then engine, then missions

### Naming Conventions
- **Mission IDs:** `"X.YY"` (chapter.mission; e.g., `"1.01"`, `"22.22"`)
- **Speaker names:** ZARA Z3R0 (not ZARA_Z3R0), RUST, PHANTOM, CIPHER, LYRA-7, EXAMINATOR, SYSTEM
- **Gear IDs:** snake_case (e.g., `"hardware_scanner"`, `"linux_badge"`)
- **Achievement IDs:** snake_case (e.g., `"first_mission"`, `"all_bosses"`)
- **Faction names:** Capitalized (e.g., `"Kernel Syndicate"`)

### XP Scaling
- **Intro missions (.01):** 30-35 XP
- **Regular missions (.02–.21):** 40-70 XP (higher difficulty = higher XP)
- **Boss missions (.22):** 220-240 XP (scales by chapter: Ch01 ~225, Ch22 ~240)
- **Quiz rewards:** +15 XP per correct answer (applies per question)
- **Total max XP:** ~51,540 (501 missions fully completed + all quizzes)

### Quiz Best Practices
- **Always 4 options:** A, B, C, D
- **Correct field:** String `"A"`, `"B"`, `"C"`, `"D"` (NOT index)
- **Option format:** `"A) Clear description"` (includes letter + parenthesis)
- **Expert questions for bosses:** LPIC-1 certification-level difficulty
- **1–5 questions per mission:** Regular 1-3, Quiz type 3-5, Boss exactly 5

### Speaker Distribution
- **No speaker >60% per chapter** (enforce via audit)
- **5 factions → 5 speaker perspectives** for narrative variety
- **Chapter 18 exception:** EXAMINATOR dominates (exam chapter, intentional)

### Hint Guidelines
- **Free hint:** General guidance, no spoilers
- **20 XP hint:** More specific, narrows approach
- **50 XP final hint:** Reveals command/answer pattern
- **All 3 tiers:** Provide for non-QUIZ missions; may skip for QUIZ

### Story Transitions
- **Always 4 lines:** Between story, explanation, example, quiz sections
- **2–10 words each:** Narrative immersion without info overload
- **Faction flavor:** Match speaker's voice and narrative arc

### Achievement Triggers
- **Unlock in code:** Check condition after mission completion
- **Award XP:** Add to player.xp immediately
- **Display celebration:** Show achievement screen with icon + name
- **Track in player.achievements:** Mark True in dict

---

## Testing & Validation

### Manual Testing Checklist
- [ ] Start new game from scratch
- [ ] Complete Ch01 fully (all 31 missions)
- [ ] Verify XP calculations and level progression
- [ ] Test hint system (all 3 tiers for 1 mission)
- [ ] Verify save/load cycle preserves state exactly
- [ ] Complete Ch22 (Grand Finale); verify all achievements trigger
- [ ] Check no console warnings/errors
- [ ] Verify ASCII art renders cleanly in terminal
- [ ] Check all speaker names consistent (ZARA Z3R0, not ZARA_Z3R0)
- [ ] Verify no single speaker >60% in any chapter (except Ch18)
- [ ] Spot-check 5 random quiz questions for accuracy

### Audit Completeness Check
```python
def audit_missions():
    from missions.ch01_hardware import CHAPTER_1_MISSIONS
    # ... import all chapters
    
    for chapter_missions in [CHAPTER_1_MISSIONS, ...]:
        for m in chapter_missions:
            assert m.mission_id, "Missing mission_id"
            assert m.title, "Missing title"
            assert m.mtype in ["SCAN", "INFILTRATE", "DECODE", "CONSTRUCT", "REPAIR", "QUIZ", "BOSS"], f"Invalid mtype: {m.mtype}"
            assert m.xp > 0, "Missing XP"
            assert m.chapter > 0, "Missing chapter"
            assert m.why_important, "Missing why_important"
            assert m.exam_tip, "Missing exam_tip"
            assert m.memory_tip, "Missing memory_tip"
            assert m.quiz_questions, "Missing quiz_questions"
            assert len(m.quiz_questions) >= 1, "Not enough quiz questions"
            
            for q in m.quiz_questions:
                assert len(q.options) == 4, "Quiz must have 4 options"
                assert q.correct in ["A", "B", "C", "D"], "Correct must be letter"
    
    print("✓ All 501 missions complete")
```

---

## Production Status

**Version 1.0 — Production Ready** ✅

- ✅ All 501 missions implemented with full metadata
- ✅ 22 chapters with cohesive narrative
- ✅ 1117 quiz questions with explanations
- ✅ XP scaling balanced (no grinding)
- ✅ 19 achievements functional
- ✅ 5 factions with narrative presence
- ✅ Terminal simulator with 40+ commands
- ✅ Save/load system with 3 slots
- ✅ Zero warnings/errors

**No external dependencies** — Pure Python 3.10+ stdlib only.

**Known Limitations:**
- Terminal simulator is permissive (substring matching, not exact command validation)
- Achievements are narrative-only (no mechanical impact on gameplay)
- Hints are free to access (no permanent consequence)

---

## Future Enhancements (Not Required)

- Chapter 23+ (LPIC-2 content)
- Tiered hint UI with visual affordances
- Achievement leaderboard (speedrun, perfect quiz streaks)
- Terminal hint system (command suggestions)
- Faction-locked content (missions gated by reputation)
- Procedurally generated quiz mode
- Network multiplayer (compare progress, faction wars)

---

## Quick Reference: Adding a Mission

1. **Create Mission instance** with all required fields
2. **Add to CHAPTER_N_MISSIONS** list (replace placeholder if exists)
3. **Verify:** 4 options, correct as "A"/"B"/"C"/"D", 5 fields populated
4. **Test:** Run game, navigate to chapter, complete mission
5. **Verify XP/achievements/gear:** Check all apply correctly

```python
Mission(
    mission_id='X.YY',
    title='Title',
    mtype='SCAN|INFILTRATE|DECODE|CONSTRUCT|REPAIR|QUIZ|BOSS',
    xp=35,
    chapter=X,
    speaker='SPEAKER_NAME',
    story='Narrative intro',
    why_important='LPIC domain relevance',
    explanation='Technical explanation',
    syntax='command syntax' if applicable,
    example='example output' if applicable,
    task_description='What player must do',
    expected_commands=['cmd1', 'cmd2'],
    hints=['free', '20xp', '50xp'],
    ascii_art='ASCII ART HERE',
    story_transitions=['transition1', 'transition2', 'transition3', 'transition4'],
    quiz_questions=[
        QuizQuestion(
            question='Q?',
            options=['A) opt', 'B) opt', 'C) opt', 'D) opt'],
            correct='A',
            explanation='Why A',
            xp_value=15,
        ),
    ],
    exam_tip='LPIC note',
    memory_tip='Mnemonic',
    # Optional:
    gear_reward='gear_id' if boss,
    faction_reward=('Faction Name', 50) if applicable,
    boss_name='Boss Name' if mtype='BOSS',
    boss_desc='Boss narrative' if mtype='BOSS',
)
```

---

## File Size Reference

| File | Lines | Purpose |
|------|-------|---------|
| main.py | ~1400 | Game loop, UI menus, chapter management, review mode |
| terminal_sim.py | ~4500 | Terminal emulator + CommandRegistry |
| mission_engine.py | ~520 | Mission dataclass + MissionRunner (phase extraction) |
| display.py | ~340 | ANSI UI + printing functions + fast mode |
| player.py | ~450 | Player dataclass + leveling (1-20) + gear + save round-trip |
| features.py | ~280 | Hints, achievements (19 base), factions |
| achievement_engine.py | ~160 | Declarative AchievementRule engine |
| storage.py | ~120 | SaveRepository Protocol + JsonFileRepository + InMemoryRepository |
| save_migrations.py | ~30 | v1 → v2 save migration |
| renderer.py | ~80 | Renderer Protocol + TerminalRenderer + NullRenderer |
| menu_builder.py | ~80 | MenuBuilder fluent API |
| chapter_registry.py | ~80 | ChapterRegistry with recap metadata |
| **Per chapter** | ~800 | ~22 missions per file |
| **Total Code** | ~8,900 | Full game engine + 22 chapters |
| **Tests** | ~600 | 68+ unit tests across 6 test modules |
| **Docs** | ~50 KB | README, GAMEPLAY_GUIDE, CLAUDE.md, etc. |
