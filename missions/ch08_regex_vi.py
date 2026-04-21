"""
NeonGrid-9 :: Kapitel 8 — REGEX PROTOCOL
LPIC-1 Topic 103.7 / 103.8
Reguläre Ausdrücke & vi/vim Editor

"In NeonGrid-9 sind Texte verschlüsselte Daten.
 Nur wer Regex spricht und vi beherrscht,
 kann Systeme lesen — und umschreiben."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_8_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 8.01 — Regex Grundlagen: Metazeichen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.01",
        chapter      = 8,
        title        = "Regex — Die Sprache der Muster",
        mtype        = "SCAN",
        xp           = 60,
        speaker      = "ZARA Z3R0",
        story        = (
            "Millionen Log-Zeilen rauschen durch NeonGrid-9.\n"
            "Zara Z3R0: 'Du musst Muster erkennen, Ghost.\n"
            " Regex ist deine Decoder-Linse.\n"
            " Lern es — oder ertrinke im Datenstrom.'"
        ),
        why_important = (
            "Reguläre Ausdrücke sind das Fundament aller Textverarbeitung.\n"
            "grep, sed, awk, find — alle nutzen Regex.\n"
            "LPIC-1 Topic 103.7 testet BRE und ERE ausführlich."
        ),
        explanation  = (
            "REGEX METAZEICHEN — Basic Regular Expressions (BRE):\n\n"
            "  .        Ein beliebiges Zeichen (außer Newline)\n"
            "  *        0 oder mehr Wiederholungen des vorherigen\n"
            "  ^        Anfang der Zeile\n"
            "  $        Ende der Zeile\n"
            "  [ ]      Zeichenklasse: [abc] = a oder b oder c\n"
            "  [^ ]     Negierte Klasse: [^abc] = nicht a,b,c\n"
            "  \\        Escape-Zeichen (Metazeichen wörtlich)\n\n"
            "EXTENDED Regular Expressions (ERE) — mit grep -E:\n\n"
            "  +        1 oder mehr Wiederholungen\n"
            "  ?        0 oder 1 Wiederholung\n"
            "  |        Alternation: foo|bar\n"
            "  ( )      Gruppe: (foo)+\n"
            "  {n,m}    n bis m Wiederholungen: [0-9]{2,4}\n\n"
            "HÄUFIGE ZEICHENKLASSEN:\n"
            "  [0-9]    Ziffern  (oder \\d in PCRE)\n"
            "  [a-z]    Kleinbuchstaben\n"
            "  [A-Z]    Großbuchstaben\n"
            "  [a-zA-Z0-9]  Alphanumerisch\n"
            "  \\s       Whitespace (Leerzeichen, Tab, Newline)\n"
            "  \\w       Wortzeichen [a-zA-Z0-9_]"
        ),
        ascii_art = """
  ██████╗ ███████╗ ██████╗ ███████╗██╗  ██╗   ██╗   ██╗   ██╗██╗
  ██╔══██╗██╔════╝██╔════╝ ██╔════╝╚██╗██╔╝   ██║   ██║   ██║██║
  ██████╔╝█████╗  ██║  ███╗█████╗   ╚███╔╝    ██║   ██║   ██║██║
  ██╔══██╗██╔══╝  ██║   ██║██╔══╝   ██╔██╗    ╚═╝   ╚═╝   ╚═╝╚═╝
  ██║  ██║███████╗╚██████╔╝███████╗██╔╝ ██╗   ██╗   ██╗   ██╗██╗
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝╚═╝

  [ CHAPTER 08 :: REGEX & VIM ]
  > Pattern engine online. .* [A-Z]+ \\d{3} — match found.""",
        story_transitions = [
            "Muster erkennen ist Macht. Regex ist die Sprache der Maschinen.",
            ". * + ? [] {} — jedes Zeichen hat Bedeutung.",
            "grep findet. sed ersetzt. awk verarbeitet. vim editiert.",
            "Ein Sysadmin ohne Regex ist blind im Datendschungel.",
        ],
        syntax       = "grep 'MUSTER' DATEI | grep -E 'ERE-MUSTER'",
        example      = (
            "grep '^root' /etc/passwd        # Zeilen die mit 'root' beginnen\n"
            "grep 'bash$' /etc/passwd        # Zeilen die mit 'bash' enden\n"
            "grep '[0-9]' /etc/passwd        # Zeilen mit mind. einer Ziffer\n"
            "grep -E 'ssh|http' /etc/services  # ssh ODER http\n"
            "grep -E '[0-9]{1,3}\\.[0-9]{1,3}' /var/log/syslog  # IP-ähnlich"
        ),
        task_description = "Zeige Zeilen aus /etc/passwd die mit 'root' beginnen",
        expected_commands = ["grep '^root' /etc/passwd"],
        hint_text    = "^ bedeutet Zeilenanfang: grep '^root' /etc/passwd",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist der Unterschied zwischen BRE und ERE in grep?',
                options     = ['A) BRE unterstützt mehr Sonderzeichen', 'B) ERE nutzt + ? | ohne Backslash, BRE braucht \\+', 'C) Kein Unterschied', 'D) BRE = für Dateien, ERE = für Stdin'],
                correct     = 'B',
                explanation = 'ERE (Extended): + ? | ( ) ohne Backslash. BRE (Basic): braucht \\+ \\? usw.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welcher Flag aktiviert Extended Regular Expressions in grep?',
                options     = ['A) grep -B', 'B) grep -E (oder egrep)', 'C) grep -X', 'D) grep -r'],
                correct     = 'B',
                explanation = "grep -E oder egrep = Extended Regex. LPIC-1 prüft: 'Wie ERE aktivieren?'",
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Prüfung: BRE vs ERE!\n"
            "  grep 'x'     → BRE (Basic)\n"
            "  grep -E 'x'  → ERE (Extended) — + ? | ( ) ohne Backslash\n"
            "  egrep 'x'    → identisch mit grep -E\n"
            "  grep -F 'x'  → Fixed string (kein Regex)"
        ),
        memory_tip   = "Merkhilfe: ^ = Anker am Anfang, $ = Anker am Ende",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.02 — grep & egrep mit Regex
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.02",
        chapter      = 8,
        title        = "grep -E / egrep — Muster-Scanner",
        mtype        = "INFILTRATE",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "Der Hacker CIPHER sendet eine verschlüsselte Nachricht:\n"
            "'Die Firewall filtert nach Mustern. Ich auch.\n"
            " grep -E ist dein Schlüssel, Ghost.\n"
            " Lern, wie man Logs nach Feinden durchsucht.'"
        ),
        why_important = (
            "grep mit regulären Ausdrücken ist das mächtigste\n"
            "Text-Such-Tool unter Linux. LPIC-1 testet Flags und Muster."
        ),
        explanation  = (
            "GREP MIT REGEX:\n\n"
            "  grep 'MUSTER' datei      BRE (Basic)\n"
            "  grep -E 'MUSTER' datei   ERE (Extended)\n"
            "  egrep 'MUSTER' datei     wie grep -E\n"
            "  grep -P 'MUSTER' datei   PCRE (Perl-kompatibel)\n\n"
            "WICHTIGE GREP-FLAGS:\n"
            "  -i    case-insensitive\n"
            "  -v    invert match (Zeilen die NICHT matchen)\n"
            "  -n    Zeilennummern zeigen\n"
            "  -c    nur Anzahl der Treffer\n"
            "  -l    nur Dateinamen mit Treffern\n"
            "  -r    rekursiv\n"
            "  -A n  n Zeilen nach dem Treffer\n"
            "  -B n  n Zeilen vor dem Treffer\n"
            "  -C n  n Zeilen um den Treffer\n"
            "  -o    nur den Treffer selbst ausgeben\n\n"
            "REGEX BEISPIELE:\n"
            "  grep '^#' datei          Kommentarzeilen\n"
            "  grep -v '^#' datei       Nicht-Kommentarzeilen\n"
            "  grep -v '^$' datei       Nicht-Leerzeilen\n"
            "  grep -E '[0-9]+' datei   Zeilen mit Zahlen\n"
            "  grep -E '^[A-Z]' datei   Großbuchstaben am Anfang"
        ),
        syntax       = "grep [-E] [-i] [-v] [-n] [-r] 'MUSTER' [DATEI...]",
        example      = (
            "grep -n 'error' /var/log/syslog\n"
            "grep -i 'ERROR' /var/log/syslog\n"
            "grep -c 'FAILED' /var/log/auth.log\n"
            "grep -E 'warning|error|critical' /var/log/syslog\n"
            "grep -v '^#' /etc/ssh/sshd_config | grep -v '^$'"
        ),
        task_description = "Zeige Zeilen aus /var/log/syslog die 'error' oder 'warning' enthalten",
        expected_commands = ["grep -E 'error|warning' /var/log/syslog"],
        hint_text    = "grep -E erlaubt | für ODER: grep -E 'error|warning' /var/log/syslog",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'grep -v ^$' mit einer Datei?",
                options     = ['A) Zeigt nur leere Zeilen', 'B) Entfernt/filtert Leerzeilen heraus', 'C) Zählt Zeilen', 'D) Fehler: ungültiger Ausdruck'],
                correct     = 'B',
                explanation = 'grep -v = invertieren. ^$ = leere Zeile (Anfang direkt Zeilenende). Also: alle nicht-leeren Zeilen.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was gibt 'grep -c MUSTER datei' zurück?",
                options     = ['A) Die gefundenen Zeilen mit Zeilennummern', 'B) Nur die Anzahl der Treffer (keine Zeilen)', 'C) Alle Dateien mit Treffern', 'D) Kontext-Zeilen'],
                correct     = 'B',
                explanation = 'grep -c = count = gibt nur die Anzahl der Treffer-Zeilen zurück.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "Häufige Prüfungsfrage: 'grep -v ^$ datei' entfernt Leerzeilen.\n"
            "grep -c gibt NUR die Anzahl zurück, keine Zeilen!\n"
            "grep -l gibt nur Dateinamen, ideal für Skripte."
        ),
        memory_tip   = "Merkhilfe: -v = inVert, -i = Ignore case, -n = Number, -c = Count",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.03 — sed mit Regex
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.03",
        chapter      = 8,
        title        = "sed — Stream-Editor mit Regex",
        mtype        = "DECODE",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Ein feindlicher Agent hat Config-Dateien\n"
            " mit falschen IP-Adressen überschrieben, Ghost.\n"
            " sed ist dein Chirurgen-Skalpell.\n"
            " Ersetze. Lösche. Transformiere.'"
        ),
        why_important = (
            "sed ist das Standard-Tool für nicht-interaktive Textbearbeitung.\n"
            "In Skripten unverzichtbar. LPIC-1 testet s/alt/neu/g und -i."
        ),
        explanation  = (
            "SED — STREAM EDITOR:\n\n"
            "GRUNDSYNTAX: sed 'BEFEHL' DATEI\n\n"
            "ERSETZEN (s-Befehl):\n"
            "  sed 's/alt/neu/' datei      ersetzt 1. Vorkommen pro Zeile\n"
            "  sed 's/alt/neu/g' datei     ersetzt ALLE Vorkommen (global)\n"
            "  sed 's/alt/neu/2' datei     ersetzt 2. Vorkommen\n"
            "  sed 's/alt/neu/gi' datei    global + case-insensitive\n"
            "  sed -i 's/alt/neu/g' datei  In-Place (Datei direkt ändern)\n"
            "  sed -i.bak 's/alt/neu/g' d  In-Place mit Backup (.bak)\n\n"
            "ZEILEN LÖSCHEN (d-Befehl):\n"
            "  sed '/MUSTER/d' datei       Zeilen mit Muster löschen\n"
            "  sed '/^#/d' datei           Kommentare löschen\n"
            "  sed '/^$/d' datei           Leerzeilen löschen\n"
            "  sed '5d' datei              Zeile 5 löschen\n"
            "  sed '5,10d' datei           Zeilen 5-10 löschen\n\n"
            "ZEILENBEREICH:\n"
            "  sed -n '5,10p' datei        Nur Zeilen 5-10 ausgeben\n"
            "  sed -n '/START/,/STOP/p' d  Von START bis STOP\n\n"
            "REGEX IN SED:\n"
            "  sed 's/[0-9]*/NUM/g' datei  Zahlen durch NUM ersetzen\n"
            "  sed 's/^/  /' datei         2 Leerzeichen vor jede Zeile"
        ),
        syntax       = "sed 's/MUSTER/ERSATZ/FLAGS' DATEI | sed -i 's/M/E/g' DATEI",
        example      = (
            "sed 's/localhost/127.0.0.1/g' /etc/hosts\n"
            "sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config\n"
            "sed '/^#/d' /etc/hosts          # Kommentare entfernen\n"
            "sed -n '1,5p' /etc/passwd       # Erste 5 Zeilen\n"
            "sed 's/[[:space:]]\\+/ /g' file # mehrfache Leerzeichen normalisieren"
        ),
        task_description = "Ersetze alle Vorkommen von 'error' durch 'ERROR' in /var/log/test.log",
        expected_commands = ["sed 's/error/ERROR/g' /var/log/test.log"],
        hint_text    = "sed 's/suche/ersetze/g' datei — /g macht es global (alle Vorkommen)",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'sed s/alt/neu/' ohne /g-Flag?",
                options     = ['A) Ersetzt alle Vorkommen', 'B) Ersetzt nur das ERSTE Vorkommen in jeder Zeile', 'C) Fehler', 'D) Ersetzt letztes Vorkommen'],
                correct     = 'B',
                explanation = 'Ohne /g: nur erstes Vorkommen pro Zeile. Mit /g: alle. PRÜFUNGS-FALLE!',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was macht sed -i?',
                options     = ['A) Ignoriert Fehler', 'B) Ändert die Datei direkt (In-Place)', 'C) Interaktiver Modus', 'D) Case-insensitive'],
                correct     = 'B',
                explanation = 'sed -i = In-Place, ändert die Datei direkt. Ohne -i: nur Ausgabe auf stdout.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGS-FALLE: sed 's/x/y/' ohne /g ersetzt nur das ERSTE Vorkommen!\n"
            "sed -i ändert die Datei DIREKT — ohne -i wird nur stdout verändert.\n"
            "-i.bak erstellt automatisch ein Backup."
        ),
        memory_tip   = "Merkhilfe: s = substitute, d = delete, p = print, -n = still (kein auto-print)",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.04 — Regex in awk
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.04",
        chapter      = 8,
        title        = "awk — Muster + Aktion",
        mtype        = "DECODE",
        xp           = 100,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'awk ist nicht nur ein Filter, Ghost.\n"
            " Es ist eine Mini-Programmiersprache.\n"
            " Wenn du Zeilen filtert UND transformierst,\n"
            " ist awk deine Waffe der Wahl.'"
        ),
        why_important = (
            "awk kombiniert Regex-Filterung mit Feldverarbeitung.\n"
            "Ideal für strukturierte Daten (CSV, /etc/passwd, Logs).\n"
            "LPIC-1 testet Muster, $-Felder, NR, NF, FS."
        ),
        explanation  = (
            "AWK SYNTAX: awk 'MUSTER { AKTION }' DATEI\n\n"
            "MUSTER-TYPEN:\n"
            "  /regex/         Regex-Muster\n"
            "  !/regex/        Negiertes Regex\n"
            "  NR==5           Numerischer Vergleich (Zeile 5)\n"
            "  NF > 3          Feldanzahl > 3\n"
            "  $1 == \"root\"    Feldinhalts-Vergleich\n"
            "  /start/,/stop/  Bereich\n\n"
            "SPEZIALVARIABLEN:\n"
            "  $0    gesamte Zeile\n"
            "  $1    1. Feld, $2 = 2. Feld, ...\n"
            "  $NF   letztes Feld\n"
            "  NR    aktuelle Zeilennummer\n"
            "  NF    Anzahl Felder in der Zeile\n"
            "  FS    Feld-Trennzeichen (default: Whitespace)\n"
            "  OFS   Output-Feld-Trennzeichen\n\n"
            "AKTIONEN:\n"
            "  print $1, $3   Felder 1 und 3\n"
            "  printf \"%s\\t%s\\n\", $1, $2\n"
            "  sum += $3; END { print sum }\n\n"
            "BEGIN/END:\n"
            "  BEGIN { FS=\":\" }  vor der ersten Zeile\n"
            "  END { print NR }  nach der letzten Zeile"
        ),
        syntax       = "awk -F: '/MUSTER/ { print $1, $NF }' DATEI",
        example      = (
            "awk -F: '{print $1}' /etc/passwd         # nur Benutzernamen\n"
            "awk -F: '$3 >= 1000 {print $1}' /etc/passwd  # UID >= 1000\n"
            "awk '/ERROR/ {print NR, $0}' /var/log/syslog  # Fehler mit Zeilennummer\n"
            "awk '{sum += $1} END {print sum}' zahlen.txt  # Summe\n"
            "awk 'NR % 2 == 0' datei                  # jede 2. Zeile"
        ),
        task_description = "Zeige nur Benutzernamen (1. Feld) aus /etc/passwd mit Trenner ':'",
        expected_commands = ["awk -F: '{print $1}' /etc/passwd"],
        hint_text    = "awk -F: setzt das Trennzeichen auf ':'. $1 ist das erste Feld.",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was druckt 'awk '{print $NF}' datei'?",
                options     = ['A) Erste Spalte', 'B) Letzte Spalte jeder Zeile', 'C) Anzahl der Felder', 'D) Fehler'],
                correct     = 'B',
                explanation = '$NF = letztes Feld (Number of Fields). NR = aktuelle Zeilennummer.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welcher awk-Befehl filtert Zeilen, die 'root' enthalten?",
                options     = ["A) awk 'root' datei", "B) awk '/root/ {print}' datei", "C) awk -g 'root' datei", 'D) awk --match root datei'],
                correct     = 'B',
                explanation = "awk '/MUSTER/' = filtert Zeilen mit Muster. Ohne Aktion = print (Standard).",
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGSTIPP: awk vs grep vs sed:\n"
            "  grep  → nur filtern\n"
            "  sed   → Text transformieren/ersetzen\n"
            "  awk   → Felder extrahieren + Logik\n"
            "FS kann auch als -F: Flag gesetzt werden."
        ),
        memory_tip   = "Merkhilfe: NR = Number of Records (Zeile), NF = Number of Fields",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.05 — vi/vim Grundlagen: Modi
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.05",
        chapter      = 8,
        title        = "vi/vim — Der Editor der Götter",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Auf jedem Linux-System ist vi installiert, Ghost.\n"
            " Kein Nano. Kein Emacs. Nur vi.\n"
            " Wenn du auf einem Notfallsystem arbeitest,\n"
            " ist vi deine einzige Waffe.'"
        ),
        why_important = (
            "vi ist auf JEDEM Unix/Linux-System vorhanden.\n"
            "LPIC-1 Topic 103.8 testet vi-Modi, Navigation und grundlegende Befehle.\n"
            "In Prüfungen kommen Fragen zu :wq, dd, yy und Suchen."
        ),
        explanation  = (
            "VI/VIM — DIE DREI MODI:\n\n"
            "  NORMAL-MODUS   Standard beim Öffnen — Befehle eingeben\n"
            "  INSERT-MODUS   Text einfügen (i, a, o, O, I, A)\n"
            "  COMMAND-MODUS  : für Ex-Befehle, / für Suche\n\n"
            "MODI WECHSELN:\n"
            "  i       → INSERT vor Cursor\n"
            "  a       → INSERT nach Cursor (append)\n"
            "  o       → neue Zeile unter Cursor + INSERT\n"
            "  O       → neue Zeile über Cursor + INSERT\n"
            "  I       → INSERT am Zeilenanfang\n"
            "  A       → INSERT am Zeilenende\n"
            "  ESC     → zurück zu NORMAL\n\n"
            "NORMAL-MODUS NAVIGATION:\n"
            "  h j k l → links, runter, rauf, rechts\n"
            "  w       → vorwärts ein Wort\n"
            "  b       → rückwärts ein Wort\n"
            "  0       → Zeilenanfang\n"
            "  $       → Zeilenende\n"
            "  gg      → erste Zeile\n"
            "  G       → letzte Zeile\n"
            "  :n      → Zeile n (z.B. :42)\n"
            "  Ctrl+F  → eine Seite vor\n"
            "  Ctrl+B  → eine Seite zurück"
        ),
        syntax       = "vi DATEI  |  vim DATEI",
        example      = (
            "vi /etc/hosts        # Datei öffnen\n"
            "# Im Normal-Modus:\n"
            "i                    # Insert-Modus starten\n"
            "ESC                  # zurück zu Normal\n"
            ":w                   # speichern\n"
            ":q                   # beenden\n"
            ":wq                  # speichern + beenden\n"
            ":q!                  # beenden OHNE speichern"
        ),
        task_description = "Öffne /etc/hosts mit vi und beende ohne Änderungen",
        expected_commands = ["vi /etc/hosts"],
        hint_text    = "Starte vi mit: vi /etc/hosts — zum Beenden: ESC dann :q!",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welche vi-Taste bringt dich IMMER in den Normal-Modus?',
                options     = ['A) Enter', 'B) q', 'C) ESC', 'D) Ctrl+C'],
                correct     = 'C',
                explanation = 'ESC = immer Normal-Modus. Mehrfach drücken schadet nicht. Essenziell für vi!',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wie speicherst und beendest du vi?',
                options     = ['A) :save', 'B) :wq oder ZZ', 'C) Ctrl+S', 'D) :exit!'],
                correct     = 'B',
                explanation = ':wq = write+quit. ZZ = Kurzform. :q! = quit ohne Speichern.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "MERKE: ESC bringt dich IMMER in den Normal-Modus.\n"
            "Du kannst ESC mehrfach drücken — kein Schaden.\n"
            ":q! = beenden ohne speichern (force quit)\n"
            ":wq = Write + Quit = speichern und beenden"
        ),
        memory_tip   = "Merkhilfe: i=insert, a=append, ESC=Normal, :wq=Write+Quit, :q!=Quit force",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.06 — vi: Bearbeiten, Kopieren, Löschen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.06",
        chapter      = 8,
        title        = "vi — Bearbeiten, Kopieren, Einfügen",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ein Config-Fehler blockiert den Server-Zugang.\n"
            " Du hast 60 Sekunden, Ghost.\n"
            " Öffne die Datei. Finde die Zeile. Lösche sie.\n"
            " Speichere. Raus. Kein Nano verfügbar.'"
        ),
        why_important = (
            "Zeilen löschen, kopieren und einfügen sind\n"
            "die häufigsten vi-Operationen im Produktiveinsatz.\n"
            "LPIC-1 testet dd, yy, p, u explizit."
        ),
        explanation  = (
            "VI EDIT-BEFEHLE (im Normal-Modus):\n\n"
            "LÖSCHEN:\n"
            "  x       Zeichen unter Cursor löschen\n"
            "  X       Zeichen vor Cursor löschen\n"
            "  dd      aktuelle Zeile löschen (in Puffer)\n"
            "  ndd     n Zeilen löschen (z.B. 3dd = 3 Zeilen)\n"
            "  dw      Wort löschen\n"
            "  d$      bis Zeilenende löschen\n"
            "  d0      bis Zeilenanfang löschen\n\n"
            "KOPIEREN (Yank):\n"
            "  yy      aktuelle Zeile kopieren\n"
            "  nyy     n Zeilen kopieren\n"
            "  yw      Wort kopieren\n\n"
            "EINFÜGEN:\n"
            "  p       nach Cursor einfügen\n"
            "  P       vor Cursor einfügen\n\n"
            "RÜCKGÄNGIG / WIEDERHOLEN:\n"
            "  u       Undo (rückgängig)\n"
            "  Ctrl+R  Redo (wiederholen)\n"
            "  .       letzten Befehl wiederholen\n\n"
            "ERSETZEN:\n"
            "  r       einzelnes Zeichen ersetzen\n"
            "  R       ab Cursor überschreiben (Replace-Modus)\n"
            "  cw      Wort ersetzen (löscht + INSERT-Modus)"
        ),
        syntax       = "dd  yy  p  P  u  (alle im Normal-Modus)",
        example      = (
            "# 5 Zeilen löschen:\n"
            "5dd\n"
            "# Zeile kopieren und 3x einfügen:\n"
            "yy\n"
            "3p\n"
            "# Letztes rückgängig:\n"
            "u\n"
            "# Zeile löschen und wiedereinfügen (= Zeile verschieben):\n"
            "dd    # löscht in Puffer\n"
            "p     # fügt unter aktueller Position ein"
        ),
        task_description = "Welcher vi-Befehl löscht die aktuelle Zeile?",
        expected_commands = ["dd"],
        hint_text    = "dd = delete line. Löscht die Zeile in den Puffer (mit p wieder einfügbar)",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'dd' in vi (im Normal-Modus)?",
                options     = ['A) Löscht ein Zeichen', 'B) Löscht die aktuelle Zeile (in Puffer)', 'C) Öffnet neues Dokument', 'D) Dupliziert die Zeile'],
                correct     = 'B',
                explanation = 'dd = delete line. Der Inhalt ist im Puffer! dd + p = Zeile verschieben.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wie kopiert man 3 Zeilen in vi?',
                options     = ['A) 3yy', 'B) copy 3', 'C) yank 3', 'D) c3'],
                correct     = 'A',
                explanation = "3yy = yank (kopieren) 3 Zeilen. Dann 'p' zum Einfügen nach dem Cursor.",
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "dd LÖSCHT in Puffer — der Inhalt ist nicht weg!\n"
            "dd + p = Zeile ausschneiden + einfügen = Zeile verschieben.\n"
            "yy + p = Zeile kopieren + einfügen = Zeile duplizieren."
        ),
        memory_tip   = "Merkhilfe: dd=delete, yy=yank(copy), p=paste, u=undo, .=repeat",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.07 — vi: Suchen und Ersetzen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.07",
        chapter      = 8,
        title        = "vi — Suchen, Ersetzen & Ex-Befehle",
        mtype        = "DECODE",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Die Config hat 200 Zeilen, Ghost.\n"
            " Der falsche Hostname steht 47 Mal drin.\n"
            " Du willst nicht 47 Mal i drücken.\n"
            " Lern vi-Suche und :s für globales Ersetzen.'"
        ),
        why_important = (
            "Suchen und Ersetzen in vi ist eine Kernkompetenz.\n"
            "LPIC-1 testet / Suche, n/N Navigation und :s/alt/neu/g."
        ),
        explanation  = (
            "VI SUCHE:\n\n"
            "  /muster     vorwärts suchen\n"
            "  ?muster     rückwärts suchen\n"
            "  n           nächsten Treffer (gleiche Richtung)\n"
            "  N           vorherigen Treffer (umgekehrte Richtung)\n"
            "  *           Wort unter Cursor vorwärts suchen\n"
            "  #           Wort unter Cursor rückwärts suchen\n\n"
            "VI EX-BEFEHLE (mit :):\n\n"
            "ERSETZEN:\n"
            "  :s/alt/neu/         erste Vorkommen in aktueller Zeile\n"
            "  :s/alt/neu/g        alle Vorkommen in aktueller Zeile\n"
            "  :%s/alt/neu/g       alle Vorkommen in GANZER DATEI\n"
            "  :%s/alt/neu/gc      mit Bestätigung (confirm)\n"
            "  :5,10s/alt/neu/g    Zeilen 5-10\n\n"
            "DATEI-BEFEHLE:\n"
            "  :w          speichern\n"
            "  :w datei    als neue Datei speichern\n"
            "  :q          beenden\n"
            "  :q!         beenden ohne Speichern\n"
            "  :wq         speichern und beenden\n"
            "  :x          wie :wq aber nur wenn geändert\n"
            "  ZZ          Normal-Modus: wie :wq\n"
            "  ZQ          Normal-Modus: wie :q!\n\n"
            "WEITERE EX-BEFEHLE:\n"
            "  :set number     Zeilennummern anzeigen\n"
            "  :set nonumber   Zeilennummern ausschalten\n"
            "  :syntax on      Syntax-Highlighting\n"
            "  :e datei        andere Datei öffnen\n"
            "  :! befehl       Shell-Befehl ausführen"
        ),
        syntax       = "/MUSTER  |  :%s/alt/neu/g  |  :wq",
        example      = (
            "/root               # suche 'root' vorwärts\n"
            "n                   # nächsten Treffer\n"
            ":%s/root/ghost/g    # alle 'root' durch 'ghost' ersetzen\n"
            ":%s/root/ghost/gc   # mit Bestätigung\n"
            ":set number         # Zeilennummern einschalten\n"
            ":42                 # direkt zu Zeile 42 springen"
        ),
        task_description = "Wie ersetzt du in vi alle Vorkommen von 'http' durch 'https' in der ganzen Datei?",
        expected_commands = [":%s/http/https/g"],
        hint_text    = ":%s/suche/ersatz/g — % bedeutet GESAMTE Datei, /g = global (alle Vorkommen)",
        quiz_questions    = [
            QuizQuestion(
                question    = "Wie ersetzt man in vi ALLE Vorkommen von 'alt' durch 'neu' in der ganzen Datei?",
                options     = ['A) :s/alt/neu/', 'B) :%s/alt/neu/g', 'C) :replace alt neu', 'D) /alt → :change/neu'],
                correct     = 'B',
                explanation = ':%s/alt/neu/g = % (ganze Datei) s (substitute) /g (global). :s ohne % = nur aktuelle Zeile.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was bedeutet ':q!' in vi?",
                options     = ['A) Speichern und beenden', 'B) Beenden OHNE zu speichern (force quit)', 'C) Quit interaktiv', 'D) Fehler: ungültiger Befehl'],
                correct     = 'B',
                explanation = ':q! = force quit ohne Speichern. Das ! überschreibt die Änderungs-Warnung.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "KRITISCH für LPIC-1:\n"
            "  :s/x/y/   → NUR erste Vorkommen in DIESER Zeile\n"
            "  :%s/x/y/g → ALLE Vorkommen in der GANZEN Datei\n"
            "Das % ist das Bereichsselektor für die gesamte Datei!"
        ),
        memory_tip   = "Merkhilfe: % = gesamte Datei, g = global, c = confirm",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.08 — Regex: POSIX Zeichenklassen & Quantifizierer
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.08",
        chapter      = 8,
        title        = "POSIX Klassen & Quantifizierer",
        mtype        = "DECODE",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'POSIX-Klassen sind der sichere Weg, Ghost.\n"
            " [0-9] funktioniert für ASCII.\n"
            " Aber [:digit:] ist offiziell POSIX — was LPIC testet.\n"
            " Kenn den Unterschied.'"
        ),
        why_important = (
            "POSIX-Zeichenklassen werden in LPIC-1-Prüfungen explizit abgefragt.\n"
            "Quantifizierer bestimmen Wiederholungsanzahl."
        ),
        explanation  = (
            "POSIX ZEICHENKLASSEN (innerhalb von []):\n\n"
            "  [:alpha:]   Buchstaben [a-zA-Z]\n"
            "  [:digit:]   Ziffern [0-9]\n"
            "  [:alnum:]   Alphanumerisch [a-zA-Z0-9]\n"
            "  [:space:]   Whitespace (Leerzeichen, Tab, Newline)\n"
            "  [:blank:]   Leerzeichen und Tab\n"
            "  [:upper:]   Großbuchstaben [A-Z]\n"
            "  [:lower:]   Kleinbuchstaben [a-z]\n"
            "  [:print:]   Druckbare Zeichen\n"
            "  [:punct:]   Satzzeichen\n\n"
            "VERWENDUNG: grep '[[:digit:]]' datei\n\n"
            "QUANTIFIZIERER (ERE mit grep -E):\n\n"
            "  *       0 oder mehr  (BRE und ERE)\n"
            "  +       1 oder mehr  (nur ERE)\n"
            "  ?       0 oder 1     (nur ERE)\n"
            "  {n}     genau n      z.B. [0-9]{3}\n"
            "  {n,}    mindestens n\n"
            "  {n,m}   zwischen n und m\n\n"
            "IN BRE müssen + ? { } escaped werden: \\+ \\? \\{\\}\n\n"
            "ANKER:\n"
            "  ^       Zeilenanfang\n"
            "  $       Zeilenende\n"
            "  \\b      Wortgrenze (PCRE/ERE)\n"
            "  \\<      Wortanfang (BRE)\n"
            "  \\>      Wortende (BRE)"
        ),
        syntax       = "grep '[[:digit:]]' DATEI  |  grep -E '[0-9]{3}' DATEI",
        example      = (
            "grep '[[:alpha:]]' datei        # Zeilen mit Buchstaben\n"
            "grep -E '[[:digit:]]{4}' datei  # mind. 4 Ziffern\n"
            "grep -E '^[[:upper:]]' datei    # Großbuchstabe am Anfang\n"
            "grep -E '[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' file  # IPv4"
        ),
        task_description = "Zeige Zeilen in /etc/passwd die mindestens eine Ziffer enthalten (POSIX-Klasse)",
        expected_commands = ["grep '[[:digit:]]' /etc/passwd"],
        hint_text    = "POSIX-Klasse für Ziffern: [[:digit:]] — in doppelten eckigen Klammern!",
        quiz_questions    = [
            QuizQuestion(
                question    = "Wie schreibt man 'eine oder mehrere Ziffern' als POSIX-Klasse in grep?",
                options     = ["A) grep '[digit]+' datei", "B) grep '[[:digit:]]\\+' datei", "C) grep '\\d+' datei", "D) grep '[0-9]+' datei"],
                correct     = 'B',
                explanation = 'POSIX: [[:digit:]] in doppelten Klammern. Mit BRE braucht + einen Backslash: \\+',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was ist der Unterschied zwischen [[:alpha:]] und [a-z]?',
                options     = ['A) Kein Unterschied', 'B) [[:alpha:]] ist POSIX-konform und locale-aware', 'C) [a-z] ist korrekter', 'D) [[:alpha:]] nur für Großbuchstaben'],
                correct     = 'B',
                explanation = '[[:alpha:]] ist POSIX-offiziell und berücksichtigt Locale (Umlaute etc.). Beide funktionieren aber POSIX ist korrekter.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "POSIX-Klassen stehen in doppelten Klammern: [[:digit:]]\n"
            "Nicht verwechseln mit [0-9] (auch korrekt aber nicht POSIX-offiziell)\n"
            "LPIC-1 fragt explizit nach [:alpha:], [:digit:], [:space:]"
        ),
        memory_tip   = "Merkhilfe: [[:alpha:]] = letters, [[:digit:]] = digits, [[:space:]] = whitespace",
        gear_reward  = None,
        faction_reward = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.09 — Regex Zeichenklassen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.09",
        chapter      = 8,
        title        = "Regex Zeichenklassen — [a-z], [A-Z0-9], POSIX",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'Die Datenbänke des Imperiums sind voll von\n"
            " Mustern, Ghost. Großbuchstaben-Codes. Zahlenpräfixe.\n"
            " Wer Zeichenklassen beherrscht, filtert das Rauschen heraus\n"
            " und findet den einen Eintrag — in Millisekunden.'"
        ),
        why_important = (
            "Zeichenklassen sind das Rückgrat jedes Regex-Musters.\n"
            "LPIC-1 Topic 103.7 prüft sowohl POSIX-Klassen als auch\n"
            "einfache Bereiche. Kenntnis beider Schreibweisen ist Pflicht."
        ),
        explanation  = (
            "ZEICHENKLASSEN IN REGEX:\n\n"
            "EINFACHE BEREICHE:\n"
            "  [a-z]        Kleinbuchstaben a bis z\n"
            "  [A-Z]        Großbuchstaben A bis Z\n"
            "  [0-9]        Ziffern 0 bis 9\n"
            "  [A-Z0-9]     Großbuchstaben ODER Ziffern\n"
            "  [a-zA-Z]     beliebiger Buchstabe\n"
            "  [^a-z]       NICHT Kleinbuchstabe (negierte Klasse)\n\n"
            "POSIX-KLASSEN (innerhalb von [ ]):\n"
            "  [:alpha:]    Buchstaben [a-zA-Z]\n"
            "  [:digit:]    Ziffern [0-9]\n"
            "  [:alnum:]    Alphanumerisch [a-zA-Z0-9]\n"
            "  [:upper:]    Großbuchstaben [A-Z]\n"
            "  [:lower:]    Kleinbuchstaben [a-z]\n"
            "  [:space:]    Whitespace (Leerzeichen, Tab, Newline)\n"
            "  [:blank:]    Leerzeichen und Tab\n"
            "  [:print:]    Druckbare Zeichen\n"
            "  [:punct:]    Satzzeichen\n"
            "  [:xdigit:]   Hex-Ziffern [0-9a-fA-F]\n\n"
            "WICHTIG: POSIX-Klassen brauchen doppelte Klammern:\n"
            "  grep '[[:digit:]]' datei   ← korrekt\n"
            "  grep '[:digit:]' datei     ← FALSCH (fehlende äußere [])\n\n"
            "ANWENDUNGSBEISPIELE:\n"
            "  grep '^[[:upper:]]' datei  Zeilen die mit Großbuchst. beginnen\n"
            "  grep '[[:digit:]]$' datei  Zeilen die mit Ziffer enden\n"
            "  grep '[^[:alnum:]]' datei  Zeilen mit Sonderzeichen"
        ),
        syntax       = "grep '[[:CLASS:]]' DATEI  |  grep '[BEREICH]' DATEI",
        example      = (
            "grep '[[:upper:]]' /etc/passwd       # Einträge mit Großbuchstaben\n"
            "grep '^[[:alpha:]]' /etc/services    # Zeilen die mit Buchstaben beginnen\n"
            "grep '[[:digit:]]\\{4\\}' datei      # genau 4 Ziffern (BRE)\n"
            "grep -E '[[:digit:]]{4}' datei       # genau 4 Ziffern (ERE)\n"
            "grep '[^[:print:]]' datei            # nicht-druckbare Zeichen finden"
        ),
        task_description = "Finde Zeilen in /etc/passwd die mit einem Großbuchstaben beginnen (POSIX)",
        expected_commands = ["grep '^[[:upper:]]' /etc/passwd"],
        hint_text    = "POSIX-Klassen in doppelten Klammern: [[:upper:]] für Großbuchstaben, ^ für Zeilenanfang",
        quiz_questions = [
            QuizQuestion(
                question   = "Welche POSIX-Klasse matcht alphanumerische Zeichen?",
                options    = [
                    "[:alpha:]",
                    "[:alnum:]",
                    "[:digit:]",
                    "[:print:]",
                ],
                correct    = 1,
                explanation = (
                    "[:alnum:] entspricht [a-zA-Z0-9] — Buchstaben und Ziffern.\n"
                    "[:alpha:] = nur Buchstaben, [:digit:] = nur Ziffern."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie matcht man korrekt Ziffern mit POSIX in grep?",
                options    = [
                    "grep '[:digit:]' datei",
                    "grep '[[:digit:]]' datei",
                    "grep '\\d' datei",
                    "grep '[digit]' datei",
                ],
                correct    = 1,
                explanation = (
                    "POSIX-Klassen brauchen doppelte eckige Klammern: [[:digit:]].\n"
                    "[:digit:] allein ist eine falsche Schreibweise in grep."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Prüfung: POSIX-Klassen immer in doppelten Klammern!\n"
            "  [[:digit:]]  → korrekt\n"
            "  [:digit:]    → FALSCH (fehlende äußere [])\n"
            "Beide Schreibweisen ([0-9] und [[:digit:]]) sind inhaltlich äquivalent."
        ),
        memory_tip   = "Merkhilfe: POSIX = doppelt geklammert: [[:alpha:]] [[:digit:]] [[:space:]]",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.10 — Regex Quantifizierer
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.10",
        chapter      = 8,
        title        = "Regex Quantifizierer — ?, +, *, {n,m}, greedy",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Das Log-Protokoll hat Felder unterschiedlicher Länge.\n"
            " Manchmal 3 Ziffern. Manchmal 6. Manchmal keine.\n"
            " Quantifizierer sagen deinem Regex wie oft ein Muster\n"
            " wiederholt werden darf — das ist die Präzisionswaffe.'"
        ),
        why_important = (
            "Quantifizierer steuern die Häufigkeit von Muster-Matches.\n"
            "LPIC-1 prüft BRE vs ERE Unterschiede bei +, ? und {n,m}.\n"
            "Greedy vs Lazy ist konzeptuell wichtig für Prüfungen."
        ),
        explanation  = (
            "QUANTIFIZIERER — WIEDERHOLUNGSANZAHL:\n\n"
            "IN BRE (grep ohne -E) UND ERE (grep -E):\n"
            "  *       0 oder mehr Wiederholungen des vorherigen Elements\n\n"
            "NUR IN ERE (grep -E, egrep, sed -E):\n"
            "  +       1 oder mehr Wiederholungen\n"
            "  ?       0 oder 1 Wiederholung (optional)\n"
            "  {n}     genau n Wiederholungen\n"
            "  {n,}    mindestens n Wiederholungen\n"
            "  {n,m}   zwischen n und m Wiederholungen\n\n"
            "IN BRE müssen +, ?, {, } mit Backslash escaped werden:\n"
            "  grep 'x\\+' datei     1 oder mehr x (BRE)\n"
            "  grep -E 'x+' datei   1 oder mehr x (ERE)\n\n"
            "GREEDY vs LAZY:\n"
            "  Standardmäßig: GREEDY (so viel wie möglich)\n"
            "  Beispiel: .* matcht so weit wie möglich\n"
            "  Lazy (PCRE mit ?): .*? matcht so wenig wie möglich\n"
            "  grep unterstützt kein Lazy (nur PCRE/grep -P)\n\n"
            "BEISPIEL-MUSTER:\n"
            "  [0-9]*      0 oder mehr Ziffern (matcht auch leere Strings)\n"
            "  [0-9]+      mindestens eine Ziffer\n"
            "  colou?r     colour oder color\n"
            "  [0-9]{3}    genau 3 Ziffern\n"
            "  [0-9]{2,4}  2 bis 4 Ziffern"
        ),
        syntax       = "grep -E 'MUSTER+' DATEI  |  grep -E 'MUSTER{n,m}' DATEI",
        example      = (
            "grep -E '[0-9]+' /etc/passwd          # Zeilen mit mind. einer Ziffer\n"
            "grep -E '^[a-z]{3,8}:' /etc/passwd    # Benutzernamen 3-8 Zeichen\n"
            "grep -E 'https?' /etc/hosts            # http oder https\n"
            "grep -E '[0-9]{1,3}(\\.[0-9]{1,3}){3}' datei  # IPv4-ähnlich\n"
            "grep -E '^#{1,6} ' README.md           # Markdown-Überschriften"
        ),
        task_description = "Finde Zeilen in /etc/passwd bei denen der Benutzername 4 bis 8 Zeichen hat",
        expected_commands = ["grep -E '^[a-z_][a-z0-9_-]{3,7}:' /etc/passwd"],
        hint_text    = "grep -E '^[a-z_][a-z0-9_-]{3,7}:' — {3,7} heißt 3 bis 7 weitere Zeichen nach dem ersten",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen * und + in ERE?",
                options    = [
                    "* matcht 0 oder mehr, + matcht 1 oder mehr",
                    "* matcht 1 oder mehr, + matcht 0 oder mehr",
                    "Beide matchen 0 oder mehr Zeichen",
                    "* ist für Zahlen, + ist für Buchstaben",
                ],
                correct    = 0,
                explanation = (
                    "* = 0 oder mehr (auch kein Match ist ok).\n"
                    "+ = 1 oder mehr (mindestens ein Vorkommen nötig).\n"
                    "+ ist nur in ERE (grep -E) ohne Backslash verfügbar."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie schreibt man {n,m} in BRE (ohne grep -E)?",
                options    = [
                    "{n,m}",
                    "\\{n,m\\}",
                    "(n,m)",
                    "\\(n,m\\)",
                ],
                correct    = 1,
                explanation = (
                    "In BRE müssen geschweifte Klammern escaped werden: \\{n,m\\}.\n"
                    "In ERE (grep -E) schreibt man einfach {n,m} ohne Backslash."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "BRE vs ERE Quantifizierer-Unterschied:\n"
            "  BRE: * ohne Escape, aber \\+ \\? \\{n,m\\} mit Backslash\n"
            "  ERE: + ? {n,m} alle ohne Backslash (grep -E)\n"
            "Greedy ist der Standard — PCRE (-P) braucht man für Lazy."
        ),
        memory_tip   = "Merkhilfe: ? = optional, + = plus eins mindestens, {n,m} = von n bis m",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.11 — Regex Gruppen & Alternation
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.11",
        chapter      = 8,
        title        = "Regex Gruppen & Alternation — (abc|def), \\1",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'Der Imperium-Log hat zwei Formate, Ghost.\n"
            " ERROR: und WARN: — beide müssen gefunden werden.\n"
            " Mit Alternation und Gruppen bündelst du Muster.\n"
            " Ein Befehl. Zwei Feinde. Erledigt.'"
        ),
        why_important = (
            "Gruppen und Alternation ermöglichen mächtige Muster-Kombinationen.\n"
            "Rückverweise (\\1) sind ein LPIC-1-Prüfungsthema in sed und grep."
        ),
        explanation  = (
            "GRUPPEN IN REGEX (ERE):\n\n"
            "CAPTURING GROUPS:\n"
            "  (muster)     Gruppe: fasst Muster zusammen + speichert Match\n"
            "  (abc)+       Gruppe 'abc' 1 oder mehr mal\n"
            "  (foo|bar)    Gruppe mit Alternation: foo oder bar\n\n"
            "ALTERNATION:\n"
            "  foo|bar      matcht 'foo' oder 'bar'\n"
            "  (cat|dog)s   matcht 'cats' oder 'dogs'\n"
            "  grep -E 'error|warning|critical'  drei Alternativen\n\n"
            "RÜCKVERWEISE (Backreferences):\n"
            "  \\1   referenziert Gruppe 1\n"
            "  \\2   referenziert Gruppe 2\n"
            "  Beispiel: grep -E '([a-z])\\1'  findet doppelte Buchstaben\n"
            "  In sed: sed 's/\\(word\\)/[\\1]/'  Gruppe in Ersatz nutzen\n\n"
            "IN BRE müssen Klammern escaped werden:\n"
            "  grep '\\(foo\\|bar\\)' datei   BRE Gruppe + Alternation\n"
            "  grep -E '(foo|bar)' datei    ERE (sauberer)\n\n"
            "NON-CAPTURING GROUPS (PCRE):\n"
            "  (?:muster)   Gruppe ohne Speicherung (nur grep -P)"
        ),
        syntax       = "grep -E '(MUSTER1|MUSTER2)' DATEI  |  sed 's/\\(GROUP\\)/[\\1]/'",
        example      = (
            "grep -E '(error|warning)' /var/log/syslog\n"
            "grep -E '^(root|ghost|daemon):' /etc/passwd\n"
            "grep -E '([0-9])\\1' datei          # doppelte Ziffern (11, 22, ...)\n"
            "sed 's/\\([a-z]*\\)_\\([a-z]*\\)/\\2_\\1/' datei  # Wörter tauschen\n"
            "echo 'foofoo' | grep -E '(foo)\\1'  # Wort-Wiederholung"
        ),
        task_description = "Finde Zeilen in /etc/passwd die mit 'root' oder 'daemon' beginnen",
        expected_commands = ["grep -E '^(root|daemon):' /etc/passwd"],
        hint_text    = "grep -E '^(root|daemon):' — Klammern gruppieren, | ist Alternation (ODER)",
        quiz_questions = [
            QuizQuestion(
                question   = "Was matcht das Regex-Muster '(ha)+'?",
                options    = [
                    "Nur 'ha'",
                    "'ha', 'haha', 'hahaha' usw.",
                    "Nur 'h' oder 'a'",
                    "Alles zwischen h und a",
                ],
                correct    = 1,
                explanation = (
                    "(ha)+ bedeutet: die Gruppe 'ha' einmal oder mehrfach.\n"
                    "Matcht 'ha', 'haha', 'hahaha' — aber nicht 'h' oder 'a' allein."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie aktiviert man Gruppen und Alternation ohne Backslash?",
                options    = [
                    "grep 'muster' datei",
                    "grep -F 'muster' datei",
                    "grep -E 'muster' datei",
                    "grep -v 'muster' datei",
                ],
                correct    = 2,
                explanation = (
                    "grep -E aktiviert Extended Regular Expressions (ERE).\n"
                    "In ERE sind ( ) | { } + ? ohne Backslash nutzbar.\n"
                    "In BRE (ohne -E) muss man \\( \\) \\| schreiben."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Prüfungstipp: Gruppen in BRE vs ERE:\n"
            "  BRE: \\(foo\\|bar\\) — Backslash vor Klammern und |\n"
            "  ERE: (foo|bar)     — kein Backslash nötig (grep -E)\n"
            "Rückverweise: \\1 referenziert die erste Capture-Gruppe."
        ),
        memory_tip   = "Merkhilfe: ( ) = Gruppe, | = ODER, \\1 = Rückverweis auf Gruppe 1",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.12 — sed mit Regex: Adressbereiche & Capturing
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.12",
        chapter      = 8,
        title        = "sed mit Regex — Adressbereiche & Capturing-Gruppen",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Die Config-Datei hat Sektionen, Ghost.\n"
            " Nur zwischen [network] und [/network] soll geändert werden.\n"
            " sed-Adressbereiche sind der chirurgische Eingriff.\n"
            " Kein Kollateralschaden. Präzision.'"
        ),
        why_important = (
            "sed-Adressbereiche und Capturing-Gruppen ermöglichen\n"
            "gezielte Bearbeitungen in Dateisektionen.\n"
            "LPIC-1 testet Adresssyntax, \\w und Rückverweise in sed."
        ),
        explanation  = (
            "SED ADRESSBEREICHE:\n\n"
            "ZEILEN-ADRESSIERUNG:\n"
            "  sed '5s/alt/neu/' datei      nur Zeile 5\n"
            "  sed '5,10s/alt/neu/' datei   Zeilen 5 bis 10\n"
            "  sed '5,+3s/alt/neu/' datei   Zeile 5 und 3 weitere\n"
            "  sed '$s/alt/neu/' datei      letzte Zeile\n\n"
            "MUSTER-ADRESSIERUNG:\n"
            "  sed '/START/,/STOP/s/x/y/'  von START bis STOP ersetzen\n"
            "  sed '/^#/d' datei            Kommentarzeilen löschen\n"
            "  sed '/^$/d' datei            Leerzeilen löschen\n\n"
            "REGEX IN SED:\n"
            "  \\w       Wortzeichen [a-zA-Z0-9_] (GNU-Erweiterung)\n"
            "  \\s       Whitespace\n"
            "  \\d       Ziffer (nur GNU sed)\n\n"
            "CAPTURING-GRUPPEN IN sed:\n"
            "  sed 's/\\(GRUPPE1\\) \\(GRUPPE2\\)/\\2 \\1/' datei   tauscht Gruppen\n"
            "  Verwendung: \\1, \\2, ... im Ersatz-Teil\n\n"
            "BEISPIEL CAPTURING:\n"
            "  sed 's/\\([0-9]\\{4\\}\\)-\\([0-9]\\{2\\}\\)-\\([0-9]\\{2\\}\\)/\\3.\\2.\\1/'\n"
            "  → wandelt 2025-04-20 in 20.04.2025 um\n\n"
            "MEHRERE BEFEHLE:\n"
            "  sed -e 's/foo/bar/' -e '/^#/d' datei\n"
            "  sed -f skript.sed datei    sed-Skript aus Datei"
        ),
        syntax       = "sed 'ADDR s/ALT/NEU/FLAGS' DATEI  |  sed '/PAT1/,/PAT2/BEFEHL'",
        example      = (
            "sed '/^#/d; /^$/d' /etc/ssh/sshd_config  # Kommentare + Leerzeilen\n"
            "sed -n '/\\[network\\]/,/\\[\\/network\\]/p' config.ini  # Sektion ausgeben\n"
            "sed 's/\\b\\(\\w\\+\\)\\b/[\\1]/g' datei  # jedes Wort in [] einrahmen\n"
            "sed 's/\\([a-z]\\+\\) \\([a-z]\\+\\)/\\2 \\1/' datei  # zwei Wörter tauschen\n"
            "sed '1~2s/^/> /' datei  # jede ungerade Zeile mit > markieren"
        ),
        task_description = "Lösche alle Kommentar- und Leerzeilen aus /etc/ssh/sshd_config",
        expected_commands = ["sed '/^#/d; /^$/d' /etc/ssh/sshd_config"],
        hint_text    = "sed '/^#/d' löscht Kommentare, '/^$/d' löscht Leerzeilen — beide mit ; kombinieren",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht 'sed -i.bak s/foo/bar/g datei'?",
                options    = [
                    "Ersetzt foo durch bar und gibt das Ergebnis aus",
                    "Ersetzt foo durch bar direkt in der Datei und erstellt datei.bak",
                    "Erstellt eine Backup-Datei ohne Änderung",
                    "Gibt einen Fehler aus, weil -i und .bak zusammen nicht erlaubt sind",
                ],
                correct    = 1,
                explanation = (
                    "sed -i.bak ändert die Datei direkt (in-place) und\n"
                    "erstellt vorher ein Backup mit Endung .bak.\n"
                    "sed -i ohne Endung ändert direkt ohne Backup."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Wie referenziert man die erste Capturing-Gruppe im Ersatz-Teil von sed?",
                options    = [
                    "$1",
                    "\\1",
                    "%1",
                    "(1)",
                ],
                correct    = 1,
                explanation = (
                    "In sed (BRE) wird die erste Gruppe mit \\( \\) gebildet\n"
                    "und im Ersatz mit \\1 referenziert.\n"
                    "In sed -E (ERE) sind es ( ) für die Gruppe, aber \\1 im Ersatz."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 sed-Prüfungstipps:\n"
            "  sed '/PAT1/,/PAT2/' → Bereichsadressierung (zwischen Muster)\n"
            "  sed -i → in-place (Datei direkt ändern)\n"
            "  \\1 \\2 → Rückverweise auf Capturing-Gruppen im s-Befehl\n"
            "  sed -e und sed -f für mehrere Befehle"
        ),
        memory_tip   = "Merkhilfe: sed = Stream EDitor: s=substitute d=delete p=print n=next",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.13 — vim Suchen & Ersetzen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.13",
        chapter      = 8,
        title        = "vim Suchen & Ersetzen — :%s, :g/pattern/d, Flags",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'Die Konfig hat tausend Zeilen, Ghost.\n"
            " Dein Ziel: alle alten API-Endpunkte ersetzen.\n"
            " Manuell? Unmöglich. Mit vim :%s — ein Befehl.\n"
            " Lern die Flags i, g und c — sie retten Leben.'"
        ),
        why_important = (
            "vim :%s ist das mächtigste Suchen-Ersetzen-Tool im Editor.\n"
            "LPIC-1 Topic 103.8 prüft :%s-Syntax, Flags und :g-Befehl.\n"
            "Im Produktiveinsatz täglich relevant."
        ),
        explanation  = (
            "VIM SUCHEN & ERSETZEN:\n\n"
            "SUCHE:\n"
            "  /muster      vorwärts suchen\n"
            "  ?muster      rückwärts suchen\n"
            "  n / N        nächsten / vorherigen Treffer\n"
            "  *            Wort unter Cursor suchen (vorwärts)\n"
            "  :noh         Suchhervorhebung ausschalten\n\n"
            "ERSETZEN MIT :s:\n"
            "  :s/alt/neu/         1. Vorkommen in aktueller Zeile\n"
            "  :s/alt/neu/g        alle in aktueller Zeile\n"
            "  :%s/alt/neu/g       alle in GANZER DATEI\n"
            "  :5,20s/alt/neu/g    nur Zeilen 5 bis 20\n"
            "  :%s/alt/neu/gc      mit Bestätigung (c = confirm)\n"
            "  :%s/alt/neu/gi      case-insensitive + global\n"
            "  :%s/\\<alt\\>/neu/g  nur ganzes Wort ersetzen\n\n"
            "FLAGS FÜR :s:\n"
            "  g    global (alle Vorkommen in der Zeile)\n"
            "  i    case-insensitive\n"
            "  c    confirm (bei jedem Vorkommen nachfragen)\n"
            "  e    kein Fehler wenn kein Treffer\n\n"
            ":g BEFEHL (global):\n"
            "  :g/muster/d          Zeilen mit Muster löschen\n"
            "  :g/^#/d              alle Kommentarzeilen löschen\n"
            "  :g/^$/d              alle Leerzeilen löschen\n"
            "  :g/muster/p          Zeilen mit Muster ausgeben\n"
            "  :v/muster/d          Zeilen OHNE Muster löschen (inverse g)"
        ),
        syntax       = ":%s/ALT/NEU/FLAGS  |  :g/MUSTER/d  |  :v/MUSTER/d",
        example      = (
            ":%s/http:/https:/g        # alle http durch https\n"
            ":%s/old_host/new_host/gc  # mit Bestätigung\n"
            ":g/^#/d                   # alle Kommentare löschen\n"
            ":g/^$/d                   # alle Leerzeilen löschen\n"
            ":5,50s/foo/bar/gi         # Zeilen 5-50, case-insensitive\n"
            ":%s/\\s\\+$//             # trailing Whitespace entfernen"
        ),
        task_description = "Wie ersetzt du in vim alle 'localhost' durch '127.0.0.1' in der gesamten Datei mit Bestätigung?",
        expected_commands = [":%s/localhost/127.0.0.1/gc"],
        hint_text    = ":%s/suche/ersatz/gc — % = ganze Datei, g = global, c = confirm (bestätigen)",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt das Flag 'c' in ':%s/foo/bar/gc'?",
                options    = [
                    "Case-insensitive Suche",
                    "Bestätigung bei jedem Ersetzen",
                    "Komprimierte Ausgabe",
                    "Kein Fehler wenn kein Treffer",
                ],
                correct    = 1,
                explanation = (
                    "c = confirm: vim fragt bei jedem Vorkommen nach (y/n/a/q).\n"
                    "i = case-insensitive, e = no-error, g = global."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was macht ':g/^#/d' in vim?",
                options    = [
                    "Sucht Zeilen die mit # beginnen",
                    "Löscht alle Zeilen die mit # beginnen",
                    "Ersetzt # durch leer",
                    "Zählt Zeilen die mit # beginnen",
                ],
                correct    = 1,
                explanation = (
                    ":g/MUSTER/BEFEHL führt den Befehl auf alle Matching-Zeilen aus.\n"
                    ":g/^#/d löscht (d) alle Zeilen die mit # beginnen (Kommentare)."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 vim Prüfungstipps:\n"
            "  :s vs :%s: ohne % nur aktuelle Zeile!\n"
            "  Flags: g=global, i=case-insensitive, c=confirm\n"
            "  :g/muster/d → alle Zeilen mit Muster löschen\n"
            "  :v/muster/d → alle Zeilen OHNE Muster löschen"
        ),
        memory_tip   = "Merkhilfe: :%s = Prozent (ganze Datei) + s (substitute). Flags: g i c",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.14 — vim Makros
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.14",
        chapter      = 8,
        title        = "vim Makros — qa, @a, Zähler & Wiederholungen",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Gleiche Aktion. 200 Zeilen. Ghost.\n"
            " Du drückst nicht 200 Mal dieselbe Taste.\n"
            " Du nimmst ein Makro auf. Du spielst es 200 Mal ab.\n"
            " vim-Makros sind dein Force-Multiplier.'"
        ),
        why_important = (
            "Makros automatisieren repetitive Bearbeitungen in vim.\n"
            "LPIC-1 Topic 103.8 prüft Makro-Aufnahme und Abspielung.\n"
            "In Prüfungen kommen Fragen zu qa...q und @a."
        ),
        explanation  = (
            "VIM MAKROS:\n\n"
            "MAKRO AUFNEHMEN:\n"
            "  qa       Aufnahme starten in Register 'a'\n"
            "  ...      Befehle ausführen die aufgezeichnet werden\n"
            "  q        Aufnahme beenden\n\n"
            "MAKRO ABSPIELEN:\n"
            "  @a       Makro aus Register 'a' einmal ausführen\n"
            "  5@a      Makro 5 Mal ausführen\n"
            "  @@       letztes Makro wiederholen\n"
            "  100@a    Makro 100 Mal (stoppt bei Fehler)\n\n"
            "REGISTER:\n"
            "  a-z      26 mögliche Makro-Register\n"
            "  :reg     alle Register anzeigen\n"
            "  :reg a   Register 'a' anzeigen\n\n"
            "MAKRO BEISPIEL — Zeile formatieren:\n"
            "  1. qa            Aufnahme in Register a\n"
            "  2. 0             Zeilenanfang\n"
            "  3. i[ <ESC>      [ am Anfang einfügen\n"
            "  4. A ]<ESC>      ] am Ende einfügen\n"
            "  5. j             nächste Zeile\n"
            "  6. q             Aufnahme beenden\n"
            "  7. 10@a          10 Mal ausführen\n\n"
            "ZÄHLER (Count) IN vim:\n"
            "  5dd      5 Zeilen löschen\n"
            "  10j      10 Zeilen runter\n"
            "  3yy      3 Zeilen kopieren\n"
            "  Zähler vor fast jeden Normal-Befehl stellbar"
        ),
        syntax       = "qa [Befehle] q  |  @a  |  N@a",
        example      = (
            "# Makro aufnehmen das jede Zeile in Anführungszeichen setzt:\n"
            "qa            # Start: Register a\n"
            "I\"<ESC>       # \" am Zeilenanfang\n"
            "A\"<ESC>       # \" am Zeilenende\n"
            "j             # nächste Zeile\n"
            "q             # Aufnahme beenden\n"
            "9@a           # 9 weitere Zeilen bearbeiten\n"
            "@@ # letztes Makro nochmal"
        ),
        task_description = "Mit welchem Befehl startet man die Makro-Aufnahme in Register 'b'?",
        expected_commands = ["qb"],
        hint_text    = "q + Registerbuchstabe startet die Aufnahme. qb = Aufnahme in Register b",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht '5@a' in vim?",
                options    = [
                    "Springt zu Zeile 5 mit Makro a",
                    "Führt das Makro in Register 'a' fünfmal aus",
                    "Speichert das Makro in Register 5",
                    "Zeigt Register a an",
                ],
                correct    = 1,
                explanation = (
                    "Zähler vor @a wiederholt das Makro entsprechend oft.\n"
                    "5@a = Makro aus Register 'a' fünfmal ausführen.\n"
                    ":reg a zeigt den Inhalt von Register a."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welche Tastenkombination beendet die Makro-Aufnahme in vim?",
                options    = [
                    "ESC",
                    "Ctrl+C",
                    "q (im Normal-Modus)",
                    ":stoprecord",
                ],
                correct    = 2,
                explanation = (
                    "q (im Normal-Modus) beendet die Makro-Aufnahme.\n"
                    "Aufnahme starten: q + Registerbuchstabe.\n"
                    "ESC bringt zurück in den Normal-Modus aber beendet keine Aufnahme."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 vim Makro-Ablauf:\n"
            "  1. qa — Aufnahme starten (Register a)\n"
            "  2. Befehle eingeben\n"
            "  3. q — Aufnahme beenden\n"
            "  4. @a — einmal ausführen\n"
            "  5. N@a — N-mal ausführen\n"
            "  :reg — Register-Inhalt anzeigen"
        ),
        memory_tip   = "Merkhilfe: q=quit-recording, @=playback, @@=repeat last",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.15 — grep Flags
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.15",
        chapter      = 8,
        title        = "grep Flags — -v, -n, -r, -l, -c, -i, -A, -B, -C",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'grep ohne Flags ist ein stumpfes Schwert, Ghost.\n"
            " -r durchsucht ganze Verzeichnisbäume.\n"
            " -A und -B geben dir Kontext um den Treffer.\n"
            " -l sagt dir nur welche Datei — perfekt für Skripte.'"
        ),
        why_important = (
            "grep-Flags sind Kerninhalte von LPIC-1 Topic 103.7.\n"
            "Kontext-Flags (-A, -B, -C) und -r, -l werden regelmäßig geprüft.\n"
            "Kombinationen mehrerer Flags sind im Prüfungsalltag Standard."
        ),
        explanation  = (
            "GREP FLAGS — VOLLSTÄNDIGE ÜBERSICHT:\n\n"
            "FILTER-FLAGS:\n"
            "  -v    invert match — Zeilen die NICHT matchen\n"
            "  -i    case-insensitive — Groß/Klein ignorieren\n"
            "  -w    whole word — nur ganze Wörter matchen\n"
            "  -x    whole line — nur ganze Zeilen matchen\n\n"
            "OUTPUT-FLAGS:\n"
            "  -n    Zeilennummern vor jeder Ausgabe\n"
            "  -c    nur Anzahl der Treffer ausgeben\n"
            "  -l    nur Dateinamen mit Treffern (list files)\n"
            "  -L    Dateinamen OHNE Treffer\n"
            "  -o    nur den gematchten Teil ausgeben\n"
            "  -q    still (quiet) — kein Output, nur Exit-Code\n\n"
            "KONTEXT-FLAGS:\n"
            "  -A n  n Zeilen NACH dem Treffer (After)\n"
            "  -B n  n Zeilen VOR dem Treffer (Before)\n"
            "  -C n  n Zeilen um den Treffer (Context = -A n -B n)\n\n"
            "REKURSIV:\n"
            "  -r    rekursiv durch Verzeichnisse\n"
            "  -R    rekursiv inkl. Symlinks\n"
            "  --include='*.py'  nur bestimmte Dateitypen\n"
            "  --exclude='*.log' bestimmte Dateien ausschließen\n\n"
            "REGEX-MODI:\n"
            "  -E    Extended Regular Expressions (ERE)\n"
            "  -F    Fixed string (kein Regex)\n"
            "  -P    Perl-kompatible Regex (PCRE)\n"
            "  -G    Basic Regular Expressions (Standard)"
        ),
        syntax       = "grep [-Flags] 'MUSTER' [DATEI...]  |  grep -r 'MUSTER' VERZEICHNIS",
        example      = (
            "grep -n 'error' /var/log/syslog          # mit Zeilennummern\n"
            "grep -v '^#' /etc/ssh/sshd_config        # nicht-Kommentare\n"
            "grep -c 'FAILED' /var/log/auth.log       # nur Anzahl\n"
            "grep -l 'TODO' /home/ghost/*.py          # Dateiliste\n"
            "grep -A 3 'ERROR' /var/log/app.log       # 3 Zeilen nach Treffer\n"
            "grep -B 2 -A 2 'Segfault' /var/log/kern.log  # Kontext\n"
            "grep -ri 'password' /etc/                # rekursiv, case-insensitiv"
        ),
        task_description = "Suche rekursiv nach 'error' in /var/log/ und zeige nur die Dateinamen",
        expected_commands = ["grep -rl 'error' /var/log/"],
        hint_text    = "grep -r = rekursiv, -l = nur Dateinamen ausgeben (list files)",
        quiz_questions = [
            QuizQuestion(
                question   = "Was gibt 'grep -c muster datei' aus?",
                options    = [
                    "Den Inhalt der gematchten Zeilen",
                    "Nur die Anzahl der Treffer-Zeilen",
                    "Die Zeilennummern der Treffer",
                    "Dateinamen mit Treffern",
                ],
                correct    = 1,
                explanation = (
                    "-c = count: gibt nur die Anzahl der Zeilen aus die matchen.\n"
                    "-n gibt Zeilennummern, -l gibt Dateinamen, ohne Flag die Zeilen selbst."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welches Flag zeigt 2 Zeilen Kontext VOR dem Treffer?",
                options    = [
                    "-A 2",
                    "-B 2",
                    "-C 2",
                    "-P 2",
                ],
                correct    = 1,
                explanation = (
                    "-B 2 = Before: 2 Zeilen VOR dem Treffer anzeigen.\n"
                    "-A 2 = After: 2 Zeilen NACH dem Treffer.\n"
                    "-C 2 = Context: 2 Zeilen vor UND nach dem Treffer."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 grep Pflicht-Flags:\n"
            "  -v (invert), -i (case), -n (number), -c (count)\n"
            "  -l (list files), -r (recursive)\n"
            "  -A/-B/-C (context after/before/context)\n"
            "Kombination: grep -rni 'muster' /etc/ — häufig in Prüfungen!"
        ),
        memory_tip   = "Merkhilfe: A=After B=Before C=Context — wie im Alphabet, A vor B vor C",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.16 — vim Splits & Tabs
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.16",
        chapter      = 8,
        title        = "vim Splits & Tabs — Multi-Window Editing",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Du editierst drei Dateien gleichzeitig, Ghost.\n"
            " vim kann das — Splits und Tabs.\n"
            " :split öffnet horizontal. :vsplit vertikal.\n"
            " Ctrl+W+W springt zwischen Fenstern.'"
        ),
        why_important = (
            "vim Multi-Window ist LPIC-1 Topic 103.8 Prüfungsstoff.\n"
            "Splits ermöglichen gleichzeitiges Editieren mehrerer Dateien.\n"
            "Prüfung fragt nach :split/:vsplit und Ctrl+W Navigation."
        ),
        explanation  = (
            "VIM SPLITS & WINDOWS:\n\n"
            "FENSTER ÖFFNEN:\n"
            "  :split datei    horizontaler Split\n"
            "  :vsplit datei   vertikaler Split\n"
            "  :new            neues leeres horizontales Fenster\n"
            "  :vnew           neues leeres vertikales Fenster\n"
            "  Ctrl+W s        horizontaler Split (aktuell)\n"
            "  Ctrl+W v        vertikaler Split (aktuell)\n\n"
            "ZWISCHEN FENSTERN NAVIGIEREN:\n"
            "  Ctrl+W w        nächstes Fenster\n"
            "  Ctrl+W h/j/k/l  links/unten/oben/rechts\n"
            "  Ctrl+W =        gleiche Größe für alle\n"
            "  Ctrl+W _        maximieren (horizontal)\n"
            "  Ctrl+W |        maximieren (vertikal)\n"
            "  :windo cmd      Befehl in allen Fenstern\n"
            "  :q              aktuelles Fenster schließen\n\n"
            "TABS:\n"
            "  :tabnew         neues Tab\n"
            "  :tabnew datei   Datei in neuem Tab\n"
            "  gt / gT         nächstes/vorheriges Tab\n"
            "  :tabclose       Tab schließen\n"
            "  :tabs           alle Tabs auflisten\n\n"
            "PUFFER:\n"
            "  :ls / :buffers  alle Puffer anzeigen\n"
            "  :b N            zu Puffer N wechseln\n"
            "  :bn / :bp       nächster/vorheriger Puffer"
        ),
        syntax       = ":split [file]  |  :vsplit [file]  |  Ctrl+W {key}",
        example      = (
            ":split /etc/hosts         # horizontaler Split\n"
            ":vsplit /etc/fstab        # vertikaler Split\n"
            "Ctrl+W w                  # nächstes Fenster\n"
            "Ctrl+W =                  # gleiche Fenstergröße\n"
            ":tabnew ~/.bashrc         # neues Tab\n"
            "gt                        # nächstes Tab"
        ),
        task_description = "Öffne vim und erstelle einen horizontalen Split",
        expected_commands = [":split", "vim"],
        hint_text    = ":split oder :sp öffnet ein horizontales Split-Fenster in vim",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher vim-Befehl öffnet einen vertikalen Split?",
                options    = [
                    ":split",
                    ":vsplit",
                    ":vertical",
                    "Ctrl+W v",
                ],
                correct    = 1,
                explanation = (
                    ":vsplit = vertikaler Split. :split = horizontaler Split.\n"
                    "Ctrl+W v ist ein Shortcut für :vsplit des aktuellen Puffers.\n"
                    "Ctrl+W s entspricht :split."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 vim Splits:\n"
            "  :split = horizontal\n"
            "  :vsplit = vertikal\n"
            "  Ctrl+W w = nächstes Fenster\n"
            "  :tabnew = neues Tab\n"
            "  gt/gT = Tab navigieren"
        ),
        memory_tip   = "v in :vsplit = vertikal. Ctrl+W = Window-Control in vim.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.17 — vimrc Konfiguration
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.17",
        chapter      = 8,
        title        = "vimrc — vim Konfiguration & Anpassung",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ein Profi benutzt kein nacktes vim, Ghost.\n"
            " ~/.vimrc ist dein Cockpit.\n"
            " Syntax-Highlighting, Zeilennummern, Autoindent —\n"
            " konfiguriere vim für den Kampf.'"
        ),
        why_important = (
            "~/.vimrc ist die persönliche vim-Konfigurationsdatei.\n"
            "LPIC-1 erwartet Kenntnis der wichtigsten set-Optionen.\n"
            "Prüfungsfragen zu syntax on, set number, autoindent häufig."
        ),
        explanation  = (
            "VIMRC — VIM KONFIGURATION:\n\n"
            "DATEI: ~/.vimrc  (User) oder /etc/vim/vimrc (System)\n\n"
            "HÄUFIGE OPTIONEN:\n"
            "  set number          Zeilennummern anzeigen\n"
            "  set relativenumber  relative Zeilennummern\n"
            "  set syntax on       Syntax-Highlighting aktivieren\n"
            "  set autoindent      automatisches Einrücken\n"
            "  set smartindent     intelligentes Einrücken\n"
            "  set tabstop=4       Tab = 4 Leerzeichen (Anzeige)\n"
            "  set shiftwidth=4    Einrückbreite = 4\n"
            "  set expandtab       Tab durch Leerzeichen ersetzen\n"
            "  set hlsearch        Suchergebnisse hervorheben\n"
            "  set incsearch       inkrementelle Suche\n"
            "  set ignorecase      Groß-/Kleinschreibung ignorieren\n"
            "  set smartcase       case-sensitive bei Großbuchstaben\n"
            "  set wrap            Zeilen umbrechen\n"
            "  set nowrap          kein Umbruch\n"
            "  set background=dark dunkles Hintergrund-Theme\n"
            "  colorscheme desert  Farbschema setzen\n\n"
            "OPTIONEN PRÜFEN UND SETZEN:\n"
            "  :set number         Option in vim setzen\n"
            "  :set nonumber       Option deaktivieren\n"
            "  :set number?        Aktuellen Wert abfragen\n"
            "  :set all            alle Optionen anzeigen\n\n"
            "ABKÜRZUNGEN & MAPPINGS:\n"
            "  abbr teh the        Tippfehler-Korrektur\n"
            "  map <F2> :w<CR>     F2 = Speichern\n"
            "  inoremap jj <Esc>   jj = Escape im Insert-Modus"
        ),
        syntax       = "~/.vimrc  |  :set OPTION  |  :set noOPTION",
        example      = (
            "\" ~/.vimrc Beispiel:\n"
            "set number\n"
            "syntax on\n"
            "set autoindent\n"
            "set tabstop=4\n"
            "set expandtab\n"
            "set hlsearch\n"
            "colorscheme desert"
        ),
        task_description = "Erstelle eine ~/.vimrc mit Zeilennummern und Syntax-Highlighting",
        expected_commands = ["~/.vimrc", "set number", "syntax on"],
        hint_text    = "Erstelle ~/.vimrc mit 'set number' und 'syntax on' als Inhalt",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher vimrc-Eintrag aktiviert Syntax-Highlighting?",
                options    = [
                    "set highlight",
                    "syntax enable",
                    "set syntax on",
                    "syntax on",
                ],
                correct    = 3,
                explanation = (
                    "'syntax on' aktiviert Syntax-Highlighting in vim.\n"
                    "'syntax enable' ist ebenfalls gültig, aber 'syntax on' ist gebräuchlicher.\n"
                    "Beide können in ~/.vimrc verwendet werden."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 vimrc Optionen:\n"
            "  set number = Zeilennummern\n"
            "  syntax on = Highlighting\n"
            "  set autoindent = auto Einrücken\n"
            "  ~/.vimrc = User-Konfiguration\n"
            "  /etc/vim/vimrc = System-Konfiguration"
        ),
        memory_tip   = "vimrc = vim Run Commands. Jede Zeile ist ein vim-Befehl ohne den Doppelpunkt.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.18 — vim Plugins & Package Manager
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.18",
        chapter      = 8,
        title        = "vim Plugins & Package Manager — Erweiterungen",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "NEXUS",
        story        = (
            "NEXUS: 'Nacktes vim ist gut, Ghost.\n"
            " Aber mit Plugins wird es zur Waffe.\n"
            " vim-plug, native Packages — kenne deine Optionen.\n"
            " :PlugInstall und los.'"
        ),
        why_important = (
            "vim Plugin-Management ist moderner Linux-Admin-Alltag.\n"
            "Native Packages (vim 8+) und vim-plug sind Standard.\n"
            "LPIC-1 kann nach Plugin-Verzeichnissen und :packadd fragen."
        ),
        explanation  = (
            "VIM PLUGINS & PACKAGE MANAGEMENT:\n\n"
            "NATIVE PACKAGES (vim 8+ / neovim):\n"
            "  Verzeichnis: ~/.vim/pack/GRUPPE/start/PLUGIN/\n"
            "  Auto-Load:   ~/.vim/pack/*/start/   (beim Start geladen)\n"
            "  Manuell:     ~/.vim/pack/*/opt/      (:packadd PLUGIN)\n"
            "  :packadd PLUGIN   Plugin manuell laden\n\n"
            "VIM-PLUG (populärer Plugin-Manager):\n"
            "  Installation: curl -fLo ~/.vim/autoload/plug.vim ...\n"
            "  ~/.vimrc Konfiguration:\n"
            "    call plug#begin('~/.vim/plugged')\n"
            "    Plug 'tpope/vim-fugitive'\n"
            "    Plug 'preservim/nerdtree'\n"
            "    call plug#end()\n\n"
            "  BEFEHLE:\n"
            "  :PlugInstall    Plugins installieren\n"
            "  :PlugUpdate     Plugins aktualisieren\n"
            "  :PlugClean      nicht gelistete Plugins entfernen\n"
            "  :PlugStatus     Status aller Plugins\n\n"
            "PLUGIN-VERZEICHNISSE:\n"
            "  ~/.vim/           User-Konfiguration\n"
            "  ~/.vim/plugin/    Skripte (immer geladen)\n"
            "  ~/.vim/autoload/  Lazy-Load Skripte\n"
            "  ~/.vim/colors/    Farbschemata\n"
            "  ~/.vim/syntax/    Syntax-Dateien\n"
            "  /usr/share/vim/   System-Plugins"
        ),
        syntax       = ":packadd PLUGIN  |  :PlugInstall  |  ~/.vim/pack/*/start/",
        example      = (
            "\" In ~/.vimrc:\n"
            "call plug#begin('~/.vim/plugged')\n"
            "Plug 'tpope/vim-sensible'\n"
            "call plug#end()\n\n"
            "\" In vim:\n"
            ":PlugInstall       \" Plugins installieren\n"
            ":packadd matchit   \" nativen Plugin laden"
        ),
        task_description = "Erkläre den Unterschied zwischen vim-plug und nativen vim-Packages",
        expected_commands = [":packadd", ":PlugInstall"],
        hint_text    = "Native Packages: ~/.vim/pack/*/start/ (auto) oder :packadd (manuell)",
        quiz_questions = [
            QuizQuestion(
                question   = "In welchem Verzeichnis werden vim native Packages automatisch beim Start geladen?",
                options    = [
                    "~/.vim/plugin/",
                    "~/.vim/pack/*/opt/",
                    "~/.vim/pack/*/start/",
                    "~/.vim/autoload/",
                ],
                correct    = 2,
                explanation = (
                    "~/.vim/pack/*/start/ enthält Plugins die automatisch beim vim-Start geladen werden.\n"
                    "~/.vim/pack/*/opt/ enthält optionale Plugins die mit :packadd manuell geladen werden.\n"
                    "~/.vim/plugin/ ist das ältere Verzeichnis für immer geladene Skripte."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 vim Packages:\n"
            "  ~/.vim/pack/*/start/ = automatisch geladen\n"
            "  ~/.vim/pack/*/opt/   = manuell mit :packadd\n"
            "  :packadd PLUGIN      = optionales Plugin laden\n"
            "  vim-plug: :PlugInstall installiert Plugins"
        ),
        memory_tip   = "start = startet automatisch. opt = optional, muss mit :packadd angefordert werden.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.19 — grep -P (PCRE)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.19",
        chapter      = 8,
        title        = "grep -P — PCRE & Lookaheads",
        mtype        = "INFILTRATE",
        xp           = 95,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'BRE und ERE sind Anfänger-Kram, Ghost.\n"
            " PCRE — Perl-Compatible Regular Expressions — ist die Waffe\n"
            " der Experten. Lookahead, Lookbehind, Non-greedy.\n"
            " grep -P öffnet diese Welt.'"
        ),
        why_important = (
            "PCRE bietet mächtigere Regex-Funktionen als BRE/ERE.\n"
            "Lookahead/Lookbehind für kontextabhängige Matches.\n"
            "LPIC-1 testet den Unterschied zwischen grep -E und grep -P."
        ),
        explanation  = (
            "GREP -P — PERL-COMPATIBLE REGULAR EXPRESSIONS (PCRE):\n\n"
            "AKTIVIERUNG: grep -P 'PCRE-MUSTER' datei\n\n"
            "PCRE-ERWEITERUNGEN (nicht in ERE):\n"
            "  \\d      Ziffer [0-9]\n"
            "  \\D      Nicht-Ziffer\n"
            "  \\w      Wortzeichen [a-zA-Z0-9_]\n"
            "  \\W      Nicht-Wortzeichen\n"
            "  \\s      Whitespace\n"
            "  \\S      Nicht-Whitespace\n"
            "  \\b      Wortgrenze\n"
            "  \\B      Nicht-Wortgrenze\n\n"
            "LOOKAHEAD & LOOKBEHIND:\n"
            "  (?=MUSTER)   Positiver Lookahead: gefolgt von MUSTER\n"
            "  (?!MUSTER)   Negativer Lookahead: NICHT gefolgt von MUSTER\n"
            "  (?<=MUSTER)  Positiver Lookbehind: vorangehend MUSTER\n"
            "  (?<!MUSTER)  Negativer Lookbehind: NICHT vorangehend\n\n"
            "GREEDY vs. NON-GREEDY:\n"
            "  .*   greedy (so viel wie möglich)\n"
            "  .*?  non-greedy (so wenig wie möglich)\n"
            "  .+?  non-greedy, mindestens 1 Zeichen\n\n"
            "BEISPIELE:\n"
            "  grep -P '\\d{3}-\\d{4}' datei    Telefonnummer-Muster\n"
            "  grep -P '(?<=:)\\d+' /etc/passwd  UID nach Doppelpunkt\n"
            "  grep -P 'foo(?=bar)' datei        'foo' gefolgt von 'bar'\n"
            "  grep -oP '\\b\\w+@\\w+\\.\\w+\\b' datei  E-Mail-Adressen"
        ),
        syntax       = "grep -P 'PCRE-MUSTER' DATEI  |  grep -oP 'MUSTER' DATEI",
        example      = (
            "grep -P '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}' /var/log/auth.log\n"
            "grep -P '(?<=Failed password for )\\w+' /var/log/auth.log\n"
            "grep -P '^(?!#)\\S' /etc/ssh/sshd_config  # aktive Optionen\n"
            "grep -oP '\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}\\b' -i mails.txt"
        ),
        task_description = "Verwende grep -P um IP-Adressen aus einer Logdatei zu extrahieren",
        expected_commands = ["grep -P", "grep -oP"],
        hint_text    = "grep -oP '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}' extrahiert IP-Adressen",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt (?=MUSTER) in einem PCRE-Regex?",
                options    = [
                    "Lookbehind: MUSTER muss voranstehen",
                    "Lookahead: Position muss von MUSTER gefolgt sein",
                    "Negation: MUSTER darf nicht folgen",
                    "Gruppe: MUSTER wird als Gruppe gespeichert",
                ],
                correct    = 1,
                explanation = (
                    "(?=MUSTER) ist ein positiver Lookahead.\n"
                    "Er matcht eine Position, auf die MUSTER folgt, ohne MUSTER selbst zu verbrauchen.\n"
                    "(?<=MUSTER) ist Lookbehind (MUSTER muss voranstehen).\n"
                    "(?!MUSTER) ist negativer Lookahead."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 grep Varianten:\n"
            "  grep -E = ERE (Extended Regular Expressions)\n"
            "  grep -P = PCRE (Perl-Compatible, mächtiger)\n"
            "  grep -F = Feste Zeichenkette (kein Regex)\n"
            "  grep -G = BRE (Standard, default)\n"
            "  Lookahead (?=) und Lookbehind (?<=) nur in PCRE!"
        ),
        memory_tip   = "P in grep -P = Perl. PCRE = Perl-Compatible Regular Expressions.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.20 — sed Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.20",
        chapter      = 8,
        title        = "sed Advanced — In-Place, Adressen & Branching",
        mtype        = "DECODE",
        xp           = 100,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Einfaches sed kennst du, Ghost.\n"
            " Jetzt die Tiefe: -i für direkte Dateiänderung,\n"
            " Adressbereiche, mehrere Ausdrücke mit -e,\n"
            " und Branch-Befehle für Schleifen.'"
        ),
        why_important = (
            "Fortgeschrittenes sed ist essentiell für Systemadministration.\n"
            "-i (in-place) ist kritisch für Config-Management-Skripte.\n"
            "LPIC-1 103.7 testet Adressbereiche und mehrfache Ausdrücke."
        ),
        explanation  = (
            "SED ADVANCED:\n\n"
            "IN-PLACE BEARBEITUNG:\n"
            "  sed -i 's/alt/neu/g' datei       direkt ändern\n"
            "  sed -i.bak 's/alt/neu/g' datei   mit Backup (.bak)\n"
            "  sed -i'' 's/alt/neu/g' datei      kein Backup (GNU)\n\n"
            "MEHRFACHE AUSDRÜCKE:\n"
            "  sed -e 's/foo/bar/' -e 's/baz/qux/' datei\n"
            "  sed 's/foo/bar/; s/baz/qux/' datei\n\n"
            "ADRESSBEREICHE:\n"
            "  sed '5s/alt/neu/' datei          nur Zeile 5\n"
            "  sed '5,10s/alt/neu/g' datei      Zeilen 5 bis 10\n"
            "  sed '/START/,/STOP/s/x/y/g' d    zwischen Mustern\n"
            "  sed '0,/MUSTER/s/x/y/' datei     bis zum 1. Muster\n"
            "  sed '$s/alt/neu/' datei           letzte Zeile\n\n"
            "BEFEHLE:\n"
            "  a\\TEXT   Zeile nach Match anhängen\n"
            "  i\\TEXT   Zeile vor Match einfügen\n"
            "  c\\TEXT   Zeile ersetzen\n"
            "  r DATEI  Datei nach Match einfügen\n"
            "  w DATEI  Matches in Datei schreiben\n"
            "  q        Beenden nach Match\n\n"
            "BRANCHING (Schleifen):\n"
            "  :label   Label definieren\n"
            "  b label  unbedingter Sprung zu label\n"
            "  t label  Sprung wenn s/// erfolgreich\n"
            "  T label  Sprung wenn s/// NICHT erfolgreich\n\n"
            "HOLD SPACE:\n"
            "  h / H    Pattern Space in Hold Space kopieren/anhängen\n"
            "  g / G    Hold Space in Pattern Space kopieren/anhängen\n"
            "  x        Pattern und Hold Space tauschen"
        ),
        syntax       = "sed [-i[.bak]] [-e AUSDRUCK] 'ADRESSE BEFEHL' DATEI",
        example      = (
            "sed -i.bak '/^#/d; /^$/d' /etc/hosts      # Kommentare+Leerzeilen weg\n"
            "sed -e 's/http:/https:/' -e 's/80/443/' nginx.conf\n"
            "sed '/\\[DEFAULT\\]/,/\\[/s/debug=.*/debug=false/' app.conf\n"
            "sed -n '/ERROR/,/RESOLVED/p' logfile.txt  # Fehlerblöcke zeigen\n"
            "sed '1~2s/^/# /' datei                    # jede 2. Zeile kommentieren"
        ),
        task_description = "Verwende sed -i um Kommentare und Leerzeilen aus /etc/hosts zu entfernen",
        expected_commands = ["sed -i", "sed -i.bak"],
        hint_text    = "sed -i '/^#/d; /^$/d' datei — löscht Kommentar- und Leerzeilen direkt",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht 'sed -i.bak s/alt/neu/g datei'?",
                options    = [
                    "Erstellt nur ein Backup ohne Änderungen",
                    "Ändert die Datei in-place und erstellt datei.bak als Backup",
                    "Fehler: -i und .bak sind getrennte Optionen",
                    "Führt sed interaktiv aus",
                ],
                correct    = 1,
                explanation = (
                    "sed -i.bak ändert die Datei direkt (in-place) und erstellt\n"
                    "eine Backup-Kopie mit der Endung .bak.\n"
                    "sed -i ohne Suffix ändert in-place ohne Backup.\n"
                    "Das Suffix kann beliebig sein: -i.orig, -i.old etc."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 sed -i:\n"
            "  -i        in-place ohne Backup\n"
            "  -i.bak    in-place mit .bak Backup\n"
            "  -e        mehrere Ausdrücke\n"
            "  Adressbereich: '5,10s/x/y/'\n"
            "  Musterbereiche: '/START/,/STOP/Befehl'"
        ),
        memory_tip   = "i = in-place (direkt). Suffix nach -i = Backup-Endung. Kein Suffix = kein Backup.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.21 — awk Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.21",
        chapter      = 8,
        title        = "awk Advanced — Arrays, printf & getline",
        mtype        = "DECODE",
        xp           = 110,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'awk ist eine vollständige Programmiersprache, Ghost.\n"
            " Arrays, printf, getline — damit analysierst du\n"
            " Logs wie ein Maschinen-Gehirn.\n"
            " NR, NF, FS, RS — deine Werkzeuge.'"
        ),
        why_important = (
            "Fortgeschrittenes awk ist für komplexe Log-Analyse unverzichtbar.\n"
            "Arrays ermöglichen Aggregation und Statistiken.\n"
            "LPIC-1 testet Variablen NR/NF/FS/RS und printf."
        ),
        explanation  = (
            "AWK ADVANCED:\n\n"
            "ALLE WICHTIGEN VARIABLEN:\n"
            "  NR     aktuelle Zeilennummer (über alle Dateien)\n"
            "  FNR    Zeilennummer in der aktuellen Datei\n"
            "  NF     Anzahl Felder in der aktuellen Zeile\n"
            "  FS     Feld-Trennzeichen (default: Whitespace)\n"
            "  OFS    Output-Feld-Trennzeichen (default: Leerzeichen)\n"
            "  RS     Record-Trennzeichen (default: Newline)\n"
            "  ORS    Output-Record-Trennzeichen\n"
            "  FILENAME  Name der aktuellen Datei\n\n"
            "PRINTF FÜR FORMATIERTE AUSGABE:\n"
            "  awk '{printf \"%-10s %5d\\n\", $1, $2}' datei\n"
            "  %s = String, %d = Integer, %f = Float\n"
            "  %-10s = linksbündig 10 Zeichen\n"
            "  %05d  = mit führenden Nullen\n\n"
            "ARRAYS:\n"
            "  arr[key] = value     Array-Zuweisung\n"
            "  for (k in arr)       über Array iterieren\n"
            "  delete arr[key]      Element löschen\n"
            "  if (key in arr)      Key-Test\n\n"
            "GETLINE:\n"
            "  getline              nächste Zeile lesen\n"
            "  getline var          in Variable speichern\n"
            "  getline < \"datei\"    aus Datei lesen\n"
            "  cmd | getline var    aus Befehl lesen\n\n"
            "SPEZIALBLÖCKE:\n"
            "  BEGIN { FS=\":\"; OFS=\"|\" }   vor der Verarbeitung\n"
            "  END   { print totals }       nach der Verarbeitung\n\n"
            "MEHRERE MUSTER:\n"
            "  /error/ { err++ }; /warn/ { warn++ }; END { print err, warn }"
        ),
        syntax       = "awk 'BEGIN{} /MUSTER/{AKTION} END{}' DATEI",
        example      = (
            "# Häufigkeit von HTTP-Status-Codes zählen:\n"
            "awk '{codes[$9]++} END{for(c in codes) print c, codes[c]}' access.log\n\n"
            "# Formatierte Ausgabe der Passwort-Datei:\n"
            "awk -F: 'BEGIN{printf \"%-15s %5s\\n\",\"User\",\"UID\"} {printf \"%-15s %5d\\n\",$1,$3}' /etc/passwd\n\n"
            "# Summe einer Spalte:\n"
            "awk '{sum += $5} END {print \"Total:\", sum}' report.txt"
        ),
        task_description = "Verwende awk um die häufigsten Wörter in einer Textdatei zu zählen",
        expected_commands = ["awk '{", "awk -F"],
        hint_text    = "awk '{words[$1]++} END{for(w in words) print words[w], w}' datei | sort -rn",
        quiz_questions = [
            QuizQuestion(
                question   = "Was enthält die awk-Variable FNR?",
                options    = [
                    "Die Gesamtzahl aller Zeilen über alle Dateien",
                    "Die Zeilennummer in der aktuellen Datei",
                    "Die Anzahl der Felder in der aktuellen Zeile",
                    "Den Namen der aktuellen Datei",
                ],
                correct    = 1,
                explanation = (
                    "FNR = File Number of Record = Zeilennummer in der AKTUELLEN Datei.\n"
                    "NR = Number of Record = globale Zeilennummer über alle Dateien.\n"
                    "Bei einer einzelnen Datei sind FNR und NR gleich.\n"
                    "NF = Number of Fields, FILENAME = Dateiname."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 awk Variablen:\n"
            "  NR = globale Zeilennummer\n"
            "  FNR = Zeilennummer in aktueller Datei\n"
            "  NF = Anzahl Felder\n"
            "  FS = Feld-Trennzeichen (-F oder BEGIN{FS=})\n"
            "  OFS = Output-Feld-Trennzeichen\n"
            "  RS = Record-Separator (default: Newline)"
        ),
        memory_tip   = "FNR = File Number of Record. NR = Number of Record (global). F = File = lokal.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.22 — Regex in Python/Shell
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.22",
        chapter      = 8,
        title        = "Regex in Shell & Python — [[ =~ ]] & BASH_REMATCH",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "NEXUS",
        story        = (
            "NEXUS: 'Regex lebt nicht nur in grep, Ghost.\n"
            " Bash hat [[ =~ ]] für Pattern-Matching in Skripten.\n"
            " BASH_REMATCH speichert Gruppen.\n"
            " Python re-Modul für mächtige Verarbeitung.'"
        ),
        why_important = (
            "Regex in Bash-Skripten mit [[ =~ ]] ist LPIC-1 Prüfungsstoff.\n"
            "BASH_REMATCH-Array für Capture Groups in Shell-Skripten.\n"
            "Unterschied grep -E vs -P wichtig für Prüfung."
        ),
        explanation  = (
            "REGEX IN BASH:\n\n"
            "PATTERN MATCHING IN BASH:\n"
            "  [[ STRING =~ REGEX ]]   Regex-Test in Bash\n"
            "  [[ STRING == GLOB ]]    Glob-Pattern (kein Regex!)\n\n"
            "BASH_REMATCH ARRAY:\n"
            "  ${BASH_REMATCH[0]}   gesamter Match\n"
            "  ${BASH_REMATCH[1]}   erste Capture-Gruppe (...)\n"
            "  ${BASH_REMATCH[2]}   zweite Capture-Gruppe\n\n"
            "BEISPIEL:\n"
            "  if [[ \"user@host.de\" =~ ^([^@]+)@(.+)$ ]]; then\n"
            "    echo \"User: ${BASH_REMATCH[1]}\"\n"
            "    echo \"Host: ${BASH_REMATCH[2]}\"\n"
            "  fi\n\n"
            "GREP VARIANTEN IM VERGLEICH:\n"
            "  grep -G  BRE (Basic)  — default\n"
            "  grep -E  ERE (Extended) — +, ?, |, () ohne Backslash\n"
            "  grep -P  PCRE — Lookahead, \\d, \\w, non-greedy\n"
            "  grep -F  Fixed String — kein Regex\n\n"
            "PYTHON RE-MODUL (Referenz):\n"
            "  import re\n"
            "  re.search(r'MUSTER', string)    ersten Match suchen\n"
            "  re.match(r'MUSTER', string)     nur am Anfang\n"
            "  re.findall(r'MUSTER', string)   alle Matches\n"
            "  re.sub(r'MUSTER', 'neu', string) ersetzen\n"
            "  re.compile(r'MUSTER')           vorkompilieren\n\n"
            "REGEX TESTEN:\n"
            "  echo 'test' | grep -P 'MUSTER'   schnell testen\n"
            "  python3 -c \"import re; print(re.search(r'x', 'text'))\""
        ),
        syntax       = "[[ STRING =~ REGEX ]]  |  BASH_REMATCH[N]  |  grep -E/-P/-G/-F",
        example      = (
            "# IP-Adresse validieren:\n"
            "ip='192.168.1.100'\n"
            "if [[ $ip =~ ^([0-9]{1,3}\\.){3}[0-9]{1,3}$ ]]; then\n"
            "  echo \"Gültige IP: $ip\"\n"
            "fi\n\n"
            "# Mit Gruppen:\n"
            "if [[ 'user:1000:1000' =~ ^([^:]+):([0-9]+) ]]; then\n"
            "  echo \"Name: ${BASH_REMATCH[1]}, UID: ${BASH_REMATCH[2]}\"\n"
            "fi"
        ),
        task_description = "Schreibe ein Bash-Skript das mit [[ =~ ]] eine E-Mail-Adresse validiert",
        expected_commands = ["[[", "=~", "BASH_REMATCH"],
        hint_text    = "[[ '$email' =~ ^[^@]+@[^@]+\\.[^@]+$ ]] prüft E-Mail-Format",
        quiz_questions = [
            QuizQuestion(
                question   = "Welches Array speichert Regex-Capture-Gruppen in Bash nach [[ =~ ]]?",
                options    = [
                    "BASH_MATCHES",
                    "REGEX_GROUPS",
                    "BASH_REMATCH",
                    "MATCH_ARRAY",
                ],
                correct    = 2,
                explanation = (
                    "BASH_REMATCH ist das spezielle Bash-Array für Regex-Captures.\n"
                    "${BASH_REMATCH[0]} = gesamter Match.\n"
                    "${BASH_REMATCH[1]} = erste Gruppe (...), ${BASH_REMATCH[2]} = zweite usw.\n"
                    "Es wird nach jedem erfolgreichen [[ STRING =~ REGEX ]] gesetzt."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Bash Regex:\n"
            "  [[ STR =~ REGEX ]] = Regex-Test in Bash\n"
            "  BASH_REMATCH[0]    = gesamter Match\n"
            "  BASH_REMATCH[1..N] = Capture-Gruppen\n"
            "  [[ STR == GLOB ]]  = Glob (kein Regex!)\n"
            "  Regex in [[ ]] darf NICHT gequotet werden!"
        ),
        memory_tip   = "REMATCH = RE-Match. [0] = alles, [1],[2]... = Gruppen. Regex NIE quoten in [[]].",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.23 — Multiline Regex & Praxis
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.23",
        chapter      = 8,
        title        = "Multiline Regex — pcregrep, grep -z & sed N",
        mtype        = "INFILTRATE",
        xp           = 100,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Manche Angriffsmuster überspannen mehrere Zeilen, Ghost.\n"
            " Standard-Regex sieht nur eine Zeile.\n"
            " pcregrep -M, grep -z, sed N — das sind die Werkzeuge\n"
            " für mehrzeilige Matches.'"
        ),
        why_important = (
            "Mehrzeilige Patterns kommen in Config-Dateien und Logs vor.\n"
            "pcregrep -M für Perl-Multiline, grep -z für Null-Byte-getrennte Zeilen.\n"
            "LPIC-1 kann nach sed N und mehrzeiliger Verarbeitung fragen."
        ),
        explanation  = (
            "MULTILINE REGEX:\n\n"
            "DAS PROBLEM:\n"
            "  Normales grep verarbeitet Zeile für Zeile.\n"
            "  Muster die mehrere Zeilen überspannen brauchen\n"
            "  spezielle Tools oder Optionen.\n\n"
            "PCREGREP -M (Multiline):\n"
            "  pcregrep -M 'ZEILE1\\nZEILE2' datei\n"
            "  pcregrep -M 'BEGIN.*?END' datei       # Non-greedy\n"
            "  pcregrep -M '^start$[\\s\\S]*?^end$' d # Blöcke finden\n"
            "  Paket: apt install pcregrep\n\n"
            "GREP -Z / -Z0:\n"
            "  grep -z 'MUSTER' datei    Zeilen mit \\0 getrennt (Null-Byte)\n"
            "  grep -z behandelt die ganze Datei als einen Stream\n"
            "  Nützlich mit find -print0 | xargs -0\n\n"
            "SED MULTILINE:\n"
            "  sed 'N; s/\\n/ /' datei    zwei Zeilen zusammenführen\n"
            "  sed ':a; N; $!ba; s/\\n/ /g' datei   alle Zeilen zusammen\n"
            "  N = nächste Zeile an Pattern Space anhängen\n"
            "  P = erste Zeile des Pattern Space ausgeben\n"
            "  D = erste Zeile löschen und neu starten\n\n"
            "AWK MULTILINE:\n"
            "  awk 'RS=\"\"' datei           Absätze als Records\n"
            "  awk 'BEGIN{RS=\"\\n\\n\"}' d  Leerzeile als Trennzeichen\n"
            "  awk '/START/,/END/' datei   Bereich über Zeilen\n\n"
            "PRAKTISCHE PATTERNS:\n"
            "  Config-Blöcke: pcregrep -M '\\[section\\][\\s\\S]*?\\['\n"
            "  Log-Fehlerblöcke: awk '/ERROR/,/^$/' logfile\n"
            "  XML-Tags: pcregrep -M '<tag>[\\s\\S]*?</tag>'"
        ),
        syntax       = "pcregrep -M 'PATTERN' DATEI  |  sed 'N; ...'  |  awk 'RS=\"\"'",
        example      = (
            "# Zwei aufeinander folgende Zeilen zusammenführen:\n"
            "sed 'N; s/\\n/ /' /etc/hosts\n\n"
            "# Blöcke zwischen BEGIN und END finden:\n"
            "awk '/BEGIN/{found=1} found{print} /END/{found=0}' datei\n\n"
            "# Absatzweise verarbeiten (Leerzeile als Trenner):\n"
            "awk 'BEGIN{RS=\"\"} /wichtig/' dokument.txt\n\n"
            "# pcregrep für mehrzeiligen Match:\n"
            "pcregrep -M 'Host: example\\.com\\r?\\nUser-Agent:' access.log"
        ),
        task_description = "Verwende sed N oder awk RS um mehrzeilige Blöcke zu verarbeiten",
        expected_commands = ["sed 'N", "awk 'BEGIN{RS", "pcregrep -M"],
        hint_text    = "sed 'N; s/\\n/ /' fügt zwei aufeinanderfolgende Zeilen zusammen",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht der sed-Befehl 'N'?",
                options    = [
                    "Gibt die nächste Zeile aus",
                    "Löscht die aktuelle Zeile",
                    "Hängt die nächste Zeile an den Pattern Space an",
                    "Wechselt in den Nicht-gierigen Modus",
                ],
                correct    = 2,
                explanation = (
                    "sed 'N' liest die nächste Zeile und hängt sie (mit \\n) an den Pattern Space.\n"
                    "So können Substitutionen über Zeilengrenzen hinweg arbeiten.\n"
                    "sed 'N; s/\\n/ /' fügt zwei Zeilen mit Leerzeichen zusammen.\n"
                    "P = erste Zeile ausgeben, D = erste Zeile löschen."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Multiline:\n"
            "  sed N = nächste Zeile an Pattern Space\n"
            "  awk RS=\"\" = Absätze als Records\n"
            "  pcregrep -M = Perl Multiline\n"
            "  grep -z = Null-Byte statt Newline als Trenner\n"
            "  awk /START/,/END/ = Bereichs-Match"
        ),
        memory_tip   = "N in sed = Next line anhängen. awk RS='' = Record Separator leer = Absätze.",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.24 — Regex QUIZ (renumbered from 8.16)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.24",
        chapter      = 8,
        title        = "QUIZ — Regex & vi Wissenstest",
        mtype        = "QUIZ",
        xp           = 150,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Zeit, Ghost. Vor dem Endkampf\n"
            " teste ich dein Regex- und vi-Wissen.\n"
            " LPIC-1 Topic 103.7 und 103.8 — no mercy.'"
        ),
        why_important = "Quiz-Wiederholung für LPIC-1 Prüfung Topic 103.7/103.8",
        explanation   = "Beantworte die Fragen zu Regex und vi.",
        syntax        = "",
        example       = "",
        task_description = "Quiz: Regex & vi",
        expected_commands = [],
        hint_text     = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht grep -E?",
                options    = [
                    "A) Erweiterte Ausgabe (mehr Details)",
                    "B) Extended Regular Expressions (ERE) aktivieren",
                    "C) Alle Dateien rekursiv durchsuchen",
                    "D) grep beenden",
                ],
                correct    = "B",
                explanation = (
                    "grep -E aktiviert Extended Regular Expressions.\n"
                    "Damit sind + ? | ( ) { } ohne Backslash nutzbar.\n"
                    "egrep ist identisch mit grep -E."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welcher vi-Befehl beendet OHNE Speichern?",
                options    = [
                    "A) :wq",
                    "B) :x",
                    "C) :q!",
                    "D) ZZ",
                ],
                correct    = "C",
                explanation = (
                    ":q! beendet vi force-quit ohne Speichern.\n"
                    ":wq und ZZ speichern und beenden.\n"
                    ":x speichert nur wenn Änderungen vorhanden."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Was macht :%s/foo/bar/g in vi?",
                options    = [
                    "A) Ersetzt 'foo' durch 'bar' in der aktuellen Zeile",
                    "B) Ersetzt 'foo' durch 'bar' global (erste Zeile)",
                    "C) Ersetzt alle Vorkommen von 'foo' durch 'bar' in der gesamten Datei",
                    "D) Sucht 'foo' ohne zu ersetzen",
                ],
                correct    = "C",
                explanation = (
                    "% = gesamte Datei, s = substitute, g = global (alle Vorkommen).\n"
                    ":s/foo/bar/g würde nur die aktuelle Zeile betreffen.\n"
                    ":%s/foo/bar/gc fragt zusätzlich bei jedem Vorkommen nach."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welches Regex matcht nur Zeilen die mit einer Ziffer enden?",
                options    = [
                    "A) grep '^[0-9]'",
                    "B) grep '[0-9]$'",
                    "C) grep '[0-9]*'",
                    "D) grep '$[0-9]'",
                ],
                correct    = "B",
                explanation = (
                    "$ verankert das Muster am Zeilenende.\n"
                    "[0-9]$ = Ziffer am Zeilenende.\n"
                    "^[0-9] wäre Ziffer am Zeilenanfang."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Was macht der vi-Befehl 'dd'?",
                options    = [
                    "A) Datei löschen",
                    "B) Aktuelles Zeichen löschen",
                    "C) Aktuelle Zeile in den Puffer löschen",
                    "D) Alle Zeilen duplizieren",
                ],
                correct    = "C",
                explanation = (
                    "dd löscht die aktuelle Zeile in den Puffer (wie Ausschneiden).\n"
                    "Mit p kann die Zeile danach wieder eingefügt werden.\n"
                    "x löscht nur das Zeichen unter dem Cursor."
                ),
                xp_value   = 30,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Prüfungsschwerpunkte 103.7/103.8:\n"
            "  - grep -E vs grep (BRE vs ERE)\n"
            "  - vi-Modi: Normal, Insert, Command\n"
            "  - :wq :q! :%s/x/y/g — die drei Must-Knows\n"
            "  - POSIX-Klassen: [[:digit:]] [[:alpha:]]"
        ),
        memory_tip   = "",
        gear_reward  = None,
        faction_reward = ("Net Runners", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 8.BOSS — REGEX DAEMON v8.0
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "8.boss",
        chapter      = 8,
        title        = "BOSS — REGEX DAEMON v8.0",
        mtype        = "BOSS",
        xp           = 250,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM ALERT: REGEX DAEMON v8.0 aktiviert.\n"
            "Ein KI-Wächter der auf Pattern-Matching spezialisiert ist.\n"
            "Er liest jeden Befehl. Analysiert jedes Muster.\n"
            "Zara Z3R0: 'Er kennt BRE, ERE und vi besser als sein Schöpfer.\n"
            " Zeig ihm, dass du es auch kannst, Ghost.'"
        ),
        why_important = "Abschluss-Boss für Topic 103.7 + 103.8",
        explanation  = (
            "BOSS-CHALLENGE: Regex & vi Gauntlet\n\n"
            "Deine Aufgaben:\n"
            "1) grep -E um IPs in Logs zu finden\n"
            "2) sed globales Ersetzen in Konfiguration\n"
            "3) awk Feldextraktion aus /etc/passwd\n"
            "4) vi Suchen+Ersetzen mit :%s\n\n"
            "KOMMANDOS ZUM ÜBEN:\n"
            "  grep -E '[0-9]{1,3}(\\.[0-9]{1,3}){3}' /var/log/syslog\n"
            "  sed 's/old_host/new_host/g' /etc/hosts\n"
            "  awk -F: '{print $1, $3}' /etc/passwd\n"
            "  vi /etc/hosts → :%s/localhost/127.0.0.1/g"
        ),
        syntax       = "",
        example      = (
            "grep -E '^[0-9]+\\.' /var/log/syslog\n"
            "sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config\n"
            "awk -F: '$3 >= 1000 {print $1}' /etc/passwd\n"
            "# In vi: :%s/http:/https:/g"
        ),
        ascii_art   = """
  ██████╗ ███████╗ ██████╗ ███████╗██╗  ██╗    ██████╗  █████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝ ██╔════╝╚██╗██╔╝    ██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║  ███╗█████╗   ╚███╔╝     ██║  ██║███████║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║   ██║██╔══╝   ██╔██╗     ██║  ██║██╔══██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╔╝███████╗██╔╝ ██╗    ██████╔╝██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

  ┌─ PATTERN MATCH ENGINE ────────────────────────────────────────────┐
  │  grep -E '[0-9]+\\..*'  :: SCANNING...   ████████░░ 80%          │
  │  sed 's/BOSS/GHOST/g'  :: REPLACING...  ██████████ ARMED         │
  │  awk '{print $3}'       :: EXTRACTING... FIELD: LOCKED           │
  └───────────────────────────────────────────────────────────────────┘

                    ⚡ CHAOSWERK FACTION :: CHAPTER 8 BOSS ⚡""",
        story_transitions = [
            "REGEX DAEMON formt Muster aus Rauschen. Dein grep kämpft dagegen.",
            ". * + ? — er schreibt Patterns die alles matchen. Du verfeinerst.",
            "sed ersetzt seine Backdoor-Strings. awk extrahiert die Wahrheit.",
            "Letztes Muster. Ein Regex der alles auflöst. Schreib ihn.",
        ],
        task_description = "BOSS: Zeige UIDs >= 1000 aus /etc/passwd mit awk",
        expected_commands = ["awk -F: '$3 >= 1000 {print $1}' /etc/passwd"],
        hint_text    = "awk -F: setzt Trennzeichen, $3 ist die UID-Spalte, >= 1000 = normale User",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'grep -E'?",
                options     = ['A) Erweiterte Ausgabe', 'B) Aktiviert Extended Regular Expressions', 'C) Ergebnis in Datei', 'D) Rekursive Suche'],
                correct     = 'B',
                explanation = 'grep -E = Extended Regex. Ermöglicht + ? | ohne Backslash.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "LPIC-1 FINAL CHECK:\n"
            "  grep -E | egrep — Extended Regex\n"
            "  sed 's/x/y/g' — global ersetzen\n"
            "  sed -i — In-Place ohne Backup\n"
            "  awk -F: '$N {print $M}' — Felder filtern\n"
            "  vi :%s/x/y/g — ganzes Dokument\n"
            "  vi :q! — beenden ohne speichern"
        ),
        memory_tip   = "Merkhilfe: BOSS = Best Of Shell Skills",
        gear_reward  = "regex_scope",
        faction_reward = ("Net Runners", 30),
    ),
]
