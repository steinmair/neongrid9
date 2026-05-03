# Trace 7: Game State & Main Loop Interface

## Interface Surface

- `class GameState` — `save()`, `auto_save(player)`
- `def main()` — entry point
- `def main_menu() -> str`
- `def new_game_menu()`
- `def load_game_menu() -> bool`
- `def manage_saves_menu()`
- `def game_hub()` — main gameplay loop
- `def chapter_menu(ch_id: int)` — chapter navigation
- `def show_player_status()`
- `def show_linux_readiness()`
- `def review_mode()`
- `def timed_exam_mode()`
- `def show_inventory()`

**Called by:** OS (python3 main.py)
**Calls into:** All engine modules and mission modules

---

## Entry Point

The only entry point is `python3 main.py`:

```
__main__ block
    |
    +-- try: main()
    +-- except KeyboardInterrupt: save + exit
    +-- except Exception: print traceback + exit
```

---

## Execution Path

### Cold Start

```
main()
    |
    +-- Check first_run: any(save_slot exists?)
    +-- if first_run: show_boot_sequence() + show_title_screen()
    |
    +-- while True:
         +-- choice = main_menu()
         +-- if choice == "1": new_game_menu(); game_hub()
         +-- if choice == "2": load_game_menu(); game_hub()
         +-- if choice == "3": manage_saves_menu()
         +-- if choice == "4": about_screen()
         +-- if choice == "q": clear(); print exit message; sys.exit(0)
```

### New Game

```
new_game_menu()
    |
    +-- prompt_input("name") → default "Ghost"
    +-- prompt_input("wahl [1/2/3]") → difficulty
    +-- Show slot info for slots 1-3
    +-- prompt_input("slot [1/2/3]") → GAME.save_slot
    +-- GAME.player = Player(name=name)
    +-- if difficulty == "3": set XP=1500, level=3
    +-- GAME.save()
    +-- show_story_prologue()
```

### Game Hub

```
game_hub()
    |
    +-- while GAME.running and GAME.player:
         +-- clear()
         +-- Show player status (xp_bar, name, title)
         +-- Show faction reputation line
         +-- Show chapter progress bars (all 22 chapters)
         +-- Show menu options
         +-- choice = prompt_input("hub")
         |
         +-- if choice == "1".."22": chapter_menu(int(choice))
         +-- if choice == "s": show_player_status()
         +-- if choice == "i": show_inventory()
         +-- if choice == "r": show_linux_readiness()
         +-- if choice == "x": review_mode()
         +-- if choice == "e": timed_exam_mode()
         +-- if choice == "v": GAME.save(); show_success("Gespeichert!")
         +-- if choice == "q": GAME.save(); GAME.running = False; break
```

**Finding:** The `if choice == "1"` through `choice == "22"` chain is 22 lines of hardcoded branches. Adding chapter 23 requires editing this list.

### Chapter Menu

```
chapter_menu(ch_id)
    |
    +-- Look up chapter data from CHAPTERS list
    +-- runner = MissionRunner(GAME.player, save_callback=GAME.auto_save)
    +-- while True:
         +-- Show all missions with completion markers
         +-- choice = prompt_input(f"kap{ch_id}")
         +-- if choice in ("q", "quit", "back"): break
         +-- if choice == "all": run all uncompleted missions
         +-- if choice starts with prefix (e.g., "1."):
              +-- mission_map lookup → runner.run(mission) → GAME.save()
         +-- if choice.isdigit(): index into list → runner.run()
         +-- if all missions completed: _show_chapter_complete() → break
```

**Finding:** `chapter_menu` has fragile string parsing:
- `choice.startswith(prefix)` for mission IDs
- `choice.isdigit()` for 1-based indexing
- These can conflict (e.g., typing "1" could mean "mission 1" OR "chapter 1 menu")

---

## Resource Management

- **Singleton:** `GAME = GameState()` is a global mutable singleton.
- **Memory:** Holds one `Player` reference. All chapter data is pre-loaded at import.
- **Save slots:** 3 JSON files on disk. Auto-save after every mission.
- **No threading:** Everything is single-threaded.

---

## Error Path

```
__main__ block
    |
    +-- except KeyboardInterrupt:
         +-- print exit message
         +-- if GAME.player: GAME.save()
         +-- sys.exit(0)
    |
    +-- except Exception as e:
         +-- print SYSTEM ERROR
         +-- traceback.print_exc()
         +-- sys.exit(1)
```

**Issues:**
- `KeyboardInterrupt` during `input()` causes the outer `except` to fire. If it happens mid-mission, `GAME.save()` saves the partially mutated state. This is actually good (no data loss), but the user sees an abrupt exit.
- Generic `except Exception` catches everything, including `SystemExit` and `GeneratorExit` (though `sys.exit(0)` inside `except KeyboardInterrupt` is fine).
- No recovery from `GameState` corruption.

---

## Performance Characteristics

- **Import time:** All 22 chapter files are imported unconditionally. This parses ~7,000 lines of Python data structures. Takes ~0.5-2 seconds.
- **Memory:** All missions stay in memory forever. ~500 Mission objects.
- **I/O bound:** The main loop spends 99%+ of time waiting for `input()`.
- **No background work:** No threads, no async, no polling.

---

## Observable Effects

- Boot sequence animation (first run only).
- Main menu with cyberpunk ASCII art.
- Chapter progress bars showing completion.
- Screen transitions between menus.
- Save file updated after every mission.

---

## Why This Design

This is a classic **menu-driven CLI application**. The `GameState` singleton centralizes the player's active session. The long `if/elif` chains in `game_hub()` and `chapter_menu()` are pragmatic for a small number of options. The unconditional import of all chapters is a trade-off: slower startup for simpler code (no lazy loading logic).

---

## Assessment

### What feels incomplete

**The issue:** No configuration system. The game has no settings file, no command-line arguments, no way to disable animations or colors.

**ELI5:** Imagine buying a TV that has no remote control, no volume button, and no menu. You can watch whatever is on, but you can't change anything.

**Impact:**
- Users who prefer no animations are stuck waiting.
- Users on terminals without color support see escape codes.
- No way to change save directory (hardcoded to `~/.neongrid9`).
- No way to start directly into a specific chapter or mission for testing.

**Robust Fixes:**
1. Add a `config.py` module that reads `~/.neongrid9/config.json` with settings for: `animation_speed`, `color_enabled`, `save_directory`.
2. Accept CLI arguments: `python3 main.py --chapter 5 --mission 3 --no-color`.
3. Use `argparse` for a minimal but extensible CLI.

---

### What feels vulnerable

**The issue:** `GAME` is a global mutable singleton. Any module can import it and modify `GAME.player`, `GAME.running`, or `GAME.save_slot`.

**ELI5:** Imagine a shared bank account where everyone in town has the PIN. Anyone can walk up to an ATM and change the balance, the PIN, or close the account.

**Impact:**
- A bug in any module could corrupt the global game state.
- Testing is hard because `GAME` persists between test cases (unless carefully reset).
- No separation of concerns: `GameState` mixes player data, save slot metadata, and loop control.

**Robust Fixes:**
1. Make `GameState` a proper class with private fields and read-only properties.
2. Pass `game_state` explicitly to functions that need it, rather than relying on the global.
3. For tests, use dependency injection: `def game_hub(game_state: GameState)` instead of accessing the global.

---

### What feels like bad design

**The issue:** `chapter_menu()` mixes three different input parsing strategies (mission ID string, numeric index, "all" keyword) with fragile string checks.

**ELI5:** Imagine a vending machine where you can select a snack by pressing a number, typing the snack's name, or saying "surprise me." But if you type "1", it might give you snack #1 OR charge you $1. The machine gets confused.

**Impact:**
- `choice.isdigit()` treats "1" as index 0 (first mission). But the user might have meant "mission 1.01".
- `choice.startswith(prefix)` for "1." will match "1.01", "1.1", etc. But what if a future chapter has 100+ missions? "10.01" might be ambiguous.
- No validation that the entered mission ID actually belongs to the current chapter.
- If the user types "boss" in chapter 1, it gets normalized to "1.boss" and looked up. But what if they type "BOSS" or "Boss"? The code lowercases, so it works, but this is implicit.

**Robust Fixes:**
1. Use a single parsing strategy: accept only mission IDs (e.g., "1.01") or a small set of keywords ("all", "next", "back").
2. Validate inputs with a schema before processing: `if not is_valid_mission_id(choice): show_error()`.
3. Replace the `if/elif` chain with a dispatch dictionary:
   ```python
   dispatch = {
       "all": play_all,
       "q": go_back,
   }
   # plus dynamic mission ID lookups
   ```
