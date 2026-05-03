# Refactoring Opportunities: NeonGrid-9

**Date:** 2026-05-02  
**Scope:** engine/, main.py, missions/  
**Goal:** Identify high-value refactors that improve testability, reduce coupling, and make AI-driven development easier.

---

## How to Read This Document

Each opportunity is rated on two axes:

- **Value:** How much does this improve maintainability, testability, or development velocity?
- **Effort:** Estimated lines-of-code change and complexity.

Priority = Value / Effort. Highest scores first.

---

## Priority 1: Critical (Blocks Testing / Development)

---

### RO-01: Display System → Renderer Protocol

**Current Pattern:**

Every function in `engine/display.py` directly calls `print()` or `sys.stdout.write()`. For example:

```python
# engine/display.py:41
def typewrite(text: str, delay: float = 0.018, color: str = C.WHITE):
    for ch in text:
        sys.stdout.write(color + ch + C.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()
```

**Why this is a problem:**
- **Untestable:** You cannot verify what the game displays without intercepting stdout in tests.
- **Unmockable:** MissionRunner calls `show_success()`, `show_error()`, etc. directly. In a unit test, these emit noise to the console and cannot be asserted against.
- **Blocks UI evolution:** A future web frontend, TUI (curses), or GUI would require rewriting every display function.
- **Blocks headless automation:** CI cannot run missions without console spam.

**Files affected:** `engine/display.py` (324 lines), `engine/mission_engine.py` (every `show_*` call), `engine/terminal_sim.py` (print calls), `main.py` (every screen function).

**Proposed Abstraction:**

Introduce a `Renderer` protocol and a default `TerminalRenderer` implementation:

```python
from typing import Protocol

class Renderer(Protocol):
    def clear(self) -> None: ...
    def typewrite(self, text: str, delay: float = 0.0, color: str = "") -> None: ...
    def show_success(self, msg: str) -> None: ...
    def show_error(self, msg: str) -> None: ...
    # ... all other display methods

class TerminalRenderer:
    """Default: prints to stdout with ANSI colors."""
    def show_success(self, msg: str):
        print(C.SUCCESS + msg + C.RESET)

class NullRenderer:
    """Test double: captures to internal buffer, no stdout."""
    def __init__(self):
        self.buffer: list[str] = []
    def show_success(self, msg: str):
        self.buffer.append(f"[SUCCESS] {msg}")
```

**Migration path:**
1. Define `Renderer` protocol with all current display signatures.
2. Create `TerminalRenderer` that delegates to today's `engine/display.py` functions (as private helpers).
3. Add `renderer: Renderer` parameter to `MissionRunner.__init__()` and `run_terminal()`.
4. Create `NullRenderer` for tests.
5. Gradually move logic from free functions into `TerminalRenderer` methods.

**Immediate benefits:**
- Smoke tests can assert on rendered output: `assert "RICHTIG!" in renderer.buffer`.
- `MissionRunner.run()` becomes unit-testable with a `NullRenderer`.
- No more `capsys` hacks or `unittest.mock.patch('builtins.print')`.

**Implementation effort:** Medium (~200 lines new code, ~60 call sites to update).  
**Risk:** Low. The protocol can be introduced incrementally; existing code continues to work via `TerminalRenderer`.

**ROI:** **Critical.** This single refactor unlocks unit testing for the entire mission engine and terminal simulator.

---

### RO-02: Save System → Storage Repository Pattern

**Current Pattern:**

```python
# engine/save_system.py:11
SAVE_DIR = Path.home() / ".neongrid9"
SAVE_FILES = {
    1: SAVE_DIR / "save_slot1.json",
    2: SAVE_DIR / "save_slot2.json",
    3: SAVE_DIR / "save_slot3.json",
}

def save_game(player: Player, slot: int = 1) -> bool:
    ensure_save_dir()
    path = SAVE_FILES.get(slot)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(player.to_dict(), f, ...)
```

**Why this is a problem:**
- **Untestable:** Every test that touches `save_game()` writes to the real filesystem under `~/.neongrid9`.
- **Hard-coded slots:** Cannot add slot 4 without editing the module.
- **Hard-coded format:** Cannot swap to SQLite, cloud, or encrypted storage without rewriting all call sites.
- **No versioning:** Save format changes risk corruption; there is no migration path baked in.

**Files affected:** `engine/save_system.py` (72 lines), `main.py` (calls `save_game`, `load_game`, `slot_info`, `delete_save`), `GameState.save()` and `GameState.auto_save()`.

**Proposed Abstraction:**

```python
from typing import Protocol

class SaveRepository(Protocol):
    def save(self, player: Player, slot: int) -> bool: ...
    def load(self, slot: int) -> Player | None: ...
    def list_slots(self) -> list[SlotMeta]: ...
    def delete(self, slot: int) -> bool: ...

class JsonFileRepository:
    """Current behavior: JSON files in ~/.neongrid9"""
    def __init__(self, dir_path: Path, max_slots: int = 3):
        ...

class InMemoryRepository:
    """Test double: dict-backed, no filesystem."""
    def __init__(self):
        self._data: dict[int, dict] = {}
```

**Immediate benefits:**
- Tests can use `InMemoryRepository` — no filesystem, no cleanup, no race conditions.
- Save-format versioning can be encapsulated in `JsonFileRepository` (e.g., add `version: 2` key, migrate on load).
- Future storage backends (SQLite, S3, encrypted) implement the same protocol.

**Implementation effort:** Low (~80 lines new code, ~8 call sites to update).  
**Risk:** Low. `main.py` just passes `repository=JsonFileRepository()` to `GameState`.

**ROI:** **Critical.** Unlocks isolated testing of save/load logic and enables CI-safe test suites.

---

## Priority 2: High (Significant Maintenance Reduction)

---

### RO-03: Achievement Checking → Rule Engine

**Current Pattern:**

`MissionRunner.run()` contains ~80 lines of inline achievement checks (lines 240–311):

```python
# engine/mission_engine.py:240-311
if len(self.player.completed_missions) == 1:
    ach = self.player.achievements.unlock('first_mission')
    ...
if mission.mtype == "BOSS":
    self.player.bosses_defeated += 1
    ach = self.player.achievements.unlock('boss_defeated')
    ...
if self.player.bosses_defeated == 22:
    ach = self.player.achievements.unlock('all_bosses')
    ...
# Chapter 1 hardcoded
if mission.chapter == 1 and len(chapter_missions) >= 31:
    ach = self.player.achievements.unlock('chapter_1_complete')
    ...
if len(self.player.completed_missions) == 100:
    ach = self.player.achievements.unlock('quest_marathon')
    ...
```

**Why this is a problem:**
- **Open/Closed violation:** Adding a new achievement requires editing `MissionRunner.run()`.
- **Scattered business logic:** The method mixes mission orchestration, display, XP math, *and* achievement rules.
- **Untestable in isolation:** You cannot test whether `quest_marathon` triggers at exactly 100 missions without running a full mission.
- **Hardcoded chapter 1:** Chapter 2–22 completion achievements don't exist because adding them would require 22 more `if` blocks.

**Files affected:** `engine/mission_engine.py` (lines 240–311), `engine/features.py` (ACHIEVEMENTS dict).

**Proposed Abstraction:**

```python
# engine/features.py
@dataclass
class AchievementRule:
    id: str
    check: Callable[[Player, Mission], bool]

RULES = [
    AchievementRule("first_mission", lambda p, m: len(p.completed_missions) == 1),
    AchievementRule("boss_defeated", lambda p, m: m.mtype == "BOSS"),
    AchievementRule("all_bosses",    lambda p, m: p.bosses_defeated >= 22),
    AchievementRule("chapter_complete", lambda p, m: is_chapter_complete(p, m.chapter)),
]

class AchievementEngine:
    def check(self, player: Player, mission: Mission) -> list[Achievement]:
        unlocked = []
        for rule in RULES:
            if rule.check(player, mission) and not player.achievements.has(rule.id):
                ach = player.achievements.unlock(rule.id)
                if ach:
                    unlocked.append(ach)
        return unlocked
```

**Immediate benefits:**
- Adding an achievement is a one-line rule registration, not a method edit.
- Achievement logic is unit-testable with mock `Player` objects.
- `MissionRunner.run()` shrinks by ~80 lines, improving readability.
- Chapter-complete achievements for all 22 chapters become trivial.

**Implementation effort:** Medium (~60 lines new code, refactor ~80 lines).  
**Risk:** Low. The rules are pure functions; if a rule is wrong, only that achievement is affected.

**ROI:** **High.** Every future achievement addition becomes a one-liner instead of a multi-file edit.

---

### RO-04: Terminal Simulator → Command Registry

**Current Pattern:**

`engine/terminal_sim.py` is a 4,457-line file. Lines 12–4348 consist of a single flat dictionary:

```python
SIMULATED_OUTPUTS = {
    "lspci": """...""",
    "lspci -v": """...""",
    # ... 787+ entries
}
```

Adding a command requires editing this monster dictionary. There is no way to:
- Unit-test a single command's output in isolation.
- Add dynamic or parameterized output (e.g., `ls` that lists different files based on state).
- Discover what commands exist programmatically without iterating the entire dict.

**Files affected:** `engine/terminal_sim.py` (4,457 lines — the entire file).

**Proposed Abstraction:**

```python
from typing import Protocol

class TerminalCommand(Protocol):
    name: str                    # Canonical command, e.g. "lspci"
    aliases: list[str]           # ["lspci -v", "lspci -k"]

    def run(self, args: list[str], state: TermState) -> str:
        """Return simulated output string."""
        ...

class LspciCommand:
    name = "lspci"
    aliases = ["lspci -v", "lspci -k", "lspci -vv"]

    def run(self, args, state):
        if "-v" in args or "-vv" in args:
            return LSPCI_VERBOSE_OUTPUT
        return LSPCI_OUTPUT

class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, TerminalCommand] = {}

    def register(self, cmd: TerminalCommand):
        self._commands[cmd.name] = cmd
        for alias in cmd.aliases:
            self._commands[alias] = cmd

    def lookup(self, user_input: str) -> tuple[bool, str]:
        # Replaces get_output() logic
        ...
```

**Migration path:**
1. Create `CommandRegistry` and `TerminalCommand` protocol.
2. Extract the first 10–20 most-used commands into classes (e.g., `lspci`, `lsusb`, `uname`).
3. Register them in a `build_default_registry()` function.
4. Keep the legacy `SIMULATED_OUTPUTS` as a fallback during transition.
5. Gradually migrate the remaining 767+ entries.

**Immediate benefits:**
- `LspciCommand` can be unit-tested in isolation: `assert "Intel Corporation" in cmd.run([], state)`.
- Commands can have **stateful behavior** (e.g., `cd` changes directory, `mkdir` creates files).
- The 4,457-line file shrinks as commands move to their own small modules.
- AI-driven development becomes easier: adding a new command is a new file, not an edit to a 4,000-line dictionary.

**Implementation effort:** High (new architecture + gradual migration of 787 entries).  
**Risk:** Medium. The migration is incremental; the old `SIMULATED_OUTPUTS` can stay as a compatibility layer.

**ROI:** **High.** This is the most impactful long-term refactor. The terminal simulator is the game's primary mechanic and its current architecture is unmaintainable at scale.

---

### RO-05: MissionRunner.run() → State Machine / Template Method

**Current Pattern:**

`MissionRunner.run()` is a ~260-line god method that sequences:

1. Boss check
2. Header + ASCII art
3. Story + transitions
4. Why important
5. Explanation
6. Syntax
7. Example
8. Terminal task (with forced-hint loop)
9. Quiz
10. Exam tip + memory tip
11. XP calculation (with inline math for failure/attempts)
12. Achievement checks (inline, 80 lines)
13. Gear reward
14. Faction reward
15. Save callback

**Why this is a problem:**
- **Single Responsibility violation:** One method handles display, input, business logic, persistence, and reward calculation.
- **Untestable phases:** You cannot test "does the XP calculation apply the first-attempt bonus?" without running the entire mission flow.
- **No replayability:** `_replay_mission()` duplicates logic instead of reusing phases.
- **Hard to extend:** Adding a new mission phase (e.g., "pre-flight check") means editing the middle of a 260-line method.

**Files affected:** `engine/mission_engine.py` (lines 78–338).

**Proposed Abstraction:**

```python
class MissionPhase(Protocol):
    def run(self, ctx: MissionContext) -> PhaseResult: ...

class StoryPhase(MissionPhase):
    def run(self, ctx):
        ctx.renderer.show_story(ctx.mission.speaker, ctx.mission.story)
        return PhaseResult.CONTINUE

class TerminalTaskPhase(MissionPhase):
    def run(self, ctx):
        success = ctx.terminal.run(ctx.mission.expected_commands, ...)
        ctx.state.terminal_success = success
        return PhaseResult.CONTINUE

class XPRewardPhase(MissionPhase):
    def run(self, ctx):
        base = ctx.mission.xp
        if not ctx.state.terminal_success:
            base //= 3
        if ctx.state.terminal_success and ctx.state.attempts == 1:
            base = int(base * 1.2)
        ctx.player.add_xp(base + ctx.state.quiz_xp)
        return PhaseResult.CONTINUE

class MissionRunner:
    PHASES = [
        StoryPhase(),
        ExplanationPhase(),
        TerminalTaskPhase(),
        QuizPhase(),
        XPRewardPhase(),
        AchievementPhase(),
        RewardPhase(),
    ]
```

**Immediate benefits:**
- Each phase is independently unit-testable with a mock `MissionContext`.
- `XPRewardPhase` can be tested with 10 boundary cases in isolation.
- Replay mode reuses the same phases, just skips input-heavy ones.
- New mission types (e.g., "speedrun") can rearrange or swap phases.

**Implementation effort:** High (~300 lines of restructuring).  
**Risk:** Medium. The method is complex; refactoring requires careful preservation of behavior. The smoke tests provide a safety net.

**ROI:** **High.** This is the heart of the game engine. Decoupling it into phases makes every other refactor easier.

---

## Priority 3: Medium (Nice to Have, Clear Benefits)

---

### RO-06: Menu System → Menu Builder

**Current Pattern:**

`main.py` contains at least 5 hand-rolled menu functions with identical structure:

```python
def main_menu() -> str:
    show_title_screen()
    print(C.WHITE + "  HAUPTMENÜ\n" + C.RESET)
    print(C.CYAN  + "  [1]" + C.RESET + "  Neues Spiel")
    print(C.CYAN  + "  [2]" + C.RESET + "  Spiel laden")
    ...
    return prompt_input("menü").lower()

def load_game_menu() -> bool:
    clear()
    print(C.NEON + "\n  SPIEL LADEN\n" + C.RESET)
    for slot in [1, 2, 3]:
        info = slot_info(slot)
        print(C.CYAN + f"  [{slot}]" + C.RESET + f"  Slot {slot}: {info}")
    ...
```

Also `game_hub()` has a 22-branch `if/elif` chain for chapter selection (lines 451–494).

**Why this is a problem:**
- **Massive duplication:** Every menu repeats `clear()`, `print(header)`, `print(options)`, `prompt_input()`, `if/elif` branching.
- **Error-prone:** Adding a menu item requires manually updating both the display and the branch logic.
- **Inaccessible:** No way to programmatically discover what menu options exist (e.g., for a TTS screen reader or automated testing).

**Files affected:** `main.py` (lines 201–512, multiple functions).

**Proposed Abstraction:**

```python
@dataclass
class MenuItem:
    key: str
    label: str
    action: Callable
    color: str = C.CYAN

class Menu:
    def __init__(self, title: str, subtitle: str = ""):
        self.title = title
        self.items: list[MenuItem] = []

    def add(self, key: str, label: str, action: Callable, color: str = C.CYAN):
        self.items.append(MenuItem(key, label, action, color))

    def run(self, renderer: Renderer) -> str:
        renderer.clear()
        renderer.header(self.title, self.subtitle)
        for item in self.items:
            renderer.print(f"  [{item.key}]  {item.label}", color=item.color)
        return renderer.prompt_input("wahl")

# Usage
main = Menu("HAUPTMENÜ")
main.add("1", "Neues Spiel", new_game_menu)
main.add("2", "Spiel laden", load_game_menu)
main.add("q", "Beenden", quit_game, color=C.GRAY)
choice = main.run(renderer)
main.dispatch(choice)
```

**Immediate benefits:**
- Adding a menu item is one line instead of two (display + branch).
- Menus are declarative and self-documenting.
- A TTS or accessibility layer can iterate `menu.items` to announce options.
- The 22-branch chapter selection in `game_hub()` collapses to a loop or dict dispatch.

**Implementation effort:** Medium (~120 lines new code, refactor ~200 lines of menus).  
**Risk:** Low. Menus are leaf nodes; they don't affect game state logic.

**ROI:** **Medium.** Reduces boilerplate significantly but doesn't unblock testing the way RO-01 or RO-02 does.

---

### RO-07: Global GameState Singleton → Dependency Injection

**Current Pattern:**

```python
# main.py:103
GAME = GameState()
```

`GAME` is a module-level singleton. `chapter_menu()` instantiates `MissionRunner(GAME.player, save_callback=GAME.auto_save)`. Every function that needs player data accesses `GAME.player`.

**Why this is a problem:**
- **Untestable:** You cannot run `game_hub()` with a mock player without monkey-patching `GAME`.
- **Hidden coupling:** `chapter_menu()` secretly depends on the global `GAME` object; the dependency is not visible in its signature.
- **No concurrent sessions:** Two players cannot coexist in the same process (relevant for future multiplayer or test parallelization).

**Files affected:** `main.py` (all menu and game-loop functions).

**Proposed Abstraction:**

Pass `GameState` (or a narrower `GameSession` interface) as an explicit parameter to every function that needs it:

```python
def game_hub(session: GameSession) -> None:
    while session.running and session.player:
        choice = prompt_input("hub")
        if choice == "1":
            chapter_menu(session, 1)
        ...

def chapter_menu(session: GameSession, ch_id: int) -> None:
    runner = MissionRunner(session.player, save_callback=session.save)
    ...
```

**Immediate benefits:**
- Tests create `GameSession(player=mock_player)` and pass it in.
- Dependencies are explicit from function signatures.
- No hidden global state = no mysterious test failures due to stale `GAME` state.

**Implementation effort:** Medium (~60 call sites to update).  
**Risk:** Low. This is a mechanical parameter threading; no logic changes.

**ROI:** **Medium.** Makes the codebase cleaner but is mostly a hygiene refactor. Combine with RO-06 (Menu Builder) to reduce the parameter-threading burden.

---

### RO-08: Configuration as Code → Typed Configuration

**Current Pattern:**

```python
# engine/player.py:11
LEVELS = [
    (1,  "Newbie Hacker",       0),
    (2,  "Script Kiddie",       500),
    ...
]

# engine/player.py:30
GEAR_CATALOG = {
    "basic_terminal": {
        "name":   "Basic Terminal",
        "desc":   "Dein erstes Interface.",
        "boost":  "starter",
        "rarity": "common",
        "tier":   1,
    },
    ...
}

# engine/features.py:59
ACHIEVEMENTS = {
    'first_mission': Achievement(...),
    ...
}
```

These are module-level dictionaries and tuples. They are effectively configuration, but:
- No IDE autocomplete for `GEAR_CATALOG["basic_terminal"]["???"]`.
- No type checking: a gear item could miss the `"tier"` key and `mypy` would not catch it.
- Runtime errors only: `GEAR_CATALOG[item_id]["name"]` raises `KeyError` if a field is missing.

**Files affected:** `engine/player.py`, `engine/features.py`.

**Proposed Abstraction:**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class GearItem:
    id: str
    name: str
    description: str
    boost: str
    rarity: str
    tier: int
    source: str = ""

@dataclass(frozen=True)
class LevelConfig:
    level: int
    title: str
    xp_threshold: int

LEVELS: tuple[LevelConfig, ...] = (
    LevelConfig(1, "Newbie Hacker", 0),
    LevelConfig(2, "Script Kiddie", 500),
    ...
)

GEAR_CATALOG: dict[str, GearItem] = {
    "basic_terminal": GearItem(
        id="basic_terminal",
        name="Basic Terminal",
        description="Dein erstes Interface.",
        boost="starter",
        rarity="common",
        tier=1,
    ),
    ...
}
```

**Immediate benefits:**
- `mypy` catches missing fields at type-check time.
- IDE autocomplete works on `gear_item.name`, `gear_item.tier`.
- `frozen=True` prevents accidental mutation of configuration at runtime.
- `GearItem.source` has a default, so optional fields don't require dummy values.

**Implementation effort:** Low (~40 lines of dataclass definitions, ~60 lines of data conversion).  
**Risk:** Very low. Pure data structure change; no logic changes.

**ROI:** **Medium.** Improves developer experience and prevents a class of runtime errors. Makes AI-generated code more reliable because the schema is explicit.

---

## Priority 4: Low (Cosmetic, Can Wait)

---

### RO-09: Hardcoded Chapter Imports → Auto-Registration

**Current Pattern:**

```python
# main.py:34-55
from missions.ch01_hardware  import CHAPTER_1_MISSIONS
from missions.ch02_boot      import CHAPTER_2_MISSIONS
...
from missions.ch22_exam      import CHAPTER_22_MISSIONS

CHAPTERS = [
    (1, CHAPTER_1_MISSIONS,   "101.1", "BOOT CAMP",        "Hardware & BIOS/UEFI"),
    ...
    (22, CHAPTER_22_MISSIONS, "ALL",   "FINAL EXAM PROTOCOL", ...),
]
```

Adding Chapter 23 requires:
1. Create `missions/ch23_newtopic.py`.
2. Add `from missions.ch23_newtopic import CHAPTER_23_MISSIONS` to `main.py`.
3. Add a tuple to `CHAPTERS`.

**Why this is a problem:**
- Adding content requires editing the entry point.
- Risk of import ordering issues or typos.
- The chapter metadata (topic, title, subtitle) is duplicated between the tuple and the file name/contents.

**Proposed Abstraction:**

```python
# In each chapter file, export metadata
CHAPTER_META = {
    "id": 1,
    "topic": "101.1",
    "title": "BOOT CAMP",
    "subtitle": "Hardware & BIOS/UEFI",
}
CHAPTER_1_MISSIONS = [...]

# In main.py or a registry module
from engine.chapter_registry import ChapterRegistry
import missions  # triggers __init__.py registration

registry = ChapterRegistry()
registry.discover("missions")  # imports all ch*.py, reads CHAPTER_META
CHAPTERS = registry.all_chapters()
```

**Immediate benefits:**
- Adding a chapter is a single new file, zero edits to `main.py`.
- Chapter metadata lives next to its missions, not in a central list.
- `ChapterRegistry` can validate that all expected chapters exist.

**Implementation effort:** Low (~40 lines).  
**Risk:** Very low. `import missions` can be controlled with `__init__.py` or `importlib`.

**ROI:** **Low.** Only saves a few lines when adding chapters, which is an infrequent operation. The real value is consistency and reduced merge conflicts when multiple people add chapters.

---

### RO-10: Recap Map → Data-Driven Recaps

**Current Pattern:**

```python
# main.py:616
recap_map = {
    1: [
        "lspci / lsusb / lshw / dmidecode",
        "dmesg / journalctl -k",
        ...
    ],
    2: [...],
    ...
    22: [...],
}
```

A 22-entry dictionary of recap strings lives in `main.py`. It is content, not logic.

**Proposed Abstraction:**

Move `recap_map` into each chapter file as `CHAPTER_RECAP` and have `_show_chapter_complete()` load it from the chapter metadata.

**ROI:** **Low.** Small cleanup; not a blocker.

---

## Summary Matrix

| ID | Opportunity | Priority | Effort | Risk | Unlocks Testing | Reduces Coupling |
|----|-------------|----------|--------|------|-----------------|------------------|
| RO-01 | Display → Renderer Protocol | **Critical** | Medium | Low | ✅ Yes | ✅ High |
| RO-02 | Save → Storage Repository | **Critical** | Low | Low | ✅ Yes | ✅ High |
| RO-03 | Achievements → Rule Engine | **High** | Medium | Low | ✅ Yes | ✅ High |
| RO-04 | Terminal → Command Registry | **High** | High | Medium | ✅ Yes | ✅ High |
| RO-05 | MissionRunner → State Machine | **High** | High | Medium | ✅ Yes | ✅ High |
| RO-06 | Menus → Menu Builder | **Medium** | Medium | Low | ❌ No | ✅ Medium |
| RO-07 | Global State → DI | **Medium** | Medium | Low | ✅ Yes | ✅ Medium |
| RO-08 | Config → Typed Dataclasses | **Medium** | Low | Very Low | ❌ No | ✅ Low |
| RO-09 | Chapter Imports → Registry | **Low** | Low | Very Low | ❌ No | ✅ Low |
| RO-10 | Recap Map → Data-Driven | **Low** | Low | Very Low | ❌ No | ❌ Low |

---

## Recommended Sequencing

Follow this order to maximize safety and cumulative benefit:

1. **RO-02 (Save Repository)** — Fast win. Enables safe testing immediately.
2. **RO-08 (Typed Configuration)** — Zero-risk. Improves type safety across the board.
3. **RO-01 (Renderer Protocol)** — The big unlock. Once display is mockable, everything becomes testable.
4. **RO-03 (Achievement Rule Engine)** — Now that you can mock display, test achievement triggers in isolation.
5. **RO-05 (MissionRunner State Machine)** — Split the god method while smoke tests guard against regressions.
6. **RO-07 (Dependency Injection)** — Thread `GameSession` through menus; combine with RO-06.
7. **RO-06 (Menu Builder)** — Replaces all hand-rolled menus once DI is in place.
8. **RO-04 (Terminal Command Registry)** — Gradual migration of the 4,457-line dictionary.
9. **RO-09 (Chapter Registry)** — Nice-to-have cleanup after major refactors are stable.
10. **RO-10 (Recap Data-Driven)** — Last, purely cosmetic.

---

## Cross-References

| Refactor | Depends On | Documents |
|----------|------------|-----------|
| RO-01 | RO-08 (typed config helps renderer signatures) | `gap_analysis.md` §3.4 (forced hint in display) |
| RO-02 | — | `cleanup_inventory.md` §2 (save system is hard-coded) |
| RO-03 | RO-01 (need mockable display to test achievements) | `gap_analysis.md` §3.3 (8 unimplemented achievements) |
| RO-04 | — | `gap_analysis.md` §3.5 (terminal simulator limits) |
| RO-05 | RO-01, RO-02, RO-03 | `gap_analysis.md` §4.1 (gear bonus not applied in runner) |
| RO-06 | RO-07 (DI makes menu builder testable) | — |
| RO-07 | — | `cleanup_inventory.md` §3 (GAME singleton) |
| RO-08 | — | `gap_analysis.md` §2.1 (data-quality issues) |
| RO-09 | — | — |
| RO-10 | RO-09 | — |

---

*End of Refactoring Opportunities*
