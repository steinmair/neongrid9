"""
NeonGrid-9 :: Kapitel 2 — Kernel Protocol
LPIC-1 Topic 101.2: Boot the System
22 Missionen + Boss
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_2_MISSIONS = [

    Mission(
        mission_id="2.01",
        title="Power On — BIOS POST Ablauf",
        mtype="SCAN", xp=35, chapter=2,
        speaker="ZARA Z3R0",
        story=(
            "Der Boot-Prozess ist das Herzstück eines Linux-Systems.\n"
            "Wer ihn versteht, kann alles reparieren — selbst wenn\n"
            "das System nicht mehr startet.\n"
            "Phase 1: POST. Bevor Linux auch nur existiert."
        ),
        why_important=(
            "Boot-Probleme sind die häufigste Admin-Notfallsituation.\n"
            "LPIC-1 prüft jede Phase des Boot-Prozesses.\n"
            "Verstehe die Reihenfolge — sie ist fundamental."
        ),
        explanation=(
            "Boot-Sequenz: 6 Phasen\n\n"
            "  1. POWER ON\n"
            "     Strom an → CPU springt zu BIOS/UEFI Reset-Vektor\n\n"
            "  2. POST (Power-On Self-Test)\n"
            "     Hardware-Prüfung: CPU, RAM, Devices\n"
            "     Fehler → Beep-Codes oder Bildschirmmeldung\n\n"
            "  3. BIOS/UEFI\n"
            "     Findet bootfähiges Gerät (Boot-Order)\n"
            "     Lädt Bootloader aus MBR/EFI-Partition\n\n"
            "  4. BOOTLOADER (GRUB2)\n"
            "     Lädt Kernel + initramfs in RAM\n"
            "     Gibt Kontrolle an Kernel\n\n"
            "  5. KERNEL\n"
            "     Initialisiert Hardware, mountet root-FS\n"
            "     Startet PID 1 (systemd/init)\n\n"
            "  6. INIT SYSTEM\n"
            "     Startet alle Dienste\n"
            "     Login-Prompt erscheint"
        ),
        ascii_art = """
  ██████╗  ██████╗  ██████╗ ████████╗    ███████╗███████╗ ██████╗
  ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔═══██╗
  ██████╔╝██║   ██║██║   ██║   ██║       ███████╗█████╗  ██║   ██║
  ██╔══██╗██║   ██║██║   ██║   ██║       ╚════██║██╔══╝  ██║▄▄ ██║
  ██████╔╝╚██████╔╝╚██████╔╝   ██║       ███████║███████╗╚██████╔╝
  ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝       ╚══════╝╚══════╝ ╚══▀▀═╝

  [ CHAPTER 02 :: BOOT SEQUENCE ]
  > BIOS/UEFI → Bootloader → Kernel → init... loading.""",
        story_transitions = [
            "Das System erwacht. POST abgeschlossen. GRUB lädt.",
            "Kernel dekomprimiert sich. initramfs entfaltet sich im RAM.",
            "PID 1 startet. Die Welt des Systems nimmt Form an.",
            "Boot abgeschlossen. Jetzt lernst du, was dahinter steckt.",
        ],
        syntax="# Boot-Reihenfolge prüfen:\ndmesg | head -20\njournalctl -b --no-pager | head -30",
        example=(
            "$ dmesg | head -5\n"
            "[0.000000] Linux version 6.1.0-17-amd64\n"
            "[0.000000] BIOS-e820: [mem 0x0-0x9efff] usable\n"
            "[0.293114] ACPI: IRQ0 used by override.\n"
            "[0.458223] PCI: Using ACPI for IRQ routing"
        ),
        task_description="Zeige die ersten Kernel-Meldungen des Boot-Prozesses.",
        expected_commands=["dmesg | head -20", "dmesg"],
        hints=[
            "Das Kommando 'dmesg' zeigt Kernel-Meldungen an. Kombiniert mit 'head -20' für die ersten 20 Zeilen.",
            "Versuche: dmesg | head ...",
            "Der vollständige Befehl: dmesg | head -20",
        ],
        hint_text="dmesg | head -20 zeigt die ersten 20 Kernel-Boot-Meldungen",
        quiz_questions=[
            QuizQuestion(
                question="In welcher Reihenfolge findet der Linux-Boot-Prozess statt?",
                options=[
                    "A) Kernel → BIOS → Bootloader → POST → Init",
                    "B) POST → BIOS/UEFI → Bootloader → Kernel → Init",
                    "C) GRUB → POST → Kernel → BIOS → systemd",
                    "D) Init → Kernel → BIOS → POST → Bootloader",
                ],
                correct="B",
                explanation="POST → BIOS/UEFI → Bootloader (GRUB2) → Kernel → Init System. Diese Reihenfolge ist LPIC-1 Grundwissen.",
            ),
        ],
        exam_tip="LPIC-1 Standardfrage: Boot-Reihenfolge.\nAntwort immer: BIOS/POST → Bootloader → Kernel → Init.",
        memory_tip="POST → GRUB → Kernel → systemd. Merke: Pfeil nach rechts, immer.",
    ),

    Mission(
        mission_id="2.02",
        title="MBR Anatomy — Master Boot Record",
        mtype="DECODE", xp=30, chapter=2,
        speaker="DAEMON",
        story=(
            "Der MBR — 512 Bytes am Anfang jeder Disk.\n"
            "Darin: Bootloader-Code, Partitionstabelle, Magic Bytes.\n"
            "Wer den MBR kennt, versteht warum BIOS nur 4\n"
            "primäre Partitionen erlaubt."
        ),
        why_important=(
            "MBR ist das Legacy-Boot-Schema.\n"
            "LPIC-1 prüft MBR-Struktur, Größenbeschränkungen\n"
            "und den Unterschied zu GPT."
        ),
        explanation=(
            "MBR — Master Boot Record\n"
            "Liegt auf Byte 0–511 der Disk (/dev/sda, Sektor 0)\n\n"
            "MBR-Struktur (512 Bytes total):\n"
            "  Bytes   0–445 : Bootstrap Code (Bootloader Stage 1)\n"
            "  Bytes 446–509 : Partitionstabelle (4 × 16 Bytes)\n"
            "  Bytes 510–511 : Magic Number (0x55 0xAA)\n\n"
            "Partitionstabelle:\n"
            "  4 Einträge × 16 Bytes = 64 Bytes\n"
            "  Max. 4 primäre Partitionen\n"
            "  ODER 3 primäre + 1 erweiterte (extended)\n"
            "  In erweiterter: logische Partitionen (bis zu 63)\n\n"
            "MBR Beschränkungen:\n"
            "  Max. Disk-Größe: 2TB (32-bit LBA)\n"
            "  Max. 4 primäre Partitionen\n"
            "  Keine Redundanz (Backup des MBR)\n\n"
            "MBR sichern:\n"
            "  dd if=/dev/sda of=mbr_backup.bin bs=512 count=1"
        ),
        syntax=(
            "# MBR betrachten:\ndd if=/dev/sda bs=512 count=1 | hexdump -C | head\n\n"
            "# MBR sichern:\ndd if=/dev/sda of=mbr_backup.bin bs=512 count=1\n\n"
            "# Magic Bytes prüfen:\ndd if=/dev/sda bs=1 skip=510 count=2 | xxd"
        ),
        example=(
            "$ fdisk -l /dev/sda | head -5\n"
            "Disk /dev/sda: 500 GiB, 500107862016 bytes\n"
            "Disklabel type: dos     ← MBR!\n"
            "Disk identifier: 0x1234abcd\n\n"
            "Device     Boot  Start     End   Size  Type\n"
            "/dev/sda1  *      2048  1026047   500M  Linux boot\n"
            "/dev/sda2      1026048 976773119 465.3G Linux LVM"
        ),
        task_description="Zeige die Partitionstabelle einer MBR-Disk.",
        expected_commands=["fdisk -l /dev/sda"],
        hints=[
            "Nutze 'fdisk' mit dem Flag '-l' (list) um Partitionstabellen anzuzeigen. Das Gerät /dev/sda ist das Ziel.",
            "Versuche: fdisk -l /dev/sda",
            "Der vollständige Befehl: fdisk -l /dev/sda",
        ],
        hint_text="fdisk -l /dev/sda — listet Partitionstabelle auf",
        quiz_questions=[
            QuizQuestion(
                question="Wie viele primäre Partitionen erlaubt MBR maximal?",
                options=["A) 2", "B) 4", "C) 8", "D) 16"],
                correct="B",
                explanation="MBR-Partitionstabelle hat 4 Einträge × 16 Bytes = 64 Bytes. Maximal 4 primäre Partitionen.",
            ),
            QuizQuestion(
                question="Welche Maximalgröße unterstützt MBR für Festplatten?",
                options=["A) 1 TB", "B) 2 TB", "C) 4 TB", "D) 8 TB"],
                correct="B",
                explanation="MBR verwendet 32-bit LBA mit 512-Byte-Sektoren: 2^32 × 512 = 2TB Maximum.",
            ),
        ],
        exam_tip=(
            "MBR-Fakten für LPIC-1:\n"
            "512 Bytes Größe. Bytes 446-509 = Partitionstabelle.\n"
            "0x55AA = Magic Number (Boot-Signatur).\n"
            "max 4 primäre ODER 3+1 extended."
        ),
        memory_tip="MBR = 512 Bytes. 446 Bytes Code + 64 Bytes Partitionstabelle + 2 Magic.",
    ),

    Mission(
        mission_id="2.03",
        title="GPT Structure — GUID Partition Table",
        mtype="DECODE", xp=30, chapter=2,
        speaker="ZARA Z3R0",
        story=(
            "Zara Z3R0: 'GPT hat MBR begraben, Ghost.\n"
            " 128 Partitionen. Redundante Tabelle. Festplatten über 2TB.\n"
            " UEFI braucht GPT — kein GPT, kein UEFI-Boot.\n"
            " Lern die Struktur. Die Prüfung fragt genau hier.'"
        ),
        why_important=(
            "GPT ist der moderne Nachfolger von MBR.\n"
            "UEFI-Systeme nutzen ausschließlich GPT.\n"
            "LPIC-1 prüft GPT-Vorteile und Struktur."
        ),
        explanation=(
            "GPT — GUID Partition Table\n\n"
            "Vorteile gegenüber MBR:\n"
            "  ✓ Bis zu 128 Partitionen (ohne extended/logical)\n"
            "  ✓ Festplatten > 2TB (64-bit LBA)\n"
            "  ✓ Redundanter Header (am Disk-Anfang UND -Ende)\n"
            "  ✓ CRC32-Checksummen für Integrität\n"
            "  ✓ GUID pro Partition (global eindeutig)\n\n"
            "GPT-Struktur:\n"
            "  LBA 0   : Protective MBR (Kompatibilität)\n"
            "  LBA 1   : GPT Header (Primary)\n"
            "  LBA 2-33: Partition Entry Array (128 Einträge)\n"
            "  ...     : Partitionen\n"
            "  LBA -33 : Backup Partition Entries\n"
            "  LBA -1  : Backup GPT Header\n\n"
            "EFI System Partition (ESP):\n"
            "  GPT-Partition mit FAT32-Dateisystem\n"
            "  Enthält Bootloader-Dateien (.efi)\n"
            "  Typisch: 512MB, gemountet auf /boot/efi"
        ),
        syntax=(
            "# GPT-Disk prüfen:\nfdisk -l /dev/nvme0n1\nparted -l\ngdisk -l /dev/nvme0n1"
        ),
        example=(
            "$ fdisk -l /dev/nvme0n1\n"
            "Disk /dev/nvme0n1: 476.9 GiB\n"
            "Disklabel type: gpt     ← GPT!\n\n"
            "Device          Start       End   Size  Type\n"
            "/dev/nvme0n1p1   2048   1050623   512M  EFI System\n"
            "/dev/nvme0n1p2  1050624  3147775     1G  Linux filesystem\n"
            "/dev/nvme0n1p3  3147776 998244351 475G  Linux filesystem"
        ),
        task_description="Erkenne ob eine Disk MBR oder GPT nutzt mit fdisk -l.",
        expected_commands=["fdisk -l /dev/nvme0n1"],
        hint_text="fdisk -l /dev/nvme0n1 — schau auf 'Disklabel type'",
        quiz_questions=[
            QuizQuestion(
                question="Wie viele Partitionen unterstützt GPT standardmäßig?",
                options=["A) 4", "B) 16", "C) 128", "D) 256"],
                correct="C",
                explanation="GPT unterstützt standardmäßig 128 Partitionen. Alle gleichwertig — kein primary/extended/logical Unterschied.",
            ),
            QuizQuestion(
                question="Was ist die EFI System Partition (ESP)?",
                options=[
                    "A) Eine Swap-Partition für UEFI",
                    "B) Eine FAT32-Partition mit Bootloader-Dateien für UEFI",
                    "C) Die Root-Partition bei UEFI-Systemen",
                    "D) Eine spezielle ext4-Partition für den Kernel",
                ],
                correct="B",
                explanation="ESP ist eine FAT32-formatierte GPT-Partition (typisch 512MB, auf /boot/efi gemountet). Sie enthält .efi-Bootloader-Dateien.",
            ),
        ],
        exam_tip=(
            "GPT vs MBR:\nGPT = 128 Partitionen, >2TB, UEFI, redundanter Header\n"
            "MBR = 4 primäre, max 2TB, BIOS\n"
            "fdisk zeigt: 'Disklabel type: gpt' oder 'dos'"
        ),
        memory_tip="GPT = 128 Partitionen + Backup-Header. MBR = 4 Partitionen + kein Backup.",
    ),

    Mission(
        mission_id="2.04",
        title="GRUB2 Install — Grundlagen",
        mtype="INFILTRATE", xp=35, chapter=2,
        speaker="ZARA Z3R0",
        story=(
            "GRUB2 — Grand Unified Bootloader Version 2.\n"
            "Er sitzt zwischen BIOS und Kernel.\n"
            "Wer GRUB kennt, kann jedes System reparieren."
        ),
        why_important=(
            "GRUB2 ist der Standard-Bootloader auf praktisch allen\n"
            "modernen Linux-Systemen. LPIC-1 prüft Installation,\n"
            "Konfiguration und Troubleshooting."
        ),
        explanation=(
            "GRUB2 — Grand Unified Bootloader 2\n\n"
            "Bestandteile:\n"
            "  Stage 1     : Im MBR (446 Bytes) oder EFI-Partition\n"
            "  Stage 1.5   : In den Sektoren zwischen MBR und erster Partition\n"
            "                (bei BIOS-GRUB)\n"
            "  Stage 2     : /boot/grub/ — der eigentliche GRUB\n\n"
            "Wichtige Verzeichnisse:\n"
            "  /boot/grub/         — GRUB2 Dateien (BIOS)\n"
            "  /boot/grub2/        — auf RHEL/Fedora\n"
            "  /boot/efi/EFI/      — UEFI GRUB\n\n"
            "Wichtige Dateien:\n"
            "  /boot/grub/grub.cfg        — Haupt-Konfiguration\n"
            "  /etc/default/grub          — Benutzer-Einstellungen\n"
            "  /etc/grub.d/               — Konfig-Skripte\n\n"
            "GRUB2 installieren:\n"
            "  grub-install /dev/sda      — BIOS-Installation\n"
            "  grub-install --target=x86_64-efi  — UEFI"
        ),
        syntax=(
            "grub-install /dev/sda              # BIOS\n"
            "grub-install --target=x86_64-efi   # UEFI\n"
            "update-grub                         # Config neu generieren\n"
            "grub2-install /dev/sda             # RHEL/CentOS"
        ),
        example=(
            "$ grub-install /dev/sda\n"
            "Installing for i386-pc platform.\n"
            "Installation finished. No error reported.\n\n"
            "$ ls /boot/grub/\n"
            "fonts  grub.cfg  grubenv  i386-pc  locale  unicode.pf2"
        ),
        task_description="Zeige den Inhalt des /boot/grub/ Verzeichnisses.",
        expected_commands=["ls /boot/grub/", "ls /boot/grub2/"],
        hint_text="ls /boot/grub/ — zeigt GRUB2-Dateien",
        quiz_questions=[
            QuizQuestion(
                question="Wo liegt die generierte GRUB2-Konfigurationsdatei?",
                options=[
                    "A) /etc/grub2.cfg",
                    "B) /boot/grub/grub.cfg",
                    "C) /etc/default/grub.cfg",
                    "D) /boot/grub2.conf",
                ],
                correct="B",
                explanation="/boot/grub/grub.cfg ist die automatisch generierte Konfiguration. Auf RHEL: /boot/grub2/grub.cfg. Diese Datei NICHT manuell bearbeiten.",
            ),
        ],
        exam_tip=(
            "grub.cfg liegt in /boot/grub/grub.cfg (Debian/Ubuntu)\n"
            "oder /boot/grub2/grub.cfg (RHEL/CentOS/Fedora).\n"
            "NIEMALS direkt bearbeiten — immer update-grub nutzen!"
        ),
        memory_tip="grub.cfg in /boot/grub/. update-grub regeneriert sie automatisch.",
    ),

    Mission(
        mission_id="2.05",
        title="GRUB2 Config — grub.cfg lesen",
        mtype="DECODE", xp=35, chapter=2,
        speaker="DAEMON",
        story=(
            "DAEMON: grub.cfg — ich generiere diese Datei.\n"
            "Editiere sie NICHT direkt — sie wird überschrieben.\n"
            "Lesen darfst du. Verstehen musst du.\n"
            "Welcher menuentry bootet als nächstes?"
        ),
        why_important=(
            "grub.cfg zu verstehen bedeutet zu wissen welche\n"
            "Betriebssysteme verfügbar sind und wie der Boot läuft."
        ),
        explanation=(
            "/boot/grub/grub.cfg — GRUB2 Hauptkonfiguration\n\n"
            "ACHTUNG: Automatisch generiert! Nicht manuell bearbeiten.\n\n"
            "Wichtige Direktiven:\n\n"
            "  set default=0\n"
            "    → Welcher Eintrag standard-gemäß bootet (0=erster)\n\n"
            "  set timeout=5\n"
            "    → Wartezeit in Sekunden vor Auto-Boot\n\n"
            "  menuentry 'Ubuntu' {\n"
            "    ...Kernel-Zeile\n"
            "  }\n"
            "    → Ein Boot-Eintrag\n\n"
            "  linux /boot/vmlinuz-6.1.0 root=UUID=xxx\n"
            "    → Kernel + root-Parameter\n\n"
            "  initrd /boot/initrd.img-6.1.0\n"
            "    → initramfs laden\n\n"
            "  insmod gzio\n"
            "    → GRUB-Module laden"
        ),
        syntax="cat /boot/grub/grub.cfg\ngrep 'menuentry' /boot/grub/grub.cfg",
        example=(
            "$ grep 'menuentry\\|linux\\|initrd' /boot/grub/grub.cfg | head -10\n"
            'menuentry \'Ubuntu 22.04\' {\n'
            "  linux /boot/vmlinuz-6.1.0 root=UUID=abc123 ro quiet\n"
            "  initrd /boot/initrd.img-6.1.0\n"
            "}"
        ),
        task_description="Zeige die menuentry-Einträge in grub.cfg.",
        expected_commands=["grep 'menuentry' /boot/grub/grub.cfg"],
        hint_text="grep menuentry /boot/grub/grub.cfg",
        quiz_questions=[
            QuizQuestion(
                question="Welche GRUB2-Direktive setzt die Standard-Boot-Wartezeit?",
                options=[
                    "A) set default=5",
                    "B) timeout=5",
                    "C) set timeout=5",
                    "D) wait=5",
                ],
                correct="C",
                explanation="set timeout=5 setzt 5 Sekunden Wartezeit. set timeout=-1 = unbegrenzt warten. set timeout=0 = sofort booten.",
            ),
            QuizQuestion(
                question="Was macht die 'initrd' Zeile in grub.cfg?",
                options=[
                    "A) Sie lädt den Kernel",
                    "B) Sie lädt das initramfs/initrd in den RAM",
                    "C) Sie definiert das Root-Dateisystem",
                    "D) Sie setzt Kernel-Parameter",
                ],
                correct="B",
                explanation="initrd lädt das initramfs (Initial RAM Disk) in den RAM. Das initramfs enthält minimale Tools zum Mounten des echten Root-Dateisystems.",
            ),
        ],
        exam_tip=(
            "grub.cfg wird GENERIERT — nie direkt editieren.\n"
            "Eigene Einstellungen in /etc/default/grub,\n"
            "dann update-grub ausführen."
        ),
        memory_tip="grub.cfg lesen ✓, aber nicht bearbeiten. Bearbeite /etc/default/grub.",
    ),

    Mission(
        mission_id="2.06",
        title="GRUB2 Custom — /etc/default/grub",
        mtype="CONSTRUCT", xp=40, chapter=2,
        speaker="ZARA Z3R0",
        story=(
            "Jetzt wird's real. Wir ändern GRUB-Einstellungen.\n"
            "/etc/default/grub ist die einzige Datei die du\n"
            "direkt bearbeitest. Dann update-grub — nie anders."
        ),
        why_important=(
            "/etc/default/grub steuert alle wesentlichen GRUB-Parameter.\n"
            "Hier änderst du Timeout, Boot-Optionen, stiller Boot, Kernel-Params."
        ),
        explanation=(
            "/etc/default/grub — GRUB2 Benutzer-Konfiguration\n\n"
            "Wichtige Variablen:\n\n"
            "  GRUB_DEFAULT=0\n"
            "    → Standard-Menüeintrag (0=erster, oder 'saved')\n\n"
            "  GRUB_TIMEOUT=5\n"
            "    → Wartezeit in Sekunden\n\n"
            "  GRUB_TIMEOUT_STYLE=menu\n"
            "    → menu / hidden / countdown\n\n"
            "  GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"\n"
            "    → Kernel-Parameter für normalen Boot\n\n"
            "  GRUB_CMDLINE_LINUX=\"\"\n"
            "    → Kernel-Parameter für ALLE Boots inkl. Recovery\n\n"
            "  GRUB_DISABLE_RECOVERY=false\n"
            "    → Recovery-Einträge im Menü\n\n"
            "  GRUB_GFXMODE=1920x1080\n"
            "    → Auflösung im GRUB-Menü\n\n"
            "Nach jeder Änderung:\n"
            "  sudo update-grub      (Debian/Ubuntu)\n"
            "  sudo grub2-mkconfig -o /boot/grub2/grub.cfg  (RHEL)"
        ),
        syntax=(
            "# Bearbeiten:\nsudo nano /etc/default/grub\n\n"
            "# Config neu generieren:\nsudo update-grub\n\n"
            "# RHEL-Variante:\nsudo grub2-mkconfig -o /boot/grub2/grub.cfg"
        ),
        example=(
            "$ cat /etc/default/grub\n"
            "GRUB_DEFAULT=0\n"
            "GRUB_TIMEOUT=5\n"
            'GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"\n'
            'GRUB_CMDLINE_LINUX=""\n'
            "GRUB_TERMINAL=console"
        ),
        task_description="Zeige den Inhalt von /etc/default/grub.",
        expected_commands=["cat /etc/default/grub"],
        hint_text="cat /etc/default/grub",
        quiz_questions=[
            QuizQuestion(
                question="Du willst den Boot-Timeout auf 10 Sekunden setzen. Welche Zeile änderst du?",
                options=[
                    "A) set timeout=10 in grub.cfg",
                    "B) GRUB_TIMEOUT=10 in /etc/default/grub, dann update-grub",
                    "C) timeout=10 in /boot/grub/grub.cfg",
                    "D) grub-timeout 10",
                ],
                correct="B",
                explanation="Richtig: GRUB_TIMEOUT=10 in /etc/default/grub setzen, dann update-grub ausführen. Niemals grub.cfg direkt ändern.",
            ),
            QuizQuestion(
                question="Was bewirkt GRUB_CMDLINE_LINUX_DEFAULT=\"quiet splash\"?",
                options=[
                    "A) Setzt GRUB-Menü auf ruhig + Splash-Screen",
                    "B) Übergibt 'quiet splash' als Parameter an den Linux-Kernel beim Standard-Boot",
                    "C) Deaktiviert den GRUB-Menü-Splash",
                    "D) Blendet den GRUB-Countdown aus",
                ],
                correct="B",
                explanation="GRUB_CMDLINE_LINUX_DEFAULT übergibt Kernel-Parameter. 'quiet' = weniger Boot-Meldungen, 'splash' = Plymouth Splash-Screen.",
            ),
        ],
        exam_tip=(
            "Wichtigste Regel: /etc/default/grub bearbeiten,\n"
            "dann update-grub ausführen.\n"
            "GRUB_CMDLINE_LINUX_DEFAULT = Kernel-Parameter nur für normalen Boot.\n"
            "GRUB_CMDLINE_LINUX = für ALLE Boots (inkl. Recovery)."
        ),
        memory_tip="/etc/default/grub = Einstellungen. update-grub = Anwenden.",
    ),

    Mission(
        mission_id="2.07",
        title="update-grub — Config regenerieren",
        mtype="INFILTRATE", xp=30, chapter=2,
        speaker="DAEMON",
        story=(
            "DAEMON: Du änderst /etc/default/grub.\n"
            "Schön. Aber grub.cfg wurde noch nicht aktualisiert.\n"
            "update-grub ist der Befehl der die Änderung aktiviert.\n"
            "Vergiss ihn — und deine Änderung existiert nicht."
        ),
        why_important="update-grub ist der Pflichtbefehl nach jeder GRUB-Konfigurationsänderung.",
        explanation=(
            "update-grub — GRUB2 Konfiguration neu generieren\n\n"
            "Was update-grub macht:\n"
            "  1. Liest /etc/default/grub\n"
            "  2. Führt alle Skripte in /etc/grub.d/ aus\n"
            "  3. Schreibt neue /boot/grub/grub.cfg\n\n"
            "/etc/grub.d/ Skripte (Reihenfolge = Nummerierung):\n"
            "  00_header      : GRUB-Header\n"
            "  05_debian_theme: Design\n"
            "  10_linux       : Linux-Einträge (autom. alle Kernels)\n"
            "  30_os-prober   : Andere Betriebssysteme\n"
            "  40_custom      : Eigene Einträge\n\n"
            "RHEL-Äquivalent:\n"
            "  grub2-mkconfig -o /boot/grub2/grub.cfg\n\n"
            "Output zeigt erkannte Systeme:\n"
            "  'Found linux image: /boot/vmlinuz-...'"
        ),
        syntax=(
            "sudo update-grub                                    # Debian/Ubuntu\n"
            "sudo grub2-mkconfig -o /boot/grub2/grub.cfg        # RHEL/CentOS\n"
            "sudo grub-mkconfig -o /boot/grub/grub.cfg          # Manuell"
        ),
        example=(
            "$ sudo update-grub\n"
            "Sourcing file /etc/default/grub\n"
            "Sourcing file /etc/default/grub.d/init-select.cfg\n"
            "Generating grub configuration file ...\n"
            "Found linux image: /boot/vmlinuz-6.1.0-17-amd64\n"
            "Found initrd image: /boot/initrd.img-6.1.0-17-amd64\n"
            "Found linux image: /boot/vmlinuz-6.1.0-13-amd64\n"
            "Warning: os-prober will not be executed...\n"
            "done"
        ),
        task_description="Führe update-grub aus um die GRUB-Konfiguration neu zu generieren.",
        expected_commands=["update-grub", "sudo update-grub"],
        hint_text="update-grub (oder sudo update-grub)",
        quiz_questions=[
            QuizQuestion(
                question="Was passiert wenn du /etc/default/grub änderst aber update-grub NICHT ausführst?",
                options=[
                    "A) Nichts — Änderungen werden automatisch übernommen",
                    "B) GRUB lädt die Datei direkt",
                    "C) Änderungen haben beim nächsten Boot keine Wirkung — grub.cfg ist veraltet",
                    "D) Das System startet nicht mehr",
                ],
                correct="C",
                explanation="/etc/default/grub wird nicht direkt gelesen. GRUB liest /boot/grub/grub.cfg. Erst nach update-grub wird grub.cfg aktualisiert.",
            ),
        ],
        exam_tip=(
            "update-grub = grub-mkconfig -o /boot/grub/grub.cfg\n"
            "RHEL: grub2-mkconfig -o /boot/grub2/grub.cfg\n"
            "Nach jedem Kernel-Update wird update-grub automatisch ausgeführt."
        ),
        memory_tip="Änderung in /etc/default/grub → IMMER update-grub danach!",
    ),

    Mission(
        mission_id="2.08",
        title="grub-install — GRUB auf Device schreiben",
        mtype="INFILTRATE", xp=35, chapter=2,
        speaker="ZARA Z3R0",
        story=(
            "Zara Z3R0: 'Das System bootet nicht. MBR korrumpiert.\n"
            " grub-install /dev/sda — das rettet dich.\n"
            " Für UEFI: grub-install --target=x86_64-efi.\n"
            " Lern beide. Notsituationen warten nicht auf Recherche.'"
        ),
        why_important=(
            "grub-install schreibt GRUB in den MBR/EFI.\n"
            "Notwendig nach frischer Installation oder MBR-Korruption."
        ),
        explanation=(
            "grub-install — GRUB2 auf Gerät installieren\n\n"
            "BIOS-Installation (MBR):\n"
            "  grub-install /dev/sda\n"
            "  → Schreibt Stage 1 in MBR\n"
            "  → Kopiert Stage 2 nach /boot/grub/\n\n"
            "UEFI-Installation:\n"
            "  grub-install --target=x86_64-efi \\\n"
            "    --efi-directory=/boot/efi \\\n"
            "    --bootloader-id=GRUB\n"
            "  → Schreibt /boot/efi/EFI/GRUB/grubx64.efi\n\n"
            "Targets:\n"
            "  i386-pc     : BIOS 32/64-bit\n"
            "  x86_64-efi  : UEFI 64-bit\n"
            "  i386-efi    : UEFI 32-bit\n"
            "  arm64-efi   : ARM UEFI\n\n"
            "Nach grub-install immer update-grub ausführen!"
        ),
        syntax=(
            "grub-install /dev/sda                          # BIOS\n"
            "grub-install --target=x86_64-efi \\            # UEFI\n"
            "  --efi-directory=/boot/efi \\\n"
            "  --bootloader-id=GRUB\n"
            "grub2-install /dev/sda                         # RHEL"
        ),
        example=(
            "$ grub-install /dev/sda\n"
            "Installing for i386-pc platform.\n"
            "Installation finished. No error reported.\n\n"
            "$ grub-install --target=x86_64-efi --efi-directory=/boot/efi\n"
            "Installing for x86_64-efi platform.\n"
            "Installation finished. No error reported."
        ),
        task_description="Zeige den Hilfetext von grub-install.",
        expected_commands=["grub-install --help", "grub-install"],
        hint_text="grub-install --help",
        quiz_questions=[
            QuizQuestion(
                question="Du willst GRUB2 für UEFI installieren. Welcher Befehl ist korrekt?",
                options=[
                    "A) grub-install /dev/sda",
                    "B) grub-install --target=x86_64-efi --efi-directory=/boot/efi",
                    "C) grub-install --mode=uefi /dev/sda",
                    "D) grub-uefi-install /boot/efi",
                ],
                correct="B",
                explanation="Für UEFI: --target=x86_64-efi und --efi-directory=/boot/efi. Das EFI-Verzeichnis muss die gemountete ESP-Partition sein.",
            ),
        ],
        exam_tip=(
            "grub-install /dev/sda = BIOS (schreibt in MBR).\n"
            "grub-install --target=x86_64-efi = UEFI (schreibt .efi Datei).\n"
            "Wichtig: Das GERÄT angeben (sda), NICHT die Partition (sda1)!"
        ),
        memory_tip="grub-install GERÄT (nicht Partition!). --target für UEFI.",
    ),

    Mission(
        mission_id="2.09",
        title="GRUB Rescue — Recovery aus GRUB-Shell",
        mtype="REPAIR", xp=50, chapter=2,
        speaker="DAEMON",
        story=(
            "Das ist der Moment wo du beweist ob du wirklich\n"
            "ein Sysadmin bist.\n"
            "System bootet nicht. Nur GRUB-Shell.\n"
            "Ich zeig dir wie du rauskommst."
        ),
        why_important=(
            "GRUB-Rettung ist eine reale Notfallsituation.\n"
            "Jeder Sysadmin wird das irgendwann brauchen.\n"
            "LPIC-1 prüft die GRUB-Shell-Befehle."
        ),
        explanation=(
            "GRUB-Shell Varianten:\n\n"
            "  grub>       : Volle Shell (GRUB geladen)\n"
            "  grub rescue>: Minimal-Shell (GRUB-Module nicht gefunden)\n\n"
            "Wichtige GRUB-Shell-Befehle:\n\n"
            "  ls                  : Partitionen auflisten\n"
            "  ls (hd0,1)/boot/    : Verzeichnis anzeigen\n"
            "  set root=(hd0,2)    : Root-Partition setzen\n"
            "  set prefix=(hd0,2)/boot/grub\n"
            "  insmod linux        : linux-Modul laden\n"
            "  linux /boot/vmlinuz root=/dev/sda2\n"
            "  initrd /boot/initrd.img\n"
            "  boot                : System starten\n\n"
            "GRUB rescue reparieren:\n"
            "  1. Live-USB booten\n"
            "  2. root mounten (mount /dev/sda2 /mnt)\n"
            "  3. chroot /mnt\n"
            "  4. grub-install /dev/sda\n"
            "  5. update-grub"
        ),
        syntax=(
            "# In der GRUB-Shell:\nls\nls (hd0,1)/\nset root=(hd0,2)\nlinux /boot/vmlinuz root=/dev/sda2 ro\ninitrd /boot/initrd.img\nboot"
        ),
        example=(
            "grub rescue> ls\n"
            "(hd0) (hd0,gpt1) (hd0,gpt2) (hd0,gpt3)\n\n"
            "grub rescue> ls (hd0,gpt2)/\n"
            "boot/ etc/ home/ usr/ var/\n\n"
            "grub rescue> set root=(hd0,gpt2)\n"
            "grub rescue> set prefix=(hd0,gpt2)/boot/grub\n"
            "grub rescue> insmod normal\n"
            "grub rescue> normal"
        ),
        task_description="Erkunde GRUB-Shell-Befehle mit 'ls' in der GRUB-Simulation.",
        expected_commands=["ls", "ls (hd0,1)/boot/"],
        hint_text="In der GRUB-Shell: ls zeigt verfügbare Partitionen",
        quiz_questions=[
            QuizQuestion(
                question="Du siehst 'grub rescue>' statt 'grub>'. Was ist der Unterschied?",
                options=[
                    "A) grub rescue ist neuer und sicherer",
                    "B) grub> hat volle Funktionen; grub rescue> ist minimal — GRUB-Module wurden nicht gefunden",
                    "C) grub rescue ist für UEFI, grub> für BIOS",
                    "D) Kein Unterschied",
                ],
                correct="B",
                explanation="grub rescue> erscheint wenn GRUB Stage 2 (/boot/grub/) nicht gefunden wurde. Sehr eingeschränkte Befehle. grub> hat volle Shell mit allen Modulen.",
            ),
            QuizQuestion(
                question="In der GRUB-Shell: Welcher Befehl listet alle gefundenen Partitionen auf?",
                options=["A) partitions", "B) list", "C) ls", "D) show devices"],
                correct="C",
                explanation="ls in der GRUB-Shell listet Partitionen (hd0), (hd0,1) etc. Oder Verzeichnisse: ls (hd0,1)/boot/",
            ),
        ],
        exam_tip=(
            "GRUB-Shell Notfallbefehle:\n"
            "ls → Partitionen sehen\n"
            "set root=(hd0,X) → Root setzen\n"
            "linux /boot/vmlinuz root=/dev/sdaX → Kernel laden\n"
            "initrd /boot/initrd.img → initramfs\n"
            "boot → starten"
        ),
        memory_tip="GRUB-Shell: ls → set root → linux → initrd → boot. Diese Reihenfolge.",
    ),

    Mission(
        mission_id="2.10",
        title="Kernel Parameters — Boot-Parameter",
        mtype="DECODE", xp=35, chapter=2,
        speaker="LYRA-7",
        story=(
            "LYRA-7: Der Kernel ist formbar beim Boot.\n"
            "root=/dev/sda1 sagt ihm wo das Root-FS liegt.\n"
            "quiet unterdrückt Ausgabe. init=/bin/bash gibt dir eine Shell.\n"
            "Kenn die Parameter — sie retten dich in Notfällen."
        ),
        why_important=(
            "Kernel-Parameter steuern das Systemverhalten beim Boot.\n"
            "LPIC-1 fragt wichtige Parameter wie root=, ro/rw, quiet, etc."
        ),
        explanation=(
            "Kernel-Parameter (Kernel Command Line)\n\n"
            "Werden vom Bootloader an den Kernel übergeben.\n"
            "In grub.cfg: linux /boot/vmlinuz <parameter>\n\n"
            "Wichtige Parameter:\n\n"
            "  root=UUID=xxx   : Root-Partition (UUID empfohlen)\n"
            "  root=/dev/sda2  : Root-Partition (Device)\n"
            "  ro              : Read-Only mounten (normal)\n"
            "  rw              : Read-Write mounten (Rescue)\n"
            "  quiet           : Weniger Boot-Meldungen\n"
            "  splash          : Plymouth Splash-Screen\n"
            "  single          : Single-User Mode\n"
            "  1               : Runlevel 1 (SysVinit)\n"
            "  systemd.unit=rescue.target : Rettungsmodus\n"
            "  init=/bin/bash  : bash als Init (Notfall)\n"
            "  nomodeset       : Keine Kernel-Mode-Setting (GPU-Fix)\n"
            "  acpi=off        : ACPI deaktivieren\n"
            "  noapic          : APIC deaktivieren\n"
            "  mem=4G          : RAM-Limit\n"
            "  elevator=deadline : I/O-Scheduler"
        ),
        syntax="cat /proc/cmdline     # Aktuelle Boot-Parameter",
        example=(
            "$ cat /proc/cmdline\n"
            "BOOT_IMAGE=/boot/vmlinuz-6.1.0-17-amd64 root=UUID=a1b2c3d4 ro quiet splash"
        ),
        task_description="Zeige die aktuellen Kernel-Boot-Parameter.",
        expected_commands=["cat /proc/cmdline"],
        hint_text="cat /proc/cmdline — zeigt aktuelle Kernel-Parameter",
        quiz_questions=[
            QuizQuestion(
                question="Du brauchst Root-Zugang zum System — das Passwort ist unbekannt. Welcher Kernel-Parameter hilft?",
                options=[
                    "A) root_override=1",
                    "B) init=/bin/bash",
                    "C) nopasswd",
                    "D) rescue=true",
                ],
                correct="B",
                explanation="init=/bin/bash startet bash direkt als PID 1 statt init/systemd — damit hast du Root-Shell ohne Passwort. Danach: mount -o remount,rw /",
            ),
            QuizQuestion(
                question="Was bewirkt der Kernel-Parameter 'ro'?",
                options=[
                    "A) Startet das System im Read-Only Modus für die gesamte Laufzeit",
                    "B) Root-Filesystem wird initial Read-Only gemountet (Normal — initramfs prüft fs, dann rw)",
                    "C) Deaktiviert alle Schreiboperationen",
                    "D) Root-Only — nur root-User darf einloggen",
                ],
                correct="B",
                explanation="ro bedeutet: Root-Filesystem initial Read-Only mounten. Das initramfs prüft und repariert das FS, dann wird es rw gemountet. Standard-Verhalten.",
            ),
        ],
        exam_tip=(
            "Kernel-Parameter für Notfall:\n"
            "init=/bin/bash → Root-Shell ohne Passwort\n"
            "single → Single-User Mode\n"
            "rw → Root-FS direkt RW (für Rettung)\n"
            "/proc/cmdline zeigt aktuelle Parameter."
        ),
        memory_tip="/proc/cmdline = aktive Kernel-Parameter. init=/bin/bash = Notfall-Root.",
    ),

    Mission(
        mission_id="2.11",
        title="cmdline lesen — /proc/cmdline",
        mtype="INFILTRATE", xp=30, chapter=2,
        speaker="SYSTEM",
        story=(
            "SYSTEM: Willst du wissen womit dein System gebootet hat?\n"
            "/proc/cmdline gibt dir die Antwort.\n"
            "Kein Raten. Kein Vermuten. Nur Fakten vom Kernel.\n"
            "Lies es. Versteh es. Dann weißt du wo du stehst."
        ),
        why_important="Aktuelle Boot-Parameter aus /proc/cmdline lesen ist Admin-Alltag.",
        explanation=(
            "/proc/cmdline — aktuelle Kernel-Parameter\n\n"
            "Zeigt genau was der Bootloader dem Kernel übergeben hat.\n\n"
            "Wichtig für:\n"
            "  Debuggen von Boot-Problemen\n"
            "  Prüfen ob Parameter aktiv sind\n"
            "  Dokumentation\n\n"
            "Parameter lesen mit systemd:\n"
            "  systemd-analyze log-level\n"
            "  kernel-command-line (in systemd-Logs)"
        ),
        syntax="cat /proc/cmdline\ncat /proc/cmdline | tr ' ' '\\n'   # eine Parameter pro Zeile",
        example=(
            "$ cat /proc/cmdline\n"
            "BOOT_IMAGE=/boot/vmlinuz-6.1.0 root=UUID=abc123 ro quiet splash\n\n"
            "$ cat /proc/cmdline | tr ' ' '\\n'\n"
            "BOOT_IMAGE=/boot/vmlinuz-6.1.0\n"
            "root=UUID=abc123\n"
            "ro\n"
            "quiet\n"
            "splash"
        ),
        task_description="Lies die aktuellen Kernel-Parameter aus.",
        expected_commands=["cat /proc/cmdline"],
        hint_text="cat /proc/cmdline",
        quiz_questions=[
            QuizQuestion(
                question="In welcher Datei findest du die aktiven Kernel-Boot-Parameter?",
                options=["A) /etc/kernel/params", "B) /boot/grub/cmdline", "C) /proc/cmdline", "D) /sys/kernel/cmdline"],
                correct="C",
                explanation="/proc/cmdline ist das virtuelle Interface zu den beim Boot übergebenen Kernel-Parametern.",
            ),
        ],
        exam_tip="/proc/cmdline = aktive Boot-Parameter. Immer verfügbar, kein root nötig.",
        memory_tip="cmdline = Kernel Command Line. /proc/cmdline = die echten, aktiven Parameter.",
    ),

    Mission(
        mission_id="2.12",
        title="initramfs — Was ist das?",
        mtype="SCAN", xp=30, chapter=2,
        speaker="DAEMON",
        story=(
            "initramfs. Initial RAM Filesystem.\n"
            "Der Kernel kann kein Root-FS mounten ohne Treiber.\n"
            "Aber Treiber sind auf dem Root-FS.\n"
            "Henne-Ei-Problem. initramfs ist die Lösung."
        ),
        why_important=(
            "initramfs verstehen ist fundamental für:\n"
            "Boot-Troubleshooting, Kernel-Updates, Rescue-Szenarien.\n"
            "LPIC-1 prüft Konzept und Verwaltungs-Tools."
        ),
        explanation=(
            "initramfs — Initial RAM Filesystem\n\n"
            "Das Problem ohne initramfs:\n"
            "  Kernel startet → will Root-FS mounten\n"
            "  Root-FS liegt auf LVM/RAID/Crypto/iSCSI\n"
            "  Dafür braucht Kernel Treiber\n"
            "  Treiber liegen auf Root-FS → Deadlock!\n\n"
            "Die Lösung:\n"
            "  initramfs = kleines, gepacktes Root-FS im RAM\n"
            "  Enthält: Treiber, Tools für echtes Root-FS\n"
            "  Kernel entpackt es in RAM → mini-Linux\n"
            "  Mini-Linux mountet echtes Root-FS\n"
            "  Übergibt Kontrolle an echtes / (pivot_root)\n\n"
            "Dateien:\n"
            "  /boot/initrd.img-<version>   (Debian/Ubuntu)\n"
            "  /boot/initramfs-<version>.img (RHEL)\n\n"
            "Format:\n"
            "  CPIO-Archiv + gzip/xz komprimiert\n"
            "  Anschauen: lsinitramfs /boot/initrd.img-*"
        ),
        syntax=(
            "ls -lh /boot/initrd.img*\n"
            "lsinitramfs /boot/initrd.img-6.1.0-17-amd64 | head -20"
        ),
        example=(
            "$ ls -lh /boot/initrd.img*\n"
            "-rw-r--r-- 1 root root 67M /boot/initrd.img-6.1.0-17-amd64\n"
            "-rw-r--r-- 1 root root 65M /boot/initrd.img-6.1.0-13-amd64\n\n"
            "$ lsinitramfs /boot/initrd.img-6.1.0-17-amd64 | head -5\n"
            ".\n"
            "./lib\n"
            "./lib/modules\n"
            "./lib/modules/6.1.0-17-amd64\n"
            "./usr/bin/busybox"
        ),
        task_description="Liste initramfs-Dateien im /boot/ Verzeichnis auf.",
        expected_commands=["ls /boot/", "ls -lh /boot/"],
        hint_text="ls /boot/ oder ls -lh /boot/ — zeigt Kernel + initramfs Dateien",
        quiz_questions=[
            QuizQuestion(
                question="Welches Problem löst das initramfs?",
                options=[
                    "A) Zu wenig RAM beim Start",
                    "B) Das Henne-Ei-Problem: Kernel braucht Treiber um Root-FS zu mounten, die auf Root-FS liegen",
                    "C) Zu langsamen Boot-Prozess",
                    "D) Fehlendes Root-Passwort",
                ],
                correct="B",
                explanation="initramfs löst das Henne-Ei-Problem: Kernel braucht Treiber (für LVM/RAID/Crypto), die auf Root-FS liegen. initramfs enthält diese Treiber im RAM.",
            ),
            QuizQuestion(
                question="In welchem Format wird initramfs gespeichert?",
                options=["A) tar.gz", "B) ISO 9660", "C) CPIO + komprimiert", "D) ext4"],
                correct="C",
                explanation="initramfs ist ein CPIO-Archiv (cpio), typisch mit gzip oder xz komprimiert. Kann mit 'cpio -t < initrd' oder 'lsinitramfs' inspiziert werden.",
            ),
        ],
        exam_tip=(
            "initramfs vs initrd:\n"
            "initrd (alte Methode) = Block-Device Image (ext2)\n"
            "initramfs (modern) = CPIO-Archiv, direkt ins RAM\n"
            "LPIC-1 nutzt oft 'initrd' als Oberbegriff für beide."
        ),
        memory_tip="initramfs = mini-Linux im RAM für den Boot. Löst Treiber-Deadlock.",
    ),

    Mission(
        mission_id="2.13",
        title="mkinitramfs / update-initramfs",
        mtype="INFILTRATE", xp=35, chapter=2,
        speaker="DAEMON",
        story=(
            "DAEMON: initramfs — das temporäre Root-FS beim Booten.\n"
            "Enthält Module die der Kernel vor dem echten Root braucht.\n"
            "Neues Modul? Neuer Kernel? update-initramfs -u.\n"
            "Vergiss das — und dein System bootet beim nächsten Mal nicht."
        ),
        why_important="Nach Kernel-Modul-Änderungen muss initramfs neu erstellt werden.",
        explanation=(
            "initramfs verwalten (Debian/Ubuntu):\n\n"
            "  update-initramfs -u\n"
            "    → Aktuellen Kernel aktualisieren (-u = update)\n\n"
            "  update-initramfs -u -k all\n"
            "    → Alle installierten Kernel\n\n"
            "  update-initramfs -c -k 6.1.0-17-amd64\n"
            "    → Neues initramfs erstellen (-c = create)\n\n"
            "  mkinitramfs -o /boot/initrd.img-6.1.0 6.1.0\n"
            "    → Direkt mit mkinitramfs erstellen\n\n"
            "RHEL/CentOS:\n"
            "  dracut -f\n"
            "    → initramfs neu erstellen (dracut = Tool)\n"
            "  dracut -f /boot/initramfs-$(uname -r).img $(uname -r)"
        ),
        syntax=(
            "update-initramfs -u              # Aktuellen Kernel\n"
            "update-initramfs -u -k all       # Alle Kernel\n"
            "dracut -f                        # RHEL/CentOS"
        ),
        example=(
            "$ sudo update-initramfs -u\n"
            "update-initramfs: Generating /boot/initrd.img-6.1.0-17-amd64\n"
            "cryptsetup: WARNING: resume target not configured\n"
            "I: The initramfs will attempt to resume from /dev/nvme0n1p2"
        ),
        task_description="Zeige Hilfe zu update-initramfs.",
        expected_commands=["update-initramfs -u", "man update-initramfs"],
        hint_text="update-initramfs -u aktualisiert das initramfs",
        quiz_questions=[
            QuizQuestion(
                question="Du hast einen neuen Treiber als Kernel-Modul installiert. Was musst du danach tun damit er beim Boot verfügbar ist?",
                options=[
                    "A) Nur neustarten",
                    "B) modprobe <modul> ausführen",
                    "C) update-initramfs -u ausführen, dann neustarten",
                    "D) Den Kernel neu kompilieren",
                ],
                correct="C",
                explanation="Neue Module müssen ins initramfs damit sie beim frühen Boot verfügbar sind. update-initramfs -u regeneriert das initramfs, dann Reboot.",
            ),
        ],
        exam_tip=(
            "Debian/Ubuntu: update-initramfs -u\n"
            "RHEL/CentOS:  dracut -f\n"
            "Beide nach Kernel-Modul-Änderungen nötig!"
        ),
        memory_tip="Modul geändert → update-initramfs -u → Reboot. Diese drei Schritte.",
    ),

    Mission(
        mission_id="2.14",
        title="/boot/ Verzeichnis — Kernel Image",
        mtype="SCAN", xp=30, chapter=2,
        speaker="SYSTEM",
        story=(
            "SYSTEM: /boot/ — hier schläft der Kernel.\n"
            "vmlinuz: komprimiertes Kernel-Image.\n"
            "initrd.img: das frühe Root-Dateisystem.\n"
            "System.map: Kernel-Symbol-Tabelle. Kenn die Bewohner."
        ),
        why_important="Kenntnis der /boot/-Dateien ist Grundlage für Boot-Management.",
        explanation=(
            "/boot/ — Boot-Verzeichnis\n\n"
            "Dateien:\n"
            "  vmlinuz-<version>      : Komprimierter Kernel (z-komprimiert)\n"
            "  initrd.img-<version>   : initramfs (Debian/Ubuntu)\n"
            "  initramfs-<ver>.img    : initramfs (RHEL/CentOS)\n"
            "  System.map-<version>   : Kernel-Symboltabelle\n"
            "  config-<version>       : Kernel-Build-Konfiguration\n"
            "  grub/                  : GRUB2-Verzeichnis\n"
            "  efi/                   : EFI-Partition (falls gemountet)\n\n"
            "vmlinuz:\n"
            "  vm = Virtual Memory (supports paging)\n"
            "  linu = linux\n"
            "  z = compressed (zlib/gzip/xz)\n\n"
            "bzImage vs vmlinuz:\n"
            "  bzImage = Build-Artifact (im Kernel-Sourcetree)\n"
            "  vmlinuz = Kopie von bzImage in /boot/"
        ),
        syntax="ls -lh /boot/\nfile /boot/vmlinuz-*",
        example=(
            "$ ls -lh /boot/\n"
            "total 234M\n"
            "-rw-r--r-- 1 root root 237K config-6.1.0-17-amd64\n"
            "drwxr-xr-x 5 root root 4.0K grub/\n"
            "-rw-r--r-- 1 root root  67M initrd.img-6.1.0-17-amd64\n"
            "-rw-r--r-- 1 root root 3.9M System.map-6.1.0-17-amd64\n"
            "-rw-r--r-- 1 root root  11M vmlinuz-6.1.0-17-amd64"
        ),
        task_description="Liste den /boot/ Ordner mit Dateigrößen auf.",
        expected_commands=["ls -lh /boot/", "ls /boot/"],
        hint_text="ls -lh /boot/ — lh zeigt human-readable Größen",
        quiz_questions=[
            QuizQuestion(
                question="Was ist 'vmlinuz' in /boot/?",
                options=[
                    "A) Eine virtuelle Maschinen-Konfiguration",
                    "B) Der komprimierte Linux-Kernel",
                    "C) Ein Log-File des Kernels",
                    "D) Die GRUB-Konfiguration",
                ],
                correct="B",
                explanation="vmlinuz = vm (virtual memory) + linu (linux) + z (compressed). Der komprimierte Kernel-Image der in RAM geladen wird.",
            ),
        ],
        exam_tip=(
            "/boot/ Dateien kennen:\n"
            "vmlinuz = Kernel\n"
            "initrd.img / initramfs = initiales RAM-Filesystem\n"
            "System.map = Kernel-Symboltabelle (für Debugging)\n"
            "config = Kernel-Build-Konfig"
        ),
        memory_tip="vmlinuz = Kernel. initrd.img = initramfs. System.map = Symbole.",
    ),

    Mission(
        mission_id="2.15",
        title="Kernel Version — uname",
        mtype="INFILTRATE", xp=25, chapter=2,
        speaker="SYSTEM",
        story=(
            "SYSTEM: Welche Kernel-Version läuft hier?\n"
            "uname -r — eine Sekunde, eine Antwort.\n"
            "uname -a gibt dir alles: Kernel, Hostname, Architektur.\n"
            "Erstes Kommando auf jedem neuen System."
        ),
        why_important="uname liefert Kernel-Version und System-Infos — Admin-Alltag.",
        explanation=(
            "uname — System-Informationen\n\n"
            "Flags:\n"
            "  -r : Kernel-Release (Version)\n"
            "  -n : Nodename (Hostname)\n"
            "  -s : Kernel-Name (Linux)\n"
            "  -m : Maschinentyp (x86_64, arm64)\n"
            "  -p : Prozessortyp\n"
            "  -i : Hardware-Plattform\n"
            "  -o : Betriebssystem (GNU/Linux)\n"
            "  -v : Kernel-Version (Build-Datum)\n"
            "  -a : ALLE Informationen\n\n"
            "Ausgabe von uname -a:\n"
            "  Linux neongrid9 6.1.0-17-amd64 #1 SMP PREEMPT_DYNAMIC\n"
            "  ─────────────────────────────────────────────────\n"
            "  OS   hostname  kernel-release  kernel-version(build)"
        ),
        syntax="uname -r    # Nur Kernel-Version\nuname -a    # Alles",
        example=(
            "$ uname -r\n"
            "6.1.0-17-amd64\n\n"
            "$ uname -a\n"
            "Linux neongrid9 6.1.0-17-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.69-1 x86_64 GNU/Linux"
        ),
        task_description="Zeige die aktuelle Kernel-Version.",
        expected_commands=["uname -r"],
        hint_text="uname -r gibt die Kernel-Release-Nummer aus",
        quiz_questions=[
            QuizQuestion(
                question="Welcher uname-Flag zeigt die Kernel-Release-Version?",
                options=["A) uname -v", "B) uname -r", "C) uname -k", "D) uname -n"],
                correct="B",
                explanation="uname -r = Kernel Release (z.B. 6.1.0-17-amd64). -v = Kernel Version (Build-Datum/Nummer). -a = alles.",
            ),
        ],
        exam_tip="uname -r = Release. uname -a = alles. Merke: r=Release (die Versionsnummer).",
        memory_tip="uname -r = Kernel-Release. uname -a = alle Infos.",
    ),

    Mission(
        mission_id="2.16",
        title="UEFI Boot — efibootmgr",
        mtype="INFILTRATE", xp=40, chapter=2,
        speaker="ZARA Z3R0",
        story=(
            "Zara Z3R0: 'UEFI hat seine eigene Boot-Liste, Ghost.\n"
            " efibootmgr zeigt sie dir. Einträge hinzufügen, löschen, sortieren.\n"
            " Dual-Boot durcheinander? efibootmgr --bootorder ändert die Reihenfolge.\n"
            " Lern das — bevor du das falsche System boot-löscht.'"
        ),
        why_important=(
            "efibootmgr verwaltet UEFI-Boot-Einträge.\n"
            "Notwendig wenn System doppelt bootet oder Bootloader-Ordnung geändert werden muss."
        ),
        explanation=(
            "efibootmgr — EFI Boot Manager\n\n"
            "Anzeigen:\n"
            "  efibootmgr            : Boot-Einträge anzeigen\n"
            "  efibootmgr -v         : Verbose\n\n"
            "Eintrag erstellen:\n"
            "  efibootmgr -c -d /dev/sda -p 1 -L 'Debian' -l '\\EFI\\debian\\grubx64.efi'\n\n"
            "Eintrag löschen:\n"
            "  efibootmgr -b 0002 -B\n\n"
            "Boot-Reihenfolge ändern:\n"
            "  efibootmgr -o 0001,0000,0002\n\n"
            "Einmalig anderen Eintrag nutzen:\n"
            "  efibootmgr -n 0002    (bootnext)\n\n"
            "Ausgabe-Felder:\n"
            "  BootCurrent : aktuell genutzter Eintrag\n"
            "  BootOrder   : Reihenfolge\n"
            "  Boot0001*   : Stern = aktiv"
        ),
        syntax="efibootmgr\nefibootmgr -v\nefibootmgr -o 0001,0000    # Reihenfolge ändern",
        example=(
            "$ efibootmgr\n"
            "BootCurrent: 0001\n"
            "Timeout: 5 seconds\n"
            "BootOrder: 0001,0000,0003\n"
            "Boot0000  Windows Boot Manager\n"
            "Boot0001* debian\n"
            "Boot0003  UEFI: USB SanDisk"
        ),
        task_description="Zeige UEFI-Boot-Einträge mit efibootmgr.",
        expected_commands=["efibootmgr"],
        hint_text="efibootmgr — EFI Boot Manager",
        quiz_questions=[
            QuizQuestion(
                question="Was macht 'efibootmgr -o 0001,0000'?",
                options=[
                    "A) Löscht Boot-Eintrag 0001 und 0000",
                    "B) Setzt die Boot-Reihenfolge: zuerst 0001, dann 0000",
                    "C) Erstellt zwei neue Boot-Einträge",
                    "D) Aktiviert Einträge 0001 und 0000",
                ],
                correct="B",
                explanation="-o setzt BootOrder. 0001,0000 = zuerst Eintrag 0001, dann 0000. Persistent über Reboots.",
            ),
        ],
        exam_tip=(
            "efibootmgr = UEFI-Boot-Einträge verwalten.\n"
            "-c = create, -B = delete, -o = order.\n"
            "Erfordert: UEFI-System + root + ESP gemountet."
        ),
        memory_tip="efibootmgr = EFI Boot Manager. -o = Reihenfolge. * = aktiv.",
    ),

    Mission(
        mission_id="2.17",
        title="Secure Boot — Konzept",
        mtype="SCAN", xp=25, chapter=2,
        speaker="LYRA-7",
        story=(
            "LYRA-7: Secure Boot — Freund oder Feind?\n"
            "Es schützt vor unsignierten Bootloadern. Gut gegen Rootkits.\n"
            "Aber: unsigned Kernel-Module werden blockiert.\n"
            "Kenn das Konzept. Die Prüfung fragt es — mit Fallstricken."
        ),
        why_important="Secure Boot beeinflusst welche Kernel/Module geladen werden können.",
        explanation=(
            "Secure Boot — UEFI-Sicherheitsmechanismus\n\n"
            "Funktionsweise:\n"
            "  UEFI prüft digitale Signatur des Bootloaders\n"
            "  → Nur signierte Bootloader dürfen starten\n"
            "  → Nur signierte Kernel\n"
            "  → Nur signierte Kernel-Module\n\n"
            "Signierungsschlüssel:\n"
            "  Platform Key (PK)   : UEFI-Hersteller\n"
            "  Key Exchange Key (KEK): OS-Hersteller\n"
            "  Database (db)       : Erlaubte Signaturen\n"
            "  Forbidden (dbx)     : Gesperrte Signaturen\n\n"
            "Linux + Secure Boot:\n"
            "  Shim → GRUB → Kernel (alle signiert)\n"
            "  Microsoft signiert shim → läuft auf allen PCs\n\n"
            "Prüfen ob Secure Boot aktiv:\n"
            "  mokutil --sb-state\n"
            "  dmesg | grep -i 'secure boot'"
        ),
        syntax=(
            "mokutil --sb-state           # Secure Boot Status\n"
            "dmesg | grep -i 'secure boot'"
        ),
        example=(
            "$ mokutil --sb-state\n"
            "SecureBoot enabled\n\n"
            "$ dmesg | grep -i 'secure'\n"
            "[    0.012345] Secure boot enabled"
        ),
        task_description="Zeige den Secure Boot Status mit dmesg.",
        expected_commands=["mokutil --sb-state", "dmesg | grep -i secure"],
        hint_text="mokutil --sb-state oder dmesg | grep -i 'secure boot'",
        quiz_questions=[
            QuizQuestion(
                question="Was überprüft Secure Boot beim Systemstart?",
                options=[
                    "A) Ob alle Festplatten verschlüsselt sind",
                    "B) Ob Bootloader und Kernel digital signiert sind",
                    "C) Ob das BIOS-Passwort korrekt ist",
                    "D) Ob der RAM defektfrei ist",
                ],
                correct="B",
                explanation="Secure Boot prüft kryptografische Signaturen: UEFI → Shim → GRUB → Kernel → Module. Nur signierter Code darf starten.",
            ),
        ],
        exam_tip="Secure Boot: mokutil --sb-state prüft den Status. Verhindert unsignierte Kernel-Module.",
        memory_tip="Secure Boot = Signatur-Kette von UEFI bis Kernel. mokutil = Verwaltung.",
    ),

    Mission(
        mission_id="2.18",
        title="Prüfungsfalle: GRUB Legacy vs GRUB2",
        mtype="QUIZ", xp=25, chapter=2,
        speaker="KERNEL-ORAKEL",
        story="Das Orakel warnt dich: GRUB Legacy und GRUB2 — häufige Verwechslung.",
        why_important="GRUB Legacy vs GRUB2 ist eine der häufigsten Prüfungsfallen in LPIC-1: unterschiedliche Konfigurationsdateien, unterschiedliche Befehle.",
        quiz_questions=[
            QuizQuestion(
                question="Wo liegt die Konfigurationsdatei von GRUB Legacy (GRUB 1)?",
                options=[
                    "A) /boot/grub/grub.cfg",
                    "B) /etc/default/grub",
                    "C) /boot/grub/menu.lst",
                    "D) /boot/grub/grub.conf",
                ],
                correct="C",
                explanation="GRUB Legacy (0.97) nutzt /boot/grub/menu.lst (Debian) oder /boot/grub/grub.conf (RHEL). GRUB2 nutzt /boot/grub/grub.cfg.",
                xp_value=20,
            ),
            QuizQuestion(
                question="Welcher Befehl installiert GRUB2 in den MBR unter Debian?",
                options=["A) grub-legacy-install", "B) grub-install", "C) grub2-setup", "D) install-grub"],
                correct="B",
                explanation="grub-install (Debian) oder grub2-install (RHEL). Auf Debian ist 'grub-install' schon GRUB2.",
                xp_value=20,
            ),
            QuizQuestion(
                question="Was ist der korrekte Weg um GRUB2-Konfiguration anzupassen?",
                options=[
                    "A) /boot/grub/grub.cfg direkt bearbeiten",
                    "B) /etc/default/grub bearbeiten + update-grub ausführen",
                    "C) grub-edit-config verwenden",
                    "D) Grub2 hat keine anpassbare Konfiguration",
                ],
                correct="B",
                explanation="/etc/default/grub für Einstellungen, dann update-grub. grub.cfg ist automatisch generiert und darf NICHT manuell bearbeitet werden.",
                xp_value=20,
            ),
        ],
        exam_tip=(
            "GRUB Legacy: /boot/grub/menu.lst\n"
            "GRUB2:       /boot/grub/grub.cfg (generiert!)\n"
            "User-Config: /etc/default/grub (GRUB2)"
        ),
        memory_tip="menu.lst = GRUB 1. grub.cfg = GRUB 2 (generiert). /etc/default/grub = Einstellungen.",
    ),

    Mission(
        mission_id="2.19",
        title="Prüfungsfalle: initrd vs initramfs",
        mtype="QUIZ", xp=25, chapter=2,
        speaker="KERNEL-ORAKEL",
        story=(
            "KERNEL-ORAKEL: initrd und initramfs — scheinbar gleich.\n"
            "Aber ein Block-Device versus ein tmpfs sind zwei Welten.\n"
            "Die Prüfung liebt diese Falle. Kenn den echten Unterschied.\n"
            "Ein falsches Ankreuzen kostet Punkte."
        ),
        why_important="initrd vs initramfs ist LPIC-1-Prüfungswissen: unterschiedliche Implementierungen des frühen Userspace, der Kernel-Module vor dem Root-Mount lädt.",
        quiz_questions=[
            QuizQuestion(
                question="Was ist der technische Unterschied zwischen initrd und initramfs?",
                options=[
                    "A) Beide sind identisch, nur unterschiedliche Namen",
                    "B) initrd = Block-Device-Image (ext2), initramfs = CPIO-Archiv direkt im RAM",
                    "C) initramfs ist älter als initrd",
                    "D) initrd ist für UEFI, initramfs für BIOS",
                ],
                correct="B",
                explanation="initrd (alt) = echtes Block-Device-Image, wird als /dev/ram0 gemountet. initramfs (modern) = CPIO-Archiv das direkt in tmpfs entpackt wird, effizienter.",
                xp_value=25,
            ),
            QuizQuestion(
                question="Welches Tool erstellt auf RHEL/CentOS das initramfs neu?",
                options=["A) mkinitramfs", "B) update-initramfs", "C) dracut", "D) initramfs-tools"],
                correct="C",
                explanation="RHEL/CentOS/Fedora: dracut -f. Debian/Ubuntu: update-initramfs -u oder mkinitramfs.",
                xp_value=20,
            ),
        ],
        exam_tip="initramfs-Tools:\nDebian/Ubuntu: update-initramfs -u\nRHEL/CentOS: dracut -f",
        memory_tip="dracut = RHEL initramfs. update-initramfs = Debian initramfs.",
    ),

    Mission(
        mission_id="2.BOSS",
        title="BOSS: Dead Boot Recovery",
        mtype="BOSS", xp=225, chapter=2,
        speaker="DAEMON",
        boss_name="DEAD BOOT — System Startet Nicht",
        boss_desc="Das System bootet nicht. Drei Phasen. Repariere jeden Fehler.",
        ascii_art="""
  ██████╗ ███████╗ █████╗ ██████╗     ██████╗  ██████╗  ██████╗ ████████╗
  ██╔══██╗██╔════╝██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝
  ██║  ██║█████╗  ███████║██║  ██║    ██████╔╝██║   ██║██║   ██║   ██║
  ██║  ██║██╔══╝  ██╔══██║██║  ██║    ██╔══██╗██║   ██║██║   ██║   ██║
  ██████╔╝███████╗██║  ██║██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝   ██║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝

  ┌─ BOOT SEQUENCE FAILED ────────────────────────────────────────────┐
  │  GRUB Error 15: File not found                                    │
  │  Kernel panic - not syncing: VFS: Unable to mount root fs         │
  │  initrd: MISSING                                                  │
  │  >> Recovery Mode: [MANUAL INTERVENTION REQUIRED]                 │
  └───────────────────────────────────────────────────────────────────┘

                    ⚡ CHAOSWERK FACTION :: CHAPTER 2 BOSS ⚡""",
        story_transitions = [
            "DEAD BOOT starrt dich an. Kein GRUB-Menü. Nur Stille.",
            "grub-install läuft. Der Daemon versucht es zu stoppen.",
            "initramfs rebuild. Kernel-Parameter gesetzt. Fast da.",
            "Letzter Reboot. Entweder bootet es — oder nicht.",
        ],
        why_important="Boot-Recovery ist eine kritische Sysadmin-Fähigkeit. GRUB reparieren, Kernel-Parameter debuggen und initramfs verstehen sind LPIC-1-Kern-Skills.",
        story=(
            "Das Schlimmste ist eingetreten.\n"
            "System bootet nicht. GRUB defekt. Kernel nicht gefunden.\n"
            "Drei Fehler. Drei Phasen.\n\n"
            "PHASE 1: MBR-Typ identifizieren\n"
            "PHASE 2: GRUB-Config regenerieren\n"
            "PHASE 3: Kernel-Parameter auslesen\n\n"
            "DAEMON: 'Niemand repariert ein System ohne dieses Wissen.'"
        ),
        task_description=(
            "Identifiziere ob die Disk MBR oder GPT nutzt."
            "||"
            "Regeneriere die GRUB2-Konfiguration."
            "||"
            "Lies die aktiven Kernel-Boot-Parameter aus."
        ),
        expected_commands=["fdisk -l /dev/nvme0n1", "update-grub", "cat /proc/cmdline"],
        hints = [
            "Das Verzeichnis oder die Datei befinden sich unter '/dev/nvme0n1'. Der Befehl beginnt mit 'fdisk'.",
            "Versuche: fdisk -l /dev/nvme0n1",
            "Der vollständige Befehl: fdisk -l /dev/nvme0n1",
        ],
        quiz_questions=[
            QuizQuestion(
                question="System bootet nicht: GRUB zeigt 'grub rescue>'. Erster Schritt?",
                options=[
                    "A) Sofort neu installieren",
                    "B) ls in GRUB-Shell um Partitionen zu finden",
                    "C) Power-Taste drücken",
                    "D) Windows installieren",
                ],
                correct="B",
                explanation="In grub rescue>: ls zeigt verfügbare Partitionen. Dann: set root=(hd0,X), set prefix=..., insmod normal, normal",
                xp_value=25,
            ),
            QuizQuestion(
                question="Nach manueller Änderung von /etc/default/grub — was MUSS als nächstes passieren?",
                options=[
                    "A) Reboot",
                    "B) update-grub ausführen um grub.cfg zu regenerieren",
                    "C) grub-install erneut ausführen",
                    "D) Nichts — Änderungen gelten sofort",
                ],
                correct="B",
                explanation="update-grub muss ausgeführt werden um /boot/grub/grub.cfg zu regenerieren. Erst dann werden die Änderungen beim nächsten Boot wirksam.",
                xp_value=20,
            ),
            QuizQuestion(
                question="Du willst nach einem Kernel-Crash die vorherigen Boot-Logs analysieren. Welcher Befehl?",
                options=[
                    "A) dmesg --previous",
                    "B) journalctl -b -1",
                    "C) cat /var/log/boot.old",
                    "D) last-boot --logs",
                ],
                correct="B",
                explanation="journalctl -b -1 zeigt den Journal des vorherigen Boots. -b = boot, -1 = einen Boot zurück. Erfordert persistentes Journal (/var/log/journal/).",
                xp_value=20,
            ),
            QuizQuestion(
                question="Was enthält /proc/cmdline?",
                options=[
                    "A) Die aktuell laufenden Befehle",
                    "B) Die Kernel-Parameter des aktuellen Boots (von GRUB übergeben)",
                    "C) Die GRUB-Konfiguration",
                    "D) Die letzte ausgeführte Shell-Befehlszeile",
                ],
                correct="B",
                explanation="/proc/cmdline zeigt die Kernel-Bootparameter des laufenden Systems (z.B. root=/dev/sda1 quiet splash). Diese wurden beim Boot von GRUB an den Kernel übergeben.",
                xp_value=25,
            ),
            QuizQuestion(
                question="Was ist initramfs und warum wird es beim Boot benötigt?",
                options=[
                    "A) Eine RAM-Disk mit Minimaltools um das Root-Dateisystem zu mounten bevor der echte Kernel startet",
                    "B) Eine Swap-Partition im RAM",
                    "C) Der GRUB-Bootloader im RAM",
                    "D) Eine temporäre BIOS-Erweiterung",
                ],
                correct="A",
                explanation="initramfs (initial RAM filesystem) ist ein komprimiertes cpio-Archiv das als temporäres Root-FS geladen wird. Es enthält Treiber und Tools um das echte Root-FS zu finden und zu mounten (z.B. bei verschlüsseltem Disk oder LVM).",
                xp_value=25,
            ),
        ],
        exam_tip=(
            "Boot-Reihenfolge LPIC-1:\n"
            "POST → BIOS/UEFI → GRUB2 → Kernel → initramfs → Init\n\n"
            "Dateien:\n"
            "/etc/default/grub → grub.cfg via update-grub\n"
            "/boot/vmlinuz     → Kernel\n"
            "/boot/initrd.img  → initramfs\n"
            "/proc/cmdline     → aktive Parameter"
        ),
        gear_reward="kernel_beacon",
        faction_reward=("Kernel Syndicate", 15),
        memory_tip="BOSS besiegt! Kernel Protocol — Boot komplett verstanden.",
    ),
]
