# Architecture Analysis — NeonGrid-9

*Reconstructed from the actual code, not from documentation claims. This document traces how the system is wired together, what patterns hold it up, and where the architecture contradicts itself.*

---

## 1. Entry Points and Execution Flows

### The Only Entry Point

There is exactly one way into the application:

```
$ python3 main.py
    │
    ▼
__main__ block in main.py
    │
    ├──► sys.version_info < (3, 10) → hard exit
    │
    ├──► first_run check (looks for ~/.neongrid9/save_slot*.json)
    │    └──► if true: show_boot_sequence() → show_title_screen()
    │
    ├──► try: main()
    │    │
    │    ├──► while True:
    │    │    ├──► choice = main_menu()
    │    │    ├──► "1" → new_game_menu() → game_hub()
    │    │    ├──► "2" → load_game_menu() → game_hub()
    │    │    ├──► "3" → manage_saves_menu()
    │    │    ├──► "4" → about_screen()
    │    │    └──► "q" → sys.exit(0)
    │    │
    │    └──► except KeyboardInterrupt → save + exit
    │    └──► except Exception → print traceback + exit
    │
    └──► All 22 chapter files have ALREADY been imported at module top level
```

**Critical observation:** By the time `main()` is called, all 22 chapter files have been parsed, all ~500 `Mission` objects constructed, and all ~1,100 `QuizQuestion` objects instantiated. The game pays a 0.5–2 second import penalty before the title screen appears.

---

### Primary Game Loop (Game Hub)

```
game_hub()
    │
    └──► while GAME.running:
         │
         ├──► clear() + show status bars (XP, faction reputation, chapter progress)
         │
         ├──► choice = prompt_input("hub")
         │    ├──► "1"–"22" → chapter_menu(int(choice))
         │    ├──► "s" → show_player_status()
         │    ├──► "i" → show_inventory()
         │    ├──► "r" → show_linux_readiness()
         │    ├──► "x" → review_mode()
         │    ├──► "e" → timed_exam_mode()
         │    ├──► "v" → GAME.save() + "Gespeichert!"
         │    └──► "q" → GAME.save() + GAME.running = False
         │
         └──► Each chapter_menu() call creates a fresh MissionRunner instance
```

**Observation:** `game_hub()` is a classic menu-driven state machine with no real state transitions — it just loops forever until the player quits. There is no "game over," no win condition, no narrative branching.

---

### Mission Execution Flow (The Heart of the System)

```
chapter_menu(ch_id)
    │
    ├──► Look up chapter data: CHAPTERS[ch_id - 1]
    ├──► Build mission_map: {m.mission_id: m for m in missions}
    ├──► Instantiate MissionRunner(GAME.player, save_callback=GAME.auto_save)
    │
    └──► while True:
         │
         ├──► Display all missions with completion markers
         ├──► choice = prompt_input(f"kap{ch_id}")
         │
         ├──► "q"/"quit"/"back" → break
         ├──► "all" → run all uncompleted missions sequentially
         ├──► starts with prefix (e.g., "1.") → mission_map[choice] → runner.run()
         ├──► isdigit() → missions[int(choice)-1] → runner.run()
         │
         └──► If all missions completed → _show_chapter_complete() → break
```

**Observation:** Three different input parsing strategies coexist in `chapter_menu()`: mission ID string, numeric index, and keywords. They can conflict (e.g., typing "1" could mean "mission index 0" or "mission ID 1.01").

---

### Mission Runner Internal Flow

```
MissionRunner.run(mission)
    │
    ├──► Already completed AND not BOSS? → _replay_mission() → return
    │
    ├──► mtype == "BOSS"? → _run_boss() → return
    │
    ├──► clear() + mission_header() + show_ascii_art()
    │
    ├──► PHASE 1: Story
    │    └──► show_story(mission.story, mission.speaker)
    │    └──► show_transition(mission.story_transitions[0])
    │
    ├──► PHASE 2: Why It Matters
    │    └──► show_info(mission.why_important)
    │    └──► show_transition(mission.story_transitions[1])
    │
    ├──► PHASE 3: Explanation + Syntax + Example
    │    └──► show_info(mission.explanation)
    │    └──► if mission.syntax: show_code(mission.syntax)
    │    └──► if mission.example: show_code(mission.example)
    │    └──► show_transition(mission.story_transitions[2])
    │
    ├──► PHASE 4: Terminal Task (if applicable)
    │    └──► if mtype in [SCAN, INFILTRATE, CONSTRUCT, REPAIR]:
    │         │
    │         ├──► Fancy prompt loop (up to 5 attempts)
    │         │    ├──► prompt_input("root@matrix")
    │         │    ├──► Check against expected_commands (exact / prefix / base)
    │         │    ├──► Wrong → offer hint → DEDUCT XP immediately
    │         │    └──► 5 failures → fallback to run_terminal()
    │         │
    │         └──► If still failed: show_warn() + show_code(expected[0])
    │
    ├──► PHASE 5: Quiz
    │    └──► _run_quiz(mission.quiz_questions)
    │         ├──► For each question: print options, prompt A/B/C/D
    │         ├──► 3 attempts per question
    │         ├──► Correct: +15 XP (first try) or +7 XP (retry)
    │         └──► record_quiz_result(chapter, correct)
    │
    ├──► PHASE 6: Exam Tip + Memory Tip
    │    └──► show_exam_tip(mission.exam_tip)
    │    └──► show_memory_tip(mission.memory_tip)
    │
    ├──► PHASE 7: Rewards
    │    ├──► Calculate base_xp (with failure penalty, first-try bonus)
    │    ├──► Add quiz XP
    │    ├──► player.add_xp(total_xp) → level up check
    │    ├──► player.complete_mission(mission.mission_id)
    │    ├──► If gear_reward: player.add_gear() + show gear info
    │    └──► If faction_reward: player.add_reputation() + show faction gain
    │
    ├──► PHASE 8: Achievements (inline checks, ~10 hardcoded conditions)
    │    ├──► first_mission (len(completed) == 1)
    │    ├──► boss_defeated (mtype == BOSS)
    │    ├──► five_bosses (bosses == 5)
    │    ├──► all_bosses (bosses == 22)
    │    ├──► quest_marathon (completed == 100 exactly)
    │    ├──► level_ten (level >= 10)
    │    ├──► chapter_*_complete (chapter mission count thresholds)
    │    └──► gear_collector (inventory >= 10)
    │
    ├──► If level_up: level_up_screen()
    ├──► save_callback(player) → JSON write
    └──► prompt_continue()
```

**Observation:** This is a 250-line "god method" that mixes display logic, game logic, state mutation, achievement checking, and persistence. It is the single most important method in the entire codebase and the hardest to modify safely.

---

### Boss Mission Flow

```
_run_boss(mission)
    │
    ├──► boss_intro() — full-screen ASCII art + red color scheme
    ├──► Show story + boss_desc
    │
    ├──► PHASE LOOP: for each expected_command:
    │    ├──► Print phase header ("Phase 1/5")
    │    ├──► run_terminal(expected=[cmd], max_attempts=3)
    │    └──► Track phase_success count
    │
    ├──► WIN CONDITION: phase_success >= total_phases * 0.6 (60% threshold)
    │    ├──► Win: full XP + boss_defeated increment
    │    └──► Loss: half XP
    │
    ├──► Boss quiz: _run_quiz() with 5 expert questions
    ├──► Inline achievement checks (duplicated from run())
    ├──► save_callback()
    └──► prompt_continue()
```

**Observation:** The 60% threshold is a fuzzy pass condition. A 5-phase boss can be defeated with only 3 successful phases. Achievement checking is partially duplicated between `run()` and `_run_boss()`.

---

## 2. Data Models and Schemas

### The Core Dataclasses

#### `Mission` (~20 fields)

```python
@dataclass
class Mission:
    mission_id: str              # "1.01", "2.15", "22.22"
    title: str                   # Display title
    mtype: str                   # SCAN | INFILTRATE | DECODE | CONSTRUCT | REPAIR | QUIZ | BOSS
    xp: int                      # Base XP reward (30–225)
    chapter: int                 # 1–22

    ascii_art: str = ""          # Multi-line ASCII art string
    story_transitions: List[str] = field(default_factory=list)  # Exactly 4 lines

    story: str = ""              # Narrative intro text
    speaker: str = "SYSTEM"      # One of 7 hardcoded names
    why_important: str = ""      # LPIC domain relevance
    explanation: str = ""        # Technical explanation
    syntax: str = ""             # Command syntax example
    example: str = ""            # Example output/demonstration

    task_description: str = ""   # What the player must do
    expected_commands: List[str] = field(default_factory=list)
    hint_text: str = ""            # Legacy single hint
    hints: List[str] = field(default_factory=list)  # [free, 20xp, 50xp]
    simulated_commands: List[str] = field(default_factory=list)

    quiz_questions: List[QuizQuestion] = field(default_factory=list)

    exam_tip: str = ""           # LPIC exam prep note
    memory_tip: str = ""         # Mnemonic or memory aid

    boss_name: str = ""          # BOSS-specific
    boss_desc: str = ""          # BOSS-specific

    gear_reward: Optional[str] = None       # GEAR_CATALOG key
    faction_reward: Optional[tuple] = None  # (faction_name, amount)
```

**Schema enforcement:** None at runtime. The dataclass constructor enforces types, but there is no validation that:
- `quiz_questions` is non-empty
- `expected_commands` is non-empty for SCAN missions
- `story_transitions` has exactly 4 elements
- `mission_id` matches the chapter number

#### `QuizQuestion` (5 fields)

```python
@dataclass
class QuizQuestion:
    question: str
    options: List[str]           # Must be exactly 4: ["A) ...", "B) ...", ...]
    correct: str                 # "A", "B", "C", or "D"
    explanation: str             # Why the correct answer is right
    xp_value: int = 15           # XP awarded for correct answer
```

**Schema enforcement:** `_run_quiz()` assumes 4 options and crashes with `IndexError` if fewer exist. No runtime validator checks this.

#### `Player` (~20 fields)

```python
@dataclass
class Player:
    name: str
    xp: int = 0
    level: int = 1
    current_chapter: int = 1
    completed_missions: Set[str] = field(default_factory=set)
    achievements: Dict[str, bool] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)
    factions: Dict[str, int] = field(default_factory=dict)
    chapter_times: Dict[int, float] = field(default_factory=dict)
    quiz_accuracy: Dict[int, tuple] = field(default_factory=dict)
    # ... additional tracking fields
```

**Critical schema gap:** `to_dict()` is missing the `achievements` field. The serialization bug means achievements are lost on every save/load cycle.

---

### The Global Data Structures

```
CHAPTERS (main.py)
    └──► List of 22 tuples: (id, missions_list, topic_tag, title, subtitle)
    └──► Manually maintained parallel to import statements

SIMULATED_OUTPUTS (terminal_sim.py)
    └──► Flat dict: {"lspci": "...output...", "lsusb -t": "...output...", ...}
    └──► ~4,000 lines of pre-written output strings
    └──► No namespacing by chapter; all commands share one namespace

ACHIEVEMENTS (features.py)
    └──► Dict of 19 Achievement dataclass instances
    └──► Declarative data, not code

GEAR_CATALOG (player.py)
    └──► Dict of gear items with rarity tiers, boost types, and descriptions
    └──► Referenced by `gear_reward` field in missions

LEVELS (player.py)
    └──► List of 15 tuples: (level_number, title, xp_threshold)
    └──► Used by _recalculate_level() to derive level from XP

FACTIONS (features.py)
    └──► List of 5 faction name strings
    └──► Referenced by faction_reward and reputation tracking
```

---

### Save File Schema (JSON)

```json
{
  "name": "GhostRunner",
  "xp": 15000,
  "level": 8,
  "current_chapter": 5,
  "completed_missions": ["1.01", "1.02", ...],
  "achievements": {"first_mission": true, ...},
  "inventory": ["basic_terminal", "hardware_scanner"],
  "factions": {"Kernel Syndicate": 50, "Root Collective": 75},
  "chapter_times": {"1": 1500.5, "2": 1200.3},
  "quiz_accuracy": {"1": [25, 30], "2": [18, 20]}
}
```

**Versioning:** No `version` field. `from_dict()` uses `.get()` defaults for missing keys, acting as an implicit migration layer. This is fragile but functional for small schema changes.

---

## 3. API Endpoints and Contracts

NeonGrid-9 has **no network API**. However, the codebase has internal "interfaces" — function signatures that form contracts between modules. These are the "APIs" of the architecture.

---

### Save System API (`engine/save_system.py`)

```python
save_game(player: Player, slot: int = 1) -> bool
load_game(slot: int = 1) -> Player | None
slot_info(slot: int) -> str
delete_save(slot: int) -> bool
```

**Contract:** `save_game` expects `player.to_dict()` to return a JSON-serializable dict. `load_game` expects the JSON to contain at least the keys that `from_dict()` reads.

**Contract breach:** `to_dict()` omits `achievements`. `from_dict()` reconstructs an empty `AchievementTracker`. Achievements are silently lost.

---

### Display API (`engine/display.py`)

```python
clear() -> None
typewrite(text, delay=0.018, color=C.WHITE) -> None
show_story(speaker, text) -> None
show_code(code, lang="bash") -> None
show_info(text) -> None
show_warn(text) -> None
show_error(text) -> None
show_success(text) -> None
show_exam_tip(tip) -> None
show_memory_tip(tip) -> None
show_hint(hint) -> None
show_achievements(unlocked) -> None
show_transition(text) -> None
show_ascii_art(art) -> None
show_xp_gain(amount) -> None
mission_header(id, title, xp, type) -> None
boss_intro(name, desc) -> None
level_up_screen(level, name) -> None
xp_bar(current, level, level_xp, next_xp, width=40) -> None
box(text, width=80) -> None
prompt_continue() -> None
prompt_input(label="terminal", valid_choices=None) -> str
```

**Contract:** All functions write to stdout and may call `time.sleep()`. None return structured data. The only "input" function is `prompt_input()`, which blocks on `input()`.

**Contract gap:** No `animate=False` parameter exists. No test can call these functions without sleeping.

---

### Mission Runner API (`engine/mission_engine.py`)

```python
class MissionRunner:
    def __init__(self, player: Player, save_callback: Callable = None)
    def run(self, mission: Mission) -> bool
    def _run_quiz(self, questions: List[QuizQuestion], chapter=0,
                  exam_start=0.0, exam_limit=0) -> int
    def _run_boss(self, mission: Mission) -> bool
    def _replay_mission(self, mission: Mission) -> bool
```

**Contract:** `run()` mutates `self.player` directly (XP, completed_missions, inventory, reputation). It calls `save_callback(player)` at the end if provided.

**Contract gap:** If `save_callback` raises an exception, all prior mutations have already been applied but are unsaved. No rollback.

---

### Terminal Simulator API (`engine/terminal_sim.py`)

```python
run_terminal(expected, task_description, hint_available=False,
             hint_text="", max_attempts=5) -> tuple[bool, int, str]
get_output(cmd: str) -> tuple[bool, str]
normalize_cmd(cmd: str) -> str
```

**Contract:** `run_terminal` presents a REPL-like prompt. It validates input against `expected` using exact/prefix/base matching. It looks up output via `get_output()` for display.

**Contract gap:** Validation logic and output lookup use DIFFERENT matching strategies. A command can print realistic output but still be rejected as "wrong."

---

### Player State API (`engine/player.py`)

```python
add_xp(amount: int) -> tuple[int, bool]        # (new_xp, leveled_up)
complete_mission(mission_id: str) -> None
record_quiz_result(chapter: int, correct: bool) -> None
add_gear(item_id: str) -> bool
add_reputation(faction: str, amount: int) -> None
gear_bonus(boost_type: str) -> float
stats_summary() -> str
to_dict() -> dict
from_dict(cls, d: dict) -> Player
```

**Contract:** `add_xp` applies level scaling and triggers level-up detection. `to_dict` / `from_dict` should round-trip all state.

**Contract breach:** Direct attribute mutation from `MissionRunner` bypasses `add_xp()` for hint deductions, potentially creating inconsistent level/XP state.

---

## 4. Architectural Patterns Used

### Pattern 1: Three-Layer Architecture (Data / Engine / Control)

```
missions/     → Data Layer (content: Mission, QuizQuestion literals)
engine/       → Engine Layer (business logic: runner, display, save, sim)
main.py       → Control Layer (menus, loops, global state)
```

**How well it holds:** The physical separation is clean. However, cross-layer coupling exists:
- `main.py` directly imports `LEVELS` and `GEAR_CATALOG` from `engine.player` (control layer reaching into data layer).
- `mission_engine.py` imports display functions directly (engine layer reaching into rendering).

**Verdict:** Three folders exist, but strict layering is not enforced.

---

### Pattern 2: Template Method (`MissionRunner.run()`)

Every mission follows the same rigid sequence:

```
Story → Why Important → Explanation → Syntax → Example → Terminal → Quiz → Exam Tip → Memory Tip → Rewards
```

`run()` is the template method. Concrete variations (BOSS, QUIZ) are handled via `if/elif` branches inside the method rather than subclass overrides.

**How well it holds:** The pattern is clearly present but implemented as a single 250-line method rather than extracted phases. This is a "Template Method" in intent but a "God Method" in implementation.

**Verdict:** Pattern recognized, but scale broke the implementation.

---

### Pattern 3: Singleton (`GameState`)

```python
# main.py
GAME = GameState()
```

A module-level singleton holds the active player, save slot, and running flag.

**How well it holds:** It works for a single-player CLI game. However, `GameState` mixes three concerns:
1. Player data (what the player owns)
2. Save slot metadata (which file to write to)
3. Loop control (whether the hub should keep running)

**Verdict:** Pragmatic but violates Single Responsibility Principle.

---

### Pattern 4: Command Pattern (Terminal Simulation)

```python
SIMULATED_OUTPUTS = {
    "lspci": "...output...",
    "lsusb -t": "...output...",
}
```

A string key represents a command; the dict lookup returns the pre-written result.

**How well it holds:** This is Command Pattern in its simplest form. The limitation is that it is stateless — no fake filesystem, no persistent working directory.

**Verdict:** Appropriate for the scope, but limits multi-step missions.

---

### Pattern 5: Observer Pattern (Achievements)

Achievement checks are inline `if` statements triggered after mission completion:

```python
if len(self.player.completed_missions) == 1:
    self.player.achievements.unlock("first_mission")
```

**How well it holds:** This is Observer-like in intent (react to state changes) but implemented as hardcoded inline checks rather than a registration/dispatch system.

**Verdict:** Pattern is implicit, not explicit. Two achievements (`perfect_quiz`, `no_hints`) are defined but never triggered because the "observer" code was never written.

---

### Pattern 6: Data-as-Code (Python Literals as Content Format)

All mission content is written as Python constructor calls:

```python
CHAPTER_1_MISSIONS = [
    Mission(mission_id="1.01", title="...", ...),
    Mission(mission_id="1.02", title="...", ...),
]
```

**How well it holds:** Zero parser code needed. Syntax errors caught at import. Git diffs are readable. But all content is loaded unconditionally, and a single typo crashes the entire game.

**Verdict:** A deliberate trade-off. Benefits content authors who know Python; punishes everyone else.

---

### Pattern 7: State Machine (Mission Types)

Seven mission types exist: `SCAN`, `INFILTRATE`, `DECODE`, `CONSTRUCT`, `REPAIR`, `QUIZ`, `BOSS`.

`run()` branches behavior based on `mtype`:
- BOSS → `_run_boss()`
- QUIZ → skip terminal
- SCAN/INFILTRATE → full terminal + quiz

**How well it holds:** Types are hardcoded strings (not an Enum). Adding an 8th type requires editing `run()` and the header color map.

**Verdict:** Works for 7 types. Would break down at 15+.

---

## 5. What Does Not Make Sense

### Anomaly 1: `FactionStatus` Is Dead Code

`features.py` defines a `FactionStatus` class with `progress_bar()` and `display()` methods. It is never instantiated anywhere. `Player.stats_summary()` manually builds faction reputation bars with inline string formatting instead.

**Why it is weird:** A complete, functional class exists for no reason. Either it was planned and abandoned, or the developer forgot to wire it in.

**What it suggests:** The faction system was envisioned as a deeper mechanic (maybe faction-locked content or faction wars) but was deprioritized. The class is a fossil of an unimplemented feature.

---

### Anomaly 2: Two Different Terminal Input Paths

A mission with `expected_commands` goes through:

1. **Fancy prompt loop** (in `MissionRunner.run()`) — up to 5 attempts, hint integration, XP deduction.
2. If 5 failures: **Full REPL** (`run_terminal()` in `terminal_sim.py`) — separate validation, separate UX.

**Why it is weird:** Two completely different code paths handle the same task. The fallback REPL has different hint behavior, different prompt styling, and different attempt counting.

**What it suggests:** The fancy prompt was added after the REPL already existed, or vice versa. They were never unified. The player experiences a jarring UX switch when the fallback triggers.

---

### Anomaly 3: Duplicated Achievement Checking

The `boss_defeated` achievement is checked in both:
- `MissionRunner.run()` (for BOSS missions that go through the standard flow)
- `MissionRunner._run_boss()` (for BOSS missions)

Since `_run_boss()` is called FROM `run()` when `mtype == "BOSS"`, the check happens twice for every boss.

**Why it is weird:** `AchievementTracker.unlock()` returns `None` if already unlocked, so the double-check is harmless but wasteful. It reveals that `_run_boss()` was written as a standalone method and later integrated into `run()` without removing redundant checks.

---

### Anomaly 4: `calculate_level()` Has Dual Behavior

```python
def calculate_level(total_xp):
    if total_xp <= 100:
        # Reputation mode: linear chunks of 20
        return min(5, max(1, (total_xp // 20) + 1))
    else:
        # XP mode: exponential thresholds
        thresholds = [0, 100, 250, 450, ...]
        ...
```

**Why it is weird:** One function handles two completely different semantic domains (reputation 0–100 and XP 0–52500) with a magic threshold of 100. A caller passing 50 gets a faction level (1–5). A caller passing 5000 gets a player level (1–15).

**What it suggests:** The function was originally for XP only. Faction reputation bars were added later, and the developer reused the same function rather than creating `calculate_reputation_level()`. The dual behavior is a hidden coupling.

---

### Anomaly 5: Manual Serialization with Missing Field

`Player.to_dict()` hardcodes 18 keys. `Player.from_dict()` hardcodes the same 18 keys. But `achievements` (the `AchievementTracker` object) is missing from `to_dict()`.

**Why it is weird:** The field IS in the dataclass. It IS initialized in `from_dict()`. But it is NOT saved. This means the developer added the field, added it to `from_dict()`, and simply forgot `to_dict()`.

**What it suggests:** No automated test covers the save/load round-trip. No lint rule checks that dataclass fields match serialization keys. This is a process gap, not a design gap.

---

### Anomaly 6: Display Clear Delegates to OS Shell

The screen clear function delegates to the OS via hardcoded platform commands (`cls` on Windows, `clear` on Unix) instead of using ANSI escape sequences.

**Why it is weird:** ANSI escape sequences achieve the same result faster, without delegating to the OS. The project already uses ANSI codes everywhere else (`class C`).

**What it suggests:** The clear function may have been written early in development before `class C` existed, or the developer did not know the ANSI clear sequence. It is an inconsistency in an otherwise ANSI-native display layer.

---

### Anomaly 7: `story_transitions` Exactly 4, But No Enforcement

Every mission is expected to have 4 transitions. `run()` accesses `tr[0]` through `tr[3]`. But the dataclass has `default_factory=list`, so a mission with 0 transitions would simply skip the transition display (guarded by `if tr:`).

**Why it is weird:** The code assumes 4 transitions, but the data model does not enforce it. A missing transition is silently ignored rather than flagged as an error.

**What it suggests:** The developer trusted the content authors (or themselves) to always provide 4 transitions. Runtime validation was deemed unnecessary for "static, complete" data.

---

### Anomaly 8: `GEAR_CATALOG` Referenced via Lazy Import

`mission_engine.py` imports `GEAR_CATALOG` inside methods rather than at module top level:

```python
def _show_gear_reward(self, gear_id):
    from engine.player import GEAR_CATALOG
    ...
```

**Why it is weird:** This is a circular import avoidance tactic. But `GEAR_CATALOG` is a static dict. It could be moved to `features.py` (where achievements and factions live) to break the cycle cleanly.

**What it suggests:** The module boundaries between `player.py` and `features.py` are not clean. `GEAR_CATALOG` contains game meta-data but lives in the player module. `features.py` references player-level concepts but is supposed to be a standalone utilities module.

---

## Summary

| Aspect | What the Architecture Claims | What the Code Actually Does |
|--------|-------------------------------|----------------------------|
| Layering | Clean Data/Engine/Control separation | Control layer reaches into Engine data; Engine reaches into Display |
| Modularity | Reusable engine components | `run()` is a 250-line god method; no phase extraction |
| Extensibility | "Easy to add chapters" | Adding chapter 23 requires 66 edits |
| Testability | Deterministic, stateless display | `time.sleep()` and `input()` block forever; no test harness |
| Data Integrity | Save/load preserves all state | `achievements` field is lost on every save |
| Achievement System | 19 unlockable achievements | 2 are dead code; triggers are scattered inline |
| Faction System | 5 factions with reputation | `FactionStatus` class is never used; purely cosmetic |
| Terminal Sim | Safe command practice | Two inconsistent input paths; validation ≠ simulation |
