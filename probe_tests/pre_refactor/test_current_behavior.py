"""
Probe Test: Current Behavior
-----------------------------
Captures the exact behavior of core engine functions BEFORE refactoring.
These tests serve as a safety net: if they fail after refactoring,
the refactoring broke something.

Run directly:
    cd /home/ande/neongrid9
    python3 probe_tests/pre_refactor/test_current_behavior.py

Coverage:
- Player XP/level progression, gear bonuses, reputation, quiz stats
- Mission dataclass defaults and QuizQuestion validation
- HintRequest creation logic
- AchievementTracker unlock semantics (idempotent, invalid IDs)
- Save/load round-trip fidelity
- calculate_level dual-mode behavior (reputation vs XP)
"""

import sys
import os
import json
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.player import Player, LEVELS, GEAR_CATALOG, FACTIONS, RARITY_COLOR
from engine.mission_engine import Mission, QuizQuestion, MissionRunner
from engine.features import (
    HintRequest, HintLevel, AchievementTracker, Achievement,
    ACHIEVEMENTS, calculate_level, FactionStatus
)
from engine.save_system import save_game, load_game, delete_save, slot_info, SAVE_DIR, SAVE_FILES


# ──────────────────────────────────────────────────────────────────────────────
# Player Core Behavior
# ──────────────────────────────────────────────────────────────────────────────

class TestPlayerCore(unittest.TestCase):
    """Anchor the Player dataclass behavior."""

    def test_default_player_state(self):
        p = Player(name="TestGhost")
        self.assertEqual(p.name, "TestGhost")
        self.assertEqual(p.xp, 0)
        self.assertEqual(p.level, 1)
        self.assertEqual(p.level_title, "Newbie Hacker")
        self.assertEqual(p.inventory, ["basic_terminal", "cracked_manpage"])
        self.assertEqual(len(p.completed_missions), 0)
        self.assertEqual(p.bosses_defeated, 0)
        self.assertEqual(p.total_quizzes, 0)
        self.assertEqual(p.correct_first_try, 0)
        self.assertEqual(p.hints_used, 0)

    def test_level_progression_exact_thresholds(self):
        """LEVELS table must produce exact level at exact XP thresholds."""
        p = Player(name="LevelTest")
        # Just under threshold
        p.xp = 499
        p._recalculate_level()
        self.assertEqual(p.level, 1)
        # Exactly at threshold
        p.xp = 500
        p._recalculate_level()
        self.assertEqual(p.level, 2)
        self.assertEqual(p.level_title, "Script Kiddie")

    def test_add_xp_returns_tuple(self):
        p = Player(name="XPTest")
        new_xp, leveled_up = p.add_xp(100)
        self.assertIsInstance(new_xp, int)
        self.assertIsInstance(leveled_up, bool)
        self.assertEqual(new_xp, p.xp)

    def test_xp_scaling_by_level(self):
        """XP scaling multipliers must match current engine values."""
        p = Player(name="ScaleTest")
        # Level 1-4: scale = 1.0
        p.level = 1
        old = p.xp
        p.add_xp(100)
        self.assertEqual(p.xp - old, 100)

        # Level 5-9: scale = 1.1
        p.level = 5
        p.xp = 5000
        old = p.xp
        p.add_xp(100)
        self.assertEqual(p.xp - old, 110)

        # Level 10-14: scale = 1.2
        p.level = 10
        p.xp = 22500
        old = p.xp
        p.add_xp(100)
        self.assertEqual(p.xp - old, 120)

        # Level 15+: scale = 1.3
        p.level = 15
        p.xp = 52500
        old = p.xp
        p.add_xp(100)
        self.assertEqual(p.xp - old, 130)

    def test_mission_completion(self):
        p = Player(name="MissionTest")
        self.assertFalse(p.mission_completed("1.01"))
        p.complete_mission("1.01")
        self.assertTrue(p.mission_completed("1.01"))
        # Idempotent
        p.complete_mission("1.01")
        self.assertEqual(len(p.completed_missions), 1)

    def test_gear_bonus_no_gear(self):
        p = Player(name="NoGear")
        self.assertEqual(p.gear_bonus("quiz_xp"), 1.0)
        self.assertEqual(p.gear_bonus("nonexistent_boost"), 1.0)

    def test_gear_bonus_ghost_mask(self):
        p = Player(name="QuizGear")
        p.add_gear("ghost_mask")
        self.assertEqual(p.gear_bonus("quiz_xp"), 1.20)

    def test_gear_bonus_linux_badge_stacks(self):
        p = Player(name="StackTest")
        p.add_gear("ghost_mask")
        p.add_gear("linux_badge")
        # ghost_mask gives 1.20, linux_badge adds +0.05 when base > 1.0
        self.assertEqual(p.gear_bonus("quiz_xp"), 1.25)

    def test_gear_bonus_linux_badge_alone(self):
        p = Player(name="BadgeOnly")
        p.add_gear("linux_badge")
        self.assertEqual(p.gear_bonus("any_boost"), 1.05)

    def test_reputation_capped_at_100(self):
        p = Player(name="RepTest")
        p.add_reputation("Kernel Syndicate", 200)
        self.assertEqual(p.reputation["Kernel Syndicate"], 100)

    def test_quiz_accuracy_empty(self):
        p = Player(name="AccuracyTest")
        self.assertEqual(p.quiz_accuracy(1), 0.0)

    def test_quiz_accuracy_calculation(self):
        p = Player(name="AccuracyTest")
        p.record_quiz_result(1, True)
        p.record_quiz_result(1, True)
        p.record_quiz_result(1, False)
        self.assertAlmostEqual(p.quiz_accuracy(1), 2/3, places=5)

    def test_stats_summary_contains_key_fields(self):
        p = Player(name="SummaryTest")
        summary = p.stats_summary()
        self.assertIn("SummaryTest", summary)
        self.assertIn("Newbie Hacker", summary)
        self.assertIn("AUSRÜSTUNG", summary)
        self.assertIn("FRAKTIONEN", summary)

    def test_to_dict_roundtrip_fidelity(self):
        p = Player(name="RoundTrip")
        p.complete_mission("1.01")
        p.complete_mission("2.05")
        p.add_gear("hardware_scanner")
        p.add_reputation("Kernel Syndicate", 25)
        p.record_quiz_result(1, True)
        p.record_quiz_result(1, False)
        p.total_quizzes = 3
        p.correct_first_try = 2
        p.bosses_defeated = 1
        p.hints_used = 3
        p.total_playtime = 1234

        d = p.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["name"], "RoundTrip")
        self.assertEqual(set(d["completed_missions"]), {"1.01", "2.05"})
        self.assertIn("hardware_scanner", d["inventory"])
        self.assertEqual(d["reputation"]["Kernel Syndicate"], 25)
        self.assertEqual(d["total_quizzes"], 3)

    def test_from_dict_populates_defaults_for_missing_keys(self):
        """Partial dict must not crash — engine fills defaults."""
        p = Player.from_dict({"name": "Partial"})
        self.assertEqual(p.name, "Partial")
        self.assertEqual(p.xp, 0)
        self.assertEqual(p.level, 1)
        self.assertEqual(p.inventory, ["basic_terminal", "cracked_manpage"])


# ──────────────────────────────────────────────────────────────────────────────
# Mission Engine
# ──────────────────────────────────────────────────────────────────────────────

class TestMissionEngine(unittest.TestCase):
    """Anchor Mission and QuizQuestion dataclass behavior."""

    def test_mission_defaults(self):
        m = Mission(
            mission_id="1.01",
            title="Test",
            mtype="SCAN",
            xp=30,
            chapter=1,
        )
        self.assertEqual(m.ascii_art, "")
        self.assertEqual(m.story_transitions, [])
        self.assertEqual(m.expected_commands, [])
        self.assertEqual(m.quiz_questions, [])
        self.assertIsNone(m.gear_reward)
        self.assertIsNone(m.faction_reward)

    def test_quiz_question_correct_as_string(self):
        q = QuizQuestion(
            question="Q?",
            options=["A) a", "B) b", "C) c", "D) d"],
            correct="B",
            explanation="Because B",
        )
        self.assertEqual(q.correct, "B")
        self.assertEqual(q.xp_value, 15)

    def test_quiz_question_correct_as_int(self):
        """Some legacy questions may use int index for correct."""
        q = QuizQuestion(
            question="Q?",
            options=["A) a", "B) b", "C) c", "D) d"],
            correct=1,
            explanation="Because B",
        )
        # The field stores int directly; resolution happens at runtime
        self.assertEqual(q.correct, 1)

    def test_mission_runner_instantiation(self):
        p = Player(name="RunnerTest")
        runner = MissionRunner(p, save_callback=None)
        self.assertIs(runner.player, p)
        self.assertIsNone(runner.save_callback)


# ──────────────────────────────────────────────────────────────────────────────
# Features (Hints, Achievements, Factions)
# ──────────────────────────────────────────────────────────────────────────────

class TestFeatures(unittest.TestCase):
    """Anchor HintRequest, AchievementTracker, and calculate_level."""

    def test_hint_request_levels(self):
        hints = ["free", "standard", "final"]
        hr0 = HintRequest.create("1.01", hints, 0)
        self.assertEqual(hr0.level, HintLevel.FREE)
        self.assertEqual(hr0.xp_cost, 0)

        hr1 = HintRequest.create("1.01", hints, 1)
        self.assertEqual(hr1.level, HintLevel.STANDARD)
        self.assertEqual(hr1.xp_cost, 20)

        hr2 = HintRequest.create("1.01", hints, 2)
        self.assertEqual(hr2.level, HintLevel.FINAL)
        self.assertEqual(hr2.xp_cost, 50)

    def test_hint_request_out_of_range(self):
        self.assertIsNone(HintRequest.create("1.01", ["only"], 1))
        self.assertIsNone(HintRequest.create("1.01", [], 0))

    def test_achievement_unlock(self):
        tracker = AchievementTracker()
        result = tracker.unlock("first_mission")
        self.assertIsInstance(result, Achievement)
        self.assertEqual(result.name, "First Signal")
        # Idempotent
        self.assertIsNone(tracker.unlock("first_mission"))
        self.assertEqual(tracker.count(), 1)

    def test_achievement_unlock_invalid_id(self):
        tracker = AchievementTracker()
        self.assertIsNone(tracker.unlock("does_not_exist"))

    def test_achievement_has(self):
        tracker = AchievementTracker()
        tracker.unlock("first_mission")
        self.assertTrue(tracker.has("first_mission"))
        self.assertFalse(tracker.has("boss_defeated"))

    def test_calculate_level_reputation_mode(self):
        """Values <= 100 use reputation scale (1-5)."""
        self.assertEqual(calculate_level(0), 1)
        self.assertEqual(calculate_level(19), 1)
        self.assertEqual(calculate_level(20), 2)
        self.assertEqual(calculate_level(100), 5)

    def test_calculate_level_xp_mode(self):
        """Values > 100 use XP scale (1-10)."""
        self.assertEqual(calculate_level(101), 2)
        self.assertEqual(calculate_level(250), 3)
        self.assertEqual(calculate_level(450), 4)
        self.assertEqual(calculate_level(3250), 10)
        self.assertEqual(calculate_level(5000), 10)

    def test_faction_status_progress_bar_width(self):
        fs = FactionStatus(name="Test", xp=50, level=3, max_xp=100)
        bar = fs.progress_bar(width=20)
        self.assertEqual(len(bar), 20)
        self.assertIn("█", bar)
        self.assertIn("░", bar)

    def test_faction_status_display_contains_name_and_level(self):
        fs = FactionStatus(name="Kernel Syndicate", xp=45, level=3, max_xp=100)
        display = fs.display()
        self.assertIn("Kernel Syndicate", display)
        self.assertIn("Lv3", display)


# ──────────────────────────────────────────────────────────────────────────────
# Save System
# ──────────────────────────────────────────────────────────────────────────────

class TestSaveSystem(unittest.TestCase):
    """Anchor save/load/delete round-trip with real filesystem."""

    def setUp(self):
        self.test_slot = 99  # Use a slot unlikely to collide with real saves
        # Monkey-patch SAVE_FILES so slot 99 is valid
        self._orig_save_files = dict(SAVE_FILES)
        SAVE_FILES[self.test_slot] = SAVE_DIR / f"save_slot{self.test_slot}.json"
        # Ensure save dir exists
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        # Clean up any pre-existing test artifact
        delete_save(self.test_slot)

    def tearDown(self):
        delete_save(self.test_slot)
        SAVE_FILES.clear()
        SAVE_FILES.update(self._orig_save_files)

    def test_save_and_load_full_player(self):
        p = Player(name="SaveTest")
        p.add_xp(3500)
        p.complete_mission("1.01")
        p.complete_mission("1.02")
        p.add_gear("hardware_scanner")
        p.add_reputation("Kernel Syndicate", 25)
        p.record_quiz_result(1, True)
        p.record_quiz_result(1, False)
        p.total_quizzes = 3
        p.correct_first_try = 2
        p.bosses_defeated = 1
        p.hints_used = 3
        p.total_playtime = 1234

        self.assertTrue(save_game(p, self.test_slot))
        p2 = load_game(self.test_slot)
        self.assertIsNotNone(p2)
        self.assertEqual(p2.name, "SaveTest")
        self.assertEqual(p2.xp, p.xp)
        self.assertEqual(p2.level, p.level)
        self.assertEqual(p2.level_title, p.level_title)
        self.assertEqual(p2.completed_missions, p.completed_missions)
        self.assertEqual(set(p2.inventory), set(p.inventory))
        self.assertEqual(p2.reputation["Kernel Syndicate"], 25)
        self.assertEqual(p2.total_quizzes, 3)
        self.assertEqual(p2.correct_first_try, 2)
        self.assertEqual(p2.bosses_defeated, 1)
        self.assertEqual(p2.hints_used, 3)
        self.assertEqual(p2.total_playtime, 1234)

    def test_load_empty_slot_returns_none(self):
        self.assertIsNone(load_game(self.test_slot))

    def test_delete_save_returns_false_when_empty(self):
        self.assertFalse(delete_save(self.test_slot))

    def test_slot_info_empty(self):
        info = slot_info(self.test_slot)
        self.assertIn("LEER", info)

    def test_slot_info_after_save(self):
        p = Player(name="SlotInfoTest")
        p.add_xp(500)
        save_game(p, self.test_slot)
        info = slot_info(self.test_slot)
        self.assertIn("SlotInfoTest", info)
        self.assertIn("LVL", info.upper())

    def test_save_returns_false_on_bad_slot(self):
        p = Player(name="BadSlot")
        self.assertFalse(save_game(p, 999))


# ──────────────────────────────────────────────────────────────────────────────
# Performance Baseline
# ──────────────────────────────────────────────────────────────────────────────

class TestPerformanceBaseline(unittest.TestCase):
    """Record execution times for hot paths. If these regress significantly
    after refactoring, investigate immediately."""

    def test_player_to_dict_speed(self):
        p = Player(name="PerfTest")
        for i in range(100):
            p.complete_mission(f"1.{i:02d}")
        start = time.perf_counter()
        for _ in range(1000):
            _ = p.to_dict()
        elapsed = time.perf_counter() - start
        # Baseline: ~0.05s for 1000 iterations on modern hardware
        self.assertLess(elapsed, 1.0, f"to_dict too slow: {elapsed:.3f}s")

    def test_player_from_dict_speed(self):
        d = Player(name="PerfTest").to_dict()
        start = time.perf_counter()
        for _ in range(1000):
            _ = Player.from_dict(d)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 1.0, f"from_dict too slow: {elapsed:.3f}s")

    def test_calculate_level_speed(self):
        start = time.perf_counter()
        for _ in range(10000):
            _ = calculate_level(1500)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 1.0, f"calculate_level too slow: {elapsed:.3f}s")


if __name__ == "__main__":
    unittest.main(verbosity=2)
