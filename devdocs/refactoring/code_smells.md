# Code Smells in NeonGrid-9

This document catalogs concrete code smells detected through static analysis of
the codebase. Each entry includes severity, exact locations, a suggested remedy,
and a fix priority.

---

## 1. Technical Debt Smells

### 1.1 God Functions (>50 lines)

| Severity | high |
|----------|------|
| Priority | **1** |

**Problem:** Multiple functions exceed 50 lines and perform many unrelated tasks,
making them hard to test, reason about, and refactor safely.

| Function | File | Lines | LOC |
|----------|------|-------|-----|
| `_show_chapter_complete` | `main.py` | 602–888 | 286 |
| `timed_exam_mode` | `main.py` | 994–1185 | 191 |
| `MissionRunner.run` | `engine/mission_engine.py` | 82–339 | 257 |
| `game_hub` | `main.py` | 395–513 | 118 |
| `_run_boss` | `engine/mission_engine.py` | 410–498 | 88 |
| `chapter_menu` | `main.py` | 515–600 | 85 |
| `review_mode` | `main.py` | 1187–1271 | 84 |
| `run_terminal` | `engine/terminal_sim.py` | ~4386 | 72 |
| `_run_quiz` | `engine/mission_engine.py` | 340–409 | 69 |
| `about_screen` | `main.py` | 321–389 | 68 |
| `Player.stats_summary` | `engine/player.py` | 274–326 | 52 |

**Suggested remedy:**
- Extract each numbered phase in `MissionRunner.run()` into private methods
  (`_show_intro()`, `_run_terminal_task()`, `_run_quiz_phase()`, `_award_rewards()`).
- Split `_show_chapter_complete` into data-loading (`_load_recap_data`) and
  rendering (`_render_recap_screen`) halves.
- Decompose `timed_exam_mode` into setup, exam loop, and result-screen functions.

---

### 1.2 Deep Nesting (>3 levels)

| Severity | high |
|----------|------|
| Priority | **2** |

**Problem:** Deeply nested control flow makes the code hard to follow and increases
cognitive load. AST analysis measured maximum nesting depth per function.

| Function | File | Max Nesting |
|----------|------|-------------|
| `game_hub` | `main.py` | **30** |
| `chapter_menu` | `main.py` | 7 |
| `main` | `main.py` | 6 |
| `MissionRunner.run` | `engine/mission_engine.py` | 6 |
| `timed_exam_mode` | `main.py` | 5 |

**Root cause in `game_hub`:** The main gameplay loop nests `if/elif` chains for
menu choices inside a `while GAME.running` loop, with additional nesting for
mission replay logic, save callbacks, and chapter-completion checks.

**Suggested remedy:**
- Replace the 22-way `if/elif` chapter dispatch with a dictionary lookup or direct
  integer cast (see *emerging_patterns.md* 4.1).
- Extract each menu branch body into a standalone function.
- Introduce early-returns (`return` instead of deep `else` blocks) in
  `MissionRunner.run()`.

---

### 1.3 Magic Numbers without Named Constants

| Severity | medium |
|----------|--------|
| Priority | **4** |

**Problem:** Numeric literals are scattered through business logic, making balance
changes error-prone and the intent opaque.

| Number | Location | Meaning |
|--------|----------|---------|
| `22` | `engine/mission_engine.py:261` | Total bosses for achievement |
| `31` | `engine/mission_engine.py:269` | Chapter 1 mission count for achievement |
| `100` | `engine/mission_engine.py:276` | Missions for "quest_marathon" |
| `5` | `engine/mission_engine.py:255, 290` | Boss quiz count / chapter mastery threshold |
| `10` | `engine/mission_engine.py:282` | Level threshold for "level_ten" achievement |
| `300` / `900` | `engine/mission_engine.py:360` | Speed-run timer thresholds (seconds) |
| `5400` | `main.py:998` | Exam time limit (seconds) |
| `800` / `500` | `main.py:1108` | Exam scoring thresholds |
| `1.2` / `1.1` / `1.3` | `engine/player.py:193–201` | XP scaling multipliers by level |
| `1500` | `main.py:252` | Starting XP for test player / load-game path |

**Suggested remedy:**
```python
# engine/constants.py
BOSS_COUNT_TOTAL = 22
CHAPTER_1_MISSION_COUNT = 31
MARATHON_MISSION_THRESHOLD = 100
CHAPTER_MASTERY_THRESHOLD = 5
SPEEDRUN_FAST_SECONDS = 300
SPEEDRUN_SLOW_SECONDS = 900
EXAM_TIME_LIMIT_SECONDS = 5400
EXAM_SCORE_EXCELLENT = 800
EXAM_SCORE_PASS = 500
```

---

### 1.4 Dead Code (Unreachable / Unused)

| Severity | low |
|----------|-----|
| Priority | **7** |

**Problem:** Fragments that are never executed or referenced clutter the codebase
and mislead readers.

| Location | Issue |
|----------|-------|
| `engine/save_system.py` | Entire module is deprecated per CLAUDE.md; superseded by `storage.py`. Still imported in some smoke tests. |
| `engine/mission_engine.py:297` | Late import `from engine.features import calculate_level` — suggests prior circular-import workaround that may no longer be needed. |
| `engine/mission_engine.py:321, 488` | Late imports of `GEAR_CATALOG` inside methods; could be moved to top-level if cycle is resolved. |

**Suggested remedy:**
- Audit `engine/save_system.py` against all imports; delete or mark `@deprecated`.
- Promote late imports to top-level after resolving any remaining cycles.

---

### 1.5 Circular Dependencies

| Severity | medium |
|----------|--------|
| Priority | **5** |

**Problem:** Inline/late imports are a symptom of circular or fragile dependency
graphs. They hide structure problems and complicate static analysis.

| Location | Import | Likely Reason |
|----------|--------|---------------|
| `engine/mission_engine.py:297` | `from engine.features import calculate_level` | Avoids cycle with `player.py` |
| `engine/mission_engine.py:321` | `from engine.player import GEAR_CATALOG` | Avoids cycle with `player.py` |
| `engine/mission_engine.py:488` | `from engine.player import GEAR_CATALOG` | Same as above |
| `smoke_tests/test_03_mission_engine.py:26` | `from main import CHAPTERS` | Test depends on UI entry point |

**Suggested remedy:**
- Move `calculate_level()` to a pure utility module (e.g., `engine/utils.py`).
- Move `GEAR_CATALOG` to a lightweight `engine/data/gear_catalog.py` so both
  `player.py` and `mission_engine.py` can import it safely.
- Replace `from main import CHAPTERS` in tests with direct chapter-file imports
  (`from missions.ch01_hardware import CHAPTER_1_MISSIONS`, etc.) or a central
  `chapter_registry.py` that has no UI dependency.

---

## 2. Architectural Smells

### 2.1 Business Logic in UI / Controllers

| Severity | high |
|----------|------|
| Priority | **1** |

**Problem:** `engine/mission_engine.py` — nominally the game-engine layer — contains
35 `print()` calls and 36 direct `C.COLOR` references, tightly coupling mission logic
to terminal rendering. `main.py` (the UI controller) additionally contains 213
`print()` statements, plus save logic, progress calculation, and menu rendering all
mixed together.

**Quantified coupling:**
- `engine/mission_engine.py`: 35 `print()`, 36 `C.*` color references
- `main.py`: 213 `print()`, mixed with `input()` calls and game-loop state

**Suggested remedy:**
- Introduce the `Renderer` protocol already sketched in `engine/renderer.py`.
- Make `MissionRunner` accept a `renderer: Renderer` in `__init__`; replace every
  `print(C. ...)` with `self.renderer.show_success(...)`, etc.
- Migrate all `print()` calls in `main.py` menu functions to use `engine/display.py`
  helpers exclusively, or push them through `Renderer` as well.

---

### 2.2 Data Access Scattered Everywhere

| Severity | medium |
|----------|--------|
| Priority | **6** |

**Problem:** Save/load logic, chapter metadata, and recap data are accessed
directly from `main.py` rather than through a single boundary.

| Concern | Scattered Locations |
|---------|---------------------|
| Save slot logic | `main.py:252`, `266`, `301`, `323` |
| Chapter recap data | `main.py:616–873` (286-line inline dict) |
| `CHAPTERS` tuple construction | `main.py` (imports all 22 chapter modules) |

**Suggested remedy:**
- Move the inline `recap_map` to `data/recaps.py` or JSON.
- Wrap save-slot operations in a `GameSession` class that owns `SaveRepository`.
- Have `main.py` depend only on `chapter_registry.py` instead of importing all
  22 mission modules directly.

---

### 2.3 No Clear Module Boundaries

| Severity | medium |
|----------|--------|
| Priority | **5** |

**Problem:** The dependency graph between `engine/` modules is dense and bidirectional.
`mission_engine.py` imports from `player.py` and `features.py`; `player.py` imports
from `features.py`; `main.py` imports everything. There is no inner/outer ring
separation.

**Evidence:**
- `engine/mission_engine.py` knows about `Player`, `GEAR_CATALOG`, `calculate_level`,
  `show_success`, `xp_bar`, `prompt_continue` — it is both engine and presenter.
- `engine/player.py` contains `GEAR_CATALOG`, `RARITY_COLOR`, and `gear_bonus()`
  logic — data, presentation color, and business logic in one file.

**Suggested remedy:**
- **Core domain** (pure data): `Mission`, `QuizQuestion`, `Player`, `LEVELS`
- **Application services** (use cases): `MissionRunner` (no prints), `SaveRepository`
- **Presentation**: `display.py`, `renderer.py`, `main.py`
- **Infrastructure**: `terminal_sim.py`, `storage.py`

Refactor toward import rules: *presentation may import application; application may
import core; never the reverse.*

---

### 2.4 Inconsistent Error Handling

| Severity | medium |
|----------|--------|
| Priority | **3** |

**Problem:** Exceptions are caught and handled differently in every module, leading
to silent failures in some paths and noisy crashes in others.

| Location | Pattern |
|----------|---------|
| `engine/save_system.py` | `except Exception as e: print(f" Speicherfehler: {e}")` — swallows error, returns `None` |
| `main.py` (top level) | `except Exception as e:` (bare catch) + `except KeyboardInterrupt:` |
| `main.py` (menus) | `except ValueError:` in some places, missing in others |
| `engine/mission_engine.py` | Almost no exception handling; assumes all inputs valid |

**Suggested remedy:**
- Define a small `NeonGridError` exception hierarchy (`SaveError`, `ValidationError`).
- Have `save_system.py` log the error and re-raise (or return a `Result` type).
- Unify the top-level handler in `main.py` to catch `NeonGridError`, log, and show
  a user-friendly message before exiting cleanly.

---

### 2.5 Mixed Abstraction Levels

| Severity | high |
|----------|------|
| Priority | **2** |

**Problem:** Single functions alternate between high-level orchestration and
low-level terminal formatting, making both concerns harder to change independently.

**Key locations:**

1. **`main.py:main()`** — mixes `while True` game-loop orchestration with direct
   `print(C.NEON + "\n  TITLE\n" + C.RESET)` screen rendering.

2. **`main.py:_show_chapter_complete()`** — mixes *chapter-complete logic*
   (checking `player.mission_completed`, awarding recap text) with *22 inline data
   lists* and *screen formatting* (`clear()`, `print(...)`).

3. **`engine/mission_engine.py:MissionRunner.run()`** — a 257-line method that
   simultaneously decides *what phase to show next* and *which ANSI color to use*
   for every line.

**Suggested remedy:**
- Adopt the `Renderer` protocol for all output; keep engine code focused on state
  transitions.
- Extract `_show_chapter_complete` into `RecapScreen(recap_data, player)` in
  `engine/display.py` or a new `screens.py` module.
- In `MissionRunner`, replace inline `print()` blocks with named phase methods that
  return *what* to display, letting a renderer handle *how*.

---

## Priority Matrix

| # | Smell | Severity | Files | Effort | Payoff |
|---|-------|----------|-------|--------|--------|
| 1 | God Functions (1.1) | high | 3 | 4 h | very high |
| 2 | Mixed Abstraction (2.5) | high | 2 | 3 h | very high |
| 3 | Deep Nesting (1.2) | high | 2 | 2 h | high |
| 4 | Inconsistent Error Handling (2.4) | medium | 3 | 1 h | high |
| 5 | Magic Numbers (1.3) | medium | 3 | 30 min | medium |
| 6 | Circular Dependencies (1.5) | medium | 3 | 1 h | medium |
| 7 | Module Boundaries (2.3) | medium | 4 | 3 h | medium |
| 8 | Data Access Scattered (2.2) | medium | 1 | 1 h | medium |
| 9 | Business Logic in UI (2.1) | high | 2 | 4 h | very high |
| 10 | Dead Code (1.4) | low | 2 | 15 min | low |

---

## Recommended Order of Attack

1. **Week 1 — Structural Wins**
   - 1.1 God Functions: Extract phases from `MissionRunner.run()`
   - 1.2 Deep Nesting: Flatten `game_hub()` dispatch
   - 2.5 Mixed Abstraction: Introduce `Renderer` in `MissionRunner`

2. **Week 2 — Safety & Boundaries**
   - 2.4 Inconsistent Error Handling: Unify exception strategy
   - 2.1 Business Logic in UI: Move all `print()` out of `mission_engine.py`
   - 1.5 Circular Dependencies: Lift late imports to top-level

3. **Week 3 — Polish**
   - 1.3 Magic Numbers: Extract constants to `engine/constants.py`
   - 2.2 Data Access Scattered: Move `recap_map` out of `main.py`
   - 1.4 Dead Code: Remove deprecated `save_system.py` or mark it
