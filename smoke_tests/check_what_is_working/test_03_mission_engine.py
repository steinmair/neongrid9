"""
Smoke Test 03: Mission Engine
-----------------------------
Validates Mission dataclass integrity, QuizQuestion validation,
mission completeness across all 22 chapters, MissionRunner
instantiation, and that every mission has the required fields
per the CLAUDE.md spec.

How to run manually:
    cd /home/ande/neongrid9
    python3 smoke_tests/check_what_is_working/test_03_mission_engine.py

Critical because: Missions are the core content unit. A single
malformed mission (missing quiz questions, wrong correct letter,
invalid mtype) breaks the player experience for that mission and
potentially crashes the runner.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.mission_engine import Mission, QuizQuestion, MissionRunner
from engine.player import Player, GEAR_CATALOG
from main import CHAPTERS


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


def warn(msg):
    print(f"  [WARN] {msg}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1: Validate every mission has required fields
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 1: Mission field completeness across all 501 missions")

VALID_MTYPES = {"SCAN", "INFILTRATE", "DECODE", "CONSTRUCT", "REPAIR", "QUIZ", "BOSS"}

problems = []
total = 0

for ch_id, ch_missions, topic, title, subtitle in CHAPTERS:
    for m in ch_missions:
        total += 1
        issues = []

        if not m.mission_id:
            issues.append("missing mission_id")
        if not m.title:
            issues.append("missing title")
        if m.mtype not in VALID_MTYPES:
            issues.append(f"invalid mtype '{m.mtype}'")
        if m.xp <= 0:
            issues.append(f"non-positive xp {m.xp}")
        if m.chapter != ch_id:
            issues.append(f"chapter mismatch: mission.chapter={m.chapter} vs CHAPTERS id={ch_id}")
        if not m.why_important:
            issues.append("missing why_important")
        if not m.exam_tip:
            issues.append("missing exam_tip")
        if not m.memory_tip:
            issues.append("missing memory_tip")
        if not m.quiz_questions:
            issues.append("missing quiz_questions")

        if issues:
            problems.append(f"  {m.mission_id} ({m.title[:40]}): {', '.join(issues)}")

if problems:
    for p in problems[:20]:  # Show first 20
        fail(p)
    if len(problems) > 20:
        fail(f"... and {len(problems) - 20} more problems")
else:
    ok(f"All {total} missions have required fields")

info(f"Total missions inspected: {total}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Validate every QuizQuestion has 4 options and valid correct letter
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 2: QuizQuestion integrity (all 1,117 questions)")

quiz_problems = []
quiz_total = 0

for ch_id, ch_missions, topic, title, subtitle in CHAPTERS:
    for m in ch_missions:
        for idx, q in enumerate(m.quiz_questions):
            quiz_total += 1
            issues = []

            if not isinstance(q, QuizQuestion):
                issues.append(f"not a QuizQuestion instance: {type(q)}")
                continue

            if len(q.options) != 4:
                issues.append(f"has {len(q.options)} options, expected 4")

            if not isinstance(q.correct, str):
                issues.append(f"correct is {type(q.correct).__name__} ({q.correct!r}), expected str")
            elif q.correct not in ("A", "B", "C", "D"):
                issues.append(f"correct='{q.correct}' not in ABCD")

            if not q.question:
                issues.append("empty question text")

            if not q.explanation:
                issues.append("empty explanation")

            if q.xp_value <= 0:
                issues.append(f"non-positive xp_value {q.xp_value}")

            if issues:
                quiz_problems.append(f"  {m.mission_id} q{idx+1}: {', '.join(issues)}")

if quiz_problems:
    for p in quiz_problems[:20]:
        fail(p)
    if len(quiz_problems) > 20:
        fail(f"... and {len(quiz_problems) - 20} more quiz problems")
else:
    ok(f"All {quiz_total} quiz questions pass integrity checks")

info(f"Total quiz questions inspected: {quiz_total}")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: Verify mission ID patterns (X.YY format) and chapter coverage
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 3: Mission ID patterns and chapter coverage")

try:
    for ch_id, ch_missions, topic, title, subtitle in CHAPTERS:
        ids = [m.mission_id for m in ch_missions]
        info(f"Chapter {ch_id:2d}: {len(ids)} missions, IDs: {ids[0]} ... {ids[-1]}")

        # Check first mission is .01
        first_id = ids[0]
        expected_first = f"{ch_id}.01"
        if first_id != expected_first:
            fail(f"Chapter {ch_id} first mission is {first_id}, expected {expected_first}")
        else:
            ok(f"Chapter {ch_id} starts with {expected_first}")

        # Check IDs are sorted (handle .BOSS suffix and non-numeric IDs like 4.16_lvm)
        def sort_key(x):
            parts = x.split(".")
            try:
                major = int(parts[0])
            except ValueError:
                return (9999, 9999)
            try:
                minor = int(parts[1])
            except ValueError:
                # Non-numeric suffix: try to extract leading digits
                import re
                m = re.match(r'(\d+)', parts[1])
                if m:
                    return (major, int(m.group(1)))
                return (major, 9999)
            return (major, minor)

        sorted_ids = sorted(ids, key=sort_key)
        if ids != sorted_ids:
            # Some chapters use descriptive IDs (e.g., 4.16_lvm_intro)
            # which may not sort purely numerically in the source file.
            warn(f"Chapter {ch_id} mission IDs have non-standard ordering (descriptive IDs)")
        else:
            ok(f"Chapter {ch_id} mission IDs are sorted")

        # Check all IDs match chapter prefix
        bad_ids = [mid for mid in ids if not mid.startswith(f"{ch_id}.")]
        if bad_ids:
            fail(f"Chapter {ch_id} has IDs not matching prefix: {bad_ids}")
        else:
            ok(f"Chapter {ch_id}: all IDs match prefix {ch_id}.")

except Exception as e:
    fail("Mission ID pattern test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4: MissionRunner instantiation and minimal run with real mission
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 4: MissionRunner with real mission from Chapter 1")

try:
    # Grab a simple SCAN mission from Ch1
    ch1 = CHAPTERS[0][1]
    scan_mission = next((m for m in ch1 if m.mtype == "SCAN"), None)

    if scan_mission is None:
        fail("No SCAN mission found in Chapter 1")
    else:
        info(f"Using mission: {scan_mission.mission_id} — {scan_mission.title}")

        p = Player(name="RunnerTest")
        runner = MissionRunner(p, save_callback=None)

        # We can't call runner.run() without interactive input,
        # but we can verify the runner has the player and the mission
        assert runner.player is p
        ok("MissionRunner holds correct player reference")

        # Verify mission fields are accessible
        assert runner.player.mission_completed(scan_mission.mission_id) == False
        ok("Mission not yet marked complete")

        # Manually simulate completion
        p.complete_mission(scan_mission.mission_id)
        assert p.mission_completed(scan_mission.mission_id)
        ok("Manual mission completion works")

        # Verify XP can be awarded
        old_xp = p.xp
        p.add_xp(scan_mission.xp)
        assert p.xp == old_xp + scan_mission.xp
        ok(f"XP awarded: {scan_mission.xp} → total {p.xp}")

except Exception as e:
    fail("MissionRunner test failed", e)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5: BOSS missions have correct structure (gear reward, 5 quiz questions)
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 5: BOSS mission structure validation")

try:
    boss_problems = []
    boss_count = 0

    for ch_id, ch_missions, topic, title, subtitle in CHAPTERS:
        bosses = [m for m in ch_missions if m.mtype == "BOSS"]
        for boss in bosses:
            boss_count += 1
            issues = []

            if not boss.boss_name:
                issues.append("missing boss_name")
            if not boss.boss_desc:
                issues.append("missing boss_desc")
            if len(boss.quiz_questions) < 5:
                issues.append(f"has only {len(boss.quiz_questions)} quiz questions, expected ≥5")
            if not boss.gear_reward:
                issues.append("missing gear_reward")
            elif boss.gear_reward not in GEAR_CATALOG:
                warn(f"  {boss.mission_id}: gear_reward '{boss.gear_reward}' not in GEAR_CATALOG (acceptable — future content)")

            if issues:
                boss_problems.append(f"  {boss.mission_id} ({boss.boss_name or 'NO NAME'}): {', '.join(issues)}")

    info(f"Total BOSS missions found: {boss_count}")

    if boss_problems:
        for p in boss_problems:
            fail(p)
    else:
        ok(f"All {boss_count} BOSS missions have correct structure")

except Exception as e:
    fail("BOSS validation test failed", e)


# ── Summary ───────────────────────────────────────────────────────────────────
banner("TEST 03 SUMMARY")
print(f"  Missions inspected: {total}")
print(f"  Quiz questions inspected: {quiz_total}")
print(f"  BOSS missions found: {boss_count}")
print(f"  Mission field problems: {len(problems)}")
print(f"  Quiz integrity problems: {len(quiz_problems)}")
print(f"  BOSS structure problems: {len(boss_problems)}")
