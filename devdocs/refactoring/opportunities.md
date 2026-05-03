# Refactoring Opportunities in NeonGrid-9

This document catalogs concrete refactoring opportunities across the codebase.
Each entry maps a detected smell to a recommended structural improvement,
with exact file paths and line ranges.

---

## 1. Repeated Code Blocks with Slight Variations
**Pattern:** Identical or near-identical blocks copied across files/functions.
**Target:** Extract into reusable functions, classes, or data-driven loops.

### 1.1 Chapter-Menu Dispatch Wall
**Where:** `main.py:451-494`
**Smell:** 22 sequential `elif` branches, each calling `chapter_menu(n)`.
```python
if choice == "1":
    chapter_menu(1)
elif choice == "2":
    chapter_menu(2)
# ... through 22
```
**Refactor:** Replace with a dictionary dispatch or direct cast:
```python
if choice.isdigit() and 1 <= (n := int(choice)) <= 22:
    chapter_menu(n)
```

### 1.2 Smoke-Test Helper Duplication
**Where:** Every smoke-test file (`test_01_initialization.py`,
`test_02_player_system.py`, `test_03_mission_engine.py`,
`test_05_display_and_features.py`)
**Smell:** The four helpers `banner`, `ok`, `fail`, `info` (and sometimes `warn`)
are copy-pasted verbatim into each file. Any formatting change requires
editing 5+ files.
**Refactor:** Create `smoke_tests/_helpers.py` and import from it.

### 1.3 Chapter Recap Dictionary
**Where:** `main.py:616-873`
**Smell:** `recap_map` contains 22 hand-written lists of recap strings.
Each list follows the identical pattern: a list of 6-12 command/concept strings.
**Refactor:** Move recap data to a lightweight YAML/JSON file or a dedicated
`data/recaps.py` module. The presentation logic (`_show_chapter_complete`)
should iterate over the loaded list rather than own the data.

### 1.4 Quiz Answer Resolution
**Where:** `engine/mission_engine.py:374`, `main.py:1076`, `main.py:1238`,
`review_mode()`
**Smell:** The snippet `letters[q.correct] if isinstance(q.correct, int) else q.correct`
(and its inverse) is repeated in at least four places.
**Refactor:** Add a property or method on `QuizQuestion`:
```python
@property
def correct_letter(self) -> str:
    return letters[self.correct] if isinstance(self.correct, int) else self.correct
```

---

## 2. Long Parameter Lists
**Pattern:** Functions or constructors that accept many positional/named arguments.
**Target:** Collapse related arguments into configuration objects or context structs.

### 2.1 Mission Dataclass — 30+ Fields
**Where:** `engine/mission_engine.py:32-72`
**Smell:** `Mission` carries every conceivable attribute (story, speaker,
syntax, example, task_description, expected_commands, hints, quiz_questions,
exam_tip, memory_tip, gear_reward, faction_reward, boss_name, boss_desc, …).
Instantiations in all 22 chapter files are extremely long.
**Refactor:** Split into cohesive sub-structures:
```python
@dataclass
class Narrative:
    story: str
    speaker: str
    transitions: List[str]
    ascii_art: str

@dataclass
class Pedagogy:
    why_important: str
    explanation: str
    syntax: str
    example: str
    exam_tip: str
    memory_tip: str

@dataclass
class Mission:
    mission_id: str
    title: str
    mtype: str
    xp: int
    chapter: int
    narrative: Narrative
    pedagogy: Pedagogy
    task: Task          # task_description, expected_commands, hints
    quiz: List[QuizQuestion]
    rewards: Rewards    # gear_reward, faction_reward
```

### 2.2 Player to_dict / from_dict Field Lists
**Where:** `engine/player.py:327-377`
**Smell:** 20+ lines of explicit field serialization/deserialization.
Any new field requires touching both methods.
**Refactor:** Use `dataclasses.asdict()` and `__init__(**d)` with a small
allow-list or `__post_init__` for computed fields (`achievements` is a
dataclass, not a primitive, so it needs special handling either way).

### 2.3 `run_terminal()` Parameter List
**Where:** `engine/terminal_sim.py` (function signature not shown in excerpt,
but call sites at `mission_engine.py:195-200` pass 5+ arguments)
**Smell:** `run_terminal(expected=..., task_description=..., hint_available=...,
hint_text=..., max_attempts=...)`
**Refactor:** Introduce a `TerminalTask` dataclass that groups the task context.

---

## 3. Multiple If/Else Checking the Same Condition
**Pattern:** Dispatch logic scattered across `if/elif` chains on a single discriminator.
**Target:** Strategy pattern, polymorphism, or dictionary-based dispatch.

### 3.1 Mission-Type Dispatch in MissionRunner
**Where:** `engine/mission_engine.py:82-88`, `131-206`, `410-497`
**Smell:** `run()` checks `mission.mtype == "BOSS"` for special handling.
Inside the main flow, terminal-task logic is gated on
`mission.mtype in ["SCAN", "INFILTRATE", "CONSTRUCT", "REPAIR"]`.
Boss handling is essentially a second, parallel runner.
**Refactor:** Define a `MissionPhase` protocol or base class:
```python
class Phase(Protocol):
    def execute(self, mission: Mission, player: Player) -> PhaseResult: ...

class ScanPhase(Phase): ...
class BossPhase(Phase): ...

PHASES: dict[str, Phase] = {
    "SCAN": ScanPhase(),
    "BOSS": BossPhase(),
    # ...
}
```

### 3.2 Gear-Boost Lookup Chain
**Where:** `engine/player.py:237-258`
**Smell:** Large `if/elif` chain on `boost_type`, plus manual inventory checks.
**Refactor:** The `bonuses` dict already exists — move the *entire* lookup
into the dict and replace the chain with a single lookup + linux_badge fallback.

### 3.3 Exam Result Rendering Fork
**Where:** `main.py:1119-1137`
**Smell:** Two massive ASCII-art strings selected by `if passed:`.
**Refactor:** Store the art in a `ResultArt` dataclass keyed by pass/fail:
```python
EXAM_ART = {
    True:  ResultArt(color=C.SUCCESS, art="..."),
    False: ResultArt(color=C.DANGER, art="..."),
}
```

### 3.4 Achievement Trigger Wall
**Where:** `engine/mission_engine.py:240-313`
**Smell:** ~15 sequential `if` blocks, each unlocking an achievement.
**Refactor:** The worktree already contains `engine/achievement_engine.py`
with `AchievementEngine` and `AchievementRule`. Adopt it: replace the inline
triggers with a declarative rule engine that iterates over a list of rules.

---

## 4. Data and Functions Always Traveling Together
**Pattern:** A data structure and the functions that operate on it live in
separate places or are passed together repeatedly.
**Target:** Co-locate into a class or dedicated module.

### 4.1 Gear Catalog + Rarity Colors + Bonus Logic
**Where:** `engine/player.py:30-141` (data), `237-258` (logic)
**Smell:** `GEAR_CATALOG`, `RARITY_COLOR`, and `gear_bonus()` are tightly
coupled but live inside `Player`. A gear item’s color and rarity are
properties of the gear, not the player.
**Refactor:** `GearItem` dataclass + `GearRegistry` module:
```python
@dataclass
class GearItem:
    id: str
    name: str
    desc: str
    rarity: str
    tier: int
    boost: str
    color: str  # moved from RARITY_COLOR
    bonus_multiplier: float = 1.0
```

### 4.2 Hint Levels, Prompts, and Colors
**Where:** `engine/features.py:12-41` (HintRequest), `266-276` (prompts/colors)
**Smell:** `HINT_PROMPTS` and `HINT_COLORS` are global dicts that belong
semantically to `HintLevel` / `HintRequest` but are orphaned at module level.
**Refactor:** Make them class attributes or `@property` methods on `HintLevel`.

### 4.3 Achievement Definitions + Tracker
**Where:** `engine/features.py:59-202` (ACHIEVEMENTS dict), `205-227` (Tracker)
**Smell:** `ACHIEVEMENTS` is a module-level dict; `AchievementTracker` is a
separate dataclass. They are never used independently.
**Refactor:** `AchievementTracker` should own the catalog, or both should
live in a dedicated `engine/achievements.py` module (the worktree’s
`achievement_engine.py` is a step in this direction).

---

## 5. Comments Explaining What (Not Why)
**Pattern:** Comments restate the obvious operation of the following line(s).
**Target:** Delete or replace with self-documenting names.

### 5.1 Inline Section Comments in MissionRunner
**Where:** `engine/mission_engine.py:95-136`
**Examples:**
```python
# 0. ASCII Art
# 1. Story-Einstieg
# 2. Warum wichtig
# 3. Erklärung
# 4. Syntax
# 5. Beispiel
# 6. Interaktive Aufgabe (Terminal)
```
These are section headers, but they indicate the function is doing too much.
**Refactor:** Extract each numbered block into a named method
(`_show_ascii_art()`, `_show_story()`, `_show_explanation()`, etc.).
The method name replaces the comment.

### 5.2 Module Header Comments
**Where:** `engine/save_system.py:1-4`, `engine/terminal_sim.py:1-5`
**Examples:**
```python
"""
NeonGrid-9 :: Save System
JSON-basierte Speicherstände mit 3 Slots
"""
```
The module path and docstring already communicate this.
**Refactor:** Keep the one-line docstring; remove the redundant subtitle.

### 5.3 Trivial Inline Comments
**Where:** `engine/player.py:193-201`
**Example:**
```python
# Level-basierter Skalierungsbonus
if self.level >= 15:
    scale = 1.3
elif self.level >= 10:
    scale = 1.2
# ...
```
The comment says exactly what the code says.
**Refactor:** Rename `scale` to `level_scaling_bonus` and delete the comment.

---

## 6. Test Setup Code Duplicated Across Files
**Pattern:** Every test file repeats the same bootstrap and helper code.
**Target:** Shared fixtures/utilities module.

### 6.1 Path Injection + Helpers
**Where:** All smoke-test files
**Smell:** Each file begins with:
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def banner(msg): ...
def ok(msg): ...
def fail(msg, exc=None): ...
def info(msg): ...
```
**Refactor:** Create `smoke_tests/conftest.py` or `smoke_tests/_helpers.py`:
```python
# _helpers.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def banner(msg): ...
def ok(msg): ...
# etc.
```
Each test file then begins with a single import:
```python
from _helpers import banner, ok, fail, info
```

### 6.2 Common Test Player Factory
**Where:** `test_02_player_system.py:56`, `test_03_mission_engine.py:222`
**Smell:** Every test manually instantiates `Player(name="...")` and often
repeats the same mutations (add XP, complete missions, add gear).
**Refactor:** Add a factory in `_helpers.py`:
```python
def make_test_player(name="TestGhost", xp=0, level=1, missions=None, gear=None):
    p = Player(name=name)
    if xp:
        p.add_xp(xp)
    for m in missions or []:
        p.complete_mission(m)
    for g in gear or []:
        p.add_gear(g)
    return p
```

---

## Priority Matrix

| # | Opportunity | Blast Radius | Effort | Payoff |
|---|-------------|--------------|--------|--------|
| 1 | Chapter dispatch loop (`main.py:451-494`) | Low | 5 min | High |
| 2 | Smoke-test helpers extraction | Low | 10 min | High |
| 3 | `QuizQuestion.correct_letter` property | Low | 5 min | Medium |
| 4 | Gear catalog + rarity + bonus co-location | Medium | 30 min | Medium |
| 5 | Achievement trigger wall → rule engine | Medium | 1 h | High |
| 6 | Mission dataclass decomposition | High | 2 h | Medium |
| 7 | Player serialization via `asdict` | Low | 15 min | Medium |
| 8 | `MissionRunner.run()` phase extraction | Medium | 1 h | High |

---

## How to Use This Document

1. Pick an item from the Priority Matrix.
2. Open the referenced file and line range.
3. Apply the recommended refactor.
4. Run the smoke tests to verify no regressions:
   ```bash
   python3 smoke_tests/check_what_is_working/test_01_initialization.py
   python3 smoke_tests/check_what_is_working/test_02_player_system.py
   python3 smoke_tests/check_what_is_working/test_03_mission_engine.py
   python3 smoke_tests/check_what_is_working/test_04_terminal_simulator.py
   python3 smoke_tests/check_what_is_working/test_05_display_and_features.py
   ```
