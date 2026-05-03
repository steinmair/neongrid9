# Module Discovery — NeonGrid-9

*Natural boundaries, coupling, cohesion, and dependency relationships derived from the code itself. This is not the folder structure — it is how the code actually clusters.*

---

## 1. Natural Module Boundaries

### Boundary A: Content (Data) Modules

**Files:** `missions/ch01_hardware.py` through `missions/ch22_final_exam.py`

**What they contain:** Pure data — `Mission(...)` and `QuizQuestion(...)` constructor calls. No logic, no functions, no classes beyond imports.

**Boundary strength:** Very strong. These files are independent of each other. `ch01_hardware.py` never imports `ch02_boot.py`. They only share the `Mission` and `QuizQuestion` dataclass definitions from `engine.mission_engine`.

**Why the boundary exists:** The "data as code" philosophy. Each chapter is a self-contained content unit.

**Cohesion:** Perfect — each file does exactly one thing: define missions for one chapter.

---

### Boundary B: Mission Engine

**File:** `engine/mission_engine.py`

**What it contains:**
- `Mission` dataclass (~20 fields)
- `QuizQuestion` dataclass (5 fields)
- `MissionRunner` class with `run()`, `_run_quiz()`, `_run_boss()`, `_replay_mission()`

**Boundary strength:** Moderate. `MissionRunner` is tightly coupled to display functions (it calls ~15 different functions from `engine.display`). It also imports `GEAR_CATALOG` lazily to avoid circular imports.

**Cohesion issue:** `MissionRunner` mixes three responsibilities:
1. Orchestrating the mission flow (story → terminal → quiz → rewards)
2. Mutating player state (XP, achievements, gear, reputation)
3. Rendering the mission screen (calling display functions)

**Why the boundary exists:** It is the central abstraction that turns data into gameplay.

---

### Boundary C: Display Renderer

**File:** `engine/display.py`

**What it contains:**
- `class C` (ANSI color constants)
- 20+ rendering functions: `typewrite()`, `show_story()`, `show_code()`, `mission_header()`, etc.
- Input functions: `prompt_input()`, `prompt_continue()`

**Boundary strength:** Strong externally, weak internally. Every other module depends on `display.py`, but `display.py` depends on nothing except stdlib (`os`, `sys`, `time`).

**Cohesion issue:** The module mixes rendering (colors, boxes, ASCII art) with input handling (`prompt_input()`). Input and output are different concerns.

**Why the boundary exists:** Centralized ANSI rendering was extracted to avoid duplicating escape sequences across the codebase.

---

### Boundary D: Player State

**File:** `engine/player.py`

**What it contains:**
- `Player` dataclass (~20 fields)
- `LEVELS` list (15 tuples)
- `GEAR_CATALOG` dict (13 items)
- `AchievementTracker` class
- XP/level calculation functions

**Boundary strength:** Moderate. `Player` is the primary data container, but `GEAR_CATALOG` and `AchievementTracker` are meta-game systems that could live in `features.py`.

**Cohesion issue:** `player.py` mixes three domains:
1. Player entity (what the player IS — name, XP, completed missions)
2. Game meta-data (gear items, level thresholds)
3. Achievement tracking (which achievements are unlocked)

**Why the boundary exists:** All player-related data was grouped into one file for convenience.

---

### Boundary E: Terminal Simulator

**File:** `engine/terminal_sim.py`

**What it contains:**
- `SIMULATED_OUTPUTS` dict (~4,000 lines of command → output mappings)
- `run_terminal()` function (REPL loop)
- `get_output()` and `normalize_cmd()` helpers

**Boundary strength:** Moderate. It depends on `engine.display` for prompts and output formatting. It is called by `mission_engine.py`.

**Cohesion issue:** The dict of simulated outputs is data, but it lives in the same file as the REPL logic. The data is not separated from the engine.

**Why the boundary exists:** The terminal is a self-contained subsystem. It simulates Linux commands without touching the real OS.

---

### Boundary F: Features / Meta-Game

**File:** `engine/features.py`

**What it contains:**
- `HintLevel` enum
- `HintRequest` dataclass
- `Achievement` dataclass
- `ACHIEVEMENTS` dict (19 achievements)
- `FactionStatus` class (dead code)
- `calculate_level()` function (dual behavior)

**Boundary strength:** Weak. `features.py` is a grab-bag of unrelated meta-game systems. It is imported by `mission_engine.py`, `player.py`, and `main.py`.

**Cohesion issue:** Hints, achievements, factions, and level calculation have nothing in common except that they are "not the core engine."

**Why the boundary exists:** The developer needed a place to put "extra stuff" that was not engine, player, or display.

---

### Boundary G: Save System

**File:** `engine/save_system.py`

**What it contains:**
- `save_game()`, `load_game()`, `slot_info()`, `delete_save()`
- `SAVE_FILES` dict mapping slot numbers to `Path` objects
- `ensure_save_dir()` helper

**Boundary strength:** Strong. It only depends on `engine.player.Player` (for `to_dict()` / `from_dict()`). It does not import display, features, or mission engine.

**Cohesion:** Good — all file I/O for persistence is in one place.

**Why the boundary exists:** Persistence is a cross-cutting concern that needs isolation.

---

### Boundary H: Main Control Loop

**File:** `main.py`

**What it contains:**
- `GameState` class
- Main menu, new game, load game, save management
- `game_hub()`, `chapter_menu()`
- `show_player_status()`, `show_linux_readiness()`, `review_mode()`, `timed_exam_mode()`
- 22 explicit chapter imports
- `CHAPTERS` tuple list

**Boundary strength:** Very weak. `main.py` is the central knot that imports everything. It knows about every module, every chapter, and every special mode.

**Cohesion issue:** `main.py` is a "god module." It contains menus, loops, special modes, progress tracking, chapter imports, and the global `GAME` singleton.

**Why the boundary exists:** In a small CLI application, `main.py` traditionally serves as the entry point and conductor.

---

## 2. Coupling Analysis

### Coupling Matrix

| Module | Depends On | Depended On By | Coupling Strength |
|--------|-----------|----------------|-------------------|
| `main.py` | ALL engine modules + ALL 22 chapter modules | OS (`python3 main.py`) | Very High |
| `mission_engine.py` | `display`, `terminal_sim`, `player` (lazy), `features` | `main.py` | High |
| `display.py` | stdlib only (`os`, `sys`, `time`) | `main.py`, `mission_engine`, `terminal_sim` | Low (outgoing), High (incoming) |
| `player.py` | `features` (for `calculate_level`) | `main.py`, `mission_engine`, `save_system`, `features` (circular) | Moderate |
| `terminal_sim.py` | `display` | `mission_engine` | Moderate |
| `features.py` | `player` (for `calculate_level`) | `main.py`, `mission_engine`, `player` (circular) | Moderate |
| `save_system.py` | `player` | `main.py` | Low |
| `missions/ch*.py` | `mission_engine` | `main.py` only | Very Low |

---

### Circular Dependencies

#### Cycle 1: `player.py` ↔ `features.py`

```
player.py imports features.calculate_level
features.py imports player.AchievementTracker (or player references)
```

**How it is resolved:** `mission_engine.py` uses lazy imports for `GEAR_CATALOG` inside methods rather than at module top level. This breaks the import cycle at runtime but is a hack.

**Impact:** Adding a new import to either file risks breaking the cycle. The lazy import pattern is not documented and could be accidentally removed.

---

#### Cycle 2: `mission_engine.py` ↔ `player.py` (via `features.py`)

```
mission_engine.py imports Player
player.py imports features.calculate_level
features.py references player-level concepts
```

**How it is resolved:** The cycle is indirect and does not cause import errors because Python's import system handles it. But the conceptual cycle exists: the engine knows about the player, the player knows about the feature system, and the feature system knows about player concepts.

---

### Cross-Layer Coupling

The architecture claims a three-layer separation (Data / Engine / Control), but the actual imports violate it:

```
Control Layer (main.py)
    ├──► imports LEVELS from engine.player    [Control → Engine data]
    ├──► imports GEAR_CATALOG from engine.player [Control → Engine data]
    └──► imports display functions directly      [Control → Engine rendering]

Engine Layer (mission_engine.py)
    ├──► imports display functions directly    [Engine → Rendering]
    └──► imports GEAR_CATALOG lazily           [Engine → Player data]

Data Layer (missions/ch*.py)
    └──► imports Mission from engine.mission_engine [Data → Engine]
```

**Verdict:** The Data layer is clean. The Engine layer bleeds into Rendering and Player data. The Control layer is a tangled mess that knows everything.

---

## 3. Cohesion Analysis

### High Cohesion Modules

| Module | Cohesion Score | Reason |
|--------|---------------|--------|
| `save_system.py` | High | Does one thing: JSON persistence. All 4 functions relate to save slots. |
| `missions/ch*.py` | Very High | Each file defines exactly one chapter's missions. |
| `display.py` (partial) | Moderate-High | All functions relate to ANSI rendering, but input functions are mixed in. |

### Low Cohesion Modules

| Module | Cohesion Score | Reason |
|--------|---------------|--------|
| `main.py` | Very Low | Menus, loops, special modes, chapter imports, prologue, boot sequence, global singleton. |
| `features.py` | Low | Hints, achievements, factions, and level calculation are unrelated. |
| `player.py` | Low-Medium | Player entity, gear catalog, level thresholds, and achievement tracking are mixed. |
| `mission_engine.py` | Low-Medium | Orchestration, state mutation, achievement checking, and display calls are mixed. |

---

## 4. Dependency Relationships

### Import Graph

```
main.py
    ├──► engine.display
    ├──► engine.player
    ├──► engine.save_system
    ├──► engine.mission_engine
    ├──► engine.terminal_sim
    ├──► engine.features
    ├──► missions.ch01_hardware
    ├──► missions.ch02_boot
    ├──► ... (22 chapter imports)
    └──► missions.ch22_final_exam

engine.mission_engine
    ├──► engine.display
    ├──► engine.terminal_sim
    ├──► engine.player (lazy for GEAR_CATALOG)
    └──► engine.features (for HintRequest)

engine.player
    ├──► engine.features (for calculate_level)
    └──► (circular back to features)

engine.terminal_sim
    └──► engine.display

engine.features
    └──► engine.player (indirect, for AchievementTracker)

engine.save_system
    └──► engine.player (for to_dict/from_dict)

missions/ch*.py
    └──► engine.mission_engine (for Mission, QuizQuestion)
```

---

### Shared Utilities and Libraries

#### The `class C` ANSI Palette

**Location:** `engine/display.py`

**Used by:** `main.py`, `mission_engine.py`, `terminal_sim.py`

**What it is:** A static class holding 15+ pre-computed ANSI escape strings. Every colored output concatenates these strings.

**Why it matters:** This is the only truly shared "library" in the codebase. Every module that prints colored text depends on it.

---

#### The `SIMULATED_OUTPUTS` Dict

**Location:** `engine/terminal_sim.py`

**Used by:** `terminal_sim.py` internally, via `get_output()`

**What it is:** A flat global dict mapping command strings to pre-written output blocks. It is never imported by other modules directly.

**Why it matters:** This is a hidden data dependency. The terminal simulator's behavior is determined by this dict, but it is not parameterized or configurable.

---

#### The `CHAPTERS` Tuple List

**Location:** `main.py`

**Used by:** `main.py` internally (game_hub, chapter_menu)

**What it is:** A manually maintained list of 22 tuples mapping chapter IDs to mission lists, topic tags, titles, and subtitles.

**Why it matters:** This is the central registry of all content. It is a control-layer data structure that tightly couples the menu system to the content.

---

#### The `ACHIEVEMENTS` Dict

**Location:** `engine/features.py`

**Used by:** `mission_engine.py` (for unlock checks), `player.py` (for AchievementTracker)

**What it is:** A declarative dict of 19 Achievement dataclass instances.

**Why it matters:** Achievement data is separated from achievement logic, but the logic is scattered inline in `mission_engine.py` rather than centralized.

---

## 5. Module Sizing

| Module | Lines | Responsibilities | Assessment |
|--------|-------|-----------------|------------|
| `main.py` | ~1,374 | Entry point, menus, loops, all chapter imports, special modes, global state | Too large. Should be split into `menus.py`, `modes.py`, and `app.py`. |
| `engine/terminal_sim.py` | ~4,457 | Simulated command outputs + REPL logic | Data overwhelms logic. The dict should be split into per-chapter files. |
| `engine/mission_engine.py` | ~514 | Mission dataclasses + MissionRunner | The `run()` method is ~250 lines. Should be split into phase methods or classes. |
| `engine/player.py` | ~392 | Player dataclass + levels + gear + achievements | Three concerns in one file. Gear catalog and level thresholds could move to `features.py`. |
| `engine/display.py` | ~324 | ANSI colors + all rendering + input functions | Input functions (`prompt_input`) should move to a separate `input.py` module. |
| `engine/features.py` | ~276 | Hints + achievements + factions + level calc | A grab-bag. Should be split into `hints.py`, `achievements.py`, `factions.py`. |
| `engine/save_system.py` | ~72 | JSON persistence | Appropriately sized. |
| `missions/ch*.py` (each) | ~600–900 | Mission data for one chapter | Appropriately sized for content files. |

---

## 6. Refactoring Recommendations

### Immediate: Split `main.py`

```
main.py              →  Entry point + GameState only
menus.py             →  main_menu, new_game_menu, load_game_menu, manage_saves_menu
hub.py               →  game_hub, chapter_menu
modes.py             →  review_mode, timed_exam_mode, show_linux_readiness
status.py            →  show_player_status, show_inventory
```

### Medium: Split `features.py`

```
engine/hints.py      →  HintLevel, HintRequest
engine/achievements.py →  Achievement, AchievementTracker, ACHIEVEMENTS
engine/factions.py   →  FactionStatus, FACTIONS, calculate_level (reputation variant)
engine/levels.py     →  LEVELS, calculate_level (XP variant)
```

### Medium: Separate Terminal Data from Logic

```
engine/terminal_data.py    →  SIMULATED_OUTPUTS (or per-chapter files)
engine/terminal_sim.py     →  REPL logic only, imports terminal_data
```

### Long-term: Extract Mission Phases

```
engine/phases/story_phase.py
engine/phases/terminal_phase.py
engine/phases/quiz_phase.py
engine/phases/reward_phase.py
```

Each phase receives a `MissionContext` and mutates it. `MissionRunner.run()` becomes an orchestrator that passes the context through the pipeline.

---

## Summary

| Module | Natural Boundary | Cohesion | Coupling | Recommended Action |
|--------|-----------------|----------|----------|-------------------|
| `missions/ch*.py` | Content unit | Very High | Very Low | Leave as-is |
| `engine/save_system.py` | Persistence | High | Low | Leave as-is |
| `engine/display.py` | Rendering | Moderate-High | High (incoming) | Extract input functions |
| `engine/terminal_sim.py` | Terminal sim | Moderate | Moderate | Split data from logic |
| `engine/mission_engine.py` | Mission flow | Low-Medium | High | Extract phases |
| `engine/player.py` | Player state | Low-Medium | Moderate | Extract gear catalog and levels |
| `engine/features.py` | Meta-game | Low | Moderate | Split into 3+ modules |
| `main.py` | Application control | Very Low | Very High | Split into 4+ modules |
