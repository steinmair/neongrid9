"""
NeonGrid-9 :: Player Engine
XP, Level, Reputation, Inventar, Skilltree
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set
from engine.features import AchievementTracker

# ── Level-Tabelle ─────────────────────────────────────────────────────────────
LEVELS = [
    (1,  "Newbie Hacker",      0),
    (2,  "Script Kiddie",      500),
    (3,  "Terminal User",      1500),
    (4,  "Shell Dweller",      3000),
    (5,  "Pipe Runner",        5000),
    (6,  "Process Wrangler",   7500),
    (7,  "Filesystem Ghost",   10500),
    (8,  "Package Smuggler",   14000),
    (9,  "Daemon Whisperer",   18000),
    (10, "Net Runner",         22500),
    (11, "Kernel Adept",       27500),
    (12, "Root Initiate",      33000),
    (13, "System Breaker",     39000),
    (14, "Shell Architect",    45500),
    (15, "Certified Ghost",    52500),
]

# ── Gear-Items ────────────────────────────────────────────────────────────────
GEAR_CATALOG = {
    # ── Starter-Gear (automatisch) ────────────────────────────────────────────
    "basic_terminal":  {
        "name":   "Basic Terminal",
        "desc":   "Dein erstes Interface. Rostig, aber funktional.",
        "boost":  "starter",
        "rarity": "common",
        "tier":   1,
    },
    "cracked_manpage": {
        "name":   "Cracked Manpage",
        "desc":   "Halb verbranntes Handbuch. Gibt gelegentlich Hinweise.",
        "boost":  "hints",
        "rarity": "common",
        "tier":   1,
    },

    # ── Kapitel-Boss-Drops ────────────────────────────────────────────────────
    "hardware_scanner": {
        "name":   "Hardware Scanner",
        "desc":   "Enthüllt versteckte Hinweise bei Hardware- & Paket-Tasks.",
        "boost":  "hw_hints",
        "rarity": "uncommon",
        "tier":   2,
        "source": "Boss-Drop: Kap. 1, 9, 12",
    },
    "kernel_beacon": {
        "name":   "Kernel Beacon",
        "desc":   "+15% XP auf Boot-, Kernel- und Init-Missionen.",
        "boost":  "boot_xp",
        "rarity": "uncommon",
        "tier":   2,
        "source": "Boss-Drop: Kap. 2, 7, 11",
    },
    "root_keycard": {
        "name":   "Root Keycard",
        "desc":   "+15% XP auf User-, Sudo- und Admin-Missionen.",
        "boost":  "admin_xp",
        "rarity": "uncommon",
        "tier":   2,
        "source": "Boss-Drop: Kap. 3, 10",
    },
    "pipe_wrench": {
        "name":   "Pipe Wrench",
        "desc":   "+10% XP auf Shell-, Pipe- und Scripting-Missionen.",
        "boost":  "pipe_xp",
        "rarity": "uncommon",
        "tier":   2,
        "source": "Boss-Drop: Kap. 4, 6, 14",
    },
    "regex_scope": {
        "name":   "Regex Scope",
        "desc":   "+10% XP auf Regex-, Textfilter- und Decode-Missionen.",
        "boost":  "regex_xp",
        "rarity": "uncommon",
        "tier":   2,
        "source": "Boss-Drop: Kap. 5, 8",
    },
    "dmesg_decoder": {
        "name":   "dmesg Decoder",
        "desc":   "Kernel-Fehlermeldungen werden klarer. +5% XP auf Scan-Missionen.",
        "boost":  "scan_xp",
        "rarity": "uncommon",
        "tier":   2,
        "source": "Erweiterte Kap. 13",
    },

    # ── Elite-Gear (späte Boss-Drops) ─────────────────────────────────────────
    "ghost_mask": {
        "name":   "Ghost Mask",
        "desc":   "+20% XP auf alle Quiz-Missionen. Du erkennst Prüfungsmuster.",
        "boost":  "quiz_xp",
        "rarity": "rare",
        "tier":   3,
        "source": "Boss-Drop: Kap. 15 — SHADOW ADMIN",
    },
    "display_lens": {
        "name":   "Display Lens",
        "desc":   "Review Mode zeigt Erklärungen vor der Antwort-Auswertung.",
        "boost":  "review_hints",
        "rarity": "rare",
        "tier":   3,
        "source": "Boss-Drop: Kap. 16 — GLITCH RENDERER",
    },
    "phantom_blade": {
        "name":   "Phantom Blade",
        "desc":   "+15% XP auf Shell-Env-, Alias- und PATH-Missionen.",
        "boost":  "shell_xp",
        "rarity": "rare",
        "tier":   3,
        "source": "Boss-Drop: Kap. 17 — PHANTOM SHELL",
    },

    # ── Legendäres Gear ───────────────────────────────────────────────────────
    "lpic1_badge": {
        "name":   "LPIC-1 Badge",
        "desc":   "+5% auf ALLE XP-Gewinne. Prestige-Item. Nur eines im Spiel.",
        "boost":  "all_xp",
        "rarity": "legendary",
        "tier":   4,
        "source": "Boss-Drop: Kap. 18 — FINAL EXAM",
    },
}

# ── Seltenheits-Farben (für Anzeige) ─────────────────────────────────────────
RARITY_COLOR = {
    "common":    "\033[37m",    # Weiß
    "uncommon":  "\033[32m",    # Grün
    "rare":      "\033[34m",    # Blau
    "legendary": "\033[33m",    # Gold/Gelb
}

# ── Fraktionen ────────────────────────────────────────────────────────────────
FACTIONS = [
    "Kernel Syndicate",   # Kap. 2, 7, 11, 13, 15, 18
    "Root Collective",    # Kap. 3, 4, 5, 10, 12, 17
    "Net Runners",        # Kap. 6, 8, 9, 14, 16
    "Ghost Processors",   # Zukünftige Kapitel
    "Firewall Dominion",  # Zukünftige Kapitel
]


@dataclass
class Player:
    name: str = "Ghost"
    xp: int = 0
    level: int = 1
    level_title: str = "Newbie Hacker"

    # Missionsfortschritt
    completed_missions: Set[str] = field(default_factory=set)
    failed_missions: Dict[str, int] = field(default_factory=dict)   # id → Fehlversuche

    # Inventar
    inventory: List[str] = field(default_factory=lambda: ["basic_terminal", "cracked_manpage"])

    # Reputation (0–100 je Fraktion)
    reputation: Dict[str, int] = field(default_factory=lambda: {f: 0 for f in FACTIONS})

    # Gesamtstatistiken
    total_quizzes: int = 0
    correct_first_try: int = 0
    bosses_defeated: int = 0
    secrets_found: int = 0
    days_played: int = 1
    streak: int = 0

    # Quiz-Statistiken pro Kapitel: {ch_id: {"asked": N, "correct": N}}
    chapter_quiz_stats: Dict[str, dict] = field(default_factory=dict)

    # Achievements
    achievements: AchievementTracker = field(default_factory=AchievementTracker)

    def add_xp(self, amount: int) -> tuple[int, bool]:
        """XP hinzufügen. Gibt (neues_xp, level_up) zurück."""
        # Level-basierter Skalierungsbonus
        if self.level >= 15:
            scale = 1.3
        elif self.level >= 10:
            scale = 1.2
        elif self.level >= 5:
            scale = 1.1
        else:
            scale = 1.0
        scaled_amount = int(amount * scale)
        old_level = self.level
        self.xp += scaled_amount
        self._recalculate_level()
        leveled_up = self.level > old_level
        return self.xp, leveled_up

    def _recalculate_level(self):
        for lvl, title, threshold in reversed(LEVELS):
            if self.xp >= threshold:
                self.level = lvl
                self.level_title = title
                break

    def get_next_level_xp(self) -> int:
        for lvl, _, threshold in LEVELS:
            if lvl == self.level + 1:
                return threshold
        return self.xp  # Max level

    def get_current_level_xp(self) -> int:
        for lvl, _, threshold in LEVELS:
            if lvl == self.level:
                return threshold
        return 0

    def has_gear(self, item_id: str) -> bool:
        return item_id in self.inventory

    def add_gear(self, item_id: str) -> bool:
        if item_id not in self.inventory and item_id in GEAR_CATALOG:
            self.inventory.append(item_id)
            return True
        return False

    def gear_bonus(self, boost_type: str) -> float:
        """Gibt XP-Multiplikator für Bonus-Typ zurück. Boni stapeln sich nicht."""
        bonuses = {
            "pipe_xp":   ("pipe_wrench",      1.10),
            "regex_xp":  ("regex_scope",      1.10),
            "admin_xp":  ("root_keycard",     1.15),
            "boot_xp":   ("kernel_beacon",    1.15),
            "scan_xp":   ("dmesg_decoder",    1.05),
            "quiz_xp":   ("ghost_mask",       1.20),
            "shell_xp":  ("phantom_blade",    1.15),
        }
        base = 1.0
        if boost_type in bonuses:
            item_id, mult = bonuses[boost_type]
            if item_id in self.inventory:
                base = mult
        # LPIC-1 Badge: +5% auf alles (additiv nach anderen Boni)
        if "lpic1_badge" in self.inventory and base > 1.0:
            base += 0.05
        elif "lpic1_badge" in self.inventory:
            base = 1.05
        return base

    def has_hint_gear(self) -> bool:
        hint_items = {"cracked_manpage", "hardware_scanner", "display_lens"}
        return bool(hint_items & set(self.inventory))

    def mission_completed(self, mission_id: str) -> bool:
        return mission_id in self.completed_missions

    def complete_mission(self, mission_id: str):
        self.completed_missions.add(mission_id)

    def add_reputation(self, faction: str, amount: int):
        if faction in self.reputation:
            self.reputation[faction] = min(100, self.reputation[faction] + amount)

    def stats_summary(self) -> str:
        lines = [
            f"  Name       : {self.name}",
            f"  Level      : {self.level} — {self.level_title}",
            f"  XP         : {self.xp}",
            f"  Missionen  : {len(self.completed_missions)} abgeschlossen",
            f"  Bosse      : {self.bosses_defeated} besiegt",
            f"  Streak     : {self.streak} Tage",
            "",
            "  REPUTATION:",
        ]
        for faction, rep in self.reputation.items():
            bar = "█" * (rep // 10) + "░" * (10 - rep // 10)
            lines.append(f"    {faction:<22} [{bar}] {rep}/100")
        lines.append("")
        lines.append("  INVENTAR:")
        for item_id in self.inventory:
            item    = GEAR_CATALOG.get(item_id, {})
            rarity  = item.get("rarity", "common")
            color   = RARITY_COLOR.get(rarity, "\033[37m")
            reset   = "\033[0m"
            tier    = item.get("tier", 1)
            tier_s  = "★" * tier + "☆" * (4 - tier)
            lines.append(f"    {color}► {item.get('name', item_id):<22}{reset} {tier_s}  {item.get('desc', '')}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "name":               self.name,
            "xp":                 self.xp,
            "level":              self.level,
            "level_title":        self.level_title,
            "completed_missions": list(self.completed_missions),
            "failed_missions":    self.failed_missions,
            "inventory":          self.inventory,
            "reputation":         self.reputation,
            "total_quizzes":      self.total_quizzes,
            "correct_first_try":  self.correct_first_try,
            "bosses_defeated":    self.bosses_defeated,
            "secrets_found":      self.secrets_found,
            "days_played":        self.days_played,
            "streak":             self.streak,
            "chapter_quiz_stats": self.chapter_quiz_stats,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Player":
        p = cls()
        p.name               = d.get("name", "Ghost")
        p.xp                 = d.get("xp", 0)
        p.level              = d.get("level", 1)
        p.level_title        = d.get("level_title", "Newbie Hacker")
        p.completed_missions = set(d.get("completed_missions", []))
        p.failed_missions    = d.get("failed_missions", {})
        p.inventory          = d.get("inventory", ["basic_terminal", "cracked_manpage"])
        saved_rep = d.get("reputation", {})
        p.reputation = {f: saved_rep.get(f, 0) for f in FACTIONS}  # migration: fill missing factions
        p.total_quizzes      = d.get("total_quizzes", 0)
        p.correct_first_try  = d.get("correct_first_try", 0)
        p.bosses_defeated    = d.get("bosses_defeated", 0)
        p.secrets_found      = d.get("secrets_found", 0)
        p.days_played        = d.get("days_played", 1)
        p.streak             = d.get("streak", 0)
        p.chapter_quiz_stats = d.get("chapter_quiz_stats", {})
        return p

    def record_quiz_result(self, chapter: int, correct: bool):
        key = str(chapter)
        if key not in self.chapter_quiz_stats:
            self.chapter_quiz_stats[key] = {"asked": 0, "correct": 0}
        self.chapter_quiz_stats[key]["asked"] += 1
        if correct:
            self.chapter_quiz_stats[key]["correct"] += 1

    def quiz_accuracy(self, chapter: int) -> float:
        stats = self.chapter_quiz_stats.get(str(chapter), {})
        asked = stats.get("asked", 0)
        if asked == 0:
            return 0.0
        return stats.get("correct", 0) / asked
