#!/usr/bin/env python3
"""
Use Python AST to safely patch mission files with hints.
This is more robust than regex-based approaches.
"""

import ast
import sys
import os
import glob
from typing import List, Any

sys.path.insert(0, '/home/ande/neongrid9')


class HintGenerator:
    @staticmethod
    def build_hints(expected_commands: List[str], task_desc: str = "") -> List[str]:
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


class MissionPatcher(ast.NodeTransformer):
    """AST transformer that adds hints to missions."""

    def __init__(self):
        self.modified = False
        self.current_mission_data = {}

    def visit_Call(self, node: ast.Call) -> ast.Call:
        """Visit function calls looking for Mission(...)."""
        # Visit children first
        self.generic_visit(node)

        # Check if this is a Mission() call
        if not (isinstance(node.func, ast.Name) and node.func.id == 'Mission'):
            return node

        # Extract keyword arguments
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

        # Skip if already has hints
        if has_hints:
            return node

        # Extract expected_commands list
        if expected_commands and isinstance(expected_commands, ast.List):
            commands = []
            for elt in expected_commands.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    commands.append(elt.value)

            if commands:
                # Generate hints
                hints = HintGenerator.build_hints(commands, task_description)

                # Create hints list node
                hints_elts = [ast.Constant(value=h) for h in hints]
                hints_list = ast.List(elts=hints_elts, ctx=ast.Load())
                hints_keyword = ast.keyword(arg='hints', value=hints_list)

                # Add to keywords right after expected_commands
                # Find position of expected_commands and insert after
                ec_idx = next(i for i, kw in enumerate(node.keywords) if kw.arg == 'expected_commands')
                node.keywords.insert(ec_idx + 1, hints_keyword)

                self.modified = True

        return node


def patch_file(filepath: str) -> bool:
    """Patch a mission file with hints using AST."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has hints
        if "hints = [" in content:
            return False

        # Parse
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"  Syntax error in {filepath}: {e}")
            return False

        # Transform
        patcher = MissionPatcher()
        patcher.visit(tree)

        if not patcher.modified:
            return False

        # Convert back to source
        try:
            new_content = ast.unparse(tree)
        except Exception as e:
            print(f"  Error unparsing {filepath}: {e}")
            return False

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return False


def main():
    """Patch all mission files."""
    files = sorted(glob.glob("/home/ande/neongrid9/missions/ch*.py"))
    processed = 0

    for filepath in files:
        filename = os.path.basename(filepath)

        if patch_file(filepath):
            processed += 1
            print(f"✓ {filename}")
        else:
            print(f"- {filename}")

    print(f"\nPatched {processed} files")


if __name__ == "__main__":
    main()
