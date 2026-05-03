# Design Concepts Inventory

## Architectural Patterns

### Three-Layer Architecture (Data / Engine / Control)
The codebase is organized into three conceptual layers: `missions/` (data/content), `engine/` (business logic), and `main.py` (control/UI). This separation keeps content (500+ missions) independent from rendering and persistence logic.

**Status:** Fully implemented. However, the layers are not strictly enforced — `main.py` directly imports `LEVELS` and `GEAR_CATALOG` from `engine.player`, and `mission_engine.py` imports display functions directly, creating cross-layer coupling.

### Template Method Pattern (`MissionRunner.run()`)
Every mission follows an identical pedagogical sequence: ASCII art → story → why_important → explanation → syntax → example → terminal task → quiz → exam_tip → memory_tip → XP reward. This rigid structure is hardcoded in `run()` as a linear script.

**Status:** Fully implemented. The sequence is intentional for pedagogical consistency, but at ~250 lines the method has become a "god method" absorbing display, game logic, achievement checks, and reward logic.

### Data-as-Code (Python Literals as Content Format)
All mission content (stories, explanations, quiz questions, ASCII art) is written as Python literals inside `.py` files rather than JSON, YAML, or a database. Python itself is the parser and validator.

**Status:** Fully implemented. Benefits: zero parser code, syntax errors caught at import time, easy git diff. Trade-off: unconditional eager loading and tight content-code coupling.

### Singleton Pattern (`GameState`)
A single global `GAME` instance holds the active player, save slot, and running flag. It is instantiated at module import time in `main.py` and imported by nothing else (other modules mutate it via parameter passing, not import).

**Status:** Implemented. Mixes player data, save metadata, and loop control in one object. No read-only properties or access control.

### Strategy Pattern (Mission Types)
Seven mission types exist (`SCAN`, `INFILTRATE`, `DECODE`, `CONSTRUCT`, `REPAIR`, `QUIZ`, `BOSS`). The `run()` method branches behavior based on `mtype` — e.g., BOSS missions call `_run_boss()`, QUIZ missions skip the terminal task.

**Status:** Implemented. Types are hardcoded strings (not an Enum) checked via `if/elif`. Adding an 8th type requires editing `run()` and the header color map in `display.py`.

---

## Input Routing

### Hardcoded `if/elif` Dispatch Chains
`game_hub()` contains 22 sequential `elif choice == "N": chapter_menu(N)` branches. `chapter_menu()` mixes three parsing strategies: mission ID string (`choice.startswith(prefix)`), numeric index (`choice.isdigit()`), and keywords (`"all"`, `"q"`).

**Status:** Implemented. Adding chapter 23 requires editing 3 places. The numeric index strategy (`missions[int(choice)-1]`) is fragile — reordering missions breaks save compatibility.

### Replay Gate (`completed_missions` check)
If a non-BOSS mission is already completed, `run()` delegates to `_replay_mission()`, which shows only the quiz for half XP. BOSS missions cannot be replayed.

**Status:** Implemented. The replay logic is a special case at the top of `run()`, not a general state machine.

---

## State Mutation Patterns

### Inline Achievement Checking
Achievement triggers are scattered as inline `if` statements inside `run()` and `_run_boss()`. There are ~10 separate checks for `first_mission`, `boss_defeated`, `five_bosses`, `all_bosses`, `quest_marathon`, `level_ten`, etc.

**Status:** Implemented but incomplete. Two achievements (`perfect_quiz`, `no_hints`) are defined but never triggered. `boss_defeated` logic is duplicated in `run()` and `_run_boss()`.

### Mid-Mission State Mutation (No Rollback)
XP is deducted for hints mid-mission. Mission completion and XP addition happen incrementally. If the process crashes after XP is added but before `save_callback` runs, the player keeps the XP but not the completion.

**Status:** Implemented. No transaction or checkpoint system exists. The save callback is called at the very end, but hint deductions happen earlier with no undo.

---

## Display Design Patterns

### Screen Statelessness
The display layer has no retained state. `clear()` wipes the screen; every function writes fresh. There is no concept of "dirty regions" or partial redraws.

**Status:** Fully implemented. Appropriate for a CLI game but makes transitions and animations less flexible.

### Decorative Box Drawing
Functions like `box()`, `mission_header()`, and `boss_intro()` draw decorative borders using Unicode box-drawing characters (`╔`, `═`, `╗`, `║`, etc.) with ANSI color prefixes.

**Status:** Fully implemented. Width is hardcoded to 66-68 characters. No responsive sizing for narrow terminals.

### Color-by-Type Mapping
`mission_header()` uses a `type_colors` dict to assign a unique color to each `mtype`. BOSS missions render in `DANGER` (red). QUIZ missions render in `NEON` (bright cyan).

**Status:** Implemented. The color map is a hardcoded dict in `display.py`. The `CONSTRUCT` type uses a raw escape string instead of a `C.*` alias, creating inconsistency.

---

## Implicit Design Decisions

### "Pedagogical Consistency > Modularity"
The rigid mission sequence (story → explanation → terminal → quiz) is not an accident — it is a deliberate teaching structure. The developer chose to keep it in one linear method rather than extract phases, prioritizing readability of the teaching flow over code modularity.

**Rationale:** A solo developer maintaining 501 missions values "I can read the whole mission flow top-to-bottom" over "each phase is independently testable."

**Impact:** High maintenance burden. Adding a new phase (e.g., a "practice" step between explanation and terminal) requires editing the middle of a 250-line method.

### "Content Completeness > Engine Polish"
The project reached "100% content-complete" (2026-04-21) before architectural refinement. All 501 missions, 1,117 quiz questions, and 22 chapters exist. Engine gaps (missing config, dead achievements, manual serialization) were accepted as "good enough for shipping."

**Rationale:** A terminal learning game's primary value is content, not engine features. The developer correctly prioritized finishing chapters over adding a settings menu.

**Impact:** The engine is in "MVP-plus" state — functional but with known fragility. Future development (new chapters, modding, testing) will hit these gaps immediately.

### "Pure Stdlib > Ecosystem"
Every design decision is filtered through "can we do this without `pip install`?" No `colorama`, no `pydantic`, no `pytest`, no `click`, no `rich`. Even `jsonschema` is avoided.

**Rationale:** Zero-setup installation (`python3 main.py`) is a core value proposition. Adding dependencies would complicate distribution for non-technical Linux learners.

**Impact:** Reinvents wheels (manual serialization, color handling, input validation) that libraries would solve. The "no dependencies" rule is a trade-off, not a bug — but it needs to be documented as an intentional constraint.

### "Fail Fast at Startup"
All 22 chapter files are imported eagerly. A syntax error in any chapter file crashes the game before the title screen.

**Rationale:** Better to crash immediately than to discover a broken chapter mid-session. This assumes the data is static and complete.

**Impact:** During active development, any chapter edit risks breaking the entire application. The "fail fast" philosophy becomes a liability when content is being actively modified.
