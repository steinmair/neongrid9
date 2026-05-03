# NeonGrid-9 Implementation Roadmap

**Version:** 1.0  
**Date:** 2026-05-02  
**Last Updated:** 2026-05-02  
**Scope:** Full codebase transformation — from content-complete to mechanically complete  
**Sources:** `gap_analysis.md`, `gap_closure_plan.md`, `refactoring_opportunities.md`, `cleanup_inventory.md`, `smoke_tests/check_what_is_working/report.md`

---

## Philosophy

**"Fix before you refactor. Refactor before you extend. Test after every change."**

Each phase must leave the codebase in a **runnable, shippable state**. No phase depends on the next phase being complete. Smoke tests run after every significant change.

**Golden Rule:** If a refactor breaks a smoke test, the refactor is wrong.

---

## Legend

| Field | Meaning |
|-------|---------|
| **ID** | Unique identifier for tracking (e.g., A.1, B.3) |
| **Task** | What to do |
| **Files** | Specific files/modules affected |
| **Depends On** | Prerequisites that must be completed first |
| **Success Criteria** | How to verify completion |
| **Time** | Estimated effort (in developer-days, assuming 1 day = ~6 focused hours) |
| **Risk** | Probability and impact of regression: Low / Medium / High |

---

# Phase A — Foundation (Week 1–2)

**Goal:** Clean up dead code, fix broken data, establish the two critical abstractions that unlock all testing, and create a CI safety net.

**Motto:** *"Make the codebase honest before making it beautiful."*

---

### A.1 Remove Unused Imports and Dead Functions [DONE]

**Task:** Delete genuinely dead code identified in `cleanup_inventory.md`.

**Files:**
- `main.py` — remove imports: `LEVELS`, `show_story`, `show_info`, `header`, `slow_print`, `box` (line 26–29)
- `engine/mission_engine.py` — remove `HintLevel` from import line 18
- `engine/terminal_sim.py` — remove `slow_print` from import line 9
- `engine/display.py` — remove `slow_print()` (line 50), `show_progress()` (line 253), `box()` (line 57)
- Update `smoke_tests/check_what_is_working/test_05_display_and_features.py` — remove `box()` test case or replace with `typewrite()` test

**Depends On:** Nothing.

**Success Criteria:**
- All 5 smoke tests still pass (or 4/5 if `box()` test is intentionally removed).
- `python3 main.py` starts without `ImportError`.
- `grep -rn "slow_print\|show_progress\|box(" engine/ main.py` returns zero hits outside definitions.

**Time:** 0.5 day

**Risk:** Low. No logic changes. Only deletion of confirmed-dead code.

---

### A.2 Fix Quiz `correct` Field Type (Data Migration) [DONE]

**Task:** Convert all quiz questions where `correct` is `int` (0–3) to `str` ("A"–"D"). This affects 727 of 1,169 questions.

**Files:** All 22 `missions/ch*.py` files.

**Method:**
1. Write a one-shot migration script `tools/fix_quiz_types.py` that:
   - Imports each chapter's `CHAPTER_N_MISSIONS`
   - Finds `QuizQuestion(correct=0)` etc.
   - Prints the exact file, line, and replacement needed
2. Apply replacements via `sed` or the script itself
3. Remove defensive `isinstance(q.correct, int)` checks in `engine/mission_engine.py` (line 374) and `main.py` (lines 1076, 1238)

**Depends On:** Nothing.

**Success Criteria:**
- `python3 smoke_tests/check_what_is_working/test_03_mission_engine.py` reports **zero** quiz integrity failures.
- `python3 -c "from main import CHAPTERS; ..."` with an assertion that `all(isinstance(q.correct, str) for ...)` passes.

**Time:** 1 day

**Risk:** Low. Mechanical find-and-replace. The data model already expects `str`; we are aligning reality with the spec.

---

### A.3 Add Missing Gear Items to `GEAR_CATALOG` [DONE]

**Task:** Define three missing gear items referenced as BOSS rewards but absent from `GEAR_CATALOG`.

**Files:** `engine/player.py` (line 30, inside `GEAR_CATALOG`)

**Items to add:**
```python
"storage_master_badge": {
    "name": "Storage Master Badge",
    "desc": "+10% XP auf Storage- und LVM-Missionen.",
    "boost": "storage_xp",
    "rarity": "rare",
    "tier": 3,
    "source": "Boss-Drop: Kap. 18",
},
"firewall_dominion_badge": {
    "name": "Firewall Dominion Badge",
    "desc": "+10% XP auf Firewall- und Security-Missionen.",
    "boost": "firewall_xp",
    "rarity": "rare",
    "tier": 3,
    "source": "Boss-Drop: Kap. 20",
},
"net_runners_badge": {
    "name": "Net Runners Badge",
    "desc": "+10% XP auf Netzwerk-Service-Missionen.",
    "boost": "net_xp",
    "rarity": "rare",
    "tier": 3,
    "source": "Boss-Drop: Kap. 21",
},
```

**Depends On:** Nothing.

**Success Criteria:**
- `smoke_tests/check_what_is_working/test_03_mission_engine.py` no longer warns about missing gear rewards.
- `python3 -c "from engine.player import GEAR_CATALOG; assert 'storage_master_badge' in GEAR_CATALOG"` passes.

**Time:** 0.5 day

**Risk:** None. Pure data addition.

---

### A.4 Add Missing BOSS Metadata (Chapters 8–22) [DONE]

**Task:** Add `boss_name` and `boss_desc` to the 15 BOSS missions that use lowercase `.boss` suffix and lack these fields.

**Files:** `missions/ch08_regex_vi.py` through `missions/ch22_exam.py` (15 files).

**Approach:**
1. Derive `boss_name` from the chapter title (e.g., Ch9 → "NET PROTOCOL OVERLORD").
2. Write a generic `boss_desc` template: `"Final challenge for {chapter_title}. All concepts combined."`
3. Hand-tune the first 3–5 for narrative flavor; keep the rest templated.

**Depends On:** Nothing.

**Success Criteria:**
- `smoke_tests/check_what_is_working/test_03_mission_engine.py` reports **zero** BOSS structure problems.
- All 22 BOSS missions have non-empty `boss_name` and `boss_desc`.

**Time:** 1 day

**Risk:** Low. Content-only change; no code logic affected.

---

### A.5 Implement Renderer Protocol (RO-01) [DONE]

**Task:** Introduce a `Renderer` protocol so display functions are mockable. This is the single most important refactor for testability.

**Files:**
- New: `engine/renderer.py` — `Renderer` Protocol + `TerminalRenderer` + `NullRenderer`
- Modify: `engine/display.py` — keep existing functions as private helpers for `TerminalRenderer`
- Modify: `engine/mission_engine.py` — add `renderer: Renderer` parameter to `MissionRunner.__init__()`
- Modify: `engine/terminal_sim.py` — replace direct `print()` calls with renderer methods
- Modify: `main.py` — instantiate `TerminalRenderer()` and pass it through

**Depends On:** A.1 (dead code removal to reduce noise).

**Success Criteria:**
- `python3 main.py` runs identically to before (visual inspection of boot sequence + main menu).
- A new test `tests/test_renderer.py` can instantiate `NullRenderer`, call `show_success("test")`, and assert `"test"` is in the buffer.
- `MissionRunner` can be instantiated with `NullRenderer` and `run()` produces no stdout.

**Time:** 2 days

**Risk:** Medium. Touches every display call site. The smoke tests are the safety net.

---

### A.6 Implement Save Storage Repository (RO-02) [DONE]

**Task:** Replace hardcoded home-directory JSON paths with a `SaveRepository` protocol. This unblocks isolated save/load testing.

**Files:**
- New: `engine/storage.py` — `SaveRepository` Protocol, `JsonFileRepository`, `InMemoryRepository`
- Modify: `engine/save_system.py` — refactor functions into `JsonFileRepository` methods
- Modify: `main.py` — `GameState` accepts `repository: SaveRepository`
- New: `tests/test_storage.py` — round-trip tests using `InMemoryRepository`

**Depends On:** Nothing.

**Success Criteria:**
- All existing save/load behavior preserved (manual test: save → quit → load).
- `InMemoryRepository` round-trip test passes without touching the filesystem.
- `JsonFileRepository` still writes to the existing directory and existing saves remain compatible.

**Time:** 1.5 days

**Risk:** Low. The protocol wraps existing behavior; no save format changes yet.

---

### A.7 Typed Configuration (RO-08) [DONE]

**Task:** Convert module-level dicts/tuples into frozen dataclasses for type safety and IDE autocomplete.

**Files:**
- Modify: `engine/player.py` — add `LevelConfig` and `GearItem` dataclasses; convert `LEVELS` and `GEAR_CATALOG`
- Modify: `engine/features.py` — `AchievementConfig` dataclass; convert `ACHIEVEMENTS`

**Depends On:** Nothing.

**Success Criteria:**
- `python3 -c "from engine.player import GEAR_CATALOG; print(GEAR_CATALOG['ghost_mask'].tier)"` works and returns `3`.
- `mypy engine/player.py` (if installed) reports no errors on the new dataclasses.
- `python3 main.py` still runs.

**Time:** 1 day

**Risk:** Very Low. Pure data structure transformation.

---

### A.8 Add Levels 16–20 to `LEVELS` [DONE]

**Task:** Extend the leveling table so players don't cap at 15 before completing all content.

**Files:** `engine/player.py` (line 11, `LEVELS` list)

**Data to append:**
```python
(16, "Kernel Architect",     60000),
(17, "System Overlord",      68000),
(18, "Net Phantom",          77000),
(19, "Root Prophet",         87000),
(20, "Linux Ghost",          98000),
```

**Depends On:** A.7 (typed config, so `LevelConfig` is the target structure).

**Success Criteria:**
- `_recalculate_level()` correctly maps 65,000 XP → level 16.
- `Player.get_next_level_xp()` returns 68,000 for a level-16 player.
- `python3 main.py` + manual save edit to 70,000 XP → verify title "System Overlord".

**Time:** 0.25 day

**Risk:** None.

---

### A.9 Establish CI Test Runner [DONE]

**Task:** Create a script that runs all smoke tests and reports a single pass/fail summary.

**Files:**
- New: `.github/workflows/smoke.yml` — GitHub Actions workflow (or `run_smoke_tests.sh` if not using GitHub)
- New: `scripts/run_smoke_tests.py` — orchestrates all 5 test files, prints summary table

**Depends On:** A.5 (Renderer) and A.6 (Storage) — CI must test the new abstractions.

**Success Criteria:**
- `python3 scripts/run_smoke_tests.py` exits with code 0 and prints: `"25/25 cases passed"`.
- The script runs in a clean environment (no home save directory required).

**Time:** 0.5 day

**Risk:** Low. CI is additive.

---

## Phase A Summary

| ID | Task | Time | Risk |
|----|------|------|------|
| A.1 | Remove dead code | 0.5 d | Low |
| A.2 | Fix quiz `correct` types | 1.0 d | Low |
| A.3 | Add missing gear items | 0.5 d | None |
| A.4 | Add BOSS metadata | 1.0 d | Low |
| A.5 | Renderer Protocol | 2.0 d | Medium |
| A.6 | Save Repository | 1.5 d | Low |
| A.7 | Typed Configuration | 1.0 d | Very Low |
| A.8 | Levels 16–20 | 0.25 d | None |
| A.9 | CI Test Runner | 0.5 d | Low |
| **Total** | | **~8.25 days** | |

**Phase A Exit Criteria:**
- All 5 smoke tests pass (25/25 cases).
- `NullRenderer` and `InMemoryRepository` exist and are tested.
- Zero dead code remains (verified by `cleanup_inventory.md` checklist).
- Save/load still works with existing saves.

---

# Phase B — Core Refactoring (Week 3–4)

**Goal:** Decouple the engine into testable, replaceable units. The two critical abstractions from Phase A (Renderer + Storage) make everything here possible.

**Motto:** *"Every module should be replaceable without breaking the game."*

---

### B.1 Achievement Rule Engine (RO-03) [DONE]

**Task:** Replace the 70-line inline achievement wall in `MissionRunner.run()` with a declarative rule registry.

**Files:**
- New: `engine/achievement_engine.py` — `AchievementRule`, `AchievementEngine`
- Modify: `engine/mission_engine.py` — remove inline achievement checks (lines 240–311), call `AchievementEngine.check()`
- New: `tests/test_achievement_engine.py` — unit tests for every rule

**Depends On:** A.5 (Renderer Protocol — achievements call `show_achievements()`, which must be mockable).

**Success Criteria:**
- `AchievementEngine` has a `RULES` list where adding an achievement is one line.
- `MissionRunner.run()` shrinks by ~70 lines.
- All existing achievements still trigger at the same conditions (verified by unit tests).
- `chapter_N_complete` rules are generated dynamically for all 22 chapters.

**Time:** 2 days

**Risk:** Medium. Achievement logic is player-visible. A bug blocks progression satisfaction.

---

### B.2 Wire Up Gear XP Bonuses [DONE]

**Task:** Call `Player.gear_bonus()` in `MissionRunner.run()` so gear is not cosmetic.

**Files:** `engine/mission_engine.py` (around line 230, XP calculation)

**Implementation:**
```python
bonus_key = {
    "SCAN": "scan_xp", "QUIZ": "quiz_xp",
    "INFILTRATE": "admin_xp", "CONSTRUCT": "pipe_xp",
    "REPAIR": "pipe_xp", "DECODE": "regex_xp", "BOSS": "all_xp",
}.get(mission.mtype)
if bonus_key:
    total_xp = int(total_xp * self.player.gear_bonus(bonus_key))
```

**Depends On:** A.3 (missing gear items must exist first) and A.7 (typed `GearItem` config).

**Success Criteria:**
- Unit test: `Player` with `ghost_mask` + QUIZ mission → `gear_bonus("quiz_xp")` returns `1.2`, XP is multiplied.
- Unit test: `linux_badge` stacks +5% additively on top of other bonuses.
- Manual: Equip `ghost_mask`, complete a QUIZ mission, verify XP is 1.2×.

**Time:** 0.5 day

**Risk:** Low. Purely additive. Missing bonus key defaults to 1.0 (no change).

---

### B.3 MissionRunner Phase Extraction (RO-05) [DONE]

**Task:** Decompose `MissionRunner.run()` from a 260-line god method into discrete, independently testable phases.

**Files:**
- New: `engine/mission_phases.py` — `MissionPhase` Protocol + implementations:
  `StoryPhase`, `ExplanationPhase`, `TerminalTaskPhase`, `QuizPhase`, `XPRewardPhase`, `AchievementPhase`, `RewardPhase`
- Modify: `engine/mission_engine.py` — `MissionRunner` becomes a phase orchestrator
- New: `tests/test_mission_phases.py` — unit test each phase with mock `MissionContext`

**Depends On:** A.5 (Renderer Protocol) and B.1 (Achievement Engine).

**Success Criteria:**
- `XPRewardPhase` can be tested in isolation with 10 boundary cases (failed mission → 1/3 XP, first-attempt success → 1.2×, etc.).
- `TerminalTaskPhase` can be tested with mock terminal input.
- `MissionRunner.run()` is under 60 lines of orchestration code.
- Smoke tests still pass.

**Time:** 3 days

**Risk:** High. This is the heart of the game engine. The smoke tests are the primary safety net.

---

### B.4 Dependency Injection for GameState (RO-07) [DONE]

**Task:** Replace the `GAME = GameState()` module-level singleton with explicit `GameSession` parameter passing.

**Files:** `main.py` (all menu and game-loop functions)

**Implementation:**
```python
@dataclass
class GameSession:
    player: Player
    renderer: Renderer
    repository: SaveRepository
    running: bool = True

def game_hub(session: GameSession) -> None:
    ...

def chapter_menu(session: GameSession, ch_id: int) -> None:
    runner = MissionRunner(session.player, renderer=session.renderer,
                           save_callback=lambda p: session.repository.save(p, 1))
```

**Depends On:** A.5 (Renderer) and A.6 (Storage Repository).

**Success Criteria:**
- `main.py` contains no module-level `GAME` variable.
- `python3 main.py` starts a new game and completes a full chapter without error.
- A unit test can create `GameSession(player=mock_player, renderer=NullRenderer(), repository=InMemoryRepository())` and call `game_hub()` without side effects.

**Time:** 1.5 days

**Risk:** Medium. Mechanical but touches ~60 call sites. Easy to miss a reference.

---

### B.5 Menu Builder Abstraction (RO-06) [DONE]

**Task:** Replace 5+ hand-rolled menu functions with a declarative `Menu` class.

**Files:**
- New: `engine/menus.py` — `Menu`, `MenuItem`
- Modify: `main.py` — replace `main_menu()`, `load_game_menu()`, `manage_saves_menu()`, `game_hub()` choice branches
- New: `tests/test_menus.py` — test menu dispatch logic

**Depends On:** B.4 (DI — menus need a `Renderer` to display).

**Success Criteria:**
- Adding a new menu item is one line (`menu.add("x", "Review", review_mode)`).
- The 22-branch `if/elif` chapter selection in `game_hub()` collapses to a loop.
- `Menu.run()` returns the selected key; `Menu.dispatch()` calls the action.
- Smoke tests still pass.

**Time:** 1.5 days

**Risk:** Low. Menus are leaf nodes.

---

### B.6 Terminal Command Registry — Architecture (RO-04) [DONE]

**Task:** Lay the foundation for replacing the 4,457-line `SIMULATED_OUTPUTS` dictionary with a `CommandRegistry`.

**Files:**
- New: `engine/command_registry.py` — `TerminalCommand` Protocol, `CommandRegistry`, `TermState`
- New: `engine/commands/` package — individual command modules (start with 10 most-used)
  - `engine/commands/lspci.py`, `lsusb.py`, `uname.py`, `lsblk.py`, `dmesg.py`
- Modify: `engine/terminal_sim.py` — add `CommandRegistry` as primary lookup, keep `SIMULATED_OUTPUTS` as fallback
- New: `tests/test_commands.py` — unit test each command class in isolation

**Depends On:** Nothing from this phase; can be done in parallel with B.1–B.5.

**Success Criteria:**
- `CommandRegistry.lookup("lspci")` returns the `LspciCommand` instance and its output.
- `get_output("lspci")` still works (backward compatibility via fallback).
- `LspciCommand.run([], state)` is unit-testable without importing the full terminal simulator.

**Time:** 2 days

**Risk:** Medium. This is a new architecture alongside legacy code. The fallback keeps things safe.

---

### B.7 Chapter Registry (RO-09) [DONE]

**Task:** Auto-discover chapters so adding Ch23 requires zero edits to `main.py`.

**Files:**
- New: `engine/chapter_registry.py` — `ChapterRegistry` with `discover()` method
- Modify: each `missions/ch*.py` — add `CHAPTER_META` dict at module level
- Modify: `main.py` — replace hardcoded `CHAPTERS` list with `registry = ChapterRegistry(); registry.discover("missions")`

**Depends On:** Nothing.

**Success Criteria:**
- `registry.all_chapters()` returns 22 chapters in the correct order.
- `main.py` no longer imports `CHAPTER_1_MISSIONS` through `CHAPTER_22_MISSIONS` individually.
- Adding a hypothetical `ch23_test.py` with `CHAPTER_META` makes it appear automatically.

**Time:** 1 day

**Risk:** Low. Import mechanics are well-understood in Python.

---

## Phase B Summary

| ID | Task | Time | Risk |
|----|------|------|------|
| B.1 | Achievement Rule Engine | 2.0 d | Medium |
| B.2 | Gear XP Bonuses | 0.5 d | Low |
| B.3 | MissionRunner Phases | 3.0 d | High |
| B.4 | Dependency Injection | 1.5 d | Medium |
| B.5 | Menu Builder | 1.5 d | Low |
| B.6 | Terminal Command Registry (arch) | 2.0 d | Medium |
| B.7 | Chapter Registry | 1.0 d | Low |
| **Total** | | **~11.5 days** | |

**Phase B Exit Criteria:**
- `MissionRunner` is under 60 lines of orchestration.
- `AchievementEngine` has declarative rules for all 19 achievements.
- `GameSession` is passed explicitly; no global `GAME` singleton.
- `CommandRegistry` exists and handles the top 10 terminal commands.
- All smoke tests pass (25/25).
- New unit tests exist for: Renderer, Storage, Achievements, Mission Phases, Menus, Commands.

---

# Phase C — Gap Filling (Week 5–8)

**Goal:** Implement the missing concepts identified in `gap_analysis.md`. Start with player-facing fixes, finish with content polish.

**Motto:** *"Make the game work the way the design document says it does."*

---

### C.1 Fix Forced Hint Anti-Pattern [DONE]

**Task:** Replace the auto-hint loop with player-initiated hint requests.

**Files:** `engine/mission_phases.py` — `TerminalTaskPhase` (the refactored version from B.3)

**Current behavior:** On wrong answer, the game automatically shows a hint and deducts XP.

**New behavior:** After wrong answer, prompt: `"[h] Hint anfordern | [Enter] Erneut versuchen | [q] Aufgeben"`. Only deduct XP when the player actively chooses `[h]`.

**Depends On:** B.3 (MissionRunner Phase Extraction — the hint logic lives in `TerminalTaskPhase`).

**Success Criteria:**
- Manual test: Enter a wrong command in a SCAN mission → game asks, not tells.
- XP is only deducted when `[h]` is pressed.
- `no_hints` achievement becomes meaningful (track `hints_used_in_mission` flag).

**Time:** 1 day

**Risk:** Low. Changes only the input loop inside one phase.

---

### C.2 Implement Missing Achievement Triggers [DONE]

**Task:** Add trigger logic for the 8 achievements that currently have zero checks.

**Files:** `engine/achievement_engine.py` (rules list from B.1)

**Achievements to wire up:**

| Achievement | Trigger Condition | Where to Track |
|-------------|-------------------|----------------|
| `perfect_quiz` | All quiz questions correct in one mission | `QuizPhase` result aggregate |
| `no_hints` | Mission completed with 0 hints used | `TerminalTaskPhase` hint counter |
| `perfect_streak` | 10 consecutive correct quiz answers | `Player.correct_first_try` across missions |
| `speedrun` | Chapter completed in <1 hour | `chapter_completion_time` (C.3) |
| `lore_collector` | All story sections viewed in a chapter | `Player` field or mission replay tracking |
| `faction_max` | Any faction reaches 100 reputation | `add_reputation()` boundary check |
| `exam_mastered` | All Ch22 missions completed | `chapter_menu()` completion check for ch=22 |
| `jackpot` | 1000+ XP earned in one session | `game_hub()` XP delta tracker |

**Depends On:** B.1 (Achievement Rule Engine), C.1 (hint tracking for `no_hints`).

**Success Criteria:**
- Unit test: mock `Player` with 10 consecutive correct answers → `perfect_streak` unlocks.
- Unit test: mock `Player` with 100 reputation in one faction → `faction_max` unlocks.
- All 19 achievements have at least one unit test verifying their trigger condition.

**Time:** 2 days

**Risk:** Medium. Player-facing progression. Must not accidentally make achievements too easy or impossible.

---

### C.3 Wire Up Dead Player Statistics [DONE]

**Task:** Make the 12 dead `Player` fields actually update during gameplay.

**Files:**
- `engine/player.py` — fields already exist
- `engine/mission_phases.py` — update at lifecycle points
- `main.py` — `game_hub()` loop timer

**Update plan:**

| Field | Update Location | Implementation |
|-------|-----------------|----------------|
| `total_playtime` | `game_hub()` loop | `time.time()` delta each iteration |
| `chapter_completion_time` | `chapter_menu()` end | `time.time() - chapter_start` |
| `boss_kill_times` | `MissionRunner._run_boss()` | `time.time() - boss_start` |
| `speaker_stats` | `StoryPhase.run()` | `player.speaker_stats[speaker] += 1` |
| `hints_used` | `TerminalTaskPhase` | Increment on active hint request (C.1) |
| `missions_per_chapter` | `XPRewardPhase.run()` | `player.missions_per_chapter[ch] += 1` |
| `failed_missions` | `TerminalTaskPhase` | `player.failed_missions[mid] += 1` on failure |
| `total_quizzes` | `QuizPhase.run()` | `player.total_quizzes += len(questions)` |
| `secrets_found` | **Deferred** | No secret system exists yet; leave at 0 |
| `days_played` | **Deferred** | Requires daily login tracking; leave at 1 |
| `streak` | **Deferred** | Requires daily login tracking; leave at 0 |

**Depends On:** B.3 (Phase Extraction), C.1 (Hint system fix for `hints_used`).

**Success Criteria:**
- Manual: Play for 5 minutes, save, load → `total_playtime` > 0.
- Manual: Complete a chapter → `chapter_completion_time[ch]` is set.
- Manual: View a story segment → `speaker_stats[speaker]` increments.
- Unit test: `QuizPhase` with 3 questions → `player.total_quizzes == 3`.

**Time:** 1.5 days

**Risk:** Low. All fields already serialize; we are just adding write sites.

---

### C.4 Fix `display_lens` Gear Effect [DONE]

**Task:** Make the `display_lens` gear item actually do what its description says.

**Files:** `main.py` — `review_mode()` (around line 1187)

**Current behavior:** `review_mode()` always shows explanations *after* the player answers wrong.

**New behavior:** If `display_lens` is in `player.inventory`, show the explanation *before* revealing whether the answer was correct.

**Depends On:** C.3 (Player inventory tracking is reliable).

**Success Criteria:**
- Manual: Equip `display_lens`, enter review mode, answer a wrong question → explanation appears before the "✗ Falsch" message.
- Without `display_lens`, the old behavior (explanation after) remains.

**Time:** 0.5 day

**Risk:** Low. One conditional in one function.

---

### C.5 Terminal Command Registry — Full Migration [DONE]

**Task:** Migrate the remaining ~777 terminal commands from `SIMULATED_OUTPUTS` into `CommandRegistry` classes.

**Files:**
- New: `engine/commands/*.py` — one module per command family (e.g., `network.py`, `filesystem.py`, `processes.py`)
- Modify: `engine/terminal_sim.py` — gradually shrink `SIMULATED_OUTPUTS`

**Approach:**
- Week 5: Migrate Ch1–Ch7 commands (hardware, boot, init, partitions, permissions, shell, processes)
- Week 6: Migrate Ch8–Ch14 commands (regex/vi, network, users, logging, packages, kernel, scripting)
- Week 7: Migrate Ch15–Ch22 commands (security, locale, shell env, storage, containers, firewall, services, exam)
- Week 8: Remove legacy `SIMULATED_OUTPUTS` fallback once all commands are migrated

**Depends On:** B.6 (Registry architecture).

**Success Criteria:**
- `SIMULATED_OUTPUTS` dictionary is empty (or removed).
- All 787+ commands are reachable via `CommandRegistry.lookup()`.
- `get_output()` delegates to `registry.lookup()` exclusively.
- Smoke test `test_04_terminal_simulator.py` still passes.

**Time:** 4 days (spread across Week 5–8, ~1 day per batch)

**Risk:** Medium. Large volume of data migration. Risk of losing a command or corrupting its output.

---

### C.6 Data-Driven Chapter Recaps [DONE]

**Task:** Move the hardcoded `recap_map` from `main.py` into chapter files.

**Files:**
- Modify: each `missions/ch*.py` — add `CHAPTER_RECAP: list[str]`
- Modify: `main.py` — `_show_chapter_complete()` reads recap from chapter metadata

**Depends On:** B.7 (Chapter Registry — recaps are chapter metadata).

**Success Criteria:**
- `main.py` contains no `recap_map` dictionary.
- `_show_chapter_complete(ch_id)` looks up `registry.get_chapter(ch_id).recap`.
- All 22 chapter recaps display identically to before.

**Time:** 0.5 day

**Risk:** None. Content relocation.

---

### C.7 Generalize Chapter Completion Achievements [DONE]

**Task:** Ensure every chapter (1–22) has a `chapter_N_complete` achievement that fires when 100% of its missions are done.

**Files:**
- `engine/achievement_engine.py` — dynamically generate rules from `CHAPTERS`
- `engine/features.py` — add `chapter_2_complete` through `chapter_22_complete` to `ACHIEVEMENTS`

**Depends On:** B.1 (Achievement Rule Engine), B.7 (Chapter Registry).

**Success Criteria:**
- Completing all missions in Ch2 unlocks `chapter_2_complete`.
- Completing all missions in Ch22 unlocks `chapter_22_complete`.
- `chapter_master` triggers when 5 chapters are 100% complete (not just "have any progress").

**Time:** 0.5 day

**Risk:** Low. Rule generation is mechanical.

---

## Phase C Summary

| ID | Task | Time | Risk |
|----|------|------|------|
| C.1 | Fix forced hints | 1.0 d | Low |
| C.2 | Missing achievement triggers | 2.0 d | Medium |
| C.3 | Wire up Player statistics | 1.5 d | Low |
| C.4 | `display_lens` gear effect | 0.5 d | Low |
| C.5 | Terminal migration (full) | 4.0 d | Medium |
| C.6 | Data-driven recaps | 0.5 d | None |
| C.7 | Chapter completion achievements | 0.5 d | Low |
| **Total** | | **~10 days** | |

**Phase C Exit Criteria:**
- All 19 achievements have trigger logic and unit tests.
- Player statistics update in real time (verified by save/load round-trip).
- Terminal simulator runs entirely on `CommandRegistry`.
- Hint system is player-driven, not forced.
- All smoke tests pass.

---

# Phase D — Integration & Polish (Week 9–10)

**Goal:** Ensure all modules work together, optimize, document, and ship.

**Motto:** *"It doesn't matter how clean the code is if the game doesn't run."*

---

### D.1 Save Format Versioning & Migration [DONE]

**Task:** Add a `version` key to save files so future format changes don't corrupt old saves.

**Files:**
- `engine/storage.py` — `JsonFileRepository.save()` adds `"_version": 2`
- `engine/storage.py` — `JsonFileRepository.load()` checks version, runs migration if needed
- New: `engine/save_migrations.py` — `migrate_v1_to_v2(data)` function

**Migration needed:**
- v1 saves lack `chapter_quiz_stats`, `boss_kill_times`, `speaker_stats`, etc. Populate defaults.

**Depends On:** A.6 (Storage Repository), C.3 (all Player fields are now meaningful).

**Success Criteria:**
- New save files contain `"_version": 2`.
- Loading a v1 save (from before this change) correctly populates missing fields with defaults.
- `InMemoryRepository` can simulate versioned saves for testing.

**Time:** 1 day

**Risk:** Medium. Save corruption is the worst kind of bug. Test with real save files from Phase A.

---

### D.2 Performance Audit [DONE]

**Task:** Profile and optimize cold-start time and mission transition speed.

**Files:** `main.py`, `engine/mission_engine.py`, `engine/terminal_sim.py`

**Likely bottlenecks:**
- Importing all 22 chapter modules at startup (~800 lines each).
- `SIMULATED_OUTPUTS` dictionary lookup (if not fully migrated by D.2).
- `time.sleep()` calls in `typewrite()` and boot sequence.

**Optimization candidates:**
- Lazy-load chapter modules when selected (reduce startup by ~60%).
- Replace the shell-based screen clear with a direct ANSI escape for faster screen clears.
- Add a `--fast` CLI flag that skips `typewrite()` delays and boot animation.

**Depends On:** C.5 (Terminal migration must be complete before optimizing lookups).

**Success Criteria:**
- `python3 main.py` cold start is under 1 second.
- Mission transition (story → quiz) is under 0.5 seconds without `typewrite` delay.
- `--fast` flag works and skips all animations.

**Time:** 1 day

**Risk:** Low. Performance changes are additive (new flags, lazy loading).

---

### D.3 Comprehensive Unit Test Suite [DONE]

**Task:** Expand beyond smoke tests into true unit tests for all engine modules.

**Files:** New/expanded `tests/` directory.

**Test modules to create/expand:**

| Module | Coverage Target |
|--------|----------------|
| `tests/test_player.py` | `add_xp()` boundaries, `gear_bonus()` combos, `to_dict()`/`from_dict()` round-trip, level calculation |
| `tests/test_mission_phases.py` | Each phase with mock context: Story, Terminal, Quiz, XP, Achievement, Reward |
| `tests/test_achievement_engine.py` | Every achievement rule with mock Player/Mission |
| `tests/test_terminal_commands.py` | Top 20 commands: exact match, prefix match, case-insensitive, unknown |
| `tests/test_storage.py` | `InMemoryRepository` round-trip, `JsonFileRepository` file creation, version migration |
| `tests/test_renderer.py` | `NullRenderer` buffer capture, `TerminalRenderer` ANSI output |
| `tests/test_menus.py` | Menu dispatch, invalid key handling, nested menus |

**Depends On:** All previous phases (the abstractions must exist to be unit-tested).

**Success Criteria:**
- `python3 -m unittest discover tests/` runs all tests and reports 100% pass rate.
- Every function in `engine/` that has business logic is covered by at least one unit test.
- Smoke tests still pass as the integration layer.

**Time:** 2 days

**Risk:** Low. Tests are additive.

---

### D.4 Documentation Synchronization [DONE]

**Task:** Update all devdocs to reflect the final codebase state.

**Files:**
- `CLAUDE.md` — update architecture diagrams, file size references, dataclass schemas
- `README.md` — update stats (501 missions, 22 chapters, 19 achievements, levels 1–20)
- `GAMEPLAY_GUIDE.md` — document hint system, gear effects, achievement list
- `devdocs/evolution/*.md` — mark completed items as `[DONE]`, add lessons learned

**Depends On:** All previous phases.

**Success Criteria:**
- A new developer can read `CLAUDE.md` and recreate the project accurately.
- All `devdocs/` files have a "Last Updated" date of 2026-05-xx (end of Phase D).

**Time:** 1 day

**Risk:** None.

---

### D.5 Final Integration Run [DONE]

**Task:** End-to-end test of the complete game loop: new game → Ch1 all missions → save → load → Ch2 partial → BOSS → exam mode.

**Files:** All.

**Test script:**
```bash
python3 scripts/full_integration_test.py
```
This script uses `NullRenderer` and `InMemoryRepository` to simulate a full playthrough programmatically.

**Depends On:** Everything.

**Success Criteria:**
- Script completes 50 missions, 2 bosses, and 1 exam block without exception.
- All Player fields are non-default at the end.
- Save/load round-trip preserves state exactly.
- 25/25 smoke tests pass.
- Unit tests: 100% pass.

**Time:** 0.5 day

**Risk:** Low. This is verification, not change.

---

## Phase D Summary

| ID | Task | Time | Risk |
|----|------|------|------|
| D.1 | Save versioning | 1.0 d | Medium |
| D.2 | Performance audit | 1.0 d | Low |
| D.3 | Unit test suite | 2.0 d | Low |
| D.4 | Documentation sync | 1.0 d | None |
| D.5 | Final integration | 0.5 d | Low |
| **Total** | | **~5.5 days** | |

**Phase D Exit Criteria:**
- `python3 scripts/run_smoke_tests.py` → 25/25 pass.
- `python3 -m unittest discover tests/` → 100% pass.
- `python3 scripts/full_integration_test.py` → completes without exception.
- Save files are versioned and backward-compatible.
- `CLAUDE.md` accurately describes the codebase.

---

# Master Timeline

| Week | Phase | Focus | Key Deliverables |
|------|-------|-------|------------------|
| 1 | A | Cleanup + Data fixes | Dead code gone, quiz types fixed, gear added, BOSS metadata complete |
| 2 | A | Critical abstractions | Renderer Protocol, Save Repository, typed config, CI runner |
| 3 | B | Engine decoupling | Achievement Rule Engine, MissionRunner phases, Gear bonuses wired |
| 4 | B | DI + Menus + Terminal arch | DI for GameState, Menu Builder, CommandRegistry foundation, Chapter Registry |
| 5 | C | Player-facing fixes | Forced hints fixed, achievement triggers, Player stats alive |
| 6 | C | Terminal migration (batch 1) | Ch1–Ch7 commands migrated to classes |
| 7 | C | Terminal migration (batch 2) | Ch8–Ch14 commands migrated |
| 8 | C | Terminal migration (batch 3) + Polish | Ch15–Ch22 commands migrated, recaps data-driven, chapter achievements generalized |
| 9 | D | Hardening | Save versioning, performance audit, full unit test suite |
| 10 | D | Ship | Documentation sync, final integration test, sign-off |

**Total estimated effort:** ~35 developer-days (spread across 10 weeks, ~3.5 days/week).

**Buffer:** Week 10 has 0.5 days allocated, leaving 2.5 days of slack for unexpected issues.

---

# Dependency Graph (Simplified)

```
A.1 ──→ A.5 ──→ B.3 ──→ C.1 ──→ C.2
        │       │       │       └──→ C.3
        │       │       └──→ C.4
        │       └──→ B.1 ──→ C.7
        │       └──→ B.4 ──→ B.5
        └──→ A.6 ──→ D.1
A.7 ──→ A.8
B.6 ──→ C.5
B.7 ──→ C.6
```

**Critical path:** A.1 → A.5 → B.3 → C.1 → C.2 → D.5

If any task on the critical path slips, the whole timeline slips. Non-critical-path tasks (B.6, B.7, C.5, C.6) can be deferred without blocking the final integration.

---

# Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Smoke test breakage during B.3 (MissionRunner phases) | Medium | High | Keep the old `run()` method as `_run_legacy()` during transition. Swap only after smoke tests pass on the new phases. |
| Save file corruption during D.1 | Low | Critical | Never overwrite the original save during migration. Load v1, migrate to v2 in memory, write to a new path, verify, then atomically rename. |
| Terminal command loss during C.5 | Medium | Medium | Maintain the legacy `SIMULATED_OUTPUTS` fallback until 100% of commands are migrated and tested. |
| Achievement balance issues during C.2 | Medium | Medium | Add "dev mode" flag that prints all achievement checks verbosely. Review with designer before shipping. |
| Phase A takes longer than 2 weeks | Medium | Medium | A.5 (Renderer) is the longest item. If it slips, defer A.9 (CI) to Week 3. Do not cut A.2 or A.3 — data quality is foundational. |

---

# How to Use This Roadmap

1. **Pick a task by ID.** Every task is self-contained and has clear success criteria.
2. **Check dependencies.** Never start a task until all its "Depends On" items are done.
3. **Run smoke tests after every change.** If smoke tests fail, stop and fix before proceeding.
4. **Update this document.** When a task is done, add `[DONE]` next to its ID and record the actual time taken.
5. **Defer, don't delete.** If a task is too big for the current week, move it to the next week. Do not skip it.

---

# Cross-Reference Matrix

| Roadmap Task | Source Document | Section |
|--------------|-----------------|---------|
| A.1 | `cleanup_inventory.md` | §1, §2 |
| A.2, A.3, A.4 | `smoke_tests/report.md` | §2, §3 |
| A.5 | `refactoring_opportunities.md` | RO-01 |
| A.6 | `refactoring_opportunities.md` | RO-02 |
| A.7 | `refactoring_opportunities.md` | RO-08 |
| A.8 | `gap_analysis.md` | §1.4 |
| B.1 | `refactoring_opportunities.md` | RO-03 |
| B.2 | `gap_analysis.md` | §1.2 |
| B.3 | `refactoring_opportunities.md` | RO-05 |
| B.4 | `refactoring_opportunities.md` | RO-07 |
| B.5 | `refactoring_opportunities.md` | RO-06 |
| B.6 | `refactoring_opportunities.md` | RO-04 |
| B.7 | `refactoring_opportunities.md` | RO-09 |
| C.1 | `gap_analysis.md` | §1.5, §3.4 |
| C.2 | `gap_analysis.md` | §1.1 |
| C.3 | `gap_analysis.md` | §1.3 |
| C.4 | `gap_analysis.md` | §1.5 |
| C.5 | `refactoring_opportunities.md` | RO-04 |
| C.6 | `refactoring_opportunities.md` | RO-10 |
| C.7 | `gap_analysis.md` | §1.1 |
| D.1 | `gap_closure_plan.md` | §2.3 |
| D.2 | `gap_analysis.md` | §4.2 |
| D.3 | `gap_closure_plan.md` | §2.1 |

---

*End of Implementation Roadmap*
