"""
NeonGrid-9 :: Save System
JSON-basierte Speicherstände mit 3 Slots
"""

import json
import os
from pathlib import Path
from engine.player import Player

SAVE_DIR = Path.home() / ".neongrid9"
SAVE_FILES = {
    1: SAVE_DIR / "save_slot1.json",
    2: SAVE_DIR / "save_slot2.json",
    3: SAVE_DIR / "save_slot3.json",
}


def ensure_save_dir():
    SAVE_DIR.mkdir(exist_ok=True)


def save_game(player: Player, slot: int = 1) -> bool:
    ensure_save_dir()
    try:
        path = SAVE_FILES.get(slot)
        if not path:
            return False
        with open(path, "w", encoding="utf-8") as f:
            json.dump(player.to_dict(), f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  Speicherfehler: {e}")
        return False


def load_game(slot: int = 1) -> Player | None:
    path = SAVE_FILES.get(slot)
    if not path or not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Player.from_dict(data)
    except Exception as e:
        print(f"  Ladefehler: {e}")
        return None


def slot_info(slot: int) -> str:
    path = SAVE_FILES.get(slot)
    if not path or not path.exists():
        return "  [LEER]"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        name  = data.get("name", "Ghost")
        level = data.get("level", 1)
        title = data.get("level_title", "Newbie Hacker")
        xp    = data.get("xp", 0)
        done  = len(data.get("completed_missions", []))
        return f"  {name}  |  LVL {level} {title}  |  {xp} XP  |  {done} Missionen"
    except Exception:
        return "  [FEHLER beim Lesen]"


def delete_save(slot: int) -> bool:
    path = SAVE_FILES.get(slot)
    if path and path.exists():
        path.unlink()
        return True
    return False
