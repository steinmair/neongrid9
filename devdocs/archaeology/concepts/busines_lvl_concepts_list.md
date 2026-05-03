# Business-Level Concepts Inventory

## Domain: Linux Certification Training

### LPIC-1 Topic Mapping
Every chapter maps to one or more Linux Professional Institute (LPI) exam topics (101.1, 101.2, 103.2, etc.). Chapter 1 = Hardware/BIOS (101.1). Chapter 22 = Grand Finale (ALL topics). This creates a study path that mirrors real certification objectives.

**Status:** Fully implemented. 22 chapters cover all LPIC-1 101 and 102 domains. Topic tags are displayed in the chapter menu and `about_screen()`.

---

## Game Progression Systems

### Chapter-Based Linear Progression
The game presents 22 chapters in sequence. Each chapter contains ~20-30 missions plus a boss. The player can jump to any chapter from the hub, but the narrative is designed to be consumed in order.

**Status:** Fully implemented. No gating — all 22 chapters are accessible from the start. The `lock` variable in `game_hub()` is commented out, suggesting gating was considered but disabled.

### Mission Type Taxonomy
Seven mission types define the pedagogical interaction:
- **SCAN** — Learn concept + execute single command
- **INFILTRATE** — Security testing; multi-step terminal tasks
- **DECODE** — Interpret output/logs; analysis focus
- **CONSTRUCT** — Build/configure system; multi-step construction
- **REPAIR** — Diagnose and fix broken systems
- **QUIZ** — Pure quiz assessment, no terminal
- **BOSS** — Chapter synthesis; combines all types

**Status:** Fully implemented. Each type has a unique color in `mission_header()`. BOSS missions award gear and faction reputation.

### XP & Leveling System
15 levels with exponential XP thresholds (0, 500, 1500, 3000, 5000... 52500). Levels 16-20 exist in `LEVELS` but only 15 are defined. A scaling bonus applies to incoming XP (+10% at level 5, +20% at level 10, +30% at level 15).

**Status:** Fully implemented. The scaling bonus applies to *incoming* XP only, not retroactively. Max total XP is ~51,540.

### 3-Tier Hint System
Hints are structured as a list: `[free_hint, 20xp_hint, 50xp_final_answer]`. The first hint is free. The second costs 20 XP. The third "reveals the answer pattern" and costs 50 XP. The player can request hints during the fancy prompt loop.

**Status:** Fully implemented. Hints are automatically shown after wrong answers. The cost is deducted immediately via direct XP mutation.

---

## Narrative & World-Building

### Cyberpunk Framing
The game is set in "NeonGrid-9, Year 2089." The BIOS Imperium controls the city through ignorance. The player is a "Ghost" recruited by ZARA Z3R0 to become a "Linux Certified Ghost."

**Status:** Fully implemented. All 22 chapters have cyberpunk-themed titles (BOOT CAMP, DARK BOOT, GHOST PROTOCOL, PARTITION WARS, etc.).

### Faction System (Narrative-Only)
5 factions exist with reputation 0-100: Kernel Syndicate, Root Collective, Net Runners, Ghost Processors, Firewall Dominion. Reputation is gained via `faction_reward` on missions. It has zero mechanical impact on gameplay — purely narrative/flavor.

**Status:** Implemented but cosmetic. The `FactionStatus` class exists (with `progress_bar()` and `display()`) but is never instantiated. `stats_summary()` manually builds faction bars instead.

### Speaker Distribution
6 narrative speakers deliver story content: ZARA Z3R0, RUST, PHANTOM, CIPHER, LYRA-7, EXAMINATOR, and SYSTEM. The rule "no speaker >60% per chapter" ensures narrative variety. Chapter 18 is an intentional exception (EXAMINATOR dominates).

**Status:** Fully implemented. `speaker_stats` tracks how often each speaker is heard. `stats_summary()` shows the top 3 speakers.

### Story Transitions
Every mission has exactly 4 `story_transitions` — short narrative lines displayed between sections (story → explanation → example → quiz). They are 2-10 words each and match the speaker's voice.

**Status:** Fully implemented. All 501 missions have 4 transitions. The `run()` method accesses them by index (`tr[0]`, `tr[1]`, etc.).

---

## Assessment & Practice

### Quiz-First Design
Every mission includes 1-5 quiz questions with 4 options (A-D). Each question has an `explanation` field explaining why the answer is correct. Quiz questions are the primary assessment mechanism.

**Status:** Fully implemented. 1,117 quiz questions across 501 missions. Boss missions have exactly 5 "expert" questions.

### Exam Tip + Memory Tip Dual System
Every mission ends with two pedagogical aids: an `exam_tip` (LPIC exam relevance, e.g., "Remember: domain 103.1") and a `memory_tip` (mnemonic or shorthand, e.g., "lspci = List PCI").

**Status:** Fully implemented. Both fields are mandatory per the audit checklist in CLAUDE.md.

### Terminal Simulation as Safe Practice
Players type Linux commands into a simulated terminal. The game validates against `expected_commands` and shows pre-written output. No real shell is executed, preventing accidental damage.

**Status:** Fully implemented. The simulator supports ~40 commands. It is safer than a real shell but has no persistent filesystem state (commands like `cd` followed by `ls` do not work as a sequence).

### Timed Exam Mode
A 90-minute exam simulation (`timed_exam_mode()`) pulls quiz questions from a selected chapter and runs them under a timer. Players earn XP based on accuracy and speed.

**Status:** Implemented. Chapter 18 has a special `[exam]` shortcut in `chapter_menu()` that launches this mode.

### Review Mode (Spaced Repetition)
`review_mode()` in `main.py` allows players to review previously completed missions or quiz questions. This is positioned as "spaced repetition" for learning reinforcement.

**Status:** Implemented. Accessible from the game hub via `[x]`.

---

## Reward & Collection Systems

### Gear System (Rarity Tiers)
Gear items have 4 rarity tiers: common (white), uncommon (green), rare (blue), legendary (gold/yellow). Each item grants an XP boost for specific mission types. The `linux_badge` is unique — only one exists per playthrough.

**Status:** Fully implemented. 13 gear items in `GEAR_CATALOG`. Gear is awarded exclusively by boss missions. `gear_bonus()` calculates the active multiplier.

### Achievement System (19 Achievements)
19 achievements with unlock conditions and XP rewards. Categories: early-game milestones (`first_mission`), chapter completion (`chapter_*_complete`), boss-related (`boss_defeated`, `five_bosses`, `all_bosses`), special skills (`perfect_quiz`, `speedrun`, `no_hints`), and collection (`gear_collector`, `faction_max`).

**Status:** Implemented but incomplete. `perfect_quiz` and `no_hints` are defined in `ACHIEVEMENTS` but never triggered. `quest_marathon` checks `len(completed_missions) == 100` exactly (not `>=`).

### Boss Battles (Chapter Finales)
Each chapter ends with a BOSS mission. Bosses have multi-phase terminal challenges (each phase is a separate `run_terminal()` call), 5 expert quiz questions, and special ASCII art. Defeating a boss awards gear and faction reputation.

**Status:** Fully implemented. 22 boss missions. The win condition is `phase_success >= total_phases * 0.6` (60% threshold).

---

## Meta-Game Features

### First-Run Boot Sequence
On first launch (no save files exist), the game shows a `show_boot_sequence()` animation simulating a Linux boot process (BIOS POST, GRUB2 loading, kernel boot, systemd startup). This is followed by a `show_story_prologue()` narrative intro.

**Status:** Fully implemented. First-run detection checks `any(os.path.exists(...save_slot...))`. Boot sequence is pure `print()` + `time.sleep()`.

### Character Status Report
`show_player_status()` displays a comprehensive character sheet: name, level, XP, completed missions, boss count, playtime, chapter progress, faction reputation bars, top speakers, and inventory with rarity colors.

**Status:** Fully implemented. Accessible via `[s]` in the game hub.

### Linux Readiness Report
`show_linux_readiness()` generates a readiness assessment based on completed missions and quiz accuracy per chapter. It identifies weak areas for targeted study.

**Status:** Implemented. Accessible via `[r]` in the game hub.

### Save Slot Management
3 independent JSON save slots. Players can create, load, and delete slots. Slot info shows name, level, XP, and mission count without loading the full save.

**Status:** Fully implemented. `slot_info()` reads the JSON file directly to display metadata.

---

## Implicit Business Concepts

### "Learn by Doing" Pedagogy
The core educational philosophy is that reading about Linux commands is insufficient — the player must *type* the command in a simulated terminal. Even DECODE missions (no terminal task) still include quiz questions to force active recall.

**Rationale:** Passive reading has low retention. Active practice (typing, answering) is the proven pedagogy for technical certification prep.

**Impact:** Every mission type, even QUIZ, forces engagement. The game never allows pure passive consumption.

### "Cyberpunk as Memory Anchor"
The narrative is not decorative — it serves as a memory aid. Associating `lspci` with "ZARA Z3R0 scanning the Sector-7 slum" creates an emotional hook that aids recall during the real exam.

**Rationale:** Mnemonics work better with narrative context. "Hardware Scanner" gear reinforces the association between the command and the story.

**Impact:** The story_transitions and ASCII art are not "fluff" — they are pedagogical tools. Removing them would reduce learning effectiveness.

### "Exam-Oriented Content Completeness"
The project was audited for completeness on 2026-04-21. Every mission has: quiz_questions, why_important, exam_tip, memory_tip, story_transitions, ascii_art. This is not a feature — it is a *content policy* enforced by the developer.

**Rationale:** Incomplete content (missing exam tips, no quiz questions) would reduce certification prep value. The audit ensures every mission is a "complete learning unit."

**Impact:** 501 missions × ~10 mandatory fields = 5,000+ data points that must be maintained. Any new mission must conform to this schema.

### "No Punishment for Failure"
Failing a terminal task still grants 1/3 of the base XP. Failing a boss grants half XP. There is no "game over." The design assumes the player is *learning*, not competing.

**Rationale:** A certification prep tool should not discourage the learner. Partial credit ensures every attempt has value.

**Impact:** The difficulty curve is flat. Advanced players may find the game too easy, but the target audience (certification learners) benefits from the forgiving design.
