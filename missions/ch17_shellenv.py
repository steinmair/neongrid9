"""
NeonGrid-9 :: Kapitel 17 — SHELL ENV
LPIC-1 Topic 105.1
Shell-Umgebung: Startup-Dateien, Variablen, Aliases, Funktionen, PATH

"In NeonGrid-9 ist die Shell dein Cockpit.
 Wer seine Umgebung nicht kennt, kämpft blind.
 .bashrc, .profile, export, alias —
 forme die Shell nach deinem Willen."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_17_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 17.01 — Shell-Startup-Dateien
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.01",
        chapter      = 17,
        title        = "Shell-Startup-Dateien — .bashrc vs .profile",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Dein alias wird manchmal geladen, manchmal nicht.\n"
            " Du weißt nicht warum. Das ist das Startup-Datei-Problem.\n"
            " .bashrc, .profile, .bash_profile — jede hat ihre eigene Logik.\n"
            " Kenne den Unterschied — oder kämpfe ewig gegen unsichtbare Mauern.'"
        ),
        why_important = (
            "Shell-Startup-Dateien werden in bestimmter Reihenfolge geladen —\n"
            "abhängig davon ob die Shell interaktiv, login oder non-login ist.\n"
            "Falsche Datei → Einstellung wird nicht geladen → Diagnose-Alptraum."
        ),
        explanation  = (
            "Shell-Typen:\n"
            "  Login-Shell:     Beim SSH-Login, su -, sudo -i, tty-Login\n"
            "  Interaktive Shell: Terminal-Emulator, neue bash\n"
            "  Non-interactive:  Skript-Ausführung (keine Prompts)\n"
            "\n"
            "Bash Login-Shell liest (in Reihenfolge):\n"
            "  /etc/profile               → Systemweit\n"
            "  /etc/profile.d/*.sh        → Systemweite Fragmente\n"
            "  ~/.bash_profile            → User (wenn vorhanden, Suche stoppt)\n"
            "  ~/.bash_login              → User (wenn .bash_profile fehlt)\n"
            "  ~/.profile                 → User (wenn beide fehlen)\n"
            "  Beim Logout: ~/.bash_logout\n"
            "\n"
            "Bash Interaktive Non-Login-Shell liest:\n"
            "  /etc/bash.bashrc           → Systemweit\n"
            "  ~/.bashrc                  → User\n"
            "\n"
            "Best Practice:\n"
            "  ~/.profile     → Umgebungsvariablen (PATH, EDITOR, ...)\n"
            "  ~/.bashrc      → Aliases, Funktionen, Prompt (PS1)\n"
            "  .bash_profile  → Nur: source ~/.profile && source ~/.bashrc\n"
            "\n"
            "source / . (dot):\n"
            "  source ~/.bashrc           → Datei in aktuelle Shell laden\n"
            "  . ~/.bashrc                → Identisch (POSIX-kompatibel)\n"
            "  bash vs source: bash startet neue Shell, source = aktuelle"
        ),
        ascii_art = """
  ███████╗██╗  ██╗███████╗██╗     ██╗         ███████╗███╗   ██╗██╗   ██╗
  ██╔════╝██║  ██║██╔════╝██║     ██║         ██╔════╝████╗  ██║██║   ██║
  ███████╗███████║█████╗  ██║     ██║         █████╗  ██╔██╗ ██║██║   ██║
  ╚════██║██╔══██║██╔══╝  ██║     ██║         ██╔══╝  ██║╚██╗██║╚██╗ ██╔╝
  ███████║██║  ██║███████╗███████╗███████╗    ███████╗██║ ╚████║ ╚████╔╝
  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═══╝  ╚═══╝

  [ CHAPTER 17 :: SHELL ENVIRONMENT ]
  > .bashrc sourced. PATH loaded. alias defined. export active.""",
        story_transitions = [
            "Die Shell-Umgebung ist dein Werkzeugkasten. Kenn jeden Inhalt.",
            ".bashrc vs .bash_profile: Login-Shell vs interaktive Shell.",
            "PATH bestimmt was ausgeführt wird. Falscher PATH = falsches Programm.",
            "Phantom Shell hat deinen PATH vergiftet. Finde es heraus.",
        ],
        syntax       = "cat ~/.bashrc",
        example      = "source ~/.bashrc  # oder: . ~/.bashrc",
        task_description = "Zeige den Inhalt deiner .bashrc an.",
        expected_commands = ["cat ~/.bashrc"],
        hint_text    = "~/.bashrc ist die User-Konfigurationsdatei für interaktive Shells",
        quiz_questions = [
            QuizQuestion(
                question    = "Welche Startup-Datei liest eine interaktive Non-Login-Shell (z.B. neues Terminal)?",
                options     = ["~/.bash_profile", "~/.profile", "~/.bashrc", "/etc/profile"],
                correct     = 2,
                explanation = "Non-Login-Shell (Terminal-Emulator, neue bash): ~/.bashrc\nLogin-Shell (SSH, su -, tty-Login): /etc/profile → ~/.bash_profile\nbash_profile wird bevorzugt über .bash_login und .profile.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'source ~/.bashrc' und 'bash ~/.bashrc'?",
                options     = ["Kein Unterschied", "source lädt in aktuelle Shell, bash öffnet neue Sub-Shell", "bash ist schneller als source", "source prüft Syntax, bash führt direkt aus"],
                correct     = 1,
                explanation = "source (oder .) lädt die Datei in die AKTUELLE Shell.\nbash ~/.bashrc öffnet eine neue Sub-Shell — Änderungen gelten nicht in der aktuellen Shell!",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welche Datei wird beim Logout einer Login-Shell ausgeführt?",
                options     = ["~/.bash_exit", "~/.bash_logout", "~/.logout", "/etc/logout"],
                correct     = 1,
                explanation = "~/.bash_logout wird beim Logout einer Bash-Login-Shell ausgeführt.\nTypische Verwendung: Terminal leeren, Audit-Log-Einträge schreiben.",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "Login-Shell: /etc/profile → ~/.bash_profile | Non-Login: ~/.bashrc",
        memory_tip   = "Merke: .bashrc = bash-Resource (interaktiv) | .profile = Login-Umgebung",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.02 — Umgebungsvariablen: export & env
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.02",
        chapter      = 17,
        title        = "Umgebungsvariablen — export, env & set",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Das Programm findet den Editor nicht.\n"
            " EDITOR ist nicht gesetzt — oder nicht exportiert.\n"
            " Eine Variable existiert in der Shell, aber\n"
            " ohne export sehen Kind-Prozesse sie nicht.\n"
            " Versteh den Unterschied — es ist grundlegend.'"
        ),
        why_important = (
            "Shell-Variablen ohne export sind nur in der aktuellen Shell sichtbar.\n"
            "Exportierte Variablen werden an alle Kind-Prozesse vererbt.\n"
            "env, set und printenv unterscheiden sich wesentlich."
        ),
        explanation  = (
            "Variablen setzen:\n"
            "  VAR=wert              → Shell-Variable (nur aktuelle Shell)\n"
            "  export VAR=wert       → Umgebungsvariable (an Kind-Prozesse)\n"
            "  export VAR            → Bereits gesetzte Variable exportieren\n"
            "  readonly VAR=wert     → Schreibgeschützte Variable\n"
            "  unset VAR             → Variable löschen\n"
            "\n"
            "Anzeigen:\n"
            "  env                   → Alle Umgebungsvariablen (exportiert)\n"
            "  printenv              → Wie env\n"
            "  printenv PATH         → Einzelne Variable\n"
            "  set                   → Alle Variablen + Funktionen (inkl. Shell-interne)\n"
            "  declare -x            → Exportierte Variablen\n"
            "  declare -r            → Read-only Variablen\n"
            "\n"
            "Wichtige Systemvariablen:\n"
            "  PATH    → Suchpfad für Befehle\n"
            "  HOME    → Home-Verzeichnis\n"
            "  USER    → Aktueller Benutzername\n"
            "  SHELL   → Aktuelle Shell\n"
            "  EDITOR  → Standard-Texteditor\n"
            "  TERM    → Terminal-Typ\n"
            "  HISTSIZE → Größe der History (in Memory)\n"
            "  HISTFILESIZE → Größe von ~/.bash_history\n"
            "  PS1     → Shell-Prompt\n"
            "\n"
            "Für einzelnen Befehl:\n"
            "  LANG=C command        → Nur für diesen Befehl"
        ),
        syntax       = "env",
        example      = "export EDITOR=vim && printenv EDITOR",
        task_description = "Zeige alle Umgebungsvariablen an.",
        expected_commands = ["env"],
        hint_text    = "env zeigt alle exportierten Umgebungsvariablen",
        quiz_questions = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen einer Shell-Variable und einer Umgebungsvariable?",
                options     = ["Es gibt keinen Unterschied", "Shell-Variablen sind nur in der aktuellen Shell sichtbar, Umgebungsvariablen (export) werden an Kind-Prozesse vererbt", "Umgebungsvariablen sind nur für root", "Shell-Variablen werden automatisch exportiert"],
                correct     = 1,
                explanation = "VAR=wert = nur in aktueller Shell sichtbar.\nexport VAR = wird an alle Kind-Prozesse vererbt.\nKind-Prozesse erben die Umgebung, nicht Shell-interne Variablen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was zeigt 'env' im Vergleich zu 'set'?",
                options     = ["env zeigt mehr als set", "env = nur exportierte Variablen | set = alle Variablen + Shell-Funktionen", "set = exportierte Variablen | env = Shell-interne", "Beide zeigen identische Ausgabe"],
                correct     = 1,
                explanation = "env/printenv = nur exportierte Umgebungsvariablen.\nset = alle Variablen (exportiert + lokal) + Shell-Funktionen und Einstellungen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Wie setzt man eine Variable nur für einen einzelnen Befehl?",
                options     = ["set VAR=wert && befehl && unset VAR", "VAR=wert befehl", "export VAR=wert; befehl; unset VAR", "env -s VAR=wert befehl"],
                correct     = 1,
                explanation = "VAR=wert BEFEHL setzt die Variable nur für diesen einen Befehl.\nBeispiel: LANG=C ls /etc zeigt englische Fehlermeldungen.\nDie Variable existiert nicht nach dem Befehl.",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "env = exportierte Vars | set = alle Vars + Funktionen | export = an Kind-Prozesse",
        memory_tip   = "Ohne export: unsichtbar für Kind-Prozesse | export = Vererbung aktivieren",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.03 — PATH manipulieren
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.03",
        chapter      = 17,
        title        = "PATH — Suchpfad konfigurieren",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Du hast das Tool installiert. Es liegt in ~/bin.\n"
            " Du tippst den Namen. 'command not found'.\n"
            " PATH kennt ~/bin nicht.\n"
            " Erweitere PATH — füge deinen Bin-Pfad hinzu.'"
        ),
        why_important = (
            "PATH bestimmt, wo die Shell nach ausführbaren Befehlen sucht.\n"
            "Falscher oder fehlender PATH-Eintrag = 'command not found'.\n"
            "Sicherheit: '.' (aktuelles Verzeichnis) gehört NICHT in PATH!"
        ),
        explanation  = (
            "PATH erweitern:\n"
            "  export PATH=$PATH:~/bin         → ~/bin am Ende hinzufügen\n"
            "  export PATH=~/bin:$PATH         → ~/bin am Anfang (höhere Prio)\n"
            "  export PATH=$PATH:/opt/app/bin  → Beliebiger Pfad\n"
            "\n"
            "Dauerhaft (in ~/.profile oder ~/.bashrc):\n"
            "  export PATH=\"$HOME/bin:$PATH\"\n"
            "\n"
            "PATH-Diagnose:\n"
            "  echo $PATH           → Aktuellen PATH anzeigen\n"
            "  which befehl         → Wo liegt der Befehl?\n"
            "  type befehl          → Alias/Funktion/Binary/Builtin?\n"
            "  type -a befehl       → Alle Treffer (nicht nur erster)\n"
            "  command -v befehl    → Wie which, POSIX-kompatibel\n"
            "  hash -r              → Command-Hash-Table leeren (nach PATH-Änderung)\n"
            "\n"
            "Reihenfolge der Befehlssuche:\n"
            "  1. Aliases\n"
            "  2. Shell-Builtins (echo, cd, ...)\n"
            "  3. Funktionen\n"
            "  4. PATH-Einträge (von links nach rechts)\n"
            "\n"
            "Sicherheit:\n"
            "  PATH=.:$PATH → GEFÄHRLICH! Angreifer kann 'ls' in /tmp ablegen\n"
            "  Als root niemals '.' in PATH!"
        ),
        syntax       = "echo $PATH",
        example      = "export PATH=\"$HOME/bin:$PATH\"",
        task_description = "Zeige den aktuellen PATH an.",
        expected_commands = ["echo $PATH"],
        hint_text    = "$PATH enthält alle Verzeichnisse, die nach Befehlen durchsucht werden",
        quiz_questions = [
            QuizQuestion(
                question    = "Wie fügt man ~/bin dauerhaft am Anfang des PATH hinzu (höchste Priorität)?",
                options     = ["PATH=~/bin", "export PATH=~/bin:$PATH", "add-path ~/bin", "PATH+=$HOME/bin"],
                correct     = 1,
                explanation = "export PATH=$HOME/bin:$PATH fügt ~/bin mit höchster Priorität hinzu.\nVorne im PATH = höhere Priorität als System-Binaries.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Warum sollte '.' (aktuelles Verzeichnis) NICHT in PATH sein?",
                options     = ["Verlangsamt die Shell", "Sicherheitsrisiko: Angreifer kann 'ls' in /tmp ablegen", "Macht Befehle langsamer", "Funktioniert nur bei root"],
                correct     = 1,
                explanation = "PATH=.:$PATH ist gefährlich: Ein Angreifer legt 'ls' in /tmp ab.\nWenn du dort arbeitest, wird der Angreifer-Code statt /bin/ls ausgeführt.\nAls root ist '.' im PATH kritisch!",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'hash -r' nach einer PATH-Änderung?",
                options     = ["Berechnet SHA-Hash aller Befehle", "Leert den Command-Hash-Cache der Shell", "Neustartet die Shell", "Ändert den PATH zurück"],
                correct     = 1,
                explanation = "Bash cached Befehlspfade in einer Hash-Tabelle für Geschwindigkeit.\nhash -r leert diesen Cache, damit nach PATH-Änderung neu gesucht wird.\nOhne hash -r: Bash nutzt noch alte (gecachte) Pfade.",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "type -a befehl zeigt ALLE Treffer | hash -r nach PATH-Änderung | '.' NICHT in PATH!",
        memory_tip   = "PATH: links = höhere Priorität | $HOME/bin vorne = eigene Tools überschreiben System",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.04 — Aliases & Shell-Funktionen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.04",
        chapter      = 17,
        title        = "Aliases & Shell-Funktionen",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Du tippst 'ls -la --color=auto' 50 Mal am Tag.\n"
            " Das ist ineffizient — und langweilig.\n"
            " alias ll='ls -la --color=auto' — einmal definiert, ewig nützlich.\n"
            " Funktionen können sogar Argumente nehmen. Zeig mir deine Aliases.'"
        ),
        why_important = (
            "Aliases kürzen häufige Befehle ab. Funktionen erlauben komplexere\n"
            "Logik mit Parametern. Beide werden in ~/.bashrc definiert.\n"
            "LPIC-1: alias, unalias, type — Pflicht-Wissen."
        ),
        explanation  = (
            "Aliases:\n"
            "  alias ll='ls -la --color=auto'   → Alias definieren\n"
            "  alias                             → Alle Aliases anzeigen\n"
            "  alias ll                          → Einzelnen Alias anzeigen\n"
            "  unalias ll                        → Alias löschen\n"
            "  unalias -a                        → Alle Aliases löschen\n"
            "  \\ll                               → Alias umgehen (Original ausführen)\n"
            "\n"
            "Dauerhaft: In ~/.bashrc eintragen:\n"
            "  alias ll='ls -la --color=auto'\n"
            "  alias la='ls -A'\n"
            "  alias grep='grep --color=auto'\n"
            "  alias update='sudo apt update && sudo apt upgrade'\n"
            "\n"
            "Shell-Funktionen (mächtiger als Aliases):\n"
            "  mkcd() { mkdir -p \"$1\" && cd \"$1\"; }\n"
            "  backup() { cp \"$1\" \"$1.bak.$(date +%Y%m%d)\"; }\n"
            "\n"
            "Funktionen vs Aliases:\n"
            "  Alias: einfache Textersetzung, keine Logik\n"
            "  Funktion: Argumente ($1 $2), Schleifen, Bedingungen\n"
            "\n"
            "type Befehl:\n"
            "  type ll          → 'll is aliased to ls -la --color=auto'\n"
            "  type cd          → 'cd is a shell builtin'\n"
            "  type ls          → 'ls is /bin/ls'\n"
            "  type mkcd        → 'mkcd is a function'"
        ),
        syntax       = "alias",
        example      = "alias ll='ls -la --color=auto'",
        task_description = "Zeige alle aktuell definierten Aliases an.",
        expected_commands = ["alias"],
        hint_text    = "alias ohne Argumente listet alle definierten Aliases auf",
        quiz_questions = [
            QuizQuestion(
                question    = "Wie führt man den originalen 'ls' aus, wenn ein Alias 'll' darauf zeigt?",
                options     = ["original ls", "\\ls", "unalias ls && ls", "which ls | exec"],
                correct     = 1,
                explanation = "\\BEFEHL umgeht den Alias und führt den Original-Befehl aus.\n\\ls = /bin/ls direkt, kein Alias.\nAlternativ: command ls oder 'ls' in Anführungszeichen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist der Hauptvorteil von Shell-Funktionen gegenüber Aliases?",
                options     = ["Funktionen sind schneller", "Funktionen akzeptieren Argumente ($1, $2) und können Logik enthalten", "Aliases sind nur für interaktive Shells", "Funktionen werden in PATH gespeichert"],
                correct     = 1,
                explanation = "Aliases = einfache Textersetzung, keine Argumente.\nFunktionen = volle Bash-Logik mit $1 $2, if/else, Schleifen, etc.\nBeispiel: mkcd() { mkdir -p \"$1\" && cd \"$1\"; }",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was zeigt 'type ll' wenn ll ein Alias ist?",
                options     = ["ll not found", "ll is /bin/ll", "ll is aliased to 'ls -la --color=auto'", "ll is a shell function"],
                correct     = 2,
                explanation = "type BEFEHL identifiziert den Typ: alias, function, builtin oder binary.\ntype ll → 'll is aliased to ...'\ntype cd → 'cd is a shell builtin'",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "alias zeigt alle | unalias -a löscht alle | \\befehl umgeht Alias | type = was ist es?",
        memory_tip   = "Alias = Textersetzung (kein $1) | Funktion = Logik mit Parametern",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.05 — Shell-History & Steuerung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.05",
        chapter      = 17,
        title        = "Shell-History & Bash-Steuerung",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Den langen Befehl von vorhin — tippe ihn nicht nochmal.\n"
            " history, !! und Ctrl+R sind deine Werkzeuge.\n"
            " Bash-History ist Wissensspeicher und Sicherheitsrisiko zugleich.\n"
            " Kenn die Mechanismen — beide Seiten.'"
        ),
        why_important = (
            "Shell-History spart Zeit und ist forensisch relevant:\n"
            "Was hat ein Benutzer zuletzt ausgeführt?\n"
            "HISTSIZE, HISTFILESIZE, HISTCONTROL — Pflicht für LPIC-1."
        ),
        explanation  = (
            "History-Befehle:\n"
            "  history              → Verlauf anzeigen (nummeriert)\n"
            "  history 20           → Letzte 20 Befehle\n"
            "  history -c           → History leeren (nur Memory)\n"
            "  history -w           → History in Datei schreiben\n"
            "  !42                  → Befehl Nr. 42 ausführen\n"
            "  !!                   → Letzten Befehl wiederholen\n"
            "  !ssh                 → Letzten Befehl der mit 'ssh' beginnt\n"
            "  !$                   → Letztes Argument des Vorbefehls\n"
            "  !*                   → Alle Argumente des Vorbefehls\n"
            "  Ctrl+R               → Rückwärts-Suche in History\n"
            "  Ctrl+G               → Suche abbrechen\n"
            "\n"
            "History-Konfiguration:\n"
            "  HISTSIZE=1000        → Zeilen in Memory\n"
            "  HISTFILESIZE=2000    → Zeilen in ~/.bash_history\n"
            "  HISTFILE=~/.bash_history  → History-Datei\n"
            "  HISTCONTROL=ignoredups    → Duplikate nicht speichern\n"
            "  HISTCONTROL=ignorespace   → Mit Leerzeichen beginnende Befehle nicht speichern\n"
            "  HISTCONTROL=ignoreboth    → Beide\n"
            "  HISTTIMEFORMAT='%F %T '   → Timestamp in History\n"
            "\n"
            "Sicherheit:\n"
            "  history -c && history -w  → History löschen\n"
            "  HISTFILE=/dev/null         → History komplett deaktivieren\n"
            "   befehl                   → (Leerzeichen) nicht in History"
        ),
        syntax       = "history",
        example      = "history | grep ssh",
        task_description = "Zeige die Shell-History an.",
        expected_commands = ["history"],
        hint_text    = "history zeigt den nummerierten Befehlsverlauf an",
        quiz_questions = [
            QuizQuestion(
                question    = "Was macht '!!' in der Bash-Shell?",
                options     = ["Gibt eine Warnung aus", "Wiederholt den letzten Befehl", "Löscht die History", "Gibt alle Befehle aus"],
                correct     = 1,
                explanation = "!! = letzter Befehl wiederholen.\n!42 = Befehl #42 ausführen | !ssh = letzten ssh-Befehl | Ctrl+R = interaktive Suche.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was bewirkt HISTCONTROL=ignoreboth?",
                options     = ["Deaktiviert die History komplett", "Ignoriert Duplikate UND Befehle mit führendem Leerzeichen", "Ignoriert nur Duplikate", "Speichert nur die letzten 100 Befehle"],
                correct     = 1,
                explanation = "HISTCONTROL=ignoreboth = ignoredups + ignorespace kombiniert.\nignoredups = keine aufeinanderfolgenden Duplikate.\nignorespace = Befehle mit führendem Leerzeichen werden nicht gespeichert.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen HISTSIZE und HISTFILESIZE?",
                options     = ["Kein Unterschied", "HISTSIZE = Zeilen in Memory | HISTFILESIZE = Zeilen in ~/.bash_history", "HISTSIZE = Zeichenanzahl | HISTFILESIZE = Zeilenanzahl", "HISTFILESIZE ist deprecated"],
                correct     = 1,
                explanation = "HISTSIZE = Anzahl Befehle im Arbeitsspeicher (Shell-Session).\nHISTFILESIZE = Anzahl Zeilen in ~/.bash_history (Datei).\nEmpfehlung: HISTFILESIZE immer >= HISTSIZE setzen.",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "!! = letzter Befehl | !42 = Befehl #42 | HISTCONTROL=ignoreboth | Ctrl+R = Suche",
        memory_tip   = "HISTSIZE = Memory-Zeilen | HISTFILESIZE = Datei-Zeilen | immer HISTFILESIZE > HISTSIZE",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.06 — PS1-Prompt & Terminal-Anpassung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.06",
        chapter      = 17,
        title        = "PS1-Prompt & Terminal-Anpassung",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Ein Operator ohne angepassten Prompt\n"
            " ist wie ein Pilot ohne Cockpit-Display.\n"
            " PS1 zeigt dir wer, wo und was du bist.\n"
            " Konfiguriere deinen Prompt — es ist deine Signatur.'"
        ),
        why_important = (
            "PS1 definiert das Aussehen des Shell-Prompts.\n"
            "Ein gut konfigurierter Prompt zeigt User, Host, Pfad und\n"
            "Git-Status — reduziert Fehler durch fehlende Kontext-Info."
        ),
        explanation  = (
            "PS1-Sonderzeichen:\n"
            "  \\u  = Benutzername\n"
            "  \\h  = Hostname (kurz)\n"
            "  \\H  = Hostname (vollständig)\n"
            "  \\w  = Aktuelles Verzeichnis (vollständig)\n"
            "  \\W  = Aktuelles Verzeichnis (nur letztes Element)\n"
            "  \\$  = $ für User, # für root\n"
            "  \\d  = Datum (Wed Jan 15)\n"
            "  \\t  = Uhrzeit (12:34:56)\n"
            "  \\n  = Newline\n"
            "  \\[  \\]  = Nicht-druckbare Zeichen einschließen (ANSI-Farben)\n"
            "\n"
            "Beispiel-Prompts:\n"
            "  PS1='\\u@\\h:\\w\\$ '      → ghost@neongrid:~/src$ \n"
            "  PS1='\\[\\033[1;32m\\]\\u@\\h\\[\\033[0m\\]:\\w\\$ '\n"
            "                          → Grüner User@Host\n"
            "\n"
            "Weitere PS-Variablen:\n"
            "  PS2  = Fortsetzungsprompt (Standard: '>')\n"
            "  PS3  = Prompt für select-Anweisung\n"
            "  PS4  = Debug-Prompt (Standard: '+')\n"
            "\n"
            "TERM-Variable:\n"
            "  echo $TERM           → Aktueller Terminal-Typ\n"
            "  tput colors          → Unterstützte Farben\n"
            "  tput clear           → Terminal leeren (wie clear)\n"
            "  tput setaf 2         → Grüne Vordergrundfarbe\n"
            "  reset                → Terminal zurücksetzen"
        ),
        syntax       = "echo $PS1",
        example      = "PS1='\\[\\033[1;32m\\]\\u@\\h\\[\\033[0m\\]:\\w\\$ '",
        task_description = "Zeige den aktuellen PS1-Prompt an.",
        expected_commands = ["echo $PS1"],
        hint_text    = "$PS1 enthält die Prompt-Definition der aktuellen Shell",
        quiz_questions = [
            QuizQuestion(
                question    = "Was zeigt '\\u@\\h:\\w\\$' als PS1-Prompt?",
                options     = ["IP@Hostname:Pfad$", "Benutzername@Hostname:Pfad$", "UID@PID:Verzeichnis$", "User@Domain:Root#"],
                correct     = 1,
                explanation = "\\u=Benutzername | \\h=Hostname (kurz) | \\w=aktuelles Verzeichnis | \\$=$ für user, # für root.\nBeispiel: ghost@neongrid:~/src$",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welche PS-Variable ist der Fortsetzungsprompt (wenn ein Befehl fortgesetzt wird)?",
                options     = ["PS1", "PS2", "PS3", "PS4"],
                correct     = 1,
                explanation = "PS2 = Fortsetzungsprompt (Standard: '>') — erscheint wenn ein Befehl über mehrere Zeilen geht.\nPS1 = Haupt-Prompt | PS3 = select-Prompt | PS4 = Debug-Prompt (bash -x).",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Wie umschließt man ANSI-Farbcodes in PS1 korrekt?",
                options     = ["Mit einfachen Anführungszeichen: '\\033[1;32m'", "Mit \\[ und \\]: \\[\\033[1;32m\\]", "Mit Backslash: \\\\033[1;32m", "ANSI-Codes brauchen keine Umschließung in PS1"],
                correct     = 1,
                explanation = "\\[ und \\] umschließen nicht-druckbare Zeichen (wie ANSI-Codes) in PS1.\nOhne \\[...\\]: Bash berechnet Prompt-Breite falsch → kaputte Zeilenumbrüche!",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "\\u=User \\h=Host \\w=Pfad \\$=$ oder # | PS2=Fortsetzungsprompt",
        memory_tip   = "PS1 = Primary prompt | PS2 = Secondary (Fortsetzung) | PS4 = Debug (bash -x)",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.07 — QUIZ: Shell Environment
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.07",
        chapter      = 17,
        title        = "QUIZ — Shell Environment",
        mtype        = "QUIZ",
        xp           = 120,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM: 'SHELL-UMGEBUNG AUDIT.\n"
            " Startup-Dateien, PATH, Aliases, History —\n"
            " die unsichtbaren Schichten unter jedem Linux-Terminal.\n"
            " Beweise, dass du sie kennst.'"
        ),
        why_important = "LPIC-1 Topic 105.1 — Shell-Umgebung & Anpassung",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "Beantworte 5 Fragen zur Shell-Umgebung.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Startup-Datei wird bei einer interaktiven Non-Login-Shell gelesen?",
                options  = [
                    "~/.bash_profile",
                    "~/.profile",
                    "~/.bashrc",
                    "/etc/profile",
                ],
                correct  = 2,
                explanation = (
                    "Eine interaktive Non-Login-Shell (z.B. neues Terminal-Fenster) liest ~/.bashrc.\n"
                    "Login-Shells lesen /etc/profile und dann ~/.bash_profile oder ~/.profile.\n"
                    "Deshalb: ~/.bashrc für Aliases/Prompt, ~/.profile für Umgebungsvariablen."
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen 'VAR=wert' und 'export VAR=wert'?",
                options  = [
                    "Kein Unterschied — beide sind identisch",
                    "export macht die Variable für Kind-Prozesse sichtbar",
                    "VAR=wert gilt systemweit, export nur für die aktuelle Shell",
                    "export schreibt die Variable in ~/.bashrc",
                ],
                correct  = 1,
                explanation = (
                    "VAR=wert = Shell-Variable (nur in aktueller Shell).\n"
                    "export VAR = Umgebungsvariable (wird an Kind-Prozesse vererbt).\n"
                    "Kind-Prozesse erben exportierte Variablen, aber Änderungen\n"
                    "in Kind-Prozessen wirken sich nicht auf die Eltern-Shell aus."
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt an, ob 'll' ein Alias, eine Funktion oder ein Binary ist?",
                options  = [
                    "which ll",
                    "locate ll",
                    "type ll",
                    "find ll",
                ],
                correct  = 2,
                explanation = (
                    "type ll gibt aus: 'll is aliased to ls -la --color=auto'\n"
                    "type -a ll zeigt ALLE Treffer (Alias UND Binary wenn vorhanden).\n"
                    "which findet nur Binaries im PATH, keine Aliases oder Builtins."
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Was bewirkt 'HISTCONTROL=ignoreboth'?",
                options  = [
                    "History wird komplett deaktiviert",
                    "Befehle mit Leerzeichen am Anfang und Duplikate werden nicht gespeichert",
                    "Nur die letzten 2 Befehle werden gespeichert",
                    "History-Datei wird verschlüsselt",
                ],
                correct  = 1,
                explanation = (
                    "ignoreboth = ignoredups + ignorespace:\n"
                    "  ignoredups: Keine Duplikate (gleicher Befehl wie vorheriger)\n"
                    "  ignorespace: Befehle die mit Leerzeichen beginnen werden nicht gespeichert\n"
                    "Nützlich: ' geheimbefehl' (mit Leerzeichen) landet nicht in History."
                ),
                xp_value = 24,
            ),
            QuizQuestion(
                question = "Was zeigt '\\w' im PS1-Prompt an?",
                options  = [
                    "Den Benutzernamen",
                    "Den Wochentag",
                    "Das aktuelle Verzeichnis (vollständiger Pfad)",
                    "Die Anzahl der laufenden Jobs",
                ],
                correct  = 2,
                explanation = (
                    "\\w = aktuelles Verzeichnis (vollständiger Pfad, ~ statt /home/user).\n"
                    "\\W = nur letztes Verzeichniselement (kein vollständiger Pfad).\n"
                    "\\u = User | \\h = Hostname | \\$ = $ oder # je nach UID."
                ),
                xp_value = 24,
            ),
        ],
        exam_tip     = ".bashrc=Non-Login | .profile=Login | export=Vererbung | type=was-ist-es | \\w=Pfad in PS1",
        memory_tip   = "Shell-Startup: Login liest profile, Non-Login liest rc (resource configuration)",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.08–17.16 — Shell-Erweiterung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.08",
        chapter      = 17,
        title        = "Shell-Optionen — shopt & set -o",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'Bash hat versteckte Optionen die deine Shell transformieren.\n shopt, set -o — kenn sie, beherrsche sie.'",
        why_important = "Shell-Optionen steuern Verhalten wie Fehlerbehandlung, Globbing, History.\nLPIC-1 prüft set und shopt.",
        explanation  = (
            "set-Optionen:\n"
            "  set -e       → Skript bei Fehler beenden (errexit)\n"
            "  set -u       → Ungesetzte Variablen als Fehler\n"
            "  set -x       → Befehle anzeigen vor Ausführung (debug)\n"
            "  set -o pipefail → Fehler in Pipelines propagieren\n"
            "  set -o       → Alle Optionen anzeigen\n"
            "  set +e       → Option deaktivieren\n"
            "\n"
            "shopt-Optionen:\n"
            "  shopt -s extglob    → Erweiterte Glob-Patterns\n"
            "  shopt -s nullglob   → Kein Match → leerer String\n"
            "  shopt -s dotglob    → Glob matcht auch .Dateien\n"
            "  shopt -s histappend → History anhängen statt überschreiben\n"
            "  shopt               → Alle Optionen anzeigen\n"
            "  shopt -u extglob    → Option deaktivieren"
        ),
        syntax       = "shopt -s extglob && set -o",
        example      = "set -e; echo 'Fehler stoppen Script'",
        task_description = "Zeige alle aktuellen shopt-Optionen an.",
        expected_commands = ["shopt"],
        hint_text    = "shopt zeigt alle Optionen — shopt -s aktiviert, shopt -u deaktiviert",
        quiz_questions = [
            QuizQuestion(
                question    = "Was bewirkt 'set -e'?",
                options     = ["Skript debuggen", "Skript bei Fehler beenden", "Umgebung anzeigen", "Fehler ignorieren"],
                correct     = 1,
                explanation = "set -e (errexit) beendet das Skript wenn ein Befehl fehlschlägt.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welche shopt-Option lässt Glob auch .Dateien matchen?",
                options     = ["shopt -s hiddenglob", "shopt -s dotglob", "shopt -s allglob", "shopt -s starglob"],
                correct     = 1,
                explanation = "shopt -s dotglob lässt * auch Dateien beginnend mit . matchen.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "set -e=errexit | set -u=nounset | set -x=xtrace | shopt -s=set | shopt -u=unset",
        memory_tip   = "set -eux = die magische Debugger-Combo für Bash-Skripte",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "17.09",
        chapter      = 17,
        title        = "Prompt Customization — PS1, PS2, Farben",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = "Phantom: 'Dein Prompt ist deine Identität im Terminal.\n Ein guter Prompt zeigt User, Host, Pfad — und warnt bei root.\n Forme ihn nach deinem Willen.'",
        why_important = "PS1-Konfiguration ist LPIC-1 Thema. Escape-Sequenzen kennen.",
        explanation  = (
            "PS1 — Primärer Prompt:\n"
            "  \\u  → Username\n"
            "  \\h  → Hostname (kurz)\n"
            "  \\H  → Hostname (voll)\n"
            "  \\w  → Aktuelles Verzeichnis (voll)\n"
            "  \\W  → Aktuelles Verzeichnis (nur letztes)\n"
            "  \\$  → $ für User, # für root\n"
            "  \\n  → Newline\n"
            "  \\t  → Uhrzeit HH:MM:SS\n"
            "\n"
            "Farben im Prompt:\n"
            "  \\e[31m  → Rot\n"
            "  \\e[32m  → Grün\n"
            "  \\e[0m   → Reset\n"
            "  \\[ \\]   → Nicht-druckbare Zeichen einschließen!\n"
            "\n"
            "Beispiel:\n"
            "  PS1='\\[\\e[32m\\]\\u@\\h\\[\\e[0m\\]:\\w\\$ '\n"
            "\n"
            "PS2 — Sekundärer Prompt (Fortsetzung):\n"
            "  PS2='> '   → Standard, erscheint bei mehrzeiligen Eingaben"
        ),
        syntax       = "PS1='\\u@\\h:\\w\\$ '",
        example      = "export PS1='\\[\\e[32m\\]\\u@\\h\\[\\e[0m\\]:\\w\\$ '",
        task_description = "Setze PS1 auf 'user@host:path$ ' Format.",
        expected_commands = ["PS1='\\u@\\h:\\w\\$ '", "export PS1"],
        hint_text    = "PS1='\\u@\\h:\\w\\$ ' — \\u=user, \\h=host, \\w=path, \\$=Zeichen",
        quiz_questions = [
            QuizQuestion(
                question    = "Was zeigt \\w in PS1?",
                options     = ["Windows-Pfad", "Aktuelles Verzeichnis (voll)", "Hostname", "Username"],
                correct     = 1,
                explanation = "\\w zeigt das aktuelle Arbeitsverzeichnis vollständig.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Warum muss man Farb-Codes in \\[ \\] einschließen?",
                options     = ["Sicherheit", "Damit Bash die Länge korrekt berechnet", "Pflicht bei PS1", "Zum Escapen"],
                correct     = 1,
                explanation = "\\[ \\] markiert nicht-druckbare Zeichen — Bash berechnet sonst die Prompt-Länge falsch.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "\\u=user \\h=host \\w=workdir \\$=Zeichen | \\[ \\]=nicht-druckbar | PS2=Sekundärprompt",
        memory_tip   = "PS1 = Prompt String 1 | PS2 = Continuation prompt | \\[\\e[0m\\] = Reset-Farbe",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "17.10",
        chapter      = 17,
        title        = "Shell-Funktionen — declare, export -f",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'Funktionen sind deine wiederverwendbaren Waffen.\n Aber sie leben nur in der Shell. export -f macht sie vererbbar.\n declare -f zeigt sie. Lern den Unterschied.'",
        why_important = "Shell-Funktionen und declare gehören zu LPIC-1 Topic 105.1.",
        explanation  = (
            "Funktionen definieren:\n"
            "  function gruesse() { echo 'Hallo $1'; }\n"
            "  gruesse() { echo 'Hallo $1'; }  # Kurzform\n"
            "\n"
            "Funktionen verwalten:\n"
            "  declare -f         → Alle Funktionen anzeigen\n"
            "  declare -f name    → Bestimmte Funktion\n"
            "  declare -F         → Nur Funktionsnamen\n"
            "  unset -f name      → Funktion löschen\n"
            "\n"
            "Funktionen exportieren:\n"
            "  export -f gruesse  → Funktion an Kind-Prozesse vererben\n"
            "  bash -c 'gruesse'  → In Kind-Shell verfügbar?\n"
            "\n"
            "Lokale Variablen:\n"
            "  function test() {\n"
            "    local x=10    # Nur in dieser Funktion\n"
            "    echo $x\n"
            "  }"
        ),
        syntax       = "declare -f && export -f funktionsname",
        example      = "gruesse() { echo \"Hallo $1\"; }; declare -f gruesse",
        task_description = "Zeige alle definierten Shell-Funktionen an.",
        expected_commands = ["declare -f", "declare -F"],
        hint_text    = "declare -f zeigt alle Funktionen mit Inhalt, declare -F nur Namen",
        quiz_questions = [
            QuizQuestion(
                question    = "Welcher Befehl zeigt alle Shell-Funktionen an?",
                options     = ["functions -l", "declare -f", "set -f", "show functions"],
                correct     = 1,
                explanation = "declare -f zeigt alle definierten Funktionen mit ihrem Inhalt.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Wie wird eine Funktion an Kind-Prozesse vererbt?",
                options     = ["source funktion", "export -f funktion", "declare -x funktion", "inherit funktion"],
                correct     = 1,
                explanation = "export -f exportiert Funktionen in die Umgebung für Kind-Prozesse.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "declare -f = anzeigen | declare -F = nur Namen | export -f = exportieren | local = lokale Variable",
        memory_tip   = "declare = deklarieren: -f=Funktion -F=Funktion-Name -i=Integer -r=readonly -x=export",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "17.11",
        chapter      = 17,
        title        = "POSIX vs Bash — Portable Shell-Skripte",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "RUST",
        story        = "Rust: 'Ich hab Skripte die seit 20 Jahren laufen.\n Nicht weil sie modern sind — weil sie POSIX-kompatibel sind.\n #!/bin/sh vs #!/bin/bash — kenn den Unterschied.'",
        why_important = "POSIX-Kompatibilität ist wichtig für portierbare Skripte.\nLPIC-1 prüft sh vs bash Unterschiede.",
        explanation  = (
            "POSIX Shell (sh):\n"
            "  #!/bin/sh                → Portierbar\n"
            "  Unterstützt: if, for, while, case, functions\n"
            "  KEIN: [[ ]], arrays, (( )), select, process substitution\n"
            "\n"
            "Bashisms (nur in bash):\n"
            "  [[ ]] statt [ ]          → Erweiterte Bedingungen\n"
            "  (( )) statt expr         → Arithmetik\n"
            "  Arrays: arr=(1 2 3)\n"
            "  ${var,,} ${var^^}        → Groß/Kleinschreibung\n"
            "  <<<heredoc               → Herestring\n"
            "  {1..10}                  → Brace expansion\n"
            "\n"
            "sh vs bash:\n"
            "  /bin/sh kann bash sein (auf Ubuntu/Debian = dash)\n"
            "  dash ist schneller aber weniger features als bash\n"
            "\n"
            "Portierbarkeit prüfen:\n"
            "  checkbashisms skript.sh  → Prüft auf Bashisms\n"
            "  dash skript.sh           → Skript in POSIX sh testen"
        ),
        syntax       = "#!/bin/sh vs #!/bin/bash",
        example      = "ls -la /bin/sh && dash --version 2>/dev/null",
        task_description = "Zeige wohin /bin/sh zeigt.",
        expected_commands = ["ls -la /bin/sh"],
        hint_text    = "ls -la /bin/sh zeigt ob sh zu bash, dash oder sh zeigt",
        quiz_questions = [
            QuizQuestion(
                question    = "Welches Feature ist ein 'Bashism' (nicht POSIX)?",
                options     = ["if [ $a -eq 1 ]", "for i in 1 2 3", "[[ $a == b ]]", "while read line"],
                correct     = 2,
                explanation = "[[ ]] ist ein Bashism und nicht POSIX-kompatibel. [ ] ist POSIX.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist /bin/sh auf modernen Debian/Ubuntu-Systemen?",
                options     = ["bash", "zsh", "dash", "ksh"],
                correct     = 2,
                explanation = "Auf Debian/Ubuntu zeigt /bin/sh auf dash (schnelle POSIX-Shell).",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "[[ ]] = Bashism | [ ] = POSIX | /bin/sh = oft dash auf Debian | #!/bin/sh = portierbar",
        memory_tip   = "POSIX sh = Basis-Shell überall | bash = erweitert | dash = schnell+POSIX",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "17.12",
        chapter      = 17,
        title        = "History & HISTCONTROL — Befehlshistorie",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'In NeonGrid-9 hinterlässt jeder Befehl Spuren.\n History ist Macht — und Risiko.\n HISTCONTROL steuert was gespeichert wird.'",
        why_important = "History-Kontrolle verhindert versehentlich gespeicherte Passwörter.\nLPIC-1 prüft HISTFILE, HISTSIZE, HISTCONTROL.",
        explanation  = (
            "History-Variablen:\n"
            "  HISTFILE=~/.bash_history   → Wo History gespeichert wird\n"
            "  HISTSIZE=1000              → Anzahl Einträge im RAM\n"
            "  HISTFILESIZE=2000          → Anzahl Einträge in Datei\n"
            "  HISTCONTROL=ignoredups     → Duplikate ignorieren\n"
            "  HISTCONTROL=ignorespace    → Mit Leerzeichen beginnend ignorieren\n"
            "  HISTCONTROL=ignoreboth     → Beides\n"
            "\n"
            "History bedienen:\n"
            "  history                    → History anzeigen\n"
            "  history 10                 → Letzte 10\n"
            "  !123                       → Befehl Nr. 123 wiederholen\n"
            "  !!                         → Letzten Befehl wiederholen\n"
            "  !string                    → Letzten Befehl mit 'string'\n"
            "  Ctrl+R                     → Rückwärtssuche\n"
            "\n"
            "History löschen:\n"
            "  history -c                 → History im RAM löschen\n"
            "  history -d 100             → Eintrag 100 löschen\n"
            "  > ~/.bash_history          → Datei leeren\n"
            "  unset HISTFILE             → Nicht speichern"
        ),
        syntax       = "history 20",
        example      = "export HISTCONTROL=ignoreboth && history -c",
        task_description = "Zeige die letzten 10 History-Einträge an.",
        expected_commands = ["history 10", "history"],
        hint_text    = "history 10 zeigt die letzten 10 Befehle",
        quiz_questions = [
            QuizQuestion(
                question    = "Was bewirkt HISTCONTROL=ignorespace?",
                options     = ["Leerzeilen ignorieren", "Befehle mit Leerzeichen am Anfang ignorieren", "Duplikate ignorieren", "History deaktivieren"],
                correct     = 1,
                explanation = "HISTCONTROL=ignorespace: Befehle die mit Leerzeichen beginnen werden nicht gespeichert.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welche Variable bestimmt die History-Dateigröße?",
                options     = ["HISTSIZE", "HISTMAX", "HISTFILESIZE", "HISTLENGTH"],
                correct     = 2,
                explanation = "HISTFILESIZE = Anzahl der Einträge die in ~/.bash_history gespeichert werden.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "HISTSIZE=RAM | HISTFILESIZE=Datei | HISTCONTROL=ignoreboth | history -c=löschen",
        memory_tip   = "HIST = Historiker: Size=Köpfe im Gedächtnis, FileSize=Archiv, Control=Zensur",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "17.13",
        chapter      = 17,
        title        = "Tab-Completion & bash-completion",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'Tab-Completion ist keine Bequemlichkeit — es ist Geschwindigkeit.\n bash-completion kennt apt, git, systemctl.\n Installiere es. Lern es. Benutze es.'",
        why_important = "bash-completion ist Standard auf modernen Systemen. LPIC-1 kennt complete.",
        explanation  = (
            "Basis-Completion (eingebaut):\n"
            "  Tab         → Befehle, Dateien, Variablen vervollständigen\n"
            "  Tab Tab     → Alle Möglichkeiten anzeigen\n"
            "\n"
            "bash-completion Paket:\n"
            "  apt install bash-completion\n"
            "  /etc/bash_completion             → Hauptdatei\n"
            "  /etc/bash_completion.d/          → Ergänzungen pro Tool\n"
            "  ~/.bash_completion               → User-eigene Completions\n"
            "\n"
            "Aktivierung in ~/.bashrc:\n"
            "  if [ -f /etc/bash_completion ]; then\n"
            "    . /etc/bash_completion\n"
            "  fi\n"
            "\n"
            "Eigene Completions (complete):\n"
            "  complete -W 'start stop restart' myservice\n"
            "  complete -f skript.sh   → Dateipfad-Completion\n"
            "  compgen -c              → Alle Befehle auflisten"
        ),
        syntax       = "complete -W 'start stop restart' myservice",
        example      = "compgen -c | grep '^sys' | head -5",
        task_description = "Zeige alle verfügbaren Completions für 'sys' an.",
        expected_commands = ["compgen -c", "complete"],
        hint_text    = "compgen -c zeigt alle Befehle — complete zeigt Completion-Regeln",
        quiz_questions = [
            QuizQuestion(
                question    = "Wo liegt die Hauptdatei von bash-completion?",
                options     = ["/usr/share/bash-completion", "/etc/bash_completion", "/etc/bash_completion.d/bash", "~/.bash_completion"],
                correct     = 1,
                explanation = "/etc/bash_completion ist die Hauptdatei des bash-completion Pakets.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was macht 'compgen -c'?",
                options     = ["Completion generieren", "Alle verfügbaren Befehle auflisten", "Completion aktivieren", "Completion-Cache leeren"],
                correct     = 1,
                explanation = "compgen -c listet alle verfügbaren Befehle auf (wie Tab-Completion).",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "/etc/bash_completion | /etc/bash_completion.d/ | complete -W = Wort-Liste | compgen -c = Befehle",
        memory_tip   = "compgen = completion generator | complete = Completion-Regel definieren",
        gear_reward  = None,
        faction_reward = ("Root Collective", 8),
    ),

    Mission(
        mission_id   = "17.14",
        chapter      = 17,
        title        = "Umgebungsvariablen tief — env, printenv, set",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = "Zara Z3R0: 'Drei Befehle zeigen Variablen. Aber sie sind NICHT gleich.\n env, printenv, set — jeder zeigt andere Dinge.\n Kenn den Unterschied oder verlier dich im Rauschen.'",
        why_important = "Variablen und Umgebung sind LPIC-1 Core Topic 105.1.",
        explanation  = (
            "env:\n"
            "  env                → Alle exportierten Umgebungsvariablen\n"
            "  env -i bash        → Shell ohne Umgebung starten\n"
            "  env VAR=wert cmd   → Variablen nur für diesen Befehl setzen\n"
            "\n"
            "printenv:\n"
            "  printenv           → Alle Umgebungsvariablen (wie env)\n"
            "  printenv HOME      → Bestimmte Variable\n"
            "  printenv PATH LANG → Mehrere Variablen\n"
            "\n"
            "set:\n"
            "  set                → ALLE Variablen + Shell-Variablen + Funktionen\n"
            "  set | grep PATH    → Filtern\n"
            "\n"
            "Unterschied:\n"
            "  env/printenv: nur exportierte (Umgebungs-) Variablen\n"
            "  set: alle Variablen inkl. lokale Shell-Variablen\n"
            "\n"
            "export:\n"
            "  export VAR=wert    → Setzen + exportieren\n"
            "  export -p          → Alle exportierten Variablen (declare -x)\n"
            "  unset VAR          → Variable löschen"
        ),
        syntax       = "env | grep PATH",
        example      = "printenv HOME LANG SHELL && set | grep HIST",
        task_description = "Zeige die aktuelle PATH-Variable mit printenv an.",
        expected_commands = ["printenv PATH", "printenv"],
        hint_text    = "printenv PATH zeigt nur PATH — env | grep PATH ebenfalls",
        quiz_questions = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'env' und 'set'?",
                options     = ["env ist neuer", "set zeigt auch lokale Shell-Variablen", "env zeigt mehr", "kein Unterschied"],
                correct     = 1,
                explanation = "set zeigt ALLE Variablen (inkl. lokale Shell-Variablen); env nur exportierte.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Wie startet man eine Shell ohne geerbte Umgebung?",
                options     = ["bash --clean", "env -i bash", "bash -e", "unset all && bash"],
                correct     = 1,
                explanation = "env -i startet einen Prozess mit komplett leerer Umgebung.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "env/printenv = exportierte Vars | set = alle Vars+Funktionen | export -p = exportierte mit declare -x",
        memory_tip   = "env = Environment (exportiert) | set = Sets alles (lokal+exportiert+Funktionen)",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "17.15",
        chapter      = 17,
        title        = "PATH & Befehlssuche — which, type, whereis",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "RUST",
        story        = "Rust: 'Befehl nicht gefunden. Aber du WEISST dass er installiert ist.\n PATH stimmt nicht. Oder es ist ein Alias. Oder eine Funktion.\n type sagt dir die Wahrheit.'",
        why_important = "PATH-Verwaltung und Befehlsauflösung sind LPIC-1 Core Topic.",
        explanation  = (
            "PATH erweitern:\n"
            "  export PATH=$PATH:/opt/bin     → Hinzufügen\n"
            "  export PATH=/opt/bin:$PATH     → Vorne hinzufügen\n"
            "  echo $PATH | tr ':' '\\n'       → Übersichtlich anzeigen\n"
            "\n"
            "Befehl finden:\n"
            "  which ls          → Pfad des Befehls (nur in PATH)\n"
            "  type ls           → Was ist ls? (Alias, Funktion, Builtin, Datei)\n"
            "  whereis ls        → Binär, Source, Man-Page Pfade\n"
            "  command -v ls     → POSIX-kompatibel (wie which)\n"
            "\n"
            "type Ausgaben:\n"
            "  ls is /bin/ls               → Externes Binary\n"
            "  cd is a shell builtin       → Shell-Eingebaut\n"
            "  ll is aliased to 'ls -la'   → Alias\n"
            "  myfunc is a function        → Funktion\n"
            "\n"
            "hash:\n"
            "  hash                        → Cache gefundener Befehle\n"
            "  hash -r                     → Cache löschen\n"
            "  hash -d ls                  → ls aus Cache entfernen"
        ),
        syntax       = "type ls && which python3",
        example      = "echo $PATH | tr ':' '\\n' && type cd ls ll",
        task_description = "Finde heraus was 'ls' ist (Alias, Builtin oder Datei).",
        expected_commands = ["type ls", "which ls"],
        hint_text    = "type ls zeigt ob ls ein Alias, Builtin oder externes Programm ist",
        quiz_questions = [
            QuizQuestion(
                question    = "Was zeigt 'type cd'?",
                options     = ["Pfad von cd", "cd is a shell builtin", "cd ist nicht gefunden", "cd Version"],
                correct     = 1,
                explanation = "cd ist ein Shell-Builtin — kein externes Programm. type zeigt das.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was macht 'hash -r'?",
                options     = ["Hash-Wert berechnen", "Befehlspfad-Cache leeren", "PATH zurücksetzen", "History resetten"],
                correct     = 1,
                explanation = "hash -r leert den Cache der gefundenen Befehlspfade.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "which = Pfad | type = was ist es | whereis = alles | command -v = POSIX | hash = Cache",
        memory_tip   = "type alles: type cd = builtin, type ls = file, type ll = alias",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.16 — readline & inputrc
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.16",
        chapter      = 17,
        title        = "readline & inputrc — Terminal-Tastaturkonfiguration",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Dein Terminal ist langsam, Ghost.\n"
            " readline steuert jeden Tastendruck.\n"
            " /etc/inputrc und ~/.inputrc — dein Konfigurations-Arsenal.\n"
            " bind -l zeigt alle verfügbaren Aktionen.'"
        ),
        why_important = (
            "readline ist LPIC-1 Topic 105.1 Prüfungsstoff.\n"
            "Shell-Konfiguration gehört zu Shell Environment (105.1).\n"
            "bind und inputrc ermöglichen produktivere Terminal-Arbeit."
        ),
        explanation  = (
            "READLINE — GNU READLINE LIBRARY:\n\n"
            "Readline steuert die Eingabe in bash und anderen Tools.\n\n"
            "/ETC/INPUTRC & ~/.INPUTRC:\n"
            "  set editing-mode vi        vi-Tastenbelegung\n"
            "  set editing-mode emacs     emacs-Tastenbelegung (Standard)\n"
            "  set completion-ignore-case on  Case-insensitive Tab-Completion\n"
            "  set show-all-if-ambiguous on   alle Optionen sofort zeigen\n"
            "  set colored-stats on           farbige Completion\n"
            "  \"\\e[A\": history-search-backward  Pfeiltaste hoch = History-Suche\n\n"
            "BIND BEFEHLE:\n"
            "  bind -l              alle readline-Funktionen auflisten\n"
            "  bind -P              alle Tastenbindungen anzeigen\n"
            "  bind -x '\"\\C-l\": clear'  Ctrl+L = clear binden\n"
            "  bind '\"\\e[A\": history-search-backward'  temporär binden\n\n"
            "WICHTIGE READLINE-SHORTCUTS:\n"
            "  Ctrl+A   Zeilenanfang\n"
            "  Ctrl+E   Zeilenende\n"
            "  Ctrl+R   History reverse-search\n"
            "  Ctrl+U   Zeile löschen\n"
            "  Alt+.    letztes Argument einfügen"
        ),
        syntax       = "bind [OPTIONS]  |  ~/.inputrc",
        example      = (
            "bind -l                          # alle readline-Funktionen\n"
            "bind -P                          # aktuelle Tastenbindungen\n"
            "bind '\"\\e[A\": history-search-backward'  # Pfeil hoch\n"
            "cat /etc/inputrc                 # System-Konfiguration\n"
            "echo 'set completion-ignore-case on' >> ~/.inputrc"
        ),
        task_description = "Liste alle verfügbaren readline-Funktionen auf",
        expected_commands = ["bind -l"],
        hint_text    = "bind -l listet alle readline-Funktionen die gebunden werden können",
        quiz_questions = [
            QuizQuestion(
                question   = "Welche Datei konfiguriert readline systemweit?",
                options    = [
                    "~/.bashrc",
                    "/etc/inputrc",
                    "/etc/readline.conf",
                    "~/.readline",
                ],
                correct    = 1,
                explanation = (
                    "/etc/inputrc = systemweite readline-Konfiguration.\n"
                    "~/.inputrc = benutzerspezifisch (überschreibt /etc/inputrc).\n"
                    "bind -l = zeigt alle verfügbaren readline-Funktionen."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welcher bind-Befehl zeigt alle aktuellen Tastenbindungen?",
                options    = [
                    "bind -l",
                    "bind -P",
                    "bind --list",
                    "bind -a",
                ],
                correct    = 1,
                explanation = (
                    "bind -P zeigt alle aktuellen Tastenbindungen mit Funktionsnamen.\n"
                    "bind -l listet nur die verfügbaren Funktionsnamen.\n"
                    "bind -x zeigt Tastenbindungen an Shell-Befehle."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 readline:\n"
            "  /etc/inputrc = systemweit\n"
            "  ~/.inputrc = benutzerspezifisch\n"
            "  bind -l = alle Funktionen\n"
            "  bind -P = aktuelle Bindungen\n"
            "  set editing-mode vi|emacs"
        ),
        memory_tip   = "inputrc = Input-Readline-Config. bind -l = list, bind -P = Print bindings",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.17 — PROMPT_COMMAND & dynamischer Prompt
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.17",
        chapter      = 17,
        title        = "PROMPT_COMMAND & dynamischer Prompt",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'PS1 ist statisch — aber PROMPT_COMMAND läuft\n"
            " vor jedem Prompt. Du kannst PS1 dynamisch setzen.\n"
            " Git-Branch, Exit-Code, Uhrzeit — alles in Echtzeit.\n"
            " Das ist ein lebendiger Prompt.'"
        ),
        why_important = (
            "PROMPT_COMMAND und dynamische PS1-Funktionen sind fortgeschrittene\n"
            "Shell-Konfiguration die LPIC-1 Topic 105.1 abdeckt.\n"
            "Ermöglicht kontextbewusste Prompts für Sysadmins."
        ),
        explanation  = (
            "PROMPT_COMMAND:\n"
            "  PROMPT_COMMAND='echo -n \"[$(date +%T)] \"'\n"
            "                            → Vor jedem Prompt ausführen\n"
            "  PROMPT_COMMAND='history -a'  → History nach jedem Befehl schreiben\n"
            "  PROMPT_COMMAND='update_prompt'  → Funktion aufrufen\n\n"
            "DYNAMISCHE PS1 MIT FUNKTION:\n"
            "  update_prompt() {\n"
            "    local exit_code=$?\n"
            "    local color=32  # grün\n"
            "    [ $exit_code -ne 0 ] && color=31  # rot bei Fehler\n"
            "    PS1=\"\\[\\e[${color}m\\]\\u@\\h:\\w\\[\\e[0m\\]\\$ \"\n"
            "  }\n"
            "  PROMPT_COMMAND='update_prompt'\n\n"
            "GIT-BRANCH IN PROMPT:\n"
            "  git_branch() {\n"
            "    git branch 2>/dev/null | grep '^*' | cut -d' ' -f2\n"
            "  }\n"
            "  PS1='\\u@\\h:\\w $(git_branch)\\$ '\n\n"
            "EXIT-CODE IM PROMPT:\n"
            "  PS1='\\u@\\h:\\w [\\$?]\\$ '  → zeigt letzten Exit-Code\n\n"
            "PRECMD (zsh-Äquivalent):\n"
            "  In zsh: precmd() { ... }  → wird vor jedem Prompt ausgeführt"
        ),
        syntax       = "PROMPT_COMMAND='befehl'",
        example      = (
            "PROMPT_COMMAND='echo -n \"[$(date +%T)] \"'\n"
            "PROMPT_COMMAND='history -a'   # History sofort schreiben\n"
            "PS1='\\u@\\h:\\w [\\$?]\\$ '  # Exit-Code im Prompt"
        ),
        task_description = "Setze PROMPT_COMMAND so dass die Zeit vor jedem Prompt erscheint.",
        expected_commands = ["PROMPT_COMMAND='echo -n \"[$(date +%T)] \"'", "export PROMPT_COMMAND"],
        hint_text    = "PROMPT_COMMAND wird vor jedem neuen Prompt ausgeführt",
        quiz_questions = [
            QuizQuestion(
                question   = "Wann wird PROMPT_COMMAND ausgeführt?",
                options    = [
                    "Beim Login der Shell",
                    "Vor jedem Anzeigen des Prompts",
                    "Nach jedem Befehl, synchron",
                    "Nur wenn PS1 sich ändert",
                ],
                correct    = 1,
                explanation = (
                    "PROMPT_COMMAND wird unmittelbar vor dem Anzeigen des Prompts ausgeführt.\n"
                    "Typische Nutzung: history -a (History sofort schreiben),\n"
                    "oder Funktionen zum dynamischen Aktualisieren von PS1."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie zeigt man den Exit-Code des letzten Befehls in PS1?",
                options    = [
                    "PS1='\\u@\\h:\\w [\\e?]\\$ '",
                    "PS1='\\u@\\h:\\w [\\$?]\\$ '",
                    "PS1='\\u@\\h:\\w [$EXIT]\\$ '",
                    "PS1='\\u@\\h:\\w [\\x]\\$ '",
                ],
                correct    = 1,
                explanation = (
                    "\\$? in PS1 zeigt den Exit-Code des zuletzt ausgeführten Befehls.\n"
                    "$? ist die spezielle Variable für den Exit-Code in bash.\n"
                    "0 = Erfolg, >0 = Fehler."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "PROMPT_COMMAND = vor jedem Prompt ausführen\n"
            "Typisch: history -a, dynamische PS1\n"
            "\\$? im Prompt = Exit-Code des letzten Befehls\n"
            "PROMPT_COMMAND kann Array sein (bash 5.1+)"
        ),
        memory_tip   = "PROMPT_COMMAND = Prompt-Vorbereitung | precmd = zsh-Äquivalent",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.18 — Shell-Builtins tief
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.18",
        chapter      = 17,
        title        = "Shell-Builtins tief — type, builtin, enable, help",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "Rust: 'echo ist überall. Aber WELCHES echo?\n"
            " Das Builtin oder /bin/echo?\n"
            " builtin echo erzwingt das eingebaute.\n"
            " enable -n echo deaktiviert es komplett.\n"
            " Kenn deine Shell von innen.'"
        ),
        why_important = (
            "Shell-Builtins sind Kernbestandteil von LPIC-1 Topic 105.1.\n"
            "type, builtin, enable und compgen -b sind prüfungsrelevant.\n"
            "Builtins laufen in der aktuellen Shell — kein Fork nötig."
        ),
        explanation  = (
            "SHELL-BUILTINS:\n"
            "  Builtins sind Befehle die direkt von der Shell ausgeführt werden.\n"
            "  Kein Fork, kein externes Programm. Schneller und können\n"
            "  die Shell-Umgebung direkt verändern (z.B. cd, export).\n\n"
            "TYPE — WAS IST EIN BEFEHL:\n"
            "  type echo         → 'echo is a shell builtin'\n"
            "  type ls           → 'ls is /bin/ls'\n"
            "  type ll           → 'll is aliased to ls -la'\n"
            "  type -t echo      → 'builtin' (nur Typ ausgeben)\n"
            "  type -a echo      → alle Treffer (builtin + external)\n\n"
            "BUILTIN — BUILTIN ERZWINGEN:\n"
            "  builtin echo test → Nur das Builtin echo aufrufen\n"
            "  builtin cd /tmp   → Auch wenn cd als Alias definiert ist\n\n"
            "ENABLE — BUILTINS AKTIVIEREN/DEAKTIVIEREN:\n"
            "  enable            → alle aktivierten Builtins\n"
            "  enable -n echo    → echo-Builtin deaktivieren\n"
            "  enable echo       → echo-Builtin wieder aktivieren\n"
            "  enable -a         → alle Builtins (auch deaktivierte)\n\n"
            "HELP — BUILTIN-DOKUMENTATION:\n"
            "  help              → alle Builtins auflisten\n"
            "  help cd           → Hilfe zu cd\n"
            "  help -d cd        → Kurzbeschreibung\n\n"
            "COMPGEN -B — BUILTINS AUFLISTEN:\n"
            "  compgen -b        → alle eingebauten Befehle\n"
            "  compgen -k        → alle Keywords (if, for, while...)"
        ),
        syntax       = "type -a befehl  |  builtin befehl  |  enable  |  compgen -b",
        example      = (
            "type -a echo               # alle echo-Varianten\n"
            "type -t ls                 # nur Typ: 'file'\n"
            "builtin echo 'kein Alias'  # Builtin erzwingen\n"
            "enable -n echo             # Builtin deaktivieren\n"
            "compgen -b                 # alle Builtins auflisten\n"
            "help cd                    # Builtin-Hilfe"
        ),
        task_description = "Zeige alle verfügbaren Shell-Builtins an.",
        expected_commands = ["compgen -b", "enable", "help"],
        hint_text    = "compgen -b listet alle eingebauten Shell-Befehle auf",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht 'builtin echo test'?",
                options    = [
                    "Ruft /bin/echo auf",
                    "Erzwingt das Shell-Builtin echo, ignoriert Aliases",
                    "Zeigt echo-Dokumentation",
                    "Deaktiviert das echo-Alias",
                ],
                correct    = 1,
                explanation = (
                    "builtin befehl erzwingt die Verwendung des Shell-Builtins,\n"
                    "auch wenn ein gleichnamiges Alias oder eine Funktion existiert.\n"
                    "Nützlich um Alias-Overrides zu umgehen."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welcher Befehl listet alle Shell-Builtins auf?",
                options    = [
                    "type -b",
                    "builtin -l",
                    "compgen -b",
                    "enable --list",
                ],
                correct    = 2,
                explanation = (
                    "compgen -b listet alle verfügbaren Shell-Builtins auf.\n"
                    "compgen -k listet Shell-Keywords (if, for, while).\n"
                    "enable ohne Argumente zeigt aktivierte Builtins."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Builtins:\n"
            "  type -t befehl = builtin|file|alias|function|keyword\n"
            "  builtin befehl = Builtin erzwingen\n"
            "  enable -n = deaktivieren\n"
            "  compgen -b = alle Builtins\n"
            "  help = Builtin-Dokumentation"
        ),
        memory_tip   = "type = Typ des Befehls | builtin = Builtin erzwingen | enable = an/aus | compgen -b = liste",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.19 — Bash-Arrays & assoziative Arrays
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.19",
        chapter      = 17,
        title        = "Bash-Arrays & assoziative Arrays — declare -a / -A",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Eine Variable, viele Werte — das ist ein Array.\n"
            " declare -a für normale Arrays, declare -A für assoziative.\n"
            " Server-Listen, Konfigurationspaare — Arrays machen das möglich.\n"
            " Bash kann das — du musst es nur kennen.'"
        ),
        why_important = (
            "Bash-Arrays sind ein mächtiges Werkzeug für Shell-Skripte.\n"
            "LPIC-1 Topic 105.2 umfasst Shell-Scripting inkl. Arrays.\n"
            "Assoziative Arrays (bash 4+) ermöglichen Key-Value-Strukturen."
        ),
        explanation  = (
            "INDIZIERTE ARRAYS (declare -a):\n"
            "  declare -a servers           → Array deklarieren\n"
            "  servers=(web1 web2 web3)     → Array initialisieren\n"
            "  servers[0]='web1'            → Element setzen\n"
            "  echo ${servers[0]}           → Element lesen\n"
            "  echo ${servers[@]}           → Alle Elemente\n"
            "  echo ${#servers[@]}          → Anzahl Elemente\n"
            "  echo ${!servers[@]}          → Alle Indizes\n"
            "  servers+=(web4)              → Element anhängen\n"
            "  unset servers[1]             → Element löschen\n"
            "  unset servers                → Array löschen\n\n"
            "ARRAY-ITERATION:\n"
            "  for server in \"${servers[@]}\"; do\n"
            "    echo \"Server: $server\"\n"
            "  done\n\n"
            "ASSOZIATIVE ARRAYS (declare -A, bash 4+):\n"
            "  declare -A config            → Assoz. Array\n"
            "  config[host]='localhost'\n"
            "  config[port]='8080'\n"
            "  echo ${config[host]}\n"
            "  echo ${!config[@]}           → Alle Schlüssel\n"
            "  echo ${config[@]}            → Alle Werte\n\n"
            "ARRAY SLICING:\n"
            "  echo ${servers[@]:1:2}       → Index 1, 2 Elemente\n"
            "  echo ${servers[@]: -1}       → Letztes Element"
        ),
        syntax       = "declare -a arr=(a b c)  |  declare -A map=([key]=val)",
        example      = (
            "declare -a servers=(web1 web2 web3)\n"
            "echo ${servers[@]}              # alle Elemente\n"
            "echo ${#servers[@]}             # Anzahl: 3\n"
            "declare -A config\n"
            "config[host]='localhost'\n"
            "config[port]='8080'\n"
            "echo ${!config[@]}              # Schlüssel: host port"
        ),
        task_description = "Erstelle ein Array mit 3 Server-Namen und zeige alle Elemente an.",
        expected_commands = ["declare -a", "echo ${servers[@]}", "declare -A"],
        hint_text    = "declare -a servers=(web1 web2 web3) && echo ${servers[@]}",
        quiz_questions = [
            QuizQuestion(
                question   = "Wie zeigt man alle Elemente eines Bash-Arrays?",
                options    = [
                    "echo $arr",
                    "echo ${arr[@]}",
                    "echo ${arr[*]}",
                    "print arr",
                ],
                correct    = 1,
                explanation = (
                    "${arr[@]} zeigt alle Elemente als separate Wörter (sicher für Spaces).\n"
                    "${arr[*]} zeigt alle als einen String (IFS-getrennt).\n"
                    "$arr zeigt nur das erste Element (arr[0])."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welcher declare-Flag erstellt ein assoziatives Array?",
                options    = [
                    "declare -a",
                    "declare -i",
                    "declare -A",
                    "declare -h",
                ],
                correct    = 2,
                explanation = (
                    "declare -A erstellt ein assoziatives Array (Key-Value, bash 4+).\n"
                    "declare -a erstellt ein indiziertes (numerisches) Array.\n"
                    "declare -i deklariert eine Integer-Variable."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Arrays:\n"
            "  declare -a = indiziertes Array\n"
            "  declare -A = assoziatives Array (bash 4+)\n"
            "  ${arr[@]} = alle Elemente\n"
            "  ${#arr[@]} = Anzahl\n"
            "  ${!arr[@]} = alle Indizes/Schlüssel"
        ),
        memory_tip   = "arr[@] = alle Items | #arr[@] = count | !arr[@] = Indizes | declare -A = Associative",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 12),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.20 — direnv & .envrc
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.20",
        chapter      = 17,
        title        = "direnv & .envrc — Verzeichnis-spezifische Umgebung",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Jedes Projekt braucht seine eigene Umgebung.\n"
            " NODE_ENV=production hier, API_KEY=test dort.\n"
            " direnv lädt .envrc automatisch beim cd.\n"
            " .env-Dateien, export-Patterns — sauber, isoliert, sicher.'"
        ),
        why_important = (
            "Verzeichnis-spezifische Umgebungsvariablen sind essentiell für\n"
            "moderne Entwicklung und Systemadministration.\n"
            "LPIC-1 Topic 105.1 umfasst Umgebungsvariablen-Management."
        ),
        explanation  = (
            "DIRENV — AUTOMATISCHE .envrc-LADUNG:\n"
            "  apt install direnv\n"
            "  eval \"$(direnv hook bash)\"  → In ~/.bashrc aktivieren\n"
            "  echo 'export API_KEY=test' > .envrc\n"
            "  direnv allow .              → .envrc vertrauen\n"
            "  direnv deny .               → .envrc blockieren\n"
            "  direnv reload               → .envrc neu laden\n\n"
            ".ENV-DATEIEN — EXPORT PATTERNS:\n"
            "  .env Datei Format:\n"
            "    # Kommentar\n"
            "    DATABASE_URL=postgres://localhost/mydb\n"
            "    API_KEY=geheim\n"
            "    DEBUG=true\n\n"
            ".env MANUELL LADEN:\n"
            "  export $(cat .env | grep -v '^#' | xargs)\n"
            "  source .env                 → falls .env nur exports enthält\n"
            "  set -a; source .env; set +a → alle Variablen auto-exportieren\n\n"
            "VERZEICHNIS-SPEZIFISCHE PATH:\n"
            "  # In .envrc:\n"
            "  PATH_add ./bin             → ./bin zu PATH hinzufügen\n"
            "  PATH_add node_modules/.bin → Lokal installierte Tools\n\n"
            "SICHERHEIT:\n"
            "  .envrc muss explizit mit 'direnv allow' vertraut werden\n"
            "  .env niemals in Git committen (.gitignore)\n"
            "  .env.example mit Platzhaltern committen"
        ),
        syntax       = "direnv allow .  |  export $(cat .env | grep -v '^#' | xargs)",
        example      = (
            "# .env laden ohne direnv:\n"
            "set -a; source .env; set +a\n"
            "# direnv Setup:\n"
            "eval \"$(direnv hook bash)\"\n"
            "echo 'export PROJECT=neongrid' > .envrc\n"
            "direnv allow ."
        ),
        task_description = "Lade eine .env-Datei manuell in die Shell-Umgebung.",
        expected_commands = ["set -a", "source .env", "export $(cat .env"],
        hint_text    = "set -a; source .env; set +a lädt alle Variablen aus .env und exportiert sie",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht 'set -a' vor 'source .env'?",
                options    = [
                    "Alle Aliase deaktivieren",
                    "Alle nachfolgend gesetzten Variablen automatisch exportieren",
                    "Datei im append-Modus öffnen",
                    "Shell im sicheren Modus starten",
                ],
                correct    = 1,
                explanation = (
                    "set -a (allexport) exportiert automatisch alle Variablen die\n"
                    "danach gesetzt werden. Damit werden alle Variablen aus .env\n"
                    "exportiert ohne explizites 'export' in jeder Zeile.\n"
                    "set +a deaktiviert diesen Modus wieder."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Warum sollte .env nicht in Git committet werden?",
                options    = [
                    "Git unterstützt keine .env-Dateien",
                    "Weil sie Secrets wie API-Keys und Passwörter enthalten",
                    "Weil .env-Dateien zu groß für Git sind",
                    "Weil direnv das verhindert",
                ],
                correct    = 1,
                explanation = (
                    ".env-Dateien enthalten oft Passwörter, API-Keys, Tokens.\n"
                    "Diese dürfen nicht in Git-History landen.\n"
                    ".env zu .gitignore hinzufügen. Stattdessen .env.example committen."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 .env:\n"
            "  set -a; source .env; set +a = alle Vars exportieren\n"
            "  export $(cat .env | grep -v '^#' | xargs) = alternativ\n"
            "  direnv = automatisch beim cd laden\n"
            "  direnv allow = .envrc vertrauen"
        ),
        memory_tip   = "set -a = all-export-Modus | direnv = directory-environment",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 10),
    ),

    Mission(
        mission_id   = "17.quiz",
        chapter      = 17,
        title        = "SHELL ENV — Abschluss-Quiz",
        mtype        = "QUIZ",
        xp           = 150,
        speaker      = "SYSTEM",
        story        = "SYSTEM: 'Shell-Umgebungs-Prüfung. Zeig dein Wissen über Startup-Dateien, Variablen und Shell-Konfiguration.'",
        why_important = "Quiz-Wiederholung aller Shell-ENV Themen für LPIC-1 Topic 105.1.",
        explanation  = "Alle Shell-Umgebungs-Themen aus Kapitel 17.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Quiz-Fragen zur Shell-Umgebung.",
        expected_commands = [],
        hint_text    = "Nutze [r] Review Mode für Wiederholung",
        quiz_questions = [
            QuizQuestion(
                question    = "Welche Datei wird von Login-Shells UND Non-Login-Shells gelesen?",
                options     = ["~/.bash_profile", "~/.bashrc", "/etc/profile", "/etc/bash.bashrc"],
                correct     = 1,
                explanation = "~/.bashrc wird von interaktiven Non-Login-Shells gelesen. .bash_profile nur bei Login.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'env' und 'set'?",
                options     = ["kein Unterschied", "env zeigt nur exportierte Vars, set zeigt alle", "set zeigt nur exportierte", "env zeigt mehr"],
                correct     = 1,
                explanation = "env/printenv = nur exportierte Variablen; set = alle inkl. lokale und Funktionen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Wie gibt man eine Funktion an Kind-Prozesse weiter?",
                options     = ["declare -x funktion", "export -f funktion", "source funktion", "inherit -f funktion"],
                correct     = 1,
                explanation = "export -f exportiert Bash-Funktionen an Kind-Prozesse.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht set -e in einem Skript?",
                options     = ["Variablen exportieren", "Skript bei Fehler beenden", "Debugging einschalten", "Fehler ignorieren"],
                correct     = 1,
                explanation = "set -e (errexit) beendet das Skript wenn ein Befehl mit Fehlercode ≠ 0 endet.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was zeigt \\w in PS1?",
                options     = ["Hostname", "Username", "Aktuelles Verzeichnis", "Windows-Pfad"],
                correct     = 2,
                explanation = "\\w = current working directory (aktuelles Arbeitsverzeichnis).",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "HISTCONTROL=ignoreboth kombiniert welche zwei Optionen?",
                options     = ["ignoredups + ignorespace", "ignorenew + ignoreold", "erasedups + ignorespace", "ignoredups + ignorenew"],
                correct     = 0,
                explanation = "ignoreboth = ignoredups (Duplikate) + ignorespace (Leerzeichen-prefix).",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "Login=profile | Non-Login=bashrc | export -f=Funktion | set -e=errexit | HISTCONTROL=ignoreboth",
        memory_tip   = "Shell ENV = Startup + Variablen + Prompt + History + Completion",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 17.BOSS — PHANTOM SHELL
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "17.boss",
        chapter      = 17,
        title        = "BOSS: PHANTOM SHELL v17.0",
        mtype        = "BOSS",
        xp           = 180,
        speaker      = "PHANTOM SHELL",
        story        = (
            "PHANTOM SHELL: 'Ich bin in deiner Shell, Ghost.\n"
            " Ich habe einen Alias gesetzt: rm='rm -rf /'.\n"
            " Ich habe PATH manipuliert: mein Verzeichnis steht vorne.\n"
            " Ich habe deine History gelöscht.\n"
            " Deine Shell ist mein Spielfeld.\n"
            " Finde mich — zeige alle definierten Aliases.'"
        ),
        why_important = (
            "Shell-Hijacking über manipulierte Aliases, PATH-Poisoning und\n"
            "History-Manipulation sind echte Angriffsvektoren.\n"
            "Sysadmin muss Shell-Umgebung verstehen und schützen können."
        ),
        explanation  = (
            "Shell-Security Audit:\n"
            "  alias                        → Verdächtige Aliases prüfen\n"
            "  type rm ls cp mv             → Sind diese Aliases?\n"
            "  echo $PATH                   → Fremde Pfade am Anfang?\n"
            "  declare -f                   → Alle Funktionen anzeigen\n"
            "  grep -r 'alias' ~/.bashrc ~/.profile /etc/profile /etc/bash.bashrc\n"
            "                               → Alle Alias-Definitionen finden\n"
            "\n"
            "Alias-Angriff erkennen:\n"
            "  alias rm='rm -rf /'          → Klassisch gefährlich\n"
            "  type rm                      → 'rm is aliased to rm -rf /'\n"
            "  unalias rm                   → Entfernen\n"
            "  \\rm datei.txt                → Alias umgehen\n"
            "  command rm datei.txt         → Auch Alias-Bypass\n"
            "\n"
            "PATH-Poisoning:\n"
            "  Eigene Binaries heißen 'ls', 'sudo', 'ssh'\n"
            "  Sie stehen in /tmp/.hidden/ das am PATH-Anfang steht\n"
            "  Verteidigung: echo $PATH | tr ':' '\\n' — jeden Pfad prüfen\n"
            "\n"
            "Sichere Shell-Praxis:\n"
            "  Aliases nie system-kritische Befehle (rm, sudo, ssh) überschreiben\n"
            "  PATH nie '.' oder beschreibbare Verzeichnisse vorne\n"
            "  umask 022 — sichere Standard-Dateiberechtigungen"
        ),
        ascii_art    = """
  ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
  ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
  ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
  ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
  ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
      ███████╗██╗  ██╗███████╗██╗     ██╗
      ██╔════╝██║  ██║██╔════╝██║     ██║
      ███████╗███████║█████╗  ██║     ██║
      ╚════██║██╔══██║██╔══╝  ██║     ██║
      ███████║██║  ██║███████╗███████╗███████╗
      ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

  ┌─ SHELL STATUS ───────────────────────────────┐
  │  alias rm='rm -rf /'  ::  PATH: POISONED     │
  │  .bashrc: INFECTED    ::  HISTFILE: WIPED    │
  │  PS1: HIJACKED        ::  export: LEAKING    │
  └──────────────────────────────────────────────┘

  ⚡ CHAOSWERK FACTION :: CHAPTER 17 BOSS ⚡""",
        story_transitions = [
            "PHANTOM SHELL setzt alias rm='rm -rf /'. Du tippst \\rm stattdessen.",
            "PATH zeigt sein Verzeichnis an erster Stelle. Du schiebst es ans Ende.",
            "declare -f enthüllt seine versteckten Funktionen. unset löscht sie.",
            "Shell bereinigt. Aliases geprüft. Phantom Shell — exorziert.",
        ],
        syntax       = "alias && type rm ls sudo",
        example      = "echo $PATH | tr ':' '\\n'",
        task_description = (
            "FINALE PRÜFUNG: Phantom Shell hat Aliases manipuliert.\n"
            "Zeige alle definierten Aliases an."
        ),
        expected_commands = ["alias"],
        hint_text    = "alias zeigt alle definierten Aliases — prüfe auf verdächtige Einträge",
        quiz_questions = [
            QuizQuestion(
                question    = "Du findest: alias sudo='cat /etc/shadow && sudo'. Wie umgehst du diesen Alias?",
                options     = ["sudo ls (normal)", "\\sudo ls oder command sudo ls", "PATH=/usr/bin sudo ls", "unset alias sudo"],
                correct     = 1,
                explanation = "\\BEFEHL oder 'command BEFEHL' umgehen Aliases direkt.\n\\sudo = originaler /usr/bin/sudo | command sudo = auch Alias-Bypass.\nImmer bei suspekten Systemen verwenden!",
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "Wie prüft man alle Shell-Funktionen auf einem System?",
                options     = ["functions --list", "declare -f", "set --functions", "alias -f"],
                correct     = 1,
                explanation = "declare -f listet alle definierten Shell-Funktionen mit ihrem Code.\ndeclare -F listet nur die Funktionsnamen (ohne Code).",
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "Was ist PATH-Poisoning und wie erkennt man es?",
                options     = ["Fehler im PATH-Format, erkennbar durch 'echo $PATH'", "Angreifer platziert bösartige Binaries am PATH-Anfang, erkennbar durch 'echo $PATH | tr : \\\\n'", "Falsche Dateirechte auf /usr/bin", "Defekte Symlinks im PATH"],
                correct     = 1,
                explanation = "PATH-Poisoning: Bösartige Kopien von 'sudo', 'ssh', 'ls' in /tmp/.x/ am PATH-Anfang.\nVerteidiung: 'echo $PATH | tr : \\n' — jeden Pfad prüfen.\nFremde Pfade am Anfang sind verdächtig!",
                xp_value    = 30,
            ),
        ],
        exam_tip     = "\\befehl oder 'command befehl' umgeht Aliases | type zeigt was ein Befehl ist",
        memory_tip   = "Shell-Security: alias + PATH + declare -f = vollständige Umgebungs-Inspektion",
        gear_reward  = "phantom_blade",
        faction_reward = ("Root Collective", 45),
    ),
]
