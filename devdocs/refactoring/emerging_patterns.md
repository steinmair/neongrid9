# Emerging Patterns in NeonGrid-9

This catalog documents structural patterns that have crystallized through
repetition across the codebase. Each entry includes exact locations,
a proposed abstraction, and an impact/risk assessment.

---

## 1. Similar Code Appearing 3+ Times

### 1.1 Badge Message Trio
**Current locations:**
- `engine/display.py:169-187`

**What it looks like:**
```python
def show_warn(text: str):
    print()
    print(C.WARN + f"  ⚠  {text}" + C.WARN + "  ⚠" + C.RESET)
    print()

def show_error(text: str):
    print()
    print(C.DANGER + f"  ✗  SYSTEM ERROR: {text}" + C.DANGER + "  ✗" + C.RESET)
    print()

def show_success(text: str):
    print()
    print(C.SUCCESS + f"  ✓  {text}" + C.SUCCESS + "  ✓" + C.RESET)
    print()
```

**Proposed abstraction:**
```python
def _show_badge(color: str, symbol: str, text: str):
    print()
    print(color + f"  {symbol}  {text}" + color + f"  {symbol}" + C.RESET)
    print()

def show_warn(text):   _show_badge(C.WARN,   "⚠", text)
def show_error(text):  _show_badge(C.DANGER, "✗", f"SYSTEM ERROR: {text}")
def show_success(text): _show_badge(C.SUCCESS, "✓", text)
```

**Estimated impact:** 1 file (`engine/display.py`)  
**Risk:** low — purely internal refactor, no call-site changes.

---

### 1.2 Screen Clear + Colored Title Header
**Current locations:**
- `main.py:112`, `137`, `162`, `216`, `266`, `301`, `323`, `400`, `604`, `892`, `901`, `996`, `1040`, `1063`, `1119`, `1190`, `1230`, `1258`, `1276`, `1356`  
  (20 occurrences in `main.py` alone)

**What it looks like:**
```python
clear()
print(C.NEON + "\n  TITLE\n" + C.RESET)
```

**Proposed abstraction:**
```python
def _screen(title: str, color: str = C.NEON):
    clear()
    print(color + f"\n  {title}\n" + C.RESET)
```

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low — mechanical replacement, no logic change.

---

### 1.3 Menu Item Print Lines
**Current locations:**
- `main.py:205-209` (main_menu)
- `main.py:227-229` (new_game_menu difficulty)
- `main.py:236-238` (new_game_menu slots)
- `main.py:268-271` (load_game_menu)
- `main.py:303-305` (manage_saves_menu)
- `main.py:436-446` (game_hub actions)
  
  28 total occurrences.

**What it looks like:**
```python
print(C.CYAN  + "  [1]" + C.RESET + "  Neues Spiel")
print(C.GRAY  + "  [q]" + C.RESET + "  Beenden")
```

**Proposed abstraction:**
```python
def _menu_item(key: str, label: str, key_color: str = C.CYAN, label_color: str = C.RESET):
    print(key_color + f"  [{key}]" + C.RESET + label_color + f"  {label}" + C.RESET)
```

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low.

---

### 1.4 Achievement Unlock + Award Block
**Current locations:**
- `engine/mission_engine.py:243-310` (10 copies)

**What it looks like:**
```python
ach = self.player.achievements.unlock('some_id')
if ach:
    unlocked.append(ach)
    self.player.add_xp(ach.xp_reward)
```

**Proposed abstraction:**
```python
def _try_unlock(self, achievement_id: str, unlocked: list) -> None:
    ach = self.player.achievements.unlock(achievement_id)
    if ach:
        unlocked.append(ach)
        self.player.add_xp(ach.xp_reward)
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** low.

---

### 1.5 Safe-Index Transition Guard
**Current locations:**
- `engine/mission_engine.py:102`, `109`, `115`, `121`

**What it looks like:**
```python
if tr: show_transition(tr[0] if len(tr) > 0 else "")
if tr: show_transition(tr[1] if len(tr) > 1 else "")
if tr: show_transition(tr[2] if len(tr) > 2 else "")
if tr: show_transition(tr[3] if len(tr) > 3 else "")
```

**Proposed abstraction:**
```python
def _maybe_transition(transitions: list, index: int):
    if transitions and index < len(transitions):
        show_transition(transitions[index])
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** low.

---

### 1.6 Time Formatting (divmod → MM:SS)
**Current locations:**
- `engine/mission_engine.py:357-358`
- `main.py:1050-1051`
- `main.py:1100`

**What it looks like:**
```python
e_mm, e_ss = divmod(elapsed, 60)
r_mm, r_ss = divmod(remain,  60)
```

**Proposed abstraction:**
```python
def _fmt_mm_ss(seconds: int) -> str:
    mm, ss = divmod(seconds, 60)
    return f"{mm:02d}:{ss:02d}"
```

**Estimated impact:** 2 files (`engine/mission_engine.py`, `main.py`)  
**Risk:** low.

---

### 1.7 Quiz Correct-Letter Resolution
**Current locations:**
- `engine/mission_engine.py:374`
- `main.py:1076`
- `main.py:1238`

**What it looks like:**
```python
correct_letter = letters[q.correct] if isinstance(q.correct, int) else q.correct
```

**Proposed abstraction:**
Add a property to `QuizQuestion`:
```python
@property
def correct_letter(self) -> str:
    letters = ["A", "B", "C", "D"]
    return letters[self.correct] if isinstance(self.correct, int) else self.correct
```

**Estimated impact:** 3 files (`engine/mission_engine.py`, `main.py`, and any future consumers)  
**Risk:** low.

---

### 1.8 Gear Reward Display Block
**Current locations:**
- `engine/mission_engine.py:319-325`
- `engine/mission_engine.py:486-491`

**What it looks like:**
```python
from engine.player import GEAR_CATALOG
item = GEAR_CATALOG.get(mission.gear_reward, {})
print(C.YELLOW + f"  ★  NEUES GEAR: {item.get('name', mission.gear_reward)}" + C.RESET)
print(C.GRAY   + f"     {item.get('desc', '')}" + C.RESET)
print()
```

**Proposed abstraction:**
```python
def _show_gear_reward(gear_id: str, label: str = "NEUES GEAR"):
    from engine.player import GEAR_CATALOG
    item = GEAR_CATALOG.get(gear_id, {})
    print(C.YELLOW + f"  ★  {label}: {item.get('name', gear_id)}" + C.RESET)
    print(C.GRAY   + f"     {item.get('desc', '')}" + C.RESET)
    print()
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** low.

---

### 1.9 Smoke-Test Bootstrap + Helpers
**Current locations:**
- `smoke_tests/check_what_is_working/test_01_initialization.py:20-42`
- `smoke_tests/check_what_is_working/test_02_player_system.py:22-47`
- `smoke_tests/check_what_is_working/test_03_mission_engine.py:22-51`
- `smoke_tests/check_what_is_working/test_04_terminal_simulator.py:20-43`
- `smoke_tests/check_what_is_working/test_05_display_and_features.py:21-50`

**What it looks like:**
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def banner(msg): ...
def ok(msg): ...
def fail(msg, exc=None): ...
def info(msg): ...
```

**Proposed abstraction:**
Create `smoke_tests/_helpers.py` containing all shared helpers and path setup.

**Estimated impact:** 5 files (all smoke tests)  
**Risk:** low.

---

## 2. Data Structures Always Appearing Together

### 2.1 Mission Identity Quartet
**Current locations:**
- `engine/display.py:104` — `mission_header(mission_id, title, xp, mtype)`
- `engine/mission_engine.py:91`, `416`, `502` — passed to `mission_header()`
- All 22 `missions/ch*.py` — `Mission(mission_id=..., title=..., xp=..., mtype=...)`

**What it looks like:**
`mission_id`, `title`, `xp`, and `mtype` are always instantiated, passed, and displayed together. No call site uses only a subset.

**Proposed abstraction:**
```python
@dataclass
class MissionHeader:
    mission_id: str
    title: str
    xp: int
    mtype: str
```
`mission_header()` then accepts a single `MissionHeader` object.

**Estimated impact:** 3 files (`engine/display.py`, `engine/mission_engine.py`, all mission files conceptually)  
**Risk:** medium — touches every `Mission` instantiation indirectly, but only display and runner directly.

---

### 2.2 XP Bar Coordinate Pair
**Current locations:**
- `main.py:404-407` — `xp_bar(player.xp, player.level, player.get_current_level_xp(), player.get_next_level_xp())`
- `engine/mission_engine.py:235-237`, `476-478` — identical 4-arg `xp_bar()` call

**What it looks like:**
`get_current_level_xp()` and `get_next_level_xp()` are **never called independently** — every `xp_bar()` call requires both.

**Proposed abstraction:**
Add a method to `Player`:
```python
def xp_bar_args(self) -> tuple[int, int, int, int]:
    return (self.xp, self.level, self.get_current_level_xp(), self.get_next_level_xp())
```
or make `xp_bar()` accept a `Player` instance directly.

**Estimated impact:** 2 files (`main.py`, `engine/mission_engine.py`)  
**Risk:** low.

---

### 2.3 Terminal Task Context Pair
**Current locations:**
- `engine/mission_engine.py:133` — `if mission.expected_commands and mission.task_description:`
- `engine/mission_engine.py:195-200` — both passed to `run_terminal()`
- `engine/mission_engine.py:436-441` — both passed to `run_terminal()`

**What it looks like:**
`expected_commands` and `task_description` are always checked together and passed together. A mission with one but not the other would be invalid.

**Proposed abstraction:**
```python
@dataclass
class TerminalTask:
    expected_commands: List[str]
    task_description: str
    hints: List[str]
```

**Estimated impact:** 2 files (`engine/mission_engine.py`, `engine/terminal_sim.py`)  
**Risk:** medium — requires updating `run_terminal()` signature.

---

### 2.4 Time Coordinate Pair
**Current locations:**
- `engine/mission_engine.py:357-358`
- `main.py:1050-1051`

**What it looks like:**
`e_mm, e_ss = divmod(elapsed, 60)` and `r_mm, r_ss = divmod(remain, 60)` always appear as paired tuples. The two variables from each `divmod` are always consumed together in a format string.

**Proposed abstraction:**
A small helper returning a formatted string eliminates the need to unpack both pairs:
```python
def fmt_timer(elapsed: int, remaining: int) -> str:
    e = divmod(elapsed, 60)
    r = divmod(remaining, 60)
    return f"Verstrichen: {e[0]:02d}:{e[1]:02d}  Verbleibend: {r[0]:02d}:{r[1]:02d}"
```

**Estimated impact:** 2 files  
**Risk:** low.

---

### 2.5 Quiz Question Core Fields
**Current locations:**
- All 22 `missions/ch*.py` files — every `QuizQuestion(question=..., options=..., correct=..., explanation=...)`
- `engine/mission_engine.py` — `_run_quiz()` consumes all four fields together

**What it looks like:**
`question`, `options`, `correct`, and `explanation` are always defined together. A `QuizQuestion` missing any one field is invalid.

**Proposed abstraction:**
The dataclass already groups them, but the repetition across 22 mission files suggests a builder or factory:
```python
def quiz(question: str, options: list[str], correct: str, explanation: str, xp: int = 15):
    return QuizQuestion(question=question, options=options, correct=correct,
                        explanation=explanation, xp_value=xp)
```

**Estimated impact:** 22 mission files (optional — would reduce boilerplate)  
**Risk:** low.

---

## 3. Functions Always Called in Sequence

### 3.1 `show_xp_gain` → `xp_bar`
**Current locations:**
- `engine/mission_engine.py:234-237`
- `engine/mission_engine.py:475-478`
- `engine/mission_engine.py:511-512`

**Sequence:**
```python
show_xp_gain(total_xp)
xp_bar(new_xp, self.player.level,
       self.player.get_current_level_xp(),
       self.player.get_next_level_xp())
```

**Proposed abstraction:**
```python
def _show_xp_progress(self, amount: int):
    show_xp_gain(amount)
    xp_bar(self.player.xp, self.player.level,
           self.player.get_current_level_xp(),
           self.player.get_next_level_xp())
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** low.

---

### 3.2 `self.player.add_xp` → `self.player.complete_mission`
**Current locations:**
- `engine/mission_engine.py:231-232`
- `engine/mission_engine.py:473-474`

**Sequence:**
```python
new_xp, leveled_up = self.player.add_xp(total_xp)
self.player.complete_mission(mission.mission_id)
```

**Proposed abstraction:**
```python
def complete_mission_with_xp(self, mission_id: str, xp: int) -> tuple[int, bool]:
    new_xp, leveled_up = self.add_xp(xp)
    self.complete_mission(mission_id)
    return new_xp, leveled_up
```

**Estimated impact:** 1 file (`engine/player.py` + call sites in `engine/mission_engine.py`)  
**Risk:** low.

---

### 3.3 `clear` → Colored Header Print
**Current locations:**
- Every menu/screen function in `main.py` (20 occurrences)

**Sequence:**
```python
clear()
print(C.NEON + "\n  SOME TITLE\n" + C.RESET)
```

(See **1.2** for the abstraction.)

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low.

---

### 3.4 `show_success` → Explanation Print
**Current locations:**
- `engine/mission_engine.py:386-387`

**Sequence:**
```python
show_success(f"RICHTIG! +{earned} XP")
print(C.CYAN + f"  → {q.explanation}" + C.RESET)
```

**Proposed abstraction:**
```python
def show_correct_answer(earned_xp: int, explanation: str):
    show_success(f"RICHTIG! +{earned_xp} XP")
    print(C.CYAN + f"  → {explanation}" + C.RESET)
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** low.

---

### 3.5 `xp_bar` → Player Status Line
**Current locations:**
- `main.py:404-409`

**Sequence:**
```python
xp_bar(player.xp, player.level,
       player.get_current_level_xp(),
       player.get_next_level_xp())
print(C.GRAY + f"  {player.name}  ::  {player.level_title}" + C.RESET)
```

**Proposed abstraction:**
```python
def show_player_hub_header(player: Player):
    xp_bar(player.xp, player.level,
           player.get_current_level_xp(),
           player.get_next_level_xp())
    print(C.GRAY + f"  {player.name}  ::  {player.level_title}" + C.RESET)
```

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low.

---

### 3.6 `if self.save_callback` → `self.save_callback(self.player)`
**Current locations:**
- `engine/mission_engine.py:334-335`
- `engine/mission_engine.py:493-494`

**Sequence:**
```python
if self.save_callback:
    self.save_callback(self.player)
```

**Proposed abstraction:**
```python
def _auto_save(self):
    if self.save_callback:
        self.save_callback(self.player)
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** low.

---

### 3.7 `show_story` → `prompt_continue`
**Current locations:**
- `engine/mission_engine.py:101-103`
- `engine/mission_engine.py:422-423`

**Sequence:**
After every `show_story()` call in `MissionRunner`, `prompt_continue()` follows immediately.

**Proposed abstraction:**
```python
def show_story_and_wait(speaker: str, text: str):
    show_story(speaker, text)
    prompt_continue()
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** low.

---

## 4. Switch Statements / If-Else Chains on the Same Variable

### 4.1 `choice` Dispatch in `game_hub()` — 22-Way Chapter Chain
**Current locations:**
- `main.py:451-494`

**What it looks like:**
```python
if choice == "1":
    chapter_menu(1)
elif choice == "2":
    chapter_menu(2)
# ... through 22
```

**Proposed abstraction:**
```python
if choice.isdigit() and 1 <= (n := int(choice)) <= 22:
    chapter_menu(n)
```

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low.

---

### 4.2 `choice` Dispatch in `game_hub()` — Action Chain
**Current locations:**
- `main.py:495-512`

**What it looks like:**
```python
elif choice in ("s", "status"):
    show_player_status()
elif choice in ("i", "inv", "inventar"):
    show_inventory()
# ...
```

**Proposed abstraction:**
```python
ACTIONS = {
    ("s", "status"):        show_player_status,
    ("i", "inv", "inventar"): show_inventory,
    # ...
}
for keys, action in ACTIONS.items():
    if choice in keys:
        action()
        break
```

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low.

---

### 4.3 `choice` Dispatch in `main()`
**Current locations:**
- `main.py:1339-1359`

**What it looks like:**
```python
if choice == "1": ...
elif choice == "2": ...
elif choice == "3": ...
elif choice == "4": ...
elif choice in ("q", "quit", "exit"): ...
```

**Proposed abstraction:**
Same dictionary dispatch pattern as 4.2.

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low.

---

### 4.4 `mission.mtype` Boss Branching
**Current locations:**
- `engine/mission_engine.py:84-88`, `200`, `248`

**What it looks like:**
```python
if self.player.mission_completed(...) and mission.mtype != "BOSS":
    ...
if mission.mtype == "BOSS":
    return self._run_boss(mission)
max_attempts = 5 if mission.mtype != "BOSS" else 3
if mission.mtype == "BOSS":
    self.player.bosses_defeated += 1
```

**Proposed abstraction:**
Use a `MissionType` enum and strategy objects:
```python
class MissionType(Enum):
    SCAN = auto()
    BOSS = auto()
    # ...

class BossMissionHandler(MissionHandler): ...
class ScanMissionHandler(MissionHandler): ...
```

**Estimated impact:** 2-3 files (`engine/mission_engine.py`, `engine/display.py` for color mapping)  
**Risk:** medium — changes core dispatch logic.

---

### 4.5 `is_correct` Binary Branch in Exam + Review
**Current locations:**
- `main.py:1086-1093` (exam mode)
- `main.py:1244-1251` (review mode)

**What it looks like:**
```python
if is_correct:
    player.correct_first_try += 1
    print(C.SUCCESS + "  ✓ RICHTIG" + C.RESET)
else:
    correct_opt = q.options[...]
    print(C.DANGER + f"  ✗ FALSCH  → ..." + C.RESET)
```

**Proposed abstraction:**
```python
def _show_quiz_result(is_correct: bool, question: QuizQuestion, player: Player):
    if is_correct:
        player.correct_first_try += 1
        print(C.SUCCESS + "  ✓ RICHTIG" + C.RESET)
    else:
        correct_opt = question.options[question.correct_letter_index]
        print(C.DANGER + f"  ✗ FALSCH  → {question.correct_letter}) {correct_opt}" + C.RESET)
```

**Estimated impact:** 1 file (`main.py`)  
**Risk:** low.

---

### 4.6 Sequential `if mission.<field>` Cascade in `run()`
**Current locations:**
- `engine/mission_engine.py:96-127`

**What it looks like:**
```python
if mission.ascii_art: ...
if mission.story: ...
if mission.why_important: ...
if mission.explanation: ...
if mission.syntax: ...
if mission.example: ...
```

**Proposed abstraction:**
Define a `Phase` protocol and iterate over a list of phases:
```python
phases = [
    ("ascii",  lambda m: m.ascii_art,  lambda m: show_ascii_art(m.ascii_art)),
    ("story",  lambda m: m.story,    lambda m: show_story(m.speaker, m.story)),
    # ...
]
for name, guard, action in phases:
    if guard(mission):
        action(mission)
```

**Estimated impact:** 1 file (`engine/mission_engine.py`)  
**Risk:** medium — significantly restructures the mission runner flow.

---

## Priority Matrix

| # | Pattern | Files | Risk | Payoff |
|---|---------|-------|------|--------|
| 1 | Badge Message Trio (1.1) | 1 | low | medium |
| 2 | Screen Clear + Header (1.2) | 1 | low | high |
| 3 | Menu Item Prints (1.3) | 1 | low | medium |
| 4 | Achievement Unlock Block (1.4) | 1 | low | high |
| 5 | Safe-Index Transition (1.5) | 1 | low | low |
| 6 | Time Formatting (1.6) | 2 | low | low |
| 7 | Quiz Correct-Letter (1.7) | 3 | low | medium |
| 8 | Gear Reward Display (1.8) | 1 | low | low |
| 9 | Smoke-Test Helpers (1.9) | 5 | low | high |
| 10 | XP Bar Coordinate Pair (2.2) | 2 | low | medium |
| 11 | Terminal Task Context (2.3) | 2 | medium | medium |
| 12 | `show_xp_gain` → `xp_bar` (3.1) | 1 | low | medium |
| 13 | `add_xp` → `complete_mission` (3.2) | 2 | low | medium |
| 14 | `show_story` → `prompt_continue` (3.7) | 1 | low | low |
| 15 | Chapter Dispatch Chain (4.1) | 1 | low | high |
| 16 | Action Dispatch Chain (4.2) | 1 | low | medium |
| 17 | `mission.mtype` Branching (4.4) | 3 | medium | high |
| 18 | `is_correct` Binary Branch (4.5) | 1 | low | medium |
| 19 | Phase Cascade (4.6) | 1 | medium | high |

---

## Recommended Order of Attack

1. **Week 1 — Low-Risk, High-Payoff:**
   - 1.2 Screen Clear + Header
   - 1.4 Achievement Unlock Block
   - 1.9 Smoke-Test Helpers
   - 4.1 Chapter Dispatch Chain

2. **Week 2 — Low-Risk, Medium-Payoff:**
   - 1.1 Badge Message Trio
   - 1.3 Menu Item Prints
   - 1.7 Quiz Correct-Letter
   - 3.1 `show_xp_gain` → `xp_bar`

3. **Week 3 — Medium-Risk:**
   - 4.4 `mission.mtype` Strategy refactor
   - 4.6 Phase Cascade refactor
   - 2.3 Terminal Task Context object
