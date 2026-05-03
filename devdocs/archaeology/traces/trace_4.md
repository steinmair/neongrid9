# Trace 4: Player State Mutation Interface

## Interface Surface

- `Player.add_xp(self, amount: int) -> tuple[int, bool]`
- `Player._recalculate_level(self)`
- `Player.complete_mission(self, mission_id: str)`
- `Player.record_quiz_result(self, chapter: int, correct: bool)`
- `Player.add_gear(self, item_id: str) -> bool`
- `Player.add_reputation(self, faction: str, amount: int)`
- `Player.gear_bonus(self, boost_type: str) -> float`
- `Player.has_hint_gear(self) -> bool`
- `Player.stats_summary(self) -> str`
- `Player.to_dict(self) -> dict`
- `Player.from_dict(cls, d: dict) -> Player`

**Called by:** `engine.mission_engine.MissionRunner`, `main.py` (`game_hub`, `timed_exam_mode`, `show_inventory`, `show_linux_readiness`)
**Depends on:** `engine.features.AchievementTracker`, `engine.features.calculate_level`

---

## Entry Point

`Player` is instantiated in `main.py:new_game_menu()`:
```python
GAME.player = Player(name=name)
```

Or loaded from save:
```python
player = load_game(slot)
GAME.player = player
```

From there, `MissionRunner` holds a reference and mutates it after every mission.

---

## Execution Path

### XP Addition

```
MissionRunner.run() or main.py:timed_exam_mode()
    │
    ▼
Player.add_xp(amount)
    │
    ├──► Level scaling:
    │    ├──► level >= 15 → scale = 1.3
    │    ├──► level >= 10 → scale = 1.2
    │    ├──► level >= 5  → scale = 1.1
    │    └──► else       → scale = 1.0
    │
    ├──► scaled_amount = int(amount * scale)
    ├──► self.xp += scaled_amount
    │
    ├──► _recalculate_level()
    │    └──► Iterate LEVELS in reverse, find first threshold <= self.xp
    │
    └──► Return (self.xp, self.level > old_level)
```

**Finding:** The scaling bonus is applied to the *incoming* amount, not retroactively. A player who reaches level 5 does not get a bonus on past XP. This is correct behavior, but the scaling is hardcoded in `add_xp()` rather than being a configurable rule.

### Mission Completion

```
MissionRunner.run()
    │
    ▼
Player.complete_mission(mission_id)
    │
    └──► self.completed_missions.add(mission_id)
```

**Simple set addition. O(1).**

### Quiz Result Recording

```
MissionRunner._run_quiz()
    │
    ▼
Player.record_quiz_result(chapter, correct)
    │
    ├──► key = str(chapter)
    ├──► Initialize {"asked": 0, "correct": 0} if key missing
    ├──► asked += 1
    └──► if correct: correct += 1
```

### Gear Addition

```
MissionRunner.run()
    │
    ▼
Player.add_gear(item_id)
    │
    ├──► if item_id not in self.inventory AND item_id in GEAR_CATALOG:
    │         self.inventory.append(item_id)
    │         return True
    └──► else: return False
```

**Finding:** `GEAR_CATALOG` is imported from `engine.player` inside `mission_engine.py` (lazy import at lines 321 and 488). This is a circular import avoidance tactic.

### Reputation Addition

```
MissionRunner.run()
    │
    ▼
Player.add_reputation(faction, amount)
    │
    └──► if faction in self.reputation:
         └──► self.reputation[faction] = min(100, current + amount)
```

### Gear Bonus Calculation

```
main.py:timed_exam_mode() or MissionRunner.run()
    │
    ▼
Player.gear_bonus(boost_type)
    │
    ├──► Lookup bonuses dict for boost_type (e.g., "quiz_xp" → ("ghost_mask", 1.20))
    ├──► If item in inventory: base = mult
    ├──► If "linux_badge" in inventory: base += 0.05 (or base = 1.05 if base was 1.0)
    └──► Return base
```

**Finding:** Gear bonuses do **not stack** for the same boost type. Having multiple items that boost quiz XP still only gives the highest multiplier. The comment says "Boni stapeln sich nicht" (bonuses do not stack), which is intentional but not clearly communicated to the player.

### Stats Summary

```
main.py:show_player_status()
    │
    ▼
Player.stats_summary()
    │
    └──► Builds a large formatted string:
         ├──► Basic stats (name, level, XP, missions, bosses, playtime)
         ├──► Chapter progress loop (ch 1-22)
         ├──► Faction reputation bars
         ├──► Top 3 speakers
         └──► Inventory with rarity colors
```

---

## Resource Management

- **Memory:** All state is in-memory Python objects. `completed_missions` is a `set` of ~500 strings (~10-20 KB). `inventory` is a list of ~20 strings. Total Player object size is well under 1 MB.
- **Mutability:** `Player` is a `@dataclass` with mutable default fields (`completed_missions: Set[str] = field(default_factory=set)`). This is safe because `field(default_factory=...)` creates a new instance per object.
- **No external resources:** No file handles, no network sockets held by `Player`.

---

## Error Path

`Player` methods generally do not raise exceptions:

- `add_xp`: No validation that `amount` is positive. Negative XP would be added directly.
- `complete_mission`: No validation that `mission_id` is well-formed.
- `add_gear`: Returns `False` on duplicate/unknown item. Caller must check.
- `add_reputation`: Silently ignores unknown factions.
- `gear_bonus`: Returns `1.0` for unknown boost types. Caller must multiply by this.
- `from_dict`: Uses `.get()` with defaults for every field. Missing keys are silently defaulted.

**No rollback mechanism:** If `MissionRunner` crashes after `add_xp()` but before `complete_mission()`, the player keeps the XP but not the completion. This is inconsistent.

---

## Performance Characteristics

- `add_xp`: O(L) where L = number of levels (15). Negligible.
- `complete_mission`: O(1) set addition.
- `record_quiz_result`: O(1) dict update.
- `stats_summary`: O(C + F + I) where C = chapters (22), F = factions (5), I = inventory (~20). Produces a ~50-line string.
- `to_dict` / `from_dict`: O(N) over all fields.

---

## Observable Effects

- XP bar updates on screen.
- Level-up screen triggers when `add_xp` returns `leveled_up = True`.
- Inventory screen shows newly acquired gear.
- Faction reputation bars increase.
- Quiz accuracy statistics change.
- Save file is updated (indirectly, via caller).

---

## Why This Design

`Player` is a classic **State Container** (also called an Entity or Model in MVC). It holds all mutable game state in one place, making it easy to save, load, and inspect. The dataclass pattern gives type hints and automatic `__init__`, while custom methods encapsulate game rules (XP scaling, level calculation, gear bonuses).

---

## Assessment

### What feels incomplete

**The issue:** `Player` does not enforce any invariants. Negative XP, duplicate gear, or unknown faction names are accepted silently.

**ELI5:** Imagine a piggy bank that accepts both coins and IOU notes. If someone writes "-5 dollars" on a piece of paper and drops it in, the bank counts it as real money. It also doesn't check if the same coin was already in the bank.

**Impact:** Bugs in `MissionRunner` or `main.py` could corrupt the save state:
- A bug that passes negative XP would silently reduce the player's total.
- A bug that calls `add_gear()` twice would be silently ignored (good), but the caller might not notice.
- An achievement that rewards faction reputation for a misspelled faction name would silently do nothing.

**Robust Fixes:**
1. Add validation: `assert amount >= 0` in `add_xp()`, `assert mission_id` in `complete_mission()`, `assert faction in FACTIONS` in `add_reputation()`.
2. Alternatively, use `pydantic` or manual validators to enforce types and ranges.
3. Log warnings for invalid operations instead of silently ignoring them.

---

### What feels vulnerable

**The issue:** Direct attribute mutation from outside the class. `MissionRunner.run()` directly modifies `self.player.xp`:
```python
self.player.xp = max(0, self.player.xp - hint_req.xp_cost)
```

This bypasses `add_xp()` entirely, meaning:
- Level scaling is not applied to the deduction (correct, but inconsistent).
- No level-down check happens if XP drops below a threshold.
- No validation occurs.

**ELI5:** Imagine a safe where the owner keeps the key under the mat. Anyone can walk up, take the key, and open the safe directly instead of asking the security guard.

**Impact:**
- If a hint costs 50 XP and the player has 30 XP, the line `max(0, self.player.xp - hint_req.xp_cost)` clamps to 0. The player's XP becomes 0, but their level is NOT recalculated. They could be Level 10 with 0 XP.
- Inconsistent XP/level state could cause display bugs or logic errors.

**Robust Fixes:**
1. Make all fields private (`_xp`, `_level`) and expose only methods (`add_xp()`, `deduct_xp()`, `get_level()`).
2. Make `xp` a `@property` with a setter that automatically calls `_recalculate_level()`.
3. Add a `deduct_xp(amount)` method that mirrors `add_xp()` with validation and level recalculation.

---

### What feels like bad design

**The issue:** `to_dict()` and `from_dict()` are manually maintained and already missing the `achievements` field (as discovered in Trace 1). This pattern requires updating four places for every new field.

**ELI5:** Imagine a library where every time you buy a new book, you have to manually write the title in four different catalogs. Sooner or later, you'll forget one catalog, and then nobody can find the book.

**Impact:**
- Data loss when new fields are added.
- Maintenance burden. The developer must remember to update both methods.
- No schema validation. `from_dict()` accepts arbitrary keys and ignores unknown ones. A corrupted save file could contain `{"xp": "not_a_number"}` and crash later.

**Robust Fixes:**
1. Use `dataclasses.asdict()` for serialization, with a custom encoder for `set` and non-serializable types.
2. For deserialization, iterate over `dataclasses.fields(Player)` to reconstruct the object automatically.
3. Add a version field to the save file schema. If `version` is missing or mismatched, run a migration function.
4. Validate loaded data with a schema (even a simple one) before constructing `Player`.
