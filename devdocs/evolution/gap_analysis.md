# NeonGrid-9 Gap Analysis

**Date:** 2026-05-02
**Auditor:** Claude Code (kimi-k2.6)
**Scope:** Full codebase audit against CLAUDE.md spec and desired future state
**Lines of Code:** ~11,140 Python lines across engine + 22 mission files + main.py

---

## Executive Summary

NeonGrid-9 is a **content-complete but mechanically incomplete** project. All 501 missions, 1,117 quiz questions, 22 chapters, and the terminal simulator dictionary exist. However, the **systems layer** — the code that makes the game *work* as a cohesive experience — has significant gaps. Roughly **40% of the Player dataclass fields are dead code** (tracked but never updated), **8 of 19 achievements have no trigger logic**, gear bonuses are defined but largely not applied, and the terminal simulator architecture cannot support the multi-step missions the data model describes.

The project is at an **inflection point**: it can be incrementally patched to a solid v1.1, or it can be re-architected to support the genuinely ambitious systems described in CLAUDE.md (procedural quiz mode, faction-locked content, networked leaderboards). This document separates these paths clearly.

---

## 1. Concepts That Need Implementation

### 1.1 Achievement Triggers (8 of 19 missing)

The `ACHIEVEMENTS` dict in `engine/features.py` defines 19 achievements. Only **11 have trigger logic** in `MissionRunner._check_achievements()` (`engine/mission_engine.py:240`). The following have **zero code checking their unlock conditions**:

| Achievement | Condition | Impact |
|-------------|-----------|--------|
| `perfect_quiz` | All quiz questions correct in one mission | High — visible skill feedback |
| `speedrun` | Complete a chapter in <1 hour | High — replayability driver |
| `lore_collector` | Read all story sections in a chapter | Low — narrative completionism |
| `faction_max` | Reach 100 reputation in any faction | Low — endgame goal |
| `no_hints` | Complete a mission without using any hints | Medium — skill gate |
| `perfect_streak` | 10 consecutive correct quiz answers | Medium — engagement loop |
| `exam_mastered` | Complete all Ch22 blocks | High — endgame milestone |

**Also missing:** The existing trigger for `chapter_1_complete` is hardcoded to chapter 1 only (`engine/mission_engine.py:269`). There is no generic `chapter_N_complete` trigger for chapters 2–22. The `chapter_master` achievement fires at "5 chapters with any progress," not "5 chapters 100% complete."

### 1.2 Gear Bonus Application

Gear bonuses are fully defined in `Player.gear_bonus()` (`engine/player.py:237`) but **almost never applied**:

| Bonus Type | Defined? | Applied in MissionRunner? | Applied in Exam Mode? |
|------------|----------|---------------------------|----------------------|
| `quiz_xp` (Ghost Mask) | Yes | **No** | Referenced but not multiplied |
| `all_xp` (Linux Badge) | Yes | **No** | **No** |
| `boot_xp` (Kernel Beacon) | Yes | **No** | N/A |
| `admin_xp` (Root Keycard) | Yes | **No** | N/A |
| `pipe_xp` (Pipe Wrench) | Yes | **No** | N/A |
| `regex_xp` (Regex Scope) | Yes | **No** | N/A |
| `scan_xp` (dmesg Decoder) | Yes | **No** | N/A |
| `shell_xp` (Phantom Blade) | Yes | **No** | N/A |

The `MissionRunner.run()` method computes `total_xp = base_xp + quiz_xp` (`engine/mission_engine.py:230`) with **zero gear multiplier logic**. The only place `gear_bonus()` is called is in `timed_exam_mode()` (`main.py:1009`), where the result is printed for flavor but not used to modify scoring.

### 1.3 Dead Player Statistics

The `Player` dataclass tracks 12 statistics that are **never updated during gameplay**. They serialize to/from save files correctly, but remain at their default values forever:

| Field | Default | Written? | Read? | Used? |
|-------|---------|----------|-------|-------|
| `total_playtime` | 0 | Yes (save/load) | No | **Never incremented** |
| `chapter_completion_time` | `{}` | Yes | No | **Never recorded** |
| `boss_kill_times` | `{}` | Yes | No | **Never recorded** |
| `speaker_stats` | `{}` | Yes | No | **Never updated** |
| `secrets_found` | 0 | Yes | No | **No secret system exists** |
| `days_played` | 1 | Yes | No | **No daily tracking** |
| `streak` | 0 | Yes | No | **No daily tracking** |
| `failed_missions` | `{}` | Yes | No | Never populated on failure |
| `hints_used` | 0 | Yes | No | Never incremented |
| `missions_per_chapter` | `{}` | Yes | No | Never updated |
| `correct_first_try` | 0 | Yes | Yes (exam mode) | Incremented only in exam mode |
| `total_quizzes` | 0 | Yes | No | Never incremented |

### 1.4 Missing Level Tiers

`LEVELS` (`engine/player.py:11`) only defines tiers 1–15. CLAUDE.md explicitly promises levels 16–20 but they are **absent from code**:

```python
# Missing:
(16, "???", ???)
(17, "???", ???)
(18, "???", ???)
(19, "???", ???)
(20, "???", ???)
```

The max achievable level is 15 ("Certified Ghost" at 52,500 XP). With ~51,540 total XP available, players will hit the level cap before completing all content.

### 1.5 Gear Effects Not Wired Up

Two gear items have described effects that require engine support but **no implementation exists**:

| Gear | Described Effect | Actual Implementation |
|------|-----------------|----------------------|
| `display_lens` | "Review Mode zeigt Erklärungen vor der Antwort-Auswertung" | `review_mode()` (`main.py:1187`) shows explanations *after* wrong answers, not before. The gear is never checked. |
| `cracked_manpage` | "Gibt gelegentlich Hinweise" | `has_hint_gear()` includes it in the set, but the mission runner's forced-hint system (`engine/mission_engine.py:178`) auto-shows hints on wrong answers regardless of gear. |

### 1.6 Faction System Is Narrative-Only

The `FactionStatus` dataclass and reputation tracking exist, but:
- **No faction-locked content** (missions, gear, or story branches gated by reputation)
- **No faction narrative consequences** (dialogue doesn't change based on reputation)
- `calculate_level()` for factions has a dual-purpose design (reputation 0-100 vs XP >100) that is confusing and unused

---

## 2. Architecture Changes Required

### 2.1 Terminal Simulator Needs Abstraction Layer

**Current State:** `engine/terminal_sim.py` is a **4,457-line string dictionary** (`SIMULATED_OUTPUTS`). The `get_output()` function does exact-match, case-insensitive, prefix, and base-command matching against this flat dictionary. It returns pre-baked strings.

**Problem:** This architecture cannot support:
- Multi-step missions (e.g., "create a user, then set a password, then verify with `id`")
- Dynamic command composition (`grep error /var/log/syslog | wc -l`)
- State-dependent output (e.g., `ls` showing different files after `touch foo`)
- Chained commands or shell logic

**Required Change:** Introduce a `FakeFilesystem` class and a `CommandParser` layer:

```python
class FakeFilesystem:
    def __init__(self, initial_state: dict): ...
    def resolve(self, path: str) -> Node: ...
    def apply(self, cmd: Command) -> str: ...

class CommandParser:
    def parse(self, raw: str) -> Command | Pipeline: ...
```

**Scope:** The existing `SIMULATED_OUTPUTS` dictionary can be **migrated incrementally** — individual commands gain stateful implementations while the dictionary remains a fallback for read-only commands (`lspci`, `dmesg`, etc.).

### 2.2 Mission Data Needs Lazy Loading

**Current State:** `main.py` imports all 22 chapter files at startup (`lines 34-55`). All 501 `Mission` objects and their quiz questions are instantiated in memory immediately. This works for a CLI tool but prevents:
- Memory-efficient operation (minor concern at ~11K lines)
- Dynamic content updates (hot-reloading mission files)
- Procedurally generated content (mixing static + generated missions)

**Required Change:** Wrap chapter imports in a `ChapterRegistry` that loads on first access:

```python
class ChapterRegistry:
    def get(self, chapter_id: int) -> list[Mission]: ...
    def all(self) -> Iterator[Mission]: ...
```

**Scope:** Low-risk refactor. The `CHAPTERS` list in `main.py` becomes a registry query.

### 2.3 XP and Reward Calculation Needs a Pipeline

**Current State:** XP calculation is inline in `MissionRunner.run()` (`engine/mission_engine.py:230`):

```python
total_xp = base_xp + quiz_xp
```

Gear bonuses, hint penalties, and faction rewards are scattered across the method.

**Required Change:** A `RewardPipeline` dataclass that composes modifiers:

```python
@dataclass
class RewardPipeline:
    base_xp: int
    quiz_bonus: int = 0
    gear_multipliers: list[float] = field(default_factory=list)
    hint_penalty: int = 0
    
    def compute(self, player: Player) -> int: ...
```

**Scope:** Refactor within `mission_engine.py`. No external API changes.

### 2.4 Player Statistics Need Lifecycle Hooks

**Current State:** `Player` is a passive data container. Gameplay code must manually remember to update fields.

**Required Change:** Emit events from `MissionRunner` and have `Player` subscribe:

```python
class MissionEvent(Enum):
    STARTED = auto()
    COMMAND_ATTEMPTED = auto()
    HINT_USED = auto()
    QUIZ_ANSWERED = auto()
    COMPLETED = auto()
    FAILED = auto()
```

Or, simpler: a `Player.record_mission_complete(mission, metadata)` method that updates all derived statistics atomically.

**Scope:** Medium refactor. Requires adding call sites in `MissionRunner`.

---

## 3. Technical Debt Blocking Progress

### 3.1 The "Forced Hint" Anti-Pattern

`MissionRunner.run()` (`engine/mission_engine.py:178`) **automatically deducts XP and shows hints** when the player enters a wrong command. There is no player choice. This breaks the game's own design (3-tier hint system with costs) and makes the `no_hints` achievement impossible to implement meaningfully.

**Blocker severity:** High. Any meaningful skill assessment or hint economy requires player-initiated hint requests.

### 3.2 Quiz Correct Field Type Confusion

`QuizQuestion.correct` is typed as `str` ("A", "B", "C", "D"). However, `timed_exam_mode()` (`main.py:1076`) contains a type check:

```python
correct_letter = letters[q.correct] if isinstance(q.correct, int) else q.correct
```

This implies some questions use `int` (0-3). The data model allows this inconsistency, and `review_mode()` (`main.py:1238`) duplicates the same defensive check. This is a **data integrity hazard** — a single malformed question breaks the exam.

**Blocker severity:** Medium. Requires a data migration/validation pass across all 1,117 questions.

### 3.3 Terminal Simulator Cannot Fail Missions

`run_terminal()` (`engine/terminal_sim.py:4392`) returns `(success, attempts, cmd)` but `MissionRunner` ignores the `attempts` count for scoring. A player who uses 5 attempts gets the same XP as someone who nails it on the first try. The `expected_commands` matching is also extremely permissive — `cmd_base == exp_base` with `len(expected) == 1` passes any flags/arguments.

**Blocker severity:** Medium. Undermines the skill component of terminal missions.

### 3.4 No Test Coverage

There are **zero automated tests**. No unit tests for `MissionRunner`, `Player.add_xp()`, `get_output()`, save/load round-trips, or achievement triggers. This means:
- Refactoring the terminal simulator is high-risk
- Adding new achievements requires manual playthrough verification
- Save format changes risk data loss

**Blocker severity:** High for refactoring, Medium for content additions.

### 3.5 Hardcoded Chapter-Specific Logic

`main.py` has multiple chapters with special-cased behavior:
- `chapter_menu()` has `if ch_id == 18: extra = ... exam mode` (`main.py:550`)
- `_show_chapter_complete()` has a `recap_map` dictionary with hardcoded recaps for chapters 1–18, but **chapters 19, 20, 21 are missing** (`main.py:616-799`)
- The `CHAPTERS` list itself is a hardcoded tuple list

**Blocker severity:** Low for v1.1, Medium for scaling beyond 22 chapters.

### 3.6 Achievement Trigger Logic Is Inline and Fragile

`_check_achievements()` (`engine/mission_engine.py:240`) is a 70-line method with nested if-statements. Adding a new achievement requires editing this method. The `chapter_1_complete` check is literally `if mission.chapter == 1 and len(chapter_missions) >= 31` — extending this to 22 chapters means 22 more hardcoded lines.

**Blocker severity:** Medium. Prevents rapid iteration on achievement design.

---

## 4. What Can Be Incrementally Improved

### 4.1 Achievement System (Can Be Patched)

**Effort:** 1–2 days
**Approach:** Add the missing trigger checks to `_check_achievements()` and generalize the chapter completion check:

```python
# Replace 22 hardcoded checks with:
for ch_id, ch_missions, *_ in CHAPTERS:
    needed = len(ch_missions)
    have = len([m for m in self.player.completed_missions if m.startswith(f"{ch_id}.")])
    if have >= needed:
        ach = self.player.achievements.unlock(f'chapter_{ch_id}_complete')
```

Also add tracking for:
- `perfect_quiz`: track correct count during quiz loop
- `no_hints`: track `hints_used` in mission metadata
- `speedrun`: record `chapter_completion_time` (requires fixing the dead field first)

### 4.2 Gear Bonus Wiring (Can Be Patched)

**Effort:** Half a day
**Approach:** Modify `MissionRunner.run()` to call `self.player.gear_bonus()` based on mission type:

```python
# Map mtype to gear bonus key
bonus_key = {
    "SCAN": "scan_xp", "QUIZ": "quiz_xp", "INFILTRATE": "admin_xp",
    # ... etc
}.get(mission.mtype)

if bonus_key:
    mult = self.player.gear_bonus(bonus_key)
    total_xp = int(total_xp * mult)
```

### 4.3 Player Statistics (Can Be Patched)

**Effort:** 1 day
**Approach:** Add update calls at key lifecycle points:
- `total_playtime`: increment in `game_hub()` loop
- `chapter_completion_time`: set when chapter completes
- `boss_kill_times`: set when boss mission completes
- `speaker_stats`: increment when story is shown
- `hints_used`: increment when hint is consumed
- `missions_per_chapter`: increment on mission complete
- `failed_missions`: populate when `run_terminal()` returns `success=False`

### 4.4 Terminal Simulator Dictionary (Can Be Extended)

**Effort:** Ongoing
**Approach:** The `SIMULATED_OUTPUTS` dictionary works for read-only commands. New commands can be added by appending entries. The architecture doesn't *block* content creation — it just can't do stateful simulation. For v1.1, this is acceptable.

### 4.5 Review Mode Enhancement (Can Be Patched)

**Effort:** Half a day
**Approach:** Check for `display_lens` in inventory and show the explanation *before* revealing the correct answer in `review_mode()`.

### 4.6 Save System Migration (Can Be Patched)

**Effort:** Half a day
**Approach:** The `Player.from_dict()` method already handles missing fields gracefully (fills defaults). Adding new fields is backward-compatible. A `save_version` field should be added to the JSON for future migrations.

---

## 5. What Requires Complete Rewrite

### 5.1 Terminal Simulator (Stateful REPL)

**Why rewrite:** The current dictionary approach cannot be incrementally evolved into a real shell simulator. Adding `FakeFilesystem` + `CommandParser` requires replacing the core of `terminal_sim.py`.

**What to keep:** The `SIMULATED_OUTPUTS` strings become the "static command" registry. Commands like `lspci`, `dmesg`, `uname` stay as dictionary lookups. Commands like `ls`, `touch`, `mkdir`, `rm`, `cat` get stateful implementations.

**Effort estimate:** 3–5 days for a basic filesystem state model.

### 5.2 Mission Content Format

**Why rewrite:** Missions are pure Python dataclass instantiations in 22 separate `.py` files. This means:
- Content creators must know Python
- No validation at edit-time (typos in `correct="A"` only surface at runtime)
- No tooling possible (no mission editor, no automated content audit)
- Import-time overhead (all 22 files loaded at startup)

**What to rewrite to:** JSON or YAML mission definitions loaded by a `MissionLoader` class. The `Mission` dataclass becomes a runtime representation, not an authoring format.

**Effort estimate:** 2–3 days for JSON loader + validator + migration script.

### 5.3 Main Menu / Game Hub Architecture

**Why rewrite:** `game_hub()` (`main.py:395`) is a 120-line `if/elif` cascade with 22 explicit chapter branches (`choice == "1"` through `choice == "22"`). Adding chapter 23 means adding another `elif`. The `chapter_menu()` function duplicates logic for every chapter.

**What to rewrite to:** A `MenuSystem` class with registered handlers:

```python
class MenuSystem:
    def register(self, key: str, handler: Callable): ...
    def run(self, prompt: str): ...
```

**Effort estimate:** 1–2 days.

### 5.4 Display System (For GUI/Web Migration)

**Why rewrite:** `engine/display.py` is tightly coupled to ANSI escape codes and `sys.stdout`. Every function calls `print()` directly. Migrating to a web UI, TUI (curses), or desktop app requires rewriting every display function.

**What to rewrite to:** A `Renderer` protocol:

```python
class Renderer(Protocol):
    def clear(self): ...
    def text(self, text: str, color: str = "white"): ...
    def box(self, title: str, content: str): ...
```

**Effort estimate:** 2–3 days for protocol + ANSI implementation. Future renderers (HTML, TUI) implement the same protocol.

---

## 6. Prioritized Roadmap

### Phase 1: Fix the Game (v1.1) — 1 week
1. **Achievement triggers** — implement missing 8 + generalize chapter completion
2. **Gear bonuses** — wire up `gear_bonus()` in `MissionRunner`
3. **Player statistics** — bring dead fields to life
4. **Hint system fix** — replace forced hints with player-requested hints
5. **Quiz field validation** — enforce `str` type, audit all 1,117 questions

### Phase 2: Harden the Engine (v1.2) — 1 week
1. **Unit tests** — pytest suite for `Player`, `MissionRunner`, `get_output()`, save/load
2. **Save versioning** — add `save_version` field, migration framework
3. **RewardPipeline** — refactor XP calculation into composable pipeline
4. **MenuSystem refactor** — eliminate 22 hardcoded chapter branches

### Phase 3: Expand the World (v1.5) — 2–3 weeks
1. **Stateful terminal simulator** — `FakeFilesystem` + `CommandParser`
2. **JSON mission format** — migrate from Python authoring to data-driven
3. **Renderer protocol** — decouple display from ANSI stdout
4. **Faction-locked content** — missions and gear gated by reputation

---

## 7. Files by Risk Level

| File | Lines | Risk Level | Reason |
|------|-------|------------|--------|
| `engine/terminal_sim.py` | 4,457 | **High** | Single flat dictionary, no tests, core gameplay dependency |
| `engine/mission_engine.py` | 514 | **High** | Inline achievement logic, fragile hint system, no gear bonus application |
| `main.py` | 1,374 | **Medium** | Hardcoded chapter branches, exam mode tightly coupled to ch22 |
| `engine/player.py` | 392 | **Medium** | Dead fields, missing levels 16–20 |
| `engine/display.py` | 324 | **Low** | Stable, but tightly coupled to ANSI |
| `engine/features.py` | 276 | **Low** | Achievement definitions complete, trigger logic missing |
| `engine/save_system.py` | 72 | **Low** | Simple JSON, backward-compatible |
| `missions/ch*.py` (×22) | ~7,800 total | **Low** | Content is stable, but format is not scalable |

---

## 8. Conclusion

NeonGrid-9 is a **content-rich prototype** wearing a production label. The game is playable and complete in terms of narrative and educational material, but the systems that make it a *game* — progression feedback, achievement satisfaction, skill assessment, and replayability — are partially unimplemented.

The good news: **none of these gaps require architectural demolition**. The project can reach a genuinely solid v1.1 with ~1 week of focused systems work. The longer-term rewrites (stateful terminal, JSON mission format, renderer protocol) are desirable for scaling but not blocking a polished release.

**Recommended immediate action:** Implement Phase 1 items. The forced-hint system and missing achievement triggers are the highest-leverage fixes for player experience.
