"""
NeonGrid-9 :: Kapitel 1 — Boot Camp
LPIC-1 Topic 101.1: Hardware Settings + Geräteerkennung
Alle 31 Missionen + Boss vollständig implementiert.
"""

from engine.mission_engine import Mission, QuizQuestion

# ══════════════════════════════════════════════════════════════════════════════
# KAPITEL 1 MISSIONEN
# ══════════════════════════════════════════════════════════════════════════════

CHAPTER_1_MISSIONS = [

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.01",
        title       = "Erste Signale — Was ist Hardware?",
        mtype       = "SCAN",
        xp          = 30,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        story       = (
            "Ich hab dich bewusstlos im Sector-7-Slum gefunden.\n"
            "Kein Terminal. Kein Wissen. Nur Potential.\n\n"
            "Hör mir zu: NeonGrid-9 läuft auf Hardware.\n"
            "Jedes System, jeder Daemon, jedes Netz — alles\n"
            "beginnt mit physischer Hardware.\n"
            "Lern sie kennen. Oder stirb unwissend."
        ),
        why_important = (
            "LPIC-1 prüft dich auf Hardware-Grundlagen.\n"
            "Als Sysadmin MUSST du wissen was im System steckt —\n"
            "sonst kannst du keinen Treiber laden, keine Fehler debuggen,\n"
            "keinen Kernel konfigurieren."
        ),
        explanation = (
            "Linux erkennt Hardware automatisch beim Boot.\n"
            "Die wichtigsten Hardware-Komponenten:\n\n"
            "  CPU    — Central Processing Unit (Prozessor)\n"
            "  RAM    — Random Access Memory (Arbeitsspeicher)\n"
            "  Disk   — Festplatten / SSDs / NVMe\n"
            "  GPU    — Grafikkarte\n"
            "  NIC    — Netzwerkkarte\n"
            "  USB    — Universal Serial Bus Geräte\n\n"
            "Infos über Hardware findest du in /proc/ und /sys/\n"
            "sowie mit spezialisierten Befehlen."
        ),
        ascii_art = """
  ██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗    ██╗ █████╗ ██████╗ ███████╗
  ██║  ██║██╔══██╗██╔══██╗██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔════╝
  ███████║███████║██████╔╝██║  ██║██║ █╗ ██║███████║██████╔╝█████╗
  ██╔══██║██╔══██║██╔══██╗██║  ██║██║███╗██║██╔══██║██╔══██╗██╔══╝
  ██║  ██║██║  ██║██║  ██║██████╔╝╚███╔███╔╝██║  ██║██║  ██║███████╗
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚══╝╚══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝

  [ CHAPTER 01 :: HARDWARE RECON ]
  > Scanning physical layer... NeonGrid-9 boot sequence initiated.""",
        story_transitions = [
            "Zara tippt auf ihr Holopad. Sensorpulse scannen die Umgebung.",
            "Die Daten fließen. /proc öffnet sich wie ein Fenster zur Maschine.",
            "Jedes Byte Hardware hat eine Adresse. Lern sie zu lesen.",
            "NeonGrid-9 wartet nicht. Starte deinen ersten Scan.",
        ],
        syntax  = "lspci    # PCI-Geräte auflisten\nlsusb    # USB-Geräte auflisten",
        example = "$ lspci\n00:02.0 VGA: Intel UHD Graphics 620\n01:00.0 Network: Intel Wireless 8265",
        task_description  = "Zeige alle PCI-Geräte im System an.",
        expected_commands = ["lspci"],
        hint_text         = "Der Befehl beginnt mit 'ls' und endet mit 'pci'",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welcher Befehl listet alle PCI-Geräte auf?",
                options   = ["A) lshw", "B) lspci", "C) dmidecode", "D) hwinfo"],
                correct   = "B",
                explanation = "lspci (list PCI) zeigt alle PCI/PCIe-Geräte. lshw ist umfassender, dmidecode liest BIOS-Infos.",
                xp_value  = 15,
            ),
            QuizQuestion(
                question  = "Wo im Dateisystem findest du Hardware-Informationen des Kernels?",
                options   = ["A) /etc/hardware", "B) /usr/hw", "C) /proc und /sys", "D) /var/devices"],
                correct   = "C",
                explanation = "/proc/ ist ein virtuelles Dateisystem mit Kernel-Laufzeitdaten. /sys/ ist das sysfs für Geräteverwaltung.",
                xp_value  = 15,
            ),
        ],
        exam_tip    = (
            "LPIC-1 fragt oft nach dem Unterschied zwischen\n"
            "/proc/ (Kernel-Laufzeitinfos) und /sys/ (Gerätehierarchie).\n"
            "/proc ist älter, /sys ist neuer und strukturierter."
        ),
        memory_tip  = "lspci = List PCI. lsusb = List USB. Merke: 'ls' vor dem Bus-Typ.",
        gear_reward = None,
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.02",
        title       = "BIOS Whisper — BIOS vs UEFI",
        mtype       = "SCAN",
        xp          = 20,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        story       = (
            "Das BIOS Imperium hat seinen Namen nicht ohne Grund.\n"
            "BIOS — Basic Input/Output System — war jahrzehntelang\n"
            "das Fundament jedes PCs. Heute dominiert UEFI.\n"
            "Versteh den Unterschied, oder werde kontrolliert."
        ),
        why_important = (
            "BIOS/UEFI ist der erste Code, der beim Einschalten läuft.\n"
            "Es initialisiert Hardware und startet den Bootloader.\n"
            "Für LPIC-1 musst du den Unterschied kennen und\n"
            "wissen wie Linux damit interagiert."
        ),
        explanation = (
            "BIOS (Legacy):\n"
            "  ► Nur 16-bit Code\n"
            "  ► MBR (Master Boot Record) — max 4 primäre Partitionen\n"
            "  ► Max. 2TB Festplattengröße\n"
            "  ► Kein Secure Boot\n"
            "  ► Gestartet von /dev/sdX Sektor 0\n\n"
            "UEFI (Unified Extensible Firmware Interface):\n"
            "  ► 32/64-bit Code, viel mächtiger\n"
            "  ► GPT (GUID Partition Table) — 128 Partitionen\n"
            "  ► Festplatten > 2TB unterstützt\n"
            "  ► Secure Boot Unterstützung\n"
            "  ► EFI System Partition (ESP) notwendig\n"
            "  ► UEFI-Variablen in /sys/firmware/efi/"
        ),
        syntax  = (
            "# UEFI-Variablen anzeigen:\nls /sys/firmware/efi/\n\n"
            "# UEFI Boot-Einträge verwalten:\nefibootmgr\n\n"
            "# Prüfen ob System UEFI nutzt:\n[ -d /sys/firmware/efi ] && echo UEFI || echo BIOS"
        ),
        example = (
            "$ ls /sys/firmware/efi/\nefivars  fw_platform_size  runtime  runtime-map  systab\n\n"
            "$ efibootmgr\nBootCurrent: 0001\nBootOrder: 0001,0000\nBoot0000* Windows Boot Manager\nBoot0001* debian"
        ),
        task_description  = "Prüfe ob dieses System UEFI oder BIOS nutzt (ls /sys/firmware/efi/).",
        expected_commands = ["ls /sys/firmware/efi/", "ls /sys/firmware/efi"],
        hint_text         = "Schau in /sys/firmware/efi/ — wenn das Verzeichnis existiert: UEFI",
        hints = [
            "Das Verzeichnis, das du suchst, ist in /sys/ — speziell im firmware-Unterverzeichnis.",
            "Versuche: ls /sys/firmware/efi/ oder ls /sys/firmware/efi",
            "Der vollständige Befehl ist: ls /sys/firmware/efi/",
        ],
        quiz_questions    = [
            QuizQuestion(
                question  = "Was ist der Hauptunterschied zwischen BIOS und UEFI bezüglich Partitionen?",
                options   = [
                    "A) BIOS nutzt GPT, UEFI nutzt MBR",
                    "B) BIOS nutzt MBR (max 4 primär), UEFI nutzt GPT (bis 128 Partitionen)",
                    "C) Beide nutzen MBR, aber UEFI unterstützt mehr davon",
                    "D) UEFI nutzt ausschließlich ext4-Dateisysteme",
                ],
                correct   = "B",
                explanation = "MBR = Legacy BIOS mit 4 primären Partitionen max. GPT = UEFI mit bis zu 128 Partitionen und >2TB Disks.",
            ),
            QuizQuestion(
                question  = "Welches Verzeichnis enthält UEFI-Variablen unter Linux?",
                options   = [
                    "A) /etc/uefi/",
                    "B) /boot/efi/",
                    "C) /sys/firmware/efi/",
                    "D) /dev/uefi/",
                ],
                correct   = "C",
                explanation = "/sys/firmware/efi/ ist das sysfs-Interface zu UEFI-Variablen. Existiert dieses Verzeichnis, läuft das System im UEFI-Modus.",
            ),
        ],
        exam_tip   = (
            "Prüfungsfrage: 'Wie erkennst du ob ein Linux-System UEFI nutzt?'\n"
            "Antwort: Prüfe ob /sys/firmware/efi/ existiert.\n"
            "Oder: [ -d /sys/firmware/efi ] && echo UEFI || echo BIOS"
        ),
        memory_tip = "UEFI = /sys/firmware/efi/ vorhanden. BIOS = Verzeichnis fehlt.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.03",
        title       = "IRQ Hunter — Interrupts lesen",
        mtype       = "INFILTRATE",
        xp          = 25,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        story       = (
            "Jedes Gerät unterbricht den Prozessor wenn es Aufmerksamkeit\n"
            "braucht. Diese Unterbrechungen heißen IRQs — Interrupt Requests.\n"
            "Wer IRQs lesen kann, versteht wie Hardware mit dem Kernel spricht."
        ),
        why_important = (
            "IRQs zeigen dir welche Hardware aktiv ist und ob es\n"
            "Konflikte gibt. Bei Hardware-Problemen ist /proc/interrupts\n"
            "oft der erste Ort zum Suchen."
        ),
        explanation = (
            "/proc/interrupts zeigt:\n"
            "  Spalte 1: IRQ-Nummer\n"
            "  Spalte 2-N: Interrupt-Zähler pro CPU-Kern\n"
            "  Letztes Feld: Gerätename\n\n"
            "Wichtige IRQs:\n"
            "  IRQ 0  — System-Timer\n"
            "  IRQ 1  — Tastatur\n"
            "  IRQ 8  — Echtzeituhr (RTC)\n"
            "  IRQ 9  — ACPI\n"
            "  IRQ 14 — IDE/ATA (historisch, Primär)\n"
            "  IRQ 15 — IDE/ATA (historisch, Sekundär)"
        ),
        syntax  = "cat /proc/interrupts",
        example = (
            "$ cat /proc/interrupts\n"
            "           CPU0   CPU1\n"
            "  0:         16      0  timer\n"
            "  1:          0   3765  i8042 (Tastatur)\n"
            "  8:          1      0  rtc0\n"
            " 14:          0      0  INT344B:00"
        ),
        task_description  = "Lies die IRQ-Tabelle des Systems aus.",
        expected_commands = ["cat /proc/interrupts"],
        hint_text         = "Nutze cat und lese die Datei /proc/interrupts",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welche Datei zeigt IRQ-Zuweisungen der Hardware?",
                options   = ["A) /proc/irq", "B) /proc/interrupts", "C) /sys/irqs", "D) /etc/hardware"],
                correct   = "B",
                explanation = "/proc/interrupts ist das virtuelle Kernel-Interface für IRQ-Statistiken.",
            ),
            QuizQuestion(
                question  = "Welcher IRQ ist traditionell der System-Timer?",
                options   = ["A) IRQ 14", "B) IRQ 8", "C) IRQ 0", "D) IRQ 1"],
                correct   = "C",
                explanation = "IRQ 0 ist der System-Timer (Programmable Interval Timer). IRQ 1 ist die Tastatur, IRQ 8 die RTC.",
            ),
        ],
        exam_tip   = (
            "LPIC-1 Falle: IRQ 14 war der Primary IDE Controller.\n"
            "Historisch relevant, auch wenn moderne NVMe/SATA-Systeme\n"
            "andere IRQ-Nummern verwenden."
        ),
        memory_tip = "/proc/interrupts = IRQ-Tabelle. Zähler steigen mit jeder Unterbrechung.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.04",
        title       = "I/O Port Trace — Ports lesen",
        mtype       = "INFILTRATE",
        xp          = 25,
        chapter     = 1,
        speaker     = "SYSTEM",
        story       = (
            "SYSTEM: I/O Ports — die unsichtbaren Kanäle zwischen\n"
            "CPU und Hardware. 0x0060 spricht mit der Tastatur.\n"
            "0x0040 tickt im Takt der Zeit.\n"
            "Lies /proc/ioports. Versteh was da fließt."
        ),
        why_important = (
            "I/O Ports sind die Kommunikationsadressen zwischen\n"
            "Betriebssystem und Hardware-Registern.\n"
            "Wichtig für LPIC-1 Grundlagenwissen."
        ),
        explanation = (
            "/proc/ioports zeigt alle I/O-Port-Adressen in hexadezimal.\n\n"
            "Wichtige Adressen:\n"
            "  0020-0021 : PIC (Programmable Interrupt Controller)\n"
            "  0040-0043 : Timer\n"
            "  0060-0060 : Tastatur (Keyboard)\n"
            "  0070-0077 : RTC (Real Time Clock)\n"
            "  00f0-00ff : FPU (Floating Point Unit)"
        ),
        syntax  = "cat /proc/ioports",
        example = (
            "$ cat /proc/ioports\n"
            "0000-0cf7 : PCI Bus 0000:00\n"
            "  0040-0043 : timer0\n"
            "  0060-0060 : keyboard\n"
            "  0070-0077 : rtc0"
        ),
        task_description  = "Zeige alle I/O Port-Adressen an.",
        expected_commands = ["cat /proc/ioports"],
        hint_text         = "Ähnlich wie /proc/interrupts — nutze cat mit dem richtigen /proc/-Pfad",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welche Datei zeigt I/O Port-Zuweisungen?",
                options   = ["A) /proc/ioports", "B) /proc/ports", "C) /sys/ioports", "D) /proc/io"],
                correct   = "A",
                explanation = "/proc/ioports listet alle registrierten I/O-Port-Adressbereiche.",
            ),
        ],
        exam_tip   = "Trio für LPIC-1: /proc/interrupts (IRQs), /proc/ioports (I/O), /proc/iomem (Speicher)",
        memory_tip = "ports → /proc/ioports. Hex-Adressen, zeigen Gerätekommunikation.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.05",
        title       = "Memory Map — DMA und Speicherbereiche",
        mtype       = "SCAN",
        xp          = 25,
        chapter     = 1,
        speaker     = "SYSTEM",
        story       = (
            "SYSTEM: Speicher ist nicht einfach 'RAM'.\n"
            "Der physische Adressraum wird aufgeteilt — zwischen\n"
            "Kernel, Geräten, BIOS. DMA erlaubt Direktzugriff.\n"
            "Scan /proc/iomem. Sieh wie dein System atmet."
        ),
        why_important = (
            "/proc/iomem zeigt die Memory Map des Systems —\n"
            "wie physischer Speicher zwischen Kernel, RAM und\n"
            "Hardware-Geräten aufgeteilt ist."
        ),
        explanation = (
            "DMA = Direct Memory Access\n"
            "Geräte können direkt in den RAM schreiben ohne CPU.\n\n"
            "/proc/iomem Einträge:\n"
            "  System RAM : Normaler Arbeitsspeicher\n"
            "  Kernel code: Wo der Kernel im RAM liegt\n"
            "  Kernel data: Kernel-Datensegment\n"
            "  Video ROM  : BIOS der Grafikkarte\n"
            "  PCI Bus    : Speicher-gemappte Geräteregister"
        ),
        syntax  = "cat /proc/iomem",
        example = (
            "$ cat /proc/iomem\n"
            "00100000-9fffffff : System RAM\n"
            "  01000000-01c11c9f : Kernel code\n"
            "  01c11ca0-0209167f : Kernel data\n"
            "ec000000-ecffffff : 0000:00:02.0 (GPU Speicher)"
        ),
        task_description  = "Lies die Memory Map des Systems.",
        expected_commands = ["cat /proc/iomem"],
        hint_text         = "/proc/iomem — 'iomem' = I/O Memory",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was zeigt /proc/iomem?",
                options   = [
                    "A) Prozessor-Speicherbelegung (Prozesse)",
                    "B) Physische Speicherbereiche-Zuordnung (Hardware + RAM)",
                    "C) Swap-Speicher-Statistiken",
                    "D) Cache-Größen der CPU",
                ],
                correct   = "B",
                explanation = "/proc/iomem zeigt die physische Speicherkarte: welche Adressen dem RAM, welche der Hardware zugeordnet sind.",
            ),
        ],
        exam_tip   = "Die drei /proc Dateien für Hardware-Ressourcen:\n/proc/interrupts — IRQs\n/proc/ioports — I/O Ports\n/proc/iomem — Speicherbereiche",
        memory_tip = "iomem = IO Memory Map. Zeigt physischen Speicher-Layout.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.06",
        title       = "CPU Profiler — /proc/cpuinfo lesen",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        story       = (
            "Dein Prozessor ist das Gehirn. Ich muss wissen\n"
            "womit ich arbeite. Zeig mir was in dir steckt."
        ),
        why_important = (
            "/proc/cpuinfo ist die Primärquelle für CPU-Informationen.\n"
            "Ohne CPU-Wissen kannst du keinen Kernel konfigurieren,\n"
            "keine Virtualisierung einrichten, keine Performance-Probleme lösen."
        ),
        explanation = (
            "/proc/cpuinfo zeigt pro CPU-Kern einen Block mit:\n\n"
            "  processor   : CPU-Kern-Nummer (0 = erster Kern)\n"
            "  vendor_id   : GenuineIntel / AuthenticAMD\n"
            "  cpu family  : CPU-Generation\n"
            "  model name  : Name des Prozessors\n"
            "  cpu MHz     : Aktuelle Taktfrequenz\n"
            "  cache size  : L2-Cache Größe\n"
            "  cpu cores   : Anzahl physischer Kerne\n"
            "  flags       : CPU-Fähigkeiten (vmx=Intel VT, svm=AMD-V)\n\n"
            "Anzahl der Kerne zählen:\n"
            "grep -c 'processor' /proc/cpuinfo"
        ),
        syntax  = "cat /proc/cpuinfo\ngrep -c 'processor' /proc/cpuinfo   # Kern-Anzahl",
        example = (
            "$ cat /proc/cpuinfo | head -10\n"
            "processor\t: 0\n"
            "vendor_id\t: GenuineIntel\n"
            "model name\t: Intel Core i7-8550U @ 1.80GHz\n"
            "cpu cores\t: 4\n"
            "flags\t\t: fpu vme vmx sse4_2 ..."
        ),
        task_description  = "Zeige CPU-Informationen aus /proc/cpuinfo an.",
        expected_commands = ["cat /proc/cpuinfo"],
        hint_text         = "cat /proc/cpuinfo — die CPU-Info-Datei im /proc/ Verzeichnis",
        quiz_questions    = [
            QuizQuestion(
                question  = "Wie zählst du die Anzahl der CPU-Kerne mit einem Befehl?",
                options   = [
                    "A) cpu --count",
                    "B) grep -c 'processor' /proc/cpuinfo",
                    "C) nproc /proc/cpuinfo",
                    "D) cat /proc/cores",
                ],
                correct   = "B",
                explanation = "grep -c zählt Zeilen mit 'processor'. Jeder Kern hat einen eigenen Block mit dieser Zeile. nproc gibt dieselbe Info, liest aber auch /proc/cpuinfo.",
            ),
            QuizQuestion(
                question  = "Welches Flag in /proc/cpuinfo zeigt Intel VT-x Virtualisierungs-Support?",
                options   = ["A) svm", "B) virt", "C) vmx", "D) kvm"],
                correct   = "C",
                explanation = "vmx = Intel Virtualization Technology for IA-32/64 (VT-x). svm = AMD Secure Virtual Machine (AMD-V).",
            ),
        ],
        exam_tip   = "LPIC-1: vmx in /proc/cpuinfo flags = Intel VT-x.\nsvm = AMD-V. Ohne diese Flags keine Hardware-Virtualisierung.",
        memory_tip = "cpuinfo = CPU Informationen. flags enthält vmx/svm für Virtualisierung.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.07",
        title       = "RAM Inspector — /proc/meminfo",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        speaker     = "SYSTEM",
        story       = (
            "SYSTEM: Dein RAM ist deine Arena.\n"
            "Wieviel frei? Wieviel gecacht? Wieviel verschwendet?\n"
            "/proc/meminfo gibt dir die harte Wahrheit.\n"
            "Kenn deinen Speicher — oder verlier die Kontrolle."
        ),
        why_important = (
            "Speichermanagement ist kritisch für jeden Sysadmin.\n"
            "/proc/meminfo gibt dir den vollständigen Speicher-Status\n"
            "in Echtzeit — kein Tool ist notwendig."
        ),
        explanation = (
            "Wichtige Felder in /proc/meminfo:\n\n"
            "  MemTotal     : Gesamter physischer RAM\n"
            "  MemFree      : Komplett ungenutzter RAM\n"
            "  MemAvailable : Verfügbarer RAM für neue Prozesse\n"
            "                 (freier RAM + nutzbarer Cache)\n"
            "  Buffers      : Puffer für Block-Devices\n"
            "  Cached       : Datei-Cache (kann freigegeben werden)\n"
            "  SwapTotal    : Gesamte Swap-Größe\n"
            "  SwapFree     : Freier Swap\n\n"
            "WICHTIG: MemFree ≠ 'freier Speicher für mich'\n"
            "Nutze MemAvailable für reale Verfügbarkeit!"
        ),
        syntax  = "cat /proc/meminfo\ngrep MemAvailable /proc/meminfo   # nur Verfügbar",
        example = (
            "$ grep -E 'MemTotal|MemAvailable|SwapFree' /proc/meminfo\n"
            "MemTotal:       16252928 kB\n"
            "MemAvailable:    8934512 kB\n"
            "SwapFree:        2097148 kB"
        ),
        task_description  = "Zeige den Speicherstatus aus /proc/meminfo.",
        expected_commands = ["cat /proc/meminfo"],
        hint_text         = "cat /proc/meminfo — meminfo im /proc/ Verzeichnis",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welches Feld in /proc/meminfo gibt den wirklich VERFÜGBAREN RAM für neue Prozesse an?",
                options   = ["A) MemFree", "B) MemAvailable", "C) Buffers", "D) Cached"],
                correct   = "B",
                explanation = "MemAvailable berücksichtigt freien RAM UND nutzbaren Cache/Buffers. MemFree ist nur wirklich ungenutzter RAM — in der Praxis meist kleiner.",
            ),
        ],
        exam_tip   = "MemFree vs MemAvailable:\nMemFree = wirklich ungenutzt (oft klein wegen Cache).\nMemAvailable = nutzbar für neue Prozesse (MemFree + freigebbarer Cache).",
        memory_tip = "MemAvailable > MemFree — Cache ist kein 'blockierter' Speicher.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.08",
        title       = "PCI Scanner — lspci Grundlagen",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        story       = (
            "lspci ist dein Scanner für den PCI-Bus.\n"
            "Jede Grafikkarte, jede Netzwerkkarte, jede\n"
            "NVMe-SSD — alles sitzt auf dem PCI-Bus.\n"
            "Scan das System."
        ),
        why_important = (
            "lspci ist das Standard-Tool für PCI-Geräteerkennung.\n"
            "LPIC-1 prüft explizit lspci und seine wichtigsten Flags."
        ),
        explanation = (
            "lspci — List PCI devices\n\n"
            "Ausgabeformat:\n"
            "  BUS:DEVICE.FUNCTION  Klasse: Gerätename\n\n"
            "Beispiel:\n"
            "  00:02.0  VGA controller: Intel UHD Graphics 620\n"
            "  ───┬───  ────┬────      ──────────┬────────────\n"
            "     │         │                    └─ Gerätename\n"
            "     │         └─ PCI Klasse\n"
            "     └─ Bus:Device.Function\n\n"
            "Wichtige PCI-Klassen:\n"
            "  VGA    — Grafikkarte\n"
            "  USB    — USB Controller\n"
            "  Audio  — Soundkarte\n"
            "  Network — Netzwerkkarte\n"
            "  NVM   — NVMe SSD"
        ),
        syntax  = "lspci           # Alle PCI-Geräte\nlspci -v        # Verbose (Details)\nlspci -vv       # Sehr verbose\nlspci -k        # Mit Kernel-Treiber",
        example = (
            "$ lspci\n"
            "00:00.0 Host bridge: Intel 8th Gen Core\n"
            "00:02.0 VGA: Intel UHD Graphics 620\n"
            "01:00.0 Network: Intel Wireless 8265\n"
            "02:00.0 NVM: Samsung NVMe SSD SM981"
        ),
        task_description  = "Liste alle PCI-Geräte auf.",
        expected_commands = ["lspci"],
        hint_text         = "Tippe: lspci",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was zeigt 'lspci -k'?",
                options   = [
                    "A) Kernel-Version",
                    "B) PCI-Geräte mit zugehörigem Kernel-Treiber",
                    "C) Kernel-Konfig für PCI",
                    "D) PCI-Bus-Konfiguration im Kernel",
                ],
                correct   = "B",
                explanation = "lspci -k zeigt zu jedem PCI-Gerät den aktiven Kernel-Treiber (z.B. 'Kernel driver in use: i915').",
            ),
        ],
        exam_tip   = "lspci -k = Kernel-Treiber sehen.\nlspci -v = Verbose Details.\nlspci -vv = sehr detailliert (LPIC prüft die Flags!).",
        memory_tip = "lspci = List PCI. -k = Kernel driver. -v = verbose.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.09",
        title       = "PCI Deep Dive — lspci -v und -k",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "SYSTEM",
        story       = (
            "SYSTEM: lspci ohne Flags zeigt dir die Oberfläche.\n"
            "lspci -v zeigt Details. lspci -k zeigt Treiber.\n"
            "Welches Modul treibt deine Netzwerkkarte?\n"
            "Lern die Flags — die Prüfung fragt genau das."
        ),
        why_important = "lspci -v/-k sind LPIC-1 Prüfungsthemen. Du musst die Flags kennen.",
        explanation = (
            "lspci Flags im Detail:\n\n"
            "  -v    : Verbose — mehr Details pro Gerät\n"
            "          (Capabilities, IRQ, Memory-Mapping)\n\n"
            "  -vv   : Sehr verbose — vollständige Infos\n\n"
            "  -k    : Kernel-Treiber — zeigt:\n"
            "          'Kernel driver in use: treibername'\n"
            "          'Kernel modules: mögliche_module'\n\n"
            "  -s    : Bestimmtes Gerät filtern\n"
            "          lspci -s 00:02.0  (Bus:Device.Func)\n\n"
            "  -n    : Numerische IDs (Vendor:Device)\n\n"
            "  -nn   : Name + numerische IDs kombiniert"
        ),
        syntax  = "lspci -v        # verbose\nlspci -k        # mit Kernel-Treiber\nlspci -s 00:02.0  # bestimmtes Gerät",
        example = (
            "$ lspci -k\n"
            "00:02.0 VGA compatible controller: Intel UHD Graphics 620\n"
            "\tKernel driver in use: i915\n"
            "\tKernel modules: i915\n\n"
            "01:00.0 Network controller: Intel Wireless 8265\n"
            "\tKernel driver in use: iwlwifi\n"
            "\tKernel modules: iwlwifi"
        ),
        task_description  = "Zeige PCI-Geräte mit ihren Kernel-Treibern.",
        expected_commands = ["lspci -k"],
        hint_text         = "lspci mit dem Flag -k",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welcher Befehl zeigt welcher Kernel-Treiber für ein PCI-Gerät aktiv ist?",
                options   = ["A) lspci -d", "B) lspci -k", "C) modinfo pci", "D) lsmod -pci"],
                correct   = "B",
                explanation = "lspci -k zeigt 'Kernel driver in use: <name>' für jedes PCI-Gerät.",
            ),
        ],
        exam_tip   = "LPIC-1 fragt: 'Welches lspci-Flag zeigt den Kernel-Treiber?' — Antwort: -k",
        memory_tip = "-k = Kernel driver. Unverzichtbar für Treiber-Debugging.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.10",
        title       = "USB Recon — lsusb Grundlagen",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        story       = (
            "USB-Geräte kommen und gehen. Maus, Tastatur,\n"
            "USB-Stick, Webcam — alles hot-pluggable.\n"
            "lsusb ist dein Radar für den USB-Bus."
        ),
        why_important = "lsusb ist das Gegenstück zu lspci für USB-Geräte. LPIC-1 Pflichtthema.",
        explanation = (
            "lsusb — List USB devices\n\n"
            "Ausgabeformat:\n"
            "  Bus NNN Device NNN: ID VVVV:PPPP Hersteller Gerät\n\n"
            "  Bus    : USB-Bus-Nummer\n"
            "  Device : Gerätenummer auf dem Bus\n"
            "  ID     : Vendor:Product (hexadezimal)\n\n"
            "Beispiele:\n"
            "  1d6b:0002 — Linux Foundation 2.0 root hub\n"
            "  04f2:b604 — Chicony (Webcam)\n"
            "  8087:0a2b — Intel (Bluetooth)\n\n"
            "Vendor/Device IDs sind im Linux USB ID Repository:"
        ),
        syntax  = "lsusb           # Alle USB-Geräte\nlsusb -v        # Verbose Details\nlsusb -t        # Tree-Ansicht\nlsusb -d 04f2:  # Nach Vendor filtern",
        example = (
            "$ lsusb\n"
            "Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub\n"
            "Bus 001 Device 005: ID 04f2:b604 Chicony Integrated Camera\n"
            "Bus 001 Device 004: ID 8087:0a2b Intel Bluetooth"
        ),
        task_description  = "Liste alle USB-Geräte auf.",
        expected_commands = ["lsusb"],
        hint_text         = "Tippe: lsusb",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was bedeutet die ID-Nummer bei lsusb? (z.B. 04f2:b604)",
                options   = [
                    "A) Speichergröße:Geräteklasse",
                    "B) Vendor-ID:Product-ID (hexadezimal)",
                    "C) Bus-Nummer:Device-Nummer",
                    "D) IRQ:DMA-Kanal",
                ],
                correct   = "B",
                explanation = "Die ID besteht aus Vendor-ID (Hersteller) und Product-ID, beide hexadezimal. 04f2 = Chicony Electronics, b604 = bestimmte Webcam.",
            ),
        ],
        exam_tip   = "lsusb = USB-Geräte. lspci = PCI-Geräte. Beide wichtig für LPIC-1.",
        memory_tip = "lsusb → List USB. ID = Vendor:Product (hex).",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.11",
        title       = "USB Detail — lsusb -v und -t",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "SYSTEM",
        story       = (
            "SYSTEM: USB — Universal Serial Bus. Universell, ja.\n"
            "Aber jedes Gerät hat eine einzigartige ID.\n"
            "lsusb -v zeigt Deskriptoren. lsusb -t zeigt den Baum.\n"
            "Identifiziere deine Hardware bis auf Chip-Level."
        ),
        why_important = "lsusb -v und -t sind LPIC-1 Prüfungsthemen. USB-Gerätehierarchie und Deskriptoren zu lesen ist Pflicht für Hardware-Diagnostik.",
        explanation = (
            "lsusb Flags:\n\n"
            "  -v    : Verbose — vollständige USB-Deskriptoren\n"
            "          (Klasse, Protokoll, Endpoints, Geschwindigkeit)\n\n"
            "  -t    : Tree — hierarchische Bus-Ansicht\n"
            "          Zeigt welche Geräte an welchem Hub hängen\n\n"
            "  -s BUS:DEV : Bestimmtes Gerät\n"
            "               lsusb -s 001:005\n\n"
            "USB-Geschwindigkeiten:\n"
            "  1.5M  = Low Speed (ältere HID-Geräte)\n"
            "  12M   = Full Speed\n"
            "  480M  = High Speed (USB 2.0)\n"
            "  5000M = SuperSpeed (USB 3.0)"
        ),
        syntax  = "lsusb -t        # Tree-Ansicht\nlsusb -v        # Verbose",
        example = (
            "$ lsusb -t\n"
            "/:  Bus 01.Port 1: Dev 1, root_hub, 480M\n"
            "    |__ Port 4: Dev 3, HID (Maus), 1.5M\n"
            "    |__ Port 8: Dev 5, Video (Webcam), 480M"
        ),
        task_description  = "Zeige USB-Geräte in der Baum-Ansicht.",
        expected_commands = ["lsusb -t"],
        hint_text         = "lsusb mit Flag -t für Tree",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was zeigt 'lsusb -t'?",
                options   = [
                    "A) Tiefe Verbose-Ausgabe aller USB-Geräte",
                    "B) USB-Bus-Hierarchie als Baumstruktur",
                    "C) USB-Temperatursensoren",
                    "D) Timeline der USB-Verbindungen",
                ],
                correct   = "B",
                explanation = "lsusb -t zeigt den USB-Bus als Baum: welcher Hub welche Geräte hat. Sehr nützlich bei komplexen USB-Setups.",
            ),
        ],
        exam_tip   = "lsusb -t = Tree (Baum). Zeigt USB-Hub-Hierarchie.",
        memory_tip = "-t = Tree. Baumansicht des USB-Bus.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.12",
        title       = "Hardware Oracle — lshw vollständig",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "KERNEL-ORAKEL",
        story       = (
            "Ich bin das Kernel-Orakel.\n"
            "lshw — Hardware List — ist die umfassendste\n"
            "Hardware-Inventarisierung die du unter Linux bekommst.\n"
            "Jeden Chip. Jeden Bus. Jede Karte. Alles."
        ),
        why_important = (
            "lshw kombiniert alle Hardware-Informationsquellen\n"
            "in einer strukturierten Ausgabe.\n"
            "Ideal für vollständige Hardware-Inventare und Troubleshooting."
        ),
        explanation = (
            "lshw — List Hardware (braucht root für volle Details)\n\n"
            "Klassen-Hierarchie:\n"
            "  system     — Gesamtsystem (Hersteller, Modell, Serial)\n"
            "  bus        — Mainboard\n"
            "  memory     — RAM Module\n"
            "  processor  — CPU\n"
            "  display    — Grafik\n"
            "  storage    — Festplatten-Controller\n"
            "  disk       — Einzelne Disks\n"
            "  network    — Netzwerkkarte\n"
            "  multimedia — Audio\n\n"
            "Ausgabeformate:\n"
            "  lshw          : Text (Standard)\n"
            "  lshw -short   : Kompakttabelle\n"
            "  lshw -html    : HTML-Report\n"
            "  lshw -json    : JSON (für Scripting)\n"
            "  lshw -xml     : XML"
        ),
        syntax  = "lshw              # Vollständige Ausgabe\nlshw -short       # Kompakttabelle\nlshw -class disk  # Nur Disks\nlshw -html > hw_report.html",
        example = (
            "$ lshw -short\n"
            "H/W path   Device  Class       Description\n"
            "===================================================\n"
            "                   system      ThinkPad X1 Carbon\n"
            "/0/4               processor   Intel Core i7-8550U\n"
            "/0/1f              memory      16GiB System Memory\n"
            "/0/100/2  /dev/fb0 display     UHD Graphics 620"
        ),
        task_description  = "Zeige eine kompakte Hardware-Übersicht.",
        expected_commands = ["lshw -short", "lshw"],
        hint_text         = "lshw mit dem Flag -short für kompakte Ansicht",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welches lshw-Flag gibt eine kurze tabellarische Übersicht?",
                options   = ["A) lshw -summary", "B) lshw -brief", "C) lshw -short", "D) lshw -table"],
                correct   = "C",
                explanation = "lshw -short gibt eine kompakte Tabelle mit H/W-Pfad, Gerät, Klasse und Beschreibung.",
            ),
        ],
        exam_tip   = "lshw ist kein LPIC-Standard-Tool aber wird häufig im Admin-Alltag verwendet. Kenne -short und -class.",
        memory_tip = "lshw = List Hardware — vollständig. -short = kompakt.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.13",
        title       = "lshw Klassen — Hardware filtern",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        story       = (
            "Das Kernel-Orakel spricht:\n"
            "lshw listet ALLES. Aber manchmal willst du nur eines.\n"
            "lshw -class disk — nur Datenträger. lshw -class network — nur NICs.\n"
            "Filter die Hardware. Zeig nur was du brauchst."
        ),
        why_important = "lshw -class erlaubt gezieltes Filtern nach Hardware-Typen — in der Prüfung wird nach der korrekten Klassen-Syntax gefragt.",
        explanation = (
            "Mit -class kannst du lshw auf bestimmte Hardware filtern:\n\n"
            "  lshw -class processor  # CPU-Info\n"
            "  lshw -class memory     # RAM Module\n"
            "  lshw -class disk       # Festplatten\n"
            "  lshw -class network    # Netzwerkkarten\n"
            "  lshw -class display    # Grafik\n\n"
            "Mit sudo bekommst du mehr Details (Serial, Firmware)."
        ),
        syntax  = "lshw -class <KLASSE>",
        example = "$ lshw -class disk\n  *-disk\n    description: ATA Disk\n    product: Samsung NVMe 970\n    size: 512GiB",
        task_description  = "Zeige nur Informationen über Disks/Speichergeräte.",
        expected_commands = ["lshw -class disk"],
        hint_text         = "lshw -class disk",
        quiz_questions    = [
            QuizQuestion(
                question  = "Wie filterst du lshw auf Netzwerkkarten?",
                options   = ["A) lshw -type network", "B) lshw -class network", "C) lshw --net", "D) lshw -n"],
                correct   = "B",
                explanation = "lshw -class <klasse> filtert auf eine Hardware-Klasse. Für Netzwerkkarten: lshw -class network.",
            ),
        ],
        exam_tip   = "lshw -class = Hardware-Klasse filtern. Klassen: disk, network, processor, memory, display.",
        memory_tip = "lshw -class KLASSE = nur diese Hardware-Klasse anzeigen.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.14",
        title       = "DMI Decoder — dmidecode",
        mtype       = "INFILTRATE",
        xp          = 40,
        chapter     = 1,
        speaker     = "KERNEL-ORAKEL",
        story       = (
            "Das DMI — Desktop Management Interface — enthält\n"
            "Informationen die das BIOS direkt vom Mainboard liest.\n"
            "Serial-Nummern. BIOS-Version. RAM-Riegel.\n"
            "dmidecode entschlüsselt sie."
        ),
        why_important = (
            "dmidecode liest SMBIOS/DMI-Tabellen — direkt vom BIOS.\n"
            "Unverzichtbar für Warranty-Infos, Asset-Tracking,\n"
            "BIOS-Version prüfen, RAM-Spezifikationen."
        ),
        explanation = (
            "dmidecode — DMI table decoder\n\n"
            "Braucht root-Rechte (oder sudo).\n\n"
            "DMI Types (wichtige Auswahl):\n"
            "  Type 0  : BIOS Information (Version, Datum)\n"
            "  Type 1  : System Information (Hersteller, Modell, Serial)\n"
            "  Type 2  : Baseboard (Mainboard)\n"
            "  Type 4  : Processor\n"
            "  Type 17 : Memory Device (RAM-Riegel Details)\n\n"
            "Filtern:\n"
            "  dmidecode -t 0    # Nur BIOS\n"
            "  dmidecode -t 17   # RAM-Details\n"
            "  dmidecode -s system-serial-number  # Serial"
        ),
        syntax  = "dmidecode             # Alles\ndmidecode -t 0        # BIOS-Info\ndmidecode -t 17       # RAM-Details\ndmidecode -s system-serial-number",
        example = (
            "$ dmidecode -t 0\n"
            "BIOS Information\n"
            "\tVendor: LENOVO\n"
            "\tVersion: N23ET68W (1.44)\n"
            "\tRelease Date: 11/08/2021\n"
            "\tROM Size: 32 MB"
        ),
        task_description  = "Lies die BIOS/DMI-Informationen des Systems.",
        expected_commands = ["dmidecode"],
        hint_text         = "Tippe: dmidecode (braucht root)",
        quiz_questions    = [
            QuizQuestion(
                question  = "Mit welchem Befehl liest du direkt BIOS-Informationen aus den DMI-Tabellen?",
                options   = ["A) biosinfo", "B) dmidecode", "C) smbios", "D) hwdecode"],
                correct   = "B",
                explanation = "dmidecode liest SMBIOS/DMI-Tabellen, die das BIOS aus dem System-ROM bereitstellt.",
            ),
            QuizQuestion(
                question  = "Welcher DMI-Type gibt RAM-Details aus?",
                options   = ["A) Type 4", "B) Type 0", "C) Type 17", "D) Type 2"],
                correct   = "C",
                explanation = "DMI Type 17 = Memory Device. Zeigt RAM-Riegel mit Größe, Typ, Geschwindigkeit, Steckplatz-Nummer.",
            ),
        ],
        exam_tip   = "dmidecode -t 17 für RAM-Details. Sehr nützlich um zu prüfen:\n'Wie viele RAM-Steckplätze hat das System? Welche sind belegt?'",
        memory_tip = "dmidecode = DMI decode. -t 17 = RAM. -t 0 = BIOS.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.15",
        title       = "Block Recon — lsblk",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "Ich bin DAEMON. Z3R0 hat mir von dir erzählt.\n"
            "Ich helf dir nicht aus Sympathie — ich tu's\n"
            "weil du das Dateisystem noch nicht kennst.\n\n"
            "lsblk. Lern es. Jetzt."
        ),
        why_important = (
            "lsblk ist das modernste Tool für Block-Device-Übersichten.\n"
            "Zeigt Disks, Partitionen und Mount-Punkte übersichtlich.\n"
            "Täglich verwendet von jedem Linux-Admin."
        ),
        explanation = (
            "lsblk — List Block Devices\n\n"
            "Block-Devices sind Geräte mit wahlfreiem Zugriff:\n"
            "  sda, sdb   — SCSI/SATA Disks\n"
            "  nvme0n1    — NVMe SSDs\n"
            "  vda        — Virtuelle Disks\n"
            "  loop0      — Loop-Devices (ISO/Images)\n\n"
            "Ausgabe-Spalten:\n"
            "  NAME   — Gerätename\n"
            "  MAJ:MIN — Major:Minor Nummer\n"
            "  RM     — Removable (1=wechselbar)\n"
            "  SIZE   — Größe\n"
            "  RO     — Read Only\n"
            "  TYPE   — disk/part/lvm\n"
            "  MOUNTPOINT — Wo gemountet"
        ),
        syntax  = "lsblk           # Standardansicht\nlsblk -f        # Mit Dateisystem-Typ + UUID\nlsblk -o NAME,SIZE,TYPE,MOUNTPOINT",
        example = (
            "$ lsblk\n"
            "NAME        SIZE RO TYPE MOUNTPOINT\n"
            "nvme0n1   476.9G  0 disk\n"
            "├─nvme0n1p1  512M  0 part /boot/efi\n"
            "├─nvme0n1p2    1G  0 part /boot\n"
            "└─nvme0n1p3 475G  0 part /\n"
            "sda          15G  0 disk\n"
            "└─sda1        15G  0 part /media/usb"
        ),
        task_description  = "Zeige alle Block-Devices und ihre Partitionen.",
        expected_commands = ["lsblk"],
        hint_text         = "Tippe: lsblk",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was bedeutet 'RM=1' in der lsblk-Ausgabe?",
                options   = [
                    "A) Read-only Mode",
                    "B) Das Gerät ist removable (wechselbar, z.B. USB-Stick)",
                    "C) RAM-backed Device",
                    "D) Remote Mount",
                ],
                correct   = "B",
                explanation = "RM steht für Removable. 1 = wechselbares Gerät (USB, DVD). 0 = fest eingebaut.",
            ),
            QuizQuestion(
                question  = "Welcher lsblk-Flag zeigt zusätzlich Dateisystem-Typ und UUID?",
                options   = ["A) lsblk -u", "B) lsblk -t", "C) lsblk -f", "D) lsblk -d"],
                correct   = "C",
                explanation = "lsblk -f zeigt FSTYPE (Dateisystem-Typ), LABEL und UUID für jede Partition.",
            ),
        ],
        exam_tip   = "lsblk ist der modernere Ersatz für 'fdisk -l' zum Überblick.\nlsblk -f für UUID/FSTYPE.",
        memory_tip = "lsblk = List Block. -f = Filesystem info. Unverzichtbar für Admin-Arbeit.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.16",
        title       = "Block IDs — blkid",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "DAEMON: /dev/sda1 — ein Name der sich ändern kann.\n"
            "UUID=abc-123 — ein Name der bleibt.\n"
            "blkid zeigt beide. /etc/fstab vertraut dem UUID.\n"
            "Kenn den Unterschied. Sonst bootet nichts."
        ),
        why_important = (
            "UUIDs sind entscheidend für /etc/fstab.\n"
            "blkid zeigt dir UUID, Dateisystem-Typ und Label\n"
            "für jede Partition — ohne diese geht kein sauberes Mounten."
        ),
        explanation = (
            "blkid — Block Device Attributes\n\n"
            "Zeigt für jede Partition:\n"
            "  UUID   — Universally Unique Identifier\n"
            "           Bleibt gleich auch wenn /dev/sda → /dev/sdb\n"
            "  TYPE   — Dateisystem (ext4, xfs, vfat, swap)\n"
            "  LABEL  — Optionaler Name\n"
            "  PARTLABEL — GPT Partitions-Label\n\n"
            "Warum UUIDs statt /dev/sdX:\n"
            "  /dev/sda kann sich ändern wenn Disks getauscht werden!\n"
            "  UUID ist immer eindeutig und unveränderlich."
        ),
        syntax  = "blkid                    # Alle Partitionen\nblkid /dev/nvme0n1p3     # Bestimmte Partition\nblkid -t TYPE=ext4       # Nach Typ filtern",
        example = (
            "$ blkid\n"
            '/dev/nvme0n1p1: UUID="A1B2-C3D4" TYPE="vfat"\n'
            '/dev/nvme0n1p2: UUID="abc-001" TYPE="ext4" LABEL="boot"\n'
            '/dev/nvme0n1p3: UUID="abc-002" TYPE="ext4" LABEL="root"'
        ),
        task_description  = "Zeige UUIDs und Dateisystem-Typen aller Partitionen.",
        expected_commands = ["blkid"],
        hint_text         = "Tippe: blkid",
        quiz_questions    = [
            QuizQuestion(
                question  = "Warum ist es besser in /etc/fstab UUIDs statt /dev/sdX zu verwenden?",
                options   = [
                    "A) UUIDs sind kürzer und einfacher zu tippen",
                    "B) /dev/sdX kann sich ändern wenn Geräte hinzugefügt werden; UUIDs sind stabil",
                    "C) UUIDs laden das Dateisystem schneller",
                    "D) /dev/sdX wird ab Kernel 5.0 nicht mehr unterstützt",
                ],
                correct   = "B",
                explanation = "Die /dev/sdX Reihenfolge hängt von der Erkennungsreihenfolge ab und kann sich ändern. UUIDs sind unveränderlich und identifizieren eine Partition eindeutig.",
            ),
        ],
        exam_tip   = "blkid = Block ID. Zeigt UUID für fstab-Einträge.\nFSTYPE: ext4=Linux, vfat=FAT32/EFI, swap=Swap-Partition.",
        memory_tip = "blkid → UUIDs der Partitionen. Basis für /etc/fstab.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.17",
        title       = "udev Paths — udevadm info",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "DAEMON: Jedes Gerät das du ansteckst — ich sehe es.\n"
            "udev empfängt den Kernel-Event. Ich erstelle /dev/sdX.\n"
            "udevadm info verrät den Pfad. udevadm monitor zeigt es live.\n"
            "Lern wie ich Geräte erkenne — du wirst es brauchen."
        ),
        why_important = (
            "udev verwaltet alle Gerätedateien in /dev/.\n"
            "udevadm ist das Admin-Tool für udev — unverzichtbar\n"
            "für Troubleshooting von Geräteproblemen."
        ),
        explanation = (
            "udev — Userspace Device Manager\n\n"
            "udev reagiert auf Kernel-Events (neue Hardware)\n"
            "und erstellt automatisch Dateien in /dev/.\n\n"
            "udevadm Befehle:\n"
            "  udevadm info /dev/sda      # Gerät-Infos\n"
            "  udevadm info -a /dev/sda   # Alle Attribute (Baum)\n"
            "  udevadm monitor            # Live-Events\n"
            "  udevadm trigger            # Regeln neu laden\n"
            "  udevadm settle             # Warten bis alle Events verarbeitet\n\n"
            "Attribute die udevadm zeigt:\n"
            "  DEVNAME   — Gerätedatei (/dev/sda)\n"
            "  DEVTYPE   — disk / partition\n"
            "  ID_VENDOR — Hersteller\n"
            "  ID_MODEL  — Modellname\n"
            "  SUBSYSTEM — block / usb / pci"
        ),
        syntax  = "udevadm info /dev/sda\nudevadm info -a /dev/sda    # Ausführlich\nudevadm monitor             # Live USB-Events",
        example = (
            "$ udevadm info /dev/sda\n"
            "P: /devices/pci0000:00/.../block/sda\n"
            "N: sda\n"
            "E: DEVNAME=/dev/sda\n"
            "E: DEVTYPE=disk\n"
            "E: ID_BUS=usb\n"
            "E: ID_VENDOR=SanDisk\n"
            "E: ID_MODEL=Cruzer_Glide"
        ),
        task_description  = "Zeige udev-Informationen für das Block-Device /dev/sda.",
        expected_commands = ["udevadm info /dev/sda"],
        hint_text         = "udevadm info /dev/sda",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was macht 'udevadm monitor'?",
                options   = [
                    "A) Zeigt alle /dev/ Dateien",
                    "B) Überwacht Live-Events wenn Geräte angesteckt/entfernt werden",
                    "C) Monitort die udev-Regeln auf Fehler",
                    "D) Zeigt udev-Daemon Logs",
                ],
                correct   = "B",
                explanation = "udevadm monitor zeigt in Echtzeit welche udev-Events ausgelöst werden — nützlich zum Debuggen wenn Geräte nicht erkannt werden.",
            ),
        ],
        exam_tip   = "udevadm info <gerät> = Gerät-Attribute.\nudevadm monitor = Live-Events beim Einstecken von Hardware.",
        memory_tip = "udev → Geräte in /dev/. udevadm info = Gerät-Details.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.18",
        title       = "Kernel Ring — dmesg Basics",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        story       = (
            "Der Kernel redet ständig — aber er flüstert.\n"
            "dmesg ist das Mikrofon für den Kernel-Ring-Buffer.\n"
            "Alles was der Kernel beim Booten und danach denkt,\n"
            "steht da."
        ),
        why_important = (
            "dmesg ist DAS Debugging-Tool für Hardware-Probleme.\n"
            "Kernel-Fehler, Treiber-Nachrichten, Hardware-Erkennung —\n"
            "alles in dmesg. LPIC-1 Pflicht."
        ),
        explanation = (
            "dmesg — Display/Driver Message (Kernel Ring Buffer)\n\n"
            "Der Kernel schreibt alle Meldungen in einen\n"
            "Ringpuffer (Ring Buffer) — dmesg liest ihn aus.\n\n"
            "Wichtige dmesg Flags:\n"
            "  dmesg              # Alles ausgeben\n"
            "  dmesg -H           # Human readable (Pager)\n"
            "  dmesg -T           # Timestamps lesbar\n"
            "  dmesg -w           # Watch (live)\n"
            "  dmesg -l err       # Nur Errors\n"
            "  dmesg -l warn,err  # Warn + Error\n"
            "  dmesg --clear      # Buffer leeren\n\n"
            "Filtern mit grep:\n"
            "  dmesg | grep -i usb\n"
            "  dmesg | grep -i error\n"
            "  dmesg | grep -i fail"
        ),
        syntax  = "dmesg\ndmesg -T          # Mit lesbarem Timestamp\ndmesg | grep -i usb\ndmesg | grep -i error",
        example = (
            "$ dmesg | tail -5\n"
            "[    2.111111] e1000e 0000:00:1f.6: NIC Link Up 1000 Mbps\n"
            "[    2.345678] EXT4-fs (nvme0n1p3): mounted filesystem\n"
            "[    3.456789] iwlwifi loaded firmware version 36"
        ),
        task_description  = "Zeige die Kernel-Boot-Meldungen.",
        expected_commands = ["dmesg"],
        hint_text         = "Tippe: dmesg",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was ist der 'Kernel Ring Buffer'?",
                options   = [
                    "A) Ein Speicherbereich für Netzwerkpakete",
                    "B) Ein kreisförmiger Puffer in dem der Kernel Meldungen speichert",
                    "C) Die CPU-Cache-Hierarchie",
                    "D) Ein USB-Ring-Bus",
                ],
                correct   = "B",
                explanation = "Der Ring Buffer ist ein zirkulärer Speicherbereich im Kernel. Neue Meldungen überschreiben die ältesten wenn er voll ist. dmesg liest diesen Buffer.",
            ),
            QuizQuestion(
                question  = "Wie filterst du dmesg auf USB-bezogene Meldungen?",
                options   = [
                    "A) dmesg --usb",
                    "B) dmesg -u",
                    "C) dmesg | grep -i usb",
                    "D) dmesg /dev/usb",
                ],
                correct   = "C",
                explanation = "grep -i (case-insensitive) filtert auf 'usb' in der Ausgabe. dmesg hat kein natives USB-Filter-Flag.",
            ),
        ],
        exam_tip   = "dmesg -T zeigt menschenlesbare Timestamps.\ndmesg -w ist wie tail -f für den Kernel-Buffer.\ndmesg | grep -i error für schnelle Fehlersuche.",
        memory_tip = "dmesg = Kernel spricht. -T = Timestamps. grep -i = filtern.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.19",
        title       = "dmesg Filter — Fehler finden",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "DAEMON: Der Kernel schreit — aber niemand hört zu.\n"
            "dmesg -T zeigt Timestamps. dmesg -l err zeigt nur Fehler.\n"
            "Hardware-Fehler, Kernel-Panics, Treiber-Abstürze — alles hier.\n"
            "Filter das Rauschen. Find die Ursache."
        ),
        why_important = "Fehler in dmesg finden ist eine Kernkompetenz für Troubleshooting.",
        explanation = (
            "dmesg Fehler-Levels:\n"
            "  emerg  — System nicht nutzbar\n"
            "  alert  — Sofortiger Eingriff nötig\n"
            "  crit   — Kritischer Zustand\n"
            "  err    — Fehler (häufig!)\n"
            "  warn   — Warnung\n"
            "  notice — Normal aber beachtenswert\n"
            "  info   — Info\n"
            "  debug  — Debug\n\n"
            "Filter-Techniken:\n"
            "  dmesg -l err,warn          # Nach Level\n"
            "  dmesg | grep -i 'fail\\|error\\|warn'\n"
            "  dmesg | grep -E 'error|fail|warn' -i\n"
            "  dmesg --level=err          # Modern"
        ),
        syntax  = "dmesg -l err\ndmesg | grep -i error\ndmesg | grep -i fail",
        example = (
            "$ dmesg | grep -i error\n"
            "[0.299456] ACPI Error: AE_NOT_FOUND, While evaluating [_S1_]\n"
            "[3.456789] EXT4-fs error: ext4_validate_block_bitmap"
        ),
        task_description  = "Suche in dmesg nach Fehler-Meldungen.",
        expected_commands = ["dmesg | grep -i error"],
        hint_text         = "Pipe dmesg durch grep: dmesg | grep -i error",
        quiz_questions    = [
            QuizQuestion(
                question  = "Wie zeigst du mit dmesg nur Fehler (err) und Warnungen (warn)?",
                options   = [
                    "A) dmesg --errors",
                    "B) dmesg -l err,warn",
                    "C) dmesg | head -20",
                    "D) dmesg -f err",
                ],
                correct   = "B",
                explanation = "dmesg -l (level) filtert nach Log-Level. -l err,warn zeigt nur Fehler und Warnungen.",
            ),
        ],
        exam_tip   = "dmesg -l err = nur Error-Level Meldungen.\nPipe-Variante: dmesg | grep -i error (portabler).",
        memory_tip = "dmesg -l err = Fehler filtern. grep -i = case-insensitive.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.20",
        title       = "Journal Kernel — journalctl -k",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "LYRA-7",
        story       = (
            "Ich bin Lyra-7. KI-Archivarin.\n"
            "Auf systemd-Systemen wird dmesg durch journalctl\n"
            "ergänzt. journalctl -k zeigt den Kernel-Buffer\n"
            "mit systemd-Timestamps und Filteroptionen."
        ),
        why_important = (
            "Auf modernen Systemen (systemd) ist journalctl -k\n"
            "oft präziser als dmesg — mit besserer Filterung\n"
            "und persistentem Speicher."
        ),
        explanation = (
            "journalctl -k — Kernel-Meldungen aus dem Journal\n\n"
            "  -k / --dmesg   : Nur Kernel-Meldungen\n"
            "  -b             : Nur dieser Boot\n"
            "  -b -1          : Vorheriger Boot\n"
            "  --since '1 hour ago'\n"
            "  -p err         : Nur Error-Level\n\n"
            "Unterschied dmesg vs journalctl -k:\n"
            "  dmesg          : Ring-Buffer (verliert ältere Msgs)\n"
            "  journalctl     : Persistent auf Disk (wenn konfiguriert)\n\n"
            "Auf älteren Systemen ohne systemd:\n"
            "  /var/log/dmesg  (Boot-Log)\n"
            "  /var/log/kern.log"
        ),
        syntax  = "journalctl -k           # Kernel-Meldungen\njournalctl -k -b        # Dieser Boot\njournalctl -k -p err    # Nur Errors",
        example = (
            "$ journalctl -k\n"
            "Jan 15 08:00:01 neongrid9 kernel: Linux version 6.1.0\n"
            "Jan 15 08:00:02 neongrid9 kernel: PCI: Using ACPI\n"
            "Jan 15 08:00:03 neongrid9 kernel: EXT4-fs mounted"
        ),
        task_description  = "Zeige Kernel-Meldungen über journalctl.",
        expected_commands = ["journalctl -k"],
        hint_text         = "journalctl -k — k steht für Kernel",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was ist der Vorteil von 'journalctl -k' gegenüber 'dmesg'?",
                options   = [
                    "A) journalctl -k ist schneller",
                    "B) Das Journal speichert Logs persistent, dmesg verliert sie bei Reboot",
                    "C) dmesg zeigt keine Kernel-Meldungen",
                    "D) journalctl -k kann ohne root ausgeführt werden",
                ],
                correct   = "B",
                explanation = "Der Kernel-Ring-Buffer (dmesg) wird bei Reboot gelöscht. Das systemd-Journal kann persistent konfiguriert werden und speichert Logs über Reboots hinaus.",
            ),
        ],
        exam_tip   = "journalctl -k = Kernel-Meldungen.\njournalctl -b = aktueller Boot.\njournalctl -b -1 = letzter Boot (für Crash-Analyse).",
        memory_tip = "journalctl -k = Kernel journal. Persistent, filterbar.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.21",
        title       = "Kernel Module — lsmod",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "DAEMON: Module sind meine Augen und Ohren.\n"
            "Ohne das richtige Modul — kein Treiber, keine Hardware.\n"
            "lsmod zeigt was läuft. Die Spalten: Name, Größe, Abhängigkeiten.\n"
            "Scan die Liste. Was läuft hier wirklich?"
        ),
        why_important = (
            "Kernel-Module sind die Treiber unter Linux.\n"
            "lsmod zeigt alle geladenen Module.\n"
            "Ohne Modul-Wissen kein Treiber-Management."
        ),
        explanation = (
            "Kernel-Module — die Treiber-Architektur:\n\n"
            "  Monolithischer Kernel + Module\n"
            "  Module können zur Laufzeit geladen/entladen werden\n"
            "  Dateierweiterung: .ko (Kernel Object)\n"
            "  Speicherort: /lib/modules/$(uname -r)/\n\n"
            "lsmod Ausgabe-Spalten:\n"
            "  Module  : Name des Moduls\n"
            "  Size    : Größe in Bytes\n"
            "  Used by : Abhängige Module (Referenzzähler)\n\n"
            "Wichtige Modul-Befehle:\n"
            "  lsmod        : Liste aller geladenen Module\n"
            "  modinfo      : Details zu einem Modul\n"
            "  modprobe     : Modul mit Abhängigkeiten laden\n"
            "  rmmod        : Modul entladen\n"
            "  insmod       : Modul direkt laden (ohne Deps)"
        ),
        syntax  = "lsmod               # Alle Module\nlsmod | grep iwl    # Nach Name filtern",
        example = (
            "$ lsmod\n"
            "Module                Size  Used by\n"
            "iwlmvm              540672  0\n"
            "iwlwifi             454656  1 iwlmvm\n"
            "i915               2850816  4\n"
            "nvme                45056   4"
        ),
        task_description  = "Liste alle geladenen Kernel-Module auf.",
        expected_commands = ["lsmod"],
        hint_text         = "Tippe: lsmod",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was bedeutet '1 iwlmvm' in der 'Used by' Spalte von lsmod?",
                options   = [
                    "A) Das Modul wurde 1 Mal installiert",
                    "B) Das Modul hat 1 abhängiges Modul namens iwlmvm",
                    "C) Das Modul läuft mit Priorität 1",
                    "D) iwlmvm ist das übergeordnete Modul",
                ],
                correct   = "B",
                explanation = "Die Zahl = Referenzzähler. 'Used by' zeigt welche anderen Module dieses Modul benötigen. Modul kann nur entladen werden wenn Referenzzähler = 0.",
            ),
        ],
        exam_tip   = "lsmod liest /proc/modules.\nModul kann nur entladen werden wenn 'Used by' = 0 (keine Abhängigkeiten).",
        memory_tip = "lsmod = List Modules. Used by-Zähler = wie oft in Benutzung.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.22",
        title       = "Module Info — modinfo",
        mtype       = "INFILTRATE",
        xp          = 35,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "DAEMON: Ein Modul ist mehr als ein Name.\n"
            "modinfo enthüllt alles: Autor, Lizenz, Parameter, Firmware.\n"
            "Welche Parameter akzeptiert e1000e? Was braucht nvidia?\n"
            "Kenn deine Module bevor du sie lädst."
        ),
        why_important = "modinfo zeigt Details zu Kernel-Modulen — Autor, Lizenz, Parameter, Firmware.",
        explanation = (
            "modinfo <modul> — Informationen über ein Kernel-Modul\n\n"
            "Ausgabe enthält:\n"
            "  filename   : Pfad zur .ko Datei\n"
            "  description: Was das Modul macht\n"
            "  license    : GPL / Proprietary\n"
            "  author     : Entwickler\n"
            "  depends    : Abhängige Module\n"
            "  firmware   : Benötigte Firmware-Dateien\n"
            "  parm       : Parameter (mit Beschreibung!)\n\n"
            "Parameter anzeigen:\n"
            "  modinfo -p i915     # Nur Parameter\n\n"
            "Parameter beim Laden setzen:\n"
            "  modprobe i915 enable_dc=1"
        ),
        syntax  = "modinfo <modul>\nmodinfo i915\nmodinfo -p usbcore    # Nur Parameter",
        example = (
            "$ modinfo i915\n"
            "filename: /lib/modules/6.1.0/kernel/drivers/gpu/drm/i915/i915.ko\n"
            "description: Intel Graphics\n"
            "license: GPL and additional rights\n"
            "author: Intel Corporation\n"
            "depends: drm_kms_helper,drm\n"
            "firmware: i915/skl_dmc_ver1_27.bin"
        ),
        task_description  = "Zeige Informationen über das i915 Grafik-Modul.",
        expected_commands = ["modinfo i915"],
        hint_text         = "modinfo i915 — i915 ist der Intel Grafik-Treiber",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welches Feld in modinfo zeigt die Parameter die beim Laden gesetzt werden können?",
                options   = ["A) depends", "B) parm", "C) options", "D) config"],
                correct   = "B",
                explanation = "parm (parameters) listet alle konfigurierbaren Modul-Parameter mit Typ-Angabe. Parameter werden mit modprobe <modul> param=wert gesetzt.",
            ),
        ],
        exam_tip   = "modinfo = Modul-Details. parm = Parameter.\nParameter-Persistenz: /etc/modprobe.d/<name>.conf",
        memory_tip = "modinfo <modul> = alles über ein Modul. parm = Parameter.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.23",
        title       = "Module laden/entladen — modprobe",
        mtype       = "INFILTRATE",
        xp          = 40,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "Module laden und entladen — das ist Macht.\n"
            "modprobe ist das richtige Tool: es kennt\n"
            "Abhängigkeiten und lädt sie automatisch."
        ),
        why_important = (
            "modprobe ist der Standard für Modul-Verwaltung.\n"
            "Es löst Abhängigkeiten auf — anders als insmod.\n"
            "LPIC-1 prüft modprobe, insmod und rmmod."
        ),
        explanation = (
            "Drei Tools für Module:\n\n"
            "  modprobe <modul>    : Lädt Modul + Abhängigkeiten\n"
            "                       (empfohlen!)\n\n"
            "  modprobe -r <modul> : Entlädt Modul + nicht mehr\n"
            "                       benötigte Abhängigkeiten\n\n"
            "  insmod <modul.ko>   : Lädt .ko Datei direkt\n"
            "                       (KEINE Abhängigkeitsauflösung)\n\n"
            "  rmmod <modul>       : Entlädt Modul\n"
            "                       (nur wenn Used by = 0)\n\n"
            "Konfiguration:\n"
            "  /etc/modprobe.d/    : Konfigurationsordner\n"
            "  /etc/modprobe.conf  : (veraltet)\n\n"
            "Module beim Boot laden:\n"
            "  /etc/modules        : Modul-Namen zeilenweise\n"
            "  /etc/modules-load.d/"
        ),
        syntax  = (
            "modprobe <modul>       # laden\n"
            "modprobe -r <modul>    # entladen\n"
            "insmod /pfad/modul.ko  # direkt laden\n"
            "rmmod <modul>          # entladen"
        ),
        example = (
            "$ modprobe usbcore    # (bereits geladen, kein Output)\n"
            "$ modprobe -r dummy   # dummy-Modul entladen\n"
            "$ rmmod usbcore\n"
            "rmmod: ERROR: Module usbcore is in use by: usbhid xhci_hcd"
        ),
        task_description  = "Versuche das usbcore-Modul zu laden.",
        expected_commands = ["modprobe usbcore"],
        hint_text         = "modprobe usbcore — usbcore ist das USB-Basis-Modul",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was ist der Unterschied zwischen modprobe und insmod?",
                options   = [
                    "A) insmod ist neuer und ersetzt modprobe",
                    "B) modprobe löst Abhängigkeiten auf, insmod lädt nur die direkte .ko Datei",
                    "C) modprobe braucht root, insmod nicht",
                    "D) insmod lädt Module aus dem Internet",
                ],
                correct   = "B",
                explanation = "modprobe löst Abhängigkeiten automatisch auf (liest depmod-Datenbank). insmod lädt nur die explizit angegebene .ko Datei — Dependencies müssen vorher manuell geladen werden.",
            ),
            QuizQuestion(
                question  = "In welcher Datei/Ordner konfigurierst du permanente modprobe-Optionen?",
                options   = [
                    "A) /etc/modules.conf",
                    "B) /etc/modprobe.d/",
                    "C) /boot/modprobe.cfg",
                    "D) /lib/modules/config",
                ],
                correct   = "B",
                explanation = "/etc/modprobe.d/ enthält .conf Dateien mit Modul-Optionen, Blacklists und Aliases. Beispiel: options i915 enable_dc=1",
            ),
        ],
        exam_tip   = "LPIC-1 Frage: 'Welches Tool löst Modul-Abhängigkeiten auf?'\nAntwort: modprobe (nicht insmod!)\n\nmodprobe -r = remove (mit Deps).",
        memory_tip = "modprobe = Module + Dependencies. insmod = nur die Datei.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.24",
        title       = "Module Config — /etc/modprobe.d/",
        mtype       = "DECODE",
        xp          = 35,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "DAEMON: modprobe lädt — aber nur einmalig.\n"
            "Für Dauerhaftigkeit schreibst du nach /etc/modprobe.d/.\n"
            "blacklist, options, alias — die drei Konfigurationstypen.\n"
            "Kontrolliere welche Module starten. Und welche nie."
        ),
        why_important = (
            "Permanente Modul-Konfiguration läuft über /etc/modprobe.d/.\n"
            "Blacklisting, Parameter, Aliases — alles hier."
        ),
        explanation = (
            "/etc/modprobe.d/ — Modul-Konfigurationsverzeichnis\n\n"
            "Dateien: *.conf (beliebiger Name)\n\n"
            "Direktiven:\n"
            "  options <modul> <param>=<wert>\n"
            "    → Modul-Parameter setzen\n"
            "    Beispiel: options snd-hda-intel model=generic\n\n"
            "  blacklist <modul>\n"
            "    → Modul NICHT laden (auch wenn Hardware erkannt)\n"
            "    Häufig für Treiber-Konflikte\n"
            "    Beispiel: blacklist nouveau  (Nvidia Open-Source)\n\n"
            "  alias <alias> <modul>\n"
            "    → Alternativen Namen definieren\n\n"
            "  install <modul> <befehl>\n"
            "    → Beim Laden diesen Befehl ausführen\n\n"
            "Blacklist greift erst nach initramfs-Update!"
        ),
        syntax  = (
            "# /etc/modprobe.d/myconfig.conf\n"
            "options snd-hda-intel model=generic\n"
            "blacklist nouveau\n"
            "alias net-pf-10 off    # IPv6 deaktivieren (alt)\n"
        ),
        example = (
            "$ cat /etc/modprobe.d/blacklist-nouveau.conf\n"
            "blacklist nouveau\n"
            "options nouveau modeset=0"
        ),
        task_description  = "Zeige die Modul-Konfigurationsdateien in /etc/modprobe.d/.",
        expected_commands = ["ls /etc/modprobe.d/"],
        hint_text         = "ls /etc/modprobe.d/ — zeigt vorhandene Konfig-Dateien",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was bewirkt 'blacklist <modul>' in /etc/modprobe.d/?",
                options   = [
                    "A) Das Modul wird sofort entladen",
                    "B) Das Modul wird nicht automatisch geladen, auch wenn die Hardware erkannt wird",
                    "C) Das Modul wird für alle User gesperrt",
                    "D) Das Modul wird aus /lib/modules/ gelöscht",
                ],
                correct   = "B",
                explanation = "blacklist verhindert dass modprobe das Modul automatisch lädt. Es kann aber noch manuell mit 'modprobe -f' oder explizitem Laden erzwungen werden.",
            ),
        ],
        exam_tip   = "Blacklist in /etc/modprobe.d/ greift nach:\n1. Datei erstellen\n2. update-initramfs -u ausführen\n3. Reboot\nOhne initramfs-Update kann das Modul beim Boot noch geladen werden!",
        memory_tip = "blacklist = Modul sperren. /etc/modprobe.d/*.conf für alle Konfiguration.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.25",
        title       = "SysFS Explorer — /sys/ Verzeichnis",
        mtype       = "SCAN",
        xp          = 30,
        chapter     = 1,
        speaker     = "LYRA-7",
        story       = (
            "sysfs ist eine direkte Verbindung zum Kernel.\n"
            "Kein Prozess, keine Datei — reiner Kernel-Zustand.\n"
            "Ich lebe hier. Komm rein."
        ),
        why_important = (
            "/sys/ ist das moderne Interface zur Kernel-internen Hierarchie.\n"
            "Für Automatisierung, Geräteverwaltung und erweiterte Diagnose."
        ),
        explanation = (
            "/sys/ — sysfs: Kernel-Gerätehierarchie\n\n"
            "Wichtige Unterverzeichnisse:\n"
            "  /sys/block/          : Block-Devices (Disks)\n"
            "  /sys/bus/            : Bus-Systeme (pci/usb/i2c)\n"
            "  /sys/class/          : Geräteklassen (net/block/input)\n"
            "  /sys/devices/        : Alle Geräte (Baumstruktur)\n"
            "  /sys/firmware/       : Firmware-Infos (UEFI/ACPI)\n"
            "  /sys/module/         : Geladene Kernel-Module\n"
            "  /sys/power/          : Power-Management\n\n"
            "Lesen und Schreiben:\n"
            "  cat /sys/class/net/eth0/speed   # NIC-Speed\n"
            "  echo 1 > /sys/class/leds/.../brightness  # LED"
        ),
        syntax  = "ls /sys/\nls /sys/class/net/     # Netzwerk-Interfaces\ncat /sys/class/net/eth0/speed",
        example = (
            "$ ls /sys/\n"
            "block  bus  class  dev  devices  firmware  fs\n"
            "hypervisor  kernel  module  power\n\n"
            "$ ls /sys/class/net/\n"
            "enp0s3  lo  wlan0"
        ),
        task_description  = "Erkunde das /sys/ Verzeichnis.",
        expected_commands = ["ls /sys"],
        hint_text         = "ls /sys",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was ist /sys/ in Linux?",
                options   = [
                    "A) Ein Verzeichnis für System-Binaries",
                    "B) Ein virtuelles Dateisystem (sysfs) das die Kernel-Gerätehierarchie abbildet",
                    "C) Das Backup-Verzeichnis für Systemdateien",
                    "D) Das Verzeichnis für System-Logs",
                ],
                correct   = "B",
                explanation = "sysfs ist ein pseudo-Dateisystem (wie /proc/) das zur Laufzeit vom Kernel generiert wird. Es stellt die interne Gerätehierarchie als Dateisystem dar.",
            ),
        ],
        exam_tip   = "/proc/ vs /sys/:\n/proc = Prozesse + Kernel-Parameter (älter)\n/sys  = Gerätehierarchie + sysfs (neuer, strukturierter)",
        memory_tip = "/sys/ = sysfs. Kernel-Gerätehierarchie. Lesen UND Schreiben möglich.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.26",
        title       = "DevFS Map — /dev/ Gerätedateien",
        mtype       = "SCAN",
        xp          = 30,
        chapter     = 1,
        speaker     = "DAEMON",
        story       = (
            "DAEMON: /dev/ — das Verzeichnis das alles enthält.\n"
            "/dev/sda ist deine Festplatte. /dev/null verschluckt Daten.\n"
            "/dev/random generiert Rauschen. /dev/tty ist dein Terminal.\n"
            "Alles ist eine Datei. Lern den Unterschied zwischen Block und Char."
        ),
        why_important = (
            "In Unix/Linux IST ALLES eine Datei — auch Hardware.\n"
            "/dev/ enthält Gerätedateien die Hardware repräsentieren."
        ),
        explanation = (
            "/dev/ — Device Filesystem\n\n"
            "Gerätedatei-Typen:\n"
            "  b (block)  — wahlfreier Zugriff (Disks)\n"
            "               /dev/sda, /dev/nvme0n1\n\n"
            "  c (char)   — sequenzieller Zugriff (Terminals, Serial)\n"
            "               /dev/tty, /dev/console, /dev/random\n\n"
            "Wichtige Gerätedateien:\n"
            "  /dev/sda           — erste SATA/SCSI Disk\n"
            "  /dev/nvme0n1       — erste NVMe SSD\n"
            "  /dev/vda           — erste virtuelle Disk (VM)\n"
            "  /dev/tty           — aktuelles Terminal\n"
            "  /dev/ttyS0         — erste serielle Schnittstelle\n"
            "  /dev/null          — Bit-Bucket (schluckt alles)\n"
            "  /dev/zero          — liefert endlose Null-Bytes\n"
            "  /dev/random        — echter Zufallsgenerator\n"
            "  /dev/urandom       — schnellerer Pseudozufall\n"
            "  /dev/stdin/stdout/stderr — Standard-Streams\n"
            "  /dev/loop0         — Loop-Device für Images\n"
            "  /dev/mapper/       — Device Mapper (LVM/LUKS)"
        ),
        syntax  = "ls /dev/           # Alle Gerätedateien\nls -l /dev/sda     # Details\nls -l /dev/null    # c = char device",
        example = (
            "$ ls -l /dev/sda /dev/null /dev/random\n"
            "brw-rw---- 1 root disk 8,0 /dev/sda\n"
            "crw-rw-rw- 1 root root 1,3 /dev/null\n"
            "crw-rw-rw- 1 root root 1,8 /dev/random\n"
            "│                    ───┬──\n"
            "│                       └── Major:Minor\n"
            "└── b=block, c=char"
        ),
        task_description  = "Erkunde das /dev/ Verzeichnis.",
        expected_commands = ["ls /dev"],
        hint_text         = "ls /dev",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was ist /dev/null?",
                options   = [
                    "A) Ein Fehler-Log",
                    "B) Das Null-Device — alles was hineingeschrieben wird, verschwindet",
                    "C) Eine leere Datei",
                    "D) Das Standard-Input-Device",
                ],
                correct   = "B",
                explanation = "/dev/null ist das 'schwarze Loch' — output dorthin umleiten verwirft ihn: cmd > /dev/null 2>&1",
            ),
            QuizQuestion(
                question  = "Was ist der Unterschied zwischen einem block device und einem char device?",
                options   = [
                    "A) Block devices sind größer als char devices",
                    "B) Block devices erlauben wahlfreien Zugriff (Disks), char devices sequenziellen (Terminals, Serial)",
                    "C) Char devices gehören dem User, Block devices dem Root",
                    "D) Kein Unterschied, nur historisch bedingte Namensgebung",
                ],
                correct   = "B",
                explanation = "Block devices: Daten in Blöcken, wahlfreier Zugriff (Disks, Partitionen). Char devices: Byte für Byte sequenziell (Terminals, Maus, Serial-Port).",
            ),
        ],
        exam_tip   = "/dev/ enthält:\n'b' = block device (Disk)\n'c' = char device (Terminal, /dev/null)\nMajor:Minor Nummern identifizieren den Treiber:Gerät.",
        memory_tip = "/dev/ = Gerätedateien. b=block, c=char. /dev/null = alles verschwindet.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.27",
        title       = "coldplug vs hotplug — udev Konzept",
        mtype       = "SCAN",
        xp          = 25,
        chapter     = 1,
        speaker     = "LYRA-7",
        story       = (
            "LYRA-7: Zwei Konzepte. Ein wichtiger Unterschied.\n"
            "Coldplug: das Gerät muss beim Boot bereits angesteckt sein.\n"
            "Hotplug: du steckst es während des Betriebs an — udev reagiert sofort.\n"
            "Die Prüfung fragt welche Geräte welches Modell nutzen."
        ),
        why_important = "LPIC-1 fragt nach dem Unterschied zwischen coldplug und hotplug Geräten.",
        explanation = (
            "Plug-Konzepte:\n\n"
            "  coldplug\n"
            "  ─────────\n"
            "  Gerät war beim Start SCHON verbunden.\n"
            "  Kernel erkennt es während des Boot-Prozesses.\n"
            "  Beispiel: eingebaute Festplatte, RAM\n\n"
            "  hotplug\n"
            "  ────────\n"
            "  Gerät wird WÄHREND des Betriebs verbunden.\n"
            "  Kernel sendet uevent an udev.\n"
            "  udev lädt Treiber + erstellt /dev/ Eintrag.\n"
            "  Beispiel: USB-Stick, externe Festplatte\n\n"
            "udev-Regeln bestimmen:\n"
            "  Welcher Name wird gegeben? (/dev/disk/by-id/...)\n"
            "  Welcher Treiber geladen?\n"
            "  Welche Rechte?\n"
            "  Welches Script ausgeführt?"
        ),
        syntax  = (
            "# udev-Regeln liegen in:\n"
            "ls /etc/udev/rules.d/         # Eigene Regeln\n"
            "ls /lib/udev/rules.d/          # System-Regeln\n"
            "udevadm monitor                # Live-Events"
        ),
        example = (
            "$ udevadm monitor\n"
            "monitor: listening on kernel and udev\n"
            "[USB einstecken]\n"
            "KERNEL[4.567] add    /devices/.../usb1/1-1 (usb)\n"
            "UDEV  [4.589] add    /devices/.../usb1/1-1 (usb)\n"
            "UDEV  [4.601] add    /block/sdb (block)"
        ),
        task_description  = "Erkunde die udev-Regeln in /etc/udev/rules.d/.",
        expected_commands = ["ls /etc/udev/rules.d/"],
        hint_text         = "ls /etc/udev/rules.d/",
        quiz_questions    = [
            QuizQuestion(
                question  = "Was ist der Unterschied zwischen coldplug und hotplug?",
                options   = [
                    "A) coldplug ist schneller als hotplug",
                    "B) coldplug = beim Boot schon da; hotplug = während Betrieb eingesteckt",
                    "C) coldplug = USB, hotplug = PCI",
                    "D) coldplug braucht udev, hotplug nicht",
                ],
                correct   = "B",
                explanation = "coldplug: Gerät war beim Boot schon verbunden (Festplatte, RAM). hotplug: wird während des Betriebs verbunden (USB) — udev reagiert auf uevent.",
            ),
        ],
        exam_tip   = "LPIC-1 Stichwörter: coldplug/hotplug, udev, uevent.\nudev-Regeln in /etc/udev/rules.d/ und /lib/udev/rules.d/.",
        memory_tip = "cold = beim Boot da. hot = im Betrieb eingesteckt → udev reagiert.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.28",
        title       = "Prüfungsfalle: IRQ 14",
        mtype       = "QUIZ",
        xp          = 25,
        chapter     = 1,
        speaker     = "KERNEL-ORAKEL",
        story       = (
            "Das Orakel spricht.\n"
            "IRQ 14 — eine Frage die im Examen erscheint.\n"
            "Beweise dass du die Antwort kennst."
        ),
        why_important = "IRQ-Nummern sind klassisches LPIC-1 Prüfungswissen. IRQ 14 = Primary IDE ist eine typische Exam-Falle.",
        quiz_questions = [
            QuizQuestion(
                question  = "Welchem klassischen Gerät ist IRQ 14 traditionell zugewiesen?",
                options   = [
                    "A) USB Controller",
                    "B) Primary IDE Controller (ATA/HDD)",
                    "C) Netzwerkkarte",
                    "D) Sound-Karte",
                ],
                correct   = "B",
                explanation = "IRQ 14 war klassisch dem Primary IDE/ATA Controller zugewiesen (für /dev/hda, /dev/hdb). IRQ 15 war Secondary IDE. Auf modernen SATA/NVMe-Systemen weitgehend obsolet, aber LPIC-1 fragt es.",
                xp_value  = 20,
            ),
            QuizQuestion(
                question  = "Was zeigt 'cat /proc/interrupts' an?",
                options   = [
                    "A) IRQ-Nummern, Zähler pro CPU und Gerätename",
                    "B) Nur die IRQ-Nummern",
                    "C) Alle Kernel-Interrupts als Baumstruktur",
                    "D) Interrupt-Service-Routinen im Kernel-Code",
                ],
                correct   = "A",
                explanation = "/proc/interrupts zeigt: IRQ-Nummer, Interrupt-Zähler pro CPU-Kern, Interrupt-Typ und Gerätename.",
                xp_value  = 20,
            ),
        ],
        exam_tip   = "IRQ 14 = Primary IDE. IRQ 15 = Secondary IDE.\nDiese Zuweisungen sind historisch aus der PC/AT-Architektur.",
        memory_tip = "14 = Primary IDE (Haupt-Festplattenkanal). 15 = Secondary.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.29",
        title       = "Prüfungsfalle: sda vs nvme vs vda",
        mtype       = "QUIZ",
        xp          = 25,
        chapter     = 1,
        speaker     = "KERNEL-ORAKEL",
        story       = (
            "Device-Naming ist eine häufige Prüfungsfalle.\n"
            "Kennst du den Unterschied zwischen sda, nvme0n1 und vda?"
        ),
        why_important = "Device-Naming (/dev/sda, /dev/nvme0n1, /dev/vda) ist fundamentales LPIC-1-Wissen für Partitionierung und Troubleshooting.",
        quiz_questions = [
            QuizQuestion(
                question  = "Welches Device-Präfix bezeichnet eine NVMe-SSD?",
                options   = ["A) /dev/sda", "B) /dev/hda", "C) /dev/nvme0n1", "D) /dev/vda"],
                correct   = "C",
                explanation = "/dev/nvme0n1 = erste NVMe SSD (NVMe 0, Namespace 1). /dev/sda = SATA/SCSI. /dev/hda = alte IDE (veraltet). /dev/vda = virtuelle Disk (KVM/QEMU).",
                xp_value  = 20,
            ),
            QuizQuestion(
                question  = "Was bedeutet /dev/sdb2?",
                options   = [
                    "A) Zweite Disk, zweite Partition",
                    "B) Zweite Partition der ersten Disk",
                    "C) System-Disk Backup, Partition 2",
                    "D) Serial-Bus-Device Nummer 2",
                ],
                correct   = "A",
                explanation = "sdb = zweite SCSI/SATA-Disk (a=erste, b=zweite, ...). 2 = zweite Partition auf dieser Disk.",
                xp_value  = 20,
            ),
            QuizQuestion(
                question  = "Welches Device wird für virtuelle Disks in KVM-VMs typischerweise verwendet?",
                options   = ["A) /dev/sda", "B) /dev/xda", "C) /dev/vda", "D) /dev/kda"],
                correct   = "C",
                explanation = "/dev/vda ist das virtio-Block-Device für KVM/QEMU VMs. Es ist performanter als emuliertes /dev/sda in VMs.",
                xp_value  = 15,
            ),
        ],
        exam_tip   = "Device-Namen:\nsda/sdb/sdc = SATA/SCSI (nach Erkennungsreihenfolge)\nnvme0n1    = NVMe SSD\nvda/vdb    = virtio (KVM)\nhda        = IDE (veraltet)\nloop0      = Loop-Device",
        memory_tip = "sda=SATA, nvme0n1=NVMe, vda=VM, hda=IDE(alt).",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.30",
        title       = "hwinfo — erweitertes Hardware-Tool",
        mtype       = "INFILTRATE",
        xp          = 30,
        chapter     = 1,
        speaker     = "SYSTEM",
        story       = (
            "SYSTEM: hwinfo — der tiefste Scan den du bekommen kannst.\n"
            "Nicht auf allen Distros vorinstalliert, aber mächtig.\n"
            "hwinfo --short gibt dir die Kurzfassung.\n"
            "hwinfo --disk geht tiefer. Kenn deine Werkzeuge."
        ),
        why_important = "hwinfo ist ein weiteres umfassendes Hardware-Tool, auf manchen Distros vorhanden.",
        explanation = (
            "hwinfo — Hardware Information Tool\n"
            "(nicht überall vorinstalliert, aber nützlich)\n\n"
            "  hwinfo --short     : Kompaktübersicht\n"
            "  hwinfo --cpu       : CPU-Details\n"
            "  hwinfo --disk      : Disk-Details\n"
            "  hwinfo --network   : Netzwerkkarten\n"
            "  hwinfo --usb       : USB-Geräte\n"
            "  hwinfo --pci       : PCI-Geräte\n\n"
            "Ähnlich wie lshw, aber andere Ausgabe-Struktur."
        ),
        syntax  = "hwinfo --short\nhwinfo --disk\nhwinfo --cpu",
        example = "$ hwinfo --short | head -20\nCPU: Intel Core i7-8550U\nDisk: /dev/nvme0n1, 512 GB\nNIC: Intel Wireless 8265",
        task_description  = "Versuche hwinfo --short auszuführen.",
        expected_commands = ["hwinfo --short", "hwinfo"],
        hint_text         = "hwinfo --short",
        quiz_questions    = [
            QuizQuestion(
                question  = "Welche zwei Tools geben ähnliche vollständige Hardware-Übersichten?",
                options   = [
                    "A) lspci und lsusb",
                    "B) lshw und hwinfo",
                    "C) dmesg und journalctl",
                    "D) dmidecode und blkid",
                ],
                correct   = "B",
                explanation = "lshw und hwinfo sind beide vollständige Hardware-Inventarisierungs-Tools. lshw ist häufiger vorinstalliert.",
            ),
        ],
        exam_tip   = "hwinfo ist kein LPIC-Standardtool, aber reale Distros (openSUSE) nutzen es.",
        memory_tip = "hwinfo ≈ lshw. --short für kompakte Ausgabe.",
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # BOSS FIGHT
    # ─────────────────────────────────────────────────────────────────────────
    Mission(
        mission_id  = "1.BOSS",
        title       = "BOSS: BIOS Overlord",
        mtype       = "BOSS",
        xp          = 200,
        chapter     = 1,
        speaker     = "ZARA Z3R0",
        boss_name   = "BIOS OVERLORD — Hardware Guardian",
        boss_desc   = "Ein dreistufiger Hardware-Angriff. Zeig was du kannst.",
        ascii_art   = """
  ██████╗ ██╗ ██████╗ ███████╗      ██████╗ ██╗   ██╗███████╗██████╗ ██╗      ██████╗ ██████╗ ██████╗
  ██╔══██╗██║██╔═══██╗██╔════╝     ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
  ██████╔╝██║██║   ██║███████╗     ██║   ██║██║   ██║█████╗  ██████╔╝██║     ██║   ██║██████╔╝██║  ██║
  ██╔══██╗██║██║   ██║╚════██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██╗██║  ██║
  ██████╔╝██║╚██████╔╝███████║     ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████╗╚██████╔╝██║  ██║██████╔╝
  ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝      ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝

  ┌─ HARDWARE INTERFACE LOCKED ──────────────────────────────────────────────────────────────────────┐
  │  > lspci -k        BLOCKED                                                                       │
  │  > lsmod           BLOCKED                                                                       │
  │  > /proc/cpuinfo   ENCRYPTED                                                                     │
  └──────────────────────────────────────────────────────────────────────────────────────────────────┘

                          ⚡ CHAOSWERK FACTION :: CHAPTER 1 BOSS ⚡""",
        story_transitions = [
            "BIOS OVERLORD rotiert seine Energieschilde. Dein Scan beginnt.",
            "lspci zeigt PCI-Busse. Der Overlord korrumpiert sie in Echtzeit.",
            "Jedes Modul ist eine Waffe. Lade das richtige.",
            "Letzte Phase. Hardware-Speicher wird gelöscht. Beeil dich.",
        ],
        why_important = "Der Boss-Kampf testet alle Hardware-Kenntnisse aus Kapitel 1: PCI-Geräte, Kernel-Module und /proc — alle drei sind LPIC-1-Prüfungsstoff.",
        story       = (
            "Der BIOS Overlord hat das Hardware-Interface gesperrt.\n"
            "Drei Phasen. Kein Fehler erlaubt.\n\n"
            "PHASE 1: Hardware scannen\n"
            "PHASE 2: Kernel-Module analysieren\n"
            "PHASE 3: /proc Dateien auslesen\n\n"
            "Z3R0: 'Wenn du das schaffst, gehörst du zu uns.'"
        ),
        task_description = (
            "Zeige alle PCI-Geräte mit Kernel-Treiber."
            "||"
            "Liste alle geladenen Kernel-Module auf."
            "||"
            "Zeige CPU-Details aus /proc/cpuinfo."
        ),
        expected_commands = ["lspci -k", "lsmod", "cat /proc/cpuinfo"],
        hints = [
            "Du brauchst drei Befehle für die drei Phasen: PCI-Geräte, Kernel-Module und /proc-Dateien.",
            "Versuche: lspci -k (Phase 1), lsmod (Phase 2), cat /proc/cpuinfo (Phase 3)",
            "Der vollständige Befehl: lspci -k && lsmod && cat /proc/cpuinfo",
        ],
        quiz_questions = [
            QuizQuestion(
                question  = "Du findest eine Grafikkarte im System. Welcher Befehl zeigt dir den aktiven Kernel-Treiber?",
                options   = ["A) lsmod -gpu", "B) lspci -k", "C) modinfo gpu", "D) cat /proc/gpu"],
                correct   = "B",
                explanation = "lspci -k zeigt 'Kernel driver in use: <name>' für jedes PCI-Gerät.",
                xp_value  = 20,
            ),
            QuizQuestion(
                question  = "Ein Kernel-Modul zeigt 'Used by: 3'. Was bedeutet das?",
                options   = [
                    "A) Das Modul wurde 3x gestartet",
                    "B) 3 andere Module oder Prozesse benötigen es — es kann nicht entladen werden",
                    "C) Das Modul hat 3 Fehler",
                    "D) Das Modul belegt 3 IRQs",
                ],
                correct   = "B",
                explanation = "Used by > 0 bedeutet: das Modul wird von anderen Modulen/Geräten genutzt. rmmod schlägt fehl bis alle Abhängigkeiten entladen sind.",
                xp_value  = 20,
            ),
            QuizQuestion(
                question  = "Welche DREI /proc Dateien zeigen Hardware-Ressourcen?",
                options   = [
                    "A) /proc/hardware, /proc/devices, /proc/memory",
                    "B) /proc/interrupts, /proc/ioports, /proc/iomem",
                    "C) /proc/cpuinfo, /proc/meminfo, /proc/diskinfo",
                    "D) /proc/irq, /proc/ports, /proc/mem",
                ],
                correct   = "B",
                explanation = "Das klassische LPIC-1 Trio: /proc/interrupts (IRQs), /proc/ioports (I/O-Adressen), /proc/iomem (Speicherbereiche).",
                xp_value  = 25,
            ),
            QuizQuestion(
                question  = "Wie erkennst du ob ein Linux-System im UEFI-Modus bootet?",
                options   = [
                    "A) Durch eficheck -mode",
                    "B) Wenn /sys/firmware/efi/ existiert",
                    "C) Wenn /boot/grub2/ vorhanden ist",
                    "D) Durch cat /proc/bootmode",
                ],
                correct   = "B",
                explanation = "[ -d /sys/firmware/efi ] — wenn dieses Verzeichnis existiert, ist das System im UEFI-Modus gebootet.",
                xp_value  = 20,
            ),
            QuizQuestion(
                question  = "Was ist der Unterschied zwischen lspci und lsusb -v?",
                options   = [
                    "A) lspci zeigt PCI-Geräte, lsusb -v zeigt USB-Geräte mit ausführlichen Details",
                    "B) lspci zeigt USB, lsusb zeigt PCI",
                    "C) Beide zeigen identische Informationen",
                    "D) lsusb -v braucht Root, lspci nicht",
                ],
                correct   = "A",
                explanation = "lspci = PCI/PCIe-Bus (Grafik, Netz, SATA). lsusb = USB-Geräte. -v = verbose (Hersteller-IDs, Klassen, Protokolle). Beide kommen aus dem Paket pciutils/usbutils.",
                xp_value  = 25,
            ),
        ],
        exam_tip   = (
            "KAPITEL 1 — Zusammenfassung für LPIC-1:\n"
            "lspci -k : PCI + Treiber\n"
            "lsusb -t : USB-Baum\n"
            "lsmod    : Module\n"
            "modprobe : Module laden (mit Deps)\n"
            "dmidecode: BIOS-Infos\n"
            "/proc/interrupts, /proc/ioports, /proc/iomem\n"
            "/sys/firmware/efi/ = UEFI-Check"
        ),
        gear_reward       = "hardware_scanner",
        faction_reward    = ("Kernel Syndicate", 10),
        memory_tip        = "BOSS besiegt! Du hast das Hardware-Level freigeschaltet.",
    ),
]
