# Hints Population Guide

## Current Status

**Missions with Complete Hints:** 5/501 (1%)
- ch01.02 (BIOS Whisper)
- ch02.01 (Power On)
- ch02.02 (MBR Anatomy)
- ch01.BOSS (Hardware Overlord)

**Remaining:** 496 missions need 3-tier hints

## Hint System Overview

Each mission can have a `hints` field with 3 tiers:

```python
hints = [
    "FREE (0 XP): Conceptual direction / initial guidance",
    "STANDARD (20 XP): More specific hints / command structure",
    "FINAL (50 XP): Complete answer / full command",
],
```

## Population Approaches

### Option 1: Manual Population (Most Reliable)

**Time:** ~2-3 minutes per 10 missions = ~500 missions ÷ 10 = **50 hours**

**Approach:**
1. Edit mission file
2. Find `expected_commands = [...]` line
3. Add `hints = [...]` field right after

**Example:**
```python
expected_commands=["lspci"],
hints=[
    "Ein Auflistungsbefehl wie 'lspci' wird benötigt.",
    "Versuche: lspci",
    "Der vollständige Befehl: lspci",
],
hint_text="..."  # old field, still present
```

**Pros:** 
- Guarantees correct syntax
- Allows customized, higher-quality hints
- Can prioritize high-value missions

**Cons:**
- Very time-consuming
- Repetitive for similar mission types

### Option 2: Automated Generation (Fast but Needs Verification)

**Time:** ~30 seconds = **instant**

**Available Scripts:**

#### `patch_hints_ast.py` - Fastest
```bash
python3 scripts/patch_hints_ast.py
```
**Pros:** Fastest, complete coverage
**Cons:** Reformats entire Python code (makes files ugly but functional)
**Status:** Tested, working, but output not pretty

#### `careful_hint_inject.py` - Most Careful
```bash
python3 scripts/careful_hint_inject.py
```
**Pros:** Tries to preserve formatting
**Cons:** Had syntax issues in testing (complex Python structures)
**Status:** Needs debugging

#### `regenerate_missions_with_hints.py` - Python-based
```bash
python3 scripts/regenerate_missions_with_hints.py
```
**Pros:** Loads missions as Python objects
**Cons:** Still need to export back to files
**Status:** Partially implemented

### Option 3: Hybrid Approach (Recommended)

1. **Populate high-value missions manually:**
   - All boss missions (22 × 1 = 22 missions)
   - First 2 chapters (ch01: 31, ch02: 20 = 51 missions)
   - Total: ~73 missions (~3-4 hours)

2. **Auto-generate remaining:**
   - Use `patch_hints_ast.py` for remaining 428 missions
   - Acceptable since format is less critical than boss/early missions

3. **Spot-check output:**
   - Verify a few chapters load correctly
   - Run test suite: `python3 scripts/test_gameflow.py`

**Total Time:** 3-4 hours + 30 minutes verification = **~4.5 hours**

## Hint Generation Pattern

The hint generator creates 3 tiers based on `expected_commands` and `task_description`:

```python
# Example: ls /sys/firmware/efi/
hints = [
    "Das Verzeichnis oder die Datei befinden sich unter '/sys/firmware/efi/'. Der Befehl beginnt mit 'ls'.",
    "Versuche: ls /sys/firmware/efi/",
    "Der vollständige Befehl: ls /sys/firmware/efi/",
],

# Example: lspci
hints = [
    "Ein Auflistungsbefehl wie 'lspci' wird benötigt.",
    "Versuche: lspci",
    "Der vollständige Befehl: lspci",
],
```

## Quality Notes

**Good Hints Should:**
- Tier 1 (Free): Give conceptual direction without revealing the answer
- Tier 2 (20 XP): Show command structure/syntax
- Tier 3 (50 XP): Provide complete working command

**Current Generator Heuristics:**
- Detects file paths → path-based hints
- Detects "zeige/liste/anzeigen" → listing command hints
- Generic fallback → command-name based hints

**Limitations:**
- Can't generate context-specific hints without understanding mission content
- All hints are generic/formulaic (acceptable but not optimal)
- Some specialized commands may need manual refinement

## Verification

After populating hints, run:

```bash
# Verify syntax
python3 -c "from missions.ch01_hardware import CHAPTER_1_MISSIONS; print('✓ Ch01 loads')"

# Run full test suite
python3 scripts/test_gameflow.py

# Quick spot check
python3 << 'EOF'
from missions.ch02_boot import CHAPTER_2_MISSIONS
for m in CHAPTER_2_MISSIONS[:3]:
    print(f"{m.mission_id}: {len(m.hints)} hints")
EOF
```

## Recommended Next Steps

1. **If pursuing automated solution:**
   ```bash
   python3 scripts/patch_hints_ast.py
   python3 scripts/test_gameflow.py
   ```
   Then accept the code reformatting as acceptable cost.

2. **If pursuing hybrid solution:**
   - Manually add hints to ch01-ch02 using Edit tool
   - Add hints to all boss missions (1.BOSS through 22.BOSS)
   - Run auto-generator on remaining chapters
   - Verify with test suite

3. **If accepting partial coverage:**
   - Leave ~5 demonstrated missions with manual hints
   - Document in README that hints are auto-generateable
   - Allow users to generate them as needed

## Cost-Benefit Analysis

| Approach | Time | Quality | Coverage |
|----------|------|---------|----------|
| Manual All | 50h | ⭐⭐⭐⭐⭐ | 100% |
| Auto All | 0.5h | ⭐⭐⭐ | 100% |
| Hybrid | 4.5h | ⭐⭐⭐⭐ | 100% |
| Partial (Demo) | 0.5h | ⭐⭐⭐⭐ | 1% |

## Files & References

- **Implemented:** `engine/features.py` - Hint system core
- **Integration:** `engine/mission_engine.py` - Hint menu in gameplay
- **Scripts:** `scripts/patch_hints_ast.py`, `scripts/careful_hint_inject.py`, etc.
- **Test:** `scripts/test_gameflow.py`
- **Example Hints:** `missions/ch01_hardware.py` (1.02, 1.BOSS), `missions/ch02_boot.py` (2.01-02)

## Conclusion

**The hint system is complete and fully functional.** The remaining work is purely data population, which can be done via:
- Automated generation (fast, acceptable quality)
- Manual refinement (time-consuming, higher quality)
- Hybrid approach (good balance)

No code changes needed—just data entry or auto-generation.
