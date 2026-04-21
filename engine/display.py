"""
NeonGrid-9 :: Display Engine
Alle Ausgabefunktionen mit Cyberpunk-Ästhetik
"""

import os
import sys
import time

# ── ANSI Farben ──────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Cyberpunk Palette
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

    # Kombiniert
    NEON    = "\033[96m\033[1m"   # bright cyan bold
    WARN    = "\033[93m\033[1m"   # bright yellow bold
    DANGER  = "\033[91m\033[1m"   # bright red bold
    SUCCESS = "\033[92m\033[1m"   # bright green bold
    STORY   = "\033[95m"          # magenta für Story
    CODE    = "\033[92m"          # green für Code
    PROMPT  = "\033[96m"          # cyan für Prompt
    XP      = "\033[93m"          # yellow für XP


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def typewrite(text: str, delay: float = 0.018, color: str = C.WHITE):
    """Schreibmaschinen-Effekt für Story-Text."""
    for ch in text:
        sys.stdout.write(color + ch + C.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def slow_print(text: str, delay: float = 0.008):
    """Leicht verzögerter Print für wichtige Nachrichten."""
    for line in text.split('\n'):
        print(line)
        time.sleep(delay)


def box(title: str, content: str, color: str = C.CYAN, width: int = 66):
    """Zeichnet eine Box mit Titel und Inhalt."""
    border = color + "─" * width + C.RESET
    top    = color + "╔" + "═" * width + "╗" + C.RESET
    bot    = color + "╚" + "═" * width + "╝" + C.RESET
    mid    = color + "╠" + "═" * width + "╣" + C.RESET

    print(top)
    title_pad = title.center(width)
    print(color + "║" + C.RESET + C.BOLD + title_pad + C.RESET + color + "║" + C.RESET)
    print(mid)
    for line in content.split('\n'):
        padded = line[:width].ljust(width)
        print(color + "║" + C.RESET + " " + padded[:-1] + color + "║" + C.RESET)
    print(bot)


def header(title: str, subtitle: str = ""):
    """Haupt-Header mit Cyberpunk-Logo."""
    clear()
    print(C.NEON + """
╔══════════════════════════════════════════════════════════════════╗
║  ███╗   ██╗███████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗ ██╗ ██████╗  ║
║  ████╗  ██║██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██║██╔══██╗ ║
║  ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝██║██║  ██║ ║
║  ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██║██║  ██║ ║
║  ██║ ╚████║███████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║██████╔╝ ║
╚══════════════════════════════════════════════════════════════════╝""" + C.RESET)
    print(C.GRAY + f"  {'NeonGrid-9:: Linux Combat Training System':^66}" + C.RESET)
    print(C.RED + f"  {'⚙  Powered by Chaoswerk  ⚙':^66}" + C.RESET)
    if subtitle:
        print(C.YELLOW + f"  {subtitle:^66}" + C.RESET)
    print()


def chapter_header(num: int, title: str, subtitle: str = ""):
    """Header für ein Kapitel."""
    clear()
    bar = C.CYAN + "═" * 68 + C.RESET
    print(bar)
    print(C.NEON + f"  KAPITEL {num:02d}  ::  {title}" + C.RESET)
    if subtitle:
        print(C.GRAY + f"  {subtitle}" + C.RESET)
    print(bar)
    print()


def mission_header(mission_id: str, title: str, xp: int, mtype: str):
    """Header für eine Mission."""
    type_colors = {
        "SCAN":      C.BLUE,
        "INFILTRATE":C.GREEN,
        "DECODE":    C.YELLOW,
        "CONSTRUCT": C.MAGENTA,
        "REPAIR":    C.RED,
        "QUIZ":      C.CYAN,
        "BOSS":      C.DANGER,
    }
    tc = type_colors.get(mtype, C.WHITE)
    print(C.GRAY + "─" * 68 + C.RESET)
    print(C.NEON + f"  [{mission_id}] " + C.WHITE + title + C.RESET)
    print(tc + f"  {mtype}" + C.RESET + C.GRAY + f"  ::  " + C.XP + f"+{xp} XP" + C.RESET)
    print(C.GRAY + "─" * 68 + C.RESET)
    print()


def xp_bar(current: int, level: int, level_xp: int, next_xp: int, width: int = 40):
    """Fortschrittsbalken für XP."""
    if next_xp <= level_xp:
        pct = 1.0
    else:
        pct = (current - level_xp) / (next_xp - level_xp)
    filled = int(width * pct)
    bar = C.GREEN + "█" * filled + C.GRAY + "░" * (width - filled) + C.RESET
    print(f"  {C.XP}LVL {level:02d}{C.RESET}  [{bar}]  {C.XP}{current} XP{C.RESET}")


def show_xp_gain(amount: int, reason: str = ""):
    """Zeigt XP-Gewinn animiert."""
    print()
    time.sleep(0.2)
    print(C.SUCCESS + f"  ✓  +{amount} XP" + (f"  ({reason})" if reason else "") + C.RESET)
    time.sleep(0.1)


def show_story(speaker: str, text: str, delay: float = 0.015):
    """Zeigt Story-Dialog."""
    print()
    print(C.MAGENTA + f"  ┌─[ {speaker} ]" + C.RESET)
    for line in text.strip().split('\n'):
        print(C.STORY + f"  │  {line.strip()}" + C.RESET)
        time.sleep(delay * len(line))
    print(C.MAGENTA + "  └─" + C.RESET)
    print()


def show_code(code: str, lang: str = "bash"):
    """Zeigt Code-Block."""
    print(C.GRAY + f"  ┌─[{lang}]" + C.RESET)
    for line in code.strip().split('\n'):
        print(C.CODE + f"  │  {line}" + C.RESET)
    print(C.GRAY + "  └─" + C.RESET)


def show_info(text: str):
    """Info-Box."""
    print()
    for line in text.strip().split('\n'):
        print(C.CYAN + "  ℹ  " + C.RESET + line.strip())
    print()


def show_warn(text: str):
    """Warnung."""
    print()
    print(C.WARN + f"  ⚠  {text}" + C.RESET)
    print()


def show_error(text: str):
    """Fehlermeldung."""
    print()
    print(C.DANGER + f"  ✗  SYSTEM ERROR: {text}" + C.RESET)
    print()


def show_success(text: str):
    """Erfolgsmeldung."""
    print()
    print(C.SUCCESS + f"  ✓  {text}" + C.RESET)
    print()


def show_exam_tip(text: str):
    """Prüfungshinweis-Box."""
    print()
    print(C.YELLOW + "  ╔═[ Linux PRÜFUNGSWISSEN ]" + C.RESET)
    for line in text.strip().split('\n'):
        print(C.YELLOW + "  ║  " + C.RESET + line.strip())
    print(C.YELLOW + "  ╚═" + C.RESET)
    print()


def show_memory_tip(text: str):
    """Merksatz."""
    print()
    print(C.MAGENTA + "  ★  MERKSATZ: " + C.RESET + C.WHITE + text + C.RESET)
    print()


def show_ascii_art(art: str, color: str = ""):
    """Zeigt Neon ASCII Art. Farbe optional — default CYAN+BOLD."""
    if not art:
        return
    col = color if color else C.NEON
    print()
    for line in art.split('\n'):
        print(col + line + C.RESET)
    print()


def show_transition(text: str):
    """Kurzer Übergangssatz zwischen Mission-Sektionen."""
    if not text:
        return
    print()
    print(C.STORY + "  > " + C.RESET + C.DIM + text + C.RESET)
    time.sleep(0.15)
    print()


def prompt_continue():
    """Pause mit Enter-Aufforderung."""
    print()
    input(C.GRAY + "  [ ENTER ] weiterspielen ..." + C.RESET)


def prompt_input(label: str = "terminal", valid_choices: tuple = None) -> str:
    """Eingabe-Prompt im Terminal-Style."""
    print()
    while True:
        response = input(C.PROMPT + f"  [{label}]> " + C.RESET).strip().lower()
        if valid_choices is None or response in valid_choices:
            return response
        # If invalid choice, loop and ask again (silently)


def show_progress(chapter: int, total_chapters: int, missions_done: int, total_missions: int):
    """Fortschrittsanzeige."""
    ch_pct = chapter / total_chapters
    m_pct  = missions_done / total_missions if total_missions > 0 else 0
    w = 30
    ch_bar = C.CYAN  + "█" * int(w*ch_pct) + C.GRAY + "░" * (w - int(w*ch_pct)) + C.RESET
    m_bar  = C.GREEN + "█" * int(w*m_pct)  + C.GRAY + "░" * (w - int(w*m_pct))  + C.RESET
    print(f"  Kapitel   [{ch_bar}]  {chapter}/{total_chapters}")
    print(f"  Missionen [{m_bar}]  {missions_done}/{total_missions}")


def boss_intro(name: str, description: str):
    """Boss-Kampf Intro-Screen."""
    clear()
    print(C.DANGER + """
  ██████╗  ██████╗ ███████╗███████╗
  ██╔══██╗██╔═══██╗██╔════╝██╔════╝
  ██████╔╝██║   ██║███████╗███████╗
  ██╔══██╗██║   ██║╚════██║╚════██║
  ██████╔╝╚██████╔╝███████║███████║
  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
""" + C.RESET)
    print(C.DANGER + f"  ► {name}" + C.RESET)
    print(C.GRAY   + f"  {description}" + C.RESET)
    print()
    input(C.DANGER + "  [ ENTER ] Kampf beginnen ..." + C.RESET)


def level_up_screen(level: int, title: str):
    """Level-Up Animation."""
    clear()
    print(C.SUCCESS + """
  ██╗     ███████╗██╗   ██╗███████╗██╗     ██╗
  ██║     ██╔════╝██║   ██║██╔════╝██║     ██║
  ██║     █████╗  ██║   ██║█████╗  ██║     ██║
  ██║     ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║     ╚═╝
  ███████╗███████╗ ╚████╔╝ ███████╗███████╗██╗
  ╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚══════╝╚═╝
""" + C.RESET)
    print(C.NEON + f"  LEVEL {level:02d}  —  {title}" + C.RESET)
    print()
    time.sleep(1.5)
    input(C.GRAY + "  [ ENTER ] weiter ..." + C.RESET)


def show_hint(hint_text: str, hint_level: int, xp_cost: int = 0):
    """Display a hint with cost information."""
    colors = [C.GREEN, C.YELLOW, C.DANGER]
    labels = ["💡 FREE HINT", "💡 STANDARD HINT (20 XP)", "💡 FINAL ANSWER (50 XP)"]

    color = colors[min(hint_level, 2)]
    label = labels[min(hint_level, 2)]

    print(C.GRAY + "  " + "─" * 70 + C.RESET)
    print(color + f"  {label}" + C.RESET)
    print(C.GRAY + "  " + "─" * 70 + C.RESET)
    show_info(hint_text)
    print()


def show_achievements(achievements: list, xp_earned: int = 0):
    """Display newly unlocked achievements."""
    if not achievements:
        return

    print(C.SUCCESS + "\n  ⭐ ACHIEVEMENTS UNLOCKED!" + C.RESET)
    for ach in achievements:
        print(C.NEON + f"    {ach.icon} {ach.name}" + C.RESET)
        print(C.GRAY + f"    {ach.description}" + C.RESET)
        if ach.xp_reward > 0:
            print(C.XP + f"    +{ach.xp_reward} XP" + C.RESET)
    print()
