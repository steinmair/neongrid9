# NeonGrid-9: LPIC-1 Cyberpunk Learning Game

## Overview

**NeonGrid-9** is an immersive, narrative-driven game for mastering Linux and passing the LPIC-1 certification (Topics 101–110). Set in a dystopian cyberpunk world, you play as a hacker learning system administration through 501 interactive missions across 22 chapters.

**Stats:**
- **501 missions** across 22 chapters
- **1,117 quiz questions** covering all LPIC-1 topics
- **47,610 max XP** (linear difficulty curve)
- **5 expert questions per boss** (final challenge per chapter)
- **22 unique bosses** representing system daemons and protocols

---

## How to Play

### Launch the Game
```bash
python3 engine/engine.py
```

### Mission Flow
Each mission presents:
1. **Story** — Narrative context (German/English mix, cyberpunk setting)
2. **Explanation** — Technical deep-dive with examples
3. **Task** — Hands-on command or concept challenge
4. **Quiz** — 1–5 multiple-choice questions testing understanding
5. **Rewards** — XP, faction reputation, gear

### Progression
- **Chapter 1–7** (early game): Hardware, boot, init, partitions, permissions, shell, processes
  - Avg 30–90 XP per mission
  - Intro boss: 150–350 XP
  - Linear warm-up for foundational knowledge
  
- **Chapter 8–14** (mid game): Regex/vi, networking, users, logging, packages, kernel, scripting
  - Avg 90–95 XP per mission
  - Boss: 375–525 XP
  - Complexity spike; expert questions introduced
  
- **Chapter 15–19** (late game): Security, locale, shell environment, exam prep, containers
  - Avg 86–199 XP per mission
  - Boss: 550–650 XP
  - Ch18 (exam) features 12-question blocks (180–200 XP each)
  
- **Chapter 20–22** (endgame): Firewall, network services, storage advanced
  - Avg 90–95 XP per mission
  - Boss: 675–725 XP
  - Integrated LPIC-1 synthesis challenges

---

## Chapter Breakdown

### Act I: System Foundations (Ch01–Ch07)
| Chapter | Topic | Boss | Intro XP | Boss XP | Notes |
|---------|-------|------|----------|---------|-------|
| 1 | Hardware Recon | BIOS Overlord | 30 | 200 | lspci, lsmod, /proc hierarchy |
| 2 | Boot Protocol | Dead Boot Recovery | 35 | 225 | GRUB, initramfs, journalctl |
| 3 | Init Wars | Init War Finale | 40 | 250 | systemd vs SysVinit, targets, units |
| 4 | Partition Wars | LVM Dominator | 45 | 275 | GPT, LVM, fstab, mkfs |
| 5 | Permission Mastery | ACL Enforcer | 50 | 300 | chmod, chown, umask, sticky bit |
| 6 | Shell Tricks | Pipeline Master | 55 | 325 | stdin/stdout/stderr, pipes, redirects |
| 7 | Process Control | Signal Handler | 60 | 350 | ps, top, kill, nice, cgroups |

### Act II: System Operations (Ch08–Ch14)
| Chapter | Topic | Boss | Intro XP | Boss XP | Notes |
|---------|-------|------|----------|---------|-------|
| 8 | Regex & Vi | Pattern Alchemist | 65 | 375 | grep -E, sed, awk, vi modes |
| 9 | Networking | DNS Oracle | 70 | 400 | ifconfig, ip, netstat, ss, DNS |
| 10 | User Management | Shadow Keeper | 75 | 425 | useradd, /etc/shadow, sudoers |
| 11 | Logging | CHRONO DAEMON | 80 | 450 | syslog, journalctl, rsyslog, logrotate |
| 12 | Packages | Package Guardian | 85 | 475 | apt, dpkg, rpm, dependency hell |
| 13 | Kernel Mastery | KERNEL ORAKEL | 90 | 500 | modprobe, dmesg, sysctl, uname |
| 14 | Scripting Mastery | BASH CONSTRUCT | 95 | 525 | bash, functions, getopts, pipefail |

### Act III: Advanced Topics (Ch15–Ch22)
| Chapter | Topic | Boss | Intro XP | Boss XP | Notes |
|---------|-------|------|----------|---------|-------|
| 15 | Security Hardening | Ghost Mask | 100 | 550 | SUID, sudoers, find, fail2ban |
| 16 | Locale & Timezone | Display Lens | 105 | 575 | locale-gen, localectl, /etc/timezone |
| 17 | Shell Environment | Phantom Blade | 110 | 600 | PATH, aliases, functions, export |
| 18 | Exam Mastery | LPIC-1 Badge | 115 | 625 | 12 comprehensive exam blocks |
| 19 | Ghost Processors | Kernel Beacon | 120 | 650 | namespaces, cgroups, containers |
| 20 | Firewall Dominion | Firewall Boss | 125 | 675 | iptables, nftables, NAT, chains |
| 21 | Network Services | Net Runners | 130 | 700 | NFS, Samba, DHCP, DNS, LDAP |
| 22 | Storage Advanced | Storage Master | 135 | 725 | RAID, LVM, quotas, iSCSI, btrfs |

---

## Mechanics

### XP & Leveling
- **Intro missions**: 30–135 XP (one per chapter, narrative setup)
- **Regular missions**: 60–200 XP (aligned to complexity)
- **Boss missions**: 200–725 XP (expert 5-question challenges)
- **Total progression**: 47,610 max XP across all 501 missions
- **Linear difficulty**: XP scales +25 per boss chapter, +5 per intro chapter

### Factions
Each mission rewards faction points:
- **Kernel Syndicate** — Hardware, boot, init
- **Root Collective** — Permissions, partitions, users, packages
- **Net Runners** — Networking, NFS, Samba, DHCP, DNS
- **Ghost Processors** — Containers, virtualization, advanced systemd
- **Firewall Dominion** — Security, firewall, intrusion detection
- Plus mission-specific factions (CHRONO DAEMON, Pipeline Master, etc.)

### Quiz Questions
- **Regular missions**: 1–4 questions per mission
- **Boss missions**: exactly 5 expert-level questions
- **Exam chapter (ch18)**: 8–12 questions per mission (prep blocks)
- **Difficulty**: Expert questions include trap answers (common exam mistakes)
- **Grading**: Immediate feedback with explanation for each answer

### Gear & Rewards
Each mission awards:
- **Task reward** (XP)
- **Gear token** (chapter-specific: hardware_scanner, root_keycard, etc.)
- **Faction XP** (toward faction reputation)
- **Explanation** (permanent learning resource)

---

## Difficulty & Pacing

### Early Game (Ch01–Ch07)
- **Difficulty**: Gentle ramp
- **Pace**: 20–30 min per chapter
- **Focus**: Foundational concepts (hardware, boot, init)
- **Quiz style**: Knowledge-based, single correct answer

### Mid Game (Ch08–Ch14)
- **Difficulty**: Moderate spike
- **Pace**: 45–60 min per chapter
- **Focus**: Advanced administration (networking, packages, kernel)
- **Quiz style**: Expert-level trap answers, flag parsing details

### Late Game (Ch15–Ch22)
- **Difficulty**: Expert synthesis
- **Pace**: 60–90 min per chapter
- **Focus**: Security, compliance, real-world scenarios
- **Quiz style**: Dangerous flag combinations, edge cases, precedence rules

### Ch18 Exam Block
- **Special**: Entire chapter is exam prep
- **Structure**: 25 exam-style quiz blocks (180–250 XP each)
- **Content**: 12-question knowledge tests + 4-question deep dives
- **Time**: ~120 min recommended for full playthrough

---

## Story & World

### Setting
**NeonGrid-9** — A sprawling digital metropolis controlled by corporate AI. You're a hacker learning to navigate system internals, competing with rival factions for control of the infrastructure.

### Main Characters
- **ZARA Z3R0** — Protagonist mentor, elite hacker guiding your journey
- **DAEMON** — Cynical system administrator, voice of pragmatism
- **CIPHER** — Security specialist, paranoid but brilliant
- **RUST** — Old-school Unix veteran, teaching practical skills
- **PHANTOM** — Virtualization expert, operates in shadows
- **SYSTEM** — Abstract OS personality, provides god's-eye view

### Narrative Arc
Each chapter follows a 3-act structure:
1. **Intro mission**: Character introduction, chapter theme setup
2. **Mid missions**: Progressive skill building, story development
3. **Boss mission**: Climactic daemon battle, faction unlock

---

## Tips for Success

### Mastery Path
1. **Read the explanation fully** — Each mission's explanation is a study guide
2. **Attempt the task** — Try the hands-on command before checking the answer
3. **Review quiz explanations** — Each wrong answer explains why it's incorrect
4. **Repeat difficult chapters** — XP scales, so revisit ch15–ch22 for grinding

### Exam Prep (Ch18)
- **Take your time** — All 12-question blocks test cumulative knowledge
- **Note trick answers** — Learn the specific flags that differ (e.g., `usermod -G` vs `-aG`)
- **Use memory tips** — Each mission includes mnemonics (e.g., "Every Admin Can Enjoy Working Night Duty" for syslog 0–7)

### LPIC-1 Alignment
NeonGrid-9 covers **100% of LPIC-1 Topics 101–110**:
- **Exam 101 (LPI-101)**: Topics 101–104 (hardware, boot, installation, filesystems)
  - **In-game**: Ch01–ch07, ch12 (packages)
- **Exam 102 (LPI-102)**: Topics 105–110 (shells, admin, services, networking, security)
  - **In-game**: Ch08–ch22

**Recommendation**: Complete Ch01–Ch14 before attempting real LPIC-1 exams; Ch15–Ch22 for advanced prep.

---

## File Structure

```
neongrid9/
├── missions/
│   ├── ch01_hardware.py           # 31 missions: hardware, BIOS, PCI, USB
│   ├── ch02_boot.py               # 19 missions: GRUB, kernel, initramfs
│   ├── ch03_init.py               # 31 missions: systemd, SysVinit, targets
│   ├── ch04_partitions.py         # 22 missions: GPT, MBR, LVM, fstab
│   ├── ch05_permissions.py        # 20 missions: chmod, chown, ACL, umask
│   ├── ch06_shell.py              # 20 missions: pipes, redirects, operators
│   ├── ch07_processes.py          # 20 missions: ps, top, signals, nice
│   ├── ch08_regex_vi.py           # 25 missions: grep -E, sed, awk, vi
│   ├── ch09_network.py            # 20 missions: ip, ss, netstat, DNS
│   ├── ch10_users.py              # 22 missions: useradd, shadow, sudoers
│   ├── ch11_logging.py            # 22 missions: syslog, journalctl, rsyslog
│   ├── ch12_packages.py           # 21 missions: apt, dpkg, rpm, dependencies
│   ├── ch13_kernel.py             # 25 missions: modprobe, sysctl, uname, dmesg
│   ├── ch14_scripting.py          # 25 missions: bash, functions, getopts
│   ├── ch15_security.py           # 22 missions: SUID, sudoers, find, hardening
│   ├── ch16_locale.py             # 22 missions: locale-gen, localectl, timezone
│   ├── ch17_shellenv.py           # 22 missions: PATH, aliases, functions, export
│   ├── ch18_exam.py               # 27 missions: 12-question exam blocks
│   ├── ch19_ghost_processors.py   # 18 missions: namespaces, cgroups, containers
│   ├── ch20_firewall_dominion.py  # 21 missions: iptables, nftables, NAT
│   ├── ch21_network_services.py   # 22 missions: NFS, Samba, DHCP, DNS, LDAP
│   └── ch22_storage_advanced.py   # 22 missions: RAID, LVM, quotas, iSCSI, btrfs
├── engine/
│   ├── engine.py                  # Main game loop & UI
│   ├── mission_engine.py          # Mission/QuizQuestion dataclasses
│   └── display.py                 # ASCII art rendering, transitions
└── README_GAMEPLAY.md             # This file
```

---

## Mission Structure

Each mission contains:
```python
Mission(
    mission_id        = "1.02",              # chapter.number
    chapter           = 1,
    title             = "PCI Devices: Treiber-Erkennung",
    mtype             = "SCAN",              # SCAN, CONSTRUCT, QUIZ
    xp                = 25,                  # 20-250 depending on chapter
    speaker           = "ZARA Z3R0",         # Narrative voice
    story             = "...",               # Cyberpunk narrative context
    why_important     = "...",               # LPIC-1 relevance
    ascii_art         = "...",               # Chapter/mission branding
    story_transitions = ["...", "...", "...", "..."],  # 4-line scene breaks
    syntax            = "lspci -k",          # Key command
    task_description  = "Zeige PCI-Treiber...",
    expected_commands = ["lspci -k"],
    hint_text         = "lspci -k zeigt...",
    quiz_questions    = [QuizQuestion(...), ...],
    exam_tip          = "...",               # Exam-focused summary
    memory_tip        = "...",               # Mnemonic aid
    gear_reward       = "hardware_scanner",
    faction_reward    = ("Kernel Syndicate", 15),
)
```

---

## FAQ

**Q: Can I skip chapters?**
A: Yes, but you'll miss narrative continuity and foundational concepts. Recommended: Ch01–Ch07 → Ch08–Ch14 → Ch15–Ch22.

**Q: What if I fail a quiz?**
A: No penalty. Each wrong answer shows the correct answer + explanation. Retry immediately.

**Q: Are missions timed?**
A: No. Complete at your own pace. Average 10–15 min per mission.

**Q: Can I use external resources?**
A: Yes. The game supplements real Linux study; man pages and online docs are encouraged.

**Q: Which chapter is hardest?**
A: Ch18 (Exam) and Ch22 (Storage Advanced). Both require synthesis of multiple topics.

**Q: How do I prepare for real LPIC-1?**
A: Complete Ch01–Ch22 + review memory tips. Then take practice exams on lpi.org.

---

## Credits

**NeonGrid-9** — LPIC-1 Learning Game  
501 missions • 1,117 expert questions • 22 cyberpunk chapters  
Built for aspiring Linux professionals and system administrators.

**Topics Covered**: LPIC-1 v5.0 (Topics 101–110)  
**Language**: German/English (code comments in English)  
**Engine**: Python 3.7+ with ANSI terminal rendering

---

*Last updated: 2026-04-21*  
*Status: Full audit complete, production-ready*
