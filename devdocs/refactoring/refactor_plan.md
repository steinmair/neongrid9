# Refactoring Plan for NeonGrid-9

A step-by-step, reversible refactoring roadmap based on the patterns
documented in `opportunities.md`, `emerging_patterns.md`, `code_smells.md`,
and `current_state.md`.

**Principle:** Never refactor and change behavior in the same commit.
Each phase ends with a validation gate: all probe tests must pass.

---

## Phase 1: Preparation

### 1.1 Add tests for current behavior

**Status:** ✅ Done.
- `probe_tests/pre_refactor/test_current_behavior.py` — 37 tests
- `probe_tests/pre_refactor/test_edge_cases.py` — 33 tests
- `probe_tests/pre_refactor/test_integration_points.py` — 24 tests

**Validation gate:**
```bash
python3 probe_tests/pre_refactor/test_current_behavior.py
python3 probe_tests/pre_refactor/test_edge_cases.py
python3 probe_tests/pre_refactor/test_integration_points.py
```

### 1.2 Create feature flags for gradual rollout

Create `engine/config.py`:

```python
"""Feature flags for gradual refactoring rollout."""

FEATURE_FLAGS = {
    # Phase 2 — Extraction helpers (safe, low risk)
    "USE_BADGE_HELPER": False,
    "USE_SCREEN_HELPER": False,
    "USE_MENU_ITEM_HELPER": False,
    "USE_FMT_MM_SS": False,
    "USE_QUIZ_CORRECT_LETTER": False,
    "USE_TRANSITION_GUARD": False,
    "USE_XP_BAR_ARGS": False,

    # Phase 3 — Abstractions (medium risk)
    "USE_RENDERER_PROTOCOL": False,
    "USE_ACHIEVEMENT_TRY_UNLOCK": False,
    "USE_PHASE_DISPATCH": False,
    "USE_TERMINAL_TASK_DATACLASS": False,

    # Phase 4 — Dispatch & structural changes (higher risk)
    "USE_CHAPTER_INT_DISPATCH": False,
    "USE_ACTION_DICT_DISPATCH": False,
    "USE_MISSION_TYPE_ENUM": False,
}


def is_enabled(flag: str) -> bool:
    return FEATURE_FLAGS.get(flag, False)
```

**Why:** Each new abstraction is toggled off by default. Old code paths remain
active until the new path is proven correct.

### 1.3 Set up parallel implementations

Create stub files that will receive new implementations while old code stays
untouched:

| File | Purpose |
|------|---------|
| `engine/config.py` | Feature flags (new) |
| `engine/constants.py` | Magic numbers extracted from `mission_engine.py`, `player.py`, `main.py` |
| `engine/_refactor_helpers.py` | Pure helper functions extracted from `display.py`, `main.py`, `mission_engine.py` |
| `engine/renderer.py` | `Renderer` Protocol + `TerminalRenderer` (new) |

**Rule:** Files prefixed with `_` during Phase 2-4 indicate they are parallel
implementations. They are promoted to public names only in Phase 5.

**Validation gate:** All probe tests pass after adding empty/new files.

---

## Phase 2: Extract (Don't Change)

**Goal:** Break apart long functions and repeated code blocks into standalone
helpers. Zero logic changes — only code movement.

### 2.1 Extract Badge Message Trio

**Where:** `engine/display.py:169-187`

```python
def _show_badge(color: str, symbol: str, text: str):
    print()
    print(color + f"  {symbol}  {text}" + color + f"  {symbol}" + C.RESET)
    print()
```

Wrap existing functions:
```python
def show_warn(text):
    if is_enabled("USE_BADGE_HELPER"):
        _show_badge(C.WARN, "⚠", text)
    else:
        print()
        print(C.WARN + f"  ⚠  {text}" + C.WARN + "  ⚠" + C.RESET)
        print()
```

**Impact:** 1 file. Risk: low.

### 2.2 Extract Screen Clear + Colored Header

**Where:** `main.py` (20 occurrences)

```python
def _screen(title: str, color: str = C.NEON):
    clear()
    print(color + f"\n  {title}\n" + C.RESET)
```

Replace each `clear()` + `print(C.NEON + "\n TITLE\n" + C.RESET)` pair with a
call to `_screen()`, gated behind `USE_SCREEN_HELPER`.

**Impact:** 1 file (`main.py`). Risk: low — mechanical replacement.

### 2.3 Extract Menu Item Print Lines

**Where:** `main.py` (28 occurrences in menu functions)

```python
def _menu_item(key: str, label: str, key_color: str = C.CYAN, label_color: str = C.RESET):
    print(key_color + f"  [{key}]" + C.RESET + label_color + f"  {label}" + C.RESET)
```

**Impact:** 1 file. Risk: low.

### 2.4 Extract Achievement Unlock Block

**Where:** `engine/mission_engine.py:243-310` (10 copies of unlock + append + add_xp)

```python
def _try_unlock(player, achievement_id: str, unlocked: list) -> None:
    ach = player.achievements.unlock(achievement_id)
    if ach:
        unlocked.append(ach)
        player.add_xp(ach.xp_reward)
```

Replace each inline block with `_try_unlock(self.player, 'first_mission', unlocked)`,
gated behind `USE_ACHIEVEMENT_TRY_UNLOCK`.

**Impact:** 1 file. Risk: low.

### 2.5 Extract Safe-Index Transition Guard

**Where:** `engine/mission_engine.py:102,109,115,121`

```python
def _maybe_transition(transitions: list, index: int) -> None:
    if transitions and index < len(transitions):
        show_transition(transitions[index])
```

**Impact:** 1 file. Risk: low.

### 2.6 Extract Time Formatting (MM:SS)

**Where:** `engine/mission_engine.py:357-358`, `main.py:1050-1051`, `main.py:1100`

```python
def _fmt_mm_ss(seconds: int) -> str:
    mm, ss = divmod(seconds, 60)
    return f"{mm:02d}:{ss:02d}"
```

**Impact:** 2 files. Risk: low.

### 2.7 Extract Quiz Correct-Letter Resolution

**Where:** `engine/mission_engine.py:374`, `main.py:1076`, `main.py:1238`

Add property to `QuizQuestion`:
```python
@property
def correct_letter(self) -> str:
    letters = ["A", "B", "C", "D"]
    return letters[self.correct] if isinstance(self.correct, int) else self.correct
```

Keep old inline resolution as fallback when `USE_QUIZ_CORRECT_LETTER` is off.

**Impact:** 3 files (engine + future consumers). Risk: low.

### 2.8 Extract XP Bar Coordinate Pair

**Where:** `main.py:404-407`, `engine/mission_engine.py:235-237`, `476-478`

```python
# engine/player.py
def xp_bar_args(self) -> tuple[int, int, int, int]:
    return (self.xp, self.level, self.get_current_level_xp(), self.get_next_level_xp())
```

**Impact:** 2 files. Risk: low.

### 2.9 Extract Sequential Function Pairs

**Where:** `engine/mission_engine.py`

```python
def _show_xp_progress(player, amount: int):
    show_xp_gain(amount)
    xp_bar(*player.xp_bar_args())

def _auto_save(runner):
    if runner.save_callback:
        runner.save_callback(runner.player)

def _show_correct_answer(earned_xp: int, explanation: str):
    show_success(f"RICHTIG! +{earned_xp} XP")
    print(C.CYAN + f"  → {explanation}" + C.RESET)
```

**Impact:** 1 file. Risk: low.

### 2.10 Extract Magic Numbers to Constants

Create `engine/constants.py`:

```python
BOSS_COUNT_TOTAL = 22
CHAPTER_1_MISSION_COUNT = 31
MARATHON_MISSION_THRESHOLD = 100
CHAPTER_MASTERY_THRESHOLD = 5
SPEEDRUN_FAST_SECONDS = 300
SPEEDRUN_SLOW_SECONDS = 900
EXAM_TIME_LIMIT_SECONDS = 5400
EXAM_SCORE_EXCELLENT = 800
EXAM_SCORE_PASS = 500

XP_SCALE_LOW = 1.0      # level < 5
XP_SCALE_MID = 1.1      # level 5-9
XP_SCALE_HIGH = 1.2     # level 10-14
XP_SCALE_MAX = 1.3      # level 15+

FIRST_ATTEMPT_BONUS = 1.2
FAILURE_PENALTY_DIVISOR = 3
```

Replace literals in `mission_engine.py`, `player.py`, `main.py` with imports.
Do NOT change values — only replace literals with named constants.

**Impact:** 3 files. Risk: low.

### 2.11 Extract Smoke-Test Helpers

Create `smoke_tests/_helpers.py` with:
- `sys.path.insert(...)` bootstrap
- `banner()`, `ok()`, `fail()`, `info()`, `warn()`
- `make_test_player(name=..., xp=..., level=..., missions=..., gear=...)`

Update all 5 smoke-test files to import from `_helpers.py`.

**Impact:** 5 files. Risk: low.

### Phase 2 Validation Gate

- [ ] All probe tests pass.
- [ ] Smoke tests pass.
- [ ] No behavioral changes observed (play one mission manually).
- [ ] Feature flags are all `False` in committed code.

---

## Phase 3: Abstract (Don't Break)

**Goal:** Introduce new abstractions and route calls through them, but keep
old paths available behind feature flags.

### 3.1 Introduce Renderer Protocol

Create `engine/renderer.py`:

```python
from typing import Protocol

class Renderer(Protocol):
    def show_success(self, text: str) -> None: ...
    def show_warn(self, text: str) -> None: ...
    def show_error(self, text: str) -> None: ...
    def show_info(self, text: str) -> None: ...
    def show_story(self, speaker: str, text: str) -> None: ...
    def show_transition(self, text: str) -> None: ...
    def prompt_continue(self) -> None: ...
    def prompt_input(self, label: str) -> str: ...
    def clear(self) -> None: ...
    def mission_header(self, mission_id, title, xp, mtype) -> None: ...
    def xp_bar(self, *args) -> None: ...
    def show_xp_gain(self, amount: int) -> None: ...
    def level_up_screen(self, level: int, title: str) -> None: ...
    def show_achievements(self, achievements: list) -> None: ...
    def show_hint(self, text: str, level: int, xp_cost: int) -> None: ...

class TerminalRenderer:
    """Default implementation — delegates to engine.display functions."""
    def show_success(self, text: str) -> None:
        from engine.display import show_success
        show_success(text)
    # ... etc
```

Modify `MissionRunner.__init__` to accept an optional renderer:
```python
def __init__(self, player: Player, save_callback=None, renderer: Renderer = None):
    self.player = player
    self.save_callback = save_callback
    self.renderer = renderer or TerminalRenderer()
```

**Gating:** Only use `self.renderer` when `USE_RENDERER_PROTOCOL` is enabled.
Otherwise, keep direct function calls.

**Impact:** 2-3 files. Risk: medium — touches all display paths in `MissionRunner`.

### 3.2 Introduce TerminalTask Dataclass

**Where:** `engine/mission_engine.py:133`, `195-200`, `436-441`

```python
from dataclasses import dataclass
from typing import List

@dataclass
class TerminalTask:
    expected_commands: List[str]
    task_description: str
    hints: List[str]
    hint_text: str = ""
    max_attempts: int = 5
```

Update `run_terminal()` signature to accept `TerminalTask`, while keeping an
overloaded path that accepts the old positional args when the flag is off.

**Impact:** 2 files (`mission_engine.py`, `terminal_sim.py`). Risk: medium.

### 3.3 Introduce Phase Dispatch in MissionRunner

**Where:** `engine/mission_engine.py:96-127`

Replace the sequential `if mission.ascii_art: ...` cascade with a phase list:

```python
_PHASES = [
    ("ascii",    lambda m: m.ascii_art,    lambda m, r: r.show_ascii_art(m.ascii_art)),
    ("story",    lambda m: m.story,        lambda m, r: _show_story_and_wait(r, m)),
    ("why",      lambda m: m.why_important, lambda m, r: _show_why(r, m)),
    ("explain",  lambda m: m.explanation,  lambda m, r: _show_explanation(r, m)),
    ("syntax",   lambda m: m.syntax,       lambda m, r: r.show_code(m.syntax)),
    ("example",  lambda m: m.example,      lambda m, r: r.show_code(m.example)),
]
```

**Gating:** Use `_PHASES` loop only when `USE_PHASE_DISPATCH` is enabled.

**Impact:** 1 file. Risk: medium — restructures the core mission flow.

### 3.4 Extract Menu Dispatch to Dictionary

**Where:** `main.py:451-512` (`game_hub()`)

```python
_CHAPTER_DISPATCH = {str(i): lambda i=i: chapter_menu(i) for i in range(1, 23)}
_ACTION_DISPATCH = {
    ("s", "status"):           show_player_status,
    ("i", "inv", "inventar"): show_inventory,
    ("r", "readiness", "report"): show_linux_readiness,
    ("x", "review"):          review_mode,
    ("e", "exam"):            timed_exam_mode,
    ("v", "save", "speichern"): lambda: (_save_and_notify(), None)[1],
    ("q", "quit", "exit"):    _quit_game,
}
```

**Gating:** Use dict dispatch when `USE_ACTION_DICT_DISPATCH` and
`USE_CHAPTER_INT_DISPATCH` are enabled.

**Impact:** 1 file. Risk: low.

### 3.5 Introduce Unified Error Handling

Create `engine/errors.py`:

```python
class NeonGridError(Exception):
    """Base exception for all game errors."""
    pass

class SaveError(NeonGridError):
    pass

class ValidationError(NeonGridError):
    pass
```

Wrap `save_game()` to raise `SaveError` instead of printing. Keep old behavior
as fallback.

**Impact:** 2-3 files. Risk: medium.

### Phase 3 Validation Gate

- [ ] All probe tests pass.
- [ ] Smoke tests pass.
- [ ] Feature flags can be toggled individually without test failures.
- [ ] Manual playthrough of one chapter completes without visual regressions.

---

## Phase 4: Migrate (Gradual Switch)

**Goal:** Switch from old code paths to new abstractions one feature at a time.
Each switch is a separate commit so it can be reverted independently.

### 4.1 Switch Menu Helpers (Low Risk)

Enable flags one by one:
1. `USE_BADGE_HELPER = True` — run tests, commit.
2. `USE_SCREEN_HELPER = True` — run tests, commit.
3. `USE_MENU_ITEM_HELPER = True` — run tests, commit.
4. `USE_FMT_MM_SS = True` — run tests, commit.
5. `USE_TRANSITION_GUARD = True` — run tests, commit.

**Monitor:** If any test fails or manual play shows visual difference,
immediately revert the last flag change.

### 4.2 Switch Quiz Correct-Letter Property

Enable `USE_QUIZ_CORRECT_LETTER = True`.

Verify:
- `test_integration_points.py::TestModuleIntegration::test_all_quiz_correct_is_valid_letter`
- All quiz questions in all 22 chapters still resolve correctly.

**Monitor:** The `test_edge_cases.py::TestMissionEdgeCases::test_quiz_question_correct_as_int`
ensures backward compatibility with int-based `correct` fields.

### 4.3 Switch Achievement Unlock Helper

Enable `USE_ACHIEVEMENT_TRY_UNLOCK = True`.

Verify:
- `test_current_behavior.py::TestFeatures::test_achievement_unlock`
- `test_integration_points.py::TestDataInvariants::test_achievements_catalog_has_critical_ids`

### 4.4 Switch XP Bar Args

Enable `USE_XP_BAR_ARGS = True`.

Verify:
- `test_current_behavior.py::TestPlayerCore::test_add_xp_returns_tuple`
- XP bar renders identically before and after.

### 4.5 Switch Chapter Dispatch

Enable `USE_CHAPTER_INT_DISPATCH = True`.

Verify:
- Entering `1` through `22` in `game_hub()` routes correctly.
- Edge cases: `"01"`, `" 1 "`, `"22"` still work.

### 4.6 Switch Action Dispatch

Enable `USE_ACTION_DICT_DISPATCH = True`.

Verify:
- All action shortcuts (`s`, `status`, `i`, `inv`, etc.) still route.
- Unknown inputs still show error.

### 4.7 Switch Renderer Protocol (High Risk — Last)

Enable `USE_RENDERER_PROTOCOL = True`.

This is the most invasive change. Verify:
- `MissionRunner.run()` produces identical screen output.
- All ANSI colors render correctly.
- `prompt_input()` still works inside missions.
- Save callback still fires after mission completion.

**Rollback ready:** If any visual regression is found, set flag back to `False`
and the old direct `print()` paths resume immediately.

### Phase 4 Validation Gate

- [ ] All probe tests pass with ALL relevant flags enabled.
- [ ] Smoke tests pass.
- [ ] Manual playthrough of Chapters 1, 5, 18, 22 completes successfully.
- [ ] Save/load round-trip tested on a real save file.

---

## Phase 5: Cleanup (Remove Old)

**Goal:** Delete dead code, remove feature flags, and update docs.
Only after Phase 4 has been stable for at least one full playthrough session.

### 5.1 Delete old implementations

| Old Code | New Replacement | File to Edit |
|----------|----------------|--------------|
| Inline `print()` badge blocks | `_show_badge()` calls | `engine/display.py` |
| Inline `clear() + print(header)` | `_screen()` calls | `main.py` |
| Inline `print(C.CYAN + " [k]")` | `_menu_item()` calls | `main.py` |
| Inline `divmod` + format | `_fmt_mm_ss()` | `mission_engine.py`, `main.py` |
| Inline achievement unlock blocks | `_try_unlock()` | `mission_engine.py` |
| `if mission.ascii_art:` cascade | Phase dispatch loop | `mission_engine.py` |
| `elif choice == "1":` wall | Dict dispatch | `main.py` |
| `run_terminal(expected=..., task=...)` | `run_terminal(TerminalTask(...))` | `mission_engine.py` |
| Hard-coded magic numbers | `engine.constants` imports | `mission_engine.py`, `player.py`, `main.py` |
| Direct `print()` in `MissionRunner` | `self.renderer.show_*()` calls | `mission_engine.py` |

### 5.2 Remove feature flags

Delete `engine/config.py` or reduce it to a single `DEBUG` flag.
Remove all `if is_enabled("..."):` branches. Keep only the new paths.

### 5.3 Update documentation

- Update `CLAUDE.md`:
  - Add `engine/constants.py` to file list.
  - Add `engine/renderer.py` to file list.
  - Update `MissionRunner` signature to include `renderer`.
- Update `devdocs/refactoring/current_state.md` to reflect the new architecture.
- Archive `devdocs/refactoring/` into a single `refactoring_log.md` with before/after stats.

### 5.4 Final validation

```bash
python3 probe_tests/pre_refactor/test_current_behavior.py
python3 probe_tests/pre_refactor/test_edge_cases.py
python3 probe_tests/pre_refactor/test_integration_points.py
python3 smoke_tests/check_what_is_working/test_01_initialization.py
python3 smoke_tests/check_what_is_working/test_02_player_system.py
python3 smoke_tests/check_what_is_working/test_03_mission_engine.py
python3 smoke_tests/check_what_is_working/test_04_terminal_simulator.py
python3 smoke_tests/check_what_is_working/test_05_display_and_features.py
```

### 5.5 Git checkpoint

Create a tag after Phase 5:
```bash
git tag -a v1.1-refactored -m "Post-refactoring cleanup complete"
```

---

## Rollback Strategy

At any point during Phase 2-4, if tests fail or behavior regresses:

1. **Single feature:** Set the relevant `FEATURE_FLAGS` entry back to `False`.
2. **Single commit:** `git revert <commit-hash>` for the specific migration commit.
3. **Full rollback:** `git checkout <phase-1-tag>` and restart from the last stable state.

The probe tests in `probe_tests/pre_refactor/` are never modified during
refactoring. If they fail, the codebase is broken — regardless of how the new
abstractions look.

---

## Timeline Estimate

| Phase | Effort | Duration (single dev) |
|-------|--------|----------------------|
| Phase 1 | Preparation | 1-2 hours |
| Phase 2 | Extract (17 items) | 4-6 hours |
| Phase 3 | Abstract (5 items) | 6-8 hours |
| Phase 4 | Migrate (7 switches) | 3-4 hours |
| Phase 5 | Cleanup | 2-3 hours |
| **Total** | | **16-23 hours** |

**Recommended pace:** One item per day. Never skip the validation gate.
