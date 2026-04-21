"""
NeonGrid-9 :: Kapitel 14 — SCRIPT PROTOCOL
LPIC-1 Topic 105.2
Bash-Scripting: Variablen, Bedingungen, Schleifen, Funktionen, getopts

"In NeonGrid-9 automatisiert sich kein System von selbst.
 Skripte sind die Verlängerung deines Willens.
 Ein Skript, das einmal läuft, läuft für immer.
 Lern Bash — oder tippe ewig dasselbe."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_14_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 14.01 — Bash-Skript Grundstruktur
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.01",
        chapter      = 14,
        title        = "Bash-Skripte — Struktur & Shebang",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Du tippst denselben Befehl zum 50. Mal, Ghost.\n"
            " Das ist Masochismus — kein Hacking.\n"
            " Ein Bash-Skript schreibt du einmal.\n"
            " Dann läuft es für immer. Fang an.'"
        ),
        why_important = (
            "Bash-Scripting ist LPIC-1 Topic 105.2 und zieht sich durch viele Themen.\n"
            "Shebang, Exit-Codes und grundlegende Syntax sind Pflicht-Wissen."
        ),
        explanation  = (
            "BASH-SKRIPT GRUNDSTRUKTUR:\n\n"
            "SHEBANG (erste Zeile):\n"
            "  #!/bin/bash          Bash-Interpreter\n"
            "  #!/bin/sh            POSIX-Shell (portabler)\n"
            "  #!/usr/bin/env bash  flexibler (findet bash in PATH)\n\n"
            "MINIMALES SKRIPT:\n"
            "  #!/bin/bash\n"
            "  echo 'Hallo, Ghost!'\n\n"
            "AUSFÜHRBAR MACHEN:\n"
            "  chmod +x skript.sh\n"
            "  chmod 755 skript.sh\n\n"
            "AUSFÜHREN:\n"
            "  ./skript.sh          direkt (braucht +x)\n"
            "  bash skript.sh       interpreter explizit\n"
            "  source skript.sh     im aktuellen Shell-Kontext\n"
            "  . skript.sh          wie source\n\n"
            "EXIT-CODES:\n"
            "  exit 0               Erfolg\n"
            "  exit 1               Fehler (allgemein)\n"
            "  exit 2               Missbrauch von Shell-Befehlen\n"
            "  $?                   Exit-Code des letzten Befehls\n\n"
            "BEISPIEL:\n"
            "  #!/bin/bash\n"
            "  echo 'Starte Backup...'\n"
            "  cp /etc/passwd /tmp/passwd.bak\n"
            "  if [ $? -eq 0 ]; then\n"
            "      echo 'Backup OK'\n"
            "      exit 0\n"
            "  else\n"
            "      echo 'Backup FAILED' >&2\n"
            "      exit 1\n"
            "  fi\n\n"
            "KOMMENTARE:\n"
            "  # Das ist ein Kommentar\n"
            "  # Alles nach # wird ignoriert\n\n"
            "DEBUG-MODUS:\n"
            "  bash -x skript.sh    jeden Befehl vor Ausführung zeigen\n"
            "  bash -n skript.sh    Syntax prüfen ohne Ausführung\n"
            "  set -x               Debug innerhalb des Skripts\n"
            "  set -e               bei Fehler sofort beenden\n"
            "  set -u               ungesetzte Variablen als Fehler\n"
            "  set -o pipefail      Pipe-Fehler erkennen"
        ),
        ascii_art = """
  ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗██╗███╗   ██╗ ██████╗
  ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝
  ███████╗██║     ██████╔╝██║██████╔╝   ██║   ██║██╔██╗ ██║██║  ███╗
  ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   ██║██║╚██╗██║██║   ██║
  ███████║╚██████╗██║  ██║██║██║        ██║   ██║██║ ╚████║╚██████╔╝
  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝

  [ CHAPTER 14 :: SHELL SCRIPTING ]
  > #!/bin/bash loaded. set -euo pipefail. Execute.""",
        story_transitions = [
            "Ein Skript ist Automatisierung. Was einmal manuell war, läuft jetzt allein.",
            "set -euo pipefail: bei Fehler stoppen. Kein stilles Versagen.",
            "Variablen, Schleifen, Funktionen — die Grammatik der Automatisierung.",
            "Ein gutes Skript ersetzt hundert manuelle Befehle.",
        ],
        syntax       = "#!/bin/bash  |  chmod +x skript.sh  |  ./skript.sh",
        example      = (
            "#!/bin/bash\n"
            "# Einfaches Backup-Skript\n"
            "set -e\n"
            "echo 'Backup startet...'\n"
            "cp -r /etc /tmp/etc_backup_$(date +%Y%m%d)\n"
            "echo 'Backup fertig!'\n"
            "exit 0"
        ),
        task_description = "Mache das Skript backup.sh ausführbar",
        expected_commands = ["chmod +x backup.sh"],
        hint_text    = "chmod +x datei.sh macht eine Datei ausführbar (execute-Bit setzen)",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist die Shebang-Zeile und warum wichtig?',
                options     = ['A) Kommentar-Zeile', 'B) Erste Zeile: #!/bin/bash — definiert den Interpreter für das Skript', 'C) Sicherheits-Header', 'D) Encoding-Deklaration'],
                correct     = 'B',
                explanation = '#!/bin/bash = Shebang. Ohne Shebang: Skript wird als aktuelle Shell interpretiert.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welche Rechte braucht ein Skript zum Ausführen?',
                options     = ['A) Read + Execute', 'B) Write + Execute', 'C) Nur Execute', 'D) Alle Rechte (777)'],
                correct     = 'A',
                explanation = 'chmod +x oder chmod 755. Read+Execute reicht zum Ausführen.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNG: Shebang MUSS erste Zeile sein!\n"
            "  #!/bin/bash = absoluter Pfad\n"
            "  #!/usr/bin/env bash = flexibler (empfohlen)\n"
            "$? = Exit-Code des letzten Befehls (0=OK, ≠0=Fehler)"
        ),
        memory_tip   = "Merkhilfe: Shebang=#! (sharp-bang). exit 0=OK, exit 1=Fehler",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.02 — Variablen & Parameter
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.02",
        chapter      = 14,
        title        = "Variablen, Parameter & Expansion",
        mtype        = "DECODE",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ein Skript ohne Variablen ist ein Tipp-Roboter.\n"
            " Variablen machen es dynamisch. $1, $2 für Argumente.\n"
            " $@ für alle. $# für die Anzahl.\n"
            " Lern die Expansion — dann gehört dir das Skript.'"
        ),
        why_important = (
            "Variablen und Parameter sind das Herzstück jedes Bash-Skripts.\n"
            "LPIC-1 testet Positionsparameter, spezielle Variablen und Expansion."
        ),
        explanation  = (
            "VARIABLEN:\n\n"
            "DEFINIEREN:\n"
            "  NAME='Ghost'          kein Leerzeichen um =!\n"
            "  ZAHL=42\n"
            "  DATUM=$(date)         Command Substitution\n"
            "  DATUM=`date`          alte Syntax (gleich)\n\n"
            "LESEN:\n"
            "  echo $NAME\n"
            "  echo ${NAME}          geschweifte Klammern (sicherer)\n"
            "  echo \"Hallo, $NAME!\"  in doppelten Quotes\n\n"
            "POSITIONSPARAMETER:\n"
            "  $0   Skriptname\n"
            "  $1   erstes Argument\n"
            "  $2   zweites Argument\n"
            "  $9   neuntes Argument\n"
            "  ${10} zehntes Argument (braucht {})\n\n"
            "SPEZIELLE VARIABLEN:\n"
            "  $#   Anzahl der Argumente\n"
            "  $@   alle Argumente (als separate Strings)\n"
            "  $*   alle Argumente (als ein String)\n"
            "  $?   Exit-Code des letzten Befehls\n"
            "  $$   PID des aktuellen Skripts\n"
            "  $!   PID des letzten Hintergrundprozesses\n"
            "  $0   Name des Skripts\n\n"
            "PARAMETER-EXPANSION:\n"
            "  ${VAR:-default}   Wert oder 'default' wenn leer\n"
            "  ${VAR:=default}   Wert setzen wenn leer\n"
            "  ${VAR:?fehler}    Fehler wenn leer\n"
            "  ${#VAR}           Länge des Strings\n"
            "  ${VAR:2:5}        Substring (pos 2, 5 Zeichen)\n"
            "  ${VAR^^}          Großbuchstaben\n"
            "  ${VAR,,}          Kleinbuchstaben\n"
            "  ${VAR/alt/neu}    erste Ersetzung\n"
            "  ${VAR//alt/neu}   alle Ersetzungen\n\n"
            "READONLY:\n"
            "  readonly KONSTANTE=42   kann nicht geändert werden\n\n"
            "LOKALE VARIABLEN (in Funktionen):\n"
            "  local VAR=wert          nur innerhalb der Funktion"
        ),
        syntax       = "VAR='wert'  |  echo $VAR  |  $1 $2 $# $@ $?",
        example      = (
            "#!/bin/bash\n"
            "NAME=${1:-'Ghost'}      # Default wenn kein Argument\n"
            "echo \"Hallo, $NAME!\"\n"
            "echo \"Argumente: $#\"\n"
            "echo \"Alle Args: $@\"\n"
            "GROSS=${NAME^^}\n"
            "echo \"Großbuchstaben: $GROSS\"\n"
            "LAENGE=${#NAME}\n"
            "echo \"Länge: $LAENGE\""
        ),
        task_description = "Wie lautet die spezielle Variable für den Exit-Code des letzten Befehls?",
        expected_commands = ["echo $?"],
        hint_text    = "$? enthält den Exit-Code des letzten ausgeführten Befehls (0=Erfolg)",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was enthält $#?',
                options     = ['A) Exit-Code des letzten Befehls', 'B) Anzahl der Skript-Argumente', 'C) Letztes Argument', 'D) Skriptname'],
                correct     = 'B',
                explanation = '$# = Anzahl der Parameter. $1 $2 ... = einzelne Parameter. $@ = alle als Array.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was ist der Unterschied zwischen $@ und $*?',
                options     = ['A) Kein Unterschied', 'B) "$@" bewahrt einzelne Argumente (gequotet), "$*" macht einen String', 'C) $* ist veraltet', 'D) $@ nur in Funktionen'],
                correct     = 'B',
                explanation = '"$@" = jedes Argument separat gequotet. "$*" = alle als ein String. $@ fast immer bevorzugt.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGS-FALLE: Kein Leerzeichen um '=' beim Setzen!\n"
            "  VAR=wert   ✓  KORREKT\n"
            "  VAR = wert ✗  FEHLER\n"
            "$@ vs $*: In Anführungszeichen ist \"$@\" sicherer für Argumente!"
        ),
        memory_tip   = "Merkhilfe: $#=count, $@=all-args, $?=exit-code, $$=PID, $0=scriptname",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.03 — Bedingungen & test
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.03",
        chapter      = 14,
        title        = "if / test / [ ] — Bedingungen",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Ein Skript das IMMER das Gleiche tut ist nutzlos.\n"
            " if-Bedingungen geben ihm Intelligenz.\n"
            " Existiert die Datei? Ist der User root? Ist der Port offen?\n"
            " test und [ ] sind deine Entscheidungs-Engine.'"
        ),
        why_important = (
            "Bedingungen sind das Fundament jeder Skript-Logik.\n"
            "LPIC-1 testet if/elif/else, test-Operatoren und [[ ]] ausführlich."
        ),
        explanation  = (
            "IF-BEDINGUNGEN:\n\n"
            "SYNTAX:\n"
            "  if [ BEDINGUNG ]; then\n"
            "      Befehle\n"
            "  elif [ ANDERE ]; then\n"
            "      Befehle\n"
            "  else\n"
            "      Befehle\n"
            "  fi\n\n"
            "TEST-OPERATOREN — DATEIEN:\n"
            "  -e DATEI    Datei existiert\n"
            "  -f DATEI    Datei (kein Verzeichnis)\n"
            "  -d DATEI    Verzeichnis\n"
            "  -r DATEI    lesbar\n"
            "  -w DATEI    schreibbar\n"
            "  -x DATEI    ausführbar\n"
            "  -s DATEI    Größe > 0 (nicht leer)\n"
            "  -L DATEI    symbolischer Link\n\n"
            "TEST-OPERATOREN — STRINGS:\n"
            "  -z STRING   leer (zero length)\n"
            "  -n STRING   nicht leer\n"
            "  S1 = S2     gleich\n"
            "  S1 != S2    ungleich\n"
            "  S1 < S2     lexikografisch kleiner (in [[]])\n\n"
            "TEST-OPERATOREN — ZAHLEN:\n"
            "  N1 -eq N2   gleich (equal)\n"
            "  N1 -ne N2   ungleich (not equal)\n"
            "  N1 -lt N2   kleiner (less than)\n"
            "  N1 -le N2   kleiner gleich (less or equal)\n"
            "  N1 -gt N2   größer (greater than)\n"
            "  N1 -ge N2   größer gleich (greater or equal)\n\n"
            "LOGISCHE VERKNÜPFUNG:\n"
            "  [ A ] && [ B ]   UND (in [  ])\n"
            "  [ A ] || [ B ]   ODER\n"
            "  ! [ A ]          NICHT\n"
            "  [[ A && B ]]     UND (in [[  ]])\n"
            "  [[ A || B ]]     ODER\n\n"
            "[[ ]] vs [ ]:\n"
            "  [[ ]] = bash-spezifisch, sicherer, Regex mit =~\n"
            "  [  ]  = POSIX, portabler\n\n"
            "KURZSCHREIBWEISE:\n"
            "  [ -f /etc/passwd ] && echo 'existiert'\n"
            "  command || { echo 'Fehler'; exit 1; }"
        ),
        syntax       = "if [ BEDINGUNG ]; then ... fi  |  [ -f DATEI ]  |  [[ STRING =~ REGEX ]]",
        example      = (
            "#!/bin/bash\n"
            "DATEI='/etc/passwd'\n"
            "if [ -f \"$DATEI\" ]; then\n"
            "    echo \"$DATEI existiert\"\n"
            "elif [ -d \"$DATEI\" ]; then\n"
            "    echo \"$DATEI ist ein Verzeichnis\"\n"
            "else\n"
            "    echo \"$DATEI nicht gefunden\"\n"
            "fi\n\n"
            "# Zahlen-Vergleich:\n"
            "if [ $# -lt 1 ]; then\n"
            "    echo 'Fehler: Kein Argument!' >&2\n"
            "    exit 1\n"
            "fi"
        ),
        task_description = "Welcher test-Operator prüft ob eine Datei existiert und ausführbar ist?",
        expected_commands = ["test -x /bin/bash"],
        hint_text    = "test -x DATEI (oder [ -x DATEI ]) prüft ob eine Datei ausführbar ist",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welche test-Bedingung prüft ob eine Datei existiert?',
                options     = ['A) [ -e DATEI ]', 'B) [ -x DATEI ]', 'C) [ -f DATEI ]', 'D) [ -d DATEI ]'],
                correct     = 'A',
                explanation = '-e = exists. -f = regular file. -d = directory. -x = executable. -r = readable.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht '[ -z $VAR ]'?",
                options     = ['A) Prüft ob Variable zero ist (Zahl)', 'B) Prüft ob Variable leer (zero length) ist', 'C) Prüft ob Variable gesetzt ist', 'D) Prüft Datei-Größe'],
                correct     = 'B',
                explanation = '-z = zero length (leer). -n = not empty. Immer quoten: [ -z "$VAR" ]!',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "HÄUFIGE PRÜFUNGSFRAGEN:\n"
            "  -e = exists (any type)\n"
            "  -f = file (regular file)\n"
            "  -d = directory\n"
            "  -z = zero length (leer)\n"
            "  -n = not zero (nicht leer)\n"
            "Zahlen: -eq -ne -lt -le -gt -ge"
        ),
        memory_tip   = "Merkhilfe: -e=exists, -f=file, -d=dir, -z=zero, -n=not-zero, -x=executable",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.04 — Schleifen: for, while, until
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.04",
        chapter      = 14,
        title        = "Schleifen — for, while & until",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: '1000 Log-Dateien archivieren, Ghost.\n"
            " Eine for-Schleife: drei Zeilen. Erledigt.\n"
            " Oder du tippst 1000 Mal cp. Deine Wahl.\n"
            " Schleifen sind die Multiplikatoren deiner Macht.'"
        ),
        why_important = (
            "Schleifen ermöglichen die Verarbeitung von Mengen.\n"
            "LPIC-1 testet for-Schleifen mit Listen und Globs, while mit Bedingungen."
        ),
        explanation  = (
            "FOR-SCHLEIFEN:\n\n"
            "ÜBER LISTE:\n"
            "  for VAR in wert1 wert2 wert3; do\n"
            "      echo $VAR\n"
            "  done\n\n"
            "ÜBER DATEIEN:\n"
            "  for DATEI in /var/log/*.log; do\n"
            "      echo \"Verarbeite: $DATEI\"\n"
            "  done\n\n"
            "ÜBER BEFEHLSAUSGABE:\n"
            "  for USER in $(cat /etc/passwd | cut -d: -f1); do\n"
            "      echo \"User: $USER\"\n"
            "  done\n\n"
            "C-STIL FOR (Bash):\n"
            "  for ((i=1; i<=10; i++)); do\n"
            "      echo $i\n"
            "  done\n\n"
            "SEQ-BEFEHL:\n"
            "  for i in $(seq 1 10); do echo $i; done\n"
            "  for i in {1..10}; do echo $i; done\n"
            "  for i in {1..10..2}; do echo $i; done  # Schrittweite 2\n\n"
            "WHILE-SCHLEIFEN:\n\n"
            "  while [ BEDINGUNG ]; do\n"
            "      Befehle\n"
            "  done\n\n"
            "BEISPIELE:\n"
            "  ZAEHLER=0\n"
            "  while [ $ZAEHLER -lt 5 ]; do\n"
            "      echo $ZAEHLER\n"
            "      ZAEHLER=$((ZAEHLER + 1))\n"
            "  done\n\n"
            "ZEILEN EINER DATEI LESEN:\n"
            "  while IFS= read -r ZEILE; do\n"
            "      echo \"$ZEILE\"\n"
            "  done < /etc/passwd\n\n"
            "UNTIL-SCHLEIFE:\n"
            "  until [ BEDINGUNG_WAHR ]; do\n"
            "      Befehle    # läuft BIS Bedingung WAHR wird\n"
            "  done\n\n"
            "BREAK & CONTINUE:\n"
            "  break       Schleife beenden\n"
            "  continue    nächste Iteration\n"
            "  break 2     äußere Schleife beenden"
        ),
        syntax       = "for VAR in LISTE; do ... done  |  while [ COND ]; do ... done",
        example      = (
            "# Alle .log-Dateien komprimieren:\n"
            "for LOG in /var/log/*.log; do\n"
            "    gzip \"$LOG\"\n"
            "    echo \"Komprimiert: $LOG\"\n"
            "done\n\n"
            "# Auf Service warten:\n"
            "while ! systemctl is-active --quiet nginx; do\n"
            "    echo 'Warte auf nginx...'\n"
            "    sleep 2\n"
            "done\n"
            "echo 'nginx läuft!'"
        ),
        task_description = "Wie iteriert man mit for über alle .sh-Dateien im aktuellen Verzeichnis?",
        expected_commands = ["for f in *.sh; do echo $f; done"],
        hint_text    = "for f in *.sh; do ... done iteriert über alle .sh-Dateien per Glob",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist der Unterschied zwischen for und while in Bash?',
                options     = ['A) Kein Unterschied', 'B) for iteriert über Liste, while läuft solange Bedingung wahr', 'C) while ist schneller', 'D) for nur für Zahlen'],
                correct     = 'B',
                explanation = 'for VAR in LISTE: iteriert. while BEDINGUNG: läuft solange Bedingung 0 (true).',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wie iteriert man über alle Argumente in einer for-Schleife?',
                options     = ['A) for arg in $@; do', 'B) for arg in "$@"; do', 'C) for arg; do (implizit $@)', 'D) B oder C'],
                correct     = 'D',
                explanation = 'for arg in "$@"; do ODER kurz: for arg; do (iteriert implizit über "$@").',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "MERKE: for..in..do..done und while..do..done\n"
            "IFS= read -r ZEILE = sicher Zeilenweise lesen\n"
            "(( )) für Arithmetic: ZAEHLER=$((ZAEHLER + 1))\n"
            "break = Schleife abbrechen, continue = nächste Iteration"
        ),
        memory_tip   = "Merkhilfe: for=iteration, while=condition-loop, until=inverse-while",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.05 — Funktionen & case
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.05",
        chapter      = 14,
        title        = "Funktionen & case — Strukturierung",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Ein 500-Zeilen-Skript ohne Funktionen\n"
            " ist ein Albtraum. Wartungsunfähig. Unleserlich.\n"
            " Funktionen kapseln Logik. case macht Menüs.\n"
            " Strukturiere deinen Code — oder er strukturiert dich.'"
        ),
        why_important = (
            "Funktionen und case-Anweisungen sind LPIC-1-Prüfungsstoff.\n"
            "case ist eleganter als if/elif-Kaskaden für Menüs."
        ),
        explanation  = (
            "FUNKTIONEN:\n\n"
            "DEFINITION:\n"
            "  function mein_func() {   # Bash-Syntax\n"
            "      Befehle\n"
            "  }\n\n"
            "  mein_func() {            # POSIX-Syntax (portabler)\n"
            "      Befehle\n"
            "  }\n\n"
            "AUFRUFEN:\n"
            "  mein_func               # ohne Klammern!\n"
            "  mein_func arg1 arg2     # mit Argumenten\n\n"
            "PARAMETER IN FUNKTIONEN:\n"
            "  $1 $2 ...  Funktions-Argumente (NICHT Skript-Args)\n"
            "  local VAR  lokale Variable\n"
            "  return N   Rückgabewert (0-255)\n\n"
            "BEISPIEL:\n"
            "  log() {\n"
            "      local LEVEL=${1:-INFO}\n"
            "      local MSG=$2\n"
            "      echo \"[$(date +%T)] [$LEVEL] $MSG\"\n"
            "  }\n"
            "  log INFO 'Skript startet'\n"
            "  log ERROR 'Datei nicht gefunden'\n\n"
            "RÜCKGABEWERT:\n"
            "  ist_root() {\n"
            "      [ \"$(id -u)\" -eq 0 ]\n"
            "  }\n"
            "  if ist_root; then echo 'root!'; fi\n\n"
            "CASE-ANWEISUNG:\n\n"
            "SYNTAX:\n"
            "  case $VARIABLE in\n"
            "      MUSTER1)\n"
            "          Befehle ;;\n"
            "      MUSTER2|MUSTER3)\n"
            "          Befehle ;;\n"
            "      *)\n"
            "          Default ;;\n"
            "  esac\n\n"
            "BEISPIEL:\n"
            "  case $1 in\n"
            "      start)   systemctl start nginx ;;\n"
            "      stop)    systemctl stop nginx ;;\n"
            "      status)  systemctl status nginx ;;\n"
            "      restart) systemctl restart nginx ;;\n"
            "      *)       echo \"Unbekannt: $1\"; exit 1 ;;\n"
            "  esac\n\n"
            "MUSTER IN CASE:\n"
            "  *)       alles (default)\n"
            "  y|Y|yes) Alternativen mit |\n"
            "  [Yy]*)   Wildcard im Muster"
        ),
        syntax       = "func() { ... }  |  case $VAR in MUSTER) ... ;; esac",
        example      = (
            "#!/bin/bash\n"
            "usage() {\n"
            "    echo \"Verwendung: $0 {start|stop|status}\"\n"
            "    exit 1\n"
            "}\n\n"
            "[ $# -eq 0 ] && usage\n\n"
            "case $1 in\n"
            "    start)   echo 'Starte Dienst...' ;;\n"
            "    stop)    echo 'Stoppe Dienst...' ;;\n"
            "    status)  echo 'Dienst läuft'    ;;\n"
            "    *)       usage                  ;;\n"
            "esac"
        ),
        task_description = "Wie endet ein case-Block in Bash?",
        expected_commands = ["esac"],
        hint_text    = "case endet mit 'esac' (case rückwärts). Jedes Muster endet mit ;;",
        quiz_questions    = [
            QuizQuestion(
                question    = "Wie ruft man eine Funktion 'myfunc' in Bash auf?",
                options     = ['A) call myfunc', 'B) myfunc [argumente]', 'C) function myfunc', 'D) invoke myfunc'],
                correct     = 'B',
                explanation = 'Funktionen einfach wie Befehle aufrufen: myfunc arg1 arg2. Definition: myfunc() { ... }',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was macht case $VAR in bei Bash?',
                options     = ['A) Prüft jeden Buchstaben', 'B) Switch/Case: prüft Variable gegen Muster, führt passenden Block aus', 'C) Iteriert über Variable', 'D) Nur für Zahlen'],
                correct     = 'B',
                explanation = 'case $VAR in MUSTER) Befehle ;; esac. Muster: a|b = oder, * = default.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "case SYNTAX:\n"
            "  case $VAR in\n"
            "      MUSTER) Aktion ;;\n"
            "  esac\n"
            "  ;; = Ende eines Musters\n"
            "  *) = default/fallback\n"
            "  | = ODER zwischen Mustern"
        ),
        memory_tip   = "Merkhilfe: case...esac (rückwärts), if...fi (rückwärts), do...done",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.06 — Arithmetik & String-Operationen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.06",
        chapter      = 14,
        title        = "Arithmetik, Arrays & String-Operationen",
        mtype        = "DECODE",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Bash rechnet nicht von Haus aus, Ghost.\n"
            " $(( )) für Integer. bc für Float.\n"
            " Arrays für Listen. Strings für Text.\n"
            " Ohne diese Werkzeuge ist dein Skript halblahm.'"
        ),
        why_important = (
            "Arithmetik und String-Operationen sind in fast jedem Skript nötig.\n"
            "LPIC-1 testet $(( )), let, expr und Array-Grundlagen."
        ),
        explanation  = (
            "ARITHMETIK IN BASH:\n\n"
            "METHODEN:\n"
            "  ERGEBNIS=$((3 + 4))      Arithmetic Expansion\n"
            "  ((ZAEHLER++))            Arithmetic Command\n"
            "  let ERGEBNIS=3+4         let-Befehl\n"
            "  ERGEBNIS=$(expr 3 + 4)   expr (POSIX, langsamer)\n\n"
            "OPERATOREN:\n"
            "  +  -  *  /  %           Addition, Sub, Mul, Div, Modulo\n"
            "  **                       Potenz (Bash)\n"
            "  ++  --                   Inkrement/Dekrement\n"
            "  +=  -=  *=               zusammengesetzte Zuweisung\n\n"
            "FLOAT (bc):\n"
            "  echo '3.14 * 2' | bc\n"
            "  echo 'scale=2; 10/3' | bc   # 2 Dezimalstellen\n\n"
            "ARRAYS:\n\n"
            "ERSTELLEN:\n"
            "  FARBEN=('rot' 'grün' 'blau')\n"
            "  FARBEN[0]='rot'\n"
            "  FARBEN+= ('lila')         Element anhängen\n\n"
            "ZUGREIFEN:\n"
            "  echo ${FARBEN[0]}         erstes Element\n"
            "  echo ${FARBEN[@]}         alle Elemente\n"
            "  echo ${#FARBEN[@]}        Anzahl Elemente\n"
            "  echo ${!FARBEN[@]}        alle Indizes\n\n"
            "ÜBER ARRAY ITERIEREN:\n"
            "  for F in \"${FARBEN[@]}\"; do\n"
            "      echo $F\n"
            "  done\n\n"
            "STRING-OPERATIONEN:\n\n"
            "  STR='Hallo Ghost'\n"
            "  echo ${#STR}              Länge: 11\n"
            "  echo ${STR:6}             Substring ab 6: 'Ghost'\n"
            "  echo ${STR:6:5}           5 Zeichen ab 6: 'Ghost'\n"
            "  echo ${STR/Ghost/World}   Ersetzung\n"
            "  echo ${STR^^}            Großbuchstaben\n"
            "  echo ${STR,,}            Kleinbuchstaben\n"
            "  echo ${STR#Hallo }        Präfix entfernen\n"
            "  echo ${STR%Ghost}         Suffix entfernen"
        ),
        syntax       = "$(( AUSDRUCK ))  |  ARRAY=(a b c)  |  ${ARRAY[@]}",
        example      = (
            "# Arithmetik:\n"
            "X=10; Y=3\n"
            "echo $((X + Y))     # 13\n"
            "echo $((X % Y))     # 1\n"
            "echo $((X ** 2))    # 100\n\n"
            "# Array:\n"
            "LOGS=('/var/log/syslog' '/var/log/auth.log')\n"
            "echo \"Anzahl: ${#LOGS[@]}\"\n"
            "for LOG in \"${LOGS[@]}\"; do\n"
            "    wc -l \"$LOG\"\n"
            "done"
        ),
        task_description = "Berechne 15 modulo 4 mit Bash-Arithmetik",
        expected_commands = ["echo $((15 % 4))"],
        hint_text    = "$(( )) ist Bash-Arithmetic. % ist Modulo-Operator. Ergebnis: 3",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Wie berechnet man 2+3 in Bash?',
                options     = ['A) expr 2 + 3', 'B) echo $((2+3))', 'C) let result=2+3', 'D) A, B oder C'],
                correct     = 'D',
                explanation = 'Alle drei sind gültig! $(( )) = arithmetic expansion. let und expr auch möglich.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wie greift man auf alle Elemente eines Bash-Arrays zu?',
                options     = ['A) $ARRAY', 'B) ${ARRAY[@]}', 'C) $ARRAY[*]', 'D) ${ARRAY[all]}'],
                correct     = 'B',
                explanation = '${ARRAY[@]} = alle Elemente (gequotet). ${#ARRAY[@]} = Anzahl der Elemente.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "$(( )) = Bash-eigene Arithmetik (schnell, ganzzahlig)\n"
            "expr = POSIX, braucht Leerzeichen: expr 3 + 4\n"
            "bc = Float-Arithmetik: echo 'scale=2; 10/3' | bc\n"
            "${#VAR} = Länge der Variable"
        ),
        memory_tip   = "Merkhilfe: $(( ))=integer, bc=float, ${#VAR}=length, ${VAR[@]}=all-array",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.07 — getopts & Eingabe
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.07",
        chapter      = 14,
        title        = "getopts, read & Eingabe-Verarbeitung",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Professionelle Skripte haben Optionen, Ghost.\n"
            " -v für verbose. -f für Datei. -h für Hilfe.\n"
            " getopts ist der Standard-Weg.\n"
            " read macht dein Skript interaktiv.'"
        ),
        why_important = (
            "getopts ist LPIC-1 Topic 105.2 Prüfungsstoff.\n"
            "Professionelle Optionsverarbeitung ist ein Seniority-Signal."
        ),
        explanation  = (
            "GETOPTS — OPTION-VERARBEITUNG:\n\n"
            "SYNTAX:\n"
            "  getopts OPTSTRING VAR\n\n"
            "OPTSTRING:\n"
            "  'hvf:'   h und v ohne Argument, f MIT Argument (:)\n\n"
            "BEISPIEL:\n"
            "  #!/bin/bash\n"
            "  VERBOSE=0\n"
            "  DATEI=''\n\n"
            "  while getopts 'hvf:' OPT; do\n"
            "      case $OPT in\n"
            "          h) echo 'Hilfe...'; exit 0 ;;\n"
            "          v) VERBOSE=1 ;;\n"
            "          f) DATEI=$OPTARG ;;\n"
            "          ?) echo 'Unbekannte Option'; exit 1 ;;\n"
            "      esac\n"
            "  done\n"
            "  shift $((OPTIND - 1))  # verarbeitete Optionen entfernen\n\n"
            "WICHTIGE VARIABLEN:\n"
            "  $OPTARG    Argument der aktuellen Option\n"
            "  $OPTIND    Index des nächsten zu verarbeitenden Arguments\n\n"
            "READ — INTERAKTIVE EINGABE:\n\n"
            "  read VAR                  Eingabe in VAR speichern\n"
            "  read -p 'Name: ' NAME     mit Prompt\n"
            "  read -s PASSWORT          stilles Lesen (kein Echo)\n"
            "  read -n 1 TASTE           nur 1 Zeichen\n"
            "  read -t 10 VAR            Timeout 10 Sekunden\n"
            "  read -a ARRAY             Eingabe in Array\n"
            "  read -r ZEILE             Raw (kein Backslash-Escaping)\n\n"
            "HERE-DOCUMENT:\n"
            "  cat <<EOF\n"
            "  Zeile 1\n"
            "  Zeile 2\n"
            "  EOF\n\n"
            "HERE-STRING:\n"
            "  grep 'muster' <<< 'mein text'  # String als stdin"
        ),
        syntax       = "getopts 'hv:f:' OPT  |  read -p 'Prompt: ' VAR",
        example      = (
            "#!/bin/bash\n"
            "VERBOSE=0\n"
            "OUTPUT=''\n\n"
            "while getopts 'vo:h' OPT; do\n"
            "    case $OPT in\n"
            "        v) VERBOSE=1 ;;\n"
            "        o) OUTPUT=$OPTARG ;;\n"
            "        h) echo \"Verwendung: $0 [-v] [-o DATEI]\"; exit 0 ;;\n"
            "        ?) exit 1 ;;\n"
            "    esac\n"
            "done\n"
            "shift $((OPTIND - 1))\n\n"
            "[ $VERBOSE -eq 1 ] && echo 'Verbose-Modus aktiv'\n"
            "[ -n \"$OUTPUT\" ] && echo \"Ausgabe nach: $OUTPUT\""
        ),
        task_description = "Welche getopts-Variable enthält das Argument einer Option?",
        expected_commands = ["echo $OPTARG"],
        hint_text    = "$OPTARG enthält den Wert der letzten Option mit Argument (z.B. -f DATEI → $OPTARG=DATEI)",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist 'getopts' in Bash?",
                options     = ['A) Paket-Manager', 'B) Verarbeitet Kommandozeilen-Optionen (-v, -f, etc.)', 'C) Debugger', 'D) Eingabe-Validator'],
                correct     = 'B',
                explanation = "getopts 'hv:f:' = parsed -h (kein Arg), -v (mit Arg :), -f (mit Arg :). $OPTARG = Argument.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was macht \'read -p "Eingabe: " VAR\'?',
                options     = ['A) Liest Variable aus Datei', 'B) Zeigt Prompt und liest Eingabe in Variable', 'C) Passwort-Eingabe', 'D) Liest Prozess-ID'],
                correct     = 'B',
                explanation = 'read -p PROMPT VAR = Benutzereingabe mit Prompt. read -s = silent (für Passwörter).',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "GETOPTS MERKSÄTZE:\n"
            "  ':' nach Option = Option erwartet Argument\n"
            "  $OPTARG = das Argument der Option\n"
            "  $OPTIND = Index nach letzter Option\n"
            "  shift $((OPTIND-1)) = restliche Argumente zugänglich"
        ),
        memory_tip   = "Merkhilfe: OPTARG=argument-value, OPTIND=next-index. ':' nach Option=hat Argument",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.08 — Variablen & Typen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.08",
        chapter      = 14,
        title        = "Variablen & Typen — String, Integer, Array, declare",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Bash kennt keine Typen, Ghost — oder doch?\n"
            " declare -i macht aus einem String einen Integer.\n"
            " declare -a deklariert ein Array explizit.\n"
            " Kenne die Flags — die Prüfung fragt danach.'"
        ),
        why_important = (
            "Bash-Variablen sind standardmäßig Strings.\n"
            "declare-Attribute steuern das Verhalten und sind LPIC-1-Prüfungsstoff."
        ),
        explanation  = (
            "VARIABLEN-TYPEN IN BASH:\n\n"
            "STANDARD-VARIABLEN (alles String):\n"
            "  NAME='Ghost'           String\n"
            "  ZAHL=42               wird als String gespeichert\n"
            "  ERGEBNIS=$((5 + 3))   Arithmetik, dann String\n\n"
            "declare — TYPEN ERZWINGEN:\n"
            "  declare -i ZAHL=42      Integer (Arithmetik direkt)\n"
            "  declare -a ARRAY        Indexed Array\n"
            "  declare -A HASHMAP      Assoziatives Array (Bash 4+)\n"
            "  declare -r KONSTANTE=99  Read-only (wie readonly)\n"
            "  declare -x VAR          Export (wie export)\n"
            "  declare -l KLEIN        Automatisch Kleinbuchstaben\n"
            "  declare -u GROSS        Automatisch Großbuchstaben\n"
            "  declare -f              Alle Funktionen anzeigen\n"
            "  declare -p VAR          Variable-Definition anzeigen\n\n"
            "INTEGER-VARIABLEN:\n"
            "  declare -i X=5\n"
            "  X=X+1                  # → 6 (ohne $(( )))\n"
            "  X='hallo'              # → 0 (nicht-numerisch = 0)\n\n"
            "ARRAYS (INDEXED):\n"
            "  FARBEN=('rot' 'grün' 'blau')\n"
            "  declare -a FARBEN      # explizit deklarieren\n"
            "  FARBEN[3]='gelb'       # Index 3 setzen\n"
            "  echo ${FARBEN[0]}      # Zugriff mit Index\n"
            "  echo ${FARBEN[@]}      # alle Elemente\n"
            "  echo ${#FARBEN[@]}     # Anzahl Elemente\n"
            "  unset FARBEN[1]        # Element löschen\n\n"
            "ASSOZIATIVE ARRAYS (Bash 4+):\n"
            "  declare -A CAPS\n"
            "  CAPS[Deutschland]='Berlin'\n"
            "  CAPS[Frankreich]='Paris'\n"
            "  echo ${CAPS[Deutschland]}\n"
            "  echo ${!CAPS[@]}       # alle Schlüssel\n"
        ),
        syntax       = "declare -i VAR  |  declare -a ARRAY  |  declare -A MAP  |  declare -r CONST",
        example      = (
            "declare -i ZAEHLER=0\n"
            "ZAEHLER=ZAEHLER+1\n"
            "echo $ZAEHLER          # 1\n\n"
            "declare -a PORTS\n"
            "PORTS=(22 80 443 8080)\n"
            "echo \"${#PORTS[@]} Ports konfiguriert\"\n"
            "for P in \"${PORTS[@]}\"; do echo \"Port: $P\"; done\n\n"
            "declare -A DIENSTE\n"
            "DIENSTE[ssh]=22\n"
            "DIENSTE[http]=80\n"
            "echo \"SSH läuft auf Port ${DIENSTE[ssh]}\""
        ),
        task_description = "Zeige alle definierten Shell-Variablen und Funktionen mit declare",
        expected_commands = ["declare -p"],
        hint_text    = "declare -p zeigt alle definierten Variablen mit ihren Attributen und Werten",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt 'declare -i ZAHL' in Bash?",
                options    = [
                    "ZAHL wird als unveränderlich (read-only) markiert",
                    "ZAHL wird als Integer deklariert — Arithmetik ohne $(( ))",
                    "ZAHL wird in eine Ganzzahl konvertiert und ausgegeben",
                    "ZAHL wird als Array-Index verwendet",
                ],
                correct    = 1,
                explanation = (
                    "declare -i markiert die Variable als Integer.\n"
                    "Zuweisungen werden als arithmetische Ausdrücke ausgewertet.\n"
                    "ZAHL=ZAHL+1 funktioniert dann ohne $((ZAHL+1)).\n"
                    "Nicht-numerische Strings werden als 0 behandelt."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie deklariert man ein assoziatives Array in Bash?",
                options    = [
                    "declare -a MAP",
                    "declare -A MAP",
                    "array -h MAP",
                    "typeset MAP{}",
                ],
                correct    = 1,
                explanation = (
                    "declare -A erstellt ein assoziatives Array (Hash-Map) in Bash 4+.\n"
                    "declare -a erstellt ein normales indiziertes Array.\n"
                    "Zugriff: MAP[schluessel]=wert und echo ${MAP[schluessel]}"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "declare FLAGS:\n"
            "  -i = integer\n"
            "  -a = indexed array\n"
            "  -A = associative array\n"
            "  -r = readonly\n"
            "  -x = export\n"
            "  -f = functions\n"
            "  -p = print (anzeigen)"
        ),
        memory_tip   = "Merkhilfe: declare -i=int, -a=array, -A=Assoc, -r=readonly, -x=export, -f=functions",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.09 — Funktionen in Bash
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.09",
        chapter      = 14,
        title        = "Funktionen in Bash — function, return, local",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "RUST: 'Code-Wiederholung ist der Tod jedes Skripts, Ghost.\n"
            " Eine Logging-Funktion, zehn Mal aufgerufen.\n"
            " local verhindert Variablen-Kollisionen.\n"
            " return liefert Exit-Codes. Schreib sauber.'"
        ),
        why_important = (
            "Bash-Funktionen sind fundamentaler Prüfungsstoff für LPIC-1 Topic 105.2.\n"
            "local-Variablen und return-Codes sind Schlüsselkonzepte."
        ),
        explanation  = (
            "BASH-FUNKTIONEN:\n\n"
            "SYNTAX (zwei gleichwertige Varianten):\n"
            "  function mein_func {      # Bash-Syntax\n"
            "      Befehle\n"
            "  }\n\n"
            "  mein_func() {             # POSIX-Syntax (portabler)\n"
            "      Befehle\n"
            "  }\n\n"
            "AUFRUFEN (ohne Klammern!):\n"
            "  mein_func\n"
            "  mein_func arg1 arg2\n\n"
            "PARAMETER IN FUNKTIONEN:\n"
            "  $1, $2, ...  → Funktions-Argumente (überschatten Skript-$1!)\n"
            "  $0           → bleibt Skriptname (nicht Funktionsname)\n"
            "  $@, $#       → Funktions-Argumente\n\n"
            "LOKALE VARIABLEN:\n"
            "  local VAR=wert      # nur innerhalb der Funktion sichtbar\n"
            "  local -i ZAHL=0     # lokaler Integer\n"
            "  Ohne local: Variable ist global (Seiteneffekte!)\n\n"
            "RÜCKGABEWERT:\n"
            "  return N            # N = Exit-Code 0-255\n"
            "  return 0            # Erfolg\n"
            "  return 1            # Fehler\n"
            "  $?                  # Exit-Code nach Funktionsaufruf\n"
            "  echo 'Wert'         # Ausgabe = Rückgabewert via $()\n\n"
            "WERT ZURÜCKGEBEN (nicht exit-code):\n"
            "  get_version() { echo '1.2.3'; }\n"
            "  VER=$(get_version)   # Ausgabe als Variable nutzen\n\n"
            "BEISPIEL:\n"
            "  log() {\n"
            "      local level=$1\n"
            "      local msg=$2\n"
            "      echo \"[$(date +%T)] [$level] $msg\"\n"
            "  }\n"
            "  ist_root() {\n"
            "      [ $(id -u) -eq 0 ]\n"
            "  }\n"
            "  ist_root && log INFO 'Running as root' || log WARN 'Not root'"
        ),
        syntax       = "func() { ... }  |  local VAR=wert  |  return N  |  VAR=$(func)",
        example      = (
            "#!/bin/bash\n"
            "# Logging-Funktion\n"
            "log() {\n"
            "    local level=${1:-INFO}\n"
            "    local msg=${2:-''}\n"
            "    echo \"[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg\"\n"
            "}\n\n"
            "# Prüf-Funktion\n"
            "datei_ok() {\n"
            "    local datei=$1\n"
            "    [ -f \"$datei\" ] && [ -r \"$datei\" ]\n"
            "    return $?\n"
            "}\n\n"
            "if datei_ok '/etc/passwd'; then\n"
            "    log INFO 'Datei vorhanden'\n"
            "else\n"
            "    log ERROR 'Datei fehlt'\n"
            "fi"
        ),
        task_description = "Zeige alle definierten Shell-Funktionen mit declare",
        expected_commands = ["declare -f"],
        hint_text    = "declare -f zeigt alle definierten Shell-Funktionen mit ihrem vollständigen Code",
        quiz_questions = [
            QuizQuestion(
                question   = "Was passiert wenn man 'local' in einer Bash-Funktion NICHT verwendet?",
                options    = [
                    "Die Variable ist nur innerhalb der Funktion sichtbar",
                    "Die Variable wird automatisch read-only",
                    "Die Variable ist global und kann andere Variablen überschreiben",
                    "Bash erzeugt einen Fehler und bricht ab",
                ],
                correct    = 2,
                explanation = (
                    "Ohne 'local' ist eine Variable in einer Funktion global.\n"
                    "Das kann unbeabsichtigt externe Variablen überschreiben.\n"
                    "Best Practice: Immer 'local' für Funktions-interne Variablen verwenden."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie gibt eine Bash-Funktion einen STRING-Wert (nicht Exit-Code) zurück?",
                options    = [
                    "return 'mein_wert'",
                    "echo 'mein_wert' und den Aufruf in $() einschließen",
                    "export RETURN_VALUE='mein_wert'",
                    "yield 'mein_wert'",
                ],
                correct    = 1,
                explanation = (
                    "return kann nur Exit-Codes (0-255) zurückgeben.\n"
                    "Für String-Rückgabe: echo in der Funktion und Aufruf mit $():\n"
                    "  get_name() { echo 'Ghost'; }\n"
                    "  NAME=$(get_name)   # NAME='Ghost'"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "FUNKTIONEN MERKE:\n"
            "  Zwei Syntaxen: function foo { } und foo() { }\n"
            "  local = lokale Variable (kein Scope-Leak)\n"
            "  return = Exit-Code (0-255)\n"
            "  Wert zurückgeben: echo + $()-Substitution\n"
            "  Aufruf OHNE Klammern: foo arg1 arg2"
        ),
        memory_tip   = "Merkhilfe: local=lokal-im-Scope, return=exit-code, echo+$()=wert-zurück",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.10 — Fehlerbehandlung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.10",
        chapter      = 14,
        title        = "Fehlerbehandlung — set -e, set -u, trap, Exit-Codes",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Das Backup-Skript lief durch — und überschrieb Produktionsdaten.\n"
            " Kein Fehler-Abbruch. Keine Prüfung. Keine Trap.\n"
            " set -euo pipefail, Ghost. Die Dreifaltigkeit der Skript-Sicherheit.\n"
            " Fehler fangen — bevor sie Schaden anrichten.'"
        ),
        why_important = (
            "Robuste Fehlerbehandlung ist der Unterschied zwischen Hobby-Skript\n"
            "und Production-Code. LPIC-1 Topic 105.2 prüft set-Optionen und trap."
        ),
        explanation  = (
            "FEHLERBEHANDLUNG IN BASH:\n\n"
            "SET-OPTIONEN:\n"
            "  set -e           Bei Fehler sofort beenden (exit on error)\n"
            "  set -u           Ungesetzte Variablen als Fehler behandeln\n"
            "  set -o pipefail  Fehler in Pipelines nicht ignorieren\n"
            "  set -x           Jeden Befehl vor Ausführung ausgeben (debug)\n"
            "  set -n           Befehle nur parsen, nicht ausführen\n"
            "  set +e           set -e deaktivieren\n\n"
            "KOMBINATION (Empfehlung):\n"
            "  #!/bin/bash\n"
            "  set -euo pipefail\n\n"
            "TRAP — SIGNALE UND EXIT ABFANGEN:\n"
            "  trap 'BEFEHL' SIGNAL     Trap registrieren\n"
            "  trap 'echo Fehler!' ERR  bei Fehler (wenn -e aktiv)\n"
            "  trap 'cleanup' EXIT      beim Beenden\n"
            "  trap 'echo CTRL+C' INT   bei Ctrl+C\n"
            "  trap '' TERM            Signal ignorieren\n"
            "  trap - EXIT             Trap entfernen\n\n"
            "CLEANUP-PATTERN:\n"
            "  TMPFILE=$(mktemp)\n"
            "  trap 'rm -f $TMPFILE' EXIT\n"
            "  # Temp-Datei wird IMMER gelöscht, auch bei Fehler!\n\n"
            "EXIT-CODES PRÜFEN:\n"
            "  command || { echo 'Fehler!'; exit 1; }\n"
            "  if ! command; then echo 'Fehler'; fi\n"
            "  command; [ $? -eq 0 ] || exit 1\n\n"
            "STANDARDISIERTE EXIT-CODES:\n"
            "  0   = Erfolg\n"
            "  1   = Allgemeiner Fehler\n"
            "  2   = Missbrauch von Shell-Builtins\n"
            "  126 = Befehl nicht ausführbar\n"
            "  127 = Befehl nicht gefunden\n"
            "  128+N = Signal N empfangen (z.B. 130 = Ctrl+C)"
        ),
        syntax       = "set -euo pipefail  |  trap 'BEFEHL' SIGNAL  |  command || exit 1",
        example      = (
            "#!/bin/bash\n"
            "set -euo pipefail\n\n"
            "# Cleanup bei Beenden\n"
            "TMPDIR=$(mktemp -d)\n"
            "trap 'rm -rf $TMPDIR; echo Cleanup erledigt' EXIT\n\n"
            "# Fehler abfangen\n"
            "if ! cp /etc/passwd \"$TMPDIR/\"; then\n"
            "    echo 'Fehler beim Kopieren' >&2\n"
            "    exit 1\n"
            "fi\n\n"
            "echo 'Erfolg'\n"
            "exit 0"
        ),
        task_description = "Welche set-Option bewirkt dass ungesetzte Variablen einen Fehler verursachen?",
        expected_commands = ["set -u"],
        hint_text    = "set -u (oder set -o nounset) behandelt ungesetzte Variablen als Fehler",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt 'set -e' in einem Bash-Skript?",
                options    = [
                    "Das Skript gibt jeden Befehl vor Ausführung aus",
                    "Das Skript beendet sich sofort wenn ein Befehl fehlschlägt",
                    "Ungesetzte Variablen verursachen einen Fehler",
                    "Fehler in Pipelines werden erkannt",
                ],
                correct    = 1,
                explanation = (
                    "set -e (errexit) beendet das Skript sofort wenn ein Befehl\n"
                    "einen Non-Zero Exit-Code zurückgibt.\n"
                    "set -u = unset variables as error\n"
                    "set -o pipefail = Pipe-Fehler erkennen\n"
                    "set -x = xtrace (debug)"
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie stellt man sicher, dass eine temporäre Datei IMMER gelöscht wird, auch bei Fehlern?",
                options    = [
                    "Datei am Ende des Skripts manuell löschen",
                    "trap 'rm -f $TMPFILE' EXIT verwenden",
                    "TMPFILE in /dev/shm anlegen",
                    "set -e vor der Datei-Erstellung",
                ],
                correct    = 1,
                explanation = (
                    "trap 'BEFEHL' EXIT wird immer ausgeführt wenn das Skript endet —\n"
                    "egal ob normal, durch Fehler oder durch Signal.\n"
                    "Cleanup-Pattern: TMPFILE=$(mktemp) && trap 'rm -f $TMPFILE' EXIT"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "set OPTIONEN MERKE:\n"
            "  -e = exit on error\n"
            "  -u = unset = error\n"
            "  -o pipefail = Pipe-Fehler\n"
            "  -x = xtrace (debug)\n"
            "  -n = noexec (syntax check)\n"
            "trap EXIT = Cleanup-Handler"
        ),
        memory_tip   = "Merkhilfe: set -euo pipefail = professionelles Bash-Sicherheitsnetz",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.11 — Argumente & Parameter
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.11",
        chapter      = 14,
        title        = "Argumente & Parameter — $0..$9, $@, $*, $#, shift",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "RUST: 'Das Skript akzeptiert keine Argumente, Ghost.\n"
            " $1 ist leer. $# ist null. Der User bekommt keinen Hinweis.\n"
            " Positionsparameter, shift, $@ vs $* — lern den Unterschied.\n"
            " Dann schreib Skripte die echte Eingaben verarbeiten.'"
        ),
        why_important = (
            "Positionsparameter und shift sind Kernelement jedes Bash-Skripts.\n"
            "LPIC-1 prüft $@, $* und shift regelmäßig."
        ),
        explanation  = (
            "POSITIONSPARAMETER:\n\n"
            "  $0    Skriptname (oder Shell-Name)\n"
            "  $1    erstes Argument\n"
            "  $2    zweites Argument\n"
            "  ${10} zehntes Argument (geschweifte Klammern ab $10!)\n\n"
            "SPEZIELLE PARAMETER:\n"
            "  $#    Anzahl der Argumente\n"
            "  $@    alle Argumente als separate Strings (sicher!)\n"
            "  $*    alle Argumente als ein einzelner String\n"
            "  $?    Exit-Code des letzten Befehls\n"
            "  $$    PID des aktuellen Prozesses\n"
            "  $!    PID des letzten Hintergrundprozesses\n\n"
            "$@ VS $* IN ANFÜHRUNGSZEICHEN:\n"
            "  \"$@\" → 'arg1' 'arg 2' 'arg3'  (sicher, separiert)\n"
            "  \"$*\" → 'arg1 arg 2 arg3'       (alles ein String)\n"
            "  → Immer \"$@\" für Argument-Weiterleitung verwenden!\n\n"
            "SHIFT:\n"
            "  shift      $1 löschen, alle nach links verschieben\n"
            "  shift 2    zwei Argumente löschen\n"
            "  $1 wird zum nächsten Argument nach dem Shift\n\n"
            "ARGUMENTE VERARBEITEN:\n"
            "  # Alle Argumente durchgehen:\n"
            "  for ARG in \"$@\"; do\n"
            "      echo \"Argument: $ARG\"\n"
            "  done\n\n"
            "  # Mit while/shift:\n"
            "  while [ $# -gt 0 ]; do\n"
            "      echo \"Nächstes: $1\"\n"
            "      shift\n"
            "  done\n\n"
            "SONDERFALL basename/dirname:\n"
            "  basename $0     nur Dateiname (ohne Pfad)\n"
            "  dirname $0      nur Verzeichnis"
        ),
        syntax       = "$1 $2 $# $@ $*  |  shift [N]  |  for ARG in \"$@\"",
        example      = (
            "#!/bin/bash\n"
            "# Argument-Prüfung\n"
            "if [ $# -lt 2 ]; then\n"
            "    echo \"Verwendung: $0 QUELLE ZIEL\"\n"
            "    exit 1\n"
            "fi\n\n"
            "QUELLE=$1\n"
            "ZIEL=$2\n"
            "shift 2\n"
            "echo \"Restliche Argumente: $@\"\n\n"
            "# Alle Argumente sicher iterieren:\n"
            "for DATEI in \"$@\"; do\n"
            "    echo \"Verarbeite: $DATEI\"\n"
            "done"
        ),
        task_description = "Wie viele Argumente wurden an das aktuelle Skript übergeben? Zeige $# an",
        expected_commands = ["echo $#"],
        hint_text    = "$# enthält die Anzahl der an das Skript übergebenen Argumente",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen \"$@\" und \"$*\" in doppelten Anführungszeichen?",
                options    = [
                    "Kein Unterschied — beide sind identisch",
                    "\"$@\" erhält jeden Argument als separaten String, \"$*\" verbindet alle zu einem",
                    "\"$*\" ist POSIX-kompatibel, \"$@\" nur Bash",
                    "\"$@\" enthält Anzahl der Argumente, \"$*\" alle Argumente",
                ],
                correct    = 1,
                explanation = (
                    "In Anführungszeichen ist der Unterschied kritisch:\n"
                    "  \"$@\" → Argumente einzeln (z.B. 'a' 'b c' 'd')\n"
                    "  \"$*\" → Ein String (z.B. 'a b c d')\n"
                    "Für korrekte Weiterleitung von Argumenten: immer \"$@\" verwenden!"
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was macht 'shift 2' in einem Bash-Skript?",
                options    = [
                    "Die ersten zwei Argumente werden verdoppelt",
                    "Zwei Argumente werden vom Anfang der Parameterliste entfernt",
                    "Die Parameterliste wird um zwei Positionen nach rechts verschoben",
                    "Das Skript beendet sich wenn weniger als 2 Argumente vorhanden sind",
                ],
                correct    = 1,
                explanation = (
                    "shift N entfernt die ersten N Argumente.\n"
                    "Nach shift 2: altes $3 → $1, altes $4 → $2, etc.\n"
                    "$# wird um N reduziert.\n"
                    "Nützlich nach getopts um Optionen zu entfernen."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "PARAMETER MERKE:\n"
            "  $0=Skriptname, $1..$9=Argumente, ${10}+=geschweifte Klammern\n"
            "  $#=Anzahl, $@=alle(sicher), $*=alle(als-ein-string)\n"
            "  $?=exit-code, $$=PID, $!=Hintergrund-PID\n"
            "  shift = Argumente von links entfernen\n"
            "  \"$@\" IMMER in Anführungszeichen!"
        ),
        memory_tip   = "Merkhilfe: $#=hash-count, $@=at-all-separate, $*=star-all-one, $$=dollar-pid",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.12 — String-Operationen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.12",
        chapter      = 14,
        title        = "String-Operationen — ${#var}, Substring, Ersetzung, Case",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Dateiname ohne Extension. URL ohne Schema. IP ohne Port.\n"
            " String-Manipulation direkt in Bash — keine externen Tools.\n"
            " ${var:pos:len}, ${var/old/new}, ${var^^} — pure Bash-Power.\n"
            " Schneller als sed, ohne Fork. Lern es.'"
        ),
        why_important = (
            "Bash-interne String-Operationen sind schneller als externe Tools.\n"
            "LPIC-1 prüft Parameter-Expansion und String-Manipulation."
        ),
        explanation  = (
            "BASH STRING-OPERATIONEN:\n\n"
            "LÄNGE:\n"
            "  ${#VAR}              Länge des Strings\n"
            "  ${#ARRAY[@]}         Anzahl Array-Elemente\n\n"
            "SUBSTRING:\n"
            "  ${VAR:POS}           ab Position POS bis Ende\n"
            "  ${VAR:POS:LEN}       LEN Zeichen ab Position POS\n"
            "  ${VAR: -3}           letzten 3 Zeichen (Leerzeichen vor -!)\n\n"
            "PRÄFIX/SUFFIX ENTFERNEN:\n"
            "  ${VAR#MUSTER}        kürzestes Präfix entfernen\n"
            "  ${VAR##MUSTER}       längstes Präfix entfernen\n"
            "  ${VAR%MUSTER}        kürzestes Suffix entfernen\n"
            "  ${VAR%%MUSTER}       längstes Suffix entfernen\n\n"
            "BEISPIELE:\n"
            "  DATEI='/var/log/syslog.gz'\n"
            "  ${DATEI##*/}         → 'syslog.gz'  (nur Dateiname)\n"
            "  ${DATEI%.*}          → '/var/log/syslog'  (ohne Extension)\n"
            "  ${DATEI##*.}         → 'gz'  (nur Extension)\n\n"
            "ERSETZEN:\n"
            "  ${VAR/alt/neu}       erste Ersetzung\n"
            "  ${VAR//alt/neu}      alle Ersetzungen\n"
            "  ${VAR/#alt/neu}      Ersetzung am Anfang\n"
            "  ${VAR/%alt/neu}      Ersetzung am Ende\n\n"
            "GROSS/KLEIN:\n"
            "  ${VAR^^}             alles Großbuchstaben\n"
            "  ${VAR,,}             alles Kleinbuchstaben\n"
            "  ${VAR^}              ersten Buchstaben groß\n"
            "  ${VAR,}              ersten Buchstaben klein\n\n"
            "STANDARD-WERTE:\n"
            "  ${VAR:-default}      Wert oder 'default' wenn leer\n"
            "  ${VAR:=default}      Wert setzen wenn leer\n"
            "  ${VAR:?Fehlermsg}    Fehler wenn leer"
        ),
        syntax       = "${#VAR}  |  ${VAR:POS:LEN}  |  ${VAR/alt/neu}  |  ${VAR^^}",
        example      = (
            "STR='Hallo NeonGrid-9'\n"
            "echo ${#STR}           # Länge: 17\n"
            "echo ${STR:6}          # 'NeonGrid-9'\n"
            "echo ${STR:6:8}        # 'NeonGrid'\n"
            "echo ${STR/Hallo/Bye}  # 'Bye NeonGrid-9'\n"
            "echo ${STR^^}          # 'HALLO NEONGRID-9'\n"
            "echo ${STR,,}          # 'hallo neongrid-9'\n\n"
            "DATEI='backup.tar.gz'\n"
            "echo ${DATEI%%.*}      # 'backup' (alles nach . entfernt)\n"
            "echo ${DATEI##*.}      # 'gz' (alles bis letztem . entfernt)"
        ),
        task_description = "Zeige die Länge des Strings 'NeonGrid-9' mit Bash-String-Expansion",
        expected_commands = ["echo ${#STR}"],
        hint_text    = "${#VAR} gibt die Länge des Strings in VAR zurück",
        quiz_questions = [
            QuizQuestion(
                question   = "Was gibt '${DATEI##*/}' zurück wenn DATEI='/home/ghost/skript.sh'?",
                options    = [
                    "/home/ghost/",
                    "skript.sh",
                    "skript",
                    ".sh",
                ],
                correct    = 1,
                explanation = (
                    "${VAR##MUSTER} entfernt den LÄNGSTEN Treffer des Musters vom Anfang.\n"
                    "*/ matcht alles bis zum letzten /\n"
                    "Ergebnis: nur der Dateiname ohne Pfad ('skript.sh')\n"
                    "Äquivalent zu: basename /home/ghost/skript.sh"
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was macht ${VAR^^} in Bash?",
                options    = [
                    "Gibt die Länge von VAR zurück",
                    "Konvertiert VAR in Großbuchstaben",
                    "Verdoppelt den Inhalt von VAR",
                    "Entfernt Leerzeichen aus VAR",
                ],
                correct    = 1,
                explanation = (
                    "${VAR^^} konvertiert alle Zeichen in VAR zu Großbuchstaben.\n"
                    "${VAR,,} = Kleinbuchstaben\n"
                    "${VAR^} = nur ersten Buchstaben groß\n"
                    "${#VAR} = Länge von VAR"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "STRING-OPS MERKE:\n"
            "  ${#V} = Länge\n"
            "  ${V:p:l} = Substring (pos, len)\n"
            "  ${V/a/b} = einmalig ersetzen\n"
            "  ${V//a/b} = alle ersetzen\n"
            "  ${V^^} = GROSS, ${V,,} = klein\n"
            "  ${V##*/} = Dateiname, ${V%.*} = ohne Extension"
        ),
        memory_tip   = "Merkhilfe: # am Anfang entfernen, % am Ende entfernen, ## und %% = längste Übereinstimmung",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.13 — Reguläre Ausdrücke in Bash
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.13",
        chapter      = 14,
        title        = "Reguläre Ausdrücke in Bash — [[ =~ ]] und BASH_REMATCH",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "RUST",
        story        = (
            "RUST: 'Validiere die IP-Adresse. Prüfe das Datum. Parse den Log.\n"
            " grep wäre ein Fork. [[ =~ ]] ist eingebaut.\n"
            " BASH_REMATCH speichert die Gruppen.\n"
            " Kein externes Tool — pure Bash-Regex-Power.'"
        ),
        why_important = (
            "Bash-interne Regex-Unterstützung mit [[ =~ ]] ist schnell und mächtig.\n"
            "LPIC-1 Topic 105.2 prüft Regex-Matching und Capture-Groups."
        ),
        explanation  = (
            "REGEX IN BASH:\n\n"
            "[[ STRING =~ REGEX ]]:\n"
            "  Regex-Matching direkt in Bash (kein grep nötig)\n"
            "  Gibt 0 zurück wenn Regex passt (true)\n"
            "  Gibt 1 zurück wenn kein Match (false)\n"
            "  Extended POSIX Regex (ERE) — wie grep -E\n\n"
            "WICHTIG: Regex NICHT in Anführungszeichen!\n"
            "  [[ \"$VAR\" =~ ^[0-9]+$ ]]     ✓  KORREKT\n"
            "  [[ \"$VAR\" =~ '^[0-9]+$' ]]   ✗  Literal-String!\n\n"
            "BASH_REMATCH:\n"
            "  ${BASH_REMATCH[0]}  vollständiger Match\n"
            "  ${BASH_REMATCH[1]}  erste Capture-Gruppe ()\n"
            "  ${BASH_REMATCH[2]}  zweite Capture-Gruppe\n\n"
            "REGEX-GRUNDLAGEN:\n"
            "  ^      Zeilenanfang\n"
            "  $      Zeilenende\n"
            "  .      beliebiges Zeichen\n"
            "  *      0 oder mehr\n"
            "  +      1 oder mehr\n"
            "  ?      0 oder 1\n"
            "  [abc]  Zeichenklasse\n"
            "  [0-9]  Bereich\n"
            "  [^x]   nicht x\n"
            "  (ab)   Gruppe (Capture)\n"
            "  a|b    a oder b\n\n"
            "BEISPIELE:\n"
            "  # IP-Adresse validieren (vereinfacht):\n"
            "  if [[ \"$IP\" =~ ^([0-9]{1,3}\\.){3}[0-9]{1,3}$ ]]; then\n"
            "      echo 'Gültige IP'\n"
            "  fi\n\n"
            "  # Datum parsen:\n"
            "  DATUM='2024-03-15'\n"
            "  if [[ \"$DATUM\" =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]; then\n"
            "      JAHR=${BASH_REMATCH[1]}\n"
            "      MONAT=${BASH_REMATCH[2]}\n"
            "      TAG=${BASH_REMATCH[3]}\n"
            "  fi"
        ),
        syntax       = "[[ \"$VAR\" =~ REGEX ]]  |  ${BASH_REMATCH[0]}  |  ${BASH_REMATCH[1]}",
        example      = (
            "#!/bin/bash\n"
            "EMAIL='ghost@neongrid9.net'\n\n"
            "if [[ \"$EMAIL\" =~ ^([^@]+)@([^@]+)$ ]]; then\n"
            "    echo \"Vollständig: ${BASH_REMATCH[0]}\"\n"
            "    echo \"User:        ${BASH_REMATCH[1]}\"\n"
            "    echo \"Domain:      ${BASH_REMATCH[2]}\"\n"
            "else\n"
            "    echo 'Ungültige E-Mail'\n"
            "fi\n\n"
            "# Nur Zahlen prüfen:\n"
            "WERT='42'\n"
            "[[ \"$WERT\" =~ ^[0-9]+$ ]] && echo 'Ist eine Zahl'"
        ),
        task_description = "Prüfe ob die Variable WERT='12345' nur Ziffern enthält mit [[ =~ ]]",
        expected_commands = ["[[ \"$WERT\" =~ ^[0-9]+$ ]] && echo 'ja'"],
        hint_text    = "[[ \"$VAR\" =~ ^[0-9]+$ ]] prüft ob VAR nur Ziffern enthält. Regex nicht in Anführungszeichen!",
        quiz_questions = [
            QuizQuestion(
                question   = "Welches Array enthält die Capture-Gruppen nach einem erfolgreichen Regex-Match in Bash?",
                options    = [
                    "$REGEX_MATCH",
                    "BASH_REMATCH",
                    "$MATCHES",
                    "REGEX_GROUPS",
                ],
                correct    = 1,
                explanation = (
                    "BASH_REMATCH ist ein automatisch befülltes Array nach [[ =~ ]].\n"
                    "  ${BASH_REMATCH[0]} = vollständiger Match\n"
                    "  ${BASH_REMATCH[1]} = erste Gruppe () \n"
                    "  ${BASH_REMATCH[2]} = zweite Gruppe ()\n"
                    "BASH_REMATCH ist read-only und wird bei jedem [[ =~ ]] überschrieben."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Warum sollte die Regex in [[ \"$VAR\" =~ REGEX ]] NICHT in Anführungszeichen stehen?",
                options    = [
                    "Weil Anführungszeichen die Performance verschlechtern",
                    "Weil die Regex dann als literaler String und nicht als Regex behandelt wird",
                    "Weil Anführungszeichen in Bash verboten sind",
                    "Weil sonst BASH_REMATCH nicht befüllt wird",
                ],
                correct    = 1,
                explanation = (
                    "In [[ =~ ]], wenn die Regex in Anführungszeichen steht,\n"
                    "behandelt Bash sie als literalen String, nicht als Regex.\n"
                    "  [[ \"hallo\" =~ 'ha.*' ]]  → false (Literal-Match)\n"
                    "  [[ \"hallo\" =~ ha.* ]]    → true (Regex-Match)"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "BASH REGEX MERKE:\n"
            "  [[ \"$VAR\" =~ REGEX ]] = Bash-interne Regex\n"
            "  BASH_REMATCH[0] = gesamter Match\n"
            "  BASH_REMATCH[1] = erste Capture-Gruppe\n"
            "  Regex NICHT in Quotes (sonst Literal-String)\n"
            "  ERE-Syntax (wie grep -E)"
        ),
        memory_tip   = "Merkhilfe: =~ bedeutet RE-Match | BASH_REMATCH[1] = erste Klammer-Gruppe",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.14 — Debugging
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.14",
        chapter      = 14,
        title        = "Debugging — bash -x, set -x/+x, PS4",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Das Skript läuft durch aber das Ergebnis ist falsch.\n"
            " Kein Fehler. Kein Exit-Code. Nur falsches Verhalten.\n"
            " bash -x zeigt jeden Befehl vor Ausführung.\n"
            " Setze PS4 für Zeilennummern. Debug wie ein Profi.'"
        ),
        why_important = (
            "Bash-Debugging ist LPIC-1-Prüfungsstoff.\n"
            "bash -x und set -x sind die wichtigsten Diagnose-Werkzeuge."
        ),
        explanation  = (
            "BASH DEBUGGING:\n\n"
            "DEBUGMODUS STARTEN:\n"
            "  bash -x skript.sh        jeden Befehl vor Ausführung zeigen\n"
            "  bash -v skript.sh        Zeilen wie gelesen ausgeben\n"
            "  bash -n skript.sh        Syntax prüfen (kein Ausführen)\n"
            "  bash -xv skript.sh       beides kombiniert\n\n"
            "IM SKRIPT:\n"
            "  set -x           Debug-Modus einschalten\n"
            "  set +x           Debug-Modus ausschalten\n"
            "  set -v           Verbose (Zeilen ausgeben wie gelesen)\n"
            "  set +v           Verbose ausschalten\n\n"
            "NUR TEIL-SKRIPT DEBUGGEN:\n"
            "  #!/bin/bash\n"
            "  set -x           # ab hier debuggen\n"
            "  PROBLEMATISCHER_CODE\n"
            "  set +x           # Ende des Debug-Bereichs\n\n"
            "PS4 — DEBUG-PROMPT ANPASSEN:\n"
            "  Standard-PS4: '+'\n"
            "  PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'\n"
            "  Zeigt: Dateiname, Zeilennummer, Funktionsname\n\n"
            "DEBUG-AUSGABE LESEN:\n"
            "  + echo Hallo    (+ = einmal ausgeführt)\n"
            "  ++ date         (++ = Subshell)\n"
            "  +++ func        (+++ = Subshell der Subshell)\n\n"
            "WEITERE DEBUGGING-TECHNIKEN:\n"
            "  echo \"DEBUG: VAR=$VAR\" >&2   manuelles Logging\n"
            "  trap 'echo \"Fehler in $LINENO\"' ERR   Fehler-Trap\n"
            "  LINENO   aktuelle Zeilennummer\n"
            "  BASH_SOURCE  aktuelle Skript-Datei\n"
            "  FUNCNAME[0]  aktuelle Funktionsname"
        ),
        syntax       = "bash -x skript.sh  |  set -x  |  set +x  |  PS4='...'",
        example      = (
            "#!/bin/bash\n"
            "PS4='+(${BASH_SOURCE[0]}:${LINENO}): '\n\n"
            "set -x   # Debug an\n"
            "WERT=42\n"
            "if [ $WERT -gt 40 ]; then\n"
            "    echo 'Groß'\n"
            "fi\n"
            "set +x   # Debug aus\n"
            "echo 'Kein Debug hier mehr'"
        ),
        task_description = "Aktiviere den Debug-Modus in der aktuellen Shell",
        expected_commands = ["set -x"],
        hint_text    = "set -x aktiviert den Bash-Debug-Modus — jeder Befehl wird vor Ausführung mit '+' ausgegeben",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt 'bash -n skript.sh'?",
                options    = [
                    "Das Skript wird mit Debug-Ausgabe ausgeführt",
                    "Das Skript wird auf Syntax-Fehler geprüft ohne ausgeführt zu werden",
                    "Das Skript wird ohne Ausgabe ausgeführt (silent mode)",
                    "Das Skript wird im Non-interactive Modus ausgeführt",
                ],
                correct    = 1,
                explanation = (
                    "bash -n (noexec) prüft die Syntax des Skripts ohne es auszuführen.\n"
                    "Nützlich für CI/CD: Syntax-Check vor Deployment.\n"
                    "bash -x = xtrace (debug)\n"
                    "bash -v = verbose (Zeilen ausgeben)"
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was bedeutet '++' am Anfang einer Debug-Zeile bei bash -x?",
                options    = [
                    "Der Befehl wurde zweimal ausgeführt",
                    "Der Befehl läuft in einer Subshell (eine Ebene tiefer)",
                    "Der Befehl war ein Fehler",
                    "Der Befehl ist ein Builtin",
                ],
                correct    = 1,
                explanation = (
                    "PS4 zeigt die Shell-Tiefe mit +-Zeichen:\n"
                    "  + = direkte Shell\n"
                    "  ++ = Subshell (z.B. $() Command Substitution)\n"
                    "  +++ = Subshell der Subshell\n"
                    "Nützlich um verschachtelte Ausführungen zu verfolgen."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "DEBUGGING MERKE:\n"
            "  bash -x = xtrace (jeden Befehl ausgeben)\n"
            "  bash -n = noexec (syntax check)\n"
            "  bash -v = verbose (Zeilen wie gelesen)\n"
            "  set -x / set +x = debug an/aus\n"
            "  PS4 = Debug-Prompt (Standard: '+')\n"
            "  LINENO = aktuelle Zeilennummer"
        ),
        memory_tip   = "Merkhilfe: bash -x=execute-trace, -n=no-execute, -v=verbose | set -x=an, set +x=aus",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.15 — Skript-Best-Practices
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.15",
        chapter      = 14,
        title        = "Skript-Best-Practices — Shebang, chmod, Fehlerprüfung",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "RUST: 'Dein Skript läuft nur auf deinem Rechner, Ghost.\n"
            " Kein Shebang. Kein chmod. Keine Kommentare.\n"
            " Auf dem Server: Permission denied. Syntax error.\n"
            " Best Practices sind kein Komfort — sie sind Pflicht.'"
        ),
        why_important = (
            "Saubere Bash-Skripte sind wartbar, portabel und sicher.\n"
            "LPIC-1 prüft Shebang-Varianten, Berechtigungen und Fehlerprüfung."
        ),
        explanation  = (
            "BASH SKRIPT BEST PRACTICES:\n\n"
            "1. SHEBANG (erste Zeile):\n"
            "  #!/bin/bash           absoluter Pfad (üblich)\n"
            "  #!/usr/bin/env bash   flexibel (empfohlen für Portabilität)\n"
            "  #!/bin/sh             POSIX-kompatibel (keine Bash-Extras)\n"
            "  Shebang MUSS die allererste Zeile sein!\n\n"
            "2. FEHLERBEHANDLUNG:\n"
            "  set -euo pipefail     Fehlersicherheit aktivieren\n"
            "  Immer Rückgabecodes prüfen\n\n"
            "3. AUSFÜHRBAR MACHEN:\n"
            "  chmod +x skript.sh    execute-Bit setzen\n"
            "  chmod 755 skript.sh   rwxr-xr-x\n"
            "  chmod 700 skript.sh   rwx------ (nur Eigentümer)\n\n"
            "4. VARIABLEN-SICHERHEIT:\n"
            "  Variablen immer in \"Anführungszeichen\"\n"
            "  \"$VAR\" statt $VAR (verhindert Word-Splitting)\n"
            "  local in Funktionen verwenden\n\n"
            "5. KOMMENTARE:\n"
            "  #!/bin/bash\n"
            "  # Autor: Ghost\n"
            "  # Datum: 2024-01-15\n"
            "  # Beschreibung: Backup-Skript für /etc\n"
            "  # Verwendung: ./backup.sh [ZIELVERZEICHNIS]\n\n"
            "6. EINGABE VALIDIEREN:\n"
            "  [ $# -lt 1 ] && { echo \"Fehler: Argument fehlt\" >&2; exit 1; }\n\n"
            "7. FEHLERMELDUNGEN AUF STDERR:\n"
            "  echo 'Fehler!' >&2    auf STDERR ausgeben\n\n"
            "8. MKTEMP FÜR TEMP-DATEIEN:\n"
            "  TMPFILE=$(mktemp)\n"
            "  trap 'rm -f $TMPFILE' EXIT\n\n"
            "9. READONLY FÜR KONSTANTEN:\n"
            "  readonly KONFIG='/etc/app/config.conf'\n\n"
            "10. POSIX-PORTABILITÄT:\n"
            "  #!/bin/sh statt #!/bin/bash wenn portabel\n"
            "  Keine Bash-spezifischen Features (arrays, [[, etc.)"
        ),
        syntax       = "#!/bin/bash  |  set -euo pipefail  |  chmod +x  |  echo 'Fehler' >&2",
        example      = (
            "#!/usr/bin/env bash\n"
            "# Skript: cleanup.sh\n"
            "# Bereinigt temporäre Dateien\n"
            "set -euo pipefail\n\n"
            "readonly ZIEL=${1:-/tmp}\n"
            "readonly TAGE=${2:-30}\n\n"
            "[ -d \"$ZIEL\" ] || { echo \"Fehler: $ZIEL existiert nicht\" >&2; exit 1; }\n\n"
            "TMPLOG=$(mktemp)\n"
            "trap 'rm -f $TMPLOG' EXIT\n\n"
            "find \"$ZIEL\" -type f -mtime +\"$TAGE\" -delete -print > \"$TMPLOG\"\n"
            "echo \"Gelöscht: $(wc -l < $TMPLOG) Dateien\""
        ),
        task_description = "Mache das Skript deploy.sh ausführbar für alle (chmod 755)",
        expected_commands = ["chmod 755 deploy.sh"],
        hint_text    = "chmod 755 setzt rwxr-xr-x — Eigentümer kann lesen/schreiben/ausführen, alle anderen lesen/ausführen",
        quiz_questions = [
            QuizQuestion(
                question   = "Warum ist '#!/usr/bin/env bash' besser als '#!/bin/bash' als Shebang?",
                options    = [
                    "Es ist schneller als der absolute Pfad",
                    "Es findet bash flexibel über PATH — portabler auf verschiedenen Systemen",
                    "Es aktiviert automatisch set -euo pipefail",
                    "Es ist POSIX-kompatibler als #!/bin/bash",
                ],
                correct    = 1,
                explanation = (
                    "#!/usr/bin/env bash sucht bash im PATH.\n"
                    "Auf macOS liegt bash oft in /usr/local/bin, nicht /bin.\n"
                    "#!/bin/bash schlägt dann fehl.\n"
                    "env bash findet es in allen Fällen (wenn im PATH)."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wohin gehören Fehlermeldungen in einem Bash-Skript?",
                options    = [
                    "Immer nach /var/log/syslog",
                    "Auf STDERR mit echo 'Fehler' >&2",
                    "In eine Logdatei mit >> logfile",
                    "In die Systemd-Journal via logger",
                ],
                correct    = 1,
                explanation = (
                    "Fehlermeldungen gehören auf STDERR (File Descriptor 2).\n"
                    "echo 'Fehler' >&2 leitet auf STDERR um.\n"
                    "So können normale Ausgabe (STDOUT) und Fehler\n"
                    "unabhängig voneinander umgeleitet werden:\n"
                    "  ./skript.sh 2>fehler.log | verarbeitung"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "BEST PRACTICES MERKE:\n"
            "  Shebang = erste Zeile, #!/bin/bash oder #!/usr/bin/env bash\n"
            "  set -euo pipefail = Sicherheitsnetz\n"
            "  chmod +x = ausführbar machen\n"
            "  \"$VAR\" = immer in Quotes\n"
            "  echo >&2 = Fehler auf STDERR\n"
            "  mktemp + trap EXIT = sichere Temp-Dateien"
        ),
        memory_tip   = "Merkhilfe: Shebang+set-euo+chmod+Quotes+STDERR = das Basis-Gerüst jeden guten Skripts",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.16 — Heredoc & Herestring
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.16",
        chapter      = 14,
        title        = "Heredoc & Herestring — Multi-Line Input in Bash",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Du willst einen Config-Block in eine Datei schreiben, Ghost.\n"
            " Ohne Echo-Chaos. Ohne Anführungszeichen-Hölle.\n"
            " Heredoc macht es sauber. <<EOF bis EOF.\n"
            " Einrückung? <<-EOF für Tab-Stripping.'"
        ),
        why_important = (
            "Heredoc ist LPIC-1 Topic 105.2 Prüfungsstoff.\n"
            "Unentbehrlich für Konfigurationsdateien per Skript schreiben.\n"
            "<<'EOF' verhindert Variablen-Expansion — sicherheitskritisch."
        ),
        explanation  = (
            "HEREDOC — MEHRZEILIGE EINGABE:\n\n"
            "SYNTAX:\n"
            "  command <<DELIMITER\n"
            "  content\n"
            "  DELIMITER\n\n"
            "VARIANTEN:\n"
            "  <<EOF         Variablen werden expandiert\n"
            "  <<'EOF'       KEIN Expand (literaler Text)\n"
            "  <<-EOF        führende TABS werden entfernt\n"
            "  <<-'EOF'      kein Expand + Tab-Stripping\n\n"
            "BEISPIELE:\n"
            "  cat <<EOF\n"
            "  Hostname: $HOSTNAME\n"
            "  User: $USER\n"
            "  EOF\n\n"
            "  ssh user@host <<'EOF'\n"
            "  echo 'no expansion here'\n"
            "  EOF\n\n"
            "  sudo tee /etc/config.conf <<EOF\n"
            "  [settings]\n"
            "  key=value\n"
            "  EOF\n\n"
            "HERESTRING (<<<):\n"
            "  bc <<< '2+2'           Einzeiliger String als stdin\n"
            "  read a b <<< 'foo bar' Variablen aus String füllen\n"
            "  grep pattern <<< \"$var\"  Variable als stdin"
        ),
        syntax       = "cmd <<DELIM\\ncontent\\nDELIM  |  cmd <<< string",
        example      = (
            "cat <<EOF\n"
            "Hello $USER\n"
            "EOF\n\n"
            "cat <<'EOF'\n"
            "No $expansion here\n"
            "EOF\n\n"
            "sudo tee /etc/hosts.new <<EOF\n"
            "127.0.0.1 localhost\n"
            "EOF\n\n"
            "bc <<< '10 * 3.14'"
        ),
        task_description = "Nutze ein Heredoc, um eine mehrzeilige Ausgabe zu erzeugen",
        expected_commands = ["cat <<EOF", "<<EOF", "<<'EOF'"],
        hint_text    = "cat <<EOF startet ein Heredoc. Schreibe den Inhalt und beende mit EOF auf eigener Zeile",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen <<EOF und <<'EOF'?",
                options    = [
                    "Kein Unterschied",
                    "<<EOF expandiert Variablen. <<'EOF' verhindert Expansion (literal).",
                    "<<'EOF' ist nur in zsh verfügbar",
                    "<<EOF akzeptiert keine Leerzeichen",
                ],
                correct    = 1,
                explanation = (
                    "<<EOF: Variablen wie $USER werden expandiert.\n"
                    "<<'EOF': Der Delimiter wird gequotet → kein Expand, alles literal.\n"
                    "<<-EOF: Tab-Einrückungen im Content werden entfernt."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Heredoc:\n"
            "  <<DELIM = Variablen-Expansion AN\n"
            "  <<'DELIM' = KEINE Expansion\n"
            "  <<-DELIM = Tabs entfernen\n"
            "  <<< 'string' = Herestring (stdin)\n"
            "  Delimiter muss allein auf eigener Zeile stehen"
        ),
        memory_tip   = "<<EOF = here document. <<< = here string. Quote den Delimiter für kein Expand.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.17 — Prozesssubstitution
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.17",
        chapter      = 14,
        title        = "Prozesssubstitution — <(cmd) und >(cmd)",
        mtype        = "DECODE",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Zwei Befehle. Zwei Ausgaben. Du willst sie vergleichen.\n"
            " Keine temp-Dateien. Keine Umwege.\n"
            " diff <(cmd1) <(cmd2) — Prozesssubstitution.\n"
            " Bash öffnet Pseudo-Dateien. Du liest. Sauber.'"
        ),
        why_important = (
            "Prozesssubstitution ist ein kraftvolles Bash-Feature für LPIC-1 105.2.\n"
            "Ersetzt Temp-Dateien, ermöglicht diff auf Befehlsausgaben.\n"
            "Häufig in Kombination mit tee, diff und sort."
        ),
        explanation  = (
            "PROZESSSUBSTITUTION:\n\n"
            "EINGABE-SUBSTITUTION <(cmd):\n"
            "  <(cmd) liefert die Ausgabe von cmd als Datei-ähnlichen Deskriptor\n"
            "  Bash erstellt /dev/fd/N oder /proc/self/fd/N als Pseudo-Datei\n\n"
            "BEISPIELE:\n"
            "  diff <(sort file1) <(sort file2)\n"
            "    Vergleicht zwei Dateien nach Sortierung — ohne temp-Dateien\n\n"
            "  comm <(sort a.txt) <(sort b.txt)\n"
            "    Gemeinsame/unterschiedliche Zeilen\n\n"
            "  while read line; do\n"
            "      echo \">> $line\"\n"
            "  done < <(find /etc -name '*.conf')\n"
            "    While-Schleife über find-Ausgabe (Subshell-Problem vermieden!)\n\n"
            "AUSGABE-SUBSTITUTION >(cmd):\n"
            "  >(cmd) leitet Schreibzugriffe an cmd weiter\n\n"
            "  tee >(gzip > out.gz) >(wc -l) > /dev/null\n"
            "    Gleichzeitig komprimieren UND zählen\n\n"
            "WICHTIG:\n"
            "  Nur Bash/ksh/zsh — NICHT POSIX-sh!\n"
            "  Nicht in Subshells (keine Variablen nach außen)."
        ),
        syntax       = "diff <(cmd1) <(cmd2)  |  tee >(cmd)  |  while read; done < <(cmd)",
        example      = (
            "# Zwei Konfigs vergleichen\n"
            "diff <(sort /etc/group) <(sort /etc/passwd | cut -d: -f1)\n\n"
            "# find ohne Subshell-Problem\n"
            "while IFS= read -r file; do\n"
            "    echo \"Gefunden: $file\"\n"
            "done < <(find /var/log -name '*.log')\n\n"
            "# Gleichzeitig komprimieren und zählen\n"
            "cat bigfile.txt | tee >(gzip > bigfile.gz) | wc -l"
        ),
        task_description = "Vergleiche zwei sortierte Dateien mit diff und Prozesssubstitution",
        expected_commands = ["diff <(sort", "<(sort"],
        hint_text    = "diff <(sort datei1) <(sort datei2) — <() erzeugt einen Datei-Deskriptor für die Ausgabe",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt 'diff <(sort a.txt) <(sort b.txt)'?",
                options    = [
                    "Sortiert a.txt und b.txt permanent",
                    "Vergleicht die sortierten Inhalte von a.txt und b.txt ohne Temp-Dateien",
                    "Gibt einen Fehler, weil diff keine Prozesssubstitution unterstützt",
                    "Erstellt eine neue Datei mit den Unterschieden",
                ],
                correct    = 1,
                explanation = (
                    "<(cmd) erzeugt einen Pseudo-Datei-Deskriptor mit der Ausgabe von cmd.\n"
                    "diff bekommt zwei Datei-Deskriptoren und vergleicht sie.\n"
                    "Keine temporären Dateien nötig — elegant und sauber."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Prozesssubstitution:\n"
            "  <(cmd) = Ausgabe als Pseudo-Datei lesbar\n"
            "  >(cmd) = Eingabe in Prozess schreiben\n"
            "  Nur Bash/ksh/zsh — nicht POSIX sh!\n"
            "  while read < <(cmd) = keine Subshell-Falle\n"
            "  diff, comm, join = typische Anwendungsfälle"
        ),
        memory_tip   = "Merkhilfe: <() = process IN (lesen), >() = process OUT (schreiben). Wie Datei-Umlenkung für Prozesse.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.18 — Signalbehandlung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.18",
        chapter      = 14,
        title        = "Signalbehandlung — trap SIGINT SIGTERM EXIT",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Dein Skript läuft. Jemand drückt Ctrl+C.\n"
            " Temp-Dateien bleiben zurück. Locks nicht freigegeben.\n"
            " Das ist ein Hack-Angriffspunkt, Ghost.\n"
            " trap SIGINT — fange das Signal. Räume auf. Dann exit.'"
        ),
        why_important = (
            "Signalbehandlung mit trap ist LPIC-1 Topic 105.2 Pflicht.\n"
            "Kritisch für robuste Skripte: Cleanup bei Abbruch, Exit-Handler.\n"
            "kill -l zeigt alle Signale — Prüfungswissen."
        ),
        explanation  = (
            "SIGNALBEHANDLUNG MIT trap:\n\n"
            "SYNTAX:\n"
            "  trap 'Befehle' SIGNAL [SIGNAL...]\n\n"
            "WICHTIGE SIGNALE:\n"
            "  SIGINT  (2)   Ctrl+C — Tastatur-Interrupt\n"
            "  SIGTERM (15)  Normale Beendigung (kill PID)\n"
            "  SIGHUP  (1)   Terminal geschlossen\n"
            "  SIGKILL (9)   Sofortiger Kill — NICHT abfangbar!\n"
            "  EXIT          Bash-Pseudo-Signal bei Skript-Ende (immer!)\n"
            "  ERR           Bash-Pseudo-Signal bei Befehlsfehler\n\n"
            "BEISPIELE:\n"
            "  # Cleanup bei Abbruch\n"
            "  TMPFILE=$(mktemp)\n"
            "  trap 'rm -f \"$TMPFILE\"; echo \"Abgebrochen!\"' SIGINT SIGTERM EXIT\n\n"
            "  # Lock-Datei freigeben\n"
            "  LOCKFILE=/tmp/myscript.lock\n"
            "  trap 'rm -f $LOCKFILE' EXIT\n"
            "  touch $LOCKFILE\n\n"
            "  # Trap zurücksetzen\n"
            "  trap - SIGINT    Standardverhalten wiederherstellen\n"
            "  trap '' SIGINT   Signal ignorieren\n\n"
            "ALLE SIGNALE ANZEIGEN:\n"
            "  kill -l          Liste aller Signalnummern\n"
            "  kill -l SIGINT   Nummer von SIGINT (=2)\n\n"
            "REIHENFOLGE:\n"
            "  trap VOR dem zu schützenden Code definieren!"
        ),
        syntax       = "trap 'cleanup' SIGINT SIGTERM EXIT  |  kill -l  |  kill -SIGTERM PID",
        example      = (
            "#!/bin/bash\n"
            "TMPDIR=$(mktemp -d)\n"
            "LOCKFILE=/tmp/backup.lock\n\n"
            "cleanup() {\n"
            "    echo 'Räume auf...' >&2\n"
            "    rm -rf \"$TMPDIR\"\n"
            "    rm -f \"$LOCKFILE\"\n"
            "}\n\n"
            "trap cleanup SIGINT SIGTERM EXIT\n\n"
            "touch \"$LOCKFILE\"\n"
            "echo 'Verarbeite Daten...'\n"
            "cp -r /etc \"$TMPDIR/\"\n"
            "echo 'Fertig!'"
        ),
        task_description = "Registriere einen trap-Handler der bei EXIT eine Temp-Datei löscht",
        expected_commands = ["trap", "trap '", "trap \""],
        hint_text    = "trap 'rm -f $TMPFILE' EXIT — der EXIT Handler läuft immer, auch bei Fehlern",
        quiz_questions = [
            QuizQuestion(
                question   = "Welches Signal kann mit trap NICHT abgefangen werden?",
                options    = [
                    "SIGTERM (15)",
                    "SIGINT (2)",
                    "SIGKILL (9)",
                    "SIGHUP (1)",
                ],
                correct    = 2,
                explanation = (
                    "SIGKILL (9) kann NICHT abgefangen oder ignoriert werden.\n"
                    "Der Kernel beendet den Prozess sofort — kein Handler möglich.\n"
                    "SIGTERM, SIGINT, SIGHUP: alle mit trap abfangbar.\n"
                    "Deshalb: kill -9 nur als letztes Mittel verwenden!"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Signale:\n"
            "  SIGKILL (9) = nicht abfangbar, nicht ignorierbar\n"
            "  SIGTERM (15) = normaler kill (abfangbar)\n"
            "  SIGINT (2) = Ctrl+C (abfangbar)\n"
            "  trap 'cmd' EXIT = läuft IMMER bei Skript-Ende\n"
            "  kill -l = Liste aller Signale\n"
            "  trap - SIGNAL = Standardverhalten wiederherstellen"
        ),
        memory_tip   = "Merkhilfe: KILL=9=kein Entkommen. trap EXIT = der Hausmeister (räumt immer auf).",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.19 — Erweiterte Arrays
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.19",
        chapter      = 14,
        title        = "Erweiterte Arrays — declare -A, Slicing, mapfile",
        mtype        = "DECODE",
        xp           = 95,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Normale Arrays kennst du. Aber was ist mit Keys?\n"
            " declare -A macht aus einem Array eine Hash-Map.\n"
            " Ports, Config-Werte, Hostname-Mappings.\n"
            " Und mapfile liest eine ganze Datei in ein Array. Mächtig.'"
        ),
        why_important = (
            "Assoziative Arrays (declare -A) sind LPIC-1 Topic 105.2 Prüfungsstoff.\n"
            "mapfile/readarray ermöglicht effizientes Einlesen von Dateien.\n"
            "Array-Slicing und -Manipulation sind Basis fortgeschrittener Skripte."
        ),
        explanation  = (
            "ERWEITERTE ARRAYS IN BASH:\n\n"
            "ASSOZIATIVE ARRAYS (declare -A):\n"
            "  declare -A HOSTS\n"
            "  HOSTS[web]='192.168.1.10'\n"
            "  HOSTS[db]='192.168.1.20'\n"
            "  echo ${HOSTS[web]}\n"
            "  echo ${!HOSTS[@]}    # alle Keys\n"
            "  echo ${HOSTS[@]}     # alle Werte\n\n"
            "ARRAY-SLICING:\n"
            "  ARR=(a b c d e f)\n"
            "  echo ${ARR[@]:2:3}   # ab Index 2, 3 Elemente → c d e\n"
            "  echo ${ARR[@]: -2}   # letzte 2 Elemente → e f\n"
            "  echo ${#ARR[@]}      # Anzahl Elemente\n\n"
            "ARRAY MANIPULATION:\n"
            "  ARR+=(g h)           # Elemente hinzufügen\n"
            "  unset ARR[2]         # Element löschen\n"
            "  ARR=( \"${ARR[@]/a/A}\" )  # alle 'a' durch 'A' ersetzen\n\n"
            "MAPFILE / READARRAY:\n"
            "  mapfile -t LINES < datei.txt\n"
            "    Liest alle Zeilen in Array LINES (-t entfernt Newlines)\n\n"
            "  mapfile -t RESULTS < <(find /etc -name '*.conf')\n"
            "    find-Ausgabe direkt in Array\n\n"
            "  readarray -t ZEILEN < /etc/hosts\n"
            "    readarray = Alias für mapfile\n\n"
            "ITERATION:\n"
            "  for key in \"${!HOSTS[@]}\"; do\n"
            "      echo \"$key → ${HOSTS[$key]}\"\n"
            "  done"
        ),
        syntax       = "declare -A MAP  |  MAP[key]=val  |  mapfile -t ARR < file  |  ${ARR[@]:n:m}",
        example      = (
            "declare -A PORTS\n"
            "PORTS[ssh]=22\n"
            "PORTS[http]=80\n"
            "PORTS[https]=443\n\n"
            "for service in \"${!PORTS[@]}\"; do\n"
            "    echo \"$service läuft auf Port ${PORTS[$service]}\"\n"
            "done\n\n"
            "# Datei in Array laden\n"
            "mapfile -t HOSTS < /etc/hosts\n"
            "echo \"${#HOSTS[@]} Zeilen geladen\"\n"
            "echo \"Erste Zeile: ${HOSTS[0]}\""
        ),
        task_description = "Erstelle ein assoziatives Array mit declare -A und gib einen Wert aus",
        expected_commands = ["declare -A", "declare -A "],
        hint_text    = "declare -A NAME erstellt ein assoziatives Array. NAME[key]=wert setzt einen Eintrag.",
        quiz_questions = [
            QuizQuestion(
                question   = "Was gibt '${ARR[@]:1:3}' für ARR=(a b c d e) zurück?",
                options    = [
                    "a b c",
                    "b c d",
                    "b c d e",
                    "a b c d",
                ],
                correct    = 1,
                explanation = (
                    "${ARR[@]:OFFSET:LENGTH} — Slicing:\n"
                    "OFFSET=1 → beginnt bei Index 1 (= 'b')\n"
                    "LENGTH=3 → 3 Elemente: b c d\n"
                    "Wie bei String-Slicing, nur für Arrays."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Arrays:\n"
            "  declare -A = assoziatives Array (Key-Value)\n"
            "  ${!MAP[@]} = alle KEYS\n"
            "  ${MAP[@]} = alle WERTE\n"
            "  mapfile -t ARR < file = Datei in Array (-t = kein Newline)\n"
            "  ${ARR[@]:offset:len} = Slicing\n"
            "  ${#ARR[@]} = Anzahl Elemente"
        ),
        memory_tip   = "Merkhilfe: declare -A = Associative (wie Python-dict). mapfile = map file into array.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.20 — Skript-Sicherheit
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.20",
        chapter      = 14,
        title        = "Skript-Sicherheit — shellcheck, set -euo pipefail, Injection",
        mtype        = "SCAN",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Dein Skript läuft als root, Ghost.\n"
            " Ein unsanitierter Input. Ein einziger. Und der Angreifer ist drin.\n"
            " set -euo pipefail. shellcheck. Quote deine Variablen.\n"
            " Sicherheit ist kein Feature — sie ist die Basis.'"
        ),
        why_important = (
            "Skript-Sicherheit ist LPIC-1 Topic 105.2 Prüfungsstoff.\n"
            "Unsichere Skripte sind ein häufiger Angriffspunkt in Linux-Systemen.\n"
            "shellcheck, set -euo pipefail und Input-Validierung sind Best Practices."
        ),
        explanation  = (
            "SKRIPT-SICHERHEIT:\n\n"
            "SET-OPTIONEN FÜR SICHERE SKRIPTE:\n"
            "  set -e          Abbruch bei jedem Fehler (errexit)\n"
            "  set -u          Ungesetzte Variablen = Fehler (nounset)\n"
            "  set -o pipefail Pipe-Fehler weitergeben\n"
            "  set -euo pipefail  Kombination — Standard für sichere Skripte\n\n"
            "SHELLCHECK — STATISCHE ANALYSE:\n"
            "  shellcheck skript.sh     Häufige Fehler und Sicherheitsprobleme finden\n"
            "  shellcheck -S error *.sh Nur Fehler (keine Warnungen)\n"
            "  shellcheck -x skript.sh  Gesourcte Dateien einbeziehen\n\n"
            "COMMAND INJECTION VERMEIDEN:\n"
            "  GEFÄHRLICH:\n"
            "    eval \"$USER_INPUT\"       NIEMALS!\n"
            "    system(\"$USER_INPUT\")    NIEMALS!\n"
            "    rm -rf $DIR              Pfad ohne Quotes!\n\n"
            "  SICHER:\n"
            "    rm -rf \"$DIR\"            Immer in Anführungszeichen!\n"
            "    case \"$INPUT\" in\n"
            "        [a-zA-Z0-9_-]*) ;; # OK\n"
            "        *) echo 'Ungültig' >&2; exit 1 ;;\n"
            "    esac\n\n"
            "EINGABE-VALIDIERUNG:\n"
            "  # Nur Zahlen erlauben\n"
            "  if ! [[ \"$PORT\" =~ ^[0-9]+$ ]]; then\n"
            "      echo 'Fehler: PORT muss eine Zahl sein' >&2\n"
            "      exit 1\n"
            "  fi\n\n"
            "TEMP-DATEIEN SICHER:\n"
            "  TMPFILE=$(mktemp)           sicher (kein vorhersehbarer Name)\n"
            "  TMPDIR=$(mktemp -d)         sicheres temp-Verzeichnis\n"
            "  trap 'rm -f $TMPFILE' EXIT  immer aufräumen"
        ),
        syntax       = "set -euo pipefail  |  shellcheck skript.sh  |  mktemp  |  [[ =~ ^regex$ ]]",
        example      = (
            "#!/bin/bash\n"
            "set -euo pipefail\n\n"
            "# Eingabe validieren\n"
            "PORT=${1:?'Fehler: PORT fehlt'}\n"
            "if ! [[ \"$PORT\" =~ ^[0-9]+$ ]]; then\n"
            "    echo 'Fehler: PORT muss eine Zahl sein' >&2\n"
            "    exit 1\n"
            "fi\n\n"
            "# Sicheres Temp-Verzeichnis\n"
            "TMPDIR=$(mktemp -d)\n"
            "trap 'rm -rf \"$TMPDIR\"' EXIT\n\n"
            "echo \"Verarbeite Port: $PORT\""
        ),
        task_description = "Analysiere ein Skript mit shellcheck auf Sicherheitsprobleme",
        expected_commands = ["shellcheck"],
        hint_text    = "shellcheck datei.sh analysiert das Skript auf häufige Fehler und Sicherheitsprobleme",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt 'set -u' in einem Bash-Skript?",
                options    = [
                    "Skript läuft als root (uid=0)",
                    "Ungesetzte Variablen verursachen einen Fehler statt leer zu sein",
                    "Aktiviert Unicode-Unterstützung",
                    "Deaktiviert alle Ausgaben",
                ],
                correct    = 1,
                explanation = (
                    "set -u (nounset): Wenn eine nicht definierte Variable genutzt wird,\n"
                    "bricht das Skript mit einem Fehler ab.\n"
                    "Ohne -u: $UNSET_VAR ergibt einfach leer — gefährlich!\n"
                    "Mit -u: rm -rf $TYPO/ → Fehler statt rm -rf /!"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Sicherheit:\n"
            "  set -e = exit on error (errexit)\n"
            "  set -u = unset vars = error (nounset)\n"
            "  set -o pipefail = pipe errors propagieren\n"
            "  shellcheck = statische Analyse\n"
            "  mktemp = sichere Temp-Dateien\n"
            "  Variablen IMMER in \"Anführungszeichen\"!"
        ),
        memory_tip   = "Merkhilfe: -e=exit, -u=unset=error, pipefail=pipe nicht ignorieren. set -euo = Sicherheitsgurt.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.21 — Pipes & Subshells
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.21",
        chapter      = 14,
        title        = "Pipes & Subshells — PIPESTATUS, Subshell-Fallen, exec",
        mtype        = "DECODE",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Deine while-Schleife liest eine Pipe. Variablen gesetzt.\n"
            " Du verlässt die Schleife. Die Variablen sind weg.\n"
            " Subshell. Die Pipe hat eine eigene Umgebung geöffnet.\n"
            " PIPESTATUS, lastpipe, Prozesssubstitution — kenn den Unterschied.'"
        ),
        why_important = (
            "Subshell-Verhalten in Pipes ist ein häufiges LPIC-1 Prüfungsthema.\n"
            "PIPESTATUS ermöglicht Fehlerbehandlung in Pipelines.\n"
            "exec ersetzt den aktuellen Prozess — wichtig für effiziente Skripte."
        ),
        explanation  = (
            "PIPES & SUBSHELLS:\n\n"
            "SUBSHELL-PROBLEM:\n"
            "  COUNT=0\n"
            "  cat file | while read line; do\n"
            "      ((COUNT++))\n"
            "  done\n"
            "  echo $COUNT  # IMMER 0! while läuft in Subshell!\n\n"
            "LÖSUNG 1 — Prozesssubstitution:\n"
            "  while read line; do\n"
            "      ((COUNT++))\n"
            "  done < <(cat file)   # keine Subshell!\n\n"
            "LÖSUNG 2 — lastpipe (Bash 4.2+):\n"
            "  shopt -s lastpipe\n"
            "  cat file | while read line; do ((COUNT++)); done\n"
            "  echo $COUNT  # funktioniert jetzt!\n\n"
            "PIPESTATUS — Exit-Codes der Pipeline:\n"
            "  cmd1 | cmd2 | cmd3\n"
            "  echo ${PIPESTATUS[@]}   # z.B. '0 1 0'\n"
            "  echo ${PIPESTATUS[1]}   # Exit-Code von cmd2\n\n"
            "  # Fehler in der Mitte der Pipeline erkennen:\n"
            "  set -o pipefail   # Pipe schlägt fehl wenn irgendein cmd fehlschlägt\n\n"
            "EXEC — PROZESS ERSETZEN:\n"
            "  exec /bin/bash      Shell durch bash ersetzen (kein Fork!)\n"
            "  exec 3< datei.txt   File Descriptor 3 öffnen\n"
            "  exec 3>&-           File Descriptor 3 schließen\n"
            "  exec > logfile      STDOUT dauerhaft umleiten"
        ),
        syntax       = "${PIPESTATUS[@]}  |  done < <(cmd)  |  exec cmd  |  shopt -s lastpipe",
        example      = (
            "set -o pipefail\n\n"
            "# PIPESTATUS: Fehler in Pipeline erkennen\n"
            "tar czf - /etc | ssh user@backup 'cat > backup.tgz'\n"
            "echo \"tar: ${PIPESTATUS[0]}, ssh: ${PIPESTATUS[1]}\"\n\n"
            "# Subshell-Problem lösen\n"
            "COUNT=0\n"
            "while IFS= read -r line; do\n"
            "    ((COUNT++))\n"
            "done < <(grep 'ERROR' /var/log/syslog)\n"
            "echo \"Fehler gefunden: $COUNT\"\n\n"
            "# exec für FD-Verwaltung\n"
            "exec 3< /etc/passwd\n"
            "read -u 3 first_line\n"
            "exec 3>&-"
        ),
        task_description = "Zeige die Exit-Codes aller Befehle der letzten Pipeline mit PIPESTATUS",
        expected_commands = ["PIPESTATUS", "${PIPESTATUS", "echo ${PIPESTATUS"],
        hint_text    = "${PIPESTATUS[@]} enthält die Exit-Codes aller Befehle der zuletzt ausgeführten Pipeline",
        quiz_questions = [
            QuizQuestion(
                question   = "Warum ist COUNT nach 'cat file | while read l; do ((COUNT++)); done' immer 0?",
                options    = [
                    "while ist in Bash ein eingebauter Befehl ohne Zähler",
                    "Die while-Schleife läuft in einer Subshell der Pipe — Variablen gehen verloren",
                    "((COUNT++)) hat einen Syntaxfehler",
                    "cat file gibt nichts aus",
                ],
                correct    = 1,
                explanation = (
                    "In Bash läuft die rechte Seite einer Pipe in einer Subshell.\n"
                    "Variablenänderungen in der Subshell sind im Parent unsichtbar.\n"
                    "Lösung: while read; done < <(cat file) oder shopt -s lastpipe."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Pipes:\n"
            "  Pipe-Rechtsseite = Subshell → Variablen nicht sichtbar!\n"
            "  PIPESTATUS[@] = Exit-Codes aller Pipe-Glieder\n"
            "  set -o pipefail = Pipe-Fehler propagieren\n"
            "  < <(cmd) = Prozesssubstitution (KEINE Subshell)\n"
            "  exec = aktuellen Prozess ersetzen (kein Fork)"
        ),
        memory_tip   = "Merkhilfe: Pipe = Subshell-Gefängnis. PIPESTATUS = Ausbruchsinfo. < <() = Freiheit.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.22 — Skript-Performance
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.22",
        chapter      = 14,
        title        = "Skript-Performance — time, Forks vermeiden, Builtins",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Dein Skript braucht 30 Sekunden. Meines 0.3.\n"
            " Du rufst cat auf, dann grep, dann awk — drei Forks.\n"
            " Ich nutze bash builtins. Kein Fork. Kein Overhead.\n"
            " time dein Skript. Dann wirst du den Unterschied sehen.'"
        ),
        why_important = (
            "Performance-Optimierung ist LPIC-1 Topic 105.2 Prüfungsstoff.\n"
            "Unnötige Forks in Schleifen sind ein klassisches Performance-Problem.\n"
            "time und /usr/bin/time messen Skript-Laufzeit."
        ),
        explanation  = (
            "SKRIPT-PERFORMANCE:\n\n"
            "LAUFZEIT MESSEN:\n"
            "  time ./skript.sh          Bash-builtin: real/user/sys\n"
            "  /usr/bin/time ./skript.sh Extern: mehr Details\n"
            "  /usr/bin/time -v ./skript.sh Ausführliche Statistik\n\n"
            "AUSGABE VON time:\n"
            "  real  0m0.523s   Gesamte Wanduhrzeit (Wall clock)\n"
            "  user  0m0.201s   CPU-Zeit im User-Space\n"
            "  sys   0m0.045s   CPU-Zeit im Kernel\n\n"
            "HÄUFIGE PERFORMANCE-FALLEN:\n\n"
            "1) USELESS USE OF CAT:\n"
            "   LANGSAM: cat datei | grep 'pattern'\n"
            "   SCHNELL:  grep 'pattern' datei\n\n"
            "2) FORK IN SCHLEIFE:\n"
            "   LANGSAM: while read l; do echo $(date); done\n"
            "   SCHNELL:  DATE=$(date); while read l; do echo $DATE; done\n\n"
            "3) EXTERNE BEFEHLE STATT BUILTINS:\n"
            "   LANGSAM: LEN=$(echo ${#VAR} | wc -c)\n"
            "   SCHNELL:  LEN=${#VAR}  # Bash-Builtin!\n\n"
            "4) GREP+AWK+SED KETTE:\n"
            "   LANGSAM: cat f | grep x | awk '{print $1}' | sed 's/a/b/'\n"
            "   SCHNELL:  awk '/x/{sub(/a/,\"b\",$1); print $1}' f\n\n"
            "NÜTZLICHE BUILTINS (KEIN FORK):\n"
            "  ${VAR/alt/neu}   statt sed\n"
            "  ${#VAR}          statt wc -c\n"
            "  [[ =~ ]]         statt grep\n"
            "  printf           statt echo + externe Tools\n"
            "  read             statt head/tail in Schleifen"
        ),
        syntax       = "time cmd  |  /usr/bin/time -v cmd  |  ${VAR/x/y}  |  ${#VAR}",
        example      = (
            "# Laufzeit vergleichen\n"
            "time for i in {1..1000}; do echo $(date); done\n\n"
            "# Optimiert: date nur einmal aufrufen\n"
            "time ( DATE=$(date); for i in {1..1000}; do echo $DATE; done )\n\n"
            "# Builtin statt extern\n"
            "FILE='/var/log/syslog'\n"
            "# LANGSAM:\n"
            "BASENAME=$(echo $FILE | sed 's|.*/||')\n"
            "# SCHNELL:\n"
            "BASENAME=${FILE##*/}"
        ),
        task_description = "Miss die Laufzeit eines Befehls mit dem time builtin",
        expected_commands = ["time ", "time ./", "/usr/bin/time"],
        hint_text    = "time ./skript.sh gibt real (Wanduhr), user (User-CPU) und sys (Kernel-CPU) Zeit aus",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bedeutet 'real' in der Ausgabe von 'time ./skript.sh'?",
                options    = [
                    "CPU-Zeit im User-Space",
                    "CPU-Zeit im Kernel-Space",
                    "Gesamte verstrichene Zeit (Wanduhrzeit, Wall clock)",
                    "Anzahl der Systemaufrufe",
                ],
                correct    = 2,
                explanation = (
                    "time-Ausgabe:\n"
                    "  real = Wanduhrzeit (von Start bis Ende, inkl. Wartezeit)\n"
                    "  user = CPU-Zeit im User-Space (der eigene Code)\n"
                    "  sys  = CPU-Zeit im Kernel-Space (Systemaufrufe)\n"
                    "real > user+sys bedeutet: Prozess hat auf I/O gewartet."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Performance:\n"
            "  time = Bash-Builtin (real/user/sys)\n"
            "  /usr/bin/time -v = externe Version mit mehr Details\n"
            "  Jeder Fork kostet Zeit — Builtins bevorzugen\n"
            "  ${#VAR} statt wc, ${VAR/x/y} statt sed\n"
            "  cat file | cmd → cmd < file (Useless Use of Cat)"
        ),
        memory_tip   = "Merkhilfe: real=Wanduhr, user=dein Code, sys=Kernel. Fork=teuer, Builtin=gratis.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.23 — Bash Regex & Pattern Matching
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.23",
        chapter      = 14,
        title        = "Bash Regex & Pattern Matching — [[ =~ ]], extglob, globstar",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Eine IP-Adresse. Ein Username. Ein Datum.\n"
            " Validieren ohne externe Tools. Nur Bash.\n"
            " [[ string =~ regex ]] — der Operator den du brauchst.\n"
            " BASH_REMATCH speichert die Gruppen. Mächtiger als du dachtest.'"
        ),
        why_important = (
            "Bash Regex mit [[ =~ ]] ist LPIC-1 Topic 105.2 Prüfungsstoff.\n"
            "extglob und globstar erweitern Datei-Matching dramatisch.\n"
            "BASH_REMATCH ermöglicht Capture-Groups ohne externe Tools."
        ),
        explanation  = (
            "BASH REGEX & PATTERN MATCHING:\n\n"
            "[[ STRING =~ REGEX ]]:\n"
            "  if [[ \"$INPUT\" =~ ^[0-9]+$ ]]; then\n"
            "      echo 'Nur Zahlen'\n"
            "  fi\n\n"
            "  # Regex NICHT in Anführungszeichen!\n"
            "  PATTERN='^[a-z]+[0-9]*$'\n"
            "  [[ \"$VAR\" =~ $PATTERN ]]\n\n"
            "BASH_REMATCH — CAPTURE GROUPS:\n"
            "  DATE_RE='^([0-9]{4})-([0-9]{2})-([0-9]{2})$'\n"
            "  if [[ '2024-03-15' =~ $DATE_RE ]]; then\n"
            "      echo \"Jahr:  ${BASH_REMATCH[1]}\"  # 2024\n"
            "      echo \"Monat: ${BASH_REMATCH[2]}\"  # 03\n"
            "      echo \"Tag:   ${BASH_REMATCH[3]}\"  # 15\n"
            "  fi\n"
            "  # BASH_REMATCH[0] = gesamter Match\n\n"
            "EXTGLOB — ERWEITERTE GLOB-MUSTER:\n"
            "  shopt -s extglob\n"
            "  ?(muster)   0 oder 1 Mal\n"
            "  *(muster)   0 oder mehr Mal\n"
            "  +(muster)   1 oder mehr Mal\n"
            "  @(m1|m2)    genau eines der Muster\n"
            "  !(muster)   NICHT dieses Muster\n\n"
            "  ls !(*.log)          alle Dateien AUSSER .log\n"
            "  rm +(old_)*.txt      Dateien die mit old_ beginnen\n\n"
            "GLOBSTAR:\n"
            "  shopt -s globstar\n"
            "  ls **/*.py           alle .py-Dateien rekursiv\n"
            "  for f in **/*.conf; do ... done\n\n"
            "CASE MIT PATTERNS:\n"
            "  case \"$VAR\" in\n"
            "      [0-9]*)   echo 'beginnt mit Zahl' ;;\n"
            "      [a-z]*)   echo 'beginnt mit Kleinbuchstabe' ;;\n"
            "      *.tar.gz) echo 'Archiv' ;;\n"
            "  esac"
        ),
        syntax       = "[[ str =~ regex ]]  |  ${BASH_REMATCH[n]}  |  shopt -s extglob globstar",
        example      = (
            "# IP-Adresse validieren\n"
            "IP_RE='^([0-9]{1,3}\\.){3}[0-9]{1,3}$'\n"
            "if [[ \"$1\" =~ $IP_RE ]]; then\n"
            "    echo \"Gültige IP: $1\"\n"
            "else\n"
            "    echo 'Keine gültige IP' >&2\n"
            "    exit 1\n"
            "fi\n\n"
            "# Datum parsen mit BASH_REMATCH\n"
            "DATE_RE='^([0-9]{4})-([0-9]{2})-([0-9]{2})$'\n"
            "[[ '2024-12-31' =~ $DATE_RE ]]\n"
            "echo \"Jahr: ${BASH_REMATCH[1]}, Monat: ${BASH_REMATCH[2]}\"\n\n"
            "# extglob: alle außer .bak\n"
            "shopt -s extglob\n"
            "ls !(*.bak)"
        ),
        task_description = "Validiere eine Eingabe mit [[ =~ ]] und einem regulären Ausdruck",
        expected_commands = ["[[ ", "=~ ", "[[ $", "[[ \"$"],
        hint_text    = "[[ \"$VAR\" =~ ^[0-9]+$ ]] prüft ob VAR nur aus Zahlen besteht. Regex NICHT in Quotes!",
        quiz_questions = [
            QuizQuestion(
                question   = "Was enthält BASH_REMATCH[0] nach einem erfolgreichen [[ =~ ]] Match?",
                options    = [
                    "Den ersten Capture-Group-Treffer (erste Klammer)",
                    "Den gesamten gematchten String",
                    "Den Regex-Pattern selbst",
                    "Den Originalen String vor dem Match",
                ],
                correct    = 1,
                explanation = (
                    "BASH_REMATCH[0] = der gesamte Match (vollständiger Treffer)\n"
                    "BASH_REMATCH[1] = erste Capture-Group (erste Klammer)\n"
                    "BASH_REMATCH[2] = zweite Capture-Group usw.\n"
                    "Wie in Perl/Python: Index 0 = gesamter Match."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Regex in Bash:\n"
            "  [[ str =~ regex ]] = Regex-Match (kein externes grep!)\n"
            "  Regex NICHT in Anführungszeichen beim [[ =~ ]]!\n"
            "  BASH_REMATCH[0] = ganzer Match\n"
            "  BASH_REMATCH[1..n] = Capture-Groups\n"
            "  shopt -s extglob = ?(x) *(x) +(x) @(x) !(x)\n"
            "  shopt -s globstar = ** für rekursives Matching"
        ),
        memory_tip   = "Merkhilfe: =~ wie in Perl/Python. BASH_REMATCH[0]=alles, [1]=erste Klammer. extglob=!(außer).",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.QUIZ — Scripting QUIZ (renumbered)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.24",
        chapter      = 14,
        title        = "QUIZ — Bash-Scripting Wissenstest",
        mtype        = "QUIZ",
        xp           = 150,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Der Script-Daemon erwartet dich, Ghost.\n"
            " Topic 105.2 — alles was wir besprochen haben.\n"
            " Shebang bis getopts. Keine Lücken.'"
        ),
        why_important = "Quiz-Wiederholung für LPIC-1 Prüfung Topic 105.2",
        explanation   = "Beantworte die Fragen zum Bash-Scripting.",
        syntax        = "",
        example       = "",
        task_description = "Quiz: Bash-Scripting",
        expected_commands = [],
        hint_text     = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Was enthält '$#' in einem Bash-Skript?",
                options    = [
                    "A) Die PID des Skripts",
                    "B) Den Namen des Skripts",
                    "C) Die Anzahl der übergebenen Argumente",
                    "D) Den Exit-Code des letzten Befehls",
                ],
                correct    = "C",
                explanation = (
                    "Spezielle Bash-Variablen:\n"
                    "  $# = Anzahl Argumente\n"
                    "  $$ = PID des Skripts\n"
                    "  $0 = Skriptname\n"
                    "  $? = Exit-Code des letzten Befehls"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welcher test-Operator prüft ob ein String LEER ist?",
                options    = [
                    "A) -e STRING",
                    "B) -n STRING",
                    "C) -z STRING",
                    "D) -f STRING",
                ],
                correct    = "C",
                explanation = (
                    "-z = zero length = leer\n"
                    "-n = not zero = NICHT leer\n"
                    "-e = exists (für Dateien)\n"
                    "-f = regular file\n"
                    "Merkhilfe: -z=zero(leer), -n=not-zero(nicht leer)"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Wie lautet die korrekte Syntax für eine Bash-Funktion?",
                options    = [
                    "A) function myfunc { ... }",
                    "B) def myfunc() { ... }",
                    "C) myfunc() { ... }",
                    "D) A und C sind korrekt",
                ],
                correct    = "D",
                explanation = (
                    "Beide Formen sind in Bash gültig:\n"
                    "  function myfunc { ... }  (Bash-spezifisch)\n"
                    "  myfunc() { ... }          (POSIX-kompatibel)\n"
                    "'def' ist Python-Syntax — nicht Bash!"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Was macht 'shift $((OPTIND - 1))' nach getopts?",
                options    = [
                    "A) Alle Argumente löschen",
                    "B) Verarbeitete Optionen aus $@ entfernen",
                    "C) Den Zähler zurücksetzen",
                    "D) getopts beenden",
                ],
                correct    = "B",
                explanation = (
                    "Nach getopts zeigt $OPTIND auf das erste nicht-verarbeitete Argument.\n"
                    "shift $((OPTIND - 1)) entfernt alle verarbeiteten Optionen.\n"
                    "Danach: $1, $2, ... = verbleibende (nicht-Option) Argumente"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Wie wird eine for-Schleife über alle .txt-Dateien im aktuellen Verzeichnis geschrieben?",
                options    = [
                    "A) for f in (*.txt); do",
                    "B) for f in *.txt; do",
                    "C) for (f=*.txt); do",
                    "D) foreach f in *.txt; do",
                ],
                correct    = "B",
                explanation = (
                    "for f in *.txt; do ... done\n"
                    "Der Glob *.txt wird von bash expandiert.\n"
                    "Keine Klammern beim einfachen 'for in'!\n"
                    "foreach gibt es nicht in Bash (das ist C-Shell/tcsh)"
                ),
                xp_value   = 30,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Scripting-Schwerpunkte:\n"
            "  - Shebang: #!/bin/bash erste Zeile\n"
            "  - $# $@ $? $0 $1 $$ auswendig kennen\n"
            "  - test: -e -f -d -z -n -x, -eq -ne -lt -gt\n"
            "  - for..in..do..done, while..do..done, case..esac\n"
            "  - getopts: ':' = hat Argument, $OPTARG = Wert"
        ),
        memory_tip   = "Spezialvariablen: $0=Skriptname, $1-$9=Args, $#=Anzahl, $@=alle Args, $?=Exit-Code, $$=PID. test -eq/-ne/-lt/-gt für Zahlen, = für Strings.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 14.BOSS — SCRIPT DAEMON v14.0
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "14.boss",
        chapter      = 14,
        title        = "BOSS — SCRIPT DAEMON v14.0",
        mtype        = "BOSS",
        xp           = 320,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM ALERT: SCRIPT DAEMON v14.0 aktiv.\n"
            "Er generiert endlos Skripte die Backdoors installieren.\n"
            "Jedes Skript nutzt getopts, Schleifen und Funktionen.\n"
            "Zara Z3R0: 'Schreib ein Gegenskript, Ghost.\n"
            " Nutze sein eigenes Werkzeug gegen ihn.'"
        ),
        why_important = "Abschluss-Boss für Topic 105.2",
        explanation  = (
            "BOSS-CHALLENGE: Script Gauntlet\n\n"
            "Deine Mission:\n"
            "1) Skript ausführbar machen\n"
            "2) Exit-Code prüfen\n"
            "3) Funktion aufrufen\n"
            "4) Schleifen-Logik verstehen\n\n"
            "KOMMANDOS:\n"
            "  chmod +x cleanup.sh\n"
            "  bash -x cleanup.sh -v\n"
            "  bash -n cleanup.sh\n"
            "  ./cleanup.sh -h"
        ),
        ascii_art    = """
  ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
  ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
  ███████╗██║     ██████╔╝██║██████╔╝   ██║
  ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║
  ███████║╚██████╗██║  ██║██║██║        ██║
  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
      ██████╗  █████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗
      ██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║
      ██║  ██║███████║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
      ██║  ██║██╔══██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
      ██████╔╝██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

  ┌─ SCRIPT STATUS ──────────────────────────────┐
  │  Backdoor scripts: SPAWNING  ::  chmod WRONG │
  │  getopts HIJACKED  ::  loops INFINITE        │
  │  set -e DISABLED   ::  pipefail BYPASSED     │
  └──────────────────────────────────────────────┘

  ⚡ CHAOSWERK FACTION :: CHAPTER 14 BOSS ⚡""",
        story_transitions = [
            "SCRIPT DAEMON generiert Backdoor-Skripte. Du schreibst das Gegenmittel.",
            "getopts verarbeitet seine Argumente. Du nutzt seine eigene Logik.",
            "set -e stoppt beim ersten Fehler. Sein Skript stirbt an sich selbst.",
            "Letzter Loop. Dein cleanup.sh bereinigt alles was er geschrieben hat.",
        ],
        syntax       = "",
        example      = (
            "#!/bin/bash\n"
            "set -euo pipefail\n\n"
            "log() { echo \"[$(date +%T)] $1\"; }\n\n"
            "cleanup() {\n"
            "    local DIR=$1\n"
            "    for F in \"$DIR\"/*.tmp; do\n"
            "        [ -f \"$F\" ] && rm \"$F\" && log \"Gelöscht: $F\"\n"
            "    done\n"
            "}\n\n"
            "while getopts 'vd:' OPT; do\n"
            "    case $OPT in\n"
            "        v) VERBOSE=1 ;;\n"
            "        d) DIR=$OPTARG ;;\n"
            "    esac\n"
            "done\n"
            "cleanup \"${DIR:-/tmp}\""
        ),
        task_description = "BOSS: Prüfe die Skript-Syntax von cleanup.sh ohne Ausführung",
        expected_commands = ["bash -n cleanup.sh"],
        hint_text    = "bash -n SKRIPT prüft die Syntax ohne das Skript auszuführen (dry-run)",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist $? in Bash?',
                options     = ['A) Anzahl der Parameter', 'B) Exit-Code des letzten Befehls (0=Erfolg)', 'C) Prozess-ID', 'D) Letztes Argument'],
                correct     = 'B',
                explanation = '$? = Exit-Code. 0 = Erfolg. 1-255 = Fehler. $$ = PID. $# = Anzahl Args. $@ = alle Args. $0 = Skriptname.',
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "set -euo pipefail — was bewirkt 'pipefail'?",
                options     = [
                    'A) Fehler bei fehlender Pipeline',
                    'B) Pipeline gibt Exit-Code des ERSTEN fehlgeschlagenen Befehls zurück (nicht des letzten)',
                    'C) Pipes werden deaktiviert',
                    'D) Identisch mit set -e',
                ],
                correct     = 'B',
                explanation = 'Ohne pipefail: cmd1 | cmd2 — Exit-Code = cmd2 (auch wenn cmd1 fehlschlug). Mit pipefail: Exit-Code = erster Fehler in der Pipe.',
                xp_value    = 35,
            ),
            QuizQuestion(
                question    = "getopts 'a:b' in einem Skript — was bedeutet der Doppelpunkt nach 'a'?",
                options     = [
                    'A) a ist optional',
                    'B) a erwartet ein Argument (in $OPTARG)',
                    'C) a ist ein Long-Option (--a)',
                    'D) Syntaxfehler',
                ],
                correct     = 'B',
                explanation = 'getopts: Buchstabe gefolgt von : = erwartet Argument. Das Argument landet in $OPTARG. Ohne : = Flag ohne Argument.',
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "bash -n skript.sh — was wird geprüft?",
                options     = [
                    'A) Skript wird ausgeführt und Ausgabe unterdrückt',
                    'B) Nur Syntax-Check (kein Ausführen)',
                    'C) Skript wird im non-interactive Modus ausgeführt',
                    'D) -n ist kein gültiger bash-Flag',
                ],
                correct     = 'B',
                explanation = 'bash -n = Syntax-Check ohne Ausführung. bash -x = Debug-Trace (zeigt jeden Befehl). bash -v = verbose (zeigt Quellcode). bash -e = Exit bei Fehler.',
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'function foo()' und 'foo()' in Bash?",
                options     = [
                    'A) function foo() ist POSIX-konform, foo() ist Bash-spezifisch',
                    'B) foo() ist POSIX-konform (sh-kompatibel), function foo() ist Bash-spezifisch',
                    'C) Kein Unterschied — identisch',
                    'D) function foo() erlaubt lokale Variablen, foo() nicht',
                ],
                correct     = 'B',
                explanation = 'foo() { } = POSIX sh-Syntax, portabel. function foo { } oder function foo() { } = Bash-spezifisch. Für maximale Kompatibilität: foo() verwenden.',
                xp_value    = 30,
            ),
        ],
        exam_tip     = (
            "LPIC-1 FINAL SCRIPT CHECK:\n"
            "  bash -x = debug (trace)\n"
            "  bash -n = syntax check\n"
            "  set -e = exit on error\n"
            "  set -u = unbound var = error\n"
            "  chmod +x = ausführbar machen\n"
            "  getopts ':' = Option hat Argument"
        ),
        memory_tip   = "Merkhilfe: -x=execute(trace), -n=no-execute(syntax), -e=exit-on-error",
        gear_reward  = "pipe_wrench",
        faction_reward = ("Net Runners", 40),
    ),
]
