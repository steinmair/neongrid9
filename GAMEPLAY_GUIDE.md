# NeonGrid-9 Gameplay Guide

## Welcome to the Cyberpunk Linux Learning Game

NeonGrid-9 is an immersive terminal-based game that teaches Linux system administration through interactive missions, boss encounters, and faction reputation. Complete all 22 chapters to master Linux topics and become a legendary Net Runner.

---

## 🎮 How to Play

### Starting the Game

```bash
python3 main.py
```

You'll begin as a **Newbie Hacker** in Chapter 1. Progress through missions, gain XP, level up, and unlock achievements.

### Mission Types

Each mission falls into one of these categories:

| Type | Description | Example |
|------|-------------|---------|
| **SCAN** | Execute terminal commands and verify output | `lspci` to list PCI devices |
| **DECODE** | Analyze code/configs and answer questions | Read bash script, answer about variables |
| **INFILTRATE** | Navigate file systems and find data | Locate config files in /etc |
| **CONSTRUCT** | Write code or create files | Write shell script that does X |
| **REPAIR** | Fix broken systems or code | Debug a failing bash script |
| **QUIZ** | Answer multiple-choice questions | Test your knowledge on topic |
| **BOSS** | Challenging multi-phase mission | Combine all skills learned in chapter |

### Your Progression

**Level System:**
- Start as **Newbie Hacker** (Level 1)
- Progress: Script Kiddie (2) → Sys Admin (3) → Net Runner (10) → **Master Operator** (20)
- Each level requires more XP but unlocks higher difficulty scaling

**XP Rewards:**
- Standard missions: 30-135 XP
- Exam missions: 200 XP
- Boss missions: 250-350 XP
- Hints used: -20 or -50 XP (choose to learn instead)

**Achievements:**
- Complete missions to unlock achievements
- Achievements give XP bonuses and bragging rights
- See [Achievement Checklist](#achievements) for full list

---

## 💡 Hint System

Every mission has up to 3 hints. Use them strategically:

### 💚 Free Hint (0 XP cost)
- Gives direction without spoiling answer
- Safe choice if you're completely stuck
- Example: "This directory starts with /etc"

### 💛 Standard Hint (20 XP cost)
- Shows partial command or approach
- Reduces penalty vs. no hint
- Example: "Try: grep -r password /etc"

### ❤️ Final Answer (50 XP cost)
- Reveals complete solution
- Use when learning from the answer
- Teaches the concept directly

**Pro Tip:** Try 2-3 times without hints first. If stuck, use Free → Standard → Final in that order.

---

## 🎯 The 22 Chapters

### Early Game: Foundation (Ch01-03)
- **Hardware Basics** — CPU, RAM, storage, BIOS
- **Boot Process** — UEFI, bootloader, kernel initialization  
- **Filesystems** — ext4, inodes, mounting, permissions

*Goal:* Understand Linux fundamentals. Prepare for deeper topics.

### Mid Game: Core Systems (Ch04-15)
- **Partitions & Disks** — fdisk, parted, LVM
- **Permissions & Owners** — chmod, chown, umask, ACLs
- **Users & Groups** — useradd, sudoers, password management
- **Processes & Signals** — ps, kill, nice, process monitoring
- **I/O & Redirection** — pipes, redirects, file descriptors
- **Shell Scripting** — bash variables, loops, functions
- **Network** — IP, DNS, netstat, firewall basics
- **Packages & Repos** — apt, rpm, package management
- **Kernel & Modules** — modprobe, kernel parameters
- **Logging & Monitoring** — syslog, journalctl, log analysis
- **Security Hardening** — SSH, sudo, firewall rules

*Goal:* Master system administration. Each boss mission tests chapter mastery.

### Late Game: Expert Topics (Ch16-22)
- **Localization** — locales, character sets, timezones
- **Shell Environment** — PATH, aliases, shell configuration
- **Exam Block** — 27 comprehensive missions covering all topics
- **Ghost Processors** — Advanced process management
- **Firewall Dominion** — iptables, nftables, packet filtering
- **Network Services** — daemons, systemd, service management
- **Storage Advanced** — RAID, snapshots, backup strategies

*Goal:* Reach mastery. Boss missions are epic challenges.

---

## 🏆 Achievements & Goals

### Early Game (5-50 XP each)
- 🟢 **First Signal** — Complete your first mission
- 🎯 **Self-Reliant** — Complete mission with no hints
- 📖 **Story Addict** — Read all story sections in a chapter

### Mid Game (100-400 XP each)
- ⭐ **Hardware Hacker** — Complete Hardware chapter (Ch01)
- 🔐 **Permission Master** — Complete Permissions chapter (Ch05)
- 🎯 **Flawless Victory** — Answer 10 consecutive quiz questions correctly
- ⚡ **Speed Runner** — Complete a chapter in under 1 hour

### Late Game (500-5000 XP each)
- ⚔️ **Daemon Slayer** — Defeat your first boss mission
- 💀 **Boss Killer** — Defeat 5 boss missions
- 👑 **Linux Master** — Defeat all 22 boss missions
- 🏆 **Faction Leader** — Reach max level (100) with a faction
- 🤝 **Diplomat** — Reach level 2+ with all 5 factions
- 🔄 **Grinder** — Complete 100+ missions
- 📚 **Scholar** — Complete all missions in 5 different chapters

**See [Achievement Checklist](#achievement-checklist) for all 18 achievements.**

---

## 🎪 Faction System

Your actions influence 5 rival factions. Build reputation and unlock perks:

### The Five Factions

1. **Kernel Syndicate** 🔴 — Pure system optimization
   - Specializes in performance tuning
   - Rewards for complex scripting

2. **Cipher Collective** 🔵 — Encryption & security
   - Specializes in cryptography
   - Rewards for security missions

3. **Echo Protocol** 🟠 — Network & communications
   - Specializes in networking
   - Rewards for network missions

4. **Void Explorers** 🟣 — Storage & filesystems
   - Specializes in data management
   - Rewards for storage missions

5. **Phantom Archive** 🟢 — Information & knowledge
   - Specializes in databases & docs
   - Rewards for learning missions

### Reputation Tracking

- Missions award **0-50 reputation** per faction
- Reputation is chapter-specific (resets per chapter)
- Build reputation by completing faction-aligned missions
- Max reputation per chapter: 100
- Faction level: 1-5 (based on current reputation)

**Pro Tip:** Build reputation with all factions for the **Diplomat** achievement (1200 XP).

---

## ⚙️ Player Stats & Progression

### Your Character

```
Level:           7 (Sys Admin)
Total XP:        5,200
Completed:       87 missions
Achievements:    6/18 unlocked
```

### Chapter Completion

Each chapter shows:
- **Missions:** How many you've completed
- **Boss Status:** Defeated? Pending? (⚔️ = completed, ⏳ = locked)
- **Hints Used:** Your efficiency (more hints = lower score on that chapter)
- **Time Spent:** Total playtime in chapter

### Inventory & Gear

Collect **gear items** from missions:
- System analyzers
- Network scanners
- Security tools
- Debugging equipment

Each item shows:
- **Name:** Equipment identifier
- **Rarity:** Common / Uncommon / Rare
- **Effect:** What it helps with (e.g., "Speeds up network diagnosis")

---

## 💾 Save System

Your progress auto-saves after every mission. You can quit anytime and resume where you left off.

**Save Location:** `~/.config/neongrid9/player_save.json`

To start fresh:
```bash
rm ~/.config/neongrid9/player_save.json
python3 main.py  # New game
```

---

## 🎓 Learning Tips

### For Beginners

1. **Read the story** — Each mission has lore that explains the concept
2. **Take your time** — Don't rush early chapters. Foundation matters.
3. **Use hints wisely** — Free hint for direction, Standard for partial answers, Final for learning
4. **Repeat hard chapters** — You can replay any chapter to solidify learning

### For Efficiency

1. **Speedrun mode** — Set a timer for 30min/chapter challenge
2. **No-hints run** — Beat chapter with zero hints for **Self-Reliant** achievement
3. **Quiz focus** — Answer all quiz questions without hints for deeper retention

### Linking to Linux Exam

| Chapter | Linux Topics |
|---------|---------------|
| Ch01-03 | 101.1, 101.2 (Hardware, Boot) |
| Ch04-05 | 101.3, 102.1 (Filesystems, Partitions) |
| Ch06-07 | 103.4, 103.5 (Users, Processes) |
| Ch08-09 | 103.2, 103.3 (I/O, Shell) |
| Ch10-11 | 104.2, 104.3 (Networks, Services) |
| Ch12-15 | 102.3, 102.4, 103.1 (Packages, Logs, Kernel) |
| Ch16-22 | 102.2, 103.6, 104.1, 104.4+ (Advanced topics) |

**See LPIC_1_MAPPING.md for detailed exam correlations.**

---

## ❓ FAQ

### "How long does the full game take?"

- **Speed run (all missions, no stories):** 8-12 hours
- **Standard playthrough (read stories):** 15-20 hours
- **Completionist (all achievements):** 25-30 hours

### "Can I skip chapters?"

No. Chapters must be completed in order (Ch01 → Ch02 → ... → Ch22). Each chapter builds on previous knowledge.

### "What if I'm stuck on a mission?"

1. Read the story again — It often hints at the answer
2. Use Free Hint
3. Try related missions in same chapter
4. Use Standard or Final hint
5. Take a break and come back fresh

### "Can I replay chapters?"

Yes! After completing Ch01, you can replay it anytime to improve your score or chase achievements.

### "Do I lose XP if I use hints?"

Using hints doesn't cost XP (except Standard/Final hints which cost 20/50 XP as noted). You still get mission XP but hints are tracked separately for scoring.

### "What's the best strategy for bosses?"

- ✅ Complete all regular missions in chapter first
- ✅ Use hints strategically (save Final for actual answer)
- ✅ Read the narrative carefully — It hints at solution
- ✅ If stuck after 2 attempts, use a hint
- ✅ Boss missions combine all chapter skills

### "Can I get all achievements?"

Yes! All achievements are earnable through normal play:
- **Speedrun:** Set 30-min timer per chapter
- **Perfect Streaks:** Practice quiz questions
- **All Bosses:** Complete game normally
- **Faction Master:** Intentionally build faction rep

### "Is there a leaderboard?"

Not yet, but you can track your stats in `player_save.json` and compare with friends.

### "Do I need Linux installed?"

No! The game simulates terminal behavior. Read mission descriptions and answer questions based on your knowledge. For advanced missions, you can test commands on a real Linux machine and report results.

---

## 🚀 Advanced Features

### Difficulty Scaling

As you level up, some missions get harder:
- Lvl 1-4: Standard difficulty
- Lvl 5-9: +10% XP, harder quiz questions
- Lvl 10-14: +20% XP, complex multi-part missions
- Lvl 15+: +30% XP, extreme challenge

### Speedrun Potential

Complete chapters fast for **Speed Runner** achievement:
- Target: <30 minutes per chapter
- Skip story dialogs (press Space)
- Pre-read mission hints
- Focus on regular missions (bosses are long)

### Completionist Goals

For 100% completion:
- 501 missions
- 22 chapters + all bosses
- 18 achievements
- All 5 factions at level 2+
- 10+ gear items collected

---

## 📚 Further Reading

- **LPIC_1_MAPPING.md** — How chapters map to Linux exam topics
- **TIPS_TRICKS.md** — Advanced strategies and speedrun tactics
- **BOSS_GUIDE.md** — Detailed boss fight breakdowns
- **LORE.md** — Full world/story timeline and characters

---

## 🎮 Commands Cheat Sheet

### In-Game Navigation

| Command | Effect |
|---------|--------|
| `Enter` | Continue/Accept |
| `Space` | Skip story dialog |
| `1-3` | Select hint level (or quiz answer) |
| `q` | Quit mission (loses progress on current mission) |

### In-Game Menus

- **Main Menu:** Select chapter or view stats
- **Chapter Hub:** Choose mission or view chapter story
- **Mission Select:** Pick specific mission
- **Results Screen:** View XP earned, hints used, achievements

---

## 🏁 Final Tips

1. **Story matters** — NeonGrid-9 has a real narrative. Read it. You'll enjoy it more.
2. **Pace yourself** — 2-3 chapters per session feels natural
3. **Challenge yourself** — Try each chapter with zero hints first
4. **Compare notes** — Ask friends about their strategies
5. **Celebrate wins** — Boss victories are epic moments. Enjoy them!

---

## Contact & Support

- **Report bugs:** Check for updates or file issues
- **Stuck on a mission?** Review the Free Hint, read the story again, try similar missions
- **Want more content?** Completing all 22 chapters is the ultimate goal

---

**Good luck, Net Runner. The Digital Frontier awaits.** 🌃

*— Z3R0, Your AI Guide*
