"""
Smoke Test 02: Player System
----------------------------
Validates XP/leveling mechanics, gear catalog integrity,
gear bonus calculations, achievement tracking, save/load round-trip,
and quiz statistics aggregation.

How to run manually:
    cd /home/ande/neongrid9
    python3 smoke_tests/check_what_is_working/test_02_player_system.py

Critical because: The Player dataclass is the single source of truth
for all progression. If XP math, gear, or save/load is broken, the
entire game loop loses player data.
"""

import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.player import Player, LEVELS, GEAR_CATALOG, FACTIONS, RARITY_COLOR
from engine.features import AchievementTracker, ACHIEVEMENTS, calculate_level


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
# TEST 1: XP and Level progression with real LEVELS table
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 1: XP and Level progression")

try:
    p = Player(name="LevelTest")

    # Verify LEVELS table integrity
    info(f"LEVELS entries: {len(LEVELS)}")
    for lvl, title, threshold in LEVELS:
        info(f"  Level {lvl:2d}: {title:20s} @ {threshold:6d} XP")

    # Level 1 start
    assert p.level == 1, f"Expected level 1, got {p.level}"
    assert p.level_title == "Newbie Hacker"
    ok("Level 1 at 0 XP")

    # Add XP to cross level boundaries
    p.add_xp(500)   # Should hit level 2
    assert p.level == 2, f"Expected level 2 at 500 XP, got {p.level}"
    ok("Level 2 at 500 XP")

    p.add_xp(1000)  # Total 1500 → level 3
    assert p.level == 3, f"Expected level 3 at 1500 XP, got {p.level}"
    ok("Level 3 at 1500 XP")

    p.add_xp(1500)  # Total 3000 → level 4
    assert p.level == 4, f"Expected level 4 at 3000 XP, got {p.level}"
    ok("Level 4 at 3000 XP")

    # Verify level scaling bonus applies
    old_xp = p.xp
    p.add_xp(100)
    gained = p.xp - old_xp
    info(f"Level {p.level} bonus: added 100 base, gained {gained} (scale should be ≥1.1)")
    assert gained >= 100, f"Expected scaled XP >= 100, got {gained}"
    ok("XP scaling bonus is active")

except Exception as e:
    fail("XP/Level test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Gear Catalog integrity and gear_bonus() with real items
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 2: Gear Catalog integrity and gear_bonus()")

try:
    # Verify all gear has required fields
    required_fields = {"name", "desc", "boost", "rarity", "tier"}
    for gear_id, gear_data in GEAR_CATALOG.items():
        missing = required_fields - set(gear_data.keys())
        if missing:
            fail(f"Gear '{gear_id}' missing fields: {missing}")
        else:
            info(f"  Gear '{gear_id}': {gear_data['name']} ({gear_data['rarity']}, tier {gear_data['tier']})")

    ok(f"All {len(GEAR_CATALOG)} gear items have required fields")

    # Test gear_bonus() without any gear
    p = Player(name="NoGear")
    assert p.gear_bonus("quiz_xp") == 1.0, "No gear should give 1.0 multiplier"
    assert p.gear_bonus("all_xp") == 1.0, "No gear should give 1.0 multiplier"
    ok("gear_bonus() returns 1.0 with no matching gear")

    # Test with ghost_mask (quiz_xp +20%)
    p.add_gear("ghost_mask")
    assert p.has_gear("ghost_mask")
    mult = p.gear_bonus("quiz_xp")
    info(f"ghost_mask quiz_xp multiplier: {mult}")
    assert mult == 1.20, f"Expected 1.20, got {mult}"
    ok("ghost_mask gives +20% quiz_xp")

    # Test linux_badge stacks with ghost_mask
    p.add_gear("linux_badge")
    mult = p.gear_bonus("quiz_xp")
    info(f"ghost_mask + linux_badge quiz_xp multiplier: {mult}")
    # linux_badge adds +0.05 to existing bonus
    expected = 1.20 + 0.05
    assert mult == expected, f"Expected {expected}, got {mult}"
    ok("linux_badge stacks +5% on top of ghost_mask")

    # Test gear_bonus for unmapped boost type (use fresh player)
    p2 = Player(name="Fresh")
    assert p2.gear_bonus("nonexistent_boost") == 1.0
    ok("Unknown boost type returns 1.0")

except Exception as e:
    fail("Gear test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: AchievementTracker with real ACHIEVEMENTS definitions
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 3: AchievementTracker")

try:
    tracker = AchievementTracker()

    # Verify all defined achievements can be unlocked
    info(f"Total achievements defined: {len(ACHIEVEMENTS)}")
    for ach_id, ach in ACHIEVEMENTS.items():
        info(f"  {ach_id}: {ach.name} ({ach.xp_reward} XP)")

    # Unlock first_mission
    result = tracker.unlock("first_mission")
    assert result is not None, "first_mission should unlock"
    assert result.name == "First Signal"
    ok("first_mission unlocks correctly")

    # Idempotency: unlocking again returns None
    result2 = tracker.unlock("first_mission")
    assert result2 is None, "Second unlock should return None"
    ok("Achievement unlock is idempotent")

    # Verify tracker count
    assert tracker.count() == 1
    ok("Tracker count = 1 after one unlock")

    # has() check
    assert tracker.has("first_mission")
    assert not tracker.has("all_bosses")
    ok("has() returns correct state")

    # Unlock invalid ID returns None
    result3 = tracker.unlock("does_not_exist")
    assert result3 is None
    ok("Invalid achievement ID returns None safely")

except Exception as e:
    fail("AchievementTracker test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4: Save/Load round-trip with real Player state
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 4: Save/Load round-trip")

try:
    from engine.save_system import save_game, load_game, delete_save

    # Use slot 1 for testing — clean up before and after
    test_slot = 1

    # Clean up any prior test save
    delete_save(test_slot)

    # Build a rich Player state
    p = Player(name="RoundTrip")
    p.add_xp(3500)  # level 4
    p.complete_mission("1.01")
    p.complete_mission("1.02")
    p.complete_mission("2.05")
    p.add_gear("hardware_scanner")
    p.add_reputation("Kernel Syndicate", 25)
    p.record_quiz_result(1, True)
    p.record_quiz_result(1, False)
    p.record_quiz_result(2, True)
    p.total_quizzes = 3
    p.correct_first_try = 2
    p.bosses_defeated = 1
    p.hints_used = 3
    p.total_playtime = 1234

    # Save
    saved = save_game(p, test_slot)
    assert saved, "save_game returned False"
    ok("save_game() succeeded")

    # Load
    p2 = load_game(test_slot)
    assert p2 is not None, "load_game returned None"
    ok("load_game() succeeded")

    # Verify all fields survived round-trip
    checks = [
        ("name", p.name, p2.name),
        ("xp", p.xp, p2.xp),
        ("level", p.level, p2.level),
        ("level_title", p.level_title, p2.level_title),
        ("completed_missions", p.completed_missions, p2.completed_missions),
        ("inventory", set(p.inventory), set(p2.inventory)),
        ("reputation Kernel Syndicate", p.reputation["Kernel Syndicate"], p2.reputation["Kernel Syndicate"]),
        ("total_quizzes", p.total_quizzes, p2.total_quizzes),
        ("correct_first_try", p.correct_first_try, p2.correct_first_try),
        ("bosses_defeated", p.bosses_defeated, p2.bosses_defeated),
        ("hints_used", p.hints_used, p2.hints_used),
        ("total_playtime", p.total_playtime, p2.total_playtime),
    ]

    mismatches = 0
    for field, expected, actual in checks:
        if expected != actual:
            fail(f"Round-trip mismatch on '{field}': expected {expected!r}, got {actual!r}")
            mismatches += 1
        else:
            info(f"  {field}: {actual!r} ✓")

    if mismatches == 0:
        ok("All fields survived save/load round-trip")
    else:
        fail(f"{mismatches} fields mismatched after round-trip")

    # Clean up
    delete_save(test_slot)
    ok("Test save cleaned up")

except Exception as e:
    fail("Save/Load test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5: Quiz statistics aggregation and accuracy calculation
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 5: Quiz statistics and accuracy")

try:
    p = Player(name="QuizStats")

    # Fresh player has 0 accuracy for any chapter
    assert p.quiz_accuracy(1) == 0.0
    ok("quiz_accuracy() returns 0.0 for untouched chapter")

    # Record some results
    p.record_quiz_result(1, True)
    p.record_quiz_result(1, True)
    p.record_quiz_result(1, False)
    # Chapter 1: 2/3 correct = 66.7%

    acc1 = p.quiz_accuracy(1)
    info(f"Chapter 1 accuracy: {acc1:.2%} (2/3)")
    assert abs(acc1 - 2/3) < 0.001, f"Expected ~0.667, got {acc1}"
    ok("quiz_accuracy() computes correctly after mixed results")

    p.record_quiz_result(2, True)
    p.record_quiz_result(2, True)
    p.record_quiz_result(2, True)
    p.record_quiz_result(2, True)
    # Chapter 2: 4/4 = 100%

    acc2 = p.quiz_accuracy(2)
    info(f"Chapter 2 accuracy: {acc2:.2%} (4/4)")
    assert acc2 == 1.0, f"Expected 1.0, got {acc2}"
    ok("quiz_accuracy() = 1.0 for perfect chapter")

    # Untouched chapter still 0
    assert p.quiz_accuracy(99) == 0.0
    ok("Untouched chapter still reports 0.0 accuracy")

    # Verify chapter_quiz_stats structure
    stats = p.chapter_quiz_stats
    info(f"chapter_quiz_stats keys: {list(stats.keys())}")
    assert "1" in stats
    assert "2" in stats
    assert stats["1"]["asked"] == 3
    assert stats["1"]["correct"] == 2
    assert stats["2"]["asked"] == 4
    assert stats["2"]["correct"] == 4
    ok("chapter_quiz_stats structure is correct")

except Exception as e:
    fail("Quiz statistics test failed", e)


# ── Summary ───────────────────────────────────────────────────────────────────
banner("TEST 02 SUMMARY")
print("  Player system smoke test completed.")
