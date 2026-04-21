"""
NeonGrid-9 :: Kapitel 10 — USER MATRIX
LPIC-1 Topic 107.1 / 107.2
Benutzer, Gruppen, Passwörter, sudo & PAM

"In NeonGrid-9 ist Identität alles.
 Wer bist du? Welcher Gruppe gehörst du an?
 Wer darf sudo? Wer darf es nicht?
 Der Kernel entscheidet. Aber du konfigurierst ihn."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_10_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 10.01 — Benutzer & /etc/passwd
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.01",
        chapter      = 10,
        title        = "Benutzerkonten — /etc/passwd & UIDs",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Das Imperium kontrolliert Identitäten, Ghost.\n"
            " Jede UID. Jede GID. Jede Shell.\n"
            " /etc/passwd ist das Herzstück der Benutzerverwaltung.\n"
            " Kenn die Datei — und du kennst das System.'"
        ),
        why_important = (
            "Benutzerverwaltung ist LPIC-1 Topic 107.1 Kernstoff.\n"
            "/etc/passwd und die UID-Struktur sind Prüfungsthema.\n"
            "Systembenutzer vs normale Benutzer — immer gefragt."
        ),
        explanation  = (
            "/ETC/PASSWD — FORMAT:\n\n"
            "  username:password:UID:GID:GECOS:home:shell\n\n"
            "BEISPIEL:\n"
            "  ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash\n"
            "  │     │ │    │    │           │           └ Login-Shell\n"
            "  │     │ │    │    │           └ Home-Verzeichnis\n"
            "  │     │ │    │    └ GECOS (Kommentar/Name)\n"
            "  │     │ │    └ Primäre GID\n"
            "  │     │ └ UID\n"
            "  │     └ 'x' = Passwort in /etc/shadow\n"
            "  └ Benutzername\n\n"
            "UID-BEREICHE:\n"
            "  0          root (Superuser)\n"
            "  1–999      Systembenutzer (Daemons, Services)\n"
            "  1000+      normale Benutzer\n"
            "  65534      nobody (no privileges)\n\n"
            "WICHTIGE SYSTEMBENUZER:\n"
            "  root:x:0:0    Superuser\n"
            "  daemon:x:1:1  Daemon-Prozesse\n"
            "  bin:x:2:2     Binaries\n"
            "  nobody:x:65534  kein Besitz\n\n"
            "SHELLS:\n"
            "  /bin/bash         interaktive Shell\n"
            "  /bin/sh           POSIX-Shell\n"
            "  /sbin/nologin     kein Login erlaubt\n"
            "  /usr/sbin/nologin kein Login (Debian)\n"
            "  /bin/false        Login verweigert"
        ),
        ascii_art = """
  ██╗   ██╗███████╗███████╗██████╗ ███████╗    ██╗
  ██║   ██║██╔════╝██╔════╝██╔══██╗██╔════╝   ██╔╝
  ██║   ██║███████╗█████╗  ██████╔╝███████╗  ██╔╝
  ██║   ██║╚════██║██╔══╝  ██╔══██╗╚════██║ ██╔╝
  ╚██████╔╝███████║███████╗██║  ██║███████║██╔╝
   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝

  [ CHAPTER 10 :: USERS & GROUPS ]
  > /etc/passwd loaded. Identity matrix online. UID scan...""",
        story_transitions = [
            "Jeder User hat eine UID. Jede Gruppe eine GID. Niemand ist anonym.",
            "/etc/passwd: offen. /etc/shadow: verschlüsselt. Kenn den Unterschied.",
            "useradd, usermod, userdel — du bestimmst wer existiert.",
            "Privilegien trennen: root ist nicht alles. sudo ist die Brücke.",
        ],
        syntax       = "cat /etc/passwd  |  getent passwd USER  |  id USER",
        example      = (
            "cat /etc/passwd\n"
            "cat /etc/passwd | grep ghost\n"
            "getent passwd ghost\n"
            "id ghost\n"
            "id\n"
            "whoami"
        ),
        task_description = "Zeige den Eintrag für den Benutzer 'ghost' in /etc/passwd",
        expected_commands = ["getent passwd ghost"],
        hint_text    = "getent passwd ghost zeigt den /etc/passwd-Eintrag für 'ghost'",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welche Datei enthält verschlüsselte Passwörter?',
                options     = ['A) /etc/passwd', 'B) /etc/shadow', 'C) /etc/password', 'D) /etc/login'],
                correct     = 'B',
                explanation = '/etc/shadow enthält gehashte Passwörter (nur root lesbar). /etc/passwd ist world-readable.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNG: /etc/passwd-Felder in Reihenfolge kennen!\n"
            "  user:pass:UID:GID:GECOS:home:shell\n"
            "Das 'x' bei password bedeutet: Passwort ist in /etc/shadow!\n"
            "UID 0 = root, UID 1-999 = System, UID 1000+ = normale User"
        ),
        memory_tip   = "Merkhilfe: /etc/passwd = 7 Felder durch ':' getrennt",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.02 — /etc/shadow & Passwort-Sicherheit
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.02",
        chapter      = 10,
        title        = "Passwörter — /etc/shadow & Hashing",
        mtype        = "DECODE",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Das Imperium speichert Passwörter im Klartext, Ghost.\n"
            " Wir nicht. /etc/shadow mit SHA-512-Hashes.\n"
            " Kenn das Format — und du weißt wie sicher ein System ist.\n"
            " Und wann ein Hash geknackt wurde.'"
        ),
        why_important = (
            "/etc/shadow ist der sichere Passwort-Speicher.\n"
            "LPIC-1 testet shadow-Format, passwd-Aging und chage."
        ),
        explanation  = (
            "/ETC/SHADOW — FORMAT (9 Felder):\n\n"
            "  user:$hash:last:min:max:warn:inactive:expire:reserved\n\n"
            "FELDER:\n"
            "  1  Benutzername\n"
            "  2  Passwort-Hash ($6$salt$hash = SHA-512)\n"
            "  3  Letztes Passwort-Änderungsdatum (Tage seit 1.1.1970)\n"
            "  4  Minimum-Tage bis Änderung erlaubt\n"
            "  5  Maximum-Tage bis Änderung erzwungen\n"
            "  6  Warn-Tage vor Ablauf\n"
            "  7  Inaktivitäts-Tage nach Ablauf bis Account gesperrt\n"
            "  8  Account-Ablaufdatum (leer = kein Ablauf)\n"
            "  9  Reserviert\n\n"
            "HASH-PRÄFIXE:\n"
            "  $1$   MD5 (veraltet, unsicher)\n"
            "  $5$   SHA-256\n"
            "  $6$   SHA-512 (Standard)\n"
            "  $y$   yescrypt (modern)\n"
            "  !     Account gesperrt\n"
            "  *     kein Passwort-Login möglich\n\n"
            "PASSWORT-AGING MIT chage:\n"
            "  chage -l ghost          Passwort-Info anzeigen\n"
            "  chage -M 90 ghost       Max 90 Tage\n"
            "  chage -m 7 ghost        Min 7 Tage\n"
            "  chage -W 14 ghost       14 Tage Warnung\n"
            "  chage -E 2089-12-31 ghost  Account-Ablauf\n"
            "  chage -d 0 ghost        sofortige Passwort-Änderung erzwingen\n\n"
            "PASSWORT SETZEN:\n"
            "  passwd              eigenes Passwort\n"
            "  passwd ghost        fremdes Passwort (als root)\n"
            "  passwd -l ghost     Account sperren\n"
            "  passwd -u ghost     Account entsperren\n"
            "  passwd -e ghost     Passwort sofort ablaufen lassen"
        ),
        syntax       = "chage -l USER  |  passwd USER  |  cat /etc/shadow",
        example      = (
            "sudo cat /etc/shadow\n"
            "chage -l ghost\n"
            "chage -M 90 -m 7 -W 14 ghost\n"
            "passwd ghost\n"
            "passwd -l ghost      # Account sperren\n"
            "passwd -u ghost      # Account entsperren"
        ),
        task_description = "Zeige die Passwort-Aging-Informationen für Benutzer 'ghost'",
        expected_commands = ["chage -l ghost"],
        hint_text    = "chage -l ghost zeigt Passwort-Alter, Ablauf und Warnzeiten",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'useradd -m username'?",
                options     = ['A) Erstellt Benutzer ohne Homeverzeichnis', 'B) Erstellt Benutzer MIT Homeverzeichnis (/home/username)', 'C) Modifiziert bestehenden Benutzer', 'D) Erstellt System-Benutzer'],
                correct     = 'B',
                explanation = 'useradd -m = create home directory. Ohne -m: kein /home/username erstellt.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welcher Befehl ändert das Passwort eines Benutzers als Root?',
                options     = ['A) useradd --password user', 'B) passwd username', 'C) chpasswd username', 'D) usermod --password user'],
                correct     = 'B',
                explanation = 'passwd USERNAME als root ändert das Passwort für jeden Benutzer.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGSFRAGE: Was bedeutet '!' am Anfang des Passwort-Hash?\n"
            "→ Account ist gesperrt (locked)!\n"
            "chage -d 0 zwingt sofortige Passwortänderung beim nächsten Login."
        ),
        memory_tip   = "Merkhilfe: chage = change age. -M=max -m=min -W=warn -E=expire -d=lastday",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.03 — useradd, usermod, userdel
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.03",
        chapter      = 10,
        title        = "useradd / usermod / userdel",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Neuer Operator im Team, Ghost.\n"
            " Erstelle den Account. Setze die Shell.\n"
            " Home-Verzeichnis anlegen. Gruppe zuweisen.\n"
            " useradd — schnell und direkt.'"
        ),
        why_important = (
            "useradd/usermod/userdel sind die Standard-Tools zur Benutzerverwaltung.\n"
            "LPIC-1 testet die wichtigen Flags: -m, -s, -g, -G, -d, -u, -c."
        ),
        explanation  = (
            "USERADD — BENUTZER ERSTELLEN:\n\n"
            "  useradd ghost                    minimaler Account\n"
            "  useradd -m ghost                 mit Home-Verzeichnis\n"
            "  useradd -m -s /bin/bash ghost    mit Shell\n"
            "  useradd -m -s /bin/bash -c 'Ghost User' ghost\n"
            "  useradd -u 1500 ghost            spezifische UID\n"
            "  useradd -g users ghost           primäre Gruppe\n"
            "  useradd -G sudo,docker ghost     Zusatzgruppen\n"
            "  useradd -d /opt/ghost ghost      anderes Home\n"
            "  useradd -r ghost                 System-Account (UID < 1000)\n"
            "  useradd -e 2089-12-31 ghost      Account-Ablauf\n\n"
            "ADDUSER (Debian/Ubuntu — interaktiv, empfohlen):\n"
            "  adduser ghost                    interaktiv mit Fragen\n\n"
            "USERMOD — BENUTZER ÄNDERN:\n\n"
            "  usermod -s /bin/zsh ghost        Shell ändern\n"
            "  usermod -d /home/newdir ghost    Home ändern\n"
            "  usermod -l newname ghost         Benutzername ändern\n"
            "  usermod -u 1600 ghost            UID ändern\n"
            "  usermod -aG docker ghost         Gruppe HINZUFÜGEN (-a!)\n"
            "  usermod -G sudo ghost            Gruppen ERSETZEN (ohne -a!)\n"
            "  usermod -L ghost                 Account sperren\n"
            "  usermod -U ghost                 Account entsperren\n\n"
            "USERDEL — BENUTZER LÖSCHEN:\n\n"
            "  userdel ghost                    nur Account (Home bleibt)\n"
            "  userdel -r ghost                 Account + Home löschen\n\n"
            "WICHTIG: -aG vs -G:\n"
            "  usermod -aG docker ghost    → docker HINZUFÜGEN (append)\n"
            "  usermod -G docker ghost     → ALLE Gruppen durch 'docker' ERSETZEN!"
        ),
        syntax       = "useradd -m -s /bin/bash -c 'NAME' USER  |  usermod -aG GROUP USER",
        example      = (
            "useradd -m -s /bin/bash -c 'Ghost User' ghost\n"
            "passwd ghost\n"
            "usermod -aG sudo ghost\n"
            "usermod -s /bin/zsh ghost\n"
            "userdel -r ghost"
        ),
        task_description = "Erstelle einen neuen Benutzer 'operator' mit Home-Verzeichnis und bash-Shell",
        expected_commands = ["useradd -m -s /bin/bash operator"],
        hint_text    = "useradd -m erstellt Home-Verzeichnis, -s /bin/bash setzt die Shell",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'groupadd entwickler'?",
                options     = ['A) Benutzer zu Gruppe hinzufügen', "B) Neue Gruppe 'entwickler' erstellen", 'C) Gruppenpasswort setzen', 'D) Gruppenmitglieder anzeigen'],
                correct     = 'B',
                explanation = 'groupadd GRUPPENNAME erstellt eine neue Gruppe in /etc/group.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wie fügt man einen Benutzer zu einer Gruppe hinzu ohne andere Gruppen zu entfernen?',
                options     = ['A) usermod -g gruppe user', 'B) usermod -aG gruppe user', 'C) groupadd -u user gruppe', 'D) gpasswd gruppe user'],
                correct     = 'B',
                explanation = 'usermod -aG = append to Group. Ohne -a würde -G alle anderen Gruppen entfernen!',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "KRITISCH: usermod -aG vs usermod -G\n"
            "  -aG = append (Gruppe hinzufügen, bestehende behalten!)\n"
            "  -G  = replace (alle Gruppen ersetzen!)\n"
            "Vergisst man -a, verliert der User alle anderen Gruppen!"
        ),
        memory_tip   = "Merkhilfe: useradd -m(ake home) -s(hell) -g(roup) -G(roups) -c(omment)",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.04 — Gruppen: groupadd, groupmod, groups
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.04",
        chapter      = 10,
        title        = "Gruppen — /etc/group & groupadd",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Gruppen sind Macht-Cluster, Ghost.\n"
            " sudo-Gruppe = Admin. docker-Gruppe = Container-Zugang.\n"
            " audio-Gruppe = Ton. Wer die Gruppen kennt,\n"
            " kennt die Zugriffsmatrix des Systems.'"
        ),
        why_important = (
            "Gruppen steuern Ressourcen-Zugriff.\n"
            "LPIC-1 testet /etc/group-Format, groupadd, groupmod, gpasswd."
        ),
        explanation  = (
            "/ETC/GROUP — FORMAT:\n\n"
            "  groupname:password:GID:members\n\n"
            "BEISPIEL:\n"
            "  docker:x:999:ghost,zara\n"
            "  sudo:x:27:ghost\n\n"
            "GID-BEREICHE:\n"
            "  0          root-Gruppe\n"
            "  1–999      Systemgruppen\n"
            "  1000+      normale Gruppen\n\n"
            "PRIMÄRE vs ZUSATZ-GRUPPEN:\n"
            "  Primärgruppe  → GID in /etc/passwd Feld 4\n"
            "                  Dateien werden dieser Gruppe zugeordnet\n"
            "  Zusatzgruppen → in /etc/group members-Feld\n\n"
            "GROUPADD:\n"
            "  groupadd hackers               neue Gruppe\n"
            "  groupadd -g 2000 hackers       spezifische GID\n"
            "  groupadd -r hackers            System-Gruppe (GID < 1000)\n\n"
            "GROUPMOD:\n"
            "  groupmod -n newname hackers    Gruppe umbenennen\n"
            "  groupmod -g 2100 hackers       GID ändern\n\n"
            "GROUPDEL:\n"
            "  groupdel hackers               Gruppe löschen\n\n"
            "GPASSWD — Gruppen-Mitglieder verwalten:\n"
            "  gpasswd -a ghost hackers       Benutzer hinzufügen\n"
            "  gpasswd -d ghost hackers       Benutzer entfernen\n"
            "  gpasswd -A ghost hackers       Ghost zum Gruppen-Admin\n\n"
            "GRUPPEN ANZEIGEN:\n"
            "  groups                    eigene Gruppen\n"
            "  groups ghost              Gruppen von ghost\n"
            "  id ghost                  UID, GID und alle Gruppen\n"
            "  cat /etc/group            alle Gruppen"
        ),
        syntax       = "groupadd NAME  |  gpasswd -a USER GROUP  |  groups USER",
        example      = (
            "groupadd hackers\n"
            "gpasswd -a ghost hackers\n"
            "groups ghost\n"
            "id ghost\n"
            "cat /etc/group | grep ghost\n"
            "groupdel hackers"
        ),
        task_description = "Füge den Benutzer 'ghost' zur Gruppe 'sudo' hinzu",
        expected_commands = ["gpasswd -a ghost sudo"],
        hint_text    = "gpasswd -a USER GROUP fügt einen Benutzer zu einer Gruppe hinzu",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was enthält /etc/passwd pro Zeile (7 Felder)?',
                options     = ['A) user:pass:uid:gid:comment:home:shell', 'B) user:uid:gid:home:shell:pass:groups', 'C) user:pass:home:shell:uid:gid:comment', 'D) uid:user:pass:gid:home:shell:comment'],
                correct     = 'A',
                explanation = '/etc/passwd: username:password(x):UID:GID:GECOS:Homedir:Shell',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "MERKE: gpasswd -a vs usermod -aG:\n"
            "  gpasswd -a ghost docker  → gleicher Effekt wie usermod -aG docker ghost\n"
            "  Beide fügen den User zur Gruppe hinzu ohne bestehende zu entfernen."
        ),
        memory_tip   = "Merkhilfe: /etc/group = 4 Felder: name:x:GID:members",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.05 — sudo & /etc/sudoers
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.05",
        chapter      = 10,
        title        = "sudo — Privilegien-Eskalation",
        mtype        = "INFILTRATE",
        xp           = 110,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'sudo ist dein Passierschein, Ghost.\n"
            " Mit großer Macht kommt große Verantwortung.\n"
            " /etc/sudoers falsch konfiguriert — und das Imperium\n"
            " spaziert mit root-Rechten durch dein System.'"
        ),
        why_important = (
            "sudo ist das Standard-Tool für privilegierte Operationen.\n"
            "LPIC-1 testet /etc/sudoers-Syntax, visudo und sudo-Logs."
        ),
        explanation  = (
            "SUDO — SUPERUSER DO:\n\n"
            "GRUNDBEFEHLE:\n"
            "  sudo BEFEHL              Befehl als root ausführen\n"
            "  sudo -u ghost BEFEHL     Befehl als anderer User\n"
            "  sudo -i                  root-Shell (Login-Shell)\n"
            "  sudo -s                  root-Shell (aktuelle Umgebung)\n"
            "  sudo -l                  erlaubte sudo-Befehle anzeigen\n"
            "  sudo -l -U ghost         für anderen User\n"
            "  sudo !!                  letzten Befehl als root wiederholen\n\n"
            "/ETC/SUDOERS — SYNTAX:\n\n"
            "  NIEMALS direkt bearbeiten — immer: visudo\n\n"
            "  FORMAT: WHO WHERE=(AS) WHAT\n\n"
            "  root    ALL=(ALL:ALL) ALL     root darf alles\n"
            "  ghost   ALL=(ALL:ALL) ALL     ghost darf alles\n"
            "  ghost   ALL=(ALL) NOPASSWD:ALL  ohne Passwort!\n"
            "  ghost   ALL=/sbin/reboot      nur reboot erlaubt\n"
            "  %sudo   ALL=(ALL:ALL) ALL     sudo-Gruppe darf alles\n"
            "  %admin  ALL=(ALL) ALL         admin-Gruppe\n\n"
            "SUDOERS.D — FRAGMENTS:\n"
            "  /etc/sudoers.d/ghost     separate Datei für ghost\n"
            "  (sicherer als /etc/sudoers direkt zu bearbeiten)\n\n"
            "SUDO-LOGGING:\n"
            "  /var/log/auth.log        sudo-Aktivitäten (Debian)\n"
            "  /var/log/secure          sudo-Aktivitäten (RHEL)\n"
            "  journalctl -u sudo       systemd-Journal\n\n"
            "SU — SWITCH USER:\n"
            "  su -              root-Shell (Login-Shell, $PATH neu)\n"
            "  su ghost          zu ghost wechseln (kein Login)\n"
            "  su - ghost        zu ghost wechseln (Login-Shell)\n"
            "  su -c 'cmd' ghost Befehl als ghost ausführen"
        ),
        syntax       = "sudo BEFEHL  |  visudo  |  sudo -l",
        example      = (
            "sudo apt update\n"
            "sudo -i\n"
            "sudo -l\n"
            "sudo -u ghost ls /home/ghost\n"
            "visudo\n"
            "su - ghost"
        ),
        task_description = "Zeige alle erlaubten sudo-Befehle für den aktuellen Benutzer",
        expected_commands = ["sudo -l"],
        hint_text    = "sudo -l listet alle Befehle die du mit sudo ausführen darfst",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was macht chage -l username?',
                options     = ['A) Ändert Passwort-Ablauf', 'B) Zeigt Passwort-Ablauf-Informationen', 'C) Sperrt das Konto', 'D) Löscht Ablauf-Daten'],
                correct     = 'B',
                explanation = 'chage -l = list. Zeigt Passwort-Ablauf, letztes Änderungsdatum, etc.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wie sperrt man ein Benutzerkonto (kein Login möglich)?',
                options     = ['A) usermod -L username', 'B) usermod -d /bin/false username', 'C) passwd --lock username', 'D) A oder C'],
                correct     = 'D',
                explanation = 'usermod -L = lock (! vor Passwort in shadow). passwd --lock macht dasselbe.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "KRITISCH: visudo statt direktem Editieren von /etc/sudoers!\n"
            "visudo prüft die Syntax VOR dem Speichern.\n"
            "Syntaxfehler in sudoers = niemand kann mehr sudo!\n"
            "NOPASSWD: = sudo ohne Passwort-Abfrage"
        ),
        memory_tip   = "Merkhilfe: visudo = vi + sudo (einziger sicherer Weg)",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.06 — PAM — Pluggable Authentication Modules
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.06",
        chapter      = 10,
        title        = "PAM — Pluggable Authentication Modules",
        mtype        = "DECODE",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'PAM ist die Torwächter-Schicht, Ghost.\n"
            " Jeder Login läuft durch PAM.\n"
            " SSH, sudo, login — alle.\n"
            " Wer PAM kennt, kontrolliert wer ins System darf.'"
        ),
        why_important = (
            "PAM ist die Authentifizierungs-Abstraktionsschicht.\n"
            "LPIC-1 testet PAM-Konfiguration, /etc/pam.d/ und Module."
        ),
        explanation  = (
            "PAM — PLUGGABLE AUTHENTICATION MODULES:\n\n"
            "PAM trennt Authentifizierung von Anwendungen.\n"
            "Jeder Service hat seine eigene PAM-Konfiguration.\n\n"
            "KONFIGURATIONS-VERZEICHNIS:\n"
            "  /etc/pam.d/           PAM-Konfigurationsdateien\n"
            "  /etc/pam.d/sshd       SSH-Authentifizierung\n"
            "  /etc/pam.d/sudo       sudo-Authentifizierung\n"
            "  /etc/pam.d/login      Konsolen-Login\n"
            "  /etc/pam.d/common-auth  gemeinsame Auth-Regeln\n\n"
            "PAM-ZEILEN-FORMAT:\n"
            "  type  control  module  [options]\n\n"
            "TYPEN (Management Groups):\n"
            "  auth        Authentifizierung (Passwort prüfen)\n"
            "  account     Account-Regeln (gesperrt? abgelaufen?)\n"
            "  password    Passwort ändern\n"
            "  session     Session-Setup (Home mounten, Umgebung)\n\n"
            "CONTROLS:\n"
            "  required    muss erfolgreich sein (Fehler → weiter prüfen)\n"
            "  requisite   muss erfolgreich sein (Fehler → sofort abbruch)\n"
            "  sufficient  reicht wenn erfolgreich (Rest wird übersprungen)\n"
            "  optional    optional (Erfolg/Fehler meist egal)\n\n"
            "WICHTIGE MODULE:\n"
            "  pam_unix.so       Standard-Unix Auth (/etc/shadow)\n"
            "  pam_ldap.so       LDAP-Authentifizierung\n"
            "  pam_limits.so     Resource Limits (/etc/security/limits.conf)\n"
            "  pam_tally2.so     Login-Versuche zählen/sperren\n"
            "  pam_faillock.so   Account nach Fehlversuchen sperren\n"
            "  pam_nologin.so    /etc/nologin prüfen\n"
            "  pam_securetty.so  nur von sicheren TTYs\n"
            "  pam_env.so        Umgebungsvariablen setzen"
        ),
        syntax       = "ls /etc/pam.d/  |  cat /etc/pam.d/sshd",
        example      = (
            "ls /etc/pam.d/\n"
            "cat /etc/pam.d/sshd\n"
            "cat /etc/pam.d/sudo\n"
            "cat /etc/pam.d/common-auth\n"
            "# Limits konfigurieren:\n"
            "cat /etc/security/limits.conf"
        ),
        task_description = "Zeige die PAM-Konfigurationen im /etc/pam.d/ Verzeichnis",
        expected_commands = ["ls /etc/pam.d/"],
        hint_text    = "ls /etc/pam.d/ zeigt alle Service-spezifischen PAM-Konfigurationen",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Wo werden Sudo-Rechte konfiguriert?',
                options     = ['A) /etc/sudoers und /etc/sudoers.d/', 'B) /etc/sudo.conf', 'C) ~/.sudorc', 'D) /etc/pam.d/sudo'],
                correct     = 'A',
                explanation = '/etc/sudoers (bearbeiten NUR mit visudo!). /etc/sudoers.d/ für zusätzliche Dateien.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was macht visudo besonders sicher?',
                options     = ['A) Verschlüsselt die sudoers-Datei', 'B) Prüft Syntax vor dem Speichern (verhindert kaputte sudo-Config)', 'C) Erstellt Backup automatisch', 'D) Setzt Rechte automatisch'],
                correct     = 'B',
                explanation = 'visudo prüft Syntax vor Speicherung. Kaputte sudoers = kein sudo mehr = gesperrt!',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PAM PRÜFUNGS-SCHWERPUNKTE:\n"
            "  Die 4 Typen: auth account password session\n"
            "  required vs requisite: beide müssen erfüllt sein,\n"
            "  aber requisite bricht sofort ab bei Fehler!"
        ),
        memory_tip   = "Merkhilfe: PAM = 4 Typen (auth account password session) × 4 Controls",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.07 — Umgebungsvariablen & Profile-Dateien
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.07",
        chapter      = 10,
        title        = "Login-Shells & Profile-Dateien",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Wann lädt bash ~/.bashrc? Wann ~/.bash_profile?\n"
            " Ghost, das ist eine der häufigsten Prüfungsfallen.\n"
            " Login-Shell vs interaktive Shell — kenn den Unterschied.\n"
            " Falsch konfiguriert — deine Umgebung startet nicht.'"
        ),
        why_important = (
            "Profile-Dateien steuern die Benutzerumgebung.\n"
            "LPIC-1 testet welche Datei wann geladen wird — häufige Prüfungsfrage!"
        ),
        explanation  = (
            "BASH START-DATEIEN:\n\n"
            "LOGIN-SHELL (ssh, su -, Konsolen-Login):\n"
            "  /etc/profile          systemweit (zuerst)\n"
            "  /etc/profile.d/*.sh   systemweite Fragmente\n"
            "  ~/.bash_profile       user-spezifisch (bevorzugt)\n"
            "  ~/.bash_login         falls .bash_profile nicht existiert\n"
            "  ~/.profile            falls .bash_login nicht existiert\n\n"
            "INTERAKTIVE NICHT-LOGIN-SHELL (Terminal öffnen, bash starten):\n"
            "  /etc/bash.bashrc      systemweit\n"
            "  ~/.bashrc             user-spezifisch\n\n"
            "LOGOUT:\n"
            "  ~/.bash_logout        beim Abmelden (Login-Shell)\n\n"
            "NICHT-INTERAKTIV (Skripte, Cron):\n"
            "  Keine ~/.bashrc oder ~/.bash_profile!\n"
            "  Nur $BASH_ENV wenn gesetzt\n\n"
            "TYPISCHES PATTERN:\n"
            "  ~/.bash_profile ruft ~/.bashrc auf:\n"
            "  [[ -f ~/.bashrc ]] && source ~/.bashrc\n\n"
            "SYSTEMWEITE KONFIGURATION:\n"
            "  /etc/environment      systemweite Umgebungsvariablen\n"
            "  /etc/profile          Login-Shell systemweit\n"
            "  /etc/bash.bashrc      interaktive Shell systemweit\n"
            "  /etc/skel/            Vorlage für neue Benutzer-Home-Verzeichnisse"
        ),
        syntax       = "source ~/.bashrc  |  . ~/.bash_profile  |  cat /etc/profile",
        example      = (
            "cat ~/.bashrc\n"
            "cat ~/.bash_profile\n"
            "cat /etc/profile\n"
            "ls /etc/profile.d/\n"
            "source ~/.bashrc       # Konfiguration neu laden\n"
            ". ~/.bash_profile      # Punkt = source"
        ),
        task_description = "Zeige den Inhalt der systemweiten /etc/profile",
        expected_commands = ["cat /etc/profile"],
        hint_text    = "/etc/profile wird für alle Login-Shells geladen (systemweit)",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist getent?',
                options     = ['A) Holt Einträge aus Datenbanken (passwd, group, hosts) inkl. LDAP/NIS', 'B) Gibt Umgebungsvariablen aus', 'C) Zeigt Netzwerk-Entitäten', 'D) Listet Benutzer-Entitlements'],
                correct     = 'A',
                explanation = 'getent = get entries. getent passwd username zeigt Benutzerinfos aus allen konfigurierten Quellen (lokal + LDAP).',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGS-FALLE:\n"
            "  SSH-Login lädt: /etc/profile, dann ~/.bash_profile\n"
            "  Terminal öffnen lädt: ~/.bashrc\n"
            "  Skript: nichts automatisch!\n"
            "/etc/skel/ = Template für neue Benutzer"
        ),
        memory_tip   = "Merkhilfe: Login=bash_profile, Non-Login=bashrc",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.08 — /etc/shadow Format
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.08",
        chapter      = 10,
        title        = "/etc/shadow Format — 9 Felder & Passwort-Hash",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'Das Passwort-Archiv des Imperiums, Ghost.\n"
            " /etc/shadow — nur root kann es lesen.\n"
            " Neun Felder. Jedes zählt.\n"
            " Wer das Format kennt, kennt die Sicherheitsstufe des Systems.'"
        ),
        why_important = (
            "/etc/shadow-Format ist LPIC-1 Topic 107.1 Pflichtinhalt.\n"
            "Die 9 Felder und ihre Bedeutung werden in Prüfungen direkt abgefragt.\n"
            "chage -l zeigt die Shadow-Informationen lesbar an."
        ),
        explanation  = (
            "/ETC/SHADOW — FORMAT (9 Felder durch ':' getrennt):\n\n"
            "  user:$hash:last:min:max:warn:inactive:expire:reserved\n\n"
            "FELDER IM DETAIL:\n"
            "  1  Benutzername\n"
            "  2  Passwort-Hash ($ID$salt$hash)\n"
            "     $1$  = MD5 (veraltet)\n"
            "     $5$  = SHA-256\n"
            "     $6$  = SHA-512 (Standard)\n"
            "     $y$  = yescrypt (modern)\n"
            "     !    = Account gesperrt\n"
            "     *    = kein Passwort-Login\n"
            "  3  Datum der letzten Passwort-Änderung\n"
            "     (Tage seit 01.01.1970)\n"
            "  4  Minimum-Tage (bevor Passwort geändert werden darf)\n"
            "     0 = keine Mindestdauer\n"
            "  5  Maximum-Tage (Passwort läuft nach X Tagen ab)\n"
            "     99999 = läuft nie ab\n"
            "  6  Warn-Tage (X Tage vor Ablauf wird gewarnt)\n"
            "  7  Inaktiv-Tage (nach Ablauf bis Account gesperrt)\n"
            "  8  Account-Ablaufdatum (Tage seit 01.01.1970, leer=kein Ablauf)\n"
            "  9  Reserviert (immer leer)\n\n"
            "BEISPIEL:\n"
            "  ghost:$6$salt$hash:19800:0:99999:7:::\n"
            "  → SHA-512-Hash, 0 Min-Tage, 99999 Max, 7 Warn-Tage, kein Ablauf\n\n"
            "CHAGE -L AUSGABE:\n"
            "  chage -l ghost     zeigt Shadow-Felder lesbar\n"
            "  chage -d 0 ghost   Passwort sofort ablaufen lassen"
        ),
        syntax       = "chage -l USER  |  sudo grep USER /etc/shadow",
        example      = (
            "sudo grep ghost /etc/shadow\n"
            "chage -l ghost\n"
            "# Passwort-Hash-Präfixe erkennen:\n"
            "sudo grep ghost /etc/shadow | cut -d: -f2 | cut -c1-3\n"
            "# Alle gesperrten Accounts:\n"
            "sudo grep '^[^:]*:!' /etc/shadow"
        ),
        task_description = "Zeige die Passwort-Aging-Informationen für den Benutzer 'root'",
        expected_commands = ["chage -l root"],
        hint_text    = "chage -l USER zeigt alle Shadow-Felder lesbar an (Last change, expires etc.)",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bedeutet '!' am Anfang des Passwort-Hash-Feldes in /etc/shadow?",
                options    = [
                    "Kein Passwort gesetzt",
                    "Account ist gesperrt (locked)",
                    "Passwort ist abgelaufen",
                    "SHA-256-Hash",
                ],
                correct    = 1,
                explanation = (
                    "! = Account ist gesperrt. Der Hash ist vorhanden aber\n"
                    "das Login ist blockiert (wie passwd -l).\n"
                    "* = kein Passwort-Login möglich (Service-Accounts)."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was bedeutet '99999' im Max-Tage-Feld (Feld 5) von /etc/shadow?",
                options    = [
                    "Passwort läuft nach 99999 Tagen ab",
                    "Passwort läuft nie ab",
                    "Account ist für 99999 Tage gesperrt",
                    "Feld ist nicht gesetzt",
                ],
                correct    = 1,
                explanation = (
                    "99999 Tage = ca. 274 Jahre = Passwort läuft nie ab.\n"
                    "Ein leeres Feld oder 99999 bedeuten kein Ablauf.\n"
                    "chage -l zeigt dies als 'Password expires: never'."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 /etc/shadow Pflicht:\n"
            "  9 Felder kennen: user:hash:last:min:max:warn:inactive:expire:reserved\n"
            "  $6$ = SHA-512 (Standard), $1$ = MD5 (veraltet)\n"
            "  ! = gesperrt, * = kein Login\n"
            "  chage -l zeigt die Felder lesbar"
        ),
        memory_tip   = "Merkhilfe: shadow = 9 Felder. Felder 3-8 = Datums/Tages-Werte",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.09 — chage
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.09",
        chapter      = 10,
        title        = "chage — Passwort-Ablauf konfigurieren",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Der neue Operator hat ein dauerhaftes Passwort, Ghost.\n"
            " Das ist ein Sicherheitsrisiko.\n"
            " chage erzwingt Rotation — alle 90 Tage.\n"
            " 14 Tage Warnung. Minimum 7 Tage. So läuft das im Team.'"
        ),
        why_important = (
            "chage ist das Tool für Passwort-Policy-Verwaltung.\n"
            "LPIC-1 Topic 107.1 prüft chage-Flags und ihre Bedeutung.\n"
            "Passwort-Aging ist Sicherheitsstandard in Unternehmensumgebungen."
        ),
        explanation  = (
            "CHAGE — CHANGE AGE (Passwort-Ablauf verwalten):\n\n"
            "ANZEIGEN:\n"
            "  chage -l USER         alle Passwort-Aging-Infos\n\n"
            "SETZEN:\n"
            "  chage -M 90 USER      Maximum: Passwort läuft nach 90 Tagen ab\n"
            "  chage -m 7 USER       Minimum: erst nach 7 Tagen änderbar\n"
            "  chage -W 14 USER      Warnung: 14 Tage vor Ablauf\n"
            "  chage -I 30 USER      Inaktiv: Account 30 Tage nach Ablauf sperren\n"
            "  chage -E 2025-12-31 USER  Account-Ablauf: Datum setzen\n"
            "  chage -E -1 USER      Account-Ablauf entfernen (-1 = nie)\n"
            "  chage -d 0 USER       Sofortige Passwort-Änderung erzwingen\n"
            "  chage -d -1 USER      Datum der letzten Änderung zurücksetzen\n\n"
            "KOMBINATIONEN:\n"
            "  chage -M 90 -m 7 -W 14 -I 30 ghost\n"
            "  → Max 90 Tage, Min 7 Tage, 14 Tage Warnung, 30 Tage Inaktiv\n\n"
            "INTERAKTIV:\n"
            "  chage ghost   (ohne Flags) → interaktiver Modus\n\n"
            "IN /ETC/LOGIN.DEFS:\n"
            "  PASS_MAX_DAYS  99999    systemweites Maximum\n"
            "  PASS_MIN_DAYS  0        systemweites Minimum\n"
            "  PASS_WARN_AGE  7        systemweite Warnung\n"
            "  (Gilt nur für NEU erstellte Benutzer)"
        ),
        syntax       = "chage [-M max] [-m min] [-W warn] [-E expire] [-d lastday] USER",
        example      = (
            "chage -l ghost\n"
            "chage -M 90 ghost           # Passwort läuft nach 90 Tagen ab\n"
            "chage -m 7 -M 90 -W 14 ghost  # vollständige Policy\n"
            "chage -d 0 ghost            # sofortige Änderung erzwingen\n"
            "chage -E 2025-12-31 ghost   # Account bis Ende 2025\n"
            "chage -E -1 ghost           # kein Account-Ablauf"
        ),
        task_description = "Setze für Benutzer 'ghost' ein Passwort-Maximum von 90 Tagen",
        expected_commands = ["chage -M 90 ghost"],
        hint_text    = "chage -M setzt die Maximum-Tage bis zur Passwort-Änderung",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt 'chage -d 0 ghost'?",
                options    = [
                    "Setzt das Passwort auf 0 Tage Gültigkeit",
                    "Erzwingt sofortige Passwort-Änderung beim nächsten Login",
                    "Sperrt den Account ghost",
                    "Löscht das Passwort-Ablaufdatum",
                ],
                correct    = 1,
                explanation = (
                    "chage -d 0 setzt das Datum der letzten Passwort-Änderung auf 0\n"
                    "(= 01.01.1970). Das Passwort gilt sofort als abgelaufen.\n"
                    "Beim nächsten Login muss das Passwort geändert werden."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welches chage-Flag setzt die Anzahl der Warn-Tage vor Passwort-Ablauf?",
                options    = [
                    "chage -M",
                    "chage -m",
                    "chage -W",
                    "chage -I",
                ],
                correct    = 2,
                explanation = (
                    "-W = Warn-Tage vor Ablauf (Warning).\n"
                    "-M = Maximum-Tage (max. Gültigkeit).\n"
                    "-m = Minimum-Tage (min. vor Änderung erlaubt).\n"
                    "-I = Inaktiv-Tage nach Ablauf."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 chage Flags:\n"
            "  -M = Max (maximum days)\n"
            "  -m = min (minimum days)\n"
            "  -W = Warn (warning days)\n"
            "  -I = Inactive (days after expire)\n"
            "  -E = Expire (account expiry date)\n"
            "  -d 0 = sofortige Passwort-Änderung erzwingen"
        ),
        memory_tip   = "Merkhilfe: chage M=Max m=min W=Warn I=Inactive E=Expire d=date",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.10 — sudo Konfiguration
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.10",
        chapter      = 10,
        title        = "sudo Konfiguration — /etc/sudoers, visudo & Aliases",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'sudo ist Macht, Ghost.\n"
            " Aber unkontrollierte Macht ist Gefahr.\n"
            " /etc/sudoers mit NOPASSWD öffnet Türen.\n"
            " Gruppen-Aliases machen es wartbar. Kenn beides.'"
        ),
        why_important = (
            "/etc/sudoers-Syntax ist LPIC-1 Topic 107.2 Kerninhalt.\n"
            "NOPASSWD, Gruppen-Regeln und Aliases werden in Prüfungen geprüft.\n"
            "visudo ist der EINZIGE sichere Weg zur Bearbeitung."
        ),
        explanation  = (
            "SUDO-KONFIGURATION — /ETC/SUDOERS:\n\n"
            "GRUNDREGEL-FORMAT:\n"
            "  WHO  WHERE = (AS_WHO) WHAT\n\n"
            "BEISPIELE:\n"
            "  root    ALL=(ALL:ALL) ALL    root darf alles\n"
            "  ghost   ALL=(ALL:ALL) ALL    ghost wie root\n"
            "  %sudo   ALL=(ALL:ALL) ALL    sudo-Gruppe\n"
            "  %admin  ALL=(ALL) ALL        admin-Gruppe\n\n"
            "NOPASSWD:\n"
            "  ghost ALL=(ALL) NOPASSWD:ALL         kein Passwort\n"
            "  ghost ALL=(ALL) NOPASSWD:/sbin/reboot  nur reboot\n\n"
            "ALIASES:\n"
            "  User_Alias  ADMINS = ghost, zara\n"
            "  Runas_Alias OPERATORS = root, admin\n"
            "  Host_Alias  SERVERS = server1, server2\n"
            "  Cmnd_Alias  NETWORKING = /sbin/ip, /sbin/ifconfig\n\n"
            "  ADMINS SERVERS = (OPERATORS) NETWORKING\n\n"
            "SUDOERS.D:\n"
            "  #includedir /etc/sudoers.d\n"
            "  → Einzeldateien in /etc/sudoers.d/ werden eingelesen\n"
            "  Sicherer: eigene Datei pro Service/User\n\n"
            "VISUDO:\n"
            "  visudo            editiert /etc/sudoers sicher\n"
            "  visudo -c         nur Syntax prüfen\n"
            "  visudo -f /etc/sudoers.d/ghost  andere Datei\n\n"
            "SUDO-LOGGING:\n"
            "  /var/log/auth.log   sudo-Events (Debian)\n"
            "  /var/log/secure     sudo-Events (RHEL)"
        ),
        syntax       = "visudo  |  sudo -l  |  sudo -l -U USER",
        example      = (
            "visudo\n"
            "visudo -c                   # Syntax prüfen\n"
            "sudo -l                     # eigene Rechte\n"
            "sudo -l -U ghost            # Rechte von ghost\n"
            "# In /etc/sudoers:\n"
            "# ghost ALL=(ALL) NOPASSWD:ALL\n"
            "# %developers ALL=(ALL) /usr/bin/systemctl restart *"
        ),
        task_description = "Zeige alle sudo-Rechte für den aktuellen Benutzer",
        expected_commands = ["sudo -l"],
        hint_text    = "sudo -l listet alle Befehle die der aktuelle User mit sudo ausführen darf",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bedeutet 'NOPASSWD:ALL' in einer sudoers-Regel?",
                options    = [
                    "Der User kann alle Befehle ohne root-Rechte ausführen",
                    "Der User kann sudo ohne Passwort-Eingabe nutzen",
                    "Alle Users können ohne Passwort sudo nutzen",
                    "Das Passwort wird nicht gespeichert",
                ],
                correct    = 1,
                explanation = (
                    "NOPASSWD: bedeutet sudo fragt NICHT nach dem Passwort.\n"
                    "ALL nach NOPASSWD: heißt alle Befehle.\n"
                    "Nützlich für Automatisierung, aber Sicherheitsrisiko!"
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welches sudo-Alias-Schlüsselwort definiert eine Gruppe von Befehlen?",
                options    = [
                    "User_Alias",
                    "Host_Alias",
                    "Cmnd_Alias",
                    "Run_Alias",
                ],
                correct    = 2,
                explanation = (
                    "Cmnd_Alias (Command Alias) definiert Gruppen von Befehlen.\n"
                    "User_Alias = Benutzergruppen, Host_Alias = Hostgruppen.\n"
                    "Beispiel: Cmnd_Alias SERVICES = /sbin/service, /bin/systemctl"
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 sudoers Basics:\n"
            "  FORMAT: WHO WHERE=(AS) WHAT\n"
            "  %gruppe = Gruppe (mit %)\n"
            "  NOPASSWD: = kein Passwort\n"
            "  Aliases: User_Alias Cmnd_Alias Host_Alias Runas_Alias\n"
            "  NIEMALS direkt bearbeiten — immer visudo!"
        ),
        memory_tip   = "Merkhilfe: visudo=sicher, %gruppe=Gruppe, NOPASSWD=kein Passwort",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.11 — su vs sudo
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.11",
        chapter      = 10,
        title        = "su vs sudo — Unterschied & Umgebungsvariablen",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'su oder sudo — das ist die Frage, Ghost.\n"
            " su gibt dir eine Shell als anderer User.\n"
            " sudo führt EINEN Befehl mit anderen Rechten aus.\n"
            " Der Unterschied liegt in den Umgebungsvariablen — und der Kontrolle.'"
        ),
        why_important = (
            "su vs sudo ist ein klassisches LPIC-1-Prüfungsthema.\n"
            "Der Unterschied in der Umgebung (PATH, HOME) ist prüfungsrelevant.\n"
            "sudo -i vs sudo -s — beide für verschiedene Anwendungsfälle."
        ),
        explanation  = (
            "SU — SWITCH USER:\n\n"
            "  su              zu root wechseln (Passwort von root)\n"
            "  su -            Login-Shell als root (Umgebung NEU)\n"
            "  su ghost        zu ghost wechseln\n"
            "  su - ghost      Login-Shell als ghost\n"
            "  su -c 'cmd'     Befehl als root ausführen\n\n"
            "SU vs SU -:\n"
            "  su             Shell als root, ABER alte Umgebung (PATH etc.)\n"
            "  su -           Login-Shell: /etc/profile, ~/.bash_profile geladen\n"
            "                 HOME, PATH, USER werden neu gesetzt\n\n"
            "SUDO:\n\n"
            "  sudo CMD        einen Befehl als root (eigenes Passwort!)\n"
            "  sudo -i         Login-Shell als root (wie su -)\n"
            "  sudo -s         Shell mit aktueller Umgebung (wie su)\n"
            "  sudo -u ghost CMD   Befehl als ghost ausführen\n"
            "  sudo -l         eigene sudo-Rechte anzeigen\n\n"
            "UNTERSCHIEDE:\n"
            "  su benötigt root-Passwort\n"
            "  sudo benötigt das EIGENE Passwort\n"
            "  sudo loggt alle Aktionen\n"
            "  sudo ist granularer konfigurierbar\n\n"
            "UMGEBUNGSVARIABLEN:\n"
            "  sudo -i: HOME=/root, PATH=/usr/sbin:... (root-Umgebung)\n"
            "  sudo -s: HOME bleibt, PATH von sudo\n"
            "  sudo CMD: minimale Umgebung (secure_path aus sudoers)\n"
            "  sudo -E CMD: aktuelle Umgebung ÜBERNEHMEN (Environment)"
        ),
        syntax       = "su - USER  |  sudo -i  |  sudo -s  |  sudo -u USER CMD",
        example      = (
            "su -                    # Login-Shell als root\n"
            "su - ghost              # Login-Shell als ghost\n"
            "su -c 'cat /etc/shadow' # einmal root-Befehl\n"
            "sudo -i                 # root Login-Shell (empfohlen)\n"
            "sudo -s                 # root Shell, eigene Umgebung\n"
            "sudo -u postgres psql   # als postgres-User\n"
            "sudo -E env | grep PATH # Umgebung mit sudo"
        ),
        task_description = "Starte eine Login-Shell als root mit sudo",
        expected_commands = ["sudo -i"],
        hint_text    = "sudo -i öffnet eine Login-Shell als root (entspricht su -) mit eigenem Passwort",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Hauptunterschied zwischen 'su' und 'su -'?",
                options    = [
                    "Kein Unterschied",
                    "su - lädt die Login-Shell-Umgebung (PATH, HOME neu gesetzt)",
                    "su - erfordert kein root-Passwort",
                    "su - ist veraltet",
                ],
                correct    = 1,
                explanation = (
                    "su - (Login-Shell): /etc/profile und ~/.bash_profile werden geladen.\n"
                    "HOME, PATH, USER werden auf root gesetzt.\n"
                    "su (ohne -): Shell als root, aber alte Umgebungsvariablen bleiben."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was ist der Vorteil von sudo gegenüber su?",
                options    = [
                    "sudo ist schneller",
                    "sudo benötigt kein Passwort",
                    "sudo loggt Aktionen und benötigt nur das eigene Passwort",
                    "sudo kann nur root ausführen",
                ],
                correct    = 2,
                explanation = (
                    "sudo benötigt nur das eigene Passwort (nicht root-Passwort).\n"
                    "sudo loggt alle Aktionen in /var/log/auth.log.\n"
                    "sudo ist granularer konfigurierbar als su."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 su vs sudo:\n"
            "  su = root-Passwort nötig\n"
            "  sudo = eigenes Passwort + sudoers-Eintrag\n"
            "  su - = Login-Shell (neue Umgebung)\n"
            "  sudo -i = Login-Shell als root (empfohlen)\n"
            "  sudo -s = Shell mit aktueller Umgebung"
        ),
        memory_tip   = "Merkhilfe: su=switch user (root-PW), sudo=do as super (eigenes PW), -=Login",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.12 — gpasswd & Gruppen verwalten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.12",
        chapter      = 10,
        title        = "gpasswd — Gruppen-Mitglieder & Admins verwalten",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'Das Net-Runner-Team braucht neue Mitglieder, Ghost.\n"
            " gpasswd -a fügt hinzu. gpasswd -d entfernt.\n"
            " gpasswd -A macht jemanden zum Gruppen-Admin.\n"
            " Kein root nötig — wenn man Gruppen-Admin ist.'"
        ),
        why_important = (
            "gpasswd ist das Spezialtool für Gruppen-Mitgliedschaft.\n"
            "LPIC-1 prüft gpasswd -a, -d, -M und -A.\n"
            "Gruppen-Admins können Mitglieder ohne root-Rechte verwalten."
        ),
        explanation  = (
            "GPASSWD — GRUPPEN-PASSWORT & MITGLIEDSCHAFT:\n\n"
            "MITGLIEDER VERWALTEN:\n"
            "  gpasswd -a USER GROUP      User zur Gruppe hinzufügen (add)\n"
            "  gpasswd -d USER GROUP      User aus Gruppe entfernen (delete)\n"
            "  gpasswd -M user1,user2 GROUP  Mitgliederliste setzen (ERSETZT!)\n\n"
            "GRUPPEN-ADMINS:\n"
            "  gpasswd -A USER GROUP      User zum Gruppen-Admin machen\n"
            "  → Gruppen-Admins können Mitglieder mit gpasswd verwalten\n"
            "     ohne root zu sein!\n\n"
            "GRUPPEN-PASSWORT:\n"
            "  gpasswd GROUP              Gruppen-Passwort setzen\n"
            "  gpasswd -r GROUP           Gruppen-Passwort entfernen\n"
            "  → selten genutzt (newgrp braucht Gruppen-PW)\n\n"
            "VERGLEICH: gpasswd vs usermod:\n"
            "  gpasswd -a ghost docker    ≡  usermod -aG docker ghost\n"
            "  Beide fügen ghost zur docker-Gruppe hinzu.\n"
            "  gpasswd -M liste GROUP     ERSETZT alle Mitglieder!\n\n"
            "GRUPPEN ANZEIGEN:\n"
            "  groups ghost               Gruppen von ghost\n"
            "  id ghost                   UID + alle Gruppen\n"
            "  getent group docker        docker-Gruppe + Mitglieder\n"
            "  cat /etc/group | grep ghost  alle Gruppen mit ghost"
        ),
        syntax       = "gpasswd -a USER GROUP  |  gpasswd -d USER GROUP  |  gpasswd -A ADMIN GROUP",
        example      = (
            "gpasswd -a ghost docker        # ghost zu docker hinzufügen\n"
            "gpasswd -d ghost docker        # ghost aus docker entfernen\n"
            "gpasswd -A ghost developers    # ghost = Gruppen-Admin\n"
            "gpasswd -M ghost,zara,cipher developers  # Mitgliederliste setzen\n"
            "groups ghost\n"
            "getent group docker"
        ),
        task_description = "Füge den Benutzer 'ghost' zur Gruppe 'developers' hinzu mit gpasswd",
        expected_commands = ["gpasswd -a ghost developers"],
        hint_text    = "gpasswd -a USER GROUP fügt den User zur Gruppe hinzu (add)",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen 'gpasswd -a' und 'gpasswd -M'?",
                options    = [
                    "Kein Unterschied",
                    "-a fügt einen User hinzu, -M setzt die komplette Mitgliederliste (ersetzt!)",
                    "-a für Admins, -M für Members",
                    "-M fügt hinzu, -a ersetzt",
                ],
                correct    = 1,
                explanation = (
                    "gpasswd -a USER: fügt einen User hinzu (append).\n"
                    "gpasswd -M user1,user2: ERSETZT alle Mitglieder!\n"
                    "Vorsicht mit -M — bestehende Mitglieder werden entfernt."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Was ermöglicht gpasswd -A USER GROUP?",
                options    = [
                    "Fügt USER als Admin des Systems hinzu",
                    "Macht USER zum Gruppen-Admin (kann Mitglieder verwalten)",
                    "Gibt USER alle Admin-Rechte",
                    "Fügt USER zur Admin-Gruppe hinzu",
                ],
                correct    = 1,
                explanation = (
                    "gpasswd -A macht einen User zum Gruppen-Administrator.\n"
                    "Gruppen-Admins können Mitglieder mit gpasswd -a/-d verwalten\n"
                    "ohne selbst root-Rechte zu haben."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 gpasswd:\n"
            "  -a = add (hinzufügen)\n"
            "  -d = delete (entfernen)\n"
            "  -M = Members setzen (ERSETZT!)\n"
            "  -A = Admin setzen\n"
            "  gpasswd -a ghost docker ≡ usermod -aG docker ghost"
        ),
        memory_tip   = "Merkhilfe: gpasswd = group password. -a=add -d=delete -M=Members -A=Admin",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.13 — /etc/skel
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.13",
        chapter      = 10,
        title        = "/etc/skel — Standard-Dateien für neue Benutzer",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Jeder neue Operator bekommt die gleiche Basis-Konfiguration.\n"
            " .bashrc. .profile. Unsere Standard-Aliases.\n"
            " /etc/skel ist die Vorlage — alle neuen Homes werden von hier kopiert.\n"
            " Einmal richtig konfiguriert — alle profitieren.'"
        ),
        why_important = (
            "/etc/skel ist LPIC-1 Topic 107.1 Prüfungsstoff.\n"
            "Dateien in /etc/skel werden bei useradd -m in das neue Home kopiert.\n"
            "Systemweite Default-Konfigurationen für alle neuen User."
        ),
        explanation  = (
            "/ETC/SKEL — SKELETON-VERZEICHNIS:\n\n"
            "FUNKTION:\n"
            "  Enthält Template-Dateien für neue Benutzer-Home-Verzeichnisse.\n"
            "  Bei useradd -m werden alle Dateien aus /etc/skel\n"
            "  in das neue Home-Verzeichnis kopiert.\n\n"
            "STANDARD-DATEIEN:\n"
            "  /etc/skel/.bashrc        bash-Konfiguration\n"
            "  /etc/skel/.bash_profile  Login-Shell-Konfiguration\n"
            "  /etc/skel/.bash_logout   Logout-Skript\n"
            "  /etc/skel/.profile       POSIX-Shell-Profil\n\n"
            "ANPASSEN:\n"
            "  Dateien in /etc/skel bearbeiten → alle künftigen User erhalten sie\n"
            "  Berechtigungen in /etc/skel werden für neue Home kopiert\n"
            "  Symlinks werden NICHT als Symlinks kopiert (dereferenziert)\n\n"
            "ANWENDUNGSBEISPIELE:\n"
            "  Firmen-Aliases in .bashrc hinterlegen\n"
            "  Standard .vimrc für alle User\n"
            "  Security-Policy-Hinweise in .bash_profile\n\n"
            "USERADD UND SKEL:\n"
            "  useradd -m ghost        → /etc/skel wird nach /home/ghost kopiert\n"
            "  useradd -k /etc/skel2   → anderes Skel-Verzeichnis\n"
            "  useradd -M ghost        → KEIN Home (kein skel-Kopieren)\n\n"
            "/ETC/DEFAULT/USERADD:\n"
            "  SKEL=/etc/skel          Standard-Skel-Pfad\n"
            "  HOME=/home              Standard Home-Basis"
        ),
        syntax       = "ls -la /etc/skel  |  cat /etc/skel/.bashrc",
        example      = (
            "ls -la /etc/skel\n"
            "cat /etc/skel/.bashrc\n"
            "cat /etc/skel/.profile\n"
            "# Eigene Datei zu skel hinzufügen:\n"
            "echo 'alias ll=\"ls -la\"' >> /etc/skel/.bashrc\n"
            "# Standard useradd-Einstellungen:\n"
            "cat /etc/default/useradd"
        ),
        task_description = "Zeige alle Dateien in /etc/skel inklusive versteckter Dateien",
        expected_commands = ["ls -la /etc/skel"],
        hint_text    = "ls -la /etc/skel — -l für lange Ausgabe, -a für versteckte Dateien (beginnend mit .)",
        quiz_questions = [
            QuizQuestion(
                question   = "Wann werden Dateien aus /etc/skel in ein Home-Verzeichnis kopiert?",
                options    = [
                    "Bei jedem Login",
                    "Bei useradd -m (Erstellen mit Home-Verzeichnis)",
                    "Bei passwd Befehl",
                    "Beim System-Start",
                ],
                correct    = 1,
                explanation = (
                    "Dateien aus /etc/skel werden bei useradd -m kopiert.\n"
                    "Das -m Flag erstellt das Home-Verzeichnis.\n"
                    "Ohne -m wird kein Home (und kein skel) angelegt."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welche Datei konfiguriert das Standard-Skel-Verzeichnis für useradd?",
                options    = [
                    "/etc/skel/.bashrc",
                    "/etc/default/useradd",
                    "/etc/login.defs",
                    "/etc/passwd",
                ],
                correct    = 1,
                explanation = (
                    "/etc/default/useradd enthält Standard-Einstellungen für useradd.\n"
                    "SKEL=/etc/skel definiert das Template-Verzeichnis.\n"
                    "/etc/login.defs enthält UID/GID-Bereiche und Passwort-Policy."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 /etc/skel:\n"
            "  useradd -m kopiert /etc/skel → neues Home\n"
            "  useradd -k PFAD = alternatives skel\n"
            "  useradd -M = kein Home (kein skel)\n"
            "  /etc/default/useradd = Standard-Einstellungen"
        ),
        memory_tip   = "Merkhilfe: skel = skeleton (Skelett) = Vorlage für neue Home-Verzeichnisse",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.14 — PAM & Authentifizierung (Überblick)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.14",
        chapter      = 10,
        title        = "PAM — Pluggable Authentication Modules (Überblick)",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'PAM ist der unsichtbare Türsteher, Ghost.\n"
            " Jeder Login. Jeder sudo. Jedes su.\n"
            " Alles läuft durch /etc/pam.d/.\n"
            " pam_unix.so prüft das Passwort. pam_cracklib prüft die Qualität.'"
        ),
        why_important = (
            "PAM ist LPIC-1 Topic 107.1/107.2 Prüfungsstoff.\n"
            "Die 4 PAM-Typen und wichtige Module werden in Prüfungen abgefragt.\n"
            "PAM-Konfiguration steuert die gesamte Authentifizierung."
        ),
        explanation  = (
            "PAM — PLUGGABLE AUTHENTICATION MODULES:\n\n"
            "PAM trennt Authentifizierung von Anwendungen.\n"
            "Konfigurationsverzeichnis: /etc/pam.d/\n\n"
            "PAM-ZEILEN-FORMAT:\n"
            "  TYPE  CONTROL  MODULE  [OPTIONEN]\n\n"
            "DIE 4 TYPEN (Management Groups):\n"
            "  auth        Wer bist du? (Passwort prüfen)\n"
            "  account     Darf der Account sich anmelden? (gesperrt? abgelaufen?)\n"
            "  password    Passwort-Änderung\n"
            "  session     Was passiert beim Login/Logout? (Home mounten, Logging)\n\n"
            "CONTROLS:\n"
            "  required    muss OK sein — Fehler sofort aber weiter prüfen\n"
            "  requisite   muss OK sein — Fehler = sofortiger Abbruch\n"
            "  sufficient  reicht bei Erfolg — Rest wird übersprungen\n"
            "  optional    Ergebnis meist egal (für Logging)\n\n"
            "WICHTIGE MODULE:\n"
            "  pam_unix.so       Standard /etc/shadow Auth\n"
            "  pam_cracklib.so   Passwort-Qualität prüfen\n"
            "  pam_pwquality.so  modernerer Ersatz für cracklib\n"
            "  pam_limits.so     Ressource-Limits (/etc/security/limits.conf)\n"
            "  pam_faillock.so   Brute-Force-Schutz (Account sperren)\n"
            "  pam_tty_audit.so  TTY-Logging\n"
            "  pam_nologin.so    /etc/nologin prüfen\n"
            "  pam_env.so        Umgebungsvariablen\n\n"
            "TYPISCHE /etc/pam.d/login:\n"
            "  auth    required  pam_unix.so\n"
            "  account required  pam_unix.so\n"
            "  session required  pam_unix.so"
        ),
        syntax       = "ls /etc/pam.d/  |  cat /etc/pam.d/sshd  |  cat /etc/pam.d/login",
        example      = (
            "ls /etc/pam.d/\n"
            "cat /etc/pam.d/sshd\n"
            "cat /etc/pam.d/sudo\n"
            "cat /etc/pam.d/login\n"
            "cat /etc/pam.d/common-auth    # Debian\n"
            "cat /etc/pam.d/system-auth    # RHEL"
        ),
        task_description = "Zeige die PAM-Konfiguration für SSH (/etc/pam.d/sshd)",
        expected_commands = ["cat /etc/pam.d/sshd"],
        hint_text    = "cat /etc/pam.d/sshd zeigt welche PAM-Module SSH für die Authentifizierung nutzt",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher PAM-Control bricht die Authentifizierung SOFORT ab bei Fehler?",
                options    = [
                    "required",
                    "optional",
                    "requisite",
                    "sufficient",
                ],
                correct    = 2,
                explanation = (
                    "requisite: Bei Fehler sofortiger Abbruch der PAM-Kette.\n"
                    "required: Fehler wird registriert, aber PAM-Kette läuft weiter.\n"
                    "sufficient: Bei Erfolg wird Rest übersprungen."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welches PAM-Modul prüft Passwort-Qualität (Komplexität)?",
                options    = [
                    "pam_unix.so",
                    "pam_limits.so",
                    "pam_cracklib.so",
                    "pam_nologin.so",
                ],
                correct    = 2,
                explanation = (
                    "pam_cracklib.so (und moderner: pam_pwquality.so) prüft Passwort-Qualität.\n"
                    "pam_unix.so = Standard-Auth (/etc/shadow).\n"
                    "pam_limits.so = Ressource-Limits, pam_nologin.so = /etc/nologin."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 PAM:\n"
            "  4 Typen: auth account password session\n"
            "  required vs requisite: beide müssen OK sein,\n"
            "  aber requisite bricht sofort ab!\n"
            "  pam_unix.so = Standard-Auth\n"
            "  pam_cracklib.so = Passwort-Qualität"
        ),
        memory_tip   = "Merkhilfe: PAM = auth(wer) account(darf) password(ändern) session(was passiert)",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.15 — nsswitch.conf
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.15",
        chapter      = 10,
        title        = "nsswitch.conf — Namensauflösung für passwd, group, hosts",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA_Z3R0",
        story        = (
            "Zara Z3R0: 'Das System sucht den User 'agent', Ghost.\n"
            " Aber wo sucht es? /etc/passwd? LDAP? NIS?\n"
            " nsswitch.conf ist die Weiche.\n"
            " Es bestimmt die Reihenfolge — für alles.'"
        ),
        why_important = (
            "nsswitch.conf ist LPIC-1 Topic 107.1 Prüfungsstoff.\n"
            "Die Auflösungsreihenfolge für passwd, group und hosts wird geprüft.\n"
            "In Unternehmensnetzen mit LDAP/NIS ist nsswitch kritisch."
        ),
        explanation  = (
            "/ETC/NSSWITCH.CONF — NAME SERVICE SWITCH:\n\n"
            "FUNKTION:\n"
            "  Steuert die Reihenfolge der Datenquellen für verschiedene Datenbanken.\n\n"
            "DATENBANKEN:\n"
            "  passwd   Benutzerinformationen (/etc/passwd, LDAP, NIS)\n"
            "  group    Gruppeninformationen (/etc/group)\n"
            "  shadow   Passwort-Hashes (/etc/shadow)\n"
            "  hosts    Hostname-Auflösung (/etc/hosts, DNS)\n"
            "  networks Netzwerk-Namen\n"
            "  services Dienst-Port-Mapping (/etc/services)\n"
            "  protocols Protokoll-Nummern\n\n"
            "QUELLEN:\n"
            "  files    lokale Dateien (/etc/passwd, /etc/hosts etc.)\n"
            "  dns      DNS-Server\n"
            "  ldap     LDAP-Verzeichnis\n"
            "  nis      NIS/YP\n"
            "  systemd  systemd-resolved, systemd-nss\n"
            "  myhostname  nur für hosts (eigener Hostname)\n\n"
            "TYPISCHE KONFIGURATION:\n"
            "  passwd:   files systemd\n"
            "  group:    files systemd\n"
            "  shadow:   files\n"
            "  hosts:    files dns myhostname\n"
            "  services: files\n\n"
            "MIT LDAP:\n"
            "  passwd:   files ldap\n"
            "  group:    files ldap\n"
            "  → erst lokale /etc/passwd, dann LDAP"
        ),
        syntax       = "cat /etc/nsswitch.conf  |  grep passwd /etc/nsswitch.conf",
        example      = (
            "cat /etc/nsswitch.conf\n"
            "grep '^passwd' /etc/nsswitch.conf\n"
            "grep '^hosts' /etc/nsswitch.conf\n"
            "grep '^group' /etc/nsswitch.conf\n"
            "# getent nutzt nsswitch.conf:\n"
            "getent passwd ghost\n"
            "getent group docker"
        ),
        task_description = "Zeige die passwd-Auflösungsreihenfolge aus /etc/nsswitch.conf",
        expected_commands = ["grep '^passwd' /etc/nsswitch.conf"],
        hint_text    = "grep '^passwd' /etc/nsswitch.conf zeigt welche Quellen für Benutzer genutzt werden",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bedeutet 'passwd: files ldap' in /etc/nsswitch.conf?",
                options    = [
                    "Erst LDAP, dann lokale Dateien",
                    "Erst lokale Dateien (/etc/passwd), dann LDAP",
                    "Nur LDAP wird genutzt",
                    "files und ldap werden gleichzeitig gefragt",
                ],
                correct    = 1,
                explanation = (
                    "Die Reihenfolge von links nach rechts ist die Suchreihenfolge.\n"
                    "'files ldap' = erst /etc/passwd, dann LDAP.\n"
                    "Bei Treffer in 'files' wird LDAP nicht mehr befragt."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welches Tool nutzt /etc/nsswitch.conf um Benutzer aufzulösen?",
                options    = [
                    "grep /etc/passwd",
                    "getent passwd",
                    "cat /etc/passwd",
                    "id",
                ],
                correct    = 1,
                explanation = (
                    "getent nutzt nsswitch.conf für die Auflösung.\n"
                    "getent passwd ghost fragt alle konfigurierten Quellen ab.\n"
                    "grep/cat lesen nur lokale Dateien, ignorieren LDAP/NIS."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 nsswitch.conf:\n"
            "  passwd/group/shadow/hosts = wichtigste Datenbanken\n"
            "  files = lokale Dateien (first)\n"
            "  dns = DNS-Server (für hosts)\n"
            "  ldap = LDAP (Enterprise)\n"
            "  getent = tool das nsswitch.conf respektiert"
        ),
        memory_tip   = "Merkhilfe: nsswitch = wer wird zuerst gefragt. files=lokal, dns/ldap=remote",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.16 — getent
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.16",
        chapter      = 10,
        title        = "getent — Datenbank-Abfragen über nsswitch.conf",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Der User ist in LDAP — nicht in /etc/passwd.\n"
            " grep findet ihn nicht. getent schon.\n"
            " getent passwd fragt ALLE Quellen ab.\n"
            " Das ist der richtige Weg in Unternehmensnetzen.'"
        ),
        why_important = (
            "getent ist LPIC-1 Topic 107.1 Pflicht.\n"
            "Es ist das einzige Tool das alle nsswitch.conf-Quellen nutzt.\n"
            "Für LDAP/NIS-Umgebungen unverzichtbar."
        ),
        explanation  = (
            "GETENT — GET ENTRIES FROM ADMINISTRATIVE DATABASES:\n\n"
            "FUNKTION:\n"
            "  getent nutzt nsswitch.conf und fragt ALLE konfigurierten Quellen ab.\n"
            "  Gegensatz zu grep /etc/passwd: nur lokale Dateien.\n\n"
            "SYNTAX:\n"
            "  getent DATENBANK [KEY]\n\n"
            "DATENBANKEN:\n"
            "  getent passwd             alle Benutzer\n"
            "  getent passwd ghost       Benutzer 'ghost'\n"
            "  getent passwd 1000        User mit UID 1000\n"
            "  getent group              alle Gruppen\n"
            "  getent group docker       Gruppe 'docker' + Mitglieder\n"
            "  getent group 999          Gruppe mit GID 999\n"
            "  getent shadow ghost       Shadow-Eintrag (root nötig)\n"
            "  getent hosts google.com   Hostname auflösen\n"
            "  getent hosts 8.8.8.8      Reverse-Lookup\n"
            "  getent services ssh       Service-Port\n"
            "  getent networks           Netzwerk-Einträge\n\n"
            "AUSGABE-FORMAT:\n"
            "  getent passwd ghost:\n"
            "  ghost:x:1000:1000:Ghost:/home/ghost:/bin/bash\n"
            "  (gleich wie /etc/passwd — aber auch LDAP-User)\n\n"
            "ANWENDUNGSFÄLLE:\n"
            "  User in LDAP prüfen: getent passwd ldap_user\n"
            "  Gruppen mit Mitgliedern: getent group\n"
            "  DNS testen: getent hosts hostname"
        ),
        syntax       = "getent DATENBANK [KEY]",
        example      = (
            "getent passwd ghost\n"
            "getent passwd 0           # root per UID\n"
            "getent group docker       # docker-Gruppe\n"
            "getent shadow ghost       # Shadow-Eintrag\n"
            "getent hosts google.com   # DNS-Lookup via nsswitch\n"
            "getent services ssh\n"
            "getent passwd | grep '/bin/bash'  # User mit bash"
        ),
        task_description = "Zeige den getent-Eintrag für die Gruppe 'root'",
        expected_commands = ["getent group root"],
        hint_text    = "getent group GRUPPENNAME zeigt Gruppeninfo inkl. Mitglieder aus allen Quellen",
        quiz_questions = [
            QuizQuestion(
                question   = "Warum ist 'getent passwd user' besser als 'grep user /etc/passwd'?",
                options    = [
                    "getent ist schneller",
                    "getent nutzt alle nsswitch.conf-Quellen (auch LDAP/NIS)",
                    "grep findet keine Benutzer",
                    "getent verschlüsselt die Ausgabe",
                ],
                correct    = 1,
                explanation = (
                    "getent nutzt alle in nsswitch.conf konfigurierten Quellen.\n"
                    "grep /etc/passwd sucht nur in der lokalen Datei.\n"
                    "In LDAP/NIS-Umgebungen findet grep keine Remote-User."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welcher getent-Befehl löst einen Hostnamen auf?",
                options    = [
                    "getent dns hostname",
                    "getent hosts hostname",
                    "getent resolve hostname",
                    "getent address hostname",
                ],
                correct    = 1,
                explanation = (
                    "getent hosts HOSTNAME nutzt nsswitch.conf für die Auflösung.\n"
                    "Es fragt /etc/hosts und dann DNS ab (je nach Konfiguration).\n"
                    "Gleichwertig zu: nslookup, aber respektiert /etc/hosts."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 getent:\n"
            "  Datenbanken: passwd group shadow hosts services\n"
            "  Nutzt nsswitch.conf = alle Quellen\n"
            "  getent passwd USER = vollständiger Eintrag\n"
            "  getent group GRP = Gruppe + Mitglieder"
        ),
        memory_tip   = "Merkhilfe: getent = GET ENTries. Fragt alles was nsswitch.conf kennt.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.17 — User-Limits & /etc/security/limits.conf
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.17",
        chapter      = 10,
        title        = "User-Limits — /etc/security/limits.conf & ulimit",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Der Imperium-Agent hat zu viele Prozesse gestartet, Ghost.\n"
            " Fork-Bomb. Das System crawlt.\n"
            " limits.conf hätte das verhindert.\n"
            " nproc begrenzt Prozesse. nofile begrenzt offene Dateien.'"
        ),
        why_important = (
            "/etc/security/limits.conf ist LPIC-1 Topic 107.1 Prüfungsstoff.\n"
            "Resource-Limits schützen das System vor einzelnen Users.\n"
            "ulimit zeigt aktuelle Limits in der Shell."
        ),
        explanation  = (
            "/ETC/SECURITY/LIMITS.CONF — RESSOURCE-LIMITS:\n\n"
            "FORMAT:\n"
            "  DOMAIN  TYPE  ITEM  VALUE\n\n"
            "DOMAIN:\n"
            "  ghost          spezifischer Benutzer\n"
            "  @developers    Gruppe\n"
            "  *              alle Benutzer\n\n"
            "TYPE:\n"
            "  soft    weiches Limit (User kann erhöhen bis hard)\n"
            "  hard    hartes Limit (nur root kann erhöhen)\n"
            "  -       gilt für soft UND hard\n\n"
            "ITEMS (wichtigste):\n"
            "  nofile     max. offene Dateien\n"
            "  nproc      max. Prozesse/Threads\n"
            "  stack      Stack-Größe (KB)\n"
            "  fsize      max. Dateigröße (KB)\n"
            "  memlock    max. gesperrter Speicher (KB)\n"
            "  core       Core-Dump-Größe (0=deaktiviert)\n"
            "  cpu        CPU-Zeit (Minuten)\n"
            "  maxlogins  max. gleichzeitige Logins\n\n"
            "BEISPIEL:\n"
            "  *      soft  nofile  1024\n"
            "  *      hard  nofile  4096\n"
            "  ghost  soft  nproc   200\n"
            "  ghost  hard  nproc   400\n"
            "  @dev   -     nofile  8192\n\n"
            "ULIMIT — AKTUELLE LIMITS ANZEIGEN/SETZEN:\n"
            "  ulimit -a            alle Limits anzeigen\n"
            "  ulimit -n            max. offene Dateien\n"
            "  ulimit -u            max. Prozesse\n"
            "  ulimit -n 4096       Limit setzen (temporär)\n"
            "  ulimit -Hn           hartes Limit zeigen\n"
            "  ulimit -Sn           weiches Limit zeigen"
        ),
        syntax       = "ulimit -a  |  cat /etc/security/limits.conf",
        example      = (
            "ulimit -a                    # alle aktuellen Limits\n"
            "ulimit -n                    # offene Dateien\n"
            "ulimit -u                    # max Prozesse\n"
            "cat /etc/security/limits.conf\n"
            "ls /etc/security/limits.d/   # Fragment-Dateien\n"
            "# Limit für Session setzen:\n"
            "ulimit -n 8192"
        ),
        task_description = "Zeige alle aktuellen Resource-Limits der Shell",
        expected_commands = ["ulimit -a"],
        hint_text    = "ulimit -a zeigt alle Ressource-Limits der aktuellen Shell-Session",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen 'soft' und 'hard' Limits in limits.conf?",
                options    = [
                    "Kein Unterschied",
                    "soft = User kann erhöhen bis hard. hard = nur root kann erhöhen.",
                    "soft = temporär, hard = permanent",
                    "hard = für root, soft = für normale User",
                ],
                correct    = 1,
                explanation = (
                    "soft limit: User kann es bis zum hard limit erhöhen.\n"
                    "hard limit: Obergrenze — nur root kann es erhöhen.\n"
                    "Beispiel: soft nofile 1024, hard nofile 4096 → User kann bis 4096."
                ),
                xp_value   = 15,
            ),
            QuizQuestion(
                question   = "Welches limits.conf Item begrenzt die maximale Anzahl von Prozessen?",
                options    = [
                    "maxproc",
                    "nproc",
                    "processes",
                    "pids",
                ],
                correct    = 1,
                explanation = (
                    "nproc = number of processes. Begrenzt Prozesse/Threads pro User.\n"
                    "nofile = number of open files.\n"
                    "nproc verhindert Fork-Bombs von einzelnen Benutzern."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 limits.conf:\n"
            "  Format: DOMAIN TYPE ITEM VALUE\n"
            "  soft=User-änderbar, hard=nur root\n"
            "  nofile=offene Dateien, nproc=Prozesse\n"
            "  ulimit -a = aktuelle Limits anzeigen\n"
            "  PAM lädt Limits: /etc/pam.d/ pam_limits.so"
        ),
        memory_tip   = "Merkhilfe: nofile=offene Dateien, nproc=Prozesse. soft=weich, hard=hart",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.18 — getent & nsswitch
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.18",
        chapter      = 10,
        title        = "getent & nsswitch.conf — Name Service Lookup",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Der Agent ist verwirrt, Ghost — er fragt /etc/passwd,\n"
            " aber die Antwort kommt aus LDAP.\n"
            " nsswitch.conf entscheidet, wo das System sucht.\n"
            " getent zeigt, was das System wirklich sieht.'"
        ),
        why_important = (
            "nsswitch.conf ist LPIC-1 Topic 107.1 Prüfungsstoff.\n"
            "getent ist das universelle Tool für NSS-Abfragen.\n"
            "Verstehe die Lookup-Reihenfolge: files → ldap → dns."
        ),
        explanation  = (
            "NSSWITCH.CONF — NAME SERVICE SWITCH:\n\n"
            "/etc/nsswitch.conf steuert die Suchreihenfolge:\n\n"
            "  passwd:    files systemd\n"
            "  group:     files systemd\n"
            "  shadow:    files\n"
            "  hosts:     files dns myhostname\n"
            "  networks:  files\n\n"
            "DATENBANKEN:\n"
            "  files    → /etc/passwd, /etc/group usw.\n"
            "  dns      → DNS-Server\n"
            "  ldap     → LDAP-Verzeichnis\n"
            "  nis      → NIS/YP-Server\n"
            "  systemd  → systemd-resolved / logind\n\n"
            "GETENT — NSS ABFRAGEN:\n"
            "  getent passwd ghost        Benutzer suchen\n"
            "  getent group sudo          Gruppe suchen\n"
            "  getent hosts example.com   Host auflösen\n"
            "  getent passwd              alle Benutzer (inkl. LDAP)\n"
            "  getent shadow ghost        Shadow-Eintrag"
        ),
        syntax       = "getent DATABASE [KEY]  |  cat /etc/nsswitch.conf",
        example      = (
            "getent passwd ghost          # Benutzer in allen NSS-Quellen\n"
            "getent group developers      # Gruppe suchen\n"
            "getent hosts 8.8.8.8         # Reverse-Lookup\n"
            "cat /etc/nsswitch.conf       # Lookup-Reihenfolge anzeigen\n"
            "getent passwd | wc -l        # alle sichtbaren Benutzer zählen"
        ),
        task_description = "Zeige den passwd-Eintrag für root via getent",
        expected_commands = ["getent passwd root"],
        hint_text    = "getent passwd root fragt alle NSS-Quellen nach dem root-Benutzer ab",
        quiz_questions = [
            QuizQuestion(
                question   = "Was zeigt 'getent passwd' im Vergleich zu 'cat /etc/passwd'?",
                options    = [
                    "Identische Ausgabe",
                    "getent zeigt auch Benutzer aus LDAP/NIS/anderen NSS-Quellen",
                    "getent zeigt nur Systembenutzer",
                    "getent filtert root heraus",
                ],
                correct    = 1,
                explanation = (
                    "getent fragt alle konfigurierten NSS-Quellen ab.\n"
                    "Bei LDAP-Integration zeigt getent auch LDAP-Benutzer.\n"
                    "cat /etc/passwd zeigt nur lokale Einträge."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 nsswitch:\n"
            "  /etc/nsswitch.conf steuert Lookup-Reihenfolge\n"
            "  getent DATABASE [KEY] — universelle NSS-Abfrage\n"
            "  passwd: files ldap → erst lokal, dann LDAP\n"
            "  hosts: files dns → erst /etc/hosts, dann DNS"
        ),
        memory_tip   = "getent = 'get entries' aus allen NSS-Quellen. Universeller als cat /etc/passwd",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.19 — chage & Passwort-Aging
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.19",
        chapter      = 10,
        title        = "chage — Passwort-Aging & Account-Ablauf",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Das Imperium nutzt abgelaufene Accounts, Ghost.\n"
            " Passwörter, die nie ändern. Accounts, die nie sperren.\n"
            " chage setzt Ablaufdaten. passwd -l sperrt sofort.\n"
            " Kontrolliere den Lebenszyklus jedes Accounts.'"
        ),
        why_important = (
            "Passwort-Aging ist LPIC-1 Topic 107.1 Prüfungsstoff.\n"
            "chage und /etc/shadow Felder sind Prüfungsthema.\n"
            "Account-Sicherheit durch zeitgesteuerte Ablaufdaten."
        ),
        explanation  = (
            "CHAGE — PASSWORT-AGING STEUERN:\n\n"
            "  chage -l username          aktuellen Status anzeigen\n"
            "  chage -M 90 username       max. Passwort-Alter (Tage)\n"
            "  chage -m 7 username        min. Passwort-Alter\n"
            "  chage -W 14 username       Warn-Tage vor Ablauf\n"
            "  chage -I 30 username       Inaktivitäts-Tage bis Sperre\n"
            "  chage -E 2025-12-31 user   Account-Ablaufdatum\n"
            "  chage -E -1 username       Account-Ablauf deaktivieren\n"
            "  chage -d 0 username        Passwort sofort ablaufen lassen\n\n"
            "/ETC/SHADOW FELDER (9 Felder):\n"
            "  1: Username\n"
            "  2: Gehashtes Passwort ($6$=SHA-512, $y$=yescrypt)\n"
            "  3: Letztes Passwort-Änderungsdatum (Tage seit 1970-01-01)\n"
            "  4: Min. Alter (chage -m)\n"
            "  5: Max. Alter (chage -M)\n"
            "  6: Warn-Tage (chage -W)\n"
            "  7: Inaktivitäts-Tage (chage -I)\n"
            "  8: Account-Ablauf (chage -E)\n"
            "  9: Reserviert\n\n"
            "PASSWD ACCOUNT-STEUERUNG:\n"
            "  passwd -l username         Account sperren (! vor Hash)\n"
            "  passwd -u username         Account entsperren\n"
            "  passwd -S username         Status anzeigen\n"
            "  passwd -e username         Passwort sofort ablaufen\n"
            "  usermod -e 2025-12-31 user Account-Ablauf setzen"
        ),
        syntax       = "chage [OPTIONS] username",
        example      = (
            "chage -l ghost               # aktuellen Aging-Status\n"
            "chage -M 90 -W 14 ghost      # max 90 Tage, 14 Tage Warnung\n"
            "chage -d 0 newuser           # Passwort bei nächstem Login erzwingen\n"
            "chage -E 2025-12-31 tempuser # Account läuft ab\n"
            "passwd -l baduser            # Account sperren\n"
            "passwd -S ghost              # Status prüfen"
        ),
        task_description = "Zeige den Passwort-Aging-Status für den root-Account",
        expected_commands = ["chage -l root"],
        hint_text    = "chage -l USERNAME zeigt alle Ablauf-Informationen des Accounts",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bewirkt 'chage -d 0 username'?",
                options    = [
                    "Löscht das Passwort",
                    "Setzt das letzte Änderungsdatum auf 0 → Passwort beim nächsten Login erzwingen",
                    "Sperrt den Account für 0 Tage",
                    "Deaktiviert das Passwort-Aging",
                ],
                correct    = 1,
                explanation = (
                    "chage -d 0 setzt 'last password change' auf Epoche-Tag 0.\n"
                    "Das System erkennt dies als abgelaufen → User muss Passwort ändern.\n"
                    "Nützlich für neue Accounts: erzwingt Passwort bei erstem Login."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 chage Flags:\n"
            "  -l = list (Infos anzeigen)\n"
            "  -M = Maximum days (Ablauf)\n"
            "  -m = minimum days\n"
            "  -W = warning days\n"
            "  -E = expiry date (YYYY-MM-DD)\n"
            "  -d 0 = Passwort sofort ablaufen lassen"
        ),
        memory_tip   = "chage = 'change age'. -M=Max, -m=min, -W=Warn, -E=Expiry, -d=date last changed",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.20 — su & sudo Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.20",
        chapter      = 10,
        title        = "su & sudo — Identitätswechsel meistern",
        mtype        = "INFILTRATE",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Manchmal musst du jemand anderes sein, Ghost.\n"
            " su wechselt komplett. sudo eskaliert gezielt.\n"
            " visudo — das Kontrollzentrum.\n"
            " Kein sudoers ohne visudo. Nie.'"
        ),
        why_important = (
            "su und sudo sind LPIC-1 Topic 107.1 Kernstoff.\n"
            "visudo und Sudoers-Syntax kommen in der Prüfung vor.\n"
            "Privilege Escalation sicher und kontrolliert einsetzen."
        ),
        explanation  = (
            "SU — BENUTZER WECHSELN:\n\n"
            "  su username          Benutzer wechseln (ohne Login-Shell)\n"
            "  su - username        Login-Shell (Umgebung komplett neu)\n"
            "  su -                 zu root wechseln (Login-Shell)\n"
            "  su -c 'cmd' user     Kommando als user ausführen\n\n"
            "Unterschied: su vs su -\n"
            "  su ghost     → Shell von root, Umgebung bleibt\n"
            "  su - ghost   → echte Login-Shell, PATH/HOME neu gesetzt\n\n"
            "SUDO — GRANULARE RECHTE:\n\n"
            "SUDOERS FORMAT (/etc/sudoers via visudo):\n"
            "  user  HOST=(RUNAS)  COMMANDS\n\n"
            "BEISPIELE:\n"
            "  ghost   ALL=(ALL)   ALL           → ghost = root\n"
            "  ghost   ALL=(ALL)   NOPASSWD:ALL  → ohne Passwort\n"
            "  %admin  ALL=(ALL)   ALL           → Gruppe admin\n"
            "  ghost   ALL=(root)  /sbin/reboot  → nur reboot\n"
            "  Cmnd_Alias PKGS = /usr/bin/apt    → Alias definieren\n\n"
            "WICHTIGE SUDO-OPTIONEN:\n"
            "  sudo -l              erlaubte Kommandos anzeigen\n"
            "  sudo -u ghost cmd    als ghost ausführen\n"
            "  sudo -s              Root-Shell öffnen\n"
            "  sudo -i              Login-Shell als root\n"
            "  sudo !!              letzten Befehl als root wiederholen\n\n"
            "VISUDO:\n"
            "  visudo               /etc/sudoers sicher bearbeiten\n"
            "  visudo -f /etc/sudoers.d/myfile  Fragment bearbeiten\n"
            "  /etc/sudoers.d/      Fragmentverzeichnis (includedir)"
        ),
        syntax       = "su [-] [username]  |  sudo [OPTIONS] COMMAND",
        example      = (
            "su -                         # zu root wechseln\n"
            "su - ghost                   # als ghost mit Login-Shell\n"
            "sudo -l                      # meine sudo-Rechte anzeigen\n"
            "sudo -u www-data ls /var/www # als www-data ausführen\n"
            "visudo                       # sudoers sicher bearbeiten\n"
            "sudo -i                      # root Login-Shell"
        ),
        task_description = "Liste alle sudo-Rechte des aktuellen Benutzers auf",
        expected_commands = ["sudo -l"],
        hint_text    = "sudo -l listet alle Kommandos, die der aktuelle User via sudo ausführen darf",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen 'su ghost' und 'su - ghost'?",
                options    = [
                    "Kein Unterschied",
                    "su ghost: Shell wechseln, Umgebung bleibt. su - ghost: Login-Shell, Umgebung komplett neu",
                    "su - ghost ist nur für root erlaubt",
                    "su ghost fragt nach dem root-Passwort, su - ghost nach dem ghost-Passwort",
                ],
                correct    = 1,
                explanation = (
                    "su user: Shell wird gewechselt, PATH/HOME bleiben von der alten Session.\n"
                    "su - user: Simuliert echten Login → HOME, PATH, Umgebung werden neu gesetzt.\n"
                    "Für korrekte Umgebung immer su - verwenden."
                ),
                xp_value   = 15,
            ),
        ],
        exam_tip     = (
            "LPIC-1 sudo/su Merkhilfen:\n"
            "  su - = Login-Shell (Umgebung neu)\n"
            "  sudo -l = liste meine Rechte\n"
            "  visudo = EINZIGE sichere Art, sudoers zu bearbeiten\n"
            "  NOPASSWD: = kein Passwort nötig\n"
            "  %gruppe = Gruppenregel in sudoers"
        ),
        memory_tip   = "visudo = vi + sudo. Syntaxcheck verhindert kaputte sudoers-Dateien",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.21 — Benutzer QUIZ (renumbered from 10.18)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.21",
        chapter      = 10,
        title        = "QUIZ — Benutzer & Gruppen Wissenstest",
        mtype        = "QUIZ",
        xp           = 150,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Vor dem letzten Gefecht, Ghost.\n"
            " Wer sind die User? Wer darf was?\n"
            " Topic 107.1 und 107.2 — keine Fehler erlaubt.'"
        ),
        why_important = "Quiz-Wiederholung für LPIC-1 Prüfung Topic 107.1/107.2",
        explanation   = "Beantworte die Fragen zu Benutzer- und Gruppenverwaltung.",
        syntax        = "",
        example       = "",
        task_description = "Quiz: Benutzer & Gruppen",
        expected_commands = [],
        hint_text     = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Was bedeutet 'x' im Passwort-Feld von /etc/passwd?",
                options    = [
                    "A) Das Passwort ist leer",
                    "B) Der Account ist gesperrt",
                    "C) Das Passwort ist in /etc/shadow gespeichert",
                    "D) Das Passwort ist verschlüsselt",
                ],
                correct    = "C",
                explanation = (
                    "'x' in /etc/passwd bedeutet: das Passwort ist\n"
                    "in /etc/shadow gespeichert (Shadow Password Suite).\n"
                    "'!' in /etc/shadow bedeutet: Account gesperrt."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welcher Befehl fügt ghost zur Gruppe docker HINZU ohne andere Gruppen zu entfernen?",
                options    = [
                    "A) usermod -G docker ghost",
                    "B) usermod -aG docker ghost",
                    "C) groupmod -a ghost docker",
                    "D) addgroup ghost docker",
                ],
                correct    = "B",
                explanation = (
                    "usermod -aG docker ghost:\n"
                    "  -a = append (anhängen, nicht ersetzen)\n"
                    "  -G = supplementary groups\n"
                    "OHNE -a würde -G alle anderen Gruppen ersetzen!"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welche Datei MUSS man nutzen um /etc/sudoers zu bearbeiten?",
                options    = [
                    "A) nano /etc/sudoers",
                    "B) vi /etc/sudoers",
                    "C) visudo",
                    "D) sudo edit /etc/sudoers",
                ],
                correct    = "C",
                explanation = (
                    "visudo ist der EINZIGE sichere Weg.\n"
                    "Es prüft die Syntax VOR dem Speichern.\n"
                    "Syntaxfehler in sudoers = niemand kann mehr sudo aufrufen!"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welche Shell verhindert interaktiven Login eines System-Accounts?",
                options    = [
                    "A) /bin/bash",
                    "B) /bin/sh",
                    "C) /usr/sbin/nologin",
                    "D) /dev/null",
                ],
                correct    = "C",
                explanation = (
                    "/usr/sbin/nologin (oder /sbin/nologin) gibt eine Meldung aus\n"
                    "und verhindert den Login — ideal für Service-Accounts.\n"
                    "/bin/false verhindert Login ohne Meldung."
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welche Profil-Datei wird beim SSH-Login eines Benutzers geladen?",
                options    = [
                    "A) ~/.bashrc",
                    "B) ~/.bash_profile",
                    "C) /etc/bash.bashrc",
                    "D) ~/.bash_history",
                ],
                correct    = "B",
                explanation = (
                    "SSH-Login = Login-Shell.\n"
                    "Login-Shell lädt: /etc/profile → ~/.bash_profile\n"
                    "Nicht-Login-Shell (Terminal öffnen) lädt: ~/.bashrc\n"
                    "~/.bash_profile kann ~/.bashrc mit source aufrufen."
                ),
                xp_value   = 30,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Benutzer-Schwerpunkte:\n"
            "  - /etc/passwd 7 Felder kennen\n"
            "  - UID 0=root, 1-999=System, 1000+=User\n"
            "  - usermod -aG (append!) vs -G (replace!)\n"
            "  - visudo = einziger sicherer Weg für sudoers\n"
            "  - Login-Shell: ~/.bash_profile | Non-Login: ~/.bashrc"
        ),
        memory_tip   = "passwd 7 Felder: user:x:uid:gid:info:home:shell. shadow hat Hashes. usermod -aG = append, -G = replace! Merke: -a für addieren.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 10.BOSS — IDENTITY DAEMON v10.0
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "10.boss",
        chapter      = 10,
        title        = "BOSS — IDENTITY DAEMON v10.0",
        mtype        = "BOSS",
        xp           = 300,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM ALERT: IDENTITY DAEMON v10.0 aktiv.\n"
            "Er kontrolliert alle UIDs. Alle GIDs. Alle Passwörter.\n"
            "Er hat ghost gesperrt. sudo deaktiviert. PAM manipuliert.\n"
            "Zara Z3R0: 'Reaktiviere ghost. Räume sudo auf.\n"
            " Dann vernichte den Daemon, Ghost. Für immer.'"
        ),
        why_important = "Abschluss-Boss für Topic 107.1/107.2",
        explanation  = (
            "BOSS-CHALLENGE: Identity Gauntlet\n\n"
            "Deine Mission:\n"
            "1) Benutzer 'agent' erstellen mit Home + bash\n"
            "2) agent zur sudo-Gruppe hinzufügen\n"
            "3) Passwort-Aging prüfen\n"
            "4) Gesperrten Account entsperren\n\n"
            "KOMMANDOS:\n"
            "  useradd -m -s /bin/bash agent\n"
            "  usermod -aG sudo agent\n"
            "  chage -l agent\n"
            "  passwd -u ghost\n"
            "  id agent"
        ),
        syntax       = "",
        example      = (
            "useradd -m -s /bin/bash agent\n"
            "usermod -aG sudo agent\n"
            "chage -M 90 -W 14 agent\n"
            "passwd -u ghost\n"
            "id agent\n"
            "getent passwd agent"
        ),
        ascii_art    = """
  ██╗██████╗ ███████╗███╗   ██╗████████╗██╗████████╗██╗   ██╗    ██████╗  █████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗
  ██║██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██║╚══██╔══╝╚██╗ ██╔╝    ██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║
  ██║██║  ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║    ╚████╔╝     ██║  ██║███████║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
  ██║██║  ██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║     ╚██╔╝      ██║  ██║██╔══██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
  ██║██████╔╝███████╗██║ ╚████║   ██║   ██║   ██║      ██║       ██████╔╝██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝   ╚═╝      ╚═╝       ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

  ┌─ IDENTITY MATRIX ─────────────────────────────────────────────────┐
  │  ghost   :: UID 1000  STATUS: LOCKED   SUDO: REVOKED             │
  │  /etc/shadow: ENCRYPTED  PAM: COMPROMISED                        │
  │  passwd -l ghost  >> EXECUTED  |  usermod --lock: ACTIVE         │
  └───────────────────────────────────────────────────────────────────┘

                    ⚡ CHAOSWERK FACTION :: CHAPTER 10 BOSS ⚡""",
        story_transitions = [
            "IDENTITY DAEMON löscht Accounts in Echtzeit. Du must schneller sein.",
            "useradd, usermod, passwd — drei Befehle drei Sekunden.",
            "Shadow-Datei korrumpiert. chage rettet die Passwort-Policy.",
            "Letzter Account gesperrt. passwd -u. Das Daemon-Schloss bricht.",
        ],
        task_description = "BOSS: Entsperre den gesperrten Account 'ghost'",
        expected_commands = ["passwd -u ghost"],
        hint_text    = "passwd -u ghost entsperrt (unlock) einen gesperrten Benutzer-Account",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welcher Befehl zeigt alle Mitglieder einer Gruppe?',
                options     = ['A) groups GRUPPE', 'B) getent group GRUPPE', 'C) groupmembers GRUPPE', 'D) cat /etc/group | grep GRUPPE'],
                correct     = 'B',
                explanation = 'getent group GRUPPE zeigt alle Mitglieder. grep funktioniert auch.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "LPIC-1 FINAL USER CHECK:\n"
            "  useradd -m -s /bin/bash USER → vollständiger Account\n"
            "  usermod -aG GROUP USER → Gruppe hinzufügen\n"
            "  passwd -l/-u USER → lock/unlock\n"
            "  chage -l USER → Passwort-Info\n"
            "  visudo → sudoers bearbeiten\n"
            "  id USER → UID/GID/Gruppen"
        ),
        memory_tip   = "Merkhilfe: BOSS = Big Operations on System Security",
        gear_reward  = "root_keycard",
        faction_reward = ("Root Collective", 35),
    ),
]
