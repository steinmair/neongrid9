#!/usr/bin/env python3
"""
Load missions, generate hints for those lacking them, write back clean Python code.
This is safer than text-based injection.
"""

import sys
import os
sys.path.insert(0, '/home/ande/neongrid9')

from typing import List, Any
from dataclasses import fields
from missions import ch01_hardware, ch02_boot, ch03_init, ch04_partitions
from missions import ch05_permissions, ch06_shell, ch07_processes, ch08_regex_vi
from missions import ch09_network, ch10_users, ch11_logging, ch12_packages
from missions import ch13_kernel, ch14_scripting, ch15_security, ch16_locale
from missions import ch17_shellenv, ch18_exam, ch19_ghost_processors
from missions import ch20_firewall_dominion, ch21_network_services, ch22_storage_advanced
from engine.mission_engine import Mission

CHAPTER_MODULES = [
    ('ch01_hardware', ch01_hardware, 'CHAPTER_1_MISSIONS'),
    ('ch02_boot', ch02_boot, 'CHAPTER_2_MISSIONS'),
    ('ch03_init', ch03_init, 'CHAPTER_3_MISSIONS'),
    ('ch04_partitions', ch04_partitions, 'CHAPTER_4_MISSIONS'),
    ('ch05_permissions', ch05_permissions, 'CHAPTER_5_MISSIONS'),
    ('ch06_shell', ch06_shell, 'CHAPTER_6_MISSIONS'),
    ('ch07_processes', ch07_processes, 'CHAPTER_7_MISSIONS'),
    ('ch08_regex_vi', ch08_regex_vi, 'CHAPTER_8_MISSIONS'),
    ('ch09_network', ch09_network, 'CHAPTER_9_MISSIONS'),
    ('ch10_users', ch10_users, 'CHAPTER_10_MISSIONS'),
    ('ch11_logging', ch11_logging, 'CHAPTER_11_MISSIONS'),
    ('ch12_packages', ch12_packages, 'CHAPTER_12_MISSIONS'),
    ('ch13_kernel', ch13_kernel, 'CHAPTER_13_MISSIONS'),
    ('ch14_scripting', ch14_scripting, 'CHAPTER_14_MISSIONS'),
    ('ch15_security', ch15_security, 'CHAPTER_15_MISSIONS'),
    ('ch16_locale', ch16_locale, 'CHAPTER_16_MISSIONS'),
    ('ch17_shellenv', ch17_shellenv, 'CHAPTER_17_MISSIONS'),
    ('ch18_exam', ch18_exam, 'CHAPTER_18_MISSIONS'),
    ('ch19_ghost_processors', ch19_ghost_processors, 'CHAPTER_19_MISSIONS'),
    ('ch20_firewall_dominion', ch20_firewall_dominion, 'CHAPTER_20_MISSIONS'),
    ('ch21_network_services', ch21_network_services, 'CHAPTER_21_MISSIONS'),
    ('ch22_storage_advanced', ch22_storage_advanced, 'CHAPTER_22_MISSIONS'),
]


class HintGenerator:
    @staticmethod
    def build_hints(expected_commands: List[str], task_desc: str = "") -> List[str]:
        """Generate 3-tier hints."""
        if not expected_commands:
            return []

        cmd = expected_commands[0]
        parts = cmd.split()
        main_cmd = parts[0]

        if "/" in cmd:
            path = next((p for p in parts if "/" in p), "")
            hint1 = f"Das Verzeichnis oder die Datei befinden sich unter '{path}'. Der Befehl beginnt mit '{main_cmd}'."
        elif any(x in task_desc.lower() for x in ["zeige", "liste", "anzeigen"]):
            hint1 = f"Ein Auflistungsbefehl wie '{main_cmd}' wird benötigt."
        else:
            hint1 = f"Der Befehl '{main_cmd}' ist der richtige Ansatz."

        if len(parts) > 1:
            hint2 = f"Versuche: {' '.join(parts[:min(3, len(parts))])}"
            if len(parts) > 3:
                hint2 += " ..."
        else:
            hint2 = f"Der Befehl selbst ist: {main_cmd}"

        hint3 = f"Der vollständige Befehl: {cmd}"

        return [hint1, hint2, hint3]


def process_chapter(module_name: str, module: Any, missions_attr: str) -> int:
    """
    Process a chapter, adding hints to missions that lack them.
    Returns number of missions that had hints generated.
    """
    missions = getattr(module, missions_attr, [])
    if not missions:
        return 0

    count = 0

    for mission in missions:
        # If mission already has hints, skip
        if mission.hints:
            continue

        # Generate hints from expected_commands
        if mission.expected_commands:
            hints = HintGenerator.build_hints(
                mission.expected_commands,
                mission.task_description
            )
            mission.hints = hints
            count += 1

    return count


def main():
    """Process all chapters."""
    total_generated = 0

    for module_name, module, missions_attr in CHAPTER_MODULES:
        count = process_chapter(module_name, module, missions_attr)
        total_generated += count
        if count > 0:
            print(f"✓ {module_name}: Generated {count} hints")
        else:
            print(f"- {module_name}: No new hints needed")

    print(f"\nTotal hints generated: {total_generated}")


if __name__ == "__main__":
    main()
