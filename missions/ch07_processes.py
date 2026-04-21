"""
NeonGrid-9 :: Kapitel 7 — GHOST PROCESS
LPIC-1 Topic 103.5 / 103.6
Prozesse: Überwachen, Steuern, Priorisieren, Signale

"In NeonGrid-9 ist jeder Prozess ein Soldat.
 Du befiehlst. Du tötest. Du priorisierst.
 Oder der Kernel tut es für dich."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_7_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 7.01 — Was ist ein Prozess?
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.01",
        chapter      = 7,
        title        = "Prozesse — Die Soldaten des Kernels",
        mtype        = "SCAN",
        xp           = 60,
        speaker      = "ZARA Z3R0",
        story        = (
            "NeonGrid-9 läuft auf tausend Prozessen gleichzeitig.\n"
            "Jeder hat eine PID. Eine Mutter. Eine Priorität.\n"
            "Zara Z3R0: 'Kenn deine Prozesse, Ghost.\n"
            " Was läuft? Was verbraucht? Was ist gefährlich?'"
        ),
        why_important = (
            "Prozessverwaltung ist Kern-Sysadmin-Wissen.\n"
            "LPIC-1 prüft: PID, PPID, States, Prozess-Hierarchie, /proc."
        ),
        explanation  = (
            "Prozess-Grundlagen:\n\n"
            "  PID   — Process ID (eindeutige Nummer)\n"
            "  PPID  — Parent Process ID (Elternprozess)\n"
            "  PID 1 — init/systemd (Ur-Prozess, alle anderen sind Kinder)\n\n"
            "Prozess-Zustände:\n"
            "  R — Running (läuft oder wartet auf CPU)\n"
            "  S — Sleeping (wartet auf Ereignis, unterbrechbar)\n"
            "  D — Uninterruptible Sleep (wartet auf I/O, nicht unterbrechbar)\n"
            "  T — Stopped (durch Signal gestoppt)\n"
            "  Z — Zombie (beendet, aber Eltern hat noch nicht gelesen)\n"
            "  I — Idle kernel thread\n\n"
            "Prozess-Informationen:\n"
            "  /proc/<PID>/         — Verzeichnis jedes Prozesses\n"
            "  /proc/<PID>/cmdline  — Befehlszeile\n"
            "  /proc/<PID>/status   — Status und Ressourcen\n"
            "  /proc/<PID>/fd/      — offene Dateideskriptoren\n"
            "  /proc/<PID>/maps     — Speicher-Mappings\n\n"
            "Prozess-Hierarchie:\n"
            "  pstree               # Baum-Ansicht\n"
            "  pstree -p            # mit PIDs\n"
            "  pstree ghost         # Prozesse eines Users"
        ),
        syntax       = "ps\npstree -p\ncat /proc/$$/status",
        example      = (
            "$ cat /proc/1/cmdline\n/sbin/init\n\n"
            "$ pstree -p | head -5\n"
            "systemd(1)─┬─sshd(1337)───sshd(2048)───bash(2049)───pstree(2100)\n"
            "           ├─cron(567)\n"
            "           └─rsyslogd(789)"
        ),
        task_description  = "Zeige die Prozess-Hierarchie",
        expected_commands = ["pstree", "ps"],
        hint_text         = "pstree -p zeigt alle Prozesse als Baum mit PIDs",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist PID 1 bei einem modernen Linux-System?',
                options     = ['A) bash', 'B) kernel', 'C) systemd (oder init)', 'D) cron'],
                correct     = 'C',
                explanation = 'PID 1 = systemd (oder init bei alten Systemen). Alle anderen Prozesse sind Kinder davon.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was ist ein Zombie-Prozess?',
                options     = ['A) Prozess ohne CPU-Zeit', 'B) Beendeter Prozess, dessen Exit-Status noch nicht vom Elternprozess abgerufen wurde', 'C) Prozess mit negativer Priorität', 'D) Daemon ohne Terminal'],
                correct     = 'B',
                explanation = 'Zombie (Z-State): Prozess fertig, aber Eltern hat wait() noch nicht aufgerufen. Zeigt Z in ps.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "PID 1 = systemd (oder init bei alten Systemen).\n"
            "PPID = Parent PID. Alle Prozesse stammen von PID 1 ab.\n"
            "Zombie = Z-State: Prozess beendet, Eltern hat exit() noch nicht gelesen.\n"
            "/proc/<PID>/ = Prozess-Informationen direkt vom Kernel."
        ),
        memory_tip       = "PID=Prozess-ID. PPID=Eltern. Z=Zombie. /proc/PID/=Kernel-Infos.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.02 — ps — Prozesse auflisten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.02",
        chapter      = 7,
        title        = "ps — Prozesse auflisten",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "Rust öffnet ein Terminal und tippt: ps aux\n"
            "Hunderte Prozesse erscheinen auf dem Bildschirm.\n"
            "'ps ist dein Röntgenblick, Ghost.\n"
            " Wer läuft. Wer verbraucht. Wer stirbt.'"
        ),
        why_important = (
            "ps ist der wichtigste Prozess-Diagnose-Befehl.\n"
            "LPIC-1 prüft ps aux, ps -ef und den Unterschied der Notationen."
        ),
        explanation  = (
            "ps — Process Status:\n\n"
            "BSD-Stil (häufigster):\n"
            "  ps aux\n"
            "    a = alle User\n"
            "    u = user-orientiertes Format\n"
            "    x = auch Prozesse ohne Terminal\n\n"
            "System-V-Stil:\n"
            "  ps -ef\n"
            "    -e = alle Prozesse\n"
            "    -f = vollständiges Format\n\n"
            "Ausgabe-Spalten (ps aux):\n"
            "  USER  — Besitzer des Prozesses\n"
            "  PID   — Prozess-ID\n"
            "  %CPU  — CPU-Nutzung\n"
            "  %MEM  — RAM-Nutzung\n"
            "  VSZ   — Virtueller Speicher (kB)\n"
            "  RSS   — Physischer RAM (kB)\n"
            "  TTY   — Terminal (?=keins)\n"
            "  STAT  — Status (R,S,D,T,Z + Flags)\n"
            "  START — Startzeit\n"
            "  TIME  — CPU-Gesamtzeit\n"
            "  COMMAND — Befehl\n\n"
            "Nützliche Kombinationen:\n"
            "  ps aux | grep ssh           # SSH-Prozesse\n"
            "  ps aux | sort -k3 -rn       # nach CPU sortiert\n"
            "  ps aux | sort -k4 -rn       # nach RAM sortiert\n"
            "  ps -p 1337 -o pid,user,cmd  # bestimmte PID + Felder\n"
            "  ps -u ghost                 # Prozesse eines Users\n"
            "  ps --forest                 # Baum-Darstellung"
        ),
        syntax       = "ps aux\nps -ef\nps aux | grep <name>",
        example      = (
            "$ ps aux | head -4\n"
            "USER       PID %CPU %MEM    VSZ   RSS TTY  STAT START   TIME COMMAND\n"
            "root         1  0.0  0.1 168932 14256 ?    Ss   08:00   0:03 /sbin/init\n"
            "root      1337  0.0  0.1  72308  8192 ?    Ss   08:00   0:00 sshd: /usr/sbin/sshd\n"
            "ghost     2048  0.0  0.0  20396  5120 pts/0 Ss  08:05   0:00 -bash"
        ),
        task_description  = "Liste alle laufenden Prozesse auf",
        expected_commands = ["ps aux", "ps -ef", "ps"],
        hint_text         = "ps aux zeigt alle Prozesse aller User",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was bedeutet STAT = 'Z' in ps aux?",
                options     = [
                    "A) Der Prozess ist im Zombie-Zustand",
                    "B) Der Prozess läuft auf einer Z-CPU",
                    "C) Der Prozess ist gesperrt",
                    "D) Der Prozess hat Zero-CPU-Nutzung",
                ],
                correct     = "A",
                explanation = "Z = Zombie. Prozess hat sich beendet, aber der Elternprozess hat noch nicht mit wait() den Exit-Code gelesen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen ps aux und ps -ef?",
                options     = [
                    "A) ps aux zeigt mehr Details",
                    "B) Beide zeigen dieselben Infos in leicht unterschiedlichem Format",
                    "C) ps -ef zeigt keine CPU/MEM-Werte",
                    "D) ps aux zeigt nur User-Prozesse",
                ],
                correct     = "B",
                explanation = "Beide zeigen alle Prozesse, aber in unterschiedlichem Format. aux = BSD-Stil (mit %CPU/%MEM). -ef = System-V-Stil (mit PPID). Inhaltlich ähnlich.",
                xp_value    = 20,
            ),
        ],
        exam_tip         = (
            "ps aux = BSD-Stil (häufigster!). ps -ef = System-V-Stil.\n"
            "Beide zeigen alle Prozesse. aux hat %CPU/%MEM. -ef hat PPID.\n"
            "ps aux | grep sshd — aber Vorsicht: grep selbst erscheint auch!\n"
            "Tipp: ps aux | grep '[s]shd' — filtert sich selbst aus."
        ),
        memory_tip       = "ps aux = alles (a=all u=user x=no-tty). STAT Z=Zombie S=Sleep R=Running.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.03 — top / htop — Live-Prozess-Monitor
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.03",
        chapter      = 7,
        title        = "top — Der Live-Prozess-Monitor",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Ghost braucht einen Echtzeit-Blick auf das System.\n"
            "Zara Z3R0: 'top. Dein Live-Dashboard, Ghost.\n"
            " Sieh wer CPU frisst. Wer RAM monopolisiert.'"
        ),
        why_important = (
            "top ist das Standard-Monitoring-Tool.\n"
            "LPIC-1 prüft top-Interaktion und Ausgabe-Interpretation."
        ),
        explanation  = (
            "top — Task Manager im Terminal:\n\n"
            "  top              # starten\n"
            "  top -n 1         # einmal ausgeben und beenden\n"
            "  top -u ghost     # nur Prozesse eines Users\n"
            "  top -p 1337,2048 # bestimmte PIDs\n\n"
            "top-Kopfzeile:\n"
            "  uptime:   Systemlaufzeit, Benutzeranzahl, Load Average\n"
            "  Tasks:    total, running, sleeping, stopped, zombie\n"
            "  %Cpu(s):  us=user, sy=system, ni=nice, id=idle, wa=I/O-wait\n"
            "  MiB Mem:  total, free, used, buff/cache\n"
            "  MiB Swap: total, free, used, avail Mem\n\n"
            "Interaktive Befehle in top:\n"
            "  q   — beenden\n"
            "  k   — Prozess killen (PID eingeben)\n"
            "  r   — renice (Priorität ändern)\n"
            "  P   — nach CPU sortieren (Standard)\n"
            "  M   — nach Speicher sortieren\n"
            "  T   — nach CPU-Zeit sortieren\n"
            "  N   — nach PID sortieren\n"
            "  u   — nach User filtern\n"
            "  f   — Spalten auswählen\n"
            "  1   — alle CPU-Kerne anzeigen\n"
            "  h   — Hilfe\n\n"
            "Load Average:\n"
            "  Drei Werte: 1min, 5min, 15min\n"
            "  Wert = 1.0 bei 1 CPU = 100% ausgelastet\n"
            "  Bei 4 CPUs: Load 4.0 = 100% ausgelastet\n\n"
            "uptime:\n"
            "  uptime    # Laufzeit + Load Average\n"
            "  w         # User + Laufzeit + Load"
        ),
        syntax       = "top\ntop -n 1 -b | head -20\nuptime",
        example      = (
            "$ uptime\n"
            " 08:15:42 up 15 min,  1 user,  load average: 0.12, 0.08, 0.03\n\n"
            "$ top -n 1 -b | head -8\n"
            "top - 08:15:43 up 15 min, 1 user, load average: 0.12, 0.08, 0.03\n"
            "Tasks: 145 total,   1 running, 144 sleeping,   0 stopped,   0 zombie\n"
            "%Cpu(s):  2.3 us,  0.7 sy,  0.0 ni, 96.7 id,  0.3 wa,  0.0 hi\n"
            "MiB Mem : 15872.0 total,  8934.5 free,  4567.8 used,  2369.7 buff/cache"
        ),
        task_description  = "Zeige Systemlaufzeit und Load Average",
        expected_commands = ["uptime", "top"],
        hint_text         = "uptime zeigt Systemlaufzeit und Load Average",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was bedeuten die drei Load-Average-Werte in top/uptime?',
                options     = ['A) RAM, CPU, Disk', 'B) Letzte 1, 5 und 15 Minuten', 'C) Min, Avg, Max CPU', 'D) 3 CPU-Kerne'],
                correct     = 'B',
                explanation = 'Load Average: 3 Werte für 1/5/15 Minuten. Load 1.0 auf 1-Core = 100% ausgelastet.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Mit welcher Taste sortiert man 'top' nach RAM-Nutzung?",
                options     = ['A) R', 'B) P', 'C) M', 'D) S'],
                correct     = 'C',
                explanation = "top: M = nach Memory, P = nach CPU, N = nach PID. 'k' = kill.",
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "Load Average: 3 Werte für 1/5/15 Minuten.\n"
            "Load = 1.0 auf 1-Core-System = voll ausgelastet.\n"
            "top: M=nach RAM, P=nach CPU, k=kill, r=renice.\n"
            "%wa (I/O wait) hoch = Festplatte ist der Flaschenhals."
        ),
        memory_tip       = "Load Average: 1-5-15min. 1.0/CPU=voll. top: P=CPU M=RAM k=kill.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.04 — Signale: kill / killall / pkill
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.04",
        chapter      = 7,
        title        = "kill / killall / pkill — Signale senden",
        mtype        = "INFILTRATE",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Ein Prozess ist außer Kontrolle. RAM frisst er auf.\n"
            "CPU 100%. System am Limit.\n"
            "Zara Z3R0: 'Zeit zu handeln, Ghost. kill ist kein Mord —\n"
            " es ist Signal-Kommunikation. Die meisten Prozesse wollen es so.'"
        ),
        why_important = (
            "Signale sind das Kommunikationssystem zwischen Prozessen und Kernel.\n"
            "LPIC-1 prüft die wichtigsten Signale und kill/killall/pkill."
        ),
        explanation  = (
            "Signale — Wichtigste:\n\n"
            "  Signal  | Nr | Beschreibung\n"
            "  --------|----|-----------------------\n"
            "  SIGHUP  |  1 | Reload (Daemon neu laden)\n"
            "  SIGINT  |  2 | Interrupt (wie Ctrl+C)\n"
            "  SIGQUIT |  3 | Quit mit Core Dump\n"
            "  SIGKILL |  9 | SOFORT töten (nicht blockierbar!)\n"
            "  SIGTERM | 15 | Graceful terminate (Standard)\n"
            "  SIGSTOP | 19 | Stopp (wie Ctrl+Z, nicht blockierbar)\n"
            "  SIGCONT | 18 | Weitermachen nach STOP\n"
            "  SIGUSR1 | 10 | User-definiert 1\n"
            "  SIGUSR2 | 12 | User-definiert 2\n\n"
            "kill — Signal an PID:\n"
            "  kill 1337              # SIGTERM (Standard)\n"
            "  kill -9 1337           # SIGKILL (sofort)\n"
            "  kill -SIGTERM 1337     # mit Signalname\n"
            "  kill -15 1337          # mit Signalnummer\n"
            "  kill -l                # alle Signale auflisten\n\n"
            "killall — Signal nach Name:\n"
            "  killall firefox        # alle firefox-Prozesse beenden\n"
            "  killall -9 firefox     # SIGKILL\n"
            "  killall -HUP nginx     # reload\n"
            "  killall -u ghost       # alle Prozesse von User ghost\n\n"
            "pkill — Pattern-basiertes kill:\n"
            "  pkill firefox          # Muster-Match\n"
            "  pkill -9 'java.*'      # Regex\n"
            "  pkill -u ghost         # alle Prozesse von ghost\n"
            "  pkill -P 1337          # alle Kinder von PID 1337\n\n"
            "pgrep — PID nach Name/Pattern finden:\n"
            "  pgrep sshd             # PIDs von sshd\n"
            "  pgrep -l sshd          # mit Namen"
        ),
        syntax       = "kill -9 <PID>\nkillall <name>\npkill -u ghost",
        example      = (
            "$ ps aux | grep firefox\nghostuser  2345 99.0  ...  firefox\n\n"
            "$ kill -15 2345    # Graceful shutdown\n"
            "$ kill -9 2345     # Wenn das nicht hilft\n\n"
            "$ killall -HUP nginx   # nginx config neu laden\n"
            "$ pgrep -l sshd\n1337 sshd"
        ),
        task_description  = "Suche nach laufenden Prozessen mit pgrep",
        expected_commands = ["pgrep", "kill", "ps aux"],
        hint_text         = "pgrep sshd findet PIDs aller sshd-Prozesse",
        quiz_questions    = [
            QuizQuestion(
                question    = "Warum sollte man SIGKILL (-9) nur als letztes Mittel einsetzen?",
                options     = [
                    "A) SIGKILL ist langsamer als SIGTERM",
                    "B) SIGKILL kann nicht blockiert werden — Prozess kann nicht aufräumen",
                    "C) SIGKILL braucht root-Rechte",
                    "D) SIGKILL löscht Dateien des Prozesses",
                ],
                correct     = "B",
                explanation = "SIGKILL (9) kann vom Prozess nicht abgefangen werden. Er hat keine Chance aufzuräumen (Dateien zu schließen, Locks zu lösen). SIGTERM (15) ist bevorzugt.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Was macht SIGHUP (1) bei einem Daemon wie nginx?",
                options     = [
                    "A) Beendet nginx sofort",
                    "B) Nginx lädt die Konfiguration neu (reload)",
                    "C) Nginx wird gestoppt und neu gestartet",
                    "D) Nginx ignoriert das Signal",
                ],
                correct     = "B",
                explanation = "Viele Daemons interpretieren SIGHUP als 'reload configuration'. Verbindungen bleiben dabei oft bestehen.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "SIGTERM(15) = höflich beenden. SIGKILL(9) = sofort, kein Aufräumen.\n"
            "SIGHUP(1) = reload. SIGINT(2) = Ctrl+C. SIGSTOP(19) = pausieren.\n"
            "kill -l = alle Signale. killall nach Name. pkill nach Muster.\n"
            "Daemon reload: kill -HUP <PID> oder killall -HUP nginx"
        ),
        memory_tip       = "15=TERM(höflich). 9=KILL(brutal). 1=HUP(reload). 2=INT(Ctrl+C).",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.05 — Jobs: & / fg / bg / jobs / nohup
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.05",
        chapter      = 7,
        title        = "Jobs — Hintergrund & Vordergrund",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "Ghost startet einen langen Download.\n"
            "Jetzt blockiert er das Terminal.\n"
            "Rust: 'Hintergrund, Ghost. & ist dein Freund.\n"
            " Lass es laufen. Mach weiter.'"
        ),
        why_important = (
            "Job-Control ist essentiell für Terminal-Produktivität.\n"
            "LPIC-1: &, fg, bg, jobs, nohup, Ctrl+Z, Ctrl+C."
        ),
        explanation  = (
            "Job-Control:\n\n"
            "Prozess im Hintergrund starten:\n"
            "  befehl &             # startet im Hintergrund\n"
            "  sleep 100 &          # sleep 100 Sekunden im BG\n"
            "  [1] 1337             # Job-Nr [1], PID 1337\n\n"
            "Jobs anzeigen:\n"
            "  jobs                 # alle Jobs der aktuellen Shell\n"
            "  jobs -l              # mit PIDs\n\n"
            "Vordergrund/Hintergrund:\n"
            "  fg                   # letzten BG-Job in FG holen\n"
            "  fg %1                # Job 1 in den Vordergrund\n"
            "  bg                   # gestoppten Job im BG weiterlaufen lassen\n"
            "  bg %2                # Job 2\n\n"
            "Tastenkombinationen:\n"
            "  Ctrl+C   — Prozess beenden (SIGINT)\n"
            "  Ctrl+Z   — Prozess pausieren (SIGSTOP) und in BG\n"
            "             → dann 'bg' zum Weiterlaufen oder 'fg' zum Holen\n\n"
            "nohup — Prozess nach Shell-Ende weiterlaufen lassen:\n"
            "  nohup befehl &\n"
            "  nohup python3 server.py > server.log 2>&1 &\n"
            "  # Ausgabe geht nach nohup.out wenn nicht umgeleitet\n"
            "  # Prozess überlebt Shell-Ende (SIGHUP wird ignoriert)\n\n"
            "disown — Job von Shell trennen:\n"
            "  disown %1            # Job 1 von Shell-Job-Liste entfernen\n"
            "  disown -h %1         # SIGHUP ignorieren aber in Liste behalten"
        ),
        syntax       = "befehl &\njobs\nfg %1\nbg\nnohup befehl &",
        example      = (
            "$ sleep 300 &\n[1] 2222\n\n"
            "$ jobs -l\n[1]+  2222 Running    sleep 300 &\n\n"
            "$ fg %1\nsleep 300\n^Z\n[1]+  Stopped    sleep 300\n\n"
            "$ bg\n[1]+ sleep 300 &\n\n"
            "$ nohup python3 server.py > server.log 2>&1 &\n[2] 3333"
        ),
        task_description  = "Starte einen Hintergrundprozess und zeige Jobs",
        expected_commands = ["jobs", "ps"],
        hint_text         = "jobs zeigt alle Hintergrundprozesse der aktuellen Shell",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'Ctrl+Z' bei einem laufenden Prozess?",
                options     = ['A) Beendet den Prozess', 'B) Pausiert den Prozess (SIGSTOP) und schickt ihn in den Hintergrund', 'C) Wechselt in den Hintergrund ohne Pause', 'D) Öffnet neues Terminal'],
                correct     = 'B',
                explanation = "Ctrl+Z = SIGSTOP = Prozess pausieren. Dann 'bg' zum Weiterlaufen im Hintergrund.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was macht nohup?',
                options     = ['A) Kein Hang-Up: Prozess läuft weiter auch nach SSH-Logout', 'B) Höhere Priorität', 'C) Keine CPU-Nutzung', 'D) Nur für Hintergrundprozesse'],
                correct     = 'A',
                explanation = 'nohup = no hangup. Prozess ignoriert SIGHUP beim SSH-Logout. Ausgabe → nohup.out.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "& = im Hintergrund starten.\n"
            "Ctrl+Z = pausieren (SIGSTOP). Dann: bg = weiterlaufen im BG.\n"
            "fg %1 = Job 1 in Vordergrund. jobs = aktuelle Jobs.\n"
            "nohup = SIGHUP ignorieren = überlebt Shell-Logout."
        ),
        memory_tip       = "& = Hintergrund. Ctrl+Z = pausiert. bg = im BG weiter. fg = in Vordergrund.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.06 — nice / renice — Prioritäten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.06",
        chapter      = 7,
        title        = "nice & renice — CPU-Prioritäten steuern",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA Z3R0",
        story        = (
            "Ein Backup-Prozess blockiert den ganzen Server.\n"
            "Alle anderen Prozesse warten.\n"
            "Zara Z3R0: 'nice, Ghost. Gib dem Backup weniger Priorität.\n"
            " Der Kernel verteilt CPU nach Nice-Wert.'"
        ),
        why_important = (
            "nice und renice steuern CPU-Priorität.\n"
            "LPIC-1: Nice-Bereich -20 bis 19, wer darf welche Werte setzen."
        ),
        explanation  = (
            "Prioritäten in Linux:\n\n"
            "  Nice-Wert: -20 (höchste Priorität) bis 19 (niedrigste)\n"
            "  Standard:  0\n"
            "  Negativ:   mehr CPU (nur root)\n"
            "  Positiv:   weniger CPU (jeder User)\n\n"
            "nice — Prozess mit Priorität starten:\n"
            "  nice befehl                # Nice = 10 (Standard-Erhöhung)\n"
            "  nice -n 15 backup.sh       # Nice = 15 (niedrige Priorität)\n"
            "  nice -n -5 wichtig.sh      # Nice = -5 (hohe Prio, nur root)\n"
            "  nice -15 backup.sh         # Kurzform ohne -n\n\n"
            "renice — laufenden Prozess ändern:\n"
            "  renice 10 -p 1337          # PID 1337 auf Nice 10\n"
            "  renice -5 -p 1337          # Auf -5 (nur root)\n"
            "  renice 5 -u ghost          # alle Prozesse von ghost\n"
            "  renice 15 -g www-data      # alle Prozesse einer Gruppe\n\n"
            "Priorität anzeigen:\n"
            "  ps aux             # NI-Spalte (Nice-Wert)\n"
            "  top                # NI-Spalte\n"
            "  ps -o pid,ni,cmd   # nur PID, NI und Command\n\n"
            "Merksatz:\n"
            "  'Nice = 19' = sehr nett = gibt anderen den Vortritt\n"
            "  'Nice = -20' = nicht nett = nimmt alles für sich"
        ),
        syntax       = "nice -n 15 backup.sh\nrenice 10 -p <PID>",
        example      = (
            "$ nice -n 19 find / -name '*.log' > /tmp/logs.txt &\n[1] 2345\n\n"
            "$ renice 15 -p 2345\n2345 (process ID) old priority 19, new priority 15\n\n"
            "$ ps -o pid,ni,cmd -p 2345\n  PID  NI CMD\n 2345  15 find / -name *.log"
        ),
        task_description  = "Zeige Nice-Werte laufender Prozesse",
        expected_commands = ["ps aux", "ps -o pid,ni,cmd"],
        hint_text         = "ps aux zeigt den NI (Nice) Wert in einer der Spalten",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welcher Nice-Wert gibt einem Prozess die HÖCHSTE CPU-Priorität?",
                options     = ["A) 19", "B) 0", "C) -20", "D) 100"],
                correct     = "C",
                explanation = "Nice-Wert -20 = höchste Priorität (bekommt am meisten CPU). 19 = niedrigste Priorität. 0 = Standard.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Welcher Benutzer darf den Nice-Wert eines Prozesses auf -5 senken?",
                options     = [
                    "A) Jeder Benutzer",
                    "B) Der Besitzer des Prozesses",
                    "C) Nur root",
                    "D) Nur Mitglieder der sudo-Gruppe",
                ],
                correct     = "C",
                explanation = "Nur root kann Nice-Werte unter 0 setzen oder Prozesse anderer User renicen. Normale User können nur auf positive Werte (0-19) erhöhen.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "Nice-Bereich: -20 (höchste Prio) bis +19 (niedrigste Prio).\n"
            "nice = beim Start setzen. renice = laufenden Prozess ändern.\n"
            "Nur root darf negative Werte setzen.\n"
            "Normale User können Wert NUR erhöhen (mehr 'nett' = weniger CPU)."
        ),
        memory_tip       = "Nice=-20=gierig. Nice=19=nett(gibt CPU ab). Nur root=negativ.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.07 — free / vmstat / iostat — Ressourcen-Monitoring
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.07",
        chapter      = 7,
        title        = "free / vmstat / iostat — Ressourcen überwachen",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "Das System wird langsam. Ghost fragt sich: RAM? CPU? Disk?\n"
            "Rust: 'free zeigt dir RAM. vmstat zeigt alles.\n"
            " iostat zeigt den Festplatten-Engpass. Diagnose, Ghost!'"
        ),
        why_important = (
            "System-Monitoring-Tools sind Examen-Standard.\n"
            "LPIC-1 fragt nach free -h Output und vmstat-Interpretation."
        ),
        explanation  = (
            "free — RAM und Swap:\n\n"
            "  free           # Bytes\n"
            "  free -h        # human-readable\n"
            "  free -m        # Megabytes\n"
            "  free -s 2      # alle 2 Sekunden aktualisieren\n\n"
            "  Ausgabe:\n"
            "    total  used  free  shared  buff/cache  available\n"
            "  'available' = was neue Prozesse nutzen können\n"
            "  buff/cache kann vom Kernel freigegeben werden\n\n"
            "vmstat — Virtual Memory Statistics:\n\n"
            "  vmstat         # einmal\n"
            "  vmstat 2       # alle 2 Sekunden\n"
            "  vmstat 2 5     # 5 Ausgaben alle 2 Sekunden\n\n"
            "  Wichtige Spalten:\n"
            "    r  — Run queue (wartende Prozesse)\n"
            "    b  — Blocked (I/O warten)\n"
            "    si/so — Swap In/Out (> 0 = System swappt)\n"
            "    us/sy — User/System CPU %\n"
            "    id    — Idle CPU %\n"
            "    wa    — I/O Wait %\n\n"
            "iostat — I/O-Statistiken:\n\n"
            "  iostat         # CPU + Disk-Statistiken\n"
            "  iostat -x      # erweitert (inkl. %util)\n"
            "  iostat 2       # alle 2 Sekunden\n"
            "  iostat -d nvme0n1  # nur ein Gerät\n\n"
            "  %util nahe 100% = Festplatte ist Flaschenhals\n\n"
            "watch — Befehl regelmäßig wiederholen:\n"
            "  watch -n 2 free -h   # free alle 2 Sekunden"
        ),
        syntax       = "free -h\nvmstat 2 5\niostat -x",
        example      = (
            "$ free -h\n"
            "               total        used        free  buff/cache   available\n"
            "Mem:            15Gi        4.5Gi       8.7Gi   2.3Gi       8.9Gi\n"
            "Swap:          2.0Gi          0B       2.0Gi\n\n"
            "$ vmstat 1 3\nprocs r  b   swpd   free  buff  cache   si  so   bi  bo  us  sy  id  wa\n"
            "      1  0      0 8934512 234567 2345678    0   0    5   2   2   1  97   0"
        ),
        task_description  = "Zeige RAM-Nutzung mit free",
        expected_commands = ["free", "free -h"],
        hint_text         = "free -h zeigt RAM in lesbarem Format",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was bedeutet si/so > 0 in vmstat?',
                options     = ['A) System-Idle > 0', 'B) Das System lagert Speicher aus (swap in/out) — RAM-Problem!', 'C) I/O-Operationen', 'D) System-Interrupts'],
                correct     = 'B',
                explanation = 'vmstat si=swap in, so=swap out. Beide > 0 = System swappt = RAM knapp!',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was zeigt 'free -h' im Feld 'available'?",
                options     = ['A) Freier RAM (physisch leer)', 'B) Tatsächlich verfügbarer RAM (inkl. Cache der freigegeben werden kann)', 'C) Swap-Größe', 'D) Shared Memory'],
                correct     = 'B',
                explanation = "'available' ist wichtiger als 'free'! Enthält freien + freigebbaren Cache.",
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "free -h: 'available' = was wirklich nutzbar ist (nicht 'free'!).\n"
            "vmstat: si/so > 0 = System swappt = RAM-Problem!\n"
            "vmstat: wa hoch = I/O-Engpass.\n"
            "iostat %util ≈ 100% = Festplatte saturiert."
        ),
        memory_tip       = "free -h: available=nutzbar. vmstat si/so>0=swap läuft. wa=I/O-wait.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.08 — lsof / fuser — Offene Dateien & Ports
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.08",
        chapter      = 7,
        title        = "lsof & fuser — Wer hält was offen?",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "'umount: device is busy.'\n"
            "Ghost starrt auf den Fehler. Was hält das Dateisystem?\n"
            "Zara Z3R0: 'lsof. List Open Files. Es zeigt dir alles.'"
        ),
        why_important = (
            "lsof ist unverzichtbar für Diagnose-Aufgaben.\n"
            "LPIC-1: lsof für Port-Analyse und 'device busy'-Debugging."
        ),
        explanation  = (
            "lsof — List Open Files:\n\n"
            "  lsof                   # ALLE offenen Dateien (sehr viel!)\n"
            "  lsof /var/log/syslog   # wer hat diese Datei offen?\n"
            "  lsof /mnt              # warum ist das Dateisystem busy?\n"
            "  lsof -u ghost          # alle offenen Dateien von ghost\n"
            "  lsof -p 1337           # alle Dateien von PID 1337\n"
            "  lsof -c sshd           # Dateien von Prozessen namens sshd\n\n"
            "Netzwerk-Diagnose:\n"
            "  lsof -i                # alle Netzwerk-Verbindungen\n"
            "  lsof -i :22            # wer lauscht/nutzt Port 22?\n"
            "  lsof -i TCP            # alle TCP-Verbindungen\n"
            "  lsof -i TCP:80         # Port 80\n"
            "  lsof -i @192.168.1.1   # Verbindungen zu einer IP\n\n"
            "Gelöschte Dateien finden:\n"
            "  lsof | grep deleted    # Dateien gelöscht aber noch geöffnet\n"
            "  # → df zeigt Speicher belegt, aber ls zeigt Datei nicht mehr\n"
            "  # → Lösung: Prozess killen oder neu starten\n\n"
            "fuser — Prozesse nach Datei/Port:\n"
            "  fuser /mnt             # PID die /mnt nutzt\n"
            "  fuser -m /mnt          # alle auf diesem Dateisystem\n"
            "  fuser -k /mnt          # Prozesse killen (SIGTERM)\n"
            "  fuser -k -9 /mnt       # SIGKILL\n"
            "  fuser 22/tcp           # wer nutzt TCP-Port 22?"
        ),
        syntax       = "lsof /mnt\nlsof -i :80\nfuser -m /mnt",
        example      = (
            "$ lsof /mnt/usb\nCOMMAND  PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME\n"
            "bash    2048  ghost  cwd    DIR    8,1     4096  128 /mnt/usb\n\n"
            "$ lsof -i :22\nCOMMAND PID  USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME\n"
            "sshd   1337  root    3u  IPv4   12345    0t0  TCP *:22 (LISTEN)"
        ),
        task_description  = "Zeige Prozesse die einen bestimmten Port nutzen",
        expected_commands = ["lsof -i :22", "lsof", "fuser"],
        hint_text         = "lsof -i :22 zeigt welcher Prozess Port 22 nutzt",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Wie findest du, welcher Prozess Port 80 belegt?',
                options     = ['A) ps -p 80', 'B) lsof -i :80', 'C) top --port 80', 'D) netstat -pid 80'],
                correct     = 'B',
                explanation = 'lsof -i :80 zeigt Prozess auf Port 80. ss -tulpn | grep :80 geht auch.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was tust du, wenn umount 'device is busy' meldet?",
                options     = ['A) Reboot sofort', 'B) lsof /mnt oder fuser -m /mnt', 'C) umount --ignore-busy', 'D) rm -rf /mnt/*'],
                correct     = 'B',
                explanation = 'lsof /mountpoint zeigt welche Prozesse das Dateisystem offen halten.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "umount: device busy → lsof /mnt oder fuser -m /mnt.\n"
            "lsof -i :80 = wer nutzt Port 80?\n"
            "lsof | grep deleted = Speicher belegt aber Datei gelöscht.\n"
            "fuser -k /mnt = Prozesse die Dateisystem nutzen killen."
        ),
        memory_tip       = "lsof=List Open Files. lsof -i=Netzwerk. fuser -m=Dateisystem-Nutzer.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.09 — screen / tmux — Terminal-Multiplexer
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.09",
        chapter      = 7,
        title        = "screen & tmux — Unsterbliche Sessions",
        mtype        = "CONSTRUCT",
        xp           = 75,
        speaker      = "RUST",
        story        = (
            "Ghost startet ein 8-Stunden-Backup über SSH.\n"
            "Die Verbindung bricht ab. Alles verloren.\n"
            "Rust grinst bitter: 'screen. Oder tmux.\n"
            " Sessions die SSH-Drops überleben.'"
        ),
        why_important = (
            "screen ist LPIC-1 Prüfungsstoff.\n"
            "Wichtig für lange Admin-Tasks über SSH."
        ),
        explanation  = (
            "screen — Terminal-Multiplexer:\n\n"
            "  screen                 # neue Session\n"
            "  screen -S 'backup'     # Session mit Name\n"
            "  screen -ls             # Sessions auflisten\n"
            "  screen -r              # letzte Session fortsetzen\n"
            "  screen -r backup       # bestimmte Session\n"
            "  screen -d -r backup    # erzwingen fortsetzen\n\n"
            "screen Tastenkombinationen (Ctrl+A = Prefix):\n"
            "  Ctrl+A d    — detach (Session läuft im Hintergrund)\n"
            "  Ctrl+A c    — neue Fenster erstellen\n"
            "  Ctrl+A n/p  — nächstes/vorheriges Fenster\n"
            "  Ctrl+A \"    — Fensterliste\n"
            "  Ctrl+A k    — Fenster töten\n"
            "  Ctrl+A ?    — Hilfe\n\n"
            "tmux — modernere Alternative:\n"
            "  tmux                   # neue Session\n"
            "  tmux new -s 'backup'   # Session mit Name\n"
            "  tmux ls                # Sessions auflisten\n"
            "  tmux attach -t backup  # Session fortsetzen\n\n"
            "tmux Prefix: Ctrl+B\n"
            "  Ctrl+B d    — detach\n"
            "  Ctrl+B %    — vertikaler Split\n"
            "  Ctrl+B \"    — horizontaler Split\n"
            "  Ctrl+B c    — neues Fenster\n"
            "  Ctrl+B ,    — Fenster umbenennen"
        ),
        syntax       = "screen -S 'session'\nCtrl+A d  # detach\nscreen -r  # reattach",
        example      = (
            "$ screen -S backup\n# Innerhalb der screen-Session:\n$ nohup tar -czf /backup/full.tar.gz /home/ &\n"
            "# Ctrl+A dann d  → detach\n\n"
            "$ screen -ls\nThere is a screen on: 3456.backup (Detached)\n\n"
            "$ screen -r backup\n# Session wieder verbunden!"
        ),
        task_description  = "Zeige laufende Screen-Sessions",
        expected_commands = ["screen -ls", "tmux ls"],
        hint_text         = "screen -ls zeigt alle aktiven Screen-Sessions",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'Ctrl+A d' in screen?",
                options     = ['A) Alle Sessions löschen', 'B) Session detachen (läuft im Hintergrund weiter)', 'C) Neues Fenster öffnen', 'D) Screen beenden'],
                correct     = 'B',
                explanation = "Ctrl+A d = detach. Session läuft weiter. 'screen -r' zum Wiederverbinden.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welcher Befehl listet alle laufenden screen-Sessions auf?',
                options     = ['A) screen -list', 'B) screen -ls', 'C) screen --show', 'D) sessions -screen'],
                correct     = 'B',
                explanation = 'screen -ls zeigt alle Sessions. screen -r SESSION zum Verbinden.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "screen -S name = Session mit Name erstellen.\n"
            "Ctrl+A d = detach (Session läuft weiter).\n"
            "screen -r = reattach (Session fortsetzen).\n"
            "nohup = Alternative für einfache Hintergrundprozesse."
        ),
        memory_tip       = "screen: Ctrl+A d=detach. screen -r=reattach. -S=Name. -ls=auflisten.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.10 — strace — Systemaufrufe verfolgen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.10",
        chapter      = 7,
        title        = "strace — Systemaufrufe eines Prozesses verfolgen",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "DAEMON",
        story        = (
            "Ein Prozess macht etwas — aber was genau?\n"
            "Ghost sieht nur die Oberfläche. strace zeigt das Innere.\n"
            "Daemon: 'strace, Ghost. System Trace.\n"
            " Jeder Kernel-Call wird sichtbar. Jede offene Datei. Jeder Netzwerk-Socket.'"
        ),
        why_important = (
            "strace ist das wichtigste Debug-Tool für Prozess-Diagnose auf Kernel-Ebene.\n"
            "LPIC-1 prüft strace Grundlagen: -p für laufende Prozesse, -e für Filter."
        ),
        explanation  = (
            "strace — System Call Tracer:\n\n"
            "Neuen Prozess mit strace starten:\n"
            "  strace ls /etc               # ls ausführen und alle syscalls zeigen\n"
            "  strace -o output.txt ls /etc  # Ausgabe in Datei\n\n"
            "Laufenden Prozess anhängen:\n"
            "  strace -p 1337               # PID 1337 beobachten\n"
            "  strace -p 1337 -o trace.txt  # in Datei schreiben\n\n"
            "Syscalls filtern (-e):\n"
            "  strace -e trace=open,read ls  # nur open() und read()\n"
            "  strace -e trace=file ls       # alle datei-bezogenen syscalls\n"
            "  strace -e trace=network curl  # netzwerk-bezogene syscalls\n"
            "  strace -e trace=process cmd   # Prozess-bezogene syscalls\n\n"
            "Nützliche Optionen:\n"
            "  strace -f cmd                 # fork() folgen (Kindprozesse)\n"
            "  strace -t cmd                 # Zeitstempel\n"
            "  strace -T cmd                 # Zeit pro syscall\n"
            "  strace -c cmd                 # Statistik: Anzahl/Zeit pro syscall\n"
            "  strace -s 200 cmd             # String-Ausgabe bis 200 Zeichen\n\n"
            "Typische Syscalls:\n"
            "  open/openat   — Datei öffnen\n"
            "  read/write    — Lesen/Schreiben\n"
            "  close         — Dateideskriptor schließen\n"
            "  execve        — Programm ausführen\n"
            "  fork/clone    — Kindprozess erstellen\n"
            "  connect       — Netzwerkverbindung aufbauen\n"
            "  mmap          — Speicher mappen\n\n"
            "Anwendungsfälle:\n"
            "  - Warum schlägt ein Befehl fehl? (Permission denied?)\n"
            "  - Welche Konfigurationsdateien liest ein Programm?\n"
            "  - Warum ist ein Programm langsam?"
        ),
        syntax       = "strace -p <PID>\nstrace -e trace=file cmd\nstrace -c cmd",
        example      = (
            "$ strace -e trace=open,openat cat /etc/hostname 2>&1 | head -5\n"
            "openat(AT_FDCWD, \"/etc/hostname\", O_RDONLY) = 3\n"
            "openat(AT_FDCWD, \"/etc/ld.so.cache\", O_RDONLY|O_CLOEXEC) = 3\n\n"
            "$ strace -c ls /etc 2>&1\n"
            "% time     seconds  usecs/call     calls    syscall\n"
            "  60.00    0.000123          3        45 openat\n"
            "  30.00    0.000061          2        28 read"
        ),
        task_description  = "Verfolge Systemaufrufe eines Befehls mit strace",
        expected_commands = ["strace ls", "strace -p"],
        hint_text         = "strace ls /etc zeigt alle Kernel-Aufrufe von ls",
        quiz_questions    = [
            QuizQuestion(
                question    = "strace -e trace=file ls — was wird gefiltert angezeigt?",
                options     = [
                    "A) Nur Systemaufrufe die mit Dateien interagieren",
                    "B) Nur Datei-Ausgaben von ls",
                    "C) Alle Systemaufrufe die 'file' als String enthalten",
                    "D) Nur Fehler bei Dateizugriffen",
                ],
                correct     = 0,
                explanation = "-e trace=file filtert auf datei-bezogene Syscalls (open, read, write, close, stat etc.).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Wozu nutzt man 'strace -p <PID>'?",
                options     = [
                    "A) Um einen Prozess zu starten",
                    "B) Um einen bereits laufenden Prozess zu beobachten",
                    "C) Um einen Prozess zu beenden",
                    "D) Um die Priorität eines Prozesses zu ändern",
                ],
                correct     = 1,
                explanation = "-p = attach to process. strace hängt sich an einen bereits laufenden Prozess und beobachtet dessen Systemaufrufe.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "strace = Systemaufrufe (kernel calls) verfolgen.\n"
            "strace -p PID = an laufenden Prozess hängen.\n"
            "strace -e trace=file = nur datei-bezogene Calls.\n"
            "strace -c = Statistik aller Syscalls."
        ),
        memory_tip       = "strace=syscall-trace. -p=laufend anhängen. -e trace=X=filtern. -c=Statistik.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.11 — lsof — Offene Dateien und Ports
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.11",
        chapter      = 7,
        title        = "lsof — List Open Files: Prozesse und Dateien",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "'umount: device is busy.'\n"
            "Ghost starrt auf den Fehler. Was hält das Dateisystem?\n"
            "Cipher: 'lsof — List Open Files.\n"
            " Jede offene Datei, jeder Port, jeder Socket. Alles sichtbar.'"
        ),
        why_important = (
            "lsof ist das wichtigste Diagnose-Tool für offene Ressourcen.\n"
            "LPIC-1 prüft lsof -p, -u, -i für Prozess-, User- und Port-Analyse."
        ),
        explanation  = (
            "lsof — List Open Files:\n\n"
            "Alle offenen Dateien:\n"
            "  lsof               # ALLE offenen Dateien (viel Output!)\n"
            "  lsof | head        # erste 10 Einträge\n\n"
            "Nach Prozess:\n"
            "  lsof -p 1337       # alle offenen Dateien von PID 1337\n"
            "  lsof -c sshd       # alle Dateien von Prozessen namens sshd\n\n"
            "Nach Benutzer:\n"
            "  lsof -u ghost      # alle offenen Dateien von User ghost\n"
            "  lsof -u ghost,root # mehrere User\n"
            "  lsof -u ^ghost     # alle AUSSER ghost (^=negation)\n\n"
            "Nach Port/Netzwerk:\n"
            "  lsof -i            # alle Netzwerk-Dateien\n"
            "  lsof -i :22        # wer nutzt Port 22?\n"
            "  lsof -i :80        # wer nutzt Port 80?\n"
            "  lsof -i TCP:443    # TCP Port 443\n"
            "  lsof -i UDP        # alle UDP-Verbindungen\n"
            "  lsof -i @10.0.0.1  # Verbindungen zu IP\n\n"
            "Nach Datei/Verzeichnis:\n"
            "  lsof /var/log/syslog   # wer hat diese Datei offen?\n"
            "  lsof /mnt              # warum ist Dateisystem busy?\n"
            "  lsof +D /var/log       # alle Dateien unter /var/log\n\n"
            "Gelöschte Dateien:\n"
            "  lsof | grep deleted    # gelöschte aber noch geöffnete Dateien\n"
            "  # df zeigt voll, ls zeigt nichts → lsof findet die 'Geister'\n\n"
            "Wichtige Ausgabe-Spalten:\n"
            "  COMMAND — Prozessname\n"
            "  PID     — Prozess-ID\n"
            "  USER    — Besitzer\n"
            "  FD      — File Descriptor\n"
            "  TYPE    — REG, DIR, CHR, IPv4, IPv6\n"
            "  NAME    — Dateiname oder Verbindung"
        ),
        syntax       = "lsof -p <PID>\nlsof -u <user>\nlsof -i :<port>",
        example      = (
            "$ lsof -i :22\n"
            "COMMAND  PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME\n"
            "sshd    1337 root    3u  IPv4   12345    0t0  TCP *:22 (LISTEN)\n\n"
            "$ lsof -p 1337 | head -5\n"
            "COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME\n"
            "sshd    1337 root  cwd    DIR    8,1     4096    2 /\n"
            "sshd    1337 root  mem    REG    8,1  1873648  123 /lib/x86_64-linux-gnu/libc.so.6"
        ),
        task_description  = "Zeige welcher Prozess Port 22 nutzt",
        expected_commands = ["lsof -i :22", "lsof -i"],
        hint_text         = "lsof -i :22 zeigt welcher Prozess TCP/UDP Port 22 nutzt",
        quiz_questions    = [
            QuizQuestion(
                question    = "'umount /mnt' schlägt mit 'device is busy' fehl. Welcher lsof-Befehl hilft?",
                options     = [
                    "A) lsof /mnt",
                    "B) lsof -i /mnt",
                    "C) lsof -p /mnt",
                    "D) lsof -d /mnt",
                ],
                correct     = 0,
                explanation = "lsof /mnt zeigt alle Prozesse die das Verzeichnis /mnt oder Dateien darin geöffnet haben. Alternativ: lsof +D /mnt für rekursiv.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "lsof -u ^ghost — was bedeutet das '^'?",
                options     = [
                    "A) Dateien die mit dem Zeichen ^ beginnen",
                    "B) Negation: alle offenen Dateien AUSSER von User ghost",
                    "C) Dateien die von ghost erstellt wurden",
                    "D) Dateien im Home-Verzeichnis von ghost",
                ],
                correct     = 1,
                explanation = "In lsof ist ^ eine Negation. -u ^ghost = alle User außer ghost. Nützlich um Systemdateien von User-Dateien zu trennen.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "lsof -p PID = offene Dateien eines Prozesses.\n"
            "lsof -u user = offene Dateien eines Users.\n"
            "lsof -i :port = wer nutzt diesen Port?\n"
            "lsof | grep deleted = gelöschte aber noch geöffnete Dateien (Speicher-Leak-Diagnose)."
        ),
        memory_tip       = "lsof=List Open Files. -p=Prozess. -u=User. -i=Netzwerk. +D=Verzeichnis rekursiv.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.12 — fuser — Prozess hinter Datei/Port finden
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.12",
        chapter      = 7,
        title        = "fuser — Wer benutzt diese Datei oder diesen Port?",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "DAEMON",
        story        = (
            "Das Dateisystem lässt sich nicht aushängen.\n"
            "Etwas benutzt es noch. Aber was?\n"
            "Daemon: 'fuser, Ghost.\n"
            " File User. Direkt. Präzise. Und fuser -k — tötet es auch gleich.'"
        ),
        why_important = (
            "fuser ist ein schnelles Tool um blockierende Prozesse zu identifizieren.\n"
            "LPIC-1 prüft fuser für Dateisystem- und Port-Diagnose."
        ),
        explanation  = (
            "fuser — File User:\n\n"
            "Welcher Prozess nutzt eine Datei/ein Verzeichnis:\n"
            "  fuser /mnt/usb            # PID die /mnt/usb nutzt\n"
            "  fuser -m /mnt/usb         # alle Prozesse auf diesem Dateisystem\n"
            "  fuser -v /var/log/syslog  # verbose mit Details\n\n"
            "Welcher Prozess nutzt einen Port:\n"
            "  fuser 22/tcp              # wer nutzt TCP-Port 22?\n"
            "  fuser 80/tcp              # wer nutzt TCP-Port 80?\n"
            "  fuser 53/udp              # wer nutzt UDP-Port 53?\n\n"
            "Prozesse killen:\n"
            "  fuser -k /mnt/usb         # alle Prozesse auf /mnt/usb beenden (SIGTERM)\n"
            "  fuser -k -9 /mnt/usb      # mit SIGKILL\n"
            "  fuser -k -SIGHUP 22/tcp   # mit SIGHUP\n\n"
            "Ausgabe:\n"
            "  $ fuser /mnt/usb\n"
            "  /mnt/usb:  2048c  3021  4096\n"
            "  # Bedeutung der Suffixe:\n"
            "  c = current directory (cwd)\n"
            "  e = executable\n"
            "  f = open file\n"
            "  m = mmap (memory-mapped)\n"
            "  r = root directory\n\n"
            "Verbose-Ausgabe:\n"
            "  fuser -v /mnt/usb\n"
            "  # Zeigt: USER, PID, ACCESS, COMMAND\n\n"
            "fuser vs lsof:\n"
            "  fuser: einfach, fokussiert, kann killen\n"
            "  lsof:  mehr Details, flexibler, mehr Optionen"
        ),
        syntax       = "fuser /mnt/usb\nfuser 80/tcp\nfuser -k /mnt\nfuser -v -m /mnt",
        example      = (
            "$ fuser /mnt/usb\n/mnt/usb:   2048c  3021\n\n"
            "$ fuser -v /mnt/usb\n"
            "                     USER        PID ACCESS COMMAND\n"
            "/mnt/usb:            ghost      2048 ..c.. bash\n"
            "                     ghost      3021 ..f.. vim\n\n"
            "$ fuser -k /mnt/usb\n/mnt/usb:   2048c  3021\n"
            "# Prozesse 2048 und 3021 wurden mit SIGTERM beendet\n\n"
            "$ fuser 22/tcp\n22/tcp:  1337"
        ),
        task_description  = "Finde Prozesse die Port 22 nutzen mit fuser",
        expected_commands = ["fuser 22/tcp", "fuser"],
        hint_text         = "fuser 22/tcp zeigt die PID des Prozesses der TCP-Port 22 nutzt",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'fuser -k /mnt/data'?",
                options     = [
                    "A) Zeigt Prozesse die /mnt/data nutzen",
                    "B) Beendet alle Prozesse die /mnt/data nutzen (SIGTERM)",
                    "C) Hängt /mnt/data aus",
                    "D) Sperrt /mnt/data für andere Prozesse",
                ],
                correct     = 1,
                explanation = "-k = kill. fuser -k sendet SIGTERM an alle Prozesse die das angegebene Dateisystem/Datei nutzen.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "fuser gibt hinter einer PID den Buchstaben 'c' aus. Was bedeutet das?",
                options     = [
                    "A) Die Datei ist im Cache",
                    "B) Das Verzeichnis ist das aktuelle Arbeitsverzeichnis (cwd) des Prozesses",
                    "C) Die Datei ist eine Konfigurationsdatei",
                    "D) Der Prozess ist ein Child-Prozess",
                ],
                correct     = 1,
                explanation = "c = current working directory. Der Prozess hat das Verzeichnis als sein aktuelles Arbeitsverzeichnis gesetzt (z.B. durch cd).",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "fuser /datei = Prozesse die Datei/Verzeichnis nutzen.\n"
            "fuser port/tcp = Prozess hinter TCP-Port.\n"
            "fuser -k = alle blockierenden Prozesse killen.\n"
            "fuser -v = verbose (User, PID, ACCESS, COMMAND)."
        ),
        memory_tip       = "fuser=File User. -k=kill. port/tcp=Port-Nutzung. 'c'=cwd(aktuell-Verz).",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.13 — Prozesspriorität & nice (vertieft)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.13",
        chapter      = 7,
        title        = "Prozesspriorität & nice — CPU fair verteilen",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "Das Backup-Skript frisst 100% CPU und blockiert alles andere.\n"
            "Ghost muss handeln ohne den Prozess zu töten.\n"
            "Cipher: 'renice, Ghost. Verändere die Priorität im laufenden Betrieb.\n"
            " ps -o pid,ni,comm zeigt dir wo du stehst.'"
        ),
        why_important = (
            "nice und renice sind LPIC-1-Kernstoff für Prozess-Prioritäten.\n"
            "Der Bereich -20 bis 19 und wer welche Werte setzen darf werden geprüft."
        ),
        explanation  = (
            "Prioritäten in Linux:\n\n"
            "  Nice-Wert: -20 (höchste Prio) bis +19 (niedrigste Prio)\n"
            "  Standard:  0\n"
            "  Negativ:   mehr CPU (NUR root)\n"
            "  Positiv:   weniger CPU (jeder User kann erhöhen)\n\n"
            "nice — Prozess mit Priorität STARTEN:\n"
            "  nice befehl                # Standard-Erhöhung auf 10\n"
            "  nice -n 15 backup.sh       # Nice = +15 (niedrige Prio)\n"
            "  nice -n -5 wichtig.sh      # Nice = -5 (nur root!)\n"
            "  nice --adjustment=15 cmd   # lange Syntax\n\n"
            "renice — LAUFENDEN Prozess ändern:\n"
            "  renice -n 10 -p 1337       # PID 1337: Nice auf 10\n"
            "  renice -n -5 -p 1337       # Nice auf -5 (nur root)\n"
            "  renice -n 5 -u ghost       # alle Prozesse von ghost\n"
            "  renice -n 15 -g www-data   # alle Prozesse der Gruppe\n\n"
            "Priorität anzeigen:\n"
            "  ps aux                     # NI-Spalte\n"
            "  ps -o pid,ni,comm          # PID, Nice, Command\n"
            "  ps -o pid,ni,comm -p 1337  # nur PID 1337\n"
            "  top                        # NI-Spalte in Echtzeit\n\n"
            "Regeln:\n"
            "  - User darf eigene Prozesse NUR von 0 bis +19 setzen\n"
            "  - User darf Nice NICHT verringern (kein 'selfisch werden')\n"
            "  - Nur root darf negative Werte und fremde Prozesse ändern\n\n"
            "Merksatz:\n"
            "  Nice +19 = sehr 'nett' = gibt CPU ab\n"
            "  Nice -20 = 'nicht nett' = nimmt CPU für sich"
        ),
        syntax       = "nice -n 15 backup.sh\nrenice -n 10 -p <PID>\nps -o pid,ni,comm",
        example      = (
            "$ nice -n 19 tar -czf /backup/home.tar.gz /home/ &\n[1] 5678\n\n"
            "$ ps -o pid,ni,comm -p 5678\n  PID  NI COMMAND\n 5678  19 tar\n\n"
            "$ renice -n 5 -p 5678\n5678 (process ID) old priority 19, new priority 5\n\n"
            "$ ps -o pid,ni,comm -p 5678\n  PID  NI COMMAND\n 5678   5 tar"
        ),
        task_description  = "Zeige Nice-Werte aller laufenden Prozesse",
        expected_commands = ["ps -o pid,ni,comm", "ps aux"],
        hint_text         = "ps -o pid,ni,comm zeigt PID, Nice-Wert und Befehlsname",
        quiz_questions    = [
            QuizQuestion(
                question    = "Ein normaler User will 'renice -n -5 -p 1234' ausführen. Was passiert?",
                options     = [
                    "A) Der Befehl funktioniert — der User besitzt den Prozess",
                    "B) Fehler: Permission denied — nur root darf negative Nice-Werte setzen",
                    "C) Der Befehl wird mit nice 5 ausgeführt (Absolutwert)",
                    "D) Der Befehl funktioniert aber der Wert wird auf 0 begrenzt",
                ],
                correct     = 1,
                explanation = "Negative Nice-Werte (mehr CPU) sind root-exklusiv. Normale User können Werte nur erhöhen (0 bis +19), nicht verringern.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "nice -n 19 backup.sh — was bewirkt der Wert 19?",
                options     = [
                    "A) backup.sh bekommt 19% der CPU",
                    "B) backup.sh startet 19 Sekunden verzögert",
                    "C) backup.sh bekommt die niedrigste CPU-Priorität und stört andere kaum",
                    "D) backup.sh bekommt 19mal mehr CPU als Standard",
                ],
                correct     = 2,
                explanation = "Nice +19 = niedrigste Priorität. backup.sh bekommt CPU nur wenn sonst niemand sie braucht. Ideal für Hintergrundaufgaben.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "Nice: -20 = höchste Prio. +19 = niedrigste. Standard = 0.\n"
            "nice = Prozess mit Prio STARTEN. renice = LAUFENDEN ändern.\n"
            "Nur root darf negative Werte setzen.\n"
            "ps -o pid,ni,comm = Nice-Werte anzeigen."
        ),
        memory_tip       = "-20=gierig(root). +19=nett(jeder). nice=starten. renice=ändern. ps ni=anzeigen.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.14 — cgroups Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.14",
        chapter      = 7,
        title        = "cgroups Grundlagen — Ressourcenkontrolle für Prozessgruppen",
        mtype        = "SCAN",
        xp           = 95,
        speaker      = "DAEMON",
        story        = (
            "nice begrenzt CPU-Priorität. Aber cgroups begrenzen echte Ressourcen.\n"
            "Daemon flüstert: 'Control Groups, Ghost.\n"
            " Der Kernel selbst zwingt Prozesse in Grenzen.\n"
            " Container? Docker? Alles cgroups darunter.'"
        ),
        why_important = (
            "cgroups sind die Grundlage für Container-Technologien.\n"
            "LPIC-1 prüft cgroup-Grundkonzepte, systemd-cgls und /sys/fs/cgroup."
        ),
        explanation  = (
            "cgroups — Control Groups:\n\n"
            "Was sind cgroups?\n"
            "  - Kernel-Feature zum Gruppieren von Prozessen\n"
            "  - Erlaubt Limitierung und Monitoring von Ressourcen:\n"
            "    CPU, RAM, I/O, Netzwerk\n"
            "  - Grundlage für Docker, LXC, systemd-Dienste\n\n"
            "cgroup-Versionen:\n"
            "  cgroup v1: ältere Hierarchie, mehrere Subsysteme\n"
            "  cgroup v2: einheitliche Hierarchie (modern, Standard bei neuen Distros)\n\n"
            "cgroup-Hierarchie anzeigen:\n"
            "  systemd-cgls           # cgroup-Baum anzeigen\n"
            "  systemd-cgls -l        # ausführlich\n"
            "  systemd-cgtop          # cgroup-Ressourcen live\n\n"
            "cgroup-Dateisystem:\n"
            "  /sys/fs/cgroup/        # cgroup v2 Einhängepunkt\n"
            "  ls /sys/fs/cgroup/     # Root-cgroups\n"
            "  cat /sys/fs/cgroup/memory.max  # RAM-Limit der root-cgroup\n\n"
            "systemd und cgroups:\n"
            "  Jeder systemd-Dienst bekommt eine eigene cgroup\n"
            "  systemctl status sshd  # zeigt cgroup-Pfad\n"
            "  systemd-cgls /system.slice  # alle System-Dienste\n\n"
            "cgroup-Prozess-Zugehörigkeit:\n"
            "  cat /proc/<PID>/cgroup    # cgroup eines Prozesses\n"
            "  cat /proc/$$/cgroup       # eigene cgroup\n\n"
            "Praktische Limits (systemd):\n"
            "  # In /etc/systemd/system/dienst.service:\n"
            "  [Service]\n"
            "  CPUQuota=50%          # max 50% CPU\n"
            "  MemoryMax=512M        # max 512 MB RAM\n"
            "  IOWeight=100          # I/O-Gewichtung"
        ),
        syntax       = "systemd-cgls\nsystemd-cgtop\ncat /proc/$$/cgroup\nls /sys/fs/cgroup/",
        example      = (
            "$ systemd-cgls | head -15\n"
            "Control group /:\n"
            "-.slice\n"
            "└─system.slice\n"
            "  ├─sshd.service\n"
            "  │ └─1337 /usr/sbin/sshd -D\n"
            "  └─cron.service\n"
            "    └─567 /usr/sbin/cron -f\n\n"
            "$ cat /proc/$$/cgroup\n"
            "0::/user.slice/user-1000.slice/session-1.scope"
        ),
        task_description  = "Zeige die cgroup-Hierarchie mit systemd-cgls",
        expected_commands = ["systemd-cgls", "cat /proc/$$/cgroup"],
        hint_text         = "systemd-cgls zeigt die Control-Group-Hierarchie des Systems",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was sind cgroups in Linux?",
                options     = [
                    "A) Benutzergruppen für systemd-Dienste",
                    "B) Kernel-Feature zur Ressourcenlimitierung und -überwachung von Prozessgruppen",
                    "C) Konfigurationsgruppen für den Kernel",
                    "D) Verschlüsselte Prozess-Gruppen",
                ],
                correct     = 1,
                explanation = "cgroups (Control Groups) ist ein Kernel-Feature das Prozesse in Gruppen organisiert und Ressourcen (CPU, RAM, I/O) begrenzen und überwachen kann.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Wo findet man das cgroup v2 Dateisystem?",
                options     = [
                    "A) /proc/cgroups",
                    "B) /sys/fs/cgroup",
                    "C) /var/lib/cgroup",
                    "D) /dev/cgroup",
                ],
                correct     = 1,
                explanation = "cgroup v2 ist unter /sys/fs/cgroup eingehängt. Dort findet man die Hierarchie und kann Limits lesen und setzen.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "cgroups = Ressourcenlimitierung für Prozessgruppen (CPU, RAM, I/O).\n"
            "systemd-cgls = cgroup-Hierarchie anzeigen.\n"
            "/sys/fs/cgroup = cgroup v2 Dateisystem.\n"
            "cat /proc/<PID>/cgroup = cgroup eines Prozesses."
        ),
        memory_tip       = "cgroup=Ressourcen-Käfig. systemd-cgls=Baum. /sys/fs/cgroup=Dateisystem.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.15 — Zombie-Prozesse
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.15",
        chapter      = 7,
        title        = "Zombie-Prozesse — Die Untoten des Kernels",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "ps aux zeigt einen Prozess mit Status 'Z'.\n"
            "Ghost fragt: 'Was ist das?'\n"
            "Cipher: 'Ein Zombie, Ghost. Beendet aber nicht begraben.\n"
            " Der Elternprozess hat seinen Tod nicht anerkannt.\n"
            " Sie sammeln sich an — und lähmen das System.'"
        ),
        why_important = (
            "Zombie-Prozesse sind ein häufiges Problem und LPIC-1-Prüfungsstoff.\n"
            "Die Ursache (fehlendes wait()) und Lösung müssen bekannt sein."
        ),
        explanation  = (
            "Zombie-Prozesse:\n\n"
            "Was ist ein Zombie?\n"
            "  - Prozess hat sich beendet (exit() aufgerufen)\n"
            "  - Elternprozess hat den Exit-Code noch NICHT mit wait() gelesen\n"
            "  - Prozesseintrag bleibt in der Prozesstabelle (als 'Z')\n"
            "  - Verbraucht KEINE CPU und kaum RAM — nur einen Eintrag in der Tabelle\n"
            "  - Aber: Zu viele Zombies = keine freien PIDs mehr!\n\n"
            "Zombie erkennen:\n"
            "  ps aux | grep 'Z'               # Status-Spalte\n"
            "  ps aux | awk '$8 == \"Z\"'        # nur Zombies\n"
            "  top                             # Zombie-Zähler in Kopfzeile\n\n"
            "Zombie-Ursache:\n"
            "  - Elternprozess hat einen Bug: ruft wait() nicht auf\n"
            "  - Elternprozess ist beschäftigt oder hängt selbst\n"
            "  - Häufig in schlecht programmierten Daemons\n\n"
            "Zombie entfernen:\n"
            "  1. Elternprozess (PPID) bestimmen:\n"
            "     ps -o pid,ppid,stat,cmd | grep Z\n"
            "  2. SIGHUP an Eltern senden (fordert reload auf):\n"
            "     kill -HUP <PPID>\n"
            "  3. Elternprozess neustarten oder killen\n"
            "     (Zombie wird dann von PID 1 adoptiert und bereinigt)\n\n"
            "  ACHTUNG: Zombie selbst kann NICHT direkt getötet werden!\n"
            "  Kein kill -9 auf den Zombie — er ist bereits tot!\n\n"
            "Zombie vs Orphan:\n"
            "  Zombie:  Kind hat sich beendet, Eltern wartet nicht\n"
            "  Orphan:  Kind läuft noch, Eltern hat sich beendet\n"
            "           → Orphan wird von PID 1 adoptiert"
        ),
        syntax       = "ps aux | grep Z\nps -o pid,ppid,stat,comm | grep Z\nkill -HUP <PPID>",
        example      = (
            "$ ps aux | awk '$8 ~ /Z/ {print $1,$2,$8,$11}'\n"
            "ghost 3456 Z <defunct>\n\n"
            "$ ps -o pid,ppid,stat,comm -p 3456\n"
            "  PID  PPID STAT COMMAND\n"
            " 3456  3400 Z    bad_daemon\n\n"
            "# Elternprozess 3400 neustarten um Zombie zu bereinigen:\n"
            "$ kill -HUP 3400"
        ),
        task_description  = "Suche nach Zombie-Prozessen im System",
        expected_commands = ["ps aux", "ps -o pid,ppid,stat,comm"],
        hint_text         = "ps aux | grep Z filtert Prozesse mit Zombie-Status",
        quiz_questions    = [
            QuizQuestion(
                question    = "Warum kann man einen Zombie-Prozess nicht mit 'kill -9' beenden?",
                options     = [
                    "A) Weil SIGKILL für Zombies gesperrt ist",
                    "B) Weil der Zombie-Prozess bereits beendet ist — er ist schon tot",
                    "C) Weil man root-Rechte braucht",
                    "D) Weil Zombies den SIGKILL ignorieren",
                ],
                correct     = 1,
                explanation = "Ein Zombie ist bereits beendet. Es gibt keinen laufenden Code mehr der ein Signal empfangen könnte. Lösung: Elternprozess bereinigen.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist die korrekte Lösung für einen hartnäckigen Zombie-Prozess?",
                options     = [
                    "A) kill -9 <Zombie-PID>",
                    "B) Den Elternprozess (PPID) finden und neustarten oder killen",
                    "C) renice -20 <Zombie-PID>",
                    "D) Eintrag in /proc/<PID> manuell löschen",
                ],
                correct     = 1,
                explanation = "Der Zombie-Prozess selbst kann nicht getötet werden. Den Elternprozess (PPID) neu starten zwingt ihn wait() aufzurufen oder der Zombie wird von init/systemd bereinigt.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "Zombie = beendet aber Eltern hat exit-Code noch nicht via wait() gelesen.\n"
            "Status 'Z' in ps aux. Zombie verbraucht keine CPU, nur PID-Slot.\n"
            "Zombie töten: Elternprozess (PPID) neustarten oder killen.\n"
            "kill -9 auf Zombie selbst wirkungslos — er ist bereits tot!"
        ),
        memory_tip       = "Zombie=tot-aber-in-Tabelle. PPID=Eltern. wait()=fehlt. Lösung=Eltern neustarten.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.16 — /proc/PID/ — Prozess-Informationen im Kernel
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.16",
        chapter      = 7,
        title        = "/proc/PID/ — Das Fenster in den Kernel",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "DAEMON",
        story        = (
            "/proc ist kein Dateisystem auf einer Festplatte.\n"
            "Es ist der Kernel selbst — live, lesbar, transparent.\n"
            "Daemon: '/proc/PID/ ist dein Fenster, Ghost.\n"
            " status, cmdline, fd/, maps, environ.\n"
            " Jeder Prozess liegt nackt vor dir.'"
        ),
        why_important = (
            "/proc ist das virtuelle Dateisystem für Kernel- und Prozessinformationen.\n"
            "LPIC-1 prüft die wichtigsten Dateien in /proc/<PID>/."
        ),
        explanation  = (
            "/proc/PID/ — Prozess-Verzeichnis:\n\n"
            "Jeder laufende Prozess hat /proc/<PID>/ mit:\n\n"
            "/proc/<PID>/cmdline:\n"
            "  - Befehlszeile des Prozesses (null-terminiert)\n"
            "  cat /proc/1337/cmdline    # rohe Ausgabe\n"
            "  cat -A /proc/1337/cmdline # zeigt '^@' als Trennzeichen\n"
            "  tr '\\0' ' ' < /proc/1337/cmdline  # lesbar machen\n\n"
            "/proc/<PID>/status:\n"
            "  - Prozess-Status, UID/GID, RAM-Nutzung\n"
            "  cat /proc/1337/status\n"
            "  grep -i 'vmrss' /proc/1337/status  # RAM-Nutzung\n"
            "  grep '^Pid:' /proc/1337/status      # PID\n\n"
            "/proc/<PID>/fd/:\n"
            "  - Verzeichnis mit allen offenen Dateideskriptoren\n"
            "  ls -la /proc/1337/fd/    # zeigt offene Dateien als Symlinks\n"
            "  ls -la /proc/$$/fd/      # eigene Shell's Dateideskriptoren\n\n"
            "/proc/<PID>/maps:\n"
            "  - Speicher-Mappings (laden Bibliotheken, Stack, Heap)\n"
            "  cat /proc/1337/maps\n\n"
            "/proc/<PID>/environ:\n"
            "  - Umgebungsvariablen des Prozesses\n"
            "  tr '\\0' '\\n' < /proc/1337/environ  # lesbar machen\n\n"
            "Weitere nützliche /proc-Dateien:\n"
            "  /proc/cpuinfo    — CPU-Informationen\n"
            "  /proc/meminfo    — RAM-Details\n"
            "  /proc/loadavg    — Load Average\n"
            "  /proc/mounts     — eingehängte Dateisysteme\n"
            "  /proc/net/tcp    — TCP-Verbindungen\n"
            "  /proc/sys/       — Kernel-Parameter (sysctl)"
        ),
        syntax       = "cat /proc/<PID>/status\nls -la /proc/<PID>/fd/\ncat /proc/meminfo",
        example      = (
            "$ cat /proc/1/cmdline\n/sbin/init\n\n"
            "$ cat /proc/$$/status | head -6\n"
            "Name:   bash\nUmask:  0022\nState:  S (sleeping)\nTgid:   2048\nPid:    2048\nPPid:   1337\n\n"
            "$ ls -la /proc/$$/fd/\n"
            "lrwxrwxrwx 1 ghost ghost 64 ... 0 -> /dev/pts/0  (stdin)\n"
            "lrwxrwxrwx 1 ghost ghost 64 ... 1 -> /dev/pts/0  (stdout)\n"
            "lrwxrwxrwx 1 ghost ghost 64 ... 2 -> /dev/pts/0  (stderr)"
        ),
        task_description  = "Lies Status-Informationen deiner Shell aus /proc",
        expected_commands = ["cat /proc/$$/status", "ls -la /proc/$$/fd/"],
        hint_text         = "cat /proc/$$/status zeigt Status-Infos der aktuellen Shell",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was zeigt /proc/<PID>/fd/ ?",
                options     = [
                    "A) Die Festplatten-Partitionen des Prozesses",
                    "B) Alle offenen Dateideskriptoren des Prozesses als Symlinks",
                    "C) Die Konfigurationsdateien des Prozesses",
                    "D) Die Scheduling-Informationen",
                ],
                correct     = 1,
                explanation = "/proc/<PID>/fd/ enthält für jeden offenen Dateideskriptor einen Symlink zum echten Ziel (Datei, Socket, Pipe etc.).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welche Datei in /proc liefert CPU-Informationen?",
                options     = [
                    "A) /proc/cpu",
                    "B) /proc/cpuinfo",
                    "C) /proc/processor",
                    "D) /proc/sys/cpu",
                ],
                correct     = 1,
                explanation = "/proc/cpuinfo enthält Details zu allen CPU-Kernen: Modell, MHz, Cache, Flags etc.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "/proc/<PID>/cmdline = Befehlszeile (null-separiert).\n"
            "/proc/<PID>/status = Status, UID/GID, RAM.\n"
            "/proc/<PID>/fd/ = offene Dateideskriptoren (als Symlinks).\n"
            "/proc/cpuinfo, /proc/meminfo, /proc/loadavg = System-Infos."
        ),
        memory_tip       = "/proc/PID/=Prozess-Spiegel. cmdline=Befehl. status=Infos. fd/=Datei-Handles.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.17 — tmux Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.17",
        chapter      = 7,
        title        = "tmux Grundlagen — Terminal-Multiplexer modern",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "Ghost verliert seine SSH-Session. Stunden Arbeit — weg.\n"
            "Cipher schüttelt den Kopf: 'tmux, Ghost.\n"
            " Sessions die Verbindungsabbrüche überleben.\n"
            " Split-Panes. Mehrere Fenster. Der moderne Weg.'"
        ),
        why_important = (
            "tmux ist der moderne Terminal-Multiplexer für produktive Admin-Arbeit.\n"
            "LPIC-1 prüft tmux-Grundbefehle und Session-Management."
        ),
        explanation  = (
            "tmux — Terminal Multiplexer:\n\n"
            "Sessions erstellen und verwalten:\n"
            "  tmux                       # neue Session (unbenannt)\n"
            "  tmux new -s backup          # neue Session namens 'backup'\n"
            "  tmux new-session -s ops     # lange Syntax\n"
            "  tmux ls                    # Sessions auflisten\n"
            "  tmux list-sessions         # lange Syntax\n\n"
            "Sessions verbinden/trennen:\n"
            "  tmux attach                # letzte Session verbinden\n"
            "  tmux attach -t backup      # bestimmte Session\n"
            "  tmux a -t backup           # Kurzform\n\n"
            "Prefix: Ctrl+B (Standard-Präfix für alle Befehle)\n\n"
            "Session-Steuerung (Prefix + Taste):\n"
            "  Ctrl+B d    — detach (Session läuft weiter)\n"
            "  Ctrl+B s    — Sessions auflisten und wechseln\n"
            "  Ctrl+B $    — Session umbenennen\n\n"
            "Fenster (Windows):\n"
            "  Ctrl+B c    — neues Fenster erstellen\n"
            "  Ctrl+B n    — nächstes Fenster\n"
            "  Ctrl+B p    — vorheriges Fenster\n"
            "  Ctrl+B 0-9  — Fenster 0-9 direkt\n"
            "  Ctrl+B ,    — Fenster umbenennen\n"
            "  Ctrl+B w    — Fenster-Liste\n\n"
            "Panes (Split-Views):\n"
            "  Ctrl+B %    — vertikaler Split (|)\n"
            "  Ctrl+B \"    — horizontaler Split (-)\n"
            "  Ctrl+B Pfeiltaste — zwischen Panes wechseln\n"
            "  Ctrl+B x    — Pane schließen\n"
            "  Ctrl+B z    — Pane maximieren/minimieren (zoom)\n\n"
            "Session von außen steuern:\n"
            "  tmux kill-session -t backup   # Session beenden\n"
            "  tmux kill-server              # alle Sessions beenden"
        ),
        syntax       = "tmux new -s 'name'\ntmux ls\ntmux attach -t 'name'\nCtrl+B d  # detach",
        example      = (
            "$ tmux new -s backup\n# Innerhalb der tmux-Session:\n"
            "$ nohup tar -czf /backup/home.tar.gz /home/ &\n"
            "# Ctrl+B dann d → detach\n\n"
            "$ tmux ls\nbackup: 1 windows (created Mon Jan 15 08:00:00 2089) [220x50] (detached)\n\n"
            "$ tmux attach -t backup\n# Session wieder verbunden!"
        ),
        task_description  = "Liste tmux Sessions auf",
        expected_commands = ["tmux ls", "tmux list-sessions"],
        hint_text         = "tmux ls listet alle aktiven tmux-Sessions auf",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welche Tastenkombination trennt (detached) eine tmux-Session?",
                options     = [
                    "A) Ctrl+C",
                    "B) Ctrl+D",
                    "C) Ctrl+B d",
                    "D) Ctrl+Z",
                ],
                correct     = 2,
                explanation = "Ctrl+B = tmux-Präfix. Danach 'd' = detach. Die Session läuft im Hintergrund weiter und kann mit 'tmux attach' wieder verbunden werden.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was macht 'tmux new -s ops'?",
                options     = [
                    "A) Startet tmux im Hintergrund",
                    "B) Erstellt eine neue tmux-Session mit dem Namen 'ops'",
                    "C) Verbindet sich mit einer vorhandenen Session namens 'ops'",
                    "D) Löscht die Session 'ops'",
                ],
                correct     = 1,
                explanation = "'tmux new' oder 'tmux new-session' erstellt eine neue Session. -s gibt den Namen an.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "tmux Präfix = Ctrl+B (nicht Ctrl+A wie screen).\n"
            "Ctrl+B d = detach. tmux attach -t name = wieder verbinden.\n"
            "tmux ls = Sessions auflisten. tmux new -s name = erstellen.\n"
            "Ctrl+B % = vertikaler Split. Ctrl+B \" = horizontaler Split."
        ),
        memory_tip       = "tmux: Ctrl+B=Präfix. d=detach. tmux ls=auflisten. attach=verbinden. -s=Name.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.18 — screen Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.18",
        chapter      = 7,
        title        = "screen Grundlagen — Der klassische Terminal-Multiplexer",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "DAEMON",
        story        = (
            "screen ist älter als tmux. Aber immer noch auf vielen Systemen.\n"
            "Daemon: 'Kenn beides, Ghost.\n"
            " screen -S, Ctrl+A d zum Detach, screen -r zum Reconnect.\n"
            " Prüfungsstoff. LPIC-1. Lern es.'"
        ),
        why_important = (
            "screen ist LPIC-1-Prüfungsstoff und auf vielen Produktivsystemen vorhanden.\n"
            "Die Grundbefehle und der Präfix Ctrl+A müssen sicher sitzen."
        ),
        explanation  = (
            "screen — Terminal-Multiplexer (klassisch):\n\n"
            "Sessions erstellen:\n"
            "  screen                 # neue Session (unbenannt)\n"
            "  screen -S backup       # neue Session mit Name\n"
            "  screen -S ops          # weitere Session\n\n"
            "Sessions verwalten:\n"
            "  screen -ls             # alle Sessions auflisten\n"
            "  screen -list           # lange Syntax\n"
            "  screen -r              # letzte Session fortsetzen\n"
            "  screen -r backup       # bestimmte Session\n"
            "  screen -d -r backup    # erzwingen fortsetzen (detach+reattach)\n\n"
            "Prefix: Ctrl+A (alle screen-Befehle beginnen damit)\n\n"
            "Wichtige Tastenkombinationen:\n"
            "  Ctrl+A d    — detach (Session läuft weiter)\n"
            "  Ctrl+A c    — neues Fenster erstellen\n"
            "  Ctrl+A n    — nächstes Fenster\n"
            "  Ctrl+A p    — vorheriges Fenster\n"
            "  Ctrl+A 0-9  — Fenster 0-9 direkt\n"
            "  Ctrl+A \"    — Fensterliste\n"
            "  Ctrl+A k    — aktuelles Fenster beenden (mit Bestätigung)\n"
            "  Ctrl+A ?    — Hilfe\n"
            "  Ctrl+A [    — Scroll-Mode (Copy-Mode)\n\n"
            "Session von außen beenden:\n"
            "  screen -X -S backup quit  # Session 'backup' beenden\n"
            "  screen -wipe              # tote Sessions entfernen\n\n"
            "screen vs tmux:\n"
            "  screen: einfacher, älter, Ctrl+A-Präfix\n"
            "  tmux:   moderner, Split-Panes nativ, Ctrl+B-Präfix"
        ),
        syntax       = "screen -S 'name'\nscreen -ls\nscreen -r 'name'\nCtrl+A d  # detach",
        example      = (
            "$ screen -S longbackup\n# Innerhalb der screen-Session:\n"
            "$ rsync -avz /home/ /backup/\n"
            "# Ctrl+A dann d → detach (rsync läuft weiter)\n\n"
            "$ screen -ls\nThere are screens on:\n"
            "  3456.longbackup\t(Detached)\n"
            "1 Socket in /run/screen/S-ghost.\n\n"
            "$ screen -r longbackup\n# Session wieder verbunden!"
        ),
        task_description  = "Liste screen-Sessions auf",
        expected_commands = ["screen -ls", "screen -list"],
        hint_text         = "screen -ls zeigt alle aktiven Screen-Sessions",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen dem screen- und dem tmux-Präfix?",
                options     = [
                    "A) Kein Unterschied, beide nutzen Ctrl+A",
                    "B) screen nutzt Ctrl+A, tmux nutzt Ctrl+B",
                    "C) screen nutzt Ctrl+B, tmux nutzt Ctrl+A",
                    "D) Beide nutzen Ctrl+B",
                ],
                correct     = 1,
                explanation = "screen = Ctrl+A als Präfix. tmux = Ctrl+B als Präfix. Das ist ein häufiger Verwirrungspunkt.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Wie verbindet man sich mit einer screen-Session namens 'ops'?",
                options     = [
                    "A) screen -a ops",
                    "B) screen -r ops",
                    "C) screen --connect ops",
                    "D) screen -j ops",
                ],
                correct     = 1,
                explanation = "screen -r = reattach. Mit dem Namen: screen -r ops. Wenn die Session noch attached ist: screen -d -r ops (erzwingen).",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "screen Präfix = Ctrl+A (nicht Ctrl+B!).\n"
            "screen -S name = neue Session. screen -ls = auflisten.\n"
            "screen -r name = reattach. Ctrl+A d = detach.\n"
            "screen -d -r = erzwungenes reattach (bei already attached)."
        ),
        memory_tip       = "screen: Ctrl+A=Präfix. -S=Session. -ls=auflisten. -r=reconnect. d=detach.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.19 — Quiz: Prozesse & Signale
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.19",
        chapter      = 7,
        title        = "QUIZ: Prozesse, Signale & Prioritäten",
        mtype        = "QUIZ",
        xp           = 130,
        speaker      = "ZARA Z3R0",
        story        = (
            "Der Prozess-Prüfraum öffnet sich.\n"
            "PIDs schweben als holografische Zahlen im Raum.\n"
            "Zara Z3R0: 'Kill the right process. Prioritize the right task.'"
        ),
        why_important    = "Prüfungsvorbereitung Topic 103.5 und 103.6.",
        explanation      = "Teste Wissen über Prozesse, Signale und Prioritäten.",
        task_description = "",
        expected_commands = [],
        quiz_questions   = [
            QuizQuestion(
                question    = "Was ist ein Zombie-Prozess?",
                options     = [
                    "A) Ein Prozess der 100% CPU verbraucht",
                    "B) Ein beendeter Prozess dessen Elternprozess exit() noch nicht gelesen hat",
                    "C) Ein Prozess ohne Terminal",
                    "D) Ein Prozess der auf I/O wartet",
                ],
                correct     = "B",
                explanation = "Zombie (Z-State): Prozess hat sich beendet, aber der Elternprozess hat den Rückgabewert noch nicht via wait() abgerufen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welches Signal beendet einen Prozess SOFORT ohne Aufräumen?",
                options     = ["A) SIGTERM (15)", "B) SIGHUP (1)", "C) SIGKILL (9)", "D) SIGINT (2)"],
                correct     = "C",
                explanation = "SIGKILL (9) kann nicht blockiert oder abgefangen werden. Sofortiger Abbruch. SIGTERM (15) gibt dem Prozess die Chance aufzuräumen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "nice -n 15 befehl — was bewirkt das?",
                options     = [
                    "A) Befehl bekommt 15% mehr CPU",
                    "B) Befehl startet mit niedrigerer CPU-Priorität",
                    "C) Befehl startet mit höherer CPU-Priorität",
                    "D) Befehl läuft 15 Minuten lang",
                ],
                correct     = "B",
                explanation = "Nice-Wert +15 = niedrigere Priorität = gibt anderen Prozessen mehr CPU. -20 wäre höchste Priorität.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'nohup befehl &'?",
                options     = [
                    "A) Befehl läuft im Vordergrund, ignoriert SIGKILL",
                    "B) Befehl läuft im Hintergrund und überlebt Shell-Logout (ignoriert SIGHUP)",
                    "C) Befehl blockiert alle Signale",
                    "D) Befehl läuft mit root-Rechten",
                ],
                correct     = "B",
                explanation = "nohup = no hangup = SIGHUP ignorieren. Beim SSH-Logout schickt die Shell SIGHUP an Kindprozesse. nohup verhindert das.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "lsof | grep deleted — was findet das?",
                options     = [
                    "A) Gelöschte Dateien im Trash",
                    "B) Dateien die gelöscht wurden aber noch von Prozessen geöffnet sind",
                    "C) Leere Dateien",
                    "D) Dateien mit falschen Rechten",
                ],
                correct     = "B",
                explanation = "Wenn eine Datei gelöscht wird aber noch ein Prozess sie offen hält, belegt sie weiter Speicherplatz. lsof | grep deleted findet diese 'ghost files'.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Ctrl+Z in einer laufenden Anwendung — was passiert?",
                options     = [
                    "A) Anwendung wird beendet (wie Ctrl+C)",
                    "B) Anwendung wird im Hintergrund pausiert (SIGSTOP)",
                    "C) Anwendung wird in den Hintergrund verschoben und läuft weiter",
                    "D) Undo der letzten Aktion",
                ],
                correct     = "B",
                explanation = "Ctrl+Z sendet SIGSTOP — pausiert den Prozess und schickt ihn in den Hintergrund als gestoppten Job. 'bg' lässt ihn weiterlaufen.",
                xp_value    = 20,
            ),
        ],
        exam_tip         = (
            "SIGKILL=9 (sofort). SIGTERM=15 (höflich). SIGHUP=1 (reload).\n"
            "nice: -20=höchste Prio, 19=niedrigste. Nur root darf negativ.\n"
            "renice ändert laufende Prozesse. nice beim Start.\n"
            "Ctrl+Z=pausiert (SIGSTOP). bg=weiter im BG. fg=Vordergrund."
        ),
        memory_tip       = "",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 8),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 7.BOSS — Der Prozess-Gott
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "7.BOSS",
        chapter      = 7,
        title        = "BOSS: Der Prozess-Gott",
        mtype        = "BOSS",
        xp           = 440,
        speaker      = "SYSTEM",
        story        = (
            "PID 0. Der Ur-Prozess.\n"
            "Kein User hat ihn gestartet. Er war immer da.\n"
            "'Ich bin der Prozess-Gott von NeonGrid-9, Ghost.\n"
            " Beweise, dass du meine Kinder kontrollieren kannst.'\n"
            " Oder ich setze deine Priorität auf 19.'"
        ),
        why_important    = "Boss-Prüfung: Kapitel 7 Gesamtwissen",
        explanation      = "Boss-Kampf: Prozess-Gott — vollständige Prüfung",
        task_description = "Überlebe den Boss-Quiz!",
        expected_commands = [],
        boss_name        = "PROZESS-GOTT v7.0",
        boss_desc        = (
            "SYSTEM PROCESS MATRIX ACTIVATED\n"
            "PID 0 AWAKENS\n\n"
            "All your processes belong to me.\n"
            "Prove you can control them.\n"
            "nice values, signals, job control.\n"
            "Answer wrong and I'll SIGKILL your XP."
        ),
        quiz_questions   = [
            QuizQuestion(
                question    = "ps aux zeigt einen Prozess mit STAT='Ds'. Was bedeutet das?",
                options     = [
                    "A) Prozess läuft und ist ein Session-Leader",
                    "B) Prozess ist in ununterbrechbarem Sleep (I/O-Wait) und Session-Leader",
                    "C) Prozess ist gestoppt und ein Daemon",
                    "D) Prozess ist ein Zombie-Daemon",
                ],
                correct     = "B",
                explanation = "D = Uninterruptible Sleep (wartet auf I/O, kann nicht per SIGKILL beendet werden!). s = Session-Leader.",
                xp_value    = 45,
            ),
            QuizQuestion(
                question    = "Ein Prozess hängt im D-State (Uninterruptible Sleep). Was tun?",
                options     = [
                    "A) kill -9 <PID> — SIGKILL tötet ihn",
                    "B) kill -15 <PID> — SIGTERM höflicher",
                    "C) Warten oder Hardware-Problem beheben — D-State ignoriert Signale",
                    "D) renice -20 <PID> — mehr CPU hilft",
                ],
                correct     = "C",
                explanation = "D-State = wartet auf Hardware/I/O. Signale werden ignoriert (auch SIGKILL!). Ursache: defekte Festplatte, NFS-Timeout, etc. Einzige Lösung: Hardware-Problem beheben oder Neustart.",
                xp_value    = 45,
            ),
            QuizQuestion(
                question    = "renice -5 -p 2345 schlägt fehl mit 'Permission denied'. Warum?",
                options     = [
                    "A) PID 2345 existiert nicht",
                    "B) Nur root darf Werte unter 0 setzen",
                    "C) renice -5 ist ungültige Syntax",
                    "D) Der Prozess ist bereits bei Nice -5",
                ],
                correct     = "B",
                explanation = "Negative Nice-Werte erhöhen die Priorität. Das ist systemrelevant. Nur root darf Prozesse bevorzugen. Normale User können nur Werte 0-19 setzen.",
                xp_value    = 45,
            ),
            QuizQuestion(
                question    = "Warum zeigt 'df -h' vollen Speicher, aber 'ls' zeigt keine großen Dateien?",
                options     = [
                    "A) Dateisystem-Fehler",
                    "B) Dateien wurden gelöscht aber von Prozessen noch offen gehalten",
                    "C) Versteckte Dateien mit 'ls -la' sichtbar",
                    "D) Inodes sind voll (df -i prüfen)",
                ],
                correct     = "B",
                explanation = "Gelöschte aber noch geöffnete Dateien belegen Speicher. lsof | grep deleted findet sie. Fix: Prozess neu starten oder killen.",
                xp_value    = 45,
            ),
            QuizQuestion(
                question    = "Ghost startet 'tar -czf backup.tar.gz /home' via SSH. Verbindung bricht ab. Was wäre die Lösung gewesen?",
                options     = [
                    "A) tar -czf backup.tar.gz /home &",
                    "B) nohup tar -czf backup.tar.gz /home &",
                    "C) nice tar -czf backup.tar.gz /home",
                    "D) screen -d tar -czf backup.tar.gz /home",
                ],
                correct     = "B",
                explanation = "nohup ignoriert SIGHUP — das Signal das bei SSH-Trennung gesendet wird. & = Hintergrund. Together: nohup cmd & = läuft auch nach SSH-Logout.",
                xp_value    = 45,
            ),
            QuizQuestion(
                question    = "Load Average zeigt '4.00 3.50 2.00' auf einem 2-Core-System. Was bedeutet das?",
                options     = [
                    "A) System läuft optimal mit 4 Prozessen",
                    "B) System ist überlastet — 4 Prozesse warten auf 2 CPUs",
                    "C) System hat 4 User eingeloggt",
                    "D) CPU-Temperatur ist hoch",
                ],
                correct     = "B",
                explanation = "Load Average > CPU-Kerne = Überlastung. Bei 2 CPUs bedeutet 4.00 = doppelte Überlastung. 2.00 wäre 100% ausgelastet.",
                xp_value    = 45,
            ),
        ],
        gear_reward      = "kernel_beacon",
        faction_reward   = ("Kernel Syndicate", 30),
    ),
]
