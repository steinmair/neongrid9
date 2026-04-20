"""
NeonGrid-9 :: Kapitel 11 — SYSLOG MATRIX
LPIC-1 Topic 108.1 / 108.2 / 107.3
Systemlogs, Zeitdienste, Cron & at

"In NeonGrid-9 hinterlässt jeder Prozess eine Spur.
 Syslog. journald. Cron-Jobs im Verborgenen.
 Wer Logs liest, sieht die Vergangenheit.
 Wer Cron kennt, kontrolliert die Zukunft."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_11_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 11.01 — syslog & rsyslog
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.01",
        chapter      = 11,
        title        = "syslog & rsyslog — Das Log-Framework",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Der Angriff wurde gelogged, Ghost.\n"
            " Irgendwo in /var/log liegt der Beweis.\n"
            " syslog und rsyslog sind das Gedächtnis des Systems.\n"
            " Lern es zu lesen — bevor das Imperium die Spuren löscht.'"
        ),
        why_important = (
            "Systemlogs sind die erste Quelle bei Incidents und Debugging.\n"
            "LPIC-1 Topic 108.2 testet rsyslog-Konfiguration, Prioritäten und Einrichtungen."
        ),
        explanation  = (
            "SYSLOG-ARCHITEKTUR:\n\n"
            "  Anwendung → syslog() → rsyslogd → /var/log/\n\n"
            "LOG-DATEIEN (Standard):\n"
            "  /var/log/syslog          allgemeine System-Logs (Debian)\n"
            "  /var/log/messages        allgemeine Logs (RHEL)\n"
            "  /var/log/auth.log        Authentifizierung, sudo, SSH (Debian)\n"
            "  /var/log/secure          Auth-Logs (RHEL)\n"
            "  /var/log/kern.log        Kernel-Meldungen\n"
            "  /var/log/dmesg           Boot-Zeit Kernel-Meldungen\n"
            "  /var/log/mail.log        Mail-Server\n"
            "  /var/log/cron.log        Cron-Jobs (RHEL)\n"
            "  /var/log/dpkg.log        Paket-Installation (Debian)\n"
            "  /var/log/nginx/          Web-Server Logs\n\n"
            "SYSLOG FACILITY (Einrichtung):\n"
            "  kern    0  Kernel\n"
            "  user    1  User-Level\n"
            "  mail    2  Mail-System\n"
            "  daemon  3  System-Daemons\n"
            "  auth    4  Sicherheit/Auth\n"
            "  syslog  5  syslogd intern\n"
            "  lpr     6  Drucker\n"
            "  news    7  Netzwerk-News\n"
            "  local0-7   benutzerdefiniert\n\n"
            "SYSLOG SEVERITY (Schweregrad):\n"
            "  0  emerg    System nicht nutzbar\n"
            "  1  alert    sofortige Aktion nötig\n"
            "  2  crit     kritische Bedingung\n"
            "  3  err      Fehler\n"
            "  4  warning  Warnung\n"
            "  5  notice   normal aber bedeutend\n"
            "  6  info     informativ\n"
            "  7  debug    Debug-Meldungen\n\n"
            "RSYSLOG KONFIGURATION:\n"
            "  /etc/rsyslog.conf          Haupt-Konfiguration\n"
            "  /etc/rsyslog.d/*.conf      Fragmente\n\n"
            "SYNTAX: facility.severity  /var/log/datei\n"
            "  *.info          /var/log/messages    alle Info+\n"
            "  kern.warning    /var/log/kernel      Kernel Warnings+\n"
            "  auth.*          /var/log/auth.log    alle Auth\n"
            "  *.none          nichts loggen\n"
            "  @192.168.1.100  remote syslog UDP\n"
            "  @@192.168.1.100 remote syslog TCP"
        ),
        syntax       = "tail -f /var/log/syslog  |  grep ERROR /var/log/syslog  |  cat /etc/rsyslog.conf",
        example      = (
            "tail -f /var/log/syslog\n"
            "tail -n 50 /var/log/auth.log\n"
            "grep 'Failed password' /var/log/auth.log\n"
            "cat /var/log/kern.log\n"
            "cat /etc/rsyslog.conf"
        ),
        task_description = "Zeige die letzten 20 Zeilen von /var/log/syslog",
        expected_commands = ["tail -n 20 /var/log/syslog"],
        hint_text    = "tail -n 20 /var/log/syslog zeigt die letzten 20 Log-Einträge",
        exam_tip     = (
            "PRÜFUNG: Severity-Level auswendig kennen!\n"
            "  0=emerg 1=alert 2=crit 3=err 4=warn 5=notice 6=info 7=debug\n"
            "Merkhilfe: Every Annoying Creature Errors Warnings Never Ignore Debug\n"
            "facility.severity — Punkt trennt Einrichtung von Schweregrad"
        ),
        memory_tip   = "Merkhilfe: 0=emerg(höchste Priorität) bis 7=debug(niedrigste)",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.02 — journalctl — systemd Journal
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.02",
        chapter      = 11,
        title        = "journalctl — systemd Journal Mastery",
        mtype        = "DECODE",
        xp           = 100,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'rsyslog ist Vergangenheit auf modernen Systemen.\n"
            " journald ist der Wächter — strukturiert, binär, durchsuchbar.\n"
            " journalctl ist dein Decoder-Ring.\n"
            " Lern die Filter — und du siehst alles.'"
        ),
        why_important = (
            "journalctl ist auf systemd-Systemen der primäre Log-Viewer.\n"
            "LPIC-1 testet journalctl-Filter ausführlich."
        ),
        explanation  = (
            "JOURNALCTL — SYSTEMD JOURNAL:\n\n"
            "GRUNDBEFEHLE:\n"
            "  journalctl                 alle Logs (pager)\n"
            "  journalctl -n 20           letzte 20 Zeilen\n"
            "  journalctl -f              live follow (wie tail -f)\n"
            "  journalctl -r              umgekehrte Reihenfolge\n\n"
            "NACH UNIT FILTERN:\n"
            "  journalctl -u ssh          SSH-Logs\n"
            "  journalctl -u nginx.service  Nginx-Logs\n"
            "  journalctl -u ssh -f       SSH live\n\n"
            "NACH PRIORITÄT FILTERN:\n"
            "  journalctl -p err          nur Fehler (err+)\n"
            "  journalctl -p warning      Warnings+\n"
            "  journalctl -p 3            numerisch (3=err)\n"
            "  journalctl -p 0..3         Bereich emerg bis err\n\n"
            "NACH ZEIT FILTERN:\n"
            "  journalctl --since today\n"
            "  journalctl --since '2089-09-25 08:00:00'\n"
            "  journalctl --since '1 hour ago'\n"
            "  journalctl --until '2089-09-25 12:00:00'\n"
            "  journalctl --since yesterday --until today\n\n"
            "NACH BOOT FILTERN:\n"
            "  journalctl -b              aktueller Boot\n"
            "  journalctl -b -1           vorheriger Boot\n"
            "  journalctl --list-boots    alle Boots anzeigen\n\n"
            "AUSGABE-FORMAT:\n"
            "  journalctl -o json         JSON-Format\n"
            "  journalctl -o json-pretty  schönes JSON\n"
            "  journalctl -o short        Standard\n"
            "  journalctl -o verbose      alle Felder\n\n"
            "JOURNAL VERWALTUNG:\n"
            "  journalctl --disk-usage    Speicherbedarf\n"
            "  journalctl --vacuum-size=500M  auf 500MB reduzieren\n"
            "  journalctl --vacuum-time=30d   älter als 30 Tage löschen\n\n"
            "JOURNAL KONFIGURATION:\n"
            "  /etc/systemd/journald.conf\n"
            "  Storage=persistent         Logs über Neustart speichern\n"
            "  Storage=volatile           nur RAM (/run/log/journal)"
        ),
        syntax       = "journalctl [-u UNIT] [-p LEVEL] [--since TIME] [-f] [-b]",
        example      = (
            "journalctl -u ssh -n 50\n"
            "journalctl -p err --since today\n"
            "journalctl -f\n"
            "journalctl -b\n"
            "journalctl --since '1 hour ago' -p warning\n"
            "journalctl --disk-usage"
        ),
        task_description = "Zeige alle Fehler-Logs (Priorität err und höher) von heute",
        expected_commands = ["journalctl -p err --since today"],
        hint_text    = "journalctl -p err filtert auf Fehler. --since today auf den heutigen Tag.",
        exam_tip     = (
            "HÄUFIGE PRÜFUNGSFRAGEN:\n"
            "  journalctl -b = aktueller Boot\n"
            "  journalctl -b -1 = VORHERIGER Boot\n"
            "  journalctl -p err = Fehler UND schlimmer (0-3)\n"
            "  journalctl -f = live follow (wie tail -f für syslog)"
        ),
        memory_tip   = "Merkhilfe: -u=unit, -p=priority, -f=follow, -b=boot, -n=lines",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.03 — logrotate
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.03",
        chapter      = 11,
        title        = "logrotate — Log-Verwaltung",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: '/var/log füllt sich jeden Tag.\n"
            " Ohne logrotate würde die Festplatte in Wochen voll sein.\n"
            " logrotate komprimiert, archiviert, löscht alte Logs.\n"
            " Automatisch. Täglich. Zuverlässig.'"
        ),
        why_important = (
            "logrotate verhindert volle Festplatten durch unkontrollierte Log-Größen.\n"
            "LPIC-1 testet logrotate-Konfiguration und wichtige Direktiven."
        ),
        explanation  = (
            "LOGROTATE:\n\n"
            "KONFIGURATION:\n"
            "  /etc/logrotate.conf        Haupt-Konfiguration\n"
            "  /etc/logrotate.d/          Service-spezifische Configs\n"
            "  /etc/logrotate.d/nginx     Nginx-Log-Rotation\n"
            "  /etc/logrotate.d/rsyslog   syslog-Rotation\n\n"
            "WICHTIGE DIREKTIVEN:\n"
            "  daily           täglich rotieren\n"
            "  weekly          wöchentlich\n"
            "  monthly         monatlich\n"
            "  rotate 7        7 alte Dateien behalten\n"
            "  compress        komprimieren (gzip)\n"
            "  delaycompress   erst beim nächsten Lauf komprimieren\n"
            "  missingok       kein Fehler wenn Datei fehlt\n"
            "  notifempty      nicht rotieren wenn leer\n"
            "  create 640 root adm  neue Datei mit Rechten erstellen\n"
            "  postrotate      Befehl nach Rotation ausführen\n"
            "    /usr/bin/killall -HUP rsyslogd\n"
            "  endscript\n"
            "  sharedscripts   postrotate nur einmal (nicht pro Datei)\n"
            "  dateext         Datum statt Nummer im Dateinamen\n"
            "  maxsize 100M    rotieren wenn größer als 100MB\n\n"
            "BEISPIEL-KONFIGURATION:\n"
            "  /var/log/nginx/*.log {\n"
            "      daily\n"
            "      rotate 14\n"
            "      compress\n"
            "      delaycompress\n"
            "      missingok\n"
            "      notifempty\n"
            "      sharedscripts\n"
            "      postrotate\n"
            "          nginx -s reload\n"
            "      endscript\n"
            "  }\n\n"
            "MANUELL AUSFÜHREN:\n"
            "  logrotate /etc/logrotate.conf    normal\n"
            "  logrotate -f /etc/logrotate.conf  force (auch wenn nicht nötig)\n"
            "  logrotate -d /etc/logrotate.conf  dry-run (nur anzeigen)"
        ),
        syntax       = "logrotate [-f] [-d] /etc/logrotate.conf",
        example      = (
            "cat /etc/logrotate.conf\n"
            "ls /etc/logrotate.d/\n"
            "cat /etc/logrotate.d/rsyslog\n"
            "logrotate -d /etc/logrotate.conf   # dry-run\n"
            "logrotate -f /etc/logrotate.conf   # force"
        ),
        task_description = "Zeige die logrotate-Konfigurationen in /etc/logrotate.d/",
        expected_commands = ["ls /etc/logrotate.d/"],
        hint_text    = "ls /etc/logrotate.d/ zeigt alle service-spezifischen logrotate-Configs",
        exam_tip     = (
            "PRÜFUNGSTHEMEN:\n"
            "  rotate N = N alte Logs behalten (dann löschen)\n"
            "  compress + delaycompress = erst beim 2. Lauf komprimieren\n"
            "  postrotate/endscript = Befehl nach Rotation (z.B. reload)"
        ),
        memory_tip   = "Merkhilfe: rotate=Anzahl, compress=gzip, daily/weekly/monthly=Häufigkeit",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.04 — Zeitdienste: NTP & timedatectl
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.04",
        chapter      = 11,
        title        = "NTP & timedatectl — Zeitsynchronisation",
        mtype        = "REPAIR",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Log-Timestamps stimmen nicht überein, Ghost.\n"
            " Das Imperium hat NTP manipuliert.\n"
            " Falsche Zeitstempel = unbrauchbare Logs = kein Beweis.\n"
            " Stelle die Zeit richtig — bevor die Logs wertlos werden.'"
        ),
        why_important = (
            "Korrekte Systemzeit ist kritisch für Logs, Zertifikate und Kerberos.\n"
            "LPIC-1 Topic 108.1 testet NTP, timedatectl und Zeitzonen."
        ),
        explanation  = (
            "ZEITDIENSTE UNTER LINUX:\n\n"
            "TIMEDATECTL (systemd):\n"
            "  timedatectl                  aktuelle Zeit und Status\n"
            "  timedatectl set-time '2089-09-25 10:00:00'  Zeit setzen\n"
            "  timedatectl set-timezone Europe/Berlin  Zeitzone\n"
            "  timedatectl list-timezones   alle Zeitzonen\n"
            "  timedatectl set-ntp true     NTP aktivieren\n"
            "  timedatectl set-ntp false    NTP deaktivieren\n\n"
            "DATE — Datum anzeigen/setzen:\n"
            "  date                         aktuelle Zeit\n"
            "  date '+%Y-%m-%d %H:%M:%S'    formatiert\n"
            "  date -s '2089-09-25 10:00'   Zeit setzen (als root)\n"
            "  date -u                      UTC-Zeit\n\n"
            "HWCLOCK — Hardware-Uhr:\n"
            "  hwclock                      Hardware-Uhr lesen\n"
            "  hwclock -s                   System-Zeit von HW-Uhr\n"
            "  hwclock -w                   HW-Uhr von System-Zeit\n"
            "  hwclock --utc                UTC-Modus\n\n"
            "NTP — Network Time Protocol:\n"
            "  /etc/ntp.conf                NTP-Konfiguration\n"
            "  ntpq -p                      NTP-Peers anzeigen\n"
            "  ntpdate pool.ntp.org         einmalig synchronisieren\n\n"
            "SYSTEMD-TIMESYNCD (modern):\n"
            "  /etc/systemd/timesyncd.conf  Konfiguration\n"
            "  systemctl status systemd-timesyncd\n"
            "  timedatectl show-timesync    Sync-Status\n\n"
            "ZEITZONEN:\n"
            "  /etc/timezone                Zeitzone (Debian)\n"
            "  /etc/localtime               Symlink zur Zeitzone\n"
            "  ls -la /etc/localtime        zeigt Zeitzone\n"
            "  ls /usr/share/zoneinfo/      alle Zeitzonen\n"
            "  TZ='Europe/Berlin' date      temporär andere Zeitzone"
        ),
        syntax       = "timedatectl  |  date  |  hwclock  |  timedatectl set-timezone TZ",
        example      = (
            "timedatectl\n"
            "timedatectl set-timezone Europe/Berlin\n"
            "timedatectl set-ntp true\n"
            "date\n"
            "date '+%Y-%m-%d %H:%M:%S'\n"
            "hwclock -w"
        ),
        task_description = "Zeige den aktuellen Zeitdienst-Status mit timedatectl",
        expected_commands = ["timedatectl"],
        hint_text    = "timedatectl zeigt Systemzeit, Zeitzone und NTP-Synchronisationsstatus",
        exam_tip     = (
            "PRÜFUNGSFRAGEN:\n"
            "  Welche Datei enthält die Zeitzone? → /etc/timezone (Debian)\n"
            "  /etc/localtime = Symlink nach /usr/share/zoneinfo/...\n"
            "  hwclock -s = System von Hardware, hwclock -w = Hardware von System"
        ),
        memory_tip   = "Merkhilfe: hwclock -s=system(holt von HW), -w=write(schreibt in HW)",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.05 — cron & crontab
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.05",
        chapter      = 11,
        title        = "cron — Aufgaben automatisieren",
        mtype        = "CONSTRUCT",
        xp           = 110,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Das Backup-Skript lief nie, Ghost.\n"
            " Weil niemand cron konfiguriert hat.\n"
            " crontab -e. Fünf Felder. Ein Befehl.\n"
            " Ab dann läuft es — täglich, wöchentlich, jede Minute.'"
        ),
        why_important = (
            "cron ist das Standard-Job-Scheduling-System.\n"
            "LPIC-1 Topic 107.3 testet crontab-Syntax und System-Cron-Verzeichnisse."
        ),
        explanation  = (
            "CRON — JOB SCHEDULER:\n\n"
            "CRONTAB SYNTAX — 5 Zeit-Felder + Befehl:\n"
            "  MIN  STD  TAG  MON  WOT  BEFEHL\n"
            "  0-59 0-23 1-31 1-12 0-7  /pfad/zum/befehl\n\n"
            "SONDERZEICHEN:\n"
            "  *     jeder Wert\n"
            "  ,     Liste: 1,5,10\n"
            "  -     Bereich: 1-5\n"
            "  /     Schritt: */5 = alle 5\n\n"
            "BEISPIELE:\n"
            "  0 2 * * *        täglich um 02:00 Uhr\n"
            "  */15 * * * *     alle 15 Minuten\n"
            "  0 9 * * 1        jeden Montag um 09:00\n"
            "  0 0 1 * *        am 1. jeden Monats\n"
            "  30 8 * * 1-5     Mo-Fr um 08:30\n"
            "  0 */6 * * *      alle 6 Stunden\n\n"
            "WOCHENTAGE: 0=Sonntag, 1=Montag, ..., 6=Samstag, 7=Sonntag\n\n"
            "CRONTAB BEFEHLE:\n"
            "  crontab -e       eigene Crontab bearbeiten\n"
            "  crontab -l       eigene Crontab anzeigen\n"
            "  crontab -r       eigene Crontab löschen\n"
            "  crontab -u ghost -e  Crontab für ghost (als root)\n"
            "  crontab -u ghost -l  Crontab für ghost anzeigen\n\n"
            "SYSTEM-CRON-VERZEICHNISSE:\n"
            "  /etc/crontab             System-Crontab (mit User-Feld!)\n"
            "  /etc/cron.d/             Cron-Fragmente\n"
            "  /etc/cron.hourly/        stündliche Skripte\n"
            "  /etc/cron.daily/         tägliche Skripte\n"
            "  /etc/cron.weekly/        wöchentliche Skripte\n"
            "  /etc/cron.monthly/       monatliche Skripte\n\n"
            "/etc/crontab FORMAT (mit User-Feld):\n"
            "  MIN STD TAG MON WOT USER BEFEHL\n"
            "  0 2 * * * root /usr/bin/backup.sh\n\n"
            "ZUGRIFFSKONTROLLE:\n"
            "  /etc/cron.allow  nur diese User dürfen crontab nutzen\n"
            "  /etc/cron.deny   diese User dürfen crontab NICHT nutzen\n\n"
            "SONDERWÖRTER:\n"
            "  @reboot          beim Boot\n"
            "  @hourly          = 0 * * * *\n"
            "  @daily           = 0 0 * * *\n"
            "  @weekly          = 0 0 * * 0\n"
            "  @monthly         = 0 0 1 * *\n"
            "  @annually        = 0 0 1 1 *"
        ),
        syntax       = "crontab -e  |  crontab -l  |  MIN STD TAG MON WOT BEFEHL",
        example      = (
            "crontab -l\n"
            "crontab -e\n"
            "# Einträge:\n"
            "0 2 * * * /home/ghost/backup.sh\n"
            "*/5 * * * * /usr/bin/check_disk.sh\n"
            "@reboot /home/ghost/start_monitor.sh\n"
            "cat /etc/crontab"
        ),
        task_description = "Zeige die aktuelle Crontab des Benutzers",
        expected_commands = ["crontab -l"],
        hint_text    = "crontab -l listet alle Cron-Jobs des aktuellen Benutzers",
        exam_tip     = (
            "PRÜFUNGS-FALLE: /etc/crontab hat 6 Felder (mit USER!):\n"
            "  MIN STD TAG MON WOT USER BEFEHL\n"
            "Normale crontab hat nur 5 Zeitfelder + Befehl (kein User)!\n"
            "Wochentag: 0 UND 7 = Sonntag!"
        ),
        memory_tip   = "Merkhilfe: Minuten Stunden Tag Monat Wochentag — 'Manche STarken Telefonieren Mit Worten'",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.06 — at & batch — Einmalige Jobs
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.06",
        chapter      = 11,
        title        = "at & batch — Einmalige Job-Planung",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Der Angriff auf den Zielserver ist für 03:00 Uhr.\n"
            " Kein cron — das ist einmalig, Ghost.\n"
            " at 03:00 — und der Job läuft exakt zur richtigen Zeit.\n"
            " Du kannst schlafen. at nicht.'"
        ),
        why_important = (
            "at ist für einmalige geplante Jobs, cron für wiederkehrende.\n"
            "LPIC-1 testet at, atq, atrm und batch."
        ),
        explanation  = (
            "AT — EINMALIGE JOB-PLANUNG:\n\n"
            "JOBS ERSTELLEN:\n"
            "  at 03:00            Job für 03:00 Uhr heute\n"
            "  at 03:00 tomorrow   morgen um 03:00\n"
            "  at noon             um 12:00\n"
            "  at midnight         um 00:00\n"
            "  at now + 1 hour     in einer Stunde\n"
            "  at now + 30 minutes in 30 Minuten\n"
            "  at 10:00 2089-12-31 am 31.12.2089\n\n"
            "EINGABE: Nach 'at' erscheint at> Prompt:\n"
            "  at> /home/ghost/backup.sh\n"
            "  at> Ctrl+D  (Job einreichen)\n\n"
            "MIT HEREDOC:\n"
            "  at midnight <<'EOF'\n"
            "  /usr/bin/backup.sh\n"
            "  EOF\n\n"
            "JOBS VERWALTEN:\n"
            "  atq                 wartende Jobs anzeigen (= at -l)\n"
            "  at -l               Jobs anzeigen\n"
            "  atrm JOB_NR         Job löschen (= at -d)\n"
            "  at -d JOB_NR        Job löschen\n"
            "  at -c JOB_NR        Job-Inhalt anzeigen\n\n"
            "BATCH — Lastabhängige Ausführung:\n"
            "  batch               läuft wenn Load Average < 1.5\n"
            "  batch < skript.sh   Skript als batch-Job\n\n"
            "ZUGRIFFSKONTROLLE:\n"
            "  /etc/at.allow       nur diese User dürfen at nutzen\n"
            "  /etc/at.deny        diese User dürfen at NICHT nutzen\n\n"
            "AUSGABE:\n"
            "  Ausgabe wird per E-Mail an den User gesendet\n"
            "  (oder in /var/spool/mail/)"
        ),
        syntax       = "at ZEIT  |  atq  |  atrm JOBNR",
        example      = (
            "at now + 1 hour\n"
            "at 02:00 tomorrow\n"
            "atq\n"
            "atrm 3\n"
            "echo '/home/ghost/backup.sh' | at midnight"
        ),
        task_description = "Zeige alle ausstehenden at-Jobs",
        expected_commands = ["atq"],
        hint_text    = "atq zeigt die Warteschlange der geplanten at-Jobs",
        exam_tip     = (
            "at vs cron:\n"
            "  cron  → wiederkehrende Jobs\n"
            "  at    → einmaliger Job zu bestimmter Zeit\n"
            "  batch → einmaliger Job bei niedriger Last\n"
            "atq = at -l (beide zeigen Jobs)"
        ),
        memory_tip   = "Merkhilfe: atq=at-queue, atrm=at-remove",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.07 — systemd Timer Units
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.07",
        chapter      = 11,
        title        = "systemd Timer — Cron der Zukunft",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Cron ist alt, Ghost. Funktioniert.\n"
            " Aber systemd Timer sind der moderne Weg.\n"
            " Integriert ins Journal. Abhängigkeiten. Transient Timers.\n"
            " LPIC-1 will beide kennen.'"
        ),
        why_important = (
            "systemd Timer ersetzen zunehmend cron auf modernen Systemen.\n"
            "LPIC-1 testet Timer-Units, OnCalendar und systemctl timer-Befehle."
        ),
        explanation  = (
            "SYSTEMD TIMER UNITS:\n\n"
            "TIMER ANZEIGEN:\n"
            "  systemctl list-timers         aktive Timer\n"
            "  systemctl list-timers --all   alle inkl. inaktive\n\n"
            "TIMER-UNIT STRUKTUR (2 Dateien):\n\n"
            "  backup.timer:\n"
            "    [Unit]\n"
            "    Description=Backup Timer\n\n"
            "    [Timer]\n"
            "    OnCalendar=daily           täglich um 00:00\n"
            "    OnCalendar=*-*-* 02:00:00  täglich um 02:00\n"
            "    OnCalendar=Mon *-*-* 08:00 jeden Montag\n"
            "    OnBootSec=5min             5 Min nach Boot\n"
            "    OnUnitActiveSec=1h         1 Std nach letztem Lauf\n"
            "    Persistent=true            verpasste Runs nachholen\n\n"
            "    [Install]\n"
            "    WantedBy=timers.target\n\n"
            "  backup.service:\n"
            "    [Unit]\n"
            "    Description=Backup Service\n\n"
            "    [Service]\n"
            "    Type=oneshot\n"
            "    ExecStart=/home/ghost/backup.sh\n\n"
            "AKTIVIEREN:\n"
            "  systemctl enable --now backup.timer\n"
            "  systemctl start backup.timer\n"
            "  systemctl status backup.timer\n\n"
            "TRANSIENT TIMER (ohne Unit-Datei):\n"
            "  systemd-run --on-calendar='02:00' /pfad/befehl\n"
            "  systemd-run --on-active=1h /pfad/befehl\n\n"
            "ONCALENDAR SYNTAX:\n"
            "  daily          = *-*-* 00:00:00\n"
            "  weekly         = Mon *-*-* 00:00:00\n"
            "  monthly        = *-*-01 00:00:00\n"
            "  hourly         = *-*-* *:00:00\n"
            "  minutely       = *-*-* *:*:00"
        ),
        syntax       = "systemctl list-timers  |  systemctl enable --now TIMER.timer",
        example      = (
            "systemctl list-timers\n"
            "systemctl list-timers --all\n"
            "systemctl status apt-daily.timer\n"
            "systemctl enable --now backup.timer\n"
            "systemd-run --on-calendar='02:00' /usr/bin/backup.sh"
        ),
        task_description = "Zeige alle aktiven systemd Timer Units",
        expected_commands = ["systemctl list-timers"],
        hint_text    = "systemctl list-timers zeigt alle aktiven Timer mit nächstem Ausführungszeitpunkt",
        exam_tip     = (
            "CRON vs SYSTEMD TIMER:\n"
            "  Cron: /etc/crontab, crontab -e\n"
            "  Timer: .timer + .service Unit-Dateien\n"
            "  Timer: Logs in journalctl, Cron in /var/log/cron\n"
            "Persistent=true = verpasste Jobs werden nachgeholt"
        ),
        memory_tip   = "Merkhilfe: jeder .timer braucht einen gleichnamigen .service",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.08 — logrotate Konfiguration (tief)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.08",
        chapter      = 11,
        title        = "logrotate Konfiguration — /etc/logrotate.d/",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: '/var/log wächst jeden Tag, Ghost.\n"
            " logrotate läuft still im Hintergrund — täglich, wöchentlich.\n"
            " /etc/logrotate.conf ist der Kern.\n"
            " /etc/logrotate.d/ sind die spezifischen Regeln.\n"
            " Kenn sie — bevor dein Disk voll ist.'"
        ),
        why_important = (
            "logrotate verhindert unkontrolliertes Wachstum von Log-Dateien.\n"
            "LPIC-1 Topic 108.2 testet logrotate-Direktiven und Konfigurationsstruktur."
        ),
        explanation  = (
            "LOGROTATE KONFIGURATION — DETAIL:\n\n"
            "KONFIGURATIONSDATEIEN:\n"
            "  /etc/logrotate.conf         Globale Einstellungen\n"
            "  /etc/logrotate.d/           Service-spezifische Configs\n"
            "  /etc/logrotate.d/rsyslog    syslog-Rotation\n"
            "  /etc/logrotate.d/nginx      Nginx-Rotation\n"
            "  /etc/logrotate.d/dpkg       dpkg-Log-Rotation\n\n"
            "ROTATIONS-INTERVALLE:\n"
            "  daily      täglich (1x pro Tag)\n"
            "  weekly     wöchentlich\n"
            "  monthly    monatlich\n"
            "  yearly     jährlich\n"
            "  size 100M  rotieren wenn Datei > 100MB (unabhängig von Zeit)\n"
            "  minsize 1M erst rotieren wenn > 1MB (kombinierbar mit daily)\n\n"
            "AUFBEWAHRUNG:\n"
            "  rotate 7   7 alte Rotationen aufbewahren, dann löschen\n"
            "  rotate 0   keine alten Logs aufbewahren\n\n"
            "KOMPRESSION:\n"
            "  compress           gzip-Kompression\n"
            "  nocompress         keine Kompression\n"
            "  delaycompress      erst beim nächsten Lauf komprimieren\n"
            "  compresscmd gzip   Kompressionsprogramm\n"
            "  uncompresscmd gunzip\n\n"
            "DATEINAMEN:\n"
            "  dateext            Datum im Dateinamen (z.B. syslog-20890925)\n"
            "  dateformat -%Y%m%d  Datumsformat\n"
            "  extension .gz      Dateierweiterung\n\n"
            "FEHLERBEHANDLUNG:\n"
            "  missingok    kein Fehler wenn Log-Datei fehlt\n"
            "  notifempty   nicht rotieren wenn Log leer ist\n\n"
            "NACH-ROTATION-HOOKS:\n"
            "  postrotate\n"
            "    /usr/bin/killall -HUP rsyslogd\n"
            "  endscript\n"
            "  sharedscripts  Hooks nur einmal ausführen (nicht pro Datei)\n\n"
            "MANUELL AUSFÜHREN:\n"
            "  logrotate /etc/logrotate.conf    normaler Lauf\n"
            "  logrotate -f /etc/logrotate.conf  erzwingen\n"
            "  logrotate -d /etc/logrotate.conf  dry-run (Simulation)\n"
            "  logrotate -v /etc/logrotate.conf  verbose"
        ),
        syntax       = "logrotate [-d] [-f] [-v] /etc/logrotate.conf",
        example      = (
            "cat /etc/logrotate.conf\n"
            "ls /etc/logrotate.d/\n"
            "cat /etc/logrotate.d/rsyslog\n"
            "logrotate -d /etc/logrotate.conf   # dry-run\n"
            "logrotate -v /etc/logrotate.conf   # verbose"
        ),
        task_description = "Zeige alle Konfigurationsdateien in /etc/logrotate.d/",
        expected_commands = ["ls /etc/logrotate.d/"],
        hint_text    = "ls /etc/logrotate.d/ listet service-spezifische logrotate-Configs",
        exam_tip     = (
            "PRÜFUNGSTHEMEN:\n"
            "  size N = nach Größe rotieren | daily/weekly/monthly = Zeitbasiert\n"
            "  rotate N = N alte Rotationen aufheben\n"
            "  compress + delaycompress = erst beim zweiten Lauf komprimieren\n"
            "  missingok = kein Fehler wenn Datei fehlt\n"
            "  postrotate/endscript = Hooks (z.B. rsyslogd reload)"
        ),
        memory_tip   = "Merkhilfe: logrotate.d = Einzelkonfigs pro Service, logrotate.conf = globale Basis",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.09 — journald Konfiguration
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.09",
        chapter      = 11,
        title        = "journald Konfiguration — /etc/systemd/journald.conf",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA_Z3R0",
        story        = (
            "ZARA_Z3R0: 'Das Journal frisst Disk-Space, Ghost.\n"
            " Ohne Konfiguration wächst /var/log/journal unkontrolliert.\n"
            " journald.conf setzt Grenzen.\n"
            " MaxDiskUsage. Storage. Vacuum.\n"
            " Kenn die Parameter — und das Journal bleibt unter Kontrolle.'"
        ),
        why_important = (
            "journald konfigurieren ist essenziell für Server-Betrieb.\n"
            "LPIC-1 testet journald.conf-Parameter, Storage-Optionen und vacuum-Befehle."
        ),
        explanation  = (
            "JOURNALD KONFIGURATION:\n\n"
            "KONFIGURATIONSDATEI:\n"
            "  /etc/systemd/journald.conf    Hauptkonfiguration\n"
            "  /etc/systemd/journald.conf.d/ Drop-in-Verzeichnis\n\n"
            "WICHTIGE PARAMETER:\n\n"
            "Storage= — wo Logs gespeichert werden:\n"
            "  Storage=auto       /var/log/journal wenn vorhanden (Standard)\n"
            "  Storage=persistent immer /var/log/journal (persistent über Reboots)\n"
            "  Storage=volatile   nur /run/log/journal (RAM, flüchtig)\n"
            "  Storage=none       kein Logging durch journald\n\n"
            "Speicherbegrenzung:\n"
            "  MaxDiskUsage=500M   max. Gesamtgröße\n"
            "  MinDiskAvail=100M   min. freier Speicher\n"
            "  MaxFileSec=1month   max. Alter einer Journal-Datei\n"
            "  MaxRetentionSec=2week  max. Aufbewahrungszeit\n"
            "  MaxFiles=100        max. Anzahl Journal-Dateien\n\n"
            "Journal-Dateigröße:\n"
            "  SystemMaxFileSize=32M  max. Größe einer System-Journal-Datei\n"
            "  RuntimeMaxFileSize=8M  max. Größe im RAM-Journal\n\n"
            "Kompression & Sicherheit:\n"
            "  Compress=yes        Kompression aktivieren (Standard)\n"
            "  ForwardToSyslog=no  nicht an rsyslog weiterleiten\n"
            "  ForwardToWall=yes   kritische Meldungen an alle Terminals\n\n"
            "JOURNAL VACUUM (Bereinigung):\n"
            "  journalctl --vacuum-size=500M    auf max. 500 MB reduzieren\n"
            "  journalctl --vacuum-time=30d     Logs älter als 30 Tage löschen\n"
            "  journalctl --vacuum-files=10     auf 10 Dateien reduzieren\n"
            "  journalctl --verify              Journal-Integrität prüfen\n"
            "  journalctl --disk-usage          aktuellen Speicherverbrauch anzeigen\n\n"
            "JOURNAL PERSISTENT MACHEN:\n"
            "  mkdir -p /var/log/journal\n"
            "  systemd-tmpfiles --create --prefix /var/log/journal\n"
            "  systemctl restart systemd-journald"
        ),
        syntax       = "journalctl --disk-usage  |  journalctl --vacuum-size=SIZE",
        example      = (
            "cat /etc/systemd/journald.conf\n"
            "journalctl --disk-usage\n"
            "journalctl --vacuum-size=500M\n"
            "journalctl --vacuum-time=30d\n"
            "journalctl --verify"
        ),
        task_description = "Zeige den aktuellen Journal-Speicherverbrauch",
        expected_commands = ["journalctl --disk-usage"],
        hint_text    = "journalctl --disk-usage zeigt wie viel Speicher das Journal belegt",
        exam_tip     = (
            "PRÜFUNGSTHEMEN:\n"
            "  Storage=persistent = /var/log/journal (über Reboots)\n"
            "  Storage=volatile   = /run/log/journal (RAM, verloren bei Reboot)\n"
            "  MaxDiskUsage       = max. Gesamtgröße\n"
            "  --vacuum-size/time = Bereinigung der Journal-Datenbank"
        ),
        memory_tip   = "Merkhilfe: persistent=Platte bleibt, volatile=RAM=flüchtig",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.10 — Systemd-Timer vs Cron (tief)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.10",
        chapter      = 11,
        title        = "Systemd-Timer vs Cron — .timer Units tief",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Cron ist robust, Ghost. Funktioniert seit Jahrzehnten.\n"
            " Aber systemd Timer sind integriert ins Journal.\n"
            " Sie kennen Abhängigkeiten. Sie tracken verpasste Läufe.\n"
            " OnCalendar= ist die neue Cron-Syntax.\n"
            " systemctl list-timers zeigt alles.'"
        ),
        why_important = (
            "Systemd Timer ersetzen zunehmend cron auf modernen Linux-Systemen.\n"
            "LPIC-1 testet .timer Unit-Struktur, OnCalendar-Syntax und systemctl-Befehle."
        ),
        explanation  = (
            "SYSTEMD TIMER — TIEFES WISSEN:\n\n"
            "TIMER-TYPEN:\n"
            "  Monotonic Timers — relativ zur Zeit:\n"
            "    OnBootSec=5min       5 Min nach Boot\n"
            "    OnActiveSec=1h       1 Std nach Timer-Aktivierung\n"
            "    OnUnitActiveSec=2h   2 Std nach letztem Service-Start\n"
            "    OnUnitInactiveSec=1h 1 Std nach letztem Service-Stop\n\n"
            "  Realtime Timers (Calendar) — absolut:\n"
            "    OnCalendar=daily           täglich um 00:00\n"
            "    OnCalendar=weekly          wöchentlich (Montag)\n"
            "    OnCalendar=monthly         am 1. jeden Monats\n"
            "    OnCalendar=*-*-* 02:30:00  täglich um 02:30\n"
            "    OnCalendar=Mon,Wed,Fri *-*-* 08:00:00  Mo/Mi/Fr\n"
            "    OnCalendar=*-*-* *:00:00   jede volle Stunde\n"
            "    OnCalendar=*-*-* *:*/15:00 alle 15 Minuten\n\n"
            "TIMER UNIT STRUKTUR:\n"
            "  /etc/systemd/system/backup.timer:\n"
            "    [Unit]\n"
            "    Description=Tägliches Backup\n"
            "    [Timer]\n"
            "    OnCalendar=*-*-* 02:00:00\n"
            "    Persistent=true\n"
            "    RandomizedDelaySec=300\n"
            "    [Install]\n"
            "    WantedBy=timers.target\n\n"
            "  /etc/systemd/system/backup.service:\n"
            "    [Unit]\n"
            "    Description=Backup-Service\n"
            "    [Service]\n"
            "    Type=oneshot\n"
            "    ExecStart=/usr/local/bin/backup.sh\n\n"
            "WICHTIGE OPTIONEN:\n"
            "  Persistent=true      verpasste Läufe nachholen (nach Downtime)\n"
            "  RandomizedDelaySec=N zufällige Verzögerung (Last verteilen)\n"
            "  AccuracySec=1min     Genauigkeit (Standard: 1 Min)\n"
            "  Unit=anderer.service anderen Service starten\n\n"
            "TIMER VERWALTEN:\n"
            "  systemctl list-timers           aktive Timer\n"
            "  systemctl list-timers --all     alle Timer\n"
            "  systemctl enable --now backup.timer\n"
            "  systemctl status backup.timer\n"
            "  systemctl start backup.timer    manuell auslösen\n\n"
            "CRON vs TIMER VERGLEICH:\n"
            "  Cron:  0 2 * * * /pfad/script.sh\n"
            "  Timer: OnCalendar=*-*-* 02:00:00\n"
            "  Timer-Vorteil: Logs in journalctl, Deps, Persistent, keine Crontab-Syntax\n"
            "  Cron-Vorteil: Einfacher, universell, kein systemd nötig"
        ),
        syntax       = "systemctl list-timers  |  OnCalendar=ZEITAUSDRUCK",
        example      = (
            "systemctl list-timers\n"
            "systemctl list-timers --all\n"
            "systemctl status apt-daily.timer\n"
            "systemctl enable --now backup.timer\n"
            "systemd-analyze calendar '*-*-* 02:00:00'   # OnCalendar prüfen"
        ),
        task_description = "Liste alle aktiven systemd Timer Units auf",
        expected_commands = ["systemctl list-timers"],
        hint_text    = "systemctl list-timers zeigt alle aktiven Timer mit nächstem Auslösezeitpunkt",
        exam_tip     = (
            "ONCALENDAR WICHTIGE WERTE:\n"
            "  daily   = *-*-* 00:00:00\n"
            "  weekly  = Mon *-*-* 00:00:00\n"
            "  monthly = *-*-01 00:00:00\n"
            "  hourly  = *-*-* *:00:00\n"
            "Persistent=true = verpasste Jobs nachholen (wichtig nach Downtime)"
        ),
        memory_tip   = "Merkhilfe: Timer ohne .service gibt es nicht — immer 2 Unit-Dateien!",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.11 — at & batch (tief)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.11",
        chapter      = 11,
        title        = "at & batch — Einmalige Jobs & Last-abhängige Ausführung",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "ZARA_Z3R0",
        story        = (
            "ZARA_Z3R0: 'Die Operation startet um 14:00, Ghost.\n"
            " Einmalig. Kein cron nötig.\n"
            " at 14:00 — und der Befehl wartet.\n"
            " atq zeigt die Warteschlange.\n"
            " atrm löscht den Job falls nötig.\n"
            " batch läuft wenn die Last niedrig ist.'"
        ),
        why_important = (
            "at für einmalige Jobs, batch für lastabhängige Ausführung.\n"
            "LPIC-1 Topic 107.3 testet at, atq, atrm, batch und Zugriffskontrolle."
        ),
        explanation  = (
            "AT — EINMALIGE JOBS PLANEN:\n\n"
            "ZEITANGABEN:\n"
            "  at 14:00              heute um 14:00\n"
            "  at 14:00 tomorrow     morgen um 14:00\n"
            "  at 14:00 2089-12-31   am bestimmten Datum\n"
            "  at now + 30 minutes   in 30 Minuten\n"
            "  at now + 2 hours      in 2 Stunden\n"
            "  at noon               um 12:00\n"
            "  at midnight           um 00:00\n"
            "  at teatime            um 16:00\n\n"
            "JOBS ERSTELLEN:\n"
            "  at 14:00                     interaktiver Prompt\n"
            "  at> /home/ghost/attack.sh    Befehl eingeben\n"
            "  at> ^D                       Ctrl+D zum Speichern\n\n"
            "  echo '/home/ghost/script.sh' | at midnight\n"
            "  at midnight < script.sh      Datei als at-Job\n\n"
            "JOBS VERWALTEN:\n"
            "  atq                  Warteschlange anzeigen (= at -l)\n"
            "  at -l                Warteschlange anzeigen (= atq)\n"
            "  atrm 3               Job Nr. 3 löschen (= at -d 3)\n"
            "  at -d 3              Job Nr. 3 löschen (= atrm 3)\n"
            "  at -c 3              Inhalt von Job Nr. 3 anzeigen\n\n"
            "AUSGABE:\n"
            "  Ausgabe wird per Mail an User geschickt\n"
            "  at -m: Mail auch bei keiner Ausgabe\n"
            "  Umleitung in Datei: /pfad/cmd > /tmp/output 2>&1\n\n"
            "BATCH — LASTABHÄNGIGE AUSFÜHRUNG:\n"
            "  batch                  läuft wenn Load Average < 0.8\n"
            "  batch < script.sh      Skript als batch-Job\n"
            "  echo 'cmd' | batch     Befehl als batch-Job\n"
            "  atd-Konfiguration: /etc/at.conf, /etc/atd.conf\n\n"
            "ZUGRIFFSKONTROLLE:\n"
            "  /etc/at.allow    nur diese User dürfen at nutzen\n"
            "                   (wenn vorhanden → /etc/at.deny wird ignoriert)\n"
            "  /etc/at.deny     diese User dürfen at NICHT nutzen\n"
            "  Logik: at.allow vorhanden → nur darin genannte User\n"
            "         at.allow nicht vorhanden → at.deny wird geprüft\n"
            "         beide fehlen → nur root darf at nutzen"
        ),
        syntax       = "at ZEIT  |  atq  |  atrm JOBNR  |  at -c JOBNR",
        example      = (
            "at 14:00\n"
            "at now + 1 hour\n"
            "echo '/home/ghost/backup.sh' | at midnight\n"
            "atq\n"
            "atrm 3\n"
            "at -c 2         # Job-Inhalt anzeigen\n"
            "echo 'make -j4' | batch"
        ),
        task_description = "Zeige alle wartenden at-Jobs mit atq",
        expected_commands = ["atq"],
        hint_text    = "atq (at queue) zeigt alle geplanten einmaligen Jobs",
        exam_tip     = (
            "PRÜFUNGS-MERKSÄTZE:\n"
            "  at   = einmaliger Job zu festgelegter Zeit\n"
            "  batch= einmaliger Job bei niedriger Systemlast\n"
            "  cron = wiederkehrender Job (Zeitplan)\n"
            "  atq = at -l | atrm N = at -d N\n"
            "/etc/at.allow hat Vorrang vor /etc/at.deny!"
        ),
        memory_tip   = "Merkhilfe: atq=at-queue anzeigen, atrm=at-remove löschen",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.12 — /etc/cron.allow & /etc/cron.deny
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.12",
        chapter      = 11,
        title        = "cron.allow & cron.deny — Cron-Zugriffskontrolle",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Nicht jeder darf Cron-Jobs erstellen, Ghost.\n"
            " Das Imperium kontrolliert wer crontab -e aufrufen darf.\n"
            " /etc/cron.allow: Whitelist.\n"
            " /etc/cron.deny: Blacklist.\n"
            " Gleiche Logik gilt für at mit at.allow/at.deny.'"
        ),
        why_important = (
            "Cron-Zugriffskontrolle ist ein LPIC-1 Prüfungsthema (Topic 107.3).\n"
            "Verstehen welche Datei Vorrang hat und die genaue Logik."
        ),
        explanation  = (
            "CRON ZUGRIFFSKONTROLLE:\n\n"
            "DATEIEN:\n"
            "  /etc/cron.allow     Whitelist: nur diese User dürfen crontab nutzen\n"
            "  /etc/cron.deny      Blacklist: diese User dürfen crontab NICHT nutzen\n\n"
            "LOGIK (Priorität):\n"
            "  1. Wenn /etc/cron.allow existiert:\n"
            "     → Nur User in cron.allow dürfen crontab nutzen\n"
            "     → cron.deny wird IGNORIERT\n"
            "     → root ist immer erlaubt (auch wenn nicht in allow)\n\n"
            "  2. Wenn /etc/cron.allow NICHT existiert:\n"
            "     → cron.deny wird geprüft\n"
            "     → User in cron.deny dürfen crontab NICHT nutzen\n"
            "     → alle anderen User dürfen\n\n"
            "  3. Wenn BEIDE nicht existieren:\n"
            "     → System-abhängig: oft nur root, oder alle User\n\n"
            "FORMAT:\n"
            "  Eine Zeile pro Benutzername:\n"
            "    ghost\n"
            "    operator\n"
            "    admin\n\n"
            "SYSTEM CRON-VERZEICHNISSE (immer zugänglich):\n"
            "  /etc/cron.d/         System-Jobs (root/cron-Daemon)\n"
            "  /etc/cron.hourly/    stündliche Skripte\n"
            "  /etc/cron.daily/     tägliche Skripte\n"
            "  /etc/cron.weekly/    wöchentliche Skripte\n"
            "  /etc/cron.monthly/   monatliche Skripte\n"
            "  → Diese Verzeichnisse sind nicht durch cron.allow/deny betroffen!\n\n"
            "GLEICHE LOGIK BEI AT:\n"
            "  /etc/at.allow   → /etc/at.deny nach gleicher Prioritätsregel\n\n"
            "PRÜFEN WER CRON NUTZEN DARF:\n"
            "  cat /etc/cron.allow\n"
            "  cat /etc/cron.deny\n"
            "  ls -la /etc/cron.allow /etc/cron.deny 2>/dev/null"
        ),
        syntax       = "cat /etc/cron.allow  |  cat /etc/cron.deny",
        example      = (
            "cat /etc/cron.allow\n"
            "cat /etc/cron.deny\n"
            "echo 'ghost' >> /etc/cron.allow\n"
            "ls /etc/cron.hourly/\n"
            "ls /etc/cron.daily/\n"
            "ls /etc/cron.weekly/"
        ),
        task_description = "Zeige den Inhalt von /etc/cron.deny (falls vorhanden)",
        expected_commands = ["cat /etc/cron.deny"],
        hint_text    = "cat /etc/cron.deny zeigt die Liste der gesperrten Cron-Benutzer",
        exam_tip     = (
            "PRÜFUNGS-MERKSÄTZE:\n"
            "  cron.allow VORHANDEN → nur darin genannte User (cron.deny ignoriert)\n"
            "  cron.allow NICHT vorhanden → cron.deny wird geprüft\n"
            "  root ist IMMER erlaubt\n"
            "  GLEICHE LOGIK: at.allow / at.deny für den at-Befehl"
        ),
        memory_tip   = "Merkhilfe: ALLOW geht vor DENY — Whitelist schlägt Blacklist",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.13 — auditd: Linux Audit System
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.13",
        chapter      = 11,
        title        = "auditd — Kernel Audit Logging",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Ghost. Root-Login um 3 Uhr morgens.\n"
            " auditd hat alles aufgezeichnet.\n"
            " Kernel-Ebene. Nicht umgehbar.'"
        ),
        why_important = (
            "auditd zeichnet sicherheitsrelevante Kernel-Ereignisse auf.\n"
            "Es ist nicht umgehbar — selbst root kann es nicht austricksen."
        ),
        explanation  = (
            "AUDITD — LINUX KERNEL AUDIT:\n\n"
            "  systemctl status auditd\n"
            "  auditctl -l          Aktive Regeln anzeigen\n"
            "  auditctl -s          Audit-Systemstatus\n\n"
            "REGELN:\n"
            "  auditctl -w /etc/passwd -p rwa -k passwd_changes\n"
            "  auditctl -w /var/log -p rwa -k logfile_access\n"
            "  -w=watch path, -p=permissions(r/w/x/a), -k=key\n\n"
            "SUCHE:\n"
            "  ausearch -k passwd_changes\n"
            "  ausearch -ua 0              Alle root-Ereignisse\n"
            "  ausearch --start today\n\n"
            "BERICHTE:\n"
            "  aureport --summary\n"
            "  aureport --auth\n"
            "  aureport --file\n\n"
            "CONFIG: /etc/audit/auditd.conf | /etc/audit/rules.d/"
        ),
        syntax       = "auditctl -w /pfad -p rwa -k schlüssel",
        example      = "auditctl -l && ausearch --start today | tail -20",
        task_description = "Zeige aktive Audit-Regeln mit auditctl -l",
        expected_commands = ["auditctl -l"],
        hint_text    = "auditctl -l zeigt alle aktiven Audit-Regeln",
        quiz_questions = [
            QuizQuestion(
                question = "Welches Tool durchsucht das Linux Audit Log?",
                options  = [
                    "ausearch",
                    "auditctl",
                    "journalctl",
                    "aureport",
                ],
                correct  = 0,
                explanation = "ausearch durchsucht /var/log/audit/audit.log nach Keys, UIDs, Programmen etc.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "auditctl=Regeln setzen | ausearch=Log durchsuchen | aureport=Zusammenfassung",
        memory_tip   = "CTL=Control (setzen) | SEARCH=Suchen | REPORT=Berichten",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.14 — Remote Syslog: rsyslog Forwarding
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.14",
        chapter      = 11,
        title        = "Remote Syslog: rsyslog Forwarding",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Logs lokal? Wer bricht ein, löscht die Logs.\n"
            " Zentrales Log-Management. rsyslog forwarded in Echtzeit.\n"
            " An den Log-Server. Unveränderlich. Forensik-sicher.'"
        ),
        why_important = (
            "Zentrales Log-Management ist Security Best Practice.\n"
            "rsyslog kann Logs via TCP/UDP an einen zentralen Server senden."
        ),
        explanation  = (
            "RSYSLOG REMOTE FORWARDING:\n\n"
            "CLIENT KONFIGURATION (/etc/rsyslog.conf):\n"
            "  *.* @192.168.1.100         UDP (@ = UDP)\n"
            "  *.* @@192.168.1.100        TCP (@@ = TCP, zuverlässiger)\n"
            "  *.* @@192.168.1.100:10514  Custom Port\n"
            "  *.* @@logserver.intern     Hostname\n\n"
            "SERVER KONFIGURATION:\n"
            "  # UDP aktivieren:\n"
            "  $ModLoad imudp\n"
            "  $UDPServerRun 514\n"
            "  # TCP aktivieren:\n"
            "  $ModLoad imtcp\n"
            "  $InputTCPServerRun 514\n\n"
            "FILTER FÜR FORWARDING:\n"
            "  auth,authpriv.* @@logserver\n"
            "  kern.crit @@logserver\n\n"
            "TEMPLATE FÜR STRUKTURIERTE LOGS:\n"
            "  $template RemoteLogs,\"/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log\"\n"
            "  *.* ?RemoteLogs"
        ),
        syntax       = "*.* @@logserver.intern  (in /etc/rsyslog.conf)",
        example      = "echo '*.* @@192.168.1.100:514' >> /etc/rsyslog.d/forward.conf && systemctl restart rsyslog",
        task_description = "Zeige rsyslog-Konfiguration mit cat /etc/rsyslog.conf | head -30",
        expected_commands = ["cat /etc/rsyslog.conf"],
        hint_text    = "cat /etc/rsyslog.conf | head -30 zeigt die rsyslog-Haupt-Konfiguration",
        quiz_questions = [
            QuizQuestion(
                question = "Was bedeutet `@@` in einer rsyslog-Forwarding-Regel?",
                options  = [
                    "TCP-Forwarding (zuverlässig)",
                    "UDP-Forwarding",
                    "Lokale Datei",
                    "Verschlüsseltes Forwarding",
                ],
                correct  = 0,
                explanation = "@@ = TCP (zuverlässig, Bestätigung). @ = UDP (schnell, kein ACK). TCP für Production.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "@ = UDP | @@ = TCP. TCP für Production empfohlen. Port 514 ist Standard-Syslog-Port.",
        memory_tip   = "Doppelt (@@ ) = doppelt sicher = TCP. Einmal (@) = einfach = UDP.",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.15 — MTA-Grundlagen: Postfix & Mail
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.15",
        chapter      = 11,
        title        = "MTA-Grundlagen — Postfix & Mail-System",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Ein Skript schickt keinen Status-Report, Ghost.\n"
            " Weil kein MTA läuft. Mail Transfer Agent.\n"
            " Cron-Jobs, System-Alerts, Root-Mails — alles braucht einen MTA.'"
        ),
        why_important = (
            "LPIC-1 Topic 108.3: MTA basics. Jeder Linux-Server benötigt\n"
            "einen MTA für System-Mails von cron, fail2ban, etc."
        ),
        explanation  = (
            "MTA KONZEPTE:\n\n"
            "  MTA = Mail Transfer Agent (sendet/empfängt zwischen Servern)\n"
            "  MDA = Mail Delivery Agent (legt Mail in Mailbox ab)\n"
            "  MUA = Mail User Agent (E-Mail-Client)\n\n"
            "BEKANNTE MTAS:\n"
            "  Postfix   = Moderner Standard (Debian/Ubuntu)\n"
            "  Sendmail  = Klassisch, komplex (historisch)\n"
            "  Exim      = Debian-Standard früher\n"
            "  Nullmailer= Nur Weiterleitung\n\n"
            "GRUNDBEFEHLE:\n"
            "  postfix status            Postfix-Status\n"
            "  mailq                     Mail-Warteschlange anzeigen\n"
            "  mail -s 'Betreff' user@host  Mail senden\n"
            "  echo 'Test' | mail -s 'Test' root\n\n"
            "KONFIG:\n"
            "  /etc/postfix/main.cf       Haupt-Konfiguration\n"
            "  /etc/aliases               System-Aliases\n"
            "  newaliases                 Alias-DB neu bauen\n"
            "  /var/log/mail.log          Mail-Log"
        ),
        syntax       = "echo 'Nachricht' | mail -s 'Betreff' empfaenger",
        example      = "echo 'Backup fertig' | mail -s 'Nightly Backup' root && mailq",
        task_description = "Zeige Mail-Warteschlange mit mailq",
        expected_commands = ["mailq"],
        hint_text    = "mailq zeigt die Postfix Mail-Warteschlange",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `newaliases`?",
                options  = [
                    "Baut die /etc/aliases.db Hash-Datenbank aus /etc/aliases neu",
                    "Erstellt neue E-Mail-Konten",
                    "Listet alle Mail-Aliases auf",
                    "Sendet eine Test-Mail",
                ],
                correct  = 0,
                explanation = "newaliases liest /etc/aliases und baut die binäre .db-Datei. Ohne dies wirken Änderungen nicht.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "newaliases NACH /etc/aliases ändern PFLICHT! mailq = Queue anzeigen. /var/log/mail.log",
        memory_tip   = "newaliases = neue Alias-Datenbank bauen. Ohne den Befehl: Änderungen ignoriert.",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.16 — Mail-Aliase & Weiterleitung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.16",
        chapter      = 11,
        title        = "Mail-Aliase & Weiterleitung",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Root bekommt Hunderte System-Mails.\n"
            " /etc/aliases leitet root an eine echte Mailbox.\n"
            " ~/.forward für persönliche Weiterleitung.'"
        ),
        why_important = (
            "Mail-Aliases ermöglichen System-Mails an reale Benutzer\n"
            "oder externe Adressen weiterzuleiten. LPIC-1 Topic 108.3."
        ),
        explanation  = (
            "/ETC/ALIASES:\n\n"
            "  SYNTAX: alias: empfaenger[, empfaenger2]\n\n"
            "  root:     ghost              root-Mail an ghost\n"
            "  webmaster: root, ghost       an mehrere Empfänger\n"
            "  devnull:  /dev/null          Mail wegwerfen\n"
            "  backup:   |/usr/bin/backup-script  an Programm pipen\n\n"
            "NACH ÄNDERUNG:\n"
            "  newaliases                   Hash-DB neu bauen\n"
            "  sendmail -bi                 Alternative\n\n"
            "~/.FORWARD:\n"
            "  echo 'user@extern.de' > ~/.forward\n"
            "  → Alle Mails dieses Users weiterleiten\n"
            "  Leerzeile = Kopie behalten + weiterleiten\n\n"
            "MAIL LESEN:\n"
            "  cat /var/mail/ghost          Direkt lesen\n"
            "  mail                         mail-Programm\n"
            "  mutt                         TUI-Mail-Client"
        ),
        syntax       = "alias: empfaenger  (in /etc/aliases), dann: newaliases",
        example      = "grep '^root:' /etc/aliases && echo 'root: ghost' >> /etc/aliases && newaliases",
        task_description = "Zeige /etc/aliases mit cat /etc/aliases",
        expected_commands = ["cat /etc/aliases"],
        hint_text    = "cat /etc/aliases zeigt alle System-Mail-Aliases",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Datei leitet Mails für einen einzelnen User weiter?",
                options  = [
                    "~/.forward",
                    "/etc/aliases",
                    "/etc/mail.forward",
                    "/etc/postfix/virtual",
                ],
                correct  = 0,
                explanation = "~/.forward im Home-Verzeichnis. /etc/aliases gilt systemweit für alle.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "newaliases nach /etc/aliases PFLICHT. ~/.forward = User-eigene Weiterleitung.",
        memory_tip   = "/etc/aliases = systemweit. ~/.forward = persönlich. newaliases = aktivieren.",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.17 — journald Persistenz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.17",
        chapter      = 11,
        title        = "journald Persistenz — Logs dauerhaft speichern",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Nach dem Reboot sind alle Logs weg, Ghost.\n"
            " journald speichert standardmäßig nur im RAM.\n"
            " Storage=persistent ändert das.\n"
            " /var/log/journal — dein digitales Gedächtnis.'"
        ),
        why_important = (
            "journald Persistenz ist LPIC-1 Topic 108.2 Prüfungsstoff.\n"
            "Ohne persistente Logs: keine Post-Mortem-Analyse nach Crashes.\n"
            "Storage-Optionen und Größenlimits kommen in der Prüfung vor."
        ),
        explanation  = (
            "JOURNALD PERSISTENZ — /ETC/SYSTEMD/JOURNALD.CONF:\n\n"
            "Storage-Optionen:\n"
            "  volatile    → nur RAM (/run/log/journal/) — verloren nach Reboot\n"
            "  persistent  → Disk (/var/log/journal/) — überlebt Reboot\n"
            "  auto        → persistent wenn /var/log/journal/ existiert (Standard)\n"
            "  none        → gar kein Logging\n\n"
            "GRÖSSEN-LIMITS:\n"
            "  SystemMaxUse=500M      max. Disk-Nutzung\n"
            "  SystemKeepFree=1G      freier Speicher auf Partition\n"
            "  MaxRetentionSec=1month Maximales Alter\n"
            "  MaxFileSec=1week       Rotations-Intervall\n\n"
            "JOURNAL-VERZEICHNISSE:\n"
            "  /run/log/journal/      flüchtig (RAM)\n"
            "  /var/log/journal/      persistent (Disk)\n\n"
            "AKTIVIEREN:\n"
            "  mkdir -p /var/log/journal\n"
            "  systemd-tmpfiles --create --prefix /var/log/journal\n"
            "  systemctl restart systemd-journald\n\n"
            "JOURNAL-INFO:\n"
            "  journalctl --disk-usage   genutzten Speicher anzeigen\n"
            "  journalctl --vacuum-size=100M  auf 100M reduzieren\n"
            "  journalctl --vacuum-time=7d    älter als 7 Tage löschen"
        ),
        syntax       = "journalctl --disk-usage  |  journalctl --vacuum-size=SIZE",
        example      = (
            "journalctl --disk-usage          # aktueller Speicherverbrauch\n"
            "journalctl --vacuum-size=200M    # auf 200MB reduzieren\n"
            "journalctl --vacuum-time=30d     # älter als 30 Tage löschen\n"
            "cat /etc/systemd/journald.conf   # Konfiguration anzeigen\n"
            "ls /var/log/journal/             # persistente Logs"
        ),
        task_description = "Zeige den Disk-Verbrauch des systemd-Journals",
        expected_commands = ["journalctl --disk-usage"],
        hint_text    = "journalctl --disk-usage zeigt wie viel Speicher das Journal belegt",
        quiz_questions = [
            QuizQuestion(
                question   = "Welche journald.conf Storage-Option speichert Logs dauerhaft auf Disk?",
                options    = [
                    "volatile",
                    "persistent",
                    "permanent",
                    "disk",
                ],
                correct    = 1,
                explanation = (
                    "Storage=persistent speichert in /var/log/journal/.\n"
                    "Storage=volatile speichert nur im RAM (/run/log/journal/).\n"
                    "Nach Storage=persistent: mkdir /var/log/journal + restart journald."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "In welchem Verzeichnis speichert journald Logs wenn Storage=volatile gesetzt ist?",
                options    = [
                    "/var/log/journal/",
                    "/tmp/journal/",
                    "/run/log/journal/",
                    "/sys/log/journal/",
                ],
                correct    = 2,
                explanation = (
                    "/run/log/journal/ ist das RAM-basierte Journal-Verzeichnis.\n"
                    "Es liegt auf dem tmpfs und wird beim Neustart geleert.\n"
                    "/var/log/journal/ ist das persistente Verzeichnis (Storage=persistent)."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 journald:\n"
            "  Storage=persistent → /var/log/journal/\n"
            "  Storage=volatile → /run/log/journal/ (RAM)\n"
            "  journalctl --disk-usage → Speicherverbrauch\n"
            "  --vacuum-size / --vacuum-time → aufräumen"
        ),
        memory_tip   = "persistent = Festplatte überlebt. volatile = RAM, weg nach Reboot.",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.18 — Log-Analyse: grep/awk auf Logs, lastlog, last, wtmp, btmp
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.18",
        chapter      = 11,
        title        = "Log-Analyse — last, lastlog, wtmp & faillog",
        mtype        = "DECODE",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Jemand war auf dem System, Ghost.\n"
            " Wer hat sich wann eingeloggt? last zeigt es.\n"
            " lastlog zeigt den letzten Login jedes Users.\n"
            " faillog zeigt fehlgeschlagene Versuche.\n"
            " Die Beweise liegen in /var/log/wtmp und /var/log/btmp.'"
        ),
        why_important = (
            "Log-Analyse ist Kernkompetenz für Sysadmins und Security-Audits.\n"
            "LPIC-1 Topic 108.2 prüft last, lastlog, faillog und wtmp/btmp.\n"
            "Diese Befehle decken unbefugte Zugriffsversuche auf."
        ),
        explanation  = (
            "LOGIN-LOGS ANALYSIEREN:\n\n"
            "last — Login-Verlauf:\n"
            "  last                   alle Login/Logout-Ereignisse\n"
            "  last ghost             Logins für User 'ghost'\n"
            "  last -n 20             letzte 20 Ereignisse\n"
            "  last reboot            alle System-Reboots\n"
            "  last -F                vollständige Zeitangaben\n"
            "  Quelle: /var/log/wtmp  (binäre Datenbank)\n\n"
            "lastlog — letzter Login pro User:\n"
            "  lastlog                alle User mit letztem Login\n"
            "  lastlog -u ghost       nur für User 'ghost'\n"
            "  lastlog -t 7           User die in letzten 7 Tagen eingeloggt waren\n"
            "  Quelle: /var/log/lastlog\n\n"
            "faillog — fehlgeschlagene Logins:\n"
            "  faillog                alle fehlgeschlagenen Login-Versuche\n"
            "  faillog -u ghost       für bestimmten User\n"
            "  faillog -r -u ghost    Zähler für ghost zurücksetzen\n"
            "  Quelle: /var/log/faillog\n\n"
            "wtmp & btmp — Binär-Logs:\n"
            "  /var/log/wtmp          Login/Logout-Verlauf (last liest hier)\n"
            "  /var/log/btmp          fehlgeschlagene Login-Versuche\n"
            "  last -f /var/log/wtmp  explizit wtmp lesen\n"
            "  lastb                  fehlgeschlagene Logins aus btmp\n"
            "  lastb -n 20            letzte 20 fehlgeschlagene Versuche\n\n"
            "GREP/AWK AUF LOGS:\n"
            "  grep 'Failed password' /var/log/auth.log\n"
            "  grep 'Accepted' /var/log/auth.log | awk '{print $9, $11}'\n"
            "  awk '/Failed/{print $1,$2,$3,$11}' /var/log/auth.log\n"
            "  grep -c 'Failed' /var/log/auth.log   # Anzahl zählen"
        ),
        syntax       = "last  |  lastlog  |  faillog  |  lastb",
        example      = (
            "last -n 20\n"
            "last reboot\n"
            "lastlog -u ghost\n"
            "faillog\n"
            "lastb -n 10\n"
            "grep 'Failed password' /var/log/auth.log | tail -20"
        ),
        task_description = "Zeige die letzten 20 Login-Ereignisse mit last",
        expected_commands = ["last -n 20", "last"],
        hint_text    = "last zeigt Login/Logout-Ereignisse aus /var/log/wtmp",
        quiz_questions = [
            QuizQuestion(
                question   = "Welche Datei enthält fehlgeschlagene Login-Versuche für den Befehl 'lastb'?",
                options    = [
                    "/var/log/wtmp",
                    "/var/log/faillog",
                    "/var/log/btmp",
                    "/var/log/auth.log",
                ],
                correct    = 2,
                explanation = (
                    "/var/log/btmp enthält fehlgeschlagene Login-Versuche (bad logins).\n"
                    "/var/log/wtmp enthält normale Login/Logout-Events (last liest hier).\n"
                    "lastb liest /var/log/btmp — last liest /var/log/wtmp."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welcher Befehl zeigt den letzten Login-Zeitpunkt für jeden Systembenutzer?",
                options    = [
                    "last -a",
                    "lastb",
                    "lastlog",
                    "who -H",
                ],
                correct    = 2,
                explanation = (
                    "lastlog zeigt für jeden User den Zeitpunkt des letzten Logins.\n"
                    "Quelle ist /var/log/lastlog.\n"
                    "last zeigt den Verlauf aller Logins, nicht nur den letzten pro User."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Login-Logs:\n"
            "  last → /var/log/wtmp (Login-Verlauf)\n"
            "  lastb → /var/log/btmp (fehlgeschlagene Logins)\n"
            "  lastlog → /var/log/lastlog (letzter Login pro User)\n"
            "  faillog → fehlgeschlagene Login-Versuche + Sperren"
        ),
        memory_tip   = "wtmp=wer war da, btmp=bad logins, lastlog=letzter pro User",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.19 — systemd-analyze: Boot-Zeiten analysieren
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.19",
        chapter      = 11,
        title        = "systemd-analyze — Boot-Zeiten & Performance",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "NEXUS",
        story        = (
            "NEXUS: 'Der Boot dauert 47 Sekunden, Ghost.\n"
            " In NeonGrid-9 ist das eine Ewigkeit.\n"
            " systemd-analyze blame zeigt den Übeltäter.\n"
            " critical-chain zeigt den kritischen Pfad.\n"
            " Optimiere. Beschleunige. Überlebe.'"
        ),
        why_important = (
            "systemd-analyze ist das Standard-Tool zur Boot-Performance-Analyse.\n"
            "LPIC-1 prüft systemd-analyze blame und critical-chain.\n"
            "Boot-Optimierung ist praxisrelevant für Server und Desktop."
        ),
        explanation  = (
            "SYSTEMD-ANALYZE — BOOT-ANALYSE:\n\n"
            "GRUNDBEFEHLE:\n"
            "  systemd-analyze            Gesamte Boot-Zeit anzeigen\n"
            "  systemd-analyze time       Boot-Zeit (kernel + userspace)\n"
            "  systemd-analyze blame      Units nach Startdauer sortiert\n"
            "  systemd-analyze critical-chain  kritischen Startpfad anzeigen\n"
            "  systemd-analyze plot > boot.svg  Boot-SVG-Grafik erzeugen\n\n"
            "AUSGABE VON 'systemd-analyze':\n"
            "  Startup finished in:\n"
            "    3.5s (firmware) + 1.2s (loader) + 4.8s (kernel) + 12.3s (userspace)\n"
            "    = 21.8s\n\n"
            "BLAME — LANGSAME UNITS FINDEN:\n"
            "  systemd-analyze blame | head -20\n"
            "  → Zeigt Units sortiert nach Startdauer\n"
            "  → Längste zuerst — Optimierungskandidaten!\n\n"
            "CRITICAL-CHAIN:\n"
            "  systemd-analyze critical-chain\n"
            "  systemd-analyze critical-chain ssh.service\n"
            "  → Zeigt den kritischen Abhängigkeitspfad einer Unit\n"
            "  → Units in rot = auf dem kritischen Pfad\n\n"
            "PLOT — SVG-VISUALISIERUNG:\n"
            "  systemd-analyze plot > /tmp/boot.svg\n"
            "  → Zeitachse aller Units als SVG\n"
            "  → Im Browser öffnen für visuelle Analyse\n\n"
            "WEITERE NÜTZLICHE OPTIONEN:\n"
            "  systemd-analyze verify unit.service  Unit-Syntax prüfen\n"
            "  systemd-analyze calendar 'Mon *-*-*'  Timer-Ausdruck prüfen\n"
            "  systemd-analyze dot | dot -Tsvg > deps.svg  Abhängigkeitsgraph"
        ),
        syntax       = "systemd-analyze blame  |  systemd-analyze critical-chain",
        example      = (
            "systemd-analyze\n"
            "systemd-analyze blame | head -20\n"
            "systemd-analyze critical-chain\n"
            "systemd-analyze critical-chain NetworkManager.service\n"
            "systemd-analyze plot > /tmp/boot.svg"
        ),
        task_description = "Analysiere die Boot-Zeit und zeige die langsamsten Units",
        expected_commands = ["systemd-analyze blame"],
        hint_text    = "systemd-analyze blame zeigt alle Units sortiert nach Startdauer",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher systemd-analyze Befehl zeigt Units nach ihrer Startdauer sortiert?",
                options    = [
                    "systemd-analyze time",
                    "systemd-analyze sort",
                    "systemd-analyze blame",
                    "systemd-analyze list",
                ],
                correct    = 2,
                explanation = (
                    "systemd-analyze blame zeigt alle Units sortiert nach Startdauer (längste zuerst).\n"
                    "systemd-analyze time zeigt nur die Gesamtzeit.\n"
                    "critical-chain zeigt den kritischen Abhängigkeitspfad."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was erzeugt 'systemd-analyze plot'?",
                options    = [
                    "Ein Textdiagramm im Terminal",
                    "Eine SVG-Grafik der Boot-Zeitachse",
                    "Ein PNG-Bild der Unit-Abhängigkeiten",
                    "Eine CSV-Datei mit Boot-Zeiten",
                ],
                correct    = 1,
                explanation = (
                    "systemd-analyze plot gibt eine SVG-Datei aus, die alle\n"
                    "Units auf einer Zeitachse darstellt.\n"
                    "Typische Nutzung: systemd-analyze plot > boot.svg"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 systemd-analyze:\n"
            "  blame → Units nach Startdauer (längste zuerst)\n"
            "  critical-chain → kritischer Startpfad\n"
            "  plot → SVG-Visualisierung der Boot-Zeitachse\n"
            "  time → Gesamte Boot-Zeit (firmware+loader+kernel+userspace)"
        ),
        memory_tip   = "blame = wer ist schuld am langsamen Boot? critical-chain = der Engpass-Pfad",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.20 — logwatch & Log-Zusammenfassungen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.20",
        chapter      = 11,
        title        = "logwatch & logcheck — Log-Zusammenfassungen",
        mtype        = "CONSTRUCT",
        xp           = 75,
        speaker      = "ARCHIVE",
        story        = (
            "ARCHIVE: 'Täglich tausende Log-Zeilen, Ghost.\n"
            " Kein Mensch liest das alles.\n"
            " logwatch komprimiert sie zu einem Tages-Report.\n"
            " logcheck filtert das Rauschen und meldet das Wichtige.\n"
            " Automatisch. Täglich. Per E-Mail.'"
        ),
        why_important = (
            "logwatch und logcheck automatisieren Log-Überwachung.\n"
            "LPIC-1 prüft Grundkenntnisse zu Log-Management-Tools.\n"
            "In der Praxis: tägliche Reports statt manuelles Log-Lesen."
        ),
        explanation  = (
            "LOGWATCH — TAGES-LOG-REPORT:\n\n"
            "INSTALLATION & NUTZUNG:\n"
            "  apt install logwatch         (Debian/Ubuntu)\n"
            "  logwatch                     interaktiven Report ausgeben\n"
            "  logwatch --output mail       Report per E-Mail senden\n"
            "  logwatch --output stdout     auf Bildschirm ausgeben\n"
            "  logwatch --detail high       detaillierter Report\n"
            "  logwatch --service sshd      nur SSH-Logs\n"
            "  logwatch --range today       nur heutige Logs\n"
            "  logwatch --range yesterday   gestrige Logs\n\n"
            "KONFIGURATION:\n"
            "  /etc/logwatch/conf/logwatch.conf   Haupt-Konfiguration\n"
            "  /usr/share/logwatch/default.conf/  Standard-Einstellungen\n"
            "  /etc/logwatch/conf/services/       Service-spezifische Configs\n\n"
            "WICHTIGE EINSTELLUNGEN (logwatch.conf):\n"
            "  MailTo = root                # Report-Empfänger\n"
            "  Detail = Med                 # Low/Med/High\n"
            "  Range = yesterday            # Zeitraum\n"
            "  Output = mail                # mail/stdout/file\n\n"
            "LOGCHECK — ANOMALIE-FILTER:\n"
            "  apt install logcheck\n"
            "  /etc/logcheck/               Konfigurationsverzeichnis\n"
            "  /etc/logcheck/ignore.d.server/  Bekannte/normale Muster ignorieren\n"
            "  /etc/logcheck/violations.d/    Sicherheits-Verletzungen erkennen\n"
            "  Läuft automatisch per cron (stündlich)\n"
            "  Sendet nur UNGEWÖHNLICHE Log-Zeilen per Mail\n\n"
            "UNTERSCHIED logwatch vs logcheck:\n"
            "  logwatch  = tägliche Zusammenfassung (alle Logs)\n"
            "  logcheck  = stündliche Anomalie-Erkennung (nur Auffälliges)"
        ),
        syntax       = "logwatch [--output stdout] [--detail high] [--service SERVICE]",
        example      = (
            "logwatch --output stdout --detail med\n"
            "logwatch --output stdout --service sshd --range today\n"
            "logwatch --output mail --detail high\n"
            "cat /etc/logwatch/conf/logwatch.conf\n"
            "ls /etc/logcheck/"
        ),
        task_description = "Zeige einen logwatch-Report für heute auf der Standardausgabe",
        expected_commands = ["logwatch --output stdout", "logwatch"],
        hint_text    = "logwatch --output stdout gibt den Report im Terminal aus statt per Mail",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Hauptunterschied zwischen logwatch und logcheck?",
                options    = [
                    "logwatch ist schneller als logcheck",
                    "logwatch erstellt Zusammenfassungen, logcheck meldet nur Anomalien",
                    "logcheck läuft täglich, logwatch stündlich",
                    "Sie sind identisch — verschiedene Namen für dasselbe Tool",
                ],
                correct    = 1,
                explanation = (
                    "logwatch erstellt tägliche Zusammenfassungen aller Logs.\n"
                    "logcheck läuft stündlich und meldet nur UNGEWÖHNLICHE Zeilen.\n"
                    "logwatch = 'was ist passiert', logcheck = 'was ist verdächtig'."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "In welcher Datei konfiguriert man den Empfänger für logwatch-Reports?",
                options    = [
                    "/etc/logwatch/logwatch.conf",
                    "/etc/logwatch/conf/logwatch.conf",
                    "/usr/share/logwatch/logwatch.conf",
                    "/etc/cron.daily/logwatch",
                ],
                correct    = 1,
                explanation = (
                    "/etc/logwatch/conf/logwatch.conf ist die lokale Konfigurationsdatei.\n"
                    "Dort setzt man MailTo, Detail, Range und Output.\n"
                    "Systemweite Defaults: /usr/share/logwatch/default.conf/"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Log-Tools:\n"
            "  logwatch = tägliche Zusammenfassung → /etc/logwatch/conf/\n"
            "  logcheck = stündliche Anomalie-Erkennung → /etc/logcheck/\n"
            "  logwatch --output stdout = Terminal statt Mail\n"
            "  logwatch --detail high = detaillierterer Report"
        ),
        memory_tip   = "logWATCH = alles im Blick (täglich), logCHECK = prüft auf Probleme (stündlich)",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.21 — QUIZ: Logging & Scheduling
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.21",
        chapter      = 11,
        title        = "QUIZ — Logging & Scheduling Wissenstest",
        mtype        = "QUIZ",
        xp           = 150,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Der Log-Daemon wartet, Ghost.\n"
            " Topic 108.1, 108.2 und 107.3 auf dem Tisch.\n"
            " Kein Fehler erlaubt — dein Wissen wird gelogged.'"
        ),
        why_important = "Quiz-Wiederholung für LPIC-1 Prüfung Topic 108.1/108.2/107.3",
        explanation   = "Beantworte die Fragen zu Logging, Zeit und Scheduling.",
        syntax        = "",
        example       = "",
        task_description = "Quiz: Logging & Scheduling",
        expected_commands = [],
        hint_text     = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Welche syslog-Severity hat Priorität 3?",
                options    = [
                    "A) warning",
                    "B) notice",
                    "C) err",
                    "D) crit",
                ],
                correct    = "C",
                explanation = (
                    "Syslog Severity-Level:\n"
                    "  0=emerg, 1=alert, 2=crit, 3=err, 4=warning\n"
                    "  5=notice, 6=info, 7=debug\n"
                    "Niedrigere Nummer = höhere Priorität!"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Was bedeutet '*/15' im Minuten-Feld einer Crontab?",
                options    = [
                    "A) Am 15. jeden Monats",
                    "B) Alle 15 Minuten",
                    "C) Um 15:00 Uhr",
                    "D) Nur in Minute 15",
                ],
                correct    = "B",
                explanation = (
                    "*/N im Cron = alle N Einheiten\n"
                    "*/15 im Minuten-Feld = alle 15 Minuten\n"
                    "*/2 im Stunden-Feld = alle 2 Stunden"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welcher Befehl zeigt alle wartenden at-Jobs?",
                options    = [
                    "A) at -l",
                    "B) atq",
                    "C) at -q",
                    "D) A und B",
                ],
                correct    = "D",
                explanation = (
                    "atq UND at -l sind identisch — beide zeigen die at-Warteschlange.\n"
                    "atrm NR bzw. at -d NR löscht Jobs."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welche Datei bestimmt die Zeitzone in Debian/Ubuntu?",
                options    = [
                    "A) /etc/localtime",
                    "B) /etc/timezone",
                    "C) /usr/share/zoneinfo/",
                    "D) /etc/ntp.conf",
                ],
                correct    = "B",
                explanation = (
                    "/etc/timezone enthält den Zeitzonennamen (z.B. 'Europe/Berlin')\n"
                    "/etc/localtime ist ein Symlink nach /usr/share/zoneinfo/...\n"
                    "Beide sind relevant, /etc/timezone ist die primäre Konfigdatei."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Was macht 'journalctl -b -1'?",
                options    = [
                    "A) Logs der letzten Stunde",
                    "B) Löscht einen Log-Eintrag",
                    "C) Zeigt Logs des vorherigen Boots",
                    "D) Zeigt Logs mit Priorität 1 (alert)",
                ],
                correct    = "C",
                explanation = (
                    "journalctl -b = Boot-Filter\n"
                    "-b ohne Zahl = aktueller Boot\n"
                    "-b -1 = vorheriger Boot\n"
                    "-b -2 = vorletzter Boot\n"
                    "--list-boots zeigt alle verfügbaren Boots"
                ),
                xp_value   = 30,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Logging/Scheduling-Schwerpunkte:\n"
            "  - Syslog Severity 0-7 auswendig kennen\n"
            "  - Crontab: MIN STD TAG MON WOT (5 Felder)\n"
            "  - /etc/crontab hat ZUSÄTZLICH User-Feld (6 Felder)\n"
            "  - journalctl -b=boot, -p=priority, -u=unit, -f=follow"
        ),
        memory_tip   = "",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 11.BOSS — CHRONO DAEMON v11.0
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "11.boss",
        chapter      = 11,
        title        = "BOSS — CHRONO DAEMON v11.0",
        mtype        = "BOSS",
        xp           = 300,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM ALERT: CHRONO DAEMON v11.0 aktiv.\n"
            "Er hat die Systemzeit manipuliert. Logs korrumpiert.\n"
            "Cron-Jobs umgeleitet. NTP gestoppt.\n"
            "Zara Z3R0: 'Stelle die Zeit wieder her. Lies die Logs.\n"
            " Finde seinen Cron-Job. Vernichte ihn. Jetzt.'"
        ),
        why_important = "Abschluss-Boss für Topic 108.1/108.2/107.3",
        explanation  = (
            "BOSS-CHALLENGE: Time & Log Gauntlet\n\n"
            "Deine Mission:\n"
            "1) Systemzeit prüfen und NTP aktivieren\n"
            "2) Fehler-Logs seit dem letzten Boot analysieren\n"
            "3) Verdächtigen Cron-Job identifizieren\n"
            "4) logrotate-Status prüfen\n\n"
            "KOMMANDOS:\n"
            "  timedatectl\n"
            "  timedatectl set-ntp true\n"
            "  journalctl -b -p err\n"
            "  crontab -l\n"
            "  cat /etc/crontab\n"
            "  logrotate -d /etc/logrotate.conf"
        ),
        syntax       = "",
        example      = (
            "timedatectl\n"
            "timedatectl set-ntp true\n"
            "journalctl -b -p err --since today\n"
            "crontab -l\n"
            "cat /etc/crontab\n"
            "ls /etc/cron.d/"
        ),
        task_description = "BOSS: Aktiviere NTP-Synchronisation mit timedatectl",
        expected_commands = ["timedatectl set-ntp true"],
        hint_text    = "timedatectl set-ntp true aktiviert automatische Zeitsynchronisation via NTP",
        exam_tip     = (
            "LPIC-1 FINAL SYSLOG CHECK:\n"
            "  Severity: 0=emerg..7=debug\n"
            "  journalctl -b -p err = Boot-Fehler\n"
            "  crontab -e/-l/-r = bearbeiten/listen/löschen\n"
            "  /etc/crontab = 6 Felder (mit USER)\n"
            "  timedatectl set-ntp true = NTP aktivieren\n"
            "  logrotate -f = erzwungene Rotation"
        ),
        memory_tip   = "Merkhilfe: BOSS = Big Operations on System Scheduling",
        gear_reward  = "kernel_beacon",
        faction_reward = ("Kernel Syndicate", 35),
    ),

]
