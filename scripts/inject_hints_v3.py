#!/usr/bin/env python3
"""
Safe hint injection with proper string escaping for special characters.
"""

import os
import glob
import re
from typing import List, Tuple

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


def parse_expected_commands(ec_str: str) -> List[str]:
    """Parse expected_commands list from string."""
    commands = []
    # Extract all quoted strings
    matches = re.findall(r'"([^"]*(?:\\.[^"]*)*)"', ec_str)
    return matches


def find_mission_blocks(content: str) -> List[Tuple[int, int]]:
    """Find start and end positions of all Mission(...) blocks."""
    blocks = []
    depth = 0
    start = -1

    for i, char in enumerate(content):
        if i + 7 <= len(content) and content[i:i+8] == "Mission(":
            start = i
            depth = 1
            i += 8
            continue

        if start >= 0:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0 and i + 1 < len(content) and content[i+1] == ',':
                    blocks.append((start, i + 2))
                    start = -1

    return blocks


def extract_commands_from_block(block: str) -> List[str]:
    """Extract expected_commands from a mission block."""
    ec_match = re.search(r'expected_commands\s*=\s*\[(.*?)\]', block, re.DOTALL)
    if not ec_match:
        return []
    return parse_expected_commands(ec_match.group(1))


def extract_task_desc_from_block(block: str) -> str:
    """Extract task_description from mission block."""
    tm = re.search(r'task_description\s*=\s*["\']([^"\']+)["\']', block)
    return tm.group(1) if tm else ""


def process_mission_file(filepath: str) -> bool:
    """Process a mission file, injecting hints where missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if file already has hints
    if "hints = [" in content:
        return False

    blocks = find_mission_blocks(content)
    if not blocks:
        return False

    modified = False
    offset = 0

    for start, end in blocks:
        block = content[start + offset:end + offset]

        # Skip if already has hints
        if "hints = [" in block:
            continue

        commands = extract_commands_from_block(block)
        if not commands:
            continue

        task_desc = extract_task_desc_from_block(block)
        hints = HintGenerator.build_hints(commands, task_desc)

        # Find insertion point (after expected_commands line)
        ec_match = re.search(r'expected_commands\s*=\s*\[(.*?)\]', block, re.DOTALL)
        if not ec_match:
            continue

        ec_end = block.find(']', ec_match.start()) + 1

        # Get indentation
        indent_match = re.search(r'(\s*)expected_commands', block)
        indent = indent_match.group(1) if indent_match else "        "

        # Format hints using repr for safe escaping
        hints_str = f",\n{indent}hints = [\n"
        for hint in hints:
            # Use repr to safely escape the string, then strip quotes
            safe_hint = repr(hint)[1:-1]  # Remove outer quotes from repr
            hints_str += f'{indent}    "{safe_hint}",\n'
        hints_str += f"{indent}]"

        # Insert hints
        insertion_point = start + offset + ec_end
        new_content = content[:insertion_point] + hints_str + content[insertion_point:]

        # Update offset for subsequent blocks
        offset += len(hints_str)

        content = new_content
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    """Process all mission files."""
    mission_files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))

    processed = 0
    skipped = 0

    for filepath in mission_files:
        filename = os.path.basename(filepath)

        # Quick check if already processed
        with open(filepath, 'r') as f:
            if "hints = [" in f.read():
                print(f"- {filename} (already processed)")
                skipped += 1
                continue

        if process_mission_file(filepath):
            processed += 1
            print(f"✓ {filename}")
        else:
            print(f"! {filename} (no missions to process)")

    print(f"\nProcessed {processed}/{len(mission_files)} files")


if __name__ == "__main__":
    main()
