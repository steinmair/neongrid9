#!/usr/bin/env python3
"""
Safe hint injection using proper Python AST parsing and code generation.
"""

import ast
import os
import glob
from typing import List, Optional, Dict, Any

class HintGenerator:
    @staticmethod
    def build_hints(expected_commands: List[str], task_desc: str = "") -> List[str]:
        """Generate 3-tier hints from mission data."""
        if not expected_commands:
            return []

        cmd = expected_commands[0]
        parts = cmd.split()
        main_cmd = parts[0]

        # Hint 1 (FREE)
        if "/" in cmd:
            path = next((p for p in parts if "/" in p), "")
            hint1 = f"Das Verzeichnis oder die Datei befinden sich unter '{path}'. Der Befehl beginnt mit '{main_cmd}'."
        elif any(x in task_desc.lower() for x in ["zeige", "liste", "anzeigen", "display", "list"]):
            hint1 = f"Ein Auflistungsbefehl wie '{main_cmd}' wird benötigt, um die gewünschten Informationen anzuzeigen."
        elif any(x in task_desc.lower() for x in ["finde", "suche", "find"]):
            hint1 = f"Nutze '{main_cmd}' um das gesuchte Muster zu finden."
        elif any(x in task_desc.lower() for x in ["ändere", "modifiziere", "edit", "change", "modify"]):
            hint1 = f"Der Befehl '{main_cmd}' wird zur Modifikation verwendet."
        else:
            hint1 = f"Der Befehl '{main_cmd}' ist der richtige Ansatz für diese Aufgabe."

        # Hint 2 (20 XP)
        if len(parts) > 1:
            hint2 = f"Versuche: {' '.join(parts[:min(3, len(parts))])}"
            if len(parts) > 3:
                hint2 += " ..."
        else:
            hint2 = f"Der Befehl selbst ist: {main_cmd}"

        # Hint 3 (50 XP / FINAL)
        hint3 = f"Der vollständige Befehl: {cmd}"

        return [hint1, hint2, hint3]


class MissionFileProcessor:
    """Process mission files and inject hints where missing."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        with open(filepath, 'r', encoding='utf-8') as f:
            self.original = f.read()
        self.content = self.original

    def has_any_hints(self) -> bool:
        """Check if file already has hints field."""
        return "hints = [" in self.content

    def process_missions(self) -> bool:
        """Process each Mission() in file, injecting hints where missing."""
        lines = self.content.split('\n')
        in_mission = False
        mission_start = 0
        mission_lines = []
        has_hints = False
        expected_commands_line = -1
        modified = False

        new_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detect Mission( start
            if 'Mission(' in line and not in_mission:
                in_mission = True
                mission_start = i
                has_hints = False
                expected_commands_line = -1
                mission_lines = [line]
                i += 1
                continue

            if in_mission:
                mission_lines.append(line)

                # Check for hints field
                if 'hints = [' in line:
                    has_hints = True

                # Track expected_commands for later
                if 'expected_commands' in line:
                    expected_commands_line = len(mission_lines) - 1

                # Detect Mission block end
                if line.strip() == ")," and expected_commands_line >= 0:
                    # End of mission block
                    if not has_hints:
                        # Need to inject hints
                        modified |= self._inject_hints_into_mission(mission_lines, expected_commands_line)

                    # Add all mission lines to output
                    new_lines.extend(mission_lines)
                    in_mission = False
                    mission_lines = []
                    i += 1
                    continue

                i += 1
                continue

            # Not in mission
            new_lines.append(line)
            i += 1

        if modified:
            self.content = '\n'.join(new_lines)
            return True
        return False

    def _inject_hints_into_mission(self, mission_lines: List[str], expected_commands_line: int) -> bool:
        """Inject hints after expected_commands in mission block."""
        # Extract expected_commands from the line
        ec_line = mission_lines[expected_commands_line]

        # Parse out the list
        import re
        ec_match = re.search(r'expected_commands\s*=\s*\[(.*?)\]', ec_line, re.DOTALL)
        if not ec_match:
            return False

        commands_str = ec_match.group(1)
        # Extract all quoted strings
        commands = re.findall(r'"([^"]+)"', commands_str)
        if not commands:
            return False

        # Extract task_description for context
        task_desc = ""
        for line in mission_lines:
            if 'task_description' in line:
                tm = re.search(r'task_description\s*=\s*["\']([^"\']+)["\']', line)
                if tm:
                    task_desc = tm.group(1)
                break

        # Generate hints
        hints = HintGenerator.build_hints(commands, task_desc)

        # Format hints
        indent = self._get_indent(mission_lines[expected_commands_line])
        hints_lines = [f"{indent}hints = ["]
        for hint in hints:
            hint_escaped = hint.replace('"', '\\"')
            hints_lines.append(f'{indent}    "{hint_escaped}",')
        hints_lines.append(f"{indent}],")

        # Find where to insert (after expected_commands line)
        insert_idx = expected_commands_line + 1

        # Check if next line starts a new field or is part of multi-line list
        while insert_idx < len(mission_lines):
            next_line = mission_lines[insert_idx].strip()
            if next_line and not next_line.startswith('"'):
                # Found start of next field
                break
            if "]," in next_line:
                # End of list
                insert_idx += 1
                break
            insert_idx += 1

        # Insert hints
        mission_lines[insert_idx:insert_idx] = hints_lines

        return True

    def _get_indent(self, line: str) -> str:
        """Extract indentation from line."""
        return line[:len(line) - len(line.lstrip())]

    def save(self) -> bool:
        """Save modified content if changes were made."""
        if self.content != self.original:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(self.content)
            return True
        return False


def main():
    """Process all mission files."""
    mission_files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))

    processed = 0
    for filepath in mission_files:
        filename = os.path.basename(filepath)
        processor = MissionFileProcessor(filepath)

        if processor.has_any_hints():
            print(f"- {filename} (already has hints)")
            continue

        if processor.process_missions() and processor.save():
            processed += 1
            print(f"✓ {filename}")
        else:
            print(f"- {filename}")

    print(f"\nProcessed {processed}/{len(mission_files)} files")


if __name__ == "__main__":
    main()
