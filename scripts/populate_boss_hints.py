#!/usr/bin/env python3
"""
Populate hints for all 22 boss missions across all chapters.
Uses line-by-line modification to preserve formatting.
"""

import os
import re
from typing import List, Optional

def generate_hints(cmd: str) -> List[str]:
    """Generate 3-tier hints for a command."""
    if not cmd:
        return []

    parts = cmd.split()
    main_cmd = parts[0]

    # Tier 1: Conceptual
    if "|" in cmd or "&&" in cmd:
        hint1 = f"Du brauchst einen Befehl, der mit '{main_cmd}' beginnt und mehrere Operationen kombiniert."
    elif "/" in cmd:
        path = next((p for p in parts if "/" in p), "")
        hint1 = f"Das Verzeichnis oder die Datei befinden sich unter '{path}'. Der Befehl beginnt mit '{main_cmd}'."
    elif any(x in cmd.lower() for x in ["-l", "-a", "-v"]):
        hint1 = f"Ein Auflistungsbefehl wie '{main_cmd}' wird benötigt."
    else:
        hint1 = f"Der Befehl '{main_cmd}' ist der richtige Ansatz für diese Boss-Phase."

    # Tier 2: Structure
    if len(parts) > 1:
        hint2 = f"Versuche: {' '.join(parts[:min(3, len(parts))])}"
        if len(parts) > 3:
            hint2 += " ..."
    else:
        hint2 = f"Der Befehl selbst ist: {main_cmd}"

    # Tier 3: Complete answer
    hint3 = f"Der vollständige Befehl: {cmd}"

    return [hint1, hint2, hint3]


def add_hints_to_file(filepath: str) -> bool:
    """Add hints to boss mission in file if missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    i = 0

    while i < len(lines):
        # Look for "mtype       = \"BOSS\"" or "mtype='BOSS'"
        if 'mtype' in lines[i] and 'BOSS' in lines[i]:
            # Found a boss mission, now find expected_commands
            j = i + 1
            while j < len(lines) and j < i + 100:  # Reasonable search distance
                if 'expected_commands' in lines[j]:
                    # Found expected_commands line
                    # Check if next field is "hints"
                    k = j + 1
                    while k < len(lines) and (lines[k].strip().startswith('"') or
                                            lines[k].strip().startswith("'")):
                        k += 1  # Skip multi-line expected_commands

                    # Check the next non-empty line
                    next_line = lines[k].strip() if k < len(lines) else ""

                    if "hints" not in next_line:
                        # Need to add hints
                        # Extract command from expected_commands
                        cmd_match = re.search(r'"([^"]*(?:\\.[^"]*)*)"', lines[j])
                        if cmd_match:
                            cmd = cmd_match.group(1)
                            hints = generate_hints(cmd)

                            # Generate hints lines
                            indent = len(lines[j]) - len(lines[j].lstrip())
                            indent_str = lines[j][:indent]

                            hints_lines = [
                                f"{indent_str}hints = [\n",
                                f"{indent_str}    \"{hints[0]}\",\n",
                                f"{indent_str}    \"{hints[1]}\",\n",
                                f"{indent_str}    \"{hints[2]}\",\n",
                                f"{indent_str}],\n"
                            ]

                            # Insert after expected_commands block
                            lines[k:k] = hints_lines
                            modified = True

                    break
                j += 1

        i += 1

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True

    return False


def main():
    """Process all mission files."""
    mission_files = [
        "missions/ch01_hardware.py",
        "missions/ch02_boot.py",
        "missions/ch03_init.py",
        "missions/ch04_partitions.py",
        "missions/ch05_permissions.py",
        "missions/ch06_shell.py",
        "missions/ch07_processes.py",
        "missions/ch08_regex_vi.py",
        "missions/ch09_network.py",
        "missions/ch10_users.py",
        "missions/ch11_logging.py",
        "missions/ch12_packages.py",
        "missions/ch13_kernel.py",
        "missions/ch14_scripting.py",
        "missions/ch15_security.py",
        "missions/ch16_locale.py",
        "missions/ch17_shellenv.py",
        "missions/ch18_exam.py",
        "missions/ch19_ghost_processors.py",
        "missions/ch20_firewall_dominion.py",
        "missions/ch21_network_services.py",
        "missions/ch22_storage_advanced.py",
    ]

    processed = 0
    for filepath in mission_files:
        if os.path.exists(filepath):
            if add_hints_to_file(filepath):
                filename = os.path.basename(filepath)
                print(f"✓ {filename}")
                processed += 1
            else:
                filename = os.path.basename(filepath)
                print(f"- {filename}")

    print(f"\nAdded hints to {processed} files")


if __name__ == "__main__":
    main()
