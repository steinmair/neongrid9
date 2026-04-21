"""
NeonGrid-9 :: Kapitel 4 — PARTITION WARS
LPIC-1 Topic 104.1 + 104.2 — Festplatten-Partitionierung & Filesysteme

"In NeonGrid-9 ist jede Partition ein Territorium.
 Wer das Layout nicht kennt, verliert seine Daten."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_4_MISSIONS: list[Mission] = [

    # ══════════════════════════════════════════════════════════════════════
    # 4.01 — MBR vs GPT Konzept
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.01",
        chapter      = 4,
        title        = "MBR vs GPT — Territorien der Alten Welt",
        mtype        = "SCAN",
        xp           = 60,
        speaker      = "RUST",
        story        = (
            "Der Datenmarkt in Sektor 4 ist ein Schlachtfeld.\n"
            "Alte MBR-Festplatten kämpfen gegen moderne GPT-Laufwerke.\n"
            "Beide speichern Partitionstabellen — aber völlig unterschiedlich.\n"
            "Rust murmelt: 'Kenn dein Laufwerk, Ghost.'"
        ),
        why_important = (
            "Partitionstabellen bestimmen wie Daten organisiert werden.\n"
            "LPIC-1 prüft MBR vs GPT: Limits, Unterschiede, Tools.\n"
            "Als Sysadmin musst du erkennen, welches Format vorliegt."
        ),
        explanation  = (
            "PARTITIONSTABELLEN — zwei Standards:\n\n"
            "MBR (Master Boot Record):\n"
            "  - 1. Sektor (512 Bytes) der Festplatte\n"
            "  - Max. 4 primäre Partitionen\n"
            "  - Max. Festplattengröße: 2 TB (32-bit LBA)\n"
            "  - Enthält auch den Bootloader (446 Bytes)\n"
            "  - Extended + Logical: mehr als 4 möglich\n\n"
            "GPT (GUID Partition Table):\n"
            "  - Teil des UEFI-Standards\n"
            "  - Bis zu 128 Partitionen (unter Linux)\n"
            "  - Max. Festplattengröße: 9.4 ZB (64-bit LBA)\n"
            "  - Redundante Partitionstabelle (Anfang + Ende)\n"
            "  - fdisk -l zeigt: 'Disklabel type: gpt'"
        ),
        ascii_art = """
  ██████╗  █████╗ ██████╗ ████████╗██╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
  ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
  ██████╔╝███████║██████╔╝   ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║███████╗
  ██╔═══╝ ██╔══██║██╔══██╗   ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
  ██║     ██║  ██║██║  ██║   ██║   ██║   ██║   ██║╚██████╔╝██║ ╚████║███████║
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝

  [ CHAPTER 04 :: DISK & PARTITIONS ]
  > Scanning block devices... MBR/GPT structures detected.""",
        story_transitions = [
            "Die Festplatte rotiert. Sektoren warten auf Befehle.",
            "GPT-Header erkannt. 128 Partitionseinträge. Platz für Daten.",
            "mkfs formatiert. mount bindet ein. Daten fließen.",
            "Kein Dateisystem — kein Speicher. Versteh die Grundlagen.",
        ],
        syntax       = "fdisk -l              # alle Partitionstabellen anzeigen\nfdisk -l /dev/nvme0n1 # ein Laufwerk",
        example      = (
            "$ fdisk -l /dev/nvme0n1\n"
            "Disk /dev/nvme0n1: 476.94 GiB\n"
            "Disklabel type: gpt\n"
            "Device             Start   End     Size  Type\n"
            "/dev/nvme0n1p1     2048    1050623 512M  EFI System\n"
            "/dev/nvme0n1p2  1050624    3147775   1G  Linux filesystem\n"
            "/dev/nvme0n1p3  3147776 ...       475G  Linux filesystem"
        ),
        task_description  = "Zeige die Partitionstabelle von /dev/nvme0n1",
        expected_commands = ["fdisk -l"],
        hint_text         = "fdisk mit Flag -l listet alle Partitionstabellen auf",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welche maximale Festplattengröße unterstützt MBR?',
                options     = ['A) 4 TB', 'B) 2 TB', 'C) 8 TB', 'D) 1 TB'],
                correct     = 'B',
                explanation = 'MBR nutzt 32-bit LBA → max 2 TB. GPT nutzt 64-bit → praktisch unbegrenzt.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wie viele primäre Partitionen erlaubt MBR maximal?',
                options     = ['A) 8', 'B) 16', 'C) 4', 'D) 128'],
                correct     = 'C',
                explanation = 'MBR: max 4 primäre Partitionen. Mehr geht nur mit Extended+Logical.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "MBR: max 4 primäre Partitionen, max 2 TB.\n"
            "GPT: bis 128 Partitionen, praktisch unbegrenzt.\n"
            "'Disklabel type: gpt' in fdisk -l = GPT-Laufwerk.\n"
            "EFI System Partition = erste GPT-Partition für UEFI-Boot."
        ),
        memory_tip        = "MBR = alt + 2TB-Limit + 4 Partitionen. GPT = neu + UEFI + 128 Partitionen.",
        gear_reward       = None,
        faction_reward    = ("Kernel Syndicate", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.02 — fdisk — MBR-Partitionen verwalten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.02",
        chapter      = 4,
        title        = "fdisk — Der MBR-Hammer",
        mtype        = "INFILTRATE",
        xp           = 75,
        speaker      = "RUST",
        story        = (
            "Im Untergeschoss des Datenmarkts trifft Ghost auf 'Rust',\n"
            "einen alten Hacker mit verwitterten Fingern.\n"
            "'fdisk ist das Werkzeug der Alten,' sagt Rust.\n"
            "'Lern es — die alten MBR-Systeme sind überall.'"
        ),
        why_important = (
            "fdisk ist das älteste und am häufigsten genutzte Partitions-Tool.\n"
            "LPIC-1 fragt nach fdisk-Interaktionen und Partition-Typen."
        ),
        explanation  = (
            "fdisk — interaktiver Partitions-Editor (MBR & GPT):\n\n"
            "Auflisten:\n"
            "  fdisk -l             # alle Festplatten\n"
            "  fdisk -l /dev/sda    # nur /dev/sda\n\n"
            "Interaktiv starten:\n"
            "  fdisk /dev/sda       # ACHTUNG: Root-Rechte nötig!\n\n"
            "Interaktive Befehle:\n"
            "  m    — Hilfe anzeigen\n"
            "  p    — Partitionstabelle anzeigen\n"
            "  n    — Neue Partition erstellen\n"
            "  d    — Partition löschen\n"
            "  t    — Partition-Typ ändern\n"
            "  w    — Änderungen SCHREIBEN und beenden\n"
            "  q    — Beenden OHNE Speichern\n\n"
            "Partition-Typen (Hex-Codes):\n"
            "  83   — Linux (Standard)\n"
            "  82   — Linux Swap\n"
            "  8e   — Linux LVM\n"
            "  ef   — EFI System\n"
            "  fd   — Linux RAID auto"
        ),
        syntax       = "fdisk -l\nfdisk /dev/sda    # interaktiv",
        example      = (
            "$ fdisk /dev/sda\n"
            "Command (m for help): p    # anzeigen\n"
            "Command (m for help): n    # neue Partition\n"
            "Command (m for help): t    # Typ ändern\n"
            "Command (m for help): w    # schreiben!"
        ),
        task_description  = "Zeige alle Partitionen mit fdisk",
        expected_commands = ["fdisk -l"],
        hint_text         = "fdisk -l zeigt alle Partitionstabellen (kein interaktiver Modus)",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welcher fdisk-Befehl schreibt Änderungen permanent auf die Platte?',
                options     = ['A) s', 'B) w', 'C) q', 'D) p'],
                correct     = 'B',
                explanation = "'w' in fdisk = Write. Ohne 'w' werden keine Änderungen gespeichert.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was ist der Hex-Code für eine Linux-Partition in fdisk?',
                options     = ['A) ef', 'B) 82', 'C) 83', 'D) 8e'],
                correct     = 'C',
                explanation = '83 = Linux, 82 = Linux Swap, 8e = Linux LVM, ef = EFI System.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "fdisk-Falle: Änderungen werden erst mit 'w' geschrieben!\n"
            "Kein 'w' = keine Änderungen = sicher zum Üben.\n"
            "fdisk kann MBR und GPT verwalten, aber gdisk ist für GPT besser."
        ),
        memory_tip        = "'w' in fdisk = Write = Schreiben. Ohne 'w' passiert nichts permanent.",
        gear_reward       = None,
        faction_reward    = ("Kernel Syndicate", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.03 — gdisk — GPT-Partitionen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.03",
        chapter      = 4,
        title        = "gdisk — Der GPT-Chirurg",
        mtype        = "INFILTRATE",
        xp           = 75,
        speaker      = "RUST",
        story        = (
            "Rust zeigt auf ein nagelneues NVMe-Laufwerk:\n"
            "'Für GPT-Laufwerke brauchst du gdisk, Ghost.\n"
            " fdisk kann GPT lesen, aber gdisk versteht es wirklich.'"
        ),
        why_important = (
            "Moderne Systeme mit UEFI nutzen GPT.\n"
            "gdisk ist der native GPT-Editor. LPIC-1 prüft GPT-Grundlagen."
        ),
        explanation  = (
            "gdisk — GPT-optimierter Partitions-Editor:\n\n"
            "  gdisk /dev/nvme0n1    # startet interaktiven Modus\n"
            "  gdisk -l /dev/nvme0n1 # nur auflisten\n\n"
            "Interaktive Befehle (ähnlich fdisk):\n"
            "  ?    — Hilfe\n"
            "  p    — Partitionstabelle anzeigen\n"
            "  n    — Neue Partition\n"
            "  d    — Partition löschen\n"
            "  t    — Typ ändern (GUID-Codes)\n"
            "  w    — Schreiben und beenden\n"
            "  q    — Beenden ohne Speichern\n\n"
            "GPT-Typ-Codes (4-stellige Hex):\n"
            "  8300 — Linux filesystem\n"
            "  8200 — Linux swap\n"
            "  8e00 — Linux LVM\n"
            "  ef00 — EFI System Partition\n"
            "  fd00 — Linux RAID\n\n"
            "sgdisk — Skript-freundliche Variante:\n"
            "  sgdisk -p /dev/nvme0n1         # print\n"
            "  sgdisk --zap-all /dev/nvme0n1  # Tabelle löschen"
        ),
        syntax       = "gdisk -l /dev/nvme0n1\ngdisk /dev/nvme0n1   # interaktiv",
        example      = "$ gdisk -l /dev/nvme0n1\nGPT fdisk (gdisk) version 1.0.8\nPartition table scan: GPT present",
        task_description  = "Zeige die Partitionstabelle",
        expected_commands = ["fdisk -l"],
        hint_text         = "fdisk -l funktioniert auch für GPT-Laufwerke zur Anzeige",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist der gdisk-Typcode für eine EFI System Partition?',
                options     = ['A) 8300', 'B) 8200', 'C) ef00', 'D) fd00'],
                correct     = 'C',
                explanation = 'ef00 = EFI System, 8300 = Linux filesystem, 8200 = Linux swap.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welches Tool ist nativ für GPT-Partitionierung optimiert?',
                options     = ['A) fdisk', 'B) cfdisk', 'C) parted', 'D) gdisk'],
                correct     = 'D',
                explanation = 'gdisk = GPT disk, nativ für GUID Partition Table. fdisk kann GPT lesen, aber gdisk versteht es vollständig.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "fdisk = traditionell (MBR-fokussiert, kann auch GPT).\n"
            "gdisk = GPT-nativ, für UEFI-Systeme empfohlen.\n"
            "parted = kann MBR + GPT, gut für Skripting.\n"
            "Alle drei können im Examen vorkommen."
        ),
        memory_tip        = "g in gdisk = GPT. GPT-Codes 4-stellig: ef00=EFI, 8300=Linux, 8200=Swap.",
        gear_reward       = None,
        faction_reward    = ("Kernel Syndicate", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.04 — parted — Der Universalchirurg
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.04",
        chapter      = 4,
        title        = "parted — Partitionieren wie ein Ghost",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0 schickt eine verschlüsselte Nachricht:\n"
            "'Für Skripte und Automatisierung: parted.\n"
            " Es versteht MBR und GPT, und macht keine Rückfragen.'"
        ),
        why_important = (
            "parted ist das universelle Tool — MBR + GPT, interaktiv + Skript.\n"
            "ACHTUNG: parted schreibt SOFORT. Kein 'w'!"
        ),
        explanation  = (
            "parted — GNU Partitions-Editor (MBR + GPT):\n\n"
            "Interaktiv:\n"
            "  parted /dev/sda          # interaktiver Modus\n\n"
            "Nicht-interaktiv (für Skripte):\n"
            "  parted /dev/sda print    # anzeigen\n"
            "  parted -l                # alle Laufwerke\n\n"
            "Interaktive Befehle:\n"
            "  print              — Partitionstabelle anzeigen\n"
            "  mklabel gpt        — GPT erstellen\n"
            "  mklabel msdos      — MBR erstellen ('msdos' = MBR!)\n"
            "  mkpart primary ext4 1MiB 10GiB  — Partition erstellen\n"
            "  rm 1               — Partition 1 löschen\n"
            "  resizepart 3 50GiB — Partition 3 vergrößern\n"
            "  quit               — Beenden\n\n"
            "!!! KRITISCH: parted schreibt SOFORT !!!\n"
            "  Kein 'w' wie bei fdisk — direkt live.\n"
            "  'msdos' = MBR in parted-Sprache (nicht 'mbr'!)\n\n"
            "Einheiten: MiB, GiB, MB, GB, % oder Sektoren"
        ),
        syntax       = "parted -l\nparted /dev/sda print\nparted /dev/sda mklabel gpt",
        example      = (
            "$ parted /dev/sda print\n"
            "Model: ATA SAMSUNG (scsi)\n"
            "Disk /dev/sda: 512GB\n"
            "Partition Table: gpt\n"
            "Number  Start   End    Size   Type  Name\n"
            " 1      1049kB  512MB  511MB  primary"
        ),
        task_description  = "Zeige alle Partitionen mit fdisk",
        expected_commands = ["fdisk -l"],
        hint_text         = "fdisk -l oder parted -l zur Anzeige",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was bedeutet 'mklabel msdos' in parted?",
                options     = ['A) Erstellt MS-DOS-Partition', 'B) Erstellt MBR-Partitionstabelle', 'C) Erstellt ext2-Dateisystem', 'D) Fehler: ungültiger Befehl'],
                correct     = 'B',
                explanation = "In parted heißt MBR 'msdos'. 'mklabel gpt' für GPT, 'mklabel msdos' für MBR.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Wann schreibt parted Änderungen auf die Festplatte?',
                options     = ["A) Erst nach 'w'", "B) Erst nach 'commit'", 'C) Sofort bei jedem Befehl', "D) Erst nach 'quit'"],
                correct     = 'C',
                explanation = "parted schreibt SOFORT! Kein 'w' wie bei fdisk. Das ist die kritische Falle.",
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "parted-Falle: Änderungen werden SOFORT geschrieben!\n"
            "'mklabel msdos' = MBR erstellen (nicht 'mbr'!)\n"
            "'mklabel gpt' = GPT erstellen.\n"
            "parted versteht prozentuale Einheiten: mkpart ... 0% 50%"
        ),
        memory_tip        = "parted = sofort = kein Undo! msdos = MBR in parted-Sprache.",
        gear_reward       = None,
        faction_reward    = ("Kernel Syndicate", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.05 — mkfs — Dateisystem erstellen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.05",
        chapter      = 4,
        title        = "mkfs — Das Dateisystem erschaffen",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "Ghost hat eine neue Partition: /dev/nvme0n1p4.\n"
            "Rust grinst: 'Eine Partition ist noch kein Dateisystem.\n"
            " Du musst sie formatieren. Ruf mkfs — den Erschaffer.'"
        ),
        why_important = (
            "Ohne Dateisystem ist eine Partition leerer Speicher.\n"
            "mkfs erstellt die Struktur für Dateien und Verzeichnisse.\n"
            "LPIC-1 prüft mkfs-Syntax und Dateisystemtypen."
        ),
        explanation  = (
            "mkfs — Make Filesystem:\n\n"
            "Syntax:\n"
            "  mkfs -t <typ> <gerät>\n"
            "  mkfs.<typ> <gerät>       # Kurzform (bevorzugt)\n\n"
            "Wichtige Typen:\n"
            "  mkfs.ext4 /dev/sda1      # ext4 (Linux-Standard)\n"
            "  mkfs.ext3 /dev/sda2      # ext3 (älter)\n"
            "  mkfs.ext2 /dev/sda3      # ext2 (kein Journaling)\n"
            "  mkfs.xfs /dev/sda1       # XFS (RHEL-Standard)\n"
            "  mkfs.btrfs /dev/sda1     # Btrfs (modern)\n"
            "  mkfs.vfat /dev/sda1      # FAT32 (USB, EFI)\n"
            "  mkfs.ntfs /dev/sda1      # NTFS (Windows)\n\n"
            "Wichtige Optionen:\n"
            "  mkfs.ext4 -L 'DATA' /dev/sda1    # Label setzen\n"
            "  mkfs.ext4 -m 5 /dev/sda1         # 5% Reserved Blocks\n"
            "  mkfs.ext4 -j /dev/sda1           # mit Journal\n\n"
            "Nach mkfs überprüfen:\n"
            "  blkid /dev/sda1    # UUID und Typ prüfen\n"
            "  lsblk -f           # Dateisystem-Info anzeigen"
        ),
        syntax       = "mkfs.ext4 /dev/sda1\nmkfs -t ext4 /dev/sda1   # äquivalent",
        example      = (
            "$ mkfs.ext4 -L 'DATA' /dev/sda1\n"
            "mke2fs 1.47.0 (5-Feb-2023)\n"
            "Creating filesystem with 2621440 4k blocks\n"
            "Allocating group tables: done\n"
            "Writing superblocks: done"
        ),
        task_description  = "Zeige Partitionen und ihre Dateisysteme",
        expected_commands = ["lsblk", "blkid"],
        hint_text         = "lsblk -f zeigt Dateisystem-Typ und Mount-Punkt",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welcher Befehl erstellt ein ext4-Dateisystem auf /dev/sda1?',
                options     = ['A) mkfs /dev/sda1', 'B) format -t ext4 /dev/sda1', 'C) mkfs.ext4 /dev/sda1', 'D) newfs ext4 /dev/sda1'],
                correct     = 'C',
                explanation = 'mkfs.ext4 /dev/sda1 oder mkfs -t ext4 /dev/sda1 sind gleichwertig.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was bedeutet 'mkfs ohne Typ-Suffix' (nur mkfs /dev/sda1)?",
                options     = ['A) Erstellt ext4', 'B) Erstellt ext2 (kein Journaling)', 'C) Fehler', 'D) Erstellt XFS'],
                correct     = 'B',
                explanation = 'mkfs ohne Suffix = mkfs.ext2 — veraltet und ohne Journaling!',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "'Wie erstellt man ein ext4-Dateisystem?'\n"
            "→ mkfs.ext4 /dev/sdXY  ODER  mkfs -t ext4 /dev/sdXY\n"
            "Beide sind gleichwertig.\n"
            "mkfs ohne Suffix = mkfs.ext2 (veraltet, kein Journaling!)"
        ),
        memory_tip        = "mkfs.ext4 = make filesystem ext4. Label: -L. Reserved: -m.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.06 — ext2/3/4 — Die Linux-Triade
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.06",
        chapter      = 4,
        title        = "ext2 / ext3 / ext4 — Die Linux-Triade",
        mtype        = "DECODE",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Im Archiv des Kernels liegen drei alte Datensteine:\n"
            "ext2, ext3, ext4 — die Triade.\n"
            "Jeder Ghost muss ihre Unterschiede kennen."
        ),
        why_important = (
            "ext4 ist der Linux-Standard. LPIC-1 fragt nach Unterschieden\n"
            "zwischen ext2/3/4 und nach den zugehörigen Tools."
        ),
        explanation  = (
            "Die ext-Familie:\n\n"
            "ext2:\n"
            "  - Kein Journaling → schnell aber unsicher bei Absturz\n"
            "  - Gut für /boot oder USB-Sticks\n"
            "  - Max. Dateigröße: 2 TB\n\n"
            "ext3:\n"
            "  - ext2 + Journaling → sicher bei Absturz\n"
            "  - Rückwärtskompatibel mit ext2\n\n"
            "ext4:\n"
            "  - Linux-Standard seit 2008\n"
            "  - Journaling + Extents (große Dateien effizienter)\n"
            "  - Delayed allocation für bessere Performance\n"
            "  - Max. Dateigröße: 16 TB, Volumen: 1 EB\n\n"
            "Tools für ext-Dateisysteme:\n"
            "  tune2fs -l /dev/sda1        # Metadaten anzeigen\n"
            "  tune2fs -L 'NAME' /dev/sda1 # Label ändern\n"
            "  tune2fs -c 20 /dev/sda1     # nach 20 Mounts prüfen\n"
            "  dumpe2fs /dev/sda1           # detaillierte Infos\n"
            "  e2fsck /dev/sda1             # Dateisystem prüfen\n"
            "  resize2fs /dev/sda1 20G      # Größe ändern"
        ),
        syntax       = "tune2fs -l /dev/sda1\ntune2fs -L 'LABEL' /dev/sda1",
        example      = "$ tune2fs -l /dev/sda1\nFilesystem magic number: 0xEF53\nFilesystem revision: 1\nFilesystem features: extents flex_bg sparse_super",
        task_description  = "Zeige Partitionen und ihre Dateisysteme",
        expected_commands = ["lsblk", "blkid"],
        hint_text         = "blkid zeigt den Dateisystem-Typ (TYPE=)",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welches ext-Dateisystem hat KEIN Journaling?",
                options     = ["A) ext4", "B) ext3", "C) ext2", "D) exfat"],
                correct     = "C",
                explanation = "ext2 hat kein Journaling. ext3 fügte Journaling hinzu, ext4 erweiterte es.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was macht tune2fs -L 'DATA' /dev/sda1?",
                options     = [
                    "A) Erstellt ein ext-Dateisystem mit Label",
                    "B) Ändert das Label eines vorhandenen ext-Dateisystems",
                    "C) Listet alle Dateisysteme mit Labels auf",
                    "D) Löscht das Label",
                ],
                correct     = "B",
                explanation = "tune2fs ändert Parameter eines vorhandenen ext-Dateisystems. -L setzt das Label.",
                xp_value    = 20,
            ),
        ],
        exam_tip         = (
            "ext2=kein Journal, ext3=Journal, ext4=Journal+Extents.\n"
            "'Welches Tool prüft ext-Dateisysteme?' → e2fsck\n"
            "'Wie Label ändern?' → tune2fs -L 'NAME' /dev/sdXY"
        ),
        memory_tip       = "2=ohne, 3=mit Journal, 4=mit Journal+Extents. tune2fs = tune ext2fs.",
        gear_reward      = None,
        faction_reward   = ("Root Collective", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.07 — XFS — Hochleistungs-Dateisystem
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.07",
        chapter      = 4,
        title        = "XFS — Hochleistungs-Filesystem der Konzerne",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "ZARA Z3R0",
        story        = (
            "Die MegaCorps nutzen XFS für ihre großen Server.\n"
            "Zara Z3R0: 'RHEL, Rocky, AlmaLinux — alle Standard XFS.\n"
            " Kenn es, Ghost. Die Konzerne wissen warum.'"
        ),
        why_important = (
            "XFS ist Standard in RHEL-basierten Systemen.\n"
            "LPIC-1 fragt nach XFS-Tools und der kritischen Einschränkung:\n"
            "xfs_growfs braucht Mountpoint, nicht Device!"
        ),
        explanation  = (
            "XFS — High-Performance 64-bit Journaling Filesystem:\n\n"
            "Eigenschaften:\n"
            "  - Standard in RHEL/CentOS/Rocky Linux\n"
            "  - Exzellent bei großen Dateien + parallelen Zugriffen\n"
            "  - Journaling (Metadata-Journal)\n"
            "  - Max: 8 EB Dateien und Volumen\n\n"
            "Erstellen:\n"
            "  mkfs.xfs /dev/sda1\n"
            "  mkfs.xfs -L 'DATA' /dev/sda1\n\n"
            "XFS-Tools:\n"
            "  xfs_info /mountpoint    # Infos (gemountet!)\n"
            "  xfs_repair /dev/sda1    # reparieren (unmounted)\n"
            "  xfs_admin -L 'X' /dev/sda1  # Label ändern\n"
            "  xfs_dump / xfs_restore  # Backup/Restore\n\n"
            "!!! KRITISCH: XFS vergrößern:\n"
            "  xfs_growfs /mountpoint  # MOUNTPOINT, nicht Device!\n"
            "  XFS kann NUR vergrößert, NICHT verkleinert werden!"
        ),
        syntax       = "mkfs.xfs /dev/sda1\nxfs_growfs /data    # Mountpoint!",
        example      = "$ xfs_info /\nmeta-data=/dev/nvme0n1p3 isize=512 agcount=4 agsize=31126528 blks",
        task_description  = "Zeige Partitionen und Dateisysteme",
        expected_commands = ["lsblk", "blkid"],
        hint_text         = "blkid oder lsblk -f zeigt den Dateisystem-Typ",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Welcher Befehl vergrößert ein XFS-Dateisystem?',
                options     = ['A) xfs_growfs /dev/sda2', 'B) xfs_growfs /mountpoint', 'C) resize2fs /dev/sda2', 'D) xfs_resize /data'],
                correct     = 'B',
                explanation = 'xfs_growfs braucht den MOUNTPOINT, nicht das Device! Das ist die XFS-Falle im Examen.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'XFS kann...',
                options     = ['A) vergrößert und verkleinert werden', 'B) nur vergrößert, nicht verkleinert werden', 'C) nur verkleinert werden', 'D) nicht geändert werden ohne Neuformat'],
                correct     = 'B',
                explanation = 'XFS kann NUR vergrößert werden. Verkleinern ist nicht möglich — Datenverlust!',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "XFS-Falle: xfs_growfs braucht den MOUNTPOINT!\n"
            "Richtig:  xfs_growfs /data\n"
            "Falsch:   xfs_growfs /dev/sda2\n"
            "XFS kann NICHT verkleinert werden — merken!"
        ),
        memory_tip        = "XFS growfs = Mountpoint. Nur vergrößern, nie verkleinern.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.08 — Swap einrichten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.08",
        chapter      = 4,
        title        = "Swap — Virtueller RAM",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "Das System läuft heiß. Der RAM ist voll.\n"
            "Rust: 'Swap rettet Leben, Ghost. Nicht ideal, aber besser als OOM Killer.\n"
            " Lern wie man Swap einrichtet.'"
        ),
        why_important = (
            "Swap ist Auslagerungsspeicher wenn RAM voll.\n"
            "LPIC-1 prüft mkswap, swapon, swapoff und fstab-Einträge."
        ),
        explanation  = (
            "SWAP einrichten:\n\n"
            "Swap-Partition:\n"
            "  1. Partition erstellen (fdisk, Typ 82)\n"
            "  2. mkswap /dev/sda2      # Als Swap formatieren\n"
            "  3. swapon /dev/sda2      # Aktivieren\n"
            "  4. swapoff /dev/sda2     # Deaktivieren\n\n"
            "Swap-Datei (ohne extra Partition):\n"
            "  dd if=/dev/zero of=/swapfile bs=1M count=2048\n"
            "  chmod 600 /swapfile       # Sicherheit!\n"
            "  mkswap /swapfile\n"
            "  swapon /swapfile\n\n"
            "Status prüfen:\n"
            "  swapon --show          # aktive Swap-Bereiche\n"
            "  free -h                # RAM + Swap Übersicht\n"
            "  cat /proc/swaps        # Kernel-Sicht\n\n"
            "Permanent in /etc/fstab:\n"
            "  UUID=xxxx  none  swap  sw  0  0\n"
            "  /swapfile  none  swap  sw  0  0\n\n"
            "Swappiness:\n"
            "  cat /proc/sys/vm/swappiness  # Default: 60\n"
            "  sysctl vm.swappiness=10      # weniger auslagern"
        ),
        syntax       = "mkswap /dev/sda2\nswapon /dev/sda2\nswapoff /dev/sda2",
        example      = "$ swapon --show\nNAME      TYPE SIZE USED PRIO\n/dev/sda2 partition 2G 0B -2",
        task_description  = "Zeige Partitionen (Swap erkennbar am Typ)",
        expected_commands = ["fdisk -l", "swapon --show", "free"],
        hint_text         = "swapon --show oder free -h zeigt Swap-Nutzung",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Was ist die korrekte Reihenfolge zum Einrichten von Swap?',
                options     = ['A) swapon → mkswap → fstab', 'B) mkswap → fstab → swapon', 'C) mkswap → swapon → fstab', 'D) fstab → mkswap → swapon'],
                correct     = 'C',
                explanation = 'Erst mkswap (formatieren), dann swapon (aktivieren), dann fstab (permanent).',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welcher fstab-Eintrag aktiviert eine Swap-Partition permanent?',
                options     = ['A) /dev/sda2  /swap  swap  defaults  0  0', 'B) /dev/sda2  none  swap  sw  0  0', 'C) /dev/sda2  swap  ext4  defaults  0  0', 'D) /dev/sda2  none  none  swap  0  0'],
                correct     = 'B',
                explanation = "Swap-fstab: Gerät, 'none' als Mountpunkt, 'swap' als Typ, 'sw' als Option.",
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "mkswap = formatiert Partition als Swap.\n"
            "swapon = aktiviert Swap.\n"
            "swapoff = deaktiviert Swap.\n"
            "fstab: none als Mountpunkt, swap als Typ, sw als Option."
        ),
        memory_tip        = "mkswap→swapon→fstab. Swap-Datei: dd+chmod 600+mkswap+swapon.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.09 — /etc/fstab
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.09",
        chapter      = 4,
        title        = "/etc/fstab — Das Hauptbuch des Dateisystems",
        mtype        = "DECODE",
        xp           = 95,
        speaker      = "ZARA Z3R0",
        story        = (
            "Jedes System braucht ein Gedächtnis.\n"
            "Ohne /etc/fstab werden Partitionen beim Neustart vergessen.\n"
            "Zara Z3R0: 'fstab ist der Vertrag zwischen System und Speicher.'"
        ),
        why_important = (
            "/etc/fstab definiert welche Partitionen wann und wie gemountet werden.\n"
            "LPIC-1 prüft fstab intensiv: Format, Felder, Optionen."
        ),
        explanation  = (
            "/etc/fstab — 6 Felder pro Zeile:\n\n"
            "  <gerät>  <mountpunkt>  <typ>  <optionen>  <dump>  <pass>\n\n"
            "Beispiele:\n"
            "  UUID=a1b2..  /      ext4  defaults         0  1\n"
            "  UUID=b2c3..  /boot  ext4  defaults         0  2\n"
            "  UUID=c3d4..  /home  ext4  defaults,noatime 0  2\n"
            "  UUID=d4e5..  none   swap  sw               0  0\n"
            "  tmpfs        /tmp   tmpfs defaults,noexec  0  0\n\n"
            "Felder:\n"
            "  Gerät:      UUID=..., LABEL=..., /dev/sdXY\n"
            "  Mountpunkt: /,  /home, /boot, none (für swap)\n"
            "  Typ:        ext4, xfs, swap, tmpfs, iso9660\n"
            "  Optionen:   defaults, ro, rw, noexec, nosuid, noatime\n"
            "  dump:       0=kein Backup, 1=Backup\n"
            "  pass:       0=kein fsck, 1=root zuerst, 2=danach\n\n"
            "Wichtige Optionen:\n"
            "  defaults = rw,suid,dev,exec,auto,nouser,async\n"
            "  noatime  = access time nicht aktualisieren (schneller)\n"
            "  noexec   = keine Programme ausführen\n"
            "  nosuid   = SUID-Bit ignorieren\n\n"
            "fstab testen:\n"
            "  mount -a    # alle fstab-Einträge mounten\n"
            "  findmnt     # gemountete Dateisysteme anzeigen\n\n"
            "autofs — automatisches Mounten bei Bedarf:\n"
            "  Paket: autofs | Dienst: systemctl enable --now autofs\n"
            "  /etc/auto.master     → Master-Map (definiert Mount-Punkte)\n"
            "  /etc/auto.misc       → Detail-Map (was wird wohin gemountet)\n"
            "  Unterschied zu fstab: Mounts nur bei Zugriff, automatisches Unmount\n"
            "  Typisch für: NFS-Shares, CD-ROMs, USB bei Bedarf"
        ),
        syntax       = "# /etc/fstab\nUUID=xxx  /home  ext4  defaults,noatime  0  2",
        example      = "$ mount -a    # testet alle fstab-Einträge\n$ findmnt     # Baumansicht der Mounts",
        task_description  = "Prüfe gemountete Dateisysteme",
        expected_commands = ["cat /etc/fstab", "findmnt", "mount"],
        hint_text         = "cat /etc/fstab zeigt den Inhalt",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was bedeutet 'pass=2' in /etc/fstab?",
                options     = [
                    "A) Partition wird zweimal gemountet",
                    "B) fsck prüft diese Partition nach der Root-Partition",
                    "C) Partition hat zweifache Redundanz",
                    "D) Zweite Mounting-Priority",
                ],
                correct     = "B",
                explanation = "pass=2: fsck prüft nach Root (pass=1). pass=0: keine Prüfung.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Welche fstab-Zeile mountet eine swap-Partition permanent?",
                options     = [
                    "A) /dev/sda2  /swap  swap  defaults  0  0",
                    "B) /dev/sda2  none   swap  sw        0  0",
                    "C) /dev/sda2  swap   none  defaults  0  1",
                    "D) UUID=xxx   /swap  swap  defaults  0  0",
                ],
                correct     = "B",
                explanation = "Swap: Gerät, none (kein Mountpunkt), swap (Typ), sw (Option), 0, 0.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "fstab pass-Feld: 0=kein fsck, 1=root zuerst, 2=danach.\n"
            "UUID statt /dev/sda: stabiler bei Geräteänderungen.\n"
            "mount -a = alle fstab-Einträge testen.\n"
            "defaults = rw,suid,dev,exec,auto,nouser,async\n"
            "autofs = automatisches Mounten bei Bedarf (/etc/auto.master)"
        ),
        memory_tip       = "6 Felder: Gerät MP Typ Optionen Dump Pass. Pass: 0=nie, 1=root, 2=rest.",
        gear_reward      = None,
        faction_reward   = ("Root Collective", 5),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.10 — mount / umount
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.10",
        chapter      = 4,
        title        = "mount & umount — Portale öffnen und schließen",
        mtype        = "INFILTRATE",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "Ghost findet ein verschlüsseltes Laufwerk im Datenmarkt.\n"
            "Um die Daten zu lesen, muss er es mounten.\n"
            "'mount = Portal öffnen. umount = Portal schließen,' sagt Rust."
        ),
        why_important = (
            "mount und umount sind Grundbefehle jedes Linux-Admins.\n"
            "LPIC-1 prüft mount-Optionen und Fehlerbehandlung."
        ),
        explanation  = (
            "mount — Dateisystem einhängen:\n\n"
            "  mount /dev/sda1 /mnt              # einhängen\n"
            "  mount -t ext4 /dev/sda1 /mnt      # Typ angeben\n"
            "  mount -o ro /dev/sda1 /mnt        # read-only\n"
            "  mount -o remount,rw /             # neu mounten rw\n"
            "  mount -a                          # alle aus fstab\n\n"
            "Aktuell gemountete Systeme:\n"
            "  mount                 # alle anzeigen\n"
            "  findmnt               # Baumdarstellung\n"
            "  cat /proc/mounts      # Kernel-Sicht\n\n"
            "umount — Dateisystem aushängen:\n"
            "  umount /mnt           # über Mountpunkt\n"
            "  umount /dev/sda1      # über Gerät\n"
            "  umount -l /mnt        # lazy unmount\n\n"
            "Fehler 'device is busy':\n"
            "  lsof /mnt             # wer nutzt das Verzeichnis?\n"
            "  fuser -m /mnt         # Prozesse anzeigen"
        ),
        syntax       = "mount /dev/sda1 /mnt\numount /mnt",
        example      = "$ mount | grep ext4\n/dev/nvme0n1p3 on / type ext4 (rw,relatime)",
        task_description  = "Zeige alle aktuell gemounteten Dateisysteme",
        expected_commands = ["mount", "findmnt", "cat /proc/mounts"],
        hint_text         = "mount ohne Argumente zeigt alle gemounteten Dateisysteme",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was tust du, wenn umount 'device is busy' meldet?",
                options     = ['A) Reboot', 'B) umount -f', 'C) lsof /mountpoint', 'D) mount -r'],
                correct     = 'C',
                explanation = 'lsof /mountpoint oder fuser -m /mountpoint zeigt, welche Prozesse das FS belegen.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Welcher Befehl mountet alle Dateisysteme aus /etc/fstab?',
                options     = ['A) mount /all', 'B) mount --fstab', 'C) mount -a', 'D) fstab-mount'],
                correct     = 'C',
                explanation = 'mount -a = alle aus fstab mounten. Gut zum Testen nach fstab-Änderungen.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "mount -a = alle fstab-Einträge mounten (testen!)\n"
            "mount -o remount,rw / = Root live auf rw umschalten\n"
            "umount schlägt fehl bei busy → lsof /mountpunkt\n"
            "findmnt = modernes mount | grep"
        ),
        memory_tip        = "mount = einhängen. umount = aushängen. Busy? → lsof /mp",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.11 — df / du
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.11",
        chapter      = 4,
        title        = "df & du — Speicherspäher",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "Alarm: 'Disk full!' erscheint auf Ghosts Bildschirm.\n"
            "Rust: 'Kein Panik. df zeigt dir WO es voll ist.\n"
            " du zeigt dir WER es verursacht.'"
        ),
        why_important = (
            "df und du sind unverzichtbar für Speicherverwaltung.\n"
            "LPIC-1 prüft Optionen und den Unterschied zwischen beiden."
        ),
        explanation  = (
            "df — Disk Free — Partition-Übersicht:\n\n"
            "  df           # alle Dateisysteme\n"
            "  df -h        # human-readable (GiB, MiB)\n"
            "  df -H        # SI-Einheiten (GB, MB = 1000er)\n"
            "  df -T        # mit Dateisystem-Typ\n"
            "  df -i        # Inodes statt Blöcke\n"
            "  df /home     # nur /home\n\n"
            "du — Disk Usage — Verzeichnis-Größen:\n\n"
            "  du /var           # Größe von /var (rekursiv)\n"
            "  du -h /var        # human-readable\n"
            "  du -s /var        # nur Gesamtgröße (summary)\n"
            "  du -sh /var/*     # Unterverzeichnisse\n"
            "  du -sh /* 2>/dev/null | sort -rh | head -10\n\n"
            "Tipp — 'Disk full' debuggen:\n"
            "  1. df -h          # welche Partition voll?\n"
            "  2. du -sh /var/* | sort -rh | head  # größte Verzeichnisse\n"
            "  3. df -i          # Inodes voll? (oft vergessen!)\n"
            "  4. lsof | grep deleted  # gelöschte offene Dateien"
        ),
        syntax       = "df -h\ndu -sh /var/*",
        example      = (
            "$ df -h\nFilesystem      Size  Used Avail Use% Mounted on\n"
            "/dev/nvme0n1p3  466G   45G  397G  11% /"
        ),
        task_description  = "Zeige freien Speicherplatz aller Partitionen",
        expected_commands = ["df", "df -h"],
        hint_text         = "df -h zeigt Speicherplatz in lesbarem Format",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was zeigt 'df -i'?",
                options     = [
                    "A) Inode-Nutzung statt Block-Nutzung",
                    "B) Interaktiven Modus",
                    "C) Dateisystem-Typ",
                    "D) Input/Output-Statistiken",
                ],
                correct     = "A",
                explanation = "df -i zeigt Inode-Nutzung. Wichtig wenn 'disk full' aber noch Block-Platz da ist.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "df = Partition-Übersicht. du = Verzeichnis-Größe.\n"
            "df -i: Wenn 'disk full' aber df -h zeigt Platz → Inodes voll!\n"
            "du -sh /* | sort -rh | head = Top-Speicherfresser."
        ),
        memory_tip       = "df = Disk Free (Partitions-Übersicht). du = Disk Usage (Verzeichnisse).",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.12 — fsck / e2fsck
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.12",
        chapter      = 4,
        title        = "fsck — Der Dateisystem-Arzt",
        mtype        = "REPAIR",
        xp           = 85,
        speaker      = "ZARA Z3R0",
        story        = (
            "Nach einem Stromausfall startet das System nicht mehr.\n"
            "Kernel-Meldung: 'EXT4-fs error: journal checksum invalid'\n"
            "Zara Z3R0: 'fsck rettet Dateisysteme. Lern es JETZT.'"
        ),
        why_important = (
            "fsck ist der Reparatur-Befehl für beschädigte Dateisysteme.\n"
            "LPIC-1: fsck nur auf unmounted Partitionen — kritische Regel!"
        ),
        explanation  = (
            "fsck — Filesystem Check:\n\n"
            "!!! NUR auf UNMOUNTED Partitionen ausführen !!!\n\n"
            "  fsck /dev/sda1           # automatisch richtiges Tool\n"
            "  fsck -t ext4 /dev/sda1   # Typ explizit\n"
            "  e2fsck /dev/sda1         # direkt ext2/3/4\n\n"
            "Wichtige Optionen:\n"
            "  fsck -n /dev/sda1   # nur prüfen, NICHT reparieren\n"
            "  fsck -y /dev/sda1   # alle Fragen mit 'ja'\n"
            "  fsck -f /dev/sda1   # force check\n\n"
            "Root-Partition reparieren:\n"
            "  1. Rescue Mode booten\n"
            "  2. umount /dev/sda1\n"
            "  3. fsck -y /dev/sda1\n"
            "  4. Reboot\n\n"
            "Auto-fsck konfigurieren:\n"
            "  tune2fs -c 20 /dev/sda1  # nach 20 Mounts\n"
            "  tune2fs -i 6m /dev/sda1  # alle 6 Monate\n\n"
            "Für andere Typen:\n"
            "  xfs_repair /dev/sda1   # XFS\n"
            "  dosfsck /dev/sda1      # FAT32"
        ),
        syntax       = "fsck -y /dev/sda1\ne2fsck /dev/sda1",
        example      = "$ fsck -n /dev/sda1\nfsck from util-linux 2.38.1\ne2fsck 1.47.0: clean, 12345 files, 98765/4096000 blocks",
        task_description  = "Zeige Partitions-Informationen",
        expected_commands = ["lsblk", "blkid"],
        hint_text         = "lsblk zeigt Partitionen und Mountpoints",
        quiz_questions    = [
            QuizQuestion(
                question    = 'Wann darf fsck auf einer Partition laufen?',
                options     = ['A) Immer, auch während des Betriebs', 'B) Nur auf unmounted Partitionen', 'C) Nur bei Reboot', 'D) Nur auf Read-Only-Partitionen'],
                correct     = 'B',
                explanation = 'fsck NIEMALS auf gemounteten Partitionen! Nur unmounted oder Read-Only.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Was macht fsck -n?',
                options     = ['A) Kein Backup erstellen', 'B) Nur prüfen ohne Reparieren (Dry Run)', 'C) Nicht interaktiv', 'D) Nein zu allen Fragen'],
                correct     = 'B',
                explanation = 'fsck -n = nur prüfen, nichts reparieren. Sicher für erste Diagnose.',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "fsck NUR auf unmounted Partitionen!\n"
            "fsck -y = alle Fehler automatisch korrigieren.\n"
            "fsck -n = nur prüfen (safe für laufende Systeme).\n"
            "pass in fstab: 0=nie, 1=root, 2=andere."
        ),
        memory_tip       = "fsck = Filesystem Check. Nur unmounted! -y=yes all, -n=dry run.",
        gear_reward      = None,
        faction_reward   = ("Root Collective", 4),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.13 — lsblk / blkid
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.13",
        chapter      = 4,
        title        = "lsblk & blkid — Den Speicher röntgen",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "ZARA Z3R0",
        story        = (
            "Ghost braucht eine schnelle Übersicht über alle Laufwerke.\n"
            "Kein fdisk, kein Scrollen — schnell und direkt.\n"
            "Zara Z3R0: 'lsblk. Dein bestes Werkzeug für Block-Geräte.'"
        ),
        why_important = (
            "lsblk und blkid sind moderne Werkzeuge für Geräteübersicht.\n"
            "LPIC-1: UUID aus blkid → in /etc/fstab verwenden."
        ),
        explanation  = (
            "lsblk — List Block Devices:\n\n"
            "  lsblk              # Baumansicht\n"
            "  lsblk -f           # mit Dateisystem-Info\n"
            "  lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,UUID\n"
            "  lsblk /dev/nvme0n1 # nur ein Gerät\n\n"
            "Typen: disk / part / lvm / raid / rom\n\n"
            "blkid — Block Device Identifier:\n\n"
            "  blkid                     # alle Geräte\n"
            "  blkid /dev/sda1           # ein Gerät\n"
            "  blkid -s UUID -o value /dev/sda1  # nur UUID\n\n"
            "Ausgabe:\n"
            "  UUID='...'    — eindeutiger Bezeichner\n"
            "  TYPE='ext4'   — Dateisystem-Typ\n"
            "  LABEL='boot'  — optionaler Name\n"
            "  PARTUUID='...' — GPT-Partition-UUID\n\n"
            "UUID statt /dev/sdX in fstab:\n"
            "  /dev/sda kann sich ändern (USB angesteckt)\n"
            "  UUID bleibt immer stabil"
        ),
        syntax       = "lsblk -f\nblkid /dev/sda1",
        example      = (
            "$ lsblk -f\nNAME      FSTYPE LABEL UUID                                 MOUNTPOINT\n"
            "nvme0n1\n"
            "├─p1      vfat         A1B2-C3D4                            /boot/efi\n"
            "└─p3      ext4   root  a1b2c3d4-...                         /"
        ),
        task_description  = "Zeige alle Block-Geräte mit Dateisystem-Infos",
        expected_commands = ["lsblk", "lsblk -f"],
        hint_text         = "lsblk -f zeigt Dateisystem-Typ, UUID und Mountpoint",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was zeigt 'lsblk -f'?",
                options     = ['A) Nur Festplattengrößen', 'B) Dateisystem-Typ, UUID und Mountpoint', 'C) Nur Partitionstypen', 'D) Festplatten-Fehler'],
                correct     = 'B',
                explanation = 'lsblk -f = kombiniert Gerätebaum mit FSTYPE, UUID und MOUNTPOINTS.',
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = 'Warum nutzt man UUID statt /dev/sda1 in /etc/fstab?',
                options     = ['A) UUID ist kürzer', 'B) UUID ist stabiler bei Geräteänderungen', 'C) /dev/sda1 funktioniert nicht', 'D) UUID ist schneller'],
                correct     = 'B',
                explanation = '/dev/sdX kann sich ändern (neue USB-Geräte). UUID bleibt immer gleich — stabiler!',
                xp_value    = 20,
            ),
        ],
        exam_tip          = (
            "lsblk = Block-Geräte Baumansicht.\n"
            "blkid = UUID und Dateisystem-Typ.\n"
            "UUID in /etc/fstab = stabiler als /dev/sdX.\n"
            "lsblk -f = kombiniert beides."
        ),
        memory_tip       = "lsblk=Baum. blkid=UUID+Typ. UUID in fstab = stabil.",
        gear_reward      = None,
        faction_reward   = ("Net Runners", 3),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.14 — LVM Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.14",
        chapter      = 4,
        title        = "LVM — Logischer Volumemanager",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0 zeigt Ghost das flexibelste Speicher-System:\n"
            "'LVM macht Partitionen dynamisch. Kein Neustart zum Vergrößern.\n"
            " Das ist der Unterschied zwischen einem Ghost und einem Noob.'"
        ),
        why_important = (
            "LVM ist Standard in Enterprise-Linux-Systemen.\n"
            "LPIC-1 prüft PV/VG/LV-Reihenfolge und Vergrößerungs-Workflow."
        ),
        explanation  = (
            "LVM — Schichten:\n"
            "  PV (Physical Volume) → VG (Volume Group) → LV (Logical Volume)\n\n"
            "1. Physical Volume:\n"
            "  pvcreate /dev/sdb1 /dev/sdc1  # PVs erstellen\n"
            "  pvdisplay                      # anzeigen\n"
            "  pvs                            # kurze Übersicht\n\n"
            "2. Volume Group:\n"
            "  vgcreate datavg /dev/sdb1 /dev/sdc1  # VG erstellen\n"
            "  vgdisplay datavg                      # anzeigen\n"
            "  vgextend datavg /dev/sdd1             # PV hinzufügen\n"
            "  vgs                                    # Übersicht\n\n"
            "3. Logical Volume:\n"
            "  lvcreate -L 10G -n datalv datavg      # 10GB\n"
            "  lvcreate -l 100%FREE -n lv0 vg0       # alles frei\n"
            "  lvdisplay                               # anzeigen\n"
            "  lvextend -L +5G /dev/datavg/datalv    # vergrößern\n"
            "  resize2fs /dev/datavg/datalv           # FS anpassen\n\n"
            "Gerätepfade:\n"
            "  /dev/<vgname>/<lvname>\n"
            "  /dev/mapper/<vgname>-<lvname>\n\n"
            "Formatieren + Mounten:\n"
            "  mkfs.ext4 /dev/datavg/datalv\n"
            "  mount /dev/datavg/datalv /data"
        ),
        syntax       = "pvcreate /dev/sdb1\nvgcreate vg0 /dev/sdb1\nlvcreate -L 10G -n lv0 vg0",
        example      = (
            "$ lvs\n  LV   VG     Attr       LSize  Pool Origin\n"
            "  root ubuntu-vg -wi-ao---- 20.00g"
        ),
        task_description  = "Zeige Partitionen (LVM sichtbar als TYPE=lvm)",
        expected_commands = ["lsblk", "fdisk -l"],
        hint_text         = "lsblk zeigt auch LVM-Volumes (TYPE=lvm)",
        quiz_questions    = [
            QuizQuestion(
                question    = "Korrekte LVM-Erstellungsreihenfolge?",
                options     = [
                    "A) lvcreate → vgcreate → pvcreate",
                    "B) pvcreate → vgcreate → lvcreate",
                    "C) vgcreate → pvcreate → lvcreate",
                    "D) mkfs → pvcreate → vgcreate",
                ],
                correct     = "B",
                explanation = "PV erst erstellen, dann VG daraus bauen, dann LV in der VG erstellen.",
                xp_value    = 25,
            ),
        ],
        exam_tip         = (
            "LVM: pvcreate → vgcreate → lvcreate\n"
            "Vergrößern: lvextend → resize2fs (ext4) oder xfs_growfs (xfs)\n"
            "lvcreate -L 10G = 10 Gigabyte\n"
            "lvcreate -l 50%FREE = 50% des freien VG-Platzes"
        ),
        memory_tip       = "PV→VG→LV. Wie Baublöcke stapeln. lvextend+resize2fs zum Wachsen.",
        gear_reward      = None,
        faction_reward   = ("Root Collective", 6),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.16 — LVM Grundkonzept
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.16_lvm_intro",
        chapter      = 4,
        title        = "LVM — Konzept: PV → VG → LV",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "Rust lehnt gegen einen alten Rack-Server im Untergeschoss.\n"
            "'Partitionen sind starre Käfige,' murmelt er.\n"
            "'Aber LVM — Logical Volume Management — das ist Freiheit.\n"
            " Du kannst Speicher vergrößern, verschieben, ohne Reboot.'\n"
            "Ghost zieht einen Stuhl heran. Das klingt mächtig."
        ),
        why_important = (
            "LVM ist Standard in professionellen Linux-Systemen.\n"
            "LPIC-1 prüft das Dreischichten-Modell: PV → VG → LV.\n"
            "Ohne LVM-Verständnis scheitern viele Prüfungen und Produktivsysteme."
        ),
        explanation  = (
            "LVM — Das Dreischichten-Modell:\n\n"
            "  Physische Ebene:  PV  (Physical Volume)\n"
            "  Gruppen-Ebene:    VG  (Volume Group)\n"
            "  Logische Ebene:   LV  (Logical Volume)\n\n"
            "Wie es funktioniert:\n"
            "  1. PV: Festplatten/Partitionen werden zu PVs gemacht\n"
            "         /dev/sdb1, /dev/sdc1 → pvcreate\n\n"
            "  2. VG: Mehrere PVs bilden einen gemeinsamen Pool (VG)\n"
            "         'datavg' hat 20 GB PV + 30 GB PV = 50 GB Pool\n\n"
            "  3. LV: Aus dem VG-Pool werden flexible LVs geschnitten\n"
            "         lvcreate -L 10G → /dev/datavg/datalv\n\n"
            "Warum LVM?\n"
            "  + Online-Vergrößerung ohne Reboot\n"
            "  + Mehrere Festplatten als eine logische Einheit\n"
            "  + Snapshots für Backups (lvsnapshot)\n"
            "  + Striping + Mirroring möglich\n\n"
            "Gerätepfade nach Erstellung:\n"
            "  /dev/<vgname>/<lvname>          # symbolischer Link\n"
            "  /dev/mapper/<vgname>-<lvname>   # dm-device"
        ),
        syntax       = (
            "# Reihenfolge: PV → VG → LV\n"
            "pvcreate /dev/sdb1\n"
            "vgcreate datavg /dev/sdb1\n"
            "lvcreate -L 10G -n datalv datavg"
        ),
        example      = (
            "$ lsblk\n"
            "NAME              MAJ:MIN  SIZE TYPE MOUNTPOINTS\n"
            "sdb                 8:16   50G  disk\n"
            "└─sdb1              8:17   50G  part\n"
            "  └─datavg-datalv 253:0    10G  lvm  /data"
        ),
        task_description  = "Zeige Block-Geräte und erkenne LVM-Volumes",
        expected_commands = ["lsblk"],
        hint_text         = "lsblk zeigt LVM-Volumes mit TYPE=lvm",
        quiz_questions    = [
            QuizQuestion(
                question    = "Was ist die korrekte Reihenfolge beim LVM-Setup?",
                options     = [
                    "pvcreate → vgcreate → lvcreate",
                    "vgcreate → pvcreate → lvcreate",
                    "lvcreate → vgcreate → pvcreate",
                    "mkfs → pvcreate → vgcreate",
                ],
                correct     = 0,
                explanation = "Erst PV erstellen, dann VG aus PVs aufbauen, zuletzt LV im VG anlegen.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welchen Vorteil bietet LVM gegenüber klassischen Partitionen?",
                options     = [
                    "LVM ist schneller als ext4",
                    "LVM-Volumes können online ohne Reboot vergrößert werden",
                    "LVM braucht kein Dateisystem",
                    "LVM-Partitionen sind automatisch verschlüsselt",
                ],
                correct     = 1,
                explanation = "Der Hauptvorteil: LVs können im laufenden Betrieb vergrößert werden (lvextend + resize2fs).",
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "LVM-Schichten merken: PV → VG → LV\n"
            "PV = echte Hardware, VG = Pool, LV = nutzbare Einheit.\n"
            "Gerätepfad: /dev/<vgname>/<lvname>\n"
            "lsblk zeigt TYPE=lvm für Logical Volumes."
        ),
        memory_tip        = "PV→VG→LV: Pflastersteine→Lagerhaus→Zimmer. Zimmer aus Lagerhaus schneiden.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.17 — Physical Volumes
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.17_pv",
        chapter      = 4,
        title        = "Physical Volumes — pvcreate, pvdisplay, pvs",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "RUST",
        story        = (
            "'Schritt eins: deine Festplatten zu PVs machen,' sagt Rust.\n"
            "Er tippt schnell auf einem Terminal im Halbdunkel.\n"
            "'pvcreate schreibt LVM-Metadaten auf die Partition.\n"
            " Danach gehört sie dem LVM-System. Kein Zurück ohne Datenverlust.'\n"
            "Ghost nickt. Macht. Risiko. Das ist NeonGrid-9."
        ),
        why_important = (
            "Physical Volumes sind die Grundlage jedes LVM-Systems.\n"
            "LPIC-1 prüft pvcreate-Syntax und pvdisplay/pvs-Ausgabe.\n"
            "Jeder Sysadmin muss PVs anlegen und inspizieren können."
        ),
        explanation  = (
            "Physical Volumes (PV) — Ebene 1 in LVM:\n\n"
            "PV erstellen:\n"
            "  pvcreate /dev/sdb1              # eine Partition als PV\n"
            "  pvcreate /dev/sdb1 /dev/sdc1    # mehrere auf einmal\n"
            "  pvcreate /dev/sdb               # ganzes Laufwerk (kein Partitionieren nötig)\n\n"
            "PVs anzeigen:\n"
            "  pvdisplay                        # ausführliche Infos\n"
            "  pvdisplay /dev/sdb1              # ein PV\n"
            "  pvs                              # kurze Tabelle\n"
            "  pvs -o+pv_used                  # mit belegtem Platz\n\n"
            "PVs entfernen:\n"
            "  pvremove /dev/sdb1              # PV-Metadaten löschen\n\n"
            "Wichtige Felder in pvdisplay:\n"
            "  PV Name:      /dev/sdb1\n"
            "  VG Name:      datavg\n"
            "  PV Size:      50.00 GiB\n"
            "  Allocatable:  yes\n"
            "  PE Size:      4.00 MiB     ← Physical Extent Größe\n"
            "  Total PE:     12799\n"
            "  Free PE:      2799\n\n"
            "Physical Extents (PE):\n"
            "  LVM teilt PVs in gleich große Blöcke (PE, Standard: 4 MiB)\n"
            "  VG fasst alle PEs aller PVs zusammen\n"
            "  LVs belegen eine Anzahl PEs"
        ),
        syntax       = (
            "pvcreate /dev/sdb1\n"
            "pvdisplay\n"
            "pvs"
        ),
        example      = (
            "$ pvs\n"
            "  PV         VG     Fmt  Attr PSize   PFree\n"
            "  /dev/sdb1  datavg lvm2 a--  <50.00g <40.00g\n"
            "  /dev/sdc1  datavg lvm2 a--  <30.00g <30.00g"
        ),
        task_description  = "Zeige Block-Geräte mit lsblk",
        expected_commands = ["lsblk", "lsblk -f"],
        hint_text         = "lsblk zeigt alle Block-Geräte einschließlich LVM-Partitionen",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welcher Befehl bereitet /dev/sdc1 als LVM Physical Volume vor?",
                options     = [
                    "lvprepare /dev/sdc1",
                    "pvcreate /dev/sdc1",
                    "vgcreate /dev/sdc1",
                    "mkfs.lvm /dev/sdc1",
                ],
                correct     = 1,
                explanation = "pvcreate schreibt LVM-Metadaten auf die Partition und macht sie zum PV.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist ein Physical Extent (PE) in LVM?",
                options     = [
                    "Eine logische Partition innerhalb eines LV",
                    "Der kleinste adressierbare Block in einem LVM-PV (Standard: 4 MiB)",
                    "Ein Backup-Bereich für LVM-Metadaten",
                    "Der maximale Speicherplatz eines PV",
                ],
                correct     = 1,
                explanation = "PEs sind die kleinsten Einheiten in LVM. Standard-PE-Größe: 4 MiB. LVs belegen eine Anzahl PEs.",
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "pvcreate = Physical Volume erstellen.\n"
            "pvdisplay = ausführliche PV-Infos.\n"
            "pvs = kurze PV-Tabelle.\n"
            "PE Size (Standard 4 MiB) wird bei vgcreate festgelegt."
        ),
        memory_tip        = "pv-Befehle: pvcreate, pvdisplay, pvs, pvremove. Alle mit 'pv' prefix.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.18 — Volume Groups
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.18_vg",
        chapter      = 4,
        title        = "Volume Groups — vgcreate, vgdisplay, vgs, vgextend",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "RUST",
        story        = (
            "Rust schiebt Ghost zwei Festplatten rüber.\n"
            "'Siehst du? Zwei PVs — aber das System soll einen großen Pool sehen.\n"
            " Dafür gibt es Volume Groups. vgcreate fasst sie zusammen.\n"
            " Wenn der Pool voll wird? vgextend — einfach mehr reinwerfen.'\n"
            "Ghost lächelt. Das ist skalierbar."
        ),
        why_important = (
            "Volume Groups sind der zentrale Pool in LVM.\n"
            "LPIC-1 prüft vgcreate-Syntax, vgextend und vgs/vgdisplay.\n"
            "VG-Management ist essenziell für Speichererweiterung in Production."
        ),
        explanation  = (
            "Volume Groups (VG) — Ebene 2 in LVM:\n\n"
            "VG erstellen:\n"
            "  vgcreate datavg /dev/sdb1              # VG aus einem PV\n"
            "  vgcreate datavg /dev/sdb1 /dev/sdc1   # VG aus mehreren PVs\n"
            "  vgcreate -s 8M datavg /dev/sdb1       # PE-Größe 8 MiB setzen\n\n"
            "VG anzeigen:\n"
            "  vgdisplay                               # ausführliche Infos\n"
            "  vgdisplay datavg                        # eine VG\n"
            "  vgs                                     # kurze Tabelle\n\n"
            "VG erweitern:\n"
            "  vgextend datavg /dev/sdd1              # neues PV hinzufügen\n\n"
            "VG verkleinern:\n"
            "  vgreduce datavg /dev/sdb1              # PV entfernen\n\n"
            "VG umbenennen / entfernen:\n"
            "  vgrename datavg newvg\n"
            "  vgremove datavg                         # nur wenn keine LVs mehr\n\n"
            "Wichtige Felder in vgdisplay:\n"
            "  VG Name:      datavg\n"
            "  VG Size:      79.99 GiB   ← Summe aller PVs\n"
            "  PE Size:      4.00 MiB\n"
            "  Total PE:     20478\n"
            "  Alloc PE / Size:  2560 / 10.00 GiB\n"
            "  Free  PE / Size: 17918 / 69.99 GiB"
        ),
        syntax       = (
            "vgcreate datavg /dev/sdb1 /dev/sdc1\n"
            "vgdisplay datavg\n"
            "vgs\n"
            "vgextend datavg /dev/sdd1"
        ),
        example      = (
            "$ vgs\n"
            "  VG     #PV #LV #SN Attr   VSize   VFree\n"
            "  datavg   2   1   0 wz--n- <79.99g <69.99g"
        ),
        task_description  = "Zeige Block-Geräte mit lsblk",
        expected_commands = ["lsblk", "lsblk -f"],
        hint_text         = "lsblk zeigt alle Geräte und LVM-Hierarchie",
        quiz_questions    = [
            QuizQuestion(
                question    = "Wie fügt man dem bestehenden Volume Group 'datavg' das neue PV /dev/sdd1 hinzu?",
                options     = [
                    "vgcreate datavg /dev/sdd1",
                    "pvextend datavg /dev/sdd1",
                    "vgextend datavg /dev/sdd1",
                    "lvextend datavg /dev/sdd1",
                ],
                correct     = 2,
                explanation = "vgextend erweitert eine bestehende VG um ein neues PV. vgcreate würde eine neue VG anlegen.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was zeigt 'vgs' an?",
                options     = [
                    "Alle vorhandenen Physical Volumes in Tabellenform",
                    "Alle vorhandenen Volume Groups in kompakter Tabellenform",
                    "Alle gemounteten Logical Volumes",
                    "Alle verfügbaren Block-Geräte",
                ],
                correct     = 1,
                explanation = "vgs zeigt eine kompakte Übersicht aller Volume Groups (wie pvs für PVs, lvs für LVs).",
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "vgcreate <name> <pv1> [<pv2> ...] = VG erstellen.\n"
            "vgextend <name> <pv> = VG um ein PV erweitern.\n"
            "vgreduce <name> <pv> = PV aus VG entfernen.\n"
            "vgs = Kurzübersicht, vgdisplay = Details."
        ),
        memory_tip        = "vg-Befehle: vgcreate, vgdisplay, vgs, vgextend, vgreduce, vgremove.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.19 — Logical Volumes erstellen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.19_lv_create",
        chapter      = 4,
        title        = "Logical Volumes — lvcreate, lvdisplay, lvs",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "RUST",
        story        = (
            "'Jetzt der letzte Schritt,' sagt Rust und tippt ruhig.\n"
            "'Wir schneiden aus dem VG-Pool unser Logical Volume.\n"
            " lvcreate. Name. Größe. VG. Fertig.\n"
            " Das LV ist deine neue Partition — flexibel und erweiterbar.'\n"
            "Ghost sieht /dev/datavg/datalv erscheinen. Sauber."
        ),
        why_important = (
            "Logical Volumes sind das Endprodukt von LVM — was du formatierst und mountest.\n"
            "LPIC-1 prüft lvcreate-Syntax mit -L (Größe) und -n (Name).\n"
            "lvcreate -l (kleine L) für Extents, -L (große L) für Größe."
        ),
        explanation  = (
            "Logical Volumes (LV) — Ebene 3 in LVM:\n\n"
            "LV erstellen:\n"
            "  lvcreate -L 10G -n datalv datavg       # 10 GiB LV\n"
            "  lvcreate -L 500M -n loglv datavg       # 500 MiB LV\n"
            "  lvcreate -l 100%FREE -n biglv datavg   # alles Freie\n"
            "  lvcreate -l 50%FREE -n halflv datavg   # 50% des freien Platzes\n"
            "  lvcreate -l 2560 -n lv0 datavg         # 2560 PEs\n\n"
            "LV anzeigen:\n"
            "  lvdisplay                               # ausführliche Infos\n"
            "  lvdisplay /dev/datavg/datalv            # ein LV\n"
            "  lvs                                     # kurze Tabelle\n\n"
            "LV umbenennen / entfernen:\n"
            "  lvrename datavg datalv newname\n"
            "  lvremove /dev/datavg/datalv             # LV löschen\n\n"
            "Gerätepfade:\n"
            "  /dev/datavg/datalv          # Symlink\n"
            "  /dev/mapper/datavg-datalv   # Device-Mapper-Gerät\n\n"
            "Wichtig: -L vs -l\n"
            "  -L 10G   = 10 Gigabyte (Größe)\n"
            "  -l 2560  = 2560 Physical Extents (Anzahl PEs)\n"
            "  -l 50%FREE = 50% des freien VG-Platzes"
        ),
        syntax       = (
            "lvcreate -L 10G -n datalv datavg\n"
            "lvdisplay\n"
            "lvs"
        ),
        example      = (
            "$ lvs\n"
            "  LV     VG     Attr       LSize  Pool Origin\n"
            "  datalv datavg -wi-a----- 10.00g\n"
            "\n"
            "$ ls -la /dev/datavg/\n"
            "lrwxrwxrwx 1 root root 7 Apr 20 /dev/datavg/datalv -> ../dm-0"
        ),
        task_description  = "Zeige Block-Geräte mit lsblk",
        expected_commands = ["lsblk", "lsblk -f"],
        hint_text         = "lsblk zeigt LVM-Volumes mit TYPE=lvm",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welcher Befehl erstellt ein 20 GiB Logical Volume namens 'datalv' in VG 'datavg'?",
                options     = [
                    "lvcreate -S 20G -n datalv datavg",
                    "lvcreate -L 20G datalv datavg",
                    "lvcreate -L 20G -n datalv datavg",
                    "lvmake -L 20G -n datalv datavg",
                ],
                correct     = 2,
                explanation = "lvcreate -L <Größe> -n <Name> <VG>. -L für Größe, -n für Name, dann die VG.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen lvcreate -L 10G und lvcreate -l 2560?",
                options     = [
                    "Kein Unterschied, beide erstellen 10 GiB",
                    "-L gibt Größe in GB/GiB an; -l gibt Anzahl der Physical Extents an",
                    "-L ist für ext4, -l ist für xfs",
                    "-l erstellt ein Linear-LV, -L ein Logical-LV",
                ],
                correct     = 1,
                explanation = "-L (groß) = Größenangabe (10G, 500M). -l (klein) = PE-Anzahl oder Prozent (100%FREE).",
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "lvcreate -L <Größe> -n <Name> <VG>\n"
            "-L = Größe (10G, 500M), -l = PE-Anzahl oder %FREE.\n"
            "Gerätepfad: /dev/<vg>/<lv> oder /dev/mapper/<vg>-<lv>.\n"
            "lvs = Kurzübersicht, lvdisplay = Details."
        ),
        memory_tip        = "lvcreate -L Größe -n Name VG. -L=Large size, -l=little extents.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.20 — LV formatieren und mounten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.20_lv_manage",
        chapter      = 4,
        title        = "LV formatieren & mounten — mkfs + fstab mit LVM",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "RUST",
        story        = (
            "Das LV existiert. Aber es ist noch leer — kein Dateisystem.\n"
            "Rust: 'Ein LV ist wie eine unformatierte Festplatte.\n"
            " mkfs.ext4 drauf, in /etc/fstab eintragen, mounten.\n"
            " Dann lebt es.'\n"
            "Ghost führt die Befehle aus. /data erscheint. Bereit."
        ),
        why_important = (
            "Nach lvcreate muss das LV formatiert und in fstab eingetragen werden.\n"
            "LPIC-1 prüft den kompletten Workflow: lvcreate → mkfs → fstab → mount.\n"
            "Der fstab-Eintrag mit LVM-Pfad ist prüfungsrelevant."
        ),
        explanation  = (
            "LV formatieren und permanent mounten:\n\n"
            "Schritt 1: Dateisystem erstellen\n"
            "  mkfs.ext4 /dev/datavg/datalv\n"
            "  mkfs.xfs  /dev/datavg/datalv    # Alternative\n\n"
            "Schritt 2: Mountpunkt erstellen\n"
            "  mkdir /data\n\n"
            "Schritt 3: Temporär mounten (testen)\n"
            "  mount /dev/datavg/datalv /data\n\n"
            "Schritt 4: Permanent in /etc/fstab eintragen\n"
            "  # Variante 1: LVM-Pfad\n"
            "  /dev/datavg/datalv  /data  ext4  defaults  0  2\n\n"
            "  # Variante 2: UUID (robuster)\n"
            "  UUID=$(blkid -s UUID -o value /dev/datavg/datalv)\n"
            "  UUID=<uuid>  /data  ext4  defaults  0  2\n\n"
            "Schritt 5: fstab testen\n"
            "  umount /data\n"
            "  mount -a        # alle fstab-Einträge mounten\n"
            "  mount | grep data\n\n"
            "Prüfen:\n"
            "  df -h /data     # Größe und freier Platz\n"
            "  lsblk -f        # Dateisystem und Mountpunkt"
        ),
        syntax       = (
            "mkfs.ext4 /dev/datavg/datalv\n"
            "mkdir /data\n"
            "mount /dev/datavg/datalv /data\n"
            "# /etc/fstab:\n"
            "/dev/datavg/datalv  /data  ext4  defaults  0  2"
        ),
        example      = (
            "$ mkfs.ext4 /dev/datavg/datalv\n"
            "mke2fs 1.47.0: Creating filesystem with 2621440 4k blocks\n"
            "Writing superblocks and filesystem accounting information: done\n"
            "\n"
            "$ mount /dev/datavg/datalv /data && df -h /data\n"
            "Filesystem                  Size  Used Avail Use% Mounted on\n"
            "/dev/mapper/datavg-datalv   9.8G   24M  9.3G   1% /data"
        ),
        task_description  = "Zeige gemountete Dateisysteme",
        expected_commands = ["mount", "findmnt", "df -h"],
        hint_text         = "mount ohne Argumente oder findmnt zeigt alle gemounteten Dateisysteme",
        quiz_questions    = [
            QuizQuestion(
                question    = "Welcher fstab-Eintrag mountet das LVM-Volume /dev/datavg/datalv nach /data mit ext4?",
                options     = [
                    "/dev/datavg/datalv  /data  lvm   defaults  0  2",
                    "/dev/datavg/datalv  /data  ext4  defaults  0  2",
                    "datavg-datalv       /data  ext4  defaults  0  0",
                    "/dev/mapper/datalv  /data  ext4  auto      0  1",
                ],
                correct     = 1,
                explanation = "Korrekt: Gerät /dev/datavg/datalv, Mountpunkt /data, Typ ext4, defaults, dump=0, pass=2.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "In welcher Reihenfolge wird ein LVM-Volume nutzbar gemacht?",
                options     = [
                    "mount → mkfs → lvcreate → fstab",
                    "lvcreate → mount → mkfs → fstab",
                    "lvcreate → mkfs → mkdir → mount → fstab",
                    "pvcreate → mkfs → lvcreate → mount",
                ],
                correct     = 2,
                explanation = "Erst LV erstellen, dann Dateisystem, Mountpunkt anlegen, temporär mounten, dann fstab.",
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "Workflow: lvcreate → mkfs.ext4 /dev/<vg>/<lv> → mkdir → mount → fstab.\n"
            "fstab-Eintrag: /dev/<vg>/<lv>  /mountpunkt  ext4  defaults  0  2\n"
            "mount -a testet alle fstab-Einträge.\n"
            "blkid gibt UUID des LV zurück für stabilen fstab-Eintrag."
        ),
        memory_tip        = "lvcreate→mkfs→mkdir→mount→fstab. Fünf Schritte zum nutzbaren LV.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.21 — LV vergrößern
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.21_lvm_resize",
        chapter      = 4,
        title        = "LV vergrößern — lvextend, resize2fs, xfs_growfs",
        mtype        = "REPAIR",
        xp           = 110,
        speaker      = "RUST",
        story        = (
            "Alarm. /data ist zu 95% voll. Produktionssystem. Jetzt.\n"
            "Rust bleibt ruhig: 'Das ist LVM. Wir vergrößern online.\n"
            " Kein Reboot. Kein Datenverlust. Drei Befehle.'\n"
            "Ghost tippt. lvextend. resize2fs. df -h zeigt mehr Platz.\n"
            "Crisis averted. Das ist der Grund für LVM."
        ),
        why_important = (
            "Online-Vergrößerung ohne Downtime ist der Hauptgrund für LVM.\n"
            "LPIC-1 prüft lvextend-Syntax und den Unterschied:\n"
            "resize2fs (ext4) vs xfs_growfs (XFS) — kritisch für die Prüfung!"
        ),
        explanation  = (
            "LV vergrößern — Online ohne Reboot:\n\n"
            "Schritt 1: LV vergrößern\n"
            "  lvextend -L +5G /dev/datavg/datalv      # +5 GiB hinzufügen\n"
            "  lvextend -L 20G /dev/datavg/datalv      # auf 20 GiB setzen\n"
            "  lvextend -l +100%FREE /dev/datavg/datalv # allen freien VG-Platz nehmen\n\n"
            "Schritt 2a: Dateisystem anpassen (ext4)\n"
            "  resize2fs /dev/datavg/datalv             # ext4 online vergrößern\n"
            "  resize2fs /dev/datavg/datalv 15G         # auf bestimmte Größe\n\n"
            "Schritt 2b: Dateisystem anpassen (XFS)\n"
            "  xfs_growfs /data                         # MOUNTPUNKT! nicht Device!\n\n"
            "Kombination in einem Befehl:\n"
            "  lvextend -L +5G -r /dev/datavg/datalv   # -r = resize FS automatisch\n\n"
            "!!! KRITISCH: XFS vs ext4\n"
            "  ext4: resize2fs /dev/<vg>/<lv>   → Device-Pfad\n"
            "  XFS:  xfs_growfs /mountpunkt     → Mountpunkt!\n\n"
            "LV verkleinern (nur ext4, NICHT XFS):\n"
            "  1. umount /data\n"
            "  2. e2fsck -f /dev/datavg/datalv\n"
            "  3. resize2fs /dev/datavg/datalv 8G\n"
            "  4. lvreduce -L 8G /dev/datavg/datalv\n"
            "  5. mount /data\n"
            "  !!! XFS kann NIE verkleinert werden !!!"
        ),
        syntax       = (
            "lvextend -L +5G /dev/datavg/datalv\n"
            "resize2fs /dev/datavg/datalv       # für ext4\n"
            "xfs_growfs /data                   # für XFS (Mountpunkt!)"
        ),
        example      = (
            "$ lvextend -L +5G /dev/datavg/datalv\n"
            "  Size of logical volume datavg/datalv changed from 10.00 GiB to 15.00 GiB.\n"
            "\n"
            "$ resize2fs /dev/datavg/datalv\n"
            "  Resizing the filesystem on /dev/datavg/datalv to 3932160 (4k) blocks.\n"
            "  The filesystem on /dev/datavg/datalv is now 3932160 (4k) blocks long.\n"
            "\n"
            "$ df -h /data\n"
            "Filesystem                  Size  Used Avail Use% Mounted on\n"
            "/dev/mapper/datavg-datalv    15G  9.5G  4.5G  68% /data"
        ),
        task_description  = "Zeige Partitionen und freien Speicherplatz",
        expected_commands = ["df -h", "lsblk"],
        hint_text         = "df -h zeigt Größe und freien Platz pro Dateisystem",
        quiz_questions    = [
            QuizQuestion(
                question    = "Nach lvextend auf einem XFS-Volume: welcher Befehl passt das Dateisystem an?",
                options     = [
                    "resize2fs /dev/datavg/datalv",
                    "xfs_resize /dev/datavg/datalv",
                    "xfs_growfs /data",
                    "fsck -f /dev/datavg/datalv",
                ],
                correct     = 2,
                explanation = "xfs_growfs braucht den MOUNTPUNKT (z.B. /data), nicht den Device-Pfad. Das ist die XFS-Falle!",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl vergrößert ein LV um 10 GiB UND passt das ext4-Dateisystem automatisch an?",
                options     = [
                    "lvextend -L +10G /dev/datavg/datalv && resize2fs /dev/datavg/datalv",
                    "lvextend -L +10G -r /dev/datavg/datalv",
                    "lvresize -L +10G /dev/datavg/datalv",
                    "lvcreate -L +10G /dev/datavg/datalv",
                ],
                correct     = 1,
                explanation = "lvextend -r (--resizefs) vergrößert das LV und ruft automatisch resize2fs bzw. xfs_growfs auf.",
                xp_value    = 15,
            ),
        ],
        exam_tip          = (
            "LVM vergrößern: lvextend → resize2fs (ext4) ODER xfs_growfs /mountpunkt (XFS).\n"
            "XFS-Falle: xfs_growfs braucht MOUNTPUNKT, nicht Device!\n"
            "lvextend -r = automatisches Resize des Dateisystems.\n"
            "XFS kann NUR vergrößert werden — niemals verkleinern!"
        ),
        memory_tip        = "lvextend+resize2fs=ext4. lvextend+xfs_growfs /mp=XFS. -r macht beides automatisch.",
        gear_reward       = None,
        faction_reward    = ("Root Collective", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.15 — Quiz: Partitionierung & Dateisysteme
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.15",
        chapter      = 4,
        title        = "QUIZ: Partitionierung & Dateisysteme",
        mtype        = "QUIZ",
        xp           = 120,
        speaker      = "ZARA Z3R0",
        story        = (
            "Zara Z3R0 aktiviert das Prüfungsprotokoll.\n"
            "'Zeit zu zeigen, was du gelernt hast, Ghost.\n"
            " Partitionen, Dateisysteme, Tools — alles auf dem Prüfstand.'"
        ),
        why_important = "Prüfungsvorbereitung für LPIC-1 Topic 104.1 + 104.2.",
        explanation   = "Teste dein Wissen über Partitionierung und Dateisysteme.",
        task_description  = "",
        expected_commands = [],
        quiz_questions    = [
            QuizQuestion(
                question    = "Wie viele primäre Partitionen unterstützt MBR maximal?",
                options     = ["A) 2", "B) 4", "C) 8", "D) 128"],
                correct     = "B",
                explanation = "MBR: max 4 primäre Partitionen. GPT: bis zu 128.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welcher Befehl erstellt ein ext4-Dateisystem auf /dev/sda1?",
                options     = [
                    "A) mkfs /dev/sda1",
                    "B) format -t ext4 /dev/sda1",
                    "C) mkfs.ext4 /dev/sda1",
                    "D) newfs ext4 /dev/sda1",
                ],
                correct     = "C",
                explanation = "mkfs.ext4 ist die gängige Kurzform. mkfs -t ext4 ist ebenfalls korrekt.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was ist das PASS-Feld '2' in /etc/fstab?",
                options     = [
                    "A) Partition zweimal mounten",
                    "B) fsck prüft nach Root-Partition",
                    "C) Zweite Backup-Kopie",
                    "D) Partition hat zwei Dateisysteme",
                ],
                correct     = "B",
                explanation = "pass=2: fsck nach Root (pass=1). pass=0: kein fsck.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welches Tool repariert ein XFS-Dateisystem?",
                options     = ["A) fsck.xfs", "B) xfs_check", "C) e2fsck", "D) xfs_repair"],
                correct     = "D",
                explanation = "xfs_repair repariert XFS. e2fsck ist für ext2/3/4.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Was zeigt 'df -i'?",
                options     = [
                    "A) Inode-Nutzung statt Block-Nutzung",
                    "B) Interaktiven Modus",
                    "C) Dateisystem-Typ",
                    "D) IO-Statistiken",
                ],
                correct     = "A",
                explanation = "df -i = Inode-Nutzung. Wichtig wenn Disk voll erscheint aber Blockplatz da ist.",
                xp_value    = 20,
            ),
            QuizQuestion(
                question    = "Welcher Befehl zeigt Block-Geräte in Baumstruktur?",
                options     = ["A) fdisk -l", "B) blkid", "C) lsblk", "D) lsdev"],
                correct     = "C",
                explanation = "lsblk zeigt Block-Geräte als Baum mit Parent-Child-Beziehungen.",
                xp_value    = 20,
            ),
        ],
        exam_tip         = (
            "LPIC-1 Schwerpunkte Topic 104:\n"
            "1. MBR: max 4 primär, max 2TB\n"
            "2. mkfs.ext4 = make filesystem ext4\n"
            "3. fstab: 6 Felder, pass 0/1/2\n"
            "4. fsck: NUR unmounted!\n"
            "5. LVM: pvcreate→vgcreate→lvcreate"
        ),
        memory_tip       = "MBR=446+64+2 bytes. GPT=128 Partitionen. LVM: PV→VG→LV wie Schichten. fstab Pass: 0=nie, 1=root, 2=rest.",
        gear_reward      = None,
        faction_reward   = ("Kernel Syndicate", 8),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 4.BOSS — Der Partition-Wächter
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "4.BOSS",
        chapter      = 4,
        title        = "BOSS: Der Partition-Wächter",
        mtype        = "BOSS",
        xp           = 350,
        speaker      = "SYSTEM",
        story        = (
            "Das Datenmarkt-System ist gesperrt.\n"
            "Ein Wächter-KI hält die Kontrolle:\n"
            "'Beweise dein Wissen über Partitionen und Dateisysteme.'\n"
            "'Oder verliere deine Daten für immer.'"
        ),
        why_important    = "Boss-Prüfung: Kapitel 4 Gesamtwissen",
        explanation      = "Boss-Kampf: Partition-Wächter — vollständige Prüfung",
        task_description = "Überlebe den Boss-Quiz!",
        expected_commands = [],
        ascii_art        = """
  ██████╗  █████╗ ██████╗ ████████╗██╗████████╗██╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║╚══██╔══╝██║██╔═══██╗████╗  ██║
  ██████╔╝███████║██████╔╝   ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
  ██╔═══╝ ██╔══██║██╔══██╗   ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
  ██║     ██║  ██║██║  ██║   ██║   ██║   ██║   ██║╚██████╔╝██║ ╚████║
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

  ┌─ STORAGE SYSTEM STATUS ───────────────────────────────────────────┐
  │  /dev/sda :: LOCKED     MBR: ENCRYPTED                           │
  │  /dev/sdb :: PROTECTED  GPT: INACCESSIBLE                        │
  │  fdisk: PERMISSION DENIED   mkfs: BLOCKED                        │
  └───────────────────────────────────────────────────────────────────┘

                    ⚡ CHAOSWERK FACTION :: CHAPTER 4 BOSS ⚡""",
        story_transitions = [
            "PARTITION-WÄCHTER erwacht. Partition-Tabellen rotieren wie Schlösser.",
            "fdisk zeigt die Struktur. Der Wächter verschlüsselt sie in Echtzeit.",
            "mkfs formatiert. mount versucht es. Zugang verweigert.",
            "Letzte Partition. Zara flüstert: 'Zeig ihm wer hier der Admin ist.'",
        ],
        boss_name        = "PARTITION-WÄCHTER v4.0",
        boss_desc        = (
            "ERROR: UNAUTHORIZED ACCESS DETECTED\n"
            "INITIATING STORAGE DEFENSE PROTOCOL\n\n"
            "You want to partition this system?\n"
            "Prove you know MBR from GPT.\n"
            "Prove you know mkfs from fsck.\n"
            "Prove you deserve this data."
        ),
        quiz_questions   = [
            QuizQuestion(
                question    = "fdisk -l zeigt 'Disklabel type: gpt'. Was bedeutet das?",
                options     = [
                    "A) Das Laufwerk nutzt MBR mit GPT-Erweiterung",
                    "B) Das Laufwerk nutzt GPT als Partitionstabelle",
                    "C) GRUB ist nicht installiert",
                    "D) Das Laufwerk ist defekt",
                ],
                correct     = "B",
                explanation = "'Disklabel type: gpt' = GPT-Partitionstabelle. 'dos' = MBR.",
                xp_value    = 35,
            ),
            QuizQuestion(
                question    = "parted /dev/sda mkpart primary ext4 1MiB 10GiB — Was passiert?",
                options     = [
                    "A) Partition geplant, wartet auf 'w'",
                    "B) Partition SOFORT erstellt und geschrieben",
                    "C) Partition erstellt aber nicht formatiert",
                    "D) Fehler — parted braucht interaktiven Modus",
                ],
                correct     = "B",
                explanation = "parted schreibt SOFORT. Kein 'w' nötig wie bei fdisk!",
                xp_value    = 35,
            ),
            QuizQuestion(
                question    = "mkfs.ext4 ausgeführt auf /dev/sda1. Was noch nötig zum Nutzen?",
                options     = [
                    "A) Nichts — bereit",
                    "B) fsck ausführen",
                    "C) mount /dev/sda1 /mountpoint",
                    "D) tune2fs aktivieren",
                ],
                correct     = "C",
                explanation = "mkfs erstellt das Dateisystem. Zum Nutzen muss es noch gemountet werden.",
                xp_value    = 35,
            ),
            QuizQuestion(
                question    = "Stromausfall. EXT4-Fehler. System startet nicht. Was ist der korrekte Weg?",
                options     = [
                    "A) fsck -y /dev/sda1 (live, gemountet)",
                    "B) Rescue Mode → umount /dev/sda1 → fsck -y /dev/sda1",
                    "C) mount -o remount,rw / → fsck /dev/sda1",
                    "D) rm -rf / und neu installieren",
                ],
                correct     = "B",
                explanation = "fsck NUR auf unmounted Partitionen. Rescue Mode booten, dann unmount, dann fsck.",
                xp_value    = 35,
            ),
            QuizQuestion(
                question    = "Korrekter LVM-Workflow für ein 20GB Logical Volume?",
                options     = [
                    "A) lvcreate → vgcreate → pvcreate",
                    "B) pvcreate /dev/sdb1 → vgcreate vg0 /dev/sdb1 → lvcreate -L 20G -n lv0 vg0",
                    "C) mkfs.lvm /dev/sdb1 → mount",
                    "D) fdisk /dev/sdb → lvcreate -L 20G",
                ],
                correct     = "B",
                explanation = "LVM: pvcreate → vgcreate → lvcreate. Immer in dieser Reihenfolge.",
                xp_value    = 35,
            ),
            QuizQuestion(
                question    = "Korrekte fstab-Zeile für Swap-Partition /dev/sda2?",
                options     = [
                    "A) /dev/sda2  /swap  swap  defaults  0  0",
                    "B) /dev/sda2  none   swap  sw        0  0",
                    "C) /dev/sda2  none   swap  defaults  0  1",
                    "D) UUID=xxx   swap   none  sw        0  0",
                ],
                correct     = "B",
                explanation = "Swap fstab: Gerät, none (kein Mountpunkt), swap (Typ), sw (Option), 0, 0.",
                xp_value    = 35,
            ),
        ],
        exam_tip         = "Boss-Wiederholung: MBR vs GPT, LVM-Workflow, fstab-Syntax, fsck NUR unmounted, mkfs.ext4 vs mkfs.xfs.",
        memory_tip       = "Eselsbrücke LVM: 'Platte, Gruppe, Laufwerk' = pvcreate, vgcreate, lvcreate. Ohne vorherigen Schritt kein nächster.",
        gear_reward      = "pipe_wrench",
        faction_reward   = ("Root Collective", 20),
    ),
]
