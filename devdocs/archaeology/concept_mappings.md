# Concept-to-Implementation Mapping — NeonGrid-9

*Every concept discovered during archaeology, traced to the actual files that implement it. This explains not just what exists, but why it exists in its current form.*

---

## 1. Data Modeling & Persistence

### 1.1 Dataclass-Driven Entities

**Ideal:** All game entities modeled as type-safe, immutable data classes with validation.

**Implementation:**
- `engine/mission_engine.py` — `Mission` (~20 fields), `QuizQuestion` (5 fields)
- `engine/player.py` — `Player` (~20 fields)
- `engine/features.py` — `Achievement` (5 fields), `HintRequest` (4 fields)

**Coverage:** Partial (~70% realized)

| Aspect | Status |
|--------|--------|
| Type-safe constructors | Fully realized — `@dataclass` provides `__init__` with type hints |
| Immutable entities | Missing — no `frozen=True`; all dataclasses are mutable |
| Validation in constructors | Missing — no `__post_init__` validators |
| Automatic serialization | Missing — hand-written `to_dict()` / `from_dict()` instead of `dataclasses.asdict()` |

**Why it diverged:**
- The developer chose mutable dataclasses because `Player` is the primary mutable state container. Freezing it would require copying on every mutation.
- No `__post_init__` validation because the data was considered "static and complete" after the 2026-04-21 audit. Runtime validation was deemed unnecessary.
- Manual serialization was chosen because `set` objects (like `completed_missions`) are not JSON-serializable by default. Writing a custom JSON encoder subclass felt like "infrastructure" when the goal was "get save/load working in 20 lines."

**Alternatives likely considered:**
1. A validation library — rejected due to "pure stdlib" constraint.
2. `dataclasses.asdict()` with custom encoder — rejected because it requires a small JSON encoder subclass, which the developer may have viewed as over-engineering.
3. `frozen=True` with `dataclasses.replace()` — rejected because every XP addition would require copying the entire `Player` object.

**Edge cases that shaped design:**
- The `achievements` field is a nested `AchievementTracker` object inside `Player`. The developer likely struggled with nested serialization and gave up, leaving it out of `to_dict()`.
- `from_dict()` uses `.get()` defaults for every field, silently handling older save files. This implicit migration pattern works but hides data corruption.

---

### 1.2 Manual Serialization

**Ideal:** Automatic, bidirectional serialization with schema validation.

**Implementation:**
- `engine/player.py` — `Player.to_dict()` (18 hardcoded keys), `Player.from_dict()` (18 hardcoded keys)
- `engine/save_system.py` — `json.dump(player.to_dict(), ...)` / `Player.from_dict(json.load(...))`

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| Round-trip serialization | Broken — `achievements` field is lost on save |
| Schema versioning | Missing — no `version` field in save JSON |
| Validation on load | Missing — `from_dict()` accepts arbitrary keys and ignores unknowns |
| Migration support | Implicit only — `.get()` defaults handle missing keys |

**Why it diverged:**
- The `Player` class started small (~5 fields). Manual serialization was trivial. By the time it grew to 10+ fields, the pattern was entrenched.
- Content production (501 missions) took priority over engine refactoring.
- The developer assumed the schema was "frozen" after project completion.

**Alternatives likely considered:**
1. `dataclasses.asdict()` + custom encoder — considered but rejected for the `set` → `list` conversion problem.
2. A schema validation library — rejected due to "pure stdlib" constraint.
3. A binary serialization format — rejected because JSON is human-readable and safe.

**Edge cases that shaped design:**
- Older save files missing faction data are silently patched with `.get("factions", {})`. This works but could hide corruption.
- A hand-edited save with `"xp": "not_a_number"` would crash on `self.xp += amount` later, not during load.

---

### 1.3 JSON File Save Slots

**Ideal:** Atomic writes, backup rotation, schema validation, versioned migration.

**Implementation:**
- `engine/save_system.py` — `save_game()`, `load_game()`, `slot_info()`, `delete_save()`
- Files: `~/.neongrid9/save_slot{1,2,3}.json`

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Human-readable JSON | Fully realized — `indent=2`, `ensure_ascii=False` |
| Multiple slots | Fully realized — 3 independent files |
| Atomic write | Missing — writes directly to target file |
| Backup/rotation | Missing — no backup files |
| Schema validation | Missing — no runtime checks |
| Error handling | Partial — generic `try/except` swallows errors silently |

**Why it diverged:**
- The developer followed the "Keep It Simple" principle. For a single-user CLI game, a JSON file is the lightest possible persistence layer.
- Atomic writes (write to temp file, then rename) would require additional file operations, which the developer likely did not consider necessary.
- No backup because the auto-save frequency (after every mission) would create too many backup files.

**Alternatives likely considered:**
1. A local database — rejected as overkill for a single-user game with no queries.
2. A binary serialization format — rejected because JSON is human-readable and editable.
3. A key-value store — rejected because JSON is simpler and cross-platform.

**Edge cases that shaped design:**
- Auto-save after every mission means a full playthrough triggers ~500 disk writes. The developer accepted this because SSDs handle it easily and the JSON files are small (~20-50 KB).
- The return value of `save_game()` is ignored by `GAME.auto_save()`, so silent failures go unnoticed.

---

### 1.4 Import-Time Data Construction

**Ideal:** Lazy loading, runtime validation, content-code separation.

**Implementation:**
- `missions/ch01_hardware.py` through `missions/ch22_final_exam.py` — top-level `Mission(...)` and `QuizQuestion(...)` constructor calls
- `main.py` — 22 explicit `from missions.chXX import CHAPTER_XX_MISSIONS` statements
- `main.py` — `CHAPTERS = [(1, CHAPTER_1_MISSIONS, ...), ...]` tuple list

**Coverage:** Fully realized for loading, missing for validation and lazy loading.

| Aspect | Status |
|--------|--------|
| Content as Python literals | Fully realized |
| Eager loading at startup | Fully realized — all 22 files imported unconditionally |
| Lazy loading | Missing — a player who only plays chapter 1 still loads all 22 |
| Runtime validation | Missing — no `validate_mission()` function |
| Graceful degradation | Missing — one syntax error crashes the entire game |

**Why it diverged:**
- The developer explicitly chose "Python is the parser" over JSON/YAML. Zero parser code, syntax errors caught at startup, easy git diffs.
- "Fail fast at startup" philosophy — better to crash immediately than discover a broken chapter mid-session.
- Fixed scope assumption — the game was designed as a complete 22-chapter experience. There was never an intention to add chapters dynamically.

**Alternatives likely considered:**
1. JSON files with `json.load()` — rejected because "Python is the parser" and JSON requires validation logic.
2. YAML — rejected due to external dependency.
3. A local database — rejected as overkill and requiring schema management.
4. Dynamic module loading — rejected because it feels like "magic" and the developer preferred explicit imports.

**Edge cases that shaped design:**
- A `SyntaxError` in any chapter file crashes the game before the title screen. The developer accepted this as a feature, not a bug.
- Adding chapter 23 requires editing 66 places (22 imports + 22 CHAPTERS tuples + 22 `if/elif` branches). The developer did not consider this a problem because the scope was fixed.

---

## 2. Rendering & Display

### 2.1 ANSI Escape Code Palette

**Ideal:** Cross-platform color support with automatic fallback for terminals without ANSI.

**Implementation:**
- `engine/display.py` — `class C` with 15+ static ANSI escape strings
- Usage: concatenated directly into `print()` and `sys.stdout.write()` calls

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| Color aliases | Fully realized |
| Cross-platform support | Partial — older Windows terminals show raw codes |
| Fallback for `dumb` TERM | Missing — no detection, no no-color mode |
| Windows compatibility layer | Missing — no external color library |

**Why it diverged:**
- Pure stdlib constraint — external color libraries are packages.
- The developer assumes modern terminal support (Windows Terminal, iTerm2, GNOME Terminal).
- "Atmosphere is a feature" — colors are considered essential, not optional.

**Alternatives likely considered:**
1. A cross-platform color library — rejected due to external dependency.
2. A rich text library — rejected due to external dependency.
3. Terminal capability detection (`os.environ.get('TERM')`) — not implemented, likely deemed unnecessary.

**Edge cases that shaped design:**
- CI logs and `dumb` terminals show raw escape sequences. The developer either did not test in these environments or accepted the trade-off.

---

### 2.2 Animated Text with Hardcoded Delays

**Ideal:** Configurable animation speed, skippable animations, accessibility mode.

**Implementation:**
- `engine/display.py` — `typewrite(text, delay=0.018, color=C.WHITE)`
- `engine/display.py` — `show_story(speaker, text)` with `delay * len(line)`
- `engine/display.py` — `show_transition(text)` with hardcoded sleep
- `engine/display.py` — `level_up_screen()` with 1.5-second forced wait

**Coverage:** Partial (~40% realized)

| Aspect | Status |
|--------|--------|
| Typewriter animation | Fully realized |
| Story pacing | Fully realized — linear delay per character |
| Configurable speed | Missing — no `Config` object, no CLI flags |
| Skip animation | Missing — no key to skip, no `--no-animation` flag |
| Accessibility mode | Missing — screen readers struggle with timed text |
| Boot sequence animation | Fully realized — 13 lines of print + sleep |

**Why it diverged:**
- "Atmosphere is a feature" philosophy — delays are part of the cyberpunk mood.
- No test suite means the untestability of `time.sleep()` was invisible.
- Configuration = complexity. Adding a config system would require ~100+ lines of "infrastructure" code.

**Alternatives likely considered:**
1. `animate=False` parameter on every function — not implemented, likely because it would touch every display call.
2. A display driver abstraction with animated and instant modes — considered over-engineering for a terminal learning game.
3. A full terminal control library — rejected because it is complex and not universally supported.

**Edge cases that shaped design:**
- A 500-character story at 0.015s delay = 7.5 seconds of forced waiting. Speedrunners cannot bypass this.
- `time.sleep()` blocks the entire process. No background threads exist to handle interrupts during animation.

---

### 2.3 Stateless Direct-to-Stdout Rendering

**Ideal:** Screen buffer, partial redraws, responsive layout.

**Implementation:**
- `engine/display.py` — every function writes directly to `sys.stdout` via `print()`
- `clear()` wipes the entire screen before each new "screen"

**Coverage:** Fully realized for the chosen approach, missing for advanced features.

| Aspect | Status |
|--------|--------|
| Immediate stdout output | Fully realized |
| No internal buffer | Fully realized — stateless by design |
| Partial redraws | Missing — every screen is a full clear + redraw |
| Responsive sizing | Missing — width is hardcoded to 66-80 characters |
| Scrollback handling | Missing — long outputs scroll off-screen |

**Why it diverged:**
- For a terminal application with no overlapping windows, a full clear + redraw is the simplest mental model.
- Partial redraws require a screen buffer and dirty-region tracking — overkill for this use case.
- Hardcoded width assumes a standard 80-column terminal.

**Alternatives likely considered:**
1. A terminal windowing library — rejected as too complex for a menu-driven CLI.
2. A rich text layout library — rejected due to external dependency.
3. Panel-based layouts — rejected due to external dependency.

**Edge cases that shaped design:**
- Narrow terminals (<66 columns) will have box-drawing characters wrap awkwardly.
- No handling for terminal resize events.

---

### 2.4 Screen Clearing via OS Delegation

**Ideal:** Fast, portable screen clearing using ANSI escapes.

**Implementation:**
- `engine/display.py` — `clear()` delegates to the OS via platform-specific commands

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Screen clearing | Fully realized |
| Speed | Suboptimal — subprocess is slower than ANSI escapes |
| Portability | Partial — fails in Docker, AppArmor, SELinux environments |
| ANSI alternative | Missing — escape-based clearing not used |

**Why it diverged:**
- The developer may not have known the ANSI clear sequence, or preferred the subprocess approach for "compatibility."
- The OS clear command works on every Unix system; ANSI escapes might not work on all terminals.
- Inconsistent with the rest of `display.py`, which uses ANSI codes for everything else.

**Alternatives likely considered:**
1. ANSI escape sequences — known but not used.
2. Platform-specific native APIs — too complex.

**Edge cases that shaped design:**
- In restricted environments (SSH without TTY, Docker), the subprocess fails silently. The screen may not clear.

---

## 3. Game Flow & Mission Execution

### 3.1 Template Method Pattern

**Ideal:** Extracted phase classes, composable mission flow, testable units.

**Implementation:**
- `engine/mission_engine.py` — `MissionRunner.run()` is a ~250-line method with inline phase logic
- Phases are not extracted; they exist as sequential blocks of code

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Rigid sequence enforced | Fully realized — story → explanation → terminal → quiz → rewards |
| Phase extraction | Missing — all in one method |
| Composability | Missing — special modes reimplement quiz loops |
| Testability | Missing — mocking requires stubbing 15+ display functions |
| Transaction safety | Missing — XP deducted for hints mid-mission with no rollback |

**Why it diverged:**
- "One screen, one function" philosophy — the developer views a mission as a linear script that runs top-to-bottom.
- Breaking it into 5 classes/methods would mean jumping around the file to understand the flow. For a solo developer, linear readability beats modularity.
- No test suite means the untestability was invisible.
- The rigid sequence is pedagogically intentional — it creates a predictable learning rhythm.

**Alternatives likely considered:**
1. Phase classes — considered but rejected as "too many abstractions."
2. Pipeline pattern with context object — considered over-engineering.
3. Strategy pattern per mission type — partially used (BOSS calls `_run_boss()`), but not fully extracted.

**Edge cases that shaped design:**
- If the game crashes after XP is added but before `save_callback`, the player keeps XP but not the mission completion. No transaction system exists.
- The `if/elif` chain for mission types (SCAN, INFILTRATE, etc.) is hardcoded. Adding an 8th type requires editing `run()` and `display.py`.

---

### 3.2 Mission Type Taxonomy

**Ideal:** Type-safe enum with strategy pattern dispatch.

**Implementation:**
- `engine/mission_engine.py` — `mtype` is a `str` field on `Mission`
- Hardcoded checks: `if mission.mtype == "BOSS":`, `if mtype in ["SCAN", "INFILTRATE", ...]`
- `engine/display.py` — `type_colors` dict maps types to ANSI colors

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| Seven distinct types | Fully realized |
| Type safety | Missing — string comparison instead of Enum |
| Strategy dispatch | Partial — BOSS has `_run_boss()`, others are inline branches |
| Extensibility | Poor — adding a type requires editing multiple files |

**Why it diverged:**
- String types are simpler than Enums for a small, fixed set. No need to import an Enum class everywhere.
- The developer likely started with 3-4 types and added more organically. By the time there were 7, refactoring to an Enum felt like churn.

**Alternatives likely considered:**
1. `enum.Enum` — not used, likely because string comparisons are "good enough."
2. Subclassing `Mission` per type — rejected because dataclass inheritance adds complexity.
3. Strategy pattern with a dispatch dict — partially present but not fully extracted.

**Edge cases that shaped design:**
- `CONSTRUCT` type uses a raw ANSI escape string instead of a `C.*` alias in `type_colors`, creating inconsistency. This suggests the type was added after the color system was established.

---

### 3.3 Replay Gate

**Ideal:** Configurable replay rules, full state reset on replay, proper XP scaling.

**Implementation:**
- `engine/mission_engine.py` — `run()` checks `if mission.mission_id in self.player.completed_missions and mission.mtype != "BOSS"`
- `_replay_mission()` shows only the quiz for half XP

**Coverage:** Partial (~70% realized)

| Aspect | Status |
|--------|--------|
| Non-BOSS replay allowed | Fully realized |
| BOSS replay blocked | Fully realized |
| Quiz-only replay | Fully realized |
| Half XP on replay | Fully realized |
| Full mission replay | Missing — story and terminal are skipped |
| Replay limits | Missing — unlimited replays |

**Why it diverged:**
- The developer wanted to encourage review without enabling XP farming. Skipping the story and terminal prevents grinding.
- BOSS missions are one-time events for narrative impact.

**Alternatives likely considered:**
1. Full mission replay with reduced XP — rejected because it would take too long and add little value.
2. No replay at all — rejected because review is part of the learning process.
3. Cooldown timers — rejected as unnecessary complexity.

**Edge cases that shaped design:**
- A player could replay the same easy mission infinitely for small XP gains. The developer accepted this because the half-XP rate is low and the game is not competitive.

---

## 4. Terminal Simulation

### 4.1 Static String Dictionary Lookup

**Ideal:** Command parser, fake filesystem, persistent state between commands.

**Implementation:**
- `engine/terminal_sim.py` — `SIMULATED_OUTPUTS` dict maps command strings to pre-written output blocks
- No parsing, no filesystem, no state persistence

**Coverage:** Partial (~40% realized)

| Aspect | Status |
|--------|--------|
| Command output lookup | Fully realized |
| ~100 command strings | Fully realized |
| Realistic output formatting | Fully realized |
| Command parsing | Missing — string matching only |
| Fake filesystem | Missing — directory navigation does not persist |
| Persistent state between commands | Missing — each invocation is independent |
| Namespacing by chapter | Missing — flat dict with all commands |

**Why it diverged:**
- String dict lookup is the simplest possible simulation. No parser, no state machine, no filesystem.
- A fake filesystem would require implementing navigation, directory tree traversal, and file contents. This is complex and error-prone.
- The developer prioritized content (501 missions) over terminal fidelity.

**Alternatives likely considered:**
1. Real subprocess execution — rejected because it is unsafe.
2. Full command parser with AST — rejected as overkill.
3. Fake path objects with directory tree — considered but deemed too complex.
4. Per-chapter output dicts — not implemented, likely because the developer did not anticipate naming collisions.

**Edge cases that shaped design:**
- Two chapters might want different outputs for the same command (e.g., `ls` in chapter 4 vs chapter 18). The flat dict handles this by having one canonical output per command.
- Multi-step missions requiring directory navigation cannot be simulated as a sequence. The player must type the full command in one line.

---

### 4.2 Multi-Strategy Command Matching

**Ideal:** Unified validation and simulation, configurable strictness per mission.

**Implementation:**
- `engine/terminal_sim.py` — `get_output()` uses 4 fallback strategies: exact, case-insensitive, prefix, base command
- `engine/mission_engine.py` — validation uses separate logic: exact match, base match (if `len(expected) == 1`)

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Exact string match | Fully realized |
| Case-insensitive match | Fully realized |
| Prefix match | Fully realized |
| Base command fallback | Partial — only if `len(expected) == 1` |
| Unified validation + simulation | Missing — different logic for each |
| Configurable strictness | Missing — no per-mission setting |

**Why it diverged:**
- The developer wrote output lookup and validation separately, likely at different times.
- The `len(expected) == 1` special case is a pragmatic shortcut for missions with a single expected command.
- No per-mission strictness because all missions were written by one developer with consistent expectations.

**Alternatives likely considered:**
1. Unified matching — use the same logic for both output lookup and validation. Not implemented, likely an oversight.
2. Regex-based matching — rejected as too complex and error-prone.
3. Exact match only — rejected because it would be too strict for players who add flags.

**Edge cases that shaped design:**
- Player types `lspci -vv` → output lookup finds it via prefix rule → prints realistic output → validation checks exact match against `["lspci -k"]` → fails. Player is confused: "It worked, why is it wrong?"
- Player types `lspci` → validation against `["lspci -k"]` → base match succeeds because `len(expected) == 1`. But `lspci` without `-k` is technically a different command.

---

### 4.3 Fancy Prompt Fallback

**Ideal:** Single, consistent terminal input path with unified UX.

**Implementation:**
- `engine/mission_engine.py` — Fancy prompt loop (up to 5 attempts, hint integration, XP deduction)
- `engine/terminal_sim.py` — `run_terminal()` full REPL (separate validation, separate UX)

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Primary input path | Fully realized (fancy prompt) |
| Fallback after 5 failures | Fully realized |
| Unified UX | Missing — jarring switch between paths |
| Unified hint behavior | Missing — REPL has different hint logic |
| Unified attempt counting | Missing — counters reset between paths |

**Why it diverged:**
- The fancy prompt was likely added after the REPL already existed, or vice versa. They were never unified.
- The fancy prompt is simpler and faster for single-command missions. The REPL is needed for multi-command missions (INFILTRATE, CONSTRUCT).
- The fallback exists to prevent players from getting permanently stuck.

**Alternatives likely considered:**
1. Use REPL for all missions — rejected because it is verbose and slow for simple missions.
2. Use fancy prompt for all missions — rejected because it cannot handle multi-step tasks.
3. Unify both into a single configurable prompt — not done, likely due to time constraints.

**Edge cases that shaped design:**
- A player who fails the fancy prompt 5 times and then succeeds in the REPL gets full XP. The 5 failures are "forgiven" by the fallback.
- The REPL shows a generic error message for unknown commands, but the fancy prompt shows a custom error message. The tone differs.

---

## 5. Progression & Meta-Game

### 5.1 XP & Leveling System

**Ideal:** Configurable thresholds, retroactive scaling, transparent formulas.

**Implementation:**
- `engine/player.py` — `LEVELS` list (15 tuples: level, title, xp_threshold)
- `engine/player.py` — `add_xp(amount)` with level scaling (+10% at L5, +20% at L10, +30% at L15)
- `engine/player.py` — `_recalculate_level()` iterates thresholds in reverse

**Coverage:** Partial (~70% realized)

| Aspect | Status |
|--------|--------|
| 15 levels with titles | Fully realized |
| Exponential XP thresholds | Fully realized |
| Incoming XP scaling | Fully realized |
| Retroactive scaling | Missing — past XP is not recalculated |
| Configurable thresholds | Missing — hardcoded list |
| Transparent formula to player | Partial — scaling is applied silently |

**Why it diverged:**
- Incoming-only scaling is simpler to implement and understand. Retroactive scaling would require recalculating total XP on every level-up.
- Hardcoded thresholds are fine for a fixed-scope game with no plans for expansion.

**Alternatives likely considered:**
1. Retroactive scaling — rejected as confusing (player's total XP would jump unpredictably).
2. Formula-based levels — rejected because custom titles per level require a lookup table anyway.
3. A calculation function instead of a threshold list — not used, likely because the developer preferred explicit thresholds.

**Edge cases that shaped design:**
- A player at level 10 who uses a hint costing 50 XP drops to 0 XP but stays level 10. `add_xp()` handles level-up but there is no `deduct_xp()` method to handle level-down.

---

### 5.2 3-Tier Hint System

**Ideal:** Configurable hint costs, per-mission override, unlimited hints.

**Implementation:**
- `engine/features.py` — `HintLevel` enum (FREE=0, STANDARD=1, FINAL=2)
- `engine/features.py` — `HintRequest.create()` with hardcoded cost array `[0, 20, 50]`
- `engine/mission_engine.py` — XP deduction on hint use

**Coverage:** Partial (~70% realized)

| Aspect | Status |
|--------|--------|
| Free hint | Fully realized |
| 20 XP hint | Fully realized |
| 50 XP final hint | Fully realized |
| Per-mission cost override | Missing — all missions use same costs |
| Unlimited hints | Partial — capped at `len(mission.hints)` |
| Hint history tracking | Missing — no record of which hints were used when |

**Why it diverged:**
- Hardcoded costs are simple and consistent. Players know what to expect.
- Per-mission override was never needed because all missions were designed with the same hint structure.

**Alternatives likely considered:**
1. Configurable costs per mission — rejected as unnecessary complexity.
2. Cooldown between hints — rejected because it would frustrate stuck players.
3. No hint cost — rejected because free final hints would remove the challenge.

**Edge cases that shaped design:**
- If a mission defines 4+ hints, the 4th hint costs 50 XP (same as FINAL) because `min(level, 2)` caps the index. The developer likely assumed all missions have exactly 3 hints.
- Hint XP deduction bypasses `add_xp()`, so level recalculation does not happen. A player could go to 0 XP and stay at their current level.

---

### 5.3 Achievement System

**Ideal:** Event-driven engine, 100% trigger coverage, centralized predicates.

**Implementation:**
- `engine/features.py` — `Achievement` dataclass, `AchievementTracker` class, `ACHIEVEMENTS` dict (19 items)
- `engine/mission_engine.py` — ~10 inline `if` checks scattered in `run()` and `_run_boss()`

**Coverage:** Partial (~70% realized)

| Aspect | Status |
|--------|--------|
| 19 defined achievements | Fully realized |
| Achievement unlock tracking | Fully realized (AchievementTracker) |
| Inline trigger checks | Fully realized |
| Event-driven architecture | Missing — no central achievement engine |
| `perfect_quiz` trigger | Missing — never checked |
| `no_hints` trigger | Missing — never checked |
| Centralized predicates | Missing — logic scattered in 250-line method |

**Why it diverged:**
- 19 achievements felt "small enough" for inline `if` statements. Event-driven architecture is perceived as over-engineering for <20 conditions.
- No CI pipeline means dead achievements are invisible. The developer simply forgot to wire up `perfect_quiz` and `no_hints`.
- The template method bias — achievement checks are viewed as "part of the reward phase," not a separate subsystem.

**Alternatives likely considered:**
1. A central achievement engine with event registration — considered but rejected as over-engineering.
2. Decorator-based triggers — too "magical" for the developer's taste.
3. A separate achievements module with all trigger logic — partially present in `features.py`, but not fully extracted.

**Edge cases that shaped design:**
- `quest_marathon` checks `len(completed_missions) == 100` exactly. If a future "complete all" feature skips from 99 to 101, the achievement never triggers.
- `boss_defeated` is checked in both `run()` and `_run_boss()`, causing a double-check for every boss.

---

### 5.4 Gear System

**Ideal:** Stackable bonuses, mechanical impact on gameplay, equip/unequip system.

**Implementation:**
- `engine/player.py` — `GEAR_CATALOG` dict (13 items with rarity, tier, boost type)
- `engine/player.py` — `gear_bonus(boost_type)` returns highest applicable multiplier
- `engine/mission_engine.py` — gear awarded by boss missions

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| 4 rarity tiers | Fully realized |
| 13 gear items | Fully realized |
| XP boost mechanics | Fully realized |
| Non-stacking for same type | Fully realized — highest wins |
| Equip/unequip system | Missing — all gear is passive |
| Mechanical gameplay impact | Missing — gear only affects XP, nothing else |
| Inventory UI | Partial — `show_inventory()` lists items with colors |

**Why it diverged:**
- Gear is narrative-only by design. The developer wanted collection rewards without complicating the core loop.
- An equip/unequip system would require UI for selection, validation for slot limits, and potentially unbalanced combinations.

**Alternatives likely considered:**
1. Stackable bonuses — rejected because it could lead to absurd multipliers.
2. Gear slots — rejected as too RPG-like for a learning tool.
3. Active gear abilities — rejected because it would distract from the learning content.

**Edge cases that shaped design:**
- Having both `ghost_mask` (+20% quiz) and `linux_badge` (+5% all) gives 1.25 total. But having two items for the *same* boost type gives only the highest. The comment says "Boni stapeln sich nicht" (bonuses do not stack), which is intentional but not communicated to the player.

---

### 5.5 Faction System

**Ideal:** Faction-locked content, reputation-based gameplay, mechanical impact.

**Implementation:**
- `engine/features.py` — `FACTIONS` list (5 names), `calculate_level()` for reputation bars
- `engine/features.py` — `FactionStatus` class (dead code — never instantiated)
- `engine/player.py` — `factions: Dict[str, int]` (0-100 scale)
- `engine/mission_engine.py` — `player.add_reputation()` on mission completion

**Coverage:** Partial (~30% realized)

| Aspect | Status |
|--------|--------|
| 5 factions defined | Fully realized |
| Reputation tracking | Fully realized |
| Reputation display bars | Partial — manually built in `stats_summary()`, `FactionStatus` unused |
| Faction-locked missions | Missing |
| Faction wars / conflict | Missing |
| Mechanical impact | Missing — purely cosmetic |
| `FactionStatus` class usage | Missing — dead code |

**Why it diverged:**
- The faction system was likely planned as a deeper mechanic but was deprioritized during content production.
- `FactionStatus` was written but never wired into `stats_summary()`. The developer built reputation bars inline instead.
- Narrative-only reputation is sufficient for the target audience (certification learners, not RPG players).

**Alternatives likely considered:**
1. Faction-locked missions — rejected because it would require gating content behind arbitrary reputation thresholds.
2. Faction-specific gear bonuses — not implemented, likely because gear already has its own boost system.
3. Delete `FactionStatus` — not done, likely because the developer intended to use it later.

**Edge cases that shaped design:**
- Reputation can exceed 100 (capped only by `min(100, ...)`). A bug that passes a large amount would cap correctly.
- `calculate_level()` handles reputation (0-100) and XP (>100) with the same function, using a magic threshold of 100. This is a hidden coupling.

---

## 6. Input Handling

### 6.1 Blocking Input Loop

**Ideal:** Non-blocking input, timeout support, command history, tab completion.

**Implementation:**
- `engine/display.py` — `prompt_input(label, valid_choices=None)` wraps built-in `input()`
- `engine/display.py` — `prompt_continue()` waits for Enter press

**Coverage:** Partial (~40% realized)

| Aspect | Status |
|--------|--------|
| Basic text input | Fully realized |
| Choice validation | Partial — `valid_choices` tuple checks lowercase match |
| Timeout | Missing — blocks indefinitely |
| Command history | Missing — no readline integration |
| Tab completion | Missing |
| Multi-line input handling | Missing — pasting multi-line text breaks display |

**Why it diverged:**
- Pure stdlib constraint — readline is in the stdlib but requires platform-specific handling and does not work well on Windows.
- The game is turn-based; non-blocking input is unnecessary.
- Tab completion would require maintaining a list of valid commands, which the developer did not prioritize.

**Alternatives likely considered:**
1. Readline for history — considered but rejected due to Windows compatibility concerns.
2. A terminal control library for advanced input — rejected as too complex.
3. Custom input loop with select — rejected because it is non-portable.

**Edge cases that shaped design:**
- Pasting multi-line text or control characters into `input()` can break the display. The developer did not sanitize input.
- EOFError (piped input, Ctrl+D) is not caught. The game would crash with a traceback.

---

### 6.2 Validated Choice Input

**Ideal:** Schema-based input validation, fuzzy matching, error recovery.

**Implementation:**
- `engine/display.py` — `prompt_input()` accepts optional `valid_choices` tuple
- `engine/mission_engine.py` — `chapter_menu()` uses `choice.isdigit()`, `choice.startswith(prefix)`, and keyword checks

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Exact choice matching | Fully realized |
| Case-insensitive matching | Fully realized — `.lower()` comparison |
| Numeric index validation | Partial — no bounds checking before list access |
| Mission ID validation | Partial — `mission_map.get()` returns None silently |
| Fuzzy matching | Missing — typos are not corrected |
| Schema validation | Missing — no centralized input schema |

**Why it diverged:**
- Simple `if/elif` chains are readable for a small number of options. A dispatch dict would require more indirection.
- Fuzzy matching is unnecessary for a learning tool — the player should type the exact command.

**Alternatives likely considered:**
1. A command-line argument parser for menus — rejected because interactive CLI menus are different from CLI arguments.
2. Fuzzy string matching — not implemented, likely deemed unnecessary.
3. Centralized input router — not done, likely because each menu has unique logic.

**Edge cases that shaped design:**
- In `chapter_menu()`, typing "1" could mean "mission index 0" OR "mission ID 1.01" depending on the parsing path. The code tries `mission_map.get()` first, then falls back to `missions[int(choice)-1]`. If both fail, the loop continues silently.
- `choice.isdigit()` treats "0" as index -1 (IndexError) and numbers higher than mission count also raise IndexError. The outer `except Exception` in `__main__` catches this but exits the game.

---

## 7. Content & Validation

### 7.1 Speaker Distribution Rule

**Ideal:** Automated enforcement, per-chapter reporting, violation warnings.

**Implementation:**
- `engine/mission_engine.py` — `speaker_stats` tracked in `Player` (dict of speaker → count)
- `engine/player.py` — `stats_summary()` shows top 3 speakers
- `CLAUDE.md` — manual audit checklist mentions "no speaker >60% per chapter"

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Speaker tracking | Fully realized |
| Top speakers display | Fully realized |
| Per-chapter distribution check | Missing — no runtime enforcement |
| Automated audit | Missing — only manual check in CLAUDE.md |
| Violation warning | Missing — game loads silently even with 100% one speaker |

**Why it diverged:**
- Speaker distribution is a content policy, not a game mechanic. Runtime enforcement would be annoying during development.
- The manual audit was run once at project completion and considered sufficient.

**Alternatives likely considered:**
1. Runtime assertion on mission load — rejected because it would crash the game for content authors.
2. A CI script for speaker distribution — not implemented, likely because there is no CI pipeline.

**Edge cases that shaped design:**
- Chapter 18 is an intentional exception (EXAMINATOR dominates). A hard rule would break this design choice.

---

### 7.2 Story Transitions

**Ideal:** Configurable count, validation, graceful handling of missing transitions.

**Implementation:**
- `engine/mission_engine.py` — `run()` accesses `tr[0]` through `tr[3]`
- `engine/mission_engine.py` — guarded by `if tr:` to handle empty lists
- `Mission` dataclass — `story_transitions: List[str] = field(default_factory=list)`

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| 4 transitions assumed | Fully realized in code |
| Graceful handling of fewer | Partial — `if tr:` skips silently |
| Validation of exactly 4 | Missing — no runtime check |
| Configurable count | Missing — hardcoded to 4 |

**Why it diverged:**
- The developer trusted content authors to always provide 4 transitions. Runtime validation was deemed unnecessary for "static, complete" data.
- `default_factory=list` means missing transitions do not crash — they are silently skipped.

**Alternatives likely considered:**
1. A fixed-length tuple type — not used because dataclass tuple fields are awkward.
2. Validation in `__post_init__` — rejected to avoid runtime overhead.

**Edge cases that shaped design:**
- A mission with 3 transitions would skip the 4th transition display. The flow would continue without warning.
- A mission with 5 transitions would ignore the 5th. No error is raised.

---

### 7.3 Content Completeness Audit

**Ideal:** Automated CI check, runtime validation, schema enforcement.

**Implementation:**
- `CLAUDE.md` — manual audit script (Python code block with assertions)
- No runtime validation
- No CI pipeline

**Coverage:** Partial (~30% realized)

| Aspect | Status |
|--------|--------|
| Manual audit checklist | Fully realized in CLAUDE.md |
| Automated CI check | Missing — no CI configuration |
| Runtime validation | Missing — no `validate_mission()` function |
| Schema enforcement | Missing — dataclass types only, no semantic checks |
| Content freeze date | Documented — 2026-04-21 |

**Why it diverged:**
- The content was "frozen" after audit. The developer assumed static, complete data does not need runtime validation.
- No CI pipeline means no automated checks on commit.
- Writing a `validate_mission()` function would require ~50 lines of code — small, but the developer prioritized content over infrastructure.

**Alternatives likely considered:**
1. A schema validation library — rejected due to external dependency.
2. Hand-rolled validator — considered but not implemented.
3. A CI pipeline with content audit — not done because the project has no CI.

**Edge cases that shaped design:**
- A mission with empty `quiz_questions` would load silently and crash or behave unexpectedly in `_run_quiz()`.
- A SCAN mission with empty `expected_commands` would skip the terminal task entirely, making the mission trivial.

---

## 8. Architecture & Infrastructure

### 8.1 Three-Layer Architecture

**Ideal:** Strict separation with no cross-layer imports, interface contracts, dependency inversion.

**Implementation:**
- `missions/` — Data Layer (content)
- `engine/` — Engine Layer (business logic)
- `main.py` — Control Layer (menus, loops)

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| Physical separation | Fully realized — 3 distinct locations |
| Data layer purity | Fully realized — no logic, only data |
| Engine layer isolation | Partial — imports display directly |
| Control layer isolation | Poor — imports everything, knows all modules |
| Interface contracts | Missing — no abstract base classes or protocols |
| Dependency inversion | Missing — concrete imports everywhere |

**Why it diverged:**
- The project is small enough that strict layering feels like over-engineering. The developer preferred direct imports for readability.
- `main.py` as a "god module" is a common pattern in small CLI applications.
- No interfaces or protocols because Python duck typing is sufficient for a single-developer project.

**Alternatives likely considered:**
1. Protocol definitions for engine interfaces — not used, likely because there is only one implementation of each.
2. Dependency injection — rejected as unnecessary for a single-player CLI game.
3. Splitting `main.py` into multiple modules — considered but not done due to the "one entry point" convention.

**Edge cases that shaped design:**
- `main.py` imports `LEVELS` and `GEAR_CATALOG` directly from `engine.player`. If `player.py` is renamed, `main.py` breaks. The developer accepted this tight coupling.

---

### 8.2 Global Mutable Singleton

**Ideal:** Encapsulated state, dependency injection, testable isolation.

**Implementation:**
- `main.py` — `GAME = GameState()` at module level
- `GameState` holds `player`, `save_slot`, `running`

**Coverage:** Partial (~50% realized)

| Aspect | Status |
|--------|--------|
| Single instance | Fully realized |
| Player data access | Fully realized |
| Save slot tracking | Fully realized |
| Loop control | Fully realized |
| Encapsulation | Missing — all fields are public |
| Dependency injection | Missing — functions access `GAME` directly |
| Reset for testing | Missing — no `reset()` method |

**Why it diverged:**
- No concurrency, no multi-user conflicts, no race conditions. Global state is simpler than DI for this use case.
- The developer values "I can see where the state lives" over "the state is passed explicitly."

**Alternatives likely considered:**
1. Passing `game_state` to every function — rejected because it would add a parameter to every function signature.
2. Thread-local state — unnecessary for a single-threaded app.
3. Proper singleton with private constructor — rejected as "too Java-like."

**Edge cases that shaped design:**
- Any module can import `GAME` and mutate it. A bug in any module could corrupt the save slot.
- Testing requires manually resetting `GAME.player` between test cases.

---

### 8.3 Circular Import Avoidance

**Ideal:** Clean dependency graph, no import hacks.

**Implementation:**
- `engine/mission_engine.py` — lazy imports for `GEAR_CATALOG` inside methods
- `engine/player.py` ↔ `engine/features.py` — indirect cycle via `calculate_level`

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| Lazy import hack | Present — works but is undocumented |
| Clean module boundaries | Partial — `GEAR_CATALOG` should live in `features.py` |
| Circular dependency resolution | Missing — cycles are broken by hacks, not design |

**Why it diverged:**
- The developer discovered the circular import during development and used the lazy import as the quickest fix.
- Moving `GEAR_CATALOG` to `features.py` would break `player.py`'s cohesion (gear is player-related) or `features.py`'s cohesion (gear is not a feature).

**Alternatives likely considered:**
1. Move `GEAR_CATALOG` to a new dedicated module — not done, likely because it felt like over-engineering.
2. Move `calculate_level()` to `player.py` — not done, likely because it is used by both player and faction display.

**Edge cases that shaped design:**
- The lazy import is only used in two methods. If a third method needs `GEAR_CATALOG`, the developer might forget the lazy import pattern and reintroduce the circular dependency.

---

## 9. Special Modes

### 9.1 Timed Exam Mode

**Ideal:** Reuse quiz engine, random question selection, proper scoring.

**Implementation:**
- `main.py` — `timed_exam_mode()` pulls 60 questions from Chapter 22
- `main.py` — Custom quiz loop with live timer
- `main.py` — Scoring: 800 points max, 500 to pass

**Coverage:** Partial (~70% realized)

| Aspect | Status |
|--------|--------|
| 90-minute timer | Fully realized |
| Question randomization | Fully realized |
| Live countdown | Fully realized |
| Pass/fail calculation | Fully realized |
| Reuse of `_run_quiz()` | Missing — custom quiz loop instead |
| Difficulty scaling | Missing — all questions have equal weight |
| Per-domain scoring | Missing — only total score |

**Why it diverged:**
- `_run_quiz()` is tightly coupled to mission state (`player`, `chapter`, `record_quiz_result`). Reusing it for exam mode would require decoupling.
- The custom loop allows different UX (timer display, no hints, no XP rewards).

**Alternatives likely considered:**
1. Refactor `_run_quiz()` to accept a `quiz_mode` parameter — not done, likely because it would require significant changes.
2. A separate exam runner class — considered but merged into `main.py` for simplicity.

**Edge cases that shaped design:**
- The exam mode does not save results. A player who passes cannot prove it later. The developer assumed the exam is for practice, not certification.

---

### 9.2 Review Mode

**Ideal:** Weighted question selection, session tracking, progress analytics.

**Implementation:**
- `main.py` — `review_mode()` collects quiz questions from all chapters
- `main.py` — Weights poorly-performing chapters higher
- `main.py` — Presents 10 random questions per session

**Coverage:** Partial (~60% realized)

| Aspect | Status |
|--------|--------|
| Question collection | Fully realized |
| Poor-chapter weighting | Partial — simple weighting, not true spaced repetition |
| 10-question sessions | Fully realized |
| Immediate feedback | Fully realized |
| Session tracking | Missing — no record of review sessions |
| Adaptive difficulty | Missing — no adjustment based on performance |
| True spaced repetition algorithm | Missing — no interval-based scheduling |

**Why it diverged:**
- True spaced repetition requires tracking per-question intervals, ease factors, and review dates. This is complex.
- The developer implemented a simpler "weight by weakness" approach that is good enough for a learning tool.

**Alternatives likely considered:**
1. A full spaced repetition algorithm — rejected as overkill.
2. Per-question tracking — would require schema changes and more complex save files.
3. A simpler box-based system — simpler than full spaced repetition but still requires box tracking.

**Edge cases that shaped design:**
- A player who has completed all chapters equally has no "weak" chapters. Review mode falls back to uniform random selection.
- Questions from chapters with 0% accuracy are heavily weighted, but the player might not have enough questions from that chapter.

---

## Summary Matrix

| Concept | Files | Coverage | Divergence Reason | Alternative Considered |
|---------|-------|----------|-------------------|----------------------|
| Dataclass Entities | `mission_engine.py`, `player.py`, `features.py` | 70% | Mutable state needed; no validation assumed frozen | A validation library, `frozen=True` |
| Manual Serialization | `player.py`, `save_system.py` | 60% | Started small, grew organically; content priority | `dataclasses.asdict()` |
| JSON Save Slots | `save_system.py` | 50% | Keep it simple; auto-save on SSD is fine | A local database, binary format |
| Data as Code | `missions/ch*.py`, `main.py` | 70% | Python is the parser; fail-fast philosophy | JSON, YAML, a local database |
| ANSI Palette | `display.py` | 60% | Pure stdlib; assumes modern terminal | A cross-platform color library |
| Animated Text | `display.py` | 40% | Atmosphere is a feature; no tests | `animate=False`, display driver |
| Template Method | `mission_engine.py` | 50% | Linear readability; no test pain | Phase classes, pipeline |
| Mission Types | `mission_engine.py`, `display.py` | 60% | String comparison is simple; small fixed set | `Enum`, strategy dispatch |
| Terminal Simulator | `terminal_sim.py` | 40% | String dict is simplest; content priority | Real shell, fake filesystem |
| Command Matching | `terminal_sim.py`, `mission_engine.py` | 50% | Separate implementations, never unified | Unified matching, regex |
| Fancy Prompt Fallback | `mission_engine.py`, `terminal_sim.py` | 50% | Two paths merged, never unified | Single configurable prompt |
| XP & Leveling | `player.py` | 70% | Incoming-only is simpler; fixed scope | Retroactive scaling, formula |
| Hint System | `features.py`, `mission_engine.py` | 70% | Consistent costs; no per-mission need | Per-mission override, cooldown |
| Achievements | `features.py`, `mission_engine.py` | 70% | Small set; no CI to catch dead ones | Achievement engine, decorators |
| Gear System | `player.py`, `mission_engine.py` | 60% | Narrative-only by design; no equip complexity | Equip system, active abilities |
| Faction System | `features.py`, `player.py`, `mission_engine.py` | 30% | Deprioritized; `FactionStatus` dead code | Faction-locked content, wars |
| Input Handling | `display.py` | 40% | Pure stdlib; turn-based game | Readline, terminal control lib |
| Input Validation | `display.py`, `mission_engine.py` | 50% | Simple if/elif is readable; small menus | Schema validation, fuzzy match |
| Speaker Distribution | `mission_engine.py`, `player.py` | 50% | Content policy, not game mechanic | Runtime assertion, CI check |
| Story Transitions | `mission_engine.py` | 60% | Trusted content authors; graceful skip | Fixed-length tuple type |
| Content Audit | `CLAUDE.md` | 30% | Content frozen; no CI | Runtime validator, CI pipeline |
| Three-Layer Arch | `missions/`, `engine/`, `main.py` | 60% | Small project; direct imports readable | Protocols, DI |
| Global Singleton | `main.py` | 50% | No concurrency; simpler than DI | Pass state explicitly |
| Circular Imports | `mission_engine.py`, `player.py`, `features.py` | 60% | Quick fix during development | Clean module boundaries |
| Timed Exam | `main.py` | 70% | `_run_quiz()` tightly coupled | Refactored quiz runner |
| Review Mode | `main.py` | 60% | True spaced repetition is complex | Full spaced repetition algorithm |
