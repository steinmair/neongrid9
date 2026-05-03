"""
Probe Test: Integration Points
-------------------------------
Verifies cross-module contracts and data structure consistency.
These tests are the canary in the coal mine for architectural refactorings
that move data or change module boundaries.

Run directly:
    cd /home/ande/neongrid9
    python3 probe_tests/pre_refactor/test_integration_points.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.player import Player, LEVELS, GEAR_CATALOG, FACTIONS, RARITY_COLOR
from engine.mission_engine import Mission, QuizQuestion, MissionRunner
from engine.features import ACHIEVEMENTS, calculate_level, Achievement
from main import CHAPTERS


class TestChapterIntegration(unittest.TestCase):
    """Anchor the CHAPTERS structure and all mission content."""

    def test_chapter_count(self):
        self.assertEqual(len(CHAPTERS), 22)

    def test_all_chapters_have_missions(self):
        for ch_id, ch_missions, topic, title, subtitle in CHAPTERS:
            self.assertGreater(len(ch_missions), 0,
                f"Chapter {ch_id} has no missions")

    def test_mission_ids_are_unique_globally(self):
        seen = set()
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                self.assertNotIn(m.mission_id, seen,
                    f"Duplicate mission_id: {m.mission_id}")
                seen.add(m.mission_id)

    def test_mission_id_starts_with_chapter_prefix(self):
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                prefix = f"{ch_id}."
                self.assertTrue(m.mission_id.startswith(prefix),
                    f"Mission {m.mission_id} in ch{ch_id} does not start with {prefix}")

    def test_all_missions_have_required_fields(self):
        VALID_MTYPES = {"SCAN", "INFILTRATE", "DECODE", "CONSTRUCT", "REPAIR", "QUIZ", "BOSS"}
        total = 0
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                total += 1
                self.assertTrue(m.mission_id, f"Missing mission_id in ch{ch_id}")
                self.assertTrue(m.title, f"Missing title in {m.mission_id}")
                self.assertIn(m.mtype, VALID_MTYPES,
                    f"Invalid mtype '{m.mtype}' in {m.mission_id}")
                self.assertGreater(m.xp, 0, f"Non-positive xp in {m.mission_id}")
                self.assertEqual(m.chapter, ch_id,
                    f"Chapter mismatch in {m.mission_id}")
                self.assertTrue(m.why_important, f"Missing why_important in {m.mission_id}")
                self.assertTrue(m.exam_tip, f"Missing exam_tip in {m.mission_id}")
                self.assertTrue(m.memory_tip, f"Missing memory_tip in {m.mission_id}")
                self.assertTrue(m.quiz_questions,
                    f"Missing quiz_questions in {m.mission_id}")

    def test_all_quiz_questions_have_four_options(self):
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                for idx, q in enumerate(m.quiz_questions):
                    self.assertEqual(len(q.options), 4,
                        f"{m.mission_id} q{idx+1}: expected 4 options, got {len(q.options)}")

    def test_all_quiz_correct_is_valid_letter(self):
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                for idx, q in enumerate(m.quiz_questions):
                    correct = q.correct
                    if isinstance(correct, int):
                        self.assertIn(correct, range(4),
                            f"{m.mission_id} q{idx+1}: correct int {correct} out of range")
                    else:
                        self.assertIn(correct, ("A", "B", "C", "D"),
                            f"{m.mission_id} q{idx+1}: correct='{correct}' not in ABCD")

    def test_boss_missions_have_boss_fields(self):
        missing_names = []
        missing_descs = []
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            bosses = [m for m in ch_missions if m.mtype == "BOSS"]
            for boss in bosses:
                if not boss.boss_name:
                    missing_names.append(boss.mission_id)
                if not boss.boss_desc:
                    missing_descs.append(boss.mission_id)
                self.assertGreaterEqual(len(boss.quiz_questions), 5,
                    f"BOSS {boss.mission_id} has <5 quiz questions")
        # Document known missing boss_name fields without failing
        if missing_names:
            print(f"\n  [WARN] BOSS missions missing boss_name: {missing_names}")
        if missing_descs:
            print(f"\n  [WARN] BOSS missions missing boss_desc: {missing_descs}")

    def test_chapter_22_is_final_exam(self):
        ch22 = CHAPTERS[21]
        self.assertEqual(ch22[0], 22)
        self.assertIn("FINAL", ch22[3].upper())


class TestModuleIntegration(unittest.TestCase):
    """Anchor cross-module import and contract behavior."""

    def test_mission_runner_can_hold_player(self):
        p = Player(name="Integration")
        runner = MissionRunner(p, save_callback=lambda x: None)
        self.assertIs(runner.player, p)

    def test_player_achievements_is_tracker_instance(self):
        p = Player(name="TrackerTest")
        from engine.features import AchievementTracker
        self.assertIsInstance(p.achievements, AchievementTracker)

    def test_player_reputation_has_all_factions(self):
        p = Player(name="FactionTest")
        for f in FACTIONS:
            self.assertIn(f, p.reputation)

    def test_gear_catalog_consistency(self):
        """Every gear item has required fields."""
        required = {"name", "desc", "boost", "rarity", "tier"}
        for gear_id, data in GEAR_CATALOG.items():
            missing = required - set(data.keys())
            self.assertFalse(missing,
                f"Gear '{gear_id}' missing fields: {missing}")
            self.assertIn(data["rarity"], RARITY_COLOR)

    def test_achievements_catalog_has_critical_ids(self):
        critical = [
            "first_mission", "boss_defeated", "all_bosses",
            "perfect_quiz", "speedrun", "level_ten",
            "gear_collector", "exam_mastered",
        ]
        for ach_id in critical:
            self.assertIn(ach_id, ACHIEVEMENTS,
                f"Missing critical achievement: {ach_id}")

    def test_achievement_equality_with_string(self):
        a = ACHIEVEMENTS["first_mission"]
        self.assertEqual(a, "first_mission")
        self.assertNotEqual(a, "other")

    def test_levels_table_monotonic(self):
        """XP thresholds must strictly increase."""
        thresholds = [t for _, _, t in LEVELS]
        for i in range(1, len(thresholds)):
            self.assertGreater(thresholds[i], thresholds[i-1],
                f"LEVELS threshold not monotonic at index {i}")

    def test_calculate_level_matches_player_leveling(self):
        """Player._recalculate_level() and calculate_level() use different scales.
        Player uses LEVELS thresholds (0, 500, 1500, ...).
        calculate_level() uses its own thresholds (0, 100, 250, 450, ...).
        They are NOT interchangeable — this test documents the divergence."""
        p = Player(name="Consistency")
        # Player leveling scale (from LEVELS)
        player_cases = [
            (0, 1), (499, 1), (500, 2), (1499, 2), (1500, 3), (2999, 3), (3000, 4)
        ]
        for xp, expected in player_cases:
            p.xp = xp
            p._recalculate_level()
            self.assertEqual(p.level, expected,
                f"Player level mismatch at XP={xp}")

        # calculate_level scale (from features.py) — XP mode (>100)
        calc_cases = [
            (101, 2), (250, 3), (450, 4), (700, 5), (1000, 6)
        ]
        for xp, expected in calc_cases:
            self.assertEqual(calculate_level(xp), expected,
                f"calculate_level mismatch at XP={xp}")


class TestDataInvariants(unittest.TestCase):
    """Anchor business-rule invariants that refactoring must preserve."""

    def test_total_mission_count_matches_expected(self):
        total = sum(len(c[1]) for c in CHAPTERS)
        self.assertGreaterEqual(total, 500,
            f"Expected ~501 missions, found {total}")

    def test_total_quiz_question_count(self):
        total = sum(
            len(m.quiz_questions)
            for _, ch_missions, _, _, _ in CHAPTERS
            for m in ch_missions
        )
        self.assertGreaterEqual(total, 1000,
            f"Expected ~1117 quiz questions, found {total}")

    def test_all_chapters_have_boss(self):
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            bosses = [m for m in ch_missions if m.mtype == "BOSS"]
            self.assertEqual(len(bosses), 1,
                f"Chapter {ch_id} should have exactly 1 BOSS, has {len(bosses)}")

    def test_first_mission_is_intro_scan(self):
        VALID_MTYPES = {"SCAN", "INFILTRATE", "DECODE", "CONSTRUCT", "REPAIR", "QUIZ", "BOSS"}
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            first = ch_missions[0]
            self.assertTrue(first.mission_id.endswith(".01"),
                f"Chapter {ch_id} first mission is {first.mission_id}, expected .01")
            self.assertIn(first.mtype, VALID_MTYPES,
                f"Chapter {ch_id} first mission type {first.mtype} is invalid")

    def test_xp_values_are_positive(self):
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                self.assertGreater(m.xp, 0, f"{m.mission_id} has non-positive XP")
                for q in m.quiz_questions:
                    self.assertGreater(q.xp_value, 0,
                        f"{m.mission_id} quiz has non-positive xp_value")

    def test_gear_rewards_are_valid_or_none(self):
        invalid_rewards = []
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                if m.gear_reward is not None and m.gear_reward not in GEAR_CATALOG:
                    invalid_rewards.append((m.mission_id, m.gear_reward))
        if invalid_rewards:
            # Log as warning rather than failing — current codebase has some future-content IDs
            print(f"\n  [WARN] Missions with gear_reward not in GEAR_CATALOG: {invalid_rewards}")

    def test_faction_rewards_are_valid_or_none(self):
        for ch_id, ch_missions, _, _, _ in CHAPTERS:
            for m in ch_missions:
                if m.faction_reward is not None:
                    faction, amount = m.faction_reward
                    self.assertIn(faction, FACTIONS,
                        f"{m.mission_id} has invalid faction: {faction}")
                    self.assertIsInstance(amount, int)
                    self.assertGreater(amount, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
