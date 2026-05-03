# Technical Concepts Inventory

## Core Data Modeling

### Dataclass-Driven Entities
Python `@dataclass` is the exclusive data modeling tool. `Mission` (~20 fields), `QuizQuestion` (5 fields), `Player` (~20 fields), `Achievement` (5 fields), and `HintRequest` (4 fields) are all dataclasses. This gives automatic `__init__`, `__repr__`, and type hints without external dependencies.

**Status:** Fully implemented. All game data is structured via dataclasses.

### Manual Serialization (`to_dict` / `from_dict`)
Every mutable entity implements hand-written serialization. `Player.to_dict()` converts `set` → `list` for JSON compatibility. `Player.from_dict()` reconstructs objects with `.get()` defaults for missing keys, acting as an implicit migration layer.

**Status:** Implemented but fragile. Adding a new field requires editing 4 places. The `achievements` field is missing from `to_dict()` — a live data-loss bug.

### Import-Time Data Construction ("Data as Code")
All 500+ `Mission` and 1,100+ `QuizQuestion` objects are instantiated at module import time in `missions/ch*.py` files. Python itself is the parser; no JSON/YAML loader exists.

**Status:** Fully implemented. All 22 chapter files are eagerly imported at startup. No lazy loading.

### Global Mutable Singleton (`GameState`)
`GAME = GameState()` is a module-level singleton holding the active `Player`, save slot, and loop control flag. Any module can import and mutate it directly.

**Status:** Implemented. Used as the single source of runtime game state.

---

## Rendering & Display

### ANSI Escape Code Palette (`class C`)
A static class `C` holds 15+ pre-computed ANSI escape strings (colors, bold, dim, combined aliases like `NEON`, `WARN`, `DANGER`). All UI output concatenates these strings directly.

**Status:** Fully implemented. Hardcoded sequences assume modern terminal support. No fallback for `dumb` TERM or Windows pre-Terminal.

### Stateless Direct-to-Stdout Rendering
The display layer has no internal buffer, no screen buffer, and no double-buffering. Each function writes directly to `sys.stdout` via `print()` and `sys.stdout.write()`.

**Status:** Fully implemented. Functions like `clear()`, `typewrite()`, `show_story()` execute immediate side effects.

### Animated Text with Hardcoded Delays
`typewrite()` iterates characters with `time.sleep(0.018)` per char. `show_story()` multiplies delay by line length (`delay * len(line)`), creating forced waits up to 15+ seconds per story.

**Status:** Fully implemented. Delays are hardcoded constants inside functions. No `animate=False` parameter exists.

### Subprocess-Based Screen Clearing
`clear()` shells out to the OS (`cls` on Windows, `clear` on Unix) instead of using ANSI escape sequences (`\033[2J\033[H`).

**Status:** Implemented. Slower than native ANSI and may fail in restricted environments (Docker, AppArmor, SELinux).

---

## Persistence

### JSON File Save Slots
Three JSON files (`~/.neongrid9/save_slot{1,2,3}.json`) store player state. `json.dump()` with `ensure_ascii=False` and `indent=2` produces human-readable output.

**Status:** Fully implemented. No backup, no atomic write, no schema validation.

### Auto-Save After Every Mission
`MissionRunner` accepts a `save_callback` callable invoked after every mission completion. For a full playthrough, this triggers ~500 disk writes.

**Status:** Fully implemented. No debouncing or batching.

---

## Terminal Simulation

### Static String Dictionary Lookup (`SIMULATED_OUTPUTS`)
A flat global dict (~4,000 lines, ~100 keys) maps command strings like `"lspci -k"` to pre-written output strings. No command parsing, no fake filesystem, no state persistence between invocations.

**Status:** Fully implemented. Mixed outputs from all 22 chapters in one flat dict. No namespacing.

### Multi-Strategy Command Matching
Validation uses three fallback strategies in order: (1) exact string match, (2) case-insensitive exact match, (3) prefix match, (4) base-command match (first word only, if `len(expected) == 1`).

**Status:** Implemented. Validation and output lookup use *different* matching logic, which can confuse players when a command prints realistic output but is rejected as "wrong."

### Fancy Prompt Fallback
After 5 failed attempts in the fancy prompt loop, the game falls back to `run_terminal()` — a full REPL simulator with separate command validation.

**Status:** Implemented. Two different input paths for the same mission, with different UX and hint behavior.

---

## State Management

### Direct Attribute Mutation (XP Deduction)
`MissionRunner.run()` directly mutates `self.player.xp = max(0, self.player.xp - hint_req.xp_cost)` instead of calling a method. This bypasses `add_xp()` and its level recalculation.

**Status:** Implemented. Can create an inconsistent state where level > recalculated level for the current XP.

### Hint Cost Array (`[0, 20, 50]`)
A hardcoded 3-element list determines XP cost per hint tier. If a mission defines 4+ hints, the 4th hint costs 50 XP (same as FINAL) because `min(level, 2)` caps the index.

**Status:** Implemented. No configuration or per-mission override.

### Gear Bonus Non-Stacking
`gear_bonus()` returns the highest applicable multiplier. Having both `ghost_mask` (+20% quiz) and `linux_badge` (+5% all) yields 1.25 total. But having two items for the *same* boost type gives only the highest.

**Status:** Implemented. Intentional but not communicated to the player.

### Reputation Migration on Load
`from_dict()` fills missing factions with `0` using a dict comprehension: `{f: saved_rep.get(f, 0) for f in FACTIONS}`. This silently handles save files created before a faction was added.

**Status:** Implemented. A lightweight, implicit data migration pattern.

---

## Input Handling

### Blocking `input()` Loop
`prompt_input()` uses Python's built-in `input()` with no timeout. The process blocks indefinitely waiting for the user to press Enter.

**Status:** Fully implemented. No async, no timeout, no non-blocking alternative.

### Validated Choice Input
`prompt_input()` accepts an optional `valid_choices` tuple. If provided, it loops until the lowercase input matches one of the choices.

**Status:** Implemented. Used for menus ("1/2/3/q") but not for free-text terminal commands.

---

## Python-Specific Techniques

### Circular Import Avoidance via Lazy Imports
`mission_engine.py` imports `GEAR_CATALOG` from `engine.player` *inside* methods rather than at module top level, breaking a circular import chain.

**Status:** Implemented. Pattern used twice in the codebase.

### Python 3.10 Version Gate
`main.py` checks `sys.version_info < (3, 10)` at module top level and exits with an error message if the version is too old.

**Status:** Implemented. Required for `match` statements or union syntax (`|`), though neither is used.

### `field(default_factory=...)` for Mutable Defaults
`Player` uses `field(default_factory=set)` and `field(default_factory=list)` for mutable fields like `completed_missions` and `inventory`, preventing the classic Python mutable-default bug.

**Status:** Implemented. Correctly used throughout.
