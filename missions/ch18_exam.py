"""
NeonGrid-9 :: Kapitel 18 — EXAM PROTOCOL
LPIC-1 Prüfungssimulation — alle Topics 101–110

"Das ist kein Training mehr, Ghost.
 Das ist die echte Prüfung.
 LPIC-1: 60 Fragen, 90 Minuten, 500 Punkte zum Bestehen.
 Du hast 17 Kapitel trainiert.
 Jetzt zeigst du, was du gelernt hast."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_18_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 18.01 — Exam Block 1: Hardware, Boot, Kernel (101.x)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.01",
        chapter      = 18,
        title        = "Exam Block 1 — Hardware & Boot (101.x)",
        mtype        = "QUIZ",
        xp           = 115,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 1 gestartet. Themen: Hardware, BIOS/UEFI,\n"
            " Boot-Prozess, GRUB2, systemd, Runlevel und Kernel.\n"
            " 12 Fragen. Keine Hilfen. Kein Hint.\n"
            " Zeig, was du weißt.'"
        ),
        why_important = "LPIC-1 Exam 101: Topics 101.1 / 101.2 / 101.3",
        ascii_art = """
  ███████╗██╗  ██╗ █████╗ ███╗   ███╗    ██████╗ ██████╗  ██████╗ ████████╗ ██████╗  ██████╗ ██████╗ ██╗
  ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║    ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗██║
  █████╗   ╚███╔╝ ███████║██╔████╔██║    ██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║
  ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║    ██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║
  ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║    ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗╚██████╔╝███████╗
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝

  [ CHAPTER 18 :: EXAM PROTOCOL 101 ]
  > LPI-101 exam mode. 60 questions. 60 minutes. 500/800 to pass.""",
        story_transitions = [
            "17 Kapitel hinter dir. Das Wissen sitzt. Jetzt der Test.",
            "LPIC-1: zwei Prüfungen, je 500/800 Punkte. Keine Lücken.",
            "Examinator wartet. Keine Hints. Keine zweite Chance.",
            "NeonGrid-9 hat dich vorbereitet. Beweise es.",
        ],
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "12 Prüfungsfragen: Hardware, Boot & Kernel.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl zeigt PCI-Geräte im System an?",
                options  = ["lsusb", "lspci", "lshw -pci", "dmidecode --pci"],
                correct  = 1,
                explanation = "lspci listet alle PCI-Geräte. lsusb für USB-Geräte, dmidecode für BIOS/SMBIOS-Infos.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welchem Verzeichnis befinden sich Device-Dateien unter Linux?",
                options  = ["/sys", "/proc", "/dev", "/run"],
                correct  = 2,
                explanation = "/dev enthält Device-Dateien (Blockgeräte, Zeichengeräte). /sys = sysfs (Kernel-Objekte), /proc = procfs.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was ist die Aufgabe von GRUB2's 'grub.cfg'?",
                options  = [
                    "Enthält das Kernel-Image",
                    "Definiert Boot-Einträge und Kernel-Parameter",
                    "Speichert BIOS-Einstellungen",
                    "Enthält die Initramfs",
                ],
                correct  = 1,
                explanation = "grub.cfg enthält die Menüeinträge, Kernel-Pfade und Boot-Parameter. Wird von grub-mkconfig generiert — nie manuell bearbeiten!",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher systemd-Befehl setzt das Standard-Boot-Target dauerhaft?",
                options  = [
                    "systemctl default graphical.target",
                    "systemctl set-default graphical.target",
                    "systemctl enable graphical.target --default",
                    "systemctl boot graphical.target",
                ],
                correct  = 1,
                explanation = "systemctl set-default TARGET setzt das Default-Target (Link /etc/systemd/system/default.target). systemctl get-default zeigt es an.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was entspricht SysVinit Runlevel 3 in systemd?",
                options  = ["rescue.target", "multi-user.target", "graphical.target", "network.target"],
                correct  = 1,
                explanation = "Runlevel 3 = Multi-User ohne GUI → multi-user.target. Runlevel 5 = mit GUI → graphical.target. Runlevel 1 = rescue.target.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt alle geladenen Kernel-Module an?",
                options  = ["modinfo", "modprobe -l", "lsmod", "insmod --list"],
                correct  = 2,
                explanation = "lsmod liest /proc/modules und zeigt Name, Größe und Abhängigkeiten aller geladenen Module.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Wie wird ein Kernel-Modul dauerhaft auf die Blacklist gesetzt?",
                options  = [
                    "rmmod --permanent MODUL",
                    "'blacklist MODUL' in /etc/modprobe.d/blacklist.conf",
                    "modprobe -b MODUL",
                    "echo MODUL >> /etc/modules.deny",
                ],
                correct  = 1,
                explanation = "Blacklist-Einträge in /etc/modprobe.d/*.conf mit 'blacklist MODULNAME' verhindern das automatische Laden durch udev.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was gibt 'uname -r' aus?",
                options  = ["CPU-Architektur", "Kernel-Release-Version", "Hostname", "OS-Name"],
                correct  = 1,
                explanation = "uname -r = Kernel-Release (z.B. 6.1.0-neongrid9). -a = alle Infos, -m = Architektur, -s = Kernel-Name.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welche Datei enthält Kernel-Boot-Parameter für das aktuelle System?",
                options  = ["/etc/kernel/cmdline", "/proc/cmdline", "/boot/cmdline", "/sys/kernel/cmdline"],
                correct  = 1,
                explanation = "/proc/cmdline zeigt die beim Boot übergebenen Kernel-Parameter — z.B. root=, quiet, splash.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl lädt ein Modul mit all seinen Abhängigkeiten?",
                options  = ["insmod", "modprobe", "rmmod", "depmod"],
                correct  = 1,
                explanation = "modprobe löst Abhängigkeiten auf und lädt alle nötigen Module. insmod lädt nur das angegebene Modul ohne Abhängigkeiten.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was ist die Funktion von initramfs beim Boot?",
                options  = [
                    "Lädt GRUB2",
                    "Stellt temporäres Root-Dateisystem bereit bis echtes / gemountet wird",
                    "Initialisiert die Netzwerkschnittstellen",
                    "Komprimiert den Kernel",
                ],
                correct  = 1,
                explanation = "initramfs (Initial RAM Filesystem) enthält Treiber und Tools um das echte Root-Filesystem zu mounten — essenziell für LVM, LUKS, NFS-Root.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Mit welchem sysctl-Befehl wird IPv4-Forwarding dauerhaft aktiviert?",
                options  = [
                    "sysctl net.ipv4.ip_forward=1",
                    "sysctl -w net.ipv4.ip_forward=1 && sysctl -p",
                    "echo 1 > /proc/sys/net/ipv4/ip_forward",
                    "sysctl --enable net.ipv4.ip_forward",
                ],
                correct  = 1,
                explanation = "-w setzt sofort, -p lädt /etc/sysctl.conf dauerhaft. Nur -p macht es persistent nach Neustart.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "101.x: lspci/lsusb | grub-mkconfig | set-default | multi-user.target | lsmod | modprobe | /proc/cmdline",
        memory_tip   = "Boot-Reihenfolge: BIOS/UEFI → GRUB2 → Kernel → initramfs → systemd → Targets",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.02 — Exam Block 2: Dateisystem & Berechtigungen (102.x / 104.x)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.02",
        chapter      = 18,
        title        = "Exam Block 2 — Dateisystem & Rechte (102.x/104.x)",
        mtype        = "QUIZ",
        xp           = 180,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 2. Partitionen, Dateisysteme,\n"
            " Berechtigungen, Links, FHS.\n"
            " Und Pakete — dpkg, apt, rpm.\n"
            " 12 Fragen. Die Uhr läuft.'"
        ),
        why_important = "LPIC-1 Exam 101: Topics 102.4 / 102.5 / 104.1 / 104.5",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "12 Prüfungsfragen: Dateisystem, Rechte & Pakete.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl erstellt ein ext4-Dateisystem auf /dev/sdb1?",
                options  = ["mkfs /dev/sdb1", "mkfs.ext4 /dev/sdb1", "format /dev/sdb1 ext4", "fdisk /dev/sdb1 --fs ext4"],
                correct  = 1,
                explanation = "mkfs.ext4 (oder mkfs -t ext4) erstellt ein ext4-Dateisystem. fdisk partitioniert nur, format gibt es nicht.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was bedeutet chmod 750 auf eine Datei?",
                options  = [
                    "rwxr-xr-x (Owner rwx, Group r-x, Other r-x)",
                    "rwxr-x--- (Owner rwx, Group r-x, Other ---)",
                    "rwx------ (Owner rwx, sonst nichts)",
                    "rwxrwxr-x (Owner rwx, Group rwx, Other r-x)",
                ],
                correct  = 1,
                explanation = "750 = 7(rwx) 5(r-x) 0(---): Owner lesen/schreiben/ausführen, Gruppe lesen/ausführen, Andere nichts.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt den Inode einer Datei an?",
                options  = ["ls -l", "ls -i", "stat", "ls -li"],
                correct  = 3,
                explanation = "ls -i zeigt Inode-Nummer. ls -li zeigt Inode + alle Details. stat zeigt ebenfalls Inode.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was ist ein Hard Link?",
                options  = [
                    "Ein Zeiger auf eine andere Datei (Pfad)",
                    "Ein zweiter Verzeichniseintrag der auf denselben Inode zeigt",
                    "Eine komprimierte Kopie der Datei",
                    "Ein symbolischer Verweis der Verzeichnisse unterstützt",
                ],
                correct  = 1,
                explanation = "Hard Links teilen denselben Inode — gleiche Daten, zwei Namen. Löschen eines entfernt nur den Namen, Daten bleiben bis letzter Link gelöscht. Kein Hard Link auf Verzeichnisse (außer . und ..).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welchem FHS-Verzeichnis liegen systemweite Konfigurationsdateien?",
                options  = ["/usr/etc", "/opt", "/etc", "/var/config"],
                correct  = 2,
                explanation = "/etc enthält systemweite Konfigurationsdateien. /usr = User-Programme, /opt = optionale Software, /var = variable Daten.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher dpkg-Befehl listet alle Dateien eines installierten Pakets auf?",
                options  = ["dpkg -s paket", "dpkg -L paket", "dpkg -l paket", "dpkg -c paket"],
                correct  = 1,
                explanation = "dpkg -L = List files (installiert). dpkg -s = Status. dpkg -l = list packages. dpkg -c = Contents (von .deb-Datei, nicht installiert).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was macht 'apt-cache depends paket'?",
                options  = [
                    "Installiert Paket mit allen Abhängigkeiten",
                    "Zeigt alle Abhängigkeiten eines Pakets",
                    "Überprüft ob Abhängigkeiten erfüllt sind",
                    "Löscht verwaiste Abhängigkeiten",
                ],
                correct  = 1,
                explanation = "apt-cache depends zeigt alle Abhängigkeiten (Depends, Recommends, Suggests). apt-cache rdepends zeigt umgekehrte Abhängigkeiten.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher rpm-Befehl findet heraus, welchem Paket /usr/bin/python3 gehört?",
                options  = ["rpm -ql python3", "rpm -qf /usr/bin/python3", "rpm -qi /usr/bin/python3", "rpm -qa python3"],
                correct  = 1,
                explanation = "rpm -qf FILE = query which package owns FILE. -ql = list files of package. -qi = info about package. -qa = list all packages.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welchen Befehl verwendet man zum Überprüfen und Reparieren eines ext4-Dateisystems?",
                options  = ["fsck.ext4", "e2fsck", "mkfs.ext4 -r", "tune2fs -c"],
                correct  = 1,
                explanation = "e2fsck (oder fsck.ext4 — beide identisch) prüft und repariert ext2/3/4-Dateisysteme. Nur bei unmounted oder read-only filesystem ausführen!",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was bedeutet das Sticky Bit auf einem Verzeichnis?",
                options  = [
                    "Nur Root kann Dateien darin löschen",
                    "Jeder darf schreiben, aber nur Eigentümer kann eigene Dateien löschen",
                    "Verzeichnis wird beim Löschen nicht gelöscht",
                    "Alle Dateien darin erben die Gruppe des Verzeichnisses",
                ],
                correct  = 1,
                explanation = "Sticky Bit (chmod +t oder 1000) auf /tmp: Jeder kann Dateien anlegen, aber nur der Eigentümer (oder root) kann eigene Dateien löschen.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt den freien Speicherplatz aller gemounteten Dateisysteme?",
                options  = ["du -h", "df -h", "lsblk -f", "mount -l"],
                correct  = 1,
                explanation = "df -h (disk free, human-readable) zeigt freien/genutzten Platz pro gemountet Dateisystem. du = disk usage (Verzeichnisgröße).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welcher Datei werden permanente Mount-Einträge konfiguriert?",
                options  = ["/etc/mounts", "/etc/fstab", "/proc/mounts", "/etc/mtab"],
                correct  = 1,
                explanation = "/etc/fstab enthält permanente Mount-Konfiguration (device, mountpoint, fstype, options, dump, pass). /proc/mounts = aktuelle Mounts.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "104.x: mkfs.ext4 | chmod 750 | ls -i (inode) | Hard Link = gleicher Inode | /etc = Configs | dpkg -L = files",
        memory_tip   = "Oktalrechte: 4=r 2=w 1=x | SUID=4000 SGID=2000 Sticky=1000 | chmod 4755 = SUID+rwxr-xr-x",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.03 — Exam Block 3: Shell, Prozesse & Netzwerk (103.x / 109.x)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.03",
        chapter      = 18,
        title        = "Exam Block 3 — Shell, Prozesse & Netzwerk (103.x/109.x)",
        mtype        = "QUIZ",
        xp           = 180,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 3. Pipes, Redirects, Textfilter.\n"
            " Prozesse, Signale, Prioritäten.\n"
            " TCP/IP, DNS, SSH, Firewall.\n"
            " 12 Fragen. Fokus.'"
        ),
        why_important = "LPIC-1 Exam 101/102: Topics 103.2 / 103.5 / 103.6 / 109.1-109.4",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "12 Prüfungsfragen: Shell, Prozesse & Netzwerk.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht 'command 2>&1 | tee output.log'?",
                options  = [
                    "Leitet nur stderr in output.log",
                    "Leitet stdout und stderr in die Pipe, tee schreibt in Datei UND Terminal",
                    "Leitet nur stdout in output.log",
                    "Erstellt output.log nur wenn Fehler auftreten",
                ],
                correct  = 1,
                explanation = "2>&1 leitet stderr nach stdout. Die Pipe übergibt beides an tee. tee schreibt gleichzeitig in Datei und stdout (Terminal).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welches Signal wird mit 'kill -9 PID' gesendet?",
                options  = ["SIGTERM (15)", "SIGKILL (9)", "SIGHUP (1)", "SIGSTOP (19)"],
                correct  = 1,
                explanation = "SIGKILL (9) kann vom Prozess nicht abgefangen oder ignoriert werden — sofortiger Abbruch durch Kernel. SIGTERM (15) kann abgefangen werden.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was bedeutet ein nice-Wert von -10 im Vergleich zu 10?",
                options  = [
                    "-10 hat niedrigere Priorität (schlechter)",
                    "-10 hat höhere Priorität (besser) — niedrigerer nice = höhere CPU-Prio",
                    "Beide haben gleiche Priorität",
                    "-10 verhindert den Prozess vom Scheduling",
                ],
                correct  = 1,
                explanation = "Nice-Werte: -20 = höchste Priorität, +19 = niedrigste Priorität. Niedrigerer nice-Wert = mehr CPU. Nur root darf negative Werte setzen.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl sucht mit Regex nach Mustern in Dateien?",
                options  = ["find", "grep", "awk", "sed"],
                correct  = 1,
                explanation = "grep (global regular expression print) sucht in Dateien. grep -E = erweiterte Regex. grep -r = rekursiv. grep -v = invertiert.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was gibt 'awk -F: '{print $1}' /etc/passwd' aus?",
                options  = [
                    "Alle Passwörter",
                    "Alle Benutzernamen (erstes Feld, Trenner ':')",
                    "Alle UIDs",
                    "Alle Home-Verzeichnisse",
                ],
                correct  = 1,
                explanation = "-F: setzt Feldtrenner auf ':'. $1 = erstes Feld. In /etc/passwd ist das der Benutzername.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt die Routing-Tabelle an?",
                options  = ["ip addr show", "ip route show", "ip link show", "netstat -i"],
                correct  = 1,
                explanation = "ip route show (oder ip r) zeigt die Routing-Tabelle. route -n ist das ältere Äquivalent. ip addr = IP-Adressen, ip link = Interfaces.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher DNS-Record-Typ ordnet einen Hostnamen einer IPv4-Adresse zu?",
                options  = ["CNAME", "MX", "A", "PTR"],
                correct  = 2,
                explanation = "A-Record = Hostname → IPv4. AAAA = Hostname → IPv6. CNAME = Alias. MX = Mail-Server. PTR = Reverse-DNS (IP → Hostname).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt alle lauschenden TCP/UDP-Ports mit PID an?",
                options  = ["netstat -r", "ss -tulpn", "ip -p show", "lsof -r"],
                correct  = 1,
                explanation = "ss -tulpn: -t=TCP -u=UDP -l=listening -p=process -n=numeric. Modernes Äquivalent zu netstat -tulpn.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was macht 'ssh -L 8080:intern.server:80 user@bastion'?",
                options  = [
                    "Öffnet Port 8080 auf bastion und leitet zu intern.server:80",
                    "Local Port Forwarding: localhost:8080 → bastion → intern.server:80",
                    "Remote Port Forwarding: intern.server:80 → bastion:8080",
                    "Erstellt einen VPN-Tunnel über bastion",
                ],
                correct  = 1,
                explanation = "ssh -L = Local Forwarding: lokaler Port 8080 wird durch SSH-Tunnel zu intern.server:80 weitergeleitet. -R = Remote, -D = Dynamic (SOCKS).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welcher Datei werden SSH-Public-Keys für passwortlose Logins hinterlegt?",
                options  = [
                    "~/.ssh/id_rsa.pub",
                    "~/.ssh/authorized_keys",
                    "~/.ssh/known_hosts",
                    "/etc/ssh/authorized_keys",
                ],
                correct  = 1,
                explanation = "~/.ssh/authorized_keys enthält öffentliche Schlüssel von Benutzern die sich einloggen dürfen. known_hosts = vertraute Server-Keys.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher sed-Befehl ersetzt ALLE Vorkommen von 'foo' durch 'bar' in einer Datei?",
                options  = [
                    "sed 's/foo/bar/' datei",
                    "sed 's/foo/bar/g' datei",
                    "sed 's/foo/bar/i' datei",
                    "sed 'g/foo/bar/' datei",
                ],
                correct  = 1,
                explanation = "s/alt/neu/g — das 'g'-Flag (global) ersetzt alle Vorkommen. Ohne 'g' nur das erste pro Zeile. -i bearbeitet Datei direkt (in-place).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welche Datei enthält die systemweiten DNS-Server-Adressen?",
                options  = ["/etc/hosts", "/etc/hostname", "/etc/resolv.conf", "/etc/nsswitch.conf"],
                correct  = 2,
                explanation = "/etc/resolv.conf enthält 'nameserver IP'-Einträge. /etc/hosts = statische Host-Zuordnungen. /etc/nsswitch.conf = Reihenfolge der Name-Auflösung.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "103.x: 2>&1 | tee | SIGKILL=9 | nice -20=höchste Prio | grep -E | awk -F | ip route | ss -tulpn",
        memory_tip   = "Redirect-Reihenfolge: 2>&1 kommt nach > | tee = T-Stück in der Pipe",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.04 — Exam Block 4: User, Logs, Cron, Scripting (105.x/107.x/108.x)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.04",
        chapter      = 18,
        title        = "Exam Block 4 — User, Logs, Cron & Scripting (105.x/107.x/108.x)",
        mtype        = "QUIZ",
        xp           = 180,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 4. Benutzer, Gruppen, PAM.\n"
            " Logging, Zeitdienste, Cron.\n"
            " Bash-Scripting.\n"
            " 12 Fragen. Du bist fast durch.'"
        ),
        why_important = "LPIC-1 Exam 102: Topics 105.1 / 105.2 / 107.1 / 107.2 / 108.1 / 108.2",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "12 Prüfungsfragen: User, Logs, Cron & Scripting.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl erstellt einen neuen Benutzer mit Home-Verzeichnis?",
                options  = [
                    "adduser ghost",
                    "useradd ghost",
                    "useradd -m ghost",
                    "newuser -h ghost",
                ],
                correct  = 2,
                explanation = "useradd -m erstellt den User MIT Home-Verzeichnis. Ohne -m: kein Home. adduser (Debian) ist ein Frontend das -m automatisch macht.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welcher Datei werden verschlüsselte Passwörter gespeichert?",
                options  = ["/etc/passwd", "/etc/shadow", "/etc/gshadow", "/etc/security/passwd"],
                correct  = 1,
                explanation = "/etc/shadow enthält gehashte Passwörter (nur root lesbar). /etc/passwd enthält früher Passwörter (heute 'x' als Platzhalter).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was bedeutet ein 'crontab -e' Eintrag '*/15 * * * * /skript.sh'?",
                options  = [
                    "Jeden 15. des Monats",
                    "Alle 15 Stunden",
                    "Alle 15 Minuten, jede Stunde, jeden Tag",
                    "Um 15:00 Uhr jeden Tag",
                ],
                correct  = 2,
                explanation = "*/15 im Minuten-Feld = alle 15 Minuten. Crontab-Felder: Minute Stunde Tag Monat Wochentag Befehl.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher journalctl-Befehl zeigt nur Fehlermeldungen (err und kritischer)?",
                options  = [
                    "journalctl --errors",
                    "journalctl -p err",
                    "journalctl -l error",
                    "journalctl --level=3",
                ],
                correct  = 1,
                explanation = "journalctl -p PRIORITY filtert nach syslog-Priorität. -p err = err und höher (err, crit, alert, emerg). Zahlen: 0=emerg bis 7=debug.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was macht 'set -euo pipefail' am Anfang eines Bash-Skripts?",
                options  = [
                    "Aktiviert erweiterte Glob-Muster",
                    "Beendet bei Fehler, unbekannter Variable oder Pipe-Fehler",
                    "Setzt den Skript-Exit-Code auf 0",
                    "Aktiviert Debug-Modus",
                ],
                correct  = 1,
                explanation = "set -e = exit on error | set -u = unset variable = error | pipefail = Pipe-Fehler werden erkannt. Standard für robuste Skripte.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt Passwort-Ablaufinformationen eines Benutzers?",
                options  = [
                    "passwd -l ghost",
                    "chage -l ghost",
                    "usermod --expiry ghost",
                    "getent shadow ghost",
                ],
                correct  = 1,
                explanation = "chage -l USER zeigt alle Passwort-Ablauf-Informationen: Last change, Expiry, Inactive, etc. chage -M 90 setzt Max-Age auf 90 Tage.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen 'wall' und 'write'?",
                options  = [
                    "wall schreibt in Log, write schreibt an Terminal",
                    "wall = Nachricht an ALLE eingeloggten User | write = Nachricht an bestimmten User",
                    "wall = root-only, write = alle User",
                    "Kein Unterschied — Synonyme",
                ],
                correct  = 1,
                explanation = "wall (write all) sendet an alle eingeloggten Benutzer. write USER [TTY] sendet an einen bestimmten Benutzer.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welche Bash-Sondervaraible enthält den Exit-Code des letzten Befehls?",
                options  = ["$!", "$#", "$?", "$$"],
                correct  = 2,
                explanation = "$? = Exit-Code des letzten Befehls (0 = Erfolg, ≠0 = Fehler). $! = PID des letzten Hintergrundprozesses. $$ = PID der Shell. $# = Anzahl Parameter.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher NTP-Client ist Standard in modernen systemd-Systemen?",
                options  = ["ntpd", "chronyd", "systemd-timesyncd", "openntpd"],
                correct  = 2,
                explanation = "systemd-timesyncd ist der eingebaute, leichtgewichtige NTP-Client in systemd. Konfiguration: /etc/systemd/timesyncd.conf.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was gibt '${VAR:-default}' aus, wenn VAR nicht gesetzt ist?",
                options  = [
                    "Leeren String",
                    "'default'",
                    "Fehlermeldung und Skript-Abbruch",
                    "Den String '$VAR'",
                ],
                correct  = 1,
                explanation = "${VAR:-default} = 'default' wenn VAR leer oder nicht gesetzt. ${VAR:=default} setzt zusätzlich VAR auf 'default'. ${VAR:?msg} bricht ab.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welcher Datei werden systemweite cron-Jobs konfiguriert?",
                options  = ["/etc/crontab", "/var/spool/cron/root", "/etc/cron.d/system", "/usr/lib/cron/jobs"],
                correct  = 0,
                explanation = "/etc/crontab enthält systemweite Cron-Jobs mit einem User-Feld (6 Felder statt 5). /etc/cron.d/ = zusätzliche System-Cron-Dateien.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welche PAM-Konfigurationsdatei steuert sudo-Authentifizierung?",
                options  = [
                    "/etc/pam.d/login",
                    "/etc/pam.d/sudo",
                    "/etc/pam.d/common-auth",
                    "/etc/sudoers",
                ],
                correct  = 1,
                explanation = "/etc/pam.d/sudo konfiguriert PAM-Module für sudo. /etc/pam.d/common-auth = gemeinsame Auth-Regeln die andere includen.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "107.x: useradd -m | /etc/shadow | chage -l | 108.x: journalctl -p | crontab */15 | 105.x: $? | ${VAR:-default}",
        memory_tip   = "Crontab: Minute Stunde Tag Monat Wochentag — 'My System Time = Minute Stunde Tag Monat Tag'",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.05 — Exam Block 5: Sicherheit, Locale, Shell-Env (105.1/107.3/110.x)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.05",
        chapter      = 18,
        title        = "Exam Block 5 — Security, Locale & Shell-Env (105.1/107.3/110.x)",
        mtype        = "QUIZ",
        xp           = 180,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Letzter Block vor dem Finale.\n"
            " Sicherheit, Lokalisierung, Shell-Umgebung.\n"
            " 12 Fragen. Das ist der schwierigste Block.\n"
            " Konzentriere dich.'"
        ),
        why_important = "LPIC-1 Exam 102: Topics 105.1 / 107.3 / 110.1 / 110.2 / 110.3",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "12 Prüfungsfragen: Security, Locale & Shell-Env.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Startup-Datei lädt eine interaktive Login-Shell für den aktuellen User?",
                options  = [
                    "~/.bashrc",
                    "~/.bash_profile (oder ~/.profile wenn nicht vorhanden)",
                    "/etc/bash.bashrc",
                    "~/.bash_login (immer)",
                ],
                correct  = 1,
                explanation = "Login-Shell sucht: ~/.bash_profile → ~/.bash_login → ~/.profile (erste gefundene). Non-Login interaktiv liest ~/.bashrc.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was macht 'export' mit einer Variable?",
                options  = [
                    "Schreibt die Variable in /etc/environment",
                    "Macht die Variable für Kind-Prozesse sichtbar",
                    "Speichert die Variable dauerhaft über Sessions",
                    "Verhindert das Überschreiben der Variable",
                ],
                correct  = 1,
                explanation = "export markiert eine Variable als Umgebungsvariable — sie wird an alle Kind-Prozesse vererbt. Ohne export: nur in aktueller Shell sichtbar.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt an ob 'ls' ein Alias, Builtin oder Binary ist?",
                options  = ["which ls", "type ls", "whereis ls", "locate ls"],
                correct  = 1,
                explanation = "type ls gibt aus: 'ls is aliased to ...' oder 'ls is /bin/ls'. which findet nur Binaries im PATH. type -a ls zeigt alle Treffer.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher GPG-Befehl entschlüsselt eine verschlüsselte Datei?",
                options  = [
                    "gpg -e datei.gpg",
                    "gpg -d datei.gpg",
                    "gpg --decrypt-file datei.gpg",
                    "gpg --open datei.gpg",
                ],
                correct  = 1,
                explanation = "gpg -d (oder --decrypt) entschlüsselt. gpg -e (--encrypt) verschlüsselt. gpg --sign signiert. gpg --verify prüft Signatur.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was ist die korrekte sudoers-Syntax um 'ghost' sudo ohne Passwort zu erlauben?",
                options  = [
                    "ghost ALL=(ALL) ALL",
                    "ghost ALL=(ALL) NOPASSWD: ALL",
                    "ghost ALL=NOPASS ALL",
                    "NOPASSWD ghost=(ALL) ALL",
                ],
                correct  = 1,
                explanation = "Syntax: WHO HOST=(RUNAS) COMMANDS. NOPASSWD: vor den Commands deaktiviert Passwort-Abfrage. Immer via visudo editieren!",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl findet SUID-Dateien im gesamten Dateisystem?",
                options  = [
                    "find / -type f -perm suid",
                    "find / -perm -4000 -type f",
                    "locate -suid /",
                    "ls -R / | grep SUID",
                ],
                correct  = 1,
                explanation = "find / -perm -4000 = SUID-Bit (4000) ist gesetzt. -perm -2000 = SGID. -perm /6000 = SUID ODER SGID. 2>/dev/null unterdrückt Permission-Fehler.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welche Umgebungsvariable hat die höchste Priorität bei Locale-Einstellungen?",
                options  = ["LANG", "LANGUAGE", "LC_MESSAGES", "LC_ALL"],
                correct  = 3,
                explanation = "LC_ALL überschreibt alle anderen LC_*-Variablen und LANG. Priorität: LC_ALL > LC_* > LANG > LANGUAGE.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was macht 'ssh -X user@host firefox'?",
                options  = [
                    "Öffnet Firefox lokal und verbindet mit host",
                    "Startet Firefox auf host und zeigt Fenster lokal via X11-Forwarding",
                    "Öffnet einen X11-VPN-Tunnel zu host",
                    "Verbindet den lokalen X-Server mit host",
                ],
                correct  = 1,
                explanation = "ssh -X aktiviert X11-Forwarding: GUI-Anwendungen laufen auf host, aber Fenster werden lokal über DISPLAY angezeigt. -Y = Trusted (weniger sicher).",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welchem fail2ban-Konfigurationsfile sollten eigene Jail-Einstellungen stehen?",
                options  = [
                    "/etc/fail2ban/jail.conf",
                    "/etc/fail2ban/jail.local",
                    "/etc/fail2ban/jail.d/custom.conf",
                    "/etc/fail2ban/custom.conf",
                ],
                correct  = 1,
                explanation = "jail.local überschreibt jail.conf. Eigene Einstellungen immer in jail.local — so werden sie durch Updates nicht überschrieben.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher Befehl konvertiert eine Datei von Latin-1 nach UTF-8?",
                options  = [
                    "charset -f latin1 -t utf8 datei",
                    "iconv -f ISO-8859-1 -t UTF-8 datei",
                    "convert --encoding utf8 datei",
                    "recode latin1/utf8 datei",
                ],
                correct  = 1,
                explanation = "iconv -f FROM -t TO ist das Standard-Tool für Zeichensatzkonvertierung. ISO-8859-1 = Latin-1. iconv -l listet alle unterstützten Encodings.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welcher CUPS-Befehl entfernt einen Druckjob aus der Warteschlange?",
                options  = [
                    "lpq -r JOB-ID",
                    "lprm JOB-ID",
                    "lpcancel JOB-ID",
                    "cups --remove JOB-ID",
                ],
                correct  = 1,
                explanation = "lprm JOB-ID entfernt den Job. lprm - entfernt alle eigenen Jobs. cancel JOB-ID ist das CUPS-native Äquivalent. lpq zeigt die Warteschlange.",
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Was gibt 'HISTCONTROL=ignorespace' in der Shell-History-Konfiguration bewirkt?",
                options  = [
                    "Leerzeilen werden nicht gespeichert",
                    "Befehle die mit einem Leerzeichen beginnen werden nicht in die History aufgenommen",
                    "Leerzeichen in Befehlen werden ignoriert",
                    "Die History wird nach Leerzeilen getrennt",
                ],
                correct  = 1,
                explanation = "ignorespace: Befehl beginnt mit Leerzeichen → nicht in History. Nützlich für sensitive Befehle die man nicht protokollieren will.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "105.1: type | export | .bash_profile | 110.x: gpg -d | sudo NOPASSWD | find -perm -4000 | LC_ALL | iconv",
        memory_tip   = "Security-Trias: Authentication (SSH-Keys/PAM) + Authorization (sudo/RBAC) + Encryption (GPG/LUKS)",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.06 — Topic 101: System Architecture Deep Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.06",
        chapter      = 18,
        title        = "Exam Block 6 — Topic 101: System Architecture Deep Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "Domain 101 — System Architecture.\n"
            "Hardware, Boot, Init, Kernel.\n"
            "Das Fundament. Ohne dieses Wissen bricht alles.\n\n"
            "EXAMINATOR: 'Tiefenprüfung beginnt.'"
        ),
        why_important = "Domain 101 macht ~20% der LPIC-101-Prüfung aus. Hardware-IDs, Boot-Sequenz, SysVinit vs systemd und Kernel-Parameter sind garantierte Prüfungsthemen.",
        explanation   = (
            "Prüfungsblock 6 testet die gesamte Domain 101 in der Tiefe:\n"
            "• 101.1: BIOS/UEFI, POST, IRQ, DMA, /proc, /sys, /dev\n"
            "• 101.2: GRUB2, MBR, GPT, initramfs, efibootmgr\n"
            "• 101.3: SysVinit-Runlevels, systemd-Targets, Unit-Files\n"
            "Fokus: Prüfungsfallen, Distro-Unterschiede, exakte Syntax."
        ),
        quiz_questions = [
            QuizQuestion(
                question    = "Welcher Runlevel entspricht in systemd dem 'rescue.target'?",
                options     = ["A) Runlevel 0", "B) Runlevel 1", "C) Runlevel 3", "D) Runlevel 5"],
                correct     = "B",
                explanation = "Runlevel 1 (Single-User) = rescue.target in systemd. Runlevel 0 = poweroff.target, 6 = reboot.target.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welcher Befehl zeigt alle geladenen systemd-Units an?",
                options     = ["A) systemctl list-all", "B) systemctl status", "C) systemctl list-units", "D) systemctl show"],
                correct     = "C",
                explanation = "'systemctl list-units' zeigt alle aktiven Units. Mit '--all' auch inaktive.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Wo liegt die GRUB2-Konfigurationsdatei die NICHT manuell bearbeitet werden soll?",
                options     = ["A) /etc/default/grub", "B) /boot/grub/grub.cfg", "C) /etc/grub.d/", "D) /boot/grub2/custom.cfg"],
                correct     = "B",
                explanation = "/boot/grub/grub.cfg wird von update-grub generiert — niemals direkt bearbeiten. Änderungen gehören in /etc/default/grub.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist der Zweck von 'mkinitramfs'?",
                options     = ["A) GRUB installieren", "B) Kernel kompilieren", "C) Initiales RAM-Dateisystem erstellen", "D) Kernel-Module laden"],
                correct     = "C",
                explanation = "mkinitramfs erstellt das initramfs-Image — ein temporäres Root-Dateisystem das beim Boot vor dem echten Root-FS geladen wird.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welcher Befehl aktiviert eine Unit dauerhaft (Autostart bei Boot)?",
                options     = ["A) systemctl start nginx", "B) systemctl enable nginx", "C) systemctl activate nginx", "D) systemctl load nginx"],
                correct     = "B",
                explanation = "'enable' = Symlink in /etc/systemd/system/ anlegen → Autostart. 'start' = nur jetzt starten, kein Autostart.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "In welcher Datei stehen die IRQ-Zuordnungen zur Laufzeit?",
                options     = ["A) /sys/bus/irq", "B) /proc/interrupts", "C) /dev/irq", "D) /etc/irq.conf"],
                correct     = "B",
                explanation = "/proc/interrupts zeigt alle aktuellen IRQ-Zuordnungen zur Laufzeit. Klassische LPIC-Frage.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welcher SysVinit-Runlevel ist auf Debian-Systemen der Standard für Multi-User mit Netzwerk?",
                options     = ["A) Runlevel 3", "B) Runlevel 5", "C) Runlevel 2", "D) Runlevel 4"],
                correct     = "C",
                explanation = "Auf Debian ist Runlevel 2 der Standard (Multi-User + Netzwerk). Auf RHEL/CentOS ist es Runlevel 3 (ohne GUI) oder 5 (mit GUI).",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht 'systemctl isolate multi-user.target'?",
                options     = ["A) Startet alle Units", "B) Wechselt sofort zu multi-user.target", "C) Erstellt multi-user.target", "D) Listet Units des Targets"],
                correct     = "B",
                explanation = "'isolate' wechselt sofort zum angegebenen Target — stoppt alle inkompatiblen Units. Äquivalent zu telinit in SysVinit.",
                xp_value    = 20,
            ),
        ],
        exam_tip     = "101-Prüfungsfallen: Runlevel 2 Debian vs RHEL | grub.cfg vs /etc/default/grub | rescue.target vs emergency.target | systemctl enable vs start",
        memory_tip   = "Domain 101 = Hardware sehen (lspci/lsusb) + Boot steuern (GRUB2) + Init verstehen (SysVinit/systemd)",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.07 — Topic 102: Installation & Package Management Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.07",
        chapter      = 18,
        title        = "Exam Block 7 — Topic 102: Installation & Package Management",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 7. Topic 102 — Installation und Paketverwaltung.\n"
            " dpkg, apt, rpm, yum/dnf, zypper, Shared Libraries.\n"
            " 10 Fragen. Zeig was du weißt.'"
        ),
        why_important = "LPIC-1 Exam 101: Topic 102 — Linux Installation & Package Management",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: Installation & Package Management.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher apt-Befehl entfernt ein Paket UND seine Konfigurationsdateien?",
                options  = ["apt remove paket", "apt purge paket", "apt clean paket", "apt delete paket"],
                correct  = 1,
                explanation = "apt purge entfernt Paket + Konfigurationsdateien. apt remove lässt Konfigdateien zurück. apt autoremove entfernt verwaiste Abhängigkeiten.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher dpkg-Befehl zeigt zu welchem Paket /bin/bash gehört?",
                options  = ["dpkg -L bash", "dpkg -S /bin/bash", "dpkg -l bash", "dpkg -i /bin/bash"],
                correct  = 1,
                explanation = "dpkg -S DATEI = Search (welches Paket enthält diese Datei). dpkg -L PAKET = List (welche Dateien hat das Paket).",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "In welcher Datei wird das APT-Repository auf Debian-Systemen konfiguriert?",
                options  = ["/etc/apt/apt.conf", "/etc/apt/sources.list", "/etc/apt/repos.d/", "/var/cache/apt/archives/"],
                correct  = 1,
                explanation = "/etc/apt/sources.list enthält Repository-URLs. /etc/apt/sources.list.d/ für zusätzliche Sources. /var/cache/apt/archives/ = heruntergeladene .deb-Dateien.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'rpm -ivh paket.rpm'?",
                options  = [
                    "Nur Informationen über das Paket anzeigen",
                    "Paket installieren mit verbose-Ausgabe und Hash-Fortschrittsbalken",
                    "Paket verifizieren und Hashsumme prüfen",
                    "Paket installieren und alle Abhängigkeiten ignorieren",
                ],
                correct  = 1,
                explanation = "rpm -ivh: -i=install, -v=verbose, -h=hash (Fortschrittsbalken aus #-Zeichen). rpm -Uvh = upgrade/install.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl findet heraus welches RPM-Paket /usr/bin/perl enthält?",
                options  = ["rpm -ql perl", "rpm -qf /usr/bin/perl", "rpm -qi perl", "yum provides perl"],
                correct  = 1,
                explanation = "rpm -qf DATEI (query file) gibt an, welches Paket diese Datei bereitstellt. yum provides macht das gleiche für noch nicht installierte Pakete.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was bewirkt 'ldconfig' nach der Installation einer neuen Shared Library?",
                options  = [
                    "Lädt alle Kernel-Module neu",
                    "Aktualisiert den dynamischen Linker-Cache /etc/ld.so.cache",
                    "Installiert fehlende Bibliotheken nach",
                    "Verlinkt alle .so-Dateien im System neu",
                ],
                correct  = 1,
                explanation = "ldconfig scannt /lib, /usr/lib und Verzeichnisse aus /etc/ld.so.conf und erstellt /etc/ld.so.cache für schnelle Bibliotheksfindung.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche Umgebungsvariable setzt temporäre zusätzliche Bibliothekspfade?",
                options  = ["LIBRARY_PATH", "LD_LIBRARY_PATH", "LD_PRELOAD", "LIB_PATH"],
                correct  = 1,
                explanation = "LD_LIBRARY_PATH = zusätzliche Suchpfade für den dynamischen Linker. LD_PRELOAD = zwingt bestimmte Library zu laden. Beides für Debugging/Tests.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt alle Abhängigkeiten einer ausführbaren Datei an?",
                options  = ["ldconfig -l", "ldd /pfad/zur/datei", "lib --deps /datei", "ld -v /datei"],
                correct  = 1,
                explanation = "ldd (List Dynamic Dependencies) zeigt alle benötigten Shared Libraries einer Binary. Nützlich für Troubleshooting fehlender Libraries.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen 'yum install' und 'dnf install'?",
                options  = [
                    "yum ist für RHEL, dnf für CentOS",
                    "dnf ist der modernere Nachfolger von yum mit besserer Abhängigkeitslösung",
                    "yum installiert Binaries, dnf installiert Quellcode",
                    "dnf benötigt root, yum nicht",
                ],
                correct  = 1,
                explanation = "dnf (Dandified Yum) ist der offizielle Nachfolger von yum ab Fedora 22/RHEL 8. Gleiche Syntax, aber schneller und robuster bei Abhängigkeitslösung.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher zypper-Befehl sucht nach einem Paket auf SUSE-Systemen?",
                options  = ["zypper find paket", "zypper se paket", "zypper search --exact paket", "zypper query paket"],
                correct  = 1,
                explanation = "zypper se (search) sucht Pakete. zypper in = install, zypper rm = remove, zypper up = update. zypper lr = list repos.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "102: dpkg -S=Datei suchen | -L=Dateien des Pakets | apt purge=mit Config | rpm -ivh | ldd=Library-Deps | ldconfig=Cache",
        memory_tip   = "dpkg -S = Suche (welches Paket) | dpkg -L = Liste (Dateien des Pakets)",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.08 — Topic 103: GNU/Unix Command Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.08",
        chapter      = 18,
        title        = "Exam Block 8 — Topic 103: GNU/Unix Command Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 8. Topic 103 — GNU und Unix-Befehle.\n"
            " Textfilter, Streams, Prozesse, Signale, Prioritäten.\n"
            " 10 Fragen. Kein Netz. Kein Hint.'"
        ),
        why_important = "LPIC-1 Exam 101: Topic 103 — GNU and Unix Commands",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: GNU/Unix-Befehle tief.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Was gibt 'sort -t: -k3 -n /etc/passwd' aus?",
                options  = [
                    "passwd alphabetisch nach Benutzername sortiert",
                    "passwd numerisch nach UID (3. Feld, Doppelpunkt-Trenner) sortiert",
                    "passwd nach Heimatverzeichnis sortiert",
                    "passwd in umgekehrter Reihenfolge",
                ],
                correct  = 1,
                explanation = "-t: setzt Feldtrenner auf ':', -k3 sortiert nach Feld 3 (UID), -n numerisch. Ohne -n wäre '10' vor '9' (alphabetisch).",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zählt Zeilen, Wörter und Zeichen einer Datei?",
                options  = ["count datei", "wc datei", "stat datei", "len datei"],
                correct  = 1,
                explanation = "wc (word count): wc -l = Zeilen, wc -w = Wörter, wc -c = Bytes, wc -m = Zeichen. wc allein = alle drei.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'uniq -c' in einer Pipeline?",
                options  = [
                    "Entfernt alle Duplikate aus einer Datei",
                    "Gibt jede einzigartige Zeile mit Anzahl der Vorkommen aus",
                    "Zählt die Gesamtanzahl einzigartiger Zeilen",
                    "Sortiert und entfernt Duplikate gleichzeitig",
                ],
                correct  = 1,
                explanation = "uniq -c präfixiert jede Zeile mit der Anzahl aufeinanderfolgender Duplikate. Typisch: sort datei | uniq -c | sort -rn (häufigste zuerst).",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Wie wird ein Prozess in den Vordergrund gebracht (nach Ctrl+Z)?",
                options  = ["jobs", "fg %1", "bg %1", "resume %1"],
                correct  = 1,
                explanation = "fg %1 bringt Job Nr. 1 in den Vordergrund. bg %1 schickt ihn in den Hintergrund (weiter laufend). jobs listet alle Hintergrund-Jobs.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'nohup ./script.sh &'?",
                options  = [
                    "Startet script.sh mit höchster Priorität",
                    "Startet script.sh im Hintergrund, immun gegen SIGHUP (Terminal-Schließen)",
                    "Verhindert dass script.sh beendet werden kann",
                    "Startet script.sh neu wenn es abstürzt",
                ],
                correct  = 1,
                explanation = "nohup ignoriert SIGHUP (wird gesendet wenn Terminal geschlossen wird). & = Hintergrund. Ausgabe geht nach nohup.out. Nützlich für lange Jobs über SSH.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt die ersten 5 Zeilen einer Datei?",
                options  = ["head -5 datei", "head -n 5 datei", "tail -r -5 datei", "A und B"],
                correct  = 3,
                explanation = "head -5 und head -n 5 sind äquivalent. head ohne Parameter zeigt die ersten 10 Zeilen. tail -n 5 zeigt die LETZTEN 5 Zeilen.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'cut -d: -f1,6 /etc/passwd'?",
                options  = [
                    "Schneidet Zeilen 1 und 6 aus der Datei",
                    "Gibt Feld 1 und 6 (Trenner ':') aus — Benutzername und Heimatverzeichnis",
                    "Entfernt Felder 1 bis 6",
                    "Zeigt nur die ersten 6 Zeichen jeder Zeile",
                ],
                correct  = 1,
                explanation = "cut -d: setzt Delimitter, -f1,6 wählt Felder 1 und 6. In /etc/passwd: Feld1=Username, Feld6=Heimatverzeichnis.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welches Signal kann ein Prozess NICHT abfangen oder ignorieren?",
                options  = ["SIGTERM (15)", "SIGHUP (1)", "SIGKILL (9)", "SIGINT (2)"],
                correct  = 2,
                explanation = "SIGKILL (9) wird direkt vom Kernel ausgeführt — der Prozess hat keine Chance zu reagieren. Alle anderen Signale können mit signal() abgefangen werden.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Wie kann der Nice-Wert eines bereits laufenden Prozesses (PID 1234) auf 5 gesetzt werden?",
                options  = [
                    "nice -n 5 1234",
                    "renice -n 5 -p 1234",
                    "renice 5 1234",
                    "B und C",
                ],
                correct  = 3,
                explanation = "renice ändert den Nice-Wert eines laufenden Prozesses. Syntax: renice -n WERT -p PID oder renice WERT PID (beide gültig). nice startet einen neuen Prozess mit Nice-Wert.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen '>' und '>>'?",
                options  = [
                    "> erstellt Datei, >> überschreibt",
                    "> überschreibt/erstellt Datei, >> hängt an",
                    "> leitet stdout um, >> leitet stderr um",
                    "Kein Unterschied — beide sind äquivalent",
                ],
                correct  = 1,
                explanation = "> (redirect) erstellt/überschreibt. >> (append redirect) hängt an bestehende Datei. noclobber-Option verhindert versehentliches Überschreiben mit >.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "103: sort -t -k -n | wc -l/-w/-c | uniq -c | fg/bg/jobs | nohup | cut -d -f | SIGKILL=9 kein Abfangen | renice -p",
        memory_tip   = "Signale: SIGHUP=1 SIGINT=2 SIGQUIT=3 SIGKILL=9 SIGTERM=15 SIGSTOP=19",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.09 — Topic 104: Filesystem Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.09",
        chapter      = 18,
        title        = "Exam Block 9 — Topic 104: Filesystem Deep Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 9. Topic 104 — Dateisysteme tief.\n"
            " Partitionierung, ext4, XFS, LVM, fstab, Links.\n"
            " 10 Fragen. Konzentrier dich.'"
        ),
        why_important = "LPIC-1 Exam 101: Topic 104 — Devices, Linux Filesystems, FHS",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: Filesystem & Partitionierung tief.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der maximale Unterschied zwischen MBR und GPT bezüglich Partitionsanzahl?",
                options  = [
                    "MBR: 4 primäre, GPT: 128 Partitionen",
                    "MBR: 8 primäre, GPT: 64 Partitionen",
                    "MBR: 4 primäre, GPT: 256 Partitionen",
                    "MBR: 16 primäre, GPT: 128 Partitionen",
                ],
                correct  = 0,
                explanation = "MBR: max. 4 primäre Partitionen (oder 3 primäre + 1 erweiterte mit beliebig vielen logischen). GPT: bis zu 128 Partitionen ohne Workaround. GPT auch für Disks > 2TB.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt den Typ und die UUID aller Block-Geräte an?",
                options  = ["lsblk", "blkid", "fdisk -l", "parted -l"],
                correct  = 1,
                explanation = "blkid zeigt UUID, TYPE (Dateisystemtyp), LABEL aller Block-Geräte. lsblk zeigt Hierarchie ohne Dateisysteminfo. fdisk/-parted für Partitionierungsdetails.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist das dritte Feld in /etc/fstab?",
                options  = ["Mount-Optionen", "Dateisystem-Typ", "Dump-Flag", "fsck-Reihenfolge"],
                correct  = 1,
                explanation = "/etc/fstab 6 Felder: 1=Device/UUID, 2=Mountpoint, 3=Typ (ext4/xfs/vfat), 4=Optionen, 5=dump, 6=fsck-Pass.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was bedeutet 'pass 2' im sechsten Feld von /etc/fstab?",
                options  = [
                    "Zweifach mounten für Redundanz",
                    "fsck prüft diese Partition nach dem Root-Dateisystem (pass 1)",
                    "Zweites Backup wird erstellt",
                    "Die Partition wird bei jedem zweiten Boot geprüft",
                ],
                correct  = 1,
                explanation = "Pass 0=nicht prüfen, Pass 1=zuerst prüfen (Root /), Pass 2=danach prüfen (andere Partitionen). fsck prüft Pass 2 Partitionen parallel.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher LVM-Befehl vergrößert ein Logical Volume um 10GB?",
                options  = [
                    "lvcreate -L +10G /dev/vg0/lv_data",
                    "lvextend -L +10G /dev/vg0/lv_data",
                    "vgextend -L +10G /dev/vg0/lv_data",
                    "lvresize +10G lv_data",
                ],
                correct  = 1,
                explanation = "lvextend -L +10G erweitert das LV. Danach: resize2fs (ext4) oder xfs_growfs (XFS) für das Dateisystem. lvextend -r erledigt beides auf einmal.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl prüft ein XFS-Dateisystem auf Fehler?",
                options  = ["fsck.xfs", "xfs_check", "xfs_repair -n /dev/sdb1", "e2fsck /dev/sdb1"],
                correct  = 2,
                explanation = "xfs_repair -n = dry-run (nur prüfen, nicht reparieren). xfs_repair ohne -n repariert. fsck.xfs existiert nicht als echtes Tool. e2fsck ist nur für ext2/3/4.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen einem Soft Link und einem Hard Link?",
                options  = [
                    "Soft Links können auf Verzeichnisse zeigen und filesystem-übergreifend sein; Hard Links nicht",
                    "Hard Links sind schneller; Soft Links sind portabler",
                    "Soft Links teilen Inode-Nummern; Hard Links nicht",
                    "Hard Links können gelöscht werden ohne Daten zu verlieren; Soft Links nicht",
                ],
                correct  = 0,
                explanation = "Soft Links (Symlinks) zeigen auf Pfad — können auf Verzeichnisse und cross-filesystem zeigen. Hard Links teilen Inode — nur innerhalb eines Filesystems, nicht für Verzeichnisse.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welches FHS-Verzeichnis enthält temporäre Dateien die einen Reboot überleben?",
                options  = ["/tmp", "/var/tmp", "/run", "/proc"],
                correct  = 1,
                explanation = "/var/tmp = persistent temp (überlebt Reboot). /tmp = flüchtig (oft RAM oder wird bei Boot geleert). /run = Runtime-Daten (RAM, nicht persistent).",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt die Inode-Auslastung eines Dateisystems an?",
                options  = ["df -h", "df -i", "du -i", "stat --inodes"],
                correct  = 1,
                explanation = "df -i zeigt Inode-Auslastung (gesamt, verwendet, frei, Prozent). Wichtig: Ein volles Dateisystem per Inodes (100% Inodes) kann keine neuen Dateien anlegen auch wenn Platz frei ist.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'tune2fs -l /dev/sda1'?",
                options  = [
                    "Vergrößert das ext2/3/4-Dateisystem",
                    "Zeigt Superblock-Informationen des ext2/3/4-Dateisystems",
                    "Repariert fehlerhafte Inodes",
                    "Setzt das Dateisystem-Label",
                ],
                correct  = 1,
                explanation = "tune2fs -l (list) zeigt alle Superblock-Parameter: UUID, Features, Mount-Count, Last Check, Block-Größe. tune2fs -L LABEL setzt das Label.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "104: MBR=4primär GPT=128 | blkid=UUID+Typ | fstab 6 Felder | pass 1=/ zuerst | lvextend +10G | /var/tmp=persistent | df -i=Inodes",
        memory_tip   = "fstab: Gerät Mountpoint Typ Optionen Dump Pass — 'G M T O D P'",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.10 — Topic 105: Shell & Scripting Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.10",
        chapter      = 18,
        title        = "Exam Block 10 — Topic 105: Shell & Scripting Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 10. Topic 105 — Shell-Scripting.\n"
            " Variablen, Konditionen, Schleifen, Funktionen, Expansionen.\n"
            " 10 Fragen. Kein Debugger. Nur dein Kopf.'"
        ),
        why_important = "LPIC-1 Exam 102: Topic 105 — Shells and Shell Scripting",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: Shell & Scripting tief.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Was gibt '${#VAR}' aus wenn VAR='NeonGrid'?",
                options  = ["NeonGrid", "8", "9", "Die Anzahl der Wörter in VAR"],
                correct  = 1,
                explanation = "${#VAR} = Länge des String-Werts von VAR. 'NeonGrid' hat 8 Zeichen. ${#@} = Anzahl der Positionsparameter.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welches Konstrukt iteriert über alle Positionsparameter eines Skripts?",
                options  = [
                    "for i in $*; do ... done",
                    "for i in \"$@\"; do ... done",
                    "while [ $# -gt 0 ]; do ... shift; done",
                    "B und C",
                ],
                correct  = 3,
                explanation = "\"$@\" = alle Parameter als separate Strings (sicher mit Leerzeichen). $* als ein String. while+shift ist auch korrekt. Beide B und C sind gültige Ansätze.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist der Exit-Code von 'test -d /etc'?",
                options  = ["1 (falsch, /etc ist kein reguläres File)", "0 (wahr, /etc ist ein Verzeichnis)", "2 (Fehler)", "unbekannt"],
                correct  = 1,
                explanation = "test -d PFAD gibt 0 (true/Erfolg) zurück wenn PFAD ein Verzeichnis ist. In Bash: 0 = wahr/Erfolg, alles andere = falsch/Fehler.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht '[ -z \"$VAR\" ]' in einer if-Bedingung?",
                options  = [
                    "Prüft ob VAR mit 'z' beginnt",
                    "Prüft ob VAR leer (zero-length) ist",
                    "Prüft ob VAR eine Zahl (zero oder mehr) enthält",
                    "Prüft ob die Datei $VAR existiert",
                ],
                correct  = 1,
                explanation = "-z STRING = true wenn STRING leer (Länge 0). -n STRING = true wenn STRING nicht leer. -z und -n sind String-Tests, -e/-f/-d sind Datei-Tests.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche Bash-Expansion gibt den letzten Teil eines Pfades zurück?",
                options  = [
                    "${PFAD##*/}",
                    "${PFAD%/*}",
                    "${PFAD#/}",
                    "$(basename $PFAD)",
                ],
                correct  = 0,
                explanation = "${VAR##MUSTER} entfernt den längsten Prefix. ${PFAD##*/} entfernt alles bis zum letzten '/'. Ergebnis = Dateiname. $(basename $PFAD) macht dasselbe als Befehl.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen 'local' und regulären Variablen in Bash-Funktionen?",
                options  = [
                    "local-Variablen sind schneller",
                    "local-Variablen sind nur innerhalb der Funktion sichtbar (Scope-Begrenzung)",
                    "local-Variablen werden nicht exportiert",
                    "Es gibt keinen Unterschied in Bash",
                ],
                correct  = 1,
                explanation = "local begrenzt die Variable auf den Geltungsbereich der Funktion. Ohne local sind Variablen global sichtbar. Best Practice: immer local in Funktionen verwenden.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was gibt 'echo $((2**10))' aus?",
                options  = ["20", "210", "1024", "Syntaxfehler"],
                correct  = 2,
                explanation = "$((Ausdruck)) = Arithmetic Expansion. 2**10 = 2 hoch 10 = 1024. Arithmetik in Bash: + - * / % ** (Potenz). Integers only.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche Option aktiviert den Debug-Modus für ein Bash-Skript?",
                options  = ["bash --debug skript.sh", "bash -x skript.sh", "bash -v skript.sh", "bash -d skript.sh"],
                correct  = 1,
                explanation = "bash -x = execution trace (zeigt jeden Befehl mit + vor Ausführung). bash -v = verbose (zeigt jede Zeile bevor sie ausgeführt wird). Oft kombiniert: bash -xv.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Wie wird eine case-Anweisung in Bash korrekt beendet?",
                options  = ["end case", "esac", "done", "fi"],
                correct  = 1,
                explanation = "case...esac (case rückwärts). if...fi (if rückwärts). for/while/until...done. Diese Mnemonic hilft: Schlüsselwort rückwärts = Ende.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'read -r line' beim Einlesen einer Zeile?",
                options  = [
                    "Liest nur eine Zeile ohne Zeilenumbruch",
                    "Verhindert die Interpretation von Backslash als Escape-Zeichen",
                    "Liest die Zeile rekursiv",
                    "Gibt die Zeile in umgekehrter Reihenfolge aus",
                ],
                correct  = 1,
                explanation = "read -r (raw mode) behandelt Backslash als normales Zeichen — kein Escape-Handling. Empfohlen für robustes Einlesen von Dateipfaden und beliebigen Strings.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "105: ${#VAR}=Länge | \"$@\"=alle Params sicher | test -z=leer -n=nichtleer | ${VAR##*/}=basename | local=Scope | $((2**10)) | bash -x=Debug | esac",
        memory_tip   = "Bash-Blöcke: if→fi | case→esac | for/while/until→done | function→}",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.11 — Topic 107: Admin Tasks Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.11",
        chapter      = 18,
        title        = "Exam Block 11 — Topic 107: Admin Tasks Deep Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 11. Topic 107 — Administrative Aufgaben.\n"
            " Benutzer, Gruppen, Cron, Locale, Zeitdienste, Drucker.\n"
            " 10 Fragen. Administrator-Level.'"
        ),
        why_important = "LPIC-1 Exam 102: Topic 107 — Administrative Tasks",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: Administrative Tasks tief.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl sperrt das Passwort eines Benutzers (aber lässt SSH-Keys zu)?",
                options  = [
                    "passwd -l ghost",
                    "usermod -L ghost",
                    "usermod -s /sbin/nologin ghost",
                    "A und B",
                ],
                correct  = 3,
                explanation = "passwd -l und usermod -L sperren das Passwort (! vor dem Hash in /etc/shadow). SSH mit Key funktioniert weiterhin. usermod -s /sbin/nologin verhindert auch Key-Login-Shell.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl fügt den User 'ghost' zur Gruppe 'docker' hinzu OHNE andere Gruppen zu entfernen?",
                options  = [
                    "usermod -G docker ghost",
                    "usermod -aG docker ghost",
                    "groupadd ghost docker",
                    "addgroup ghost docker",
                ],
                correct  = 1,
                explanation = "usermod -aG: -a=append (wichtig!), -G=supplementary groups. Ohne -a würde -G alle anderen Gruppen entfernen! Teure Prüfungsfalle.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was steht im 7. Feld von /etc/passwd?",
                options  = ["Passwort-Hash", "Heimatverzeichnis", "Login-Shell", "Kommentar/GECOS"],
                correct  = 2,
                explanation = "/etc/passwd 7 Felder: 1=Name 2=Passwort(x) 3=UID 4=GID 5=GECOS 6=Home 7=Shell. Shell /sbin/nologin oder /bin/false = kein Login.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher chage-Befehl setzt das maximale Passwort-Alter auf 90 Tage?",
                options  = ["chage -M 90 ghost", "chage -m 90 ghost", "chage -W 90 ghost", "chage -E 90 ghost"],
                correct  = 0,
                explanation = "chage -M = Maximum age (max. Tage bis Passwortänderung). -m = minimum age. -W = warning days. -E = expiry date (Ablaufdatum des Kontos).",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "In welchem Verzeichnis liegen User-spezifische Crontab-Dateien?",
                options  = ["/etc/cron.d/", "/var/spool/cron/crontabs/", "/home/user/.crontab", "/usr/lib/cron/"],
                correct  = 1,
                explanation = "/var/spool/cron/crontabs/ (Debian) oder /var/spool/cron/ (RHEL) enthält User-Crontab-Dateien. Nie direkt editieren — nur über crontab -e!",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'localectl set-locale LANG=de_DE.UTF-8'?",
                options  = [
                    "Ändert nur die aktuelle Session-Sprache",
                    "Setzt die systemweite Locale dauerhaft (persistiert in /etc/locale.conf)",
                    "Installiert das deutsche Sprachpaket",
                    "Erzeugt die Locale-Daten für de_DE",
                ],
                correct  = 1,
                explanation = "localectl set-locale schreibt dauerhaft in /etc/locale.conf (systemd-Systeme) oder /etc/default/locale (Debian). locale-gen generiert Locale-Daten.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt alle verfügbaren Zeitzonen an?",
                options  = [
                    "tzselect --list",
                    "timedatectl list-timezones",
                    "ls /usr/share/zoneinfo/",
                    "B und C",
                ],
                correct  = 3,
                explanation = "timedatectl list-timezones = vollständige Liste. ls /usr/share/zoneinfo/ = Verzeichnisinhalt mit regionalen Unterordnern. Beide zeigen verfügbare Zeitzonen.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche Datei enthält die Passwort-Alterungsregeln für alle neuen Benutzer?",
                options  = ["/etc/login.defs", "/etc/pam.d/passwd", "/etc/security/pwquality.conf", "/etc/shadow"],
                correct  = 0,
                explanation = "/etc/login.defs enthält Standardwerte für PASS_MAX_DAYS, PASS_MIN_DAYS, PASS_WARN_AGE, UID_MIN, UID_MAX. Gilt für neu erstellte Benutzer.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'getent passwd ghost' statt direkt /etc/passwd zu lesen?",
                options  = [
                    "Ist langsamer aber sicherer",
                    "Berücksichtigt auch LDAP/NIS-Benutzer über NSS",
                    "Zeigt nur lokale Benutzer",
                    "Gibt das verschlüsselte Passwort aus",
                ],
                correct  = 1,
                explanation = "getent verwendet NSS (Name Service Switch aus /etc/nsswitch.conf) — liefert damit auch LDAP, NIS, SSSD-Benutzer. getent passwd = alle Benutzer aus allen Quellen.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl aktualisiert die Drucker-Warteschlange bei CUPS?",
                options  = ["lpr -u", "cupsenable druckername", "lpstat -r", "cupsaccept druckername"],
                correct  = 3,
                explanation = "cupsaccept = Warteschlange akzeptiert neue Jobs. cupsreject = lehnt neue Jobs ab. cupsenable/cupsdisable = Drucker aktivieren/deaktivieren (Druckvorgang). Beide nötig für vollständigen Betrieb.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "107: usermod -aG (append!!) | chage -M=Max | /var/spool/cron | localectl | /etc/login.defs | getent=NSS | cupsaccept vs cupsenable",
        memory_tip   = "usermod -aG: das -a ist PFLICHT — ohne -a werden ALLE anderen Gruppen gelöscht!",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.12 — Topic 108: System Services Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.12",
        chapter      = 18,
        title        = "Exam Block 12 — Topic 108: System Services Deep Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 12. Topic 108 — Systemdienste.\n"
            " Boot, systemd, Logging, Zeitdienste, Drucker, MTA.\n"
            " 10 Fragen. System-Administration auf Expert-Level.'"
        ),
        why_important = "LPIC-1 Exam 102: Topic 108 — Essential System Services",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: System Services tief.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher systemctl-Befehl verhindert dauerhaft den Start eines Dienstes (auch durch andere Units)?",
                options  = ["systemctl disable dienst", "systemctl stop dienst", "systemctl mask dienst", "systemctl deactivate dienst"],
                correct  = 2,
                explanation = "systemctl mask erstellt einen Symlink nach /dev/null — der Dienst kann nicht gestartet werden, auch nicht als Abhängigkeit. unmask macht es rückgängig.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was zeigt 'systemd-analyze blame'?",
                options  = [
                    "Fehler im Journal seit dem letzten Boot",
                    "Alle Units sortiert nach ihrer Boot-Zeit (längste zuerst)",
                    "Welche Unit zuletzt einen Fehler hatte",
                    "CPU-Verbrauch aller Services",
                ],
                correct  = 1,
                explanation = "systemd-analyze blame zeigt alle Units sortiert nach Startzeit (längste zuerst) — gut für Boot-Optimierung. systemd-analyze time = Gesamtboot-Zeit.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche rsyslog-Konfigurationssyntax leitet ALLE Mail-Logs an eine Remote-Adresse via TCP?",
                options  = [
                    "mail.* @192.168.1.100",
                    "mail.* @@192.168.1.100",
                    "mail.* tcp://192.168.1.100",
                    "mail.* >192.168.1.100",
                ],
                correct  = 1,
                explanation = "@ = UDP (einzelnes @), @@ = TCP (doppeltes @@). mail.* = alle Mail-Severity-Level. Syntax: facility.severity Ziel.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Wie kann die Systemzeit von der Hardware-Uhr gelesen werden?",
                options  = ["hwclock -r", "hwclock --show", "hwclock -s", "A und B"],
                correct  = 3,
                explanation = "hwclock -r und --show zeigen die Hardware-Uhr. hwclock -s = System-Zeit von Hardware setzen. hwclock -w = Hardware von System setzen.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist der Standard-MTA auf modernen Debian/Ubuntu-Systemen?",
                options  = ["Sendmail", "Exim4", "Postfix", "Nullmailer"],
                correct  = 2,
                explanation = "Postfix ist der Standard-MTA auf modernen Debian/Ubuntu-Systemen. Exim4 war früher Standard. Sendmail ist veraltet. Nullmailer kann nur senden.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl aktiviert NTP-Synchronisation dauerhaft auf systemd-Systemen?",
                options  = [
                    "systemctl enable ntp",
                    "timedatectl set-ntp true",
                    "ntpd --enable",
                    "systemctl start systemd-timesyncd",
                ],
                correct  = 1,
                explanation = "timedatectl set-ntp true aktiviert NTP-Synchronisation dauerhaft. Dies konfiguriert systemd-timesyncd. systemctl enable/start systemd-timesyncd macht dasselbe manuell.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "In welcher Datei werden systemd-Dienst-Override-Optionen (Drop-Ins) gespeichert?",
                options  = [
                    "/etc/systemd/system/dienst.service",
                    "/etc/systemd/system/dienst.service.d/override.conf",
                    "/usr/lib/systemd/system/dienst.service",
                    "/run/systemd/override/dienst.conf",
                ],
                correct  = 1,
                explanation = "Drop-In-Dateien liegen in /etc/systemd/system/UNIT.d/*.conf. systemctl edit dienst.service erstellt automatisch /etc/systemd/system/dienst.service.d/override.conf.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl leert den Journal-Cache und behält nur die neuesten 2 Wochen?",
                options  = [
                    "journalctl --clean --time=2weeks",
                    "journalctl --vacuum-time=2weeks",
                    "journalctl --expire=2w",
                    "systemd-journald --vacuum 2weeks",
                ],
                correct  = 1,
                explanation = "journalctl --vacuum-time=Xd/weeks/months löscht Journal-Einträge älter als X. --vacuum-size=X reduziert auf Dateigröße. --vacuum-files=N behält N Dateien.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche Datei enthält die Mail-Weiterleitungsregeln für den Root-User?",
                options  = ["/etc/mail/aliases", "/etc/aliases", "~root/.forward", "A und B"],
                correct  = 3,
                explanation = "/etc/aliases (Systemweite Aliases) und ~/.forward (User-spezifisch) können beide Root-Mails weiterleiten. /etc/aliases benötigt 'newaliases' nach Änderung.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht 'mailq' ohne Argumente?",
                options  = [
                    "Leert die E-Mail-Warteschlange",
                    "Zeigt alle E-Mails in der Postfix-Warteschlange",
                    "Startet den Mail-Queue-Daemon",
                    "Gibt Statistiken über gesendete Mails aus",
                ],
                correct  = 1,
                explanation = "mailq zeigt alle E-Mails die auf Zustellung warten (Mail Transfer Queue). Äquivalent zu sendmail -bp oder postqueue -p bei Postfix.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "108: mask=permanent sperren | systemd-analyze blame | @@=TCP @=UDP | hwclock -s=von HW | timedatectl set-ntp | Drop-Ins=.service.d/ | mailq=Queue",
        memory_tip   = "systemctl mask = /dev/null Symlink = unüberwindbares Verbot | disable = nur autostart weg",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.13 — Topic 109: Networking Deep Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.13",
        chapter      = 18,
        title        = "Exam Block 13 — Topic 109: Networking Deep Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 13. Topic 109 — Netzwerke tief.\n"
            " IP, Routing, DNS, SSH, Firewall — alles.\n"
            " 10 Fragen. Das Netz kennt keine Gnade.'"
        ),
        why_important = "LPIC-1 Exam 102: Topic 109 — Networking Fundamentals",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: Networking tief.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Wie viele nutzbare Host-Adressen hat ein /26-Netzwerk?",
                options  = ["62", "64", "126", "30"],
                correct  = 0,
                explanation = "/26 = 26 Netzwerkbits, 6 Hostbits. 2^6=64 Adressen, -2 (Netz+Broadcast) = 62 nutzbare Hosts.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl fügt eine temporäre Route für 10.20.30.0/24 via 192.168.1.1 hinzu?",
                options  = [
                    "route add 10.20.30.0/24 gw 192.168.1.1",
                    "ip route add 10.20.30.0/24 via 192.168.1.1",
                    "ip route insert 10.20.30.0/24 192.168.1.1",
                    "netstat -r add 10.20.30.0/24",
                ],
                correct  = 1,
                explanation = "ip route add NETZ via GATEWAY ist die moderne Syntax. route add ist veraltet. Temporär bis Neustart — für Persistenz: /etc/network/interfaces oder NetworkManager.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was gibt 'dig +short google.com MX' aus?",
                options  = [
                    "Die IPv4-Adresse von google.com",
                    "Den Reverse-DNS-Namen von google.com",
                    "Die Mail-Exchange-Server für google.com",
                    "Den CNAME-Alias für google.com",
                ],
                correct  = 2,
                explanation = "MX-Record = Mail Exchanger. dig DOMAIN MX = MX-Records abfragen. +short = kompakte Ausgabe ohne Header.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "In welcher Reihenfolge werden Name-Auflösungen durchgeführt (Standard)?",
                options  = [
                    "DNS → /etc/hosts → WINS",
                    "/etc/hosts → DNS (konfiguriert in /etc/nsswitch.conf)",
                    "DNS → /etc/hosts → /etc/resolv.conf",
                    "/etc/resolv.conf → /etc/hosts",
                ],
                correct  = 1,
                explanation = "/etc/nsswitch.conf definiert die Reihenfolge (hosts: files dns). Standard: erst /etc/hosts (files), dann DNS. Kann je nach Distribution variieren.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher SSH-Befehl kopiert den Public Key zum Remote-Host für passwortlosen Login?",
                options  = [
                    "scp ~/.ssh/id_rsa.pub user@host:",
                    "ssh-copy-id user@host",
                    "ssh-add user@host",
                    "ssh user@host 'cat > .ssh/authorized_keys'",
                ],
                correct  = 1,
                explanation = "ssh-copy-id kopiert den Public Key in ~/.ssh/authorized_keys auf dem Remote-Host (korrekte Rechte werden automatisch gesetzt). scp würde nur kopieren ohne Rechte zu setzen.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht '-D 8080' in einem SSH-Befehl?",
                options  = [
                    "Leitet lokalen Port 8080 zu einem Remote-Dienst",
                    "Erstellt einen SOCKS-Proxy auf lokalem Port 8080",
                    "Leitet Remote-Port 8080 zu localhost",
                    "Deaktiviert SSH-Kompression auf Port 8080",
                ],
                correct  = 1,
                explanation = "ssh -D PORT = Dynamic Port Forwarding = SOCKS5-Proxy. Alle Verbindungen über den Proxy laufen durch den SSH-Tunnel. -L = Local, -R = Remote, -D = Dynamic (SOCKS).",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher iptables-Befehl erlaubt eingehende SSH-Verbindungen (Port 22)?",
                options  = [
                    "iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT",
                    "iptables -A INPUT -p tcp --dport 22 -j ACCEPT",
                    "iptables -I FORWARD -p tcp --sport 22 -j ACCEPT",
                    "iptables -A INPUT -p ssh -j ACCEPT",
                ],
                correct  = 1,
                explanation = "iptables -A INPUT = Append zur INPUT-Chain (eingehend). -p tcp --dport 22 = TCP Zielport 22. -j ACCEPT = annehmen. OUTPUT = ausgehend, FORWARD = weiterleiten.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was ist der Zweck von /etc/hosts.allow und /etc/hosts.deny?",
                options  = [
                    "Konfiguration des HTTP-Access-Controls",
                    "TCP Wrappers — Zugangskontrolle für Netzwerkdienste",
                    "DNS-Whitelist und -Blacklist",
                    "SSH-Key-Verwaltung für bestimmte Hosts",
                ],
                correct  = 1,
                explanation = "TCP Wrappers (tcpd/libwrap): hosts.allow = Whitelist, hosts.deny = Blacklist. Gleiche Logik wie cron.allow/deny. Prüfung: allow vor deny.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt die aktuell aktiven Netzwerkverbindungen mit PIDs an?",
                options  = ["netstat -an", "ss -tulpn", "ip connection show", "lsof -n"],
                correct  = 1,
                explanation = "ss -tulpn: -t=TCP -u=UDP -l=listening -p=PID/Prozess -n=numerisch. Moderneres, schnelleres Tool als netstat. ss -an zeigt alle Verbindungen.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche Datei konfiguriert dauerhaft den Hostnamen auf systemd-Systemen?",
                options  = ["/etc/hostname", "/etc/hosts", "/proc/sys/kernel/hostname", "/etc/network/hostname"],
                correct  = 0,
                explanation = "/etc/hostname enthält den statischen Hostnamen. hostnamectl set-hostname NEWNAME schreibt dorthin. /etc/hosts für lokale Namensauflösung.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "109: /26=62 Hosts | ip route add via | dig MX | nsswitch.conf=Reihenfolge | ssh-copy-id | -D=SOCKS | iptables INPUT/OUTPUT | ss -tulpn",
        memory_tip   = "SSH Tunnels: -L Local (dein Port) -R Remote (ihr Port) -D Dynamic (SOCKS Proxy)",
        gear_reward  = None,
        faction_reward = ("Net Runners", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.14 — Topic 110: Security Deep Quiz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.14",
        chapter      = 18,
        title        = "Exam Block 14 — Topic 110: Security Deep Quiz",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Letzter Block vor dem Boss, Ghost.\n"
            " Topic 110 — Sicherheit. Der härteste Bereich.\n"
            " SUID, SSH, GPG, sudo, LUKS, fail2ban, OpenSSL.\n"
            " 10 Fragen. Kein Pardon.'"
        ),
        why_important = "LPIC-1 Exam 102: Topic 110 — Security",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "10 Prüfungsfragen: Security tief.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Was passiert wenn das SUID-Bit auf /usr/bin/program gesetzt ist?",
                options  = [
                    "Nur root darf das Programm ausführen",
                    "Das Programm läuft mit den Rechten des Datei-Eigentümers, nicht des aufrufenden Users",
                    "Das Programm wird beim Login automatisch gestartet",
                    "Das Programm bekommt Kernel-Rechte",
                ],
                correct  = 1,
                explanation = "SUID (Set User ID): Das Programm läuft mit UID des Eigentümers (oft root). Beispiel: /usr/bin/passwd (owned by root, SUID) — kann /etc/shadow schreiben.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher OpenSSH-Parameter verhindert Login als root via SSH?",
                options  = [
                    "DenyUsers root",
                    "PermitRootLogin no",
                    "AllowUsers !root",
                    "RootLogin disabled",
                ],
                correct  = 1,
                explanation = "PermitRootLogin no in /etc/ssh/sshd_config verhindert direkten Root-Login. PermitRootLogin without-password erlaubt Root nur mit Key. sshd -t prüft Syntax.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher GPG-Befehl verschlüsselt eine Datei für 'Alice' (ihr öffentlicher Schlüssel muss importiert sein)?",
                options  = [
                    "gpg -e datei.txt",
                    "gpg -e -r Alice datei.txt",
                    "gpg --encrypt --recipient Alice datei.txt",
                    "B und C",
                ],
                correct  = 3,
                explanation = "gpg -e -r EMPFÄNGER DATEI oder gpg --encrypt --recipient EMPFÄNGER DATEI. -r/--recipient bestimmt den Empfänger. gpg -e ohne -r verschlüsselt symmetrisch.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was bedeutet 'bantime = -1' in der fail2ban-Konfiguration?",
                options  = [
                    "Kein Banning aktiv",
                    "Permanentes Banning (kein automatisches Unban)",
                    "Banning für 1 Sekunde",
                    "Banning wird nach 1 Fehlversuch aktiviert",
                ],
                correct  = 1,
                explanation = "bantime = -1 in fail2ban = permanentes Banning. bantime = 3600 = 1 Stunde. fail2ban-client set sshd unbanip IP hebt manuelle Bans auf.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher LUKS-Befehl öffnet ein verschlüsseltes LUKS-Volume?",
                options  = [
                    "luks-open /dev/sdb1 secret",
                    "cryptsetup luksOpen /dev/sdb1 secret",
                    "cryptsetup open --type luks /dev/sdb1 secret",
                    "B und C",
                ],
                correct  = 3,
                explanation = "cryptsetup luksOpen und cryptsetup open --type luks sind äquivalent. Ergebnis: /dev/mapper/secret. Dann mounten: mount /dev/mapper/secret /mnt.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was gibt 'openssl dgst -sha256 datei.txt' aus?",
                options  = [
                    "Verschlüsselt datei.txt mit SHA-256",
                    "Den SHA-256-Hashwert der Datei",
                    "Ein SHA-256-Zertifikat",
                    "Den SHA-256-verschlüsselten Dateiinhalt",
                ],
                correct  = 1,
                explanation = "openssl dgst -sha256 berechnet den SHA-256-Prüfsummen-Hash der Datei. Nicht verschlüsseln — nur Integrität prüfen. sha256sum datei.txt macht dasselbe.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher sudo-Eintrag erlaubt user 'ghost' nur den Befehl /bin/systemctl restart nginx?",
                options  = [
                    "ghost ALL=(ALL) /bin/systemctl restart nginx",
                    "ghost ALL=(root) NOPASSWD: /bin/systemctl restart nginx",
                    "ghost localhost=(root) /bin/systemctl restart nginx",
                    "A und C",
                ],
                correct  = 3,
                explanation = "ghost ALL=(ALL) /bin/systemctl restart nginx = mit Passwort. ghost localhost=(root) /bin/systemctl restart nginx = nur lokal. Beide sind syntaktisch korrekt.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl überprüft eine GPG-Signatur einer Datei?",
                options  = [
                    "gpg --check datei.sig",
                    "gpg --verify datei.sig datei.txt",
                    "gpg -d datei.sig",
                    "gpg --authenticate datei.sig",
                ],
                correct  = 1,
                explanation = "gpg --verify SIGNATUR DATEI prüft ob die Signatur valide ist und von welchem Key sie stammt. gpg -d entschlüsselt. Signieren: gpg --sign oder gpg --detach-sign.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was prüft 'sudo -l' für den aktuellen User?",
                options  = [
                    "Die letzten sudo-Befehle aus dem Log",
                    "Welche Befehle der User via sudo ausführen darf",
                    "Ob sudo installiert ist",
                    "Die sudo-Konfigurationsdatei auf Syntaxfehler",
                ],
                correct  = 1,
                explanation = "sudo -l (list) zeigt alle erlaubten (und verbotenen) sudo-Befehle für den aktuellen Benutzer. sudo -ll = ausführlichere Darstellung.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt alle Benutzer die sich zuletzt erfolglos eingeloggt haben?",
                options  = ["last -f /var/log/auth.log", "lastb", "faillog", "B und C"],
                correct  = 3,
                explanation = "lastb liest /var/log/btmp (failed logins). faillog zeigt Fehllogins aus /var/log/faillog. Beide sind für Sicherheits-Audits relevant.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "110: SUID=läuft als Eigentümer | PermitRootLogin no | gpg -e -r | bantime=-1=permanent | cryptsetup luksOpen | openssl dgst | sudo -l | lastb=failed logins",
        memory_tip   = "GPG: -e=encrypt -d=decrypt --sign=signieren --verify=prüfen --list-keys=anzeigen",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.15 — Exam Block 15: Topic 101.1 Hardware & Devices Deep
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.15",
        chapter      = 18,
        title        = "Exam Block 15 — Hardware Deep Dive",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Hardware-Layer. Die Grundlage von allem.\n"
            " lspci, lsusb, /proc, /sys — vollständige Abdeckung.\n"
            " Dieser Block ist Pflicht für Exam 101.'"
        ),
        why_important = "LPIC-1 Exam 101 Topic 101.1 Hardware-Erkennung hat hohe Prüfungsrelevanz.",
        explanation  = "Tiefgehende Prüfungsvorbereitung für Hardware und Geräteverwaltung.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Hardware-Fragen korrekt.",
        expected_commands = [],
        hint_text    = "Denk an lspci, lsusb, dmidecode, /proc/interrupts, udev",
        quiz_questions = [
            QuizQuestion(
                question = "Welches Tool zeigt PCI-Geräte und ihre Treiber?",
                options  = ["lspci -k", "lsusb -t", "dmidecode -t pci", "udevadm info /dev/sda"],
                correct  = 0,
                explanation = "lspci -k zeigt PCI-Geräte mit dem aktuell verwendeten Kernel-Treiber.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was zeigt `/proc/interrupts`?",
                options  = [
                    "IRQ-Nummern und wie oft jedes Gerät einen Interrupt ausgelöst hat",
                    "Alle blockierten Prozesse",
                    "CPU-Interrupt-Frequenz",
                    "Geräte-Treiber-Status",
                ],
                correct  = 0,
                explanation = "/proc/interrupts zeigt IRQ-Nummern, Interrupt-Counts und Handler-Namen.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Wo liegen udev-Regeln für benutzerdefinierte Gerätekonfiguration?",
                options  = [
                    "/etc/udev/rules.d/",
                    "/usr/lib/udev/rules.d/",
                    "/proc/udev/rules/",
                    "/sys/bus/usb/rules/",
                ],
                correct  = 0,
                explanation = "/etc/udev/rules.d/ für benutzerdefinierte Regeln. /usr/lib/udev/rules.d/ für Paket-Regeln.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was bedeutet 'coldplug' vs 'hotplug'?",
                options  = [
                    "coldplug = Gerät beim Boot, hotplug = Gerät während Betrieb einstecken",
                    "coldplug = USB, hotplug = PCI",
                    "coldplug = extern, hotplug = intern",
                    "coldplug = langsam, hotplug = schnell",
                ],
                correct  = 0,
                explanation = "Coldplug: Geräte die beim Systemstart vorhanden sind. Hotplug: Dynamisch während Betrieb.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "lspci -k zeigt Treiber. /proc/interrupts = IRQs. /proc/ioports = I/O-Ports. udevadm trigger = Regeln neu laden.",
        memory_tip   = "lspci (PCI), lsusb (USB), dmidecode (BIOS/Hardware-Info), udevadm (Geräteverwaltung).",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.16 — Exam Block 16: Scripting & Automation Deep
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.16",
        chapter      = 18,
        title        = "Exam Block 16 — Scripting Deep Dive",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Bash-Scripting. Der Kleber des Systems.\n"
            " Variablen, Schleifen, Funktionen, getopts.\n"
            " Topic 105.2 — vollständige Prüfungssimulation.'"
        ),
        why_important = "LPIC-1 Exam 102 Topic 105.2 Bash-Scripting ist prüfungsrelevant.",
        explanation  = "Prüfungsvorbereitung für Bash-Scripting.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Scripting-Fragen.",
        expected_commands = [],
        hint_text    = "Denk an $?, $#, $@, set -e, getopts, case, IFS",
        quiz_questions = [
            QuizQuestion(
                question = "Was gibt `$?` zurück?",
                options  = [
                    "Exit-Code des zuletzt ausgeführten Befehls",
                    "Anzahl der Parameter",
                    "Alle Parameter als eine Zeichenkette",
                    "PID des letzten Hintergrundprozesses",
                ],
                correct  = 0,
                explanation = "$? = Exit-Code des letzten Befehls. 0 = Erfolg, ≠0 = Fehler.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht `set -e` in einem Bash-Script?",
                options  = [
                    "Script beendet sich sofort wenn ein Befehl mit Fehler endet",
                    "Aktiviert Xtrace (Debug-Mode)",
                    "Behandelt ungesetzte Variablen als Fehler",
                    "Exportiert alle Variablen",
                ],
                correct  = 0,
                explanation = "set -e = exit on error. set -u = unbound variable error. set -x = xtrace debug.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Wie liest man eine Datei Zeile für Zeile sicher?",
                options  = [
                    "while IFS= read -r line; do ...; done < datei",
                    "for line in $(cat datei); do ...; done",
                    "cat datei | while read line; do ...; done",
                    "read datei | while line; do ...; done",
                ],
                correct  = 0,
                explanation = "IFS= verhindert Trimming, -r verhindert Backslash-Interpretation. Sicherste Methode.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht `getopts 'hvf:' OPT` in einer while-Schleife?",
                options  = [
                    "Parst Optionen: -h -v als Flags, -f erwartet ein Argument",
                    "Definiert Optionen für das Help-Menü",
                    "Liest alle Umgebungsvariablen",
                    "Setzt Funktions-Optionen",
                ],
                correct  = 0,
                explanation = "f: (mit Doppelpunkt) = f erwartet ein Argument in $OPTARG. h und v sind Flags.",
                xp_value = 20,
            ),
        ],
        exam_tip     = "$? = Exit-Code | $# = Anzahl Args | $@ = alle Args | $$ = PID | $0 = Skriptname",
        memory_tip   = "set -euo pipefail = safe scripting defaults. IFS= read -r = safe line reading.",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.17 — Exam Block 17: Netzwerk Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.17",
        chapter      = 18,
        title        = "Exam Block 17 — Netzwerk Advanced",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Netzwerk. TCP/IP, Subnetting, Routing.\n"
            " Der letzte Block vor dem Endkampf.\n"
            " Topic 109 — advanced.'"
        ),
        why_important = "LPIC-1 Topic 109 Networking ist ein Schwerpunkt in Exam 102.",
        explanation  = "Prüfungsvorbereitung für Netzwerk-Konfiguration und -Diagnose.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Netzwerk-Fragen.",
        expected_commands = [],
        hint_text    = "Denk an ip addr, ip route, ss, dig, ssh-keygen",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist die Netzwerk-Adresse von 192.168.5.130/26?",
                options  = [
                    "192.168.5.128",
                    "192.168.5.0",
                    "192.168.5.64",
                    "192.168.5.192",
                ],
                correct  = 0,
                explanation = "/26 = Subnetzmaske 255.255.255.192. 130 AND 192 = 128. Netzadresse = 192.168.5.128",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welcher ssh-keygen-Typ ist für neue Systeme empfohlen?",
                options  = [
                    "ssh-keygen -t ed25519",
                    "ssh-keygen -t rsa -b 1024",
                    "ssh-keygen -t dsa",
                    "ssh-keygen -t rsa -b 512",
                ],
                correct  = 0,
                explanation = "Ed25519 ist modern, sicher und schnell. RSA 4096 ist Alternative. DSA ist veraltet.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Was macht `ip route add default via 192.168.1.1`?",
                options  = [
                    "Setzt 192.168.1.1 als Standard-Gateway",
                    "Fügt eine Route zu 192.168.1.1 hinzu",
                    "Entfernt die Standard-Route",
                    "Zeigt die Routing-Tabelle",
                ],
                correct  = 0,
                explanation = "default = 0.0.0.0/0 = alle Pakete ohne spezifische Route gehen via diesen Gateway.",
                xp_value = 20,
            ),
            QuizQuestion(
                question = "Welche DNS-Record-Typen sollte man für LPIC-1 kennen?",
                options  = [
                    "A (IPv4), AAAA (IPv6), MX (Mail), PTR (Reverse), CNAME (Alias), NS (Nameserver)",
                    "A, B, C, D (Adressklassen)",
                    "TCP, UDP, ICMP",
                    "HTTP, HTTPS, FTP, SSH",
                ],
                correct  = 0,
                explanation = "A=IPv4, AAAA=IPv6, MX=Mail, PTR=Reverse-DNS, CNAME=Alias, NS=Nameserver, SOA=Zone Authority",
                xp_value = 20,
            ),
        ],
        exam_tip     = "Subnetting: /26=64 Hosts /25=128 /24=256. A=IPv4 AAAA=IPv6 MX=Mail PTR=Reverse.",
        memory_tip   = "ip route = moderne Routing-Tabelle. ss -tulpn = lauschende Ports. dig = DNS-Diagnose.",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 10),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.18 — Exam Block 18: Gemischte Fragen (Timed Challenge)
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.18",
        chapter      = 18,
        title        = "Exam Block 18 — Speed Round: Alle Topics",
        mtype        = "QUIZ",
        xp           = 250,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Letzter Test vor dem Boss. Speed Round.\n"
            " Alle Topics. Schnelle Fragen. Keine Zeit zum Überlegen.\n"
            " Das echte Exam hat 60 Fragen in 90 Minuten. Das hier — 5 in 2.'"
        ),
        why_important = "Prüfungssimulation: schnelle Fragen-Beantwortung über alle LPIC-1 Topics.",
        explanation  = "Speed Round — alle Topics gemischt.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Speed-Round-Fragen.",
        expected_commands = [],
        hint_text    = "Vertraue deinem Wissen. Erste Antwort ist oft richtig.",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl zeigt den aktuellen Runlevel?",
                options  = ["runlevel", "telinit -q", "systemctl list-targets", "who -r"],
                correct  = 0,
                explanation = "runlevel zeigt Previous und Current runlevel. who -r ist Alternative.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Was macht `chmod 4755 /usr/bin/myapp`?",
                options  = [
                    "Setzt SUID-Bit: Programm läuft als Eigentümer",
                    "Setzt SGID-Bit",
                    "Setzt Sticky-Bit",
                    "Macht Datei ausführbar für alle",
                ],
                correct  = 0,
                explanation = "4755: 4=SUID, 7=rwx(owner), 5=r-x(group), 5=r-x(other). Läuft als Dateieigentümer.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen `>` und `>>`?",
                options  = [
                    "> überschreibt, >> hängt an",
                    "> hängt an, >> überschreibt",
                    "Beide überschreiben",
                    "> ist für stderr, >> für stdout",
                ],
                correct  = 0,
                explanation = "> truncate und schreiben. >> append. 2> stderr umleiten. &> beides umleiten.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt alle Kernel-Module?",
                options  = ["lsmod", "modinfo", "modprobe -l", "insmod --list"],
                correct  = 0,
                explanation = "lsmod liest /proc/modules und zeigt geladene Module mit Size und Usern.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Wie viele Punkte braucht man um LPIC-1 zu bestehen?",
                options  = ["500 von 800", "600 von 1000", "70% von 100", "450 von 600"],
                correct  = 0,
                explanation = "500/800 Punkte pro Prüfung (101 und 102). 90 Minuten, ~60 Fragen jeweils.",
                xp_value = 25,
            ),
        ],
        exam_tip     = "LPIC-1 = 500/800 pro Exam. 90 Min. 2 Exams (101+102). Gültig 5 Jahre.",
        memory_tip   = "Speed Round trainiert Exam-Geschwindigkeit. Im echten Exam: ~1.5 Min/Frage.",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.19 — Exam Block 19: Storage & RAID Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.19",
        chapter      = 18,
        title        = "Exam Block 19 — Storage & RAID Advanced",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 19. Storage tief.\n"
            " mdadm, LVM, btrfs, RAID-Level — kein Nachschlagen.\n"
            " 8 Fragen. Kein Fehler erlaubt.'"
        ),
        why_important = "LPIC-1 Exam 101: Topics 104.1 / 104.2 — Storage, RAID, LVM",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: Storage & RAID Advanced.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher Befehl erstellt ein RAID-5-Array aus 3 Laufwerken?",
                options    = [
                    "mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd",
                    "mdadm --build /dev/md0 --raid5 /dev/sdb /dev/sdc /dev/sdd",
                    "raid-create --level 5 /dev/md0 /dev/sdb /dev/sdc /dev/sdd",
                    "mkraid --level=5 /dev/md0 /dev/sdb /dev/sdc /dev/sdd",
                ],
                correct    = 0,
                explanation = (
                    "mdadm --create mit --level=5 und --raid-devices=3 erstellt RAID-5.\n"
                    "RAID-5 benötigt mindestens 3 Laufwerke und toleriert 1 Ausfall.\n"
                    "Die Konfiguration wird in /etc/mdadm/mdadm.conf gespeichert."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Wie viele Laufwerke dürfen bei RAID-6 gleichzeitig ausfallen?",
                options    = ["0", "1", "2", "3"],
                correct    = 2,
                explanation = (
                    "RAID-6 verwendet zwei Paritätsblöcke und toleriert 2 gleichzeitige Ausfälle.\n"
                    "RAID-5 = 1 Ausfall. RAID-1 = n-1 Ausfälle (bei n Laufwerken).\n"
                    "RAID-6 benötigt mindestens 4 Laufwerke."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher LVM-Befehl zeigt alle Physical Volumes an?",
                options    = ["lvdisplay", "vgdisplay", "pvdisplay", "lvm --list"],
                correct    = 2,
                explanation = (
                    "pvdisplay zeigt detaillierte Infos über Physical Volumes.\n"
                    "pvs = kompaktere Übersicht. vgdisplay = Volume Groups. lvdisplay = Logical Volumes.\n"
                    "Hierarchie: PV → VG → LV"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Wie erweitert man ein ext4-Dateisystem nach LV-Vergrößerung?",
                options    = [
                    "fsck /dev/mapper/vg-lv",
                    "resize2fs /dev/mapper/vg-lv",
                    "lvresize /dev/mapper/vg-lv",
                    "tune2fs -L /dev/mapper/vg-lv",
                ],
                correct    = 1,
                explanation = (
                    "resize2fs passt das ext2/3/4-Dateisystem an die neue LV-Größe an.\n"
                    "Reihenfolge: lvextend → resize2fs (oder lvextend --resizefs).\n"
                    "Für XFS: xfs_growfs (nur vergrößern, kein Verkleinern)."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist ein btrfs-Subvolume?",
                options    = [
                    "Eine Partition innerhalb von btrfs",
                    "Ein eigenständig mountbarer Dateisystem-Namespace innerhalb btrfs",
                    "Ein RAID-Gerät in btrfs",
                    "Eine verschlüsselte btrfs-Partition",
                ],
                correct    = 1,
                explanation = (
                    "btrfs-Subvolumes sind unabhängige Dateisystem-Namespaces die\n"
                    "separat gemountet werden können. Basis für Snapshots.\n"
                    "btrfs subvolume create /mnt/sub1 | btrfs subvolume list /mnt"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl zeigt den RAID-Status in /proc?",
                options    = [
                    "cat /proc/raid",
                    "cat /proc/mdstat",
                    "mdadm --status",
                    "cat /sys/block/md0/status",
                ],
                correct    = 1,
                explanation = (
                    "/proc/mdstat zeigt den aktuellen Status aller Software-RAID-Arrays.\n"
                    "Zeigt Synchronisierungsfortschritt, Gerätestatus und RAID-Level.\n"
                    "mdadm --detail /dev/md0 für detailliertere Infos."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welches RAID-Level bietet Striping ohne Redundanz?",
                options    = ["RAID-0", "RAID-1", "RAID-5", "RAID-10"],
                correct    = 0,
                explanation = (
                    "RAID-0 = Striping: Daten auf alle Laufwerke verteilt, maximale Geschwindigkeit.\n"
                    "Kein Fehlertoleranz — ein Ausfall = Datenverlust.\n"
                    "RAID-1 = Mirroring | RAID-5 = Striping+Parität | RAID-10 = Mirror+Stripe"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was macht 'vgextend vg0 /dev/sde'?",
                options    = [
                    "Erstellt eine neue Volume Group vg0",
                    "Fügt /dev/sde als Physical Volume zur Volume Group vg0 hinzu",
                    "Vergrößert einen Logical Volume in vg0",
                    "Erstellt einen Snapshot von vg0",
                ],
                correct    = 1,
                explanation = (
                    "vgextend fügt ein Physical Volume zu einer bestehenden Volume Group hinzu.\n"
                    "Vorher: pvcreate /dev/sde (PV initialisieren).\n"
                    "Danach kann lvextend den neuen Speicher nutzen."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "RAID-0=Stripe | RAID-1=Mirror | RAID-5=Parität | RAID-6=2xParität | pvdisplay/vgdisplay/lvdisplay",
        memory_tip   = "LVM: PV→VG→LV wie Ziegelstein→Lager→Regal",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.20 — Exam Block 20: Container & Virtualization
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.20",
        chapter      = 18,
        title        = "Exam Block 20 — Container & Virtualization",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 20. Container und VMs.\n"
            " docker, podman, systemd-nspawn, KVM.\n"
            " Die moderne Infrastruktur wartet.'"
        ),
        why_important = "LPIC-1 Exam 102: Virtualisierung und Container-Grundlagen",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: Container & Virtualization.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen einem Container und einer VM?",
                options    = [
                    "Container sind langsamer als VMs",
                    "Container teilen den Host-Kernel, VMs haben eigenen Kernel",
                    "VMs haben keinen eigenen Kernel",
                    "Container können keinen Netzwerk-Stack haben",
                ],
                correct    = 1,
                explanation = (
                    "Container nutzen den Host-Kernel (via Namespaces+cgroups).\n"
                    "VMs haben vollständige Hardware-Virtualisierung mit eigenem Kernel.\n"
                    "Container = leichter, schneller | VM = volle Isolation."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl startet einen Container im Hintergrund mit docker?",
                options    = [
                    "docker run nginx",
                    "docker run -d nginx",
                    "docker start -d nginx",
                    "docker exec -d nginx",
                ],
                correct    = 1,
                explanation = (
                    "docker run -d (detach) startet Container im Hintergrund.\n"
                    "docker run ohne -d = interaktiv im Vordergrund.\n"
                    "docker ps zeigt laufende Container."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist der Hauptvorteil von podman gegenüber docker?",
                options    = [
                    "Podman ist schneller",
                    "Podman läuft rootless ohne Daemon",
                    "Podman unterstützt mehr Images",
                    "Podman ist in C geschrieben",
                ],
                correct    = 1,
                explanation = (
                    "podman läuft rootless (kein Root-Daemon erforderlich) und daemonless.\n"
                    "Kompatibel mit Docker CLI-Syntax.\n"
                    "Bessere Sicherheit da kein privilegierter Daemon läuft."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche Linux-Kernel-Features bilden die Grundlage für Container?",
                options    = [
                    "RAID und LVM",
                    "Namespaces und cgroups",
                    "iptables und nftables",
                    "systemd und udev",
                ],
                correct    = 1,
                explanation = (
                    "Namespaces isolieren: PID, Netzwerk, Mount, User, IPC, UTS.\n"
                    "cgroups (Control Groups) begrenzen Ressourcen: CPU, RAM, I/O.\n"
                    "Zusammen ermöglichen sie Container-Isolation."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was macht systemd-nspawn?",
                options    = [
                    "Startet systemd in einem Namespace-Container",
                    "Konfiguriert systemd-Netzwerk",
                    "Spawnt neue systemd-Units",
                    "Startet einen KVM-Gast",
                ],
                correct    = 0,
                explanation = (
                    "systemd-nspawn erstellt leichtgewichtige Container (Chroot auf Steroiden).\n"
                    "Nutzt Namespaces für Isolation. Gut für System-Container.\n"
                    "Wird von machinectl verwaltet."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl zeigt alle laufenden und gestoppten docker-Container?",
                options    = [
                    "docker ps",
                    "docker ps -a",
                    "docker list --all",
                    "docker containers",
                ],
                correct    = 1,
                explanation = (
                    "docker ps -a zeigt alle Container (laufend und gestoppt).\n"
                    "docker ps (ohne -a) zeigt nur laufende Container.\n"
                    "docker ps -q gibt nur IDs aus (für Scripting)."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist KVM?",
                options    = [
                    "Ein Container-Format",
                    "Kernel-based Virtual Machine — Typ-1-Hypervisor im Kernel",
                    "Ein Kubernetes-Tool",
                    "Ein Dateisystem für VMs",
                ],
                correct    = 1,
                explanation = (
                    "KVM (Kernel-based Virtual Machine) ist ein Typ-1-Hypervisor direkt im Linux-Kernel.\n"
                    "Benötigt CPU-Virtualisierungserweiterungen (Intel VT-x / AMD-V).\n"
                    "Wird oft mit QEMU und libvirt/virsh verwaltet."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welches Verzeichnis enthält die Konfiguration von docker-Containern?",
                options    = [
                    "/etc/docker",
                    "/var/lib/docker",
                    "/run/docker",
                    "/home/docker",
                ],
                correct    = 1,
                explanation = (
                    "/var/lib/docker enthält Images, Container, Volumes und Netzwerke.\n"
                    "/etc/docker/daemon.json = Docker-Daemon-Konfiguration.\n"
                    "docker info zeigt alle Pfade und Konfigurationsdetails."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "Container = Namespaces+cgroups | docker run -d = Hintergrund | podman = rootless | KVM = Typ-1-Hypervisor",
        memory_tip   = "Container teilen Kernel, VMs nicht | Namespaces = Isolation | cgroups = Limits",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.21 — Exam Block 21: Firewall & Security Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.21",
        chapter      = 18,
        title        = "Exam Block 21 — Firewall & Security Advanced",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 21. Sicherheit.\n"
            " iptables, nftables, fail2ban, LUKS.\n"
            " NeonGrid-9 wird angegriffen. Halte die Linie.'"
        ),
        why_important = "LPIC-1 Exam 102: Topics 110.1/110.2 — Security & Firewall",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: Firewall & Security Advanced.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Welche iptables-Chain verarbeitet Pakete die für den lokalen Prozess bestimmt sind?",
                options    = ["FORWARD", "OUTPUT", "INPUT", "PREROUTING"],
                correct    = 2,
                explanation = (
                    "INPUT-Chain: Pakete die an den lokalen Host adressiert sind.\n"
                    "OUTPUT: Pakete die der lokale Host sendet.\n"
                    "FORWARD: Pakete die weitergeleitet werden (Router-Funktion)."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl blockiert alle eingehenden Verbindungen außer SSH mit iptables?",
                options    = [
                    "iptables -A INPUT -p tcp --dport 22 -j ACCEPT && iptables -A INPUT -j DROP",
                    "iptables -D INPUT -p tcp --dport 22 -j DENY",
                    "iptables --block all --allow 22",
                    "iptables -F INPUT && iptables -A INPUT -j DROP",
                ],
                correct    = 0,
                explanation = (
                    "Reihenfolge ist kritisch: SSH zuerst ACCEPT, dann DROP für den Rest.\n"
                    "iptables verarbeitet Regeln von oben nach unten — erste Übereinstimmung gewinnt.\n"
                    "Auch ESTABLISHED,RELATED erlauben für bestehende Verbindungen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist nftables?",
                options    = [
                    "Ein neues Dateisystem-Tool",
                    "Der Nachfolger von iptables/ip6tables/ebtables/arptables",
                    "Ein Netzwerk-Debugging-Tool",
                    "Ein Load-Balancer",
                ],
                correct    = 1,
                explanation = (
                    "nftables ersetzt iptables, ip6tables, ebtables und arptables.\n"
                    "Modernere Syntax, bessere Performance, ein Framework für alle Protokolle.\n"
                    "nft list ruleset | nft add rule inet filter input tcp dport 22 accept"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was macht fail2ban?",
                options    = [
                    "Firewall-Regeln automatisch erstellen",
                    "Brute-Force-Angriffe erkennen und IPs temporär sperren",
                    "SSH-Verbindungen verschlüsseln",
                    "Kernel-Module überwachen",
                ],
                correct    = 1,
                explanation = (
                    "fail2ban überwacht Log-Dateien (SSH, Apache...) und sperrt IPs\n"
                    "nach zu vielen fehlgeschlagenen Login-Versuchen via iptables/nftables.\n"
                    "fail2ban-client status sshd | fail2ban-client set sshd unbanip IP"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl verschlüsselt eine Partition mit LUKS?",
                options    = [
                    "cryptsetup luksFormat /dev/sdb1",
                    "luks-encrypt /dev/sdb1",
                    "openssl enc -aes /dev/sdb1",
                    "dm-crypt create /dev/sdb1",
                ],
                correct    = 0,
                explanation = (
                    "cryptsetup luksFormat initialisiert LUKS-Verschlüsselung auf der Partition.\n"
                    "Danach: cryptsetup luksOpen /dev/sdb1 secret → /dev/mapper/secret\n"
                    "LUKS = Linux Unified Key Setup, Standard für Festplattenverschlüsselung."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was zeigt 'iptables -L -n -v'?",
                options    = [
                    "Alle Netzwerk-Interfaces",
                    "Alle Firewall-Regeln mit Zähler und numerischen Adressen",
                    "Alle aktiven Verbindungen",
                    "Alle gesperrten IPs",
                ],
                correct    = 1,
                explanation = (
                    "-L = list rules | -n = numerische Ausgabe (keine DNS-Auflösung) | -v = verbose (Zähler).\n"
                    "iptables -L -n --line-numbers zeigt auch Zeilennummern.\n"
                    "iptables-save > /etc/iptables/rules.v4 für persistente Regeln."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche Datei konfiguriert sudo-Berechtigungen?",
                options    = [
                    "/etc/sudo.conf",
                    "/etc/sudoers",
                    "/etc/sudo/permissions",
                    "/var/sudo/config",
                ],
                correct    = 1,
                explanation = (
                    "/etc/sudoers enthält sudo-Berechtigungen. IMMER mit visudo bearbeiten!\n"
                    "visudo prüft die Syntax vor dem Speichern.\n"
                    "/etc/sudoers.d/ = Verzeichnis für modulare sudo-Konfiguration."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist der Unterschied zwischen DROP und REJECT in iptables?",
                options    = [
                    "Kein Unterschied",
                    "DROP verwirft still, REJECT sendet Fehlerantwort zurück",
                    "REJECT ist schneller als DROP",
                    "DROP gilt nur für UDP, REJECT für TCP",
                ],
                correct    = 1,
                explanation = (
                    "DROP: Paket wird still verworfen — Absender bekommt keine Antwort (Timeout).\n"
                    "REJECT: Paket wird verworfen + ICMP-Fehlermeldung zurückgesendet.\n"
                    "DROP = besser gegen Port-Scanning | REJECT = schnelleres Client-Feedback."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "INPUT=eingehend | OUTPUT=ausgehend | FORWARD=weiterleiten | DROP=still | REJECT=Fehler",
        memory_tip   = "iptables: Reihenfolge zählt, erste Regel gewinnt | nftables = moderner Nachfolger",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.22 — Exam Block 22: Network Services
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.22",
        chapter      = 18,
        title        = "Exam Block 22 — Network Services",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 22. Netzwerkdienste.\n"
            " NFS, Samba, DHCP, LDAP, DNS.\n"
            " Das Netzwerk hält NeonGrid-9 am Leben.'"
        ),
        why_important = "LPIC-1 Exam 102: Topics 108.x/109.x — Netzwerkdienste",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: Network Services.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Welche Konfigurationsdatei definiert NFS-Exports?",
                options    = ["/etc/nfs.conf", "/etc/exports", "/etc/nfs/shares", "/etc/fstab"],
                correct    = 1,
                explanation = (
                    "/etc/exports definiert welche Verzeichnisse per NFS exportiert werden.\n"
                    "Format: /pfad client(optionen) — z.B. /data 192.168.1.0/24(rw,sync)\n"
                    "exportfs -ra lädt die Konfiguration neu."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Samba-Befehl testet die smb.conf auf Fehler?",
                options    = ["smbtest", "testparm", "samba-check", "smb --verify"],
                correct    = 1,
                explanation = (
                    "testparm prüft /etc/samba/smb.conf auf Syntaxfehler.\n"
                    "testparm -s gibt die aktive Konfiguration ohne Kommentare aus.\n"
                    "systemctl restart smbd nmbd nach Konfigurationsänderungen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Port wird von DNS verwendet?",
                options    = ["53", "67", "389", "445"],
                correct    = 0,
                explanation = (
                    "DNS verwendet Port 53 (UDP für Abfragen, TCP für Zone Transfers).\n"
                    "Port 67/68 = DHCP | Port 389 = LDAP | Port 445 = SMB/Samba.\n"
                    "dig, nslookup und host sind DNS-Abfrage-Tools."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche Datei enthält die DHCP-Server-Konfiguration auf Debian/Ubuntu?",
                options    = [
                    "/etc/dhcp/dhcpd.conf",
                    "/etc/dhcpd.conf",
                    "/etc/network/dhcp.conf",
                    "/var/lib/dhcp/dhcpd.conf",
                ],
                correct    = 0,
                explanation = (
                    "/etc/dhcp/dhcpd.conf ist die Hauptkonfiguration für isc-dhcp-server.\n"
                    "/var/lib/dhcp/dhcpd.leases enthält aktive DHCP-Leases.\n"
                    "dhcpd -t -cf /etc/dhcp/dhcpd.conf prüft die Konfiguration."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist der Standardport für LDAP?",
                options    = ["389", "636", "88", "3389"],
                correct    = 0,
                explanation = (
                    "LDAP = Port 389 (unverschlüsselt).\n"
                    "LDAPS = Port 636 (LDAP über TLS/SSL).\n"
                    "Port 88 = Kerberos | Port 3389 = RDP."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl zeigt DNS-Informationen für eine Domain an?",
                options    = ["whois domain.com", "dig domain.com", "nmap domain.com", "traceroute domain.com"],
                correct    = 1,
                explanation = (
                    "dig ist das mächtigste DNS-Abfrage-Tool.\n"
                    "dig domain.com = A-Record | dig domain.com MX = Mail-Server\n"
                    "dig @8.8.8.8 domain.com = bestimmten DNS-Server abfragen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche Datei auf dem Client konfiguriert NFS-Mounts beim Boot?",
                options    = ["/etc/nfs.conf", "/etc/fstab", "/etc/mounts", "/etc/auto.master"],
                correct    = 1,
                explanation = (
                    "/etc/fstab definiert alle Mounts beim Boot, auch NFS.\n"
                    "Format: server:/export /mountpoint nfs defaults 0 0\n"
                    "/etc/auto.master + autofs für automatisches Mounten."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Samba-Dienst ist für NetBIOS-Namensauflösung zuständig?",
                options    = ["smbd", "nmbd", "winbindd", "samba"],
                correct    = 1,
                explanation = (
                    "nmbd (NetBIOS Message Block Daemon) regelt NetBIOS-Namensauflösung.\n"
                    "smbd = Datei- und Druckerfreigabe.\n"
                    "winbindd = Integration mit Windows Active Directory."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "NFS=/etc/exports | Samba=testparm | DNS=Port53 | DHCP=/etc/dhcp/dhcpd.conf | LDAP=Port389",
        memory_tip   = "Netzwerkdienste: jeder hat seinen Standardport und seine Hauptkonfigdatei",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.23 — Exam Block 23: User Management Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.23",
        chapter      = 18,
        title        = "Exam Block 23 — User Management Advanced",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 23. Benutzerverwaltung.\n"
            " PAM, nsswitch, chage, limits.conf.\n"
            " Wer darf was — und wie lange.'"
        ),
        why_important = "LPIC-1 Exam 102: Topics 107.x — User & Group Management",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: User Management Advanced.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Was kontrolliert PAM (Pluggable Authentication Modules)?",
                options    = [
                    "Nur Passwort-Hashing",
                    "Authentifizierung, Autorisierung, Sitzungsverwaltung und Passwort-Management",
                    "Nur SSH-Login",
                    "Nur sudo-Berechtigungen",
                ],
                correct    = 1,
                explanation = (
                    "PAM ist ein flexibles Framework für 4 Bereiche:\n"
                    "auth = Authentifizierung | account = Kontoprüfung\n"
                    "password = Passwort-Änderung | session = Sitzungsverwaltung\n"
                    "Konfiguration in /etc/pam.d/"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was definiert /etc/nsswitch.conf?",
                options    = [
                    "Netzwerk-Switch-Konfiguration",
                    "Die Reihenfolge der Namensauflösungs-Datenbanken",
                    "LDAP-Server-Einstellungen",
                    "DNS-Konfiguration",
                ],
                correct    = 1,
                explanation = (
                    "/etc/nsswitch.conf (Name Service Switch) bestimmt die Reihenfolge:\n"
                    "passwd: files ldap → erst lokale Dateien, dann LDAP\n"
                    "hosts: files dns → erst /etc/hosts, dann DNS."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl zeigt das Passwort-Ablaufdatum eines Benutzers?",
                options    = [
                    "passwd -l user",
                    "chage -l user",
                    "usermod --expiry user",
                    "id --expire user",
                ],
                correct    = 1,
                explanation = (
                    "chage -l user zeigt alle Passwort-Aging-Informationen.\n"
                    "chage -M 90 user = maximales Passwort-Alter auf 90 Tage setzen.\n"
                    "chage -E 2026-12-31 user = Konto-Ablaufdatum setzen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche Datei definiert Ressourcenlimits für Benutzer?",
                options    = [
                    "/etc/limits.conf",
                    "/etc/security/limits.conf",
                    "/etc/ulimits.conf",
                    "/etc/pam/limits.conf",
                ],
                correct    = 1,
                explanation = (
                    "/etc/security/limits.conf setzt Ressourcenlimits (via PAM pam_limits).\n"
                    "Format: user type resource value\n"
                    "z.B. * hard nofile 65536 (max. offene Dateien für alle).\n"
                    "ulimit -a zeigt aktuelle Limits der Shell."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was speichert /etc/shadow?",
                options    = [
                    "Benutzer-Home-Verzeichnisse",
                    "Verschlüsselte Passwort-Hashes und Passwort-Aging-Info",
                    "Gruppen-Mitgliedschaften",
                    "SSH-Public-Keys",
                ],
                correct    = 1,
                explanation = (
                    "/etc/shadow enthält verschlüsselte Passwörter (Hashes) und\n"
                    "Passwort-Aging-Daten (letzte Änderung, Min/Max-Alter, Ablauf).\n"
                    "Nur lesbar für root. /etc/passwd enthält keine Passwörter mehr (x)."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl sperrt ein Benutzerkonto?",
                options    = [
                    "userdel --lock user",
                    "passwd -l user",
                    "usermod --disable user",
                    "chage --lock user",
                ],
                correct    = 1,
                explanation = (
                    "passwd -l user (lock) sperrt das Konto durch ein '!' vor dem Passwort-Hash.\n"
                    "passwd -u user (unlock) entsperrt wieder.\n"
                    "usermod -L user / usermod -U user machen dasselbe."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was macht 'useradd -m -s /bin/bash newuser'?",
                options    = [
                    "Erstellt User ohne Home-Verzeichnis mit bash",
                    "Erstellt User mit Home-Verzeichnis (-m) und bash als Shell (-s)",
                    "Modifiziert bestehenden User",
                    "Löscht User und erstellt neu",
                ],
                correct    = 1,
                explanation = (
                    "-m = Home-Verzeichnis erstellen (/home/newuser)\n"
                    "-s /bin/bash = Login-Shell setzen\n"
                    "useradd -m -s /bin/bash -G sudo newuser = auch sudo-Gruppe"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "In welcher Datei werden Gruppen-Passwörter gespeichert?",
                options    = ["/etc/group", "/etc/gshadow", "/etc/shadow", "/etc/gpasswd"],
                correct    = 1,
                explanation = (
                    "/etc/gshadow enthält Gruppen-Passwörter und Verwaltungsinfos.\n"
                    "/etc/group enthält Gruppenname, GID und Mitglieder.\n"
                    "gpasswd -a user group fügt User zur Gruppe hinzu."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "PAM=/etc/pam.d/ | nsswitch=/etc/nsswitch.conf | chage -l=Ablauf | limits=/etc/security/limits.conf",
        memory_tip   = "shadow=verschlüsselt | gshadow=Gruppen-Passwörter | chage=change age",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.24 — Exam Block 24: Logging & Scheduling Deep
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.24",
        chapter      = 18,
        title        = "Exam Block 24 — Logging & Scheduling Deep",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 24. Logs und Scheduling.\n"
            " journald, rsyslog, cron, systemd-timer.\n"
            " Was passiert wann — und wer schreibt es auf.'"
        ),
        why_important = "LPIC-1 Exam 102: Topics 108.2 / 107.2 — Logging & Scheduling",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: Logging & Scheduling Deep.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher Befehl zeigt die letzten 50 journald-Log-Einträge?",
                options    = [
                    "journalctl -n 50",
                    "journalctl --tail 50",
                    "journald -l 50",
                    "systemctl log -n 50",
                ],
                correct    = 0,
                explanation = (
                    "journalctl -n 50 zeigt die letzten 50 Log-Einträge.\n"
                    "journalctl -f = live verfolgen (wie tail -f).\n"
                    "journalctl -u ssh = nur SSH-Unit | journalctl --since '1 hour ago'"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche rsyslog-Facility repräsentiert Kernel-Meldungen?",
                options    = ["kern", "syslog", "daemon", "local0"],
                correct    = 0,
                explanation = (
                    "kern = Kernel-Meldungen (Facility 0).\n"
                    "auth/authpriv = Authentifizierung | daemon = System-Daemons\n"
                    "local0-local7 = benutzerdefinierte Facilities.\n"
                    "Severity: emerg > alert > crit > err > warning > notice > info > debug"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was bedeutet '*/5 * * * *' in einer Crontab?",
                options    = [
                    "Alle 5 Stunden",
                    "Alle 5 Minuten",
                    "Am 5. jedes Monats",
                    "Jeden 5. Wochentag",
                ],
                correct    = 1,
                explanation = (
                    "*/5 im Minuten-Feld = alle 5 Minuten.\n"
                    "Crontab-Format: Minute Stunde Tag Monat Wochentag Befehl\n"
                    "*/5 * * * * = jede 5. Minute | 0 * * * * = jede volle Stunde"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Wo liegen benutzer-spezifische Crontabs?",
                options    = [
                    "/etc/cron.d/",
                    "/var/spool/cron/crontabs/",
                    "/home/user/.crontab",
                    "/etc/crontabs/",
                ],
                correct    = 1,
                explanation = (
                    "/var/spool/cron/crontabs/ enthält Benutzer-Crontabs (benannt nach Username).\n"
                    "/etc/cron.d/ = System-Crontabs mit User-Angabe\n"
                    "crontab -e = Crontab des aktuellen Users editieren"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist der Vorteil von systemd-timer gegenüber cron?",
                options    = [
                    "Systemd-Timer sind schneller",
                    "Systemd-Timer sind in systemd integriert, haben Dependencies und journald-Logging",
                    "Systemd-Timer können keine Wildcards verwenden",
                    "Cron kann keine systemd-Units starten",
                ],
                correct    = 1,
                explanation = (
                    "systemd-Timer Vorteile: Integration mit systemd-Abhängigkeiten,\n"
                    "automatisches Logging via journald, Ausführung nach Boot-Verzögerung möglich.\n"
                    "systemctl list-timers zeigt alle aktiven Timer."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche Datei konfiguriert rsyslog?",
                options    = [
                    "/etc/syslog.conf",
                    "/etc/rsyslog.conf",
                    "/etc/log/rsyslog.conf",
                    "/var/log/rsyslog.conf",
                ],
                correct    = 1,
                explanation = (
                    "/etc/rsyslog.conf ist die Hauptkonfigurationsdatei von rsyslog.\n"
                    "/etc/rsyslog.d/*.conf = modulare Konfigurationen.\n"
                    "rsyslogd -N1 -f /etc/rsyslog.conf prüft die Konfiguration."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was macht 'journalctl --vacuum-size=500M'?",
                options    = [
                    "Reserviert 500 MB für Logs",
                    "Löscht alte Journal-Logs bis nur noch 500 MB übrig sind",
                    "Komprimiert alle Logs auf 500 MB",
                    "Begrenzt zukünftige Log-Größe auf 500 MB",
                ],
                correct    = 1,
                explanation = (
                    "--vacuum-size=500M entfernt alte Journal-Dateien bis die Gesamtgröße ≤500MB.\n"
                    "--vacuum-time=2weeks = Logs älter als 2 Wochen löschen.\n"
                    "/etc/systemd/journald.conf: SystemMaxUse= für dauerhafte Begrenzung."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl listet alle systemd-Timer an?",
                options    = [
                    "systemctl --type=timer",
                    "systemctl list-timers",
                    "systemctl show timers",
                    "timer list --all",
                ],
                correct    = 1,
                explanation = (
                    "systemctl list-timers zeigt alle Timer mit nächster/letzter Ausführung.\n"
                    "systemctl list-timers --all = auch inaktive Timer.\n"
                    "Jeder Timer braucht eine gleichnamige .service-Unit."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "journalctl -n/-f/-u | cron=*/5=alle5Min | /var/spool/cron/crontabs/ | rsyslog=/etc/rsyslog.conf",
        memory_tip   = "cron = Klassiker | systemd-timer = Modern mit Dependencies | journald = zentrales Logging",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.25 — Exam Block 25: Kernel & Hardware Deep
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.25",
        chapter      = 18,
        title        = "Exam Block 25 — Kernel & Hardware Deep",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 25. Kernel und Hardware.\n"
            " Module, /proc, sysctl, udev, dmesg.\n"
            " Das Herz des Systems — kenn es.'"
        ),
        why_important = "LPIC-1 Exam 101: Topics 101.1/101.2/102.6 — Kernel, Hardware & Modules",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: Kernel & Hardware Deep.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Welcher Befehl lädt ein Kernel-Modul mit allen Abhängigkeiten?",
                options    = ["insmod modul.ko", "modprobe modul", "lsmod --load modul", "modload modul"],
                correct    = 1,
                explanation = (
                    "modprobe lädt das Modul und alle Abhängigkeiten automatisch.\n"
                    "insmod lädt nur das angegebene Modul (keine Abhängigkeiten).\n"
                    "modprobe -r modul = Modul entladen (wie rmmod)."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was zeigt 'cat /proc/cpuinfo'?",
                options    = [
                    "CPU-Auslastung in Echtzeit",
                    "Detaillierte CPU-Informationen aus dem Kernel",
                    "CPU-Temperatur",
                    "CPU-Frequenz einstellen",
                ],
                correct    = 1,
                explanation = (
                    "/proc/cpuinfo enthält CPU-Modell, Kerne, Flags (Features), Cache-Größe.\n"
                    "grep 'model name' /proc/cpuinfo = CPU-Modell\n"
                    "grep -c '^processor' /proc/cpuinfo = Anzahl Kerne/Threads."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher sysctl-Parameter aktiviert IP-Forwarding?",
                options    = [
                    "sysctl net.ipv4.forward=1",
                    "sysctl net.ipv4.ip_forward=1",
                    "sysctl kernel.ip_forward=1",
                    "sysctl net.forward.ipv4=1",
                ],
                correct    = 1,
                explanation = (
                    "net.ipv4.ip_forward=1 aktiviert IPv4-Paketweiterleitung (Router-Funktion).\n"
                    "sysctl -w net.ipv4.ip_forward=1 = temporär\n"
                    "/etc/sysctl.conf oder /etc/sysctl.d/*.conf = dauerhaft"
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist udev?",
                options    = [
                    "Ein Texteditor für Kernel-Konfiguration",
                    "Der Userspace-Geräte-Manager der /dev-Einträge dynamisch erstellt",
                    "Ein Tool zum Laden von Kernel-Modulen",
                    "Ein Hardware-Monitoring-Daemon",
                ],
                correct    = 1,
                explanation = (
                    "udev verwaltet /dev dynamisch — erstellt und löscht Gerätedateien.\n"
                    "Verarbeitet Kernel-Ereignisse (uevent) via udev-Regeln.\n"
                    "udevadm monitor = Kernel/udev-Events verfolgen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was zeigt 'dmesg | tail -20'?",
                options    = [
                    "Die letzten 20 Zeilen der systemd-Logs",
                    "Die letzten 20 Kernel-Ring-Buffer-Meldungen",
                    "Die letzten 20 Boot-Meldungen aus /var/log/boot.log",
                    "Die letzten 20 Fehler aus /var/log/syslog",
                ],
                correct    = 1,
                explanation = (
                    "dmesg liest den Kernel-Ring-Buffer — Kernel-Meldungen seit Boot.\n"
                    "dmesg -T = menschenlesbare Timestamps.\n"
                    "dmesg | grep -i error = Fehler suchen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Wo werden Modul-Parameter dauerhaft konfiguriert?",
                options    = [
                    "/etc/modules",
                    "/etc/modprobe.d/*.conf",
                    "/proc/modules",
                    "/sys/module/",
                ],
                correct    = 1,
                explanation = (
                    "/etc/modprobe.d/*.conf enthält Modul-Optionen und Aliases.\n"
                    "options modul_name param=wert\n"
                    "/etc/modules = Module die beim Boot geladen werden sollen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welcher Befehl zeigt Hardware-Informationen aus dem BIOS/UEFI?",
                options    = [
                    "lshw --bios",
                    "dmidecode",
                    "hwinfo --bios",
                    "biosinfo",
                ],
                correct    = 1,
                explanation = (
                    "dmidecode liest SMBIOS/DMI-Daten und zeigt BIOS, RAM, CPU, System-Infos.\n"
                    "dmidecode -t memory = RAM-Infos\n"
                    "dmidecode -t bios = BIOS-Version und -Hersteller."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was enthält /proc/meminfo?",
                options    = [
                    "Speicher-Auslastung von Prozessen",
                    "Detaillierte Speicher-Statistiken des Kernels",
                    "Swap-Partition-Konfiguration",
                    "Physische RAM-Module-Informationen",
                ],
                correct    = 1,
                explanation = (
                    "/proc/meminfo zeigt MemTotal, MemFree, MemAvailable, Buffers, Cached etc.\n"
                    "free -h liest /proc/meminfo und zeigt es übersichtlich.\n"
                    "MemAvailable = tatsächlich verfügbarer RAM (besser als MemFree)."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "modprobe=mit Deps | insmod=ohne Deps | sysctl=Kernel-Parameter | udev=dynamisch /dev | dmesg=Kernel-Log",
        memory_tip   = "/proc = Kernel-Schnittstelle | /sys = Kernel-Objekte | udev = /dev-Manager",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.26 — Exam Block 26: Shell Scripting Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.26",
        chapter      = 18,
        title        = "Exam Block 26 — Shell Scripting Advanced",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Block 26. Letzter Block vor dem Boss.\n"
            " Shell Scripting Advanced: Arrays, Funktionen, Fehlerbehandlung, getopts.\n"
            " Das ist das Finale. Zeig alles was du weißt.'"
        ),
        why_important = "LPIC-1 Exam 102: Topic 105.2 — Customize or Write Shell Scripts",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "8 Prüfungsfragen: Shell Scripting Advanced.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question   = "Was macht 'set -euo pipefail' am Anfang eines Skripts?",
                options    = [
                    "Aktiviert Debug-Modus",
                    "Beendet bei Fehler (-e), meldet ungesetzte Variablen (-u), propagiert Pipeline-Fehler (pipefail)",
                    "Startet Skript im sicheren Modus",
                    "Deaktiviert alle Fehlerbehandlung",
                ],
                correct    = 1,
                explanation = (
                    "set -e = errexit (bei Fehler beenden)\n"
                    "set -u = nounset (ungesetzte Variable = Fehler)\n"
                    "set -o pipefail = Pipeline-Fehler propagieren\n"
                    "Diese Kombination ist Best Practice für robuste Skripte."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Wie verarbeitet man Kommandozeilen-Optionen in einem Bash-Skript?",
                options    = [
                    "Mit dem parseargs-Befehl",
                    "Mit getopts",
                    "Mit argparse",
                    "Mit optparse",
                ],
                correct    = 1,
                explanation = (
                    "getopts ist das POSIX-konforme Tool für kurze Optionen (-a, -b, -c).\n"
                    "while getopts 'abc:' opt; do case $opt in ...; done\n"
                    "getopt (ohne s) unterstützt auch lange Optionen (--help)."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist der Exit-Code 0 in einem Shell-Skript?",
                options    = [
                    "Fehler",
                    "Erfolg",
                    "Abbruch durch Signal",
                    "Unbekannter Status",
                ],
                correct    = 1,
                explanation = (
                    "Exit-Code 0 = Erfolg (true).\n"
                    "Exit-Code 1-255 = Fehler (1 = allgemeiner Fehler, 127 = Befehl nicht gefunden).\n"
                    "$? = letzter Exit-Code | exit 0 = sauberes Beenden."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Wie übergibt man alle Array-Elemente sicher an eine Funktion?",
                options    = [
                    'funktion $array',
                    'funktion "${array[@]}"',
                    'funktion ${array[*]}',
                    'funktion $(echo $array)',
                ],
                correct    = 1,
                explanation = (
                    '"${array[@]}" übergibt jeden Element als separates Wort (mit Anführungszeichen).\n'
                    'Korrekt bei Elementen mit Leerzeichen.\n'
                    '${array[*]} ohne Quotes = unsicher, ${array[@]} ohne Quotes = word-splitting.'
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was bewirkt 'trap cleanup EXIT' in einem Skript?",
                options    = [
                    "Fängt Ctrl+C ab",
                    "Führt 'cleanup' aus wenn das Skript beendet wird (normal oder Fehler)",
                    "Deaktiviert alle Signale",
                    "Loggt alle Befehle",
                ],
                correct    = 1,
                explanation = (
                    "trap befehl SIGNAL führt 'befehl' aus wenn das Signal eintrifft.\n"
                    "EXIT = beim Beenden (immer). INT = Ctrl+C. TERM = kill.\n"
                    "Typisch für Cleanup-Funktionen: temporäre Dateien löschen."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was macht 'local' in einer Shell-Funktion?",
                options    = [
                    "Macht die Variable global",
                    "Beschränkt den Gültigkeitsbereich der Variable auf die Funktion",
                    "Exportiert die Variable",
                    "Macht die Variable read-only",
                ],
                correct    = 1,
                explanation = (
                    "local var=wert erstellt eine Variable die nur in der Funktion sichtbar ist.\n"
                    "Verhindert versehentliches Überschreiben globaler Variablen.\n"
                    "local ist nur innerhalb von Funktionen gültig."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Welche Shebang-Zeile ist am portabelsten für bash-Skripte?",
                options    = [
                    "#!/bin/bash",
                    "#!/usr/bin/env bash",
                    "#!/bin/sh -e",
                    "#!bash",
                ],
                correct    = 1,
                explanation = (
                    "#!/usr/bin/env bash findet bash über den PATH — portabler als #!/bin/bash\n"
                    "da bash nicht immer in /bin liegt (z.B. auf macOS: /usr/local/bin/bash).\n"
                    "#!/bin/sh = POSIX-Shell, kein bash-spezifisches Verhalten."
                ),
                xp_value   = 20,
            ),
            QuizQuestion(
                question   = "Was ist Prozess-Substitution in bash?",
                options    = [
                    "$(befehl) = Command Substitution",
                    "<(befehl) = Prozess-Ausgabe als Datei behandeln",
                    "> befehl = Ausgabe umleiten",
                    "| befehl = Pipe",
                ],
                correct    = 1,
                explanation = (
                    "<(befehl) = Prozess-Substitution: Ausgabe als temporäre Datei bereitgestellt.\n"
                    "diff <(sort datei1) <(sort datei2) = sortierte Dateien vergleichen.\n"
                    "Nur in bash, nicht POSIX sh."
                ),
                xp_value   = 20,
            ),
        ],
        exam_tip     = "set -euo pipefail = Best Practice | getopts = Optionen | trap EXIT = Cleanup | local = Scope",
        memory_tip   = "Shell Scripting: -e=exit, -u=unset, -o pipefail=Pipeline | getopts=Optionen parsen",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 18.BOSS — FINAL EXAM — LPIC-1 CERTIFICATION
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "18.boss",
        chapter      = 18,
        title        = "BOSS: FINAL EXAM — LPIC-1 CERTIFICATION",
        mtype        = "BOSS",
        xp           = 625,
        speaker      = "EXAMINATOR",
        story        = (
            "EXAMINATOR: 'Ghost. Du hast 17 Kapitel durchkämpft.\n"
            " 60 Prüfungsfragen beantwortet.\n"
            " Du kennst Hardware, Boot, Dateisysteme, Prozesse,\n"
            " Netzwerk, Benutzer, Logs, Scripting, Sicherheit.\n"
            " Das ist NeonGrid-9. Das ist LPIC-1.\n"
            " Eine letzte Frage — die härteste.\n"
            " Beweise, dass du bereit bist.'"
        ),
        why_important = (
            "LPIC-1 ist der weltweit anerkannte Einstiegs-Zertifizierungsstandard\n"
            "für Linux-Systemadministration. 2 Prüfungen: 101 und 102.\n"
            "Je 60 Minuten, ~60 Fragen, 500/800 Punkte zum Bestehen (62.5%)."
        ),
        explanation  = (
            "LPIC-1 Prüfungs-Überblick:\n"
            "\n"
            "Exam 101 (LPI-101):\n"
            "  Topic 101: Systemarchitektur (Hardware, Boot, Kernel)\n"
            "  Topic 102: Linux-Installation & Paketverwaltung\n"
            "  Topic 103: GNU & Unix-Befehle (Shell, Pipes, Prozesse)\n"
            "  Topic 104: Geräte, Dateisysteme, FHS\n"
            "\n"
            "Exam 102 (LPI-102):\n"
            "  Topic 105: Shells & Scripting\n"
            "  Topic 106: User Interfaces & Desktops (X11, CUPS)\n"
            "  Topic 107: Administrative Aufgaben (User, Cron, Locale)\n"
            "  Topic 108: Systemdienste (Boot, Logs, Zeit, Drucker)\n"
            "  Topic 109: Netzwerkgrundlagen\n"
            "  Topic 110: Sicherheit\n"
            "\n"
            "Bestehenskriterium: 500 von 800 Punkten (62.5%)\n"
            "Prüfungsdauer: 90 Minuten je Exam\n"
            "Fragen-Typen: Multiple Choice, Fill-in, Multiple Answer\n"
            "\n"
            "Prüfungs-Anmeldung: lpi.org\n"
            "Gültigkeitsdauer: 5 Jahre"
        ),
        ascii_art    = """
  ███████╗██╗  ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗
  ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
  █████╗   ╚███╔╝ ███████║██╔████╔██║██║██╔██╗ ██║███████║   ██║   ██║   ██║██████╔╝
  ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██║   ██║██╔══██╗
  ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ╚██████╔╝██║  ██║
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

  ┌─ EXAM STATUS ────────────────────────────────┐
  │  LPI-101: PENDING    ::  LPI-102: PENDING    │
  │  17 Chapters: CLEARED ::  XP: MAXIMUM       │
  │  Score Target: 500/800  ::  LPIC-1: AWAITS  │
  └──────────────────────────────────────────────┘

  ⚡ CHAOSWERK FACTION :: CHAPTER 18 FINAL BOSS ⚡""",
        story_transitions = [
            "EXAMINATOR lädt die härtesten Fragen. Du hast alles gelernt.",
            "17 Kapitel. 500 Missionen. Ein Ziel: LPIC-1 bestehen.",
            "Zara sieht zu. Das gesamte NeonGrid-9 hält den Atem an.",
            "Eine Frage. Die letzte. Deine Antwort entscheidet alles.",
        ],
        syntax       = "# Lern-Reihenfolge für echte Prüfung:",
        example      = "# lpi.org → Candidate → Register → Exam 101 → Exam 102",
        task_description = (
            "FINALE PRÜFUNG: Eine letzte Frage.\n"
            "Zeige deine LPIC-1 Bereitschaft.\n"
            "Führe 'uname -a' aus — das Fundament von allem."
        ),
        expected_commands = ["uname -a"],
        hint_text    = "uname -a zeigt alle Systeminformationen — Kernel, Host, Arch",
        quiz_questions = [
            QuizQuestion(
                question    = "Wie viele Punkte braucht man zum Bestehen einer LPIC-1-Prüfung?",
                options     = ["400 von 800", "500 von 800 (62,5%)", "600 von 800", "700 von 800"],
                correct     = 1,
                explanation = "LPIC-1 Bestehenskriterium: 500 von 800 Punkten (62,5%).\nJede der zwei Prüfungen (LPI-101 und LPI-102) muss einzeln bestanden werden.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Welche Topics deckt LPIC-1 Exam 101 (LPI-101) ab?",
                options     = ["Topics 101-104 (Systemarchitektur, Installation, Befehle, Geräte)", "Topics 105-110 (Shells, Desktop, Admin, Dienste, Netz, Sicherheit)", "Alle Topics 101-110", "Nur Networking und Security"],
                correct     = 0,
                explanation = "LPI-101: Topics 101-104 (Hardware, Boot, Linux-Installation, Pakete, Befehle, Dateisysteme).\nLPI-102: Topics 105-110 (Shells, Desktop, Admin, Dienste, Netzwerk, Sicherheit).",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Was zeigt 'uname -r'?",
                options     = ["Root-Verzeichnis", "Kernel-Release (Versionsnummer)", "Hostname", "Architektur"],
                correct     = 1,
                explanation = "uname -r = Kernel-Release (z.B. 6.1.0-debian).\nuname -s = Kernel-Name | uname -m = Maschinenarchitektur | uname -a = alles.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Auf der LPIC-1-Prüfung bekommst du eine Frage über einen Befehl den du nicht kennst. Was ist die beste Strategie?",
                options     = [
                    "Eliminierung falscher Antworten: man-page-Konventionen, bekannte Flag-Muster (-v verbose, -r recursive, -n dry-run) und Ausschluss offensichtlicher Fallen nutzen",
                    "Immer die längste Antwort wählen",
                    "Die mittlere Option ist statistisch am häufigsten korrekt",
                    "Frage überspringen und am Ende zurückkehren",
                ],
                correct     = 0,
                explanation = "Eliminierung ist die stärkste Test-Strategie: Falsche Flags ausschließen, POSIX-Konventionen anwenden. Auf LPIC-1 gibt es keine Punktabzüge — immer eine Antwort geben. Option C (mittlere) ist ein Mythos.",
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "Welche LPIC-1 Topic-Nummer deckt 'Grundlegende Dateiverwaltung' (ls, cp, mv, find, file) ab?",
                options     = [
                    "Topic 103.3",
                    "Topic 104.2",
                    "Topic 101.1",
                    "Topic 102.4",
                ],
                correct     = 0,
                explanation = "Topic 103.3 'Perform basic file management' deckt ls, cp, mv, rm, mkdir, find, file, dd ab. Topic 104.x = Filesysteme. Topic 101.x = Hardware/Architektur. Topic 102.x = Linux-Installation.",
                xp_value    = 30,
            ),
        ],
        exam_tip     = "LPIC-1: 2 Prüfungen (101+102) | je 90 Min | 500/800 Punkte | lpi.org anmelden",
        memory_tip   = "NeonGrid-9 deckt alle LPIC-1 v5.0 Topics ab — du bist bereit.",
        gear_reward  = "lpic1_badge",
        faction_reward = ("Kernel Syndicate", 100),
    ),
]
