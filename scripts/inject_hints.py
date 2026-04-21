#!/usr/bin/env python3
"""
Scan all mission files for missions lacking hints field, generate and inject 3-tier hints.
"""

import re
import os
import glob

def build_hints(expected_commands: list, task_desc: str, explanation: str = "") -> list:
    """Generate 3-tier hints from mission components."""
    if not expected_commands:
        return []

    cmd = expected_commands[0] if isinstance(expected_commands, list) else str(expected_commands)
    parts = cmd.split()
    main_cmd = parts[0]

    # Hint 1 (FREE): Conceptual direction
    hint1 = ""
    if "/" in cmd:
        # File path command
        path = next((p for p in parts if "/" in p), "")
        if path:
            hint1 = f"Das Verzeichnis oder die Datei befinden sich unter '{path}'. Beginne mit '{main_cmd}'."
        else:
            hint1 = f"Der Befehl '{main_cmd}' wird mit einem Pfad-Argument benötigt."
    elif any(x in task_desc.lower() for x in ["zeige", "liste", "anzeigen", "display"]):
        hint1 = f"Der Befehl '{main_cmd}' zeigt die Information an, die du brauchst."
    elif any(x in task_desc.lower() for x in ["finde", "suche", "grep"]):
        hint1 = f"Ein Such- oder Filter-Befehl wie '{main_cmd}' wird hier benötigt."
    elif any(x in task_desc.lower() for x in ["ändere", "modifiziere", "edit"]):
        hint1 = f"Nutze '{main_cmd}' um die Änderung durchzuführen."
    else:
        hint1 = f"Der erste Befehl, den du brauchst, beginnt mit '{main_cmd}'."

    # Hint 2 (20 XP): More specific
    flags = [p for p in parts[1:] if p.startswith('-')]
    args = [p for p in parts[1:] if not p.startswith('-')]

    if len(parts) > 1:
        hint2 = f"Versuche: {' '.join(parts[:min(3, len(parts))])}"
        if len(parts) > 3:
            hint2 += " ..."
    else:
        hint2 = f"Der Befehl ist einfach: {main_cmd}"

    # Hint 3 (50 XP / FINAL): Complete answer
    hint3 = f"Der vollständige Befehl: {cmd}"

    return [hint1, hint2, hint3]


def process_mission_file(filepath: str) -> bool:
    """
    Process a mission file, adding hints field to missions that lack it.
    Returns True if changes were made.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has any missions already with hints field
    if "hints = [" in content:
        # File already processed, skip
        return False

    # Find all Mission(...) blocks
    mission_pattern = r'Mission\(([\s\S]*?)\n    \),'
    matches = list(re.finditer(mission_pattern, content))

    if not matches:
        return False

    changes_made = False

    # Process each mission block
    for match in reversed(matches):  # Reverse to maintain indices
        mission_block = match.group(1)

        # Skip if hints already present
        if "hints = [" in mission_block:
            continue

        # Extract expected_commands
        cmd_match = re.search(r'expected_commands\s*=\s*\[(.*?)\]', mission_block)
        if not cmd_match:
            continue

        # Parse commands list
        cmd_str = cmd_match.group(1).strip()
        commands = re.findall(r'"([^"]+)"', cmd_str)
        if not commands:
            continue

        # Extract task_description for context
        task_match = re.search(r'task_description\s*=\s*["\']([^"\']+)["\']', mission_block)
        task_desc = task_match.group(1) if task_match else ""

        # Extract explanation for additional context
        exp_match = re.search(r'explanation\s*=\s*\(?(.*?)\)?,\s*(?:ascii_art|syntax)', mission_block, re.DOTALL)
        explanation = exp_match.group(1) if exp_match else ""

        # Generate hints
        hints = build_hints(commands, task_desc, explanation)

        # Find insertion point (after expected_commands line)
        insertion_match = re.search(r'expected_commands\s*=\s*\[.*?\],', mission_block)
        if insertion_match:
            insert_pos = match.start() + insertion_match.end()

            # Format hints for insertion
            hints_str = f"\n        hints = [\n"
            for hint in hints:
                # Escape quotes in hints
                hint_escaped = hint.replace('"', '\\"')
                hints_str += f'            "{hint_escaped}",\n'
            hints_str += "        ],"

            # Insert hints
            content = content[:insert_pos] + hints_str + content[insert_pos:]
            changes_made = True

    if changes_made:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    """Process all mission files."""
    mission_files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))

    total = len(mission_files)
    processed = 0

    for filepath in mission_files:
        chapter = os.path.basename(filepath)
        if process_mission_file(filepath):
            processed += 1
            print(f"✓ {chapter}")
        else:
            print(f"- {chapter}")

    print(f"\nProcessed {processed}/{total} files")


if __name__ == "__main__":
    main()
