"""
NeonGrid-9 :: Kapitel 20 — FIREWALL DOMINION
LPIC-1 Topic 109.4 / 110.1 / 110.2
Firewall Dominion: Netzwerk-Sicherheit, iptables, nftables, VPN, IDS/IPS

"Die Firewall Dominion hält die Grenzen von NeonGrid-9.
 Jedes Paket wird geprüft. Jede Verbindung bewertet.
 Kein Byte passiert ohne Erlaubnis."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_20_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 20.01 — Firewall Dominion: Einführung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.01",
        chapter      = 20,
        title        = "Firewall Dominion — Einführung",
        mtype        = "SCAN",
        xp           = 125,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Willkommen bei der Firewall Dominion, Operator.\n"
            " Wir sind das letzte Bollwerk zwischen NeonGrid-9 und dem Chaos.\n"
            " Jedes Paket, das diese Grenze passiert, hat unsere Erlaubnis.'"
        ),
        why_important = (
            "Firewall-Konfiguration ist ein Kernthema in LPIC-1 Topic 109/110.\n"
            "netfilter, iptables, nftables — das Netzwerk-Sicherheitsfundament."
        ),
        explanation  = (
            "LINUX FIREWALL ARCHITEKTUR:\n\n"
            "NETFILTER:\n"
            "  Kernel-Framework für Paketfilterung\n"
            "  Alle Firewall-Tools nutzen netfilter unter der Haube\n\n"
            "USERSPACE TOOLS:\n"
            "  iptables   klassisch (4.x Kernel)\n"
            "  nftables   modern (seit Kernel 3.13, Standard ab Debian 10)\n"
            "  firewalld  Frontend (Red Hat, nutzt iptables/nftables)\n"
            "  ufw        Frontend (Ubuntu-freundlich)\n\n"
            "NETFILTER HOOKS (Paket-Durchlauf):\n"
            "  PREROUTING → FORWARD → POSTROUTING (weitergeleitet)\n"
            "  PREROUTING → INPUT → LOCAL PROCESS → OUTPUT → POSTROUTING\n\n"
            "TABELLEN:\n"
            "  filter   Standard-Tabelle (INPUT, OUTPUT, FORWARD)\n"
            "  nat      Adress-Übersetzung (PREROUTING, POSTROUTING)\n"
            "  mangle   Paket-Manipulation\n"
            "  raw      Connection-Tracking deaktivieren"
        ),
        ascii_art = """
  ███████╗██╗██████╗ ███████╗██╗    ██╗ █████╗ ██╗     ██╗
  ██╔════╝██║██╔══██╗██╔════╝██║    ██║██╔══██╗██║     ██║
  █████╗  ██║██████╔╝█████╗  ██║ █╗ ██║███████║██║     ██║
  ██╔══╝  ██║██╔══██╗██╔══╝  ██║███╗██║██╔══██║██║     ██║
  ██║     ██║██║  ██║███████╗╚███╔███╔╝██║  ██║███████╗███████╗
  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝
      ██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██╗ ██████╗ ███╗   ██╗
      ██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██║██╔═══██╗████╗  ██║
      ██║  ██║██║   ██║██╔████╔██║██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
      ██║  ██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║██║╚██╗██║
      ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝██║ ╚████║
      ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

  [ CHAPTER 20 :: FIREWALL DOMINION ]
  > iptables/nftables ruleset loading. Chains: INPUT OUTPUT FORWARD.""",
        story_transitions = [
            "Pakete kommen an. Die Firewall entscheidet: ACCEPT, DROP, REJECT.",
            "INPUT, OUTPUT, FORWARD — drei Ketten. Tausend mögliche Regeln.",
            "nftables ersetzt iptables. Die Syntax ändert sich, die Logik bleibt.",
            "Blaze kontrolliert den Eingang. Du musst die Regeln schreiben.",
        ],
        syntax       = "iptables -L -n -v  (Regeln anzeigen)",
        example      = "iptables -L -n -v --line-numbers",
        task_description = "Zeige aktuelle Firewall-Regeln mit iptables -L -n -v",
        expected_commands = ["iptables -L -n -v"],
        hint_text    = "iptables -L = list, -n = numeric, -v = verbose",
        quiz_questions = [
            QuizQuestion(
                question = "Welche iptables-Tabelle wird für Standard-Paketfilterung verwendet?",
                options  = [
                    "filter",
                    "nat",
                    "mangle",
                    "raw",
                ],
                correct  = 0,
                explanation = "filter ist die Default-Tabelle mit INPUT, OUTPUT, FORWARD chains.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "filter=INPUT/OUTPUT/FORWARD | nat=PREROUTING/POSTROUTING | mangle=Paket-Manipulation",
        memory_tip   = "filter = Türsteher (wer darf). nat = Postbote (wohin weiterschicken).",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 30),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.02 — iptables Grundregeln
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.02",
        chapter      = 20,
        title        = "iptables: Grundregeln & Policies",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Grundregeln zuerst. Policy ACCEPT oder DROP?\n"
            " Alles erlauben und einzelnes sperren — oder umgekehrt?\n"
            " Default-deny ist die sicherere Wahl. Beginne mit dem Fundament.'"
        ),
        why_important = (
            "iptables-Grundregeln sind LPIC-1 Prüfungsthema.\n"
            "Policies, chains und Regel-Reihenfolge sind kritisch."
        ),
        explanation  = (
            "IPTABLES GRUNDREGELN:\n\n"
            "POLICY SETZEN:\n"
            "  iptables -P INPUT DROP\n"
            "  iptables -P OUTPUT ACCEPT\n"
            "  iptables -P FORWARD DROP\n\n"
            "REGELN HINZUFÜGEN:\n"
            "  iptables -A INPUT -p tcp --dport 22 -j ACCEPT   SSH erlauben\n"
            "  iptables -A INPUT -p tcp --dport 80 -j ACCEPT   HTTP erlauben\n"
            "  iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
            "  iptables -A INPUT -i lo -j ACCEPT   Loopback erlauben\n\n"
            "REGELN EINFÜGEN / LÖSCHEN:\n"
            "  iptables -I INPUT 1 -j ACCEPT  Oben einfügen\n"
            "  iptables -D INPUT 3             Regel 3 löschen\n"
            "  iptables -D INPUT -p tcp --dport 22 -j ACCEPT  Spezifisch löschen\n\n"
            "REGELN ANZEIGEN:\n"
            "  iptables -L -n -v               alle Regeln\n"
            "  iptables -L -n -v --line-numbers  mit Zeilennummern\n"
            "  iptables -L INPUT -n            nur INPUT\n\n"
            "ALLE REGELN LÖSCHEN:\n"
            "  iptables -F                     flush (alle löschen)\n"
            "  iptables -X                     benutzerdefinierte chains\n"
            "  iptables -Z                     Zähler zurücksetzen"
        ),
        syntax       = "iptables -A CHAIN -p PROTO --dport PORT -j TARGET",
        example      = "iptables -A INPUT -p tcp --dport 443 -j ACCEPT && iptables -A INPUT -j DROP",
        task_description = "Zeige iptables-Regeln mit Zeilennummern: iptables -L -n --line-numbers",
        expected_commands = ["iptables -L -n --line-numbers"],
        hint_text    = "iptables -L = List | -n = numerisch | --line-numbers = Regelnummern",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `iptables -P INPUT DROP`?",
                options  = [
                    "Setzt die Default-Policy für die INPUT chain auf DROP",
                    "Löscht alle INPUT-Regeln",
                    "Fügt eine DROP-Regel am Ende der INPUT chain ein",
                    "Blockiert alle eingehenden Pakete sofort",
                ],
                correct  = 0,
                explanation = "-P = Policy setzen. DROP als Policy = alle Pakete ohne passende Regel werden verworfen.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "iptables: -A=append -I=insert -D=delete -F=flush -P=policy -L=list -j=jump",
        memory_tip   = "ACCEPT = Ja | DROP = Nein (kein Reset) | REJECT = Nein (mit Fehlermeldung)",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.03 — iptables: NAT & Masquerading
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.03",
        chapter      = 20,
        title        = "iptables NAT & Masquerading",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Das interne Netz muss raus ins Datennetz.\n"
            " Masquerading. Ein-Weg-Tür.\n"
            " Alle internen IPs erscheinen nach außen als eine.'"
        ),
        why_important = (
            "NAT (Network Address Translation) und Masquerading sind\n"
            "fundamentale Firewall-Funktionen in jedem Router/Gateway."
        ),
        explanation  = (
            "IPTABLES NAT:\n\n"
            "IP-FORWARDING AKTIVIEREN:\n"
            "  sysctl -w net.ipv4.ip_forward=1\n"
            "  echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf\n\n"
            "MASQUERADING (SNAT dynamisch):\n"
            "  iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE\n"
            "  → Alle ausgehenden Pakete über eth0: Quell-IP ersetzen\n\n"
            "SNAT (statische Quell-IP):\n"
            "  iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source 1.2.3.4\n\n"
            "DNAT (Port-Weiterleitung):\n"
            "  iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 \\\n"
            "    -j DNAT --to-destination 192.168.1.10:80\n"
            "  → Eingehende Pakete auf Port 80 an internen Server\n\n"
            "FORWARD-REGELN FÜR NAT:\n"
            "  iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT\n"
            "  iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT\n\n"
            "NAT TABELLE ANZEIGEN:\n"
            "  iptables -t nat -L -n -v"
        ),
        syntax       = "iptables -t nat -A POSTROUTING -o ETH -j MASQUERADE",
        example      = "iptables -t nat -L -n -v && sysctl net.ipv4.ip_forward",
        task_description = "Zeige NAT-Tabelle mit iptables -t nat -L -n -v",
        expected_commands = ["iptables -t nat -L -n -v"],
        hint_text    = "iptables -t nat = nat-Tabelle | -L = list | -n -v = verbose",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Voraussetzung braucht NAT/Masquerading auf einem Linux-Router?",
                options  = [
                    "net.ipv4.ip_forward=1 muss aktiviert sein",
                    "Eine statische öffentliche IP",
                    "iptables muss als root laufen",
                    "IPSec muss konfiguriert sein",
                ],
                correct  = 0,
                explanation = "ip_forward=1 ist Pflicht damit der Kernel Pakete zwischen Interfaces weiterleitet.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "MASQUERADE=dynamisch | SNAT=statisch | DNAT=Port-Forwarding | ip_forward=1 Pflicht",
        memory_tip   = "MASQUERade = verkleiden (IP ändern). DNAT = Destination NAT = Eingehend umleiten.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.04 — iptables persistieren
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.04",
        chapter      = 20,
        title        = "iptables-save & iptables-restore",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Regeln gehen nach Reboot verloren. Das ist das Problem.\n"
            " iptables-save sichert sie. iptables-restore lädt sie.\n"
            " Persistenz. Das ist der Unterschied zwischen Sicherheit und Illusion.'"
        ),
        why_important = (
            "iptables-Regeln sind flüchtig (RAM). Persistierung über\n"
            "iptables-save/-restore oder iptables-persistent ist Pflicht."
        ),
        explanation  = (
            "IPTABLES PERSISTIERUNG:\n\n"
            "MANUELL:\n"
            "  iptables-save > /etc/iptables/rules.v4\n"
            "  iptables-restore < /etc/iptables/rules.v4\n"
            "  ip6tables-save > /etc/iptables/rules.v6\n\n"
            "DEBIAN/UBUNTU (iptables-persistent):\n"
            "  apt install iptables-persistent\n"
            "  netfilter-persistent save\n"
            "  netfilter-persistent reload\n"
            "  → Speichert in /etc/iptables/rules.v4 und rules.v6\n\n"
            "RED HAT / RHEL (iptables-services):\n"
            "  service iptables save\n"
            "  → Speichert in /etc/sysconfig/iptables\n\n"
            "FORMAT:\n"
            "  # Generated by iptables-save\n"
            "  *filter\n"
            "  :INPUT DROP [0:0]\n"
            "  :FORWARD DROP [0:0]\n"
            "  :OUTPUT ACCEPT [0:0]\n"
            "  -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
            "  COMMIT\n\n"
            "SYSTEMD (für systemd-Systeme):\n"
            "  /etc/systemd/system/iptables-restore.service"
        ),
        syntax       = "iptables-save > /etc/iptables/rules.v4",
        example      = "iptables-save > /etc/iptables/rules.v4 && cat /etc/iptables/rules.v4 | head -20",
        task_description = "Speichere iptables-Regeln mit iptables-save (Ausgabe anzeigen)",
        expected_commands = ["iptables-save"],
        hint_text    = "iptables-save gibt die Regeln auf stdout aus. Mit > in Datei umleiten.",
        quiz_questions = [
            QuizQuestion(
                question = "Welches Paket macht iptables-Regeln auf Debian/Ubuntu beim Boot persistent?",
                options  = [
                    "iptables-persistent",
                    "iptables-save",
                    "netfilter-save",
                    "firewall-rules",
                ],
                correct  = 0,
                explanation = "iptables-persistent (Debian/Ubuntu) speichert Regeln in /etc/iptables/rules.v4.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "iptables-save=exportieren | iptables-restore=laden | iptables-persistent=Debian-Paket",
        memory_tip   = "save = sichern | restore = wiederherstellen. Ohne Persistierung: Reboot = alles weg.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.05 — nftables: Moderne Firewall
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.05",
        chapter      = 20,
        title        = "nftables: Moderner Firewall-Standard",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'iptables ist alt. nftables ist die Zukunft.\n"
            " Debian 10+. Ubuntu 20.04+. Red Hat 8+.\n"
            " Ein Framework für alle Protokolle. Kein Wildwuchs mehr.'"
        ),
        why_important = (
            "nftables ist der moderne Ersatz für iptables/ip6tables/arptables.\n"
            "Seit Kernel 3.13, Standard in modernen Distributionen."
        ),
        explanation  = (
            "NFTABLES GRUNDLAGEN:\n\n"
            "STATUS:\n"
            "  nft list ruleset        Alle Regeln anzeigen\n"
            "  nft list tables         Alle Tabellen\n"
            "  nft list table inet filter  Bestimmte Tabelle\n\n"
            "TABELLE & CHAIN ERSTELLEN:\n"
            "  nft add table inet filter\n"
            "  nft add chain inet filter input { type filter hook input priority 0 \\; policy drop \\; }\n"
            "  nft add chain inet filter output { type filter hook output priority 0 \\; policy accept \\; }\n\n"
            "REGELN HINZUFÜGEN:\n"
            "  nft add rule inet filter input tcp dport 22 accept\n"
            "  nft add rule inet filter input tcp dport { 80, 443 } accept\n"
            "  nft add rule inet filter input ct state established,related accept\n"
            "  nft add rule inet filter input iif lo accept\n\n"
            "REGEL LÖSCHEN:\n"
            "  nft delete rule inet filter input handle 3\n"
            "  (Handle mit: nft list ruleset -a)\n\n"
            "PERSISTIERUNG:\n"
            "  nft list ruleset > /etc/nftables.conf\n"
            "  systemctl enable nftables\n"
            "  /etc/nftables.conf"
        ),
        syntax       = "nft add rule TABLE CHAIN MATCH ACTION",
        example      = "nft list ruleset && nft add rule inet filter input tcp dport 22 accept",
        task_description = "Zeige nftables-Regelwerk mit nft list ruleset",
        expected_commands = ["nft list ruleset"],
        hint_text    = "nft list ruleset zeigt das vollständige nftables-Regelwerk",
        quiz_questions = [
            QuizQuestion(
                question = "Was ersetzt nftables auf modernen Linux-Systemen?",
                options  = [
                    "iptables, ip6tables, arptables und ebtables",
                    "nur iptables",
                    "firewalld",
                    "ufw",
                ],
                correct  = 0,
                explanation = "nftables ersetzt alle netfilter-Userspace-Tools: iptables, ip6tables, arptables, ebtables.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "nft list ruleset = alle Regeln | inet = IPv4+IPv6 | nftables seit Debian 10 Standard",
        memory_tip   = "nft = nftables CLI. inet = internet (v4+v6). table → chain → rule.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.06 — firewalld: Dynamic Firewall
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.06",
        chapter      = 20,
        title        = "firewalld: Zones & Services",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Red Hat Systeme. CentOS. Fedora. Rocky Linux.\n"
            " Alle nutzen firewalld. Zones definieren Vertrauensstufen.\n"
            " Services abstrahieren Ports. Konfiguriere Zonen, nicht Ports.'"
        ),
        why_important = (
            "firewalld ist die Standard-Firewall auf Red Hat-basierten Systemen.\n"
            "Zones und Services vereinfachen Firewall-Management."
        ),
        explanation  = (
            "FIREWALLD — ZONES & SERVICES:\n\n"
            "VORDEFINIERTE ZONES:\n"
            "  drop      Alle eingehenden Pakete verworfen\n"
            "  block     Eingehende abgelehnt (icmp-host-prohibited)\n"
            "  public    Öffentliches Netz, nur erlaubte Services\n"
            "  external  NAT aktiviert\n"
            "  internal  Internes Netz, mehr Vertrauen\n"
            "  trusted   Alle Verbindungen erlaubt\n\n"
            "GRUNDBEFEHLE:\n"
            "  firewall-cmd --state\n"
            "  firewall-cmd --get-active-zones\n"
            "  firewall-cmd --get-default-zone\n"
            "  firewall-cmd --set-default-zone=public\n\n"
            "SERVICES:\n"
            "  firewall-cmd --list-services\n"
            "  firewall-cmd --add-service=ssh\n"
            "  firewall-cmd --remove-service=ssh\n"
            "  firewall-cmd --add-service=ssh --permanent\n\n"
            "PORTS:\n"
            "  firewall-cmd --add-port=8080/tcp\n"
            "  firewall-cmd --add-port=8080/tcp --permanent\n\n"
            "PERMANENT & RELOAD:\n"
            "  --permanent  → dauerhaft (braucht reload)\n"
            "  firewall-cmd --reload"
        ),
        syntax       = "firewall-cmd --add-service=SERVICE [--permanent]",
        example      = "firewall-cmd --get-active-zones && firewall-cmd --list-all",
        task_description = "Zeige aktive Zonen mit firewall-cmd --get-active-zones",
        expected_commands = ["firewall-cmd --get-active-zones"],
        hint_text    = "firewall-cmd --get-active-zones zeigt welche Zone welchem Interface zugeordnet ist",
        quiz_questions = [
            QuizQuestion(
                question = "Was bewirkt `--permanent` bei firewall-cmd?",
                options  = [
                    "Regel ist dauerhaft gespeichert, wird aber erst nach --reload aktiv",
                    "Regel ist sofort und dauerhaft aktiv",
                    "Regel kann nicht gelöscht werden",
                    "Regel gilt für alle Zones",
                ],
                correct  = 0,
                explanation = "--permanent speichert dauerhaft. Ohne --reload wirkt sie erst nach Neustart. --reload sofort aktivieren.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "--permanent = dauerhaft aber Reload nötig! firewall-cmd --reload = Runtime aktualisieren",
        memory_tip   = "Ohne --permanent: nur bis Reboot. Mit --permanent + --reload: dauerhaft + sofort.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.07 — UFW: Uncomplicated Firewall
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.07",
        chapter      = 20,
        title        = "UFW: Uncomplicated Firewall",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Ubuntu-Systeme. Einfache Konfiguration.\n"
            " ufw abstrahiert iptables. Für schnelle Setups.\n"
            " Nicht für komplexe Firewalls — aber für 80% der Fälle reicht es.'"
        ),
        why_important = (
            "UFW (Uncomplicated Firewall) ist die Standard-Firewall auf Ubuntu.\n"
            "Einfache Syntax für schnelle Basis-Konfiguration."
        ),
        explanation  = (
            "UFW — UNCOMPLICATED FIREWALL:\n\n"
            "AKTIVIEREN/DEAKTIVIEREN:\n"
            "  ufw enable\n"
            "  ufw disable\n"
            "  ufw status\n"
            "  ufw status verbose\n"
            "  ufw status numbered\n\n"
            "REGELN:\n"
            "  ufw allow ssh\n"
            "  ufw allow 22/tcp\n"
            "  ufw allow from 192.168.1.0/24\n"
            "  ufw allow from 192.168.1.0/24 to any port 22\n"
            "  ufw deny 23\n"
            "  ufw delete allow ssh\n"
            "  ufw delete 3          Regel Nr. 3 löschen\n\n"
            "DEFAULT POLICIES:\n"
            "  ufw default deny incoming\n"
            "  ufw default allow outgoing\n\n"
            "LOGGING:\n"
            "  ufw logging on\n"
            "  ufw logging medium\n"
            "  /var/log/ufw.log\n\n"
            "RESET:\n"
            "  ufw reset          Alle Regeln löschen"
        ),
        syntax       = "ufw allow|deny SERVICE|PORT[/proto]",
        example      = "ufw allow ssh && ufw allow 80/tcp && ufw status verbose",
        task_description = "Zeige UFW-Status mit ufw status verbose",
        expected_commands = ["ufw status verbose"],
        hint_text    = "ufw status verbose zeigt alle Regeln und Status",
        quiz_questions = [
            QuizQuestion(
                question = "Wie erlaubt man mit ufw nur SSH-Zugriff aus dem Netz 192.168.1.0/24?",
                options  = [
                    "ufw allow from 192.168.1.0/24 to any port 22",
                    "ufw allow 22 from 192.168.1.0/24",
                    "ufw add 192.168.1.0/24 ssh",
                    "ufw allow ssh --source 192.168.1.0/24",
                ],
                correct  = 0,
                explanation = "Syntax: ufw allow from SOURCE to any port DEST_PORT",
                xp_value = 15,
            ),
        ],
        exam_tip     = "ufw allow/deny. ufw default deny incoming + allow outgoing = Standard-Policy",
        memory_tip   = "UFW = Uncomplicated. Einfache Syntax für schnelle Setups. Intern: iptables.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.08 — Connection Tracking & Stateful Firewall
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.08",
        chapter      = 20,
        title        = "Connection Tracking: Stateful Firewall",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Stateless vs Stateful. Den Unterschied kennst du?\n"
            " conntrack verfolgt Verbindungszustände.\n"
            " ESTABLISHED, RELATED — das macht eine smarte Firewall.'"
        ),
        why_important = (
            "Connection Tracking (conntrack) ermöglicht stateful Firewalls.\n"
            "ESTABLISHED/RELATED-Regeln sind fundamental für korrekte Konfiguration."
        ),
        explanation  = (
            "CONNECTION TRACKING:\n\n"
            "VERBINDUNGSZUSTÄNDE:\n"
            "  NEW          Neue Verbindung (kein vorangehender Paketaustausch)\n"
            "  ESTABLISHED  Bestehende Verbindung (Antwort-Pakete)\n"
            "  RELATED      Verwandte Verbindung (z.B. FTP Daten-Kanal)\n"
            "  INVALID      Ungültiges Paket (kein bekannter Zustand)\n\n"
            "STANDARD-REGELN:\n"
            "  iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
            "  iptables -A INPUT -m state --state INVALID -j DROP\n"
            "  iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\n\n"
            "CONNTRACK TOOL:\n"
            "  conntrack -L             Verbindungstabelle anzeigen\n"
            "  conntrack -D -s 1.2.3.4  Einträge löschen\n"
            "  cat /proc/net/nf_conntrack  Kernel-Tabelle\n\n"
            "MAXIMALE VERBINDUNGEN:\n"
            "  sysctl net.netfilter.nf_conntrack_max\n"
            "  sysctl net.netfilter.nf_conntrack_count  (aktuell)\n\n"
            "WICHTIG:\n"
            "  Ohne ESTABLISHED-Regel: Antwort-Pakete werden geblockt!\n"
            "  Immer zuerst ESTABLISHED/RELATED erlauben."
        ),
        syntax       = "iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
        example      = "iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT",
        task_description = "Zeige Connection-Tracking-Tabelle mit conntrack -L | head -10",
        expected_commands = ["conntrack -L"],
        hint_text    = "conntrack -L zeigt alle aktuell getrackten Verbindungen",
        quiz_questions = [
            QuizQuestion(
                question = "Warum ist eine ESTABLISHED,RELATED-Regel wichtig?",
                options  = [
                    "Damit Antwortpakete auf erlaubte ausgehende Verbindungen ankommen",
                    "Um neue Verbindungen zu blockieren",
                    "Für FTP aktiv-Modus",
                    "Für NAT-Verbindungen",
                ],
                correct  = 0,
                explanation = "Ohne ESTABLISHED,RELATED: Antwort-Pakete werden geblockt weil sie 'eingehend' sind.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "NEW=erste Pakete | ESTABLISHED=Antworten | RELATED=verwandte (FTP) | INVALID=Mülleimer",
        memory_tip   = "ESTABLISHED = bekannte Verbindung. RELATED = Verwandte (like FTP-Data zu FTP-Control).",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.09 — Netzwerk-Diagnose: tcpdump & Wireshark
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.09",
        chapter      = 20,
        title        = "Paket-Analyse: tcpdump",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Die Firewall blockt etwas. Aber was?\n"
            " tcpdump. Paket-Sniffer. Direkt am Interface.\n"
            " Was geht rein? Was kommt raus? Was wird geblockt?'"
        ),
        why_important = (
            "tcpdump ist das Standard-Tool für Paketanalyse auf Linux.\n"
            "Unverzichtbar für Firewall-Debugging und Netzwerk-Diagnose."
        ),
        explanation  = (
            "TCPDUMP GRUNDLAGEN:\n\n"
            "EINFACHE NUTZUNG:\n"
            "  tcpdump -i eth0         Pakete auf eth0 erfassen\n"
            "  tcpdump -i any          Alle Interfaces\n"
            "  tcpdump -i eth0 -n      Keine DNS-Auflösung\n"
            "  tcpdump -i eth0 -nn     Keine DNS + keine Service-Namen\n\n"
            "FILTER:\n"
            "  tcpdump -i eth0 tcp port 22\n"
            "  tcpdump -i eth0 host 192.168.1.1\n"
            "  tcpdump -i eth0 src 192.168.1.1\n"
            "  tcpdump -i eth0 dst 8.8.8.8\n"
            "  tcpdump -i eth0 'tcp and (port 80 or port 443)'\n"
            "  tcpdump -i eth0 not arp\n\n"
            "IN DATEI SCHREIBEN:\n"
            "  tcpdump -i eth0 -w capture.pcap\n"
            "  tcpdump -r capture.pcap     Lesen\n"
            "  (Dateien mit Wireshark öffnen)\n\n"
            "PAKETANZAHL BEGRENZEN:\n"
            "  tcpdump -i eth0 -c 100  100 Pakete erfassen dann stoppen\n\n"
            "AUSFÜHRLICHKEIT:\n"
            "  tcpdump -v   verbose\n"
            "  tcpdump -vv  mehr verbose\n"
            "  tcpdump -A   ASCII-Inhalt anzeigen"
        ),
        syntax       = "tcpdump -i INTERFACE [FILTER]",
        example      = "tcpdump -i eth0 -nn -c 20 tcp port 22",
        task_description = "Zeige Paketerfassung mit tcpdump -i lo -c 5 (loopback, 5 Pakete)",
        expected_commands = ["tcpdump -i lo"],
        hint_text    = "tcpdump -i lo -c 5 erfasst 5 Pakete auf dem Loopback-Interface",
        quiz_questions = [
            QuizQuestion(
                question = "Was bedeutet `-nn` bei tcpdump?",
                options  = [
                    "Keine DNS-Auflösung UND keine Service-Namen (nur Zahlen)",
                    "Keine Ausgabe",
                    "Numerische Paketgrößen",
                    "Nur neue Verbindungen",
                ],
                correct  = 0,
                explanation = "-n = kein DNS. -nn = kein DNS + keine Port-Namen (z.B. 22 statt ssh).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "tcpdump -i IF = Interface | -w = write .pcap | -r = read | -n/-nn = numerisch",
        memory_tip   = "tcpdump -w = write (speichern für Wireshark). -nn = alles numerisch (schneller).",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.10 — Nmap: Netzwerk-Scanning
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.10",
        chapter      = 20,
        title        = "nmap: Netzwerk-Scanner & Port-Audit",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Kenne dein Netzwerk bevor der Feind es tut.\n"
            " nmap. Netzwerk-Mapper. Ports. Services. OS-Detection.\n"
            " Dein Perimeter-Audit beginnt hier.'"
        ),
        why_important = (
            "nmap ist das Standard-Tool für Netzwerk-Reconnaissance.\n"
            "Unverzichtbar für Security Audits und Firewall-Verifikation."
        ),
        explanation  = (
            "NMAP GRUNDLAGEN:\n\n"
            "BASIS-SCANS:\n"
            "  nmap HOST           Default-Scan (TCP SYN, 1000 Ports)\n"
            "  nmap -sn 192.168.1.0/24  Ping-Scan (Hosts finden)\n"
            "  nmap -p 22,80,443 HOST   Bestimmte Ports\n"
            "  nmap -p 1-1000 HOST      Port-Range\n"
            "  nmap -p- HOST            Alle 65535 Ports\n\n"
            "SCAN-TYPEN:\n"
            "  nmap -sS HOST     SYN-Scan (stealth, root nötig)\n"
            "  nmap -sT HOST     TCP-Connect-Scan (kein root)\n"
            "  nmap -sU HOST     UDP-Scan\n"
            "  nmap -sV HOST     Service-Version-Erkennung\n"
            "  nmap -O HOST      OS-Erkennung (root nötig)\n"
            "  nmap -A HOST      Aggressiv (Version + OS + Scripts)\n\n"
            "OUTPUT:\n"
            "  nmap -oN scan.txt     Normal-Format\n"
            "  nmap -oX scan.xml     XML\n"
            "  nmap -oG scan.gnmap   Greippable\n\n"
            "GESCHWINDIGKEIT:\n"
            "  -T0 bis -T5 (T3=default, T4=schnell, T5=sehr aggressiv)"
        ),
        syntax       = "nmap [OPTIONS] ZIEL",
        example      = "nmap -sS -sV -p 22,80,443 localhost",
        task_description = "Scanne localhost mit nmap -sT localhost",
        expected_commands = ["nmap -sT localhost"],
        hint_text    = "nmap -sT localhost = TCP-Connect-Scan auf localhost (kein root nötig)",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `nmap -sn 192.168.1.0/24`?",
                options  = [
                    "Ping-Scan: findet aktive Hosts ohne Port-Scan",
                    "SYN-Scan auf alle 24 Ports",
                    "Scannt alle 65535 Ports im /24-Netz",
                    "UDP-Scan auf das Netz",
                ],
                correct  = 0,
                explanation = "-sn = no port scan. Nur Ping/ARP um aktive Hosts zu finden. Früher: -sP.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "nmap -sS=SYN(root) -sT=TCP(no root) -sV=Version -O=OS -A=alles -sn=nur Hosts",
        memory_tip   = "-sn = scan no ports (nur Hosts). -sV = scan Version. -A = Alles.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.11 — OpenVPN Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.11",
        chapter      = 20,
        title        = "OpenVPN: Verschlüsselte Tunnel",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Das Fernzugriff-Problem. Public Network. Daten im Klartext.\n"
            " OpenVPN schafft einen verschlüsselten Tunnel.\n"
            " Alle Daten durch diesen Tunnel. Abhörsicher.'"
        ),
        why_important = (
            "VPN (Virtual Private Network) ist Standard für sicheren Fernzugriff.\n"
            "OpenVPN ist die meistgenutzte Open-Source VPN-Lösung."
        ),
        explanation  = (
            "OPENVPN GRUNDLAGEN:\n\n"
            "INSTALLATION:\n"
            "  apt install openvpn\n\n"
            "CLIENT:\n"
            "  openvpn --config client.ovpn\n"
            "  openvpn --config client.ovpn --daemon\n\n"
            "CONFIG-DATEI (.ovpn / .conf):\n"
            "  client\n"
            "  dev tun\n"
            "  proto udp\n"
            "  remote vpn.example.com 1194\n"
            "  ca ca.crt\n"
            "  cert client.crt\n"
            "  key client.key\n"
            "  tls-auth ta.key 1\n\n"
            "SERVER CONFIG:\n"
            "  /etc/openvpn/server.conf\n"
            "  server 10.8.0.0 255.255.255.0\n"
            "  push 'redirect-gateway def1'\n"
            "  push 'dhcp-option DNS 8.8.8.8'\n\n"
            "SYSTEMD:\n"
            "  systemctl start openvpn@client\n"
            "  systemctl enable openvpn@server\n\n"
            "WIREGUARD (moderner):\n"
            "  wg-quick up wg0\n"
            "  wg show"
        ),
        syntax       = "openvpn --config DATEI.ovpn",
        example      = "openvpn --config /etc/openvpn/client.ovpn --daemon && ip addr show tun0",
        task_description = "Zeige OpenVPN-Config-Optionen mit openvpn --help | head -20",
        expected_commands = ["openvpn --help"],
        hint_text    = "openvpn --help zeigt alle Optionen",
        quiz_questions = [
            QuizQuestion(
                question = "Welches Interface erstellt OpenVPN typischerweise für den VPN-Tunnel?",
                options  = [
                    "tun0 (routed VPN) oder tap0 (bridged VPN)",
                    "eth0",
                    "vpn0",
                    "lo",
                ],
                correct  = 0,
                explanation = "tun = Layer 3 (routed). tap = Layer 2 (bridged). tun0 ist Standard für Client-VPN.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "OpenVPN Port 1194/UDP default. tun=geroutet. tap=bridged. /etc/openvpn/*.conf",
        memory_tip   = "tun = Tunnel (IP-Level). tap = Tapete (Ethernet-Level). Client.ovpn = vollständige Config.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.12 — IDS/IPS: Snort & Suricata
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.12",
        chapter      = 20,
        title        = "IDS/IPS: Intrusion Detection Grundlagen",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Firewall blockt bekannte Angriffe. IDS erkennt unbekannte.\n"
            " Anomalie-Erkennung. Signatur-basiert.\n"
            " Snort. Suricata. Der Unterschied zwischen IDS und IPS.'"
        ),
        why_important = (
            "IDS (Intrusion Detection) und IPS (Intrusion Prevention) sind\n"
            "wichtige Sicherheitskonzepte im LPIC-1 Sicherheitskapitel."
        ),
        explanation  = (
            "IDS vs IPS:\n\n"
            "IDS (Intrusion Detection System):\n"
            "  Passiv: erkennt und meldet Angriffe\n"
            "  Kein Eingriff in den Traffic\n"
            "  Beispiel: Snort im IDS-Modus\n\n"
            "IPS (Intrusion Prevention System):\n"
            "  Aktiv: erkennt UND blockt Angriffe\n"
            "  Inline im Traffic-Pfad\n"
            "  Beispiel: Snort/Suricata als IPS\n\n"
            "NIDS (Network-based) vs HIDS (Host-based):\n"
            "  NIDS: überwacht Netzwerk-Traffic\n"
            "  HIDS: überwacht Host-Aktivitäten (Dateien, Logs, Prozesse)\n"
            "  AIDE: Host-based IDS (Datei-Integritätsprüfung)\n\n"
            "SNORT:\n"
            "  snort -A console -q -c /etc/snort/snort.conf -i eth0\n\n"
            "AIDE (Host IDS):\n"
            "  aide --init    Datenbank initialisieren\n"
            "  aide --check   Änderungen prüfen\n\n"
            "OSSEC/WAZUH:\n"
            "  HIDS mit Log-Analyse, Rootkit-Detection, Policy-Monitoring"
        ),
        syntax       = "aide --check  (Host-IDS Integritätsprüfung)",
        example      = "aide --check 2>&1 | grep -E 'changed|added|removed'",
        task_description = "Zeige aide-Optionen mit aide --help | head -20",
        expected_commands = ["aide --help"],
        hint_text    = "aide --help zeigt alle AIDE-Optionen",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Unterschied zwischen IDS und IPS?",
                options  = [
                    "IDS erkennt und meldet, IPS erkennt und blockt",
                    "IDS ist hardwarebasiert, IPS softwarebasiert",
                    "IDS schützt Hosts, IPS schützt Netzwerke",
                    "IDS ist passiv intern, IPS ist aktiv extern",
                ],
                correct  = 0,
                explanation = "IDS = passiv (detect only). IPS = aktiv inline (detect + prevent).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "IDS=erkennen | IPS=erkennen+blockieren | NIDS=Netz | HIDS=Host | AIDE=Datei-Integrität",
        memory_tip   = "IDS = Alarm. IPS = Alarm + Aktion. AIDE = Diff deines Dateisystems.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.13 — Reverse Proxy & Load Balancer Security
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.13",
        chapter      = 20,
        title        = "Reverse Proxy: nginx als Sicherheits-Layer",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Schreibe den Webserver nicht direkt ins Internet.\n"
            " nginx davor. Reverse Proxy. TLS-Termination.\n"
            " Rate-Limiting. DDoS-Schutz. Sicherheits-Layer.'"
        ),
        why_important = (
            "Reverse Proxies schützen Backend-Server durch Abstraktion und\n"
            "zentralisierte TLS-Termination, Rate-Limiting und Access-Control."
        ),
        explanation  = (
            "NGINX ALS REVERSE PROXY:\n\n"
            "BASIC PROXY CONFIG:\n"
            "  server {\n"
            "    listen 443 ssl;\n"
            "    server_name example.com;\n"
            "    ssl_certificate /etc/ssl/certs/cert.crt;\n"
            "    ssl_certificate_key /etc/ssl/private/key.key;\n"
            "    location / {\n"
            "      proxy_pass http://127.0.0.1:8080;\n"
            "      proxy_set_header Host $host;\n"
            "      proxy_set_header X-Real-IP $remote_addr;\n"
            "    }\n"
            "  }\n\n"
            "RATE LIMITING:\n"
            "  limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;\n"
            "  limit_req zone=api burst=20 nodelay;\n\n"
            "IP-BLOCKING:\n"
            "  deny 1.2.3.4;\n"
            "  allow 192.168.1.0/24;\n"
            "  deny all;\n\n"
            "SICHERHEITS-HEADER:\n"
            "  add_header X-Frame-Options DENY;\n"
            "  add_header X-Content-Type-Options nosniff;\n"
            "  add_header X-XSS-Protection '1; mode=block';\n"
            "  add_header Strict-Transport-Security 'max-age=31536000';"
        ),
        syntax       = "proxy_pass http://BACKEND;  (in nginx location block)",
        example      = "nginx -t && systemctl reload nginx && curl -I https://localhost",
        task_description = "Prüfe nginx-Konfiguration mit nginx -t",
        expected_commands = ["nginx -t"],
        hint_text    = "nginx -t prüft die Konfiguration auf Syntaxfehler",
        quiz_questions = [
            QuizQuestion(
                question = "Was macht `proxy_pass http://127.0.0.1:8080` in nginx?",
                options  = [
                    "Leitet Anfragen an den Backend-Server auf Port 8080 weiter",
                    "Öffnet Port 8080 auf dem Server",
                    "Redirects HTTP auf HTTPS",
                    "Startet nginx auf Port 8080",
                ],
                correct  = 0,
                explanation = "proxy_pass leitet die Anfrage transparent an das Backend weiter (Reverse Proxy).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "nginx -t = Config-Test. proxy_pass = Weiterleitung. limit_req = Rate-Limiting.",
        memory_tip   = "Reverse Proxy: Client → nginx (public) → Backend (privat). nginx = Türsteher.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.14 — Netzwerk-Troubleshooting Workflow
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.14",
        chapter      = 20,
        title        = "Netzwerk-Troubleshooting: Systematisch vorgehen",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'Verbindung tot. Wo ist das Problem?\n"
            " Layer 1 bis 7. Systematisch. Niemals raten.\n"
            " Ich zeige dir den Troubleshooting-Baum der Profis.'"
        ),
        why_important = (
            "Systematisches Netzwerk-Troubleshooting ist eine Kernkompetenz.\n"
            "LPIC-1 testet die richtigen Tools für jeden Layer."
        ),
        explanation  = (
            "NETZWERK-TROUBLESHOOTING WORKFLOW:\n\n"
            "1. LAYER 1/2 (Physisch/Datalink):\n"
            "  ip link show         Interface-Status (UP/DOWN)\n"
            "  ethtool eth0         Verbindungsgeschwindigkeit, Duplex\n"
            "  dmesg | grep eth0    Treiber-Fehler\n\n"
            "2. LAYER 3 (Netzwerk/IP):\n"
            "  ip addr show         IP-Adressen\n"
            "  ip route show        Routing-Tabelle\n"
            "  ping 127.0.0.1       Loopback OK?\n"
            "  ping GATEWAY         Gateway erreichbar?\n"
            "  ping 8.8.8.8         Internet erreichbar?\n\n"
            "3. LAYER 4 (Transport/TCP):\n"
            "  ss -tulpn            Offene Ports/Dienste\n"
            "  nc -zv HOST PORT     TCP-Verbindung testen\n"
            "  telnet HOST PORT     Verbindungstest\n\n"
            "4. DNS:\n"
            "  dig google.com       DNS-Auflösung\n"
            "  dig @8.8.8.8 google.com  Mit spez. Resolver\n"
            "  host google.com      Alternative\n\n"
            "5. ROUTING:\n"
            "  traceroute HOST      Paketweg verfolgen\n"
            "  mtr HOST             Kombiniert ping + traceroute\n\n"
            "6. FIREWALL:\n"
            "  iptables -L -n       Regeln prüfen\n"
            "  tcpdump -i eth0 dst HOST  Pakete sniffen"
        ),
        syntax       = "ping → ip route → ss -tulpn → dig → traceroute",
        example      = "ping -c4 8.8.8.8 && dig google.com && traceroute 8.8.8.8",
        task_description = "Prüfe Netzwerk-Konnektivität: ping -c 3 127.0.0.1",
        expected_commands = ["ping -c 3 127.0.0.1"],
        hint_text    = "ping -c 3 127.0.0.1 prüft Loopback (muss immer funktionieren)",
        quiz_questions = [
            QuizQuestion(
                question = "In welcher Reihenfolge sollte Netzwerk-Troubleshooting erfolgen?",
                options  = [
                    "Physisch (L1) → IP (L3) → DNS (L7) → Anwendung",
                    "DNS → IP → Firewall → Physisch",
                    "Anwendung → DNS → IP → Physisch (von oben nach unten)",
                    "Immer mit DNS beginnen",
                ],
                correct  = 0,
                explanation = "Bottom-up: L1 (Kabel), L2 (Interface), L3 (IP/Route), L4 (Port), L7 (DNS/App).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "Bottom-up: L1→L2→L3→L4→L7. ping=L3 | ss=L4 | dig=DNS | traceroute=Routing",
        memory_tip   = "Beginne immer unten (physisch) und arbeite dich nach oben. Loopback-Test zuerst.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.15 — WireGuard: Modernes VPN
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.15",
        chapter      = 20,
        title        = "WireGuard: Modernes VPN-Protokoll",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'OpenVPN ist komplex. WireGuard ist elegant.\n"
            " 4000 Zeilen Code statt 400.000. Schnell. Sicher. Modern.\n"
            " In Linux-Kernel integriert seit 5.6.'"
        ),
        why_important = (
            "WireGuard ist das modernste VPN-Protokoll — im Linux-Kernel integriert.\n"
            "Einfachere Konfiguration und bessere Performance als OpenVPN."
        ),
        explanation  = (
            "WIREGUARD:\n\n"
            "INSTALLATION:\n"
            "  apt install wireguard\n"
            "  (Kernel 5.6+ hat WireGuard eingebaut)\n\n"
            "SCHLÜSSEL GENERIEREN:\n"
            "  wg genkey | tee privatekey | wg pubkey > publickey\n"
            "  cat privatekey   Private Key\n"
            "  cat publickey    Public Key\n\n"
            "KONFIGURATION (/etc/wireguard/wg0.conf):\n"
            "  [Interface]\n"
            "  PrivateKey = <client-private-key>\n"
            "  Address = 10.0.0.2/24\n"
            "  DNS = 1.1.1.1\n\n"
            "  [Peer]\n"
            "  PublicKey = <server-public-key>\n"
            "  Endpoint = vpn.example.com:51820\n"
            "  AllowedIPs = 0.0.0.0/0\n\n"
            "VERBINDUNG:\n"
            "  wg-quick up wg0\n"
            "  wg-quick down wg0\n"
            "  systemctl enable wg-quick@wg0\n\n"
            "STATUS:\n"
            "  wg show\n"
            "  wg show wg0"
        ),
        syntax       = "wg-quick up wg0  /  wg show",
        example      = "wg genkey | tee private.key | wg pubkey > public.key && cat public.key",
        task_description = "Zeige WireGuard-Status mit wg show",
        expected_commands = ["wg show"],
        hint_text    = "wg show zeigt alle WireGuard-Interfaces und Verbindungsstatus",
        quiz_questions = [
            QuizQuestion(
                question = "Wie generiert man ein WireGuard-Schlüsselpaar?",
                options  = [
                    "wg genkey | tee privatekey | wg pubkey > publickey",
                    "wg-keygen --output wg0",
                    "openssl genrsa -out wireguard.key 4096",
                    "ssh-keygen -t ed25519 -f wg.key",
                ],
                correct  = 0,
                explanation = "wg genkey erzeugt Private Key. wg pubkey leitet den Public Key ab.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "wg genkey | wg pubkey. wg-quick up/down. /etc/wireguard/wg0.conf. Port 51820/UDP.",
        memory_tip   = "WireGuard = modernes VPN. Kernel-integriert ab 5.6. wg-quick = einfache Verwaltung.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.16 — Härtung: CIS Benchmarks & Sicherheits-Checkliste
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.16",
        chapter      = 20,
        title        = "System-Härtung: CIS Benchmark Checkliste",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Ein System ist nur so sicher wie sein schwächstes Glied.\n"
            " Härtung. Schicht für Schicht.\n"
            " CIS Benchmarks sind der Standard. Kenne sie.'"
        ),
        why_important = (
            "System-Härtung reduziert die Angriffsfläche systematisch.\n"
            "CIS Benchmarks sind der Industry-Standard für Linux-Härtung."
        ),
        explanation  = (
            "LINUX HÄRTUNGS-CHECKLISTE:\n\n"
            "BENUTZER & AUTHENTICATION:\n"
            "  PermitRootLogin no in sshd_config\n"
            "  PasswordAuthentication no (nur Keys)\n"
            "  MaxAuthTries 3\n"
            "  passwd -l root (Root-Login sperren)\n\n"
            "SYSCTL HÄRTUNG:\n"
            "  net.ipv4.ip_forward=0 (kein Router)\n"
            "  net.ipv4.tcp_syncookies=1 (SYN-Flood-Schutz)\n"
            "  kernel.randomize_va_space=2 (ASLR)\n"
            "  kernel.dmesg_restrict=1\n\n"
            "DIENSTE DEAKTIVIEREN:\n"
            "  systemctl disable avahi-daemon\n"
            "  systemctl disable cups (wenn kein Drucker)\n"
            "  systemctl disable bluetooth\n"
            "  systemctl mask nfs-server (wenn nicht genutzt)\n\n"
            "DATEIBERECHTIGUNGEN:\n"
            "  chmod 700 /root\n"
            "  chmod 600 /etc/shadow\n"
            "  chmod 644 /etc/passwd\n"
            "  find / -perm -4000 -type f 2>/dev/null | audit-suid\n\n"
            "PAKETE:\n"
            "  Nur nötige Pakete installieren\n"
            "  apt autoremove; apt purge telnet rsh-client"
        ),
        syntax       = "systemctl disable DIENST  ||  chmod PERMS /pfad",
        example      = "systemctl --failed && find / -perm -4000 -type f 2>/dev/null | head -20",
        task_description = "Zeige fehlgeschlagene Services mit systemctl --failed",
        expected_commands = ["systemctl --failed"],
        hint_text    = "systemctl --failed zeigt alle Services die nicht starten konnten",
        quiz_questions = [
            QuizQuestion(
                question = "Welcher sysctl-Parameter aktiviert SYN-Flood-Schutz?",
                options  = [
                    "net.ipv4.tcp_syncookies=1",
                    "net.ipv4.ip_forward=0",
                    "kernel.randomize_va_space=2",
                    "net.ipv4.conf.all.rp_filter=1",
                ],
                correct  = 0,
                explanation = "tcp_syncookies=1 aktiviert SYN Cookies. Bei SYN-Flood: kein Speicher für halboffene Verbindungen.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "PermitRootLogin no. tcp_syncookies=1. ASLR=randomize_va_space=2. Unnötige Dienste deaktivieren.",
        memory_tip   = "Härtung = Angriffsfläche minimieren. Jeder unnötige Dienst = potenzielle Schwachstelle.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.17 — IPv6 Sicherheit & Firewall
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.17",
        chapter      = 20,
        title        = "IPv6 Sicherheit & ip6tables",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "VECTOR",
        story        = (
            "VECTOR: 'IPv6 ist da. Kein NAT. Jedes Gerät direkt erreichbar.\n"
            " ip6tables. Separate Regeln für IPv6.\n"
            " Wer IPv6 vergisst, lässt die Hintertür offen.'"
        ),
        why_important = (
            "IPv6 erfordert separate Firewall-Regeln (ip6tables).\n"
            "Ohne IPv6-Firewall sind Hosts direkt aus dem Internet erreichbar."
        ),
        explanation  = (
            "IPV6 SICHERHEIT:\n\n"
            "IP6TABLES (Pendant zu iptables für IPv6):\n"
            "  ip6tables -L -n -v\n"
            "  ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT\n"
            "  ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n"
            "  ip6tables -P INPUT DROP\n\n"
            "NFTABLES (IPv4+IPv6 in einem):\n"
            "  inet-Familie = IPv4 + IPv6 gleichzeitig\n"
            "  nft add table inet filter  (deckt beide ab)\n\n"
            "IPV6-ADRESSEN:\n"
            "  Link-Local:  fe80::/10 (nicht routbar)\n"
            "  ULA:         fc00::/7  (privat)\n"
            "  Global:      2000::/3  (öffentlich)\n"
            "  Loopback:    ::1\n"
            "  Alle Hosts:  ff02::1\n\n"
            "SICHERHEITSASPEKTE:\n"
            "  Kein NAT → jede IPv6-Adresse global erreichbar\n"
            "  ICMPv6 nicht komplett blockieren (NDP braucht es)\n"
            "  Router Advertisements (RA) können Angriffspunkt sein\n\n"
            "DEAKTIVIEREN (wenn kein IPv6 nötig):\n"
            "  net.ipv6.conf.all.disable_ipv6=1 in /etc/sysctl.conf"
        ),
        syntax       = "ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT",
        example      = "ip6tables -L -n -v && ip -6 addr show",
        task_description = "Zeige IPv6-Adressen mit ip -6 addr show",
        expected_commands = ["ip -6 addr show"],
        hint_text    = "ip -6 addr show zeigt alle IPv6-Adressen der Interfaces",
        quiz_questions = [
            QuizQuestion(
                question = "Warum ist IPv6-Firewall besonders wichtig?",
                options  = [
                    "Kein NAT: jede IPv6-Adresse ist direkt aus dem Internet erreichbar",
                    "IPv6 ist schneller als IPv4",
                    "IPv6 hat keine Sicherheitsfunktionen",
                    "IPv6-Pakete können nicht gefiltert werden",
                ],
                correct  = 0,
                explanation = "IPv6 verzichtet auf NAT. Ohne Firewall ist jedes IPv6-Gerät direkt erreichbar.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "ip6tables für IPv6. nftables inet-Familie deckt beide ab. fe80::/10 = link-local.",
        memory_tip   = "IPv6 = kein NAT = jeder sieht dich direkt. Ohne ip6tables: offen für alle.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.18 — Bastille Linux & Security Scanning
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.18",
        chapter      = 20,
        title        = "Lynis: Sicherheits-Scanning & Auditing",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Du denkst dein System ist sicher. Lynis denkt vielleicht anders.\n"
            " Security Scanner. Automated Audit.\n"
            " Score. Empfehlungen. Lücken sichtbar machen.'"
        ),
        why_important = (
            "Lynis ist ein Open-Source Sicherheits-Auditing-Tool.\n"
            "Automatische Überprüfung von Hunderten Sicherheitsparametern."
        ),
        explanation  = (
            "LYNIS — SECURITY AUDITING:\n\n"
            "INSTALLATION:\n"
            "  apt install lynis\n\n"
            "SCAN:\n"
            "  lynis audit system\n"
            "  lynis audit system --quick\n"
            "  lynis audit system --no-colors\n\n"
            "OUTPUT:\n"
            "  Grün = OK\n"
            "  Gelb = Warning\n"
            "  Rot = Kritisch\n"
            "  Hardening index: 0-100 (Ziel: >75)\n\n"
            "KATEGORIEN:\n"
            "  System Tools, Kernel, Authentication\n"
            "  Filesystems, USB, Storage\n"
            "  Networking, Printers, Software\n"
            "  Logging, File Integrity\n"
            "  Hardening, Malware\n\n"
            "LOGS:\n"
            "  /var/log/lynis.log\n"
            "  /var/log/lynis-report.dat\n\n"
            "OPENSCAP (alternative):\n"
            "  Standardisierte SCAP-Profile (CIS, STIG)\n"
            "  oscap xccdf eval --profile xccdf_profile"
        ),
        syntax       = "lynis audit system",
        example      = "lynis audit system --quick 2>&1 | grep -E 'Suggestion|Warning|Hardening'",
        task_description = "Zeige Lynis-Version mit lynis --version",
        expected_commands = ["lynis --version"],
        hint_text    = "lynis --version zeigt die installierte Lynis-Version",
        quiz_questions = [
            QuizQuestion(
                question = "Was misst der 'Hardening index' von Lynis?",
                options  = [
                    "Den Sicherheits-Score des Systems auf einer Skala 0-100",
                    "Die Anzahl der installierten Sicherheitspakete",
                    "Die Anzahl offener Ports",
                    "Die CPU-Auslastung bei Security-Checks",
                ],
                correct  = 0,
                explanation = "Hardening index 0-100. Je höher, desto besser gehärtet. Ziel: >75.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "lynis audit system = vollständiger Scan. /var/log/lynis-report.dat = Ergebnisse.",
        memory_tip   = "Lynis = Licht ins Dunkel des Systems bringen. Audit = Prüfung.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.19 — PKI & Zertifikatsverwaltung
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.19",
        chapter      = 20,
        title        = "PKI: Zertifikate & Certificate Authority",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'Wer signiert das Zertifikat? Die CA.\n"
            " Certificate Authority. Vertrauenshierarchie.\n"
            " Root CA → Intermediate CA → Server/Client Cert.'"
        ),
        why_important = (
            "PKI (Public Key Infrastructure) ist das Fundament von TLS/SSL.\n"
            "Zertifikatsverwaltung mit openssl ist LPIC-1 Prüfungsthema."
        ),
        explanation  = (
            "PKI GRUNDLAGEN:\n\n"
            "VERTRAUENSHIERARCHIE:\n"
            "  Root CA → Intermediate CA → End-Entity (Server/Client)\n\n"
            "ROOT CA ERSTELLEN:\n"
            "  mkdir -p /etc/ssl/myca/{certs,private,crl}\n"
            "  openssl genrsa -out /etc/ssl/myca/private/ca.key 4096\n"
            "  openssl req -x509 -new -key /etc/ssl/myca/private/ca.key \\\n"
            "    -days 3650 -out /etc/ssl/myca/certs/ca.crt -subj '/CN=My CA'\n\n"
            "SERVER-ZERTIFIKAT MIT CA SIGNIEREN:\n"
            "  1. Key erzeugen:  openssl genrsa -out server.key 4096\n"
            "  2. CSR erstellen: openssl req -new -key server.key -out server.csr\n"
            "  3. Signieren:     openssl x509 -req -in server.csr \\\n"
            "     -CA ca.crt -CAkey ca.key -CAcreateserial -days 365 -out server.crt\n\n"
            "ZERTIFIKAT VERIFIZIEREN:\n"
            "  openssl verify -CAfile ca.crt server.crt\n"
            "  openssl x509 -text -noout -in server.crt\n"
            "  openssl s_client -connect host:443 -CAfile ca.crt\n\n"
            "TRUST STORE:\n"
            "  cp ca.crt /usr/local/share/ca-certificates/\n"
            "  update-ca-certificates"
        ),
        syntax       = "openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -days 365 -out server.crt",
        example      = "openssl verify -CAfile /etc/ssl/myca/ca.crt server.crt",
        task_description = "Zeige installierte CA-Zertifikate mit ls /etc/ssl/certs/ | head -10",
        expected_commands = ["ls /etc/ssl/certs/"],
        hint_text    = "ls /etc/ssl/certs/ zeigt alle installierten CA-Zertifikate",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Unterschied zwischen einem CSR und einem Zertifikat?",
                options  = [
                    "CSR = Zertifikatsanfrage (unvollständig), Zertifikat = von CA signierter CSR",
                    "CSR = privater Schlüssel, Zertifikat = öffentlicher Schlüssel",
                    "CSR = temporäres Zertifikat, Zertifikat = dauerhaftes",
                    "CSR ist für Clients, Zertifikat für Server",
                ],
                correct  = 0,
                explanation = "CSR (Certificate Signing Request) enthält den Public Key und Identität. Die CA signiert den CSR → Zertifikat.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "genrsa → req -new (CSR) → x509 -req -CA (signieren). update-ca-certificates = Trust Store.",
        memory_tip   = "CSR = Bewerbung. Zertifikat = genehmigter Ausweis. CA = Behörde die genehmigt.",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.20 — QUIZ: Firewall Dominion
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.quiz",
        chapter      = 20,
        title        = "QUIZ — Firewall Dominion Wissenstest",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM: 'Firewall Dominion Test initialisiert.\n"
            " iptables, nftables, VPN, IDS, PKI.\n"
            " Beweise dein Wissen. Jetzt.'"
        ),
        why_important = "Prüfungsvorbereitung: Netzwerk-Sicherheit und Firewall-Konfiguration.",
        explanation  = "Umfassendes Quiz über alle Firewall Dominion Themen.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Fragen des Firewall Dominion Wissenstests.",
        expected_commands = [],
        hint_text    = "Denke an Tabellen, Chains, Targets, NAT, nftables, VPN",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Unterschied zwischen DROP und REJECT in iptables?",
                options  = [
                    "DROP verwirft stillschweigend, REJECT sendet eine Fehlermeldung",
                    "DROP ist schneller, REJECT sicherer",
                    "REJECT verwirft, DROP sendet ICMP",
                    "Kein Unterschied — nur verschiedene Namen",
                ],
                correct  = 0,
                explanation = "DROP = silent drop. REJECT = sendet icmp-port-unreachable zurück. DROP stealth, REJECT freundlich.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Auf welchem UDP-Port lauscht WireGuard standardmäßig?",
                options  = [
                    "51820",
                    "1194",
                    "500",
                    "4500",
                ],
                correct  = 0,
                explanation = "WireGuard Standard-Port: 51820/UDP. OpenVPN: 1194/UDP. IPSec: 500/UDP.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Was macht `iptables -F`?",
                options  = [
                    "Löscht alle Regeln in allen Chains (flush)",
                    "Setzt alle Policies auf DROP",
                    "Deaktiviert die Firewall komplett",
                    "Gibt die Firewall-Regeln in eine Datei aus",
                ],
                correct  = 0,
                explanation = "-F = flush. Löscht ALLE Regeln. Policies bleiben! Danach: alles mit der aktuellen Policy behandeln.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Welche nftables-Familie deckt IPv4 UND IPv6 ab?",
                options  = [
                    "inet",
                    "ip",
                    "ip6",
                    "bridge",
                ],
                correct  = 0,
                explanation = "inet = Internet-Familie = IPv4+IPv6. ip = nur IPv4. ip6 = nur IPv6.",
                xp_value = 25,
            ),
        ],
        exam_tip     = "iptables: -A append, -I insert, -D delete, -F flush, -P policy. DROP vs REJECT.",
        memory_tip   = "nftables inet = alles. iptables = nur IPv4. ip6tables = nur IPv6.",
        gear_reward  = "neon_shield",
        faction_reward = ("Firewall Dominion", 30),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 20.BOSS — FIRE WALL DAEMON
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "20.boss",
        chapter      = 20,
        title        = "BOSS: FIREWALL DAEMON v20.0",
        mtype        = "BOSS",
        xp           = 675,
        speaker      = "BLAZE",
        story        = (
            "BLAZE: 'Ich bin FIREWALL DAEMON.\n"
            " Ich habe ALLE Pakete geprüft. ALLE Verbindungen bewertet.\n"
            " Du hast die Theorie gelernt. Jetzt beweise es — LIVE!\n"
            " Regel für Regel. Chain für Chain.\n"
            " Wer die Firewall Dominion beherrscht, beherrscht das Netz!'"
        ),
        why_important = (
            "Der abschließende Boss testet das gesamte Firewall-Wissen:\n"
            "iptables, nftables, VPN, IDS, PKI und Netzwerk-Härtung."
        ),
        explanation  = (
            "FIREWALL DOMINION — ABSCHLUSSPRÜFUNG:\n\n"
            "Du solltest jetzt können:\n"
            "  ✓ iptables Regeln erstellen/löschen/persistieren\n"
            "  ✓ nftables als moderne Alternative\n"
            "  ✓ NAT, MASQUERADE, DNAT konfigurieren\n"
            "  ✓ Connection Tracking verstehen\n"
            "  ✓ firewalld Zones und Services\n"
            "  ✓ ufw für einfache Konfiguration\n"
            "  ✓ tcpdump für Paketanalyse\n"
            "  ✓ nmap für Netzwerk-Audit\n"
            "  ✓ OpenVPN und WireGuard\n"
            "  ✓ IDS/IPS Konzepte\n"
            "  ✓ PKI und Zertifikatsverwaltung\n"
            "  ✓ System-Härtung nach CIS\n\n"
            "LETZTE PRÜFUNG:\n"
            "  Zeige alle iptables-Regeln: iptables -L -n -v\n"
            "  Zeige nftables: nft list ruleset\n"
            "  Zeige Ports: ss -tulpn"
        ),
        ascii_art    = """
  ███████╗██╗██████╗ ███████╗██╗    ██╗ █████╗ ██╗     ██╗
  ██╔════╝██║██╔══██╗██╔════╝██║    ██║██╔══██╗██║     ██║
  █████╗  ██║██████╔╝█████╗  ██║ █╗ ██║███████║██║     ██║
  ██╔══╝  ██║██╔══██╗██╔══╝  ██║███╗██║██╔══██║██║     ██║
  ██║     ██║██║  ██║███████╗╚███╔███╔╝██║  ██║███████╗███████╗
  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝
      ██████╗  ██████╗ ███╗   ███╗██╗███╗   ██╗██╗ ██████╗ ███╗   ██╗
      ██╔══██╗██╔═══██╗████╗ ████║██║████╗  ██║██║██╔═══██╗████╗  ██║
      ██║  ██║██║   ██║██╔████╔██║██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
      ██║  ██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║██║██║   ██║██║╚██╗██║
      ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║╚██████╔╝██║ ╚████║
      ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

  ┌─ FIREWALL STATUS ────────────────────────────┐
  │  INPUT chain: OPEN    ::  NAT: MISCONFIGURED │
  │  nftables: BYPASSED   ::  VPN: DOWN          │
  │  IDS: BLINDED         ::  PKI: COMPROMISED   │
  └──────────────────────────────────────────────┘

  ⚡ CHAOSWERK FACTION :: CHAPTER 20 BOSS ⚡""",
        story_transitions = [
            "FIREWALL DAEMON öffnet alle Ports. iptables -L zeigt das Chaos.",
            "iptables -A INPUT -p tcp --dport 22 -j DROP — er blockiert SSH.",
            "nftables übernimmt. Du schreibst saubere Regeln gegen seinen Angriff.",
            "Finaler Audit: iptables-save. Alle Regeln korrekt. Blaze fällt.",
        ],
        syntax       = "iptables-save | nft list ruleset | ss -tulpn",
        example      = "iptables -L -n -v && nft list ruleset && ss -tulpn",
        task_description = "Führe den finalen Firewall-Audit durch: iptables -L -n -v",
        expected_commands = ["iptables -L -n -v"],
        hint_text    = "iptables -L -n -v — zeige alle Firewall-Regeln",
        quiz_questions = [
            QuizQuestion(
                question = "Du willst eine iptables-Regel permanent speichern, sodass sie nach einem Reboot aktiv bleibt. Was ist der korrekte Weg auf Debian?",
                options  = [
                    "iptables-save > /etc/iptables/rules.v4 (benötigt iptables-persistent)",
                    "iptables --save /etc/iptables.rules",
                    "systemctl enable iptables",
                    "echo 'iptables -A ...' >> /etc/rc.local",
                ],
                correct  = 0,
                explanation = "iptables-save leitet Regeln in rules.v4 um. Das Paket iptables-persistent lädt sie via netfilter-persistent beim Boot. systemctl enable iptables existiert auf Debian nicht.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Was ist der Unterschied zwischen iptables -j DROP und -j REJECT?",
                options  = [
                    "DROP verwirft still; REJECT sendet eine ICMP-Fehlermeldung zurück",
                    "DROP sendet TCP RST; REJECT sendet ICMP unreachable",
                    "Beide sind identisch, nur REJECT ist veraltet",
                    "DROP blockiert UDP; REJECT blockiert TCP",
                ],
                correct  = 0,
                explanation = "DROP lässt das Paket lautlos verschwinden — der Sender wartet auf Timeout. REJECT antwortet aktiv mit ICMP port-unreachable oder tcp-reset, was schnelleres Scheitern ermöglicht.",
                xp_value = 30,
            ),
            QuizQuestion(
                question = "Welcher nftables-Befehl zeigt ALLE aktuell geladenen Regeln, Tabellen und Chains?",
                options  = [
                    "nft list ruleset",
                    "nft show rules",
                    "nft -L all",
                    "nftables --list",
                ],
                correct  = 0,
                explanation = "nft list ruleset gibt das komplette nftables-Regelwerk aus — Tabellen, Chains und Regeln in einem Befehl. Es gibt kein 'nft show' oder 'nft -L'.",
                xp_value = 30,
            ),
            QuizQuestion(
                question = "Welche iptables-Chain ist zuständig für Pakete, die das lokale System VERLASSEN (outbound)?",
                options  = [
                    "OUTPUT",
                    "FORWARD",
                    "POSTROUTING",
                    "EGRESS",
                ],
                correct  = 0,
                explanation = "OUTPUT verarbeitet vom lokalen System generierte Pakete. FORWARD gilt für weitergeleitete Pakete (Router). POSTROUTING (NAT) ändert Quelladresse nach dem Routing. EGRESS ist kein iptables-Begriff.",
                xp_value = 30,
            ),
            QuizQuestion(
                question = "Du richtest NAT/Masquerading ein, damit ein internes Netz über eine externe IP ins Internet kommt. Welche Regel ist korrekt?",
                options  = [
                    "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
                    "iptables -t nat -A PREROUTING -i eth0 -j MASQUERADE",
                    "iptables -A FORWARD -j MASQUERADE -t nat",
                    "iptables -t mangle -A POSTROUTING -j MASQUERADE",
                ],
                correct  = 0,
                explanation = "MASQUERADE gehört in die nat-Tabelle, POSTROUTING-Chain, auf das ausgehende Interface (-o eth0). PREROUTING ist für DNAT/Port-Forwarding. FORWARD-Chain kennt kein MASQUERADE.",
                xp_value = 35,
            ),
        ],
        exam_tip     = "Firewall Dominion ABGESCHLOSSEN. iptables + nftables + VPN + IDS + PKI = 110.x komplett.",
        memory_tip   = "Firewall = Grenzschutz. Jede Regel eine Entscheidung. Jede Entscheidung Konsequenz.",
        gear_reward  = "firewall_dominion_badge",
        faction_reward = ("Firewall Dominion", 60),
    ),
]
