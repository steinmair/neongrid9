#!/usr/bin/env python3
"""
Surgical hint injection: Find expected_commands, check if hints exist,
insert 3-tier hints with minimal formatting changes.
"""

import os
import glob
import re
from typing import List, Optional, Tuple


class HintGenerator:
    @staticmethod
    def build_hints(cmd: str, task_desc: str = "") -> List[str]:
        """Generate 3-tier hints."""
        if not cmd:
            return []

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


def extract_mission_blocks(content: str) -> List[Tuple[int, int, str]]:
    """Find all Mission(...) blocks and extract their content.
    Returns list of (start_pos, end_pos, block_content)
    """
    blocks = []
    i = 0
    while i < len(content):
        # Find "Mission("
        pos = content.find("Mission(", i)
        if pos == -1:
            break

        # Find matching closing parenthesis
        depth = 1
        j = pos + 8
        while j < len(content) and depth > 0:
            if content[j] == '(':
                depth += 1
            elif content[j] == ')':
                depth -= 1
            j += 1

        if depth == 0:
            block = content[pos:j]
            blocks.append((pos, j, block))

        i = j

    return blocks


def process_single_mission(block: str) -> Optional[str]:
    """Process a single mission block, adding hints if missing.
    Returns modified block or None if no changes needed.
    """
    # Skip if already has hints
    if "hints = [" in block:
        return None

    # Find expected_commands
    ec_match = re.search(r'expected_commands\s*=\s*\[([^\]]*)\]', block, re.DOTALL)
    if not ec_match:
        return None

    # Extract first command
    cmd_str = ec_match.group(1).strip()
    cmd_match = re.search(r'"([^"]*(?:\\.[^"]*)*)"', cmd_str)
    if not cmd_match:
        return None

    cmd = cmd_match.group(1)

    # Get task description for context
    task_match = re.search(r'task_description\s*=\s*["\']([^"\']+)["\']', block)
    task_desc = task_match.group(1) if task_match else ""

    # Generate hints
    hints = HintGenerator.build_hints(cmd, task_desc)

    # Build hints string
    hints_str = "hints = [\n            "
    hints_str += ',\n            '.join(f'"{h}"' for h in hints)
    hints_str += ",\n        ],"

    # Find insertion point (after expected_commands closing bracket and comma)
    ec_end = ec_match.end()
    insert_pos = block.find(",", ec_end)
    if insert_pos == -1:
        return None
    insert_pos += 1

    # Insert hints
    new_block = block[:insert_pos] + f"\n        {hints_str}" + block[insert_pos:]

    return new_block


def process_file(filepath: str) -> bool:
    """Process a mission file, adding hints where missing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Skip if already has hints
    if "hints = [" in original_content:
        return False

    # Find all mission blocks
    blocks = extract_mission_blocks(original_content)
    if not blocks:
        return False

    modified = False
    offset = 0
    new_content = original_content

    # Process blocks in reverse order to maintain positions
    for start, end, block in reversed(blocks):
        new_block = process_single_mission(block)
        if new_block:
            # Calculate adjusted positions
            adj_start = start + offset
            adj_end = end + offset

            # Replace in content
            new_content = new_content[:adj_start] + new_block + new_content[adj_end:]

            # Update offset
            offset += len(new_block) - (end - start)
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False


def main():
    """Process all mission files."""
    mission_files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))

    processed = 0
    for filepath in mission_files:
        filename = os.path.basename(filepath)

        # Quick check
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
