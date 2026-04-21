"""
NeonGrid-9 :: Kapitel 6 — DATA STREAMS
LPIC-1 Topic 103.1 / 103.2 / 103.3 / 103.4
Shell-Umgebung, Textfilter, Pipes & Redirects

"Daten fließen wie Strom durch NeonGrid-9.
 Wer die Streams kontrolliert, kontrolliert alles."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_6_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 6.01 — Shell-Grundlagen: Variablen & Umgebung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.01",
        chapter      = 6,
        title        = "Shell-Umgebung — Variablen & PATH",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "ZARA Z3R0",
        story        = (
            "Die Shell ist dein Terminal zu NeonGrid-9.\n"
            "Ohne sie bist du blind.\n"
            "Zara Z3R0: 'Kenn deine Umgebung, Ghost.\n"
            " Variablen, PATH, env — das Fundament.'"
        ),
        why_important = (
            "Shell-Variablen und Umgebungsvariablen sind Basis jedes Linux-Admins.\n"
            "LPIC-1 prüft: lokale vs. Umgebungsvariablen, PATH, export, env."
        ),
        explanation  = (
            "Shell-Variablen:\n\n"
            "Setzen (lokal, nur aktuelle Shell):\n"
            "  NAME='Ghost'\n"
            "  PORT=8080\n\n"
            "Exportieren (Umgebungsvariable, vererbt an Kind-Prozesse):\n"
            "  export NAME='Ghost'\n"
            "  export PORT=8080\n"
            "  NAME='Ghost'; export NAME    # zwei Schritte\n\n"
            "Zugriff:\n"
            "  echo $NAME\n"
            "  echo ${NAME}     # sicherer mit geschweiften Klammern\n"
            "  echo \"Hallo $NAME!\"\n\n"
            "Wichtige Umgebungsvariablen:\n"
            "  $PATH    — Suchpfad für Befehle\n"
            "  $HOME    — Heimverzeichnis (/home/ghost)\n"
            "  $USER    — Benutzername\n"
            "  $SHELL   — aktuelle Shell (/bin/bash)\n"
            "  $PWD     — aktuelles Verzeichnis\n"
            "  $OLDPWD  — vorheriges Verzeichnis\n"
            "  $?       — Exit-Code des letzten Befehls\n"
            "  $!       — PID des letzten Hintergrundprozesses\n"
            "  $$       — PID der aktuellen Shell\n\n"
            "Umgebung anzeigen:\n"
            "  env          # alle Umgebungsvariablen\n"
            "  printenv     # wie env\n"
            "  printenv PATH\n"
            "  set          # alle Shell-Variablen\n\n"
            "PATH erweitern:\n"
            "  export PATH=$PATH:/usr/local/neongrid/bin\n\n"
            "Variable löschen:\n"
            "  unset NAME"
        ),
        syntax       = "export VARNAME=wert\necho $VARNAME\nenv | grep PATH",
        example      = (
            "$ export MISSION='active'\n"
            "$ echo $MISSION\nactive\n"
            "$ printenv PATH\n"
            "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ),
        task_description  = "Zeige alle Umgebungsvariablen",
        expected_commands = ["env", "printenv"],
        hint_text         = "env zeigt alle Umgebungsvariablen",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'VAR=wert' und 'export VAR=wert'?",
                options     = ['A) Kein Unterschied', 'B) export macht die Variable für Kind-Prozesse verfügbar', 'C) VAR=wert ist sicherer', 'D) export ist permanenter'],
                correct     = 'B',
                explanation = 'export = Umgebungsvariable (an Kinder vererbt). VAR=wert = lokal in aktueller Shell.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was enthält $?',
                options     = ['A) Den Dateinamen des aktuellen Skripts', 'B) Den Exit-Code des letzten Befehls', 'C) Die Prozess-ID der Shell', 'D) Den aktuellen Pfad'],
                correct     = 'B',
                explanation = '$? = Exit-Code. 0 = Erfolg, 1-255 = Fehler. Wichtig nach jedem Befehl prüfen!',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "Lokale Variable: NAME=wert — nur in aktueller Shell.\n"
            "Umgebungsvariable: export NAME=wert — vererbt an Kinder.\n"
            "$? = Exit-Code: 0 = Erfolg, 1-255 = Fehler.\n"
            "PATH = durch : getrennte Verzeichnisse, in Reihenfolge durchsucht."
        ),
        memory_tip       = "export = exportieren = Kinder erben die Variable. $?=Exit-Code. 0=OK.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.02 — Command History & Shortcuts
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.02",
        chapter      = 6,
        title        = "History & Shortcuts — Schneller hacken",
        mtype        = "SCAN",
        xp           = 55,
        speaker      = "RUST",
        story        = (
            "Im Kampf zählt Geschwindigkeit.\n"
            "Rust zeigt Ghost seine schmutzigen Tricks:\n"
            "'history, !!, Ctrl+R — du gibst nie denselben Befehl zweimal ein.'"
        ),
        why_important = (
            "Bash History und Shortcuts sparen Zeit und werden im Examen verlangt.\n"
            "LPIC-1: history, !!, !n, Ctrl+R, HISTSIZE, HISTFILE."
        ),
        explanation  = (
            "Bash History:\n\n"
            "  history        # alle gespeicherten Befehle\n"
            "  history 20     # letzte 20 Befehle\n"
            "  history -c     # History löschen\n\n"
            "History-Expansion:\n"
            "  !!           — letzten Befehl wiederholen\n"
            "  !42          — Befehl Nr. 42 ausführen\n"
            "  !ls          — letzten Befehl der mit 'ls' beginnt\n"
            "  !$           — letztes Argument des vorherigen Befehls\n"
            "  !*           — alle Argumente des vorherigen Befehls\n"
            "  sudo !!      — letzten Befehl als root\n\n"
            "Interaktive Suche:\n"
            "  Ctrl+R       — rückwärts in History suchen\n"
            "  Ctrl+G       — Suche abbrechen\n\n"
            "History-Variablen:\n"
            "  HISTSIZE=1000          — Anzahl in RAM\n"
            "  HISTFILESIZE=2000      — Anzahl in Datei\n"
            "  HISTFILE=~/.bash_history\n"
            "  HISTCONTROL=ignoredups # keine Duplikate\n\n"
            "Tastenkürzel:\n"
            "  Ctrl+A   — Anfang der Zeile\n"
            "  Ctrl+E   — Ende der Zeile\n"
            "  Ctrl+U   — Zeile löschen\n"
            "  Ctrl+L   — Screen leeren (wie clear)\n"
            "  Tab      — Autovervollständigung\n"
            "  Tab Tab  — alle Möglichkeiten zeigen"
        ),
        syntax       = "history\n!!\nsudo !!\nCtrl+R",
        example      = (
            "$ history 5\n"
            "  96  ls -la /etc\n"
            "  97  cat /etc/passwd\n"
            "  98  grep root /etc/passwd\n"
            "  99  sudo systemctl restart ssh\n"
            " 100  history 5\n\n"
            "$ !!    # führt 'history 5' erneut aus\n"
            "$ !99   # führt 'sudo systemctl restart ssh' aus"
        ),
        task_description  = "Zeige die letzten 10 Befehle",
        expected_commands = ["history", "history 10"],
        hint_text         = "history oder history 10 zeigt die letzten Befehle",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht '!!' in der Bash?",
                options     = ['A) Führt letzten Befehl als Root aus', 'B) Wiederholt den letzten Befehl', 'C) Zeigt Befehlshistorie', 'D) Löscht History'],
                correct     = 'B',
                explanation = "!! = letzten Befehl wiederholen. 'sudo !!' = letzten Befehl als root — sehr praktisch!",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was ist HISTSIZE?',
                options     = ['A) Maximale Größe von ~/.bash_history auf Disk', 'B) Anzahl der History-Einträge im RAM', 'C) Maximale Befehlslänge', 'D) Anzahl der History-Dateien'],
                correct     = 'B',
                explanation = 'HISTSIZE = Einträge im RAM (aktuelle Session). HISTFILESIZE = Einträge in ~/.bash_history.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "!! = letzten Befehl wiederholen.\n"
            "sudo !! = letzten Befehl als root — sehr nützlich!\n"
            "HISTSIZE = Einträge im RAM. HISTFILESIZE = Einträge in ~/.bash_history."
        ),
        memory_tip       = "!! = letzt. !n = Nr n. sudo !! = letzt als root. Ctrl+R = suchen.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 2),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.03 — I/O Redirection: > >> < 2>
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.03",
        chapter      = 6,
        title        = "I/O Redirection — Streams umleiten",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "ZARA Z3R0",
        story        = (
            "Daten fließen durch drei Kanäle: stdin, stdout, stderr.\n"
            "Zara Z3R0: 'Leite sie um, Ghost. Speichere Ausgaben.\n"
            " Unterdrücke Fehler. Steuere den Fluss.'"
        ),
        why_important = (
            "Redirection ist Grundlage jedes Shell-Skripts und jeder Admin-Arbeit.\n"
            "LPIC-1 prüft alle Redirect-Operatoren und ihre Bedeutung."
        ),
        explanation  = (
            "Standard-Streams:\n"
            "  stdin  (0) — Tastatur-Eingabe\n"
            "  stdout (1) — normale Ausgabe\n"
            "  stderr (2) — Fehler-Ausgabe\n\n"
            "Output-Redirection:\n"
            "  befehl > datei       # stdout → Datei (überschreibt)\n"
            "  befehl >> datei      # stdout → Datei (anhängen)\n"
            "  befehl 2> fehler.log # stderr → Datei\n"
            "  befehl 2>> fehler.log# stderr anhängen\n"
            "  befehl &> alles.log  # stdout + stderr → Datei\n"
            "  befehl > /dev/null   # stdout verwerfen\n"
            "  befehl 2>/dev/null   # stderr verwerfen\n"
            "  befehl > out 2>&1    # stderr zu stdout (klassisch)\n"
            "  befehl &>/dev/null   # alles verwerfen\n\n"
            "Input-Redirection:\n"
            "  befehl < datei       # stdin aus Datei\n"
            "  befehl << EOF        # Here Document\n"
            "  cat << EOF\n"
            "  Zeile 1\n"
            "  EOF\n\n"
            "Kombiniert:\n"
            "  sort < unsortiert.txt > sortiert.txt\n"
            "  find / -name '*.log' 2>/dev/null > logs.txt\n\n"
            "/dev/null — das schwarze Loch:\n"
            "  Alles was hierhin geschrieben wird, verschwindet.\n"
            "  command 2>/dev/null  # Fehler unterdrücken"
        ),
        syntax       = "cmd > out.txt\ncmd >> out.txt\ncmd 2>/dev/null\ncmd > out.txt 2>&1",
        example      = (
            "$ ls /etc > /tmp/etc_list.txt        # stdout in Datei\n"
            "$ ls /nope 2>/dev/null               # Fehler unterdrücken\n"
            "$ find / -name '*.conf' > out 2>&1   # alles in out\n"
            "$ cat >> /etc/hosts << EOF\n"
            "192.168.1.100 neongrid9-node\n"
            "EOF"
        ),
        task_description  = "Zeige wie Befehle Daten ausgeben",
        expected_commands = ["ls", "cat"],
        hint_text         = "ls /etc > /tmp/out.txt leitet Ausgabe in eine Datei",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'cmd > datei 2>&1'?",
                options     = [
                    "A) stdout → datei, stderr bleibt auf Terminal",
                    "B) stdout + stderr → datei",
                    "C) stderr → datei, stdout bleibt auf Terminal",
                    "D) Fehler — ungültige Syntax",
                ],
                correct     = "B",
                explanation = "2>&1 = stderr (2) zum selben Ziel wie stdout (1). stdout ist bereits → datei. Ergebnis: beides in datei.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Was ist /dev/null?",
                options     = [
                    "A) Eine leere Datei die nie voll wird",
                    "B) Ein virtuelles Gerät das alle Daten verwirft",
                    "C) Der Null-Pointer des Kernels",
                    "D) Ein temporäres Verzeichnis",
                ],
                correct     = "B",
                explanation = "/dev/null ist das 'schwarze Loch' — alles was dorthin geschrieben wird, ist weg. Lesen ergibt EOF sofort.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "Reihenfolge wichtig: cmd > out 2>&1\n"
            "NICHT: cmd 2>&1 > out  (stderr geht dann auf Terminal!)\n"
            ">> = anhängen, > = überschreiben.\n"
            "2>/dev/null = Fehlermeldungen unterdrücken (sauberere Ausgabe)."
        ),
        memory_tip       = "> überschreibt. >> hängt an. 2> für Fehler. 2>&1 = stderr zu stdout.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.04 — Pipes & tee
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.04",
        chapter      = 6,
        title        = "Pipes & tee — Daten-Pipelines bauen",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "Die mächtigste Waffe der Shell ist die Pipe.\n"
            "Rust grinst: 'stdout von einem Befehl → stdin des nächsten.\n"
            " Ketten bauen, Ghost. Das ist Unix-Philosophie.'"
        ),
        why_important = (
            "Pipes sind der Kern der Unix-Philosophie: kleine Tools kombinieren.\n"
            "LPIC-1 prüft Pipe-Syntax und tee für gleichzeitige Ausgabe."
        ),
        explanation  = (
            "Pipe — stdout → stdin weiterleiten:\n\n"
            "  befehl1 | befehl2\n"
            "  befehl1 | befehl2 | befehl3\n\n"
            "Beispiele:\n"
            "  ls -l | grep '.conf'\n"
            "  cat /etc/passwd | sort\n"
            "  ps aux | grep ssh\n"
            "  dmesg | grep -i error | tail -20\n"
            "  cat /var/log/syslog | grep 'Jan 15' | wc -l\n\n"
            "tee — gleichzeitig in Datei UND auf stdout:\n\n"
            "  befehl | tee datei\n"
            "  befehl | tee -a datei   # append\n\n"
            "  ls -la | tee /tmp/listing.txt\n"
            "  # → Ausgabe auf Terminal UND in Datei\n\n"
            "  install.sh 2>&1 | tee install.log\n"
            "  # → stdout+stderr auf Terminal UND in install.log\n\n"
            "Named Pipes (FIFO):\n"
            "  mkfifo /tmp/mypipe\n"
            "  ls -Type = 'p' (pipe)\n\n"
            "xargs — stdin als Argumente übergeben:\n"
            "  find /tmp -name '*.tmp' | xargs rm\n"
            "  cat list.txt | xargs ls -la\n"
            "  find . -name '*.log' | xargs -I{} cp {} /backup/"
        ),
        syntax       = "cmd1 | cmd2 | cmd3\ncmd | tee datei",
        example      = (
            "$ ps aux | grep -v grep | grep sshd | wc -l\n3\n\n"
            "$ dmesg | grep -i error | tee /tmp/errors.log\n"
            "[  0.299456] ACPI Error: ...\n"
            "[  3.456789] EXT4-fs error: ...\n"
            "(gleichzeitig in /tmp/errors.log gespeichert)"
        ),
        task_description  = "Zeige laufende Prozesse mit ps gefiltert durch grep",
        expected_commands = ["ps aux", "ps"],
        hint_text         = "ps aux | grep ssh kombiniert ps und grep per Pipe",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'tee' in einer Pipeline?",
                options     = ['A) Leitet stdout in /dev/null', 'B) Schreibt auf stdout UND in eine Datei gleichzeitig', 'C) Dupliziert stderr', 'D) Verbindet zwei Pipes'],
                correct     = 'B',
                explanation = 'tee = T-Stück: Ausgabe geht sowohl auf Terminal als auch in Datei. tee -a = append.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was passiert bei 'cmd1 | cmd2'?",
                options     = ['A) cmd2 liest aus einer Datei', 'B) stdout von cmd1 wird stdin von cmd2', 'C) Beide Befehle laufen nacheinander', 'D) Fehler bei Leerzeichen'],
                correct     = 'B',
                explanation = 'Pipe | verbindet stdout des ersten Befehls mit stdin des zweiten.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "Pipe | verbindet stdout → stdin.\n"
            "tee = T-Stück: Ausgabe geht auf Terminal UND in Datei.\n"
            "tee -a = append statt überschreiben.\n"
            "xargs übergibt stdin als Kommandoargumente."
        ),
        memory_tip       = "| = Pipe. tee = T-Stück (Terminal + Datei). xargs = stdin→Argumente.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.05 — grep — Der Text-Detektiv
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.05",
        chapter      = 6,
        title        = "grep — Den Text durchleuchten",
        mtype        = "INFILTRATE",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "In den Logdateien steckt die Wahrheit.\n"
            "Aber Gigabytes an Text durchsuchen?\n"
            "Zara Z3R0: 'grep. Ein Befehl. Millionen Zeilen. Sekundenbruchteile.'"
        ),
        why_important = (
            "grep ist der meistgenutzte Textfilter in Linux.\n"
            "LPIC-1 prüft grep-Optionen, Regex-Grundlagen und egrep/fgrep."
        ),
        explanation  = (
            "grep — Global Regular Expression Print:\n\n"
            "Grundsyntax:\n"
            "  grep 'muster' datei\n"
            "  befehl | grep 'muster'\n\n"
            "Wichtige Optionen:\n"
            "  grep -i 'error' log     # case-insensitive\n"
            "  grep -n 'root' passwd   # mit Zeilennummer\n"
            "  grep -v 'comment' datei # invertieren (ohne Treffer)\n"
            "  grep -c 'error' log     # nur Anzahl\n"
            "  grep -l 'error' /var/log/* # nur Dateinamen\n"
            "  grep -r 'password' /etc # rekursiv\n"
            "  grep -w 'root' passwd   # ganzes Wort\n"
            "  grep -A 3 'ERROR' log   # 3 Zeilen nach Treffer\n"
            "  grep -B 2 'ERROR' log   # 2 Zeilen vor Treffer\n"
            "  grep -C 2 'ERROR' log   # 2 Zeilen vor+nach\n\n"
            "Regex-Grundlagen:\n"
            "  .       — ein beliebiges Zeichen\n"
            "  *       — vorheriges 0 oder mehr mal\n"
            "  ^       — Zeilenanfang\n"
            "  $       — Zeilenende\n"
            "  [abc]   — eine von: a, b oder c\n"
            "  [^abc]  — keine von: a, b, c\n"
            "  \\b      — Wortgrenze\n\n"
            "Varianten:\n"
            "  grep  = Basic Regular Expressions (BRE)\n"
            "  egrep = Extended RE  (wie grep -E): +, ?, |, ()\n"
            "  fgrep = Fixed string (wie grep -F): kein Regex\n\n"
            "Beispiele:\n"
            "  grep '^root' /etc/passwd         # Zeilen mit 'root' am Anfang\n"
            "  grep 'error$' /var/log/syslog    # Zeilen die auf 'error' enden\n"
            "  egrep 'error|warn' /var/log/syslog  # error ODER warn\n"
            "  grep -v '^#' /etc/ssh/sshd_config | grep -v '^$'  # kein Kommentar/Leerzeile"
        ),
        syntax       = "grep 'muster' datei\ngrep -i -n -v -r 'muster' pfad",
        example      = (
            "$ grep -n 'root' /etc/passwd\n"
            "1:root:x:0:0:root:/root:/bin/bash\n"
            "4:sync:x:4:65534:sync:/bin:/bin/sync\n\n"
            "$ grep -v '^#' /etc/ssh/sshd_config | grep -v '^$'\n"
            "Port 22\nPermitRootLogin no\nPasswordAuthentication no"
        ),
        task_description  = "Suche nach 'root' in /etc/passwd",
        expected_commands = ["grep", "grep root /etc/passwd"],
        hint_text         = "grep 'root' /etc/passwd sucht nach dem Muster 'root'",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'grep -v 'comment' datei'?",
                options     = [
                    "A) Zeigt alle Zeilen mit 'comment'",
                    "B) Zeigt alle Zeilen OHNE 'comment'",
                    "C) Zählt Zeilen mit 'comment'",
                    "D) Zeigt verbose Ausgabe",
                ],
                correct     = "B",
                explanation = "-v = invert = invertieren. Zeigt Zeilen die NICHT auf das Muster passen.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welche grep-Variante unterstützt erweiterte Regex (|, +, ?)?",
                options     = ["A) grep", "B) fgrep", "C) egrep (grep -E)", "D) pgrep"],
                correct     = "C",
                explanation = "egrep (oder grep -E) = Extended Regular Expressions: |, +, ?, () ohne Backslash.",
                xp_value    = 20,
            ),
        ],
        exam_tip         = (
            "grep -v = ohne Treffer. grep -i = case-insensitive.\n"
            "grep -r = rekursiv. grep -n = Zeilennummern.\n"
            "^muster = am Zeilenanfang. muster$ = am Zeilenende.\n"
            "egrep = grep -E (Extended Regex mit |, +, ?)."
        ),
        memory_tip       = "grep -v=ohne. -i=case-ignore. -n=Nummern. -r=rekursiv. ^=Anfang.$=Ende.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.06 — cut / sort / uniq / wc
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.06",
        chapter      = 6,
        title        = "cut / sort / uniq / wc — Text-Werkzeuge",
        mtype        = "DECODE",
        xp           = 95,
        speaker      = "RUST",
        story        = (
            "Ein Logfile mit 50.000 Zeilen liegt vor Ghost.\n"
            "Rust: 'cut, sort, uniq, wc — vier Werkzeuge.\n"
            " Kombiniert können sie jedes Datenproblem lösen.'"
        ),
        why_important = (
            "Diese vier Befehle sind LPIC-1 Kernstoff für Textverarbeitung.\n"
            "Häufig in Kombination geprüft."
        ),
        explanation  = (
            "cut — Spalten ausschneiden:\n"
            "  cut -d: -f1 /etc/passwd      # Feld 1, Trennzeichen ':'\n"
            "  cut -d: -f1,3 /etc/passwd    # Felder 1 und 3\n"
            "  cut -d: -f1-3 /etc/passwd    # Felder 1 bis 3\n"
            "  cut -c1-10 datei             # Zeichen 1 bis 10\n\n"
            "sort — Sortieren:\n"
            "  sort datei                   # alphabetisch\n"
            "  sort -r datei                # umgekehrt\n"
            "  sort -n datei                # numerisch\n"
            "  sort -k2 datei               # nach Spalte 2\n"
            "  sort -t: -k3 -n /etc/passwd  # /etc/passwd nach UID\n"
            "  sort -u datei                # sortiert + eindeutig\n\n"
            "uniq — Duplikate entfernen:\n"
            "  sort datei | uniq            # Duplikate entfernen\n"
            "  sort datei | uniq -c         # mit Zählwert\n"
            "  sort datei | uniq -d         # nur Duplikate zeigen\n"
            "  sort datei | uniq -u         # nur Einmalige zeigen\n"
            "  WICHTIG: uniq braucht sortierte Eingabe!\n\n"
            "wc — Word Count:\n"
            "  wc datei                     # Zeilen Wörter Bytes\n"
            "  wc -l datei                  # nur Zeilen\n"
            "  wc -w datei                  # nur Wörter\n"
            "  wc -c datei                  # nur Bytes\n"
            "  wc -m datei                  # Zeichen (multibyte)\n\n"
            "Praxis-Kombination:\n"
            "  cut -d: -f1 /etc/passwd | sort | uniq\n"
            "  cat access.log | cut -d' ' -f1 | sort | uniq -c | sort -rn | head"
        ),
        syntax       = "cut -d: -f1 /etc/passwd\nsort -n datei\nwc -l datei",
        example      = (
            "$ cut -d: -f1,3 /etc/passwd | head -4\n"
            "root:0\ndaemon:1\nbin:2\nsys:3\n\n"
            "$ cat /var/log/syslog | grep 'error' | wc -l\n42\n\n"
            "$ cut -d: -f1 /etc/passwd | sort | uniq -c | sort -rn\n"
            "      1 root\n      1 ghost\n      1 www-data"
        ),
        task_description  = "Zähle die Zeilen in /etc/passwd mit wc",
        expected_commands = ["wc -l /etc/passwd", "wc"],
        hint_text         = "wc -l /etc/passwd zählt die Zeilen",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'cut -d: -f1 /etc/passwd'?",
                options     = [
                    "A) Zeigt alles nach dem ersten ':'",
                    "B) Zeigt das erste Feld (Benutzername) aus /etc/passwd",
                    "C) Schneidet die erste Zeile ab",
                    "D) Zeigt Zeichen 1 bis zum ':'",
                ],
                correct     = "B",
                explanation = "-d: setzt ':' als Trennzeichen. -f1 wählt das erste Feld. /etc/passwd = Benutzernamenliste.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Warum braucht uniq sortierte Eingabe?",
                options     = [
                    "A) Weil uniq nur Zeilen-Paare vergleicht",
                    "B) Weil uniq alphabetisch sortiert",
                    "C) Weil uniq nur aufeinanderfolgende Duplikate findet",
                    "D) Weil uniq sonst abstürzt",
                ],
                correct     = "C",
                explanation = "uniq vergleicht immer nur benachbarte Zeilen. Unsortierte Daten: Duplikate die nicht nebeneinander stehen, werden übersehen.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "cut -d: -f1 = Feld 1 mit ':' als Trenner. -c = Zeichen.\n"
            "sort -n = numerisch. sort -r = reverse. sort -k3 = Spalte 3.\n"
            "uniq -c = Zählen. uniq braucht sort davor!\n"
            "wc -l = Zeilen. wc -w = Wörter. wc -c = Bytes."
        ),
        memory_tip       = "cut=Spalten. sort -n=Zahlen. uniq=Duplikate(braucht sort!). wc -l=Zeilen.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.07 — head / tail / cat / less
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.07",
        chapter      = 6,
        title        = "head / tail / cat / less — Dateien lesen",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "ZARA Z3R0",
        story        = (
            "50 Gigabyte Logfile. Ghost will die letzten Fehler sehen.\n"
            "Zara Z3R0: 'Öffne die Datei nicht komplett, Ghost.\n"
            " tail zeigt dir das Ende. head den Anfang. less alles.'"
        ),
        why_important = (
            "head, tail, cat, less sind Standardwerkzeuge für Dateianalyse.\n"
            "LPIC-1: tail -f für Live-Monitoring ist besonders wichtig."
        ),
        explanation  = (
            "head — Anfang anzeigen:\n"
            "  head datei           # erste 10 Zeilen\n"
            "  head -n 20 datei     # erste 20 Zeilen\n"
            "  head -5 datei        # erste 5 (Kurzform)\n"
            "  head -c 100 datei    # erste 100 Bytes\n\n"
            "tail — Ende anzeigen:\n"
            "  tail datei           # letzte 10 Zeilen\n"
            "  tail -n 20 datei     # letzte 20 Zeilen\n"
            "  tail -f datei        # LIVE folgen (Log-Monitoring!)\n"
            "  tail -F datei        # live + Datei-Rotation\n"
            "  tail -n +5 datei     # ab Zeile 5 bis Ende\n\n"
            "cat — Datei ausgeben:\n"
            "  cat datei            # Inhalt anzeigen\n"
            "  cat -n datei         # mit Zeilennummern\n"
            "  cat -A datei         # versteckte Zeichen (^I=Tab, $=Newline)\n"
            "  cat datei1 datei2    # verketten\n"
            "  cat datei1 datei2 > combined.txt\n\n"
            "less — interaktiv:\n"
            "  less datei           # paged viewer\n"
            "  /muster              # vorwärts suchen\n"
            "  ?muster              # rückwärts suchen\n"
            "  n                    # nächster Treffer\n"
            "  N                    # vorheriger Treffer\n"
            "  G                    # Ende der Datei\n"
            "  g                    # Anfang der Datei\n"
            "  q                    # beenden\n\n"
            "more — ältere Alternative zu less (nur vorwärts)"
        ),
        syntax       = "tail -f /var/log/syslog\nhead -20 datei\ncat -n datei",
        example      = (
            "$ tail -f /var/log/auth.log\n"
            "Jan 15 08:05:01 neongrid9 sshd[1337]: Accepted publickey for ghost\n"
            "Jan 15 08:05:02 neongrid9 systemd-logind[987]: New session 3\n"
            "(Live — neue Zeilen erscheinen sofort. Ctrl+C zum Beenden)"
        ),
        task_description  = "Zeige die ersten 5 Zeilen von /etc/passwd",
        expected_commands = ["head", "head -5 /etc/passwd", "head -n 5 /etc/passwd"],
        hint_text         = "head -5 /etc/passwd zeigt die ersten 5 Zeilen",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'tail -f /var/log/syslog'?",
                options     = ['A) Zeigt letzten Fehler', 'B) Zeigt Log-Datei live/in Echtzeit', 'C) Zeigt nur Fehler', 'D) Filtert Log'],
                correct     = 'B',
                explanation = 'tail -f = follow = Live-Monitoring. Neue Zeilen werden sofort angezeigt.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was ist der Unterschied zwischen tail -f und tail -F?',
                options     = ['A) Kein Unterschied', 'B) -F funktioniert auch nach Log-Rotation (öffnet neue Datei)', 'C) -f ist schneller', 'D) -F zeigt mehr Zeilen'],
                correct     = 'B',
                explanation = 'tail -F = --follow=name, öffnet die Datei neu nach Log-Rotation. Wichtig für Produktions-Logs.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "tail -f = follow = Live-Monitoring von Logfiles.\n"
            "tail -F = wie -f aber funktioniert auch bei Log-Rotation.\n"
            "cat -A zeigt versteckte Zeichen (Windows-Zeilenenden = ^M$).\n"
            "head -c 100 = erste 100 Bytes, nicht Zeilen."
        ),
        memory_tip       = "tail -f = follow (live). head=Anfang. tail=Ende. cat=alles. less=interaktiv.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.08 — tr / sed — Text transformieren
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.08",
        chapter      = 6,
        title        = "tr & sed — Text transformieren",
        mtype        = "DECODE",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Ghost muss einen Datensatz bereinigen.\n"
            "Großbuchstaben → Kleinbuchstaben. Trennzeichen ersetzen.\n"
            "Zara Z3R0: 'tr und sed, Ghost. Die Transformatoren der Shell.'"
        ),
        why_important = (
            "tr und sed sind Power-Tools für Text-Manipulation.\n"
            "LPIC-1 prüft tr für Zeichen-Substitution und sed -i für In-Place-Editing."
        ),
        explanation  = (
            "tr — Translate/Delete Zeichen:\n\n"
            "  echo 'Hello' | tr 'a-z' 'A-Z'   # Kleinbuchstaben → GROSS\n"
            "  echo 'HELLO' | tr 'A-Z' 'a-z'   # GROSS → Kleinbuchstaben\n"
            "  echo 'a:b:c' | tr ':' ','        # : → ,\n"
            "  tr -d '\\n' < datei              # Newlines löschen\n"
            "  tr -s ' ' < datei                # mehrfache Spaces komprimieren\n"
            "  tr -cd '0-9' < datei             # nur Ziffern behalten\n\n"
            "  Zeichenklassen:\n"
            "    [:alpha:] [:digit:] [:upper:] [:lower:] [:space:]\n"
            "  echo 'abc123' | tr -d '[:digit:]'  # Ziffern löschen\n\n"
            "sed — Stream Editor:\n\n"
            "  sed 's/alt/neu/' datei        # erste Übereinstimmung ersetzen\n"
            "  sed 's/alt/neu/g' datei       # alle ersetzen (g=global)\n"
            "  sed 's/alt/neu/gi' datei      # alle, case-insensitive\n"
            "  sed -i 's/alt/neu/g' datei    # in-place (Datei direkt ändern)\n"
            "  sed -i.bak 's/alt/neu/g' datei # mit Backup\n\n"
            "  sed '3d' datei                # Zeile 3 löschen\n"
            "  sed '/muster/d' datei         # Zeilen mit Muster löschen\n"
            "  sed -n '5,10p' datei          # nur Zeilen 5-10 drucken\n"
            "  sed -n '/start/,/end/p' datei # Bereich drucken\n"
            "  sed 's/^/PREFIX/' datei       # Präfix hinzufügen\n"
            "  sed 's/$/ SUFFIX/' datei      # Suffix hinzufügen"
        ),
        syntax       = "echo 'text' | tr 'a-z' 'A-Z'\nsed 's/alt/neu/g' datei\nsed -i 's/alt/neu/g' datei",
        example      = (
            "$ echo 'neongrid-9' | tr 'a-z' 'A-Z'\nNEONGRID-9\n\n"
            "$ sed -i.bak 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config\n"
            "# Original gesichert als /etc/ssh/sshd_config.bak"
        ),
        task_description  = "Konvertiere Text mit tr",
        expected_commands = ["tr", "sed"],
        hint_text         = "echo 'text' | tr 'a-z' 'A-Z' konvertiert zu Großbuchstaben",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'sed -i 's/foo/bar/g' datei.txt'?",
                options     = [
                    "A) Gibt modifizierten Text aus, Datei unverändert",
                    "B) Modifiziert datei.txt direkt (in-place)",
                    "C) Erstellt eine neue Datei datei.txt.new",
                    "D) Fehler — -i braucht einen Backup-Suffix",
                ],
                correct     = "B",
                explanation = "sed -i = in-place. Die Datei wird direkt geändert. Ohne -i: Ausgabe auf stdout, Datei unverändert.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "sed 's/alt/neu/g' = ersetzen (g=global, alle Treffer).\n"
            "sed -i = in-place (Datei direkt ändern).\n"
            "tr 'A-Z' 'a-z' = Großbuchstaben zu Klein.\n"
            "tr -d 'zeichen' = Zeichen löschen."
        ),
        memory_tip       = "tr=Zeichen ersetzen/löschen. sed s/alt/neu/g=Text ersetzen. -i=in-place.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.09 — awk — Spalten-Extraktor
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.09",
        chapter      = 6,
        title        = "awk — Der Daten-Extraktor",
        mtype        = "DECODE",
        xp           = 95,
        speaker      = "RUST",
        story        = (
            "Ghost braucht nur die IP-Adressen aus einem Logfile.\n"
            "Nicht die ganze Zeile. Nur Spalte 1.\n"
            "Rust: 'awk. Eine Zeile Code. Millionen Zeilen verarbeitet.'"
        ),
        why_important = (
            "awk ist der Standard-Tool für spaltenbasierte Text-Verarbeitung.\n"
            "LPIC-1 prüft Grundlagen: $1, $NF, FS, NR, print."
        ),
        explanation  = (
            "awk — Spalten und Muster verarbeiten:\n\n"
            "Grundsyntax:\n"
            "  awk '{aktion}' datei\n"
            "  awk '/muster/{aktion}' datei\n\n"
            "Spezialvariablen:\n"
            "  $0   — gesamte Zeile\n"
            "  $1   — erstes Feld\n"
            "  $2   — zweites Feld\n"
            "  $NF  — letztes Feld (NF = Number of Fields)\n"
            "  NR   — aktuelle Zeilennummer\n"
            "  FS   — Field Separator (Standard: Leerzeichen/Tab)\n\n"
            "Trennzeichen setzen:\n"
            "  awk -F: '{print $1}' /etc/passwd    # ':' als Trenner\n"
            "  awk -F, '{print $2}' csv.txt         # ',' als Trenner\n\n"
            "Beispiele:\n"
            "  awk '{print $1}' datei               # erste Spalte\n"
            "  awk '{print $1,$3}' datei             # Spalten 1 und 3\n"
            "  awk -F: '{print $1,$3}' /etc/passwd  # User + UID\n"
            "  awk '{print NR, $0}' datei            # mit Zeilennummer\n"
            "  awk '/error/{print}' log.txt          # Zeilen mit 'error'\n"
            "  awk '$3 > 1000' /etc/passwd           # UID > 1000\n"
            "  awk 'NR==1' datei                     # nur erste Zeile\n"
            "  awk 'END{print NR}' datei             # Anzahl Zeilen (wie wc -l)\n\n"
            "Vs. cut:\n"
            "  cut: einfach, schnell, nur ein Trenner\n"
            "  awk: flexibel, kann filtern und rechnen"
        ),
        syntax       = "awk '{print $1}' datei\nawk -F: '{print $1,$3}' /etc/passwd",
        example      = (
            "$ awk -F: '{print $1,$3}' /etc/passwd | head -4\n"
            "root 0\ndaemon 1\nbin 2\nghost 1000\n\n"
            "$ ps aux | awk '{print $1,$2,$11}'\n"
            "USER PID COMMAND\nroot 1 /sbin/init\nghost 1337 sshd"
        ),
        task_description  = "Extrahiere Benutzernamen aus /etc/passwd mit awk",
        expected_commands = ["awk", "awk -F: '{print $1}' /etc/passwd"],
        hint_text         = "awk -F: '{print $1}' /etc/passwd druckt erste Spalte",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was bedeutet $NF in awk?',
                options     = ['A) Kein Feld gefunden', 'B) Letzte Spalte (Number of Fields)', 'C) Neue Funktion', 'D) Null-Feld'],
                correct     = 'B',
                explanation = '$NF = letzte Spalte. $1 = erste, $2 = zweite. NR = aktuelle Zeilennummer.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welcher awk-Befehl nutzt Doppelpunkt als Feldtrenner?',
                options     = ["A) awk '$:' /etc/passwd", "B) awk -F: '{print $1}' /etc/passwd", 'C) awk --sep: /etc/passwd', "D) awk ':' /etc/passwd"],
                correct     = 'B',
                explanation = 'awk -F: = Feldtrenner Doppelpunkt. Klassisch für /etc/passwd.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "awk $1=erste Spalte. $NF=letzte Spalte. NR=Zeilennummer.\n"
            "awk -F: = Doppelpunkt als Trennzeichen.\n"
            "awk '/muster/{print}' = grep-ähnliches Filtern.\n"
            "awk 'END{print NR}' = Zeilen zählen."
        ),
        memory_tip       = "awk $1=erste Spalte. -F=Field Separator. NR=Row Number. NF=Felder gesamt.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.10 — Datei-Management: cp / mv / rm / touch / mkdir
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.10",
        chapter      = 6,
        title        = "cp / mv / rm / touch / mkdir — Dateisystem-Operationen",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "Grundoperationen. Jeder Ghost braucht sie.\n"
            "Rust: 'cp, mv, rm, mkdir — einfach aber tödlich.\n"
            " rm -rf / ist das Ende. Kenn sie gut.'"
        ),
        why_important = (
            "Basis-Dateioperationen sind LPIC-1 Pflicht.\n"
            "Wichtige Flags (-r, -f, -i, -p) werden geprüft."
        ),
        explanation  = (
            "cp — Copy:\n"
            "  cp datei ziel            # Datei kopieren\n"
            "  cp -r verz/ ziel/        # Verzeichnis rekursiv\n"
            "  cp -p datei ziel         # Rechte + Zeitstempel behalten\n"
            "  cp -a verz/ ziel/        # Archiv (wie -rp + Symlinks)\n"
            "  cp -i datei ziel         # nachfragen bei Überschreiben\n"
            "  cp -u datei ziel         # nur wenn neuer\n\n"
            "mv — Move/Rename:\n"
            "  mv alt.txt neu.txt       # umbenennen\n"
            "  mv datei /opt/           # verschieben\n"
            "  mv -i datei ziel         # nachfragen\n"
            "  mv -f datei ziel         # force\n\n"
            "rm — Remove:\n"
            "  rm datei                 # Datei löschen\n"
            "  rm -r verzeichnis/       # Verzeichnis rekursiv\n"
            "  rm -f datei              # force (kein Fehler wenn fehlt)\n"
            "  rm -rf verzeichnis/      # GEFÄHRLICH: alles ohne Rückfrage\n"
            "  rm -i datei              # immer nachfragen\n\n"
            "touch — Datei erstellen/Zeitstempel aktualisieren:\n"
            "  touch datei.txt          # erstellen oder atime/mtime aktualisieren\n"
            "  touch -t 202501150800 datei  # Zeitstempel setzen\n\n"
            "mkdir — Verzeichnis erstellen:\n"
            "  mkdir verzeichnis\n"
            "  mkdir -p /pfad/zu/neuem/verz  # eltern automatisch erstellen\n"
            "  mkdir -m 700 privat/          # mit Rechten\n\n"
            "rmdir — leeres Verzeichnis löschen:\n"
            "  rmdir verzeichnis        # nur wenn leer!"
        ),
        syntax       = "cp -a quelle/ ziel/\nrm -rf verzeichnis/\nmkdir -p /pfad/tief",
        example      = (
            "$ mkdir -p /opt/neongrid/config\n"
            "$ cp -a /etc/nginx/ /opt/neongrid/config/nginx_backup/\n"
            "$ touch /tmp/checkpoint_$(date +%Y%m%d)\n"
            "$ rm -rf /tmp/old_cache/"
        ),
        task_description  = "Zeige den Inhalt eines Verzeichnisses",
        expected_commands = ["ls", "ls -la"],
        hint_text         = "ls -la zeigt Verzeichnisinhalt mit Rechten",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'cp -a' und 'cp -p'?",
                options     = ['A) Kein Unterschied', 'B) -a = archive (Rechte+Zeit+Symlinks), -p = nur Rechte+Zeit', 'C) -p ist komplett, -a nur Rechte', 'D) -a für Verzeichnisse, -p für Dateien'],
                correct     = 'B',
                explanation = 'cp -a = archive, erhält alles inkl. Symlinks. cp -p = preserve (Rechte+Zeitstempel).',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was passiert bei 'rm -rf /verzeichnis/'?",
                options     = ['A) Nur leere Verzeichnisse werden gelöscht', 'B) Alle Dateien und Verzeichnisse werden sofort gelöscht (kein Undo!)', 'C) Fragt nach Bestätigung', 'D) Verschiebt in Trash'],
                correct     = 'B',
                explanation = 'rm -rf = rekursiv force = sofort gelöscht, kein Undo, kein Papierkorb!',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "cp -a = archive (Rechte + Zeitstempel + Symlinks). cp -p nur Rechte/Zeit.\n"
            "rm -rf = rekursiv force = KEIN UNDO!\n"
            "mkdir -p = parent-Verzeichnisse automatisch erstellen.\n"
            "touch = Datei erstellen ODER Zeitstempel aktualisieren."
        ),
        memory_tip       = "cp -a=alles behalten. rm -rf=kein Undo. mkdir -p=eltern auch. touch=erstellen/aktualisieren.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.11 — Quoting & Globbing
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.11",
        chapter      = 6,
        title        = "Quoting & Globbing — Shell-Expansion meistern",
        mtype        = "DECODE",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Die Shell interpretiert Zeichen bevor sie den Befehl ausführt.\n"
            "Das kann dich retten oder ruinieren.\n"
            "Zara Z3R0: 'Quoting und Globbing kontrollieren — oder sie kontrollieren dich.'"
        ),
        why_important = (
            "Quoting und Globbing-Regeln sind LPIC-1 Pflicht.\n"
            "Falsche Quotes = falsche Ergebnisse = Datenverlust."
        ),
        explanation  = (
            "Globbing — Wildcards:\n"
            "  *        — beliebig viele Zeichen\n"
            "  ?        — genau ein Zeichen\n"
            "  [abc]    — eines von: a, b, c\n"
            "  [a-z]    — Bereich a bis z\n"
            "  [!abc]   — nicht a, b, c\n"
            "  {a,b,c}  — Brace Expansion: a, b, c\n\n"
            "Beispiele:\n"
            "  ls *.log             # alle .log Dateien\n"
            "  ls file?.txt         # file1.txt, fileA.txt ...\n"
            "  ls file[0-9].txt     # file0.txt bis file9.txt\n"
            "  mkdir {jan,feb,mar}  # drei Verzeichnisse\n"
            "  cp /etc/{hosts,passwd,fstab} /backup/\n\n"
            "Quoting:\n"
            "  Doppelte Anführungszeichen \"...\"\n"
            "  - $ Variablen werden expandiert\n"
            "  - ` Backticks werden ausgeführt\n"
            "  - Leerzeichen geschützt\n"
            "  echo \"Hallo $USER\"    # → Hallo ghost\n\n"
            "  Einfache Anführungszeichen '...'\n"
            "  - ALLES wird wörtlich genommen\n"
            "  - Keine Expansion\n"
            "  echo 'Hallo $USER'    # → Hallo $USER\n\n"
            "  Backslash \\\n"
            "  - Nächstes Zeichen schützen\n"
            "  echo \\$USER          # → $USER\n"
            "  rm datei\\ mit\\ leerzeichen.txt\n\n"
            "Command Substitution:\n"
            "  $(befehl)   oder  `befehl`\n"
            "  echo \"Heute ist $(date)\"\n"
            "  FILES=$(ls /etc/*.conf)"
        ),
        syntax       = "echo \"$USER\"\necho '$USER'\nls *.log\ncp /etc/{hosts,passwd} /backup/",
        example      = (
            "$ echo \"Hallo $USER, heute ist $(date +%A)\"\n"
            "Hallo ghost, heute ist Wednesday\n\n"
            "$ echo 'Hallo $USER, heute ist $(date +%A)'\n"
            "Hallo $USER, heute ist $(date +%A)\n\n"
            "$ cp /etc/{hosts,fstab,passwd} /tmp/backup/\n"
            "# Kopiert drei Dateien auf einmal"
        ),
        task_description  = "Teste den Unterschied zwischen einfachen und doppelten Quotes",
        expected_commands = ["echo", "ls"],
        hint_text         = "echo \"$HOME\" vs echo '$HOME' zeigt den Unterschied",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was gibt 'echo '$HOME'' aus?",
                options     = [
                    "A) /home/ghost (den echten Wert von $HOME)",
                    "B) $HOME (wörtlich, keine Expansion)",
                    "C) Fehler",
                    "D) Den Home-Pfad des root-Users",
                ],
                correct     = "B",
                explanation = "Einfache Quotes unterdrücken ALLE Expansion. $HOME wird wörtlich als '$HOME' ausgegeben.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "Doppelte Quotes: $VAR wird expandiert, Leerzeichen geschützt.\n"
            "Einfache Quotes: ALLES wörtlich, keine Expansion.\n"
            "$(befehl) = Command Substitution (Backticks sind veraltet).\n"
            "Brace Expansion: {a,b,c} = a b c; {1..5} = 1 2 3 4 5."
        ),
        memory_tip       = "Einfach='wörtlich'. Doppelt=\"$expandiert\". $()=Befehl. *=Wildcard.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.12 — awk Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.12",
        chapter      = 6,
        title        = "awk Grundlagen — Felder, FS, NR, NF",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Das Logfile hat zehn Felder pro Zeile.\n"
            "Ghost braucht nur das erste — die IP-Adresse.\n"
            "Zara Z3R0: 'awk '{print $1}', Ghost.\n"
            " Ein Befehl. Millionen Zeilen. Nur die Spalte die zählt.'"
        ),
        why_important = (
            "awk ist das Standard-Tool für spaltenbasierte Text-Verarbeitung.\n"
            "LPIC-1 prüft $1, $NF, FS, NR, NF und den Unterschied zu cut."
        ),
        explanation  = (
            "awk Grundlagen:\n\n"
            "Syntax:\n"
            "  awk '{aktion}' datei\n"
            "  awk '/muster/{aktion}' datei\n"
            "  awk 'BEGIN{...} {aktion} END{...}' datei\n\n"
            "Spezialvariablen:\n"
            "  $0    — gesamte Zeile\n"
            "  $1    — erstes Feld (erste Spalte)\n"
            "  $2    — zweites Feld\n"
            "  $NF   — letztes Feld (NF = Number of Fields)\n"
            "  NR    — aktuelle Zeilennummer (Number of Records)\n"
            "  NF    — Anzahl Felder in aktueller Zeile\n"
            "  FS    — Field Separator (Standard: Whitespace)\n"
            "  OFS   — Output Field Separator\n\n"
            "Trennzeichen setzen:\n"
            "  awk -F: '{print $1}' /etc/passwd    # ':' als Trenner\n"
            "  awk -F, '{print $2}' csv.txt         # ',' als Trenner\n"
            "  awk 'BEGIN{FS=\":\"}{print $1}' datei  # via BEGIN-Block\n\n"
            "Einfache Beispiele:\n"
            "  awk '{print $1}' datei               # erste Spalte\n"
            "  awk '{print $1,$3}' datei             # Spalten 1 und 3\n"
            "  awk '{print NR, $0}' datei            # Zeilennummer + Zeile\n"
            "  awk -F: '{print $1,$3}' /etc/passwd  # Benutzername + UID\n"
            "  awk '{print NF}' datei                # Anzahl Felder pro Zeile\n"
            "  awk 'END{print NR}' datei             # Anzahl Zeilen (wie wc -l)\n\n"
            "BEGIN und END:\n"
            "  awk 'BEGIN{print \"Start\"} {print $1} END{print \"Fertig\"}' datei\n"
            "  awk 'BEGIN{sum=0}{sum+=$1}END{print sum}' zahlen.txt"
        ),
        syntax       = "awk '{print $1}' datei\nawk -F: '{print $1,$3}' /etc/passwd\nawk 'END{print NR}' datei",
        example      = (
            "$ awk -F: '{print $1,$3}' /etc/passwd | head -4\n"
            "root 0\ndaemon 1\nbin 2\nghost 1000\n\n"
            "$ awk '{print NR\": \"$0}' /etc/hostname\n"
            "1: neongrid9\n\n"
            "$ ps aux | awk '{print $1,$2,$11}' | head -3\n"
            "USER PID COMMAND\nroot 1 /sbin/init\nghost 1337 sshd"
        ),
        task_description  = "Extrahiere die Benutzernamen aus /etc/passwd mit awk",
        expected_commands = ["awk -F: '{print $1}' /etc/passwd", "awk"],
        hint_text         = "awk -F: '{print $1}' /etc/passwd druckt das erste Feld mit ':' als Trenner",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was gibt 'awk '{print $NF}' datei' aus?",
                options     = [
                    "A) Die Anzahl der Felder pro Zeile",
                    "B) Das letzte Feld jeder Zeile",
                    "C) Die vorletzte Spalte",
                    "D) Den Wert der Variable NF als Text",
                ],
                correct     = 1,
                explanation = "$NF = das Feld mit der Nummer NF (= Anzahl Felder). Das ist also immer das letzte Feld der Zeile.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was macht der END-Block in awk?",
                options     = [
                    "A) Er wird vor der ersten Zeile ausgeführt",
                    "B) Er wird nach der letzten Zeile ausgeführt",
                    "C) Er definiert das Trennzeichen",
                    "D) Er beendet die Verarbeitung sofort",
                ],
                correct     = 1,
                explanation = "END{...} wird einmal nach Verarbeitung aller Zeilen ausgeführt. Ideal für Summen, Zähler oder Abschluss-Ausgaben.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "awk $1=erste Spalte. $NF=letzte Spalte. NR=Zeilennummer.\n"
            "awk -F: = Doppelpunkt als Trennzeichen.\n"
            "BEGIN{} = vor erster Zeile. END{} = nach letzter Zeile.\n"
            "awk 'END{print NR}' = Zeilen zählen (wie wc -l)."
        ),
        memory_tip       = "awk $1=erste. $NF=letzte. NR=ZeilenNr. -F=Trenner. END=nach allem.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.13 — awk Bedingungen & Ausgabe
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.13",
        chapter      = 6,
        title        = "awk Bedingungen & Ausgabe — Filtern und Rechnen",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "RUST",
        story        = (
            "Ghost braucht alle Zeilen aus dem Log mit Status > 400.\n"
            "Nur awk kann das in einem Schritt: filtern und ausgeben.\n"
            "Rust: 'awk '/muster/' und awk '$3 > 100' — Bedingungen, Ghost.\n"
            " Kein grep. Kein cut. Nur awk.'"
        ),
        why_important = (
            "awk-Bedingungen und Berechnungen heben das Tool über cut und grep hinaus.\n"
            "LPIC-1 prüft Pattern-Matching und numerische Vergleiche in awk."
        ),
        explanation  = (
            "awk Bedingungen:\n\n"
            "Muster-Matching:\n"
            "  awk '/error/{print}' log.txt         # Zeilen mit 'error'\n"
            "  awk '/^root/' /etc/passwd             # Zeilen die mit root beginnen\n"
            "  awk '!/^#/' datei                    # Zeilen ohne führendes #\n\n"
            "Numerische Vergleiche:\n"
            "  awk '$3 > 1000' /etc/passwd           # UID > 1000\n"
            "  awk '$2 == 0' /etc/passwd             # zweites Feld = 0\n"
            "  awk 'NR > 5' datei                    # nur ab Zeile 6\n"
            "  awk 'NR == 1' datei                   # nur erste Zeile\n"
            "  awk 'NR >= 5 && NR <= 10' datei       # Zeilen 5-10\n\n"
            "Logische Operatoren:\n"
            "  awk '$1 == \"root\" && $3 == 0' /etc/passwd  # UND\n"
            "  awk '$3 == 0 || $3 > 1000' /etc/passwd     # ODER\n"
            "  awk '!($3 == 0)' /etc/passwd               # NICHT\n\n"
            "Ausgabe formatieren:\n"
            "  awk '{printf \"%s\\t%s\\n\", $1, $3}' datei  # printf\n"
            "  awk 'BEGIN{OFS=\"|\"}{print $1,$2,$3}' datei # OFS setzen\n\n"
            "Berechnungen:\n"
            "  awk '{sum += $5} END{print sum}' log.txt   # Summe\n"
            "  awk '{count++} END{print count}' datei      # Zählen\n"
            "  awk '$3 > max{max=$3} END{print max}' dat   # Maximum"
        ),
        syntax       = "awk '/pattern/{print}' datei\nawk '$3 > 100{print $1}' datei\nawk '{sum+=$1}END{print sum}' datei",
        example      = (
            "$ awk -F: '$3 > 1000 {print $1, $3}' /etc/passwd\n"
            "ghost 1000\nnobody 65534\n\n"
            "$ awk '/Failed/{print $11}' /var/log/auth.log | sort | uniq -c\n"
            "     5 192.168.1.100\n    12 10.0.0.1\n\n"
            "$ awk '{sum += $NF} END{print \"Total:\", sum}' bills.txt\n"
            "Total: 1337.42"
        ),
        task_description  = "Filtere /etc/passwd mit awk nach UID > 0",
        expected_commands = ["awk -F: '$3 > 0 {print $1}' /etc/passwd", "awk"],
        hint_text         = "awk -F: '$3 > 0 {print $1}' /etc/passwd zeigt User mit UID über 0",
        quiz_questions    = [
            QuizQuestion(
                question    = "awk '/^[^#]/' /etc/sshd_config — was gibt das aus?",
                options     = [
                    "A) Nur Kommentarzeilen (beginnend mit #)",
                    "B) Alle Zeilen außer Kommentaren",
                    "C) Zeilen die mit '#' enden",
                    "D) Zeilen mit Whitespace am Anfang",
                ],
                correct     = 1,
                explanation = "^[^#] = Zeilenanfang gefolgt von 'nicht #'. Damit werden alle Nicht-Kommentar-Zeilen ausgegeben.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "awk '{sum += $1} END{print sum}' zahlen.txt — was passiert?",
                options     = [
                    "A) Gibt die erste Spalte jeder Zeile aus",
                    "B) Summiert alle Werte der ersten Spalte und gibt die Summe am Ende aus",
                    "C) Zählt die Zeilen",
                    "D) Gibt die letzte Zeile aus",
                ],
                correct     = 1,
                explanation = "sum += $1 addiert jede Zeile zur Summe. END{print sum} gibt das Ergebnis nach allen Zeilen aus.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "awk '/muster/' = Pattern-Matching (wie grep in awk).\n"
            "awk '$3 > 1000' = Numerischer Vergleich auf Feld 3.\n"
            "awk '{sum+=$1}END{print sum}' = Summieren.\n"
            "NR==1 = nur erste Zeile. NR>=5 && NR<=10 = Zeilenbereiche."
        ),
        memory_tip       = "awk '/muster/'=grep-like. $3>1000=Vergleich. sum+=$1=Rechnen. END=nach allem.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.14 — sed Erweitert
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.14",
        chapter      = 6,
        title        = "sed Erweitert — -n, -i, -e und Adressbereiche",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA_Z3R0",
        story        = (
            "sed kann mehr als nur ersetzen.\n"
            "Ghost muss Konfigurationsdateien direkt bearbeiten, Bereiche ausgeben.\n"
            "Zara Z3R0: 'sed -n, -i, Adressbereiche.\n"
            " Der Stream Editor ist mächtiger als du denkst, Ghost.'"
        ),
        why_important = (
            "Erweiterte sed-Optionen sind LPIC-1-Prüfungsstoff.\n"
            "sed -i für In-Place-Editing und -n für selektive Ausgabe sind besonders wichtig."
        ),
        explanation  = (
            "sed Erweitert:\n\n"
            "sed -n (silent mode — keine automatische Ausgabe):\n"
            "  sed -n '5p' datei          # nur Zeile 5 ausgeben\n"
            "  sed -n '5,10p' datei       # Zeilen 5-10 ausgeben\n"
            "  sed -n '/muster/p' datei   # Zeilen mit Muster ausgeben\n"
            "  sed -n '/start/,/end/p' d  # Bereich start bis end\n\n"
            "sed -i (in-place — Datei direkt ändern):\n"
            "  sed -i 's/alt/neu/g' datei\n"
            "  sed -i.bak 's/alt/neu/g' datei  # mit Backup als .bak\n"
            "  sed -i '' 's/alt/neu/g' datei   # BSD-Syntax (macOS)\n\n"
            "Mehrere Ausdrücke mit -e:\n"
            "  sed -e 's/foo/bar/g' -e 's/baz/qux/g' datei\n"
            "  sed -e '/^#/d' -e '/^$/d' datei  # Kommentare + Leerzeilen löschen\n\n"
            "Adressbereiche:\n"
            "  sed '3d' datei              # Zeile 3 löschen\n"
            "  sed '3,7d' datei            # Zeilen 3-7 löschen\n"
            "  sed '/muster/d' datei       # Zeilen mit Muster löschen\n"
            "  sed '1~2d' datei            # jede zweite Zeile löschen (ab 1)\n"
            "  sed '5q' datei              # nach Zeile 5 aufhören\n\n"
            "Nützliche Patterns:\n"
            "  sed 's/^/PRÄFIX/' datei     # jeder Zeile Präfix hinzufügen\n"
            "  sed 's/$/ SUFFIX/' datei    # Suffix anhängen\n"
            "  sed 's/[[:space:]]*$//' d   # trailing Whitespace entfernen\n"
            "  sed '/^$/d' datei           # leere Zeilen löschen"
        ),
        syntax       = "sed -n '5,10p' datei\nsed -i.bak 's/alt/neu/g' datei\nsed -e '/^#/d' -e '/^$/d' datei",
        example      = (
            "$ sed -n '/^Port/p' /etc/ssh/sshd_config\nPort 22\n\n"
            "$ sed -i.bak 's/Port 22/Port 2222/' /etc/ssh/sshd_config\n"
            "# Original gesichert als /etc/ssh/sshd_config.bak\n\n"
            "$ sed -e '/^#/d' -e '/^$/d' /etc/ssh/sshd_config | head -5\n"
            "Port 2222\nPermitRootLogin no\nPasswordAuthentication no"
        ),
        task_description  = "Filtere Kommentare aus einer Konfigurationsdatei mit sed",
        expected_commands = ["sed -e '/^#/d' -e '/^$/d'", "sed"],
        hint_text         = "sed '/^#/d' datei löscht alle Kommentarzeilen aus der Ausgabe",
        quiz_questions    = [
            QuizQuestion(
                question    = "sed -n '/Error/p' logfile — was passiert?",
                options     = [
                    "A) Zeilen mit 'Error' werden gelöscht",
                    "B) Nur Zeilen mit 'Error' werden ausgegeben (-n unterdrückt Rest)",
                    "C) Alle Zeilen werden ausgegeben, 'Error'-Zeilen markiert",
                    "D) Die Datei wird nach 'Error' sortiert",
                ],
                correct     = 1,
                explanation = "-n = silent mode, unterdrückt automatische Ausgabe. p = print. Zusammen: nur explizit geprinte Zeilen erscheinen.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist der Vorteil von 'sed -i.bak' gegenüber 'sed -i'?",
                options     = [
                    "A) -i.bak ist schneller",
                    "B) -i.bak erstellt automatisch eine Backup-Kopie der Originaldatei",
                    "C) -i.bak verarbeitet mehrere Dateien",
                    "D) Kein Unterschied",
                ],
                correct     = 1,
                explanation = "-i.bak: Original wird als datei.bak gesichert bevor sed die Änderungen schreibt. -i ohne Suffix überschreibt ohne Backup.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "sed -n = silent (keine auto-Ausgabe). Kombiniert mit p: nur bestimmte Zeilen.\n"
            "sed -i = in-place. sed -i.bak = mit Backup.\n"
            "sed -e 'ausdruck1' -e 'ausdruck2' = mehrere Operationen.\n"
            "Adressbereich: '5,10d' = Zeilen 5-10 löschen. '/start/,/end/p' = Bereich."
        ),
        memory_tip       = "sed -n=still+p=drucken. -i=in-place. -e=mehrere. '5,10p'=Bereich.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.15 — tr — Zeichen transformieren
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.15",
        chapter      = 6,
        title        = "tr — Zeichen ersetzen, löschen und komprimieren",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "Das Logfile hat Windows-Zeilenenden. Großbuchstaben-Chaos.\n"
            "Rust: 'tr, Ghost. Translate.\n"
            " Ein Zeichentauscher, ein Löscher, ein Kompressor.\n"
            " Klein, aber tödlich präzise.'"
        ),
        why_important = (
            "tr ist ein schnelles Tool für Zeichen-Substitution und -Filterung.\n"
            "LPIC-1 prüft tr -d (löschen), tr -s (squeeze) und Zeichenklassen."
        ),
        explanation  = (
            "tr — Translate (Zeichen ersetzen):\n\n"
            "Grundsyntax:\n"
            "  tr SET1 SET2          # Zeichen aus SET1 → SET2\n"
            "  tr -d SET1            # Zeichen aus SET1 löschen\n"
            "  tr -s SET1            # aufeinanderfolgende Zeichen komprimieren\n"
            "  tr -c SET1 SET2       # Komplement (NICHT in SET1)\n\n"
            "Groß/Klein-Konvertierung:\n"
            "  echo 'hello' | tr 'a-z' 'A-Z'       # klein → GROSS\n"
            "  echo 'HELLO' | tr 'A-Z' 'a-z'       # GROSS → klein\n"
            "  echo 'hElLo' | tr '[:upper:]' '[:lower:]'\n\n"
            "Zeichen ersetzen:\n"
            "  echo 'a:b:c' | tr ':' ','            # : → ,\n"
            "  echo 'abc' | tr 'abc' 'xyz'          # a→x, b→y, c→z\n\n"
            "Zeichen löschen (-d):\n"
            "  tr -d '\\n' < datei                  # Newlines entfernen\n"
            "  tr -d '[:digit:]' < datei            # Ziffern entfernen\n"
            "  tr -d '\\r' < windows.txt            # Windows CR entfernen\n\n"
            "Squeeze (-s) — Wiederholungen komprimieren:\n"
            "  echo 'hello   world' | tr -s ' '     # mehrfache Spaces → 1\n"
            "  echo 'aaabbbccc' | tr -s 'a-z'       # → abc\n\n"
            "POSIX-Zeichenklassen:\n"
            "  [:alpha:]  — Buchstaben\n"
            "  [:digit:]  — Ziffern\n"
            "  [:upper:]  — Großbuchstaben\n"
            "  [:lower:]  — Kleinbuchstaben\n"
            "  [:space:]  — Whitespace (Leerzeichen, Tab, Newline)\n"
            "  [:alnum:]  — Buchstaben + Ziffern\n"
            "  [:punct:]  — Satzzeichen"
        ),
        syntax       = "echo 'text' | tr 'a-z' 'A-Z'\ntr -d '[:digit:]' < datei\ntr -s ' ' < datei",
        example      = (
            "$ echo 'NeonGrid-9' | tr 'a-z' 'A-Z'\nNEONGRID-9\n\n"
            "$ echo 'User: ghost   IP: 192.168.1.1' | tr -s ' '\n"
            "User: ghost IP: 192.168.1.1\n\n"
            "$ cat windows.txt | tr -d '\\r' > unix.txt\n"
            "# Windows-Zeilenenden (\\r\\n) → Unix (\\n)"
        ),
        task_description  = "Konvertiere Text zu Großbuchstaben mit tr",
        expected_commands = ["tr 'a-z' 'A-Z'", "tr '[:lower:]' '[:upper:]'"],
        hint_text         = "echo 'text' | tr 'a-z' 'A-Z' konvertiert zu Großbuchstaben",
        quiz_questions    = [
            QuizQuestion(
                question    = "tr -d '[:space:]' < datei — was passiert?",
                options     = [
                    "A) Leerzeichen werden durch Unterstriche ersetzt",
                    "B) Alle Whitespace-Zeichen werden gelöscht",
                    "C) Nur Leerzeichen am Zeilenanfang werden gelöscht",
                    "D) Zeilenumbrüche werden durch Leerzeichen ersetzt",
                ],
                correct     = 1,
                explanation = "-d = löschen. [:space:] = POSIX-Klasse für alle Whitespace-Zeichen (Leerzeichen, Tab, Newline, etc.).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was macht 'tr -s ' '' (tr -s mit Leerzeichen)?",
                options     = [
                    "A) Löscht alle Leerzeichen",
                    "B) Komprimiert mehrfache aufeinanderfolgende Leerzeichen zu einem",
                    "C) Ersetzt Leerzeichen durch Tabs",
                    "D) Fügt Leerzeichen zwischen jeden Buchstaben ein",
                ],
                correct     = 1,
                explanation = "-s = squeeze. Mehrfache aufeinanderfolgende gleiche Zeichen werden auf eines reduziert. Ideal zum Bereinigen von Ausgaben mit variablem Whitespace.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "tr SET1 SET2 = Zeichen ersetzen.\n"
            "tr -d SET = Zeichen löschen.\n"
            "tr -s SET = squeeze (Wiederholungen komprimieren).\n"
            "[:digit:] [:upper:] [:lower:] [:space:] = POSIX-Zeichenklassen."
        ),
        memory_tip       = "tr=translate. -d=delete. -s=squeeze(komprimieren). [:class:]=POSIX.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.16 — wc — Zeilen, Wörter, Bytes
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.16",
        chapter      = 6,
        title        = "wc — Zeilen, Wörter und Bytes zählen",
        mtype        = "CONSTRUCT",
        xp           = 75,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Wie viele Zeilen hat das Logfile? Wie viele Fehler?\n"
            "Zara Z3R0 tippt wc -l und hat die Antwort in Millisekunden.\n"
            "'wc, Ghost. Word Count.\n"
            " -l, -w, -c, -m — vier Optionen. Alles was du brauchst.'"
        ),
        why_important = (
            "wc ist ein Standardwerkzeug für schnelle Datei-Statistiken.\n"
            "LPIC-1 prüft die Unterschiede zwischen -l, -w, -c und -m."
        ),
        explanation  = (
            "wc — Word Count:\n\n"
            "Grundnutzung:\n"
            "  wc datei           # Zeilen Wörter Bytes Dateiname\n"
            "  wc datei1 datei2   # mehrere Dateien + Summe\n\n"
            "Optionen:\n"
            "  wc -l datei        # nur Zeilen (lines)\n"
            "  wc -w datei        # nur Wörter (words)\n"
            "  wc -c datei        # nur Bytes (bytes/chars)\n"
            "  wc -m datei        # Zeichen (multibyte-fähig)\n"
            "  wc -L datei        # längste Zeile (max line length)\n\n"
            "Wichtiger Unterschied -c vs -m:\n"
            "  -c = Bytes (ASCII: identisch mit Zeichen)\n"
            "  -m = Zeichen (bei UTF-8: Multibyte-Zeichen korrekt)\n"
            "  Bei reinem ASCII: -c == -m\n\n"
            "Typische Anwendungen:\n"
            "  wc -l /etc/passwd          # wie viele Benutzer?\n"
            "  grep 'ERROR' logfile | wc -l  # Fehleranzahl\n"
            "  cat datei | wc -w          # Wörter zählen\n"
            "  ls /etc | wc -l            # Dateien in /etc zählen\n\n"
            "Mehrere Dateien:\n"
            "  wc -l /etc/passwd /etc/group\n"
            "  # Zeigt Einzelwerte + Gesamtsumme\n\n"
            "Pipe-Kombination:\n"
            "  find /var/log -name '*.log' | wc -l   # Anzahl Log-Dateien\n"
            "  cat access.log | grep '404' | wc -l   # 404-Fehler"
        ),
        syntax       = "wc -l datei\nwc -w datei\nwc -c datei\ngrep 'fehler' log | wc -l",
        example      = (
            "$ wc /etc/passwd\n"
            "  32  64 1820 /etc/passwd\n"
            "# 32 Zeilen, 64 Wörter, 1820 Bytes\n\n"
            "$ wc -l /etc/passwd\n32 /etc/passwd\n\n"
            "$ grep -c 'nologin' /etc/passwd\n18\n\n"
            "$ ls /etc | wc -l\n187"
        ),
        task_description  = "Zähle die Zeilen in /etc/passwd mit wc -l",
        expected_commands = ["wc -l /etc/passwd", "wc -l"],
        hint_text         = "wc -l /etc/passwd zählt die Zeilen in /etc/passwd",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'wc -c' und 'wc -m'?",
                options     = [
                    "A) Kein Unterschied",
                    "B) -c zählt Bytes, -m zählt Zeichen (multibyte-bewusst)",
                    "C) -c zählt Zeilen, -m zählt Wörter",
                    "D) -c ist schneller als -m",
                ],
                correct     = 1,
                explanation = "-c zählt Bytes. Bei UTF-8 können Zeichen 1-4 Bytes belegen. -m zählt korrekt die Anzahl der Zeichen (multibyte-aware).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "grep 'ERROR' /var/log/syslog | wc -l — was zählt das?",
                options     = [
                    "A) Die Anzahl der Zeichen in 'ERROR'",
                    "B) Die Anzahl der Zeilen die 'ERROR' enthalten",
                    "C) Die Anzahl der Wörter nach 'ERROR'",
                    "D) Die Größe der Logdatei",
                ],
                correct     = 1,
                explanation = "grep 'ERROR' filtert Zeilen mit 'ERROR'. wc -l zählt diese Zeilen. Ergebnis: Anzahl der Fehlermeldungen.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "wc -l = Zeilen. wc -w = Wörter. wc -c = Bytes. wc -m = Zeichen.\n"
            "wc ohne Option gibt alle drei (Zeilen, Wörter, Bytes) aus.\n"
            "cmd | wc -l = häufigste Kombination zum Zählen.\n"
            "-c vs -m: bei UTF-8 können sie sich unterscheiden."
        ),
        memory_tip       = "wc -l=Lines. -w=Words. -c=Chars/bytes. -m=Multibyte-Chars.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.17 — head & tail — Dateianfang und -ende
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.17",
        chapter      = 6,
        title        = "head & tail — Dateianfang, -ende und Live-Monitoring",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "50 Gigabyte Logfile. Ghost will die letzten 20 Fehler sehen.\n"
            "Und dann live weiter beobachten während neue kommen.\n"
            "Rust: 'tail -f. Dein Live-Auge auf das System, Ghost.\n"
            " tail -F noch besser — überlebt Log-Rotation.'"
        ),
        why_important = (
            "head und tail sind Kernwerkzeuge für Datei-Analyse.\n"
            "LPIC-1: tail -f für Live-Monitoring und tail -F für Log-Rotation sind wichtig."
        ),
        explanation  = (
            "head — Dateianfang:\n\n"
            "  head datei           # erste 10 Zeilen (Standard)\n"
            "  head -n 20 datei     # erste 20 Zeilen\n"
            "  head -20 datei       # Kurzform\n"
            "  head -c 100 datei    # erste 100 Bytes\n"
            "  head -n -5 datei     # alles AUSSER die letzten 5 Zeilen\n\n"
            "tail — Dateiende:\n\n"
            "  tail datei           # letzte 10 Zeilen\n"
            "  tail -n 20 datei     # letzte 20 Zeilen\n"
            "  tail -20 datei       # Kurzform\n"
            "  tail -c 100 datei    # letzte 100 Bytes\n"
            "  tail -n +5 datei     # ab Zeile 5 bis Ende\n\n"
            "tail -f — follow (Live-Monitoring):\n"
            "  tail -f /var/log/syslog    # Datei folgen\n"
            "  tail -f /var/log/auth.log  # Auth-Logs live\n"
            "  # Neue Zeilen erscheinen sofort. Ctrl+C zum Beenden.\n\n"
            "tail -F — follow + Log-Rotation:\n"
            "  tail -F /var/log/syslog    # überlebt Rotation!\n"
            "  # Wenn syslog durch syslog.1 ersetzt wird,\n"
            "  # bleibt tail -F an der neuen syslog-Datei.\n"
            "  # tail -f würde am alten Datei-Deskriptor hängen.\n\n"
            "Mehrere Dateien:\n"
            "  tail -f /var/log/syslog /var/log/auth.log\n"
            "  # Zeigt beide Logs mit Dateiname-Header\n\n"
            "Kombination:\n"
            "  tail -n +2 datei           # Überschriftenzeile überspringen\n"
            "  head -n 100 log | tail -n 10  # Zeilen 91-100"
        ),
        syntax       = "tail -f /var/log/syslog\ntail -F /var/log/syslog\nhead -20 datei\ntail -n +2 datei",
        example      = (
            "$ tail -f /var/log/auth.log\n"
            "Jan 15 08:05:01 neongrid9 sshd[1337]: Accepted publickey for ghost\n"
            "Jan 15 08:05:15 neongrid9 sudo: ghost : TTY=pts/0 ; COMMAND=/usr/bin/apt\n"
            "(neue Zeilen erscheinen live — Ctrl+C beendet)\n\n"
            "$ tail -n +2 /etc/passwd | head -3\n"
            "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n"
            "bin:x:2:2:bin:/bin:/usr/sbin/nologin"
        ),
        task_description  = "Zeige die letzten 5 Zeilen von /etc/passwd",
        expected_commands = ["tail -5 /etc/passwd", "tail -n 5 /etc/passwd"],
        hint_text         = "tail -5 /etc/passwd zeigt die letzten 5 Zeilen",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'tail -f' und 'tail -F'?",
                options     = [
                    "A) -F ist schneller",
                    "B) -f folgt dem Datei-Deskriptor, -F folgt dem Dateinamen (überlebt Log-Rotation)",
                    "C) -F zeigt mehr Zeilen",
                    "D) -f ist veraltet, -F ist der neue Standard",
                ],
                correct     = 1,
                explanation = "-f hängt am Datei-Deskriptor. Bei Log-Rotation (Datei umbenannt, neue erstellt) 'hängt' -f an der alten Datei. -F erkennt Rotation und wechselt zur neuen Datei.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "tail -n +5 datei — was gibt das aus?",
                options     = [
                    "A) Die ersten 5 Zeilen",
                    "B) Die letzten 5 Zeilen",
                    "C) Ab Zeile 5 bis zum Ende der Datei",
                    "D) Zeile 5 allein",
                ],
                correct     = 2,
                explanation = "tail -n +5 = 'ab Zeile 5 bis Ende'. Das '+' ändert die Semantik: statt 'letzte 5' bedeutet es 'ab Position 5'.",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "tail -f = folgt der Datei live (Ctrl+C zum Beenden).\n"
            "tail -F = wie -f aber überlebt Log-Rotation (folgt Dateinamen).\n"
            "tail -n +5 = ab Zeile 5 bis Ende ('+' = ab Position).\n"
            "head -n -5 = alles außer die letzten 5 Zeilen."
        ),
        memory_tip       = "tail -f=live(Datei-Handle). -F=live+Rotation(Dateiname). +5=ab Zeile 5.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.18 — Hier-Dokumente (Heredoc)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.18",
        chapter      = 6,
        title        = "Heredoc — Mehrzeilige Eingabe mit cat <<EOF",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Ghost muss eine Konfigurationsdatei direkt im Skript schreiben.\n"
            "Zeile für Zeile echo ist mühsam.\n"
            "Zara Z3R0: 'Heredoc, Ghost. cat <<EOF.\n"
            " Mehrere Zeilen. Ein Befehl. Variablen expandieren — oder nicht.'"
        ),
        why_important = (
            "Heredocs sind für Shell-Skripte und direkte Eingaben essenziell.\n"
            "LPIC-1 prüft Syntax, Variablenexpansion und Einsatz in Skripten."
        ),
        explanation  = (
            "Heredoc — Here Document:\n\n"
            "Grundsyntax:\n"
            "  befehl << MARKER\n"
            "  Zeile 1\n"
            "  Zeile 2\n"
            "  MARKER\n\n"
            "Häufigstes Beispiel:\n"
            "  cat << EOF\n"
            "  Zeile 1\n"
            "  Zeile 2\n"
            "  EOF\n\n"
            "Variablenexpansion:\n"
            "  NAME=Ghost\n"
            "  cat << EOF\n"
            "  Willkommen, $NAME!\n"
            "  Dein Home: $HOME\n"
            "  EOF\n"
            "  # → Variablen werden expandiert\n\n"
            "Expansion verhindern (Marker in Quotes):\n"
            "  cat << 'EOF'\n"
            "  Kein $NAME hier — alles wörtlich\n"
            "  EOF\n\n"
            "In Dateien schreiben:\n"
            "  cat << EOF > /etc/motd\n"
            "  Willkommen auf NeonGrid-9\n"
            "  Zugang nur für autorisierte Hacker!\n"
            "  EOF\n\n"
            "  cat << EOF >> /etc/hosts\n"
            "  192.168.1.100 neongrid9-node\n"
            "  EOF\n\n"
            "Heredoc in Skripten:\n"
            "  #!/bin/bash\n"
            "  mysql -u root << SQL\n"
            "  CREATE DATABASE neongrid;\n"
            "  GRANT ALL ON neongrid.* TO 'ghost'@'localhost';\n"
            "  SQL\n\n"
            "Herestring (<<<):\n"
            "  grep 'muster' <<< 'zu durchsuchender Text'\n"
            "  wc -w <<< 'drei vier fünf'"
        ),
        syntax       = "cat << EOF\n  Zeile 1\n  EOF\ncat << EOF > datei\n  Inhalt\n  EOF",
        example      = (
            "$ cat << EOF > /tmp/test.txt\n"
            "> NeonGrid-9 Zugang\n"
            "> Benutzer: $USER\n"
            "> EOF\n\n"
            "$ cat /tmp/test.txt\n"
            "NeonGrid-9 Zugang\nBenutzer: ghost\n\n"
            "$ grep root <<< \"$(cat /etc/passwd)\"\n"
            "root:x:0:0:root:/root:/bin/bash"
        ),
        task_description  = "Schreibe Text mit Heredoc in eine Datei",
        expected_commands = ["cat << EOF", "cat <<EOF"],
        hint_text         = "cat << EOF > /tmp/test.txt schreibt mehrzeiligen Text in eine Datei",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'cat << EOF' und 'cat << 'EOF''?",
                options     = [
                    "A) Kein Unterschied",
                    "B) Mit Quotes: $-Variablen und `Backticks` werden NICHT expandiert (alles wörtlich)",
                    "C) Mit Quotes: schnellere Ausführung",
                    "D) Mit Quotes: Eingabe aus einer Datei statt Tastatur",
                ],
                correct     = 1,
                explanation = "Heredoc ohne Quotes: Variablen ($VAR) und Backticks werden expandiert. Mit Quotes ('EOF' oder \"EOF\"): alles wird wörtlich behandelt, keine Expansion.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl schreibt mehrzeiligen Text direkt in /etc/hosts?",
                options     = [
                    "A) echo -e 'zeile1\\nzeile2' >> /etc/hosts",
                    "B) cat << EOF >> /etc/hosts",
                    "C) heredoc /etc/hosts",
                    "D) write /etc/hosts << EOF",
                ],
                correct     = 1,
                explanation = "cat << EOF >> /etc/hosts leitet das Heredoc als stdin an cat und hängt die Ausgabe an /etc/hosts an (>>).",
                xp_value    = 15,
            ),
        ],
        exam_tip         = (
            "cat << EOF = Heredoc, Eingabe endet mit 'EOF' am Zeilenanfang.\n"
            "Variablen werden expandiert. 'EOF' (in Quotes) unterdrückt Expansion.\n"
            "cat << EOF > datei = in Datei schreiben.\n"
            "cat << EOF >> datei = an Datei anhängen."
        ),
        memory_tip       = "<<EOF=Heredoc(Variablen expandiert). <<'EOF'=wörtlich. >>=anhängen.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.19 — Quiz: Streams & Pipes
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.19",
        chapter      = 6,
        title        = "QUIZ: Streams, Pipes & Textfilter",
        mtype        = "QUIZ",
        xp           = 130,
        speaker      = "ZARA Z3R0",
        story        = (
            "Der Data-Stream-Prüfraum öffnet sich.\n"
            "Zara Z3R0: 'Pipes, Redirects, grep, awk — teste dein Wissen.\n"
            " Im Examen gibt es keine zweite Chance.'"
        ),
        why_important    = "Prüfungsvorbereitung Topic 103.1-103.4.",
        explanation      = "Teste Wissen über Streams, Filter und Shell-Tools.",
        task_description = "",
        expected_commands = [],
        quiz_questions   = [
            QuizQuestion(
                question    = "Was macht 'find /tmp -name '*.log' 2>/dev/null'?",
                options     = [
                    "A) Sucht nach *.log, Ausgabe in /dev/null",
                    "B) Sucht nach *.log, Fehlermeldungen werden unterdrückt",
                    "C) Löscht alle .log-Dateien in /tmp",
                    "D) Findet Dateien in /dev/null",
                ],
                correct     = "B",
                explanation = "2>/dev/null leitet stderr (Fehlermeldungen, z.B. 'Permission denied') nach /dev/null. Nur stdout erscheint.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen '>' und '>>'?",
                options     = [
                    "A) > = anhängen, >> = überschreiben",
                    "B) > = überschreiben, >> = anhängen",
                    "C) Kein Unterschied",
                    "D) > für Dateien, >> für Verzeichnisse",
                ],
                correct     = "B",
                explanation = "> überschreibt die Zieldatei (oder erstellt sie). >> hängt an eine bestehende Datei an.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "cat /etc/passwd | sort | uniq -c | sort -rn | head -3 — was passiert?",
                options     = [
                    "A) Zeigt die 3 häufigsten Zeilen",
                    "B) Zeigt die 3 ersten Zeilen sortiert",
                    "C) Fehler — uniq braucht -u",
                    "D) Zeigt die 3 letzten Zeilen",
                ],
                correct     = "A",
                explanation = "sort = sortieren. uniq -c = zählen. sort -rn = numerisch absteigend. head -3 = erste 3 (= häufigste).",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "awk -F: '{print $1}' /etc/passwd — was ist $1?",
                options     = [
                    "A) Die gesamte Zeile",
                    "B) Das erste Feld (Benutzername)",
                    "C) Die erste Zeile der Datei",
                    "D) Der erste Buchstabe jeder Zeile",
                ],
                correct     = "B",
                explanation = "$1 = erstes Feld. -F: setzt ':' als Trennzeichen. In /etc/passwd ist $1 der Benutzername.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "grep -v '^#' /etc/ssh/sshd_config — was zeigt das?",
                options     = [
                    "A) Nur Kommentarzeilen",
                    "B) Alle Zeilen außer Kommentaren (die mit # beginnen)",
                    "C) Zeilen die '#' enthalten",
                    "D) Die Zeile mit '#' am Anfang",
                ],
                correct     = "B",
                explanation = "-v = invertieren. ^# = beginnt mit #. Ergebnis: alle Zeilen OHNE führendes #.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'cmd | tee output.txt'?",
                options     = [
                    "A) Ausgabe NUR in output.txt",
                    "B) Ausgabe NUR auf Terminal",
                    "C) Ausgabe auf Terminal UND in output.txt gleichzeitig",
                    "D) Ausgabe wechselt zwischen Terminal und Datei",
                ],
                correct     = "C",
                explanation = "tee = T-Stück. Ausgabe geht gleichzeitig auf stdout (Terminal) UND in die Datei.",
                xp_value    = 20,
            ),
        ],
        exam_tip         = (
            "Quick Review Topic 103:\n"
            "Redirection: > überschreibt, >> hängt an, 2> Fehler, 2>&1 alles.\n"
            "grep -v = ohne Muster. grep -i = case-insensitive.\n"
            "sort | uniq -c = zählen und sortieren.\n"
            "awk $1=erste Spalte, -F=Trennzeichen."
        ),
        memory_tip       = "",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 8),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 6.BOSS — Der Stream-Lord
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "6.BOSS",
        chapter      = 6,
        title        = "BOSS: Der Stream-Lord",
        mtype        = "BOSS",
        xp           = 420,
        speaker      = "SYSTEM",
        story        = (
            "Aus den Datenpipelines materialisiert sich eine Gestalt.\n"
            "Der Stream-Lord — Herr aller I/O-Kanäle.\n"
            "'Du glaubst, du verstehst Pipes? Redirection? Textfilter?\n"
            " Dann decode meine Matrix, Ghost.'"
        ),
        why_important    = "Boss-Prüfung: Kapitel 6 Gesamtwissen",
        explanation      = "Boss-Kampf: Stream-Lord — vollständige Prüfung",
        task_description = "Überlebe den Boss-Quiz!",
        expected_commands = [],
        boss_name        = "STREAM-LORD v6.0",
        boss_desc        = (
            "INITIATING DATA STREAM DEFENSE\n"
            "STDIN: /dev/urandom\n"
            "STDOUT: /dev/null\n"
            "STDERR: your_face.txt\n\n"
            "Prove you can redirect, filter and transform.\n"
            "Or get flushed into /dev/null."
        ),
        quiz_questions   = [
            QuizQuestion(
                question    = "find / -name 'shadow' 2>/dev/null — warum 2>/dev/null?",
                options     = [
                    "A) Um die shadow-Datei zu löschen",
                    "B) Um 'Permission denied'-Fehler bei nicht-lesbaren Verzeichnissen zu unterdrücken",
                    "C) Um die Ausgabe in eine Datei zu schreiben",
                    "D) Weil find sonst abstürzt",
                ],
                correct     = "B",
                explanation = "find durchsucht das gesamte System. Viele Verzeichnisse sind für normale User gesperrt → 'Permission denied'. 2>/dev/null entfernt diese Rausch-Fehler.",
                xp_value    = 40,
            ),
            QuizQuestion(
                question    = "Befehlskette: cat /var/log/auth.log | grep 'Failed' | awk '{print $11}' | sort | uniq -c | sort -rn — was ist das Ergebnis?",
                options     = [
                    "A) Anzahl der fehlgeschlagenen Logins pro Benutzer",
                    "B) Alle IPs die sich erfolgreich eingeloggt haben",
                    "C) Häufigste Quell-IPs von fehlgeschlagenen Login-Versuchen",
                    "D) Zeilen mit dem Wort 'Failed' sortiert",
                ],
                correct     = "C",
                explanation = "grep 'Failed' filtert Fehlversuche. awk $11 holt die IP. sort+uniq -c zählt pro IP. sort -rn = häufigste zuerst. = Brute-Force-Analyse!",
                xp_value    = 40,
            ),
            QuizQuestion(
                question    = "sed -n '10,20p' datei — was passiert?",
                options     = [
                    "A) Löscht Zeilen 10 bis 20",
                    "B) Druckt nur Zeilen 10 bis 20",
                    "C) Ersetzt Zeile 10 durch Zeile 20",
                    "D) Gibt alle Zeilen außer 10-20 aus",
                ],
                correct     = "B",
                explanation = "-n unterdrückt automatische Ausgabe. p = print. 10,20p = drucke Zeilen 10-20.",
                xp_value    = 40,
            ),
            QuizQuestion(
                question    = "echo \"$HOME\" vs echo '$HOME' — was ist der Unterschied?",
                options     = [
                    "A) Kein Unterschied",
                    "B) Doppelte Quotes expandieren $HOME, einfache drucken '$HOME' wörtlich",
                    "C) Einfache Quotes expandieren, doppelte nicht",
                    "D) Beide drucken den Heimverzeichnis-Pfad",
                ],
                correct     = "B",
                explanation = "Doppelte Quotes erlauben $-Expansion. Einfache Quotes = 100% wörtlich. Grundregel!",
                xp_value    = 40,
            ),
            QuizQuestion(
                question    = "ls *.txt | xargs rm — was passiert bei leerer Ausgabe von ls *.txt?",
                options     = [
                    "A) xargs rm macht nichts — kein Input",
                    "B) xargs rm löscht alle Dateien!",
                    "C) rm gibt einen Fehler",
                    "D) ls gibt einen Fehler",
                ],
                correct     = "B",
                explanation = "Wenn ls *.txt keine Dateien findet, gibt es einen Fehler auf stderr, aber xargs bekommt NICHTS. xargs rm ohne Argumente ruft 'rm' ohne Argumente auf — was manchmal alles löscht! Besser: xargs -r rm (nur wenn Input vorhanden).",
                xp_value    = 40,
            ),
            QuizQuestion(
                question    = "tr -d '[:space:]' < datei — was macht das?",
                options     = [
                    "A) Ersetzt Leerzeichen durch Unterstriche",
                    "B) Löscht alle Whitespace-Zeichen (Leerzeichen, Tabs, Newlines)",
                    "C) Löscht nur Leerzeichen, nicht Tabs",
                    "D) Fehler — tr nimmt keine Zeichenklassen",
                ],
                correct     = "B",
                explanation = "tr -d = löschen. [:space:] = POSIX-Zeichenklasse für alle Whitespace-Zeichen inkl. Tabs und Newlines.",
                xp_value    = 40,
            ),
        ],
        gear_reward      = "pipe_wrench",
        faction_reward   = ("Net Runners", 25),
    ),
]
