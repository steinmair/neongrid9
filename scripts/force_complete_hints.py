#!/usr/bin/env python3
"""
Force completion of all hints by reprocessing all mission files.
Accept reformatting as cost for 100% coverage.
"""

import ast
import sys
import os
import glob

sys.path.insert(0, '/home/ande/neongrid9')


class HintGenerator:
    @staticmethod
    def build_hints(cmd, task_desc=""):
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


class MissionPatcher(ast.NodeTransformer):
    """Add hints to all missions that lack them."""

    def __init__(self):
        self.modified = False
        self.hint_count = 0

    def visit_Call(self, node):
        self.generic_visit(node)
        if not (isinstance(node.func, ast.Name) and node.func.id == 'Mission'):
            return node

        # Check for existing hints
        has_hints = any(kw.arg == 'hints' for kw in node.keywords)
        if has_hints:
            return node

        # Find expected_commands
        expected_commands = None
        task_description = ""
        ec_idx = -1

        for i, keyword in enumerate(node.keywords):
            if keyword.arg == 'expected_commands':
                expected_commands = keyword.value
                ec_idx = i
            elif keyword.arg == 'task_description':
                if isinstance(keyword.value, ast.Constant):
                    task_description = keyword.value.value

        if expected_commands and isinstance(expected_commands, ast.List) and ec_idx >= 0:
            commands = []
            for elt in expected_commands.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    commands.append(elt.value)

            if commands:
                hints = HintGenerator.build_hints(commands[0], task_description)
                hints_elts = [ast.Constant(value=h) for h in hints]
                hints_list = ast.List(elts=hints_elts, ctx=ast.Load())
                hints_keyword = ast.keyword(arg='hints', value=hints_list)

                node.keywords.insert(ec_idx + 1, hints_keyword)
                self.modified = True
                self.hint_count += 1

        return node


def process_file(filepath):
    """Process a file, adding hints to all missions without them."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"  Syntax error: {e}")
        return 0

    patcher = MissionPatcher()
    patcher.visit(tree)

    if not patcher.modified:
        return 0

    try:
        new_content = ast.unparse(tree)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return patcher.hint_count
    except Exception as e:
        print(f"  Unparse error: {e}")
        return 0


def main():
    """Process all mission files."""
    mission_files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))

    total_hints = 0
    total_files = 0

    for filepath in mission_files:
        filename = os.path.basename(filepath)
        hints_added = process_file(filepath)

        if hints_added > 0:
            total_hints += hints_added
            total_files += 1
            print(f"✓ {filename}: +{hints_added} hints")

    print(f"\n{'='*70}")
    print(f"Hints added: {total_hints}")
    print(f"Files modified: {total_files}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
