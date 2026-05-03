"""
Smoke Test 01: Initialization & Core Imports
---------------------------------------------
Validates that the entire codebase can be imported without errors,
that core data structures instantiate correctly, and that the
project-level constants (mission counts, chapter counts) match spec.

How to run manually:
    cd /home/ande/neongrid9
    python3 smoke_tests/check_what_is_working/test_01_initialization.py

Critical because: If imports fail or basic counts are wrong,
nothing else in the game can function.
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


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
# TEST 1: Import all engine modules
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 1: Import all engine modules")

try:
    from engine.display import C, clear, header, mission_header, xp_bar
    from engine.player import Player, LEVELS, GEAR_CATALOG, FACTIONS, RARITY_COLOR
    from engine.mission_engine import Mission, QuizQuestion, MissionRunner
    from engine.terminal_sim import get_output, run_terminal, SIMULATED_OUTPUTS
    from engine.save_system import save_game, load_game, slot_info, delete_save
    from engine.features import HintLevel, HintRequest, Achievement, AchievementTracker, ACHIEVEMENTS, calculate_level
    ok("All engine modules imported successfully")
except Exception as e:
    fail("Engine module import failed", e)
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Import all 22 mission chapter modules
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 2: Import all 22 mission chapter modules")

mission_modules = [
    ("missions.ch01_hardware", "CHAPTER_1_MISSIONS"),
    ("missions.ch02_boot", "CHAPTER_2_MISSIONS"),
    ("missions.ch03_init", "CHAPTER_3_MISSIONS"),
    ("missions.ch04_partitions", "CHAPTER_4_MISSIONS"),
    ("missions.ch05_permissions", "CHAPTER_5_MISSIONS"),
    ("missions.ch06_shell", "CHAPTER_6_MISSIONS"),
    ("missions.ch07_processes", "CHAPTER_7_MISSIONS"),
    ("missions.ch08_regex_vi", "CHAPTER_8_MISSIONS"),
    ("missions.ch09_network", "CHAPTER_9_MISSIONS"),
    ("missions.ch10_users", "CHAPTER_10_MISSIONS"),
    ("missions.ch11_logging", "CHAPTER_11_MISSIONS"),
    ("missions.ch12_packages", "CHAPTER_12_MISSIONS"),
    ("missions.ch13_kernel", "CHAPTER_13_MISSIONS"),
    ("missions.ch14_scripting", "CHAPTER_14_MISSIONS"),
    ("missions.ch15_security", "CHAPTER_15_MISSIONS"),
    ("missions.ch16_locale", "CHAPTER_16_MISSIONS"),
    ("missions.ch17_shellenv", "CHAPTER_17_MISSIONS"),
    ("missions.ch18_storage", "CHAPTER_18_MISSIONS"),
    ("missions.ch19_ghost_processors", "CHAPTER_19_MISSIONS"),
    ("missions.ch20_firewall_dominion", "CHAPTER_20_MISSIONS"),
    ("missions.ch21_network_services", "CHAPTER_21_MISSIONS"),
    ("missions.ch22_exam", "CHAPTER_22_MISSIONS"),
]

import importlib

chapter_lists = {}
all_imported = True
for mod_name, attr_name in mission_modules:
    try:
        mod = importlib.import_module(mod_name)
        chapter_lists[attr_name] = getattr(mod, attr_name)
        ok(f"{mod_name}.{attr_name} — {len(chapter_lists[attr_name])} missions")
    except Exception as e:
        fail(f"{mod_name}.{attr_name}", e)
        all_imported = False

if all_imported:
    ok("All 22 chapter modules imported successfully")
else:
    fail("Some chapter modules failed to import")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: Verify total mission count matches spec (501)
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 3: Verify total mission count matches spec (501)")

total_missions = sum(len(mlist) for mlist in chapter_lists.values())
info(f"Total missions found: {total_missions}")

expected = 501
if total_missions == expected:
    ok(f"Mission count matches spec: {total_missions} == {expected}")
elif total_missions > 0:
    fail(f"Mission count MISMATCH: got {total_missions}, expected {expected}")
    # Non-fatal: content may have evolved
else:
    fail(f"No missions found at all")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4: Instantiate core data structures with real data
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 4: Instantiate core data structures with real data")

try:
    # Player with defaults
    p = Player(name="TestGhost")
    info(f"Player created: name={p.name}, xp={p.xp}, level={p.level}, title={p.level_title}")
    assert p.name == "TestGhost"
    assert p.xp == 0
    assert p.level == 1
    ok("Player default instantiation")

    # QuizQuestion
    q = QuizQuestion(
        question="What does ls do?",
        options=["A) List files", "B) Copy files", "C) Delete files", "D) Move files"],
        correct="A",
        explanation="ls lists directory contents.",
        xp_value=15,
    )
    assert len(q.options) == 4
    assert q.correct == "A"
    ok("QuizQuestion instantiation")

    # Mission with minimal fields
    m = Mission(
        mission_id="99.01",
        title="Smoke Test Mission",
        mtype="SCAN",
        xp=30,
        chapter=99,
        story="Test story.",
        speaker="SYSTEM",
        why_important="Testing.",
        explanation="Test explanation.",
        task_description="Run ls.",
        expected_commands=["ls"],
        quiz_questions=[q],
        exam_tip="Remember: test.",
        memory_tip="T-E-S-T.",
    )
    assert m.mission_id == "99.01"
    assert m.mtype == "SCAN"
    assert len(m.quiz_questions) == 1
    ok("Mission instantiation with real QuizQuestion")

    # HintRequest
    hr = HintRequest.create("99.01", ["free hint", "paid hint", "answer"], 0)
    assert hr is not None
    assert hr.xp_cost == 0
    assert hr.text == "free hint"
    ok("HintRequest.create() level 0")

except Exception as e:
    fail("Core data structure instantiation failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5: Verify CHAPTERS metadata in main.py matches imported data
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 5: Verify CHAPTERS metadata in main.py matches imported data")

try:
    from main import CHAPTERS

    info(f"CHAPTERS list length: {len(CHAPTERS)}")
    assert len(CHAPTERS) == 22, f"Expected 22 chapters, got {len(CHAPTERS)}"
    ok("main.CHAPTERS has 22 entries")

    # Verify each chapter tuple has 5 elements: (id, missions, topic, title, subtitle)
    for idx, ch in enumerate(CHAPTERS, 1):
        ch_id, missions, topic, title, subtitle = ch
        assert ch_id == idx, f"Chapter {idx} has ID {ch_id}"
        assert isinstance(missions, list), f"Chapter {idx} missions not a list"
        assert len(missions) > 0, f"Chapter {idx} has zero missions"
        assert isinstance(topic, str), f"Chapter {idx} topic not a string"
        assert isinstance(title, str), f"Chapter {idx} title not a string"
        assert isinstance(subtitle, str), f"Chapter {idx} subtitle not a string"

    ok("All 22 CHAPTERS tuples have correct structure and non-empty mission lists")

    # Cross-check: CHAPTERS mission counts match imported module counts
    mismatches = 0
    for ch_id, ch_missions, topic, title, subtitle in CHAPTERS:
        attr_name = f"CHAPTER_{ch_id}_MISSIONS"
        imported_count = len(chapter_lists.get(attr_name, []))
        chapters_count = len(ch_missions)
        if imported_count != chapters_count:
            fail(f"Chapter {ch_id}: imported count {imported_count} != CHAPTERS count {chapters_count}")
            mismatches += 1
        else:
            info(f"Chapter {ch_id:2d}: {chapters_count:2d} missions — match")

    if mismatches == 0:
        ok("All chapter mission counts match between imports and CHAPTERS")
    else:
        fail(f"{mismatches} chapters have count mismatches")

except Exception as e:
    fail("CHAPTERS metadata validation failed", e)


# ── Summary ───────────────────────────────────────────────────────────────────
banner("TEST 01 SUMMARY")
print("  Initialization smoke test completed.")
print(f"  Total missions in codebase: {total_missions}")
print(f"  Engine modules: OK")
print(f"  Chapter modules: {'OK' if all_imported else 'PARTIAL FAILURE'}")
