# Trace 2: Mission Runner Execution Interface

## Interface Surface

- `class MissionRunner`
  - `__init__(self, player: Player, save_callback: Callable = None)`
  - `run(self, mission: Mission) -> bool`
  - `_run_quiz(self, questions: List[QuizQuestion], chapter: int = 0, exam_start: float = 0.0, exam_limit: int = 0) -> int`
  - `_run_boss(self, mission: Mission) -> bool`
  - `_replay_mission(self, mission: Mission) -> bool`

**Called by:** `main.py` (`chapter_menu`)
**Calls into:** `engine.display.*`, `engine.terminal_sim.run_terminal`, `engine.player.Player`, `engine.features.HintRequest`, `engine.features.calculate_level` (indirectly), `engine.player.GEAR_CATALOG` (lazy import)

---

## Entry Point

The entry is in `main.py:chapter_menu()`:

```python
runner = MissionRunner(GAME.player, save_callback=GAME.auto_save)
# ... user selects a mission ...
runner.run(mission)
```

`MissionRunner` is instantiated fresh for every `chapter_menu()` session (not per mission). It holds a reference to the current `Player` and an optional save callback.

---

## Execution Path

### Normal Mission Flow (`run()`)

```
MissionRunner.run(mission)
    │
    ├──► Check if mission already completed AND not BOSS → _replay_mission()
    │
    ├──► Check if BOSS → _run_boss()
    │
    └──► Standard Flow:
         │
         ├──► clear() + mission_header() — screen setup
         │
         ├──► show_ascii_art() — if mission has art
         │
         ├──► show_story(speaker, story) + show_transition() + prompt_continue()
         │
         ├──► show_info(why_important) + transition
         │
         ├──► show_info(explanation) + transition
         │
         ├──► show_code(syntax) + transition
         │
         ├──► show_code(example) + prompt_continue()
         │
         ├──► TERMINAL TASK (if expected_commands):
         │    │
         │    ├──► Fancy prompt loop: up to 5 attempts
         │    │    │
         │    │    ├──► prompt_input("root@matrix")
         │    │    ├──► Check exact match against expected_commands
         │    │    ├──► Check base match (if single expected command)
         │    │    ├──► On wrong: HintRequest.create() → show_hint() → DEDUCT XP
         │    │    └──► After 5 failures: run_terminal() fallback
         │    │
         │    └──► If still failed after fallback:
         │         └──► show_warn("Versuche aufgebraucht.") + show_code(expected[0])
         │
         ├──► QUIZ (if quiz_questions):
         │    └──► _run_quiz() — loop over questions
         │         │
         │         ├──► Print question + options
         │         ├──► prompt_input("antwort [A/B/C/D]")
         │         ├──► 3 attempts per question
         │         ├──► Correct: +15 XP (first try) or +7 XP (second try)
         │         ├──► Wrong: show error + explanation
         │         └──► record_quiz_result(chapter, correct)
         │
         ├──► show_exam_tip() + prompt_continue()
         ├──► show_memory_tip()
         │
         ├──► XP CALCULATION:
         │    ├──► base_xp = mission.xp
         │    ├──► if terminal failed: base_xp //= 3
         │    ├──► if first-try success: base_xp *= 1.2
         │    ├──► total_xp = base_xp + quiz_xp
         │    └──► player.add_xp(total_xp) → returns (new_xp, leveled_up)
         │
         ├──► player.complete_mission(mission.mission_id)
         │
         ├──► ACHIEVEMENT CHECKS (inline, ~10 hardcoded conditions):
         │    ├──► first_mission (if completed_missions == 1)
         │    ├──► boss_defeated (if mtype == BOSS)
         │    ├──► five_bosses (if bosses_defeated == 5)
         │    ├──► all_bosses (if bosses_defeated == 22)
         │    ├──► chapter_1_complete (if chapter 1 missions >= 31)
         │    ├──► quest_marathon (if completed == 100)
         │    ├──► level_ten (if level >= 10)
         │    ├──► chapter_master (if 5+ chapters complete)
         │    ├──► all_factions (if all faction levels >= 2)
         │    └──► gear_collector (if inventory >= 10)
         │
         ├──► show_achievements(unlocked)
         ├──► if leveled_up: level_up_screen()
         │
         ├──► GEAR REWARD (if mission.gear_reward):
         │    └──► player.add_gear() → print gear info from GEAR_CATALOG
         │
         ├──► FACTION REWARD (if mission.faction_reward):
         │    └──► player.add_reputation() → print reputation gain
         │
         ├──► save_callback(player) → auto_save
         │
         └──► prompt_continue()
```

### Boss Mission Flow (`_run_boss()`)

```
_run_boss(mission)
    │
    ├──► boss_intro() — full-screen boss intro
    ├──► mission_header() + ascii_art (red color) + story
    │
    ├──► BOSS PHASES:
    │    └──► For each expected_command:
    │         ├──► Print phase header
    │         ├──► run_terminal(expected=[cmd], max_attempts=3)
    │         └──► Track phase_success count
    │
    ├──► Boss quiz: _run_quiz()
    │
    ├──► WIN CONDITION: phase_success >= total_phases * 0.6
    │    ├──► Win: full XP + boss_defeated increment
    │    └──► Loss: half XP
    │
    └──► Same reward/achievement logic as standard flow
```

### Replay Flow (`_replay_mission()`)

```
_replay_mission(mission)
    │
    ├──► Show header with "[WIEDERHOLUNG]" suffix
    ├──► Ask "Quiz wiederholen? [j/n]"
    └──► If yes: _run_quiz() → half XP bonus (quiz_xp // 2)
```

---

## Resource Management

- **Screen state:** `clear()` is called at the start of every mission. No screen buffer is retained.
- **Memory:** `Mission` objects are pre-loaded at import time and reused. No per-mission allocation.
- **User input:** `prompt_input()` blocks on `input()` until the user presses Enter.
- **Time:** `time.sleep()` calls inside `show_story()`, `show_transition()`, `typewrite()` for animation. During these sleeps, the process is blocked.

---

## Error Path

There is **no structured error handling inside `run()`**. The method assumes all inputs and data are valid:

- `mission.story_transitions` accessed with `tr[0]`, `tr[1]`, etc. — if the list has fewer than 4 elements, some transitions are empty strings (guarded by `if tr: ...`).
- `mission.quiz_questions` accessed directly — if empty, the quiz section is skipped.
- `mission.expected_commands` accessed directly — if empty, the terminal task is skipped.
- `KeyboardInterrupt` is NOT caught inside `run()`. It propagates up to `main()`'s outer `try/except`.
- The fancy prompt loop can deduct XP even if the player later succeeds: `self.player.xp = max(0, self.player.xp - hint_req.xp_cost)`. This mutation happens mid-mission with no rollback mechanism.

If `save_callback` raises an exception, the entire `run()` method crashes, but all prior state mutations (XP, completed_missions, gear, reputation) have already been applied.

---

## Performance Characteristics

- **CPU:** Negligible. All logic is string comparison and dict lookup.
- **I/O:** Bound by user typing speed and `time.sleep()` animations. A mission takes 2-5 minutes of wall-clock time, of which <0.1% is actual computation.
- **Memory:** The `SIMULATED_OUTPUTS` dict in `terminal_sim.py` is ~4,000 lines. It's loaded once at import and stays in memory.
- **No concurrency:** Single-threaded. `time.sleep()` blocks the entire process.

---

## Observable Effects

- Terminal screen redraws multiple times per mission.
- Player state changes: XP, completed_missions, inventory, reputation, achievements.
- JSON save file is overwritten.
- Achievement popups appear if thresholds are crossed.
- Level-up screen appears if XP threshold crossed.

---

## Why This Design

`MissionRunner.run()` implements a **Template Method** pattern. Every mission follows the same pedagogical sequence: context → explanation → practice → assessment → reward. This consistency is intentional — it creates a predictable learning rhythm. The inline achievement checks are a pragmatic shortcut: because there are only 19 achievements and they depend on simple counters, a full event-driven system would be overkill.

---

## Assessment

### What feels incomplete

**The issue:** Achievement `perfect_quiz` is defined in `features.py` but **never checked or unlocked** anywhere in the codebase. There is also no mechanism to track whether a mission was completed without hints (required for `no_hints`).

**ELI5:** Imagine a treasure chest in a video game that has a label on it but no keyhole. You can see it exists, but there's no way to open it, no matter what you do.

**Impact:** Two achievements (`perfect_quiz`, `no_hints`) are permanently unattainable. Players who meet the criteria will never see them. This creates frustration and makes the achievement completion percentage misleading.

**Robust Fixes:**
1. In `_run_quiz()`, track whether all questions were answered correctly on the first try. If yes, unlock `perfect_quiz`.
2. Add a `hints_used_in_mission` flag to `MissionRunner.run()`. If `hints_used == 0` and the mission succeeds, unlock `no_hints`.
3. Centralize achievement trigger checks into a single `_check_achievements(mission, mission_context)` method instead of scattering them inline.

---

### What feels vulnerable

**The issue:** Mid-mission state mutations have **no rollback**. If the process crashes after XP is added but before `save_callback` runs, the player loses that progress. More critically, if the fancy prompt deducts XP for hints and then the user quits or the terminal crashes, that XP loss persists.

**ELI5:** Imagine a cashier who takes money out of your wallet before you've decided to buy anything. If you change your mind and leave the store, the money is still gone.

**Impact:** A crash or forced quit during a mission can leave the player with:
- A deducted XP balance (from hints) but no mission completion
- Partially updated quiz stats but no save
- Inconsistent state between what's in memory and what's on disk

**Robust Fixes:**
1. Implement a **mission transaction**: collect all mutations (XP delta, mission completion, gear, reputation) into a `MissionResult` object. Apply them atomically at the end, just before `save_callback`.
2. Move `save_callback` to a `finally` block so it runs even if an exception occurs.
3. Implement an **auto-save checkpoint** mid-mission (e.g., after the terminal task completes, before the quiz).

---

### What feels like bad design

**The issue:** `run()` is a single method spanning ~250 lines of deeply nested code with inline achievement checks, XP calculations, gear rewards, and faction updates all mixed together. This violates the Single Responsibility Principle.

**ELI5:** Imagine a recipe that tells you how to chop vegetables, cook the meat, set the table, wash the dishes, AND calculate the nutritional value of the meal — all in one paragraph. If you want to change just the table setting, you have to read the entire recipe.

**Impact:**
- Adding a new mission type requires editing `run()`'s `if/elif` chain.
- Adding a new achievement requires finding the right spot in the middle of `run()`.
- Testing is impossible without mocking the entire terminal, display, and save system.
- The method cannot be reused or composed. For example, `timed_exam_mode()` in `main.py` reimplements its own quiz loop instead of using `_run_quiz()` because `_run_quiz()` is tightly coupled to mission state.

**Robust Fixes:**
1. **Extract phases into methods:** `_run_story_phase()`, `_run_terminal_phase()`, `_run_quiz_phase()`, `_run_reward_phase()`.
2. **Extract achievement checking into a dedicated `AchievementEngine` class** that receives events (`mission_completed`, `boss_defeated`, `quiz_perfect`) and decides what to unlock.
3. **Use a pipeline pattern:** `MissionRunner` becomes an orchestrator that passes a `MissionContext` object through a list of phase handlers. Each handler mutates the context. The final handler applies all changes to `Player`.
4. Make `_run_quiz()` reusable for exam mode by decoupling it from `Player` mutation (return results, let caller decide what to do with them).
