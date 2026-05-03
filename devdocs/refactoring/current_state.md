# Current State of NeonGrid-9 Architecture

This document captures the architecture **as it exists today**, before any
refactoring begins. It serves as an anchor: if a refactoring changes something
described here, that change must be deliberate and documented.

---

## 1. How It Works Now

### 1.1 Overall Flow

```
main.py                     engine/                     missions/
─────────                   ───────                     ─────────
main()                      display.py                  ch01_hardware.py
├── show_boot_sequence()    ├── C (ANSI colors)         ├── CHAPTER_1_MISSIONS
├── main_menu()             ├── clear()                 │   ├── Mission(...)
├── new_game_menu()         ├── mission_header()        │   └── Mission(...)
├── load_game_menu()        ├── xp_bar()                ch02_boot.py
├── game_hub()              ├── prompt_input()          ...
│   ├── chapter_menu()      └── ...
│   ├── show_player_status()  player.py
│   ├── show_inventory()      ├── Player dataclass
│   ├── show_linux_readiness()├── LEVELS, GEAR_CATALOG
│   ├── review_mode()         ├── FACTIONS, RARITY_COLOR
│   └── timed_exam_mode()     └── AchievementTracker
└── about_screen()
                            mission_engine.py
                            ├── Mission dataclass
                            ├── QuizQuestion dataclass
                            └── MissionRunner.run()
                                ├── _run_quiz()
                                ├── _run_boss()
                                └── _replay_mission()

                            save_system.py
                            ├── save_game()
                            ├── load_game()
                            └── delete_save()

                            features.py
                            ├── HintLevel / HintRequest
                            ├── Achievement / AchievementTracker
                            ├── ACHIEVEMENTS catalog
                            ├── FactionStatus
                            └── calculate_level()

                            terminal_sim.py
                            └── run_terminal()  (+ 40+ simulated Linux commands)
```

### 1.2 Module Responsibilities

| Module | Responsibility | Lines |
|--------|---------------|-------|
| `main.py` | Entry point, game loop, all menus, save slot management, exam/review modes, progress display | ~1374 |
| `engine/display.py` | All ANSI color definitions (`C` class) and UI rendering functions (`clear`, `header`, `mission_header`, `xp_bar`, etc.) | ~325 |
| `engine/mission_engine.py` | `Mission` and `QuizQuestion` dataclasses; `MissionRunner` that orchestrates story → explanation → terminal → quiz → rewards | ~515 |
| `engine/player.py` | `Player` dataclass with XP/leveling, gear catalog, reputation, quiz stats, save serialization (`to_dict`/`from_dict`) | ~393 |
| `engine/features.py` | Hint system, achievement definitions (`ACHIEVEMENTS` dict), `AchievementTracker`, faction visualization, `calculate_level()` | ~277 |
| `engine/terminal_sim.py` | `run_terminal()` REPL with simulated Linux command outputs | ~4457 |
| `engine/save_system.py` | JSON save/load to `~/.neongrid9/save_slot{N}.json` | ~73 |
| `missions/ch*.py` (×22) | Each exports `CHAPTER_N_MISSIONS`: a list of `Mission` instances with all content filled in | ~800 avg |

### 1.3 Game Loop Detail

`main.py::main()` runs an infinite `while True` loop that shows the main menu
and dispatches to sub-menus. When a player is loaded or created,
`game_hub()` takes over and runs its own infinite loop until the player quits.

Inside `game_hub()`:
1. Display player status (XP bar, name, level title, faction reputation)
2. Display chapter progress bars (22 chapters, completion count)
3. Read a choice string
4. If choice is `"1"` through `"22"`, call `chapter_menu(n)`
5. If choice is action letters (`s`, `i`, `r`, `x`, `e`, `v`, `q`),
   call the corresponding function

`chapter_menu()`:
1. Show all missions in the chapter with completion status
2. Accept mission ID, numeric index, `all`, or `q`
3. If a mission is selected, instantiate `MissionRunner` and call `run()`
4. Auto-save after every mission
5. If all missions are complete, show `_show_chapter_complete()`

### 1.4 Mission Execution Detail

`MissionRunner.run(mission)` is a 257-line sequential function:

1. **Replay guard** — if mission already completed and not BOSS, jump to replay
2. **BOSS guard** — if BOSS, jump to `_run_boss()`
3. **Header** — `clear()` + `mission_header()`
4. **ASCII art** — if present
5. **Story** — `show_story()` + `prompt_continue()`
6. **Why important** — `show_info()` + transition
7. **Explanation** — `show_info()` + transition
8. **Syntax / Example** — `show_code()` + transitions
9. **Terminal task** — if `expected_commands` and `task_description` exist,
   run a command-input loop with auto-hints on failure.
   If still not solved, fall back to `run_terminal()`.
10. **Quiz** — `_run_quiz()` (iterates questions, awards XP)
11. **Exam tip / Memory tip** — display
12. **XP calculation** — base XP with first-attempt bonus (1.2×) or failure
    penalty (÷3). Add gear/faction rewards.
13. **Achievements** — inline `if` checks for 10+ achievement conditions
14. **Level up** — if XP crossed threshold, show `level_up_screen()`
15. **Save** — call `save_callback` if set

### 1.5 Data Persistence

`save_system.py` writes `player.to_dict()` as JSON to `~/.neongrid9/`.
`Player.from_dict()` reconstructs the object field-by-field with explicit
defaults for missing keys (migration-friendly).

There are **3 save slots**. Slot selection happens in `new_game_menu()`.
Auto-save triggers after every mission completion in `chapter_menu()` and
`game_hub()`.

### 1.6 Terminal Simulator

`terminal_sim.py` is the largest file (~4457 lines). It contains:
- `run_terminal()` — the REPL loop that reads player commands
- `SIMULATED_OUTPUTS` — a massive dict mapping Linux commands to fake outputs
- Substring matching against `expected_commands` to determine success

The simulator is **permissive**: it matches command bases (`ls` matches `ls -la`).

---

## 2. Why It Works This Way

### 2.1 Design Philosophy: Pure Standard Library

The entire project intentionally has **zero external dependencies**.
This means:
- No `pytest` → tests use built-in `unittest`
- No `rich` or `curses` → ANSI escape codes handled manually
- No `pydantic` or `attrs` → `dataclasses` from stdlib
- No `click` or `argparse` → simple `input()` loops

**Consequence:** The UI layer is tightly coupled to the engine because there
is no rendering framework abstraction. Every `print()` and `input()` is
hard-coded in the flow functions.

### 2.2 Content-First, Engine-Second

The project was built by generating 22 chapter files first, then writing the
engine to run them. The `Mission` dataclass accumulated fields organically as
new content types were needed (bosses, gear rewards, faction rewards,
story transitions, memory tips).

**Consequence:** `Mission` has 20+ fields. The chapter files are verbose but
self-contained. Refactoring `Mission` into sub-structures would require touching
all 22 chapter files.

### 2.3 Single-File Entry Point for Players

`main.py` is designed to be the only file a player runs:
```bash
python3 main.py
```
Everything imports from here. The `CHAPTERS` tuple is constructed by importing
all 22 chapter modules inside `main.py`.

**Consequence:** `main.py` is a 1374-line monolith that imports everything,
knows everything, and does everything. It is simultaneously the UI controller,
the game loop, the menu renderer, and the save manager.

### 2.4 Inline Achievement Checks

Achievements are checked with sequential `if` blocks inside `MissionRunner.run()`
rather than a rule engine. This was chosen because:
- It is explicit and easy to debug
- It requires no additional abstraction
- Achievement conditions are simple counts and thresholds

**Consequence:** Adding a new achievement requires editing `mission_engine.py`
and inserting a new `if` block in the right place.

### 2.5 Late Imports as Circular-Dependency Patches

`mission_engine.py` contains three late imports:
```python
from engine.features import calculate_level  # line 297
from engine.player import GEAR_CATALOG       # lines 321, 488
```

These exist because `engine/player.py` imports `AchievementTracker` from
`engine/features.py`, and `mission_engine.py` imports `Player` from `player.py`.
Moving `calculate_level` or `GEAR_CATALOG` to a shared module would resolve this,
but the late imports work.

**Consequence:** Static analysis tools flag these. They also make the code
harder to follow because imports are scattered.

### 2.6 ANSI Color Class (`C`) as Global State

The `C` color class in `display.py` is imported by almost every module.
Color constants are concatenated directly into strings:
```python
print(C.SUCCESS + f"  ✓  {text}" + C.SUCCESS + "  ✓" + C.RESET)
```

This was chosen because it is simple, requires no library, and allows dynamic
string construction.

**Consequence:** 36 color references inside `mission_engine.py` mean the engine
module is tightly coupled to the display module. The `Renderer` protocol
(already drafted in `engine/renderer.py`) was designed to solve this but is
not yet adopted.

---

## 3. Known Limitations

### 3.1 Testability

- `MissionRunner.run()` calls `input()` directly → **cannot be unit tested**
  without monkey-patching `builtins.input`.
- `game_hub()`, `chapter_menu()`, `timed_exam_mode()` all call `input()` → same
  problem.
- Result: Only data-layer tests (`Player`, `Mission`, `QuizQuestion`) are easy.
  Integration tests require importing from `main.py`, creating a test → UI
  dependency.

### 3.2 Scalability of the Menu System

- The 22-way `elif` chain in `game_hub()` is **O(n)** on chapter count.
  Adding chapter 23 requires adding another `elif` branch.
- The chapter progress display renders all 22 chapters every loop iteration.
  This is fine for 22 chapters but would degrade if the count grew significantly.

### 3.3 Save Format Rigidity

- `Player.to_dict()` and `Player.from_dict()` list every field explicitly.
  Adding a new field requires editing both methods.
- There is no schema version in the JSON. `from_dict` uses `.get(key, default)`
  which works as an implicit migration, but there's no formal versioning.

### 3.4 Terminal Simulator Coupling

- `run_terminal()` lives in `terminal_sim.py` but is called from
  `mission_engine.py` and `main.py`.
- The simulated command outputs are inline strings in a dict, not loaded from
  data files. Editing the simulator requires editing a 4457-line file.

### 3.5 Error Handling

- `save_system.py` catches `Exception` and prints a message → **silent failure**
- `main.py` top-level catches `KeyboardInterrupt` and `Exception` → user sees
  a generic error message with traceback
- There is no structured logging or error reporting

### 3.6 Data and Presentation Mixed

- `_show_chapter_complete()` in `main.py` contains a 22-entry inline
  `recap_map` dictionary. The presentation logic owns the data.
- `MissionRunner.run()` decides *what to show next* AND *which color to use*.
  These should be separate concerns.

### 3.7 No Centralized Constants

- Magic numbers for achievements (22 bosses, 100 missions, 5 chapter mastery)
  are hard-coded in `mission_engine.py`.
- XP scaling thresholds (1.1, 1.2, 1.3) are hard-coded in `player.py`.
- Exam timing (5400s, 800/500 scoring) is hard-coded in `main.py`.

---

## 4. Invariants That Must Be Preserved During Refactoring

These are contractual guarantees that any refactoring must maintain:

### 4.1 Player State Invariants
- `Player.xp` is always ≥ 0
- `Player.level` is always between 1 and `max(LEVELS)`
- `Player.completed_missions` is a `set` of strings
- `Player.inventory` always starts with `["basic_terminal", "cracked_manpage"]`
- `Player.reputation` always has all 5 factions as keys

### 4.2 Mission Invariants
- Every `Mission` has `mission_id` in format `{chapter}.{index}` (e.g. `"1.01"`)
- `mtype` is one of: `SCAN`, `INFILTRATE`, `DECODE`, `CONSTRUCT`, `REPAIR`, `QUIZ`, `BOSS`
- `quiz_questions` always has ≥ 1 question
- Every `QuizQuestion` has exactly 4 `options`
- `correct` is either `"A"`, `"B"`, `"C"`, `"D"` or an `int` 0-3

### 4.3 Save File Invariants
- Save files live in `~/.neongrid9/save_slot{N}.json`
- JSON is UTF-8, indented, with `ensure_ascii=False`
- `load_game` returns `None` on any error (missing file, corrupt JSON)
- `save_game` returns `False` on any error (bad slot, IO error)

### 4.4 Achievement Invariants
- `AchievementTracker.unlock()` is idempotent
- Invalid achievement IDs return `None`
- Unlocking an achievement does NOT award XP to the player automatically
  (the caller must call `player.add_xp(ach.xp_reward)`)

### 4.5 Gear Invariants
- `GEAR_CATALOG` keys are `snake_case` strings
- `gear_bonus()` returns `1.0` for unknown boost types
- `linux_badge` adds +5% additively when another bonus is active, or 1.05 alone

---

## 5. Refactoring Risk Map

| Area | Risk | Mitigation |
|------|------|------------|
| `MissionRunner.run()` phase extraction | **High** — 257 lines of sequential logic with implicit state | Keep tests green; extract one phase at a time |
| `main.py` menu dispatch flattening | Medium — changes control flow but not data | Run smoke tests after each `elif` removal |
| `Player.to_dict()`/`from_dict()` → `asdict()` | Medium — may lose default-field semantics | Compare dict output byte-for-byte |
| `C` color references → `Renderer` protocol | **High** — touches every print line | Introduce protocol gradually; keep old functions as wrappers |
| `recap_map` extraction to data file | Low — pure data move | Verify all 22 chapters still show correct recap |
| Late import removal | Low — may expose circular cycles | Import order tests; CI check |
| Achievement `if` wall → rule engine | Medium — changes unlock timing | Unit-test each rule independently before replacing inline checks |
