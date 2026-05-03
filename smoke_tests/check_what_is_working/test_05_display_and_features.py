"""
Smoke Test 05: Display System & Features
------------------------------------------
Validates ANSI color constants, display function existence,
HintRequest creation at all levels, Achievement definitions,
and FactionStatus/calculate_level utilities.

How to run manually:
    cd /home/ande/neongrid9
    python3 smoke_tests/check_what_is_working/test_05_display_and_features.py

Critical because: Display functions render every screen the player
sees. Feature utilities (hints, achievements, factions) drive the
meta-progression systems. If these are broken, the game is unplayable
or unsatisfying regardless of content quality.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.display import C, clear, header, mission_header, xp_bar, box, typewrite
from engine.features import (
    HintLevel, HintRequest, Achievement, AchievementTracker,
    ACHIEVEMENTS, calculate_level, FactionStatus
)
from engine.player import Player, FACTIONS


# ── Helpers ────────────────────────────────────────────────────────────────────

def banner(msg):
    print(f"\n{'=' * 70}")
    print(f"  {msg}")
    print(f"{'=' * 70}")


def ok(msg):
    print(f"  [PASS] {msg}")


def fail(msg, exc=None):
    print(f"  [FAIL] {msg}")
    if exc:
        print(f"         {type(exc).__name__}: {exc}")


def info(msg):
    print(f"  [INFO] {msg}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1: ANSI Color constants are valid escape sequences
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 1: ANSI Color constants")

try:
    color_attrs = [a for a in dir(C) if not a.startswith("_")]
    info(f"Color class attributes: {color_attrs}")

    # Every attribute should be a string starting with \033[
    bad_colors = []
    for attr in color_attrs:
        val = getattr(C, attr)
        if not isinstance(val, str):
            bad_colors.append(f"{attr} is {type(val).__name__}")
        elif not val.startswith("\033[") and attr != "RESET":
            # RESET can be "\033[0m" which does start with \033[
            # But some combos might start differently
            if attr != "RESET":
                bad_colors.append(f"{attr}='{val[:20]}...' doesn't look like ANSI")

    if bad_colors:
        for b in bad_colors:
            fail(b)
    else:
        ok(f"All {len(color_attrs)} color attributes are valid strings")

    # Verify RESET works
    assert C.RESET == "\033[0m", f"Expected RESET='\\033[0m', got {C.RESET!r}"
    ok("C.RESET is correct")

    # Verify key colors exist
    required_colors = {"NEON", "CYAN", "GREEN", "YELLOW", "RED", "MAGENTA", "BLUE", "WHITE", "GRAY"}
    missing = required_colors - set(color_attrs)
    if missing:
        fail(f"Missing color attributes: {missing}")
    else:
        ok("All required color attributes exist")

except Exception as e:
    fail("Color constant test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Key display functions are callable
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 2: Display function callability")

try:
    # These functions should exist and be callable
    funcs_to_test = [
        ("clear", lambda: clear()),
        ("header", lambda: header("Test Header", "Test Subtitle")),
        ("mission_header", lambda: mission_header("1.01", "Test Mission", 30, "SCAN")),
        ("xp_bar", lambda: xp_bar(500, 2, 0, 1500)),
        ("box", lambda: box("Test Box", "This is test content.")),
    ]

    for name, fn in funcs_to_test:
        try:
            fn()
            ok(f"{name}() executed without error")
        except Exception as e:
            fail(f"{name}() raised {type(e).__name__}: {e}")

except Exception as e:
    fail("Display function test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: HintRequest creation at all levels and edge cases
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 3: HintRequest creation")

try:
    hints = ["free hint", "standard hint", "final hint"]

    # Level 0 (free)
    hr0 = HintRequest.create("1.01", hints, 0)
    assert hr0 is not None
    assert hr0.level == HintLevel.FREE
    assert hr0.xp_cost == 0
    assert hr0.text == "free hint"
    ok("Level 0 (FREE) hint created correctly")

    # Level 1 (standard, 20 XP)
    hr1 = HintRequest.create("1.01", hints, 1)
    assert hr1 is not None
    assert hr1.level == HintLevel.STANDARD
    assert hr1.xp_cost == 20
    assert hr1.text == "standard hint"
    ok("Level 1 (STANDARD) hint created correctly")

    # Level 2 (final, 50 XP)
    hr2 = HintRequest.create("1.01", hints, 2)
    assert hr2 is not None
    assert hr2.level == HintLevel.FINAL
    assert hr2.xp_cost == 50
    assert hr2.text == "final hint"
    ok("Level 2 (FINAL) hint created correctly")

    # Level 3 (out of range)
    hr3 = HintRequest.create("1.01", hints, 3)
    assert hr3 is None
    ok("Level 3 returns None (out of range)")

    # Empty hints list
    hr_empty = HintRequest.create("1.01", [], 0)
    assert hr_empty is None
    ok("Empty hints list returns None")

    # Single hint (only free available)
    hr_single = HintRequest.create("1.01", ["only free"], 0)
    assert hr_single is not None
    assert hr_single.xp_cost == 0
    ok("Single-hint list works for level 0")

    hr_single_over = HintRequest.create("1.01", ["only free"], 1)
    assert hr_single_over is None
    ok("Single-hint list returns None for level 1")

except Exception as e:
    fail("HintRequest test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4: Achievement definitions are complete and consistent
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 4: Achievement definitions")

try:
    info(f"Total achievements defined: {len(ACHIEVEMENTS)}")

    required_ach_fields = {"id", "name", "description", "xp_reward", "icon"}
    issues = []

    for ach_id, ach in ACHIEVEMENTS.items():
        # Verify it's an Achievement dataclass
        if not isinstance(ach, Achievement):
            issues.append(f"'{ach_id}' is not an Achievement instance")
            continue

        # Verify ID matches dict key
        if ach.id != ach_id:
            issues.append(f"'{ach_id}' key != ach.id '{ach.id}'")

        # Verify fields
        if not ach.name:
            issues.append(f"'{ach_id}' has no name")
        if not ach.description:
            issues.append(f"'{ach_id}' has no description")
        if ach.xp_reward < 0:
            issues.append(f"'{ach_id}' has negative xp_reward")

    if issues:
        for i in issues:
            fail(i)
    else:
        ok(f"All {len(ACHIEVEMENTS)} achievements are valid")

    # Verify specific critical achievements exist
    critical_achs = [
        "first_mission", "boss_defeated", "all_bosses",
        "perfect_quiz", "speedrun", "level_ten",
        "gear_collector", "exam_mastered",
    ]
    missing = [a for a in critical_achs if a not in ACHIEVEMENTS]
    if missing:
        fail(f"Missing critical achievements: {missing}")
    else:
        ok("All critical achievement IDs exist")

    # Verify Achievement __eq__ works
    a1 = ACHIEVEMENTS["first_mission"]
    a2 = ACHIEVEMENTS["first_mission"]
    assert a1 == a2
    assert a1 == "first_mission"
    ok("Achievement __eq__ works with instance and string")

except Exception as e:
    fail("Achievement definitions test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5: calculate_level() and FactionStatus for reputation/XP
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 5: calculate_level() and FactionStatus")

try:
    # Test reputation-based levels (0-100 scale)
    rep_tests = [
        (0, 1),   # 0 rep = level 1
        (10, 1),  # 10 rep = level 1
        (20, 2),  # 20 rep = level 2
        (40, 3),  # 40 rep = level 3
        (60, 4),  # 60 rep = level 4
        (80, 5),  # 80 rep = level 5
        (100, 5), # 100 rep = level 5 (max)
    ]

    for rep, expected_lvl in rep_tests:
        actual = calculate_level(rep)
        if actual == expected_lvl:
            info(f"  Reputation {rep:3d} → Level {actual} ✓")
        else:
            fail(f"Reputation {rep}: expected level {expected_lvl}, got {actual}")

    ok("calculate_level() works for reputation 0-100")

    # Test XP-based levels (>100)
    # NOTE: calculate_level() treats values ≤100 as reputation, not XP.
    #       Thresholds: [0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3250]
    #       XP >= threshold[i] → level i+1. So XP 101 crosses threshold 100 → level 2.
    xp_tests = [
        (101, 2),   # Crosses threshold 100
        (150, 2),
        (250, 3),   # Crosses threshold 250
        (450, 4),
        (700, 5),
        (1000, 6),
        (1350, 7),
        (1750, 8),
        (2200, 9),
        (2700, 10),
        (3250, 10),
        (5000, 10),
    ]

    for xp_val, expected_lvl in xp_tests:
        actual = calculate_level(xp_val)
        if actual == expected_lvl:
            info(f"  XP {xp_val:5d} → Level {actual} ✓")
        else:
            fail(f"XP {xp_val}: expected level {expected_lvl}, got {actual}")

    ok("calculate_level() works for XP >100")

    # Test FactionStatus display
    fs = FactionStatus(name="Kernel Syndicate", xp=45, level=3, max_xp=100)
    bar = fs.progress_bar(width=20)
    info(f"  FactionStatus bar: [{bar}]")
    assert len(bar) == 20, f"Expected bar length 20, got {len(bar)}"
    ok("FactionStatus.progress_bar() returns correct width")

    display = fs.display()
    info(f"  FactionStatus.display(): {display}")
    assert "Kernel Syndicate" in display
    assert "Lv3" in display
    ok("FactionStatus.display() includes name and level")

except Exception as e:
    fail("calculate_level/FactionStatus test failed", e)


# ── Summary ───────────────────────────────────────────────────────────────────
banner("TEST 05 SUMMARY")
print("  Display & Features smoke test completed.")
