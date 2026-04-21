#!/usr/bin/env python3
"""
Simplest possible approach: Find expected_commands patterns, insert hints after.
"""

import os
import glob
import re
from typing import List

class HintGenerator:
    @staticmethod
    def build_hints(cmd: str, task_desc: str = "") -> List[str]:
        """Generate 3-tier hints from a single command."""
        if not cmd:
            return []

        parts = cmd.split()
        main_cmd = parts[0]

        # Hint 1: Direction
        if "/" in cmd:
            path = next((p for p in parts if "/" in p), "")
            hint1 = f"Das Verzeichnis oder die Datei befinden sich unter '{path}'. Der Befehl beginnt mit '{main_cmd}'."
        elif any(x in task_desc.lower() for x in ["zeige", "liste", "anzeigen"]):
            hint1 = f"Ein Auflistungsbefehl wie '{main_cmd}' wird benötigt."
        else:
            hint1 = f"Der Befehl '{main_cmd}' ist der richtige Ansatz."

        # Hint 2: Structure
        if len(parts) > 1:
            hint2 = f"Versuche: {' '.join(parts[:min(3, len(parts))])}"
            if len(parts) > 3:
                hint2 += " ..."
        else:
            hint2 = f"Der Befehl selbst ist: {main_cmd}"

        # Hint 3: Answer
        hint3 = f"Der vollständige Befehl: {cmd}"

        return [hint1, hint2, hint3]


def process_file(filepath: str) -> bool:
    """Add hints to a mission file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has hints
    if "hints = [" in content:
        return False

    lines = content.split('\n')
    new_lines = []
    modified = False
    i = 0

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Check for expected_commands line
        if 'expected_commands' in line and '=' in line:
            # Check if next line closes the list
            match = re.match(r'(\s*)expected_commands\s*=\s*\[(.*)\]\s*[,]?\s*$', line)
            if match:
                indent = match.group(1)
                cmd_str = match.group(2).strip()

                # Single-line list - extract command
                commands = re.findall(r'"([^"]*(?:\\.[^"]*)*)"', cmd_str)
                if commands:
                    # Generate hints
                    hints = HintGenerator.build_hints(commands[0], "")

                    # Add hints after this line
                    hints_lines = [f'{indent}hints = [']
                    for hint in hints:
                        safe_hint = repr(hint)[1:-1]
                        hints_lines.append(f'{indent}    "{safe_hint}",')
                    hints_lines.append(f'{indent}],')

                    # Insert hints (skip the comma from expected_commands)
                    new_lines[-1] = line.rstrip(',').rstrip()
                    new_lines.append(',')
                    new_lines.extend(hints_lines)
                    modified = True

            else:
                # Multi-line list - find where it ends
                cmd_part = line.split('[')[1] if '[' in line else ''
                close_idx = i + 1

                # Find closing bracket
                while close_idx < len(lines) and ']' not in lines[close_idx]:
                    close_idx += 1

                if close_idx < len(lines):
                    # Collect all command lines
                    cmd_lines = [cmd_part]
                    for j in range(i + 1, close_idx + 1):
                        cmd_lines.append(lines[j].strip())

                    cmd_str = ' '.join(cmd_lines).replace(']', '').strip()
                    commands = re.findall(r'"([^"]*(?:\\.[^"]*)*)"', cmd_str)

                    if commands:
                        indent = re.match(r'^(\s*)', line).group(1)
                        hints = HintGenerator.build_hints(commands[0], "")

                        # Build hints section
                        hints_lines = [f'{indent}hints = [']
                        for hint in hints:
                            safe_hint = repr(hint)[1:-1]
                            hints_lines.append(f'{indent}    "{safe_hint}",')
                        hints_lines.append(f'{indent}],')

                        # Replace the closing bracket line with hints
                        new_lines.extend(lines[i+1:close_idx])
                        new_lines.extend(hints_lines)

                        i = close_idx
                        modified = True

        i += 1

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        return True

    return False


def main():
    """Process all mission files."""
    mission_files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))

    processed = 0

    for filepath in mission_files:
        filename = os.path.basename(filepath)

        # Check if already processed
        with open(filepath, 'r') as f:
            if "hints = [" in f.read():
                print(f"- {filename}")
                continue

        if process_file(filepath):
            processed += 1
            print(f"✓ {filename}")
        else:
            print(f"! {filename}")

    print(f"\nProcessed {processed} files")


if __name__ == "__main__":
    main()
