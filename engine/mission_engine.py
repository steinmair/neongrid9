"""
NeonGrid-9 :: Mission Engine
Läuft jede Mission ab, verwaltet Quiz, Terminal-Tasks, XP-Vergabe.
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable

from engine.display import (
    C, clear, mission_header, show_story, show_code, show_info,
    show_warn, show_error, show_success, show_exam_tip, show_memory_tip,
    show_xp_gain, xp_bar, prompt_continue, prompt_input, boss_intro, level_up_screen,
    show_ascii_art, show_transition, show_hint, show_achievements
)
from engine.player import Player
from engine.terminal_sim import run_terminal
from engine.features import HintRequest, HintLevel


# ── Datenstruktur: Quiz-Frage ──────────────────────────────────────────────────
@dataclass
class QuizQuestion:
    question: str
    options: List[str]           # ["A) ...", "B) ...", "C) ...", "D) ..."]
    correct: str                 # "A", "B", "C" oder "D"
    explanation: str
    xp_value: int = 15


# ── Datenstruktur: Mission ─────────────────────────────────────────────────────
@dataclass
class Mission:
    mission_id: str
    title: str
    mtype: str                          # SCAN / INFILTRATE / DECODE / CONSTRUCT / REPAIR / QUIZ / BOSS
    xp: int
    chapter: int

    # Visuals
    ascii_art: str = ""                              # Neon ASCII art für Mission-Einstieg
    story_transitions: List[str] = field(default_factory=list)  # Kurze Übergänge zwischen Sektionen

    # Story + Lerninhalt
    story: str = ""
    speaker: str = "SYSTEM"
    why_important: str = ""
    explanation: str = ""
    syntax: str = ""
    example: str = ""
    simulated_commands: List[str] = field(default_factory=list)  # Was tippen

    # Aufgabe
    task_description: str = ""
    expected_commands: List[str] = field(default_factory=list)
    hint_text: str = ""
    hints: List[str] = field(default_factory=list)  # [free_hint, 20xp_hint, 50xp_final_answer]

    # Quiz
    quiz_questions: List[QuizQuestion] = field(default_factory=list)

    # Prüfungswissen
    exam_tip: str = ""
    memory_tip: str = ""

    # Boss-spezifisch
    boss_name: str = ""
    boss_desc: str = ""

    # Gear-Reward
    gear_reward: Optional[str] = None
    faction_reward: Optional[tuple] = None   # (faction, amount)


# ── Mission Runner ─────────────────────────────────────────────────────────────
class MissionRunner:

    def __init__(self, player: Player, save_callback: Callable = None):
        self.player = player
        self.save_callback = save_callback

    def run(self, mission: Mission) -> bool:
        """Führt eine Mission aus. Returns True bei Erfolg."""
        if self.player.mission_completed(mission.mission_id) and mission.mtype != "BOSS":
            return self._replay_mission(mission)

        if mission.mtype == "BOSS":
            return self._run_boss(mission)

        clear()
        mission_header(mission.mission_id, mission.title, mission.xp, mission.mtype)

        tr = mission.story_transitions  # shorthand

        # 0. ASCII Art
        if mission.ascii_art:
            show_ascii_art(mission.ascii_art)

        # 1. Story-Einstieg
        if mission.story:
            show_story(mission.speaker, mission.story)
            if tr: show_transition(tr[0] if len(tr) > 0 else "")
            prompt_continue()

        # 2. Warum wichtig
        if mission.why_important:
            print(C.YELLOW + "  ── WARUM WICHTIG? " + "─" * 49 + C.RESET)
            show_info(mission.why_important)
            if tr: show_transition(tr[1] if len(tr) > 1 else "")

        # 3. Erklärung
        if mission.explanation:
            print(C.CYAN + "  ── ERKLÄRUNG " + "─" * 53 + C.RESET)
            show_info(mission.explanation)
            if tr: show_transition(tr[2] if len(tr) > 2 else "")

        # 4. Syntax
        if mission.syntax:
            print(C.CYAN + "  ── SYNTAX " + "─" * 57 + C.RESET)
            show_code(mission.syntax)
            if tr: show_transition(tr[3] if len(tr) > 3 else "")

        # 5. Beispiel
        if mission.example:
            print(C.CYAN + "  ── BEISPIEL " + "─" * 55 + C.RESET)
            show_code(mission.example)

        prompt_continue()

        # 6. Interaktive Aufgabe (Terminal)
        success = True
        attempts_used = 0
        if mission.expected_commands and mission.task_description:
            print(C.GREEN + "  ── AUFGABE " + "─" * 56 + C.RESET)
            print(C.WHITE + f"\n  {mission.task_description}\n" + C.RESET)

            # Try to get correct command from hint menu
            success = False
            attempts_used = 0
            final_cmd = ""

            # Hint menu loop
            hints_used = 0
            if mission.hints:
                while True:
                    hint_choice = prompt_input(
                        C.CYAN + "  [h]int / [q]uiz / [s]kip / Befehl? " + C.RESET
                    )
                    hint_choice_lower = hint_choice.lower()

                    if hint_choice_lower == "h":
                        if hints_used < len(mission.hints):
                            hint_req = HintRequest.create(mission.mission_id, mission.hints, hints_used)
                            if hint_req:
                                show_hint(hint_req.text, hints_used, hint_req.xp_cost)
                                if hint_req.xp_cost > 0:
                                    self.player.xp = max(0, self.player.xp - hint_req.xp_cost)
                                hints_used += 1
                        else:
                            show_warn("Keine weiteren Hinweise verfügbar.")
                    elif hint_choice_lower == "q":
                        break
                    elif hint_choice_lower == "s":
                        return True  # Skip mission
                    elif hint_choice.strip():  # Wenn User einen Befehl eingegeben hat
                        # Prüfe ob der eingegeben Befehl korrekt ist
                        cmd_base = hint_choice.strip().split()[0].lower()
                        for exp in mission.expected_commands:
                            exp_base = exp.strip().split()[0].lower()
                            # Exakter Match
                            if hint_choice.strip().lower() == exp.strip().lower():
                                show_success("Befehl akzeptiert — Ziel erreicht!")
                                success = True
                                attempts_used = 1
                                final_cmd = hint_choice
                                break
                            # Teilweise richtig: richtiger Basis-Befehl
                            if cmd_base == exp_base and len(mission.expected_commands) == 1:
                                show_success("Befehl akzeptiert — Ziel erreicht!")
                                success = True
                                attempts_used = 1
                                final_cmd = hint_choice
                                break

                        # Egal ob korrekt oder nicht, verlasse Hint-Menu
                        break

            # Wenn Befehl bei Hint-Menu nicht korrekt war, gehe zum Terminal
            if not success:
                hint_avail = self.player.has_hint_gear() or bool(mission.hint_text)
                success, attempts_used, final_cmd = run_terminal(
                    expected      = mission.expected_commands,
                    task_description = mission.task_description,
                    hint_available= hint_avail,
                    hint_text     = mission.hint_text,
                    max_attempts  = 5 if mission.mtype != "BOSS" else 3
                )

            if not success:
                show_warn("Versuche aufgebraucht. Zeige Lösung:")
                show_code(mission.expected_commands[0])
                prompt_continue()

        # 7. Quiz
        quiz_xp = 0
        if mission.quiz_questions:
            print(C.CYAN + "\n  ── MINI QUIZ " + "─" * 54 + C.RESET)
            quiz_xp = self._run_quiz(mission.quiz_questions, mission.chapter)

        # 8. Prüfungswissen
        if mission.exam_tip:
            show_exam_tip(mission.exam_tip)
            prompt_continue()

        # 9. Merksatz
        if mission.memory_tip:
            show_memory_tip(mission.memory_tip)

        # ── XP berechnen ──
        base_xp = mission.xp
        if not success:
            base_xp = base_xp // 3  # Teilpunkte wenn gescheitert
        if attempts_used == 1 and success:
            base_xp = int(base_xp * 1.2)  # Bonus für ersten Versuch

        total_xp = base_xp + quiz_xp
        new_xp, leveled_up = self.player.add_xp(total_xp)
        self.player.complete_mission(mission.mission_id)

        show_xp_gain(total_xp)
        xp_bar(new_xp, self.player.level,
               self.player.get_current_level_xp(),
               self.player.get_next_level_xp())
        print()

        # Check achievements
        unlocked = []
        if len(self.player.completed_missions) == 1:
            ach = self.player.achievements.unlock('first_mission')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

        if mission.mtype == "BOSS":
            self.player.bosses_defeated += 1
            ach = self.player.achievements.unlock('boss_defeated')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

            if self.player.bosses_defeated == 5:
                ach = self.player.achievements.unlock('five_bosses')
                if ach:
                    unlocked.append(ach)
                    self.player.add_xp(ach.xp_reward)

            if self.player.bosses_defeated == 22:
                ach = self.player.achievements.unlock('all_bosses')
                if ach:
                    unlocked.append(ach)
                    self.player.add_xp(ach.xp_reward)

        # Chapter completion check
        chapter_missions = [m for m in self.player.completed_missions if m.startswith(f"{mission.chapter}.")]
        if mission.chapter == 1 and len(chapter_missions) >= 31:
            ach = self.player.achievements.unlock('chapter_1_complete')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

        # New achievement triggers
        if len(self.player.completed_missions) == 100:
            ach = self.player.achievements.unlock('quest_marathon')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

        if self.player.level >= 10:
            ach = self.player.achievements.unlock('level_ten')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

        # Check for chapter masters (5+ chapters complete)
        chapters_complete = len(set(m.split('.')[0] for m in self.player.completed_missions))
        if chapters_complete >= 5:
            ach = self.player.achievements.unlock('chapter_master')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

        # Check for all factions at level 2+
        from engine.features import calculate_level
        faction_levels = [calculate_level(rep) for rep in self.player.reputation.values()]
        if all(lvl >= 2 for lvl in faction_levels):
            ach = self.player.achievements.unlock('all_factions')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

        # Check for gear collector (10+ items)
        if len(self.player.inventory) >= 10:
            ach = self.player.achievements.unlock('gear_collector')
            if ach:
                unlocked.append(ach)
                self.player.add_xp(ach.xp_reward)

        if unlocked:
            show_achievements(unlocked)

        if leveled_up:
            level_up_screen(self.player.level, self.player.level_title)

        # Gear-Belohnung
        if mission.gear_reward:
            if self.player.add_gear(mission.gear_reward):
                from engine.player import GEAR_CATALOG
                item = GEAR_CATALOG.get(mission.gear_reward, {})
                print(C.YELLOW + f"  ★  NEUES GEAR: {item.get('name', mission.gear_reward)}" + C.RESET)
                print(C.GRAY   + f"     {item.get('desc', '')}" + C.RESET)
                print()

        # Fraktions-Reputation
        if mission.faction_reward:
            faction, amount = mission.faction_reward
            self.player.add_reputation(faction, amount)
            print(C.MAGENTA + f"  ↑  REPUTATION: {faction} +{amount}" + C.RESET)
            print()

        if self.save_callback:
            self.save_callback(self.player)

        prompt_continue()
        return success

    def _run_quiz(self, questions: List[QuizQuestion], chapter: int = 0,
                  exam_start: float = 0.0, exam_limit: int = 0) -> int:
        """Führt Quiz-Fragen aus. Returns earned XP.

        exam_start: time.time() des Exam-Starts (0 = kein Timer)
        exam_limit: Sekunden-Limit für Anzeige (0 = kein Limit)
        """
        total_xp = 0
        self.player.total_quizzes += len(questions)
        letters = ["A", "B", "C", "D"]

        for i, q in enumerate(questions, 1):
            # Timer-Zeile
            timer_line = ""
            if exam_start:
                elapsed  = int(time.time() - exam_start)
                remain   = max(0, exam_limit - elapsed) if exam_limit else 0
                e_mm, e_ss = divmod(elapsed, 60)
                r_mm, r_ss = divmod(remain,  60)
                if exam_limit:
                    t_color = C.DANGER if remain < 300 else C.YELLOW if remain < 900 else C.GREEN
                    timer_line = (f"  {C.GRAY}Verstrichen: {e_mm:02d}:{e_ss:02d}  "
                                  f"{t_color}Verbleibend: {r_mm:02d}:{r_ss:02d}{C.RESET}")
                else:
                    timer_line = f"  {C.GRAY}Verstrichen: {e_mm:02d}:{e_ss:02d}{C.RESET}"

            print(f"\n  {C.YELLOW}FRAGE {i}/{len(questions)}{C.RESET}"
                  + (f"   {timer_line}" if timer_line else ""))
            print(C.WHITE + f"  {q.question}" + C.RESET)
            print()
            for idx, opt in enumerate(q.options):
                print(C.GRAY + f"    {letters[idx]}) {opt}" + C.RESET)
            print()

            correct_letter = letters[q.correct] if isinstance(q.correct, int) else q.correct

            attempts = 0
            answered_correct = False
            while attempts < 3:
                answer = prompt_input("antwort [A/B/C/D]").upper().strip()
                if answer not in ("A", "B", "C", "D"):
                    print(C.WARN + "  Bitte A, B, C oder D eingeben." + C.RESET)
                    continue

                if answer == correct_letter:
                    earned = q.xp_value if attempts == 0 else q.xp_value // 2
                    show_success(f"RICHTIG! +{earned} XP")
                    print(C.CYAN + f"  → {q.explanation}" + C.RESET)
                    total_xp += earned
                    answered_correct = True
                    if attempts == 0:
                        self.player.correct_first_try += 1
                    break
                else:
                    attempts += 1
                    remaining = 3 - attempts
                    print(C.DANGER + f"  ✗  Falsch. " + C.RESET +
                          (f"Noch {remaining} Versuch(e)." if remaining > 0 else ""))
                    if remaining == 0:
                        correct_opt = q.options[
                            q.correct if isinstance(q.correct, int) else letters.index(q.correct)
                        ]
                        print(C.YELLOW + f"  Richtige Antwort: {correct_letter}) {correct_opt}" + C.RESET)
                        print(C.CYAN   + f"  → {q.explanation}" + C.RESET)

            if chapter:
                self.player.record_quiz_result(chapter, answered_correct)

        return total_xp

    def _run_boss(self, mission: Mission) -> bool:
        """Boss-Kampf mit mehreren Phasen."""
        boss_intro(mission.boss_name or mission.title,
                   mission.boss_desc or "Ein komplexer Angriff auf deine Fähigkeiten.")

        clear()
        mission_header(mission.mission_id, mission.title, mission.xp, "BOSS")

        if mission.ascii_art:
            show_ascii_art(mission.ascii_art, C.DANGER)

        if mission.story:
            show_story(mission.speaker, mission.story)
            prompt_continue()

        # Boss: mehrere Terminal-Challenges
        phase_success = 0
        total_phases  = max(1, len(mission.expected_commands))

        for i, expected_cmd in enumerate(mission.expected_commands, 1):
            print(C.DANGER + f"\n  ── BOSS PHASE {i}/{total_phases} " + "─" * 46 + C.RESET)
            # Task-Beschreibung per Phase
            tasks = mission.task_description.split("||") if "||" in mission.task_description else [mission.task_description]
            task  = tasks[i-1].strip() if i-1 < len(tasks) else mission.task_description

            print(C.WHITE + f"\n  {task}\n" + C.RESET)
            success, _, _ = run_terminal(
                expected=[expected_cmd],
                task_description=task,
                hint_available=False,
                max_attempts=3
            )
            if success:
                phase_success += 1
                show_success(f"Phase {i} bestanden!")
            else:
                show_warn(f"Phase {i} gescheitert. Lösung: {expected_cmd}")
            prompt_continue()

        # Boss-Quiz
        quiz_xp = 0
        if mission.quiz_questions:
            print(C.DANGER + "\n  ── BOSS QUIZ: FINAL TEST " + "─" * 43 + C.RESET)
            quiz_xp = self._run_quiz(mission.quiz_questions, mission.chapter)

        # Wertung
        win = phase_success >= (total_phases * 0.6)

        if win:
            print(C.SUCCESS + """
  ██╗    ██╗██╗███╗   ██╗
  ██║    ██║██║████╗  ██║
  ██║ █╗ ██║██║██╔██╗ ██║
  ██║███╗██║██║██║╚██╗██║
  ╚███╔███╔╝██║██║ ╚████║
   ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝
""" + C.RESET)
            self.player.bosses_defeated += 1
            xp_earned = mission.xp + quiz_xp
        else:
            print(C.WARN + "\n  BOSS nicht vollständig besiegt — Teilerfolg.\n" + C.RESET)
            xp_earned = (mission.xp // 2) + quiz_xp

        new_xp, leveled_up = self.player.add_xp(xp_earned)
        self.player.complete_mission(mission.mission_id)
        show_xp_gain(xp_earned)
        xp_bar(new_xp, self.player.level,
               self.player.get_current_level_xp(),
               self.player.get_next_level_xp())

        if leveled_up:
            level_up_screen(self.player.level, self.player.level_title)

        if mission.exam_tip:
            show_exam_tip(mission.exam_tip)

        if mission.gear_reward and win:
            if self.player.add_gear(mission.gear_reward):
                from engine.player import GEAR_CATALOG
                item = GEAR_CATALOG.get(mission.gear_reward, {})
                print(C.YELLOW + f"\n  ★  BOSS REWARD: {item.get('name', mission.gear_reward)}" + C.RESET)
                print(C.GRAY   + f"     {item.get('desc', '')}" + C.RESET)

        if self.save_callback:
            self.save_callback(self.player)

        prompt_continue()
        return win

    def _replay_mission(self, mission: Mission) -> bool:
        """Bereits abgeschlossene Mission — nur Quiz wiederholen."""
        clear()
        mission_header(mission.mission_id, mission.title + " [WIEDERHOLUNG]", 0, mission.mtype)
        print(C.GRAY + "  Diese Mission hast du bereits abgeschlossen.\n" + C.RESET)
        if mission.quiz_questions:
            choice = prompt_input("Quiz wiederholen? [j/n]").lower()
            if choice == "j":
                quiz_xp = self._run_quiz(mission.quiz_questions)
                if quiz_xp > 0:
                    bonus = quiz_xp // 2
                    new_xp, leveled_up = self.player.add_xp(bonus)
                    show_xp_gain(bonus, "Wiederholung")
                    if leveled_up:
                        level_up_screen(self.player.level, self.player.level_title)
        return True
