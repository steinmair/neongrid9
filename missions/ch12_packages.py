"""
NeonGrid-9 :: Kapitel 12 — INSTALL PROTOCOL
LPIC-1 Topic 102.4 / 102.5
Paketverwaltung: dpkg, apt, rpm, yum/dnf, zypper

"In NeonGrid-9 ist Software Munition.
 dpkg, apt, rpm, dnf — die Waffenkammern des Systems.
 Wer Pakete kontrolliert, kontrolliert das System.
 Wer es nicht tut, installiert Backdoors."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_12_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 12.01 — dpkg — Das Debian-Paketformat
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.01",
        chapter      = 12,
        title        = "dpkg — Debian Package Manager",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Jede Software in NeonGrid-9 ist ein Paket, Ghost.\n"
            " dpkg ist die Basis. Kein Netzwerk. Kein Repo.\n"
            " Nur: .deb-Datei rein, dpkg -i raus.\n"
            " Kenn das Werkzeug — oder bleib entwaffnet.'"
        ),
        why_important = (
            "dpkg ist das Low-Level-Paketmanagement-Tool für Debian-Systeme.\n"
            "LPIC-1 Topic 102.4 testet dpkg-Befehle, .deb-Struktur und Abfragen."
        ),
        explanation  = (
            "DPKG — DEBIAN PACKAGE MANAGER:\n\n"
            "INSTALLATION:\n"
            "  dpkg -i paket.deb         Paket installieren\n"
            "  dpkg -i *.deb             mehrere Pakete installieren\n"
            "  dpkg --install paket.deb  wie -i\n\n"
            "ENTFERNEN:\n"
            "  dpkg -r paketname         Paket entfernen (Config bleibt)\n"
            "  dpkg -P paketname         Paket + Config entfernen (purge)\n"
            "  dpkg --remove paketname   wie -r\n"
            "  dpkg --purge paketname    wie -P\n\n"
            "ABFRAGEN:\n"
            "  dpkg -l                   alle installierten Pakete\n"
            "  dpkg -l | grep nginx      nach Paket suchen\n"
            "  dpkg -l 'nginx*'          mit Wildcard\n"
            "  dpkg -s nginx             Paket-Status/Info\n"
            "  dpkg -L nginx             Dateien eines Pakets auflisten\n"
            "  dpkg -S /usr/bin/python3  welches Paket enthält diese Datei?\n"
            "  dpkg --get-selections     alle Pakete mit Status\n\n"
            "INHALT OHNE INSTALLATION:\n"
            "  dpkg -c paket.deb         Inhalt einer .deb-Datei\n"
            "  dpkg -I paket.deb         Info einer .deb-Datei\n\n"
            "STATUS-CODES in dpkg -l:\n"
            "  ii  installiert (desired=install, status=installed)\n"
            "  rc  entfernt, Config bleibt (removed, config)\n"
            "  un  unbekannt/nicht installiert\n\n"
            "PAKET-DATENBANK:\n"
            "  /var/lib/dpkg/            dpkg-Datenbank\n"
            "  /var/lib/dpkg/status      Status aller Pakete\n"
            "  /var/lib/dpkg/info/       Paket-Skripte und Dateilisten\n\n"
            "PROBLEME BEHEBEN:\n"
            "  dpkg --configure -a       alle halb-konfigurierten Pakete\n"
            "  dpkg --force-depends -i   Abhängigkeiten ignorieren"
        ),
        ascii_art = """
  ██████╗  █████╗  ██████╗██╗  ██╗ █████╗  ██████╗ ███████╗███████╗
  ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝ ██╔════╝██╔════╝
  ██████╔╝███████║██║     █████╔╝ ███████║██║  ███╗█████╗  ███████╗
  ██╔═══╝ ██╔══██║██║     ██╔═██╗ ██╔══██║██║   ██║██╔══╝  ╚════██║
  ██║     ██║  ██║╚██████╗██║  ██╗██║  ██║╚██████╔╝███████╗███████║
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝

  [ CHAPTER 12 :: PACKAGE MANAGEMENT ]
  > apt/dpkg/rpm matrix online. Dependency graph resolving...""",
        story_transitions = [
            "Software kommt in Paketen. Pakete haben Abhängigkeiten.",
            "dpkg installiert rohe .deb. apt löst Abhängigkeiten auf.",
            "rpm, yum, dnf — andere Distros, gleiche Idee.",
            "Kein unkontrolliertes apt install. Versteh was du installierst.",
        ],
        syntax       = "dpkg -i PKG.deb  |  dpkg -l  |  dpkg -s PKG  |  dpkg -L PKG",
        example      = (
            "dpkg -l\n"
            "dpkg -l | grep python3\n"
            "dpkg -s openssh-server\n"
            "dpkg -L openssh-server\n"
            "dpkg -S /usr/bin/ssh\n"
            "dpkg -i ./custom-tool_1.0_amd64.deb"
        ),
        task_description = "Zeige alle installierten Pakete mit dpkg",
        expected_commands = ["dpkg -l"],
        hint_text    = "dpkg -l listet alle installierten Pakete. Pipe zu grep um zu filtern.",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'dpkg -l'?",
                options     = ['A) Installiert Paket', 'B) Listet alle installierten Pakete', 'C) Zeigt Paket-Log', 'D) Löscht Paket'],
                correct     = 'B',
                explanation = 'dpkg -l = list all installed packages. dpkg -L PKG = listet Dateien eines Pakets.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welcher Befehl zeigt, zu welchem Paket eine Datei gehört?',
                options     = ['A) dpkg -s /pfad', 'B) dpkg -S /pfad/zur/datei', 'C) dpkg -q datei', 'D) apt-file datei'],
                correct     = 'B',
                explanation = 'dpkg -S = search. Zeigt welches Paket die Datei installiert hat.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGS-MERKSÄTZE:\n"
            "  dpkg -i = install\n"
            "  dpkg -r = remove (Config bleibt)\n"
            "  dpkg -P = purge (alles weg)\n"
            "  dpkg -l = list\n"
            "  dpkg -L PKG = List files of package\n"
            "  dpkg -S /pfad = Search which package owns file"
        ),
        memory_tip   = "Merkhilfe: -i=install, -r=remove, -P=Purge, -l=list, -L=List files, -S=Search",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.02 — apt — Advanced Package Tool
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.02",
        chapter      = 12,
        title        = "apt — Paketmanager mit Abhängigkeiten",
        mtype        = "INFILTRATE",
        xp           = 100,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'dpkg kennt keine Abhängigkeiten, Ghost.\n"
            " apt schon. apt holt Pakete aus dem Repo.\n"
            " Löst Konflikte. Aktualisiert alles.\n"
            " apt ist dein vollautomatischer Waffenschmied.'"
        ),
        why_important = (
            "apt ist das primäre Paketmanagement-Tool für Debian/Ubuntu.\n"
            "LPIC-1 testet apt, apt-get, apt-cache und Repository-Konfiguration."
        ),
        explanation  = (
            "APT — ADVANCED PACKAGE TOOL:\n\n"
            "PAKETLISTEN AKTUALISIEREN:\n"
            "  apt update                Paketlisten vom Repo holen\n"
            "  (IMMER vor install/upgrade ausführen!)\n\n"
            "PAKETE INSTALLIEREN:\n"
            "  apt install nginx         Paket installieren\n"
            "  apt install -y nginx      ohne Rückfrage\n"
            "  apt install nginx=1.18.*  spezifische Version\n"
            "  apt install ./paket.deb   lokale .deb-Datei\n\n"
            "PAKETE AKTUALISIEREN:\n"
            "  apt upgrade               alle Pakete aktualisieren\n"
            "  apt full-upgrade          wie upgrade + Abhängigkeiten lösen\n"
            "  apt upgrade nginx         einzelnes Paket\n\n"
            "PAKETE ENTFERNEN:\n"
            "  apt remove nginx          Paket entfernen (Config bleibt)\n"
            "  apt purge nginx           Paket + Config entfernen\n"
            "  apt autoremove            verwaiste Abhängigkeiten entfernen\n\n"
            "PAKETE SUCHEN UND INFO:\n"
            "  apt search nginx          Paket suchen\n"
            "  apt show nginx            Paket-Details\n"
            "  apt list --installed      installierte Pakete\n"
            "  apt list --upgradable     aktualisierbare Pakete\n\n"
            "APT-CACHE (low-level Abfragen):\n"
            "  apt-cache search nginx    Paket suchen\n"
            "  apt-cache show nginx      Paket-Info\n"
            "  apt-cache depends nginx   Abhängigkeiten\n"
            "  apt-cache rdepends nginx  Wer hängt von nginx ab?\n"
            "  apt-cache policy nginx    verfügbare Versionen\n\n"
            "APT-GET (älteres Tool, aber noch häufig):\n"
            "  apt-get update / install / remove / upgrade\n"
            "  apt-get dist-upgrade      = apt full-upgrade\n"
            "  apt-get clean             Cache leeren\n"
            "  apt-get autoclean         alte Cache-Dateien löschen\n\n"
            "REPOSITORY-KONFIGURATION:\n"
            "  /etc/apt/sources.list                  Haupt-Quellen\n"
            "  /etc/apt/sources.list.d/               Zusätzliche Quellen\n"
            "  deb http://repo.url/ bookworm main     Debian-Format\n"
            "  deb-src http://repo.url/ bookworm main Quellcode"
        ),
        syntax       = "apt update  |  apt install PKG  |  apt search PKG  |  apt show PKG",
        example      = (
            "apt update\n"
            "apt install -y curl wget git\n"
            "apt search python3\n"
            "apt show openssh-server\n"
            "apt remove --purge nginx\n"
            "apt autoremove\n"
            "apt list --installed | grep nginx"
        ),
        task_description = "Aktualisiere die Paketlisten vom Repository",
        expected_commands = ["apt update"],
        hint_text    = "apt update holt aktuelle Paketlisten von den konfigurierten Repos",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'apt upgrade' im Vergleich zu 'apt full-upgrade'?",
                options     = ['A) Kein Unterschied', 'B) apt upgrade entfernt keine Pakete, full-upgrade schon (bei Konflikten)', 'C) full-upgrade ist sicherer', 'D) apt upgrade ist für Kernel'],
                correct     = 'B',
                explanation = 'apt upgrade: keine Pakete entfernt. full-upgrade (dist-upgrade): entfernt bei Bedarf.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Warum muss man 'apt update' vor 'apt install' ausführen?",
                options     = ['A) Lädt Paket herunter', 'B) Aktualisiert die lokale Paketliste (Metadaten) vom Repository', 'C) Prüft Abhängigkeiten', 'D) Authentifiziert Repository'],
                correct     = 'B',
                explanation = 'apt update = Paketliste aktualisieren (keine Installation!). Ohne update: veraltete Infos.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "REIHENFOLGE MERKEN:\n"
            "  1. apt update      (Listen holen)\n"
            "  2. apt upgrade     (Pakete aktualisieren)\n"
            "apt remove = Config bleibt\n"
            "apt purge  = alles weg (wie dpkg -P)"
        ),
        memory_tip   = "Merkhilfe: update=Listen, upgrade=Pakete, install=neu, purge=alles weg",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.03 — APT Repository-Konfiguration
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.03",
        chapter      = 12,
        title        = "APT Repositories — Quellen konfigurieren",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Das Imperium kontrolliert die offiziellen Repos.\n"
            " Wir brauchen eigene Quellen, Ghost.\n"
            " /etc/apt/sources.list — das ist das Tor zum freien Software-Markt.\n"
            " Konfiguriere es. Sicher. Korrekt.'"
        ),
        why_important = (
            "Repository-Konfiguration steuert woher Software kommt.\n"
            "LPIC-1 testet sources.list-Syntax, GPG-Keys und apt-key."
        ),
        explanation  = (
            "APT SOURCES.LIST FORMAT:\n\n"
            "  deb URL DISTRIBUTION KOMPONENTEN\n\n"
            "BEISPIELE:\n"
            "  deb http://deb.debian.org/debian bookworm main contrib non-free\n"
            "  deb http://security.debian.org/ bookworm-security main\n"
            "  deb-src http://deb.debian.org/debian bookworm main\n\n"
            "FELDER:\n"
            "  deb          binäre Pakete\n"
            "  deb-src      Quellcode-Pakete\n"
            "  URL          Repository-URL\n"
            "  DISTRIBUTION bookworm, bullseye, focal, jammy, stable, ...\n"
            "  KOMPONENTEN  main, contrib, non-free, restricted, universe\n\n"
            "KOMPONENTEN:\n"
            "  main         offiziell unterstützt, Open Source\n"
            "  contrib      Open Source, aber Abhängigkeiten in non-free\n"
            "  non-free     proprietäre Software\n"
            "  restricted   (Ubuntu) proprietäre Treiber\n"
            "  universe     (Ubuntu) Community-gepflegt\n\n"
            "NEUERES FORMAT (.sources in /etc/apt/sources.list.d/):\n"
            "  Types: deb\n"
            "  URIs: http://deb.debian.org/debian\n"
            "  Suites: bookworm\n"
            "  Components: main\n\n"
            "GPG-KEYS:\n"
            "  apt-key list              alle vertrauten Keys\n"
            "  apt-key add key.gpg       Key hinzufügen (veraltet)\n"
            "  gpg --dearmor key.gpg     Key in /usr/share/keyrings/ speichern\n\n"
            "ADD-APT-REPOSITORY:\n"
            "  add-apt-repository ppa:user/repo  (Ubuntu PPAs)\n"
            "  add-apt-repository 'deb URL DIST COMP'\n\n"
            "PINNING (Paket-Versionen fixieren):\n"
            "  /etc/apt/preferences.d/   Pinning-Konfiguration\n"
            "  apt-cache policy nginx    Pin-Prioritäten anzeigen"
        ),
        syntax       = "cat /etc/apt/sources.list  |  apt-key list  |  add-apt-repository",
        example      = (
            "cat /etc/apt/sources.list\n"
            "ls /etc/apt/sources.list.d/\n"
            "apt-cache policy nginx\n"
            "apt-cache show nginx | grep Version\n"
            "# PPAs (Ubuntu):\n"
            "add-apt-repository ppa:ondrej/php\n"
            "apt update"
        ),
        task_description = "Zeige die konfigurierten APT-Paketquellen",
        expected_commands = ["cat /etc/apt/sources.list"],
        hint_text    = "/etc/apt/sources.list enthält die konfigurierten Repository-URLs",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was steht in /etc/apt/sources.list?',
                options     = ['A) Installierte Pakete', 'B) Repository-URLs und Komponenten (main, contrib, etc.)', 'C) GPG-Schlüssel', 'D) Paket-Cache'],
                correct     = 'B',
                explanation = '/etc/apt/sources.list: Repository-Quellen. /etc/apt/sources.list.d/: Drop-in Dateien.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'apt-key add -'?",
                options     = ['A) Fügt leeren Schlüssel hinzu', 'B) Fügt GPG-Schlüssel aus Stdin zum apt-Keyring hinzu', 'C) Erstellt neuen Schlüssel', 'D) Zeigt alle Schlüssel'],
                correct     = 'B',
                explanation = 'apt-key add KEY = GPG-Signaturschlüssel für Repository-Verifikation hinzufügen.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGSFRAGE: Was macht 'deb-src'?\n"
            "→ Quellcode-Pakete herunterladen (für apt-get source)\n"
            "Komponenten: main=offiziell, contrib=abhängig von non-free, non-free=proprietär"
        ),
        memory_tip   = "Merkhilfe: deb=binary, deb-src=source. main contrib non-free = Freizügigkeit",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.04 — rpm — Red Hat Package Manager
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.04",
        chapter      = 12,
        title        = "rpm — Red Hat Package Manager",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Nicht alle Systeme laufen auf Debian, Ghost.\n"
            " RHEL. CentOS. Fedora. AlmaLinux.\n"
            " Sie alle nutzen rpm. Gleiche Konzepte — andere Befehle.\n"
            " LPIC kennt keine Grenzen zwischen den Distros.'"
        ),
        why_important = (
            "rpm ist das Low-Level-Tool für RHEL/CentOS/Fedora.\n"
            "LPIC-1 Topic 102.4 testet rpm explizit neben dpkg."
        ),
        explanation  = (
            "RPM — RED HAT PACKAGE MANAGER:\n\n"
            "INSTALLATION:\n"
            "  rpm -i paket.rpm          installieren\n"
            "  rpm -iv paket.rpm         mit verbose\n"
            "  rpm -ivh paket.rpm        mit verbose + Fortschritt\n"
            "  rpm -U paket.rpm          upgrade (oder install)\n"
            "  rpm -F paket.rpm          freshen (nur wenn installiert)\n\n"
            "ENTFERNEN:\n"
            "  rpm -e paketname          Paket entfernen\n"
            "  rpm -e --nodeps paketname Abhängigkeiten ignorieren\n\n"
            "ABFRAGEN (-q Flags):\n"
            "  rpm -qa                   alle installierten Pakete\n"
            "  rpm -qa | grep nginx      filtern\n"
            "  rpm -qi nginx             Info über Paket\n"
            "  rpm -ql nginx             Dateien des Pakets\n"
            "  rpm -qf /usr/bin/python3  welches Paket besitzt Datei?\n"
            "  rpm -qd nginx             Dokumentationsdateien\n"
            "  rpm -qc nginx             Konfigurationsdateien\n"
            "  rpm -qR nginx             Abhängigkeiten (Requires)\n"
            "  rpm -q --changelog nginx  Changelog\n\n"
            "OHNE INSTALLATION (aus .rpm-Datei):\n"
            "  rpm -qip paket.rpm        Info ohne Install\n"
            "  rpm -qlp paket.rpm        Dateien ohne Install\n\n"
            "VERIFIZIERUNG:\n"
            "  rpm -V nginx              Paket-Integrität prüfen\n"
            "  rpm -Va                   alle Pakete prüfen\n"
            "  rpm -K paket.rpm          GPG-Signatur prüfen\n\n"
            "DATENBANK:\n"
            "  /var/lib/rpm/             RPM-Datenbank\n"
            "  rpm --rebuilddb           Datenbank neu aufbauen\n\n"
            "RPM AUSGABE-FORMAT:\n"
            "  name-version-release.arch.rpm\n"
            "  nginx-1.20.1-9.el8.x86_64.rpm"
        ),
        syntax       = "rpm -ivh PKG.rpm  |  rpm -qa  |  rpm -qi PKG  |  rpm -qf /pfad",
        example      = (
            "rpm -qa\n"
            "rpm -qa | grep ssh\n"
            "rpm -qi openssh\n"
            "rpm -ql openssh\n"
            "rpm -qf /usr/sbin/sshd\n"
            "rpm -ivh ./nginx-1.20.1-9.el8.x86_64.rpm\n"
            "rpm -e nginx"
        ),
        task_description = "Welches Paket enthält die Datei /usr/bin/python3 (rpm)?",
        expected_commands = ["rpm -qf /usr/bin/python3"],
        hint_text    = "rpm -qf /pfad/zur/datei zeigt welches Paket die Datei gehört",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welcher rpm-Befehl zeigt, zu welchem Paket eine Datei gehört?',
                options     = ['A) rpm -qi /pfad', 'B) rpm -qf /pfad/zur/datei', 'C) rpm -ql datei', 'D) rpm -qs datei'],
                correct     = 'B',
                explanation = 'rpm -qf = query file. rpm -qi = query info. rpm -ql = query list (Dateien des Pakets).',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'rpm -ivh paket.rpm'?",
                options     = ['A) Informationen anzeigen', 'B) Installieren mit verbose + Fortschrittsbalken', 'C) Auf Updates prüfen', 'D) Verify Hashsumme'],
                correct     = 'B',
                explanation = 'rpm -ivh: i=install, v=verbose, h=hash (Fortschrittsbalken #####).',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "DPKG vs RPM Vergleich:\n"
            "  dpkg -i    = rpm -ivh   (install)\n"
            "  dpkg -r    = rpm -e     (remove)\n"
            "  dpkg -l    = rpm -qa    (list all)\n"
            "  dpkg -L    = rpm -ql    (list files)\n"
            "  dpkg -S    = rpm -qf    (search file)\n"
            "  dpkg -s    = rpm -qi    (show info)"
        ),
        memory_tip   = "Merkhilfe: rpm -q = query. Dann: a=all, i=info, l=list, f=file, R=requires",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.05 — yum & dnf — RPM mit Abhängigkeiten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.05",
        chapter      = 12,
        title        = "yum & dnf — RPM Paketmanager",
        mtype        = "INFILTRATE",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'rpm allein kann keine Abhängigkeiten lösen, Ghost.\n"
            " yum hat das für RHEL jahrelang getan.\n"
            " dnf ist der Nachfolger — schneller, smarter.\n"
            " Beide kennst du — beide prüft LPIC-1.'"
        ),
        why_important = (
            "yum/dnf ist das High-Level-RPM-Tool (wie apt für Debian).\n"
            "LPIC-1 testet beide da yum auf alten und dnf auf neuen Systemen läuft."
        ),
        explanation  = (
            "YUM / DNF — RPM MIT ABHÄNGIGKEITEN:\n\n"
            "INSTALLATION:\n"
            "  yum install nginx         Paket installieren\n"
            "  dnf install nginx         (moderner)\n"
            "  yum install -y nginx      ohne Rückfrage\n"
            "  yum localinstall p.rpm    lokale .rpm-Datei\n\n"
            "AKTUALISIEREN:\n"
            "  yum update                alle Pakete\n"
            "  yum update nginx          einzelnes Paket\n"
            "  yum check-update          verfügbare Updates anzeigen\n\n"
            "ENTFERNEN:\n"
            "  yum remove nginx          Paket entfernen\n"
            "  yum autoremove            verwaiste Abhängigkeiten\n\n"
            "SUCHEN UND INFO:\n"
            "  yum search nginx          Paket suchen\n"
            "  yum info nginx            Paket-Info\n"
            "  yum list installed        installierte Pakete\n"
            "  yum list available        verfügbare Pakete\n"
            "  yum provides /usr/bin/python3  welches Paket?\n"
            "  yum deplist nginx         Abhängigkeiten\n\n"
            "GRUPPEN:\n"
            "  yum grouplist             Paketgruppen anzeigen\n"
            "  yum groupinstall 'Development Tools'\n"
            "  yum groupremove 'Development Tools'\n\n"
            "HISTORY:\n"
            "  yum history               Transaktions-Geschichte\n"
            "  yum history undo LAST     letzte Transaktion rückgängig\n\n"
            "CACHE:\n"
            "  yum clean all             Cache leeren\n"
            "  yum makecache             Cache neu aufbauen\n\n"
            "DNF UNTERSCHIEDE:\n"
            "  dnf ist schneller dank libsolv\n"
            "  dnf repolist              Repos anzeigen\n"
            "  dnf module list           Module (RHEL 8+)\n"
            "  dnf history               wie yum history\n\n"
            "REPOSITORY KONFIGURATION:\n"
            "  /etc/yum.repos.d/         .repo-Dateien\n"
            "  /etc/yum.conf             Haupt-Konfiguration\n"
            "  yum repolist              aktive Repos\n"
            "  yum-config-manager --add-repo URL\n"
            "  dnf config-manager --add-repo URL"
        ),
        syntax       = "yum/dnf install PKG  |  yum/dnf search PKG  |  yum/dnf update",
        example      = (
            "yum update\n"
            "yum install -y httpd\n"
            "yum search python3\n"
            "yum info httpd\n"
            "yum provides /usr/sbin/httpd\n"
            "yum remove httpd\n"
            "dnf install nginx\n"
            "dnf repolist"
        ),
        task_description = "Suche nach dem Paket 'httpd' mit yum",
        expected_commands = ["yum search httpd"],
        hint_text    = "yum search PAKETNAME durchsucht alle konfigurierten Repositories",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist der Unterschied zwischen yum und dnf?',
                options     = ['A) yum ist moderner', 'B) dnf ist der moderne Nachfolger von yum (schneller, bessere Abhängigkeiten)', 'C) Kein Unterschied', 'D) yum ist für RHEL, dnf für Fedora'],
                correct     = 'B',
                explanation = 'dnf = Dandified YUM, moderner Ersatz. RHEL8+ nutzt dnf. yum ist oft ein Alias.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'yum/dnf provides /pfad/zur/datei'?",
                options     = ['A) Zeigt Abhängigkeiten', 'B) Zeigt welches Paket diese Datei bereitstellt', 'C) Überprüft Datei-Integrität', 'D) Installiert Datei'],
                correct     = 'B',
                explanation = 'provides = Gegenstück zu dpkg -S. Sucht Paket das eine bestimmte Datei enthält.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "APT vs YUM/DNF:\n"
            "  apt update        = yum check-update / dnf check-update\n"
            "  apt install       = yum install / dnf install\n"
            "  apt search        = yum search / dnf search\n"
            "  apt show          = yum info / dnf info\n"
            "  apt-cache depends = yum deplist / dnf repoquery --requires"
        ),
        memory_tip   = "Merkhilfe: yum/dnf hat die gleiche Syntax — dnf ist der neuere Nachfolger",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.06 — zypper — SUSE Paketmanager
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.06",
        chapter      = 12,
        title        = "zypper — SUSE/openSUSE Paketmanager",
        mtype        = "SCAN",
        xp           = 70,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'LPIC-1 testet nicht nur Debian und RHEL, Ghost.\n"
            " SUSE ist die dritte Säule.\n"
            " zypper — kurz, prägnant, effektiv.\n"
            " Lern die Grundbefehle — der Rest ist Intuition.'"
        ),
        why_important = (
            "zypper ist der Paketmanager für SUSE/openSUSE.\n"
            "LPIC-1 Topic 102.5 testet zypper als dritte Paketmanager-Familie."
        ),
        explanation  = (
            "ZYPPER — SUSE PAKETMANAGER:\n\n"
            "INSTALLATION:\n"
            "  zypper install nginx      oder: zypper in nginx\n"
            "  zypper install -y nginx   ohne Rückfrage\n\n"
            "AKTUALISIEREN:\n"
            "  zypper update             alle Pakete\n"
            "  zypper update nginx       einzelnes Paket\n"
            "  zypper list-updates       verfügbare Updates\n\n"
            "ENTFERNEN:\n"
            "  zypper remove nginx       oder: zypper rm nginx\n\n"
            "SUCHEN UND INFO:\n"
            "  zypper search nginx       oder: zypper se nginx\n"
            "  zypper info nginx\n"
            "  zypper what-provides /usr/sbin/nginx\n\n"
            "REPOS:\n"
            "  zypper repos              Repos anzeigen (zypper lr)\n"
            "  zypper addrepo URL NAME   Repo hinzufügen\n"
            "  zypper removerepo NAME    Repo entfernen\n"
            "  zypper refresh            Repo-Daten aktualisieren\n\n"
            "VERGLEICH DER DREI FAMILIEN:\n\n"
            "  AKTION          DEBIAN          RPM             SUSE\n"
            "  ─────────────────────────────────────────────────────\n"
            "  Low-Level       dpkg            rpm             rpm\n"
            "  High-Level      apt             yum/dnf         zypper\n"
            "  Install         apt install     yum install     zypper in\n"
            "  Remove          apt remove      yum remove      zypper rm\n"
            "  Update Lists    apt update      yum check-upd   zypper refresh\n"
            "  Upgrade All     apt upgrade     yum update      zypper update\n"
            "  Search          apt search      yum search      zypper se\n"
            "  Info            apt show        yum info        zypper info\n"
            "  List Files      dpkg -L         rpm -ql         rpm -ql\n"
            "  File Owner      dpkg -S         rpm -qf         rpm -qf\n"
            "  Paketformat     .deb            .rpm            .rpm"
        ),
        syntax       = "zypper install PKG  |  zypper search PKG  |  zypper update",
        example      = (
            "zypper search nginx\n"
            "zypper install nginx\n"
            "zypper update\n"
            "zypper remove nginx\n"
            "zypper repos\n"
            "zypper refresh"
        ),
        task_description = "Zeige alle konfigurierten zypper-Repositories",
        expected_commands = ["zypper repos"],
        hint_text    = "zypper repos (oder zypper lr) listet alle konfigurierten Repositories",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht 'zypper search PKG'?",
                options     = ['A) Installiert Paket', 'B) Sucht nach Paket in Repositories', 'C) Zeigt Paket-Details', 'D) Entfernt Paket'],
                correct     = 'B',
                explanation = 'zypper search (oder se) sucht. zypper install (in), zypper remove (rm).',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Zypper ist der Paketmanager für welche Distributionen?',
                options     = ['A) Debian/Ubuntu', 'B) RHEL/CentOS', 'C) SUSE/openSUSE', 'D) Arch Linux'],
                correct     = 'C',
                explanation = 'zypper = SUSE/openSUSE. apt/dpkg = Debian/Ubuntu. yum/dnf/rpm = RHEL.',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "MERKE: Alle drei Familien nutzen rpm als Low-Level-Format!\n"
            "Nur Debian nutzt .deb — alle anderen nutzen .rpm\n"
            "zypper in = install, zypper rm = remove, zypper se = search"
        ),
        memory_tip   = "Merkhilfe: zypper in/rm/se = install/remove/search (kurz-Syntax)",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.07 — Shared Libraries & ldconfig
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.07",
        chapter      = 12,
        title        = "Shared Libraries — ldd & ldconfig",
        mtype        = "DECODE",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Die Backdoor-Binary startet nicht, Ghost.\n"
            " 'libcrypto.so.3: not found'\n"
            " Shared Libraries fehlen oder sind nicht registriert.\n"
            " ldd zeigt dir was fehlt. ldconfig behebt es.'"
        ),
        why_important = (
            "Shared Libraries sind Abhängigkeiten von Programmen.\n"
            "LPIC-1 Topic 102.3 testet ldd, ldconfig und Library-Pfade."
        ),
        explanation  = (
            "SHARED LIBRARIES:\n\n"
            "LIBRARY-TYPEN:\n"
            "  Static (.a)    in Binary eingebettet — groß, unabhängig\n"
            "  Dynamic (.so)  zur Laufzeit geladen — klein, geteilt\n\n"
            "NAMING CONVENTION:\n"
            "  libname.so.MAJOR.MINOR.PATCH\n"
            "  libssl.so.3.0.8\n"
            "  libssl.so.3     → Symlink (SONAME)\n"
            "  libssl.so       → Symlink (Link name)\n\n"
            "LIBRARY-PFADE:\n"
            "  /lib/            essentielle Libs (Boot)\n"
            "  /usr/lib/        Standard-Libraries\n"
            "  /usr/local/lib/  lokale Libraries\n"
            "  /lib/x86_64-linux-gnu/  Architektur-spezifisch\n\n"
            "LDD — LIBRARY DEPENDENCIES:\n"
            "  ldd /usr/bin/python3       Abhängigkeiten anzeigen\n"
            "  ldd -v /usr/bin/python3    verbose\n\n"
            "LDCONFIG — LIBRARY-CACHE:\n"
            "  ldconfig                   Cache aktualisieren\n"
            "  ldconfig -p                Cache anzeigen\n"
            "  ldconfig -v                verbose\n\n"
            "KONFIGURATION:\n"
            "  /etc/ld.so.conf            Haupt-Konfiguration\n"
            "  /etc/ld.so.conf.d/         Fragmente\n"
            "  /etc/ld.so.cache           Cache-Datei (binär)\n\n"
            "LD_LIBRARY_PATH (Umgebungsvariable):\n"
            "  export LD_LIBRARY_PATH=/custom/lib\n"
            "  Durchsucht wird VOR /etc/ld.so.cache\n"
            "  Sicherheitsrisiko! Nicht in Produktiv-Umgebungen!\n\n"
            "NEUE LIBRARY REGISTRIEREN:\n"
            "  1. Library nach /usr/local/lib/ kopieren\n"
            "  2. echo '/usr/local/lib' >> /etc/ld.so.conf.d/custom.conf\n"
            "  3. ldconfig ausführen"
        ),
        syntax       = "ldd /pfad/zu/binary  |  ldconfig  |  ldconfig -p",
        example      = (
            "ldd /usr/bin/python3\n"
            "ldd /usr/bin/ssh\n"
            "ldconfig -p\n"
            "ldconfig -p | grep libssl\n"
            "ldconfig\n"
            "cat /etc/ld.so.conf"
        ),
        task_description = "Zeige die Library-Abhängigkeiten von /usr/bin/python3",
        expected_commands = ["ldd /usr/bin/python3"],
        hint_text    = "ldd zeigt alle Shared Libraries die ein Programm benötigt",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was zeigt 'ldd /pfad/zum/programm'?",
                options     = ['A) Dateiformat des Programms', 'B) Benötigte Shared Libraries (dynamische Abhängigkeiten)', 'C) Debug-Symbole', 'D) Programmversion'],
                correct     = 'B',
                explanation = 'ldd = list dynamic dependencies. Zeigt alle .so-Dateien die das Programm braucht.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was macht ldconfig?',
                options     = ['A) Library konfigurieren (kompilieren)', 'B) Shared Library Cache aktualisieren (nach Installation neuer .so-Dateien)', 'C) Alle Libraries auflisten', 'D) Library-Pfade in .bashrc setzen'],
                correct     = 'B',
                explanation = 'ldconfig aktualisiert den ld.so-Cache. Nach neuer Library: ldconfig ausführen!',
                xp_value    = 20,
            ),
        ],
        exam_tip     = (
            "PRÜFUNGSFRAGE: Was macht ldconfig?\n"
            "→ Erstellt/aktualisiert den Shared-Library-Cache (/etc/ld.so.cache)\n"
            "Nach einer neuen Library IMMER ldconfig ausführen!\n"
            "ldd = list dynamic dependencies"
        ),
        memory_tip   = "Merkhilfe: ldd=list deps, ldconfig=update cache, LD_LIBRARY_PATH=runtime override",
        gear_reward  = None,
        faction_reward = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.09 — RPM Grundlagen (vertieft)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id    = "12.09",
        chapter       = 12,
        title         = "RPM Grundlagen",
        mtype         = "SCAN",
        xp            = 90,
        speaker       = "CIPHER",
        story         = (
            "CIPHER: 'Das RPM-Format läuft auf Millionen von Servern, Ghost.\n"
            " RHEL, CentOS, Fedora, AlmaLinux — das Imperium liebt RPM.\n"
            " -ivh, -e, -qa, -ql, -qi — diese Flags sind deine Schlüssel.\n"
            " Kenn sie auswendig. Die Prüfung zeigt keine Gnade.'"
        ),
        why_important = (
            "RPM-Grundbefehle sind Pflicht für LPIC-1 Topic 102.4.\n"
            "Install, Remove, Query-Flags — alle kommen in der Prüfung vor."
        ),
        explanation   = (
            "RPM GRUNDLAGEN — FLAGGEN-ÜBERSICHT:\n\n"
            "INSTALLATION / UPGRADE / ENTFERNEN:\n"
            "  rpm -ivh paket.rpm        install + verbose + Hashmarks\n"
            "  rpm -Uvh paket.rpm        upgrade (installiert auch neu)\n"
            "  rpm -Fvh paket.rpm        freshen (nur upgrade, nicht neu)\n"
            "  rpm -e paketname          Paket entfernen (erase)\n"
            "  rpm -e --nodeps paket     Entfernen ohne Abhängigkeitsprüfung\n\n"
            "QUERY-FLAGS (alle beginnen mit -q):\n"
            "  rpm -q  paket             Ist Paket installiert? (Version)\n"
            "  rpm -qa                   Alle installierten Pakete (query all)\n"
            "  rpm -qi paket             Paket-Info (name, version, desc)\n"
            "  rpm -ql paket             Dateiliste des Pakets (list)\n"
            "  rpm -qf /pfad/zur/datei   Welches Paket besitzt die Datei?\n"
            "  rpm -qd paket             Nur Doku-Dateien des Pakets\n"
            "  rpm -qc paket             Nur Konfig-Dateien des Pakets\n"
            "  rpm -qR paket             Abhängigkeiten (Requires)\n"
            "  rpm -q --changelog paket  Changelog des Pakets\n\n"
            "ABFRAGE OHNE INSTALLATION (aus .rpm-Datei):\n"
            "  rpm -qip paket.rpm        Info aus der .rpm-Datei\n"
            "  rpm -qlp paket.rpm        Dateiliste aus der .rpm-Datei\n\n"
            "VERIFIZIERUNG:\n"
            "  rpm -V  paket             Integrität eines Pakets prüfen\n"
            "  rpm -Va                   Alle installierten Pakete prüfen\n"
            "  rpm -K  paket.rpm         GPG-Signatur einer .rpm-Datei prüfen\n\n"
            "RPM-DATENBANK:\n"
            "  /var/lib/rpm/             Speicherort der RPM-Datenbank\n"
            "  rpm --rebuilddb           Datenbank neu aufbauen (bei Korruption)\n\n"
            "PAKETNAME-FORMAT:\n"
            "  name-version-release.arch.rpm\n"
            "  nginx-1.20.1-9.el8.x86_64.rpm\n"
            "  Felder: Name | Version | Release (Distro-Build) | Architektur"
        ),
        syntax        = "rpm -ivh PKG.rpm  |  rpm -e PKG  |  rpm -qa  |  rpm -ql PKG  |  rpm -qi PKG",
        example       = (
            "rpm -ivh ./nginx-1.20.1-9.el8.x86_64.rpm\n"
            "rpm -qa\n"
            "rpm -qa | grep ssh\n"
            "rpm -qi openssh-server\n"
            "rpm -ql openssh-server\n"
            "rpm -qf /usr/sbin/sshd\n"
            "rpm -qc openssh-server\n"
            "rpm -e nginx"
        ),
        task_description  = "Liste alle installierten RPM-Pakete auf",
        expected_commands = ["rpm -qa"],
        hint_text         = "rpm -qa steht für 'query all' — listet alle installierten Pakete",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welcher rpm-Befehl zeigt die Konfigurationsdateien eines installierten Pakets?",
                options     = [
                    "rpm -ql paket",
                    "rpm -qc paket",
                    "rpm -qi paket",
                    "rpm -qd paket",
                ],
                correct     = 1,
                explanation = (
                    "rpm -qc zeigt nur die Konfigurations-Dateien eines Pakets (config files).\n"
                    "rpm -ql = alle Dateien, rpm -qd = Doku-Dateien, rpm -qi = Paket-Info."
                ),
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was bewirkt 'rpm -Fvh paket.rpm'?",
                options     = [
                    "Installiert das Paket neu, auch wenn noch nicht vorhanden",
                    "Erzwingt die Installation ohne Abhängigkeitsprüfung",
                    "Aktualisiert das Paket nur, wenn es bereits installiert ist (freshen)",
                    "Entfernt das Paket und installiert die neue Version",
                ],
                correct     = 2,
                explanation = (
                    "rpm -F = freshen: aktualisiert nur bereits installierte Pakete.\n"
                    "rpm -U = upgrade: installiert auch wenn Paket noch nicht vorhanden.\n"
                    "rpm -i = install: schlägt fehl wenn Paket bereits installiert ist."
                ),
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "PRÜFUNGS-MERKSÄTZE RPM:\n"
            "  -i  = install (neu, schlägt bei vorhandenem Paket fehl)\n"
            "  -U  = upgrade (install oder upgrade)\n"
            "  -F  = freshen (nur upgrade bestehender Pakete)\n"
            "  -e  = erase (entfernen)\n"
            "  -q  = query (Abfrage-Prefix)\n"
            "  -qa = query all (alle Pakete)\n"
            "  -qf = query file (Datei → Paket)\n"
            "  -ql = query list (Paket → Dateien)\n"
            "  -qi = query info\n"
            "  -qc = query config files\n"
            "  -qd = query doc files"
        ),
        memory_tip        = "Merkhilfe: -ivh = install+verbose+hash. -q Prefix + a/i/l/f/c/d/R = Query-Flags",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.10 — rpm2cpio & Archiv-Extraktion
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id    = "12.10",
        chapter       = 12,
        title         = "rpm2cpio & Archiv-Extraktion",
        mtype         = "CONSTRUCT",
        xp            = 85,
        speaker = "ZARA Z3R0",
        story         = (
            "Zara Z3R0: 'Manchmal willst du nur eine einzelne Datei, Ghost.\n"
            " Kein volles Install — nur extrahieren.\n"
            " rpm2cpio verwandelt ein .rpm in ein cpio-Archiv.\n"
            " cpio -idmv holt dir alles raus. Sauber. Präzise.'"
        ),
        why_important = (
            "rpm2cpio + cpio erlaubt Extraktion aus .rpm ohne Installation.\n"
            "LPIC-1 Topic 102.4 prüft diesen Workflow explizit."
        ),
        explanation   = (
            "RPM2CPIO UND CPIO — ARCHIV-EXTRAKTION:\n\n"
            "GRUNDPRINZIP:\n"
            "  .rpm-Dateien sind im Kern cpio-Archive mit RPM-Header.\n"
            "  rpm2cpio konvertiert .rpm → cpio-Stream.\n"
            "  cpio liest den Stream und extrahiert die Dateien.\n\n"
            "SYNTAX:\n"
            "  rpm2cpio paket.rpm | cpio -idmv\n\n"
            "CPIO-FLAGS:\n"
            "  -i  = extract (entpacken)\n"
            "  -d  = create leading directories (Verzeichnisse anlegen)\n"
            "  -m  = preserve modification time (Zeitstempel behalten)\n"
            "  -v  = verbose (Ausgabe der Dateinamen)\n\n"
            "ANWENDUNGSFÄLLE:\n"
            "  1) Einzelne Datei aus .rpm extrahieren (ohne Installation)\n"
            "  2) Inhalt prüfen bevor man installiert\n"
            "  3) Gelöschte Konfig-Datei aus .rpm wiederherstellen\n\n"
            "BEISPIEL — NUR EINE DATEI EXTRAHIEREN:\n"
            "  rpm2cpio nginx.rpm | cpio -idmv './etc/nginx/nginx.conf'\n\n"
            "INHALT ANZEIGEN (ohne extrahieren):\n"
            "  rpm2cpio paket.rpm | cpio -t        Inhaltsverzeichnis\n"
            "  rpm2cpio paket.rpm | cpio -tv       mit Details\n\n"
            "VERGLEICH MIT DPKG (Debian-Äquivalent):\n"
            "  dpkg -c paket.deb   = rpm2cpio paket.rpm | cpio -t\n"
            "  dpkg-deb -x paket.deb /ziel  =  rpm2cpio paket.rpm | cpio -idmv\n\n"
            "CPIO-ARCHIVE ALLGEMEIN:\n"
            "  cpio -o < liste > archiv.cpio   erstellen (out)\n"
            "  cpio -i < archiv.cpio           entpacken (in)\n"
            "  find . | cpio -o > backup.cpio  mit find kombinieren"
        ),
        syntax        = "rpm2cpio PKG.rpm | cpio -idmv",
        example       = (
            "# Inhalt eines RPM anzeigen:\n"
            "rpm2cpio nginx.rpm | cpio -t\n\n"
            "# Alles extrahieren:\n"
            "rpm2cpio nginx.rpm | cpio -idmv\n\n"
            "# Einzelne Datei extrahieren:\n"
            "rpm2cpio nginx.rpm | cpio -idmv './etc/nginx/nginx.conf'\n\n"
            "# Debian-Äquivalent zum Vergleich:\n"
            "dpkg-deb -x paket.deb /tmp/extract/"
        ),
        task_description  = "Extrahiere alle Dateien aus einem RPM-Paket mit rpm2cpio",
        expected_commands = ["rpm2cpio pkg.rpm | cpio -idmv"],
        hint_text         = "rpm2cpio konvertiert .rpm zu cpio-Stream; cpio -idmv extrahiert (-i=in, -d=dirs, -m=mtime, -v=verbose)",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was macht der Flag '-d' in 'cpio -idmv'?",
                options     = [
                    "Aktiviert Debug-Ausgabe",
                    "Legt fehlende Verzeichnisse automatisch an",
                    "Dekomprimiert gzip-komprimierte Archive",
                    "Löscht die Quelldatei nach der Extraktion",
                ],
                correct     = 1,
                explanation = (
                    "cpio -d erstellt führende Verzeichnisse automatisch beim Extrahieren.\n"
                    "Ohne -d schlägt cpio fehl, wenn ein Zielverzeichnis nicht existiert."
                ),
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl zeigt nur den Inhalt eines .rpm ohne zu extrahieren?",
                options     = [
                    "rpm2cpio paket.rpm | cpio -idmv",
                    "rpm2cpio paket.rpm | cpio -t",
                    "rpm -qlp paket.rpm",
                    "Sowohl B als auch C sind korrekt",
                ],
                correct     = 3,
                explanation = (
                    "Beide Methoden zeigen den Inhalt ohne Installation:\n"
                    "  rpm2cpio paket.rpm | cpio -t  (cpio table of contents)\n"
                    "  rpm -qlp paket.rpm            (rpm query list from package file)"
                ),
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "PRÜFUNGS-MERKSATZ:\n"
            "  rpm2cpio paket.rpm | cpio -idmv\n"
            "  Flags: -i=extract, -d=make dirs, -m=preserve mtime, -v=verbose\n"
            "  Nur Inhaltsverzeichnis: cpio -t (table)\n"
            "  Debian-Äquivalent: dpkg-deb -x oder dpkg -c"
        ),
        memory_tip        = "Merkhilfe: rpm2cpio = RPM zu CPIO. cpio -idmv = In, Dirs, Mtime, Verbose",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.11 — YUM/DNF Paketverwaltung (vertieft)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id    = "12.11",
        chapter       = 12,
        title         = "YUM/DNF Paketverwaltung",
        mtype         = "CONSTRUCT",
        xp            = 95,
        speaker       = "CIPHER",
        story         = (
            "CIPHER: 'rpm kennt keine Repos, Ghost.\n"
            " yum hat das jahrelang übernommen — dnf hat es perfektioniert.\n"
            " install, remove, update, search — beide Werkzeuge sprechen dieselbe Sprache.\n"
            " Lern sie beide. RHEL 7 nutzt yum, RHEL 8+ dnf.'"
        ),
        why_important = (
            "yum und dnf sind die High-Level-Paketmanager für RPM-Systeme.\n"
            "LPIC-1 Topic 102.5 testet Installieren, Entfernen, Suchen und Gruppen."
        ),
        explanation   = (
            "YUM / DNF — HIGH-LEVEL RPM PAKETVERWALTUNG:\n\n"
            "GRUNDBEFEHLE (yum und dnf syntax-kompatibel):\n"
            "  yum install nginx         Paket installieren\n"
            "  dnf install nginx         (moderner Nachfolger)\n"
            "  yum install -y nginx      ohne Rückfrage (yes)\n"
            "  yum localinstall p.rpm    lokale .rpm-Datei installieren\n"
            "  dnf install ./p.rpm       wie localinstall in dnf\n\n"
            "ENTFERNEN:\n"
            "  yum remove nginx          Paket entfernen\n"
            "  dnf remove nginx          (gleiches Ergebnis)\n"
            "  yum autoremove            verwaiste Abhängigkeiten entfernen\n"
            "  dnf autoremove            (wie yum autoremove)\n\n"
            "AKTUALISIEREN:\n"
            "  yum update                alle Pakete aktualisieren\n"
            "  yum update nginx          einzelnes Paket aktualisieren\n"
            "  yum check-update          verfügbare Updates anzeigen (kein Update)\n"
            "  dnf upgrade               wie yum update in dnf\n\n"
            "SUCHEN UND INFO:\n"
            "  yum search nginx          Paket suchen (Name + Beschreibung)\n"
            "  yum info nginx            Paket-Details anzeigen\n"
            "  yum list installed        alle installierten Pakete\n"
            "  yum list available        alle verfügbaren Pakete\n"
            "  yum provides /usr/sbin/httpd  Welches Paket liefert diese Datei?\n"
            "  dnf repoquery --list nginx    Dateien eines Pakets (dnf)\n\n"
            "PAKETGRUPPEN:\n"
            "  yum grouplist             verfügbare Paketgruppen\n"
            "  yum groupinstall 'Development Tools'\n"
            "  yum groupremove  'Development Tools'\n"
            "  yum groupinfo    'Development Tools'\n\n"
            "HISTORY & RÜCKGÄNGIG MACHEN:\n"
            "  yum history               Transaktionsliste\n"
            "  yum history info 5        Details zu Transaktion #5\n"
            "  yum history undo last     letzte Transaktion rückgängig\n"
            "  dnf history               (gleiches Verhalten)\n\n"
            "CACHE:\n"
            "  yum clean all             Cache vollständig leeren\n"
            "  yum clean packages        nur heruntergeladene Pakete\n"
            "  yum makecache             Cache neu aufbauen\n\n"
            "DNF-SPEZIFIKA (RHEL 8+):\n"
            "  dnf repolist              alle aktiven Repos\n"
            "  dnf module list           Module anzeigen (AppStream)\n"
            "  dnf module enable php:8.1 Modul-Stream aktivieren\n"
            "  dnf repoquery --requires nginx  Abhängigkeiten\n\n"
            "APT vs YUM/DNF VERGLEICH:\n"
            "  apt update        =  yum check-update\n"
            "  apt upgrade       =  yum update\n"
            "  apt install       =  yum install\n"
            "  apt remove        =  yum remove\n"
            "  apt search        =  yum search\n"
            "  apt show          =  yum info\n"
            "  apt-cache depends =  yum deplist"
        ),
        syntax        = "yum/dnf install PKG  |  yum/dnf remove PKG  |  yum/dnf update  |  yum/dnf search PKG",
        example       = (
            "yum install -y httpd\n"
            "yum search python3\n"
            "yum info httpd\n"
            "yum provides /usr/sbin/httpd\n"
            "yum update\n"
            "yum remove httpd\n"
            "yum autoremove\n"
            "yum history\n"
            "dnf install nginx\n"
            "dnf repolist\n"
            "dnf module list"
        ),
        task_description  = "Installiere das Paket 'httpd' mit yum ohne Rückfrage",
        expected_commands = ["yum install -y httpd"],
        hint_text         = "yum install -y PAKET installiert ohne interaktive Bestätigung",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welcher Befehl zeigt, welches yum-Paket die Datei /usr/sbin/httpd bereitstellt?",
                options     = [
                    "yum info httpd",
                    "yum list httpd",
                    "yum provides /usr/sbin/httpd",
                    "yum search /usr/sbin/httpd",
                ],
                correct     = 2,
                explanation = (
                    "yum provides /pfad/zur/datei zeigt welches Paket eine Datei oder Capability liefert.\n"
                    "Entspricht 'rpm -qf' und 'dpkg -S' für Debian."
                ),
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'yum update' und 'yum check-update'?",
                options     = [
                    "Kein Unterschied — beide aktualisieren alle Pakete",
                    "check-update zeigt verfügbare Updates ohne zu installieren; update installiert sie",
                    "update prüft nur Abhängigkeiten; check-update führt das Update durch",
                    "check-update aktualisiert nur Sicherheitspakete",
                ],
                correct     = 1,
                explanation = (
                    "yum check-update listet nur verfügbare Updates (kein Download, keine Installation).\n"
                    "yum update lädt Updates herunter und installiert sie.\n"
                    "Analogie: apt update (Listen holen) ≈ yum check-update."
                ),
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "PRÜFUNGS-MERKSÄTZE YUM/DNF:\n"
            "  yum install / remove / update / search / info\n"
            "  yum provides = welches Paket liefert Datei/Capability\n"
            "  yum check-update = Updates anzeigen (kein Install)\n"
            "  yum groupinstall 'Gruppenname'\n"
            "  yum history undo last = Rollback\n"
            "  dnf = Nachfolger von yum (RHEL 8+), gleiche Syntax"
        ),
        memory_tip        = "Merkhilfe: yum/dnf = rpm + Abhängigkeiten + Repos. provides = wer liefert was",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.12 — YUM Repos & Konfiguration
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id    = "12.12",
        chapter       = 12,
        title         = "YUM Repos & Konfiguration",
        mtype         = "SCAN",
        xp            = 90,
        speaker = "ZARA Z3R0",
        story         = (
            "Zara Z3R0: 'Das Imperium kontrolliert die offiziellen RHEL-Repos, Ghost.\n"
            " Wir brauchen eigene Quellen — EPEL, Remi, eigene Mirrors.\n"
            " /etc/yum.repos.d/ ist das Tor.\n"
            " yum repolist zeigt dir was aktiv ist. Konfiguriere es korrekt.'"
        ),
        why_important = (
            "Repository-Konfiguration steuert woher YUM/DNF Pakete holt.\n"
            "LPIC-1 testet .repo-Dateiformat, yum repolist und dnf repoquery."
        ),
        explanation   = (
            "YUM REPOS & KONFIGURATION:\n\n"
            "REPO-VERZEICHNISSE:\n"
            "  /etc/yum.repos.d/         .repo-Dateien (pro Repo eine Datei)\n"
            "  /etc/yum.conf             Haupt-Konfiguration\n"
            "  /etc/dnf/dnf.conf         dnf-Konfiguration (RHEL 8+)\n\n"
            ".repo DATEI FORMAT:\n"
            "  [repo-id]\n"
            "  name=Beschreibung\n"
            "  baseurl=http://mirror.example.com/repo/\n"
            "  enabled=1\n"
            "  gpgcheck=1\n"
            "  gpgkey=http://mirror.example.com/RPM-GPG-KEY\n\n"
            "FELDER:\n"
            "  enabled=1/0     Repo aktiv oder deaktiviert\n"
            "  gpgcheck=1/0    GPG-Signatur prüfen\n"
            "  baseurl         direkter URL\n"
            "  mirrorlist      URL zu einer Mirrorliste\n"
            "  metalink        Fedora/RHEL-Metadaten-Link\n\n"
            "REPO-VERWALTUNG:\n"
            "  yum repolist              aktive Repos anzeigen\n"
            "  yum repolist all          alle (auch deaktivierte) Repos\n"
            "  yum repolist enabled      nur aktivierte Repos\n"
            "  yum repoinfo epel         Details zu einem Repo\n\n"
            "REPO HINZUFÜGEN:\n"
            "  yum-config-manager --add-repo URL\n"
            "  dnf config-manager --add-repo URL\n"
            "  yum-config-manager --enable repo-id\n"
            "  yum-config-manager --disable repo-id\n\n"
            "DNF REPOQUERY:\n"
            "  dnf repoquery nginx           Paket im Repo suchen\n"
            "  dnf repoquery --list nginx    Dateien im Repo-Paket\n"
            "  dnf repoquery --requires nginx  Abhängigkeiten\n"
            "  dnf repoquery --whatprovides /usr/sbin/nginx\n\n"
            "EPEL (Extra Packages for Enterprise Linux):\n"
            "  yum install epel-release  EPEL-Repo aktivieren\n"
            "  Nach Installation: yum install htop (aus EPEL)\n\n"
            "CACHE-PFADE:\n"
            "  /var/cache/yum/           yum Cache-Verzeichnis\n"
            "  /var/cache/dnf/           dnf Cache-Verzeichnis\n"
            "  yum clean all             Cache leeren"
        ),
        syntax        = "yum repolist  |  dnf repoquery PKG  |  yum-config-manager --add-repo URL",
        example       = (
            "yum repolist\n"
            "yum repolist all\n"
            "cat /etc/yum.repos.d/epel.repo\n"
            "ls /etc/yum.repos.d/\n"
            "yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo\n"
            "yum repoinfo base\n"
            "dnf repoquery --list nginx\n"
            "dnf repoquery --requires nginx"
        ),
        task_description  = "Zeige alle aktiven YUM/DNF Repositories",
        expected_commands = ["yum repolist"],
        hint_text         = "yum repolist listet alle aktivierten Repositories auf",
        quiz_questions    = [
            QuizQuestion(
                question    = "In welchem Verzeichnis liegen die YUM/DNF Repository-Konfigurationsdateien?",
                options     = [
                    "/etc/apt/sources.list.d/",
                    "/etc/yum.repos.d/",
                    "/var/lib/rpm/repos/",
                    "/usr/share/yum/repos/",
                ],
                correct     = 1,
                explanation = (
                    "/etc/yum.repos.d/ enthält .repo-Dateien für YUM und DNF.\n"
                    "Jede .repo-Datei kann ein oder mehrere Repository-Abschnitte [repo-id] definieren.\n"
                    "/etc/apt/sources.list.d/ ist das Debian-Äquivalent."
                ),
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was macht 'dnf repoquery --whatprovides /usr/sbin/nginx'?",
                options     = [
                    "Installiert das Paket das /usr/sbin/nginx enthält",
                    "Zeigt alle Pakete die /usr/sbin/nginx als Abhängigkeit haben",
                    "Zeigt welches Repo-Paket die Datei /usr/sbin/nginx bereitstellt",
                    "Listet alle Dateien im nginx-Paket aus dem Repo",
                ],
                correct     = 2,
                explanation = (
                    "dnf repoquery --whatprovides zeigt welches Paket (im Repo) eine Datei oder Capability liefert.\n"
                    "Ähnlich wie 'rpm -qf' aber sucht im Repo, nicht nur unter installierten Paketen."
                ),
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "PRÜFUNGS-MERKSÄTZE YUM REPOS:\n"
            "  /etc/yum.repos.d/ = Repo-Konfigurationsverzeichnis\n"
            "  .repo-Felder: enabled=, gpgcheck=, baseurl=, mirrorlist=\n"
            "  yum repolist = aktive Repos anzeigen\n"
            "  yum repolist all = alle Repos (inkl. deaktivierte)\n"
            "  yum-config-manager --add-repo URL = Repo hinzufügen\n"
            "  dnf repoquery = Paketabfragen im Repo"
        ),
        memory_tip        = "Merkhilfe: /etc/yum.repos.d/*.repo = Debian /etc/apt/sources.list.d/*.list",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.13 — Zypper (SUSE/openSUSE) vertieft
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id    = "12.13",
        chapter       = 12,
        title         = "Zypper (SUSE/openSUSE)",
        mtype         = "SCAN",
        xp            = 80,
        speaker       = "CIPHER",
        story         = (
            "CIPHER: 'Die dritte Paketfamilie, Ghost — SUSE.\n"
            " openSUSE Tumbleweed, SLES, openSUSE Leap.\n"
            " zypper install, remove, update, search, repos.\n"
            " Fünf Befehle. Alle prüfungsrelevant. Lern sie jetzt.'"
        ),
        why_important = (
            "zypper ist der Paketmanager für SUSE Linux / openSUSE.\n"
            "LPIC-1 Topic 102.5 testet zypper als dritte Paketmanager-Familie."
        ),
        explanation   = (
            "ZYPPER — SUSE PAKETMANAGER IM DETAIL:\n\n"
            "GRUNDBEFEHLE (Langform und Kurzform):\n"
            "  zypper install nginx       zypper in nginx\n"
            "  zypper remove  nginx       zypper rm nginx\n"
            "  zypper update              zypper up\n"
            "  zypper search  nginx       zypper se nginx\n"
            "  zypper info    nginx       (kein Kurzalias)\n\n"
            "INSTALLATION:\n"
            "  zypper install -y nginx    ohne Rückfrage\n"
            "  zypper install ./p.rpm     lokale .rpm-Datei\n"
            "  zypper install --no-recommends nginx  ohne empfohlene Pakete\n\n"
            "AKTUALISIEREN:\n"
            "  zypper update             alle Pakete aktualisieren\n"
            "  zypper update nginx       einzelnes Paket\n"
            "  zypper list-updates       verfügbare Updates anzeigen\n"
            "  zypper patch              Patches einspielen\n"
            "  zypper dist-upgrade       Distributions-Upgrade (zypper dup)\n\n"
            "SUCHEN:\n"
            "  zypper search nginx       nach Name/Beschreibung suchen\n"
            "  zypper search -t pattern  nach Mustern suchen\n"
            "  zypper what-provides /usr/sbin/nginx  Datei → Paket\n\n"
            "REPOSITORY-VERWALTUNG:\n"
            "  zypper repos              alle Repos (zypper lr)\n"
            "  zypper repos -d           Repos mit Details\n"
            "  zypper addrepo URL NAME   Repo hinzufügen (zypper ar)\n"
            "  zypper removerepo NAME    Repo entfernen (zypper rr)\n"
            "  zypper refresh            Repo-Metadaten aktualisieren (zypper ref)\n"
            "  zypper modifyrepo -e NAME Repo aktivieren\n"
            "  zypper modifyrepo -d NAME Repo deaktivieren\n\n"
            "PATCHES UND PATTERNS:\n"
            "  zypper patch-check        Verfügbare Patches prüfen\n"
            "  zypper install -t pattern lamp_server  Pattern installieren\n\n"
            "VERIFIER & LOCKS:\n"
            "  zypper verify             Abhängigkeiten prüfen\n"
            "  zypper addlock nginx      Paket sperren (kein Update)\n"
            "  zypper locks              gesperrte Pakete\n\n"
            "VERGLEICH ALLER DREI FAMILIEN:\n"
            "  AKTION          DEBIAN         RHEL/CentOS     SUSE\n"
            "  ─────────────────────────────────────────────────────\n"
            "  Low-Level       dpkg           rpm             rpm\n"
            "  High-Level      apt            yum/dnf         zypper\n"
            "  Install         apt install    yum install     zypper in\n"
            "  Remove          apt remove     yum remove      zypper rm\n"
            "  Update Lists    apt update     yum check-upd   zypper refresh\n"
            "  Upgrade         apt upgrade    yum update      zypper up\n"
            "  Search          apt search     yum search      zypper se\n"
            "  File → Paket    dpkg -S        rpm -qf         zypper wp\n"
            "  Repo hinzuf.    add-apt-repo   yum-config-mgr  zypper ar\n"
            "  Paketformat     .deb           .rpm            .rpm"
        ),
        syntax        = "zypper install PKG  |  zypper remove PKG  |  zypper search PKG  |  zypper repos",
        example       = (
            "zypper search nginx\n"
            "zypper install -y nginx\n"
            "zypper info nginx\n"
            "zypper update\n"
            "zypper list-updates\n"
            "zypper remove nginx\n"
            "zypper repos\n"
            "zypper refresh\n"
            "zypper addrepo https://download.opensuse.org/repositories/network/openSUSE_Leap_15.5/ network\n"
            "zypper what-provides /usr/sbin/nginx"
        ),
        task_description  = "Zeige alle konfigurierten Repositories mit zypper",
        expected_commands = ["zypper repos"],
        hint_text         = "zypper repos (Kurzform: zypper lr) listet alle konfigurierten Repositories",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welcher zypper-Befehl entspricht 'apt update' (Paketlisten aktualisieren)?",
                options     = [
                    "zypper update",
                    "zypper upgrade",
                    "zypper refresh",
                    "zypper check-update",
                ],
                correct     = 2,
                explanation = (
                    "zypper refresh (kurz: zypper ref) aktualisiert die Repo-Metadaten.\n"
                    "Das entspricht 'apt update' (Listen holen) oder 'yum check-update'.\n"
                    "zypper update installiert dann die verfügbaren Aktualisierungen."
                ),
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Mit welchem Befehl fügt man ein neues Repository zu zypper hinzu?",
                options     = [
                    "zypper install-repo URL NAME",
                    "zypper repos --add URL NAME",
                    "zypper addrepo URL NAME",
                    "zypper repo-add URL NAME",
                ],
                correct     = 2,
                explanation = (
                    "zypper addrepo URL NAME (Kurzform: zypper ar) fügt ein neues Repo hinzu.\n"
                    "Danach 'zypper refresh' ausführen um Metadaten zu laden.\n"
                    "Entfernen: zypper removerepo NAME (zypper rr)."
                ),
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "PRÜFUNGS-MERKSÄTZE ZYPPER:\n"
            "  zypper in  = install\n"
            "  zypper rm  = remove\n"
            "  zypper up  = update\n"
            "  zypper se  = search\n"
            "  zypper lr  = repos (list repos)\n"
            "  zypper ref = refresh (Metadaten holen = apt update)\n"
            "  zypper ar  = addrepo\n"
            "  zypper rr  = removerepo\n"
            "  zypper dup = dist-upgrade\n"
            "ALLE DREI nutzen .rpm als Low-Level-Format!"
        ),
        memory_tip        = "Merkhilfe: zypper in/rm/up/se/lr/ref = install/remove/update/search/list-repos/refresh",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.14 — Shared Libraries: ldd, ldconfig, LD_LIBRARY_PATH
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.14",
        chapter      = 12,
        title        = "Shared Libraries: ldd & ldconfig",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara: 'Ein Programm ist nur so stark wie seine Libraries, Ghost.\n"
            " ldd zeigt welche .so-Dateien es braucht.\n"
            " ldconfig aktualisiert den Cache. Ohne Cache — kein Start.'"
        ),
        why_important = (
            "Shared Libraries (*.so) sind Code-Bibliotheken die von mehreren\n"
            "Programmen geteilt werden. LPIC-1 Topic 102.3 testet ldd und ldconfig."
        ),
        explanation  = (
            "SHARED LIBRARIES:\n\n"
            "LDD — LIBRARY DEPENDENCIES:\n"
            "  ldd /usr/bin/ls       Zeigt alle benötigten .so-Dateien\n"
            "  ldd -v /usr/bin/ls    Verbose mit Symbol-Versionen\n"
            "  ldd -r /usr/bin/ls    Fehlende Symbole prüfen\n\n"
            "LDCONFIG — LIBRARY CACHE:\n"
            "  ldconfig              Cache neu aufbauen\n"
            "  ldconfig -p           Alle gecachten Libraries anzeigen\n"
            "  ldconfig -p | grep libssl  Bestimmte Library suchen\n\n"
            "KONFIGURATION:\n"
            "  /etc/ld.so.conf       Haupt-Konfigurationsdatei\n"
            "  /etc/ld.so.conf.d/*.conf  Zusätzliche Library-Pfade\n"
            "  /etc/ld.so.cache      Binärer Cache (von ldconfig erzeugt)\n\n"
            "LD_LIBRARY_PATH:\n"
            "  export LD_LIBRARY_PATH=/opt/myapp/lib:$LD_LIBRARY_PATH\n"
            "  → Temporär für aktuelle Session (Umgebungsvariable)\n\n"
            "SONAME SCHEMA:\n"
            "  libcrypto.so.1.1  = Library.so.MAJOR.MINOR\n"
            "  Symlink: libcrypto.so → libcrypto.so.1.1"
        ),
        syntax       = "ldd /pfad/zum/programm",
        example      = "ldd /usr/bin/ssh | grep -v 'linux-vdso'",
        task_description = "Zeige Library-Abhängigkeiten von /bin/ls mit ldd",
        expected_commands = ["ldd /bin/ls"],
        hint_text    = "ldd /bin/ls zeigt alle Shared Libraries die ls benötigt",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `ldconfig -p`?",
                options  = [
                    "Zeigt alle gecachten Shared Libraries",
                    "Löscht den Library-Cache",
                    "Installiert neue Libraries",
                    "Prüft Library-Abhängigkeiten",
                ],
                correct  = 0,
                explanation = "ldconfig -p gibt den Inhalt des /etc/ld.so.cache aus — alle bekannten Libraries.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "ldd=Abhängigkeiten | ldconfig=Cache | /etc/ld.so.conf=Pfade | LD_LIBRARY_PATH=temporär",
        memory_tip   = "ldd fragt 'Was brauchst du?' | ldconfig sagt 'Wo ist was?' — der Cache-Verwalter.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.15 — Quellcode kompilieren: configure, make, make install
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.15",
        chapter      = 12,
        title        = "Quellcode kompilieren: configure & make",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Kein .deb, kein .rpm. Nur Quellcode und ein Compiler.\n"
            " Drei Befehle: ./configure, make, make install.\n"
            " Das klassische Unix-Trio. Kenne es auswendig.'"
        ),
        why_important = (
            "Quellcode-Kompilierung via autotools (configure/make) ist der\n"
            "klassische Weg Software zu installieren wenn kein Paket existiert."
        ),
        explanation  = (
            "QUELLCODE KOMPILIEREN:\n\n"
            "STANDARD WORKFLOW:\n"
            "  tar xzf software-1.0.tar.gz\n"
            "  cd software-1.0\n"
            "  ./configure --prefix=/usr/local\n"
            "  make\n"
            "  make install      (als root oder mit sudo)\n\n"
            "CONFIGURE-OPTIONEN:\n"
            "  ./configure --help        Alle Optionen anzeigen\n"
            "  ./configure --prefix=/opt  Installations-Prefix\n"
            "  ./configure --with-ssl     Feature aktivieren\n"
            "  ./configure --without-x    Feature deaktivieren\n\n"
            "MAKE-OPTIONEN:\n"
            "  make -j4          4 parallele Jobs (schneller)\n"
            "  make clean        Kompilierte Dateien löschen\n"
            "  make distclean    Auch configure-Dateien löschen\n"
            "  make uninstall    Deinstallieren (wenn unterstützt)\n"
            "  make -n           Dry run (zeigt Befehle ohne Ausführung)\n\n"
            "CHECKINSTALL:\n"
            "  checkinstall      Erstellt .deb/.rpm aus make install\n"
            "  → Sauberes Deinstallieren möglich!"
        ),
        syntax       = "./configure [--prefix=DIR] && make && make install",
        example      = "./configure --prefix=/usr/local --with-ssl && make -j$(nproc) && sudo make install",
        task_description = "Zeige make-Version mit make --version",
        expected_commands = ["make --version"],
        hint_text    = "make --version zeigt die GNU Make Version",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `./configure --prefix=/usr/local`?",
                options  = [
                    "Legt das Installations-Verzeichnis auf /usr/local fest",
                    "Installiert das Programm nach /usr/local",
                    "Kompiliert den Quellcode",
                    "Prüft ob alle Abhängigkeiten installiert sind",
                ],
                correct  = 0,
                explanation = "--prefix legt nur den Ziel-Pfad fest. Die Installation passiert erst mit make install.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "./configure → make → make install. --prefix=/usr/local für benutzerdefinierte Pfade.",
        memory_tip   = "Configure (planen) → Make (bauen) → Make install (einbauen). Wie ein Haus bauen.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.16 — apt Pinning & Preferences
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.16",
        chapter      = 12,
        title        = "apt Pinning: Paket-Versionen fixieren",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara: 'Production läuft auf nginx 1.18. apt würde auf 1.22 updaten.\n"
            " Pinning hält die Version. Eine Preferences-Datei.\n"
            " Kontrolliere was apt updaten darf — und was nicht.'"
        ),
        why_important = (
            "apt Pinning verhindert ungewollte Updates auf kritischen Paketen\n"
            "und ermöglicht Pakete aus anderen Distributions-Zweigen zu mischen."
        ),
        explanation  = (
            "APT PINNING & PREFERENCES:\n\n"
            "DATEI: /etc/apt/preferences oder /etc/apt/preferences.d/*.pref\n\n"
            "SYNTAX:\n"
            "  Package: nginx\n"
            "  Pin: version 1.18.*\n"
            "  Pin-Priority: 1001\n\n"
            "PRIORITÄTS-WERTE:\n"
            "  > 1000  Installieren auch wenn Downgrade nötig\n"
            "  990+    Bevorzugt über alle anderen Quellen\n"
            "  500     Standard-Priorität\n"
            "  100     Backup-Quelle\n"
            "  < 0     Nie installieren\n\n"
            "BEISPIELE:\n"
            "  Pin: release a=stable       Nur aus stable\n"
            "  Pin: release o=Debian       Nur von Debian\n"
            "  Pin: origin packages.nginx.org  Von bestimmtem Server\n\n"
            "PAKETE HOLD SETZEN (einfacherer Weg):\n"
            "  apt-mark hold nginx         Version einfrieren\n"
            "  apt-mark unhold nginx       Einfrieren aufheben\n"
            "  apt-mark showhold           Alle eingefrorenen Pakete"
        ),
        syntax       = "apt-mark hold paketname",
        example      = "apt-mark hold nginx && apt-mark showhold",
        task_description = "Zeige eingefrorene Pakete mit apt-mark showhold",
        expected_commands = ["apt-mark showhold"],
        hint_text    = "apt-mark showhold listet alle Pakete die nicht automatisch aktualisiert werden",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl verhindert, dass `nginx` durch apt aktualisiert wird?",
                options  = [
                    "apt-mark hold nginx",
                    "apt pin nginx",
                    "apt-get freeze nginx",
                    "dpkg --hold nginx",
                ],
                correct  = 0,
                explanation = "apt-mark hold friert ein Paket ein. Beim nächsten apt upgrade wird es übersprungen.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "apt-mark hold=einfrieren | unhold=freigeben | showhold=Liste. Preferences.d für komplexes Pinning.",
        memory_tip   = "hold = 'Stopp, nicht updaten!' | unhold = 'OK, du darfst wieder aktualisieren.'",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.17 — dpkg-reconfigure & dpkg-divert
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.17",
        chapter      = 12,
        title        = "dpkg-reconfigure & dpkg-divert",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ein Paket falsch konfiguriert. Kein Problem.\n"
            " dpkg-reconfigure startet den Setup-Wizard neu.\n"
            " dpkg-divert leitet Dateien um — elegant ohne Paket zu ändern.'"
        ),
        why_important = (
            "dpkg-reconfigure ermöglicht die Neukonfiguration eines Pakets ohne\n"
            "Deinstallation. dpkg-divert schützt lokale Dateien vor Paket-Überschreiben."
        ),
        explanation  = (
            "DPKG-RECONFIGURE:\n\n"
            "  dpkg-reconfigure paketname\n"
            "  → Startet den Debconf-Konfigurations-Dialog neu\n"
            "  dpkg-reconfigure locales    Locale neu konfigurieren\n"
            "  dpkg-reconfigure tzdata     Zeitzone neu setzen\n"
            "  dpkg-reconfigure sshd       SSH-Daemon neu konfigurieren\n"
            "  dpkg-reconfigure -plow paket  Alle Fragen stellen\n"
            "  dpkg-reconfigure -phigh paket Nur wichtige Fragen\n\n"
            "DPKG-DIVERT — DATEI UMLEITUNG:\n"
            "  dpkg-divert --add /etc/nginx/nginx.conf\n"
            "  → Paket-Version wird nach nginx.conf.dpkg-divert umgeleitet\n"
            "  → Deine Version bleibt bei nginx.conf\n\n"
            "  dpkg-divert --list          Alle aktiven Diversions\n"
            "  dpkg-divert --remove /pfad  Diversion entfernen\n\n"
            "ANWENDUNGSFALL:\n"
            "  Paket will /usr/bin/X überschreiben?\n"
            "  → dpkg-divert schützt deine Version"
        ),
        syntax       = "dpkg-reconfigure paketname",
        example      = "dpkg-reconfigure tzdata && dpkg-reconfigure locales",
        task_description = "Zeige dpkg-reconfigure Hilfe mit dpkg-reconfigure --help",
        expected_commands = ["dpkg-reconfigure --help"],
        hint_text    = "dpkg-reconfigure --help zeigt Optionen",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `dpkg-reconfigure tzdata`?",
                options  = [
                    "Startet den Zeitzone-Konfigurations-Dialog des tzdata-Pakets neu",
                    "Installiert tzdata neu",
                    "Deinstalliert und reinstalliert tzdata",
                    "Zeigt die aktuelle Zeitzone",
                ],
                correct  = 0,
                explanation = "dpkg-reconfigure führt die Post-Install-Konfiguration des Pakets erneut aus.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "dpkg-reconfigure = Neustart des Setup-Wizards. dpkg-divert = Datei-Umleitungsschutz.",
        memory_tip   = "RE-configure = nochmal konfigurieren. DIVERT = umleiten (wie Verkehrsumleitung).",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.18 — Snap & Flatpak: Universalpakete
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.18",
        chapter      = 12,
        title        = "Snap & Flatpak: Universelle Pakete",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Distro-unabhängige Pakete. Container für Apps.\n"
            " snap von Canonical. flatpak von Red Hat.\n"
            " Sandboxed. Selbst-enthaltend. Sicher.'"
        ),
        why_important = (
            "Snap und Flatpak sind moderne Paketformate die Anwendungen distro-unabhängig\n"
            "und sandboxed ausliefern. Teil des modernen Linux-Ökosystems."
        ),
        explanation  = (
            "SNAP (Canonical/Ubuntu):\n\n"
            "  snap find firefox           Paket suchen\n"
            "  snap install firefox        Installieren\n"
            "  snap remove firefox         Entfernen\n"
            "  snap list                   Installierte Snaps\n"
            "  snap refresh                Alle Snaps aktualisieren\n"
            "  snap refresh firefox        Einzelnes Snap aktualisieren\n"
            "  snap connections firefox    Interfaces/Berechtigungen\n"
            "  snapd                       Snap-Daemon (läuft immer)\n\n"
            "FLATPAK (freedesktop.org):\n\n"
            "  flatpak search firefox\n"
            "  flatpak install flathub org.mozilla.firefox\n"
            "  flatpak run org.mozilla.firefox\n"
            "  flatpak list\n"
            "  flatpak uninstall org.mozilla.firefox\n"
            "  flatpak update\n\n"
            "REPOS (Remotes):\n"
            "  flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo\n"
            "  flatpak remotes"
        ),
        syntax       = "snap install|remove|list|refresh PAKET",
        example      = "snap list && snap find vlc | head -5",
        task_description = "Zeige installierte Snaps mit snap list",
        expected_commands = ["snap list"],
        hint_text    = "snap list zeigt alle installierten Snap-Pakete",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Aussage über Snap-Pakete ist korrekt?",
                options  = [
                    "Snap-Pakete sind selbst-enthaltend und sandboxed",
                    "Snap nutzt /etc/apt/sources.list als Repository",
                    "Snap ist nur für Red Hat Systeme verfügbar",
                    "Snap-Pakete können nicht mit dpkg entfernt werden",
                ],
                correct  = 0,
                explanation = "Snaps sind selbst-enthaltend (alle Deps enthalten) und laufen in einer Sandbox.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "snap install/remove/list/refresh. snapd muss laufen. Flatpak: remotes verwalten.",
        memory_tip   = "Snap = Ubuntu-Container-App. Flatpak = Distro-neutral. Beide: sandboxed.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.19 — RPM Signatur & Repository-Sicherheit
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.19",
        chapter      = 12,
        title        = "RPM Signaturen & Repo-Sicherheit",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara: 'Ein Paket aus dem Netz. Vertrauenswürdig?\n"
            " Prüfe die Signatur. Importiere den GPG-Key.\n"
            " Kein Key — kein Install. Sicherheit zuerst.'"
        ),
        why_important = (
            "Paket-Signaturen verhindern das Installieren manipulierter Software.\n"
            "Sowohl apt als auch rpm/dnf verwenden GPG zur Verifikation."
        ),
        explanation  = (
            "PAKET-SIGNATUREN:\n\n"
            "RPM GPG-KEYS:\n"
            "  rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release\n"
            "  rpm -qa gpg-pubkey           Importierte Keys anzeigen\n"
            "  rpm --checksig paket.rpm     Signatur prüfen\n"
            "  rpm -K paket.rpm             wie --checksig\n\n"
            "YUM/DNF REPO-KEYS:\n"
            "  /etc/yum.repos.d/rhel.repo: gpgcheck=1\n"
            "  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release\n\n"
            "APT GPG-KEYS:\n"
            "  apt-key list                 Alle vertrauenswürdigen Keys\n"
            "  apt-key add key.asc          Key importieren (veraltet)\n"
            "  gpg --dearmor key.asc > /etc/apt/keyrings/repo.gpg  (modern)\n"
            "  In sources.list: signed-by=/etc/apt/keyrings/repo.gpg\n\n"
            "DEBSIG:\n"
            "  dpkg-sig --verify paket.deb  .deb Signatur prüfen\n\n"
            "WARUM WICHTIG:\n"
            "  Supply-Chain-Angriffe via manipulierte Pakete sind real!\n"
            "  gpgcheck=1 in repos und Signaturen prüfen ist Pflicht."
        ),
        syntax       = "rpm --checksig paket.rpm",
        example      = "rpm -qa gpg-pubkey --qf '%{NAME}-%{VERSION}\\n'",
        task_description = "Prüfe importierte GPG-Keys mit rpm -qa gpg-pubkey",
        expected_commands = ["rpm -qa gpg-pubkey"],
        hint_text    = "rpm -qa gpg-pubkey listet alle importierten GPG-Schlüssel",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `rpm --checksig paket.rpm`?",
                options  = [
                    "Prüft die GPG-Signatur des RPM-Pakets",
                    "Installiert das Paket mit Signaturprüfung",
                    "Erstellt eine Signatur für das Paket",
                    "Aktualisiert den GPG-Key des Pakets",
                ],
                correct  = 0,
                explanation = "--checksig verifiziert die Paket-Signatur gegen importierte GPG-Keys.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "rpm --checksig/-K prüft Signatur. rpm --import importiert Key. gpgcheck=1 in .repo.",
        memory_tip   = "checksig = Unterschrift prüfen. --import = Key ins Vertrauen aufnehmen.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.20 — pip & Python-Paket-Verwaltung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.20",
        chapter      = 12,
        title        = "pip: Python-Paketverwaltung",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Python-Tools. Häufig aus pip, nicht aus apt.\n"
            " pip install. Virtuelle Environments.\n"
            " Wissen für Automatisierungs-Skripte in NeonGrid.'"
        ),
        why_important = (
            "pip ist der Python-Paketmanager. venv ermöglicht isolierte\n"
            "Python-Umgebungen ohne System-Python zu verändern."
        ),
        explanation  = (
            "PIP — PYTHON PACKAGE INSTALLER:\n\n"
            "GRUNDBEFEHLE:\n"
            "  pip install requests         Paket installieren\n"
            "  pip install requests==2.28.0  Specific version\n"
            "  pip install -r requirements.txt  Aus Datei\n"
            "  pip uninstall requests\n"
            "  pip list                     Installierte Pakete\n"
            "  pip show requests            Paket-Info\n"
            "  pip search requests          Suchen (veraltet, PyPI direkt)\n"
            "  pip freeze > requirements.txt  Dependencies exportieren\n"
            "  pip install --upgrade pip    pip selbst aktualisieren\n\n"
            "VIRTUAL ENVIRONMENTS (venv):\n"
            "  python3 -m venv myenv        Neues venv\n"
            "  source myenv/bin/activate    Aktivieren\n"
            "  deactivate                   Deaktivieren\n"
            "  rm -rf myenv                 Löschen\n\n"
            "SYSTEM VS USER:\n"
            "  pip install --user requests  Nur für aktuellen User (~/.local)\n"
            "  pip install requests         System-weit (als root)\n\n"
            "PIP3 vs PIP:\n"
            "  pip3 = Python 3 | pip = Systemstandard"
        ),
        syntax       = "pip install PAKET [==VERSION]",
        example      = "pip3 install ansible && pip3 list | grep ansible",
        task_description = "Zeige installierte pip-Pakete mit pip3 list",
        expected_commands = ["pip3 list"],
        hint_text    = "pip3 list zeigt alle installierten Python-3-Pakete",
        quiz_questions = [
            QuizQuestion(
                question = "Wie installiert man pip-Pakete nur für den aktuellen User?",
                options  = [
                    "pip install --user paketname",
                    "pip install --local paketname",
                    "pip install --home paketname",
                    "pip install -u paketname",
                ],
                correct  = 0,
                explanation = "--user installiert nach ~/.local/lib/python3.x/site-packages/ statt System-weit.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "pip install=install | pip list=liste | pip freeze=requirements.txt | pip --user=nur User",
        memory_tip   = "pip freeze = einfrieren was installiert ist (für requirements.txt). --user = kein root nötig.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.21 — QUIZ: Paketverwaltung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.21",
        chapter      = 12,
        title        = "QUIZ — Paketverwaltung Wissenstest",
        mtype        = "QUIZ",
        xp           = 150,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Vor dem Endkampf ein Test, Ghost.\n"
            " apt, dpkg, rpm, yum, zypper — alle in einem Quiz.\n"
            " Topic 102.4 und 102.5. No excuses.'"
        ),
        why_important = "Quiz-Wiederholung für LPIC-1 Prüfung Topic 102.4/102.5",
        explanation   = "Beantworte die Fragen zur Paketverwaltung.",
        syntax        = "",
        example       = "",
        task_description = "Quiz: Paketverwaltung",
        expected_commands = [],
        hint_text     = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher Befehl zeigt welches dpkg-Paket die Datei /usr/bin/curl enthält?",
                options    = [
                    "A) dpkg -l curl",
                    "B) dpkg -L curl",
                    "C) dpkg -S /usr/bin/curl",
                    "D) dpkg -q /usr/bin/curl",
                ],
                correct    = "C",
                explanation = (
                    "dpkg -S /pfad sucht welches Paket die Datei besitzt.\n"
                    "dpkg -L paket listet Dateien EINES Pakets.\n"
                    "Merkhilfe: -S = Search (Datei → Paket), -L = List (Paket → Dateien)"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen 'apt remove' und 'apt purge'?",
                options    = [
                    "A) remove ist schneller, purge ist sicherer",
                    "B) remove lässt Konfigurationsdateien, purge löscht alles",
                    "C) remove löscht alles, purge lässt Konfigurationsdateien",
                    "D) Kein Unterschied",
                ],
                correct    = "B",
                explanation = (
                    "apt remove = Paket entfernen, Konfigurationsdateien bleiben\n"
                    "apt purge  = Paket + alle Konfigurationsdateien entfernen\n"
                    "Entspricht: dpkg -r (remove) vs dpkg -P (purge)"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welcher rpm-Befehl zeigt alle installierten Pakete?",
                options    = [
                    "A) rpm -ql",
                    "B) rpm -qi",
                    "C) rpm -qa",
                    "D) rpm -qf",
                ],
                correct    = "C",
                explanation = (
                    "rpm -q = query, -a = all\n"
                    "rpm -qa = Query All installed packages\n"
                    "rpm -ql = list files of package\n"
                    "rpm -qi = info about package\n"
                    "rpm -qf = which package owns this file"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Was macht 'ldconfig'?",
                options    = [
                    "A) Listet alle installierten Libraries",
                    "B) Aktualisiert den Shared-Library-Cache",
                    "C) Installiert eine neue Library",
                    "D) Zeigt Abhängigkeiten eines Programms",
                ],
                correct    = "B",
                explanation = (
                    "ldconfig liest /etc/ld.so.conf und erstellt/aktualisiert\n"
                    "den Cache-Index /etc/ld.so.cache.\n"
                    "Nach dem Hinzufügen einer neuen Library IMMER ldconfig aufrufen!"
                ),
                xp_value   = 30,
            ),
            QuizQuestion(
                question   = "Welches Tool entspricht auf SUSE dem 'apt' auf Debian?",
                options    = [
                    "A) rpm",
                    "B) yum",
                    "C) dnf",
                    "D) zypper",
                ],
                correct    = "D",
                explanation = (
                    "Paketmanager-Familien:\n"
                    "  Debian/Ubuntu: dpkg (low) + apt (high)\n"
                    "  RHEL/CentOS:   rpm (low) + yum/dnf (high)\n"
                    "  SUSE/openSUSE: rpm (low) + zypper (high)"
                ),
                xp_value   = 30,
            ),
        ],
        exam_tip     = (
            "LPIC-1 Paketverwaltungs-Schwerpunkte:\n"
            "  - dpkg -i/-r/-P/-l/-L/-S kennen\n"
            "  - apt update vs apt upgrade (Reihenfolge!)\n"
            "  - rpm -i/-e/-q/-qa/-ql/-qf kennen\n"
            "  - dpkg↔rpm Äquivalenz-Paare\n"
            "  - ldconfig nach neuer Library"
        ),
        memory_tip   = "dpkg -i=install, -r=remove, -P=purge (config weg!), -l=list, -L=list-files, -S=search-file. apt update (Liste)→upgrade (Pakete). rpm -q/qa/ql/qf.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 12.BOSS — PACKAGE DAEMON v12.0
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "12.boss",
        chapter      = 12,
        title        = "BOSS — PACKAGE DAEMON v12.0",
        mtype        = "BOSS",
        xp           = 475,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM ALERT: PACKAGE DAEMON v12.0 aktiv.\n"
            "Er hat die APT-Quellen manipuliert. Backdoor-Pakete eingeschleust.\n"
            "Alle Updates kommen jetzt vom Imperium-Server.\n"
            "Zara Z3R0: 'Bereinige die sources.list. Prüfe installierte Pakete.\n"
            " Finde die Backdoor. Lösche sie. Jetzt.'"
        ),
        why_important = "Abschluss-Boss für Topic 102.4/102.5",
        explanation  = (
            "BOSS-CHALLENGE: Package Gauntlet\n\n"
            "Deine Mission:\n"
            "1) Paketlisten aktualisieren\n"
            "2) Verdächtiges Paket identifizieren\n"
            "3) Paket-Eigentümer einer Datei finden\n"
            "4) Backdoor-Paket purgen\n\n"
            "KOMMANDOS:\n"
            "  apt update\n"
            "  dpkg -l | grep -i backdoor\n"
            "  dpkg -S /usr/bin/mystery\n"
            "  apt purge mystery-package\n"
            "  apt autoremove\n"
            "  ldconfig"
        ),
        syntax       = "",
        example      = (
            "apt update\n"
            "dpkg -l\n"
            "dpkg -S /usr/bin/mystery\n"
            "apt purge mystery-package\n"
            "apt autoremove\n"
            "rpm -qa  # auf RPM-Systemen"
        ),
        ascii_art    = """
  ██████╗  █████╗  ██████╗██╗  ██╗██████╗  ██████╗  ██████╗ ██████╗
  ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗
  ██████╔╝███████║██║     █████╔╝ ██║  ██║██║   ██║██║   ██║██████╔╝
  ██╔══██╗██╔══██║██║     ██╔═██╗ ██║  ██║██║   ██║██║   ██║██╔══██╗
  ██████╔╝██║  ██║╚██████╗██║  ██╗██████╔╝╚██████╔╝╚██████╔╝██║  ██║
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝

  ┌─ PACKAGE MANAGER COMPROMISED ─────────────────────────────────────┐
  │  apt update :: MIRROR POISONED   backdoor-agent: INSTALLED       │
  │  dpkg -l :: 666 UNKNOWN PACKAGES  rpm: DATABASE CORRUPTED        │
  │  /var/cache/apt: TAINTED   pip: MALICIOUS PACKAGES INJECTED      │
  └───────────────────────────────────────────────────────────────────┘

                    ⚡ CHAOSWERK FACTION :: CHAPTER 12 BOSS ⚡""",
        story_transitions = [
            "Backdoor-Agent installiert sich schneller als du löschen kannst.",
            "dpkg -l zeigt seine Tarnung. apt purge trifft ihn tief.",
            "Dependency-Tree hält ihn am Leben. apt autoremove schneidet frei.",
            "Letztes Paket. Konfiguration gelöscht. System sauber.",
        ],
        task_description = "BOSS: Bereinige das System — entferne Paket 'backdoor-agent' vollständig inkl. Config",
        expected_commands = ["apt purge backdoor-agent"],
        hints = [
            "Ein Auflistungsbefehl wie 'apt' wird benötigt.",
            "Versuche: apt purge backdoor-agent",
            "Der vollständige Befehl: apt purge backdoor-agent",
        ],
        hint_text    = "apt purge entfernt Paket UND Konfigurationsdateien vollständig",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen 'dpkg -r' und 'dpkg -P'?",
                options     = ['A) Kein Unterschied', 'B) -r entfernt Paket (Konfig bleibt), -P purge (Konfig auch gelöscht)', 'C) -r ist für RHEL, -P für Debian', 'D) -P ist sicherer'],
                correct     = 'B',
                explanation = 'dpkg -r = remove (Konfigurationsdateien bleiben). dpkg -P = purge (alles weg, inkl. /etc-Dateien).',
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "apt-get upgrade vs apt-get dist-upgrade — was ist der kritische Unterschied?",
                options     = [
                    'A) Kein Unterschied — Aliase',
                    'B) upgrade: keine neuen/gelöschten Pakete. dist-upgrade: kann Pakete hinzufügen/entfernen',
                    'C) dist-upgrade installiert eine neue Distribution',
                    'D) upgrade ist für Kernel, dist-upgrade für Userspace',
                ],
                correct     = 'B',
                explanation = 'upgrade: aktualisiert nur was installiert ist, keine Dependency-Änderungen. dist-upgrade: löst Konflikte durch Hinzufügen/Entfernen von Paketen.',
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "dpkg -S /usr/bin/ssh — was gibt das zurück?",
                options     = [
                    'A) Fehler: -S existiert nicht',
                    'B) Den Paketnamen der /usr/bin/ssh enthält (openssh-client)',
                    'C) Die Größe der Datei',
                    'D) MD5-Checksum der Datei',
                ],
                correct     = 'B',
                explanation = 'dpkg -S DATEI = sucht welches Paket die Datei enthält (Search). dpkg -L PAKET = listet Dateien eines Pakets.',
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "rpm -qf /etc/ssh/sshd_config — was gibt das zurück?",
                options     = [
                    'A) Inhalt der Konfigurationsdatei',
                    'B) Das RPM-Paket das diese Datei installiert hat',
                    'C) Fehler: rpm hat kein -qf Flag',
                    'D) MD5-Checksum der Datei',
                ],
                correct     = 'B',
                explanation = 'rpm -qf FILE = query file — welches Paket besitzt diese Datei? Äquivalent zu dpkg -S auf RHEL-Systemen.',
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Nach Installation einer neuen Shared Library — was ist ZWINGEND nötig?",
                options     = [
                    'A) Neustart des Systems',
                    'B) ldconfig ausführen (aktualisiert /etc/ld.so.cache)',
                    'C) apt update',
                    'D) depmod -a',
                ],
                correct     = 'B',
                explanation = 'ldconfig aktualisiert den Shared-Library-Cache (/etc/ld.so.cache). Ohne ldconfig findet der Linker neue .so-Dateien nicht. /etc/ld.so.conf definiert Suchpfade.',
                xp_value    = 30,
            ),
        ],
        exam_tip     = (
            "LPIC-1 FINAL PACKAGE CHECK:\n"
            "  dpkg -i/-r/-P/-l/-L/-S\n"
            "  apt update → apt upgrade (Reihenfolge!)\n"
            "  rpm -ivh/-e/-qa/-ql/-qf\n"
            "  yum/dnf install/remove/search\n"
            "  zypper in/rm/se\n"
            "  ldd = Library-Deps, ldconfig = Cache"
        ),
        memory_tip   = "Merkhilfe: purge = alles weg inkl. Config",
        gear_reward  = "hardware_scanner",
        faction_reward = ("Root Collective", 40),
    ),
]
