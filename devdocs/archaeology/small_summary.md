# NeonGrid-9 :: Code-Archaeology Summary

> What this project actually is, read from the code itself.

## The Big Picture

**NeonGrid-9** is a story-driven, text-based learning game that runs in a terminal window. Its purpose — read plainly from the code — is to teach Linux system administration in a way that feels like playing an RPG. The player doesn't read a textbook; they complete "missions" guided by fictional characters inside a cyberpunk-themed world called "NeonGrid-9".

The framing story, visible in the code's intro screens and mission texts, casts the player as a nameless "Ghost" who wakes up in a dystopian city controlled by the "BIOS Imperium." A hacker named Zara Z3R0 recruits the player, promising to turn them into a "Linux Certified Ghost" — or leave them as "cannon fodder." This narrative wrapper is consistently present across all 22 chapters and over 500 individual missions.

## How It Works (From the Code)

### The Learning Loop

Each mission follows a rigid but effective structure, enforced by the `MissionRunner` class in `engine/mission_engine.py`:

1. **Story** — A character speaks to the player in a typewriter-style text animation, setting context for the topic.
2. **Why It Matters** — A brief explanation of why this Linux concept is important for real-world system administration.
3. **Explanation** — The actual teaching content: how a command works, what a filesystem does, how permissions function.
4. **Syntax & Example** — Code blocks showing the correct command and realistic terminal output.
5. **Interactive Task** — The player types a Linux command into a simulated terminal. The game checks if the command is correct.
6. **Quiz** — 1-5 multiple-choice questions test whether the player understood the material.
7. **Rewards** — Experience points (XP) are awarded. If the mission is completed well, the player may level up, earn gear, or gain faction reputation.

### The 22 Chapters

The code imports 22 separate chapter files (e.g., `missions/ch01_hardware.py`, `missions/ch22_exam.py`). Each chapter covers a specific Linux certification topic:

- Hardware & BIOS/UEFI
- Boot managers & GRUB2
- Processes, systemd, and init systems
- Filesystems, partitioning, and LVM
- File permissions and the Filesystem Hierarchy Standard
- Shell scripting, pipes, and text filters
- Regular expressions and the vi editor
- Networking, TCP/IP, DNS, SSH
- Users, groups, sudo, and PAM
- Logging, time services, cron, and at
- Package management (dpkg, apt, rpm, yum, zypper)
- Kernel modules, /proc, sysctl, udev
- Bash scripting
- Security, SSH hardening, GPG, fail2ban
- Locales, timezones, X11, printing
- Shell environment, PATH, aliases, history
- Advanced storage: RAID, LVM, quotas, iSCSI, btrfs
- Containers and virtualization
- Firewalls, iptables, nftables, VPNs
- Network services: NFS, Samba, DHCP, DNS, LDAP
- Final exam simulation

The final chapter (`ch22_exam.py`) is particularly revealing: it contains 60 exam-style questions across all topics, simulating the actual LPIC-1 certification exam with a 90-minute timer and a scoring system where 500/800 points are required to pass.

### Characters and Voices

From reading the code, the game uses a cast of recurring speakers who deliver mission stories:

- **ZARA Z3R0** — The mentor figure; appears frequently in early chapters.
- **DAEMON** — A terse, systems-focused character.
- **LYRA-7** — An AI archivist; explains modern systemd and journal concepts.
- **SYSTEM** — Impersonal, encyclopedic narrator.
- **KERNEL-ORAKEL** — Speaks during quiz-only "exam trap" missions.
- **EXAMINATOR** — Administers the final certification simulation.

This isn't just cosmetic. The code explicitly tracks which speaker the player has heard most often in their save file (`speaker_stats`), suggesting the developers intended this to be part of the player's profile and sense of progress.

### Game Systems (Read from `engine/player.py` and `engine/features.py`)

The code reveals a fully-featured progression engine:

**Levels and Titles:**
The player advances through 15 levels with cyberpunk-themed titles:
- Level 1: "Newbie Hacker" (0 XP)
- Level 5: "Pipe Runner" (5,000 XP)
- Level 10: "Net Runner" (22,500 XP)
- Level 15: "Certified Ghost" (52,500 XP)

**Gear (Inventory):**
The player collects items like a "Hardware Scanner," "Ghost Mask," or "Linux Badge." These aren't just cosmetic — the code shows they provide XP bonuses for specific mission types (e.g., +20% XP on quiz missions). Gear has rarity tiers: Common, Uncommon, Rare, and Legendary.

**Factions:**
Five in-game factions exist ("Kernel Syndicate," "Root Collective," "Net Runners," "Ghost Processors," "Firewall Dominion"). Completing missions earns reputation points. The code tracks reputation per faction (0–100 scale) and calculates a "faction level" from it, though this appears to be primarily for narrative flavor.

**Achievements:**
The code defines 19 achievements with unlock conditions checked after every mission:
- Complete your first mission
- Defeat your first boss
- Defeat all 22 bosses
- Reach level 10
- Collect 10+ gear items
- Complete 100+ missions
- Reach level 2+ with all 5 factions

**Hints:**
If a player gets stuck on a terminal command, the game offers a three-tier hint system:
1. Free hint (general guidance)
2. Standard hint (costs 20 XP)
3. Final answer (costs 50 XP, reveals the command)

The code deducts XP immediately when hints are used.

### The Terminal Simulator

A critical component is `engine/terminal_sim.py`. Rather than running real Linux commands on the player's actual computer, the game contains a large dictionary of pre-written outputs for common commands. When the player types `lspci`, the game looks up the string "lspci" and prints a realistic, pre-crafted response showing Intel graphics, wireless controllers, and NVMe SSDs — complete with real-looking PCI bus addresses and vendor IDs.

The simulation covers commands across all domains: `ls`, `cat`, `grep`, `find`, `chmod`, `ps`, `kill`, `ping`, `ip`, `ss`, `systemctl`, `apt`, `yum`, `fdisk`, `mkfs`, `mount`, `df`, `journalctl`, `dmesg`, and many more. Each chapter's missions reference the specific commands the player is expected to type.

This design choice is important: it makes the game completely safe to run (no risk of damaging the host system) and portable (works on any OS with Python, including Windows), while still teaching correct command syntax and expected output patterns.

### Save System

The game stores progress in JSON files inside a hidden `.neongrid9` folder in the user's home directory. Three independent save slots are supported. The save file contains:
- Player name, XP, level, and title
- Which missions are completed
- Inventory and faction reputation
- Quiz accuracy statistics per chapter
- Total playtime, boss kill times, chapter completion times
- Achievement unlocks
- Hint usage counts

## Special Modes (Beyond Normal Missions)

The `main.py` code reveals several modes accessible from the main hub:

**Linux Readiness Report:**
Generates a per-chapter progress breakdown showing mission completion percentage, XP earned, and quiz accuracy. Weak topics (under 60% quiz accuracy) are highlighted in red with a recommendation to use Review Mode.

**Review Mode (Spaced Repetition):**
The game collects all quiz questions from all chapters, weights them so that questions from chapters where the player performed poorly appear more frequently, and presents a random session of 10 questions. The player gets immediate feedback with explanations.

**Timed Exam Mode:**
A 90-minute simulation using the 60 questions from Chapter 22. A live timer counts down. The scoring system mimics the real LPIC-1 exam: 800 points maximum, 500 required to pass. The code even calculates how many additional correct answers the player would have needed to pass if they failed.

## What the Code Says About Project Maturity

Reading the code files reveals a project that is **content-complete** and highly polished:

- All 22 chapter files exist and are imported in `main.py`.
- The chapter completion screen (`_show_chapter_complete`) contains hand-written recap summaries for every single chapter — each one listing the specific commands and concepts the player should now know.
- The terminal simulator contains realistic output for dozens of commands, crafted to look like output from a real ThinkPad X1 Carbon running Debian.
- Boss missions have custom ASCII art, multi-phase terminal challenges, and unique gear rewards.
- The exam mode has a full scoring bar visualization with a passing threshold marker.
- The save system handles data migration (e.g., filling in missing factions for older save files).
- Error handling exists for keyboard interrupts, JSON parse failures, and missing save files.

There are no placeholder files, no TODO comments indicating missing content, and no chapter stubs. Every mission in every chapter is fully populated with story text, explanations, syntax examples, expected commands, hints, quiz questions, exam tips, and memory aids.

## Summary

From a code archaeology perspective, NeonGrid-9 is a **complete, self-contained educational game engine** built entirely with Python's standard library. It doesn't need a web browser, a database, or external assets. It teaches Linux system administration by wrapping technical content in a cyberpunk RPG narrative, using a simulated terminal for safe hands-on practice, and motivating the player through a robust progression system of levels, gear, achievements, and faction reputation. The code shows no signs of being a prototype — it is a finished, shipping product with over 7,000 lines of hand-crafted mission content.
