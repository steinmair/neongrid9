# Trace 3: Terminal Simulation Interface

## Interface Surface

- `run_terminal(expected: list[str], task_description: str, hint_available: bool = False, hint_text: str = "", max_attempts: int = 5) -> tuple[bool, int, str]`
- `get_output(cmd: str) -> tuple[bool, str]`
- `normalize_cmd(cmd: str) -> str`

**Called by:** `engine.mission_engine.MissionRunner.run()` (fancy prompt fallback) and `MissionRunner._run_boss()`
**Calls into:** `engine.display.C`, `engine.display.prompt_input`, `engine.display.show_code`, `engine.display.show_error`, `engine.display.show_success`
**Internal data:** `SIMULATED_OUTPUTS` (global dict, ~4,000 lines)

---

## Entry Point

The terminal is entered from two places in `mission_engine.py`:

1. **Standard mission fallback:** After the fancy prompt loop fails 5 times, `run_terminal()` is called as a second chance.
2. **Boss phases:** Each boss phase calls `run_terminal(expected=[cmd], max_attempts=3)` directly.

The caller provides:
- `expected`: A list of valid command strings (e.g., `["lspci", "lspci -k"]`)
- `task_description`: What the player should do
- `hint_available` / `hint_text`: Whether to show a hint
- `max_attempts`: How many tries before giving up

---

## Execution Path

```
mission_engine.py:run_terminal(expected, task_description, hint_available, hint_text, max_attempts)
    │
    ├──► Print terminal simulation frame (box with "TERMINAL SIMULATION")
    │
    ├──► LOOP while attempts < max_attempts:
    │    │
    │    ├──► cmd = prompt_input("root@neongrid9")
    │    │    └──► Reads from stdin with "[root@neongrid9]> " prompt
    │    │
    │    ├──► Handle special commands:
    │    │    ├──► "quit"/"exit"/"q" → return (False, attempts, last_cmd)
    │    │    ├──► "hint" → print hint_text (if available)
    │    │    └──► "help" → print expected commands list
    │    │
    │    ├──► get_output(cmd) → LOOKUP PHASE
    │    │    │
    │    │    ├──► normalize_cmd(cmd) → cmd.strip().lower()
    │    │    │
    │    │    ├──► Attempt 1: EXACT string match in SIMULATED_OUTPUTS
    │    │    ├──► Attempt 2: Case-insensitive exact match
    │    │    ├──► Attempt 3: Prefix match (e.g., "lspci -vv" starts with "lspci -v")
    │    │    └──► Attempt 4: Base command match (first word matches first word of key)
    │    │
    │    ├──► If found: print output (max 20 lines, with "... (Ausgabe gekürzt)" if longer)
    │    │
    │    ├──► VALIDATION PHASE (separate from lookup!):
    │    │    │
    │    │    ├──► cmd_base = cmd.split()[0].lower()
    │    │    ├──► For each exp in expected:
    │    │    │    ├──► exp_base = exp.split()[0].lower()
    │    │    │    ├──► EXACT match: cmd.strip().lower() == exp.strip().lower() → SUCCESS
    │    │    │    └──► BASE match: cmd_base == exp_base AND len(expected) == 1 → SUCCESS
    │    │    └──► If success: return (True, attempts + 1, cmd)
    │    │
    │    └──► If not success: increment attempts, print warning with remaining count
    │         └──► Distinguish "command not found" vs "command executed but not the target"
    │
    └──► LOOP ENDS → return (False, attempts, last_cmd)
```

---

## Resource Management

- **Memory:** `SIMULATED_OUTPUTS` is a module-level global dict loaded at import time. It remains in memory for the process lifetime.
- **CPU:** Lookup is O(m * n) where m = number of simulated commands (~50-100) and n = average key length. In practice this is negligible.
- **I/O:** Blocks on `input()` via `prompt_input()`. No file or network I/O.
- **Output truncation:** Hard limit of 20 lines per output to prevent screen flooding.

---

## Error Path

The terminal simulator does not raise exceptions. It handles edge cases defensively:

- **Empty input:** `if not cmd: continue` — silently loops.
- **Unknown command:** `get_output()` returns `(False, "bash: {cmd}: command not found")`.
- **No expected commands:** Validation loop iterates over empty list → never matches → always fails.
- **KeyboardInterrupt:** Not caught here. Propagates to `main.py`.

**Silent behavior:** If `hint_text` is empty but `hint_available` is True, the "hint" command prints "Nicht verfügbar — check die Erklärung nochmal."

---

## Performance Characteristics

- **Lookup speed:** ~0.01 ms per command. Four nested loops over ~50 keys.
- **Output printing:** Truncated to 20 lines. Large outputs (like `lshw`) are pre-truncated in the dict itself.
- **No state persistence:** The terminal does not maintain a fake filesystem between calls. Each invocation is independent.
- **Memory footprint:** `SIMULATED_OUTPUTS` + string constants ≈ a few hundred KB.

---

## Observable Effects

- Terminal frame is drawn on screen.
- User sees simulated command output (green text).
- Wrong commands show warnings (yellow text).
- Special commands (hint, help, quit) have side effects.
- Return value tells the caller whether the task was completed.

---

## Why This Design

A simulated terminal is safer and more portable than a real shell. It prevents players from accidentally running destructive commands, works on Windows/macOS without Linux, and guarantees that the "correct" output is always shown regardless of the host system. The lookup-by-string approach is the simplest possible simulation: no parsing, no state machine, just pattern matching.

---

## Assessment

### What feels incomplete

**The issue:** The fake terminal has **no persistent state**. Commands like `cd /tmp` followed by `ls` would not work because `get_output()` does a static string lookup with no concept of a working directory or fake filesystem.

**ELI5:** Imagine a toy phone where every button plays a pre-recorded message. You can press "1" and hear "Hello," but you can't dial a number by pressing "1" then "2" then "3." Each press is independent.

**Impact:** Missions that require multi-step navigation (e.g., `cd /etc && cat fstab`) cannot be simulated as a sequence. The player must type the full command in one line. This limits the types of missions that can use the terminal — `CONSTRUCT` and `REPAIR` types are harder to implement realistically.

**Robust Fixes:**
1. Add a minimal `FakeFilesystem` class with a current directory, a directory tree, and file contents.
2. Parse common commands (`cd`, `ls`, `cat`, `pwd`) against the fake filesystem before falling back to `SIMULATED_OUTPUTS`.
3. Store filesystem state in the `MissionRunner` context so it persists across commands within a single mission.

---

### What feels vulnerable

**The issue:** The command validation and output simulation are **decoupled and use different matching logic**. A command can produce a realistic output (via `get_output()`) but still be rejected as "wrong" by the validation logic. Conversely, a command can be accepted as correct even if `get_output()` has no simulation for it.

**ELI5:** Imagine a teacher who grades your homework using a different answer key than the one they showed you in class. You might write something that looks perfect but still gets marked wrong. Or you might write gibberish that happens to match the secret answer key.

**Impact:**
- Player types `lspci -vv` → `get_output()` finds a match via prefix rule → prints realistic output → validation checks exact match against `["lspci -k"]` → fails because `-vv` != `-k`. Player is confused: "It worked, why is it wrong?"
- Player types `lspci -k` → `get_output()` finds exact match → prints output → validation succeeds. Good.
- Player types `lspci` → `get_output()` finds exact match → prints output → validation against `["lspci -k"]` → **base match succeeds because `len(expected) == 1`** → accepted! But `lspci` without `-k` is technically a different command.

The base-match fallback (`len(expected) == 1`) is a fuzzy heuristic that can accept wrong commands.

**Robust Fixes:**
1. Unify matching: Use the same logic for output simulation AND validation. If `get_output()` found the command, and the normalized base matches the expected base, accept it.
2. Remove the `len(expected) == 1` special case. Instead, allow a configurable "strictness" per mission.
3. Provide a `SIMULATED_COMMANDS` registry that maps expected commands to their canonical outputs, so validation and simulation draw from the same source of truth.

---

### What feels like bad design

**The issue:** `SIMULATED_OUTPUTS` is a single, flat, ~4,000-line global dictionary defined at module level. It mixes outputs from all 22 chapters, is loaded unconditionally at import time, and has no namespacing or lazy loading.

**ELI5:** Imagine a restaurant where every dish from every cuisine in the world is on one giant menu. When you sit down, the waiter brings you the entire menu even if you only want a sandwich. It's overwhelming, slow to flip through, and hard to update.

**Impact:**
- **Startup time:** All 4,000+ lines of output strings are parsed and stored in memory at import time, even if the player never uses the terminal.
- **Maintenance:** Adding a new command requires scrolling through 4,000 lines to find where to insert it. No per-chapter organization.
- **Naming collisions:** Two chapters might want different outputs for the same command string (e.g., `ls` in chapter 4 vs chapter 18). The flat dict can't handle this.
- **No extensibility:** Content authors can't add new simulations without editing `engine/terminal_sim.py`, which violates the engine/data separation.

**Robust Fixes:**
1. **Lazy loading:** Load outputs on first use via a `SimulatedCommandRegistry` that caches lookups.
2. **Namespacing:** Store outputs in chapter-specific sub-dicts (e.g., `SIMULATED_OUTPUTS["ch01"]["lspci"]`).
3. **Data-driven:** Move output strings into the `Mission` dataclass as a `simulated_outputs` field. The engine uses the mission's own data instead of a global dict.
4. **Modular files:** Split `SIMULATED_OUTPUTS` into per-chapter files (`engine/terminal_outputs/ch01_hardware.py`) that are imported on demand.
