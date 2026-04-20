"""
NeonGrid-9 :: Kapitel 15 — SECURITY PROTOCOL
LPIC-1 Topic 110.1 / 110.2 / 110.3
Sicherheit: GPG, SSH-Härtung, fail2ban, sudo, Dateiverschlüsselung, find-SUID

"In NeonGrid-9 schläft die Bedrohung nie.
 Jeder offene Port ist eine Einladung.
 Jeder SUID-Bit eine Waffe.
 Härte dein System — oder jemand anderes tut es für dich."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_15_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 15.01 — Sicherheitslücken finden: find SUID/SGID
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.01",
        chapter      = 15,
        title        = "SUID/SGID-Jäger",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Ghost. Jemand hat SUID-Bits auf Binaries gesetzt,\n"
            " die das nicht brauchen. Das ist eine offene Hintertür.\n"
            " Finde alle SUID-Dateien im System — bevor die Gegner sie nutzen.'"
        ),
        why_important = (
            "SUID (Set User ID) und SGID (Set Group ID) lassen Programme mit\n"
            "erhöhten Rechten laufen. Falsch gesetzte SUID-Bits auf editierbaren\n"
            "Binaries sind klassische Privilege-Escalation-Vektoren."
        ),
        explanation  = (
            "find / -perm -4000  → alle SUID-Dateien (laufen als Eigentümer)\n"
            "find / -perm -2000  → alle SGID-Dateien (laufen als Gruppe)\n"
            "find / -perm /6000  → SUID oder SGID (OR-Verknüpfung)\n"
            "find / -perm -4000 -type f  → nur reguläre Dateien\n"
            "Bekannte legitime SUID: /usr/bin/sudo /usr/bin/passwd /usr/bin/su\n"
            "Verdächtig: Editoren, Shell-Interpreter, cp, find, vim mit SUID!"
        ),
        syntax       = "find / -perm -4000 -type f 2>/dev/null",
        example      = "find / -perm /6000 -type f -ls 2>/dev/null",
        task_description = "Suche alle SUID-Dateien im System.",
        expected_commands = ["find / -perm -4000 -type f 2>/dev/null"],
        hint_text    = "find / -perm -4000 — -4000 bedeutet SUID-Bit gesetzt",
        quiz_questions = [],
        exam_tip     = "find / -perm -4000 (SUID) vs -perm -2000 (SGID) vs -perm /6000 (beides)",
        memory_tip   = "SUID=4000 SGID=2000 — wie chmod-Oktalen: 4=SUID 2=SGID 1=Sticky",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.02 — SSH-Härtung: sshd_config
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.02",
        chapter      = 15,
        title        = "SSH-Härtung — sshd_config",
        mtype        = "INFILTRATE",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'SSH mit Root-Login und Passwort-Auth — das ist\n"
            " kein Server, das ist ein Einladungsschild.\n"
            " Schließ die Türen. Nur Key-Auth. Root raus. Port wechseln.\n"
            " Zeig mir die aktuelle SSH-Konfiguration.'"
        ),
        why_important = (
            "SSH ist der häufigste Angriffsvektor auf Linux-Server.\n"
            "PermitRootLogin no, PasswordAuthentication no und ein\n"
            "nicht-standardmäßiger Port reduzieren Brute-Force-Angriffe massiv."
        ),
        explanation  = (
            "/etc/ssh/sshd_config — Haupt-Konfigurationsdatei des SSH-Daemons\n"
            "Wichtige Direktiven:\n"
            "  Port 2222              → Nicht-Standard-Port (kein Schutz, aber weniger Lärm)\n"
            "  PermitRootLogin no     → Root-SSH verbieten (MUSS!)\n"
            "  PermitRootLogin prohibit-password  → Root nur mit Key (Alias: without-password)\n"
            "  PasswordAuthentication no → Nur Key-Auth erlauben\n"
            "  PubkeyAuthentication yes  → Key-Auth aktiv\n"
            "  MaxAuthTries 3            → Max. 3 Versuche pro Verbindung\n"
            "  AllowUsers ghost admin    → Nur diese User dürfen sich einloggen\n"
            "  ClientAliveInterval 300   → Timeout nach 300s Inaktivität\n"
            "  X11Forwarding no          → Keine X11-Weiterleitung\n"
            "Nach Änderung: systemctl restart sshd / sshd -t (Syntax-Check)"
        ),
        syntax       = "cat /etc/ssh/sshd_config | grep -v '^#' | grep -v '^$'",
        example      = "sshd -t  # Syntax-Check ohne Neustart",
        task_description = "Zeige die aktive SSH-Konfiguration an.",
        expected_commands = ["cat /etc/ssh/sshd_config"],
        hint_text    = "Die SSH-Daemon-Konfiguration liegt in /etc/ssh/sshd_config",
        quiz_questions = [],
        exam_tip     = "PermitRootLogin no + PasswordAuthentication no = SSH-Grundhärtung | prohibit-password (Alias: without-password)",
        memory_tip   = "sshd_config = Server-Config | ssh_config = Client-Config",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.03 — GPG: Schlüssel erzeugen & Dateien verschlüsseln
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.03",
        chapter      = 15,
        title        = "GPG — Verschlüsselung & Signaturen",
        mtype        = "DECODE",
        xp           = 110,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Die Nachricht wurde abgefangen, Ghost.\n"
            " Aber sie konnten sie nicht lesen — GPG-verschlüsselt.\n"
            " Lern GPG. Asymmetrische Kryptographie ist dein Schutzschild\n"
            " in einem Netz voller Augen.'"
        ),
        why_important = (
            "GPG (GNU Privacy Guard) implementiert OpenPGP-Standard.\n"
            "Wird für Dateiverschlüsselung, E-Mail-Signierung und\n"
            "Paketverifikation (apt-key, RPM) eingesetzt."
        ),
        explanation  = (
            "gpg --gen-key                     → Schlüsselpaar erzeugen\n"
            "gpg --list-keys                   → Öffentliche Schlüssel anzeigen\n"
            "gpg --list-secret-keys            → Private Schlüssel anzeigen\n"
            "gpg --export -a 'Name' > pub.asc  → Public Key exportieren (ASCII)\n"
            "gpg --import pub.asc              → Public Key importieren\n"
            "gpg -e -r 'Empfänger' datei.txt   → Verschlüsseln (encrypt)\n"
            "gpg -d datei.txt.gpg              → Entschlüsseln (decrypt)\n"
            "gpg --sign datei.txt              → Datei signieren\n"
            "gpg --verify datei.txt.sig        → Signatur prüfen\n"
            "gpg --fingerprint 'Name'          → Key-Fingerprint anzeigen\n"
            "gpg --symmetric datei.txt         → Symmetrisch (Passwort) verschlüsseln"
        ),
        syntax       = "gpg --list-keys",
        example      = "gpg -e -r 'ghost@neongrid.net' geheimbotschaft.txt",
        task_description = "Liste alle GPG-Schlüssel im Keyring auf.",
        expected_commands = ["gpg --list-keys"],
        hint_text    = "gpg --list-keys zeigt alle öffentlichen Schlüssel im lokalen Keyring",
        quiz_questions = [],
        exam_tip     = "gpg -e = encrypt | gpg -d = decrypt | gpg --sign = signieren | gpg --verify = prüfen",
        memory_tip   = "GPG: -e encrypt -d decrypt — wie 'encode/decode' rückwärts",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.04 — fail2ban & Brute-Force-Schutz
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.04",
        chapter      = 15,
        title        = "fail2ban — Brute-Force-Schutz",
        mtype        = "REPAIR",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Ghost! 47.000 SSH-Login-Versuche in einer Stunde.\n"
            " Dieselbe IP. Das ist ein Brute-Force-Angriff.\n"
            " fail2ban überwacht Logs und bannt Angreifer automatisch.\n"
            " Aktiviere es — jetzt.'"
        ),
        why_important = (
            "fail2ban liest Log-Dateien, erkennt Muster (z.B. fehlgeschlagene\n"
            "Logins) und blockiert Quell-IPs via iptables/firewalld.\n"
            "Essentiell für jeden öffentlich erreichbaren Server."
        ),
        explanation  = (
            "fail2ban Konzepte:\n"
            "  Jail    = Überwachungsregel (z.B. ssh, apache, nginx)\n"
            "  Filter  = Log-Muster (Regex) zum Erkennen von Angriffen\n"
            "  Action  = Was passiert bei Treffer (Ban via iptables)\n"
            "\n"
            "Konfiguration:\n"
            "  /etc/fail2ban/jail.conf        → Default-Konfiguration\n"
            "  /etc/fail2ban/jail.local       → Eigene Überschreibungen (hier editieren!)\n"
            "  /etc/fail2ban/filter.d/        → Filter-Definitionen\n"
            "  /etc/fail2ban/action.d/        → Aktions-Definitionen\n"
            "\n"
            "Wichtige Direktiven in jail.local:\n"
            "  [sshd]\n"
            "  enabled  = true\n"
            "  maxretry = 3\n"
            "  bantime  = 3600\n"
            "  findtime = 600\n"
            "\n"
            "Verwaltung:\n"
            "  fail2ban-client status          → Alle Jails anzeigen\n"
            "  fail2ban-client status sshd     → Status des SSH-Jails\n"
            "  fail2ban-client set sshd unbanip 1.2.3.4 → IP entbannen\n"
            "  fail2ban-client banned          → Alle gebannten IPs"
        ),
        syntax       = "fail2ban-client status sshd",
        example      = "fail2ban-client set sshd unbanip 192.168.1.100",
        task_description = "Zeige den Status des fail2ban SSH-Jails.",
        expected_commands = ["fail2ban-client status sshd"],
        hint_text    = "fail2ban-client status sshd — zeigt aktive Bans und Statistiken",
        quiz_questions = [],
        exam_tip     = "jail.local überschreibt jail.conf — eigene Konfiguration immer in jail.local",
        memory_tip   = "fail2ban: find(time) → max(retry) erreicht → ban(time) — drei Parameter",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.05 — sudo & sudoers: Rechtevergabe
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.05",
        chapter      = 15,
        title        = "sudo & sudoers — Rechtevergabe",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0: 'Der neue Operator braucht Deployment-Rechte,\n"
            " aber keinen vollen Root-Zugang.\n"
            " sudo mit präzisen Regeln ist die Antwort.\n"
            " Gib ihm genau das was er braucht — nicht mehr.'"
        ),
        why_important = (
            "Principle of Least Privilege: Nutzer erhalten nur die Rechte,\n"
            "die sie tatsächlich benötigen. sudoers erlaubt granulare Kontrolle\n"
            "bis auf einzelne Befehle, Hosts und Tageszeiten."
        ),
        explanation  = (
            "sudoers-Syntax: WHO HOST=(RUNAS) COMMANDS\n"
            "\n"
            "Beispiele:\n"
            "  ghost ALL=(ALL) ALL              → ghost darf alles als root\n"
            "  ghost ALL=(ALL) NOPASSWD: ALL    → ohne Passwort\n"
            "  ghost ALL=(ALL) /usr/bin/systemctl restart nginx  → nur nginx restart\n"
            "  %admin ALL=(ALL) ALL             → Gruppe admin\n"
            "  ghost ALL=(www-data) /usr/bin/php  → als www-data ausführen\n"
            "\n"
            "Wichtige Befehle:\n"
            "  visudo              → sudoers sicher editieren (Syntax-Check!)\n"
            "  sudo -l             → eigene sudo-Rechte anzeigen\n"
            "  sudo -l -U ghost    → sudo-Rechte von User ghost anzeigen\n"
            "  sudo -u www-data id → Befehl als anderer User\n"
            "\n"
            "Includes:\n"
            "  #includedir /etc/sudoers.d/     → Fragmentdateien\n"
            "  Eigene Regeln nach /etc/sudoers.d/99-ghost"
        ),
        syntax       = "visudo",
        example      = "sudo -l  # Zeige eigene sudo-Rechte",
        task_description = "Zeige deine eigenen sudo-Rechte an.",
        expected_commands = ["sudo -l"],
        hint_text    = "sudo -l listet alle erlaubten und verbotenen sudo-Befehle auf",
        quiz_questions = [],
        exam_tip     = "visudo = sudo-sicherer Editor | sudo -l = Rechte anzeigen | %gruppe = Gruppe in sudoers",
        memory_tip   = "sudoers: WHO WHERE=(AS_WHOM) WHAT — vier Felder",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.06 — Dateiverschlüsselung: openssl & cryptsetup
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.06",
        chapter      = 15,
        title        = "openssl & LUKS — Dateiverschlüsselung",
        mtype        = "DECODE",
        xp           = 100,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Die Festplatte des Agenten wurde konfisziert.\n"
            " Aber die Daten sind LUKS-verschlüsselt.\n"
            " Ohne Passphrase: Datenschrott.\n"
            " Lern openssl für Dateien, LUKS für ganze Partitionen.'"
        ),
        why_important = (
            "openssl verschlüsselt einzelne Dateien symmetrisch oder asymmetrisch.\n"
            "LUKS (Linux Unified Key Setup) verschlüsselt Block-Devices (Partitionen,\n"
            "USB-Sticks) transparent — Standard für Festplattenverschlüsselung."
        ),
        explanation  = (
            "openssl (Dateien):\n"
            "  openssl enc -aes-256-cbc -in datei.txt -out datei.enc\n"
            "    → AES-256-CBC Verschlüsselung\n"
            "  openssl enc -d -aes-256-cbc -in datei.enc -out datei.txt\n"
            "    → Entschlüsseln (-d = decrypt)\n"
            "  openssl dgst -sha256 datei.txt\n"
            "    → SHA-256 Prüfsumme\n"
            "  openssl rand -base64 32\n"
            "    → 32 Byte Zufallspasswort (Base64)\n"
            "\n"
            "LUKS (Block-Device-Verschlüsselung):\n"
            "  cryptsetup luksFormat /dev/sdb1       → LUKS-Container erstellen\n"
            "  cryptsetup luksOpen /dev/sdb1 geheim  → Container öffnen → /dev/mapper/geheim\n"
            "  mkfs.ext4 /dev/mapper/geheim          → Formatieren\n"
            "  mount /dev/mapper/geheim /mnt          → Einhängen\n"
            "  cryptsetup luksClose geheim           → Container schließen\n"
            "  cryptsetup luksDump /dev/sdb1         → LUKS-Header-Info\n"
            "  /etc/crypttab → automatisches Öffnen beim Boot"
        ),
        syntax       = "openssl enc -aes-256-cbc -in datei.txt -out datei.enc",
        example      = "openssl dgst -sha256 /etc/passwd",
        task_description = "Erstelle eine SHA-256-Prüfsumme von /etc/passwd.",
        expected_commands = ["openssl dgst -sha256 /etc/passwd"],
        hint_text    = "openssl dgst -sha256 DATEI — berechnet SHA-256 Prüfsumme",
        quiz_questions = [],
        exam_tip     = "LUKS: luksFormat → luksOpen → (mkfs) → mount | luksClose zum Schließen",
        memory_tip   = "openssl enc -d = decrypt | openssl enc (ohne -d) = encrypt",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.07 — Netzwerk-Sicherheit: nmap, netstat, iptables
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.07",
        chapter      = 15,
        title        = "Netzwerk-Härtung — offene Ports & Firewall",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Vor der Verteidigung kommt das Audit.\n"
            " Welche Ports lauschen? Welche Services sind exponiert?\n"
            " nmap ist der Blick von außen.\n"
            " ss und iptables sind die Kontrolle von innen.'"
        ),
        why_important = (
            "Sicherheits-Audit: Jeder lauschende Port ist eine potenzielle\n"
            "Angriffsfläche. Minimierung offener Ports, korrekte Firewall-Regeln\n"
            "und regelmäßige Überprüfung sind Grundlagen der Systemhärtung."
        ),
        explanation  = (
            "Port-Scan & Audit:\n"
            "  nmap -sV localhost          → Service-Erkennung auf lokalem System\n"
            "  nmap -sS -O target          → SYN-Scan + OS-Erkennung\n"
            "  ss -tulpn                   → Lauschende Ports (aus Sicht des Systems)\n"
            "  netstat -tulpn              → Alternativ (älteres Tool)\n"
            "\n"
            "iptables (Firewall):\n"
            "  iptables -L -n -v           → Regeln anzeigen (numerisch, verbose)\n"
            "  iptables -A INPUT -p tcp --dport 22 -j ACCEPT  → SSH erlauben\n"
            "  iptables -A INPUT -j DROP   → Alles andere blockieren\n"
            "  iptables -I INPUT 1 ...     → Regel an Position 1 einfügen\n"
            "  iptables -D INPUT 3         → Regel 3 löschen\n"
            "  iptables-save > /etc/iptables/rules.v4  → Regeln speichern\n"
            "  iptables-restore < /etc/iptables/rules.v4  → Regeln laden\n"
            "\n"
            "Chains: INPUT (eingehend) | OUTPUT (ausgehend) | FORWARD (weitergeleitet)\n"
            "Policies: ACCEPT | DROP | REJECT\n"
            "Targets: ACCEPT | DROP | REJECT | LOG | MASQUERADE"
        ),
        syntax       = "iptables -L -n -v",
        example      = "ss -tulpn | grep LISTEN",
        task_description = "Zeige alle Firewall-Regeln mit iptables.",
        expected_commands = ["iptables -L -n -v"],
        hint_text    = "iptables -L -n -v — List all rules, numeric, verbose",
        quiz_questions = [],
        exam_tip     = "iptables Chains: INPUT=eingehend OUTPUT=ausgehend FORWARD=weitergeleitet",
        memory_tip   = "iptables -A = append (hinten) | -I = insert (vorne/Position) | -D = delete",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.08 — nftables Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.08",
        chapter      = 15,
        title        = "nftables Grundlagen",
        mtype        = "SCAN",
        xp           = 95,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Ghost. iptables ist Geschichte.\n"
            " Debian 10, Ubuntu 20.04, RHEL 8 — alle haben auf nftables gewechselt.\n"
            " Ein modernes Firewall-Framework. Atomar. Einheitlich.\n"
            " Zeig mir das aktuelle Ruleset — bevor wir anfangen, es umzubauen.'"
        ),
        why_important = (
            "nftables ist der moderne Nachfolger von iptables auf Debian 10+,\n"
            "Ubuntu 20.04+ und RHEL 8+. Es vereint ip/ip6/arp/bridge-Tables in\n"
            "einem einzigen Framework und ermöglicht atomare Regelaktualisierungen\n"
            "ohne Race Conditions. LPIC-1 Topic 110.1 testet grundlegendes Wissen."
        ),
        explanation  = (
            "nftables Grundkonzepte:\n"
            "  nft list ruleset          → Gesamtes aktives Regelwerk anzeigen\n"
            "  nft list tables           → Alle Tables anzeigen\n"
            "  nft add rule inet filter input tcp dport 22 accept\n"
            "                            → Regel hinzufügen\n"
            "  nft delete rule inet filter input handle 5\n"
            "                            → Regel anhand Handle löschen\n"
            "\n"
            "Konfigurationsdatei: /etc/nftables.conf\n"
            "  → Persistente Regeln; wird beim Boot via systemd geladen\n"
            "\n"
            "Vorteile gegenüber iptables:\n"
            "  • Vereint ip/ip6/arp/bridge-Tables in einem Framework\n"
            "  • Atomare Updates: Regeländerungen werden atomar angewendet\n"
            "  • Effizientere Syntax, weniger Redundanz\n"
            "  • Sets und Maps: Gruppen von Adressen/Ports in einer Regel\n"
            "\n"
            "Kernstruktur: Table → Chain → Rule\n"
            "  nft add table inet filter\n"
            "  nft add chain inet filter input { type filter hook input priority 0\\; }\n"
            "  nft add rule  inet filter input tcp dport 80 accept"
        ),
        syntax       = "nft list ruleset",
        example      = "nft list tables",
        task_description = "Zeige das gesamte aktive nftables-Ruleset an.",
        expected_commands = ["nft list ruleset"],
        hint_text    = "nft list ruleset — zeigt alle Tables, Chains und Rules auf einmal",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl zeigt das gesamte aktive nftables-Regelwerk an?",
                options  = [
                    "nft show all",
                    "nft list ruleset",
                    "nftables -L -n -v",
                    "nft dump tables",
                ],
                correct  = 1,
                explanation = (
                    "nft list ruleset zeigt alle Tables, Chains und Rules des aktiven Regelwerks.\n"
                    "Äquivalent zu iptables -L -n -v, aber für das gesamte nftables-Framework.\n"
                    "nft list tables zeigt nur die Table-Namen ohne Chains/Rules."
                ),
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In welcher Datei werden persistente nftables-Regeln gespeichert?",
                options  = [
                    "/etc/iptables/rules.v4",
                    "/etc/firewall/nftables.rules",
                    "/etc/nftables.conf",
                    "/var/lib/nftables/rules",
                ],
                correct  = 2,
                explanation = (
                    "/etc/nftables.conf ist die Standard-Konfigurationsdatei für persistente nftables-Regeln.\n"
                    "Sie wird via systemd-Service nftables.service beim Boot geladen.\n"
                    "/etc/iptables/rules.v4 gehört zu iptables, nicht nftables."
                ),
                xp_value = 15,
            ),
        ],
        exam_tip     = "nft list ruleset (alles) | nft list tables (nur Tables) | /etc/nftables.conf (persistent)",
        memory_tip   = "nft = New Firewall Tool — Table → Chain → Rule, atomar und einheitlich",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.09 — nftables Regeln schreiben
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.09",
        chapter      = 15,
        title        = "nftables Regeln schreiben",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Das Ruleset steht. Jetzt bauen wir es aus.\n"
            " Port 22 muss offen sein — aber nur gezielt, nur sauber.\n"
            " nftables-Syntax ist präziser als iptables.\n"
            " Schreib die Regel. Versteh die Hierarchie.'"
        ),
        why_important = (
            "Das Schreiben präziser Firewall-Regeln ist eine Kernkompetenz der\n"
            "Systemhärtung. Die nftables-Hierarchie Table/Chain/Rule zu verstehen\n"
            "und den Unterschied zu iptables zu kennen, ist LPIC-1-Prüfungsstoff."
        ),
        explanation  = (
            "nftables Table/Chain/Rule-Hierarchie:\n"
            "  Table  = Namensraum (z.B. 'inet filter' für IPv4+IPv6)\n"
            "  Chain  = Verarbeitungssequenz (z.B. 'input', 'forward', 'output')\n"
            "  Rule   = Einzelne Match+Action (z.B. tcp dport 22 accept)\n"
            "\n"
            "Regel hinzufügen:\n"
            "  nft add rule inet filter input tcp dport 22 accept\n"
            "    → SSH-Port erlauben in Tabelle inet, Chain input\n"
            "\n"
            "Vergleich mit iptables-Äquivalent:\n"
            "  iptables -A INPUT -p tcp --dport 22 -j ACCEPT\n"
            "  nft add rule inet filter input tcp dport 22 accept\n"
            "\n"
            "Weitere nftables-Beispiele:\n"
            "  nft add rule inet filter input ip saddr 192.168.1.0/24 accept\n"
            "  nft add rule inet filter input tcp dport { 80, 443 } accept\n"
            "  nft add rule inet filter input ct state established,related accept\n"
            "  nft add rule inet filter input drop\n"
            "\n"
            "Handle ermitteln (zum Löschen):\n"
            "  nft list ruleset -a      → zeigt Handles an\n"
            "  nft delete rule inet filter input handle 7"
        ),
        syntax       = "nft add rule inet filter input tcp dport 22 accept",
        example      = "nft list ruleset -a  # Handles anzeigen",
        task_description = "Füge eine nftables-Regel hinzu, die SSH (Port 22) in der inet filter input-Chain erlaubt.",
        expected_commands = ["nft add rule inet filter input tcp dport 22 accept"],
        hint_text    = "nft add rule inet filter input tcp dport 22 accept — inet = IPv4+IPv6, filter = Table, input = Chain",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist das iptables-Äquivalent zu 'nft add rule inet filter input tcp dport 22 accept'?",
                options  = [
                    "iptables -I INPUT tcp 22 ACCEPT",
                    "iptables -A INPUT -p tcp --dport 22 -j ACCEPT",
                    "iptables --add INPUT -tcp -port 22 -action ACCEPT",
                    "iptables -R INPUT 1 -p tcp -dport 22 -j ACCEPT",
                ],
                correct  = 1,
                explanation = (
                    "iptables -A INPUT -p tcp --dport 22 -j ACCEPT ist das direkte Äquivalent.\n"
                    "-A INPUT = append zu INPUT Chain (wie nft add rule ... input)\n"
                    "-p tcp --dport 22 = Protokoll TCP Port 22 (wie tcp dport 22)\n"
                    "-j ACCEPT = Jump zu ACCEPT (wie accept in nftables)"
                ),
                xp_value = 15,
            ),
            QuizQuestion(
                question = "In der nftables-Hierarchie: Was ist die korrekte Reihenfolge von übergeordnet zu untergeordnet?",
                options  = [
                    "Rule → Chain → Table",
                    "Chain → Table → Rule",
                    "Table → Rule → Chain",
                    "Table → Chain → Rule",
                ],
                correct  = 3,
                explanation = (
                    "Table → Chain → Rule ist die korrekte Hierarchie.\n"
                    "Table (z.B. 'inet filter') enthält Chains.\n"
                    "Chain (z.B. 'input') enthält Rules.\n"
                    "Rules sind die eigentlichen Match+Action-Paare."
                ),
                xp_value = 15,
            ),
        ],
        exam_tip     = "nft add rule TABLE CHAIN MATCH ACTION | iptables -A CHAIN -p PROTO --dport PORT -j TARGET",
        memory_tip   = "nftables: Table(Namensraum) → Chain(Sequenz) → Rule(Match+Action) — drei Ebenen",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.10 — PAM — Pluggable Authentication Modules
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.10",
        chapter      = 15,
        title        = "PAM — Pluggable Authentication Modules",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ghost. Authentifizierung in Linux ist kein monolithischer Block.\n"
            " Es ist ein Modulstack — PAM.\n"
            " Jeder Login, jedes sudo, jedes su läuft durch diesen Stack.\n"
            " Versteh PAM — und du verstehst wer wirklich rein darf.'"
        ),
        why_important = (
            "PAM (Pluggable Authentication Modules) ist der zentrale\n"
            "Authentifizierungsrahmen in Linux. SSH-Login, sudo, su, login —\n"
            "alle nutzen PAM. Fehlkonfigurationen können das System öffnen\n"
            "oder legitime Nutzer aussperren. LPIC-1 Topic 110.3."
        ),
        explanation  = (
            "PAM-Struktur:\n"
            "  /etc/pam.d/           → Verzeichnis mit Service-Konfigurationen\n"
            "  /etc/pam.d/sshd       → PAM-Stack für SSH-Logins\n"
            "  /etc/pam.d/sudo       → PAM-Stack für sudo-Aufrufe\n"
            "  /etc/pam.d/common-*   → Gemeinsame Basis-Konfigurationen (Debian)\n"
            "\n"
            "Zeilenformat in pam.d-Dateien:\n"
            "  TYPE  CONTROL  MODULE  [ARGUMENTS]\n"
            "  auth  required pam_unix.so  nullok\n"
            "\n"
            "Control-Flags (Verhalten bei Erfolg/Fehler):\n"
            "  required   → Muss erfolgreich sein; Fehler stoppt Stack NICHT sofort\n"
            "  requisite  → Muss erfolgreich sein; Fehler stoppt Stack SOFORT\n"
            "  sufficient → Bei Erfolg: Authentifizierung OK (wenn kein required davor fehlschlug)\n"
            "  optional   → Ergebnis wird meist ignoriert\n"
            "\n"
            "Häufige PAM-Module:\n"
            "  pam_unix.so      → Standard Unix-Authentifizierung (/etc/shadow)\n"
            "  pam_limits.so    → Ressourcenlimits aus /etc/security/limits.conf\n"
            "  pam_listfile.so  → Erlaubnis anhand von Dateilisten (allow/deny)\n"
            "\n"
            "PAM-Typen:\n"
            "  auth     → Identität prüfen (Passwort)\n"
            "  account  → Konto-Bedingungen (Ablauf, Sperren)\n"
            "  session  → Session-Setup (Umgebung, Limits)\n"
            "  password → Passwort ändern"
        ),
        syntax       = "ls /etc/pam.d/",
        example      = "cat /etc/pam.d/sshd",
        task_description = "Zeige den Inhalt der PAM-Konfiguration für SSH an.",
        expected_commands = ["cat /etc/pam.d/sshd"],
        hint_text    = "cat /etc/pam.d/sshd — zeigt den PAM-Stack für SSH-Logins",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher PAM-Control-Flag stoppt den PAM-Stack sofort bei einem Fehler?",
                options  = [
                    "required",
                    "optional",
                    "requisite",
                    "sufficient",
                ],
                correct  = 2,
                explanation = (
                    "requisite stoppt den PAM-Stack sofort bei einem Fehler — keine weiteren Module werden aufgerufen.\n"
                    "required lässt den Stack weiterlaufen, schlägt aber am Ende fehl.\n"
                    "sufficient: Bei Erfolg sofort OK (wenn kein required davor fehlschlug).\n"
                    "optional: Ergebnis wird ignoriert (außer es ist das einzige Modul)."
                ),
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welches PAM-Modul liest Ressourcenlimits aus /etc/security/limits.conf?",
                options  = [
                    "pam_unix.so",
                    "pam_listfile.so",
                    "pam_env.so",
                    "pam_limits.so",
                ],
                correct  = 3,
                explanation = (
                    "pam_limits.so liest und setzt Ressourcenlimits aus /etc/security/limits.conf.\n"
                    "Es wird typischerweise im session-Typ eingebunden.\n"
                    "pam_unix.so = Passwort-Authentifizierung | pam_listfile.so = Dateibasierte Listen."
                ),
                xp_value = 15,
            ),
        ],
        exam_tip     = "PAM Control-Flags: required(weiter) requisite(sofort-stop) sufficient(sofort-ok) optional(egal)",
        memory_tip   = "PAM = Pluggable: Jeder Service hat eigene /etc/pam.d/SERVICE-Datei",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.11 — PAM & /etc/security/limits.conf
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.11",
        chapter      = 15,
        title        = "PAM & /etc/security/limits.conf",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ein Operator hat Prozesse gestartet, die das System\n"
            " in die Knie zwingen. Zu viele offene Files. Zu viel RAM.\n"
            " limits.conf ist deine Waffe dagegen.\n"
            " PAM setzt die Limits — du definierst sie.'"
        ),
        why_important = (
            "Ressourcenlimits verhindern, dass einzelne Nutzer oder Prozesse\n"
            "das System destabilisieren (Fork-Bombs, Datei-Descriptor-Erschöpfung).\n"
            "/etc/security/limits.conf wird via pam_limits.so bei jeder Session\n"
            "geladen. ulimit zeigt aktive Limits im Shell-Kontext."
        ),
        explanation  = (
            "Zusammenhang ulimit ↔ PAM ↔ limits.conf:\n"
            "  1. PAM-Session-Modul pam_limits.so wird beim Login aufgerufen\n"
            "  2. Es liest /etc/security/limits.conf\n"
            "  3. Limits werden für die Session gesetzt\n"
            "  4. ulimit -a zeigt die gesetzten Limits in der aktuellen Shell\n"
            "\n"
            "/etc/security/limits.conf Format:\n"
            "  DOMAIN  TYPE  ITEM   VALUE\n"
            "  ghost   soft  nofile 4096\n"
            "  ghost   hard  nofile 8192\n"
            "  @devs   soft  nproc  200\n"
            "  *       hard  core   0\n"
            "\n"
            "Felder:\n"
            "  DOMAIN = Benutzername | @Gruppe | * (alle)\n"
            "  TYPE   = soft (Warnschwelle, vom User änderbar bis hard)\n"
            "         = hard (Maximum, nur root kann überschreiben)\n"
            "  ITEM   = nofile (max. offene Dateien) | nproc (max. Prozesse)\n"
            "         = memlock | fsize | core | ...\n"
            "\n"
            "pam_limits.so in /etc/pam.d/common-session (Debian/Ubuntu):\n"
            "  session required pam_limits.so\n"
            "\n"
            "Aktive Limits anzeigen:\n"
            "  ulimit -a        → alle Limits\n"
            "  ulimit -n        → max. offene Dateien (nofile)\n"
            "  ulimit -u        → max. Prozesse (nproc)"
        ),
        syntax       = "cat /etc/security/limits.conf",
        example      = "ulimit -a  # Aktive Limits der aktuellen Shell anzeigen",
        task_description = "Zeige den Inhalt von /etc/security/limits.conf an.",
        expected_commands = ["cat /etc/security/limits.conf"],
        hint_text    = "cat /etc/security/limits.conf — zeigt alle konfigurierten Ressourcenlimits",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Unterschied zwischen 'soft' und 'hard' Limits in limits.conf?",
                options  = [
                    "soft = für root, hard = für normale User",
                    "soft = Warnschwelle (User kann bis hard erhöhen), hard = absolutes Maximum",
                    "soft = temporär (bis Logout), hard = permanent (nach Reboot)",
                    "soft = RAM-Limits, hard = CPU-Limits",
                ],
                correct  = 1,
                explanation = (
                    "soft = Warnschwelle: Der User kann seinen eigenen soft-Limit bis zum hard-Limit erhöhen.\n"
                    "hard = absolutes Maximum: Nur root kann hard-Limits ändern.\n"
                    "Ein User kann also ulimit -n 6000 setzen, wenn soft=4096 und hard=8192."
                ),
                xp_value = 15,
            ),
            QuizQuestion(
                question = "Welches PAM-Modul muss in der session-Sektion eingebunden sein, damit limits.conf wirkt?",
                options  = [
                    "pam_unix.so",
                    "pam_security.so",
                    "pam_limits.so",
                    "pam_ulimit.so",
                ],
                correct  = 2,
                explanation = (
                    "pam_limits.so liest /etc/security/limits.conf und setzt die Limits für die Session.\n"
                    "Es muss im session-Typ eingebunden sein (nicht auth oder account).\n"
                    "Typischer Eintrag: 'session required pam_limits.so' in /etc/pam.d/common-session."
                ),
                xp_value = 15,
            ),
        ],
        exam_tip     = "limits.conf: DOMAIN TYPE ITEM VALUE | soft=User-änderbar bis hard | pam_limits.so lädt es",
        memory_tip   = "ulimit → PAM → limits.conf: soft ist der Startpunkt, hard ist die Wand",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.12 — SSH Port Forwarding & Tunnels
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.12",
        chapter      = 15,
        title        = "SSH Tunnels & Port Forwarding",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ghost. Du musst auf den internen DB-Server zugreifen,\n"
            " der nur von innen erreichbar ist. SSH-Tunnel ist die Lösung.\n"
            " Kein VPN. Nur ein verschlüsselter Kanal durch die Firewall.'"
        ),
        why_important = (
            "SSH Port Forwarding ermöglicht sicheren Zugriff auf interne Services\n"
            "durch verschlüsselte Tunnel. LPIC-1 Topic 110.3 testet ssh -L und -R."
        ),
        explanation  = (
            "SSH TUNNELING:\n\n"
            "LOCAL FORWARDING (-L): Lokaler Port → Remote\n"
            "  ssh -L 8080:internal-db:5432 user@jumphost\n"
            "  → localhost:8080 leitet zu internal-db:5432 weiter\n\n"
            "REMOTE FORWARDING (-R): Remote Port → Lokal\n"
            "  ssh -R 9090:localhost:80 user@remote\n"
            "  → remote:9090 leitet zu localhost:80 weiter\n\n"
            "DYNAMIC FORWARDING (-D): SOCKS-Proxy\n"
            "  ssh -D 1080 user@remote\n"
            "  → Browser via SOCKS5 localhost:1080 tunneln\n\n"
            "JUMP HOST (-J):\n"
            "  ssh -J jumphost user@internal\n"
            "  ProxyJump in ~/.ssh/config\n\n"
            "KEEPALIVE / HINTERGRUND:\n"
            "  ssh -fN -L 8080:db:5432 user@jumphost\n"
            "  -f=background, -N=no command, -C=compression"
        ),
        syntax       = "ssh -L [bind:]localport:host:hostport user@sshserver",
        example      = "ssh -L 8080:192.168.1.10:5432 admin@vpn.example.com",
        task_description = "Zeige SSH-Tunnel-Optionen mit ssh -h | grep -A2 -- '-L'",
        expected_commands = ["ssh -L"],
        hint_text    = "ssh -L localport:zielhost:zielport user@jumphost",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `ssh -L 8080:db.intern:3306 user@jump`?",
                options  = [
                    "Leitet localhost:8080 → db.intern:3306 über jump weiter",
                    "Öffnet Port 8080 auf db.intern",
                    "Leitet db.intern:3306 → localhost:8080",
                    "Erstellt einen SOCKS-Proxy auf Port 8080",
                ],
                correct  = 0,
                explanation = "-L = Local Forwarding: lokaler Port → über SSH-Server → Ziel",
                xp_value = 15,
            ),
        ],
        exam_tip     = "ssh -L lokal, -R remote, -D dynamisch (SOCKS). -f background -N kein Befehl.",
        memory_tip   = "L=Local (ich leite), R=Remote (Server leitet), D=Dynamic (SOCKS-Proxy)",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.13 — OpenSSL Zertifikate
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.13",
        chapter      = 15,
        title        = "OpenSSL: Schlüssel & Zertifikate",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Kryptographie ist das Herzstück jeder sicheren Verbindung.\n"
            " Ein selbst-signiertes Zertifikat für interne Services.\n"
            " openssl ist dein Werkzeug. Drei Befehle. Kein Kompromiss.'"
        ),
        why_important = (
            "SSL/TLS-Zertifikate sichern Netzwerkverbindungen. openssl ist das\n"
            "Standard-Tool zum Erzeugen von Keys, CSRs und Self-Signed Certs."
        ),
        explanation  = (
            "OPENSSL — SCHLÜSSEL & ZERTIFIKATE:\n\n"
            "SCHLÜSSEL ERZEUGEN:\n"
            "  openssl genrsa -out server.key 4096\n"
            "  openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:4096\n\n"
            "CSR (Certificate Signing Request):\n"
            "  openssl req -new -key server.key -out server.csr\n"
            "  openssl req -text -noout -in server.csr  (CSR lesen)\n\n"
            "SELF-SIGNED CERT:\n"
            "  openssl req -x509 -nodes -days 365 -newkey rsa:4096 \\\n"
            "    -keyout server.key -out server.crt\n\n"
            "ZERTIFIKAT PRÜFEN:\n"
            "  openssl x509 -text -noout -in server.crt\n"
            "  openssl x509 -enddate -noout -in server.crt\n"
            "  openssl s_client -connect host:443\n\n"
            "HASH / DGST:\n"
            "  openssl dgst -sha256 datei.tar.gz\n"
            "  openssl dgst -md5 datei"
        ),
        syntax       = "openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout key -out cert",
        example      = "openssl x509 -text -noout -in server.crt | grep -E 'Subject|Issuer|Not After'",
        task_description = "Prüfe ein Zertifikat mit openssl x509 -text -noout -in /etc/ssl/certs/ca-certificates.crt | head -20",
        expected_commands = ["openssl x509"],
        hint_text    = "openssl x509 -text -noout -in datei.crt",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher openssl-Befehl erzeugt ein self-signed Zertifikat?",
                options  = [
                    "openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout key -out cert",
                    "openssl genrsa -out server.crt 4096",
                    "openssl ca -selfsign -keyfile key -cert cert",
                    "openssl x509 -new -key server.key -out server.crt",
                ],
                correct  = 0,
                explanation = "req -x509 kombiniert CSR-Erstellung und Selbst-Signierung in einem Schritt",
                xp_value = 15,
            ),
        ],
        exam_tip     = "openssl genrsa=Key | req -new=CSR | req -x509=Self-Signed | x509 -text=anzeigen",
        memory_tip   = "genrsa → req (CSR) → x509 (Zertifikat) — der Weg eines TLS-Schlüssels",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.14 — auditd: Systemereignisse protokollieren
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.14",
        chapter      = 15,
        title        = "auditd — Systemauditing",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Wir brauchen Beweise, Ghost. Jede Datei, die root anfasst.\n"
            " auditd zeichnet alles auf — Kernel-Ebene, nicht umgehbar.\n"
            " Aktiviere die Regeln. Finde die Spur.'"
        ),
        why_important = (
            "auditd ist das Linux Kernel Audit System. Es zeichnet sicherheitsrelevante\n"
            "Ereignisse auf — Datei-Zugriffe, Logins, Befehlsausführungen, Systemcalls."
        ),
        explanation  = (
            "AUDITD — LINUX AUDIT SYSTEM:\n\n"
            "STATUS:\n"
            "  systemctl status auditd\n"
            "  auditctl -l          Regeln anzeigen\n"
            "  auditctl -s          Audit-Status\n\n"
            "REGELN SETZEN:\n"
            "  auditctl -w /etc/passwd -p rwxa -k passwd_watch\n"
            "  auditctl -w /etc/shadow -p rwxa -k shadow_watch\n"
            "  auditctl -a always,exit -F arch=b64 -S execve -k cmd_exec\n"
            "  -w=watch path, -p=permissions(r/w/x/a), -k=key\n\n"
            "LOG DURCHSUCHEN:\n"
            "  ausearch -k passwd_watch\n"
            "  ausearch -x /bin/su\n"
            "  ausearch --start today --end now\n\n"
            "BERICHTE:\n"
            "  aureport --summary\n"
            "  aureport --auth\n"
            "  aureport --file\n\n"
            "CONFIG: /etc/audit/auditd.conf, /etc/audit/rules.d/"
        ),
        syntax       = "auditctl -w /pfad -p rwxa -k schlüsselname",
        example      = "auditctl -w /etc/shadow -p rwxa -k shadow_watch && ausearch -k shadow_watch",
        task_description = "Zeige aktuelle Audit-Regeln mit auditctl -l",
        expected_commands = ["auditctl -l"],
        hint_text    = "auditctl -l zeigt alle aktiven Audit-Regeln",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl sucht im Audit-Log nach Ereignissen mit Key 'passwd_watch'?",
                options  = [
                    "ausearch -k passwd_watch",
                    "auditctl -k passwd_watch",
                    "aureport -k passwd_watch",
                    "journalctl -k passwd_watch",
                ],
                correct  = 0,
                explanation = "ausearch durchsucht das Audit-Log nach Keys, Pfaden, Programmen oder Zeiten",
                xp_value = 15,
            ),
        ],
        exam_tip     = "auditctl -w=Datei überwachen | ausearch -k=nach Key suchen | aureport=Zusammenfassung",
        memory_tip   = "auditCTL = Kontrolle (Regeln) | auditSEARCH = Suche | auditREPORT = Bericht",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.15 — TCP Wrappers: /etc/hosts.allow & hosts.deny
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.15",
        chapter      = 15,
        title        = "TCP Wrappers: hosts.allow & hosts.deny",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Alte Waffe, aber noch nicht tot. TCP Wrappers.\n"
            " Bevor eine Verbindung an sshd kommt, prüft tcpd die Allow-Liste.\n"
            " Kleines Netz, schnelle Lösung. Kenn die Reihenfolge.'"
        ),
        why_important = (
            "TCP Wrappers (libwrap) sind ein Host-basiertes Zugangskontrollsystem.\n"
            "Obwohl veraltet, sind sie Teil des LPIC-1 Lehrplans (Topic 110.2)."
        ),
        explanation  = (
            "TCP WRAPPERS:\n\n"
            "FUNKTIONSWEISE:\n"
            "  Reihenfolge: /etc/hosts.allow ZUERST, dann /etc/hosts.deny\n"
            "  Wenn ein Eintrag in hosts.allow passt → ERLAUBT (kein hosts.deny prüfen)\n"
            "  Wenn ein Eintrag in hosts.deny passt → VERWEIGERT\n"
            "  Wenn nichts passt → ERLAUBT (implizit)\n\n"
            "SYNTAX: daemon : client_list\n"
            "  sshd : 192.168.1.0/255.255.255.0   IP-Bereich\n"
            "  sshd : .example.com                 Domain-Suffix\n"
            "  ALL : ALL                           alles/jeder\n"
            "  ALL : PARANOID                      Hostname ≠ IP → blockieren\n\n"
            "BEISPIELE:\n"
            "  /etc/hosts.allow: sshd : 192.168.1.0/255.255.255.0\n"
            "  /etc/hosts.deny:  ALL : ALL\n"
            "  → Nur SSH aus 192.168.1.0/24 erlaubt, alles andere gesperrt\n\n"
            "TEST:\n"
            "  tcpdmatch sshd 192.168.1.1\n"
            "  hosts_access sshd 10.0.0.1"
        ),
        syntax       = "daemon : clientliste   (in /etc/hosts.allow oder /etc/hosts.deny)",
        example      = "# /etc/hosts.allow\nsshd : 192.168.0.0/255.255.0.0\n# /etc/hosts.deny\nALL : ALL",
        task_description = "Zeige den Inhalt von /etc/hosts.allow",
        expected_commands = ["cat /etc/hosts.allow"],
        hint_text    = "cat /etc/hosts.allow — oder less, head, nano",
        quiz_questions = [
            QuizQuestion(
                question = "In welcher Reihenfolge prüft TCP Wrappers die Dateien?",
                options  = [
                    "hosts.allow zuerst, dann hosts.deny",
                    "hosts.deny zuerst, dann hosts.allow",
                    "Beide gleichzeitig, deny hat Priorität",
                    "Beide gleichzeitig, allow hat Priorität",
                ],
                correct  = 0,
                explanation = "hosts.allow wird ZUERST geprüft. Bei Match → erlaubt. Kein Match → hosts.deny prüfen.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "allow ZUERST prüfen! Kein Match in beiden → erlaubt (fail-open). ALL:ALL in deny sperrt alles.",
        memory_tip   = "Allow vor Deny. Wie eine Gästeliste: erst schauen wer darf, dann wer nicht.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.16 — sudo: erweiterte Konfiguration
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.16",
        chapter      = 15,
        title        = "sudo Advanced: Aliases & Defaults",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Root-Zugriff ist ein Skalpell, kein Vorschlaghammer.\n"
            " visudo. Aliases definieren. Defaults setzen.\n"
            " Wer braucht was — und nichts mehr.'"
        ),
        why_important = (
            "sudo Konfiguration über Aliases, Defaults und Cmnd_Alias ist wichtig\n"
            "für granulare Rechtevergabe ohne vollständige Root-Rechte."
        ),
        explanation  = (
            "SUDO ADVANCED CONFIGURATION:\n\n"
            "ALIASES IN /etc/sudoers:\n"
            "  User_Alias ADMINS = alice, bob\n"
            "  Cmnd_Alias SERVICES = /bin/systemctl, /usr/sbin/service\n"
            "  Host_Alias SERVERS = 192.168.1.0/24\n"
            "  Runas_Alias OPERATORS = operator, admin\n\n"
            "REGELN:\n"
            "  ADMINS ALL=(ALL) SERVICES\n"
            "  → ADMINS können SERVICES auf allen Hosts ausführen\n"
            "  alice ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx\n"
            "  → Kein Passwort für diesen Befehl\n\n"
            "DEFAULTS:\n"
            "  Defaults env_reset\n"
            "  Defaults mail_badpass\n"
            "  Defaults secure_path='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'\n"
            "  Defaults logfile=/var/log/sudo.log\n\n"
            "ÜBERPRÜFEN:\n"
            "  sudo -l               Was darf ich?\n"
            "  sudo -l -U alice      Was darf alice?\n"
            "  sudo -u www-data id   Als anderer User ausführen"
        ),
        syntax       = "User Host=(Runas) [NOPASSWD:] Befehlsliste",
        example      = "alice ALL=(ALL) NOPASSWD: /usr/bin/apt update, /bin/systemctl restart *",
        task_description = "Zeige erlaubte sudo-Befehle mit sudo -l",
        expected_commands = ["sudo -l"],
        hint_text    = "sudo -l zeigt was du mit sudo ausführen darfst",
        quiz_questions = [
            QuizQuestion(
                question = "Was bedeutet NOPASSWD in einer sudoers-Regel?",
                options  = [
                    "Der Befehl kann ohne Passwort-Eingabe via sudo ausgeführt werden",
                    "Root benötigt kein Passwort",
                    "Der Benutzer hat kein Passwort gesetzt",
                    "sudo fragt das root-Passwort statt des User-Passworts",
                ],
                correct  = 0,
                explanation = "NOPASSWD: erlaubt sudo für diesen Befehl ohne Passwort-Prompt",
                xp_value = 15,
            ),
        ],
        exam_tip     = "visudo = EINZIGER sicherer Weg. sudo -l = Was darf ich? NOPASSWD = kein Prompt.",
        memory_tip   = "Aliases gruppieren, Defaults konfigurieren, Regeln: Wer Wo=(Als) Was",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.17 — LUKS: Erweiterte Verschlüsselung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.17",
        chapter      = 15,
        title        = "LUKS: Schlüsselverwaltung & luksDump",
        mtype        = "SCAN",
        xp           = 95,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Ghost. Verschlüsselte Partition mit 3 Schlüsseln.\n"
            " Notfall-Key im Vault. Haupt-Key rotieren.\n"
            " cryptsetup kennt jeden Slot. Kenne die Befehle.'"
        ),
        why_important = (
            "LUKS (Linux Unified Key Setup) unterstützt bis zu 8 Schlüssel-Slots.\n"
            "Key-Management ist kritisch für Backup-Zugriff und Rotation."
        ),
        explanation  = (
            "LUKS SCHLÜSSELVERWALTUNG:\n\n"
            "LUKS INFO:\n"
            "  cryptsetup luksDump /dev/sdb1\n"
            "  → Zeigt LUKS-Header: UUID, Cipher, Key-Slots (0-7)\n\n"
            "SCHLÜSSEL HINZUFÜGEN:\n"
            "  cryptsetup luksAddKey /dev/sdb1\n"
            "  → Fragt bestehenden Key, dann neuen Key\n"
            "  → Nächster freier Slot wird verwendet\n\n"
            "SCHLÜSSEL ENTFERNEN:\n"
            "  cryptsetup luksRemoveKey /dev/sdb1\n"
            "  → Fragt den zu entfernenden Key\n"
            "  cryptsetup luksKillSlot /dev/sdb1 1\n"
            "  → Slot 1 mit Master-Key leeren\n\n"
            "BACKUP DES LUKS-HEADERS:\n"
            "  cryptsetup luksHeaderBackup /dev/sdb1 --header-backup-file luks-header.bak\n"
            "  cryptsetup luksHeaderRestore /dev/sdb1 --header-backup-file luks-header.bak\n\n"
            "ÖFFNEN / SCHLIESSEN:\n"
            "  cryptsetup luksOpen /dev/sdb1 secret_vol\n"
            "  cryptsetup luksClose secret_vol"
        ),
        syntax       = "cryptsetup luksDump /dev/sdb1",
        example      = "cryptsetup luksDump /dev/sda5 | grep -E 'UUID|Cipher|Key Slot'",
        task_description = "Zeige LUKS-Informationen mit cryptsetup luksDump (Simulation)",
        expected_commands = ["cryptsetup luksDump"],
        hint_text    = "cryptsetup luksDump /dev/sdX zeigt alle LUKS-Header-Infos",
        quiz_questions = [
            QuizQuestion(
                question = "Wie viele Schlüssel-Slots unterstützt LUKS1 maximal?",
                options  = [
                    "8",
                    "4",
                    "16",
                    "1",
                ],
                correct  = 0,
                explanation = "LUKS1 hat 8 Key Slots (0-7). LUKS2 hat 32 Token-Slots.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "luksDump=Info | luksAddKey=Slot befüllen | luksRemoveKey/luksKillSlot=Slot leeren",
        memory_tip   = "LUKS hat 8 Safes (Slots). Jeder kann einen Schlüssel zur selben verschlüsselten Tür haben.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.18 — Security Hardening: sysctl & login.defs
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.18",
        chapter      = 15,
        title        = "System-Härtung: sysctl & login.defs",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Härtung ist kein Einzel-Befehl. Es ist eine Haltung.\n"
            " sysctl für Kernel-Parameter. login.defs für Account-Defaults.\n"
            " Konfiguriere das System so, dass es sich selbst schützt.'"
        ),
        why_important = (
            "System-Härtung via sysctl und /etc/login.defs reduziert die Angriffsfläche.\n"
            "Sicherheitskritische Parameter wie IP-Forwarding und Passwort-Aging."
        ),
        explanation  = (
            "SYSTEM-HÄRTUNG:\n\n"
            "SYSCTL SICHERHEITS-PARAMETER:\n"
            "  net.ipv4.ip_forward = 0           IP-Forwarding aus (kein Router)\n"
            "  net.ipv4.conf.all.accept_redirects = 0  ICMP-Redirects ablehnen\n"
            "  net.ipv4.conf.all.rp_filter = 1   Reverse Path Filtering\n"
            "  net.ipv4.tcp_syncookies = 1        SYN-Flood-Schutz\n"
            "  kernel.randomize_va_space = 2      ASLR aktivieren\n"
            "  kernel.dmesg_restrict = 1          dmesg für normale User sperren\n\n"
            "DAUERHAFT: /etc/sysctl.conf oder /etc/sysctl.d/99-hardening.conf\n"
            "  sysctl -p /etc/sysctl.d/99-hardening.conf\n\n"
            "/etc/login.defs WICHTIGE PARAMETER:\n"
            "  PASS_MAX_DAYS   90    Passwort läuft nach 90 Tagen ab\n"
            "  PASS_MIN_DAYS   1     Minimum 1 Tag zwischen Passwort-Änderungen\n"
            "  PASS_WARN_AGE   7     7 Tage Vorwarnung\n"
            "  LOGIN_RETRIES   3     Max. 3 Fehlversuche\n"
            "  UID_MIN         1000  Erste UID für normale User\n"
            "  CREATE_HOME     yes   Home-Verzeichnis automatisch anlegen"
        ),
        syntax       = "sysctl -w net.ipv4.ip_forward=0",
        example      = "sysctl -a | grep -E 'ip_forward|randomize_va_space|syncookies'",
        task_description = "Prüfe ob IP-Forwarding deaktiviert ist mit sysctl net.ipv4.ip_forward",
        expected_commands = ["sysctl net.ipv4.ip_forward"],
        hint_text    = "sysctl net.ipv4.ip_forward — 0 = aus, 1 = ein",
        quiz_questions = [
            QuizQuestion(
                question = "Wo werden sysctl-Parameter dauerhaft konfiguriert?",
                options  = [
                    "/etc/sysctl.conf oder /etc/sysctl.d/*.conf",
                    "/etc/kernel.conf",
                    "/proc/sys/net/ipv4/ip_forward (dauerhaft)",
                    "/boot/sysctl.conf",
                ],
                correct  = 0,
                explanation = "/etc/sysctl.conf und /etc/sysctl.d/ sind dauerhaft. /proc/sys/ ist nur bis Reboot.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "sysctl -w = sofort | sysctl -p = aus Datei laden | /proc/sys/ = flüchtig",
        memory_tip   = "sysctl.conf = dauerhafter Kernel-Tuner. login.defs = Standard-Werte für neue User.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.19 — Netzwerk-Sicherheits-Monitoring mit netstat/ss
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.19",
        chapter      = 15,
        title        = "Port-Scanning & Netzwerk-Audit",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Know your own perimeter, Ghost.\n"
            " Was lauscht auf deinem System? Welche Ports sind offen?\n"
            " Bevor der Feind es weiß — wisse du es selbst.'"
        ),
        why_important = (
            "Offene Ports sind potenzielle Angriffsvektoren. ss und netstat zeigen\n"
            "lauschende Dienste. Regelmäßiges Auditing ist Pflicht."
        ),
        explanation  = (
            "PORT-AUDIT TOOLS:\n\n"
            "SS (SOCKET STATISTICS — modern):\n"
            "  ss -tulpn     TCP+UDP lauschend, Prozess-Info, numerisch\n"
            "  ss -tnp       TCP mit Prozessen\n"
            "  ss -4 -tulpn  nur IPv4\n"
            "  ss -6 -tulpn  nur IPv6\n"
            "  ss -s         Zusammenfassung\n\n"
            "NETSTAT (klassisch, aus net-tools):\n"
            "  netstat -tulpn   wie ss -tulpn\n"
            "  netstat -rn      Routing-Tabelle\n"
            "  netstat -s       Protokoll-Statistiken\n\n"
            "NMAP (Netzwerk-Scanner):\n"
            "  nmap -sS localhost      SYN-Scan lokal\n"
            "  nmap -sV -p- localhost  Service-Version alle Ports\n"
            "  nmap -O localhost       OS-Detection\n\n"
            "LSOF (offene Dateien/Ports):\n"
            "  lsof -i :22     Wer nutzt Port 22?\n"
            "  lsof -i -P -n   alle Netzwerk-Verbindungen"
        ),
        syntax       = "ss -tulpn | grep LISTEN",
        example      = "ss -tulpn | awk '/LISTEN/{print $1,$5,$7}'",
        task_description = "Zeige alle lauschenden Ports mit ss -tulpn",
        expected_commands = ["ss -tulpn"],
        hint_text    = "ss -tulpn: t=TCP u=UDP l=LISTEN p=Prozess n=numerisch",
        quiz_questions = [
            QuizQuestion(
                question = "Was zeigt `ss -tulpn`?",
                options  = [
                    "TCP und UDP lauschende Ports mit Prozessname und numerischen Adressen",
                    "Nur TCP-Verbindungen",
                    "Alle offenen Dateien des Systems",
                    "Routing-Tabelle",
                ],
                correct  = 0,
                explanation = "t=TCP, u=UDP, l=listening, p=process, n=numeric (kein DNS-Lookup)",
                xp_value = 15,
            ),
        ],
        exam_tip     = "ss > netstat (moderneres Tool). ss -tulpn ist der Standard-Audit-Befehl.",
        memory_tip   = "TULPN: TCP UDP Listen Process Numeric — jede Option hat einen Sinn.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.20 — Intrusion Detection: fail2ban Advanced
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.20",
        chapter      = 15,
        title        = "fail2ban: Jails & Aktionen konfigurieren",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Drei Fehlversuche. Ban für 10 Minuten.\n"
            " fail2ban beobachtet die Logs und sperrt Angreifer automatisch.\n"
            " jail.local überschreibt jail.conf — niemals jail.conf direkt editieren.'"
        ),
        why_important = (
            "fail2ban schützt automatisch gegen Brute-Force-Angriffe durch\n"
            "dynamisches Sperren von IP-Adressen via iptables/nftables."
        ),
        explanation  = (
            "FAIL2BAN KONFIGURATION:\n\n"
            "STRUKTUR:\n"
            "  /etc/fail2ban/jail.conf      Basis-Konfiguration (nicht ändern!)\n"
            "  /etc/fail2ban/jail.local     Überschreibungen (hier arbeiten)\n"
            "  /etc/fail2ban/jail.d/*.conf  Einzelne Jail-Dateien\n\n"
            "JAIL.LOCAL BEISPIEL:\n"
            "  [DEFAULT]\n"
            "  bantime  = 10m    Sperrdauer\n"
            "  findtime = 10m    Zeitfenster für Fehlversuche\n"
            "  maxretry = 3      Max. Fehlversuche\n\n"
            "  [sshd]\n"
            "  enabled = true\n"
            "  port    = ssh\n"
            "  logpath = %(sshd_log)s\n"
            "  maxretry = 3\n\n"
            "VERWALTUNG:\n"
            "  fail2ban-client status\n"
            "  fail2ban-client status sshd\n"
            "  fail2ban-client set sshd unbanip 1.2.3.4\n"
            "  fail2ban-client set sshd banip 1.2.3.4\n\n"
            "AKTIONEN:\n"
            "  iptables (Standard) / nftables / route / mail-whois"
        ),
        syntax       = "fail2ban-client status sshd",
        example      = "fail2ban-client status && fail2ban-client status sshd | grep -E 'Banned|Currently'",
        task_description = "Zeige fail2ban-Status mit fail2ban-client status",
        expected_commands = ["fail2ban-client status"],
        hint_text    = "fail2ban-client status zeigt alle aktiven Jails",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Datei sollte angepasst werden, um fail2ban zu konfigurieren?",
                options  = [
                    "/etc/fail2ban/jail.local",
                    "/etc/fail2ban/jail.conf",
                    "/etc/fail2ban/fail2ban.conf",
                    "/etc/fail2ban/filter.d/sshd.conf",
                ],
                correct  = 0,
                explanation = "jail.local überschreibt jail.conf. Nie jail.conf direkt bearbeiten (wird bei Updates überschrieben).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "jail.local überschreibt jail.conf. fail2ban-client status sshd zeigt gebannte IPs.",
        memory_tip   = "jail.conf = Original (unberührt) | jail.local = deine Änderungen",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.21 — QUIZ: Sicherheit
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.21",
        chapter      = 15,
        title        = "QUIZ — Security Protocol",
        mtype        = "QUIZ",
        xp           = 130,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM: 'SICHERHEITSAUDIT INITIIERT.\n"
            " NeonGrid-9 überprüft deine Kenntnisse der Systemhärtung.\n"
            " Ein kompromittierter Sysadmin ist schlimmer als kein Sysadmin.\n"
            " Beweise dein Wissen — jetzt.'"
        ),
        why_important = "LPIC-1 Prüfung: Topic 110.1/110.2/110.3 — Systemsicherheit",
        explanation  = "",
        syntax       = "",
        example      = "",
        task_description = "Beantworte 5 Sicherheitsfragen.",
        expected_commands = [],
        hint_text    = "",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher Befehl findet alle SUID-Dateien im System?",
                options  = [
                    "find / -type f -mode suid",
                    "find / -perm -4000 -type f",
                    "ls -la / | grep SUID",
                    "locate -perm suid /",
                ],
                correct  = 1,
                explanation = (
                    "find / -perm -4000 -type f sucht alle regulären Dateien mit gesetztem SUID-Bit.\n"
                    "-perm -4000 bedeutet: Bit 4000 (SUID) ist gesetzt.\n"
                    "2>/dev/null unterdrückt Fehlermeldungen (Permission denied)."
                ),
                xp_value = 26,
            ),
            QuizQuestion(
                question = "Welche sshd_config-Direktive verhindert Root-Logins via SSH?",
                options  = [
                    "DenyUsers root",
                    "RootLogin disabled",
                    "PermitRootLogin no",
                    "AllowRoot false",
                ],
                correct  = 2,
                explanation = (
                    "PermitRootLogin no verhindert, dass sich root direkt via SSH einloggen kann.\n"
                    "Mögliche Werte: yes | no | without-password | forced-commands-only\n"
                    "without-password = Root-Login nur mit Key, kein Passwort."
                ),
                xp_value = 26,
            ),
            QuizQuestion(
                question = "Was macht 'fail2ban-client set sshd unbanip 1.2.3.4'?",
                options  = [
                    "Bannt die IP 1.2.3.4 im SSH-Jail",
                    "Löscht den SSH-Jail komplett",
                    "Hebt den Ban der IP 1.2.3.4 im SSH-Jail auf",
                    "Fügt die IP zur Whitelist hinzu",
                ],
                correct  = 2,
                explanation = (
                    "unbanip hebt einen bestehenden Ban auf — z.B. wenn eine legitime IP\n"
                    "versehentlich gebannt wurde (z.B. Admin hat sein Passwort vergessen).\n"
                    "fail2ban-client status sshd zeigt alle aktuell gebannten IPs."
                ),
                xp_value = 26,
            ),
            QuizQuestion(
                question = "Welche Datei sollte für eigene sudo-Regeln verwendet werden?",
                options  = [
                    "/etc/sudo.conf",
                    "/etc/sudoers (direkt editieren)",
                    "/etc/sudoers.d/eigene-regeln (via visudo)",
                    "/etc/sudo.d/rules",
                ],
                correct  = 2,
                explanation = (
                    "/etc/sudoers.d/ enthält Fragment-Dateien, die mit #includedir eingebunden werden.\n"
                    "Eigene Regeln hier ablegen, nie /etc/sudoers direkt editieren!\n"
                    "Immer visudo verwenden — es prüft die Syntax vor dem Speichern."
                ),
                xp_value = 26,
            ),
            QuizQuestion(
                question = "Welcher openssl-Befehl entschlüsselt eine AES-256-CBC verschlüsselte Datei?",
                options  = [
                    "openssl enc -aes-256-cbc -in datei.enc -out datei.txt",
                    "openssl dec -aes-256-cbc -in datei.enc -out datei.txt",
                    "openssl enc -d -aes-256-cbc -in datei.enc -out datei.txt",
                    "openssl decrypt -aes-256-cbc datei.enc",
                ],
                correct  = 2,
                explanation = (
                    "openssl enc -d = decrypt mode.\n"
                    "Ohne -d = encrypt (verschlüsseln).\n"
                    "Gleicher Befehl, gleicher Algorithmus, gleicher Key — nur -d macht den Unterschied."
                ),
                xp_value = 26,
            ),
        ],
        exam_tip     = "SUID=4000 SGID=2000 | PermitRootLogin no | visudo | fail2ban jail.local | openssl -d",
        memory_tip   = "Security-Trias: Authentifizierung (SSH-Keys) + Autorisierung (sudo) + Verschlüsselung (GPG/LUKS)",
        gear_reward  = None,
        faction_reward = None,
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 15.BOSS — SHADOW ADMIN
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "15.boss",
        chapter      = 15,
        title        = "BOSS: SHADOW ADMIN v15.0",
        mtype        = "BOSS",
        xp           = 200,
        speaker      = "SHADOW ADMIN",
        story        = (
            "SHADOW ADMIN: 'Du dachtest, dein System wäre sicher, Ghost.\n"
            " SUID auf /usr/bin/vim. SSH mit Root-Login.\n"
            " Kein fail2ban. Sudo ohne Einschränkung.\n"
            " Ich war schon drin, während du noch geschlafen hast.\n"
            " Aber jetzt bin ich direkt vor dir. Zeit für die finale Prüfung.\n"
            " Zeig mir: Was tust du ZUERST nach einer Kompromittierung?'"
        ),
        why_important = (
            "Incident Response und Security Hardening sind LPIC-1-Prüfungsthemen.\n"
            "Ein kompromittiertes System erkennen, isolieren und absichern —\n"
            "die richtige Reihenfolge rettet Daten und Reputation."
        ),
        explanation  = (
            "Incident Response Grundschritte:\n"
            "1. Erkennen: last / lastb / who / w — wer ist/war eingeloggt?\n"
            "2. Isolieren: Netzwerkverbindungen kappen (ip link set eth0 down)\n"
            "3. Beweise sichern: Logs kopieren BEVOR sie rotieren\n"
            "4. Analysieren: auth.log / secure / journalctl -p warning\n"
            "5. Bereinigen: Backdoors entfernen, SUID-Bits prüfen\n"
            "6. Härten: SSH-Config, fail2ban, sudo-Regeln\n"
            "7. Wiederherstellen: Aus sauberem Backup\n"
            "\n"
            "Nützliche Forensik-Befehle:\n"
            "  last -F             → Login-History mit vollständigen Timestamps\n"
            "  lastb               → Fehlgeschlagene Logins\n"
            "  w                   → Eingeloggte User und ihre Aktivität\n"
            "  ps aux --sort=-%mem → Speicher-hungrige Prozesse (Backdoors?)\n"
            "  netstat -tulpn      → Unbekannte lauschende Ports\n"
            "  find / -mtime -1 -type f 2>/dev/null → Kürzlich geänderte Dateien\n"
            "  find / -perm -4000 -type f 2>/dev/null → SUID-Check\n"
            "  cat /etc/crontab && crontab -l → Verdächtige Cron-Jobs"
        ),
        syntax       = "last -F && lastb | head -20",
        example      = "find / -mtime -1 -type f 2>/dev/null | grep -v /proc",
        task_description = (
            "FINALE PRÜFUNG: Führe einen vollständigen Sicherheits-Audit durch.\n"
            "Prüfe Login-History mit 'last'."
        ),
        expected_commands = ["last"],
        hint_text    = "last zeigt die Login-History aus /var/log/wtmp",
        quiz_questions = [],
        exam_tip     = "Prüfung: SUID find -perm -4000 | PermitRootLogin no | visudo | fail2ban | openssl -d",
        memory_tip   = "Security = Erkennen + Isolieren + Analysieren + Härten + Wiederherstellen",
        gear_reward  = "ghost_mask",
        faction_reward = ("Kernel Syndicate", 50),
    ),
]
