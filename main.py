#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  NEONGRID-9 :: Linux COMBAT TRAINING SYSTEM                   ║
║  Version 1.0  |  Sektor 101 — Kapitel 1-3                      ║
║                                                                  ║
║  "The system does not care who you are.                         ║
║   Only what you know."                                          ║
╚══════════════════════════════════════════════════════════════════╝

Starten:  python3 main.py
Python:   3.10+
Deps:     keine (pure stdlib)
"""

import sys
import os
import time

# Python-Version prüfen
if sys.version_info < (3, 10):
    print("NeonGrid-9 benötigt Python 3.10+")
    print(f"Deine Version: {sys.version}")
    sys.exit(1)

from engine.display import (
    C, clear, header, chapter_header, show_story, show_info,
    show_success, show_warn, show_error, xp_bar, prompt_continue,
    prompt_input, typewrite, slow_print, box, level_up_screen
)
from engine.player import Player, LEVELS, GEAR_CATALOG
from engine.save_system import save_game, load_game, slot_info, delete_save
from engine.mission_engine import MissionRunner
from missions.ch01_hardware  import CHAPTER_1_MISSIONS
from missions.ch02_boot      import CHAPTER_2_MISSIONS
from missions.ch03_init      import CHAPTER_3_MISSIONS
from missions.ch04_partitions  import CHAPTER_4_MISSIONS
from missions.ch05_permissions import CHAPTER_5_MISSIONS
from missions.ch06_shell       import CHAPTER_6_MISSIONS
from missions.ch07_processes   import CHAPTER_7_MISSIONS
from missions.ch08_regex_vi    import CHAPTER_8_MISSIONS
from missions.ch09_network     import CHAPTER_9_MISSIONS
from missions.ch10_users       import CHAPTER_10_MISSIONS
from missions.ch11_logging     import CHAPTER_11_MISSIONS
from missions.ch12_packages    import CHAPTER_12_MISSIONS
from missions.ch13_kernel      import CHAPTER_13_MISSIONS
from missions.ch14_scripting   import CHAPTER_14_MISSIONS
from missions.ch15_security    import CHAPTER_15_MISSIONS
from missions.ch16_locale      import CHAPTER_16_MISSIONS
from missions.ch17_shellenv    import CHAPTER_17_MISSIONS
from missions.ch18_storage     import CHAPTER_18_MISSIONS
from missions.ch19_ghost_processors import CHAPTER_19_MISSIONS
from missions.ch20_firewall_dominion import CHAPTER_20_MISSIONS
from missions.ch21_network_services import CHAPTER_21_MISSIONS
from missions.ch22_exam         import CHAPTER_22_MISSIONS

# Kapitel-Metadaten  (id, missions_list, topic_tag, title, subtitle)
CHAPTERS = [
    (1, CHAPTER_1_MISSIONS,   "101.1", "BOOT CAMP",        "Hardware & BIOS/UEFI"),
    (2, CHAPTER_2_MISSIONS,   "101.2", "DARK BOOT",        "Boot-Manager & GRUB2"),
    (3, CHAPTER_3_MISSIONS,   "101.3", "GHOST PROTOCOL",   "SysVinit, systemd & Runlevels"),
    (4, CHAPTER_4_MISSIONS,   "104.1", "PARTITION WARS",   "Partitionierung & Dateisysteme"),
    (5, CHAPTER_5_MISSIONS,   "104.5", "PERMISSION MATRIX","Dateirechte, Links & FHS"),
    (6, CHAPTER_6_MISSIONS,   "103.2", "DATA STREAMS",     "Shell, Pipes, Redirects & Textfilter"),
    (7, CHAPTER_7_MISSIONS,   "103.5", "GHOST PROCESS",    "Prozesse, Signale & Prioritäten"),
    (8, CHAPTER_8_MISSIONS,   "103.7", "REGEX PROTOCOL",   "Reguläre Ausdrücke & vi Editor"),
    (9, CHAPTER_9_MISSIONS,   "109.1", "NET PROTOCOL",     "TCP/IP, ip, ss, DNS, SSH & Firewall"),
    (10, CHAPTER_10_MISSIONS, "107.1", "USER MATRIX",      "Benutzer, Gruppen, sudo & PAM"),
    (11, CHAPTER_11_MISSIONS, "108.1", "SYSLOG MATRIX",    "Logs, Zeitdienste, cron & at"),
    (12, CHAPTER_12_MISSIONS, "102.4", "INSTALL PROTOCOL", "dpkg, apt, rpm, yum/dnf & zypper"),
    (13, CHAPTER_13_MISSIONS, "101.1", "KERNEL FORGE",     "Module, /proc, sysctl, udev & dmesg"),
    (14, CHAPTER_14_MISSIONS, "105.2", "SCRIPT PROTOCOL",  "Bash-Scripting: Variablen, Schleifen, Funktionen"),
    (15, CHAPTER_15_MISSIONS, "110.1", "SECURITY PROTOCOL","SUID, SSH-Härtung, GPG, fail2ban, sudo & LUKS"),
    (16, CHAPTER_16_MISSIONS, "107.3", "LOCALE MATRIX",    "Locale, Zeitzonen, X11, CUPS & Desktop"),
    (17, CHAPTER_17_MISSIONS, "105.1", "SHELL ENV",        "Startup-Dateien, PATH, Aliases, History & PS1"),
    (18, CHAPTER_18_MISSIONS, "104.1/104.3", "STORAGE ADVANCED", "RAID, LVM, Quotas, iSCSI & btrfs"),
    (19, CHAPTER_19_MISSIONS, "102.6/103.6", "GHOST PROTOCOL II", "Container & Virtualization"),
    (20, CHAPTER_20_MISSIONS, "109.4/110.1", "FIREWALL DOMINION", "iptables, nftables, VPN & Netzwerk-Sicherheit"),
    (21, CHAPTER_21_MISSIONS, "109.2/109.4", "NETWORK SERVICES", "NFS, Samba, DHCP, DNS, LDAP & Netzwerkdienste"),
    (22, CHAPTER_22_MISSIONS, "ALL",   "FINAL EXAM PROTOCOL", "Linux Zertifizierungsprüfung — alle Topics"),
]


# ══════════════════════════════════════════════════════════════════════════════
# GAME STATE
# ══════════════════════════════════════════════════════════════════════════════

class GameState:
    def __init__(self):
        self.player:       Player | None = None
        self.save_slot:    int           = 1
        self.current_chapter: int        = 1
        self.running:      bool          = True

    def save(self):
        if self.player:
            save_game(self.player, self.save_slot)

    def auto_save(self, player: Player):
        save_game(player, self.save_slot)


GAME = GameState()


# ══════════════════════════════════════════════════════════════════════════════
# INTRO SCREENS
# ══════════════════════════════════════════════════════════════════════════════

def show_boot_sequence():
    """Boot-Sequenz Animation."""
    clear()
    boot_lines = [
        (C.GREEN,  "BIOS v2.089... POST complete"),
        (C.GREEN,  "CPU: Intel NeoCore @ 4.2GHz — OK"),
        (C.GREEN,  "RAM: 16384 MB — OK"),
        (C.GREEN,  "Disk: NeonDrive 512G — OK"),
        (C.YELLOW, "Loading GRUB2..."),
        (C.CYAN,   "Loading Linux kernel 6.1.0-neongrid9..."),
        (C.CYAN,   "Loading initial ramdisk..."),
        (C.GREEN,  "[    0.000000] Linux version 6.1.0-neongrid9"),
        (C.GREEN,  "[    0.456789] Detected 8 CPU cores"),
        (C.GREEN,  "[    1.234567] systemd: Starting NeonGrid-9..."),
        (C.GREEN,  "[    2.345678] EXT4-fs mounted on /"),
        (C.GREEN,  "[    3.456789] Network: wlan0 UP"),
        (C.YELLOW, "[    4.000000] NeonGrid-9 Learning System: ONLINE"),
    ]
    for color, line in boot_lines:
        print(color + line + C.RESET)
        time.sleep(0.08)
    print()
    time.sleep(0.5)


def show_title_screen():
    """Hauptmenü-Titelscreen."""
    clear()
    print(C.NEON + r"""
  ███╗   ██╗███████╗ ██████╗ ███╗   ██╗
  ████╗  ██║██╔════╝██╔═══██╗████╗  ██║
  ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║
  ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║
  ██║ ╚████║███████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝

   ██████╗ ██████╗ ██╗██████╗        █████╗
  ██╔════╝ ██╔══██╗██║██╔══██╗      ██╔══██╗
  ██║  ███╗██████╔╝██║██║  ██║      ╚██████║
  ██║   ██║██╔══██╗██║██║  ██║       ╚═══██║
  ╚██████╔╝██║  ██║██║██████╔╝██╗   █████╔╝
   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝   ╚════╝  """ + C.RESET)
    print()
    print(C.CYAN + "  " + "═" * 44 + C.RESET)
    print(C.YELLOW + "   Linux COMBAT TRAINING SYSTEM  v1.0" + C.RESET)
    print(C.GRAY  + '   "The system does not care who you are."' + C.RESET)
    print(C.CYAN + "  " + "═" * 44 + C.RESET)
    print()


def show_story_prologue():
    """Story-Prolog beim ersten Start."""
    clear()
    print(C.NEON + "\n  NEONGRID-9  ::  YEAR 2089\n" + C.RESET)
    time.sleep(0.5)

    typewrite(
        "  Die Megacity NeonGrid-9 läuft auf Linux-Systemen.",
        delay=0.02, color=C.WHITE
    )
    typewrite(
        "  Das BIOS Imperium kontrolliert alles durch Unwissenheit.",
        delay=0.02, color=C.GRAY
    )
    time.sleep(0.3)
    typewrite(
        "  Du wachst auf. Kein Terminal. Kein Wissen. Kein Zugang.",
        delay=0.02, color=C.WHITE
    )
    time.sleep(0.3)
    typewrite(
        '  Eine Stimme: "Ich bin Zara Z3R0. Du hast Potential."',
        delay=0.02, color=C.MAGENTA
    )
    typewrite(
        '  "Ich werde dich zum Linux Certified Ghost machen."',
        delay=0.02, color=C.MAGENTA
    )
    typewrite(
        '  "Oder du bleibst Kanonenfutter für das Imperium."',
        delay=0.02, color=C.DANGER
    )
    print()
    time.sleep(0.5)
    prompt_continue()


# ══════════════════════════════════════════════════════════════════════════════
# MENÜS
# ══════════════════════════════════════════════════════════════════════════════

def main_menu() -> str:
    """Hauptmenü. Returns Auswahl."""
    show_title_screen()
    print(C.WHITE + "  HAUPTMENÜ\n" + C.RESET)
    print(C.CYAN  + "  [1]" + C.RESET + "  Neues Spiel")
    print(C.CYAN  + "  [2]" + C.RESET + "  Spiel laden")
    print(C.CYAN  + "  [3]" + C.RESET + "  Spielstand verwalten")
    print(C.CYAN  + "  [4]" + C.RESET + "  Über NeonGrid-9")
    print(C.GRAY  + "  [q]" + C.RESET + "  Beenden")
    print()
    return prompt_input("menü").lower()


def new_game_menu():
    """Neues Spiel starten."""
    clear()
    print(C.NEON + "\n  NEUES SPIEL\n" + C.RESET)

    # Name
    print(C.WHITE + "  Dein Hacker-Name?" + C.RESET)
    print(C.GRAY  + "  (Leer lassen = 'Ghost')" + C.RESET)
    name = prompt_input("name").strip() or "Ghost"

    # Schwierigkeit / Startprofil
    print()
    print(C.WHITE + "  Dein Linux-Level?\n" + C.RESET)
    print(C.CYAN  + "  [1]" + C.RESET + "  Absoluter Anfänger (Empfohlen)")
    print(C.CYAN  + "  [2]" + C.RESET + "  Kenne ein paar Befehle")
    print(C.CYAN  + "  [3]" + C.RESET + "  Linux-Erfahren, brauche LPIC-Fokus")
    print()
    level_choice = prompt_input("wahl [1/2/3]").strip()

    # Save-Slot
    print()
    print(C.WHITE + "  Speichern auf welchem Slot?\n" + C.RESET)
    for slot in [1, 2, 3]:
        info = slot_info(slot)
        print(C.CYAN + f"  [{slot}]" + C.RESET + f"  Slot {slot}: {info}")
    print()
    slot_choice = prompt_input("slot [1/2/3]").strip()
    try:
        GAME.save_slot = int(slot_choice)
        if GAME.save_slot not in [1, 2, 3]:
            GAME.save_slot = 1
    except ValueError:
        GAME.save_slot = 1

    # Player erstellen
    GAME.player = Player(name=name)

    if level_choice == "3":
        GAME.player.xp = 1500   # Level 3 start
        GAME.player.level = 3
        GAME.player.level_title = "Terminal User"

    GAME.save()

    # Prolog zeigen
    show_story_prologue()

    return True


def load_game_menu() -> bool:
    """Spiel laden."""
    clear()
    print(C.NEON + "\n  SPIEL LADEN\n" + C.RESET)
    for slot in [1, 2, 3]:
        info = slot_info(slot)
        print(C.CYAN + f"  [{slot}]" + C.RESET + f"  Slot {slot}: {info}")
    print(C.GRAY + "  [q]" + C.RESET + "  Zurück")
    print()

    choice = prompt_input("slot").lower()
    if choice == "q":
        return False

    try:
        slot = int(choice)
        if slot not in [1, 2, 3]:
            show_error("Ungültiger Slot.")
            return False
    except ValueError:
        return False

    player = load_game(slot)
    if player:
        GAME.player    = player
        GAME.save_slot = slot
        show_success(f"Geladen: {player.name} — Level {player.level} ({player.xp} XP)")
        time.sleep(1)
        return True
    else:
        show_error("Kein Speicherstand in diesem Slot.")
        time.sleep(1)
        return False


def manage_saves_menu():
    """Spielstände verwalten."""
    clear()
    print(C.NEON + "\n  SPIELSTÄNDE\n" + C.RESET)
    for slot in [1, 2, 3]:
        info = slot_info(slot)
        print(C.CYAN + f"  [{slot}]" + C.RESET + f"  {info}")
    print()
    print(C.GRAY + "  d1/d2/d3 = Slot löschen  |  q = Zurück" + C.RESET)

    choice = prompt_input("aktion").lower()
    if choice in ("d1", "d2", "d3"):
        slot = int(choice[1])
        confirm = prompt_input(f"Slot {slot} wirklich löschen? [ja/nein]").lower()
        if confirm == "ja":
            if delete_save(slot):
                show_success(f"Slot {slot} gelöscht.")
            else:
                show_warn("Slot war bereits leer.")
        time.sleep(0.8)


def about_screen():
    """Über-Screen / Credits."""
    clear()
    total_missions = sum(len(c[1]) for c in CHAPTERS)
    total_xp       = sum(sum(m.xp for m in c[1]) for c in CHAPTERS)
    total_questions = sum(
        sum(len(m.quiz_questions) for m in c[1]) for c in CHAPTERS
    )

    print(C.NEON + r"""
  ███╗   ██╗███████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗ ██╗██████╗     █████╗
  ████╗  ██║██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██║██╔══██╗   ██╔══██╗
  ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝██║██║  ██║   ╚██████║
  ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██║██║  ██║    ╚═══██║
  ██║ ╚████║███████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║██████╔╝    █████╔╝
  ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝    ╚════╝
""" + C.RESET)

    print(C.CYAN + "  " + "─" * 66 + C.RESET)
    print(C.WHITE + "  Linux COMBAT TRAINING SYSTEM  ::  Version 1.0" + C.RESET)
    print(C.GRAY  + '  "The system does not care who you are. Only what you know."' + C.RESET)
    print(C.CYAN + "  " + "─" * 66 + C.RESET)

    print(C.YELLOW + "\n  STATISTIKEN\n" + C.RESET)
    print(f"  Kapitel          {len(CHAPTERS):>6}")
    print(f"  Missionen        {total_missions:>6}")
    print(f"  Quiz-Fragen      {total_questions:>6}")
    print(f"  Erreichbare XP   {total_xp:>6,}")
    print(f"  Gear-Items       {len(GEAR_CATALOG):>6}")
    print(f"  Linux Version   {'5.0':>6}")

    print(C.YELLOW + "\n  Linux TOPICS\n" + C.RESET)
    for ch_id, ch_missions, ch_topic, ch_title, ch_sub in CHAPTERS:
        xp = sum(m.xp for m in ch_missions)
        print(f"  {C.CYAN}Kap.{ch_id:>2}{C.RESET}  {ch_title:<18}"
              f"  {C.GRAY}{ch_topic:<7}{C.RESET}"
              f"  {len(ch_missions):>2} Miss.  {xp:>5} XP"
              f"  {C.GRAY}{ch_sub}{C.RESET}")

    print(C.YELLOW + "\n  TERMINAL-SIMULATOR\n" + C.RESET)
    print(C.GRAY + "  hint  — Hinweis anzeigen" + C.RESET)
    print(C.GRAY + "  help  — Lösung zeigen" + C.RESET)
    print(C.GRAY + "  quit  — Mission überspringen" + C.RESET)
    print(C.GRAY + "  Tippe echte Linux-Befehle — der Simulator kennt über 400 Ausgaben." + C.RESET)

    print(C.CYAN + "\n  " + "─" * 66 + C.RESET)
    print(C.YELLOW + "\n  CREDITS\n" + C.RESET)
    print(C.WHITE  + "  Entwicklung & Konzept" + C.RESET)
    print(C.NEON   + "    Chaoswerk" + C.RESET)
    print()
    print(C.WHITE  + "  Engine & KI-Unterstützung" + C.RESET)
    print(C.GRAY   + "    Claude (Anthropic)  —  claude.ai" + C.RESET)
    print()
    print(C.WHITE  + "  Zertifizierungsstandard" + C.RESET)
    print(C.GRAY   + "    Linux Professional Institute  —  lpi.org" + C.RESET)
    print(C.GRAY   + "    Linux Version 5.0  (Exams 101 + 102)" + C.RESET)
    print()
    print(C.WHITE  + "  Technologie" + C.RESET)
    print(C.GRAY   + "    Python 3.10+  —  pure stdlib  —  keine Dependencies" + C.RESET)
    print(C.GRAY   + "    ANSI-Escape-Codes  —  Terminal-native Rendering" + C.RESET)
    print()
    print(C.CYAN + "  " + "─" * 66 + C.RESET)
    print()
    print(C.NEON   + "  Powered by Chaoswerk" + C.RESET)
    print(C.GRAY   + "  NeonGrid-9 ist freie Lern-Software." + C.RESET)
    print(C.GRAY   + '  "Knowledge is the only weapon they cannot take from you."' + C.RESET)
    print()
    prompt_continue()


# ══════════════════════════════════════════════════════════════════════════════
# GAME HUB — Hauptspiel-Interface
# ══════════════════════════════════════════════════════════════════════════════

def game_hub():
    """Haupt-Hub während des Spielens."""
    while GAME.running and GAME.player:
        player = GAME.player

        clear()
        print(C.NEON + "\n  NEONGRID-9 — OPERATIONS HUB\n" + C.RESET)

        # Status
        xp_bar(
            player.xp, player.level,
            player.get_current_level_xp(),
            player.get_next_level_xp()
        )
        print(C.GRAY + f"  {player.name}  ::  {player.level_title}" + C.RESET)
        print()

        # Fraktions-Status kompakt
        factions_line = "  "
        for faction, rep in player.reputation.items():
            if rep > 0:
                short = faction.split()[0][:3].upper()
                factions_line += C.MAGENTA + f"{short}:{rep} " + C.RESET
        if factions_line.strip():
            print(factions_line)
            print()

        # Missionsfortschritt pro Kapitel
        print(C.WHITE + "  MISSIONEN\n" + C.RESET)
        for ch_id, ch_missions, ch_topic, ch_title, ch_sub in CHAPTERS:
            completed = sum(
                1 for m in ch_missions if player.mission_completed(m.mission_id)
            )
            total = len(ch_missions)
            pct   = int(completed / total * 20) if total else 0
            bar   = C.SUCCESS + "█" * pct + C.GRAY + "░" * (20 - pct) + C.RESET
            lock  = ""
            print(f"  {C.CYAN}[{ch_id}]{C.RESET}  Kap.{ch_id}: {ch_title:<16}  {bar}  "
                  f"{C.YELLOW}{completed:>2}/{total}{C.RESET}{lock}")
        print()
        print(C.WHITE + "  KAPITEL\n" + C.RESET)
        print(C.CYAN  + "  [1-18]" + C.RESET + "  Kapitel auswählen")
        print(C.CYAN  + "  [all]" + C.RESET + "   Alle Missionen im Kapitel spielen")
        print()
        print(C.WHITE + "  AKTIONEN\n" + C.RESET)
        print(C.CYAN  + "  [s]" + C.RESET + "  Charakterstatus")
        print(C.CYAN  + "  [i]" + C.RESET + "  Inventar & Gear")
        print(C.CYAN  + "  [r]" + C.RESET + "  Linux Readiness Report")
        print(C.CYAN  + "  [x]" + C.RESET + "  Review Mode (Spaced Repetition)")
        print(C.CYAN  + "  [e]" + C.RESET + "  Exam Mode — 90 Min Prüfungssimulation")
        print(C.CYAN  + "  [v]" + C.RESET + "  Speichern")
        print(C.GRAY  + "  [q]" + C.RESET + "  Hauptmenü")
        print()

        choice = prompt_input("hub").lower()

        if choice == "1":
            chapter_menu(1)
        elif choice == "2":
            chapter_menu(2)
        elif choice == "3":
            chapter_menu(3)
        elif choice == "4":
            chapter_menu(4)
        elif choice == "5":
            chapter_menu(5)
        elif choice == "6":
            chapter_menu(6)
        elif choice == "7":
            chapter_menu(7)
        elif choice == "8":
            chapter_menu(8)
        elif choice == "9":
            chapter_menu(9)
        elif choice == "10":
            chapter_menu(10)
        elif choice == "11":
            chapter_menu(11)
        elif choice == "12":
            chapter_menu(12)
        elif choice == "13":
            chapter_menu(13)
        elif choice == "14":
            chapter_menu(14)
        elif choice == "15":
            chapter_menu(15)
        elif choice == "16":
            chapter_menu(16)
        elif choice == "17":
            chapter_menu(17)
        elif choice == "18":
            chapter_menu(18)
        elif choice in ("s", "status"):
            show_player_status()
        elif choice in ("i", "inv", "inventar"):
            show_inventory()
        elif choice in ("r", "readiness", "report"):
            show_linux_readiness()
        elif choice in ("x", "review"):
            review_mode()
        elif choice in ("e", "exam"):
            timed_exam_mode()
        elif choice in ("v", "save", "speichern"):
            GAME.save()
            show_success("Gespeichert!")
            time.sleep(0.8)
        elif choice in ("q", "quit", "exit"):
            GAME.save()
            GAME.running = False
            break


def chapter_menu(ch_id: int):
    """Generisches Kapitel-Missionsmenü für alle Kapitel."""
    # Kapitel-Daten nachschlagen
    ch_data = next((c for c in CHAPTERS if c[0] == ch_id), None)
    if not ch_data:
        show_error(f"Kapitel {ch_id} nicht gefunden.")
        return

    _, ch_missions, ch_topic, ch_title, ch_sub = ch_data
    runner = MissionRunner(GAME.player, save_callback=GAME.auto_save)
    prefix = str(ch_id) + "."

    while True:
        chapter_header(ch_id, ch_title, f"Linux Topic {ch_topic} — {ch_sub}")

        player = GAME.player
        print(C.WHITE + "  Missionen:\n" + C.RESET)

        for mission in ch_missions:
            done   = player.mission_completed(mission.mission_id)
            status = C.SUCCESS + "✓" + C.RESET if done else C.GRAY + "○" + C.RESET
            id_str = f"{mission.mission_id:>7}"
            if mission.mtype == "BOSS":
                tc = C.DANGER
            elif done:
                tc = C.GRAY
            else:
                tc = C.WHITE
            print(f"  {status} {C.GRAY}{id_str}{C.RESET}  {tc}{mission.title[:44]:<44}{C.RESET}  "
                  f"{C.YELLOW}+{mission.xp:>3}XP{C.RESET}")

        done_count  = sum(1 for m in ch_missions if player.mission_completed(m.mission_id))
        total_count = len(ch_missions)
        print()
        extra = ""
        if ch_id == 18:
            extra = C.YELLOW + "  [exam] = Timed Exam Mode (90 Min)\n" + C.RESET
        print(extra + C.GRAY + f"  Fortschritt: {done_count}/{total_count}  |  "
              f"Mission-ID (z.B. {ch_id}.03)  |  'all' = alle spielen  |  'q' = zurück" + C.RESET)
        print()

        choice = prompt_input(f"kap{ch_id}").lower().strip()

        if choice in ("q", "quit", "back"):
            break

        elif choice in ("exam", "e") and ch_id == 18:
            timed_exam_mode()

        elif choice == "all":
            for mission in ch_missions:
                if not player.mission_completed(mission.mission_id):
                    runner.run(mission)
                    GAME.save()

        elif choice.startswith(prefix) or choice == f"{ch_id}.boss":
            mission_map = {m.mission_id.lower(): m for m in ch_missions}
            if "boss" in choice:
                key = f"{ch_id}.boss"
            else:
                key = choice
            mission = mission_map.get(key)
            if mission:
                runner.run(mission)
                GAME.save()
            else:
                show_error(f"Mission '{choice}' nicht gefunden.")
                time.sleep(0.8)

        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(ch_missions):
                runner.run(ch_missions[idx])
                GAME.save()
            else:
                show_error("Index außerhalb des Bereichs.")
                time.sleep(0.8)
        else:
            show_error(f"'{choice}' nicht erkannt. Nutze die Mission-ID (z.B. {ch_id}.03)")
            time.sleep(0.8)

        # Kapitel-Abschluss prüfen
        if all(player.mission_completed(m.mission_id) for m in ch_missions):
            _show_chapter_complete(ch_id, ch_title, ch_topic)
            break


def _show_chapter_complete(ch_id: int, ch_title: str, ch_topic: str):
    """Kapitel-Abschluss Screen."""
    clear()
    print(C.SUCCESS + """
  ██████╗██╗  ██╗ █████╗ ██████╗ ████████╗███████╗██████╗
 ██╔════╝██║  ██║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
 ██║     ███████║███████║██████╔╝   ██║   █████╗  ██████╔╝
 ██║     ██╔══██║██╔══██║██╔═══╝    ██║   ██╔══╝  ██╔══██╗
 ╚██████╗██║  ██║██║  ██║██║        ██║   ███████╗██║  ██║
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝
    """ + C.RESET)
    print(C.NEON + f"  KAPITEL {ch_id} — {ch_title} — ABGESCHLOSSEN!\n" + C.RESET)

    # Kapitelspezifisches Recap
    recap_map = {
        1: [
            "lspci / lsusb / lshw / dmidecode",
            "dmesg / journalctl -k",
            "lsblk / blkid / udevadm",
            "lsmod / modinfo / modprobe",
            "/proc/interrupts + /proc/ioports + /proc/iomem",
            "/sys/firmware/efi — UEFI-Erkennung",
            "coldplug vs hotplug",
        ],
        2: [
            "POST → MBR/GPT → GRUB2 → Kernel → initramfs",
            "grub.cfg / /etc/default/grub / update-grub",
            "grub-install / grub-mkconfig",
            "Kernel-Parameter (quiet, splash, ro, single)",
            "/proc/cmdline — geladene Kernel-Argumente",
            "initramfs: mkinitramfs / update-initramfs",
            "efibootmgr — UEFI Boot-Einträge",
        ],
        3: [
            "SysVinit: Runlevels 0-6 / telinit / /etc/inittab",
            "systemd: Units, Targets, systemctl",
            "systemctl start/stop/restart/reload/enable/disable",
            "systemctl get-default / set-default / isolate",
            "journalctl -u / -b / -p / -f / --since",
            "systemd-analyze blame — Boot-Performance",
            "mask/unmask — Dienste permanent sperren",
        ],
        4: [
            "MBR (4 Primär, 2TB) vs GPT (128 Partitionen)",
            "fdisk -l / gdisk / parted — Partitions-Tools",
            "mkfs.ext4 / mkfs.xfs / mkfs.vfat — Dateisysteme erstellen",
            "ext2/3/4: Unterschiede + tune2fs / e2fsck",
            "XFS: xfs_growfs /mountpoint (nicht Device!)",
            "/etc/fstab: 6 Felder, pass 0/1/2",
            "mount -a / umount / df -h / du -sh",
            "LVM: pvcreate → vgcreate → lvcreate → lvextend",
        ],
        5: [
            "rwx-Oktal: r=4, w=2, x=1. 755=rwxr-xr-x",
            "chmod 755 / chmod u+x / chmod -R",
            "chown user:group / chgrp",
            "umask: Datei=666-umask, Verzeichnis=777-umask",
            "SUID=4xxx (s/S), SGID=2xxx, Sticky=1xxx (t/T)",
            "Hard Links: gleiche Inode. Symlinks: ln -s, Pfadzeiger",
            "find: -name -type -perm -mtime -user -exec",
            "FHS: /etc /var/log /tmp /usr/local /proc /sys",
        ],
        6: [
            "Umgebungsvariablen: export, env, printenv, $PATH, $?",
            "I/O Redirection: > >> < 2> 2>&1 &> /dev/null",
            "Pipes: | und tee (Terminal + Datei gleichzeitig)",
            "grep: -i -v -n -r -A -B -C. egrep=grep -E",
            "cut -d -f / sort -n -r -k / uniq -c / wc -l",
            "head / tail -f (live) / cat -n / less",
            "tr 'A-Z' 'a-z' / sed 's/alt/neu/g' / sed -i",
            "awk -F: '{print $1}' / $NF / NR / Muster",
        ],
        7: [
            "ps aux / ps -ef — laufende Prozesse anzeigen",
            "top / htop — interaktiv, load average 1/5/15min",
            "kill -9 PID / killall name / pkill pattern",
            "Signale: SIGHUP=1, SIGINT=2, SIGKILL=9, SIGTERM=15",
            "Jobs: & (Hintergrund), fg, bg, jobs, nohup",
            "nice -n 10 cmd / renice -n 5 -p PID (−20..+19)",
            "free -h / vmstat / iostat — Ressourcen-Monitoring",
            "lsof -i :PORT / fuser -k /mountpoint",
        ],
        8: [
            "Regex Metazeichen: . * ^ $ [ ] + ? | ( ) { }",
            "BRE (grep) vs ERE (grep -E / egrep) — + ? | brauchen kein \\",
            "grep -i -v -n -c -r -A -B -C — wichtige Flags",
            "sed 's/alt/neu/g' — global ersetzen | sed -i In-Place",
            "awk -F: '{print $1}' — Felder | NR NF $NF BEGIN END",
            "POSIX-Klassen: [[:digit:]] [[:alpha:]] [[:space:]]",
            "vi-Modi: Normal (ESC), Insert (i/a/o), Command (:)",
            "vi: dd=delete, yy=yank, p=paste, u=undo, :%s/x/y/g",
        ],
        9: [
            "TCP/IP: A=8bit, B=16bit, C=24bit | /24=254 Hosts",
            "Private IPs: 10.x/8, 172.16-31.x/12, 192.168.x/16",
            "ip addr show / ip route show / ip link set eth0 up",
            "ss -tulpn — TCP+UDP lauschend, Prozesse, numerisch",
            "DNS: A=IPv4, AAAA=IPv6, MX=Mail, PTR=Reverse, CNAME=Alias",
            "dig +short HOST | dig -x IP | dig @DNS HOST",
            "ping -c 4 HOST | traceroute HOST | tracepath HOST",
            "ssh-keygen -t ed25519 | ssh-copy-id | authorized_keys",
        ],
        10: [
            "/etc/passwd: user:x:UID:GID:GECOS:home:shell (7 Felder)",
            "UID 0=root, 1-999=System, 1000+=normaler User",
            "useradd -m -s /bin/bash USER | usermod -aG GROUP USER",
            "usermod -aG (append!) vs usermod -G (replace!) — kritisch!",
            "visudo = EINZIGER sicherer Weg für /etc/sudoers",
            "chage -l/-M/-m/-W/-E — Passwort-Aging",
            "PAM: /etc/pam.d/ | Typen: auth account password session",
            "Login-Shell: ~/.bash_profile | Non-Login: ~/.bashrc",
        ],
        11: [
            "Syslog Severity: 0=emerg 1=alert 2=crit 3=err 4=warn 5=notice 6=info 7=debug",
            "rsyslog: facility.severity /var/log/datei | /etc/rsyslog.d/",
            "journalctl -u UNIT -p LEVEL --since TIME -b BOOT -f",
            "logrotate: daily/weekly/monthly, rotate N, compress, postrotate",
            "crontab: MIN STD TAG MON WOT BEFEHL (5 Zeit-Felder)",
            "/etc/crontab = 6 Felder (+ USER). /etc/cron.d/ = Fragmente",
            "@reboot @daily @weekly — cron Sonderwörter",
            "at ZEIT | atq (= at -l) | atrm NR (= at -d)",
        ],
        12: [
            "dpkg: -i=install -r=remove -P=purge -l=list -L=files -S=search",
            "apt update (Listen) → apt upgrade (Pakete) | apt purge = alles weg",
            "apt-cache search/show/depends/policy | /etc/apt/sources.list",
            "rpm: -ivh=install -e=remove -qa=all -ql=files -qf=file -qi=info",
            "yum/dnf install/remove/search/update/provides — RPM mit Deps",
            "zypper in/rm/se — SUSE-Paketmanager (rpm-basiert)",
            "ldd /binary = Library-Deps | ldconfig = Cache aktualisieren",
            "/etc/ld.so.conf | /etc/ld.so.cache | LD_LIBRARY_PATH",
        ],
        13: [
            "lsmod | modinfo MOD | modprobe MOD (mit Deps!) | rmmod MOD",
            "modprobe vs insmod: modprobe löst Abhängigkeiten auf!",
            "Blacklist: 'blacklist MOD' in /etc/modprobe.d/blacklist.conf",
            "/proc: cpuinfo meminfo version cmdline loadavg modules",
            "uname: -r=release -a=all -m=arch -s=sysname -n=nodename",
            "sysctl -w=sofort, sysctl -p=/etc/sysctl.conf laden (dauerhaft)",
            "udevadm info/monitor/control --reload-rules | /etc/udev/rules.d/",
            "dmesg -T (Zeitstempel) | journalctl -k | /boot/vmlinuz-VERSION",
        ],
        15: [
            "find / -perm -4000 -type f 2>/dev/null — SUID-Dateien finden",
            "find / -perm -2000 (SGID) | find / -perm /6000 (SUID oder SGID)",
            "/etc/ssh/sshd_config: PermitRootLogin no + PasswordAuthentication no",
            "sshd -t = Syntax-Check | systemctl restart sshd nach Änderung",
            "gpg -e -r 'Name' datei | gpg -d datei.gpg | gpg --list-keys",
            "gpg --sign | gpg --verify | gpg --fingerprint | gpg --export -a",
            "fail2ban: jail.local | maxretry/bantime/findtime | fail2ban-client status sshd",
            "visudo! nie /etc/sudoers direkt | sudo -l | /etc/sudoers.d/ für Fragmente",
            "openssl enc -aes-256-cbc | openssl enc -d (decrypt) | openssl dgst -sha256",
            "LUKS: luksFormat → luksOpen → mkfs → mount → luksClose",
            "iptables -L -n -v | -A append | -I insert | -D delete | iptables-save",
            "Incident Response: last/lastb → isolieren → Logs → analysieren → härten",
        ],
        16: [
            "locale / locale -a / localectl set-locale LANG=de_DE.UTF-8",
            "LC_ALL überschreibt alle LC_*-Variablen — höchste Priorität",
            "iconv -f ISO-8859-1 -t UTF-8 datei.txt > neu.txt",
            "timedatectl set-timezone Europe/Berlin | /etc/localtime = Symlink",
            "ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime",
            "DISPLAY=:0 lokal | ssh -X/-Y für X11-Forwarding | xauth = Cookies",
            "X Server = Hardware | X Client = App | Window Manager = Fensterrahmen",
            "GDM (GNOME) / SDDM (KDE) / LightDM — Display Manager = Login-Screen",
            "graphical.target = GUI-Boot | multi-user.target = CLI-Boot",
            "lpr/lp drucken | lpq Warteschlange | lprm/cancel entfernen | lpstat -p",
            "cupsenable/-disable | cupsaccept/-reject | /etc/cups/cupsd.conf",
            "AT-SPI2 = Accessibility-Framework | Orca = Screenreader",
        ],
        17: [
            "Login-Shell: /etc/profile → /etc/profile.d/*.sh → ~/.bash_profile",
            "Non-Login interaktiv: /etc/bash.bashrc → ~/.bashrc",
            "source ~/.bashrc = Datei in aktuelle Shell laden (. ist POSIX-Alias)",
            "export VAR=wert → an Kind-Prozesse vererbt | VAR=wert = nur aktuelle Shell",
            "env = exportierte Vars | set = alle Vars+Funktionen | printenv = wie env",
            "PATH: links hat höhere Priorität | '.' niemals in PATH!",
            "hash -r nach PATH-Änderung | type -a befehl = alle Treffer",
            "alias ll='ls -la' | unalias ll | \\ll = Alias umgehen",
            "type: alias/builtin/function/file — wichtigster Diagnose-Befehl",
            "!! = letzter Befehl | !42 = #42 | !$ = letztes Arg | Ctrl+R = Suche",
            "HISTCONTROL=ignoreboth (ignoredups+ignorespace)",
            "PS1: \\u=User \\h=Host \\w=Pfad \\$=$ oder # | PS2=Fortsetzungsprompt",
        ],
        18: [
            "Linux: 2 Prüfungen (101 + 102) | je 90 Minuten | 500/800 Punkte zum Bestehen",
            "Exam 101: Hardware, Boot, Kernel, Pakete, Shell, Dateisysteme",
            "Exam 102: Scripting, Desktop, User, Logs, Netzwerk, Sicherheit",
            "Prüfungs-Anmeldung: lpi.org | Gültigkeitsdauer: 5 Jahre",
            "60 Fragen pro Exam | Multiple Choice + Fill-in + Multiple Answer",
            "Topic 101: lspci lsusb dmidecode | grub-mkconfig | systemd-targets",
            "Topic 103: grep sed awk | SIGKILL=9 | nice -20=höchste Prio",
            "Topic 104: mkfs.ext4 | chmod 750 | df -h | /etc/fstab | Hard Link = Inode",
            "Topic 107: useradd -m | /etc/shadow | chage -l | crontab */15",
            "Topic 109: ip route | ss -tulpn | authorized_keys | ssh -L Forwarding",
            "Topic 110: find -perm -4000 | PermitRootLogin no | gpg -d | visudo",
            "Du hast alle 18 Kapitel abgeschlossen — Linux bereit!",
        ],
        19: [
            "Namespaces: PID NET MNT UTS IPC USER CGROUP — Isolation für Container",
            "unshare --pid --fork --mount-proc /bin/bash — neue Namespace-Shell",
            "nsenter -t PID --pid --net --mnt -- bash — in laufenden Namespace einsteigen",
            "cgroups v2: /sys/fs/cgroup/ | systemd-run --scope --property=MemoryMax=",
            "chroot /new/root /bin/bash — Dateisystem-Wurzel wechseln",
            "systemd-nspawn -D /container -b — leichtgewichtiger Container (wie lite Docker)",
            "machinectl list/start/stop/shell — systemd-nspawn-Maschinen verwalten",
            "cloud-init: user-data, meta-data | /var/lib/cloud/ | cloud-init status --wait",
            "KVM/QEMU: virsh list --all | virsh start/stop/snapshot | virt-manager",
            "D-Bus: busctl list | machine-id: /etc/machine-id (eindeutige Instanz-ID)",
            "AppArmor: aa-status | aa-enforce/aa-complain | /etc/apparmor.d/",
            "SELinux: getenforce/setenforce | ls -Z | chcon -t TYPE | restorecon",
            "systemd Drop-ins: /etc/systemd/system/unit.d/override.conf",
            "systemd-resolved: resolvectl status | /etc/systemd/resolved.conf",
        ],
        14: [
            "Shebang: #!/bin/bash — erste Zeile, macht Datei zum Skript",
            "chmod +x script.sh | bash -x (debug) | bash -n (syntax check)",
            "set -e (exit on error) | set -u (unset vars = error) | set -euo pipefail",
            "$1 $2 ... $# $@ $* $? $$ $0 — Spezialvariablen auswendig!",
            "Expansion: ${VAR:-default} ${VAR:=assign} ${#VAR} ${VAR#prefix}",
            "test -e -f -d -r -w -x -z -n | [ ] vs [[ ]] — Leerzeichen wichtig!",
            "for i in LIST; while COND; until COND — break/continue",
            "IFS= read -r line < file — sicheres Zeilenlesen",
            "func() { } | local VAR | return CODE — Funktionen & Scope",
            "case $VAR in pattern) ;; esac — elegante Mehrfachverzweigung",
            "$(( expr )) | let | expr | bc — Arithmetik in Bash",
            "getopts 'hvf:' OPT — $OPTARG $OPTIND — Optionen parsen",
        ],
        19: [
            "docker run/exec/ps/rm/rmi/build — Container-Lebenszyklus",
            "podman run --userns=keep-id — rootless Container",
            "systemd-nspawn -D /path — leichtgewichtige Container",
            "virsh list/start/shutdown/destroy — KVM-VMs steuern",
            "docker volume create | docker network ls — Storage & Netzwerk",
            "OverlayFS: lowerdir=/ upperdir= workdir= — Layer-Filesystem",
            "capsh --print | getcap/setcap — Linux Capabilities",
            "cgroups v2: /sys/fs/cgroup/ — Ressourcenlimits",
        ],
        20: [
            "iptables -A/-I/-D/-F -t filter/nat/mangle — Regeln verwalten",
            "iptables -t nat -A POSTROUTING -j MASQUERADE — NAT/IP-Forwarding",
            "nft add table/chain/rule — nftables Syntax",
            "firewall-cmd --zone=public --add-service=http --permanent",
            "conntrack -L — Connection Tracking Status",
            "tcpdump -i eth0 port 80 -w capture.pcap — Paketmitschnitt",
            "openvpn --config server.conf | wg-quick up wg0 — VPN",
            "fail2ban-client status sshd — IDS/IPS Schutz",
            "lynis audit system — CIS-Hardening Scanner",
        ],
        21: [
            "mount -t nfs server:/export /mnt | /etc/exports — NFS",
            "smbclient -L //server | mount -t cifs — Samba/CIFS",
            "dhclient -v eth0 | /etc/dhcp/dhcpd.conf — DHCP DORA",
            "dig @8.8.8.8 example.com MX +trace — DNS-Abfragen",
            "ldapsearch -x -H ldap:// -b dc=example — LDAP",
            "/etc/nsswitch.conf: passwd: files ldap — Name Resolution",
            "chronyc tracking | timedatectl — NTP-Synchronisation",
            "nmcli con add/mod/up/down — NetworkManager CLI",
            "ip link add bond0 type bond | bridge — Bonding & Bridges",
        ],
        22: [
            "mdadm --create /dev/md0 --level=5 --raid-devices=3 — RAID",
            "mdadm --manage /dev/md0 --add /dev/sdd — RAID-Recovery",
            "pvcreate/vgcreate/lvcreate — LVM-Stack aufbauen",
            "lvcreate -s -n snap -L 1G /dev/vg/lv — LVM-Snapshot",
            "lvcreate --thin -V 10G --name lv vg/pool — Thin Provisioning",
            "edquota -u user | repquota -a — Disk Quotas",
            "btrfs subvolume create/snapshot/list — btrfs-Subvolumes",
            "iscsiadm -m discovery -t st -p server — iSCSI-Client",
            "smartctl -a /dev/sda | e2fsck -f — Disk-Health & Repair",
        ],
    }
    recap = recap_map.get(ch_id, [f"Topic {ch_topic} abgeschlossen"])
    print(C.WHITE + "  Du kennst jetzt:\n" + C.RESET)
    for item in recap:
        print(C.GREEN + f"  ✓  {item}" + C.RESET)
    print()
    print(C.YELLOW + f"  ╔═[ Linux STATUS ]" + C.RESET)
    print(C.YELLOW + f"  ║  Topic {ch_topic}: ABGESCHLOSSEN ✓" + C.RESET)
    # Nächstes Kapitel anzeigen
    next_ch = next((c for c in CHAPTERS if c[0] == ch_id + 1), None)
    if next_ch:
        print(C.YELLOW + f"  ║  Nächstes: Kapitel {next_ch[0]} — {next_ch[3]}" + C.RESET)
    print(C.YELLOW + "  ╚═" + C.RESET)
    print()
    prompt_continue()


def show_player_status():
    """Spieler-Status anzeigen."""
    clear()
    print(C.NEON + "\n  GHOST PROFILE\n" + C.RESET)
    print(GAME.player.stats_summary())
    print()
    prompt_continue()


def show_linux_readiness():
    """Linux Readiness Report — pro Topic, Quiz-Genauigkeit, Gesamtbewertung."""
    clear()
    player = GAME.player
    print(C.NEON + "\n  Linux READINESS REPORT\n" + C.RESET)
    print(C.GRAY + "  ─" * 35 + C.RESET)

    total_missions = sum(len(m) for _, m, *_ in CHAPTERS)
    done_missions  = sum(
        1 for _, ch_m, *_ in CHAPTERS
        for m in ch_m if player.mission_completed(m.mission_id)
    )
    overall_pct = int(done_missions / total_missions * 100) if total_missions else 0

    total_xp_possible = sum(
        sum(mi.xp for mi in ch_m) for _, ch_m, *_ in CHAPTERS
    )

    print(f"\n  {C.WHITE}GESAMT-FORTSCHRITT{C.RESET}")
    prog_bar_w = 40
    filled = int(overall_pct / 100 * prog_bar_w)
    bar = C.SUCCESS + "█" * filled + C.GRAY + "░" * (prog_bar_w - filled) + C.RESET
    print(f"  {bar}  {C.YELLOW}{overall_pct}%{C.RESET}")
    print(f"  {done_missions}/{total_missions} Missionen  |  "
          f"{player.xp:,} / {total_xp_possible:,} XP\n")

    print(C.GRAY + "  ─" * 35 + C.RESET)
    print(f"\n  {C.WHITE}PER-KAPITEL STATUS{C.RESET}\n")
    print(f"  {'#':<3} {'Titel':<18} {'Topic':<7} {'Miss':>5} {'XP%':>5} {'Quiz':>6}  {'Status'}")
    print(C.GRAY + "  " + "─" * 62 + C.RESET)

    weak_topics = []
    for ch_id, ch_missions, ch_topic, ch_title, _ in CHAPTERS:
        ch_done  = sum(1 for m in ch_missions if player.mission_completed(m.mission_id))
        ch_total = len(ch_missions)
        ch_xp_done = sum(
            mi.xp for mi in ch_missions if player.mission_completed(mi.mission_id)
        )
        ch_xp_total = sum(mi.xp for mi in ch_missions)
        xp_pct = int(ch_xp_done / ch_xp_total * 100) if ch_xp_total else 0

        accuracy = player.quiz_accuracy(ch_id)
        acc_str  = f"{int(accuracy * 100):3d}%" if player.chapter_quiz_stats.get(str(ch_id)) else "  --"

        if ch_done == ch_total:
            status_color = C.SUCCESS
            status = "✓ DONE"
        elif ch_done > 0:
            status_color = C.YELLOW
            status = f"~ {ch_done}/{ch_total}"
        else:
            status_color = C.GRAY
            status = "○ OFFEN"

        acc_color = C.RESET
        if player.chapter_quiz_stats.get(str(ch_id)):
            if accuracy < 0.6:
                acc_color = C.DANGER
                weak_topics.append((ch_id, ch_title, ch_topic, int(accuracy * 100)))
            elif accuracy < 0.8:
                acc_color = C.YELLOW

        print(f"  {C.CYAN}{ch_id:>2}{C.RESET}  {ch_title:<18} {C.GRAY}{ch_topic:<7}{C.RESET} "
              f"{ch_done:>2}/{ch_total:<2}  {xp_pct:>3}%  "
              f"{acc_color}{acc_str}{C.RESET}  {status_color}{status}{C.RESET}")

    # Gesamtbewertung
    print(C.GRAY + "\n  ─" * 35 + C.RESET)
    total_asked   = sum(v["asked"]   for v in player.chapter_quiz_stats.values())
    total_correct = sum(v["correct"] for v in player.chapter_quiz_stats.values())
    overall_acc   = int(total_correct / total_asked * 100) if total_asked else 0

    readiness_score = int(overall_pct * 0.5 + overall_acc * 0.5)
    if readiness_score >= 80:
        r_color, r_verdict = C.SUCCESS, "Linux BEREIT ✓"
    elif readiness_score >= 62:
        r_color, r_verdict = C.YELLOW,  "FAST BEREIT — weiter üben"
    else:
        r_color, r_verdict = C.DANGER,  "MEHR TRAINING NÖTIG"

    print(f"\n  {C.WHITE}GESAMTBEWERTUNG{C.RESET}")
    print(f"  Quiz-Genauigkeit : {overall_acc}%  ({total_correct}/{total_asked} korrekt)")
    print(f"  Fortschritt      : {overall_pct}%")
    print(f"  Readiness-Score  : {r_color}{readiness_score}/100 — {r_verdict}{C.RESET}")

    if weak_topics:
        print(f"\n  {C.DANGER}SCHWACHE TOPICS (< 60% Quiz-Genauigkeit):{C.RESET}")
        for ch_id, title, topic, acc in weak_topics:
            print(f"  {C.WARN}  ► Kap.{ch_id} {title} ({topic}) — {acc}% Genauigkeit{C.RESET}")
        print(f"\n  {C.CYAN}  Tipp: [x] Review Mode zum gezielten Wiederholen{C.RESET}")

    print()
    prompt_continue()


def timed_exam_mode():
    """Linux Prüfungssimulation — 90 Minuten, 60 Fragen, LPIC-Scoring."""
    clear()
    player = GAME.player
    EXAM_LIMIT = 90 * 60  # 5400 Sekunden

    print(C.NEON + "\n  Linux PRÜFUNGSSIMULATION\n" + C.RESET)
    print(C.CYAN + "  " + "─" * 60 + C.RESET)
    print(f"\n  {C.WHITE}Regelwerk:{C.RESET}")
    print(f"  {C.GRAY}• 60 Fragen aus allen Linux Topics")
    print(f"  • 90 Minuten Zeitlimit")
    print(f"  • Bestehensgrenze: 500 / 800 Punkte (62,5%)")
    print(f"  • Jede richtige Antwort = ~13 Punkte")
    print(f"  • Timer läuft pro Frage — keine Pause{C.RESET}\n")
    print(C.YELLOW + "  Gear-Boni aktiv:" + C.RESET)
    quiz_bonus = player.gear_bonus("quiz_xp")
    if quiz_bonus > 1.0:
        print(C.GREEN + f"  ✓ Ghost Mask: +{int((quiz_bonus-1)*100)}% Quiz-XP" + C.RESET)
    if "linux_badge" in player.inventory:
        print(C.YELLOW + "  ✓ Linux Badge: +5% auf alle XP" + C.RESET)
    print()
    print(C.DANGER + "  [ENTER] Prüfung starten  |  [q] Abbrechen\n" + C.RESET)

    go = prompt_input("starten").lower()
    if go == "q":
        return

    # Alle ch22-Quiz-Fragen sammeln (Blöcke 22.01–22.26)
    from missions.ch22_exam import CHAPTER_22_MISSIONS
    import random
    letters = ["A", "B", "C", "D"]

    exam_blocks = [m for m in CHAPTER_22_MISSIONS if m.quiz_questions]
    all_questions = []
    for block in exam_blocks:
        for q in block.quiz_questions:
            all_questions.append((block.title, q))

    # Leichte Zufalls-Mischung innerhalb der Blöcke (realistischer)
    random.shuffle(all_questions)

    # Exam-Start
    exam_start   = time.time()
    correct_list = []   # True/False pro Frage
    block_scores = {b.mission_id: {"correct": 0, "total": 0} for b in exam_blocks}

    clear()
    print(C.NEON + "\n  ╔══════════════════════════════════════════════════╗")
    print(         "  ║   Linux EXAM — START                           ║")
    print(         "  ║   90 Minuten | 60 Fragen | 500/800 zum Bestehen ║")
    print(         "  ╚══════════════════════════════════════════════════╝\n" + C.RESET)
    time.sleep(1.5)

    for q_num, (block_title, q) in enumerate(all_questions, 1):
        elapsed  = int(time.time() - exam_start)
        remain   = max(0, EXAM_LIMIT - elapsed)
        r_mm, r_ss = divmod(remain, 60)
        e_mm, e_ss = divmod(elapsed, 60)

        # Zeit abgelaufen?
        if remain == 0:
            print(C.DANGER + "\n  ⏱  ZEIT ABGELAUFEN! Prüfung wird ausgewertet...\n" + C.RESET)
            time.sleep(1.5)
            break

        t_color = C.DANGER if remain < 300 else C.YELLOW if remain < 900 else C.GREEN
        progress_pct = int(q_num / len(all_questions) * 30)
        prog_bar = C.SUCCESS + "█" * progress_pct + C.GRAY + "░" * (30 - progress_pct) + C.RESET

        clear()
        print(f"  {C.NEON}Linux EXAM{C.RESET}   "
              f"{prog_bar}  "
              f"{C.YELLOW}Frage {q_num:>2}/60{C.RESET}   "
              f"{t_color}⏱ {r_mm:02d}:{r_ss:02d}{C.RESET}")
        print(C.GRAY + f"  {block_title}" + C.RESET)
        print(C.CYAN + "  " + "─" * 62 + C.RESET)

        print(C.WHITE + f"\n  {q.question}\n" + C.RESET)
        for idx, opt in enumerate(q.options):
            print(C.GRAY + f"    {letters[idx]}) {opt}" + C.RESET)
        print()

        correct_letter = letters[q.correct] if isinstance(q.correct, int) else q.correct

        answer = prompt_input("antwort [A/B/C/D]").upper().strip()
        while answer not in ("A", "B", "C", "D"):
            answer = prompt_input("antwort [A/B/C/D]").upper().strip()

        is_correct = (answer == correct_letter)
        correct_list.append(is_correct)
        player.record_quiz_result(18, is_correct)

        if is_correct:
            player.correct_first_try += 1
            print(C.SUCCESS + "  ✓ RICHTIG" + C.RESET)
        else:
            correct_opt = q.options[
                q.correct if isinstance(q.correct, int) else letters.index(q.correct)
            ]
            print(C.DANGER + f"  ✗ FALSCH  → {correct_letter}) {correct_opt}" + C.RESET)

        player.total_quizzes += 1
        time.sleep(0.4)

    # ── Auswertung ────────────────────────────────────────────────────────────
    total_elapsed   = int(time.time() - exam_start)
    t_mm, t_ss      = divmod(total_elapsed, 60)
    answered         = len(correct_list)
    correct_count    = sum(correct_list)
    wrong_count      = answered - correct_count
    unanswered       = 60 - answered

    # Linux Punkte: 800 Punkte max, linear auf 60 Fragen gemappt
    # Punkte pro richtiger Antwort = 800/60 ≈ 13.33
    linux_score = int(correct_count * 800 / 60)
    passed     = linux_score >= 500
    accuracy   = int(correct_count / answered * 100) if answered else 0

    # XP für den Spieler
    xp_earned = correct_count * 15
    if quiz_bonus > 1.0:
        xp_earned = int(xp_earned * quiz_bonus)
    new_xp, leveled_up = player.add_xp(xp_earned)
    GAME.auto_save(player)

    clear()
    if passed:
        verdict_color = C.SUCCESS
        verdict_art = r"""
  ██████╗  █████╗ ███████╗███████╗██╗███████╗██████╗ ████████╗
  ██╔══██╗██╔══██╗██╔════╝██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝
  ██████╔╝███████║███████╗███████╗██║█████╗  ██████╔╝   ██║
  ██╔═══╝ ██╔══██║╚════██║╚════██║██║██╔══╝  ██╔══██╗   ██║
  ██║     ██║  ██║███████║███████║██║███████╗██║  ██║   ██║
  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝"""
    else:
        verdict_color = C.DANGER
        verdict_art = r"""
  ███╗   ██╗██╗ ██████╗██╗  ██╗████████╗
  ████╗  ██║██║██╔════╝██║  ██║╚══██╔══╝
  ██╔██╗ ██║██║██║     ███████║   ██║
  ██║╚██╗██║██║██║     ██╔══██║   ██║
  ██║ ╚████║██║╚██████╗██║  ██║   ██║
  ╚═╝  ╚═══╝╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝"""

    print(verdict_color + verdict_art + C.RESET)
    print()
    print(C.NEON + "  Linux PRÜFUNGSERGEBNIS\n" + C.RESET)
    print(C.CYAN + "  " + "─" * 54 + C.RESET)
    print(f"\n  {'Fragen beantwortet:':<26} {answered}/60")
    print(f"  {'Richtig:':<26} {C.SUCCESS}{correct_count}{C.RESET}")
    print(f"  {'Falsch:':<26} {C.DANGER}{wrong_count}{C.RESET}")
    if unanswered:
        print(f"  {'Nicht beantwortet:':<26} {C.GRAY}{unanswered}{C.RESET}")
    print(f"  {'Genauigkeit:':<26} {accuracy}%")
    print(f"  {'Prüfungszeit:':<26} {t_mm:02d}:{t_ss:02d} / 90:00")
    print()
    print(C.CYAN + "  " + "─" * 54 + C.RESET)

    score_bar_w = 40
    score_filled = int(linux_score / 800 * score_bar_w)
    pass_pos     = int(500 / 800 * score_bar_w)
    bar_chars    = list(C.GRAY + "░" * score_bar_w + C.RESET)
    score_bar    = ""
    for i in range(score_bar_w):
        if i < score_filled:
            score_bar += C.SUCCESS + "█"
        elif i == pass_pos:
            score_bar += C.YELLOW + "|"
        else:
            score_bar += C.GRAY + "░"
    score_bar += C.RESET

    print(f"\n  Linux PUNKTE:  {verdict_color}{linux_score:>3} / 800{C.RESET}  "
          f"(Bestehensgrenze: 500)")
    print(f"  {score_bar}")
    print(f"  {'0':>2}{'':>17}500{'':>15}800")

    if passed:
        print(C.SUCCESS + f"\n  ✓  BESTANDEN — Du würdest die echte Linux Prüfung bestehen!\n" + C.RESET)
    else:
        deficit = 500 - linux_score
        need    = int(deficit * 60 / 800) + 1
        print(C.DANGER + f"\n  ✗  NICHT BESTANDEN — {deficit} Punkte fehlen ({need} weitere korrekte Antworten)\n" + C.RESET)

    print(f"  {C.YELLOW}+{xp_earned} XP verdient{C.RESET}")
    if leveled_up:
        level_up_screen(player.level, player.level_title)

    print()
    prompt_continue()


def review_mode():
    """Spaced-Repetition lite — zufällige Quiz-Fragen aus schwachen Kapiteln."""
    import random
    clear()
    player  = GAME.player
    runner  = MissionRunner(player, GAME.auto_save)

    print(C.NEON + "\n  REVIEW MODE — GEZIELTE WIEDERHOLUNG\n" + C.RESET)

    # Alle Quiz-Fragen aus allen Kapiteln sammeln, mit Kapitel-Kontext
    pool: list[tuple] = []  # (chapter_id, topic, title, question)
    for ch_id, ch_missions, ch_topic, ch_title, _ in CHAPTERS:
        for mission in ch_missions:
            for q in mission.quiz_questions:
                pool.append((ch_id, ch_topic, ch_title, q))

    if not pool:
        print(C.GRAY + "  Keine Quiz-Fragen gefunden.\n" + C.RESET)
        prompt_continue()
        return

    # Schwache Kapitel bevorzugen (Gewichtung)
    def weight(ch_id):
        acc = player.quiz_accuracy(ch_id)
        if acc == 0.0:
            return 2   # Nicht gespielt → normal
        return max(1, int(10 * (1 - acc)))  # Schlechte Genauigkeit → höheres Gewicht

    weighted_pool = []
    for ch_id, ch_topic, ch_title, q in pool:
        w = weight(ch_id)
        weighted_pool.extend([(ch_id, ch_topic, ch_title, q)] * w)

    random.shuffle(weighted_pool)
    session = weighted_pool[:10]

    print(C.WHITE + f"  {len(session)} Fragen — bevorzugt aus schwachen Topics\n" + C.RESET)
    print(C.GRAY + "  [Enter] zum Starten\n" + C.RESET)
    prompt_continue()

    letters = ["A", "B", "C", "D"]
    correct_count = 0
    for i, (ch_id, ch_topic, ch_title, q) in enumerate(session, 1):
        clear()
        print(C.CYAN + f"  REVIEW {i}/{len(session)}  " +
              C.GRAY + f"│ Kap.{ch_id}: {ch_title}  [{ch_topic}]" + C.RESET + "\n")
        print(C.WHITE + f"  {q.question}\n" + C.RESET)
        for idx, opt in enumerate(q.options):
            print(C.GRAY + f"    {letters[idx]}) {opt}" + C.RESET)
        print()

        correct_letter = letters[q.correct] if isinstance(q.correct, int) else q.correct
        answer = prompt_input("antwort [A/B/C/D]").upper().strip()

        while answer not in ("A", "B", "C", "D"):
            answer = prompt_input("antwort [A/B/C/D]").upper().strip()

        if answer == correct_letter:
            show_success("RICHTIG!")
            correct_count += 1
            player.record_quiz_result(ch_id, True)
        else:
            correct_opt = q.options[q.correct if isinstance(q.correct, int) else letters.index(q.correct)]
            print(C.DANGER + f"  ✗  Falsch. Richtig: {correct_letter}) {correct_opt}" + C.RESET)
            player.record_quiz_result(ch_id, False)

        print(C.CYAN + f"  → {q.explanation}" + C.RESET)
        print()
        prompt_continue()

    # Session-Auswertung
    clear()
    pct = int(correct_count / len(session) * 100)
    print(C.NEON + "\n  REVIEW ABGESCHLOSSEN\n" + C.RESET)
    print(f"  Ergebnis: {correct_count}/{len(session)} richtig  ({pct}%)\n")
    if pct >= 80:
        print(C.SUCCESS + "  Ausgezeichnet! Du beherrschst diese Topics.\n" + C.RESET)
    elif pct >= 60:
        print(C.YELLOW + "  Gut, aber es gibt noch Lücken. Wiederholen!\n" + C.RESET)
    else:
        print(C.DANGER + "  Diese Topics brauchen mehr Aufmerksamkeit.\n" + C.RESET)

    GAME.auto_save(player)
    prompt_continue()


def show_inventory():
    """Inventar anzeigen."""
    from engine.player import RARITY_COLOR
    clear()
    player = GAME.player
    print(C.NEON + "\n  GEAR & INVENTORY\n" + C.RESET)

    rarity_order = {"legendary": 0, "rare": 1, "uncommon": 2, "common": 3}
    sorted_inv   = sorted(
        player.inventory,
        key=lambda i: rarity_order.get(GEAR_CATALOG.get(i, {}).get("rarity", "common"), 3)
    )

    if not sorted_inv:
        print(C.GRAY + "  Kein Gear vorhanden.\n" + C.RESET)
    else:
        current_rarity = None
        for item_id in sorted_inv:
            item   = GEAR_CATALOG.get(item_id, {})
            rarity = item.get("rarity", "common")
            color  = RARITY_COLOR.get(rarity, C.RESET)
            tier   = item.get("tier", 1)
            tier_s = "★" * tier + "☆" * (4 - tier)
            source = item.get("source", "")

            if rarity != current_rarity:
                current_rarity = rarity
                label = rarity.upper()
                print(C.GRAY + f"\n  ── {label} " + "─" * (30 - len(label)) + C.RESET)

            print(color + f"  ► {item.get('name', item_id):<22}" + C.RESET +
                  f" {tier_s}  " + C.GRAY + item.get("desc", "") + C.RESET)
            if source:
                print(C.GRAY + f"      {source}" + C.RESET)

    # Nicht-gesammelte Legendaries anzeigen
    all_legendary = [
        (k, v) for k, v in GEAR_CATALOG.items()
        if v.get("rarity") == "legendary" and k not in player.inventory
    ]
    if all_legendary:
        print(C.GRAY + "\n  ── NICHT FREIGESCHALTET " + "─" * 12 + C.RESET)
        for k, v in all_legendary:
            print(C.GRAY + f"  ○ {v['name']:<22} ????  {v.get('source', '')}" + C.RESET)

    print()
    prompt_continue()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # Boot-Sequenz nur beim ersten Start
    first_run = not any(
        os.path.exists(os.path.expanduser(f"~/.neongrid9/save_slot{i}.json"))
        for i in [1, 2, 3]
    )

    if first_run:
        show_boot_sequence()

    while True:
        choice = main_menu()

        if choice == "1":
            if new_game_menu():
                GAME.running = True
                game_hub()

        elif choice == "2":
            if load_game_menu():
                GAME.running = True
                game_hub()

        elif choice == "3":
            manage_saves_menu()

        elif choice == "4":
            about_screen()

        elif choice in ("q", "quit", "exit"):
            clear()
            print(C.NEON + "\n  NeonGrid-9 wird beendet...\n" + C.RESET)
            print(C.GRAY + '  "Knowledge is the only weapon they cannot take from you."\n' + C.RESET)
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(C.YELLOW + "\n\n  Unterbrochen. Auf Wiedersehen, Ghost.\n" + C.RESET)
        if GAME.player:
            GAME.save()
        sys.exit(0)
    except Exception as e:
        print(C.DANGER + f"\n  SYSTEM ERROR: {e}\n" + C.RESET)
        import traceback
        traceback.print_exc()
        sys.exit(1)
