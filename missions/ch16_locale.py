"""
NeonGrid-9 :: Kapitel 16 — LOCALE MATRIX
LPIC-1 Topic 107.3 / 106.1 / 106.2 / 106.3 / 108.4
Lokalisierung, X11, Accessibility, Drucken (CUPS)

"In NeonGrid-9 sprechen die Terminals viele Sprachen.
 Zeichensätze, Zeitzonen, Display-Server —
 wer die Locale nicht kennt, bekommt ??? statt Umlaute.
 Wer X11 nicht versteht, sieht nichts."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_16_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 16.01 — Locale & Zeichensätze
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.01",
        chapter      = 16,
        title        = "Locale & Zeichensätze — UTF-8 & iconv",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Ghost, das Terminal wirft ??? statt Umlaute aus.\n"
            " Falsche Locale. Falsches Encoding.\n"
            " In einem globalen Netz ist UTF-8 Pflicht — kein Optional.\n"
            " Zeig mir deine aktuelle Locale-Konfiguration.'"
        ),
        why_important = (
            "Locale bestimmt Sprache, Zeichensatz, Datum-/Zeitformat, Währung.\n"
            "Falsch konfigurierte Locales verursachen Encoding-Fehler,\n"
            "kaputte Log-Einträge und Anwendungsabstürze bei Sonderzeichen."
        ),
        explanation  = (
            "locale                    → Alle aktuellen Locale-Variablen anzeigen\n"
            "locale -a                 → Alle installierten Locales auflisten\n"
            "localectl                 → Systemweite Locale (systemd)\n"
            "localectl set-locale LANG=de_DE.UTF-8  → Systemlocale setzen\n"
            "\n"
            "Wichtige Locale-Variablen:\n"
            "  LANG=de_DE.UTF-8       → Haupt-Locale (Fallback für alle LC_*)\n"
            "  LC_ALL                 → Überschreibt ALLE anderen LC_-Variablen\n"
            "  LC_MESSAGES            → Sprache für Systemmeldungen\n"
            "  LC_TIME                → Datum-/Zeitformat\n"
            "  LC_NUMERIC             → Zahlenformat (Komma/Punkt)\n"
            "  LC_COLLATE             → Sortierreihenfolge\n"
            "\n"
            "Zeichensatz-Konvertierung:\n"
            "  iconv -f ISO-8859-1 -t UTF-8 datei.txt > neu.txt\n"
            "  iconv -l               → Alle unterstützten Encodings\n"
            "  file datei.txt         → Dateitype + Encoding erkennen\n"
            "  od -c datei.txt        → Oktal-Dump (Bytes sichtbar machen)\n"
            "\n"
            "/etc/locale.gen          → Locales aktivieren (Debian/Ubuntu)\n"
            "locale-gen               → Locales generieren\n"
            "update-locale            → /etc/default/locale aktualisieren"
        ),
        syntax       = "locale",
        example      = "iconv -f ISO-8859-1 -t UTF-8 alte_datei.txt > neue_datei.txt",
        task_description = "Zeige alle aktuellen Locale-Einstellungen an.",
        expected_commands = ["locale"],
        hint_text    = "locale ohne Argumente zeigt alle aktuell gesetzten LC_-Variablen",
        quiz_questions = [],
        exam_tip     = "LANG=Haupt-Locale | LC_ALL überschreibt alles | iconv -f Quelle -t Ziel",
        memory_tip   = "Locale-Hierarchie: LC_ALL > LC_* > LANG — höchste Priorität gewinnt",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.02 — Zeitzonen & localectl / timedatectl
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.02",
        chapter      = 16,
        title        = "Zeitzonen — timedatectl & /usr/share/zoneinfo",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Logs aus drei Servern. Drei verschiedene Zeitzonen.\n"
            " Timestamps stimmen nicht überein — Incident-Rekonstruktion unmöglich.\n"
            " Alle Server müssen UTC laufen. Zeig mir den aktuellen Zeitzonenstatus.'"
        ),
        why_important = (
            "Falsche Zeitzonen zerreißen Log-Korrelation, cron-Jobs und\n"
            "TLS-Zertifikats-Validierung. Server laufen idealerweise auf UTC,\n"
            "Clients nutzen lokale Zeitzonen via TZ-Variable."
        ),
        explanation  = (
            "timedatectl                           → Zeitzone, Zeit, NTP-Status\n"
            "timedatectl list-timezones            → Alle Zeitzonen auflisten\n"
            "timedatectl set-timezone Europe/Berlin → Zeitzone setzen\n"
            "\n"
            "Manuell (ohne systemd):\n"
            "  ls /usr/share/zoneinfo/             → Verfügbare Zeitzonen\n"
            "  ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime\n"
            "  echo 'Europe/Berlin' > /etc/timezone\n"
            "  dpkg-reconfigure tzdata             → Interaktiv auf Debian\n"
            "\n"
            "TZ-Variable (temporär / pro Prozess):\n"
            "  TZ='America/New_York' date          → Datum in anderer Zeitzone\n"
            "  export TZ=UTC                       → Für aktuelle Shell\n"
            "\n"
            "date Ausgabeformate:\n"
            "  date +%Y-%m-%d                      → 2024-01-15\n"
            "  date +%s                            → Unix-Timestamp\n"
            "  date -d '@1705312800'               → Timestamp → Datum\n"
            "  date -u                             → UTC-Zeit"
        ),
        syntax       = "timedatectl",
        example      = "timedatectl set-timezone Europe/Berlin",
        task_description = "Zeige den aktuellen Zeitzonenstatus des Systems.",
        expected_commands = ["timedatectl"],
        hint_text    = "timedatectl zeigt Zeitzone, Zeit und NTP-Synchronisationsstatus",
        quiz_questions = [],
        exam_tip     = "timedatectl set-timezone | ln -sf /usr/share/zoneinfo/... /etc/localtime",
        memory_tip   = "/etc/localtime = Symlink auf /usr/share/zoneinfo/REGION/STADT",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.03 — X Window System: Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.03",
        chapter      = 16,
        title        = "X Window System — Display-Server & DISPLAY",
        mtype        = "INFILTRATE",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Der Agent braucht eine grafische Verbindung —\n"
            " GUI-Anwendung über SSH forwarden.\n"
            " X11 ist das Protokoll hinter jeder Linux-GUI.\n"
            " Versteh es, und du kannst GUIs über das Netz tunneln.'"
        ),
        why_important = (
            "X11 (X Window System) ist das Netzwerkprotokoll für grafische\n"
            "Linux-Oberflächen. DISPLAY-Variable, X11-Forwarding via SSH und\n"
            "xauth sind LPIC-1-Prüfungsthemen."
        ),
        explanation  = (
            "X11-Architektur:\n"
            "  X Server  = verwaltet Hardware (Display, Tastatur, Maus)\n"
            "  X Client  = Anwendung, die Fenster zeichnet\n"
            "  Window Manager = verwaltet Fensterrahmen (nicht X selbst!)\n"
            "  Display Manager = Login-Screen (GDM, SDDM, LightDM)\n"
            "\n"
            "DISPLAY-Variable:\n"
            "  DISPLAY=:0           → Lokal, erster Display\n"
            "  DISPLAY=:0.0         → Display 0, Screen 0\n"
            "  DISPLAY=host:0       → Remote X11\n"
            "  echo $DISPLAY        → Aktuellen Display anzeigen\n"
            "\n"
            "X11 über SSH:\n"
            "  ssh -X user@host     → X11-Forwarding (trusted=nein)\n"
            "  ssh -Y user@host     → Trusted X11-Forwarding (unsicher!)\n"
            "  In /etc/ssh/sshd_config: X11Forwarding yes\n"
            "\n"
            "xauth:\n"
            "  xauth list           → Authorisierungseinträge anzeigen\n"
            "  xauth add ...        → Eintrag hinzufügen\n"
            "  ~/.Xauthority        → Cookie-Datei\n"
            "\n"
            "Nützliche X-Befehle:\n"
            "  xdpyinfo             → Display-Informationen\n"
            "  xrandr               → Auflösung/Monitore konfigurieren\n"
            "  xset q               → X-Einstellungen anzeigen\n"
            "  /etc/X11/xorg.conf   → X-Konfiguration (heute meist auto)"
        ),
        syntax       = "echo $DISPLAY",
        example      = "ssh -X ghost@10.0.0.1 firefox",
        task_description = "Zeige den aktuellen X11-Display-Wert an.",
        expected_commands = ["echo $DISPLAY"],
        hint_text    = "Die DISPLAY-Umgebungsvariable enthält den aktuellen X11-Display",
        quiz_questions = [],
        exam_tip     = "DISPLAY=:0 lokal | ssh -X forwarding | xauth = Authentifizierung | xdpyinfo = Info",
        memory_tip   = "X Client schickt Zeichenbefehle → X Server zeigt sie an (umgekehrt wie man denkt!)",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.04 — Wayland & Display Manager
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.04",
        chapter      = 16,
        title        = "Display Manager & Wayland",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'X11 ist alt, Ghost. Wayland ist die Zukunft.\n"
            " Aber für die LPIC-1-Prüfung musst du beide kennen.\n"
            " Display Manager starten die GUI-Session.\n"
            " Kenne die Namen — GDM, SDDM, LightDM.'"
        ),
        why_important = (
            "Display Manager (DM) verwalten grafische Login-Sessions.\n"
            "Wayland ist der modernere X11-Nachfolger — sichere Architektur,\n"
            "kein Netzwerktransparent, aber compositing-nativ."
        ),
        explanation  = (
            "Display Manager (Login-Screen):\n"
            "  GDM    = GNOME Display Manager (Standard bei GNOME)\n"
            "  SDDM   = Simple Desktop Display Manager (KDE Plasma)\n"
            "  LightDM = Leichtgewichtiger DM (XFCE, LXDE)\n"
            "  XDM    = X Display Manager (klassisch, minimalistisch)\n"
            "\n"
            "Verwaltung:\n"
            "  systemctl status gdm          → DM-Status\n"
            "  dpkg-reconfigure gdm3         → Standard-DM wechseln (Debian)\n"
            "  /etc/gdm3/custom.conf         → GDM-Konfiguration\n"
            "\n"
            "Wayland vs X11:\n"
            "  X11:    Netzwerktransparent | veraltet | X11-Forwarding möglich\n"
            "  Wayland: Sicherer | moderner | kein Netz-Forwarding nativ\n"
            "  XWAYLAND: X11-Kompatibilitätslayer unter Wayland\n"
            "\n"
            "Session-Typen prüfen:\n"
            "  echo $XDG_SESSION_TYPE   → 'x11' oder 'wayland'\n"
            "  loginctl show-session    → Session-Details\n"
            "\n"
            "Runlevel / Target für GUI:\n"
            "  systemctl get-default    → Aktuelles Default-Target\n"
            "  graphical.target         → Mit GUI (früher Runlevel 5)\n"
            "  multi-user.target        → Ohne GUI (früher Runlevel 3)\n"
            "  systemctl set-default graphical.target"
        ),
        syntax       = "echo $XDG_SESSION_TYPE",
        example      = "systemctl set-default graphical.target",
        task_description = "Prüfe den aktuellen Session-Typ (X11 oder Wayland).",
        expected_commands = ["echo $XDG_SESSION_TYPE"],
        hint_text    = "XDG_SESSION_TYPE enthält 'x11' oder 'wayland'",
        quiz_questions = [],
        exam_tip     = "graphical.target = GUI-Boot | multi-user.target = CLI-Boot | GDM/SDDM/LightDM = Display Manager",
        memory_tip   = "Display Manager = Login-Screen | Window Manager = Fensterrahmen | Desktop = beides zusammen",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.05 — Drucken mit CUPS
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.05",
        chapter      = 16,
        title        = "CUPS — Drucken unter Linux",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Missionsbriefing muss gedruckt werden.\n"
            " Kein PDF-Viewer, kein E-Mail — physisches Papier.\n"
            " CUPS ist das universelle Drucksystem unter Linux.\n"
            " Lern es — manchmal muss Papier sein.'"
        ),
        why_important = (
            "CUPS (Common Unix Printing System) ist der Standard-Druckserver\n"
            "unter Linux. Verwaltet Drucker, Druckjobs und Protokolle (IPP, LPD).\n"
            "LPIC-1-Prüfung: lpr, lpq, lprm, lp, lpstat, cupsenable."
        ),
        explanation  = (
            "CUPS-Verwaltung:\n"
            "  systemctl status cups        → CUPS-Status\n"
            "  http://localhost:631          → Web-Interface\n"
            "  /etc/cups/cupsd.conf         → Haupt-Konfiguration\n"
            "  /etc/cups/printers.conf      → Drucker-Konfiguration\n"
            "\n"
            "Drucken:\n"
            "  lpr datei.txt               → Auf Standarddrucker drucken\n"
            "  lpr -P druckername datei    → Auf bestimmten Drucker\n"
            "  lp datei.txt               → Alternativ (CUPS-nativ)\n"
            "  lp -d druckername datei    → Mit Drucker-Angabe\n"
            "  lp -n 3 datei.txt          → 3 Kopien\n"
            "\n"
            "Druckwarteschlange:\n"
            "  lpq                         → Warteschlange anzeigen\n"
            "  lpq -P druckername          → Bestimmter Drucker\n"
            "  lpstat -p                   → Alle Drucker + Status\n"
            "  lpstat -a                   → Welche Drucker akzeptieren Jobs?\n"
            "  lpstat -d                   → Standarddrucker\n"
            "\n"
            "Jobs verwalten:\n"
            "  lprm [job-id]               → Job aus Warteschlange entfernen\n"
            "  lprm -                      → Alle eigenen Jobs entfernen\n"
            "  cancel [job-id]             → CUPS-nativ\n"
            "\n"
            "Drucker-Verwaltung:\n"
            "  cupsenable druckername      → Drucker aktivieren\n"
            "  cupsdisable druckername     → Drucker deaktivieren\n"
            "  cupsaccept druckername      → Jobs akzeptieren\n"
            "  cupsreject druckername      → Jobs ablehnen\n"
            "  lpadmin -p NAME -E -v URI -m PPD  → Drucker hinzufügen"
        ),
        syntax       = "lpstat -p",
        example      = "lpr -P HP_LaserJet report.pdf",
        task_description = "Zeige alle konfigurierten Drucker und deren Status.",
        expected_commands = ["lpstat -p"],
        hint_text    = "lpstat -p zeigt alle Drucker mit ihrem aktuellen Status",
        quiz_questions = [],
        exam_tip     = "lpr/lp drucken | lpq/lpstat Warteschlange | lprm/cancel entfernen | cupsenable aktivieren",
        memory_tip   = "CUPS: lpr=drucken lpq=queue-anzeigen lprm=remove — alles mit 'lp' prefix",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.06 — Accessibility & Desktop-Einstellungen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.06",
        chapter      = 16,
        title        = "Accessibility & Desktop-Umgebungen",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Ein guter Operator hinterlässt keine Spuren.\n"
            " Aber er kennt auch die Desktop-Tools:\n"
            " Screenreader, Vergrößerung, Tastatur-Accessibility.\n"
            " LPIC-1 fragt danach — lern die Namen.'"
        ),
        why_important = (
            "Accessibility-Tools ermöglichen Nutzung für Menschen mit\n"
            "Einschränkungen. LPIC-1 prüft Kenntnis von AT-SPI, Orca,\n"
            "und grundlegenden Desktop-Umgebungskonzepten."
        ),
        explanation  = (
            "Accessibility-Framework:\n"
            "  AT-SPI2  = Accessibility Technology Service Provider Interface\n"
            "           → Basis-Framework für alle Linux-Accessibility-Tools\n"
            "  Orca     = Screenreader für GNOME (Text-zu-Sprache)\n"
            "  GOK      = GNOME On-screen Keyboard\n"
            "  Dasher   = Vorhersage-basierte Texteingabe\n"
            "  Brltty   = Braille-Display-Unterstützung\n"
            "\n"
            "Desktop-Umgebungen (DE):\n"
            "  GNOME    = Standard Ubuntu/Fedora, GTK3/4\n"
            "  KDE Plasma = Qt-basiert, sehr anpassbar\n"
            "  XFCE     = Leichtgewichtig, GTK2/3\n"
            "  LXDE/LXQt = Sehr ressourcenschonend\n"
            "  MATE     = GNOME 2 Fork\n"
            "  Cinnamon = GNOME 3 Fork (Linux Mint)\n"
            "\n"
            "Window Manager (ohne DE):\n"
            "  i3       = Tiling WM, keyboard-driven\n"
            "  Openbox  = Leichtgewichtiger stacking WM\n"
            "  Fluxbox  = Minimalistischer WM\n"
            "\n"
            "XDG-Verzeichnisse:\n"
            "  ~/.config    → XDG_CONFIG_HOME (App-Konfigurationen)\n"
            "  ~/.local      → XDG_DATA_HOME\n"
            "  ~/.cache      → XDG_CACHE_HOME\n"
            "  /etc/xdg/     → Systemweite XDG-Konfigs"
        ),
        syntax       = "echo $XDG_CONFIG_HOME",
        example      = "ls ~/.config/",
        task_description = "Zeige den XDG-Konfigurationspfad an.",
        expected_commands = ["echo $XDG_CONFIG_HOME"],
        hint_text    = "XDG_CONFIG_HOME ist die XDG Base Directory für Konfigurationsdateien",
        quiz_questions = [],
        exam_tip     = "AT-SPI2 = Accessibility-Framework | Orca = Screenreader | XDG_CONFIG_HOME = ~/.config",
        memory_tip   = "XDG Base Dirs: CONFIG=~/.config DATA=~/.local CACHE=~/.cache",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.07 — QUIZ: Locale, X11, CUPS
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.07",
        chapter      = 16,
        title        = "QUIZ — Locale Matrix",
        mtype        = "QUIZ",
        xp           = 120,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM: 'LOCALE-MATRIX AUDIT.\n"
            " Zeichensätze, Display-Server, Drucker — klingt langweilig.\n"
            " Bis die Prüfung diese Fragen stellt.\n"
            " Beweise dein Wissen der Desktop-Schicht.'"
        ),
        why_important = "LPIC-1 Topic 107.3 / 106.1-106.3 / 108.4 — Desktop & Lokalisierung",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "Beantworte 5 Fragen zu Locale, X11 und CUPS.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Umgebungsvariable überschreibt ALLE anderen LC_*-Variablen?",
                options  = [
                    "LANG",
                    "LC_MESSAGES",
                    "LC_ALL",
                    "LANGUAGE",
                ],
                correct  = 2,
                explanation = (
                    "LC_ALL überschreibt alle anderen LC_*-Variablen und LANG.\n"
                    "Priorität: LC_ALL > LC_* > LANG\n"
                    "LC_ALL=C erzwingt POSIX-Locale (ASCII, englische Meldungen)."
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Mit welchem Befehl konvertiert man eine Datei von ISO-8859-1 nach UTF-8?",
                options  = [
                    "convert -from ISO-8859-1 -to UTF-8 datei.txt",
                    "iconv -f ISO-8859-1 -t UTF-8 datei.txt",
                    "charset --from=latin1 --to=utf8 datei.txt",
                    "recode ISO-8859-1..UTF-8 datei.txt",
                ],
                correct  = 1,
                explanation = (
                    "iconv -f FROM -t TO konvertiert Zeichensätze.\n"
                    "-f = from (Quell-Encoding)\n"
                    "-t = to (Ziel-Encoding)\n"
                    "recode ist auch ein valides Tool, aber iconv ist der LPIC-1-Standard."
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Was beschreibt 'DISPLAY=192.168.1.5:0.0' in X11?",
                options  = [
                    "X-Server auf Rechner 192.168.1.5, Display 0, Screen 0",
                    "SSH-Verbindung zu 192.168.1.5 auf Port 0",
                    "VNC-Server auf 192.168.1.5 Display 0",
                    "X-Client verbindet zu 192.168.1.5 über TCP Port 0",
                ],
                correct  = 0,
                explanation = (
                    "DISPLAY=HOST:DISPLAY.SCREEN\n"
                    "192.168.1.5 = Hostname des X-Servers\n"
                    ":0 = erster Display (TCP Port 6000+0=6000)\n"
                    ".0 = erster Screen\n"
                    "DISPLAY=:0 = lokaler X-Server (Unix-Socket, kein TCP)"
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt alle Drucker und deren Status unter CUPS?",
                options  = [
                    "lpr -l",
                    "lpstat -p",
                    "cups --list",
                    "print -a",
                ],
                correct  = 1,
                explanation = (
                    "lpstat -p listet alle konfigurierten Drucker mit Status.\n"
                    "lpstat -a zeigt, welche Drucker Jobs akzeptieren.\n"
                    "lpstat -d zeigt den Standarddrucker.\n"
                    "lpq zeigt die Warteschlange eines Druckers."
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Welche Datei ist der Symlink für die aktive Systemzeitzone?",
                options  = [
                    "/etc/timezone",
                    "/etc/localtime",
                    "/usr/share/zoneinfo/localtime",
                    "/etc/timedatectl.conf",
                ],
                correct  = 1,
                explanation = (
                    "/etc/localtime ist ein Symlink auf die aktive Zeitzonendatei,\n"
                    "z.B. /usr/share/zoneinfo/Europe/Berlin\n"
                    "/etc/timezone enthält den Zeitzonennamen als Text (Debian/Ubuntu).\n"
                    "timedatectl set-timezone aktualisiert beide automatisch."
                ),
                xp_value = 24,
            ),
        ],
        exam_tip     = "LC_ALL > LANG | iconv -f -t | DISPLAY=HOST:DISP.SCREEN | lpstat -p | /etc/localtime",
        memory_tip   = "CUPS-Befehle: lpr(int) lp(rint) lpq(ueue) lprm(emove) lpstat — alle mit 'lp'",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.08–16.19 — Erweiterung: Locale, X11, Tastatur, Fonts, Accessibility
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.08",
        chapter      = 16,
        title        = "Tastaturbelegung — localectl & loadkeys",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'Das Keyboard ist falsch belegt. ü wird zu [ und ä zu ].\n In NeonGrid-9 ist das tödlich im Gefecht. Korrigiere die Tastaturbelegung.'",
        why_important = "Falsche Tastaturbelegung macht Administration unmöglich.\nLPIC-1 prüft localectl und loadkeys.",
        explanation  = (
            "Tastatur im Terminal (TTY):\n"
            "  loadkeys de              → Tastaturlayout setzen (temporär)\n"
            "  localectl set-keymap de  → Persistentes Tastaturlayout\n"
            "  localectl status         → Aktuelles Layout anzeigen\n"
            "\n"
            "Tastatur unter X11:\n"
            "  setxkbmap de             → Layout in X11-Session setzen\n"
            "  setxkbmap -query         → Aktuelles X11-Layout\n"
            "  /etc/default/keyboard    → Persistente Konfiguration\n"
            "    XKBLAYOUT=de\n"
            "    XKBVARIANT=nodeadkeys\n"
            "\n"
            "Sonderzeichen:\n"
            "  loadkeys -d              → Standard-Layout anzeigen\n"
            "  dumpkeys > layout.map    → Aktuelles Layout exportieren"
        ),
        syntax       = "localectl set-keymap de",
        example      = "localectl status",
        task_description = "Zeige die aktuelle Tastaturbelegung an.",
        expected_commands = ["localectl status", "localectl"],
        hint_text    = "localectl zeigt Layout — localectl set-keymap de setzt es",
        quiz_questions = [
            QuizQuestion(
                question    = "Welcher Befehl setzt die Tastaturbelegung persistent?",
                options     = ["loadkeys de", "localectl set-keymap de", "setxkbmap de", "keyboard de"],
                correct     = 1,
                explanation = "localectl set-keymap ist persistent; loadkeys ist nur für die aktuelle Session.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "In welcher Datei wird die Tastaturbelegung unter Debian/Ubuntu gespeichert?",
                options     = ["/etc/keyboard", "/etc/default/keyboard", "/etc/X11/keyboard", "/etc/keymap"],
                correct     = 1,
                explanation = "/etc/default/keyboard enthält XKBLAYOUT und XKBVARIANT.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "localectl = persistent | loadkeys = temporär (TTY) | setxkbmap = temporär (X11)",
        memory_tip   = "local-ectl → lokal = Tastatur, Locale, Zeit",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    Mission(
        mission_id   = "16.09",
        chapter      = 16,
        title        = "Zeichenkodierung — ASCII, UTF-8, ISO-8859",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'Daten kommen als Byte-Stream. Ob sie lesbar sind,\n hängt vom Encoding ab. Falsch gelesen — Datenmüll. Kenn die Standards.'",
        why_important = "Encoding-Fehler verursachen kaputte Logs, Datenbankprobleme,\nDarstellungsfehler. LPIC-1 prüft iconv und Encoding-Konzepte.",
        explanation  = (
            "Zeichensatz-Grundlagen:\n"
            "  ASCII:      7-bit, 128 Zeichen, kein Umlaut\n"
            "  ISO-8859-1: 8-bit, 256 Zeichen, westeuropäische Umlaute\n"
            "  UTF-8:      Variabel 1-4 Byte, alle Unicode-Zeichen\n"
            "              Rückwärtskompatibel mit ASCII\n"
            "\n"
            "Encoding erkennen:\n"
            "  file datei.txt           → Encoding und Dateityp\n"
            "  od -c datei.txt          → Rohe Bytes anzeigen\n"
            "  hexdump -C datei.txt     → Hex-Dump\n"
            "\n"
            "iconv — Konvertierung:\n"
            "  iconv -f ISO-8859-1 -t UTF-8 alt.txt > neu.txt\n"
            "  iconv -l                 → Alle unterstützten Encodings\n"
            "  iconv -f UTF-8 -t ASCII//TRANSLIT datei.txt  → Umlaute ersetzen"
        ),
        syntax       = "iconv -f ISO-8859-1 -t UTF-8 datei.txt",
        example      = "file /etc/passwd && iconv -l | grep -i utf",
        task_description = "Liste alle unterstützten Encodings von iconv auf.",
        expected_commands = ["iconv -l"],
        hint_text    = "iconv -l listet alle Encodings — iconv -f FROM -t TO konvertiert",
        quiz_questions = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen ASCII und UTF-8?",
                options     = ["ASCII = 8-bit, UTF-8 = 7-bit", "UTF-8 ist rückwärtskompatibel mit ASCII", "ASCII unterstützt Umlaute", "UTF-8 ist nur für asiatische Zeichen"],
                correct     = 1,
                explanation = "UTF-8 ist rückwärtskompatibel mit ASCII — die ersten 128 Zeichen sind identisch.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl konvertiert eine Datei von ISO-8859-1 nach UTF-8?",
                options     = ["convert -f iso -t utf datei", "iconv -f ISO-8859-1 -t UTF-8 datei.txt", "locale-convert datei.txt", "charconv datei.txt"],
                correct     = 1,
                explanation = "iconv -f FROM -t TO ist der Standard-Konvertierungsbefehl.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "iconv -f FROM -t TO | file erkennt Encoding | UTF-8 = rückwärtskompatibel mit ASCII",
        memory_tip   = "iconv = i-convert = Zeichensatz konvertieren",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    Mission(
        mission_id   = "16.10",
        chapter      = 16,
        title        = "X11 & DISPLAY-Variable — Remote Display",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "PHANTOM",
        story        = "Phantom: 'Du willst eine GUI-Applikation über SSH anzeigen.\n DISPLAY=:0 reicht nicht. Du brauchst X11-Forwarding und xauth.\n Lass mich zeigen wie Ghost-Prozesse sich visuell materialisieren.'",
        why_important = "X11-Forwarding und die DISPLAY-Variable sind LPIC-1 Prüfungsthema.\nOhne sie: keine GUI-Apps über SSH.",
        explanation  = (
            "DISPLAY-Variable:\n"
            "  DISPLAY=HOST:DISPLAY_NR.SCREEN_NR\n"
            "  DISPLAY=:0       → Lokales Display 0, Screen 0\n"
            "  DISPLAY=:0.1     → Lokales Display 0, Screen 1\n"
            "  DISPLAY=192.168.1.1:0  → Remote X-Server\n"
            "\n"
            "X11-Forwarding via SSH:\n"
            "  ssh -X user@host         → X11-Forwarding aktivieren\n"
            "  ssh -Y user@host         → Trusted X11-Forwarding\n"
            "  /etc/ssh/sshd_config: X11Forwarding yes\n"
            "\n"
            "xauth:\n"
            "  xauth list               → Alle Authorizations\n"
            "  xauth add HOST:0 . COOKIE  → Cookie hinzufügen\n"
            "  ~/.Xauthority            → Authorisierungsdatei\n"
            "\n"
            "xhost:\n"
            "  xhost +hostname          → Host erlauben\n"
            "  xhost -hostname          → Host verbieten\n"
            "  xhost +                  → ALLE erlauben (unsicher!)"
        ),
        syntax       = "DISPLAY=:0 xterm &",
        example      = "ssh -X ghost@server xclock",
        task_description = "Zeige die aktuelle DISPLAY-Variable an.",
        expected_commands = ["echo $DISPLAY"],
        hint_text    = "echo $DISPLAY zeigt das aktuelle Display — DISPLAY=:0 setzt es",
        quiz_questions = [
            QuizQuestion(
                question    = "Was bedeutet DISPLAY=:0?",
                options     = ["Remote Host, Display 0", "Lokaler X-Server, Display 0, Screen 0", "Kein Display", "IPv6 Display"],
                correct     = 1,
                explanation = "DISPLAY=:0 = lokaler X-Server (kein Host), Display-Nummer 0.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher SSH-Flag aktiviert X11-Forwarding?",
                options     = ["-x", "-X", "-G", "-T"],
                correct     = 1,
                explanation = "ssh -X aktiviert X11-Forwarding. -Y ist trusted (weniger sicher eingeschränkt).",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "DISPLAY=HOST:D.S | ssh -X = X11-Forwarding | xhost + = ALLE erlauben (gefährlich)",
        memory_tip   = "DISPLAY = Adresse:Bildschirmnummer.Monitor — wie eine Telefonnummer für X11",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    Mission(
        mission_id   = "16.11",
        chapter      = 16,
        title        = "Display Manager — GDM, LightDM, SDDM",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = "Phantom: 'Der Login-Screen ist der Wächter des grafischen Systems.\n GDM, LightDM, SDDM — jeder DM hat seine Stärken.\n Kenn ihren Status. Kenn ihre Konfiguration.'",
        why_important = "Display Manager starten X11/Wayland und zeigen den Login-Bildschirm.\nLPIC-1 prüft Display Manager Konzepte.",
        explanation  = (
            "Display Manager (DM) = Login-Manager für GUI:\n"
            "  gdm3       → GNOME Display Manager (Ubuntu default)\n"
            "  lightdm    → Leichtgewichtig (Ubuntu/XFCE)\n"
            "  sddm       → Simple DM (KDE/Plasma)\n"
            "  xdm        → Klassisch, X Display Manager\n"
            "\n"
            "Verwaltung:\n"
            "  systemctl status gdm3     → Status\n"
            "  systemctl enable gdm3     → Autostart\n"
            "  dpkg-reconfigure gdm3     → Standard-DM wechseln\n"
            "\n"
            "Konfiguration:\n"
            "  /etc/gdm3/custom.conf     → GDM Konfiguration\n"
            "  /etc/lightdm/lightdm.conf → LightDM Konfiguration\n"
            "\n"
            "Default DM setzen (Debian/Ubuntu):\n"
            "  update-alternatives --config x-display-manager\n"
            "  /etc/X11/default-display-manager"
        ),
        syntax       = "systemctl status gdm3",
        example      = "cat /etc/X11/default-display-manager",
        task_description = "Zeige den Status des Display Managers an.",
        expected_commands = ["systemctl status gdm3", "systemctl status lightdm", "systemctl status sddm"],
        hint_text    = "systemctl status gdm3/lightdm/sddm — je nach installiertem DM",
        quiz_questions = [
            QuizQuestion(
                question    = "In welcher Datei steht der Standard-Display-Manager unter Debian?",
                options     = ["/etc/gdm/default", "/etc/X11/default-display-manager", "/etc/dm/default", "/etc/systemd/display-manager"],
                correct     = 1,
                explanation = "/etc/X11/default-display-manager enthält den Pfad zum Standard-DM.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher DM ist der Standard bei GNOME/Ubuntu?",
                options     = ["lightdm", "sddm", "gdm3", "xdm"],
                correct     = 2,
                explanation = "gdm3 (GNOME Display Manager 3) ist Standard bei Ubuntu mit GNOME.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "/etc/X11/default-display-manager | update-alternatives --config x-display-manager",
        memory_tip   = "DM = Display Manager = Türsteher für die grafische Oberfläche",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    Mission(
        mission_id   = "16.12",
        chapter      = 16,
        title        = "Wayland vs X11 — Moderne Display-Server",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = "Phantom: 'X11 ist 40 Jahre alt. Wayland ist die Zukunft.\n Aber vieles läuft noch auf X11. In NeonGrid-9 leben beide parallel.\n Kenn den Unterschied — oder scheitere an der falschen Schicht.'",
        why_important = "Wayland ersetzt X11 auf modernen Systemen. LPIC-1 kennt beide.",
        explanation  = (
            "X11 (X Window System):\n"
            "  Protokoll seit 1984, Netzwerktransparent\n"
            "  X-Server = steuert Hardware\n"
            "  X-Client = Applikation (Fenster)\n"
            "  X11 hat Client/Server-Architektur — auch über Netzwerk\n"
            "\n"
            "Wayland:\n"
            "  Modern, sicherer als X11\n"
            "  Compositor = kombiniert Display-Server + Window-Manager\n"
            "  Kein Netzwerk-Transparent nativ\n"
            "  Compositors: GNOME Mutter, KDE KWin, Sway\n"
            "\n"
            "Prüfen welches System läuft:\n"
            "  echo $WAYLAND_DISPLAY    → gesetzt bei Wayland\n"
            "  echo $DISPLAY            → gesetzt bei X11\n"
            "  loginctl show-session $XDG_SESSION_ID | grep Type\n"
            "\n"
            "XWayland:\n"
            "  Kompatibilitätsschicht für X11-Apps unter Wayland\n"
            "  Startet automatisch bei Bedarf"
        ),
        syntax       = "echo $WAYLAND_DISPLAY; echo $DISPLAY",
        example      = "loginctl show-session 1 | grep Type",
        task_description = "Prüfe ob das System unter X11 oder Wayland läuft.",
        expected_commands = ["echo $WAYLAND_DISPLAY", "echo $DISPLAY", "loginctl"],
        hint_text    = "WAYLAND_DISPLAY ist gesetzt bei Wayland, DISPLAY bei X11",
        quiz_questions = [
            QuizQuestion(
                question    = "Was ist der Hauptvorteil von Wayland gegenüber X11?",
                options     = ["Netzwerk-Transparenz", "Bessere Sicherheit und moderneres Design", "Mehr Kompatibilität", "Schnellerer Start"],
                correct     = 1,
                explanation = "Wayland ist sicherer — Clients können nicht gegenseitig ihre Fenster lesen.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist XWayland?",
                options     = ["X11 auf Windows", "Kompatibilitätsschicht für X11-Apps unter Wayland", "Wayland-Fork von X11", "Display Manager"],
                correct     = 1,
                explanation = "XWayland ermöglicht X11-Anwendungen unter Wayland zu laufen.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "WAYLAND_DISPLAY gesetzt = Wayland | DISPLAY gesetzt = X11 | XWayland = Kompatibilitätsschicht",
        memory_tip   = "Wayland = Way moderner als X11 | XWayland = Brücke zwischen alt und neu",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    Mission(
        mission_id   = "16.13",
        chapter      = 16,
        title        = "Zeitzonen — timedatectl & /etc/localtime",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'Logs zeigen UTC, dein System läuft in CET.\n Das macht Fehlersuche zur Tortur. Konfiguriere die Zeitzone korrekt.\n In NeonGrid-9 entscheiden Millisekunden.'",
        why_important = "Zeitzone-Fehler korrumpieren Log-Timestamps und verursachen\nAuthentifizierungsfehler (Kerberos, TLS-Zertifikate).",
        explanation  = (
            "Zeitzone setzen:\n"
            "  timedatectl list-timezones           → Alle Zeitzonen\n"
            "  timedatectl set-timezone Europe/Berlin → Zeitzone setzen\n"
            "  timedatectl status                   → Aktuelle Zeit + Zone\n"
            "\n"
            "/etc/localtime:\n"
            "  Symlink nach /usr/share/zoneinfo/...\n"
            "  ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime\n"
            "\n"
            "/etc/timezone:\n"
            "  Enthält Zeitzonenname: 'Europe/Berlin'\n"
            "  dpkg-reconfigure tzdata → Interaktiv setzen\n"
            "\n"
            "TZ-Variable:\n"
            "  TZ=America/New_York date → Temporär für einen Befehl\n"
            "  export TZ=UTC            → Für aktuelle Shell"
        ),
        syntax       = "timedatectl set-timezone Europe/Berlin",
        example      = "timedatectl status && cat /etc/timezone",
        task_description = "Zeige die aktuelle Zeitzone und NTP-Status an.",
        expected_commands = ["timedatectl status", "timedatectl"],
        hint_text    = "timedatectl status zeigt Zeitzone und NTP-Status",
        quiz_questions = [
            QuizQuestion(
                question    = "Wohin zeigt /etc/localtime?",
                options     = ["/etc/timezone", "/usr/share/zoneinfo/...", "/var/lib/timezone", "/proc/timezone"],
                correct     = 1,
                explanation = "/etc/localtime ist ein Symlink nach /usr/share/zoneinfo/REGION/STADT.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl setzt die Zeitzone persistent?",
                options     = ["date --timezone Europe/Berlin", "timedatectl set-timezone Europe/Berlin", "export TZ=Europe/Berlin", "timezone Europe/Berlin"],
                correct     = 1,
                explanation = "timedatectl set-timezone ist persistent und aktualisiert /etc/localtime.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "timedatectl set-timezone | /etc/localtime = Symlink | /etc/timezone = Name | TZ-Variable = temporär",
        memory_tip   = "timedatectl = time + date + ctl = alles in einem",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    Mission(
        mission_id   = "16.14",
        chapter      = 16,
        title        = "CUPS Drucken — lpr, lpq, lprm, lpstat",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'In NeonGrid-9 druckt niemand. Aber die Prüfung fragt danach.\n CUPS, lpr, lpq — lern die Befehle. Nicht für heute, sondern für die Prüfung.'",
        why_important = "LPIC-1 Topic 108.4 prüft CUPS Grundlagen. lpr, lpq, lprm sind Pflichtwissen.",
        explanation  = (
            "CUPS (Common Unix Printing System):\n"
            "  Daemon: cupsd\n"
            "  Web-Interface: http://localhost:631\n"
            "  Konfiguration: /etc/cups/\n"
            "\n"
            "Drucken:\n"
            "  lpr datei.pdf            → Drucken (Standard-Drucker)\n"
            "  lpr -P drucker datei.pdf → Bestimmter Drucker\n"
            "  lp datei.pdf             → Alternative zu lpr\n"
            "  lp -d drucker datei.pdf  → Drucker angeben\n"
            "\n"
            "Druckwarteschlange:\n"
            "  lpq                      → Warteschlange anzeigen\n"
            "  lpq -P drucker           → Bestimmter Drucker\n"
            "  lprm job_id              → Job entfernen\n"
            "  cancel job_id            → Alternative zu lprm\n"
            "\n"
            "Status:\n"
            "  lpstat -p                → Alle Drucker\n"
            "  lpstat -t                → Vollständiger Status\n"
            "  lpstat -d                → Standard-Drucker"
        ),
        syntax       = "lpr datei.pdf",
        example      = "lpstat -p && lpq",
        task_description = "Zeige alle Drucker und ihre Status an.",
        expected_commands = ["lpstat -p", "lpstat"],
        hint_text    = "lpstat -p zeigt alle Drucker — lpq zeigt Druckwarteschlange",
        quiz_questions = [
            QuizQuestion(
                question    = "Welcher Befehl zeigt die Druckwarteschlange an?",
                options     = ["lpr -q", "lpq", "lprm -l", "lpstat -q"],
                correct     = 1,
                explanation = "lpq zeigt die aktuelle Druckwarteschlange.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Auf welchem Port läuft das CUPS Web-Interface?",
                options     = ["80", "443", "631", "515"],
                correct     = 2,
                explanation = "CUPS Web-Interface läuft auf Port 631 (http://localhost:631).",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "lpr = drucken | lpq = queue anzeigen | lprm = job entfernen | lpstat -p = Drucker auflisten",
        memory_tip   = "lp = Line Printer: lpr(int) lp(q)ueue lp(r)(m)emove lp(stat)us",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    Mission(
        mission_id   = "16.15",
        chapter      = 16,
        title        = "Accessibility — Barrierefreiheit in Linux",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'NeonGrid-9 ist für alle zugänglich — auch für Ghosts mit Einschränkungen.\n Barrierefreiheit ist LPIC-Thema. Kenn die Tools.'",
        why_important = "LPIC-1 Topic 106.3 fragt nach Accessibility-Tools. Grundwissen genügt.",
        explanation  = (
            "Screen Reader:\n"
            "  orca         → GNOME Screen Reader (Sprachausgabe)\n"
            "  espeak       → Text-to-Speech: espeak 'Hallo Welt'\n"
            "  festival     → TTS-System: echo 'Hallo' | festival --tts\n"
            "\n"
            "Vergrößerung:\n"
            "  xmag         → X11-Lupe\n"
            "  kmag         → KDE-Lupe\n"
            "  GNOME: Einstellungen → Erleichterte Bedienung → Zoom\n"
            "\n"
            "Tastatur-Optionen (AccessX):\n"
            "  xkbset        → Tastatur-Zugänglichkeit\n"
            "  StickyKeys    → Modifier-Tasten einrasten\n"
            "  SlowKeys      → Zufällige Tastendrücke ignorieren\n"
            "  BounceKeys    → Doppelte Tastendrücke filtern\n"
            "\n"
            "Kontrast & Farben:\n"
            "  High-Contrast Themes in GNOME/KDE\n"
            "  xcalib        → Monitor-Kalibrierung"
        ),
        syntax       = "espeak 'Hallo Welt'",
        example      = "orca &",
        task_description = "Gib mit espeak eine Nachricht aus.",
        expected_commands = ["espeak", "orca"],
        hint_text    = "espeak 'Text' gibt Text als Sprache aus",
        quiz_questions = [
            QuizQuestion(
                question    = "Welches Tool ist der GNOME Screen Reader?",
                options     = ["espeak", "orca", "festival", "xmag"],
                correct     = 1,
                explanation = "Orca ist der Standard-Screen-Reader für GNOME.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was macht StickyKeys?",
                options     = ["Tastatur einrasten", "Modifier-Tasten einrasten lassen", "Tastendrücke verlangsamen", "Doppelklicks filtern"],
                correct     = 1,
                explanation = "StickyKeys lässt Modifier-Tasten (Shift, Ctrl, Alt) einrasten — für einhändige Bedienung.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "orca = GNOME Screen Reader | espeak = TTS | AccessX = Tastaturzugänglichkeit | xmag = Lupe",
        memory_tip   = "Accessibility = Zugänglichkeit = orca liest, espeak spricht, xmag vergrößert",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    Mission(
        mission_id   = "16.16",
        chapter      = 16,
        title        = "xorg.conf — X11 Grafikkonfiguration",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = "Phantom: 'Der Bildschirm bleibt schwarz. Der X-Server startet nicht.\n xorg.conf ist falsch — oder fehlt. Kenn die Struktur, kenn die Rettung.'",
        why_important = "xorg.conf ist LPIC-1 Prüfungsstoff. Grundstruktur und Hauptsektionen kennen.",
        explanation  = (
            "xorg.conf Struktur:\n"
            "  Befindet sich in /etc/X11/xorg.conf oder /etc/X11/xorg.conf.d/\n"
            "\n"
            "Wichtige Sektionen:\n"
            "  Section \"ServerLayout\"   → Verbindet Screen, InputDevice, Monitor\n"
            "  Section \"Monitor\"        → Bildschirm-Eigenschaften, HorizSync\n"
            "  Section \"Device\"         → Grafikkarte, Treiber (z.B. intel, nvidia)\n"
            "  Section \"Screen\"         → Auflösung, Farbtiefe, Monitor-Zuordnung\n"
            "  Section \"InputDevice\"    → Tastatur, Maus\n"
            "\n"
            "Diagnostik:\n"
            "  Xorg -configure          → Neue xorg.conf generieren\n"
            "  X :1 -retro &            → Test-X-Server starten\n"
            "  /var/log/Xorg.0.log      → X11 Log-Datei\n"
            "  grep '(EE)' /var/log/Xorg.0.log  → Fehler suchen\n"
            "  grep '(WW)' /var/log/Xorg.0.log  → Warnungen\n"
            "\n"
            "Ohne xorg.conf:\n"
            "  Moderne Systeme auto-konfigurieren sich (udev + KMS)\n"
            "  xorg.conf nur für spezielle Einstellungen nötig"
        ),
        syntax       = "grep '(EE)' /var/log/Xorg.0.log",
        example      = "Xorg -configure && cat /root/xorg.conf.new",
        task_description = "Suche nach Fehlern im X11-Log.",
        expected_commands = ["grep '(EE)' /var/log/Xorg.0.log", "cat /var/log/Xorg.0.log"],
        hint_text    = "grep '(EE)' /var/log/Xorg.0.log zeigt X11-Fehler",
        quiz_questions = [
            QuizQuestion(
                question    = "Welche Sektion in xorg.conf definiert die Grafikkarte?",
                options     = ["Section \"Graphics\"", "Section \"Device\"", "Section \"Video\"", "Section \"Hardware\""],
                correct     = 1,
                explanation = "Section \"Device\" enthält Grafikkarten-Einstellungen (Treiber, BusID).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was bedeutet (EE) in /var/log/Xorg.0.log?",
                options     = ["Extended Event", "Error Entry — Fehler", "End of Event", "Extra Extension"],
                correct     = 1,
                explanation = "(EE) = Error, (WW) = Warning, (II) = Information im X11-Log.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "/var/log/Xorg.0.log: (EE)=Error (WW)=Warning | Section Device = Grafikkarte | Xorg -configure",
        memory_tip   = "EE = Error, WW = Warning, II = Info — wie Ampelfarben im X-Log",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    Mission(
        mission_id   = "16.17",
        chapter      = 16,
        title        = "systemd-localed & localectl tief",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'localectl — ein Befehl für Locale UND Tastatur UND X11-Keymap.\n Der systemd-localed Daemon macht es möglich. Nutz ihn vollständig.'",
        why_important = "localectl ist der moderne Weg für Locale- und Tastatur-Verwaltung unter systemd.",
        explanation  = (
            "localectl Funktionen:\n"
            "  localectl status                        → Aktuelle Einstellungen\n"
            "  localectl set-locale LANG=de_DE.UTF-8   → Locale setzen\n"
            "  localectl set-keymap de                 → Tastatur (Konsole)\n"
            "  localectl set-x11-keymap de             → Tastatur (X11)\n"
            "  localectl set-x11-keymap de pc105 nodeadkeys  → Mit Variante\n"
            "\n"
            "Mehrere Locales:\n"
            "  localectl set-locale LANG=de_DE.UTF-8 LC_MESSAGES=en_US.UTF-8\n"
            "\n"
            "systemd-localed Daemon:\n"
            "  systemctl status systemd-localed\n"
            "  D-Bus Interface: org.freedesktop.locale1\n"
            "\n"
            "Konfigurationsdateien:\n"
            "  /etc/locale.conf         → Locale (systemd-Systeme)\n"
            "  /etc/vconsole.conf       → Konsolen-Tastatur"
        ),
        syntax       = "localectl set-locale LANG=de_DE.UTF-8",
        example      = "localectl status",
        task_description = "Zeige alle aktuellen Locale- und Tastatureinstellungen an.",
        expected_commands = ["localectl status", "localectl"],
        hint_text    = "localectl status zeigt alles in einem",
        quiz_questions = [
            QuizQuestion(
                question    = "In welcher Datei speichert systemd die Locale-Konfiguration?",
                options     = ["/etc/default/locale", "/etc/locale.conf", "/etc/locale.gen", "/etc/sysconfig/locale"],
                correct     = 1,
                explanation = "/etc/locale.conf ist die systemd-eigene Locale-Konfigurationsdatei.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl setzt die X11-Tastaturbelegung?",
                options     = ["localectl set-keymap de", "setxkbmap de", "localectl set-x11-keymap de", "xkbset de"],
                correct     = 2,
                explanation = "localectl set-x11-keymap setzt persistent die X11-Tastaturbelegung.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "/etc/locale.conf = systemd Locale | /etc/vconsole.conf = Konsolen-Tastatur | localectl = alles",
        memory_tip   = "localectl = local + ctl = Locale UND Keyboard in einem Befehl",
        gear_reward  = None,
        faction_reward = ("Net Runners", 8),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.18 — Locale-Umgebungsvariablen: LC_ALL, LC_MESSAGES, LANG
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.18",
        chapter      = 16,
        title        = "Locale-Umgebungsvariablen — LC_ALL, LANG & Priorität",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Das Terminal zeigt Fehlermeldungen auf Englisch\n"
            " obwohl das System auf Deutsch konfiguriert ist, Ghost.\n"
            " LC_MESSAGES überschreibt LANG für Systemmeldungen.\n"
            " Und LC_ALL? Das zerschlägt alles andere.\n"
            " Kenn die Priorität — oder verliere dich im Zeichensalat.'"
        ),
        why_important = (
            "Locale-Variablen steuern Sprache, Zahlen- und Datumsformat.\n"
            "LPIC-1 Topic 107.3 prüft die Priorität der LC_-Variablen.\n"
            "Falsch gesetzte Locales verursachen Encoding-Bugs in Produktionssystemen."
        ),
        explanation  = (
            "LOCALE-VARIABLEN — VOLLSTÄNDIGE ÜBERSICHT:\n\n"
            "PRIORITÄT (höchste zuerst):\n"
            "  1. LC_ALL           überschreibt ALLES — auch LC_* und LANG\n"
            "  2. LC_*             spezifische Kategorien (je nach Kontext)\n"
            "  3. LANG             Fallback für alle nicht gesetzten LC_*\n\n"
            "WICHTIGE LC_-VARIABLEN:\n"
            "  LANG=de_DE.UTF-8    Haupt-Locale (Fallback für alle LC_*)\n"
            "  LC_ALL=de_DE.UTF-8  Überschreibt ALLE anderen Locale-Vars\n"
            "  LC_MESSAGES=en_US   Sprache für Fehlermeldungen und Ausgaben\n"
            "  LC_CTYPE=de_DE.UTF-8  Zeichenklassifizierung (was ist ein Buchstabe?)\n"
            "  LC_COLLATE          Sortierreihenfolge (z.B. ä nach a oder am Ende)\n"
            "  LC_TIME             Datum-/Zeitformat (Montag oder Monday)\n"
            "  LC_NUMERIC          Zahlenformat (1.234,56 oder 1,234.56)\n"
            "  LC_MONETARY         Währungsformat\n"
            "  LC_PAPER            Papierformat (A4 oder Letter)\n\n"
            "PRAKTISCHE BEISPIELE:\n"
            "  LANG=de_DE.UTF-8 LC_MESSAGES=en_US.UTF-8\n"
            "  → System auf Deutsch, aber Fehlermeldungen auf Englisch\n"
            "  → Hilfreich für Debugging (englische Fehlermeldungen googeln)\n\n"
            "  LC_ALL=C            → POSIX-Locale erzwingen (ASCII, englisch)\n"
            "  → Nützlich in Skripten für konsistente Ausgabe\n"
            "  → LC_ALL=C sort → POSIX-Sortierung\n\n"
            "LOCALE ANZEIGEN UND SETZEN:\n"
            "  locale               aktuelle Werte anzeigen\n"
            "  locale -a            alle installierten Locales\n"
            "  locale -k LC_TIME    Schlüssel einer Kategorie anzeigen\n"
            "  export LANG=de_DE.UTF-8  temporär setzen\n"
            "  localectl set-locale LANG=de_DE.UTF-8  persistent (systemd)\n\n"
            "KONFIGURATIONSDATEIEN:\n"
            "  /etc/locale.conf         systemd-Systeme (Arch, Fedora)\n"
            "  /etc/default/locale      Debian/Ubuntu\n"
            "  /etc/locale.gen          verfügbare Locales (Debian)"
        ),
        syntax       = "locale  |  locale -a  |  export LC_ALL=C",
        example      = (
            "locale\n"
            "locale -a | grep de_DE\n"
            "export LANG=de_DE.UTF-8\n"
            "export LC_ALL=C\n"
            "LANG=de_DE.UTF-8 LC_MESSAGES=en_US.UTF-8 ls --help | head -5\n"
            "cat /etc/default/locale"
        ),
        task_description = "Zeige alle aktuellen Locale-Umgebungsvariablen an",
        expected_commands = ["locale"],
        hint_text    = "locale ohne Argumente zeigt alle aktuell gesetzten LC_-Variablen",
        quiz_questions = [
            QuizQuestion(
                question   = "In welcher Reihenfolge werden Locale-Variablen priorisiert (höchste zuerst)?",
                options    = [
                    "LANG > LC_* > LC_ALL",
                    "LC_* > LANG > LC_ALL",
                    "LC_ALL > LC_* > LANG",
                    "LANG > LC_ALL > LC_*",
                ],
                correct    = 2,
                explanation = (
                    "LC_ALL hat die höchste Priorität und überschreibt alle anderen.\n"
                    "LC_* (spezifische Kategorien) überschreiben LANG.\n"
                    "LANG ist der Fallback wenn keine spezifische LC_-Variable gesetzt ist."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welche Locale-Variable steuert die Sprache von Fehlermeldungen und Programmausgaben?",
                options    = [
                    "LANG",
                    "LC_ALL",
                    "LC_MESSAGES",
                    "LC_CTYPE",
                ],
                correct    = 2,
                explanation = (
                    "LC_MESSAGES bestimmt die Sprache für Systemmeldungen und Programmausgaben.\n"
                    "Trick: LANG=de_DE LC_MESSAGES=en_US → System deutsch, Meldungen englisch.\n"
                    "LC_CTYPE kontrolliert Zeichenklassifizierung (Buchstaben, Ziffern etc.)."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Locale-Priorität:\n"
            "  LC_ALL > LC_* > LANG\n"
            "  LC_ALL=C → POSIX-Locale (ASCII, englische Meldungen)\n"
            "  LC_MESSAGES → Sprache der Ausgaben\n"
            "  LC_CTYPE → Zeichenklassifizierung\n"
            "  /etc/default/locale → Debian, /etc/locale.conf → systemd"
        ),
        memory_tip   = "LC_ALL = ALL überschreibt alles. LANG = Sprach-Fallback. LC_MESSAGES = Meldungssprache.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.19 — Zeichenkodierung Konvertierung: iconv, file -i, hexdump, od
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.19",
        chapter      = 16,
        title        = "Zeichenkodierung — iconv, hexdump & od",
        mtype        = "DECODE",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Die Datei kommt vom alten Mainframe, Ghost.\n"
            " ISO-8859-1. Unsere Systeme erwarten UTF-8.\n"
            " iconv konvertiert. file -i verrät das Encoding.\n"
            " hexdump zeigt die rohen Bytes — die Wahrheit unter dem Text.\n"
            " Decode the signal.'"
        ),
        why_important = (
            "Encoding-Konvertierung ist Alltag beim Daten-Import aus Legacy-Systemen.\n"
            "LPIC-1 Topic 107.3 prüft iconv, file -i und Byte-Analyse.\n"
            "Falsche Encodings verursachen Datenverlust und kaputte Datenbanken."
        ),
        explanation  = (
            "ZEICHENKODIERUNG ERKENNEN UND KONVERTIEREN:\n\n"
            "ENCODING ERKENNEN:\n"
            "  file datei.txt           → Dateityp und Encoding erkennen\n"
            "  file -i datei.txt        → MIME-Type mit Charset-Info\n"
            "  file -b --mime-encoding datei.txt  → nur Encoding\n"
            "  Ausgabe: datei.txt: ISO-8859 text\n"
            "  Ausgabe: datei.txt: UTF-8 Unicode text\n\n"
            "ICONV — KONVERTIERUNG:\n"
            "  iconv -f QUELLE -t ZIEL datei.txt        → Ausgabe auf stdout\n"
            "  iconv -f ISO-8859-1 -t UTF-8 alt.txt     → UTF-8 auf stdout\n"
            "  iconv -f ISO-8859-1 -t UTF-8 alt.txt > neu.txt  → in Datei\n"
            "  iconv -f UTF-8 -t ASCII//TRANSLIT in.txt → Umlaute transliterieren\n"
            "  iconv -f UTF-8 -t ASCII//IGNORE in.txt   → nicht konvertierbare ignorieren\n"
            "  iconv -l                 → alle unterstützten Encodings\n"
            "  iconv -l | grep -i utf   → nur UTF-Varianten\n\n"
            "HEXDUMP — BYTES ANALYSIEREN:\n"
            "  hexdump -C datei.txt     → Hex + ASCII nebeneinander\n"
            "  hexdump -C datei.txt | head -5  → erste 5 Zeilen\n"
            "  hexdump -n 16 datei.txt  → erste 16 Bytes\n"
            "  BOM-Erkennung: EF BB BF = UTF-8 BOM\n"
            "                 FF FE    = UTF-16 LE BOM\n\n"
            "OD — OKTAL/HEX DUMP:\n"
            "  od -c datei.txt          → Zeichen-Dump (escaped chars)\n"
            "  od -x datei.txt          → Hex-Dump (16-bit)\n"
            "  od -An -tx1 datei.txt    → Bytes als Hex, ohne Adressen\n"
            "  od -c datei.txt | head   → Bytes und Sonderzeichen sehen\n\n"
            "PRAKTISCHES VORGEHEN:\n"
            "  1. file -i datei.txt       → Encoding herausfinden\n"
            "  2. hexdump -C datei.txt | head  → Bytes prüfen\n"
            "  3. iconv -f ALT -t UTF-8 datei.txt > neu.txt  → konvertieren\n"
            "  4. file -i neu.txt         → Ergebnis verifizieren"
        ),
        syntax       = "iconv -f ISO-8859-1 -t UTF-8 datei.txt > neu.txt",
        example      = (
            "file -i /etc/passwd\n"
            "file -b --mime-encoding /etc/motd\n"
            "iconv -f ISO-8859-1 -t UTF-8 alte_datei.txt > neue_datei.txt\n"
            "iconv -f UTF-8 -t ASCII//TRANSLIT eingabe.txt\n"
            "hexdump -C datei.txt | head -10\n"
            "od -c datei.txt | head -5"
        ),
        task_description = "Erkenne das Encoding einer Datei mit file -i",
        expected_commands = ["file -i /etc/passwd", "file -i"],
        hint_text    = "file -i datei zeigt den MIME-Typ inklusive Charset/Encoding",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher Befehl konvertiert eine Datei von ISO-8859-1 nach UTF-8?",
                options    = [
                    "convert -from ISO-8859-1 -to UTF-8 datei.txt",
                    "iconv -f ISO-8859-1 -t UTF-8 datei.txt",
                    "charset --input=iso -output=utf8 datei.txt",
                    "encode -source latin1 -dest utf8 datei.txt",
                ],
                correct    = 1,
                explanation = (
                    "iconv -f FROM -t TO ist der Standard-Befehl für Encoding-Konvertierung.\n"
                    "-f = from (Quell-Encoding), -t = to (Ziel-Encoding).\n"
                    "Ohne Ausgabedatei schreibt iconv auf stdout."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was zeigt 'file -i datei.txt' an?",
                options    = [
                    "Nur die Dateigröße",
                    "MIME-Typ und Zeichenkodierung (charset)",
                    "Die letzten 10 Zeilen der Datei",
                    "Die Inode-Nummer der Datei",
                ],
                correct    = 1,
                explanation = (
                    "file -i gibt den MIME-Typ mit Charset aus, z.B.:\n"
                    "  datei.txt: text/plain; charset=utf-8\n"
                    "  datei.txt: text/plain; charset=iso-8859-1\n"
                    "file ohne -i zeigt nur eine menschenlesbare Beschreibung."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Encoding-Tools:\n"
            "  file -i → MIME-Typ + Charset\n"
            "  iconv -f FROM -t TO → konvertieren\n"
            "  iconv -l → alle Encodings auflisten\n"
            "  hexdump -C → Hex + ASCII Dump\n"
            "  od -c → Oktal/Zeichen Dump\n"
            "  //TRANSLIT = Umlaute ersetzen, //IGNORE = überspringen"
        ),
        memory_tip   = "iconv = i-Convert: -f=from -t=to. file -i = Info mit Encoding",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.20 — Fontconfig & Schriften: fc-list, fc-cache, /etc/fonts/
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.20",
        chapter      = 16,
        title        = "Fontconfig — Schriften verwalten & fc-list",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "GHOST",
        story        = (
            "GHOST: 'Die Zeichen auf dem Display sind falsch, Ghost.\n"
            " Nicht das Encoding — die Schrift fehlt.\n"
            " fc-list zeigt installierte Fonts.\n"
            " fc-cache baut den Font-Cache neu.\n"
            " /etc/fonts/ ist das Nervenzentrum des Schrift-Systems.'"
        ),
        why_important = (
            "Fontconfig verwaltet alle Schriften unter Linux.\n"
            "LPIC-1 prüft Grundkenntnisse zu fc-list, fc-cache und /etc/fonts/.\n"
            "Font-Probleme sind häufige Ursache für kaputte GUI-Anwendungen."
        ),
        explanation  = (
            "FONTCONFIG — SCHRIFT-VERWALTUNG UNTER LINUX:\n\n"
            "FC-LIST — FONTS ANZEIGEN:\n"
            "  fc-list                  alle installierten Schriften\n"
            "  fc-list | grep -i mono   Monospace-Schriften finden\n"
            "  fc-list | grep -i dejavu DejaVu-Fonts\n"
            "  fc-list : family         nur Familiennamen\n"
            "  fc-list :lang=de         Schriften mit Deutsch-Support\n"
            "  fc-list :spacing=mono    nur Monospace-Fonts\n\n"
            "FC-CACHE — FONT-CACHE AKTUALISIEREN:\n"
            "  fc-cache                 User-Font-Cache aktualisieren\n"
            "  fc-cache -f              erzwingen (auch ohne Änderungen)\n"
            "  fc-cache -v              verbose (zeigt verarbeitete Verzeichnisse)\n"
            "  fc-cache -fv             force + verbose\n"
            "  sudo fc-cache -fv        System-Font-Cache aktualisieren\n\n"
            "FONT-VERZEICHNISSE:\n"
            "  /usr/share/fonts/        System-Fonts (alle User)\n"
            "  /usr/local/share/fonts/  lokal installierte System-Fonts\n"
            "  ~/.local/share/fonts/    User-eigene Fonts\n"
            "  ~/.fonts/                älterer User-Font-Pfad\n\n"
            "FONTCONFIG-KONFIGURATION:\n"
            "  /etc/fonts/              Haupt-Konfigurationsverzeichnis\n"
            "  /etc/fonts/fonts.conf    Haupt-Konfiguration\n"
            "  /etc/fonts/conf.d/       Konfigurations-Fragmente\n"
            "  /etc/fonts/local.conf    lokale Anpassungen\n"
            "  ~/.config/fontconfig/    User-eigene Konfiguration\n\n"
            "FONTS INSTALLIEREN:\n"
            "  1. Font-Datei nach /usr/share/fonts/ oder ~/.local/share/fonts/ kopieren\n"
            "  2. fc-cache -fv ausführen\n"
            "  3. Mit fc-list prüfen ob Font erkannt wird\n\n"
            "FC-MATCH — FONT SUCHEN:\n"
            "  fc-match DejaVu          besten passenden Font finden\n"
            "  fc-match monospace       Standard-Monospace-Font\n"
            "  fc-query /pfad/font.ttf  Font-Datei analysieren"
        ),
        syntax       = "fc-list  |  fc-cache -fv  |  fc-match FONTNAME",
        example      = (
            "fc-list | head -20\n"
            "fc-list | grep -i mono\n"
            "fc-list :lang=de\n"
            "fc-cache -fv\n"
            "sudo fc-cache -fv\n"
            "fc-match monospace\n"
            "ls /etc/fonts/conf.d/"
        ),
        task_description = "Liste alle installierten Schriften mit fc-list auf",
        expected_commands = ["fc-list"],
        hint_text    = "fc-list zeigt alle von fontconfig erkannten installierten Schriften",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher Befehl aktualisiert den Fontconfig-Schrift-Cache?",
                options    = [
                    "font-update",
                    "update-fonts",
                    "fc-cache -fv",
                    "fontconfig --rebuild",
                ],
                correct    = 2,
                explanation = (
                    "fc-cache -fv aktualisiert den Font-Cache.\n"
                    "-f = force (erzwingen), -v = verbose.\n"
                    "Nach dem Installieren neuer Fonts immer fc-cache ausführen."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "In welchem Verzeichnis liegt die Fontconfig-Hauptkonfiguration?",
                options    = [
                    "/etc/X11/fonts/",
                    "/usr/share/fonts/",
                    "/etc/fonts/",
                    "/var/lib/fontconfig/",
                ],
                correct    = 2,
                explanation = (
                    "/etc/fonts/ ist das Fontconfig-Konfigurationsverzeichnis.\n"
                    "/etc/fonts/fonts.conf = Hauptkonfiguration.\n"
                    "/etc/fonts/conf.d/ = Konfigurations-Fragmente (wie /etc/rsyslog.d/).\n"
                    "/usr/share/fonts/ enthält die Schrift-Dateien selbst."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Fontconfig:\n"
            "  fc-list → installierte Fonts anzeigen\n"
            "  fc-cache -fv → Font-Cache neu aufbauen\n"
            "  /etc/fonts/ → Konfigurationsverzeichnis\n"
            "  /usr/share/fonts/ → System-Font-Dateien\n"
            "  ~/.local/share/fonts/ → User-Fonts"
        ),
        memory_tip   = "fc = font config: fc-list=auflisten, fc-cache=cache bauen, fc-match=suchen",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    Mission(
        mission_id   = "16.quiz",
        chapter      = 16,
        title        = "LOCALE MATRIX — Abschluss-Quiz",
        mtype        = "QUIZ",
        xp           = 150,
        speaker      = "SYSTEM",
        story        = "SYSTEM: 'Locale Matrix Prüfung. Zeig was du über Lokalisierung, X11 und Drucken weißt.'",
        why_important = "Quiz-Wiederholung aller Locale-Matrix Themen für LPIC-1 Vorbereitung.",
        explanation  = "Alle Locale-, X11-, Tastatur-, Zeitzone- und CUPS-Themen aus Kapitel 16.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Quiz-Fragen zu Lokalisierung, X11 und CUPS.",
        expected_commands = [],
        hint_text    = "Nutze [r] Review Mode für Wiederholung",
        quiz_questions = [
            QuizQuestion(
                question    = "Welche Variable überschreibt ALLE anderen LC_-Variablen?",
                options     = ["LANG", "LC_MESSAGES", "LC_ALL", "LANGUAGE"],
                correct     = 2,
                explanation = "LC_ALL überschreibt alle anderen Locale-Variablen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'locale-gen'?",
                options     = ["Locale-Variablen anzeigen", "Locales generieren/kompilieren", "Locale setzen", "Tastatur generieren"],
                correct     = 1,
                explanation = "locale-gen kompiliert die in /etc/locale.gen aktivierten Locales.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welcher Befehl konvertiert Zeichenkodierung?",
                options     = ["charconv", "iconv", "encode", "recode"],
                correct     = 1,
                explanation = "iconv konvertiert zwischen verschiedenen Zeichenkodierungen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist DISPLAY=:0?",
                options     = ["Remote X-Server", "Kein Display", "Lokaler X-Server, Display 0", "Wayland Display"],
                correct     = 2,
                explanation = "DISPLAY=:0 bedeutet: lokaler X-Server, Display-Nummer 0.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "CUPS Web-Interface läuft auf Port:",
                options     = ["80", "443", "515", "631"],
                correct     = 3,
                explanation = "CUPS läuft auf Port 631 (http://localhost:631).",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Wohin zeigt /etc/localtime?",
                options     = ["/etc/timezone", "/usr/share/zoneinfo/...", "/var/lib/timezone", "/proc/sys/timezone"],
                correct     = 1,
                explanation = "/etc/localtime ist Symlink nach /usr/share/zoneinfo/REGION/STADT.",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "LC_ALL > LANG | iconv -f FROM -t TO | DISPLAY=:D.S | CUPS Port 631 | /etc/localtime = Symlink",
        memory_tip   = "Locale-Matrix: Sprache + Tastatur + Display + Zeit + Drucker",
        gear_reward  = None,
        faction_reward = ("Net Runners", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 16.BOSS — GLITCH RENDERER
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "16.boss",
        chapter      = 16,
        title        = "BOSS: GLITCH RENDERER v16.0",
        mtype        = "BOSS",
        xp           = 180,
        speaker      = "GLITCH RENDERER",
        story        = (
            "GLITCH RENDERER: 'Du siehst mich nicht, Ghost.\n"
            " Falsche Locale — dein Terminal zeigt nur ???.\n"
            " Falsche Zeitzone — deine Logs stimmen nicht.\n"
            " X11 gecrashed — kein Display.\n"
            " Ich bin das Chaos in der Rendering-Schicht.\n"
            " Stelle die Locale auf UTF-8 — wenn du kannst.'"
        ),
        why_important = (
            "Lokalisierung, X11 und Drucken klingen trivial — bis der Server\n"
            "nach Mitternacht Umlaute als ??? loggt und du weißt nicht warum.\n"
            "Sysadmin-Pflichtkenntnis: Locale-Debugging rettet Logs."
        ),
        explanation  = (
            "Locale-Debugging Workflow:\n"
            "  locale                    → Aktuelle Werte\n"
            "  locale -a | grep de_DE    → Ist de_DE.UTF-8 installiert?\n"
            "  sudo locale-gen de_DE.UTF-8  → Locale generieren\n"
            "  sudo update-locale LANG=de_DE.UTF-8  → Systemweite Locale\n"
            "  source /etc/default/locale   → In aktuelle Shell laden\n"
            "\n"
            "X11-Diagnose:\n"
            "  xdpyinfo 2>/dev/null || echo 'Kein X-Display'\n"
            "  DISPLAY=:0 xterm &   → Neues Terminal öffnen\n"
            "  Xorg -configure      → Neue xorg.conf generieren\n"
            "\n"
            "CUPS-Diagnose:\n"
            "  systemctl status cups\n"
            "  tail -f /var/log/cups/error_log\n"
            "  lpstat -t            → Vollständiger Status"
        ),
        syntax       = "locale -a | grep UTF-8 | head -5",
        example      = "sudo localectl set-locale LANG=de_DE.UTF-8",
        task_description = (
            "FINALE PRÜFUNG: Das System hat eine defekte Locale.\n"
            "Zeige alle installierten Locales an."
        ),
        expected_commands = ["locale -a"],
        hint_text    = "locale -a listet alle installierten Locales auf",
        quiz_questions = [],
        exam_tip     = "locale -a = installierte Locales | locale-gen = generieren | update-locale = setzen",
        memory_tip   = "Locale-Fix: locale -a → locale-gen → update-locale → source /etc/default/locale",
        gear_reward  = "display_lens",
        faction_reward = ("Net Runners", 35),
    ),
]
