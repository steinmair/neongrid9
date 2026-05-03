"""
Smoke Test 04: Terminal Simulator
-----------------------------------
Validates command matching (exact, case-insensitive, prefix),
output generation for real commands, unknown command handling,
and the run_terminal() function signature.

How to run manually:
    cd /home/ande/neongrid9
    python3 smoke_tests/check_what_is_working/test_04_terminal_simulator.py

Critical because: The terminal simulator is the primary interactive
mechanic. If command matching is broken, players cannot complete
terminal-based missions regardless of their actual Linux knowledge.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine.terminal_sim import get_output, run_terminal, SIMULATED_OUTPUTS


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
# TEST 1: Exact command match for known commands
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 1: Exact command match")

test_commands = [
    "lspci",
    "lsusb",
    "lsusb -v",
    "uname -a",
    "cat /proc/cpuinfo",
    "dmesg",
    "lsblk",
    "fdisk -l",
    "runlevel",
    "service ssh status",
]

found_count = 0
for cmd in test_commands:
    found, output = get_output(cmd)
    if found:
        found_count += 1
        info(f"  '{cmd}' → {len(output)} chars output")
    else:
        fail(f"  '{cmd}' → NOT FOUND")

if found_count == len(test_commands):
    ok(f"All {len(test_commands)} commands matched exactly")
else:
    fail(f"Only {found_count}/{len(test_commands)} commands matched")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Case-insensitive matching
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 2: Case-insensitive matching")

case_tests = [
    ("LSPCI", "lspci"),
    ("LsUsb", "lsusb"),
    ("UNAME -A", "uname -a"),
    ("DMESG", "dmesg"),
]

matched = 0
for test_cmd, canonical in case_tests:
    found, output = get_output(test_cmd)
    if found:
        matched += 1
        info(f"  '{test_cmd}' → matched (canonical: '{canonical}')")
    else:
        fail(f"  '{test_cmd}' → NOT FOUND (expected match for '{canonical}')")

if matched == len(case_tests):
    ok(f"All {len(case_tests)} case variations matched")
else:
    fail(f"Only {matched}/{len(case_tests)} case variations matched")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: Prefix matching (command with extra flags)
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 3: Prefix matching")

prefix_tests = [
    ("lspci -vv", "lspci"),
    ("lsusb -vvv", "lsusb"),
    ("uname -r -m", "uname"),
    ("dmesg | grep error", "dmesg"),
]

matched = 0
for test_cmd, expected_base in prefix_tests:
    found, output = get_output(test_cmd)
    if found:
        matched += 1
        info(f"  '{test_cmd}' → matched via prefix (base: '{expected_base}')")
        # Verify the output mentions it's a prefix match
        if "Flags simuliert" in output or "Basis-Ausgabe" in output:
            info(f"    Output contains prefix-match indicator")
    else:
        fail(f"  '{test_cmd}' → NOT FOUND (expected prefix match for '{expected_base}')")

if matched == len(prefix_tests):
    ok(f"All {len(prefix_tests)} prefix variations matched")
else:
    fail(f"Only {matched}/{len(prefix_tests)} prefix variations matched")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 4: Unknown commands return proper error
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 4: Unknown command handling")

unknown_commands = [
    "notacommand",
    "foobar",
    "xyzzy",
    "zzzzz_unknown_cmd_12345",
]

all_rejected = True
for cmd in unknown_commands:
    found, output = get_output(cmd)
    if found:
        fail(f"  '{cmd}' → unexpectedly FOUND: {output[:60]}...")
        all_rejected = False
    else:
        if "command not found" in output or "bash:" in output:
            info(f"  '{cmd}' → correctly rejected: {output[:60]}")
        else:
            fail(f"  '{cmd}' → rejected but unexpected message: {output[:60]}")

if all_rejected:
    ok(f"All {len(unknown_commands)} unknown commands correctly rejected")
else:
    fail("Some unknown commands were incorrectly matched")


# ══════════════════════════════════════════════════════════════════════════════
# TEST 5: SIMULATED_OUTPUTS coverage and run_terminal() signature
# ══════════════════════════════════════════════════════════════════════════════
banner("TEST 5: SIMULATED_OUTPUTS dictionary coverage")

try:
    total_commands = len(SIMULATED_OUTPUTS)
    info(f"Total commands in SIMULATED_OUTPUTS: {total_commands}")
    assert total_commands > 100, f"Expected >100 commands, got {total_commands}"
    ok(f"SIMULATED_OUTPUTS has {total_commands} entries (>100)")

    # Verify all values are non-empty strings
    empty_values = [k for k, v in SIMULATED_OUTPUTS.items() if not v or not isinstance(v, str)]
    if empty_values:
        fail(f"{len(empty_values)} commands have empty or non-string values")
    else:
        ok("All SIMULATED_OUTPUTS values are non-empty strings")

    # Verify run_terminal() function exists and has correct signature
    import inspect
    sig = inspect.signature(run_terminal)
    params = list(sig.parameters.keys())
    info(f"run_terminal() parameters: {params}")

    expected_params = {"expected", "task_description", "hint_available", "hint_text", "max_attempts"}
    actual_params = set(params)
    if expected_params.issubset(actual_params):
        ok("run_terminal() has all expected parameters")
    else:
        missing = expected_params - actual_params
        fail(f"run_terminal() missing parameters: {missing}")

except Exception as e:
    fail("Coverage/signature test failed", e)


# ── Summary ───────────────────────────────────────────────────────────────────
banner("TEST 04 SUMMARY")
print("  Terminal simulator smoke test completed.")
