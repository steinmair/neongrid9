"""
Probe Test: Edge Cases
----------------------
Captures boundary behavior, empty inputs, and degenerate states.
These are the cases most likely to break during refactoring because
they rely on implicit default paths rather than obvious happy-path logic.

Run directly:
    cd /home/ande/neongrid9
    python3 probe_tests/pre_refactor/test_edge_cases.py
"""

import sys
import os
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.player import Player, LEVELS, GEAR_CATALOG, FACTIONS
from engine.mission_engine import Mission, QuizQuestion, MissionRunner
from engine.features import (
    HintRequest, AchievementTracker, calculate_level, FactionStatus
)
from engine.save_system import save_game, load_game, delete_save, SAVE_DIR, SAVE_FILES


class TestPlayerEdgeCases(unittest.TestCase):
    """Anchor Player behavior at boundaries."""

    def test_add_xp_zero(self):
        p = Player(name="ZeroXP")
        old = p.xp
        new_xp, leveled_up = p.add_xp(0)
        self.assertEqual(new_xp, old)
        self.assertFalse(leveled_up)

    def test_add_xp_negative(self):
        """Current engine allows negative XP input. Record this."""
        p = Player(name="NegXP")
        p.xp = 100
        new_xp, _ = p.add_xp(-50)
        self.assertEqual(new_xp, 50)

    def test_level_beyond_max(self):
        """Player with XP above max level table should stay at max level."""
        p = Player(name="OverLevel")
        p.xp = 999999
        p._recalculate_level()
        max_level = max(lvl for lvl, _, _ in LEVELS)
        self.assertEqual(p.level, max_level)

    def test_empty_inventory_gear_bonus(self):
        p = Player(name="EmptyInv")
        p.inventory = []
        self.assertEqual(p.gear_bonus("quiz_xp"), 1.0)
        self.assertEqual(p.gear_bonus("all_xp"), 1.0)

    def test_add_gear_already_owned(self):
        p = Player(name="DupGear")
        p.add_gear("ghost_mask")
        first = len(p.inventory)
        result = p.add_gear("ghost_mask")
        self.assertFalse(result)
        self.assertEqual(len(p.inventory), first)

    def test_add_gear_invalid_id(self):
        p = Player(name="BadGear")
        self.assertFalse(p.add_gear("not_a_real_gear"))

    def test_quiz_accuracy_no_data(self):
        p = Player(name="NoQuiz")
        self.assertEqual(p.quiz_accuracy(999), 0.0)
        self.assertEqual(p.quiz_accuracy(1), 0.0)

    def test_quiz_accuracy_perfect(self):
        p = Player(name="Perfect")
        for _ in range(5):
            p.record_quiz_result(3, True)
        self.assertEqual(p.quiz_accuracy(3), 1.0)

    def test_quiz_accuracy_zero_correct(self):
        p = Player(name="AllWrong")
        for _ in range(5):
            p.record_quiz_result(3, False)
        self.assertEqual(p.quiz_accuracy(3), 0.0)

    def test_reputation_unknown_faction(self):
        """Adding reputation to unknown faction is silently ignored."""
        p = Player(name="UnknownFaction")
        p.add_reputation("Not A Faction", 50)
        self.assertNotIn("Not A Faction", p.reputation)

    def test_stats_summary_with_no_faction_rep(self):
        p = Player(name="NoRep")
        summary = p.stats_summary()
        self.assertIn("Kernel Syndicate", summary)

    def test_has_hint_gear_without_hint_gear(self):
        p = Player(name="NoHintGear")
        p.inventory = ["basic_terminal"]
        self.assertFalse(p.has_hint_gear())

    def test_has_hint_gear_with_cracked_manpage(self):
        p = Player(name="HintGear")
        p.inventory = ["basic_terminal", "cracked_manpage"]
        self.assertTrue(p.has_hint_gear())

    def test_to_dict_with_empty_collections(self):
        p = Player(name="Empty")
        p.completed_missions = set()
        p.inventory = []
        d = p.to_dict()
        self.assertEqual(d["completed_missions"], [])
        self.assertEqual(d["inventory"], [])

    def test_from_dict_with_partial_and_extra_keys(self):
        """Extra keys in JSON should not crash; missing keys use defaults."""
        d = {
            "name": "Extra",
            "xp": 100,
            "unknown_field": "should_be_ignored",
        }
        p = Player.from_dict(d)
        self.assertEqual(p.name, "Extra")
        self.assertEqual(p.xp, 100)
        self.assertEqual(p.level, 1)
        # unknown_field is not mapped — no error


class TestMissionEdgeCases(unittest.TestCase):
    """Anchor Mission behavior at boundaries."""

    def test_mission_no_quiz_questions(self):
        """Some missions (e.g. pure terminal tasks) may have no quiz."""
        m = Mission(
            mission_id="9.99",
            title="No Quiz",
            mtype="SCAN",
            xp=30,
            chapter=1,
            quiz_questions=[],
        )
        self.assertEqual(len(m.quiz_questions), 0)

    def test_mission_no_expected_commands(self):
        """QUIZ-type missions have no terminal task."""
        m = Mission(
            mission_id="9.98",
            title="Quiz Only",
            mtype="QUIZ",
            xp=30,
            chapter=1,
            expected_commands=[],
            task_description="",
        )
        self.assertEqual(len(m.expected_commands), 0)

    def test_mission_empty_hints(self):
        m = Mission(
            mission_id="9.97",
            title="No Hints",
            mtype="SCAN",
            xp=30,
            chapter=1,
            hints=[],
        )
        self.assertEqual(len(m.hints), 0)

    def test_boss_without_gear_reward(self):
        m = Mission(
            mission_id="1.22",
            title="Boss",
            mtype="BOSS",
            xp=200,
            chapter=1,
            boss_name="Test Boss",
            boss_desc="Desc",
            gear_reward=None,
        )
        self.assertIsNone(m.gear_reward)

    def test_quiz_question_empty_options(self):
        """Degenerate: 0 options — current engine allows this. Record it."""
        q = QuizQuestion(
            question="Empty?",
            options=[],
            correct="A",
            explanation="none",
        )
        self.assertEqual(len(q.options), 0)

    def test_quiz_question_empty_explanation(self):
        q = QuizQuestion(
            question="NoExplain?",
            options=["A) a", "B) b", "C) c", "D) d"],
            correct="A",
            explanation="",
        )
        self.assertEqual(q.explanation, "")

    def test_quiz_question_negative_xp(self):
        """Current engine allows negative xp_value. Record this."""
        q = QuizQuestion(
            question="Neg?",
            options=["A) a"],
            correct="A",
            explanation="bad",
            xp_value=-5,
        )
        self.assertEqual(q.xp_value, -5)


class TestSaveEdgeCases(unittest.TestCase):
    """Anchor save system resilience."""

    def setUp(self):
        self.test_slot = 98
        self._orig_save_files = dict(SAVE_FILES)
        SAVE_FILES[self.test_slot] = SAVE_DIR / f"save_slot{self.test_slot}.json"
        delete_save(self.test_slot)

    def tearDown(self):
        delete_save(self.test_slot)
        SAVE_FILES.clear()
        SAVE_FILES.update(self._orig_save_files)

    def test_load_corrupt_json(self):
        """Corrupt JSON must return None, not crash."""
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        path = SAVE_DIR / f"save_slot{self.test_slot}.json"
        path.write_text("this is not json")
        result = load_game(self.test_slot)
        self.assertIsNone(result)

    def test_load_empty_json_file(self):
        """Empty file must return None."""
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        path = SAVE_DIR / f"save_slot{self.test_slot}.json"
        path.write_text("")
        result = load_game(self.test_slot)
        self.assertIsNone(result)

    def test_load_json_null(self):
        """JSON null must return None."""
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        path = SAVE_DIR / f"save_slot{self.test_slot}.json"
        path.write_text("null")
        result = load_game(self.test_slot)
        self.assertIsNone(result)

    def test_save_with_unicode_name(self):
        p = Player(name="Zärä Z3R0 🔥")
        save_game(p, self.test_slot)
        p2 = load_game(self.test_slot)
        self.assertEqual(p2.name, "Zärä Z3R0 🔥")


class TestFeatureEdgeCases(unittest.TestCase):
    """Anchor HintRequest and Achievement edge behavior."""

    def test_hint_request_level_negative(self):
        """Negative level index raises ValueError in current engine. Record this."""
        hints = ["free"]
        with self.assertRaises(ValueError):
            HintRequest.create("1.01", hints, -1)

    def test_achievement_unlock_same_id_twice(self):
        tracker = AchievementTracker()
        tracker.unlock("first_mission")
        tracker.unlock("first_mission")
        self.assertEqual(tracker.count(), 1)

    def test_calculate_level_exact_boundary_100(self):
        """100 is the switch point between rep and XP mode."""
        # 100 <= 100 → reputation mode
        self.assertEqual(calculate_level(100), 5)
        # 101 > 100 → XP mode, threshold 100 crossed → level 2
        self.assertEqual(calculate_level(101), 2)

    def test_faction_status_zero_xp(self):
        fs = FactionStatus(name="Zero", xp=0, level=1, max_xp=100)
        bar = fs.progress_bar(width=10)
        self.assertEqual(bar, "░░░░░░░░░░")

    def test_faction_status_max_xp(self):
        fs = FactionStatus(name="Max", xp=100, level=5, max_xp=100)
        bar = fs.progress_bar(width=10)
        self.assertEqual(bar, "██████████")


class TestMissionRunnerEdgeCases(unittest.TestCase):
    """Anchor MissionRunner boundary behavior."""

    def test_runner_with_no_save_callback(self):
        p = Player(name="NoSaveCB")
        runner = MissionRunner(p, save_callback=None)
        self.assertIsNone(runner.save_callback)

    def test_runner_replay_on_uncompleted_mission(self):
        """Replay path is only taken if mission is completed AND not BOSS."""
        p = Player(name="ReplayTest")
        m = Mission(mission_id="1.01", title="T", mtype="SCAN", xp=30, chapter=1)
        runner = MissionRunner(p, save_callback=None)
        # Not completed → run() will execute full path (we can't test run() due to input(),
        # but we can verify the decision logic by checking the method that would be called)
        self.assertFalse(p.mission_completed(m.mission_id))


if __name__ == "__main__":
    unittest.main(verbosity=2)
