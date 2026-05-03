# Philosophy — NeonGrid-9 Design Principles

*Derived from structural analysis, coding patterns, and implicit decisions visible in the codebase. This document surfaces assumptions that are not written in README or CLAUDE.md but are evident from how the code is organized and written.*

---

## 1. Pedagogical Consistency Over Modularity

**Principle:** Every mission must follow the exact same teaching sequence: story → explanation → syntax → example → terminal task → quiz → exam tip → memory tip. This sequence is not configurable per mission type or chapter.

**Evidence:**
- `MissionRunner.run()` implements this as a hardcoded linear script (~250 lines) with no phase extraction.
- Even `BOss` missions, which have multi-phase terminal challenges, still follow the same sequence after the boss-specific intro.
- The `story_transitions` field is always exactly 4 elements, accessed by index `tr[0]` through `tr[3]`.

**Rationale:** The developer valued predictable learning rhythm over flexible architecture. A student always knows what comes next. Breaking the sequence into reusable methods or a pipeline would make the flow implicit and harder to read.

**Impact:** Adding a new phase (e.g. a "practice" step) requires editing the middle of a 250-line method. The method is untestable and cannot be composed.

---

## 2. Data as Code (Python Is the Parser)

**Principle:** All content is written as Python literals in `.py` files rather than JSON, YAML, Markdown, or a database. Python itself is the parser, validator, and loader.

**Evidence:**
- 22 chapter files contain `Mission(...)` and `QuizQuestion(...)` constructor calls as top-level module code.
- No `json.load()` for mission data exists anywhere.
- No content validation function exists. The only "validation" is Python's syntax checker at import time.

**Rationale:** Zero dependencies, zero parser code, syntax errors caught at startup, easy version control via git. The developer explicitly rejected JSON/YAML because "Python is the parser."

**Impact:** All 22 files are imported unconditionally at startup. A single typo crashes the game before the title screen. Content authors must know Python to write missions.

---

## 3. Pure Stdlib Over Ecosystem

**Principle:** Every design decision is filtered through "can we do this without `pip install`?" No external packages. No `pytest`, no `colorama`, no `click`, no `rich`, no `pydantic`, no `jsonschema`.

**Evidence:**
- `requirements.txt` does not exist.
- README and header comments explicitly state "Deps: keine (pure stdlib)."
- Manual serialization (`to_dict`/`from_dict`) instead of `pydantic` or `dataclasses.asdict()` with a custom encoder.
- ANSI codes are hardcoded strings instead of `colorama` for Windows compatibility.
- `input()` is used directly instead of `readline` for history.

**Rationale:** Zero-setup installation (`python3 main.py`) is a core value proposition for non-technical Linux learners.

**Impact:** Reinvents wheels (serialization, color handling, input validation) that libraries would solve. Windows compatibility is degraded. Testing requires `unittest` (verbose) instead of `pytest` (ergonomic).

---

## 4. Atmosphere Is a Feature (Not a Bug)

**Principle:** The cyberpunk aesthetic — typewriter text animations, deliberate pacing, neon colors, ASCII art — is not decorative. It is an intentional design choice that should not be configurable or skippable.

**Evidence:**
- `time.sleep()` is hardcoded inside `typewrite()`, `show_story()`, and `show_transition()` with no `animate=False` parameter.
- The boot sequence animation (`show_boot_sequence()`) is 13 lines of `print()` + `time.sleep(0.08)` with no skip flag.
- `level_up_screen()` forces a 1.5-second `time.sleep()` before accepting Enter.
- No `--no-animation` or `--no-color` CLI flags exist.

**Rationale:** The developer views delays as part of the mood and immersion. Making them configurable would "break the experience."

**Impact:** The game is untestable, inaccessible for screen readers, and frustrating for speedrunners and power users.

---

## 5. Fail Fast at Startup

**Principle:** It is better to crash immediately at import time than to discover a broken chapter mid-session.

**Evidence:**
- All 22 chapter files are imported eagerly at the top of `main.py`.
- No `try/except` around chapter imports. A `SyntaxError` in `ch15_security.py` prevents the game from launching.
- No graceful degradation (e.g. "Chapter 15 unavailable, but the rest works").

**Rationale:** Startup crashes are easier to debug than runtime crashes. The data is assumed static and complete.

**Impact:** During active development, any chapter edit risks breaking the entire application. The "fail fast" philosophy becomes a liability when content is being modified.

---

## 6. Content Completeness Over Engine Polish

**Principle:** The project is "done" when all 501 missions are written, not when the engine is perfect. Engine gaps are accepted as "good enough for shipping."

**Evidence:**
- The audit date (2026-04-21) confirms 100% content completion before any architectural refactoring.
- Two achievements are dead (`perfect_quiz`, `no_hints`) but the game ships anyway.
- `FactionStatus` class exists but is never instantiated.
- The `achievements` field is missing from `to_dict()` but no fix was applied.

**Rationale:** A terminal learning game's primary value is content, not engine features. The developer correctly prioritized finishing chapters over adding a settings menu.

**Impact:** The engine is in "MVP-plus" state — functional but with known fragility. Future development will hit these gaps immediately.

---

## 7. Narrative as Memory Anchor

**Principle:** The cyberpunk story is not fluff. It serves as a pedagogical memory aid. Associating `lspci` with "ZARA Z3R0 scanning Sector-7" creates an emotional hook that aids recall.

**Evidence:**
- Every mission has `story`, `speaker`, `story_transitions`, and `ascii_art`.
- The speaker distribution rule (no speaker >60% per chapter) is enforced.
- `speaker_stats` tracks how often each speaker is heard.
- Gear items have narrative names ("Hardware Scanner", "Ghost Mask") tied to boss narratives.

**Rationale:** Mnemonics work better with narrative context. The developer views story as a learning tool, not decoration.

**Impact:** Removing story content would reduce learning effectiveness. The story is a first-class pedagogical feature.

---

## 8. Forgiving Difficulty (No Punishment for Failure)

**Principle:** This is a learning tool, not a competitive game. Failure should never discourage the player.

**Evidence:**
- Failing a terminal task still grants 1/3 of base XP.
- Failing a BOss grants half XP.
- There is no "game over" state.
- Hints are free to access (first tier), and the cost is small (20/50 XP).
- Quiz questions allow 3 attempts per question.

**Rationale:** A certification prep tool should not discourage the learner. Partial credit ensures every attempt has value.

**Impact:** The difficulty curve is flat. Advanced players may find the game too easy, but the target audience benefits from the forgiving design.

---

## 9. Explicit Is Better Than Implicit (When It Is Simple)

**Principle:** The developer prefers visible, hand-written code over "magic" abstractions — but only when the hand-written code is short.

**Evidence:**
- 22 explicit import statements in `main.py` instead of dynamic `importlib` discovery.
- 22 explicit `elif choice == "N"` branches instead of a dispatch dict.
- Manual `to_dict()` with 18 hardcoded keys instead of `dataclasses.asdict()`.
- Hardcoded `CHAPTERS` tuple list instead of auto-discovery.

**Rationale:** Explicit code is readable and debuggable. The developer distrusts "magic" that hides what is happening.

**Impact:** High maintenance burden. Adding a chapter requires editing 66 places. The code is brittle to change.

---

## 10. One Screen, One Function

**Principle:** Each screen (menu, mission, quiz, boss intro) is rendered by a single function that handles everything for that screen.

**Evidence:**
- `MissionRunner.run()` renders the entire mission in one method.
- `game_hub()` renders the entire hub in one function.
- `chapter_menu()` handles display, input, and dispatch in one function.
- No "render tree" or "screen manager" exists. Each function calls `clear()` and prints from top to bottom.

**Rationale:** For a terminal application with no overlapping windows, a single function per screen is the simplest mental model.

**Impact:** No code reuse between screens. `timed_exam_mode()` reimplements its own quiz loop instead of reusing `_run_quiz()` because `_run_quiz()` is tightly coupled to mission state.

---

## 11. Global Mutable State Is Acceptable for Single-Player

**Principle:** In a single-player, single-process, single-threaded CLI game, global mutable state is a pragmatic simplification.

**Evidence:**
- `GAME = GameState()` is a module-level singleton.
- `SIMULATED_OUTPUTS` is a module-level global dict.
- `ACHIEVEMENTS` is a module-level global dict.
- `CHAPTERS` is a module-level global list.
- `MissionRunner.run()` directly mutates `self.player.xp`.

**Rationale:** No concurrency, no multi-user conflicts, no race conditions. Global state is simpler than dependency injection for this use case.

**Impact:** Testing is harder because state persists between test cases. No separation of concerns — `GameState` mixes player data, save slot metadata, and loop control.

---

## 12. Minimalist Error Handling

**Principle:** Errors are caught at a high level with generic `except Exception` blocks. The game should never crash mid-mission.

**Evidence:**
- `save_system.py` wraps all file I/O in `try/except Exception`.
- `main.py` has `except KeyboardInterrupt` and `except Exception` at the top level.
- `mission_engine.py` has no internal error handling inside `run()`.
- Terminal simulator returns `(False, "bash: {cmd}: command not found")` instead of raising.

**Rationale:** A crash mid-mission would lose progress and frustrate the learner. Generic catching is "good enough" because the only expected error is disk I/O or user interrupt.

**Impact:** Silent failures (e.g. auto-save failing) go unnoticed by the player. No error recovery or rollback exists.
