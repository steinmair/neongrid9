# NeonGrid-9 Gap Closure Plan

**Date:** 2026-05-02
**Based on:** `devdocs/evolution/gap_analysis.md`
**Goal:** Transform the gap analysis into an actionable, phased implementation roadmap.

---

## Philosophy

This plan follows a **"fix before you refactor"** philosophy. We patch the broken player experience first (quick wins), then harden the engine (incremental improvements), then restructure for growth (major refactoring), and finally replace subsystems that have reached architectural limits (complete rewrites).

Each phase is designed to leave the codebase in a **shippable state**. No phase requires the next phase to be complete for the game to work.

---

## Phase 1: Quick Wins (Can Do Immediately)

*Timeline: 2–3 days*
*Goal: Fix the most visible player-facing bugs and complete unfinished systems without architectural changes.*

### 1.1 Fix the Forced Hint System

**What:** Currently, `MissionRunner.run()` automatically shows hints and deducts XP when the player enters a wrong command (`engine/mission_engine.py:178`). The player has no agency.

**How:** Replace the auto-hint loop with player-initiated hint requests. After a wrong answer, prompt: `"[h] Hint anfordern | [Enter] Erneut versuchen | [q] Aufgeben"`. Only deduct XP when the player actively chooses a hint.

**Files:** `engine/mission_engine.py` (lines 143–191)

**Dependencies:** None.

**Risk:** Low. Changes only the mission-runner input loop. No external APIs affected.

**Testing:**
- Manual: Complete a SCAN mission, verify hints are opt-in.
- Manual: Verify XP is only deducted on active hint request.

---

### 1.2 Wire Up Gear XP Bonuses

**What:** `Player.gear_bonus()` exists but `MissionRunner` never calls it. Gear is cosmetic.

**How:** Add a single call in `MissionRunner.run()` before `show_xp_gain()`:

```python
# Map mission type to gear bonus key
bonus_key = {
    "SCAN": "scan_xp",
    "QUIZ": "quiz_xp",
    "INFILTRATE": "admin_xp",
    "CONSTRUCT": "pipe_xp",
    "REPAIR": "pipe_xp",
    "DECODE": "regex_xp",
    "BOSS": "all_xp",
}.get(mission.mtype)

if bonus_key:
    mult = self.player.gear_bonus(bonus_key)
    total_xp = int(total_xp * mult)
```

**Files:** `engine/mission_engine.py` (around line 230)

**Dependencies:** None.

**Risk:** Low. Purely additive. If a bonus key is missing, `mult = 1.0` (no change).

**Testing:**
- Manual: Equip `ghost_mask`, complete a QUIZ mission, verify XP is 1.2×.
- Manual: Equip `linux_badge`, verify +5% stacks additively.

---

### 1.3 Implement Missing Achievement Triggers

**What:** 8 achievements have definitions but no trigger logic. Only 11 fire.

**How:** Extend `_check_achievements()` in `MissionRunner` with the missing checks. Generalize chapter completion:

```python
# Replace hardcoded chapter_1_complete with loop:
for ch_id, ch_missions, *_ in CHAPTERS:
    needed = len(ch_missions)
    have = len([m for m in self.player.completed_missions
                if m.startswith(f"{ch_id}.")])
    if have >= needed:
        ach = self.player.achievements.unlock(f'chapter_{ch_id}_complete')
        if ach: unlocked.append(ach)
```

Add tracking during the quiz loop for:
- `perfect_quiz`: track `all_correct` flag during quiz execution
- `no_hints`: track `hints_used_in_mission` flag
- `perfect_streak`: check `consecutive_correct` across all quiz answers
- `exam_mastered`: count Ch22 missions completed

**Files:** `engine/mission_engine.py`

**Dependencies:** 1.1 (forced hint fix) for `no_hints` to be meaningful.

**Risk:** Low. Logic is contained within the existing achievement check method.

**Testing:**
- Manual: Complete a mission with all quiz questions correct → verify `perfect_quiz` unlocks.
- Manual: Complete Ch1 fully → verify `chapter_1_complete` still works.

---

### 1.4 Bring Dead Player Statistics to Life

**What:** 12 `Player` fields are tracked but never updated.

**How:** Add atomic update calls at the right lifecycle points:

| Field | Where to Update |
|-------|----------------|
| `total_playtime` | Increment in `game_hub()` main loop (every iteration, e.g. +sleep time) |
| `chapter_completion_time` | Record when `chapter_menu()` detects all missions complete |
| `boss_kill_times` | Record in `_run_boss()` on success |
| `speaker_stats` | Increment in `show_story()` or `MissionRunner` story phase |
| `hints_used` | Increment when player actively requests a hint |
| `missions_per_chapter` | Increment on `complete_mission()` |
| `failed_missions` | Populate when `run_terminal()` returns `False` |
| `total_quizzes` | Increment on each quiz question presented |

**Files:** `engine/player.py`, `engine/mission_engine.py`, `main.py`

**Dependencies:** 1.1 (hint system fix) for `hints_used` to be accurate.

**Risk:** Low. All fields are already serialized in `to_dict()` / `from_dict()`. No save format changes.

**Testing:**
- Manual: Play for 5 minutes, save, load → verify `total_playtime` increased.
- Manual: Complete a chapter, verify `chapter_completion_time` is set.

---

### 1.5 Add Levels 16–20

**What:** `LEVELS` stops at 15. Players cap before finishing all content.

**How:** Append to `LEVELS` in `engine/player.py`:

```python
(16, "Kernel Architect",     60000),
(17, "System Overlord",      68000),
(18, "Net Phantom",          77000),
(19, "Root Prophet",         87000),
(20, "Linux Ghost",          98000),
```

**Files:** `engine/player.py`

**Dependencies:** None.

**Risk:** None. Pure data addition. `_recalculate_level()` already handles arbitrary length.

**Testing:**
- Manual: Edit save file to 65,000 XP, load → verify level 16 title displays.

---

### 1.6 Validate Quiz Question `correct` Field

**What:** Some questions may use `int` (0–3) instead of `str` ("A"–"D"). This causes silent failures in exam mode.

**How:** Write a one-shot validation script that audits all 22 chapter files:

```python
# validate_quizzes.py
for ch in CHAPTERS:
    for m in ch[1]:
        for q in m.quiz_questions:
            assert isinstance(q.correct, str), f"{m.mission_id}: correct is {type(q.correct)}"
            assert q.correct in "ABCD", f"{m.mission_id}: correct={q.correct!r}"
            assert len(q.options) == 4, f"{m.mission_id}: {len(q.options)} options"
```

Run it, fix any violations, then remove the defensive `isinstance(q.correct, int)` checks from `timed_exam_mode()` and `review_mode()`.

**Files:** Validation script + `main.py` (lines 1076, 1238)

**Dependencies:** None.

**Risk:** Low. The script is read-only until violations are fixed.

**Testing:**
- Run validation script → expect zero assertions.
- Manual: Run timed exam mode → verify no `IndexError` on `letters[q.correct]`.

---

## Phase 2: Incremental Improvements (Module by Module)

*Timeline: 1 week*
*Goal: Harden individual subsystems with tests and remove hardcoded logic.*

### 2.1 Introduce Unit Tests

**What:** Zero automated tests exist.

**How:** Add a `tests/` directory with pytest (already in `.gitignore`, but not used). Since the project is pure stdlib, pytest must be installed as a dev dependency. Alternatively, write a lightweight `unittest`-based suite to keep zero external dependencies.

**Recommended test modules:**

| Module | What to Test |
|--------|-------------|
| `tests/test_player.py` | `add_xp()`, `gear_bonus()`, `to_dict()`/`from_dict()` round-trip, level boundary conditions |
| `tests/test_mission_engine.py` | `MissionRunner` with mock `Player`, achievement trigger logic, XP math |
| `tests/test_terminal_sim.py` | `get_output()` exact match, prefix match, unknown command, case insensitivity |
| `tests/test_save_system.py` | Save/load round-trip preserves all fields, missing field migration |

**Files:** New `tests/` directory.

**Dependencies:** None for `unittest`. Optional: `pytest` if user approves dev dependency.

**Risk:** Very Low. Tests are additive and live in a separate directory.

**Testing:** N/A (this *is* the testing).

---

### 2.2 Refactor Achievement Checks into Declarative Rules

**What:** `_check_achievements()` is a 70-line wall of nested if-statements. Adding a new achievement requires editing this method.

**How:** Replace inline checks with a rule registry:

```python
class AchievementRule:
    id: str
    check: Callable[[Player, Mission], bool]

RULES = [
    AchievementRule("first_mission", lambda p, m: len(p.completed_missions) == 1),
    AchievementRule("boss_defeated", lambda p, m: m.mtype == "BOSS"),
    # ... etc
]
```

`MissionRunner` iterates `RULES` after each mission. Chapter completion rules are generated dynamically from `CHAPTERS`.

**Files:** `engine/mission_engine.py`, `engine/features.py`

**Dependencies:** Phase 1.3 (missing triggers implemented) — refactor *after* the logic exists, not before.

**Risk:** Medium. Achievement logic is player-visible. A bug here blocks progression satisfaction.

**Testing:**
- Unit: Mock `Player` and `Mission`, verify each rule fires correctly.
- Unit: Verify chapter completion rules are generated for all 22 chapters.

---

### 2.3 Add Save Format Versioning

**What:** Save files have no version field. Future format changes risk data loss.

**How:** Add `"save_version": 1` to `Player.to_dict()`. `from_dict()` checks the version and applies migrations:

```python
@classmethod
def from_dict(cls, d: dict) -> "Player":
    version = d.get("save_version", 0)
    if version < 1:
        # Migrate: old saves didn't have chapter_quiz_stats
        d.setdefault("chapter_quiz_stats", {})
    # ...
    p = cls()
    # ...
    return p
```

**Files:** `engine/player.py`, `engine/save_system.py`

**Dependencies:** Phase 1.4 (dead fields alive) — versioning matters more when data is actually written.

**Risk:** Low. Backward-compatible by design.

**Testing:**
- Unit: Save a player, load it, verify `save_version == 1`.
- Unit: Load a hand-crafted version-0 dict, verify migration path runs.

---

### 2.4 Introduce `RewardPipeline` for XP Calculation

**What:** XP math is inline in `MissionRunner.run()` (`base_xp + quiz_xp`). Gear, hints, and future modifiers are scattered.

**How:** Extract into a small pipeline class:

```python
@dataclass
class RewardPipeline:
    base_xp: int
    quiz_xp: int = 0
    gear_mult: float = 1.0
    hint_penalty: int = 0

    def compute(self) -> int:
        raw = self.base_xp + self.quiz_xp - self.hint_penalty
        return max(0, int(raw * self.gear_mult))
```

`MissionRunner` builds the pipeline and passes it to `player.add_xp()`.

**Files:** `engine/mission_engine.py`

**Dependencies:** Phase 1.2 (gear bonuses wired up) — pipeline generalizes existing logic.

**Risk:** Low. The pipeline is a pure function. Easy to unit test.

**Testing:**
- Unit: `RewardPipeline(base=100, quiz=30, gear_mult=1.2, hint_penalty=20).compute() == 132`

---

### 2.5 Generalize Chapter Menu System

**What:** `game_hub()` has 22 hardcoded `elif choice == "1"` through `"22"` branches.

**How:** Replace with a loop and a lookup:

```python
chapter_ids = [str(c[0]) for c in CHAPTERS]
if choice in chapter_ids:
    chapter_menu(int(choice))
```

**Files:** `main.py` (lines 451–494)

**Dependencies:** None.

**Risk:** Low. Eliminates duplication, no behavior change.

**Testing:**
- Manual: Verify every chapter 1–22 can still be selected.

---

### 2.6 Complete Chapter Recap Map

**What:** `_show_chapter_complete()` has hardcoded recaps for chapters 1–18, but **chapters 19, 20, 21, 22 are missing** (`main.py:616-799`).

**How:** Add recaps for the missing chapters based on their topics (from `CHAPTERS` metadata):

| Chapter | Topic | Key Recap Points |
|---------|-------|-----------------|
| 19 | Container & Virtualization | `docker`, `podman`, `lxc`, `chroot`, cgroups, namespaces |
| 20 | Firewall & Network Security | `iptables`, `nftables`, `firewalld`, VPN basics, `tcpdump` |
| 21 | Network Services | `nfs`, `samba`, `dhcpd`, `bind`, `ldap`, `postfix` |
| 22 | Final Exam | All topics, exam strategy, time management |

**Files:** `main.py`

**Dependencies:** None.

**Risk:** None. Content addition only.

**Testing:**
- Manual: Complete chapters 19–22, verify recap screens appear.

---

## Phase 3: Major Refactoring (Requires Planning)

*Timeline: 1–2 weeks*
*Goal: Restructure subsystems that work but cannot scale. These are internal changes with no player-visible behavior change (unless noted).*

### 3.1 Decouple Display from ANSI stdout

**What:** `engine/display.py` calls `print()` and uses ANSI escape codes directly. Every function is a concrete implementation, not an interface.

**How:** Introduce a `Renderer` protocol and a `ANSIRenderer` implementation:

```python
from typing import Protocol

class Renderer(Protocol):
    def clear(self) -> None: ...
    def text(self, s: str, color: str = "white") -> None: ...
    def box(self, title: str, content: str) -> None: ...
    def prompt(self, text: str) -> str: ...
    def sleep(self, seconds: float) -> None: ...

class ANSIRenderer:
    def clear(self):
        # Platform-appropriate clear using shutil or terminal escape
        ...
    def text(self, s, color="white"):
        print(f"{C.__dict__[color.upper()]}{s}{C.RESET}")
    # ... etc
```

Refactor `engine/display.py` into `renderers/ansi.py`. `main.py` and `mission_engine.py` accept a `renderer: Renderer` parameter instead of importing display functions globally.

**Files:**
- New `renderers/__init__.py`
- New `renderers/ansi.py` (migrated from `engine/display.py`)
- Update `main.py`, `engine/mission_engine.py`, `engine/terminal_sim.py`

**Dependencies:** Phase 2.1 (unit tests) — refactoring without tests is reckless.

**Risk:** **High.** Every screen in the game flows through these functions. A bug in `ANSIRenderer.text()` breaks all output.

**Mitigation:**
- Do not change function signatures or behavior during migration. Move code only.
- Run the full manual test checklist after migration.

**Testing:**
- Unit: Mock `Renderer`, verify `mission_header()` calls `renderer.text()` with expected arguments.
- Manual: Complete one full chapter, verify all screens render correctly.

---

### 3.2 Introduce `ChapterRegistry` for Lazy Loading

**What:** `main.py` imports all 22 chapter files at startup. This is fast at current scale (~11K lines) but prevents dynamic content and procedural generation.

**How:** Create a `ChapterRegistry` that imports on first access:

```python
class ChapterRegistry:
    def __init__(self):
        self._cache: dict[int, list[Mission]] = {}
        self._loaders = {
            1: lambda: __import__("missions.ch01_hardware", fromlist=["CHAPTER_1_MISSIONS"]).CHAPTER_1_MISSIONS,
            # ... 22 entries
        }

    def get(self, ch_id: int) -> list[Mission]:
        if ch_id not in self._cache:
            self._cache[ch_id] = self._loaders[ch_id]()
        return self._cache[ch_id]
```

Replace `CHAPTERS` constant in `main.py` with `registry = ChapterRegistry()`.

**Files:** `engine/chapter_registry.py`, `main.py`

**Dependencies:** Phase 2.1 (unit tests) + Phase 2.5 (menu generalization).

**Risk:** Medium. Startup behavior changes slightly. Import errors surface later (on chapter access, not on game launch).

**Testing:**
- Unit: Verify `registry.get(1)` returns 31 missions.
- Unit: Verify `registry.get(1)` is cached (second call returns same object).
- Manual: Start game, navigate to chapter 22, verify no `ImportError`.

---

### 3.3 Introduce `PlayerEventBus` for Statistics

**What:** `Player` statistics are updated by ad-hoc calls scattered across `MissionRunner`, `main.py`, and `terminal_sim.py`. Adding a new statistic requires finding every relevant call site.

**How:** Centralize through an event bus:

```python
class PlayerEventBus:
    def emit(self, event: PlayerEvent, **kwargs): ...

class Player:
    def on_mission_complete(self, mission: Mission, metadata: dict): ...
    def on_mission_fail(self, mission: Mission): ...
    def on_hint_used(self, level: HintLevel): ...
    def on_quiz_answer(self, chapter: int, correct: bool): ...
```

`MissionRunner` calls `player.on_mission_complete(mission, {...})` once, and the `Player` class updates all derived fields internally.

**Files:** `engine/player.py`, `engine/mission_engine.py`, `engine/features.py`

**Dependencies:** Phase 1.4 (dead fields alive) + Phase 2.1 (unit tests).

**Risk:** Medium. Touches the core data model. A bug here corrupts save data.

**Testing:**
- Unit: Mock `Player`, emit `MISSION_COMPLETE`, verify all relevant counters increment.
- Unit: Verify `to_dict()` includes newly updated fields.

---

### 3.4 Refactor `MissionRunner` into State Machine

**What:** `MissionRunner.run()` is a 300+ line method with sequential phases (story → explanation → task → quiz). Adding a new phase (e.g., "pre-quiz warmup") requires inserting code in the middle.

**How:** Decompose into a state machine:

```python
class MissionRunner:
    PHASES = [
        StoryPhase,
        ExplanationPhase,
        TaskPhase,
        QuizPhase,
        RewardPhase,
    ]

    def run(self, mission: Mission) -> bool:
        state = MissionState(mission, self.player)
        for phase_cls in self.PHASES:
            phase = phase_cls(state, self.renderer)
            if not phase.run():
                return False
        return True
```

Each phase is a small class with a single responsibility.

**Files:** `engine/mission_engine.py` (major rewrite of this file)

**Dependencies:** Phase 3.1 (Renderer protocol) + Phase 2.1 (unit tests).

**Risk:** **High.** This is the heart of the game. A bug in phase ordering breaks every mission.

**Mitigation:**
- Keep the old `run()` method as a thin wrapper calling the new state machine. Remove only after 100% parity is verified.
- Maintain a `PHASE_ORDER` constant that exactly mirrors the current sequence.

**Testing:**
- Unit: Verify each phase class calls the correct renderer methods.
- Unit: Verify `MissionRunner` iterates phases in order.
- Manual: Complete one mission of each type (SCAN, INFILTRATE, QUIZ, BOSS), verify behavior unchanged.

---

## Phase 4: Complete Rewrites (If Necessary)

*Timeline: 2–4 weeks*
*Goal: Replace subsystems that have reached their architectural limit. These are destructive changes that require the prior phases to be complete and stable.*

### 4.1 Terminal Simulator: Stateful REPL

**Why rewrite:** The current `SIMULATED_OUTPUTS` dictionary (4,457 lines) cannot support:
- Multi-step missions (e.g., "create user → set password → verify")
- Command pipelines (`grep error /var/log/syslog | wc -l`)
- State-dependent output (`ls` after `touch foo`)
- Directory navigation (`cd /etc && ls`)

**What to keep:** The string dictionary becomes a *fallback* for read-only commands (`lspci`, `dmesg`, `uname -a`). These commands don't need state.

**Architecture:**

```
engine/terminal/
├── __init__.py
├── simulator.py          # Entry point: run_terminal()
├── filesystem.py         # FakeFilesystem, Node, File, Directory
├── parser.py             # CommandParser, PipelineParser
├── commands/             # Individual command implementations
│   ├── __init__.py
│   ├── base.py           # Command base class
│   ├── ls.py             # Stateful: reads filesystem
│   ├── cat.py            # Stateful: reads file content
│   ├── touch.py          # Stateful: mutates filesystem
│   ├── mkdir.py          # Stateful: mutates filesystem
│   ├── grep.py           # Stateful: reads + filters
│   └── static.py         # Fallback to SIMULATED_OUTPUTS
```

**Files:**
- New `engine/terminal/` package
- Migrate relevant strings from `engine/terminal_sim.py`
- Deprecate `engine/terminal_sim.py` (remove after parity)

**Dependencies:**
- Phase 2.1 (unit tests) — critical for verifying parity
- Phase 3.1 (Renderer protocol) — terminal output goes through renderer
- Phase 3.4 (MissionRunner state machine) — task phase needs clean simulator interface

**Risk:** **Very High.** The terminal simulator is the game's primary interactive mechanic. Breaking it breaks the entire experience.

**Mitigation:**
- Run old and new simulators side-by-side for every command in `SIMULATED_OUTPUTS`. Verify output matches character-for-character.
- Introduce a `TERMINAL_BACKEND` env var to toggle between old and new during transition.
- Rewrite only the *interactive* commands (`ls`, `cd`, `touch`, `mkdir`, `rm`, `cat`, `echo`, `grep`, `find`). Keep read-only commands as dictionary lookups.

**Testing:**
- Unit: `FakeFilesystem` CRUD operations.
- Unit: Each command class (`LsCommand`, `CatCommand`, etc.) with mock filesystem.
- Integration: Full multi-step mission using new simulator.
- Manual: Play 5 missions of each type, verify no regression.

---

### 4.2 Mission Content Format: JSON/YAML

**Why rewrite:** Missions are pure Python in 22 `.py` files. This means:
- Content creators must know Python
- No edit-time validation (typos in `correct="A"` only surface at runtime)
- No content tooling (no mission editor, no automated audit)
- Import-time overhead
- Git diffs for content changes are noisy (Python syntax)

**Architecture:**

```
content/
├── chapters/
│   ├── ch01_hardware.json      # 31 missions
│   ├── ch02_boot.json
│   └── ...
└── schema/
    └── mission_schema.json     # JSON Schema for validation

engine/
├── mission_loader.py           # JSON -> Mission dataclass
└── mission_validator.py        # Schema validation + custom rules
```

**Migration strategy:**
1. Build `MissionLoader` that reads JSON and produces identical `Mission` objects
2. Write `migrate.py` that imports all 22 chapter `.py` files and dumps them as JSON
3. Verify round-trip: JSON → Mission → dict → compare to original
4. Switch `ChapterRegistry` to load JSON instead of Python
5. Keep `.py` files in repo until v1.5 is stable, then archive

**JSON structure (one mission):**

```json
{
  "mission_id": "1.01",
  "title": "Erste Signale — Was ist Hardware?",
  "mtype": "SCAN",
  "xp": 30,
  "chapter": 1,
  "speaker": "ZARA Z3R0",
  "story": "Ich hab dich bewusstlos...",
  "quiz_questions": [
    {
      "question": "Was zeigt lspci?",
      "options": ["A) USB-Geräte", "B) PCI-Geräte", "C) CPU-Info", "D) Netzwerk-Status"],
      "correct": "B",
      "explanation": "lspci listet PCI-Bus-Geräte.",
      "xp_value": 15
    }
  ],
  "hints": ["Denke an den Bus.", "PCI Express.", "lspci = PCI list"]
}
```

**Files:**
- New `content/chapters/*.json`
- New `engine/mission_loader.py`
- New `engine/mission_validator.py`
- New `tools/migrate_missions.py`
- Deprecate `missions/*.py`

**Dependencies:**
- Phase 2.1 (unit tests)
- Phase 3.2 (ChapterRegistry)
- Phase 3.4 (MissionRunner state machine)

**Risk:** **High.** Content is the game's value. Corrupting a mission file means losing authored work.

**Mitigation:**
- `migrate.py` is read-only (never edits `.py` files).
- JSON is validated against schema before the game loads it.
- Keep `.py` files in git history forever (they are the source of truth until JSON is verified).
- The `Mission` dataclass remains the runtime representation — only the *authoring* format changes.

**Testing:**
- Unit: `MissionLoader` produces `Mission` with all fields correct.
- Unit: `MissionValidator` catches missing `mission_id`, wrong `correct` value, etc.
- Integration: Load all 22 JSON chapters, verify mission count = 501.
- Manual: Play one mission from each chapter, verify behavior unchanged.

---

### 4.3 Networking Layer (Future v2.0)

**Why rewrite:** The game is purely offline. CLAUDE.md lists "Network multiplayer (compare progress, faction wars)" as a future enhancement.

**What this entails:** This is **not a rewrite of existing code** but a new subsystem:

```
engine/
├── network/
│   ├── __init__.py
│   ├── client.py           # HTTP client for leaderboard API
│   ├── leaderboard.py      # Local cache + sync
│   └── sync.py             # Save file cloud sync
```

**Dependencies:**
- Phase 4.2 (JSON mission format) — server needs to validate mission IDs
- Phase 3.3 (PlayerEventBus) — sync events to server

**Risk:** Not applicable until v2.0. Out of scope for current closure plan.

**Testing:** N/A.

---

## Cross-Phase Concerns

### Testing Strategy Summary

| Phase | Primary Testing | Secondary Testing |
|-------|----------------|-------------------|
| 1 (Quick Wins) | Manual playthrough of affected features | Ad-hoc save/load verification |
| 2 (Incremental) | `unittest` / `pytest` for all new logic | Manual regression of full chapter |
| 3 (Refactoring) | Unit tests for every moved function | Manual visual verification of all screens |
| 4 (Rewrites) | Side-by-side output comparison | Full playthrough of all 501 missions |

### Rollback Strategy

- **Phase 1–2:** All changes are backward-compatible. Rollback via `git revert`.
- **Phase 3:** Keep old implementations alongside new ones during transition. Toggle via env vars or feature flags.
- **Phase 4:** Old implementations remain in repo until new ones are 100% verified. Delete only after v1.5 release.

### Definition of Done (per phase)

- **Phase 1:** All quick-win items are manually verified. Save files from before Phase 1 still load correctly.
- **Phase 2:** Unit test suite passes. Code coverage >60% for `engine/*.py`.
- **Phase 3:** All manual test checklist items pass. No player-visible regressions.
- **Phase 4:** Automated parity tests pass (JSON round-trip, terminal output comparison). Full manual playthrough of all 22 chapters.

---

## Appendix: Manual Test Checklist

This checklist must pass after every phase:

- [ ] Start new game from scratch
- [ ] Complete Ch01 fully (all missions)
- [ ] Verify XP calculations and level progression
- [ ] Test hint system (all 3 tiers for 1 mission)
- [ ] Verify save/load cycle preserves state exactly
- [ ] Complete a BOSS mission, verify gear drops
- [ ] Verify achievement unlocks (trigger + display + XP reward)
- [ ] Check no console warnings/errors
- [ ] Verify ASCII art renders cleanly in terminal
- [ ] Verify all speaker names consistent
- [ ] Spot-check 5 random quiz questions for accuracy
- [ ] Verify `review_mode()` works
- [ ] Verify `timed_exam_mode()` completes without crash
- [ ] Load an old save file (from before current phase)
