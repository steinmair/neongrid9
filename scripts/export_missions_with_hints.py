#!/usr/bin/env python3
"""
Load missions with generated hints, then export them back to Python files.
Uses a careful formatting approach to maintain code style.
"""

import sys
import os
sys.path.insert(0, '/home/ande/neongrid9')

from typing import List, Any
from missions import (
    ch01_hardware, ch02_boot, ch03_init, ch04_partitions,
    ch05_permissions, ch06_shell, ch07_processes, ch08_regex_vi,
    ch09_network, ch10_users, ch11_logging, ch12_packages,
    ch13_kernel, ch14_scripting, ch15_security, ch16_locale,
    ch17_shellenv, ch18_exam, ch19_ghost_processors,
    ch20_firewall_dominion, ch21_network_services, ch22_storage_advanced
)
from engine.mission_engine import Mission, QuizQuestion


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


def format_value(value: Any, indent: int = 2) -> str:
    """Format a Python value for code output."""
    ind = " " * indent

    if value is None:
        return "None"
    elif isinstance(value, bool):
        return str(value)
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        if '\n' in value:
            # Multi-line string
            lines = value.split('\n')
            if len(lines) <= 2 and all(len(l) < 70 for l in lines):
                return repr(value)
            # Use triple-quoted string
            escaped = value.replace('\\', '\\\\').replace('"""', r'\"\"\"')
            return f'(\n{ind}    """{escaped}"""\n{ind})'
        else:
            return repr(value)
    elif isinstance(value, list):
        if not value:
            return "[]"
        # Check if it's a list of strings
        if all(isinstance(v, str) for v in value):
            if len(value) <= 2 and all(len(v) < 50 for v in value):
                return f"[{', '.join(repr(v) for v in value)}]"
            # Multi-line list
            items = f",\n{ind}        ".join(repr(v) for v in value)
            return f"[\n{ind}        {items},\n{ind}    ]"
        elif all(isinstance(v, QuizQuestion) for v in value):
            # QuizQuestion objects
            items = f",\n{ind}    ".join(format_mission_obj(v, indent + 4) for v in value)
            return f"[\n{ind}        {items},\n{ind}    ]"
        else:
            return repr(value)
    else:
        return repr(value)


def format_mission_obj(obj: Any, indent: int = 2) -> str:
    """Format a Mission object for code output."""
    if isinstance(obj, QuizQuestion):
        ind = " " * indent
        lines = [f"QuizQuestion("]
        lines.append(f"{ind}    question  = {repr(obj.question)},")
        lines.append(f"{ind}    options   = {format_value(obj.options, indent)},")
        lines.append(f"{ind}    correct   = {repr(obj.correct)},")
        lines.append(f"{ind}    explanation = {repr(obj.explanation)},")
        if obj.xp_value:
            lines.append(f"{ind}    xp_value  = {obj.xp_value},")
        lines.append(f"{ind})")
        return "\n".join(lines)
    return repr(obj)


CHAPTERS = [
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


def generate_hints_for_chapter(module: Any, missions_attr: str) -> None:
    """Generate and add hints to missions in a chapter."""
    missions = getattr(module, missions_attr, [])
    for mission in missions:
        if not mission.hints and mission.expected_commands:
            mission.hints = HintGenerator.build_hints(
                mission.expected_commands,
                mission.task_description
            )


def main():
    """Generate hints for all chapters."""
    print("Generating hints for all chapters...")
    total = 0

    for module_name, module, missions_attr in CHAPTERS:
        generate_hints_for_chapter(module, missions_attr)
        missions = getattr(module, missions_attr, [])
        count = sum(1 for m in missions if m.hints)
        total += count
        print(f"✓ {module_name}: {count} missions with hints")

    print(f"\nTotal: {total}/501 missions have hints")
    print("\nNote: Hints are now in memory. To persist, manually commit mission files or use Edit tool.")


if __name__ == "__main__":
    main()
