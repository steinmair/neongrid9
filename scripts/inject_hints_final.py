#!/usr/bin/env python3
"""
Final version: Simple, robust hint injection for all missions.
Uses straightforward regex matching instead of complex parsing.
"""

import os
import glob
import re
from typing import List

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


def process_mission_file(filepath: str) -> bool:
    """
    Process a mission file, injecting hints where missing.
    Uses a simpler approach: regex to find each mission and check for hints.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if file already has hints
    if "hints = [" in content:
        return False

    modified = False

    # Find all Mission(...), blocks using multiline regex
    # This pattern matches Mission( followed by content ending with ),
    pattern = r'(Mission\([^)]*?expected_commands\s*=\s*\[([^\]]*?)\])'

    def replace_fn(match):
        nonlocal modified
        full_match = match.group(1)

        # Skip if already has hints
        if "hints = [" in full_match:
            return full_match

        # Extract commands
        commands_str = match.group(2)
        commands = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', commands_str)

        if not commands:
            return full_match

        # Try to get task_description from the block
        # Look backwards from the matched position to find task_description
        start_pos = match.start()
        block_start = content.rfind('Mission(', 0, start_pos)
        block_context = content[block_start:match.end() + 200]

        task_match = re.search(r'task_description\s*=\s*["\']([^"\']+)["\']', block_context)
        task_desc = task_match.group(1) if task_match else ""

        # Generate hints
        hints = HintGenerator.build_hints(commands, task_desc)

        # Format hints
        hints_str = ",\n        hints = [\n"
        for hint in hints:
            # Use repr to safely escape, then extract just the body
            safe_hint = repr(hint)[1:-1]
            hints_str += f'            "{safe_hint}",\n'
        hints_str += "        ]"

        modified = True
        return full_match + hints_str

    # Apply replacement
    new_content = re.sub(pattern, replace_fn, content, flags=re.DOTALL)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
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
            print(f"! {filename}")

    print(f"\nProcessed {processed} files, skipped {skipped}")


if __name__ == "__main__":
    main()
