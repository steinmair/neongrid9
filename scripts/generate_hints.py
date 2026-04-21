#!/usr/bin/env python3
"""
Generate 3-tier hints for all missions based on task descriptions and expected commands.
Outputs Python code ready to insert into mission files.
"""

def generate_hints(task_desc: str, expected_commands: list, explanation: str = "", mission_type: str = "") -> list:
    """
    Generate 3-tier hints (free, standard 20xp, final 50xp) from mission data.
    """
    if not expected_commands:
        return []

    cmd = expected_commands[0] if isinstance(expected_commands, list) else expected_commands

    # Parse the command to extract key components
    parts = cmd.split()
    main_cmd = parts[0] if parts else cmd

    # Extract arguments/flags
    flags = [p for p in parts[1:] if p.startswith('-')]
    args = [p for p in parts[1:] if not p.startswith('-')]

    # Build hints based on command structure
    hints = []

    # FREE HINT: Conceptual guidance
    if mission_type == "SCAN" or "zeige" in task_desc.lower() or "liste" in task_desc.lower():
        if "file" in task_desc.lower() or "datei" in task_desc.lower():
            hints.append(f"Du brauchst einen Befehl, der mit '{main_cmd}' beginnt.")
        elif "/" in cmd:
            dir_hint = cmd.split()[1] if len(parts) > 1 else cmd
            hints.append(f"Schau im Verzeichnis '{dir_hint}' nach. Der Befehl beginnt mit '{main_cmd}'.")
        else:
            hints.append(f"Der Befehl beginnt mit '{main_cmd}' und zeigt Systeminformationen an.")
    elif mission_type == "DECODE":
        hints.append(f"Nutze einen Text-Verarbeitungsbefehl wie '{main_cmd}' um das Muster zu erkennen.")
    elif mission_type == "INFILTRATE":
        hints.append(f"Der Befehl ist '{main_cmd}' mit bestimmten Optionen.")
    elif mission_type == "REPAIR":
        hints.append(f"Du musst mit '{main_cmd}' arbeiten um das System zu reparieren.")
    elif mission_type == "CONSTRUCT":
        hints.append(f"Erstelle oder konfiguriere etwas mit '{main_cmd}'.")
    else:
        hints.append(f"Der richtige Befehl beginnt mit '{main_cmd}'.")

    # STANDARD HINT (20 XP): More specific guidance
    if flags:
        flag_hint = " ".join(flags) if len(flags) <= 2 else f"{flags[0]} ..."
        hints.append(f"Versuche: {main_cmd} {flag_hint}")
    elif args and "/" in cmd:
        hints.append(f"Versuche: {main_cmd} {args[0]}")
    elif "/" in cmd:
        path = [p for p in parts[1:] if "/" in p]
        if path:
            hints.append(f"Der Befehl ist: {main_cmd} {path[0]}")
        else:
            hints.append(f"Nutze {main_cmd} mit einem Pfad-Argument.")
    else:
        if len(parts) > 1:
            hints.append(f"Versuche: {main_cmd} {parts[1]}")
        else:
            hints.append(f"Der Befehl selbst ist: {main_cmd}")

    # FINAL HINT (50 XP): The complete answer
    hints.append(f"Der vollständige Befehl ist: {cmd}")

    return hints[:3] if len(hints) >= 3 else hints


def extract_missions_and_hints(chapter_num: int) -> dict:
    """
    Read a chapter file and extract mission data for hint generation.
    Returns dict of mission_id -> (task_desc, expected_commands, explanation)
    """
    try:
        chapter_file = f"missions/ch{chapter_num:02d}_*.py"
        import glob
        files = glob.glob(chapter_file)
        if not files:
            return {}

        # This is a simplified extractor - in practice we'd parse the AST
        return {}
    except Exception as e:
        print(f"Error reading chapter {chapter_num}: {e}")
        return {}


if __name__ == "__main__":
    # Test hint generation
    test_commands = [
        ("lspci", "Zeige alle PCI-Geräte im System an.", "SCAN"),
        ("ls /sys/firmware/efi/", "Prüfe ob dieses System UEFI oder BIOS nutzt.", "SCAN"),
        ("grep pattern file.txt", "Finde alle Zeilen die 'pattern' enthalten.", "DECODE"),
        ("chmod 755 script.sh", "Mache die Datei ausführbar.", "REPAIR"),
    ]

    for cmd, task, mtype in test_commands:
        hints = generate_hints(task, [cmd], mission_type=mtype)
        print(f"\n{cmd}:")
        for i, hint in enumerate(hints):
            cost = ["FREE", "20 XP", "50 XP"][i]
            print(f"  [{cost}] {hint}")
