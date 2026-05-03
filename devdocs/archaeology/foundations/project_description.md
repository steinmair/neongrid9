# Project Description — NeonGrid-9

*Derived from codebase analysis, traces, and concept inventories. This document describes what the system actually does, not what documentation claims.*

---

## What the System Actually Does

NeonGrid-9 is a single-player, terminal-based menu-driven CLI application written in Python 3.10+. It is a **pedagogical flashcard-and-drill system wrapped in a cyberpunk narrative skin**. The core activity is:

1. The player selects a chapter (1–22).
2. The player selects a mission within that chapter.
3. The system displays pre-written narrative text (story, explanation, exam tips, memory aids) with forced `time.sleep()` animations.
4. The player types a Linux command into a simulated terminal.
5. The system validates the input against a hardcoded `expected_commands` list using string matching (exact, prefix, or base-command fallback).
6. If validation fails 5 times, the system falls back to a second simulated terminal (`run_terminal`).
7. The player answers 1–5 multiple-choice quiz questions.
8. The system awards XP, updates a `completed_missions` set, checks inline achievement thresholds, saves to JSON, and returns to the chapter menu.

**What it is NOT:**
- It is not a real Linux shell or VM. No commands are executed.
- It is not an adaptive learning system. The sequence is static and identical for every player.
- It is not a multiplayer or networked application.
- It is not a game engine with a rendering loop, collision detection, or state machine.

---

## Actual Architecture

### Data Layer (Static, Import-Time)
22 Python module files (`missions/ch01_hardware.py` through `missions/ch22_exam.py`) contain ~7,000 lines of dataclass constructor calls. All 500+ `Mission` objects and 1,100+ `QuizQuestion` objects are built when `main.py` is imported. There is no lazy loading, no database, no JSON parser for content.

### Engine Layer (Procedural, Monolithic)
- `mission_engine.py` — One `MissionRunner` class with a ~250-line `run()` method containing the entire mission flow.
- `terminal_sim.py` — A flat string dictionary (`SIMULATED_OUTPUTS`) mapping command strings to pre-written output blocks.
- `display.py` — 20+ stateless functions that print ANSI-escaped text directly to stdout.
- `player.py` — A `@dataclass` holding mutable game state (XP, inventory, reputation, achievements).
- `features.py` — Achievement and hint system definitions.
- `save_system.py` — JSON read/write to `~/.neongrid9/save_slot{1,2,3}.json`.

### Control Layer (Global Singleton)
`main.py` instantiates `GAME = GameState()` at module import time. It contains the main menu loop, chapter menu dispatch (22 hardcoded `elif` branches), and special modes (review, timed exam).

---

## Current User Base and Use Cases

### Primary Use Case: Solo LPIC-1 Certification Prep
The intended user is a German-speaking individual preparing for the Linux Professional Institute LPIC-1 certification (Exams 101 + 102). They use the application to:
1. Learn Linux commands and concepts through structured flashcard-like missions.
2. Practice typing commands in a safe, simulated terminal.
3. Test knowledge with multiple-choice questions.
4. Track progress via XP, levels, and faction reputation.

### Actual Use Case: Linear Content Consumption
Because the game has no gating, no difficulty adaptation, and no branching paths, the actual usage pattern is:
1. Start at Chapter 1.
2. Complete missions in order (or skip to any chapter).
3. Read pre-written content, answer quizzes, collect XP.
4. Save progress periodically (auto-save after every mission).
5. Review weak areas via `show_linux_readiness()` or `review_mode()`.

### Edge Use Cases (Supported but Not Optimized)
- **Speedrunners** — The game records `chapter_completion_time`, but hardcoded animations add unavoidable overhead.
- **Completionists** — 19 achievements exist, but 2 are dead (never triggered), and the max is 17/19.
- **Replay** — Completed non-BOSS missions can be replayed for half quiz XP.
- **Timed Exam Mode** — A 90-minute simulation pulling random quiz questions from a chapter.

---

## Actual Problems Being Solved

### Problem 1: Safe Command Practice
New Linux learners are often afraid to run commands on a real system. The terminal simulator provides a risk-free environment where typing `rm -rf /` produces a simulated "command not found" instead of destroying the system.

**How it is solved:** `SIMULATED_OUTPUTS` maps 100+ command strings to pre-written output. No real shell is invoked. Validation is substring matching, not exact command parsing.

### Problem 2: Structured Study Path for LPIC-1
LPIC-1 covers ~15 topic domains. Self-study learners struggle to organize their learning. The game maps each chapter to specific LPIC domains (101.1, 104.1, etc.) and enforces a consistent pedagogical sequence.

**How it is solved:** Each `Mission` has `why_important`, `explanation`, `exam_tip`, and `memory_tip` fields. The `run()` method displays them in a fixed order.

### Problem 3: Retention Through Active Recall
Passive reading (e.g. man pages) has low retention. The game forces active engagement: typing commands, answering quiz questions, and receiving immediate feedback.

**How it is solved:** Every mission includes a terminal task (typing) and quiz questions (recall). XP rewards reinforce correct answers.

### Problem 4: Motivation Through Gamification
Certification prep is dry. The cyberpunk narrative, XP system, levels, gear, and achievements attempt to make studying engaging.

**How it is solved:** XP thresholds, level titles, gear rarity, faction reputation bars, and achievement popups create a skinner-box reward loop.

### Problem 5: Progress Persistence Across Sessions
Learners study in short bursts. The save system allows resuming from any of 3 slots.

**How it is solved:** JSON save files store all `Player` fields. Auto-save after every mission ensures minimal data loss.

---

## What the System Actually Does Poorly

### Accessibility
- No `--no-color` flag. Raw ANSI codes appear as gibberish on `dumb` terminals.
- No `--no-animation` flag. Forced `time.sleep()` delays make the game unusable for screen readers and slow readers.
- No high-contrast mode. Red/green colorblind users cannot distinguish success from danger.

### Portability
- The screen clear function shells out to the OS (`cls`/`clear`) instead of using ANSI escapes. This can fail in Docker and restricted environments.
- Hardcoded German text. No i18n. Only German speakers can use it.

### Robustness
- A single syntax error in any chapter file crashes the entire application at startup.
- No runtime validation of mission data. Empty `quiz_questions` or mismatched `mission_id` values are silently accepted.
- Generic `except Exception` swallows all errors. Save failures are silently ignored in `auto_save()`.

### Testability
- Hardcoded `time.sleep()` makes automated tests impractical.
- `input()` blocks forever. No test harness exists.
- `MissionRunner.run()` is 250 lines with no phase extraction. Mocking requires stubbing 15+ display functions.

### Maintainability
- Adding chapter 23 requires editing 66 places (imports, `CHAPTERS` list, `if/elif` chain).
- Manual serialization (`to_dict`/`from_dict`) is boilerplate-heavy and already missing the `achievements` field.
- Achievement triggers are scattered inline in a 250-line method.
