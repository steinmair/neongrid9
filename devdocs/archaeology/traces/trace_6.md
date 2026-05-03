# Trace 6: Achievement/Hint Features Interface

## Interface Surface

**Hint system:**
- `class HintLevel(Enum)` — FREE=0, STANDARD=1, FINAL=2
- `class HintRequest` — `create(mission_id, hints, level) -> Optional[HintRequest]`

**Achievement system:**
- `class Achievement` — dataclass with id, name, description, xp_reward, icon
- `class AchievementTracker` — `unlock(achievement_id) -> Optional[Achievement]`, `has()`, `count()`
- `ACHIEVEMENTS` — global dict of 19 predefined achievements

**Faction helpers:**
- `calculate_level(total_xp: int) -> int`
- `class FactionStatus` — `progress_bar()`, `display()`

**Called by:** `engine.mission_engine.MissionRunner` (Hints, Achievement unlocks), `engine.player.Player` (AchievementTracker default, calculate_level for reputation bars), `main.py` (Faction display)

---

## Entry Point

### Hint Creation

```
mission_engine:MissionRunner.run()
    |
    +-- Player types wrong command in fancy prompt
    +-- if hints_used < len(mission.hints):
         +-- hint_req = HintRequest.create(mission.mission_id, mission.hints, hints_used)
         +-- if hint_req: show_hint(hint_req.text, hints_used, hint_req.xp_cost)
         +-- if hint_req.xp_cost > 0: player.xp = max(0, player.xp - hint_req.xp_cost)
         +-- hints_used += 1
```

### Achievement Unlock

```
mission_engine:MissionRunner.run()  # after mission completion
    |
    +-- ach = player.achievements.unlock('first_mission')
    +-- if ach: unlocked.append(ach); player.add_xp(ach.xp_reward)
    +-- ach = player.achievements.unlock('boss_defeated')  # if BOSS
    +-- ... (10 more inline checks)
    +-- if unlocked: show_achievements(unlocked)
```

### Faction Level Calculation

```
player.py:Player.stats_summary()
    |
    +-- calculate_level(rep)  # rep = 0-100
    +-- returns: min(5, max(1, (total_xp // 20) + 1)) for reputation
```

---

## Execution Path

### HintRequest.create()

```
HintRequest.create(mission_id, hints, level)
    |
    +-- if not hints or level >= len(hints): return None
    +-- costs = [0, 20, 50]
    +-- xp_cost = costs[min(level, len(costs)-1)]
    +-- hint_level = HintLevel(min(level, 2))
    +-- return HintRequest(mission_id, hint_level, xp_cost, hints[level])
```

**Finding:** The cost array is hardcoded `[0, 20, 50]`. If a mission has 4+ hints, the 4th hint costs 50 XP (same as FINAL) because `min(level, 2)` caps it.

### AchievementTracker.unlock()

```
AchievementTracker.unlock(achievement_id)
    |
    +-- if achievement_id in self.unlocked: return None  # already unlocked
    +-- if achievement_id not in ACHIEVEMENTS: return None  # unknown ID
    +-- self.unlocked.add(achievement_id)
    +-- return ACHIEVEMENTS[achievement_id]  # returns Achievement object
```

### calculate_level()

```
calculate_level(total_xp)
    |
    +-- if total_xp <= 100:
    |      +-- return min(5, max(1, (total_xp // 20) + 1))
    +-- else:
    |      +-- thresholds = [0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3250]
    |      +-- for i, threshold in enumerate(thresholds[1:], 1):
    |             if total_xp < threshold: return i
    |      +-- return 10
```

**Dual behavior:** For reputation (0-100), it uses linear chunks of 20. For XP (>100), it uses exponential thresholds. The function caller must know which semantic they intend.

---

## Resource Management

- **Memory:** `ACHIEVEMENTS` dict holds 19 `Achievement` objects. Each is ~5 strings + 2 ints. Negligible.
- **AchievementTracker:** Holds a `Set[str]` of unlocked IDs. For a completionist run, this is 19 strings.
- **No I/O:** All operations are in-memory.

---

## Error Path

- `HintRequest.create()`: Returns `None` if hints list is empty or level out of bounds. Caller in `MissionRunner` checks `if hint_req:` — safe.
- `AchievementTracker.unlock()`: Returns `None` for invalid IDs or already-unlocked. Caller checks `if ach:` — safe.
- `calculate_level()`: Returns 1 for negative input (due to `max(1, ...)`). No error raised.

---

## Performance Characteristics

- `create()`: O(1) array lookup.
- `unlock()`: O(1) set membership test and dict lookup.
- `calculate_level()`: O(1) for reputation, O(10) for XP.
- **Negligible overall.** These are not bottlenecks.

---

## Observable Effects

- Hint displays with colored labels (FREE / STANDARD / FINAL).
- Achievement unlock popups with icons and XP rewards.
- Faction reputation bars in player status.

---

## Why This Design

The features module isolates game-meta systems (hints, achievements, factions) from the core engine. This allows adding new achievements or hint tiers without touching `mission_engine.py` or `player.py`. The `ACHIEVEMENTS` dict is declarative — achievements are data, not code.

---

## Assessment

### What feels incomplete

**The issue:** Two achievements (`perfect_quiz`, `no_hints`) are defined in `ACHIEVEMENTS` but **never triggered** in the codebase. There is no code path that calls `unlock('perfect_quiz')` or `unlock('no_hints')`.

**ELI5:** Imagine a treasure hunt where the organizer hid two extra prizes but forgot to write the clues for them. The prizes exist, but nobody can ever find them.

**Impact:** Players who answer every quiz question perfectly or complete missions without hints will never see these achievements. This makes the achievement completion rate permanently unattainable (17/19 max instead of 19/19).

**Robust Fixes:**
1. In `_run_quiz()`, track a `all_correct_first_try` flag. If true after the quiz, call `unlock('perfect_quiz')`.
2. In `MissionRunner.run()`, track `hints_used_in_mission`. If `hints_used == 0` and success, call `unlock('no_hints')`.
3. Add a CI test that verifies every achievement ID in `ACHIEVEMENTS` has at least one call site that could trigger it.

---

### What feels vulnerable

**The issue:** Achievement triggers are scattered inline inside `MissionRunner.run()` rather than being event-driven. This means:
- Adding a new achievement requires editing `mission_engine.py`.
- There's no guarantee that an achievement check isn't missed.
- The same logic is duplicated (e.g., `boss_defeated` is checked in both `run()` and `_run_boss()`).

**ELI5:** Imagine a school where every teacher has to remember to give out gold stars themselves, instead of a principal who listens for good behavior and hands them out centrally. Some teachers will forget.

**Impact:**
- Maintenance burden: 10+ inline achievement checks in a 250-line method.
- Risk of inconsistency: `all_bosses` is checked in `run()` but not `_run_boss()`. If a boss is defeated via a future code path, the check might be missed.
- The `quest_marathon` achievement checks `len(self.player.completed_missions) == 100` exactly. If the player somehow skips from 99 to 101 (e.g., via a future "complete all" feature), it would never trigger.

**Robust Fixes:**
1. Create an `AchievementEngine` class that subscribes to events:
   ```python
   achievement_engine.on('mission_completed', check_first_mission)
   achievement_engine.on('boss_defeated', check_boss_achievements)
   ```
2. Emit events from `MissionRunner` at key moments: `mission_completed`, `quiz_perfect`, `hint_used`, `level_up`.
3. Register achievement conditions as predicate functions in a dict, separate from the runner.

---

### What feels like bad design

**The issue:** `FactionStatus` class is defined but **never instantiated or used anywhere** in the codebase. It exists as dead code.

**ELI5:** Imagine building a beautiful model car and putting it on a shelf in your closet where nobody ever sees it. You spent time making it, but it serves no purpose.

**Impact:**
- Dead code adds cognitive load. A new developer might think factions are displayed with progress bars, but they're not.
- `stats_summary()` manually builds faction bars with `calculate_level()` instead of using `FactionStatus`.
- `FactionStatus.display()` returns a formatted string that nobody calls.

**Robust Fixes:**
1. Either use `FactionStatus` in `Player.stats_summary()` to build the faction display, or delete the class.
2. If keeping it, add a `player.get_faction_statuses() -> List[FactionStatus]` method and use it for rendering.
3. Add a CI lint rule (e.g., `vulture`) to detect unused code.
