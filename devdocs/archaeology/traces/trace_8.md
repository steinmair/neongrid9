# Trace 8: Chapter Data Interface

## Interface Surface

- `CHAPTER_1_MISSIONS` through `CHAPTER_22_MISSIONS` — module-level lists exported by each chapter file
- `CHAPTERS` — global tuple list in `main.py` mapping `(id, missions_list, topic_tag, title, subtitle)`
- `Mission` dataclass — instantiated at module import time in every chapter file
- `QuizQuestion` dataclass — nested inside `Mission` instances

**Called by:** `main.py` (imports and `CHAPTERS` construction), `main.py:chapter_menu()` (lookup by index or mission ID)
**Defined in:** `engine/mission_engine.py` (dataclasses), `missions/ch01_hardware.py` through `missions/ch22_final_exam.py` (data)

---

## Entry Point

The only entry point is the import statement at the top of `main.py`:

```
main.py (top level)
    |
    +-- from missions.ch01_hardware import CHAPTER_1_MISSIONS
    +-- from missions.ch02_boot import CHAPTER_2_MISSIONS
    +-- ... (22 explicit imports)
    +-- from missions.ch22_exam import CHAPTER_22_MISSIONS
    |
    +-- CHAPTERS = [
             (1, CHAPTER_1_MISSIONS, "101.1", "BOOT CAMP", "Hardware & BIOS/UEFI"),
             ...
             (22, CHAPTER_22_MISSIONS, "ALL", "FINAL EXAM PROTOCOL", "...")
         ]
```

---

## Execution Path

### Import-Time Side Effects

```
Python imports missions.ch01_hardware
    |
    +-- Top-level code executes immediately:
    +-- from engine.mission_engine import Mission, QuizQuestion
    +-- CHAPTER_1_MISSIONS = [
             Mission(mission_id='1.01', title='...', mtype='SCAN', xp=30, ...),
             Mission(mission_id='1.02', ...),
             ...
             Mission(mission_id='1.BOSS', mtype='BOSS', xp=200, ...),
         ]
    |
    +-- Each Mission() call constructs a dataclass with ~20 fields
    +-- Each QuizQuestion() call constructs nested question objects
    +-- Total: ~31 Mission objects + ~60 QuizQuestion objects for chapter 1 alone
```

**Finding:** All 22 chapter files execute their top-level `Mission(...)` constructors at import time. This means ~500 Mission objects and ~1,100 QuizQuestion objects are built before `main()` is even called. There is no lazy loading — a player who only wants chapter 1 still pays the cost of parsing all 22 files.

### Chapter Lookup in Game Hub

```
game_hub()
    |
    +-- for ch_id, missions, topic, title, subtitle in CHAPTERS:
    +--     show chapter progress bars
    +-- choice = prompt_input("hub")
    +-- if choice.isdigit() and 1 <= int(choice) <= 22:
    +--     chapter_menu(int(choice))
```

### Mission Lookup in Chapter Menu

```
chapter_menu(ch_id)
    |
    +-- ch_data = CHAPTERS[ch_id - 1]   # 0-based index into CHAPTERS
    +-- missions = ch_data[1]             # the actual list reference
    +-- Build mission_map: {m.mission_id: m for m in missions}
    +-- Display missions with completion markers
    +-- choice = prompt_input(f"kap{ch_id}")
    |
    +-- if choice.startswith(prefix) or choice.isdigit():
    +--     mission = mission_map.get(...) or missions[int(choice)-1]
    +--     runner.run(mission)
```

**Finding:** The lookup uses two different strategies:
1. String ID lookup (`mission_map.get("1.05")`) — reliable and explicit
2. Numeric index (`missions[4]`) — fragile if missions are reordered

---

## Resource Management

- **Memory:** All 22 chapter files remain in `sys.modules` after import. The `CHAPTERS` list holds 22 tuple references, each containing a reference to a list of ~20-30 `Mission` objects. Total memory: ~500 Mission objects + nested QuizQuestions + ASCII art strings. Estimated 2-5 MB.
- **Import time:** Parsing ~7,000 lines of Python data structures takes 0.5-2 seconds depending on hardware.
- **No I/O at runtime:** Once imported, all chapter data is in-memory. No file reads during gameplay.
- **Immutability:** The `Mission` dataclass instances are technically mutable (Python dataclasses have no enforced immutability), but the game treats them as read-only. `MissionRunner` never mutates a `Mission` object.

---

## Error Path

- **Missing chapter file:** ImportError at startup. The game crashes before reaching the menu.
- **Missing `CHAPTER_N_MISSIONS` variable:** ImportError or NameError at startup.
- **Corrupted mission data (e.g., missing required field):** The dataclass `__init__` would raise `TypeError` at import time, crashing the game before `main()` runs.
- **Mission ID not found in `mission_map`:** `runner.run()` is never called. The loop continues. No crash, but the user sees no feedback.
- **Index out of bounds in `missions[int(choice)-1]`:** If the user types a number higher than the mission count, this raises `IndexError`. The outer `except Exception` in `__main__` catches it and exits with a traceback.

---

## Performance Characteristics

- **Import time:** O(total_missions) = ~500 dataclass constructions. Dominates startup.
- **Lookup time:** O(1) for `mission_map` dict. O(1) for list index. Negligible.
- **Memory:** O(total_missions + total_quiz_questions + total_ascii_art_size). All held for process lifetime.
- **No runtime disk I/O** for chapter data after import.

---

## Observable Effects

- Chapter selection menu shows titles from `CHAPTERS` tuples.
- Progress bars in `game_hub()` iterate over `CHAPTERS` to count completed missions per chapter.
- Mission titles, stories, and ASCII art are rendered from the `Mission` objects.

---

## Why This Design

This is a **data-as-code** approach. All mission content is written as Python literals inside `.py` files rather than JSON, YAML, or a database. The benefits:
1. No parser needed — Python itself is the parser.
2. No external dependencies — no `json`, `toml`, or `sqlite3` loading logic.
3. Static validation — syntax errors in mission data are caught at import time.
4. Easy to version control — each chapter is a normal Python file in git.

The trade-off is unconditional loading at startup and tight coupling between content and code.

---

## Assessment

### What feels incomplete

**The issue:** There is no runtime validation that mission data is well-formed. A mission could have `quiz_questions=[]`, `expected_commands=[]` for a SCAN mission, or a `mission_id` that doesn't match its chapter number — and the game would still load it silently.

**ELI5:** Imagine a cookbook where some recipes are missing ingredients or have the wrong page numbers. The book still prints, but when someone tries to cook, the recipe fails halfway through.

**Impact:**
- A mission with no `quiz_questions` would crash or behave unexpectedly in `_run_quiz()`.
- A SCAN mission with empty `expected_commands` would make the terminal task impossible to complete.
- A `mission_id` mismatch (e.g., chapter 5 mission labeled "4.01") would break save-file compatibility and achievement tracking.

**Robust Fixes:**
1. Add a `validate_mission(m: Mission) -> List[str]` function that checks:
   - `mission_id` starts with `{chapter}.`
   - `mtype` is valid
   - `quiz_questions` has at least 1 question
   - `expected_commands` is non-empty for SCAN/INFILTRATE/CONSTRUCT/REPAIR
   - `hints` has 3 entries (or 0 for QUIZ)
2. Run validation at import time or in a CI test:
   ```python
   for ch in CHAPTERS:
       for m in ch[1]:
           errors = validate_mission(m)
           assert not errors, f"{m.mission_id}: {errors}"
   ```
3. Add a chapter audit script (similar to the one in CLAUDE.md) that runs on every commit.

---

### What feels vulnerable

**The issue:** All 22 chapter files are imported unconditionally. If a single chapter file has a syntax error, a NameError, or an invalid `Mission` field, the entire game crashes at startup. There is no graceful degradation (e.g., "Chapter 15 is unavailable, but the rest works").

**ELI5:** Imagine a restaurant where the kitchen refuses to open if even one ingredient is missing — even if that ingredient is for a dish nobody ordered today.

**Impact:**
- A typo in `missions/ch18_storage.py` prevents the game from launching at all.
- A missing comma in a `Mission(...)` call raises `SyntaxError` before the player sees the title screen.
- During development, editing any chapter file risks breaking the entire application.

**Robust Fixes:**
1. Wrap each chapter import in a try/except and mark failed chapters as "unavailable":
   ```python
   def load_chapter(n):
       try:
           mod = importlib.import_module(f"missions.ch{n:02d}_...")
           return getattr(mod, f"CHAPTER_{n}_MISSIONS")
       except Exception as e:
           log_error(f"Chapter {n} failed to load: {e}")
           return []
   ```
2. Use `importlib` for lazy loading: only import a chapter when the player first selects it.
3. Move mission data to JSON files that are validated by a schema before loading. This separates content from code and allows the engine to start even if one file is malformed.

---

### What feels like bad design

**The issue:** The `CHAPTERS` list in `main.py` is a manually maintained parallel structure to the imports. Adding chapter 23 requires editing **three** places: the import statement, the `CHAPTERS` list, and the `if choice == "23"` branch in `game_hub()` (see Trace 7).

**ELI5:** Imagine a school where the student roster is written on three different whiteboards in three different rooms. If a new student enrolls, someone has to update all three whiteboards — and it's easy to forget one.

**Impact:**
- **Maintenance burden:** 22 import lines + 22 tuple entries + 22 `if` branches = 66 places to edit for a new chapter.
- **Risk of inconsistency:** The `CHAPTERS` tuple order must exactly match the `if choice == "1".."22"` chain. If they drift, selecting chapter 5 might load chapter 6's data.
- **No self-registration:** Chapter files cannot declare their own metadata. They only export a list; `main.py` must know the title, topic, and subtitle for every chapter.

**Robust Fixes:**
1. **Self-registration pattern:** Each chapter file exports both its missions and its metadata:
   ```python
   # missions/ch23_future.py
   CHAPTER_23_MISSIONS = [...]
   CHAPTER_23_META = {"id": 23, "topic": "999.9", "title": "FUTURE", "subtitle": "..."}
   ```
   `main.py` discovers chapters dynamically instead of hardcoding them.

2. **Auto-discovery:** Use `importlib` + `pkgutil` to find all `missions.ch*` modules, import them, and build `CHAPTERS` automatically:
   ```python
   import pkgutil, importlib
   chapters = []
   for mod_info in pkgutil.iter_modules(missions.__path__):
       mod = importlib.import_module(f"missions.{mod_info.name}")
       missions = getattr(mod, f"CHAPTER_{n}_MISSIONS")
       meta = getattr(mod, f"CHAPTER_{n}_META")
       chapters.append((meta["id"], missions, meta["topic"], meta["title"], meta["subtitle"]))
   ```

3. **Remove the `if choice == "1".."22"` chain** (see Trace 7 for details) and replace it with a dynamic dispatch using the auto-discovered chapter count.

4. **Single source of truth:** If auto-discovery is too complex, at least generate `CHAPTERS` from the imports programmatically:
   ```python
   CHAPTER_IMPORTS = [
       (1, CHAPTER_1_MISSIONS, "101.1", "BOOT CAMP", "Hardware & BIOS/UEFI"),
       # ...
   ]
   CHAPTERS = CHAPTER_IMPORTS  # Only define once
   ```
   Then use `len(CHAPTERS)` to drive the menu loop instead of hardcoded `"22"`.
