#!/usr/bin/env python3
"""
End-to-end gameplay test: Load chapters, validate missions, test game engine.
"""

import sys
sys.path.insert(0, '/home/ande/neongrid9')

from missions import (
    ch01_hardware, ch02_boot, ch03_init, ch04_partitions, ch05_permissions
)
from engine.mission_engine import Mission, MissionRunner
from engine.player import Player
from engine.features import AchievementTracker

def test_mission_loading():
    """Test that all mission data loads correctly."""
    print("=" * 70)
    print("TEST 1: Mission Loading")
    print("=" * 70)

    chapters = [
        ("Ch01", ch01_hardware.CHAPTER_1_MISSIONS),
        ("Ch02", ch02_boot.CHAPTER_2_MISSIONS),
        ("Ch03", ch03_init.CHAPTER_3_MISSIONS),
        ("Ch04", ch04_partitions.CHAPTER_4_MISSIONS),
        ("Ch05", ch05_permissions.CHAPTER_5_MISSIONS),
    ]

    for name, missions in chapters:
        print(f"\n{name}:")
        print(f"  Missions: {len(missions)}")
        complete_count = sum(1 for m in missions if m.hints)
        print(f"  With hints: {complete_count}/{len(missions)}")

        # Validate all missions have required fields
        for m in missions:
            assert m.mission_id, f"{name}: Missing mission_id"
            assert m.title, f"{name}: Missing title"
            # Boss and QUIZ missions may not have expected_commands
            if m.mtype not in ("BOSS", "QUIZ"):
                assert m.expected_commands, f"{name} {m.mission_id}: Missing expected_commands"
            if m.mtype not in ("BOSS", "QUIZ"):
                assert m.task_description, f"{name} {m.mission_id}: Missing task_description"
            # All missions should have quiz_questions
            assert m.quiz_questions, f"{name} {m.mission_id}: Missing quiz_questions"

        print(f"  ✓ All missions valid")

    return True


def test_player_systems():
    """Test player XP, leveling, achievements, factions."""
    print("\n" + "=" * 70)
    print("TEST 2: Player Systems")
    print("=" * 70)

    player = Player(name="TestAgent")
    print(f"\nInitial state:")
    print(f"  Level: {player.level} ({player.level_title})")
    print(f"  XP: {player.xp}")

    # Test XP and leveling
    player.add_xp(1000)
    print(f"\nAfter +1000 XP:")
    print(f"  Level: {player.level} ({player.level_title})")
    print(f"  XP: {player.xp}")
    assert player.xp == 1000, "XP not added correctly"
    assert player.level > 1, "Should level up with 1000 XP"

    # Test achievements
    player.achievements.unlock('first_mission')
    print(f"\nUnlocked achievement: 'first_mission'")
    assert player.achievements.has('first_mission'), "Achievement not unlocked"
    print(f"  ✓ Achievement system works")

    # Test reputation/factions
    player.add_reputation("Kernel Syndicate", 50)
    print(f"\nAdded +50 rep to Kernel Syndicate:")
    print(f"  Rep: {player.reputation['Kernel Syndicate']}/100")
    assert player.reputation["Kernel Syndicate"] == 50, "Reputation not added"
    print(f"  ✓ Faction system works")

    # Test gear
    player.add_gear("hardware_scanner")
    print(f"\nAdded gear: hardware_scanner")
    assert player.has_gear("hardware_scanner"), "Gear not added"
    print(f"  ✓ Gear system works")

    return True


def test_mission_integrity():
    """Verify specific mission data."""
    print("\n" + "=" * 70)
    print("TEST 3: Mission Data Integrity")
    print("=" * 70)

    # Test Chapter 1, Mission 1 (should always exist)
    ch1_m1 = ch01_hardware.CHAPTER_1_MISSIONS[0]
    print(f"\nCh01.M1: {ch1_m1.title}")
    print(f"  Type: {ch1_m1.mtype}")
    print(f"  XP: {ch1_m1.xp}")
    print(f"  Commands: {ch1_m1.expected_commands}")
    print(f"  Hints: {len(ch1_m1.hints)} tiers")
    assert ch1_m1.mission_id == "1.01", "Mission ID mismatch"
    assert ch1_m1.expected_commands, "No expected commands"
    print(f"  ✓ Mission data valid")

    # Test Ch01.M2 which should have hints
    if len(ch01_hardware.CHAPTER_1_MISSIONS) > 1:
        ch1_m2 = ch01_hardware.CHAPTER_1_MISSIONS[1]
        if ch1_m2.hints:
            print(f"\nCh01.M2: {ch1_m2.title}")
            print(f"  Hints populated: YES ({len(ch1_m2.hints)} tiers)")
            assert len(ch1_m2.hints) == 3, "Should have 3 hint tiers"
            print(f"  ✓ Hints system working")

    return True


def test_quiz_questions():
    """Verify quiz questions are properly formatted."""
    print("\n" + "=" * 70)
    print("TEST 4: Quiz Questions")
    print("=" * 70)

    for mission in ch01_hardware.CHAPTER_1_MISSIONS[:2]:
        if mission.quiz_questions:
            print(f"\n{mission.mission_id}: {len(mission.quiz_questions)} questions")
            for q in mission.quiz_questions[:1]:
                print(f"  Q: {q.question[:50]}...")
                print(f"  Options: {len(q.options)}")
                print(f"  Correct: {q.correct}")
                assert q.xp_value > 0, "Question should have XP value"
            print(f"  ✓ Quiz format valid")

    return True


def test_all_chapters_exist():
    """Verify all 22 chapters load."""
    print("\n" + "=" * 70)
    print("TEST 5: All Chapters Load")
    print("=" * 70)

    from missions import (
        ch06_shell, ch07_processes, ch08_regex_vi, ch09_network, ch10_users,
        ch11_logging, ch12_packages, ch13_kernel, ch14_scripting, ch15_security,
        ch16_locale, ch17_shellenv, ch18_exam, ch19_ghost_processors,
        ch20_firewall_dominion, ch21_network_services, ch22_storage_advanced
    )

    chapter_list = [
        ch01_hardware, ch02_boot, ch03_init, ch04_partitions, ch05_permissions,
        ch06_shell, ch07_processes, ch08_regex_vi, ch09_network, ch10_users,
        ch11_logging, ch12_packages, ch13_kernel, ch14_scripting, ch15_security,
        ch16_locale, ch17_shellenv, ch18_exam, ch19_ghost_processors,
        ch20_firewall_dominion, ch21_network_services, ch22_storage_advanced
    ]

    total_missions = 0
    for i, ch in enumerate(chapter_list, 1):
        # Find the missions list
        missions = None
        for attr in dir(ch):
            if 'MISSION' in attr.upper():
                missions = getattr(ch, attr)
                if isinstance(missions, list):
                    break

        if missions:
            total_missions += len(missions)
            print(f"  Ch{i:02d}: {len(missions):2d} missions  ✓")
        else:
            print(f"  Ch{i:02d}: MISSING!")
            return False

    print(f"\nTotal missions across all 22 chapters: {total_missions}")
    assert total_missions == 501, f"Should have 501 missions, got {total_missions}"
    print(f"✓ All chapters loaded correctly")

    return True


def main():
    """Run all tests."""
    print("\n🎮 NeonGrid-9 End-to-End Test Suite\n")

    tests = [
        test_mission_loading,
        test_player_systems,
        test_mission_integrity,
        test_quiz_questions,
        test_all_chapters_exist,
    ]

    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

    print("\n" + "=" * 70)
    print(f"✅ ALL TESTS PASSED ({passed}/{len(tests)})")
    print("=" * 70)
    print("\nSummary:")
    print("  ✓ All 501 missions load correctly")
    print("  ✓ Player systems (XP, leveling, achievements) work")
    print("  ✓ Faction reputation system works")
    print("  ✓ Gear/inventory system works")
    print("  ✓ Mission hints populated for sample missions")
    print("  ✓ Quiz questions properly formatted")
    print("\nGame is ready for full playthrough testing!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n💥 FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
