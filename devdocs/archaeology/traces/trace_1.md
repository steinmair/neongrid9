# Trace 1: Save System Interface

## Interface Surface

- `save_game(player: Player, slot: int = 1) -> bool`
- `load_game(slot: int = 1) -> Player | None`
- `slot_info(slot: int) -> str`
- `delete_save(slot: int) -> bool`

**Called by:** `main.py` (`new_game_menu`, `load_game_menu`, `manage_saves_menu`, `game_hub`, `GameState.save`, `GameState.auto_save`)
**Depends on:** `engine.player.Player`

---

## Entry Point

The entry point is always in `main.py` when the player triggers an action that requires persistence:

1. **Save:** After every mission completion (`MissionRunner.run()` → `GAME.auto_save(player)`) or manual save (`game_hub()` choice "v").
2. **Load:** From the main menu (choice "2") → `load_game_menu()` → `load_game(slot)`.
3. **Info:** Displayed in `new_game_menu()`, `load_game_menu()`, `manage_saves_menu()`.
4. **Delete:** From `manage_saves_menu()` when user confirms deletion.

---

## Execution Path

### Saving

```
main.py:GAME.auto_save(player)
    │
    ▼
save_system.save_game(player, slot)
    │
    ├──► ensure_save_dir() → Path.mkdir(exist_ok=True)
    │
    └──► path = SAVE_FILES[slot] (looks up Path in dict)
         │
         └──► with open(path, "w", ...) as f:
              │
              └──► json.dump(player.to_dict(), f, indent=2, ensure_ascii=False)
                   │
                   └──► player.to_dict() recursively serializes:
                        - completed_missions: set → list
                        - inventory: list
                        - reputation: dict
                        - chapter_quiz_stats: dict
                        - achievements: NOT serialized directly (AchievementTracker is a field but to_dict() doesn't include it!)
```

**Critical finding:** `player.to_dict()` does **not** serialize the `achievements` field (the `AchievementTracker` object). Looking at the code, `to_dict()` returns a dict with 18 keys, and `achievements` is missing. However, `from_dict()` reconstructs `achievements` with `AchievementTracker()` (empty default). **This means achievements are lost on save/load.**

Wait, let me double-check this. Looking at player.py lines 327-350:
```python
def to_dict(self) -> dict:
    return {
        "name": self.name,
        "xp": self.xp,
        ...
        "missions_per_chapter": self.missions_per_chapter,
    }
```

And from_dict (lines 352-377):
```python
p = cls()
p.name = d.get("name", "Ghost")
...
p.missions_per_chapter = d.get("missions_per_chapter", {})
return p
```

The `achievements` field is a dataclass field with `default_factory=AchievementTracker`, but it is NOT in `to_dict()` and NOT restored in `from_dict()`. This is a genuine bug I found by reading the code carefully.

### Loading

```
main.py:load_game_menu()
    │
    ▼
save_system.load_game(slot)
    │
    ├──► path = SAVE_FILES[slot]
    ├──► if not path.exists(): return None
    │
    └──► with open(path, "r", ...) as f:
         │
         └──► data = json.load(f)
              │
              └──► Player.from_dict(data)
                   │
                   ├──► Creates empty Player()
                   ├──► Overwrites fields from JSON
                   ├──► Migration: fills missing factions with 0
                   └──► Returns Player instance
```

### Slot Info

```
main.py:new_game_menu() or load_game_menu()
    │
    ▼
save_system.slot_info(slot)
    │
    ├──► path = SAVE_FILES[slot]
    ├──► if not path.exists(): return "  [LEER]"
    │
    └──► with open(path, "r", ...) as f:
         │
         └──► data = json.load(f)
              │
              └──► Format string: f"  {name}  |  LVL {level} {title}  |  {xp} XP  |  {done} Missionen"
```

### Delete

```
main.py:manage_saves_menu()
    │
    ▼
save_system.delete_save(slot)
    │
    ├──► path = SAVE_FILES[slot]
    ├──► if path.exists(): path.unlink()
    └──► return bool(path.exists() before unlink)
```

---

## Resource Management

- **File descriptors:** Managed via `with open(...)` context managers — correctly closed.
- **Directory creation:** `mkdir(exist_ok=True)` is safe and idempotent.
- **Disk I/O:** Synchronous blocking writes. Save happens after every mission, which means ~500 disk writes for a full playthrough.
- **Memory:** Player dict is transient during serialization; no persistent memory leak.

---

## Error Path

All four functions wrap their core logic in `try/except`:

```python
try:
    # file operations
except Exception as e:
    print(f"  Speicherfehler: {e}")  # or "Ladefehler", etc.
    return False / None
```

**Issues with this approach:**
- `PermissionError` (no write access to home dir) → prints to stdout, returns failure silently.
- `JSONDecodeError` (corrupted save file) → returns `None`, caller shows "Kein Speicherstand".
- `OSError` (disk full) → caught generically, user sees generic error.
- **No retry logic.** No backup of corrupted files.

In `main.py`, the callers handle failure as follows:
- `load_game_menu()`: Shows `show_error("Kein Speicherstand in diesem Slot.")`, returns `False`.
- `save_game()`: Return value is **ignored** in `GAME.auto_save()`. The player never knows if auto-save failed.

---

## Performance Characteristics

- **Save:** O(n) where n = size of player state dict. For a completionist run (~500 missions), JSON is ~20-50 KB. Write takes ~1-5 ms on SSD.
- **Load:** O(n) parse. ~1-3 ms.
- **Frequency:** Auto-save after every mission. For 501 missions, that's 501 writes.
- **No batching, no debouncing.** A speedrun player could trigger 30 saves in 30 minutes.

---

## Observable Effects

- Files created in `~/.neongrid9/save_slot{1,2,3}.json`.
- JSON contains human-readable player state.
- Files can be inspected, edited, or backed up by the user.

---

## Why This Design

The design follows the **Keep It Simple** principle. For a single-user, single-process terminal game, a JSON file is the lightest possible persistence layer. It requires zero setup, zero dependencies, and produces human-readable output. The three-slot system is a classic console-game convention.

---

## Assessment

### What feels incomplete

**The issue:** `player.to_dict()` does not serialize the `achievements` field (`AchievementTracker`). After loading a game, all unlocked achievements are lost.

**ELI5:** Imagine you collect stickers in a book. When you put the book away (save), you take out all the sticker pages and forget to put them back in the box. When you open the box later (load), the stickers are gone.

**Impact:** Players lose all achievement progress every time they save and reload. This breaks the entire achievement system. Since auto-save happens after every mission, achievements effectively never persist across sessions.

**Robust Fixes:**
1. Add `"achievements": list(self.player.achievements.unlocked)` to `to_dict()`.
2. Add `p.achievements = AchievementTracker(); p.achievements.unlocked = set(d.get("achievements", []))` to `from_dict()`.
3. Add a unit test that round-trips a Player with achievements through save/load and asserts they are preserved.

---

### What feels vulnerable

**The issue:** Generic `except Exception` swallows all errors. The return value of `save_game` is ignored by `GAME.auto_save()`, so silent failures go unnoticed by the player.

**ELI5:** Imagine a vending machine that sometimes fails to drop your snack but still says "Thank you." You walk away hungry and never know what happened.

**Impact:** If the disk is full, permissions are wrong, or the filesystem is read-only, the game tells the player "Gespeichert!" but actually wrote nothing. The player loses all progress since the last successful save.

**Robust Fixes:**
1. Return a `SaveResult` dataclass with `(success: bool, error: str | None)` instead of `bool`.
2. Make `GameState.auto_save()` check the return value and display an error if save fails.
3. Distinguish error types: `PermissionError` → tell user to check permissions; `OSError` → disk full; `JSONEncodeError` → data corruption.
4. Write to a temporary file first, then atomic rename (`os.replace`) to prevent half-written saves.

---

### What feels like bad design

**The issue:** Manual serialization (`to_dict` / `from_dict`) is boilerplate-heavy and fragile. Adding a new field to `Player` requires editing four places: the dataclass definition, `to_dict()`, `from_dict()`, and `__init__` defaults.

**ELI5:** Imagine filling out a form where every time you add a new question, you have to rewrite the entire form in three different languages. You will eventually forget one.

**Impact:** The `achievements` bug is a direct consequence of this pattern. Any future field added to `Player` has a high probability of being forgotten in serialization. This creates a maintenance burden and subtle data-loss bugs.

**Robust Fixes:**
1. Use `dataclasses.asdict()` for automatic serialization, with custom hooks for non-serializable types (`set` → `list`).
2. Use `dataclasses.fields(Player)` to drive deserialization, iterating over declared fields rather than hardcoding keys.
3. Alternatively, add a JSON schema validation step (e.g., `jsonschema` or a lightweight hand-rolled validator) that verifies all expected keys exist after deserialization.
