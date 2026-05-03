# Known Requirements — NeonGrid-9

*Inferred directly from the implementation. If the code enforces it, assumes it, or depends on it, it is listed here as a requirement, constraint, or measure.*

---

## Functional Requirements (Inferred)

| ID | Requirement | Evidence in Code |
|----|-------------|------------------|
| FR-01 | The system must present 22 chapters, each containing 20-31 missions. | 22 `missions/ch*.py` files, `CHAPTERS` list with 22 tuples. |
| FR-02 | Each mission must follow a fixed pedagogical sequence: story → explanation → syntax/example → terminal task → quiz → exam tip → memory tip. | `MissionRunner.run()` implements this as a hardcoded linear script. |
| FR-03 | The system must simulate a Linux terminal without executing real shell commands. | `terminal_sim.py` uses a static `SIMULATED_OUTPUTS` dict. No `subprocess` calls for player commands. |
| FR-04 | The system must validate player-typed commands against a list of expected command strings. | `run_terminal()` uses exact, prefix, and base-command matching against `expected_commands`. |
| FR-05 | The system must present 1-5 multiple-choice quiz questions per mission with 4 options (A-D). | `QuizQuestion` dataclass requires 4 options; `_run_quiz()` loops over `mission.quiz_questions`. |
| FR-06 | The system must award XP based on mission completion, quiz correctness, and gear bonuses. | `add_xp()` applies level scaling; `gear_bonus()` multiplies incoming XP. |
| FR-07 | The system must track completed missions in a persistent save file across 3 independent slots. | `save_system.py` writes JSON to `~/.neongrid9/save_slot{1,2,3}.json`. |
| FR-08 | The system must auto-save after every mission completion. | `MissionRunner.run()` calls `save_callback(player)` at the end of every mission. |
| FR-09 | The system must support replaying completed non-BOSS missions for half quiz XP. | `_replay_mission()` checks `mission_id in player.completed_missions` and `mtype != "BOSS"`. |
| FR-10 | The system must display a timed exam mode simulating a 90-minute LPIC-1 exam. | `timed_exam_mode()` in `main.py` pulls 60 questions from Chapter 22 with a live timer. |
| FR-11 | The system must offer a 3-tier hint system (free, 20 XP, 50 XP). | `HintRequest.create()` uses a hardcoded `[0, 20, 50]` cost array. |
| FR-12 | The system must trigger achievements after mission completion based on counters. | Inline `if` checks in `run()` for `first_mission`, `boss_defeated`, `five_bosses`, etc. |
| FR-13 | The system must display player status, inventory, and faction reputation. | `show_player_status()` calls `player.stats_summary()` which builds formatted output. |
| FR-14 | The system must provide a review mode for spaced repetition of weak areas. | `review_mode()` in `main.py` collects quiz questions and weights poorly-performing chapters higher. |
| FR-15 | The system must display a Linux readiness report showing per-chapter progress and quiz accuracy. | `show_linux_readiness()` iterates `CHAPTERS` and highlights accuracy below 60%. |
| FR-16 | The system must support three starting difficulty profiles (beginner, intermediate, expert) with different starting XP. | `new_game_menu()` sets XP=0, 500, or 1500 based on choice "1", "2", or "3". |

---

## Non-Functional Requirements (Inferred)

| ID | Requirement | Evidence |
|----|-------------|----------|
| NFR-01 | The game must run with zero external dependencies (pure Python stdlib). | No `requirements.txt`, no `setup.py`, no `pip install` references. |
| NFR-02 | The game must target Python 3.10 or newer. | `sys.version_info < (3, 10)` check at top of `main.py`. |
| NFR-03 | The game must be playable entirely offline with no network access. | No socket, urllib, or HTTP imports anywhere. |
| NFR-04 | Persistence must use human-readable JSON files in the user's home directory. | `json.dump(..., indent=2, ensure_ascii=False)` to `~/.neongrid9/`. |
| NFR-05 | All text content must be in German. | Every `story`, `explanation`, `exam_tip`, and menu string is hardcoded German. |
| NFR-06 | Startup time is acceptable even with unconditional import of all 22 chapter files. | Eager import of ~7,000 lines of dataclass constructors at module load. |

---

## Constraints (Visible in Code)

| ID | Constraint | Why It Exists |
|----|------------|---------------|
| C-01 | No external packages (stdlib only). | Developer explicitly rejected `pip` ecosystem for zero-setup distribution. |
| C-02 | All mission data must be Python literals in `.py` files (data-as-code). | No JSON/YAML parser needed; git diffs are readable; syntax errors caught at import. |
| C-03 | All 22 chapters are imported unconditionally at startup. | Fail-fast philosophy; no lazy loading logic. |
| C-04 | Terminal output is ANSI-escaped stdout with no fallback. | Pure stdlib; no `colorama`. Assumes modern terminal support. |
| C-05 | Screen clearing delegates to the OS shell via hardcoded platform commands. | Chosen over ANSI escapes; assumes shell access. |
| C-06 | Animation delays (`time.sleep()`) are hardcoded and non-configurable. | Atmosphere-is-a-feature philosophy; no config system exists. |
| C-07 | Input is blocking via built-in `input()` with no timeout. | Pure stdlib; no `readline`, `select`, or async. |
| C-08 | German is the only supported language. | Target audience is German-speaking LPIC-1 learners. No i18n framework. |
| C-09 | Single-player, single-threaded, single-process. | No concurrency model exists; global mutable state assumed safe. |
| C-10 | The save directory is hardcoded to `~/.neongrid9/`. | No config file or CLI flag overrides the path. |

---

## Compliance / Security Measures Present

| ID | Measure | Evidence | Gap |
|----|---------|----------|-----|
| SEC-01 | No real shell commands are executed from player input. | `terminal_sim.py` only does string dict lookups. No `subprocess`, `os.system`, or `exec()` for player commands. | Safe. |
| SEC-02 | Player input is never evaluated as code. | Validation is string comparison (`in`, `==`, `startswith`). No `eval()` or `exec()`. | Safe. |
| SEC-03 | Save files are JSON (not executable). | `json.dump()` serializes plain data. No pickle. | Safe. |
| SEC-04 | Save file writes are inside `try/except`. | `save_system.py` catches `Exception` and prints an error rather than crashing. | However, the return value is ignored — silent failure possible. |
| SEC-05 | No network access. | No socket, urllib, or HTTP code. The game cannot leak data externally. | Safe. |
| SEC-06 | KeyboardInterrupt is caught at the top level. | `main.py` saves player state before exiting on Ctrl+C. | However, partial mission state may be saved if interrupted mid-mission. |

---

## Implicit Requirements (Not Documented but Enforced)

| ID | Implicit Requirement | How It Is Enforced |
|----|----------------------|--------------------|
| IR-01 | Every mission must have exactly 4 `story_transitions`. | `run()` accesses `tr[0]` through `tr[3]` without bounds checking beyond `if tr:`. |
| IR-02 | Every `QuizQuestion` must have exactly 4 options (A-D). | `_run_quiz()` prints all 4 options and expects input matching A/B/C/D. |
| IR-03 | The `correct` field of a quiz question must be a single uppercase letter string. | Validation checks `response.upper() == question.correct`. |
| IR-04 | `mission_id` must match the pattern `{chapter}.{index}`. | `mission_map` lookup and achievement tracking depend on this format. |
| IR-05 | `expected_commands` must be non-empty for SCAN/INFILTRATE/CONSTRUCT/REPAIR missions. | If empty, the terminal task is silently skipped. |
| IR-06 | `mtype` must be one of 7 hardcoded strings. | `mission_header()` uses a hardcoded `type_colors` dict; unknown types render without color. |
| IR-07 | `speaker` names must follow a specific set (ZARA Z3R0, RUST, PHANTOM, CIPHER, LYRA-7, EXAMINATOR, SYSTEM). | `speaker_stats` tracks these names explicitly. |
| IR-08 | `GEAR_CATALOG` IDs must match the `gear_reward` field exactly. | `add_gear()` checks `item_id in GEAR_CATALOG`. |
| IR-09 | Save files must be backward-compatible with older schema versions. | `from_dict()` uses `.get()` with defaults for every field. |
| IR-10 | Achievements are narrative-only and have no mechanical gameplay impact beyond XP rewards. | No achievement unlocks new missions, features, or content. |
