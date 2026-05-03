# Code Archaeology: Cleanup Inventory

**Project:** NeonGrid-9  
**Date:** 2026-05-02  
**Auditor:** Claude Code  
**Scope:** engine/, main.py, missions/  
**Methodology:** Static analysis — grep for definitions vs. call sites, import-vs-usage, dynamic loading scan.

---

## Safety Warning

**Never delete immediately.** Code that looks unused might be:

- Loaded dynamically via `getattr`, `__import__`, `importlib`, `eval`, or `exec`
- Referenced in configuration files or external build scripts
- Kept for compliance, audit trails, or future re-enabling
- Used by test harnesses, CI pipelines, or IDE tooling

**This inventory marks every candidate with a risk rating.** Review each item before removal.

---

## Executive Summary

| Category | Count | Risk Level |
|----------|-------|------------|
| Dead functions (never called) | 4 | Low–Medium |
| Unused imports | 6 | Low |
| Dead Player dataclass fields (never written) | 4 | Medium |
| Empty package markers | 2 | **Keep** |
| Dynamic loading patterns | 0 found | — |
| Duplicate implementations | 0 found | — |
| Commented-out code blocks | 0 found | — |

**Overall assessment:** The codebase is relatively clean. The highest-value removals are unused imports (reduces noise) and dead display functions (reduces maintenance surface). The dead Player fields are architectural debt, not removable without gameplay logic changes.

---

## 1. Dead Functions (Defined but Never Called)

### 1.1 `slow_print()` — `engine/display.py:50`

```python
def slow_print(text: str, delay: float = 0.008):
    """Langsamer Print mit sehr kurzer Verzögerung."""
```

**Why it appears unused:**
- Zero call sites across `engine/`, `main.py`, and all `missions/`.
- It *is* imported by `main.py:29` and `engine/terminal_sim.py:9`, but never invoked in either file.
- `typewrite()` (line 41) provides the same functionality and is actively used.

**Risk of removal:** **Low.** No dynamic loading detected. `typewrite` is the canonical slow-print utility.

**Recommended action:** Remove function definition and both unused imports.

---

### 1.2 `show_progress()` — `engine/display.py:253`

```python
def show_progress(chapter: int, total_chapters: int, missions_done: int, total_missions: int):
    """Fortschrittsbalken für Kapitel."""
```

**Why it appears unused:**
- Zero call sites in the entire codebase.
- No references in strings, comments, or configuration.

**Risk of removal:** **Low.** Self-contained rendering function with no side effects on global state.

**Recommended action:** Remove. If a chapter-progress HUD is desired in the future, re-implement from `xp_bar()` as a shared helper.

---

### 1.3 `box()` — `engine/display.py:57`

```python
def box(title: str, content: str, color: str = C.CYAN, width: int = 66):
    """Zeichnet eine Box um Inhalt."""
```

**Why it appears unused:**
- Zero call sites in production code.
- Only called by `smoke_tests/check_what_is_working/test_05_display_and_features.py:108`.
- Imported by `main.py:29` but never used there.

**Risk of removal:** **Medium.** The smoke test references it. Removing the function would break the smoke test unless the test is updated to skip `box()` or remove the `box()` assertion.

**Recommended action:** Either (a) keep and adopt in production UI, or (b) remove function + update smoke test + remove import in `main.py`.

---

### 1.4 `normalize_cmd()` — `engine/terminal_sim.py:4350`

```python
def normalize_cmd(cmd: str) -> str:
    """Normalisiert einen Befehl: lowercase, strip, collapse whitespace."""
```

**Why it appears unused:**
- Zero call sites in the entire codebase.
- The terminal simulator does its own normalization inline (case-insensitive substring matching in `get_output`).

**Risk of removal:** **Low.** Pure function with no external dependencies. If the terminal simulator is ever refactored to use a centralized normalization pipeline, this would be the right function — but currently it is orphaned.

**Recommended action:** Remove. Re-introduce if the terminal simulator's matching logic is centralized.

---

## 2. Unused Imports

### 2.1 `main.py` — Multiple unused display imports

| Import | Line | Used? | Note |
|--------|------|-------|------|
| `LEVELS` | 31 | No | Referenced only in `engine/player.py` and `engine/mission_engine.py` |
| `show_story` | 27 | No | A local `show_story_prologue()` exists but does *not* call `show_story()` |
| `show_info` | 27 | No | No call site in `main.py` |
| `header` | 27 | No | Only `chapter_header` is used in `main.py` |
| `slow_print` | 29 | No | See 1.1 |
| `box` | 29 | No | See 1.3 |

**Risk of removal:** **Low.** Removing unused imports reduces import-time overhead slightly and declutters the namespace. No dynamic loading.

**Recommended action:** Remove all six unused imports from `main.py`. Ensure no future merge re-introduces them.

---

### 2.2 `engine/mission_engine.py` — `HintLevel`

```python
from engine.features import HintRequest, HintLevel
```

**Why it appears unused:**
- `HintLevel` is imported at line 18 but never referenced in the file.
- Only `HintRequest` is used (e.g., `HintRequest.create(...)`).

**Risk of removal:** **Low.** Removing `HintLevel` from this import does not affect other files that import it directly from `engine.features`.

**Recommended action:** Remove `HintLevel` from this import line.

---

### 2.3 `engine/terminal_sim.py` — `slow_print`

```python
from engine.display import C, show_code, slow_print
```

**Why it appears unused:**
- `slow_print` is imported at line 9 but never called in the 4,457-line file.

**Risk of removal:** **Low.** No side effects.

**Recommended action:** Remove `slow_print` from this import line.

---

## 3. Dead Player Dataclass Fields (Tracked but Never Updated)

These fields exist on `Player`, are read by `stats_summary()` and round-tripped through save/load, but **no gameplay code ever writes to them**. They are architectural placeholders.

### 3.1 `total_playtime`

**Declaration:** `engine/player.py` — `total_playtime: int = 0`

**Read sites:**
- `stats_summary()` line 275–276 (formats hours/minutes)
- `to_dict()` line 346
- `from_dict()` line 373

**Write sites:** **None.** No `player.total_playtime += …` or similar anywhere in `engine/` or `main.py`.

**Risk of removal:** **Medium.** Removing the field would break `to_dict()` / `from_dict()` round-trips for existing save files that contain this key. Safe to remove only if save migration logic is added, or if the field is actually wired up (e.g., timer in `MissionRunner`).

**Recommended action:** Do **not** remove. Instead, wire it up in `MissionRunner.run()` or `game_hub()` with `time.time()` delta tracking. Documented in `gap_analysis.md` Section 4.3.

---

### 3.2 `chapter_completion_time`

**Declaration:** `engine/player.py` — `chapter_completion_time: Dict[int, float] = field(default_factory=dict)`

**Read sites:**
- `stats_summary()` line 294
- `to_dict()` line 344
- `from_dict()` line 371

**Write sites:** **None.** No code sets `player.chapter_completion_time[ch] = elapsed`.

**Risk of removal:** **Medium.** Same save-format compatibility concern as `total_playtime`.

**Recommended action:** Do **not** remove. Wire it up at chapter-complete boundary in `main.py` (around line 598, `_show_chapter_complete`).

---

### 3.3 `speaker_stats`

**Declaration:** `engine/player.py` — `speaker_stats: Dict[str, int] = field(default_factory=dict)`

**Read sites:**
- `stats_summary()` line 308–311 (sorts and displays top speakers)
- `to_dict()` line 347
- `from_dict()` line 374

**Write sites:** **None.** No code increments speaker counters when `show_story(speaker, text)` is called.

**Risk of removal:** **Medium.** Save compatibility.

**Recommended action:** Do **not** remove. Wire it up in `show_story()` or `MissionRunner.run()` by incrementing `player.speaker_stats[speaker] += 1`.

---

### 3.4 `hint_stats`

**Declaration:** `engine/player.py` — `hint_stats: Dict[str, int] = field(default_factory=dict)`

**Read sites:**
- `to_dict()` line 348
- `from_dict()` line 375

**Write sites:** **None.** Not even read in `stats_summary()`.

**Risk of removal:** **Medium.** Save compatibility. Also, this field is the most obviously dead because it has no UI consumption at all.

**Recommended action:** Do **not** remove yet. Either wire it up in the hint-request flow or remove as part of a broader Player dataclass cleanup (Phase 1 of `gap_closure_plan.md`).

---

## 4. Package Markers (Keep)

### 4.1 `engine/__init__.py`

**Status:** Empty file.  
**Action:** **Keep.** Required for `engine/` to be recognized as a Python package. Removing it would break all absolute imports (`from engine.display import …`).

### 4.2 `missions/__init__.py`

**Status:** Empty file.  
**Action:** **Keep.** Same rationale as above. `main.py` imports `from missions.ch01_hardware import CHAPTER_1_MISSIONS`, which relies on `missions/` being a package.

---

## 5. Dynamic Loading Scan

**Result:** **No dynamic loading patterns found.**

The following patterns were searched for and returned zero results:

| Pattern | Files Scanned | Hits |
|---------|---------------|------|
| `getattr(` | `engine/`, `main.py` | 0 |
| `__import__` | `engine/`, `main.py` | 0 |
| `eval(` | `engine/`, `main.py` | 0 |
| `exec(` | `engine/`, `main.py` | 0 |
| `importlib` | `engine/`, `main.py` | 0 |

**Implication:** Every function definition can be safely assumed to be either directly called or genuinely dead. There are no hidden dynamic call sites.

---

## 6. Duplicate Implementations

**Result:** **None found.**

Searched for:
- Multiple definitions of `calculate_level` → only `engine/features.py:249`
- Multiple definitions of `gear_bonus` → only `engine/player.py:237`
- Multiple definitions of `add_xp` → only `engine/player.py:191`
- Multiple save/load implementations → only `engine/save_system.py`

All core logic is centralized in exactly one location.

---

## 7. Commented-Out Code Blocks

**Result:** **None found.**

The codebase contains no `# def …`, `# class …`, or `# import …` patterns that indicate disabled code. All `#` lines in production code are either:

- Decorative section headers (`# ── Vordefinierte Achievements ────────────────────────────────────────────────`)
- Inline comments explaining terminal simulator output (`# from /etc/grub.d and settings from /etc/default/grub`)

No commented-out logic blocks to purge.

---

## 8. Orphaned / Unused Files

**Result:** **None found.**

All `.py` files in the project are referenced by at least one import chain:

| File | Referenced By |
|------|---------------|
| `main.py` | Entry point (executed directly) |
| `engine/__init__.py` | Package marker (implicitly loaded) |
| `engine/display.py` | Imported by `main.py`, `engine/terminal_sim.py`, smoke tests |
| `engine/player.py` | Imported by `main.py`, `engine/mission_engine.py`, smoke tests |
| `engine/features.py` | Imported by `main.py`, `engine/mission_engine.py`, smoke tests |
| `engine/terminal_sim.py` | Imported by `main.py`, smoke tests |
| `engine/save_system.py` | Imported by `main.py` |
| `engine/mission_engine.py` | Imported by `main.py`, smoke tests |
| `missions/__init__.py` | Package marker |
| `missions/ch01_hardware.py` … `ch22_final_exam.py` | Imported by `main.py` |

All documentation files (`README.md`, `CLAUDE.md`, `GAMEPLAY_GUIDE.md`, `LINUX_TOPICS.md`, `TIPS_TRICKS.md`) are referenced in `README.md` hyperlinks or serve as project specification. None are orphaned.

The `.claude/settings.local.json` file is an active permissions configuration for Claude Code sessions and should not be removed.

---

## 9. Recommended Cleanup Order

If you choose to proceed with removals, follow this sequence to minimize merge conflicts and test breakage:

1. **Unused imports** (2.1, 2.2, 2.3) — zero functional impact, immediate readability gain.
2. **`normalize_cmd()`** (1.4) — isolated, no dependencies.
3. **`show_progress()`** (1.2) — isolated, no dependencies.
4. **`slow_print()`** (1.1) — remove imports first, then function. Update smoke test if it tests `slow_print`.
5. **`box()`** (1.3) — last, because smoke test `test_05` calls it. Decide whether to keep `box()` as a production feature or remove it and update the test.
6. **Dead Player fields** (3.1–3.4) — do **not** remove. Wire them up or leave as documented architectural debt.

---

## 10. Cross-References

| Issue | Documented In | Planned Fix In |
|-------|---------------|----------------|
| 4 dead Player fields | `gap_analysis.md` Section 4.3 | `gap_closure_plan.md` Phase 1 |
| `box()` unused | This file Section 1.3 | `gap_closure_plan.md` Phase 1 (adopt or remove) |
| `slow_print()` / `show_progress()` unused | This file Section 1.1, 1.2 | `gap_closure_plan.md` Phase 1 |
| Unused imports | This file Section 2 | `gap_closure_plan.md` Phase 1 |
| Forced hint anti-pattern | `gap_analysis.md` Section 3.4 | `gap_closure_plan.md` Phase 1 |
| Gear bonus never applied | `gap_analysis.md` Section 3.1 | `gap_closure_plan.md` Phase 1 |
| 8 unimplemented achievements | `gap_analysis.md` Section 3.3 | `gap_closure_plan.md` Phase 1 |
| 727 quiz `correct` as `int` | `gap_analysis.md` Section 2.1 | `gap_closure_plan.md` Phase 1 |
| 15 BOSS missions missing metadata | `gap_analysis.md` Section 2.2 | `gap_closure_plan.md` Phase 1 |

---

*End of Cleanup Inventory*
