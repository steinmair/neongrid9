"""
NeonGrid-9 :: Advanced Features
Hints, Achievements, Faction Visualizations
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum


# ── Hint System ────────────────────────────────────────────────────────────────
class HintLevel(Enum):
    FREE = 0        # No cost
    STANDARD = 1    # 20 XP cost
    FINAL = 2       # 50 XP cost (reveals answer)


@dataclass
class HintRequest:
    mission_id: str
    level: HintLevel
    xp_cost: int
    text: str

    @staticmethod
    def create(mission_id: str, hints: List[str], level: int) -> Optional['HintRequest']:
        """Create hint request if hints exist at that level."""
        if not hints or level >= len(hints):
            return None

        costs = [0, 20, 50]
        xp_cost = costs[min(level, len(costs)-1)]
        hint_level = HintLevel(min(level, 2))

        return HintRequest(
            mission_id=mission_id,
            level=hint_level,
            xp_cost=xp_cost,
            text=hints[level]
        )


# ── Achievement System ─────────────────────────────────────────────────────────
@dataclass
class Achievement:
    id: str
    name: str
    description: str
    xp_reward: int
    icon: str = "⭐"

    def __eq__(self, other):
        if isinstance(other, Achievement):
            return self.id == other.id
        return self.id == other


# ── Vordefinierte Achievements ────────────────────────────────────────────────
ACHIEVEMENTS = {
    # Early game
    'first_mission': Achievement(
        id='first_mission',
        name='First Signal',
        description='Complete your first mission.',
        xp_reward=50,
        icon='🟢'
    ),
    'chapter_1_complete': Achievement(
        id='chapter_1_complete',
        name='Hardware Hacker',
        description='Complete all Hardware chapter missions.',
        xp_reward=200,
        icon='⚙️'
    ),

    # Mid game
    'chapter_5_complete': Achievement(
        id='chapter_5_complete',
        name='Permission Master',
        description='Complete the Permissions chapter.',
        xp_reward=300,
        icon='🔐'
    ),
    'boss_defeated': Achievement(
        id='boss_defeated',
        name='Daemon Slayer',
        description='Defeat your first boss mission.',
        xp_reward=500,
        icon='⚔️'
    ),
    'five_bosses': Achievement(
        id='five_bosses',
        name='Boss Killer',
        description='Defeat 5 boss missions.',
        xp_reward=1000,
        icon='💀'
    ),

    # Late game
    'all_bosses': Achievement(
        id='all_bosses',
        name='Linux Master',
        description='Defeat all 22 boss missions.',
        xp_reward=5000,
        icon='👑'
    ),
    'exam_mastered': Achievement(
        id='exam_mastered',
        name='Exam Overlord',
        description='Complete all exam chapter (18) blocks.',
        xp_reward=1500,
        icon='📚'
    ),

    # Special
    'perfect_quiz': Achievement(
        id='perfect_quiz',
        name='Quiz Perfect',
        description='Get all quiz questions correct in one mission.',
        xp_reward=250,
        icon='🎯'
    ),
    'speedrun': Achievement(
        id='speedrun',
        name='Speed Runner',
        description='Complete a chapter in under 1 hour.',
        xp_reward=300,
        icon='⚡'
    ),
    'lore_collector': Achievement(
        id='lore_collector',
        name='Story Addict',
        description='Read all story sections in a chapter.',
        xp_reward=150,
        icon='📖'
    ),
    'faction_max': Achievement(
        id='faction_max',
        name='Faction Leader',
        description='Reach max level (100) in any faction.',
        xp_reward=800,
        icon='🏆'
    ),

    # New achievements for polish
    'perfect_streak': Achievement(
        id='perfect_streak',
        name='Flawless Victory',
        description='Answer 10 consecutive quiz questions correctly.',
        xp_reward=400,
        icon='🎯'
    ),
    'no_hints': Achievement(
        id='no_hints',
        name='Self-Reliant',
        description='Complete a mission without using any hints.',
        xp_reward=150,
        icon='💪'
    ),
    'all_factions': Achievement(
        id='all_factions',
        name='Diplomat',
        description='Reach level 2+ with all 5 factions.',
        xp_reward=1200,
        icon='🤝'
    ),
    'gear_collector': Achievement(
        id='gear_collector',
        name='Arsenal Master',
        description='Collect 10+ different gear items.',
        xp_reward=500,
        icon='⚡'
    ),
    'quest_marathon': Achievement(
        id='quest_marathon',
        name='Grinder',
        description='Complete 100+ missions.',
        xp_reward=1500,
        icon='🔄'
    ),
    'chapter_master': Achievement(
        id='chapter_master',
        name='Scholar',
        description='Complete all missions in 5 different chapters.',
        xp_reward=2000,
        icon='📚'
    ),
    'level_ten': Achievement(
        id='level_ten',
        name='Rising Power',
        description='Reach level 10 (Net Runner).',
        xp_reward=1000,
        icon='⬆️'
    ),
    'jackpot': Achievement(
        id='jackpot',
        name='Lucky Strike',
        description='Earn 1000+ XP in a single playthrough session.',
        xp_reward=300,
        icon='🍀'
    ),
}


@dataclass
class AchievementTracker:
    """Tracks player achievements."""
    unlocked: Set[str] = field(default_factory=set)

    def unlock(self, achievement_id: str) -> Optional[Achievement]:
        """Unlock an achievement, return it if newly unlocked."""
        if achievement_id in self.unlocked:
            return None  # Already unlocked

        if achievement_id not in ACHIEVEMENTS:
            return None  # Invalid ID

        self.unlocked.add(achievement_id)
        return ACHIEVEMENTS[achievement_id]

    def has(self, achievement_id: str) -> bool:
        """Check if achievement is unlocked."""
        return achievement_id in self.unlocked

    def count(self) -> int:
        """Total unlocked achievements."""
        return len(self.unlocked)


# ── Faction Visualization ──────────────────────────────────────────────────────
@dataclass
class FactionStatus:
    name: str
    xp: int
    level: int  # 0-10
    max_xp: int

    def progress_bar(self, width: int = 20) -> str:
        """Generate progress bar for faction."""
        filled = int((self.xp / self.max_xp) * width)
        empty = width - filled
        return '█' * filled + '░' * empty

    def display(self) -> str:
        """Format faction status for display."""
        return f"{self.name:<20} {self.progress_bar()} {self.xp}/{self.max_xp} (Lv{self.level})"


def calculate_level(total_xp: int) -> int:
    """Calculate faction level from total XP or reputation. Levels 1-10."""
    # If value is ≤100, treat as reputation (0-100 scale)
    # Otherwise treat as XP (exponential scale)
    if total_xp <= 100:
        # Reputation levels: 1-5 based on rep/20
        return min(5, max(1, (total_xp // 20) + 1))
    else:
        # XP-based levels: 1-10
        thresholds = [0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3250]
        for i, threshold in enumerate(thresholds[1:], 1):
            if total_xp < threshold:
                return i
        return 10


# ── Hint Display Helpers ───────────────────────────────────────────────────────
HINT_PROMPTS = {
    0: "💡 Free Hint (no cost)",
    1: "💡 Standard Hint (20 XP)",
    2: "💡 Final Answer (50 XP)",
}

HINT_COLORS = {
    0: '\033[92m',  # Green
    1: '\033[93m',  # Yellow
    2: '\033[91m',  # Red
}
