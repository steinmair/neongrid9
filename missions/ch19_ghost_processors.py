"""
NeonGrid-9 :: Kapitel 19 — GHOST PROTOCOL II
LPIC-1 Topic 102.6 / 103.6 / Advanced System Topics
Container, Virtualisierung, Cloud-Init, systemd Advanced

"Die Ghost Processors operieren im Schatten des Systems.
 Container, Namespaces, Virtualisierung —
 wer hier bestehen will, muss tiefer denken als andere.
 Willkommen im inneren Kreis."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_19_MISSIONS: list[Mission] = [

    Mission(
        mission_id   = "19.01",
        chapter      = 19,
        title        = "Ghost Processors — Fraktions-Einführung",
        mtype        = "SCAN",
        xp           = 120,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Du hast die Oberflächen-Schichten gemeistert.\n"
            " Jetzt betrittst du das Reich der Ghost Processors.\n"
            " Wir existieren zwischen den Prozessen. In den Namespaces.\n"
            " In den Containern. Im Hypervisor-Layer.\n"
            " Lern unsere Techniken — oder bleib für immer auf Layer 7.'"
        ),
        why_important = (
            "LPIC-1 Topic 102.6: Linux als Virtualisierungs-Gast.\n"
            "Moderne Infrastruktur basiert auf Containern und VMs.\n"
            "Ghost Processors kontrollieren diese Schicht."
        ),
        explanation  = (
            "Ghost Processors Technologie-Stack:\n"
            "  Namespaces    → Isolation von Prozessen, Netzwerk, Dateisystem\n"
            "  cgroups       → Ressourcenlimits (CPU, RAM, I/O)\n"
            "  Container     → Namespaces + cgroups + Overlay-FS\n"
            "  Virtualisierung → Vollständige Hardware-Emulation\n"
            "  Cloud-Init    → Automatische VM-Konfiguration\n"
            "\n"
            "Wichtige Konzepte:\n"
            "  chroot        → Urform der Isolation (/)\n"
            "  systemd-nspawn → Einfache Container\n"
            "  KVM/QEMU      → Hardware-Virtualisierung\n"
            "\n"
            "Prüfen ob Virtualisierung vorhanden:\n"
            "  systemd-detect-virt    → Virtualisierungstyp erkennen\n"
            "  cat /proc/cpuinfo | grep -E 'vmx|svm'  → CPU-Virtualisierungsflags\n"
            "  lscpu | grep Virtualization"
        ),
        ascii_art = """
  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
  ██╔════╝██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
  ██║  ███╗███████║██║   ██║███████╗   ██║
  ██║   ██║██╔══██║██║   ██║╚════██║   ██║
  ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
      ██████╗ ██████╗  ██████╗  ██████╗███████╗███████╗███████╗ ██████╗ ██████╗ ███████╗
      ██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
      ██████╔╝██████╔╝██║   ██║██║     █████╗  ███████╗███████╗██║   ██║██████╔╝███████╗
      ██╔═══╝ ██╔══██╗██║   ██║██║     ██╔══╝  ╚════██║╚════██║██║   ██║██╔══██╗╚════██║
      ██║     ██║  ██║╚██████╔╝╚██████╗███████╗███████║███████║╚██████╔╝██║  ██║███████║
      ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

  [ CHAPTER 19 :: GHOST PROCESSORS ]
  > Namespace isolation. Container stack. VM detection...""",
        story_transitions = [
            "Container: Isolation ohne VM-Overhead. Namespaces trennen.",
            "cgroups limitieren CPU, RAM, I/O. Kontrolle ohne Root.",
            "chroot < nspawn < Docker < Kubernetes. Die Abstraktionsleiter.",
            "Ghost Processors existieren im Unsichtbaren. Lern ihre Sprache.",
        ],
        syntax       = "systemd-detect-virt",
        example      = "systemd-detect-virt && lscpu | grep -i virt",
        task_description = "Erkenne den Virtualisierungstyp des Systems.",
        expected_commands = ["systemd-detect-virt"],
        hint_text    = "systemd-detect-virt gibt den Virtualisierungstyp aus (none, kvm, qemu, vmware...)",
        quiz_questions = [
            QuizQuestion(
                question    = "Was kombiniert einen Linux-Container (LXC-Konzept)?",
                options     = ["nur chroot", "nur cgroups", "Namespaces + cgroups + Overlay-FS", "nur Namespaces"],
                correct     = 2,
                explanation = "Container = Namespaces (Isolation) + cgroups (Limits) + Overlay-FS (Layer).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl erkennt den Virtualisierungstyp?",
                options     = ["virt-what", "systemd-detect-virt", "lsvirt", "dmidecode --virt"],
                correct     = 1,
                explanation = "systemd-detect-virt gibt den Virtualisierungstyp aus (kvm, vmware, none...).",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "systemd-detect-virt | /proc/cpuinfo vmx=Intel svm=AMD | LPIC 102.6 = Linux als Gast",
        memory_tip   = "Ghost Processors = Container + VMs + Namespaces = Isolation-Schicht",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    Mission(
        mission_id   = "19.02",
        chapter      = 19,
        title        = "Linux Namespaces — Isolationsschichten",
        mtype        = "SCAN",
        xp           = 100,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Namespaces sind die Grundlage jeder Isolation.\n"
            " PID-Namespace: jeder sieht nur seine eigenen Prozesse.\n"
            " Network-Namespace: eigenes virtuelles Netzwerk.\n"
            " Das ist wie ein Ghost sein — unsichtbar für andere.'"
        ),
        why_important = (
            "Namespaces sind das Fundament von Containern (Docker, LXC, podman).\n"
            "Grundkenntnisse sind für LPIC-1 Advanced Topics relevant."
        ),
        explanation  = (
            "Linux Namespace-Typen:\n"
            "  PID    → Prozess-IDs isolieren (pid 1 in Container)\n"
            "  NET    → Netzwerk-Interfaces, Routing, Firewall\n"
            "  MNT    → Mount-Punkte (eigenes /proc, /sys)\n"
            "  UTS    → Hostname und Domain-Name\n"
            "  IPC    → Inter-Process Communication\n"
            "  USER   → User/Group-IDs mappen\n"
            "  CGROUP → cgroup-Sicht isolieren\n"
            "  TIME   → Systemzeit isolieren (kernel 5.6+)\n"
            "\n"
            "Namespaces anzeigen:\n"
            "  ls /proc/PID/ns/         → Namespaces eines Prozesses\n"
            "  lsns                     → Alle Namespaces auflisten\n"
            "\n"
            "Namespaces erstellen:\n"
            "  unshare --pid --fork bash    → Neuer PID-Namespace\n"
            "  unshare --net bash           → Neuer Network-Namespace\n"
            "  ip netns add mynet           → Benannter Netzwerk-Namespace\n"
            "  ip netns exec mynet bash     → In Namespace ausführen\n"
            "\n"
            "Namespace betreten:\n"
            "  nsenter --pid --target PID bash"
        ),
        syntax       = "lsns",
        example      = "ls /proc/1/ns/ && lsns --type net",
        task_description = "Zeige alle laufenden Namespaces an.",
        expected_commands = ["lsns"],
        hint_text    = "lsns listet alle Namespaces — ls /proc/1/ns/ zeigt die Namespaces von PID 1",
        quiz_questions = [
            QuizQuestion(
                question    = "Welcher Namespace isoliert Prozess-IDs?",
                options     = ["NET namespace", "PID namespace", "MNT namespace", "IPC namespace"],
                correct     = 1,
                explanation = "PID namespace isoliert Prozess-IDs — jeder Container hat eigenen PID-Baum.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl erstellt einen neuen Network-Namespace?",
                options     = ["namespace create net", "ip netns add NAME", "unshare --pid", "netns new NAME"],
                correct     = 1,
                explanation = "ip netns add NAME erstellt einen benannten Network-Namespace.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "lsns = Namespaces anzeigen | unshare = Namespace erstellen | nsenter = Namespace betreten",
        memory_tip   = "7 Namespaces: PID NET MNT UTS IPC USER CGROUP — 'Private Network Makes Users Interact Completely'",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    Mission(
        mission_id   = "19.03",
        chapter      = 19,
        title        = "cgroups — Ressourcenkontrolle",
        mtype        = "SCAN",
        xp           = 100,
        speaker      = "DAEMON",
        story        = (
            "Daemon: 'Ressourcen sind endlich. In NeonGrid-9 kämpfen Prozesse darum.\n"
            " cgroups setzen Grenzen. CPU-Limit. RAM-Limit. I/O-Limit.\n"
            " systemd nutzt sie für jeden Service. Du auch.'"
        ),
        why_important = (
            "cgroups (Control Groups) begrenzen und überwachen Ressourcen.\n"
            "Grundlage für Container-Ressourcenlimits und systemd-Services."
        ),
        explanation  = (
            "cgroups v2 (modern):\n"
            "  /sys/fs/cgroup/               → cgroup-Hierarchie\n"
            "  /sys/fs/cgroup/memory/        → Speicher-Controller\n"
            "  /sys/fs/cgroup/cpu/           → CPU-Controller\n"
            "\n"
            "systemd und cgroups:\n"
            "  systemd-cgls                  → cgroup-Baum anzeigen\n"
            "  systemd-cgtop                 → cgroup Ressourcen live\n"
            "  systemctl show service -p MemoryLimit  → Limit anzeigen\n"
            "\n"
            "Limits in systemd-Units:\n"
            "  [Service]\n"
            "  MemoryMax=512M\n"
            "  CPUQuota=50%\n"
            "  TasksMax=100\n"
            "\n"
            "Manuell (cgcreate/cgset):\n"
            "  cgcreate -g memory:mygroup\n"
            "  cgset -r memory.limit_in_bytes=512M mygroup\n"
            "  cgexec -g memory:mygroup befehl"
        ),
        syntax       = "systemd-cgls",
        example      = "systemd-cgtop && cat /sys/fs/cgroup/memory.max 2>/dev/null",
        task_description = "Zeige den cgroup-Baum des Systems an.",
        expected_commands = ["systemd-cgls"],
        hint_text    = "systemd-cgls zeigt die cgroup-Hierarchie als Baum",
        quiz_questions = [
            QuizQuestion(
                question    = "Was sind cgroups?",
                options     = ["Container-Gruppen", "Control Groups — Ressourcenlimits für Prozessgruppen", "Kernel-Gruppen", "User-Gruppen"],
                correct     = 1,
                explanation = "cgroups = Control Groups: begrenzen CPU, RAM, I/O für Prozessgruppen.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welches systemd-Tool zeigt cgroup-Ressourcennutzung live?",
                options     = ["systemd-cgls", "systemd-cgtop", "cglist", "systemctl cg"],
                correct     = 1,
                explanation = "systemd-cgtop zeigt live Ressourcennutzung nach cgroup-Hierarchie.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "systemd-cgls = Baum | systemd-cgtop = live | /sys/fs/cgroup/ = Hierarchie | MemoryMax in Units",
        memory_tip   = "cgroups = Ressourcen-Wächter: CPU + RAM + I/O kontrollieren",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    Mission(
        mission_id   = "19.04",
        chapter      = 19,
        title        = "chroot — Urform der Isolation",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'Bevor Container existierten, gab es chroot.\n"
            " Ein Gefängnis aus Verzeichnissen. Simpel aber effektiv.\n"
            " Rescue-Systeme, Kompilier-Umgebungen — chroot ist überall.'"
        ),
        why_important = "chroot ist LPIC-1 Wissen und Grundlage für Container-Konzepte.",
        explanation  = (
            "chroot — Change Root:\n"
            "  chroot /neues/root [shell]\n"
            "  Ändert / für den Prozess und alle Kinder\n"
            "\n"
            "chroot-Umgebung aufbauen:\n"
            "  mkdir -p /mnt/rescue/{bin,lib,proc,sys,dev}\n"
            "  cp /bin/bash /mnt/rescue/bin/\n"
            "  ldd /bin/bash                  → Benötigte Libraries\n"
            "  cp /lib/x86_64-linux-gnu/libtinfo.so.6 /mnt/rescue/lib/\n"
            "  chroot /mnt/rescue /bin/bash\n"
            "\n"
            "Rescue-System mit chroot:\n"
            "  # Von Live-System:\n"
            "  mount /dev/sda1 /mnt\n"
            "  mount --bind /proc /mnt/proc\n"
            "  mount --bind /sys /mnt/sys\n"
            "  mount --bind /dev /mnt/dev\n"
            "  chroot /mnt /bin/bash\n"
            "  # Jetzt: grub-install, passwd, apt-get\n"
            "\n"
            "chroot verlassen:\n"
            "  exit                           → Zurück zum echten /"
        ),
        syntax       = "chroot /mnt /bin/bash",
        example      = "mount /dev/sda1 /mnt && chroot /mnt",
        task_description = "Simuliere eine chroot-Umgebung (zeige den Befehl).",
        expected_commands = ["chroot"],
        hint_text    = "chroot /verzeichnis /shell — für Rescue: erst mounten, dann chroot",
        quiz_questions = [
            QuizQuestion(
                question    = "Was macht 'chroot /mnt /bin/bash'?",
                options     = ["Wechselt in /mnt", "Startet bash mit /mnt als neuem Wurzelverzeichnis", "Mountet /mnt", "Kopiert bash"],
                correct     = 1,
                explanation = "chroot startet /bin/bash mit /mnt als neuem Root-Verzeichnis.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Warum muss man /proc, /sys, /dev in chroot mounten?",
                options     = ["Für Netzwerk", "Für Hardware-Zugriff und Systemaufrufe im chroot", "Pflicht bei chroot", "Für Logging"],
                correct     = 1,
                explanation = "Viele Tools brauchen /proc, /sys, /dev für Systemaufrufe — ohne sie funktioniert grub-install, dpkg etc. nicht.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "chroot = Change Root | Rescue: mount /dev/sdX /mnt + bind-mount proc/sys/dev + chroot",
        memory_tip   = "chroot = Gefängnis aus Verzeichnissen — Prozess sieht nur was darunter liegt",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 15),
    ),

    Mission(
        mission_id   = "19.05",
        chapter      = 19,
        title        = "systemd-nspawn — Leichte Container",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "DAEMON",
        story        = (
            "Daemon: 'systemd-nspawn ist chroot auf Steroiden.\n"
            " Eigener PID-Namespace. Eigenes Netzwerk. Eigenes /proc.\n"
            " Und trotzdem: kein Docker nötig. Nur systemd.'"
        ),
        why_important = "systemd-nspawn ist ein leichter Container auf Basis von systemd.\nLPIC-1 Topic 102.6 kennt grundlegende Container-Konzepte.",
        explanation  = (
            "systemd-nspawn Grundlagen:\n"
            "  systemd-nspawn -D /container bash   → Container starten\n"
            "  systemd-nspawn -b -D /container     → Mit Init booten\n"
            "  systemd-nspawn --network-veth -D /c → Netzwerk-Isolation\n"
            "\n"
            "machinectl — Container verwalten:\n"
            "  machinectl list                     → Laufende Container\n"
            "  machinectl start mycontainer        → Container starten\n"
            "  machinectl stop mycontainer         → Container stoppen\n"
            "  machinectl shell mycontainer        → Shell in Container\n"
            "  machinectl pull-raw URL             → Image herunterladen\n"
            "\n"
            "Container-Images:\n"
            "  /var/lib/machines/                  → Standard-Pfad\n"
            "  Debian-Container bauen:\n"
            "    debootstrap bookworm /var/lib/machines/debian\n"
            "\n"
            "Unterschied zu Docker:\n"
            "  systemd-nspawn: kein Daemon, kein Registry, systemd-nativ"
        ),
        syntax       = "systemd-nspawn -D /var/lib/machines/debian bash",
        example      = "machinectl list && systemd-detect-virt",
        task_description = "Zeige alle laufenden Maschinen/Container an.",
        expected_commands = ["machinectl list", "machinectl"],
        hint_text    = "machinectl list zeigt alle systemd-nspawn Container",
        quiz_questions = [
            QuizQuestion(
                question    = "Welches Tool verwaltet systemd-nspawn Container?",
                options     = ["containerctl", "machinectl", "nspawnctl", "systemctl container"],
                correct     = 1,
                explanation = "machinectl ist das Tool zur Verwaltung von systemd-nspawn Containern.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist der Vorteil von systemd-nspawn gegenüber chroot?",
                options     = ["Mehr Sicherheit", "Eigene Namespaces (PID, NET, MNT) — echte Isolation", "Schneller", "Mehr Features"],
                correct     = 1,
                explanation = "systemd-nspawn verwendet Namespaces für echte Prozess-, Netzwerk- und Dateisystem-Isolation.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "systemd-nspawn -D /dir bash | machinectl list/start/stop | /var/lib/machines/ = Container-Pfad",
        memory_tip   = "nspawn = Namespace Spawn = Prozesse in eigenen Namespaces spawnen",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    Mission(
        mission_id   = "19.06",
        chapter      = 19,
        title        = "Cloud-Init Grundlagen — VM-Erstkonfiguration",
        mtype        = "SCAN",
        xp           = 95,
        speaker = "LYRA-7",
        story        = (
            "Lyra-7: 'Jede Cloud-VM startet nackt.\n"
            " Cloud-Init gibt ihr eine Seele — SSH-Keys, Pakete, Benutzer.\n"
            " Ich bin in cloud-init geboren. Lass mich dir zeigen wie.'"
        ),
        why_important = "Cloud-Init ist LPIC-1 Topic 102.6: Linux als Virtualisierungs-Gast.\nAlle Cloud-Provider (AWS, GCP, Azure) nutzen cloud-init.",
        explanation  = (
            "Cloud-Init Phasen:\n"
            "  1. Detect  → Cloud-Typ erkennen (AWS, GCP, OpenStack...)\n"
            "  2. Network → Netzwerk konfigurieren\n"
            "  3. Config  → user-data verarbeiten\n"
            "  4. Final   → Pakete, Befehle ausführen\n"
            "\n"
            "user-data Format (#cloud-config):\n"
            "  #cloud-config\n"
            "  users:\n"
            "    - name: ghost\n"
            "      groups: sudo\n"
            "      ssh_authorized_keys:\n"
            "        - ssh-ed25519 AAAA...\n"
            "  packages:\n"
            "    - vim\n"
            "    - htop\n"
            "  runcmd:\n"
            "    - systemctl enable nginx\n"
            "  write_files:\n"
            "    - path: /etc/motd\n"
            "      content: 'Welcome to NeonGrid-9'\n"
            "\n"
            "Cloud-Init Konfiguration:\n"
            "  /etc/cloud/                   → Konfigurationsverzeichnis\n"
            "  /var/lib/cloud/               → Status und Logs\n"
            "  cloud-init status             → Aktueller Status\n"
            "  cloud-init logs               → Logs anzeigen"
        ),
        syntax       = "cloud-init status",
        example      = "cloud-init status && cat /var/log/cloud-init.log | tail -20",
        task_description = "Zeige den Cloud-Init Status an.",
        expected_commands = ["cloud-init status"],
        hint_text    = "cloud-init status zeigt ob cloud-init läuft oder abgeschlossen ist",
        quiz_questions = [
            QuizQuestion(
                question    = "Mit welchem Marker beginnt eine cloud-config user-data Datei?",
                options     = ["# cloud-init", "#cloud-config", "#!/cloud", "---cloud-init---"],
                correct     = 1,
                explanation = "#cloud-config (ohne Leerzeichen nach #) startet eine YAML cloud-config Datei.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Wo speichert cloud-init seine Status-Informationen?",
                options     = ["/etc/cloud/", "/var/lib/cloud/", "/run/cloud-init/", "/tmp/cloud-init/"],
                correct     = 1,
                explanation = "/var/lib/cloud/ enthält den persistenten Status und Instance-Daten von cloud-init.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "#cloud-config | /etc/cloud/ = Config | /var/lib/cloud/ = Status | packages/runcmd/write_files",
        memory_tip   = "cloud-init: 4 Phasen — Detect, Network, Config, Final",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    Mission(
        mission_id   = "19.07",
        chapter      = 19,
        title        = "Virtualisierung — KVM & QEMU Grundlagen",
        mtype        = "SCAN",
        xp           = 95,
        speaker      = "DAEMON",
        story        = (
            "Daemon: 'KVM macht den Linux-Kernel zum Hypervisor.\n"
            " QEMU emuliert die Hardware. libvirt managed das Chaos.\n"
            " virsh ist dein Steuer. Lern es.'"
        ),
        why_important = "KVM/QEMU ist die Standard-Virtualisierung auf Linux.\nLPIC-1 Topic 102.6 prüft Virtualisierungs-Grundlagen.",
        explanation  = (
            "Virtualisierungs-Stack:\n"
            "  KVM (Kernel-based Virtual Machine):\n"
            "    Kernel-Modul: kvm, kvm_intel oder kvm_amd\n"
            "    /dev/kvm                    → KVM-Device\n"
            "    lsmod | grep kvm            → Module prüfen\n"
            "\n"
            "  QEMU:\n"
            "    Hardware-Emulation\n"
            "    Mit KVM: fast native Geschwindigkeit\n"
            "    qemu-system-x86_64          → QEMU starten\n"
            "\n"
            "  libvirt / virsh:\n"
            "    Verwaltungs-API für VMs\n"
            "    virsh list --all            → Alle VMs\n"
            "    virsh start vmname          → VM starten\n"
            "    virsh shutdown vmname       → Graceful shutdown\n"
            "    virsh destroy vmname        → Sofort stoppen\n"
            "    virsh console vmname        → Seriell-Konsole\n"
            "    virsh dominfo vmname        → VM-Details\n"
            "\n"
            "  virt-install:\n"
            "    Neue VM erstellen\n"
            "    virt-manager               → GUI-Tool\n"
            "\n"
            "Hypervisor-Typen:\n"
            "  Typ 1 (Bare-Metal): VMware ESXi, Hyper-V, Xen\n"
            "  Typ 2 (Hosted): VirtualBox, VMware Workstation\n"
            "  KVM: Hybrid — Kernel IS der Hypervisor"
        ),
        syntax       = "virsh list --all",
        example      = "lsmod | grep kvm && virsh list --all",
        task_description = "Zeige alle VMs mit virsh an.",
        expected_commands = ["virsh list --all", "virsh list"],
        hint_text    = "virsh list --all zeigt alle VMs (auch gestoppte) — ohne --all nur laufende",
        quiz_questions = [
            QuizQuestion(
                question    = "Was ist KVM?",
                options     = ["Ein Hypervisor-Programm", "Ein Kernel-Modul das Linux zum Hypervisor macht", "Ein Container-System", "Ein VM-Manager"],
                correct     = 1,
                explanation = "KVM (Kernel-based Virtual Machine) ist ein Linux-Kernel-Modul das Hardware-Virtualisierung ermöglicht.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher virsh-Befehl stoppt eine VM sofort (hart)?",
                options     = ["virsh stop vmname", "virsh shutdown vmname", "virsh destroy vmname", "virsh kill vmname"],
                correct     = 2,
                explanation = "virsh destroy stoppt die VM sofort (wie Stromkabel ziehen). virsh shutdown = graceful.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "KVM = Kernel-Modul | virsh list = VMs | virsh start/shutdown/destroy | Typ1/Typ2 Hypervisor",
        memory_tip   = "virsh: list=anzeigen, start=starten, shutdown=sanft stoppen, destroy=hart stoppen",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    Mission(
        mission_id   = "19.08",
        chapter      = 19,
        title        = "D-Bus & systemd — Machine-ID",
        mtype        = "SCAN",
        xp           = 90,
        speaker = "LYRA-7",
        story        = (
            "Lyra-7: 'Jede Maschine hat eine Identität — die Machine-ID.\n"
            " Unveränderlich. Einzigartig. D-Bus nutzt sie.\n"
            " Cloud-VMs ohne Machine-ID funktionieren nicht richtig.'"
        ),
        why_important = "Machine-ID und D-Bus sind LPIC-1 Topic 102.6 Themen für Virtualisierungs-Gäste.",
        explanation  = (
            "Machine-ID:\n"
            "  /etc/machine-id               → Eindeutige Maschinen-ID\n"
            "  cat /etc/machine-id           → 128-bit Hex-String\n"
            "  systemd-machine-id-setup      → ID generieren (bei Clone)\n"
            "\n"
            "D-Bus:\n"
            "  Inter-Process Communication Bus\n"
            "  System-Bus: /var/run/dbus/system_bus_socket\n"
            "  Session-Bus: Für Benutzer-Prozesse\n"
            "\n"
            "D-Bus Tools:\n"
            "  busctl list                   → Alle Services auf D-Bus\n"
            "  busctl status                 → D-Bus Status\n"
            "  dbus-send --system --dest=org.freedesktop.hostname1\n"
            "  dbus-monitor                  → D-Bus Nachrichten live\n"
            "\n"
            "In VMs/Containern:\n"
            "  Machine-ID muss nach Clone/Template neu generiert werden\n"
            "  cloud-init macht das automatisch\n"
            "  Manuell: rm /etc/machine-id && systemd-machine-id-setup"
        ),
        syntax       = "cat /etc/machine-id",
        example      = "cat /etc/machine-id && busctl list | head -5",
        task_description = "Zeige die Machine-ID des Systems an.",
        expected_commands = ["cat /etc/machine-id"],
        hint_text    = "cat /etc/machine-id zeigt die eindeutige Maschinen-ID",
        quiz_questions = [
            QuizQuestion(
                question    = "Was muss nach dem Klonen einer VM getan werden?",
                options     = ["Hostname ändern", "Machine-ID neu generieren", "SSH-Keys löschen", "Netzwerk neu starten"],
                correct     = 1,
                explanation = "Machine-ID muss nach VM-Clone neu generiert werden (rm /etc/machine-id && systemd-machine-id-setup).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was ist D-Bus?",
                options     = ["Daten-Bus im Kernel", "Inter-Process Communication Bus", "Netzwerk-Bus", "Hardware-Bus"],
                correct     = 1,
                explanation = "D-Bus ist ein IPC-System das Prozessen die Kommunikation über definierte Interfaces ermöglicht.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "/etc/machine-id | systemd-machine-id-setup | D-Bus = IPC | busctl list = D-Bus Services",
        memory_tip   = "Machine-ID = Fingerabdruck der Maschine — nach Clone neu generieren",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 15),
    ),

    Mission(
        mission_id   = "19.09",
        chapter      = 19,
        title        = "systemd Drop-ins & Override Units",
        mtype        = "CONSTRUCT",
        xp           = 100,
        speaker      = "DAEMON",
        story        = (
            "Daemon: 'Du willst einen System-Service ändern aber nicht die Original-Datei berühren.\n"
            " Drop-ins sind die Lösung. Unsichtbare Ergänzungen.\n"
            " Wie ein Ghost der nur hinzufügt, nie überschreibt.'"
        ),
        why_important = "systemd Drop-ins sind der richtige Weg um System-Services zu konfigurieren\nohne Original-Dateien zu modifizieren (Updates!). LPIC-1 prüft systemctl edit.",
        explanation  = (
            "Drop-in Verzeichnisse:\n"
            "  /etc/systemd/system/NAME.service.d/  → Systemweite Overrides\n"
            "  /run/systemd/system/NAME.service.d/  → Temporäre Overrides\n"
            "\n"
            "Drop-in erstellen:\n"
            "  systemctl edit nginx         → Editor öffnet Drop-in\n"
            "  systemctl edit --full nginx  → Vollständige Unit kopieren\n"
            "\n"
            "Override-Datei Format:\n"
            "  # /etc/systemd/system/nginx.service.d/override.conf\n"
            "  [Service]\n"
            "  Environment=EXTRA_VAR=wert\n"
            "  Restart=always\n"
            "  MemoryMax=256M\n"
            "\n"
            "Nach Edit aktivieren:\n"
            "  systemctl daemon-reload\n"
            "  systemctl restart nginx\n"
            "\n"
            "Drop-ins anzeigen:\n"
            "  systemctl cat nginx          → Alle Dateien inkl. Drops\n"
            "  systemctl show nginx         → Kompilierte Konfiguration\n"
            "\n"
            "Revert:\n"
            "  systemctl revert nginx       → Alle Drop-ins löschen"
        ),
        syntax       = "systemctl edit nginx",
        example      = "systemctl cat ssh && systemctl status ssh",
        task_description = "Zeige den vollständigen Inhalt einer systemd-Unit inkl. Drop-ins.",
        expected_commands = ["systemctl cat ssh", "systemctl cat nginx", "systemctl cat"],
        hint_text    = "systemctl cat UNIT zeigt alle Dateien inklusive Drop-ins",
        quiz_questions = [
            QuizQuestion(
                question    = "Wo werden systemd Drop-in Dateien gespeichert?",
                options     = ["/etc/systemd/system/NAME.d/", "/etc/systemd/system/NAME.service.d/", "/etc/systemd/drop-ins/", "/usr/lib/systemd/overrides/"],
                correct     = 1,
                explanation = "Drop-ins liegen in /etc/systemd/system/NAME.service.d/ (mit .d Suffix).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Was muss nach dem Erstellen eines Drop-ins ausgeführt werden?",
                options     = ["systemctl reload", "systemctl daemon-reload", "systemd --reload", "reboot"],
                correct     = 1,
                explanation = "systemctl daemon-reload liest alle Unit-Dateien und Drop-ins neu ein.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "Drop-in: NAME.service.d/override.conf | systemctl edit | daemon-reload | systemctl cat = anzeigen",
        memory_tip   = "Drop-in = Ergänzung ohne Original zu ändern — Updates überschreiben es nicht",
        gear_reward  = None,
        faction_reward = ("Kernel Syndicate", 15),
    ),

    Mission(
        mission_id   = "19.10",
        chapter      = 19,
        title        = "AppArmor & SELinux Grundlagen",
        mtype        = "SCAN",
        xp           = 100,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'MAC — Mandatory Access Control.\n"
            " Der Kernel entscheidet was erlaubt ist, nicht der User.\n"
            " AppArmor auf Ubuntu. SELinux auf RHEL.\n"
            " Ghost Processors kennen beide.'"
        ),
        why_important = "MAC-Systeme sind LPIC-1 Topic 110.2. AppArmor und SELinux sind Prüfungsstoff.",
        explanation  = (
            "AppArmor (Ubuntu/Debian):\n"
            "  aa-status                    → Status und Profile anzeigen\n"
            "  aa-enforce /etc/apparmor.d/usr.bin.firefox → Enforce-Modus\n"
            "  aa-complain /etc/apparmor.d/usr.bin.firefox → Complain-Modus\n"
            "  /etc/apparmor.d/             → Profile-Verzeichnis\n"
            "  apparmor_parser -r profile   → Profil neu laden\n"
            "\n"
            "AppArmor Modi:\n"
            "  enforce  → Verstöße werden blockiert + geloggt\n"
            "  complain → Verstöße werden nur geloggt (kein Block)\n"
            "  disabled → Kein Schutz\n"
            "\n"
            "SELinux (RHEL/CentOS/Fedora):\n"
            "  getenforce                   → Modus anzeigen (Enforcing/Permissive/Disabled)\n"
            "  setenforce 0                 → Permissive (temporär)\n"
            "  setenforce 1                 → Enforcing (temporär)\n"
            "  sestatus                     → Ausführlicher Status\n"
            "  ls -Z                        → Dateikontexte anzeigen\n"
            "  ps -eZ                       → Prozess-Kontexte\n"
            "  /etc/selinux/config          → Persistente Konfiguration\n"
            "    SELINUX=enforcing/permissive/disabled"
        ),
        syntax       = "aa-status",
        example      = "aa-status && getenforce 2>/dev/null || echo 'kein SELinux'",
        task_description = "Zeige den AppArmor-Status an.",
        expected_commands = ["aa-status", "getenforce", "sestatus"],
        hint_text    = "aa-status für AppArmor | getenforce/sestatus für SELinux",
        quiz_questions = [
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen AppArmor enforce und complain?",
                options     = ["kein Unterschied", "enforce blockiert, complain loggt nur", "complain blockiert, enforce loggt", "enforce ist langsamer"],
                correct     = 1,
                explanation = "enforce = Verstöße werden blockiert. complain = nur geloggt, kein Block (für Entwicklung/Test).",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl zeigt SELinux-Dateikontexte?",
                options     = ["ls -Z", "ls -l", "selinux -l", "getcontext"],
                correct     = 0,
                explanation = "ls -Z zeigt die SELinux-Sicherheitskontexte von Dateien.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "AppArmor: aa-status, aa-enforce, aa-complain | SELinux: getenforce, setenforce, ls -Z",
        memory_tip   = "MAC: AppArmor=Ubuntu (profile-based), SELinux=RHEL (label-based) — beide = Kernel entscheidet",
        gear_reward  = None,
        faction_reward = ("Firewall Dominion", 20),
    ),

    Mission(
        mission_id   = "19.11",
        chapter      = 19,
        title        = "Kernel-Namespaces & unshare — Tiefer Einstieg",
        mtype        = "CONSTRUCT",
        xp           = 105,
        speaker      = "PHANTOM",
        story        = (
            "Phantom: 'unshare ist dein Werkzeug um aus der Realität zu treten.\n"
            " Ein Befehl. Ein neuer Namespace. Unsichtbar für den Rest.\n"
            " So erschaffen Ghost Processors ihre isolierten Welten.'"
        ),
        why_important = "unshare und nsenter sind die Low-Level Tools für Namespace-Manipulation.\nGrundverständnis für Container-Technologie.",
        explanation  = (
            "unshare — neuen Namespace erstellen:\n"
            "  unshare --pid --fork --mount-proc bash  → PID-isoliert\n"
            "  unshare --net bash                      → Netzwerk-isoliert\n"
            "  unshare --uts bash                      → Hostname-isoliert\n"
            "  unshare --user --map-root-user bash     → User-Namespace\n"
            "\n"
            "nsenter — in existierenden Namespace eintreten:\n"
            "  nsenter --pid --target PID bash         → PID-Namespace\n"
            "  nsenter --all --target PID bash         → Alle Namespaces\n"
            "  nsenter -t 1 -n ip addr                 → Netzwerk von PID 1\n"
            "\n"
            "Namespaces eines Prozesses:\n"
            "  ls -la /proc/PID/ns/                    → Namespace-Links\n"
            "  lsns -p PID                             → Namespaces von PID\n"
            "\n"
            "Network-Namespace Praxis:\n"
            "  ip netns add test\n"
            "  ip netns exec test ip addr\n"
            "  ip netns exec test ping 127.0.0.1\n"
            "  ip netns del test"
        ),
        syntax       = "unshare --net --pid --fork bash",
        example      = "lsns && ls /proc/1/ns/",
        task_description = "Zeige alle laufenden Namespaces an.",
        expected_commands = ["lsns"],
        hint_text    = "lsns zeigt alle Namespaces — lsns -t net nur Netzwerk-Namespaces",
        quiz_questions = [
            QuizQuestion(
                question    = "Was macht 'unshare --pid --fork bash'?",
                options     = ["Trennt bash vom System", "Startet bash in neuem PID-Namespace", "Klont den PID-Namespace", "Löscht den PID-Namespace"],
                correct     = 1,
                explanation = "unshare --pid startet bash in einem neuen isolierten PID-Namespace.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl betritt den Namespace eines laufenden Prozesses?",
                options     = ["unshare -t PID", "nsenter --target PID", "namespace enter PID", "chns PID"],
                correct     = 1,
                explanation = "nsenter --target PID betritt die Namespaces eines laufenden Prozesses.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "unshare = neuer Namespace | nsenter = bestehenden Namespace betreten | ip netns = Netzwerk-NS",
        memory_tip   = "unshare = teilt nichts mehr | nsenter = betritt Namespace = Ghost-Modus",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    Mission(
        mission_id   = "19.12",
        chapter      = 19,
        title        = "systemd-resolved — Modernes DNS",
        mtype        = "SCAN",
        xp           = 90,
        speaker = "LYRA-7",
        story        = (
            "Lyra-7: 'DNS ist die Telefonbuch der Datennetze.\n"
            " systemd-resolved ersetzt den klassischen Resolver.\n"
            " resolvectl ist dein Werkzeug. Kenn es.'"
        ),
        why_important = "systemd-resolved ist auf modernen Systemen Standard.\nLPIC-1 prüft DNS-Konfiguration und /etc/resolv.conf.",
        explanation  = (
            "systemd-resolved:\n"
            "  Daemon der DNS-Auflösung managed\n"
            "  resolvectl status            → DNS-Status und Server\n"
            "  resolvectl query hostname    → DNS-Lookup\n"
            "  resolvectl statistics        → Cache-Statistiken\n"
            "  resolvectl flush-caches      → DNS-Cache leeren\n"
            "\n"
            "/etc/resolv.conf:\n"
            "  Oft Symlink zu systemd-resolved stub:\n"
            "  ls -la /etc/resolv.conf\n"
            "  → /run/systemd/resolve/stub-resolv.conf\n"
            "\n"
            "Konfiguration:\n"
            "  /etc/systemd/resolved.conf   → Haupt-Konfiguration\n"
            "  DNS=8.8.8.8 8.8.4.4\n"
            "  FallbackDNS=1.1.1.1\n"
            "  DNSSEC=yes\n"
            "  DNSOverTLS=yes\n"
            "\n"
            "DNS-over-TLS:\n"
            "  Verschlüsselt DNS-Anfragen\n"
            "  DNSOverTLS=opportunistic    → Wenn verfügbar"
        ),
        syntax       = "resolvectl status",
        example      = "resolvectl query github.com && resolvectl statistics",
        task_description = "Zeige den DNS-Auflösungs-Status an.",
        expected_commands = ["resolvectl status", "resolvectl"],
        hint_text    = "resolvectl status zeigt DNS-Server und Konfiguration",
        quiz_questions = [
            QuizQuestion(
                question    = "Wohin zeigt /etc/resolv.conf auf modernen systemd-Systemen?",
                options     = ["/etc/dns.conf", "/run/systemd/resolve/stub-resolv.conf", "/var/lib/systemd/dns", "/etc/systemd/dns.conf"],
                correct     = 1,
                explanation = "/etc/resolv.conf ist auf systemd-Systemen oft ein Symlink nach /run/systemd/resolve/stub-resolv.conf.",
                xp_value    = 15,
            ),
            QuizQuestion(
                question    = "Welcher Befehl leert den DNS-Cache von systemd-resolved?",
                options     = ["systemctl restart systemd-resolved", "resolvectl flush-caches", "resolvectl clear", "dns --flush"],
                correct     = 1,
                explanation = "resolvectl flush-caches leert den DNS-Resolver-Cache.",
                xp_value    = 15,
            ),
        ],
        exam_tip     = "resolvectl status | /etc/systemd/resolved.conf | DNSOverTLS | resolvectl flush-caches",
        memory_tip   = "resolvectl = resolved + ctl = DNS steuern",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 15),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 19.13 — Docker Grundlagen
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "19.13",
        chapter      = 19,
        title        = "Docker: Container-Runtime Grundlagen",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "DAEMON",
        story        = (
            "DAEMON: 'Ghost. Die Ghost Processors nutzen Docker als Waffenkammer.\n"
            " Container. Isoliert. Portable. Reproducible.\n"
            " Lerne die Basics — ohne Docker bist du blind in dieser Welt.'"
        ),
        why_important = (
            "Docker ist die am weitesten verbreitete Container-Runtime.\n"
            "Grundlegende Docker-Kenntnisse werden zunehmend für LPIC-1 relevant."
        ),
        explanation  = (
            "DOCKER GRUNDLAGEN:\n\n"
            "CONTAINER VERWALTEN:\n"
            "  docker run ubuntu bash      Container starten\n"
            "  docker run -it ubuntu bash  Interaktiv\n"
            "  docker run -d nginx         Im Hintergrund (detached)\n"
            "  docker run -p 8080:80 nginx  Port-Mapping\n"
            "  docker ps                   Laufende Container\n"
            "  docker ps -a                Alle Container\n"
            "  docker stop CONTAINER       Stoppen\n"
            "  docker rm CONTAINER         Entfernen\n"
            "  docker exec -it CONT bash   Shell in Container\n\n"
            "IMAGES:\n"
            "  docker images               Lokale Images\n"
            "  docker pull nginx           Image herunterladen\n"
            "  docker rmi nginx            Image löschen\n"
            "  docker build -t myapp .     Image bauen\n\n"
            "VOLUMES & NETZWERK:\n"
            "  docker run -v /data:/data nginx  Volume mounten\n"
            "  docker network ls               Netzwerke\n"
            "  docker inspect CONTAINER        Details\n\n"
            "LOGS:\n"
            "  docker logs CONTAINER\n"
            "  docker logs -f CONTAINER  (live)"
        ),
        syntax       = "docker run [OPTIONS] IMAGE [COMMAND]",
        example      = "docker ps -a && docker images",
        task_description = "Zeige laufende Docker-Container mit docker ps",
        expected_commands = ["docker ps"],
        hint_text    = "docker ps zeigt laufende Container, docker ps -a alle (auch gestoppte)",
        quiz_questions = [
            QuizQuestion(
                question = "Welches docker-Kommando startet einen Container interaktiv mit einer Shell?",
                options  = [
                    "docker run -it ubuntu bash",
                    "docker exec ubuntu bash",
                    "docker start -i ubuntu",
                    "docker attach ubuntu bash",
                ],
                correct  = 0,
                explanation = "-it = interaktiv mit Terminal. docker exec ist für laufende Container.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "docker run=starten | ps=liste | exec=in Container | logs=ausgabe | images=lokale Images",
        memory_tip   = "docker run = neu starten. docker exec = in laufenden Container. docker ps = status.",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 19.14 — Podman: Rootless Containers
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "19.14",
        chapter      = 19,
        title        = "Podman: Rootless Container",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Docker braucht root. Das ist eine Schwäche.\n"
            " Podman läuft ohne root-Daemon.\n"
            " Docker-kompatible CLI — aber sicherer.'"
        ),
        why_important = (
            "Podman ist die rootless Docker-Alternative von Red Hat.\n"
            "Kein Daemon, kein root — sicherer für Multi-User-Systeme."
        ),
        explanation  = (
            "PODMAN — ROOTLESS CONTAINERS:\n\n"
            "GRUNDBEFEHLE (docker-kompatibel):\n"
            "  podman run -it ubuntu bash\n"
            "  podman ps / podman ps -a\n"
            "  podman images\n"
            "  podman pull nginx\n"
            "  podman exec -it CONT bash\n"
            "  podman stop CONT / podman rm CONT\n\n"
            "UNTERSCHIEDE ZU DOCKER:\n"
            "  Kein Daemon (kein dockerd)\n"
            "  Rootless: läuft als normaler User\n"
            "  OCI-konform: kompatibel mit Docker-Images\n"
            "  Pods: Gruppe von Containern (wie Kubernetes)\n\n"
            "PODS:\n"
            "  podman pod create --name mypod\n"
            "  podman run --pod mypod nginx\n"
            "  podman pod ps\n"
            "  podman pod stop mypod\n\n"
            "ALIAS FÜR MIGRATION:\n"
            "  alias docker=podman\n"
            "  → Drop-in Replacement für die meisten Befehle\n\n"
            "BUILDAH:\n"
            "  buildah bud -t myimage .   Image bauen (OCI)\n"
            "  Companion-Tool zu Podman"
        ),
        syntax       = "podman run [OPTIONS] IMAGE [COMMAND]",
        example      = "podman run --rm alpine uname -a && podman images",
        task_description = "Zeige podman-Version mit podman --version",
        expected_commands = ["podman --version"],
        hint_text    = "podman --version zeigt die installierte Podman-Version",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Hauptunterschied zwischen Docker und Podman?",
                options  = [
                    "Podman benötigt keinen root-Daemon und kann rootless laufen",
                    "Podman unterstützt keine Docker-Images",
                    "Docker ist schneller als Podman",
                    "Podman läuft nur auf Red Hat Systemen",
                ],
                correct  = 0,
                explanation = "Podman ist daemonless und rootless. Docker benötigt dockerd (root). Beide OCI-kompatibel.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "Podman = Docker-kompatibel aber rootless + daemonless. buildah = Image-Builder.",
        memory_tip   = "Pod-man = verwaltet Pods (wie kubectl). Kein Daemon = kein Single-Point-of-Failure.",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 19.15 — OverlayFS: Wie Container-Dateisysteme funktionieren
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "19.15",
        chapter      = 19,
        title        = "OverlayFS — Container-Dateisystem-Layer",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "DAEMON",
        story        = (
            "DAEMON: 'Wie teilen sich 100 Container dasselbe Base-Image?\n"
            " OverlayFS. Schichten. Read-only unten. Read-write oben.\n"
            " Das ist der Kern jeder Container-Runtime.'"
        ),
        why_important = (
            "OverlayFS ist das Dateisystem hinter Docker/Podman.\n"
            "Schicht-Architektur ermöglicht effiziente Image-Nutzung."
        ),
        explanation  = (
            "OVERLAYFS — CONTAINER-DATEISYSTEM:\n\n"
            "KONZEPT:\n"
            "  lower  = Read-only Layer (Base Image)\n"
            "  upper  = Read-write Layer (Container-Änderungen)\n"
            "  work   = Arbeitsverzeichnis (für atomic ops)\n"
            "  merged = Was der Container sieht (Kombination)\n\n"
            "MANUELLES OVERLAYFS:\n"
            "  mount -t overlay overlay \\\n"
            "    -o lowerdir=/base,upperdir=/changes,workdir=/work \\\n"
            "    /merged\n\n"
            "DOCKER OVERLAYFS:\n"
            "  docker info | grep Storage\n"
            "  → Storage Driver: overlay2\n"
            "  /var/lib/docker/overlay2/  Layer-Verzeichnisse\n\n"
            "COPY-ON-WRITE:\n"
            "  Datei unverändert → bleibt im lower layer\n"
            "  Datei geändert → Kopie in upper layer (CoW)\n"
            "  Datei gelöscht → Whiteout-Datei in upper layer\n\n"
            "SCHICHTEN ANZEIGEN:\n"
            "  docker history nginx       Layer-History\n"
            "  docker inspect nginx | jq '.[0].RootFS'"
        ),
        syntax       = "mount -t overlay overlay -o lowerdir=X,upperdir=Y,workdir=Z /merged",
        example      = "docker info | grep 'Storage Driver' && docker history nginx | head -10",
        task_description = "Zeige Docker-Storage-Info mit docker info | grep Storage",
        expected_commands = ["docker info"],
        hint_text    = "docker info zeigt den Storage Driver (overlay2 bei modernem Docker)",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der 'upper' Layer in OverlayFS?",
                options  = [
                    "Der read-write Layer — Container-Änderungen landen hier",
                    "Der read-only Base-Image Layer",
                    "Das Arbeitsverzeichnis für atomare Operationen",
                    "Der gemountete View der zusammengeführten Schichten",
                ],
                correct  = 0,
                explanation = "upper = R/W. lower = R/O (Base). merged = was der Container sieht. work = intern.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "overlay2 ist Standard Storage-Driver. CoW = nur geänderte Dateien werden kopiert.",
        memory_tip   = "Lower = Fundament (unberührt). Upper = Container-Schicht (Änderungen). Merged = Gesamt-Bild.",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 19.16 — Linux Capabilities: Feinsteuerung von Root-Rechten
    # ══════════════════════════════════════════════════════════════════════
    Mission(
        mission_id   = "19.16",
        chapter      = 19,
        title        = "Linux Capabilities: Feinsteuerung von Rechten",
        mtype        = "SCAN",
        xp           = 90,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Root oder nicht-root — das ist zu simpel.\n"
            " Capabilities teilen root-Rechte in kleine Einheiten.\n"
            " CAP_NET_ADMIN für Netzwerk. CAP_SYS_TIME für Zeit.\n"
            " Principle of Least Privilege — granular.'"
        ),
        why_important = (
            "Linux Capabilities ermöglichen granulare Privilegien ohne vollen root-Zugriff.\n"
            "Sicherheits-Best-Practice für Container und Dienste."
        ),
        explanation  = (
            "LINUX CAPABILITIES:\n\n"
            "KONZEPT:\n"
            "  Root-Rechte aufgeteilt in ~40 Capabilities\n"
            "  Jede Capability kann einzeln gewährt/entzogen werden\n\n"
            "WICHTIGE CAPABILITIES:\n"
            "  CAP_NET_ADMIN   Netzwerk-Konfiguration (ip, iptables)\n"
            "  CAP_NET_BIND_SERVICE  Ports < 1024 binden\n"
            "  CAP_SYS_TIME    Systemzeit ändern\n"
            "  CAP_SYS_PTRACE  Prozesse tracen (strace)\n"
            "  CAP_CHOWN       Datei-Eigentümer ändern\n"
            "  CAP_KILL        Signals an fremde Prozesse senden\n"
            "  CAP_SETUID      UID wechseln\n\n"
            "TOOLS:\n"
            "  getcap /usr/bin/ping      Capabilities einer Datei\n"
            "  setcap cap_net_raw+ep /usr/bin/ping  Capability setzen\n"
            "  capsh --print             Aktuelle Capabilities\n"
            "  cat /proc/self/status | grep Cap  Capability-Hex\n\n"
            "DOCKER:\n"
            "  docker run --cap-drop ALL --cap-add NET_ADMIN nginx\n"
            "  docker run --privileged nginx  (alle Caps, gefährlich!)"
        ),
        syntax       = "getcap BINARY | setcap CAP+ep BINARY",
        example      = "getcap /usr/bin/ping && capsh --print | grep Current",
        task_description = "Zeige Capabilities von ping mit getcap /usr/bin/ping",
        expected_commands = ["getcap /usr/bin/ping"],
        hint_text    = "getcap /usr/bin/ping zeigt die Capabilities des ping-Binaries",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Capability erlaubt es einem Nicht-Root-Prozess, Port 80 zu binden?",
                options  = [
                    "CAP_NET_BIND_SERVICE",
                    "CAP_NET_ADMIN",
                    "CAP_NET_RAW",
                    "CAP_SYS_ADMIN",
                ],
                correct  = 0,
                explanation = "CAP_NET_BIND_SERVICE erlaubt das Binden von privilegierten Ports (< 1024).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "getcap=Capabilities lesen | setcap=setzen | capsh --print=aktuelle Session",
        memory_tip   = "Capabilities = feingranulare root-Rechte. + ep = erlaubt + vererbt.",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 20),
    ),

    # ══════════════════════════════════════════════════════════════════════
    # 19.quiz
    Mission(
        mission_id   = "19.quiz",
        chapter      = 19,
        title        = "GHOST PROTOCOL II — Abschluss-Quiz",
        mtype        = "QUIZ",
        xp           = 250,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM: 'Ghost Processors Zertifizierungs-Test.\n"
            " Container, Namespaces, Virtualisierung, Cloud-Init.\n"
            " Zeig dass du das Unsichtbare verstehst.'"
        ),
        why_important = "Quiz-Wiederholung aller Ghost-Processors Themen: Container, VMs, Cloud-Init.",
        explanation  = "Alle Themen aus Kapitel 19: Namespaces, cgroups, Container, Virtualisierung, Cloud-Init.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Quiz-Fragen zu Container und Virtualisierung.",
        expected_commands = [],
        hint_text    = "Nutze [r] Review Mode für Wiederholung",
        quiz_questions = [
            QuizQuestion(
                question    = "Was kombiniert einen Linux-Container?",
                options     = ["nur chroot", "Namespaces + cgroups + Overlay-FS", "nur Namespaces", "KVM + Docker"],
                correct     = 1,
                explanation = "Container = Namespaces (Isolation) + cgroups (Ressourcenlimits) + Overlay-FS.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Welcher Namespace isoliert Prozess-IDs?",
                options     = ["NET", "MNT", "PID", "UTS"],
                correct     = 2,
                explanation = "PID-Namespace isoliert Prozess-IDs — jeder Container hat eigenen PID 1.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Was ist der Marker für cloud-config user-data?",
                options     = ["# cloud-init", "#cloud-config", "---cloud---", "!cloud-config"],
                correct     = 1,
                explanation = "#cloud-config (kein Leerzeichen) startet eine YAML cloud-init Konfiguration.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Welcher virsh-Befehl stoppt eine VM gracefully?",
                options     = ["virsh stop", "virsh destroy", "virsh shutdown", "virsh halt"],
                correct     = 2,
                explanation = "virsh shutdown sendet ein ACPI-Signal — VM fährt ordentlich herunter.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Welches Tool verwaltet systemd-nspawn Container?",
                options     = ["nspawnctl", "machinectl", "containerctl", "systemctl container"],
                correct     = 1,
                explanation = "machinectl ist das Verwaltungstool für systemd-nspawn Container.",
                xp_value    = 25,
            ),
            QuizQuestion(
                question    = "Was passiert nach dem Klonen einer VM mit Machine-ID?",
                options     = ["Nichts — ID ist eindeutig", "Machine-ID muss neu generiert werden", "ID wird automatisch geändert", "ID muss gelöscht bleiben"],
                correct     = 1,
                explanation = "Machine-ID muss nach Clone neu generiert werden: rm /etc/machine-id && systemd-machine-id-setup.",
                xp_value    = 25,
            ),
        ],
        exam_tip     = "Container=NS+cg+FS | PID-NS | #cloud-config | virsh shutdown | machinectl | machine-id nach Clone",
        memory_tip   = "Ghost Processors = Meister der Isolation: Namespace, Container, VM, Cloud",
        gear_reward  = None,
        faction_reward = ("Ghost Processors", 30),
    ),

    Mission(
        mission_id   = "19.boss",
        chapter      = 19,
        title        = "PHANTOM CODE — Ghost Processors Boss",
        mtype        = "BOSS",
        xp           = 650,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM: '[ PHANTOM CODE AKTIVIERT ]\n"
            " Die Ghost Processors fordern dich heraus.\n"
            " Container-Isolation. Namespace-Manipulation. VM-Kontrolle.\n"
            " Beweise dass du zu den Unsichtbaren gehörst.\n"
            " Die NeonGrid-9 Infrastruktur hängt davon ab.'"
        ),
        why_important = "Boss-Herausforderung: Alle Ghost-Processors Konzepte in einem Test.",
        explanation  = (
            "PHANTOM CODE Boss-Wissen:\n"
            "\n"
            "Container-Stack:\n"
            "  PID + NET + MNT + UTS + IPC + USER + CGROUP = 7 Namespaces\n"
            "  cgroups: CPU, Memory, I/O Limits\n"
            "  chroot < systemd-nspawn < Container (Docker/Podman)\n"
            "\n"
            "Virtualisierung:\n"
            "  KVM = Kernel-Modul | QEMU = Emulation | libvirt = API\n"
            "  virsh: list, start, shutdown, destroy, console\n"
            "  Typ 1 = Bare-Metal | Typ 2 = Hosted\n"
            "\n"
            "Cloud-Init:\n"
            "  #cloud-config | packages | runcmd | write_files\n"
            "  /etc/cloud/ + /var/lib/cloud/\n"
            "\n"
            "systemd Advanced:\n"
            "  Drop-ins: NAME.service.d/override.conf\n"
            "  systemctl edit/cat/revert\n"
            "  daemon-reload nach Änderungen\n"
            "\n"
            "Security:\n"
            "  AppArmor: aa-status, enforce/complain\n"
            "  SELinux: getenforce, setenforce, ls -Z"
        ),
        ascii_art    = """
  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
  ██╔════╝██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
  ██║  ███╗███████║██║   ██║███████╗   ██║
  ██║   ██║██╔══██║██║   ██║╚════██║   ██║
  ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║
   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
      ██████╗ ██████╗  ██████╗  ██████╗███████╗███████╗███████╗ ██████╗ ██████╗ ███████╗
      ██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
      ██████╔╝██████╔╝██║   ██║██║     █████╗  ███████╗███████╗██║   ██║██████╔╝███████╗
      ██╔═══╝ ██╔══██╗██║   ██║██║     ██╔══╝  ╚════██║╚════██║██║   ██║██╔══██╗╚════██║
      ██║     ██║  ██║╚██████╔╝╚██████╗███████╗███████║███████║╚██████╔╝██║  ██║███████║
      ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

  ┌─ PHANTOM STATUS ─────────────────────────────┐
  │  Namespaces: HIJACKED  ::  cgroups: ESCAPED  │
  │  Containers: ROGUE     ::  VMs: COMPROMISED  │
  │  Capabilities: LEAKED  ::  SELinux: BYPASSED │
  └──────────────────────────────────────────────┘

  ⚡ CHAOSWERK FACTION :: CHAPTER 19 BOSS ⚡""",
        story_transitions = [
            "PHANTOM CODE aktiviert sich. Namespaces kollabieren. lsns zeigt Chaos.",
            "Container brechen aus. nsenter -t PID --net taucht in seinen Namespace.",
            "cgroups memory.limit_in_bytes gesetzt. Er erstickt an eigenen Limits.",
            "Letzte VM. systemd-detect-virt enttarnt sie. Ghost Processor — besiegt.",
        ],
        syntax       = "lsns && machinectl list && virsh list --all 2>/dev/null",
        example      = "systemd-detect-virt && cat /etc/machine-id",
        task_description = (
            "BOSS-CHALLENGE: Identifiziere die Virtualisierungsumgebung.\n"
            "Zeige den Virtualisierungstyp an."
        ),
        expected_commands = ["systemd-detect-virt", "lsns", "machinectl"],
        hints = [
            "Ein Auflistungsbefehl wie 'systemd-detect-virt' wird benötigt.",
            "Der Befehl selbst ist: systemd-detect-virt",
            "Der vollständige Befehl: systemd-detect-virt",
        ],
        hint_text    = "systemd-detect-virt — welche Virtualisierungsebene läuft?",
        quiz_questions = [
            QuizQuestion(
                question    = "Was ist der korrekte Weg einen systemd-Service zu konfigurieren ohne die Original-Datei zu ändern?",
                options     = ["Unit-Datei direkt editieren", "Drop-in Datei in NAME.service.d/ erstellen", "service --override", "/etc/systemd/overrides/"],
                correct     = 1,
                explanation = "Drop-in Dateien in NAME.service.d/override.conf sind der korrekte Weg — Updates überschreiben sie nicht.",
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "AppArmor complain-Modus bedeutet:",
                options     = ["Verstöße blockieren", "Nur loggen, nicht blockieren", "Profil deaktiviert", "Nur für root"],
                correct     = 1,
                explanation = "complain = Verstöße werden geloggt aber nicht blockiert. enforce = Blockierung aktiv.",
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "Welcher Befehl generiert eine neue Machine-ID?",
                options     = ["systemctl new-machine-id", "systemd-machine-id-setup", "machinectl new-id", "uuidgen > /etc/machine-id"],
                correct     = 1,
                explanation = "systemd-machine-id-setup generiert und schreibt eine neue Machine-ID in /etc/machine-id.",
                xp_value    = 30,
            ),
            QuizQuestion(
                question    = "Was ist der Unterschied zwischen einem Linux-Container (LXC) und einer virtuellen Maschine (KVM)?",
                options     = [
                    "Container teilen den Host-Kernel (OS-Virtualisierung); VMs haben eigenen Kernel und emulieren Hardware (Hypervisor-Virtualisierung)",
                    "Container sind langsamer als VMs weil sie mehr Overhead haben",
                    "VMs teilen den Kernel; Container haben eigene Kernel",
                    "Beide verwenden den gleichen Isolationsmechanismus",
                ],
                correct     = 0,
                explanation = "Container (LXC, Docker) = Namespaces + cgroups auf dem Host-Kernel — schnell, leicht, kein eigener Kernel. VMs (KVM, VMware) = vollständige Hardware-Emulation mit eigenem OS-Image — stärkere Isolation, mehr Overhead.",
                xp_value    = 35,
            ),
            QuizQuestion(
                question    = "Welche zwei Linux-Kernel-Features bilden die Grundlage aller Container-Technologien?",
                options     = [
                    "Namespaces (Isolation) und cgroups (Ressourcenlimits)",
                    "SELinux und AppArmor",
                    "iptables und netfilter",
                    "systemd und D-Bus",
                ],
                correct     = 0,
                explanation = "Namespaces isolieren Prozesse (PID, NET, MNT, UTS, IPC, USER). cgroups (Control Groups) begrenzen Ressourcen (CPU, RAM, I/O). Docker, LXC, podman — alle bauen auf diesen zwei Kernel-Features auf.",
                xp_value    = 35,
            ),
        ],
        exam_tip     = "Ghost Processors: Container=NS+CG | Cloud-Init=#cloud-config | Drop-in=.service.d | AppArmor/SELinux",
        memory_tip   = "Ghost Processors meistern das Unsichtbare: Isolation, Virtualisierung, Automation",
        gear_reward  = "kernel_beacon",
        faction_reward = ("Ghost Processors", 60),
    ),
]
