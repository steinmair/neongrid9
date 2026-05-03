# Missing Concepts Inventory

These are concepts that are **expected or required** for a codebase of this scope and purpose, but are currently **absent or incomplete**. Each entry includes: what it is, why it is needed, and the impact of its absence.

---

## 1. Configuration System

**What it is:** A mechanism to read settings from a file (`~/.neongrid9/config.json`) or CLI arguments (`--no-color`, `--no-animation`, `--chapter 5`).

**Why it is needed:**
- Players on terminals without ANSI support see raw escape codes.
- Players with reading difficulties or motor impairments cannot speed up animations.
- Speedrunners and testers are forced to wait through `time.sleep()` delays.
- No way to change the save directory from the hardcoded `~/.neongrid9`.

**Impact:** The game is unusable on some terminals. Testing is painful. No customization.

**Rationale for absence:** "Pure stdlib" constraint + atmosphere-as-feature design. The developer viewed hardcoded delays as part of the cyberpunk experience.

---

## 2. Data Validation / Schema System

**What it is:** A `validate_mission(m: Mission) -> List[str]` function that checks mandatory fields, mission ID consistency, quiz question count, and expected_commands presence.

**Why it is needed:**
- A mission with empty `quiz_questions` would crash in `_run_quiz()`.
- A SCAN mission with empty `expected_commands` makes the terminal task impossible.
- A `mission_id` mismatch (e.g., chapter 5 mission labeled "4.01") breaks save compatibility.
- The `achievements` field was forgotten in `to_dict()` — a schema would have caught this.

**Impact:** Silent data corruption, runtime crashes, and inconsistent save states. Content authors have no guardrails.

**Rationale for absence:** The content was "frozen" after a 2026-04-21 audit. The developer assumed static, complete data does not need runtime validation.

---

## 3. Event-Driven Architecture (Observer Pattern)

**What it is:** A central `AchievementEngine` that registers listeners for events (`mission_completed`, `quiz_perfect`, `hint_used`, `boss_defeated`) and evaluates unlock conditions independently of `MissionRunner`.

**Why it is needed:**
- Two achievements (`perfect_quiz`, `no_hints`) are defined but never triggered.
- `boss_defeated` logic is duplicated in `run()` and `_run_boss()`.
- Adding a new achievement requires editing a 250-line method.
- `quest_marathon` checks `len(completed_missions) == 100` exactly — if a "complete all" feature skips from 99 to 101, it never triggers.

**Impact:** Dead features, duplicated logic, maintenance burden.

**Rationale for absence:** 19 achievements felt "small enough" for inline `if` statements. No test suite existed to flag dead achievements.

---

## 4. Transactional State Management (Atomic Mission Completion)

**What it is:** A `MissionResult` dataclass that collects all state changes (XP delta, mission completion, gear, reputation, achievements) and applies them atomically at the end of a mission.

**Why it is needed:**
- If the game crashes after XP is deducted for hints but before `save_callback`, the player loses XP with no mission completion.
- If `save_callback` raises an exception, all prior mutations (XP, gear, reputation) have already been applied but are unsaved.
- No rollback mechanism exists for partial mission failures.

**Impact:** Data inconsistency and player frustration. A crash mid-mission corrupts progress.

**Rationale for absence:** The game runs in a single thread with no async. The developer assumed `KeyboardInterrupt` is the only crash path, and the outer `except` handles saving.

---

## 5. Lazy Loading / Auto-Discovery for Chapters

**What it is:** Using `importlib` + `pkgutil` to discover chapter files dynamically, loading them only when the player selects the chapter.

**Why it is needed:**
- All 22 chapter files are imported unconditionally. A syntax error in `ch18_storage.py` crashes the game before the title screen.
- Adding chapter 23 requires editing 66 places (22 imports + 22 CHAPTERS tuples + 22 `if` branches).
- Memory footprint includes all 500+ missions even if the player only plays chapter 1.
- Import time is 0.5-2 seconds.

**Impact:** Fragile startup, high maintenance burden, slow cold start.

**Rationale for absence:** "Data as Code" philosophy. The developer chose explicit imports for discoverability and preferred startup crashes to mid-session crashes.

---

## 6. Display Driver Abstraction

**What it is:** A `DisplayDriver` interface with `AnimatedDisplay` (uses `time.sleep()`) and `InstantDisplay` (no delays) implementations. Configurable via CLI flag or config file.

**Why it is needed:**
- Automated tests must wait for `time.sleep()` to finish. A 10-mission test suite would take minutes.
- Users on slow terminals or with reading difficulties cannot skip animations.
- CI/CD cannot run the game headlessly because `input()` blocks forever.
- Raw ANSI codes appear as gibberish on `dumb` TERM or Windows Command Prompt.

**Impact:** Untestable, inaccessible, and non-portable display layer.

**Rationale for absence:** "Pure stdlib" + "atmosphere is a feature." The developer viewed delays as part of the cyberpunk mood.

---

## 7. Testing Framework / Unit Tests

**What it is:** A `tests/` directory with unit tests for `Player` serialization, `MissionRunner` logic, achievement triggers, and terminal command matching.

**Why it is needed:**
- The `achievements` serialization bug would have been caught by a round-trip test.
- The `perfect_quiz` dead achievement would have been caught by a coverage test.
- Refactoring `run()` is too risky without tests.
- `calculate_level()` has dual behavior (reputation vs XP) that should be verified.

**Impact:** Bugs persist undetected. Refactoring is blocked. No regression safety.

**Rationale for absence:** "Pure stdlib" constraint. Writing tests without `pytest` requires `unittest`, which is verbose. The developer prioritized content over infrastructure.

---

## 8. Logging System (Structured)

**What it is:** A `logging` module-based system with log levels (DEBUG, INFO, WARN, ERROR) writing to `~/.neongrid9/game.log`.

**Why it is needed:**
- Save failures are silently swallowed by `except Exception: print(...)`.
- Achievement unlocks are not logged — if a player claims an achievement didn't trigger, there is no evidence.
- Terminal simulator command lookups are not traced for debugging.
- No audit trail for player actions.

**Impact:** Impossible to debug player issues. Silent failures go unnoticed.

**Rationale for absence:** `print()` is simpler than `logging` for a CLI game. The developer used stdout as the single output channel.

---

## 9. Save File Versioning / Migration System

**What it is:** A `version` field in the save JSON. If the loaded version is older than the current engine, a migration function upgrades the data (e.g., adding missing factions, converting old field names).

**Why it is needed:**
- `from_dict()` already does lightweight migration (filling missing factions with 0), but this is implicit and undocumented.
- Adding a new field to `Player` breaks old saves unless `.get()` defaults are provided.
- There is no way to detect a corrupted or tampered save file.
- No schema validation means a hand-edited save with `"xp": "not_a_number"` will crash later.

**Impact:** Data loss when the schema changes. Old saves may behave unpredictably.

**Rationale for absence:** The schema was "frozen" at project completion. The developer assumed no further fields would be added.

---

## 10. Input Sanitization & Command History

**What it is:**
- A command history buffer so players can press Up/Arrow to recall previous terminal commands.
- Input sanitization to prevent control character injection.
- Tab-completion for known commands.

**Why it is needed:**
- Retyping `lspci -vv` after a typo is frustrating. Real terminals have history.
- Pasting multi-line text or control characters into `input()` can break the display.
- Tab-completion would reinforce command memorization.

**Impact:** Poor UX compared to a real terminal. Friction reduces learning efficiency.

**Rationale for absence:** Python's built-in `input()` has no history or completion. Adding `readline` would require platform-specific handling and complicate the "pure stdlib" promise.

---

## 11. Difficulty Adaptation / Dynamic Quiz Scaling

**What it is:** Adjusting quiz question difficulty or XP rewards based on player performance. If a player consistently answers hardware questions correctly, the game could reduce hardware quiz frequency or increase difficulty.

**Why it is needed:**
- Advanced Linux users find early chapters too easy. The game offers only 3 static starting profiles (beginner, intermediate, expert).
- There is no adaptive learning path. A player who already knows `lspci` still has to sit through 5 missions about it.

**Impact:** Low replay value for experienced users. The game cannot personalize the learning curve.

**Rationale for absence:** Adaptive learning is complex. The developer chose a linear, chapter-based structure for pedagogical clarity.

---

## 12. Accessibility Features

**What it is:**
- `--no-animation` flag for screen readers and slow readers.
- `--no-color` flag for colorblind users or monochrome terminals.
- High-contrast mode.
- Keyboard shortcut navigation (e.g., `1` for chapter 1 without typing the full number).

**Why it is needed:**
- Screen readers struggle with typewriter text animations.
- Red/green colorblind users cannot distinguish `C.SUCCESS` from `C.DANGER`.
- ANSI escape codes are invisible to screen readers or render as noise.

**Impact:** The game is inaccessible to players with visual impairments, motor disabilities, or color vision deficiencies.

**Rationale for absence:** "Pure stdlib" + "atmosphere is a feature." The developer did not consider accessibility a priority for a terminal-based learning tool.

---

## 13. Analytics / Telemetry (Opt-in)

**What it is:** Optional, anonymized tracking of quiz accuracy, hint usage, mission completion times, and commonly failed commands. Written to a local file for the player's own review.

**Why it is needed:**
- Players cannot see their own learning patterns (e.g., "I always fail network questions").
- The developer has no data on which missions are too hard or too easy.
- `show_linux_readiness()` is static — it does not improve with usage data.

**Impact:** No feedback loop for content improvement. Players lack self-assessment tools beyond the basic stats screen.

**Rationale for absence:** Privacy concerns and "pure stdlib" constraint. The developer included `chapter_quiz_stats` but does not surface it in a meaningful analytics view.

---

## 14. Plugin / Modding System

**What it is:** A mechanism to load custom chapters from a `mods/` directory or external Python modules, extending the game without editing core files.

**Why it is needed:**
- The current architecture requires editing `main.py` to add a chapter.
- Linux content evolves (new kernel versions, new tools). A modding system would allow community contributions.
- LPIC-2 content (chapter 23+) is mentioned in CLAUDE.md as a "future enhancement" but requires core changes.

**Impact:** The project cannot grow without modifying the engine. Community content is impossible.

**Rationale for absence:** The scope was fixed at 22 chapters. The developer did not design for extensibility because the content was "complete."

---

## 15. Localization / i18n (Internationalization)

**What it is:** A string table system where all UI text, story text, and quiz questions are loaded from language-specific files. Default is German; English (and others) could be added.

**Why it is needed:**
- The game is entirely in German. Non-German speakers cannot use it.
- LPIC-1 is a global certification. English is the lingua franca of Linux documentation.
- Hardcoded German strings are scattered across 7,000+ lines of code.

**Impact:** The addressable market is limited to German speakers. No pathway to English, Spanish, French, etc.

**Rationale for absence:** The developer is German and targeted German LPIC learners. Retrofitting i18n into 7,000 lines of inline German text is a massive undertaking.

---

## 16. Error Recovery & Rollback

**What it is:** A checkpoint system that saves player state *before* a mission starts. If the mission crashes or the player quits, the state can be restored to the pre-mission checkpoint.

**Why it is needed:**
- Hint XP deductions are irreversible. A player who accidentally triggers hints loses XP permanently.
- A crash after hint deduction but before mission completion leaves inconsistent state.
- The outer `except KeyboardInterrupt` saves the *current* state, including partial mission progress.

**Impact:** Players can lose progress or get stuck with bad decisions.

**Rationale for absence:** "Fail fast" philosophy. The developer assumed the only error path is `KeyboardInterrupt`, which saves current state.

---

## 17. CLI Argument Parsing (`argparse`)

**What it is:** Using Python's built-in `argparse` to support flags like `--slot 2`, `--no-color`, `--chapter 5`, `--mission 3.01`, `--speedrun`.

**Why it is needed:**
- No way to jump directly to a specific mission for testing or review.
- No way to run the game in a headless or CI environment.
- No way to override the save directory for portable installs.

**Impact:** Developers and power users cannot script or automate the game.

**Rationale for absence:** The game is designed as an interactive experience. The developer viewed CLI flags as unnecessary complexity for a "just run it" tool.

---

## Summary: Criticality Ranking

| # | Concept | Criticality | Effort to Add |
|---|---------|-------------|---------------|
| 1 | Configuration System | High | Low |
| 2 | Data Validation | High | Low |
| 3 | Event-Driven Achievements | Medium | Medium |
| 4 | Transactional State | Medium | Medium |
| 5 | Lazy Auto-Discovery | Medium | Medium |
| 6 | Display Driver Abstraction | Medium | Medium |
| 7 | Testing Framework | High | Medium |
| 8 | Logging System | Medium | Low |
| 9 | Save Versioning | Medium | Low |
| 10 | Input History | Low | Low |
| 11 | Difficulty Adaptation | Low | High |
| 12 | Accessibility Features | High | Medium |
| 13 | Analytics (Opt-in) | Low | Medium |
| 14 | Plugin/Modding System | Low | High |
| 15 | Localization | High | Very High |
| 16 | Error Recovery | Medium | Medium |
| 17 | CLI Argument Parsing | Low | Low |
