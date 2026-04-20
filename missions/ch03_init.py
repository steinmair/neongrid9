"""
NeonGrid-9 :: Kapitel 3 — Init Wars
LPIC-1 Topic 101.3: Runlevels / Boot Targets / systemd / SysVinit
33 Missionen + Boss
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_3_MISSIONS = [

    Mission(
        mission_id="3.01",
        title="Init Origins — SysVinit Grundkonzept",
        mtype="SCAN", xp=20, chapter=3,
        speaker="DAEMON",
        story=(
            "Init ist PID 1. Der erste Prozess.\n"
            "Alle anderen Prozesse sind seine Kinder.\n"
            "Wer PID 1 kennt, versteht wie ein System lebt — und stirbt."
        ),
        why_important=(
            "Das Init-System bestimmt wie Dienste gestartet werden,\n"
            "in welcher Reihenfolge und was beim Herunterfahren passiert.\n"
            "LPIC-1 prüft SysVinit, Upstart UND systemd."
        ),
        explanation=(
            "Init-Systeme im Überblick:\n\n"
            "  SysVinit (System V Init)\n"
            "  ─────────────────────────\n"
            "  Klassisch. Seit Unix System V.\n"
            "  Runlevel-basiert (0–6)\n"
            "  Skripte in /etc/init.d/\n"
            "  Serieller Start (langsam)\n"
            "  Konfiguration: /etc/inittab\n\n"
            "  Upstart\n"
            "  ────────\n"
            "  Übergangs-Init von Ubuntu (2006–2014)\n"
            "  Event-basiert\n"
            "  Weitgehend veraltet\n\n"
            "  systemd\n"
            "  ────────\n"
            "  Modernes Init-System (seit ~2011)\n"
            "  Paralleler Start (schnell)\n"
            "  Unit-basiert statt Skript-basiert\n"
            "  Socket-Aktivierung\n"
            "  Integriertes Logging (journald)\n"
            "  Standard auf: Debian, Ubuntu, RHEL, Fedora, Arch\n\n"
            "PID 1 prüfen:\n"
            "  cat /proc/1/comm\n"
            "  ps -p 1"
        ),
        syntax="cat /proc/1/comm\nps -p 1\nls -la /sbin/init",
        example=(
            "$ cat /proc/1/comm\n"
            "systemd\n\n"
            "$ ps -p 1\n"
            "  PID TTY          TIME CMD\n"
            "    1 ?        00:00:02 systemd\n\n"
            "$ ls -la /sbin/init\n"
            "lrwxrwxrwx 1 root root 20 /sbin/init -> /lib/systemd/systemd"
        ),
        task_description="Finde heraus welches Init-System auf diesem System läuft.",
        expected_commands=["cat /proc/1/comm", "ps -p 1"],
        hint_text="cat /proc/1/comm zeigt den Namen von PID 1",
        quiz_questions=[
            QuizQuestion(
                question="Was ist PID 1?",
                options=[
                    "A) Der Kernel-Prozess",
                    "B) Der erste Userspace-Prozess — das Init-System",
                    "C) Der erste Benutzer-Login",
                    "D) Der GRUB-Prozess",
                ],
                correct="B",
                explanation="PID 1 ist der erste Userspace-Prozess, gestartet vom Kernel. Alle anderen Prozesse sind direkte oder indirekte Kinder von PID 1.",
            ),
        ],
        exam_tip="PID 1 = Init-System. 'cat /proc/1/comm' zeigt welches (systemd/init).\n/sbin/init ist oft ein Symlink auf /lib/systemd/systemd.",
        memory_tip="PID 1 = Init. Alles startet von hier. Alle anderen = Kinder.",
    ),

    Mission(
        mission_id="3.02",
        title="Runlevel 0–6 — Alle Runlevels",
        mtype="SCAN", xp=25, chapter=3,
        speaker="DAEMON",
        why_important="Runlevels sind fundamentales SysVinit-Konzept und LPIC-1 Prüfungsstoff.",
        explanation=(
            "SysVinit Runlevels:\n\n"
            "  0 : HALT — System ausschalten\n"
            "  1 : Single-User Mode — Wartungsmodus (kein Netzwerk)\n"
            "  2 : Multi-User ohne NFS (Debian: wie 3)\n"
            "  3 : Multi-User mit Netzwerk, kein GUI\n"
            "  4 : Benutzerdefiniert (selten genutzt)\n"
            "  5 : Multi-User + Netzwerk + GUI (X11)\n"
            "  6 : REBOOT — System neu starten\n\n"
            "Wichtiger Unterschied Debian vs. RedHat:\n\n"
            "  Debian/Ubuntu:\n"
            "    Runlevel 2 = voller Multi-User mit Netzwerk\n"
            "    Runlevel 3, 4, 5 = identisch mit 2!\n"
            "    (Kein Unterschied zwischen 2, 3, 4, 5 unter Debian)\n\n"
            "  RedHat/CentOS/Fedora:\n"
            "    Runlevel 3 = Multi-User, kein GUI (Server)\n"
            "    Runlevel 5 = Multi-User + GUI (Desktop)\n\n"
            "Special:\n"
            "  s / S = Single-User (wie Runlevel 1)\n"
            "  N     = Initialer Runlevel beim Boot"
        ),
        syntax="runlevel\nwho -r\ncat /etc/inittab | grep initdefault",
        example=(
            "$ runlevel\n"
            "N 5\n"
            "# N = kein vorheriger Runlevel (frischer Boot)\n"
            "# 5 = aktueller Runlevel\n\n"
            "$ who -r\n"
            "         run-level 5  2024-01-15 08:00"
        ),
        task_description="Erkunde die Runlevel-Konzepte — lies die Erklärung vollständig.",
        expected_commands=["runlevel", "who -r"],
        hint_text="runlevel zeigt den aktuellen Runlevel",
        quiz_questions=[
            QuizQuestion(
                question="Was ist Runlevel 1?",
                options=[
                    "A) System ausschalten",
                    "B) Single-User Mode — Wartung, kein Netzwerk",
                    "C) Multi-User mit GUI",
                    "D) Reboot",
                ],
                correct="B",
                explanation="Runlevel 1 = Single-User Mode. Nur root kann einloggen, kein Netzwerk, minimal. Für Wartung und Reparaturen.",
            ),
            QuizQuestion(
                question="Unter Debian: Was ist der Unterschied zwischen Runlevel 3 und Runlevel 5?",
                options=[
                    "A) Runlevel 3 = ohne GUI, Runlevel 5 = mit GUI",
                    "B) Unter Debian gibt es keinen Unterschied — beide sind Multi-User",
                    "C) Runlevel 3 = Netzwerk, Runlevel 5 = kein Netzwerk",
                    "D) Runlevel 5 bootet schneller",
                ],
                correct="B",
                explanation="Unter Debian sind Runlevel 2, 3, 4 und 5 identisch — alle sind voll-funktionaler Multi-User Mode. Der Unterschied existiert nur unter RedHat.",
                xp_value=20,
            ),
        ],
        exam_tip=(
            "LPIC-1 Falle: Runlevel-Bedeutung unterscheidet sich!\n"
            "Debian: 2/3/4/5 = gleich (alles Multi-User)\n"
            "RedHat: 3 = kein GUI, 5 = mit GUI\n"
            "0 = halt, 1 = single, 6 = reboot — ÜBERALL gleich!"
        ),
        memory_tip="0=halt, 1=single, 6=reboot — universell. 3/5 = je nach Distro verschieden.",
    ),

    Mission(
        mission_id="3.03",
        title="runlevel Befehl — aktuellen Runlevel",
        mtype="INFILTRATE", xp=25, chapter=3,
        speaker="SYSTEM",
        why_important="Der 'runlevel' Befehl ist LPIC-1 Prüfungsstoff.",
        explanation=(
            "runlevel — aktuellen und vorherigen Runlevel anzeigen\n\n"
            "Ausgabe: '<vorheriger> <aktueller>'\n\n"
            "Beispiele:\n"
            "  N 5  → frisch gebootet (N=None), Runlevel 5\n"
            "  3 5  → war in 3, jetzt in 5\n"
            "  5 1  → war in 5 (GUI), jetzt in 1 (single)\n\n"
            "Alternativen:\n"
            "  who -r      : Runlevel mit Zeitstempel\n"
            "  systemctl get-default  : systemd-Äquivalent"
        ),
        syntax="runlevel\nwho -r",
        example=(
            "$ runlevel\n"
            "N 5\n\n"
            "$ who -r\n"
            "         run-level 5  2024-01-15 08:00"
        ),
        task_description="Ermittle den aktuellen Runlevel des Systems.",
        expected_commands=["runlevel"],
        hint_text="Tippe: runlevel",
        quiz_questions=[
            QuizQuestion(
                question="'runlevel' gibt 'N 3' aus. Was bedeutet das?",
                options=[
                    "A) Netzwerk ist in Runlevel 3",
                    "B) Kein vorheriger Runlevel (N), aktuell Runlevel 3",
                    "C) Runlevel 3 ist nicht verfügbar",
                    "D) Null-Runlevel 3 aktiv",
                ],
                correct="B",
                explanation="N = no previous runlevel (System frisch gebootet oder kein Wechsel). 3 = aktueller Runlevel.",
            ),
        ],
        exam_tip="runlevel Ausgabe: '<vorheriger> <aktueller>'. N = kein vorheriger.",
        memory_tip="runlevel = zwei Zahlen: vorher aktuell. N = gerade gebootet.",
    ),

    Mission(
        mission_id="3.04",
        title="telinit — Runlevel wechseln",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="DAEMON",
        why_important="telinit ist der klassische Befehl zum Runlevel-Wechsel in SysVinit.",
        explanation=(
            "telinit — tell init\n\n"
            "Runlevel wechseln:\n"
            "  telinit 3   : Wechsel zu Runlevel 3\n"
            "  telinit 1   : Single-User Mode\n"
            "  telinit 0   : System ausschalten\n"
            "  telinit 6   : Reboot\n\n"
            "Kurzform:\n"
            "  init 3      : Identisch mit telinit 3\n\n"
            "Systemd-Äquivalente:\n"
            "  telinit 0 = systemctl poweroff\n"
            "  telinit 6 = systemctl reboot\n"
            "  telinit 1 = systemctl rescue\n"
            "  telinit 3 = systemctl isolate multi-user.target\n"
            "  telinit 5 = systemctl isolate graphical.target\n\n"
            "Auf systemd-Systemen:\n"
            "  telinit existiert als Symlink/Compat zu systemctl"
        ),
        syntax="telinit 3\ninit 3\nsystemctl isolate multi-user.target",
        example=(
            "# System in Runlevel 1 (Single-User) wechseln:\n"
            "$ sudo telinit 1\n"
            "# oder auf systemd:\n"
            "$ sudo systemctl isolate rescue.target"
        ),
        task_description="Erkunde telinit — zeige welcher Prozess es ist.",
        expected_commands=["which telinit", "telinit --help"],
        hint_text="which telinit zeigt wo telinit liegt",
        quiz_questions=[
            QuizQuestion(
                question="Mit welchem Befehl wechselst du in SysVinit zu Runlevel 3?",
                options=["A) runlevel set 3", "B) telinit 3", "C) switch-runlevel 3", "D) init-change 3"],
                correct="B",
                explanation="telinit 3 (oder init 3) wechselt sofort zu Runlevel 3. Alle Dienste des Runlevels werden gestartet/gestoppt.",
            ),
        ],
        exam_tip=(
            "telinit 0 = halt. telinit 6 = reboot. telinit 1 = single.\n"
            "Auf systemd: 'systemctl isolate <target>' ist das Äquivalent."
        ),
        memory_tip="telinit <zahl> = Runlevel wechseln. 0=halt, 6=reboot, 1=single.",
    ),

    Mission(
        mission_id="3.05",
        title="/etc/inittab — SysVinit Konfiguration",
        mtype="DECODE", xp=35, chapter=3,
        speaker="DAEMON",
        story=(
            "Die inittab — die Bibel des alten Init.\n"
            "Sie definiert was beim Start passiert,\n"
            "welche Terminals geöffnet werden, was bei Runlevel-Wechsel."
        ),
        why_important=(
            "/etc/inittab ist LPIC-1 Prüfungsstoff.\n"
            "Auch wenn moderne Systeme systemd nutzen,\n"
            "musst du inittab lesen können."
        ),
        explanation=(
            "/etc/inittab — SysVinit Hauptkonfiguration\n\n"
            "Format jeder Zeile:\n"
            "  id:runlevels:action:process\n\n"
            "  id       : 1-4 Zeichen Identifier\n"
            "  runlevels: für welche Runlevels gilt die Zeile\n"
            "  action   : was init tun soll\n"
            "  process  : auszuführender Befehl\n\n"
            "Wichtige Actions:\n"
            "  initdefault : Standard-Runlevel beim Boot\n"
            "  sysinit     : Beim Start (vor Runlevel)\n"
            "  boot        : Beim Start (nach sysinit)\n"
            "  bootwait    : Wie boot aber init wartet\n"
            "  wait        : In diesem Runlevel, init wartet\n"
            "  respawn     : Neustart wenn Prozess endet\n"
            "  ctrlaltdel  : Reaktion auf Ctrl+Alt+Del\n"
            "  powerfail   : Reaktion auf Stromausfall\n\n"
            "Beispiel:\n"
            "  id:5:initdefault:   → Standard Runlevel 5\n"
            "  1:2345:respawn:/sbin/mingetty tty1  → Login-Prompt"
        ),
        syntax="cat /etc/inittab\ngrep 'initdefault' /etc/inittab",
        example=(
            "$ cat /etc/inittab\n"
            "# Default runlevel\n"
            "id:5:initdefault:\n\n"
            "# System init\n"
            "si::sysinit:/etc/init.d/rcS\n\n"
            "# Runlevel scripts\n"
            "l0:0:wait:/etc/init.d/rc 0\n"
            "l3:3:wait:/etc/init.d/rc 3\n"
            "l5:5:wait:/etc/init.d/rc 5\n\n"
            "# Terminals\n"
            "1:2345:respawn:/sbin/agetty tty1 38400 linux\n"
            "2:23:respawn:/sbin/agetty tty2 38400 linux\n\n"
            "# Ctrl+Alt+Del\n"
            "ca::ctrlaltdel:/sbin/shutdown -t3 -r now"
        ),
        task_description="Analysiere inittab — finde den Standard-Runlevel.",
        expected_commands=["grep 'initdefault' /etc/inittab", "cat /etc/inittab"],
        hint_text="grep initdefault /etc/inittab — zeigt Standard-Runlevel",
        quiz_questions=[
            QuizQuestion(
                question="Was bedeutet diese inittab-Zeile: 'id:3:initdefault:'?",
                options=[
                    "A) Führe init mit ID 3 aus",
                    "B) Standard-Runlevel beim Boot ist 3",
                    "C) Warte 3 Sekunden beim Start",
                    "D) Init-Prozess mit PID 3",
                ],
                correct="B",
                explanation="'initdefault' action setzt den Standard-Runlevel. id:3:initdefault: → System bootet in Runlevel 3.",
            ),
            QuizQuestion(
                question="Was bedeutet 'respawn' in /etc/inittab?",
                options=[
                    "A) Einmalig ausführen",
                    "B) Den Prozess automatisch neu starten wenn er endet",
                    "C) Beim System-Start ausführen",
                    "D) Nur im angegebenen Runlevel",
                ],
                correct="B",
                explanation="respawn: Wenn der Prozess endet, startet init ihn automatisch neu. Wird für Login-Prompts (getty) verwendet.",
            ),
        ],
        exam_tip=(
            "inittab Format: id:runlevels:action:process\n"
            "initdefault = Standard-Runlevel\n"
            "respawn = Neustart bei Prozessende (für Terminals!)"
        ),
        memory_tip="inittab: id:level:action:process. initdefault = Standard. respawn = auto-restart.",
    ),

    Mission(
        mission_id="3.06",
        title="/etc/init.d/ — Service-Skripte",
        mtype="DECODE", xp=30, chapter=3,
        speaker="DAEMON",
        why_important="SysVinit-Dienst-Skripte in /etc/init.d/ sind LPIC-1 Pflichtthema.",
        explanation=(
            "/etc/init.d/ — SysVinit Dienst-Skripte\n\n"
            "Jeder Dienst hat ein Shell-Skript in /etc/init.d/.\n"
            "Das Skript akzeptiert Argumente:\n\n"
            "  start    : Dienst starten\n"
            "  stop     : Dienst stoppen\n"
            "  restart  : stopp + start\n"
            "  reload   : Konfiguration neu laden (kein Stopp)\n"
            "  status   : Status anzeigen\n\n"
            "Aufruf:\n"
            "  /etc/init.d/ssh start\n"
            "  /etc/init.d/nginx restart\n\n"
            "Runlevel-Verzeichnisse:\n"
            "  /etc/rc0.d/  : Runlevel 0 Scripts (K = Kill)\n"
            "  /etc/rc1.d/  : Runlevel 1\n"
            "  /etc/rc3.d/  : Runlevel 3 (S = Start)\n"
            "  /etc/rc5.d/  : Runlevel 5\n\n"
            "Dateinamen in rc*.d/:\n"
            "  K01apache2  → Kill (stoppen), Priorität 01\n"
            "  S50ssh      → Start, Priorität 50\n"
            "  (Symlinks auf /etc/init.d/)"
        ),
        syntax=(
            "/etc/init.d/ssh start\n"
            "/etc/init.d/ssh status\n"
            "ls /etc/rc5.d/          # Runlevel 5 Dienste\n"
            "ls -la /etc/rc5.d/S*    # Startende Dienste"
        ),
        example=(
            "$ ls /etc/rc5.d/ | head -8\n"
            "K01apache2\n"
            "S01networking\n"
            "S10rsyslog\n"
            "S50ssh\n"
            "S99rc.local\n\n"
            "$ ls -la /etc/rc5.d/S50ssh\n"
            "lrwxrwxrwx 1 root root 13 /etc/rc5.d/S50ssh -> ../init.d/ssh"
        ),
        task_description="Liste Dienste in /etc/init.d/ auf.",
        expected_commands=["ls /etc/init.d/"],
        hint_text="ls /etc/init.d/",
        quiz_questions=[
            QuizQuestion(
                question="Was bedeutet 'K01apache2' in /etc/rc0.d/?",
                options=[
                    "A) Starte apache2 mit Priorität 01",
                    "B) Stoppe (Kill) apache2 mit Priorität 01 in Runlevel 0",
                    "C) Konfiguriere apache2",
                    "D) Kernel-Modul für apache2",
                ],
                correct="B",
                explanation="K = Kill (stoppen). 01 = Priorität (niedrig = früh). apache2 = Dienstname. In /etc/rc0.d/ = beim Runlevel-Wechsel zu 0 (Halt).",
            ),
            QuizQuestion(
                question="Was sind die Einträge in /etc/rc5.d/ typischerweise?",
                options=[
                    "A) Echte Shell-Skripte",
                    "B) Symlinks auf /etc/init.d/ Skripte",
                    "C) Binärdateien",
                    "D) Konfigurationsdateien",
                ],
                correct="B",
                explanation="Die Einträge in /etc/rcX.d/ sind Symlinks auf /etc/init.d/ Skripte. Nur der Dateiname (K/S + Priorität) ändert sich.",
            ),
        ],
        exam_tip=(
            "/etc/rcX.d/ enthält SYMLINKS auf /etc/init.d/ Skripte.\n"
            "S = Start, K = Kill. Zahl = Priorität (01 vor 99).\n"
            "Reihenfolge: S01 → S10 → S50 → S99"
        ),
        memory_tip="S=Start, K=Kill, Zahl=Priorität. Symlinks in /etc/rcX.d/ → /etc/init.d/.",
    ),

    Mission(
        mission_id="3.07",
        title="service Befehl — Dienste steuern",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="SYSTEM",
        why_important="'service' ist der Standard-Befehl für SysVinit-Dienste. LPIC-1 Pflicht.",
        explanation=(
            "service — Wrapper für /etc/init.d/ Skripte\n\n"
            "Syntax:\n"
            "  service <name> <aktion>\n\n"
            "Aktionen:\n"
            "  start    : starten\n"
            "  stop     : stoppen\n"
            "  restart  : neu starten\n"
            "  reload   : Konfig neu laden\n"
            "  status   : Status anzeigen\n\n"
            "Vorteil von 'service' gegenüber /etc/init.d/:\n"
            "  Funktioniert auf SysVinit UND systemd-Systemen\n"
            "  Auf systemd: service delegiert an systemctl\n\n"
            "Alle Dienste anzeigen:\n"
            "  service --status-all\n\n"
            "Ausgabe von --status-all:\n"
            "  [ + ]  ssh        → läuft\n"
            "  [ - ]  apache2    → gestoppt\n"
            "  [ ? ]  bluetooth  → unbekannt"
        ),
        syntax=(
            "service ssh status\n"
            "service ssh start\n"
            "service ssh restart\n"
            "service --status-all"
        ),
        example=(
            "$ service ssh status\n"
            "● ssh.service - OpenBSD Secure Shell server\n"
            "     Loaded: loaded (/lib/systemd/system/ssh.service)\n"
            "     Active: active (running) since Mon 2024-01-15\n\n"
            "$ service --status-all\n"
            " [ + ]  cron\n"
            " [ + ]  ssh\n"
            " [ - ]  apache2\n"
            " [ ? ]  rsync"
        ),
        task_description="Zeige den Status aller Dienste mit service.",
        expected_commands=["service --status-all"],
        hint_text="service --status-all zeigt alle Dienste",
        quiz_questions=[
            QuizQuestion(
                question="Was bedeutet '[ - ]' in der Ausgabe von 'service --status-all'?",
                options=[
                    "A) Dienst läuft",
                    "B) Dienst ist gestoppt",
                    "C) Dienst ist deaktiviert",
                    "D) Dienst nicht gefunden",
                ],
                correct="B",
                explanation="[ + ] = läuft, [ - ] = gestoppt, [ ? ] = Status unbekannt (kein status-Argument im Skript).",
            ),
        ],
        exam_tip="service = SysVinit-Wrapper, funktioniert auch auf systemd.\nservice --status-all = alle Dienste anzeigen.",
        memory_tip="service <name> start/stop/restart/status. Wrapper für init.d UND systemd.",
    ),

    Mission(
        mission_id="3.08",
        title="update-rc.d — Dienste aktivieren (Debian)",
        mtype="INFILTRATE", xp=35, chapter=3,
        speaker="DAEMON",
        why_important="update-rc.d verwaltet Dienst-Symlinks in /etc/rcX.d/ auf Debian-Systemen.",
        explanation=(
            "update-rc.d — Update /etc/rcX.d/ Links\n\n"
            "Dienst beim Boot aktivieren:\n"
            "  update-rc.d ssh enable\n"
            "  update-rc.d ssh defaults\n\n"
            "Dienst beim Boot deaktivieren:\n"
            "  update-rc.d apache2 disable\n\n"
            "Dienst komplett entfernen:\n"
            "  update-rc.d -f apache2 remove\n\n"
            "Mit expliziten Prioritäten:\n"
            "  update-rc.d ssh start 20 2 3 4 5 . stop 80 0 1 6 .\n\n"
            "Auf modernen Debian/Ubuntu:\n"
            "  update-rc.d delegiert oft an systemctl\n\n"
            "RHEL-Äquivalent:\n"
            "  chkconfig (SysVinit)\n"
            "  systemctl enable/disable"
        ),
        syntax=(
            "update-rc.d ssh enable     # Beim Boot aktivieren\n"
            "update-rc.d ssh disable    # Beim Boot deaktivieren\n"
            "update-rc.d -f ssh remove  # Entfernen"
        ),
        example=(
            "$ sudo update-rc.d ssh enable\n"
            "Synchronizing state of ssh.service...\n"
            "Executing: /lib/systemd/systemd-sysv-install enable ssh\n\n"
            "$ sudo update-rc.d apache2 disable\n"
            "Synchronizing state of apache2.service..."
        ),
        task_description="Zeige Hilfe zu update-rc.d.",
        expected_commands=["update-rc.d --help", "update-rc.d"],
        hint_text="update-rc.d --help oder einfach update-rc.d ohne Argumente",
        quiz_questions=[
            QuizQuestion(
                question="Welcher Befehl aktiviert auf Debian einen Dienst für automatischen Start?",
                options=["A) service enable ssh", "B) update-rc.d ssh enable", "C) rc-update add ssh", "D) init-enable ssh"],
                correct="B",
                explanation="update-rc.d ssh enable aktiviert den Dienst für automatischen Start beim Boot auf Debian/Ubuntu.",
            ),
        ],
        exam_tip=(
            "Debian: update-rc.d enable/disable\n"
            "RHEL:   chkconfig on/off\n"
            "Beide: systemctl enable/disable auf systemd-Systemen"
        ),
        memory_tip="update-rc.d = Debian Dienst-Aktivierung. enable=an, disable=aus.",
    ),

    Mission(
        mission_id="3.09",
        title="chkconfig — Dienste (RHEL/CentOS)",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="SYSTEM",
        why_important="chkconfig ist das RHEL-Äquivalent zu update-rc.d. LPIC-1 prüft beide.",
        explanation=(
            "chkconfig — Check Configuration (RHEL/CentOS)\n\n"
            "Alle Dienste anzeigen:\n"
            "  chkconfig --list\n\n"
            "Dienst aktivieren (für Runlevel 3 + 5):\n"
            "  chkconfig httpd on\n\n"
            "Dienst deaktivieren:\n"
            "  chkconfig httpd off\n\n"
            "Status eines Dienstes:\n"
            "  chkconfig httpd\n\n"
            "Für spezifischen Runlevel:\n"
            "  chkconfig --level 3 httpd on\n\n"
            "Ausgabe von --list:\n"
            "  httpd  0:off 1:off 2:off 3:on 4:on 5:on 6:off"
        ),
        syntax=(
            "chkconfig --list           # Alle Dienste\n"
            "chkconfig httpd on         # Aktivieren\n"
            "chkconfig httpd off        # Deaktivieren\n"
            "chkconfig --level 3 httpd on"
        ),
        example=(
            "$ chkconfig --list\n"
            "httpd          0:off  1:off  2:on  3:on  4:on  5:on  6:off\n"
            "sshd           0:off  1:off  2:on  3:on  4:on  5:on  6:off\n"
            "iptables       0:off  1:off  2:on  3:on  4:on  5:on  6:off"
        ),
        task_description="Zeige Hilfe zu chkconfig.",
        expected_commands=["chkconfig --help", "chkconfig --list"],
        hint_text="chkconfig --list zeigt alle Dienste und Runlevels",
        quiz_questions=[
            QuizQuestion(
                question="'chkconfig httpd' zeigt: '0:off 1:off 2:off 3:on 5:on'. Was bedeutet '3:on'?",
                options=[
                    "A) httpd läuft gerade auf Runlevel 3",
                    "B) httpd wird beim Wechsel zu Runlevel 3 gestartet",
                    "C) httpd hat 3 Abhängigkeiten",
                    "D) httpd Priorität ist 3",
                ],
                correct="B",
                explanation="'3:on' bedeutet httpd wird automatisch gestartet wenn das System in Runlevel 3 wechselt.",
            ),
        ],
        exam_tip="chkconfig = RHEL. update-rc.d = Debian. Beide verwalten Dienst-Autostart.",
        memory_tip="chkconfig --list = alle Dienste + Runlevel-Status.",
    ),

    Mission(
        mission_id="3.10",
        title="systemd Basics — Was ist systemd?",
        mtype="SCAN", xp=25, chapter=3,
        speaker="LYRA-7",
        story=(
            "systemd. Die Revolution des Init-Systems.\n"
            "Schneller. Paralleler. Mächtiger.\n"
            "Und umstritten. Aber Standard.\n"
            "Ich bin das Archiv — ich kenn die Geschichte."
        ),
        why_important=(
            "systemd ist das Init-System auf praktisch allen modernen\n"
            "Linux-Distributionen. LPIC-1 V5 testet systemd intensiv."
        ),
        explanation=(
            "systemd — System und Service Manager\n\n"
            "Hauptmerkmale:\n"
            "  ✓ Parallelisierung: Dienste starten gleichzeitig\n"
            "  ✓ On-demand Aktivierung (Socket/D-Bus/Pfad)\n"
            "  ✓ Cgroup-Integration: Prozess-Hierarchien\n"
            "  ✓ Integriertes Logging: journald\n"
            "  ✓ Snapshot-Funktion: System-Zustände\n"
            "  ✓ Transaktionale Updates\n\n"
            "Verzeichnisse:\n"
            "  /lib/systemd/system/   : System-Unit-Files\n"
            "  /etc/systemd/system/   : Admin-Unit-Files (Vorrang!)\n"
            "  /run/systemd/          : Runtime\n\n"
            "PID 1 prüfen:\n"
            "  systemctl --version\n"
            "  ps -p 1\n\n"
            "systemd Bestandteile:\n"
            "  systemd   : PID 1, System-Manager\n"
            "  systemctl : Steuerungs-CLI\n"
            "  journald  : Logging-Daemon\n"
            "  networkd  : Netzwerk-Manager\n"
            "  logind    : Login-Manager\n"
            "  resolved  : DNS-Resolver\n"
            "  timesyncd : NTP-Client"
        ),
        syntax="systemctl --version\nps -p 1\nls /lib/systemd/system/ | head -20",
        example=(
            "$ systemctl --version\n"
            "systemd 252 (252.22-1~deb12u1)\n"
            "+CGROUPS +XATTR +SECCOMP +BLKID +FDISK\n\n"
            "$ ps -p 1\n"
            "    1 ?   00:00:02 systemd"
        ),
        task_description="Zeige systemd-Version und PID-1-Information.",
        expected_commands=["systemctl --version"],
        hint_text="systemctl --version",
        quiz_questions=[
            QuizQuestion(
                question="Was ist ein Hauptvorteil von systemd gegenüber SysVinit?",
                options=[
                    "A) systemd ist älter und stabiler",
                    "B) Parallele Dienst-Starts statt sequentiellem Start",
                    "C) systemd nutzt weniger RAM",
                    "D) systemd unterstützt mehr Runlevels",
                ],
                correct="B",
                explanation="systemd startet unabhängige Dienste parallel — dadurch deutlich schnellerer Boot. SysVinit startet Dienste streng sequentiell.",
            ),
        ],
        exam_tip="systemd-Konfiguration: /etc/systemd/system/ (Admin) hat Vorrang vor /lib/systemd/system/ (System).",
        memory_tip="systemd = PID 1, parallel, Unit-Files, journald. Modern und Standard.",
    ),

    Mission(
        mission_id="3.11",
        title="Units & Targets — systemd Unit-Typen",
        mtype="SCAN", xp=30, chapter=3,
        speaker="LYRA-7",
        why_important="Units sind das Herzstück von systemd. Jeder Admin muss sie kennen.",
        explanation=(
            "systemd Units — Verwaltungseinheiten\n\n"
            "Unit-Typen:\n"
            "  .service  : Dienst/Programm\n"
            "              ssh.service, nginx.service\n\n"
            "  .target   : Gruppe von Units (≈ Runlevel)\n"
            "              multi-user.target, graphical.target\n\n"
            "  .socket   : Socket-Aktivierung\n"
            "              sshd.socket — startet sshd bei Verbindung\n\n"
            "  .timer    : Zeitgesteuert (≈ cron)\n"
            "              apt-daily.timer\n\n"
            "  .mount    : Mountpunkt\n"
            "              home.mount, boot-efi.mount\n\n"
            "  .automount: Automatisches Mounten\n\n"
            "  .device   : Gerät (auto-erstellt von udev)\n\n"
            "  .path     : Dateisystem-Ereignisse\n\n"
            "  .slice    : Cgroup-Hierarchie\n\n"
            "  .scope    : Extern verwaltete Prozesse\n\n"
            "Targets (Runlevel-Äquivalente):\n"
            "  poweroff.target   → Runlevel 0\n"
            "  rescue.target     → Runlevel 1\n"
            "  multi-user.target → Runlevel 3\n"
            "  graphical.target  → Runlevel 5\n"
            "  reboot.target     → Runlevel 6"
        ),
        syntax=(
            "systemctl list-units --type=service\n"
            "systemctl list-units --type=target\n"
            "systemctl list-units --all"
        ),
        example=(
            "$ systemctl list-units --type=target\n"
            "UNIT                   LOAD   ACTIVE SUB    DESCRIPTION\n"
            "basic.target           loaded active active Basic System\n"
            "graphical.target       loaded active active Graphical Interface\n"
            "multi-user.target      loaded active active Multi-User System\n"
            "network.target         loaded active active Network\n"
            "sysinit.target         loaded active active System Initialization"
        ),
        task_description="Liste alle aktiven systemd-Targets auf.",
        expected_commands=["systemctl list-units --type=target"],
        hint_text="systemctl list-units --type=target",
        quiz_questions=[
            QuizQuestion(
                question="Welches systemd-Target entspricht dem SysVinit Runlevel 5 (Multi-User + GUI)?",
                options=[
                    "A) desktop.target",
                    "B) graphical.target",
                    "C) multi-user.target",
                    "D) gui.target",
                ],
                correct="B",
                explanation="graphical.target = SysVinit Runlevel 5 (Multi-User + grafische Oberfläche). multi-user.target = Runlevel 3 (kein GUI).",
            ),
            QuizQuestion(
                question="Was ist ein .socket Unit in systemd?",
                options=[
                    "A) Eine Netzwerkkarten-Konfiguration",
                    "B) Socket-Aktivierung: Dienst wird on-demand gestartet wenn Verbindung eingeht",
                    "C) Ein Unix-Socket für IPC",
                    "D) SSL/TLS Zertifikatsverwaltung",
                ],
                correct="B",
                explanation=".socket Units ermöglichen Socket-Aktivierung: systemd hört auf dem Socket, startet den Dienst erst wenn eine Verbindung kommt.",
            ),
        ],
        exam_tip=(
            "Runlevel ↔ Target:\n"
            "0 → poweroff.target\n"
            "1 → rescue.target\n"
            "3 → multi-user.target\n"
            "5 → graphical.target\n"
            "6 → reboot.target"
        ),
        memory_tip="Targets = systemd-Runlevels. multi-user=3, graphical=5.",
    ),

    Mission(
        mission_id="3.12",
        title="systemctl status — Dienst-Status",
        mtype="INFILTRATE", xp=25, chapter=3,
        speaker="SYSTEM",
        why_important="systemctl status ist der meistgenutzte systemd-Befehl. Täglich im Einsatz.",
        explanation=(
            "systemctl status <unit>\n\n"
            "Zeigt:\n"
            "  ● ssh.service         : Unit-Name + Status-Punkt\n"
            "     Loaded:            : Wo Unit-File liegt\n"
            "     Active:            : active/inactive/failed\n"
            "     Main PID:          : Haupt-PID\n"
            "     CGroup:            : Prozess-Hierarchie\n"
            "     Logs:              : Letzte Journaleinträge\n\n"
            "Status-Farben:\n"
            "  ● grün  = active (running)\n"
            "  ● rot   = failed\n"
            "  ○ grau  = inactive\n\n"
            "Ohne Unit-Name:\n"
            "  systemctl status       → Gesamt-Systemstatus"
        ),
        syntax="systemctl status ssh\nsystemctl status nginx.service\nsystemctl status",
        example=(
            "$ systemctl status ssh\n"
            "● ssh.service - OpenBSD Secure Shell server\n"
            "     Loaded: loaded (/lib/systemd/system/ssh.service; enabled)\n"
            "     Active: active (running) since Mon 2024-01-15 08:00:01\n"
            "   Main PID: 1234 (sshd)\n"
            "      Tasks: 1 (limit: 4660)\n"
            "     Memory: 5.2M\n"
            "        CPU: 123ms\n"
            "     CGroup: /system.slice/ssh.service\n"
            "             └─1234 sshd: /usr/sbin/sshd -D\n\n"
            "Jan 15 08:00:01 neongrid9 systemd[1]: Started ssh.service."
        ),
        task_description="Zeige den Status des SSH-Dienstes.",
        expected_commands=["systemctl status ssh"],
        hint_text="systemctl status ssh",
        quiz_questions=[
            QuizQuestion(
                question="systemctl status zeigt 'Active: failed'. Was bedeutet das?",
                options=[
                    "A) Dienst läuft aber mit Fehlern",
                    "B) Dienst ist gestoppt nach einem Fehler (Exit-Code != 0)",
                    "C) Dienst ist nicht installiert",
                    "D) Dienst fehlt die Berechtigung",
                ],
                correct="B",
                explanation="'failed' bedeutet: Dienst wurde versucht zu starten, aber mit nicht-null Exit-Code beendet. Die letzten Log-Zeilen zeigen warum.",
            ),
        ],
        exam_tip="active (running) = läuft. inactive = gestoppt. failed = abgestürzt.",
        memory_tip="systemctl status = wichtigster Diagnosebefehl. Zeigt Status + Logs.",
    ),

    Mission(
        mission_id="3.13",
        title="systemctl start/stop/restart — Dienste steuern",
        mtype="INFILTRATE", xp=25, chapter=3,
        speaker="SYSTEM",
        why_important="Grundlegende Dienst-Steuerung mit systemctl. Tägliche Admin-Praxis.",
        explanation=(
            "systemctl Dienst-Steuerung:\n\n"
            "  systemctl start <unit>   : Dienst JETZT starten\n"
            "  systemctl stop <unit>    : Dienst JETZT stoppen\n"
            "  systemctl restart <unit> : stop + start\n"
            "  systemctl reload <unit>  : Konfig neu laden (kein Stopp)\n"
            "  systemctl reload-or-restart <unit> : reload wenn möglich\n\n"
            "Unterschied restart vs reload:\n"
            "  restart: Dienst stoppt komplett, startet neu\n"
            "           → alle Verbindungen werden getrennt!\n"
            "  reload:  Dienst liest Konfig neu (SIGHUP)\n"
            "           → Verbindungen bleiben bestehen\n\n"
            "Nur enable/disable ändert ob Dienst beim Boot startet.\n"
            "start/stop ist NUR für jetzt, nicht persistent!"
        ),
        syntax=(
            "systemctl start ssh\n"
            "systemctl stop ssh\n"
            "systemctl restart ssh\n"
            "systemctl reload nginx"
        ),
        example=(
            "$ sudo systemctl start ssh\n"
            "# (kein Output = Erfolg)\n\n"
            "$ sudo systemctl restart nginx\n"
            "# nginx neu gestartet"
        ),
        task_description="Zeige den Status von SSH nach einer Steuerung.",
        expected_commands=["systemctl start ssh", "systemctl status ssh"],
        hint_text="systemctl start ssh, dann systemctl status ssh",
        quiz_questions=[
            QuizQuestion(
                question="Du änderst nginx.conf. Welcher Befehl wendet die Änderung an OHNE Verbindungen zu trennen?",
                options=[
                    "A) systemctl restart nginx",
                    "B) systemctl reload nginx",
                    "C) systemctl stop nginx && systemctl start nginx",
                    "D) systemctl apply nginx",
                ],
                correct="B",
                explanation="reload sendet SIGHUP — nginx liest Konfig neu ohne Prozess-Neustart. Bestehende Verbindungen bleiben offen.",
            ),
        ],
        exam_tip="restart = alle Verbindungen unterbrechen.\nreload = keine Unterbrechung, nur Konfig neu laden.",
        memory_tip="reload = sanft, bestehende Verbindungen bleiben. restart = hart, alles neu.",
    ),

    Mission(
        mission_id="3.14",
        title="systemctl enable/disable — Autostart",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="DAEMON",
        why_important=(
            "enable/disable steuert ob ein Dienst beim Boot automatisch startet.\n"
            "Kritischer Unterschied zu start/stop!"
        ),
        explanation=(
            "systemctl enable/disable:\n\n"
            "  enable  : Dienst beim Boot automatisch starten\n"
            "            Erstellt Symlink in /etc/systemd/system/\n\n"
            "  disable : Autostart deaktivieren\n"
            "            Entfernt Symlink\n\n"
            "  enable --now  : enable UND sofort starten\n"
            "  disable --now : disable UND sofort stoppen\n\n"
            "WICHTIG — Unterschied:\n"
            "  start  = jetzt starten (kein Effekt nach Reboot)\n"
            "  enable = Autostart beim Boot (kein sofortiger Start!)\n\n"
            "Beides zusammen:\n"
            "  systemctl enable --now ssh\n"
            "  systemctl disable --now apache2\n\n"
            "Prüfen:\n"
            "  systemctl is-enabled ssh\n"
            "  → enabled / disabled / masked"
        ),
        syntax=(
            "systemctl enable ssh         # Autostart ein\n"
            "systemctl disable ssh        # Autostart aus\n"
            "systemctl enable --now ssh   # Ein + sofort starten\n"
            "systemctl is-enabled ssh     # Status prüfen"
        ),
        example=(
            "$ sudo systemctl enable ssh\n"
            "Synchronizing state of ssh.service...\n"
            "Created symlink /etc/systemd/system/sshd.service →\n"
            "  /lib/systemd/system/ssh.service\n\n"
            "$ systemctl is-enabled ssh\n"
            "enabled"
        ),
        task_description="Prüfe ob der SSH-Dienst für Autostart aktiviert ist.",
        expected_commands=["systemctl is-enabled ssh"],
        hint_text="systemctl is-enabled ssh",
        quiz_questions=[
            QuizQuestion(
                question="Was ist der Unterschied zwischen 'systemctl start ssh' und 'systemctl enable ssh'?",
                options=[
                    "A) Beide sind identisch",
                    "B) start = jetzt starten; enable = beim Boot automatisch starten",
                    "C) enable startet AND konfiguriert den Dienst",
                    "D) start = einmalig; enable = dauernd",
                ],
                correct="B",
                explanation="start = sofort starten (nicht persistent). enable = Autostart beim Boot (kein sofortiger Start). Kombiniert: enable --now",
            ),
            QuizQuestion(
                question="'systemctl is-enabled ssh' gibt 'masked' zurück. Was bedeutet das?",
                options=[
                    "A) SSH ist aktiviert und versteckt",
                    "B) SSH ist vollständig gesperrt — weder start noch enable möglich",
                    "C) SSH hat eine Maske für Passwörter",
                    "D) SSH wartet auf eine Bedingung",
                ],
                correct="B",
                explanation="masked = Unit ist auf /dev/null gelinkt. Kann nicht gestartet oder enabled werden. Stärker als disabled. Rückgängig: systemctl unmask.",
            ),
        ],
        exam_tip=(
            "enable ≠ start! Häufige Verwechslung!\n"
            "enable = Symlink in /etc/systemd/system/ erstellen\n"
            "enable --now = enable + start (empfohlen)"
        ),
        memory_tip="enable = Boot-Autostart. start = jetzt. enable --now = beides.",
    ),

    Mission(
        mission_id="3.15",
        title="systemctl restart/reload — Unterschied",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="SYSTEM",
        explanation=(
            "restart vs reload — detailliert:\n\n"
            "  restart:\n"
            "  SIGTERM → warte → SIGKILL → neue Instanz\n"
            "  Alle Verbindungen werden unterbrochen\n"
            "  PID ändert sich\n\n"
            "  reload:\n"
            "  SIGHUP an Dienst\n"
            "  Dienst liest Konfiguration neu\n"
            "  Kein Prozess-Neustart, keine Verbindungsunterbrechung\n"
            "  Nicht alle Dienste unterstützen reload!\n\n"
            "  reload-or-restart:\n"
            "  Versucht reload, falls nicht unterstützt: restart\n"
            "  Empfohlen für Konfigurationsänderungen!\n\n"
            "Wann was nutzen:\n"
            "  restart: Dienst hängt, neue Binary installiert\n"
            "  reload:  Nur Konfigurationsänderungen (nginx, apache2)"
        ),
        syntax=(
            "systemctl restart ssh\n"
            "systemctl reload nginx\n"
            "systemctl reload-or-restart sshd"
        ),
        example=(
            "# reload-or-restart ist die sichere Wahl:\n"
            "$ sudo systemctl reload-or-restart nginx\n"
            "# Wenn nginx reload unterstützt → reload\n"
            "# Wenn nicht → restart"
        ),
        task_description="Prüfe ob nginx reload-Unterstützung hat.",
        expected_commands=["systemctl reload nginx", "systemctl reload-or-restart nginx"],
        hint_text="systemctl reload nginx oder reload-or-restart nginx",
        quiz_questions=[
            QuizQuestion(
                question="Welches Signal sendet systemctl reload an den Dienst?",
                options=["A) SIGKILL", "B) SIGTERM", "C) SIGHUP", "D) SIGUSR1"],
                correct="C",
                explanation="SIGHUP (Signal 1) ist traditionell das 'reload config' Signal. Die meisten Daemons implementieren Config-Reload als Reaktion auf SIGHUP.",
            ),
        ],
        exam_tip="reload = SIGHUP. restart = SIGTERM dann neue Instanz.",
        memory_tip="reload = SIGHUP = sanft. restart = neu starten = unterbricht alles.",
    ),

    Mission(
        mission_id="3.16",
        title="systemctl is-active/is-enabled — Prüfen",
        mtype="INFILTRATE", xp=25, chapter=3,
        speaker="SYSTEM",
        why_important="is-active und is-enabled sind ideal für Scripts und Automatisierung.",
        explanation=(
            "systemctl Prüfbefehle:\n\n"
            "  systemctl is-active ssh\n"
            "    → active / inactive / failed\n"
            "    Exit-Code: 0 = active, 1 = nicht active\n\n"
            "  systemctl is-enabled ssh\n"
            "    → enabled / disabled / masked / static\n"
            "    Exit-Code: 0 = enabled, 1 = nicht enabled\n\n"
            "  systemctl is-failed ssh\n"
            "    → failed / active / inactive\n"
            "    Exit-Code: 0 = failed, 1 = nicht failed\n\n"
            "In Scripts:\n"
            "  if systemctl is-active --quiet ssh; then\n"
            "    echo 'SSH läuft'\n"
            "  fi\n\n"
            "--quiet: unterdrückt Ausgabe (nur Exit-Code)"
        ),
        syntax=(
            "systemctl is-active ssh\n"
            "systemctl is-enabled ssh\n"
            "systemctl is-failed ssh\n"
            "systemctl is-active --quiet ssh && echo running"
        ),
        example=(
            "$ systemctl is-active ssh\n"
            "active\n\n"
            "$ systemctl is-enabled ssh\n"
            "enabled\n\n"
            "$ systemctl is-active --quiet ssh && echo 'SSH läuft'"
        ),
        task_description="Prüfe ob SSH active und enabled ist.",
        expected_commands=["systemctl is-active ssh"],
        hint_text="systemctl is-active ssh",
        quiz_questions=[
            QuizQuestion(
                question="Du willst in einem Shell-Script prüfen ob nginx läuft, ohne Ausgabe. Welcher Befehl?",
                options=[
                    "A) systemctl status nginx > /dev/null",
                    "B) systemctl is-active --quiet nginx",
                    "C) service nginx check",
                    "D) ps aux | grep nginx > /dev/null",
                ],
                correct="B",
                explanation="systemctl is-active --quiet: kein Output, nur Exit-Code. 0 = active. Ideal für if-Bedingungen in Scripts.",
            ),
        ],
        exam_tip="is-active --quiet = Script-freundlich. Nur Exit-Code, keine Ausgabe.",
        memory_tip="is-active = läuft gerade? is-enabled = startet beim Boot?",
    ),

    Mission(
        mission_id="3.17",
        title="systemctl list-units — Units anzeigen",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="LYRA-7",
        why_important="list-units gibt vollständige Übersicht aller systemd-Units.",
        explanation=(
            "systemctl list-units — alle Units anzeigen\n\n"
            "  systemctl list-units\n"
            "    → aktive Units (default)\n\n"
            "  systemctl list-units --all\n"
            "    → aktive + inaktive Units\n\n"
            "  systemctl list-units --type=service\n"
            "    → nur .service Units\n\n"
            "  systemctl list-units --type=target\n"
            "    → nur .target Units\n\n"
            "  systemctl list-units --state=failed\n"
            "    → nur fehlgeschlagene Units\n\n"
            "Spalten:\n"
            "  UNIT    : Name\n"
            "  LOAD    : loaded / not-found / masked\n"
            "  ACTIVE  : active / inactive / failed\n"
            "  SUB     : Subzustand (running/dead/exited)\n"
            "  DESCRIPTION\n\n"
            "list-unit-files:\n"
            "  systemctl list-unit-files\n"
            "    → alle Unit-Files (auch inaktive) + enabled-Status"
        ),
        syntax=(
            "systemctl list-units\n"
            "systemctl list-units --type=service\n"
            "systemctl list-units --state=failed\n"
            "systemctl list-unit-files --type=service"
        ),
        example=(
            "$ systemctl list-units --state=failed\n"
            "UNIT           LOAD   ACTIVE SUB    DESCRIPTION\n"
            "apache2.service loaded failed failed The Apache HTTP Server\n\n"
            "LOAD   = Reflects whether the unit definition was properly loaded.\n"
            "ACTIVE = The high-level unit activation state.\n"
            "SUB    = The low-level unit activation state."
        ),
        task_description="Zeige alle fehlgeschlagenen Units.",
        expected_commands=["systemctl list-units --state=failed"],
        hint_text="systemctl list-units --state=failed",
        quiz_questions=[
            QuizQuestion(
                question="Was ist der Unterschied zwischen 'list-units' und 'list-unit-files'?",
                options=[
                    "A) Identisch, nur verschiedene Namen",
                    "B) list-units = laufende Instanzen; list-unit-files = alle installierten Unit-Files + enabled-Status",
                    "C) list-unit-files zeigt nur enabled Units",
                    "D) list-units ist veraltet",
                ],
                correct="B",
                explanation="list-units: laufende/aktive Units. list-unit-files: alle installierten .service/.timer etc. Dateien mit enabled/disabled/static Status.",
            ),
        ],
        exam_tip="list-units = Laufende Instanzen. list-unit-files = installierte Dateien + Status.",
        memory_tip="list-units = was läuft. list-unit-files = was installiert + enabled ist.",
    ),

    Mission(
        mission_id="3.18",
        title="systemd Targets — Zielzustände",
        mtype="SCAN", xp=30, chapter=3,
        speaker="LYRA-7",
        why_important="Targets sind der Ersatz für Runlevels. LPIC-1 prüft die Äquivalenz.",
        explanation=(
            "systemd Targets — Gruppen von Units\n\n"
            "Standard Targets:\n"
            "  poweroff.target    = Runlevel 0 (Shutdown)\n"
            "  rescue.target      = Runlevel 1 (Single-User)\n"
            "  emergency.target   = noch minimaler als rescue\n"
            "  multi-user.target  = Runlevel 2/3/4 (kein GUI)\n"
            "  graphical.target   = Runlevel 5 (mit GUI)\n"
            "  reboot.target      = Runlevel 6 (Reboot)\n\n"
            "Target-Abhängigkeiten:\n"
            "  graphical.target → multi-user.target\n"
            "                   → basic.target\n"
            "                   → sysinit.target\n\n"
            "Default Target:\n"
            "  systemctl get-default\n"
            "  /etc/systemd/system/default.target (Symlink)"
        ),
        syntax=(
            "systemctl get-default\n"
            "systemctl list-units --type=target\n"
            "ls -la /etc/systemd/system/default.target"
        ),
        example=(
            "$ systemctl get-default\n"
            "graphical.target\n\n"
            "$ ls -la /etc/systemd/system/default.target\n"
            "lrwxrwxrwx ... default.target -> /lib/systemd/system/graphical.target"
        ),
        task_description="Zeige das Default-Target des Systems.",
        expected_commands=["systemctl get-default"],
        hint_text="systemctl get-default",
        quiz_questions=[
            QuizQuestion(
                question="Welches Target entspricht dem SysVinit Runlevel 3?",
                options=[
                    "A) server.target",
                    "B) multi-user.target",
                    "C) network.target",
                    "D) console.target",
                ],
                correct="B",
                explanation="multi-user.target = SysVinit Runlevel 3 (Multi-User, Netzwerk, kein GUI). graphical.target = Runlevel 5 (mit GUI).",
            ),
        ],
        exam_tip=(
            "Runlevel ↔ Target Mapping:\n"
            "0 → poweroff.target\n"
            "1 → rescue.target\n"
            "3 → multi-user.target\n"
            "5 → graphical.target\n"
            "6 → reboot.target\n"
            "Auf LPIC exakt auswendig lernen!"
        ),
        memory_tip="multi-user=3(kein GUI). graphical=5(mit GUI). poweroff=0. reboot=6.",
    ),

    Mission(
        mission_id="3.19",
        title="Boot Target setzen — Default ändern",
        mtype="INFILTRATE", xp=35, chapter=3,
        speaker="DAEMON",
        story=(
            "Ein Server braucht kein GUI.\n"
            "Ändere das Default-Target auf multi-user.\n"
            "Spart RAM. Spart CPU. Sicherer."
        ),
        why_important="Default-Target setzen ist eine häufige Admin-Aufgabe. LPIC-1 Pflicht.",
        explanation=(
            "Default Target setzen:\n\n"
            "  systemctl set-default multi-user.target\n"
            "    → Server ohne GUI\n\n"
            "  systemctl set-default graphical.target\n"
            "    → Desktop mit GUI\n\n"
            "Was passiert:\n"
            "  Symlink /etc/systemd/system/default.target\n"
            "  wird auf das Ziel-Target gesetzt\n\n"
            "Prüfen:\n"
            "  systemctl get-default\n\n"
            "SysVinit-Äquivalent:\n"
            "  /etc/inittab: id:3:initdefault:\n\n"
            "Temporär für diesen Boot (in GRUB):\n"
            "  Kernel-Parameter: systemd.unit=multi-user.target"
        ),
        syntax=(
            "systemctl set-default multi-user.target\n"
            "systemctl set-default graphical.target\n"
            "systemctl get-default"
        ),
        example=(
            "$ sudo systemctl set-default multi-user.target\n"
            "Created symlink /etc/systemd/system/default.target →\n"
            "  /lib/systemd/system/multi-user.target\n\n"
            "$ systemctl get-default\n"
            "multi-user.target"
        ),
        task_description="Setze das Default-Target auf multi-user.target.",
        expected_commands=["systemctl set-default multi-user.target"],
        hint_text="systemctl set-default multi-user.target",
        quiz_questions=[
            QuizQuestion(
                question="Du willst einen Server auf GUI-losen Betrieb umstellen. Welcher Befehl?",
                options=[
                    "A) systemctl disable graphical.target",
                    "B) systemctl set-default multi-user.target",
                    "C) telinit 3",
                    "D) echo 3 > /etc/systemd/default-level",
                ],
                correct="B",
                explanation="systemctl set-default multi-user.target setzt den Standard-Boot-Target dauerhaft auf Runlevel 3 (kein GUI).",
            ),
        ],
        exam_tip="set-default = dauerhafter Wechsel (über Reboot hinaus).\nisolate = sofortiger Wechsel (nicht dauerhaft).",
        memory_tip="set-default = dauerhaft. isolate = sofort aber nicht dauerhaft.",
    ),

    Mission(
        mission_id="3.20",
        title="isolate Target — Sofortiger Wechsel",
        mtype="INFILTRATE", xp=35, chapter=3,
        speaker="DAEMON",
        why_important="isolate wechselt sofort das aktive Target — wie telinit für systemd.",
        explanation=(
            "systemctl isolate <target>\n\n"
            "Wechselt SOFORT zum angegebenen Target.\n"
            "Stoppt alle Units die nicht im Ziel-Target benötigt werden.\n\n"
            "Beispiele:\n"
            "  systemctl isolate multi-user.target\n"
            "    → Wechsel zu Runlevel 3 (GUI stoppen)\n\n"
            "  systemctl isolate rescue.target\n"
            "    → Wechsel zu Single-User Mode\n\n"
            "  systemctl isolate graphical.target\n"
            "    → GUI starten\n\n"
            "Wichtig: Target muss AllowIsolate=yes haben!\n"
            "(graphical, multi-user, rescue, emergency haben es)\n\n"
            "Kurzformen:\n"
            "  systemctl rescue    = isolate rescue.target\n"
            "  systemctl emergency = isolate emergency.target\n"
            "  systemctl reboot    = isolate reboot.target\n"
            "  systemctl poweroff  = isolate poweroff.target"
        ),
        syntax=(
            "systemctl isolate multi-user.target\n"
            "systemctl isolate rescue.target\n"
            "systemctl rescue\n"
            "systemctl poweroff"
        ),
        example=(
            "# In Rescue-Mode wechseln:\n"
            "$ sudo systemctl isolate rescue.target\n"
            "# System wechselt zu Single-User Mode\n\n"
            "# Kurzform für Herunterfahren:\n"
            "$ sudo systemctl poweroff\n"
            "# Identisch mit:\n"
            "$ sudo systemctl isolate poweroff.target"
        ),
        task_description="Zeige die isolierbaren Targets.",
        expected_commands=["systemctl list-units --type=target"],
        hint_text="systemctl list-units --type=target zeigt alle Targets",
        quiz_questions=[
            QuizQuestion(
                question="Was ist der Unterschied zwischen 'systemctl set-default' und 'systemctl isolate'?",
                options=[
                    "A) Beide sind gleich",
                    "B) set-default = dauerhaft (nach Reboot); isolate = sofort für diese Session",
                    "C) isolate ist dauerhafter als set-default",
                    "D) set-default funktioniert nur mit SysVinit",
                ],
                correct="B",
                explanation="set-default: Ändert /etc/systemd/system/default.target Symlink → bleibt nach Reboot. isolate: sofortiger Wechsel für die laufende Session.",
            ),
        ],
        exam_tip="isolate = sofort. set-default = dauerhaft. Wie telinit (sofort) vs /etc/inittab (dauerhaft).",
        memory_tip="isolate = jetzt wechseln. set-default = nach Reboot wechseln.",
    ),

    Mission(
        mission_id="3.21",
        title="Unit Files — /etc/systemd/system/",
        mtype="DECODE", xp=40, chapter=3,
        speaker="LYRA-7",
        story=(
            "Unit Files sind die Seelen von systemd-Diensten.\n"
            "Wer sie lesen kann, versteht jeden Dienst.\n"
            "Wer sie schreiben kann, erschafft neue."
        ),
        why_important=(
            "Unit-File-Struktur ist essentielles Wissen für jeden\n"
            "modernen Linux-Sysadmin. LPIC-1 prüft die Sektionen."
        ),
        explanation=(
            "systemd Unit-File Struktur:\n\n"
            "  [Unit]\n"
            "  Description=  : Beschreibung\n"
            "  After=         : Startet nach dieser Unit\n"
            "  Requires=      : Harte Abhängigkeit\n"
            "  Wants=         : Weiche Abhängigkeit\n"
            "  Before=        : Startet vor dieser Unit\n\n"
            "  [Service]     (für .service)\n"
            "  Type=          : simple/forking/oneshot/notify/dbus\n"
            "  ExecStart=     : Befehl zum Starten\n"
            "  ExecStop=      : Befehl zum Stoppen\n"
            "  ExecReload=    : Befehl für Reload\n"
            "  Restart=       : on-failure/always/on-abnormal\n"
            "  User=          : Als welchen User starten\n"
            "  WorkingDirectory=\n"
            "  Environment=   : Umgebungsvariablen\n\n"
            "  [Install]\n"
            "  WantedBy=      : Wo eingehängt (für enable)\n"
            "                   multi-user.target / graphical.target\n"
            "  RequiredBy=    : Hartes Einhängen"
        ),
        syntax=(
            "systemctl cat ssh.service       # Unit anzeigen\n"
            "cat /lib/systemd/system/ssh.service"
        ),
        example=(
            "$ systemctl cat ssh.service\n"
            "# /lib/systemd/system/ssh.service\n"
            "[Unit]\n"
            "Description=OpenBSD Secure Shell server\n"
            "After=network.target auditd.service\n"
            "Wants=network.target\n\n"
            "[Service]\n"
            "Type=notify\n"
            "ExecStartPre=/usr/sbin/sshd -t\n"
            "ExecStart=/usr/sbin/sshd -D\n"
            "ExecReload=/bin/kill -HUP $MAINPID\n"
            "Restart=on-failure\n\n"
            "[Install]\n"
            "WantedBy=multi-user.target"
        ),
        task_description="Zeige den Inhalt des SSH Unit-Files.",
        expected_commands=["systemctl cat ssh.service", "systemctl cat ssh"],
        hint_text="systemctl cat ssh.service",
        quiz_questions=[
            QuizQuestion(
                question="Was bedeutet 'WantedBy=multi-user.target' im [Install]-Abschnitt?",
                options=[
                    "A) Der Dienst benötigt multi-user.target um zu starten",
                    "B) Bei 'enable': der Dienst wird in multi-user.target eingehängt → startet in Runlevel 3",
                    "C) Der Dienst startet nur wenn multi-user.target nicht aktiv ist",
                    "D) multi-user.target ist eine Abhängigkeit des Dienstes",
                ],
                correct="B",
                explanation="WantedBy definiert wo der enable-Symlink erstellt wird. WantedBy=multi-user.target → Symlink in multi-user.target.wants/ → Dienst startet automatisch wenn multi-user.target aktiv ist.",
            ),
            QuizQuestion(
                question="Was ist der Unterschied zwischen 'Requires=' und 'Wants=' in einem Unit-File?",
                options=[
                    "A) Kein Unterschied",
                    "B) Requires = harte Abhängigkeit (scheitert wenn Dep fehlt); Wants = weich (startet trotzdem)",
                    "C) Wants = harte Abhängigkeit",
                    "D) Requires ist nur für .target Units",
                ],
                correct="B",
                explanation="Requires: wenn die abhängige Unit nicht starten kann, schlägt auch diese Unit fehl. Wants: weiche Empfehlung, Unit startet auch wenn Dep fehlt.",
            ),
        ],
        exam_tip=(
            "Unit-File Sektionen:\n"
            "[Unit]    = Metadaten, Abhängigkeiten\n"
            "[Service] = Wie der Dienst läuft\n"
            "[Install] = Für enable/disable"
        ),
        memory_tip="[Unit]=Wer. [Service]=Wie. [Install]=Wann (für enable).",
    ),

    Mission(
        mission_id="3.22",
        title="Eigene Unit erstellen",
        mtype="CONSTRUCT", xp=50, chapter=3,
        speaker="DAEMON",
        story=(
            "Du willst nicht nur fremde Dienste steuern.\n"
            "Du willst eigene erschaffen.\n"
            "Das ist der Unterschied zwischen User und Admin."
        ),
        why_important="Eigene Unit-Files schreiben ist eine fundamentale Admin-Fähigkeit.",
        explanation=(
            "Eigenen Dienst erstellen:\n\n"
            "1. Unit-File schreiben:\n"
            "   /etc/systemd/system/meinservice.service\n\n"
            "2. systemd informieren:\n"
            "   systemctl daemon-reload\n\n"
            "3. Dienst aktivieren:\n"
            "   systemctl enable --now meinservice\n\n"
            "Minimales Service-File:\n\n"
            "  [Unit]\n"
            "  Description=Mein eigener Dienst\n\n"
            "  [Service]\n"
            "  ExecStart=/usr/local/bin/meinskript.sh\n"
            "  Restart=on-failure\n\n"
            "  [Install]\n"
            "  WantedBy=multi-user.target\n\n"
            "Service-Typen:\n"
            "  simple    : ExecStart ist Hauptprozess (default)\n"
            "  forking   : Klassischer Daemon (forkt, parent beendet)\n"
            "  oneshot   : Einmalig ausführen, dann fertig\n"
            "  notify    : Dienst meldet Ready per sd_notify()"
        ),
        syntax=(
            "# Erstellen:\nsudo nano /etc/systemd/system/mein.service\n\n"
            "# Nach Erstellung/Änderung:\nsudo systemctl daemon-reload\n\n"
            "# Aktivieren:\nsudo systemctl enable --now mein.service"
        ),
        example=(
            "$ cat /etc/systemd/system/hello.service\n"
            "[Unit]\n"
            "Description=Hello World Service\n\n"
            "[Service]\n"
            "Type=oneshot\n"
            "ExecStart=/bin/echo 'Hello NeonGrid-9'\n"
            "RemainAfterExit=yes\n\n"
            "[Install]\n"
            "WantedBy=multi-user.target"
        ),
        task_description="Zeige die Verzeichnisstruktur /etc/systemd/system/.",
        expected_commands=["ls /etc/systemd/system/"],
        hint_text="ls /etc/systemd/system/",
        quiz_questions=[
            QuizQuestion(
                question="Du hast eine neue Unit-File in /etc/systemd/system/ erstellt. Was musst du als nächstes tun?",
                options=[
                    "A) Direkt systemctl start ausführen",
                    "B) systemctl daemon-reload ausführen",
                    "C) Das System neustarten",
                    "D) systemctl scan-units ausführen",
                ],
                correct="B",
                explanation="Nach jeder Änderung an Unit-Files: systemctl daemon-reload. Erst dann kennt systemd die neue/geänderte Datei.",
            ),
        ],
        exam_tip=(
            "Nach Unit-File Änderung:\n"
            "1. systemctl daemon-reload\n"
            "2. systemctl enable --now <unit>\n"
            "OHNE daemon-reload: Änderungen werden ignoriert!"
        ),
        memory_tip="Neue Unit → daemon-reload → enable --now. Diese Reihenfolge immer.",
    ),

    Mission(
        mission_id="3.23",
        title="journalctl — systemd Journal",
        mtype="INFILTRATE", xp=35, chapter=3,
        speaker="LYRA-7",
        story=(
            "Das Journal ist Gedächtnis.\n"
            "Alles was systemd kennt, steht hier.\n"
            "Ich hüte dieses Archiv."
        ),
        why_important="journalctl ist das primäre Log-Tool auf systemd-Systemen. LPIC-1 Pflicht.",
        explanation=(
            "journalctl — systemd Journal Reader\n\n"
            "Grundbefehle:\n"
            "  journalctl              : Alle Logs (älteste zuerst)\n"
            "  journalctl -r           : Neueste zuerst (reverse)\n"
            "  journalctl -f           : Follow (live, wie tail -f)\n"
            "  journalctl -n 20        : Letzte 20 Zeilen\n"
            "  journalctl -e           : Zum Ende springen\n\n"
            "Filter:\n"
            "  journalctl -u ssh       : Nur SSH-Logs\n"
            "  journalctl -b           : Dieser Boot\n"
            "  journalctl -b -1        : Vorheriger Boot\n"
            "  journalctl -k           : Nur Kernel\n"
            "  journalctl -p err       : Nur Errors\n"
            "  journalctl -p warning   : Nur Warnings\n\n"
            "Zeit:\n"
            "  journalctl --since '1 hour ago'\n"
            "  journalctl --since '2024-01-15 08:00'\n"
            "  journalctl --until '2024-01-15 09:00'\n\n"
            "Format:\n"
            "  journalctl -o short-iso : ISO-Timestamps\n"
            "  journalctl -o json      : JSON-Format"
        ),
        syntax=(
            "journalctl -f                    # Live\n"
            "journalctl -u ssh -n 50          # SSH, letzte 50\n"
            "journalctl -b -1 -p err          # Letzter Boot, Errors\n"
            "journalctl --since '1 hour ago'"
        ),
        example=(
            "$ journalctl -u ssh -n 5\n"
            "Jan 15 08:00:01 neongrid9 systemd[1]: Started ssh.service.\n"
            "Jan 15 08:00:01 neongrid9 sshd[1234]: Server listening on 0.0.0.0 port 22.\n"
            "Jan 15 09:15:23 neongrid9 sshd[1235]: Accepted publickey for admin\n"
            "Jan 15 09:15:30 neongrid9 sshd[1235]: Disconnected from user admin"
        ),
        task_description="Zeige die letzten 10 Einträge des SSH-Dienstes.",
        expected_commands=["journalctl -u ssh -n 10"],
        hint_text="journalctl -u ssh -n 10",
        quiz_questions=[
            QuizQuestion(
                question="Wie zeigst du Logs des vorherigen Boots?",
                options=[
                    "A) journalctl --last-boot",
                    "B) journalctl -b -1",
                    "C) journalctl --previous",
                    "D) journalctl -p prev",
                ],
                correct="B",
                explanation="journalctl -b <N>: -b 0 oder -b = aktueller Boot, -b -1 = vorheriger, -b -2 = vorletzter. Erfordert persistentes Journal.",
            ),
        ],
        exam_tip=(
            "journalctl Filter-Kombination:\n"
            "journalctl -b -1 -p err -u sshd\n"
            "= vorheriger Boot, nur Errors, nur SSH"
        ),
        memory_tip="journalctl -u=Unit, -b=Boot, -f=Follow, -p=Priority. Kombinierbar!",
    ),

    Mission(
        mission_id="3.24",
        title="journalctl -u — Dienst-Logs",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="LYRA-7",
        why_important="Service-spezifische Logs sind die häufigste journalctl-Anwendung.",
        explanation=(
            "journalctl -u <unit> — Unit-spezifische Logs\n\n"
            "  -u ssh          : SSH-Service Logs\n"
            "  -u ssh.service  : gleich (mit .service)\n"
            "  -u 'ssh*'       : alle Units beginnend mit ssh\n\n"
            "Kombinationen:\n"
            "  journalctl -u nginx -f        : Live-Logs\n"
            "  journalctl -u nginx -n 100    : Letzte 100\n"
            "  journalctl -u nginx --since today\n"
            "  journalctl -u nginx -p err    : Nur Errors\n\n"
            "Mehrere Units gleichzeitig:\n"
            "  journalctl -u nginx -u php-fpm"
        ),
        syntax="journalctl -u nginx\njournalctl -u ssh -f\njournalctl -u systemd-networkd -n 20",
        example=(
            "$ journalctl -u nginx -n 5\n"
            "Jan 15 08:00:05 neongrid9 systemd[1]: Starting nginx...\n"
            "Jan 15 08:00:05 neongrid9 nginx[2345]: config test OK\n"
            "Jan 15 08:00:05 neongrid9 systemd[1]: Started nginx.service."
        ),
        task_description="Zeige SSH-Logs der letzten 20 Einträge.",
        expected_commands=["journalctl -u ssh -n 20"],
        hint_text="journalctl -u ssh -n 20",
        quiz_questions=[
            QuizQuestion(
                question="Du willst live Logs von nginx UND php-fpm gleichzeitig sehen. Wie?",
                options=[
                    "A) journalctl -u nginx,php-fpm -f",
                    "B) journalctl -u nginx -u php-fpm -f",
                    "C) journalctl -f nginx php-fpm",
                    "D) journalctl --multi nginx php-fpm",
                ],
                correct="B",
                explanation="Mehrere -u Flags: journalctl -u nginx -u php-fpm -f zeigt beide Dienste gleichzeitig live.",
            ),
        ],
        exam_tip="journalctl -u ssh -f = Live-SSH-Log. Mehrere Units: mehrere -u Flags.",
        memory_tip="-u = Unit. Mehrfach verwendbar. -f = live folgen.",
    ),

    Mission(
        mission_id="3.25",
        title="journalctl --since/--until — Zeitfilter",
        mtype="INFILTRATE", xp=35, chapter=3,
        speaker="LYRA-7",
        why_important="Zeitbasierte Filterung ist essentiell für Incident-Analyse.",
        explanation=(
            "journalctl Zeitfilter:\n\n"
            "  --since 'YYYY-MM-DD HH:MM:SS'\n"
            "  --until 'YYYY-MM-DD HH:MM:SS'\n\n"
            "Relative Zeiten:\n"
            "  --since '1 hour ago'\n"
            "  --since '2 days ago'\n"
            "  --since yesterday\n"
            "  --since today\n\n"
            "Kombination:\n"
            "  --since '08:00' --until '09:00'\n"
            "  (heute 08:00 bis 09:00)\n\n"
            "Mit Unit:\n"
            "  journalctl -u nginx --since '1 hour ago' -p err"
        ),
        syntax=(
            "journalctl --since '1 hour ago'\n"
            "journalctl --since '2024-01-15 08:00' --until '2024-01-15 09:00'\n"
            "journalctl -u nginx --since yesterday"
        ),
        example=(
            "$ journalctl --since '10 minutes ago'\n"
            "-- Logs begin at Mon 2024-01-15 08:00:00 --\n"
            "Jan 15 09:50:01 neongrid9 systemd[1]: Reloading nginx.service\n"
            "Jan 15 09:51:23 neongrid9 sshd[1234]: Accepted publickey"
        ),
        task_description="Zeige Logs der letzten Stunde.",
        expected_commands=["journalctl --since '1 hour ago'"],
        hint_text="journalctl --since '1 hour ago'",
        quiz_questions=[
            QuizQuestion(
                question="Wie zeigst du alle Logs von heute 08:00 bis 09:00?",
                options=[
                    "A) journalctl -t '08:00-09:00'",
                    "B) journalctl --since '08:00' --until '09:00'",
                    "C) journalctl --time 08:00 09:00",
                    "D) journalctl -from 08:00 -to 09:00",
                ],
                correct="B",
                explanation="--since und --until kombiniert. Zeitangabe ohne Datum = heute. Format: 'HH:MM' oder 'YYYY-MM-DD HH:MM:SS'.",
            ),
        ],
        exam_tip="--since / --until für Zeitfenster. 'today', 'yesterday', relative Zeiten.",
        memory_tip="--since + --until = Zeitfenster für Logs.",
    ),

    Mission(
        mission_id="3.26",
        title="systemd-analyze — Boot-Performance",
        mtype="INFILTRATE", xp=35, chapter=3,
        speaker="LYRA-7",
        why_important="systemd-analyze zeigt Boot-Performance und hilft Boot-Zeit zu optimieren.",
        explanation=(
            "systemd-analyze — Boot-Analyse\n\n"
            "  systemd-analyze\n"
            "    → Gesamte Boot-Zeit\n\n"
            "  systemd-analyze blame\n"
            "    → Dienste nach Boot-Zeit sortiert\n\n"
            "  systemd-analyze critical-chain\n"
            "    → Kritischer Pfad des Boots\n\n"
            "  systemd-analyze plot > boot.svg\n"
            "    → SVG-Grafik der Boot-Zeiten\n\n"
            "  systemd-analyze verify <unit>\n"
            "    → Unit-File auf Fehler prüfen\n\n"
            "Ausgabe von systemd-analyze:\n"
            "  Startup finished in:\n"
            "  firmware: Zeit für UEFI\n"
            "  loader:   Zeit für GRUB\n"
            "  kernel:   Zeit für Kernel-Init\n"
            "  userspace: Zeit für systemd-Dienste"
        ),
        syntax=(
            "systemd-analyze\n"
            "systemd-analyze blame\n"
            "systemd-analyze critical-chain"
        ),
        example=(
            "$ systemd-analyze\n"
            "Startup finished in 2.456s (firmware) + 1.234s (loader) +\n"
            "  0.567s (kernel) + 4.890s (userspace) = 9.147s\n\n"
            "$ systemd-analyze blame | head -5\n"
            "3.456s NetworkManager-wait-online.service\n"
            "2.123s apt-daily-upgrade.service\n"
            "1.890s accounts-daemon.service\n"
            "1.234s ModemManager.service\n"
            "0.987s snap.service"
        ),
        task_description="Messe die Boot-Zeit mit systemd-analyze.",
        expected_commands=["systemd-analyze"],
        hint_text="systemd-analyze zeigt die gesamte Boot-Zeit",
        quiz_questions=[
            QuizQuestion(
                question="Du willst wissen welcher Dienst beim Boot am längsten braucht. Welcher Befehl?",
                options=[
                    "A) systemd-analyze slowest",
                    "B) systemd-analyze blame",
                    "C) journalctl --boot-time",
                    "D) systemctl list-units --sort=time",
                ],
                correct="B",
                explanation="systemd-analyze blame zeigt alle Dienste sortiert nach ihrer Startzeit — längstes zuerst.",
            ),
        ],
        exam_tip="systemd-analyze blame = Dienste nach Boot-Zeit.\nsystemd-analyze critical-chain = Engpass im Boot-Pfad.",
        memory_tip="blame = Schuldiger für langsamen Boot. critical-chain = Boot-Engpass.",
    ),

    Mission(
        mission_id="3.27",
        title="shutdown/halt/reboot — System herunterfahren",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="DAEMON",
        why_important="Korrekte Shutdown-Befehle sind essentiell. Nie einfach den Stecker ziehen.",
        explanation=(
            "System herunterfahren/neustarten:\n\n"
            "  shutdown -h now    : Sofort ausschalten\n"
            "  shutdown -h +5     : In 5 Minuten\n"
            "  shutdown -h 20:00  : Um 20:00 Uhr\n"
            "  shutdown -r now    : Sofort neustarten\n"
            "  shutdown -c        : Geplanten Shutdown abbrechen\n\n"
            "Nachricht an Benutzer:\n"
            "  shutdown -h +10 'System wird gewartet'\n\n"
            "Kurzformen:\n"
            "  poweroff  : Sofort ausschalten\n"
            "  halt      : Prozesse stoppen (ohne Power off auf alten Systemen)\n"
            "  reboot    : Sofort neustarten\n\n"
            "systemd-Äquivalente:\n"
            "  systemctl poweroff\n"
            "  systemctl reboot\n"
            "  systemctl halt\n\n"
            "wall — Nachricht an alle eingeloggten User:\n"
            "  wall 'System wird in 5 Min heruntergefahren'"
        ),
        syntax=(
            "shutdown -h now\n"
            "shutdown -r now\n"
            "shutdown -h +10 'Wartung'\n"
            "systemctl poweroff\n"
            "wall 'Nachricht an alle'"
        ),
        example=(
            "$ sudo shutdown -h +5 'Wartung in 5 Minuten'\n"
            "Broadcast message to all users:\n"
            "The system is going down for poweroff at Mon 2024-01-15 09:30:00\n\n"
            "$ sudo shutdown -c\n"
            "Shutdown cancelled."
        ),
        task_description="Prüfe die shutdown-Hilfe.",
        expected_commands=["shutdown --help", "man shutdown"],
        hint_text="shutdown --help",
        quiz_questions=[
            QuizQuestion(
                question="Welcher Befehl plant einen Shutdown in 30 Minuten mit einer Nachricht?",
                options=[
                    "A) shutdown -h 30 'Wartung'",
                    "B) shutdown -h +30 'Wartung'",
                    "C) halt +30 'Wartung'",
                    "D) poweroff --delay 30",
                ],
                correct="B",
                explanation="+30 = in 30 Minuten. Ohne + = Uhrzeit. Also shutdown -h +30 'Nachricht'.",
            ),
        ],
        exam_tip="shutdown -h +N = in N Minuten. shutdown -h 20:00 = um 20:00. -c = abbrechen.",
        memory_tip="shutdown -h now=sofort. -h +5=in 5 Min. -c=abbrechen.",
    ),

    Mission(
        mission_id="3.28",
        title="Prüfungsfalle: Runlevel 1 vs rescue.target",
        mtype="QUIZ", xp=25, chapter=3,
        speaker="KERNEL-ORAKEL",
        story="Orakel-Test: SysVinit vs systemd — häufige Verwechslungen.",
        quiz_questions=[
            QuizQuestion(
                question="Runlevel 1 entspricht in systemd welchem Target?",
                options=["A) single.target", "B) rescue.target", "C) maintenance.target", "D) emergency.target"],
                correct="B",
                explanation="Runlevel 1 = rescue.target in systemd. emergency.target ist noch minimaler (kein Netzwerk, kein Logging, nur Root-Shell).",
                xp_value=20,
            ),
            QuizQuestion(
                question="Was ist der Unterschied zwischen rescue.target und emergency.target?",
                options=[
                    "A) Kein Unterschied",
                    "B) rescue.target mountet Root-FS rw; emergency.target = minimale Shell ohne FS-Prüfung",
                    "C) emergency.target ist für UEFI",
                    "D) rescue.target ist nur für GRUB-Probleme",
                ],
                correct="B",
                explanation="rescue.target: Root-FS gemountet, systemd läuft, mehr Services. emergency.target: minimale Shell, Root-FS read-only, für wenn rescue nicht mehr geht.",
                xp_value=20,
            ),
            QuizQuestion(
                question="Welcher Kernel-Parameter startet das System in rescue.target?",
                options=["A) single", "B) rescue", "C) systemd.unit=rescue.target", "D) Alle drei sind korrekt"],
                correct="D",
                explanation="Alle drei funktionieren: 'single', '1', 'rescue', 'systemd.unit=rescue.target' starten rescue/single-user mode.",
                xp_value=20,
            ),
        ],
        exam_tip=(
            "rescue.target = Runlevel 1 = single-user = Wartungsmodus\n"
            "emergency.target = noch minimaler\n"
            "Kernel-Parameter für Rescue: 'single' oder 'systemd.unit=rescue.target'"
        ),
        memory_tip="rescue = Runlevel 1. emergency = extremer Notfall. systemd.unit=rescue.target in GRUB.",
    ),

    Mission(
        mission_id="3.29",
        title="Prüfungsfalle: SysVinit Runlevel 2 Debian vs RHEL",
        mtype="QUIZ", xp=25, chapter=3,
        speaker="KERNEL-ORAKEL",
        quiz_questions=[
            QuizQuestion(
                question="Unter welcher Distribution hat Runlevel 2 die gleiche Bedeutung wie Runlevel 5?",
                options=["A) RHEL/CentOS", "B) Debian/Ubuntu", "C) Arch Linux", "D) Gentoo"],
                correct="B",
                explanation="Unter Debian/Ubuntu sind Runlevel 2, 3, 4, 5 IDENTISCH — alle Multi-User mit Netzwerk. Nur RHEL unterscheidet 3 (kein GUI) von 5 (mit GUI).",
                xp_value=20,
            ),
            QuizQuestion(
                question="Auf welchem Runlevel startet Debian/Ubuntu standardmäßig in den meisten Installationen?",
                options=["A) Runlevel 3", "B) Runlevel 5", "C) Runlevel 2", "D) Runlevel 4"],
                correct="C",
                explanation="Debian nutzt standardmäßig Runlevel 2 als Default-Runlevel — was aber identisch mit 3, 4 und 5 ist.",
                xp_value=20,
            ),
        ],
        exam_tip="PRÜFUNGSFALLE: Debian 2=3=4=5 (alle gleich). RHEL 3=kein GUI, 5=mit GUI. 0 und 6 überall gleich.",
        memory_tip="Debian: 2/3/4/5 identisch. RHEL: 3=server, 5=desktop.",
    ),

    Mission(
        mission_id="3.30",
        title="systemctl mask/unmask",
        mtype="INFILTRATE", xp=30, chapter=3,
        speaker="DAEMON",
        why_important="mask ist stärker als disable. Verhindert jeden Start.",
        explanation=(
            "systemctl mask/unmask:\n\n"
            "  mask    : Unit auf /dev/null linken\n"
            "            → Dienst kann NICHT gestartet werden\n"
            "            → auch nicht als Abhängigkeit\n\n"
            "  unmask  : Masking aufheben\n\n"
            "Wann mask statt disable?\n"
            "  disable: Autostart aus, manuellem Start erlaubt\n"
            "  mask:    Start komplett unmöglich\n\n"
            "Beispiel:\n"
            "  systemctl mask bluetooth.service\n"
            "  → Bluetooth kann nicht starten\n\n"
            "Sicherheitshärtung:\n"
            "  systemctl mask rpcbind.service avahi-daemon.service\n"
            "  → Dienste die du nicht brauchst sperren"
        ),
        syntax=(
            "systemctl mask bluetooth.service\n"
            "systemctl unmask bluetooth.service\n"
            "systemctl is-enabled bluetooth.service  # = masked"
        ),
        example=(
            "$ sudo systemctl mask bluetooth\n"
            "Created symlink /etc/systemd/system/bluetooth.service → /dev/null\n\n"
            "$ systemctl is-enabled bluetooth\n"
            "masked\n\n"
            "$ sudo systemctl start bluetooth\n"
            "Failed to start bluetooth.service: Unit is masked."
        ),
        task_description="Prüfe ob Bluetooth gemaskiert ist.",
        expected_commands=["systemctl is-enabled bluetooth"],
        hint_text="systemctl is-enabled bluetooth",
        quiz_questions=[
            QuizQuestion(
                question="Was ist der Unterschied zwischen 'systemctl disable' und 'systemctl mask'?",
                options=[
                    "A) Identisch",
                    "B) disable = Autostart aus; mask = auch manueller Start verhindert",
                    "C) mask ist temporär, disable permanent",
                    "D) disable entfernt den Dienst vom System",
                ],
                correct="B",
                explanation="mask > disable. mask linkt auf /dev/null — kein Start möglich. disable entfernt nur den Autostart-Symlink.",
            ),
        ],
        exam_tip="mask = stärkste Sperrung. Symlink → /dev/null. is-enabled zeigt 'masked'.",
        memory_tip="mask = absolut gesperrt. disable = nur kein Autostart.",
    ),

    Mission(
        mission_id="3.31",
        title="SysVinit vs systemd — Vergleich",
        mtype="QUIZ", xp=30, chapter=3,
        speaker="KERNEL-ORAKEL",
        story="Das Orakel prüft dein Verständnis beider Init-Systeme.",
        quiz_questions=[
            QuizQuestion(
                question="Wie aktivierst du einen Dienst für Autostart in SysVinit (Debian) vs systemd?",
                options=[
                    "A) SysV: service enable; systemd: systemctl enable",
                    "B) SysV: update-rc.d ssh enable; systemd: systemctl enable ssh",
                    "C) Beide: chkconfig ssh on",
                    "D) SysV: systemctl enable; systemd: update-rc.d enable",
                ],
                correct="B",
                explanation="Debian SysVinit: update-rc.d ssh enable. RHEL SysVinit: chkconfig sshd on. systemd: systemctl enable ssh.",
                xp_value=25,
            ),
            QuizQuestion(
                question="Du willst einen Dienst-Status prüfen. SysVinit vs systemd?",
                options=[
                    "A) SysV: /etc/init.d/ssh status; systemd: systemctl status ssh",
                    "B) Beide: service ssh status",
                    "C) SysV: systemctl status ssh; systemd: service ssh status",
                    "D) Beide: /etc/init.d/ssh status",
                ],
                correct="A",
                explanation="SysVinit direkt: /etc/init.d/ssh status (oder: service ssh status als Wrapper). systemd: systemctl status ssh.",
                xp_value=20,
            ),
        ],
        exam_tip=(
            "Befehls-Äquivalenz:\n"
            "/etc/init.d/X start  ↔  systemctl start X\n"
            "update-rc.d X enable ↔  systemctl enable X\n"
            "chkconfig X on       ↔  systemctl enable X\n"
            "runlevel             ↔  systemctl get-default\n"
            "telinit X            ↔  systemctl isolate X.target"
        ),
        memory_tip="SysVinit-Befehle → systemd-Äquivalente kennen. LPIC fragt beide!",
    ),

    Mission(
        mission_id="3.BOSS",
        title="BOSS: Init War — Das Finale",
        mtype="BOSS", xp=150, chapter=3,
        speaker="DAEMON",
        boss_name="INIT WAR — Das System kämpft zurück",
        boss_desc="systemd vs SysVinit. Drei Phasen. Zeig dass du beide beherrschst.",
        story=(
            "Das BIOS Imperium hat beide Init-Systeme korrumpiert.\n"
            "Du musst:\n"
            "PHASE 1: SysVinit-Runlevel identifizieren\n"
            "PHASE 2: systemd-Dienst reparieren\n"
            "PHASE 3: Boot-Zielzustand setzen\n\n"
            "DAEMON: 'Wer Init kontrolliert, kontrolliert das System.'"
        ),
        task_description=(
            "Zeige den aktuellen systemd-Default-Target."
            "||"
            "Zeige alle fehlgeschlagenen systemd-Units."
            "||"
            "Setze das Default-Target auf multi-user.target."
        ),
        expected_commands=[
            "systemctl get-default",
            "systemctl list-units --state=failed",
            "systemctl set-default multi-user.target",
        ],
        quiz_questions=[
            QuizQuestion(
                question="System startet in GUI obwohl es ein Server sein soll. Lösung?",
                options=[
                    "A) Grafikkarte entfernen",
                    "B) systemctl set-default multi-user.target; reboot",
                    "C) GRUB_CMDLINE_LINUX_DEFAULT='no-gui'",
                    "D) update-rc.d gdm disable",
                ],
                correct="B",
                explanation="systemctl set-default multi-user.target setzt dauerhaft das Boot-Ziel auf Runlevel-3-Äquivalent. Nach Reboot kein GUI mehr.",
                xp_value=25,
            ),
            QuizQuestion(
                question="Ein Dienst startet nicht. systemctl status zeigt 'failed'. Nächster Schritt?",
                options=[
                    "A) systemctl delete failed.service",
                    "B) journalctl -u <dienst> -n 50 um Fehlerursache zu sehen",
                    "C) update-grub",
                    "D) modprobe <dienst>",
                ],
                correct="B",
                explanation="journalctl -u <dienst> zeigt die Logs des gescheiterten Dienstes. Die letzten Zeilen enthalten fast immer die Fehlerursache.",
                xp_value=25,
            ),
            QuizQuestion(
                question="Was macht 'systemctl daemon-reload' und wann ist es nötig?",
                options=[
                    "A) Startet systemd neu",
                    "B) Liest alle Unit-Files neu — nötig nach Änderungen an .service Dateien",
                    "C) Lädt alle Dienste neu",
                    "D) Löscht den systemd-Cache",
                ],
                correct="B",
                explanation="daemon-reload liest alle Unit-Files neu (ohne systemd neu zu starten). MUSS nach jeder Änderung an .service/.timer etc. ausgeführt werden.",
                xp_value=20,
            ),
            QuizQuestion(
                question="Vollständige Äquivalenz: 'telinit 0' entspricht welchem systemctl-Befehl?",
                options=[
                    "A) systemctl halt",
                    "B) systemctl poweroff",
                    "C) systemctl isolate poweroff.target",
                    "D) Sowohl B als auch C",
                ],
                correct="D",
                explanation="telinit 0 = Runlevel 0 = System ausschalten. systemd-Äquivalente: systemctl poweroff ODER systemctl isolate poweroff.target — beide korrekt.",
                xp_value=20,
            ),
        ],
        exam_tip=(
            "Init Wars — Zusammenfassung:\n\n"
            "BOOT-REIHENFOLGE: POST→BIOS→GRUB→Kernel→Init\n\n"
            "RUNLEVEL ↔ TARGETS:\n"
            "0=poweroff, 1=rescue, 3=multi-user, 5=graphical, 6=reboot\n\n"
            "SysVinit BEFEHLE:\n"
            "telinit, service, update-rc.d, chkconfig, /etc/inittab\n\n"
            "systemd BEFEHLE:\n"
            "systemctl start/stop/enable/disable/status/isolate"
        ),
        gear_reward="root_keycard",
        faction_reward=("Root Collective", 15),
        memory_tip="Init War gewonnen! Du kennst SysVinit UND systemd.",
    ),
]
