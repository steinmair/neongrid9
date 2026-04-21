#!/usr/bin/env python3
"""
Complete hint population for all 501 missions using AST unparsing.
Accept code reformatting as acceptable cost for complete coverage.
"""

import ast
import sys
import os
import glob

sys.path.insert(0, '/home/ande/neongrid9')

class HintGenerator:
    @staticmethod
    def build_hints(expected_commands, task_desc=""):
        """Generate 3-tier hints."""
        if not expected_commands:
            return []

        cmd = expected_commands[0] if isinstance(expected_commands, list) else str(expected_commands)
        parts = cmd.split()
        main_cmd = parts[0]

        # Hint 1
        if "/" in cmd:
            path = next((p for p in parts if "/" in p), "")
            hint1 = f"Das Verzeichnis oder die Datei befinden sich unter '{path}'. Der Befehl beginnt mit '{main_cmd}'."
        elif any(x in task_desc.lower() for x in ["zeige", "liste", "anzeigen"]):
            hint1 = f"Ein Auflistungsbefehl wie '{main_cmd}' wird benötigt."
        else:
            hint1 = f"Der Befehl '{main_cmd}' ist der richtige Ansatz."

        # Hint 2
        if len(parts) > 1:
            hint2 = f"Versuche: {' '.join(parts[:min(3, len(parts))])}"
            if len(parts) > 3:
                hint2 += " ..."
        else:
            hint2 = f"Der Befehl selbst ist: {main_cmd}"

        # Hint 3
        hint3 = f"Der vollständige Befehl: {cmd}"

        return [hint1, hint2, hint3]


class MissionPatcher(ast.NodeTransformer):
    """AST transformer that adds hints to missions."""

    def __init__(self):
        self.modified = False
        self.hint_count = 0

    def visit_Call(self, node):
        """Visit function calls looking for Mission(...)."""
        self.generic_visit(node)

        if not (isinstance(node.func, ast.Name) and node.func.id == 'Mission'):
            return node

        # Extract data
        kwargs = {}
        expected_commands = None
        task_description = ""
        has_hints = False

        for keyword in node.keywords:
            kwargs[keyword.arg] = keyword.value
            if keyword.arg == 'expected_commands':
                expected_commands = keyword.value
            elif keyword.arg == 'task_description':
                if isinstance(keyword.value, ast.Constant):
                    task_description = keyword.value.value
            elif keyword.arg == 'hints':
                has_hints = True

        if has_hints:
            return node

        if expected_commands and isinstance(expected_commands, ast.List):
            commands = []
            for elt in expected_commands.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    commands.append(elt.value)

            if commands:
                hints = HintGenerator.build_hints(commands, task_description)
                hints_elts = [ast.Constant(value=h) for h in hints]
                hints_list = ast.List(elts=hints_elts, ctx=ast.Load())
                hints_keyword = ast.keyword(arg='hints', value=hints_list)

                # Insert after expected_commands
                ec_idx = next((i for i, kw in enumerate(node.keywords) if kw.arg == 'expected_commands'), -1)
                if ec_idx >= 0:
                    node.keywords.insert(ec_idx + 1, hints_keyword)
                    self.modified = True
                    self.hint_count += 1

        return node


def process_file(filepath):
    """Process a mission file with AST."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already fully processed
    if "hints = [" in content:
        return 0

    try:
        tree = ast.parse(content)
    except SyntaxError:
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
        print(f"Error unparsing {filepath}: {e}")
        return 0


def main():
    """Process all mission files."""
    mission_files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))

    total_hints_added = 0
    processed_files = 0

    for filepath in mission_files:
        filename = os.path.basename(filepath)
        hints_added = process_file(filepath)

        if hints_added > 0:
            total_hints_added += hints_added
            processed_files += 1
            print(f"✓ {filename}: +{hints_added} hints")
        else:
            print(f"- {filename}")

    print(f"\n{'='*70}")
    print(f"Total hints added: {total_hints_added}")
    print(f"Files modified: {processed_files}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
