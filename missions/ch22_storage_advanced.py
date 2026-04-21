"""
NeonGrid-9 :: Kapitel 22 — STORAGE ADVANCED
LPIC-1 Topic 104.1 / 104.3 / 104.4
Storage: RAID, LVM Advanced, Disk Quotas, iSCSI, btrfs

"In NeonGrid-9 sind Daten das einzige was zählt.
 RAID schützt sie. Quotas begrenzen sie.
 LVM skaliert sie. Kenne die Werkzeuge deiner Daten."
"""

from engine.mission_engine import Mission, QuizQuestion

CHAPTER_22_MISSIONS: list[Mission] = [

    Mission(
        mission_id   = "22.01",
        chapter      = 22,
        title        = "Storage Advanced — Einführung & RAID-Konzepte",
        mtype        = "SCAN",
        xp           = 135,
        speaker      = "RUST",
        story        = (
            "RUST: 'Datenverlust ist keine Option, Ghost.\n"
            " RAID. Redundancy. Mehrere Disks. Eine logische Einheit.\n"
            " Kenn die Level. Versteh die Tradeoffs.'"
        ),
        why_important = "RAID-Konzepte sind LPIC-1 Prüfungsthema (Topic 104.3).",
        explanation  = (
            "RAID LEVEL ÜBERSICHT:\n\n"
            "RAID 0 (Striping):\n"
            "  + Volle Kapazität, hohe Performance\n"
            "  - KEIN Schutz. Ein Disk-Fehler = alles weg!\n"
            "  Mindest-Disks: 2\n\n"
            "RAID 1 (Mirroring):\n"
            "  + Perfekte Redundanz (Spiegel)\n"
            "  - Nur 50% Kapazität\n"
            "  Mindest-Disks: 2\n\n"
            "RAID 5 (Striping + Parity):\n"
            "  + Gute Kapazität (N-1), eine Disk-Fehler tolerant\n"
            "  - Langsame Schreiboperationen\n"
            "  Mindest-Disks: 3\n\n"
            "RAID 6 (Double Parity):\n"
            "  + Zwei Disk-Fehler tolerant\n"
            "  - Noch langsamere Schreiboperationen\n"
            "  Mindest-Disks: 4\n\n"
            "RAID 10 (1+0, Mirror+Stripe):\n"
            "  + Hohe Performance + Redundanz\n"
            "  - 50% Kapazität\n"
            "  Mindest-Disks: 4\n\n"
            "SOFTWARE RAID: mdadm\n"
            "HARDWARE RAID: Controller-Karte (BIOS-Ebene)"
        ),
        ascii_art = """
  ███████╗████████╗ ██████╗ ██████╗  █████╗  ██████╗ ███████╗
  ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝
  ███████╗   ██║   ██║   ██║██████╔╝███████║██║  ███╗█████╗
  ╚════██║   ██║   ██║   ██║██╔══██╗██╔══██║██║   ██║██╔══╝
  ███████║   ██║   ╚██████╔╝██║  ██║██║  ██║╚██████╔╝███████╗
  ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
       █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗██████╗
      ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗
      ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║     █████╗  ██║  ██║
      ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║     ██╔══╝  ██║  ██║
      ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗███████╗██████╔╝
      ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝

  [ CHAPTER 22 :: STORAGE ADVANCED ]
  > RAID array: assembling. LVM: scanning VGs. mdstat: loading...""",
        story_transitions = [
            "RAID schützt Daten durch Redundanz. Ein Disk-Ausfall überlebt.",
            "LVM abstrahiert physische Disks. Resize ohne Neustart.",
            "Quota begrenzt. btrfs versioniert. iSCSI netzt Storage.",
            "Rust bewacht die Daten. Du musst die Arrays kennen.",
        ],
        syntax       = "mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sd[bcd]1",
        example      = "cat /proc/mdstat && mdadm --detail /dev/md0",
        task_description = "Zeige RAID-Status mit cat /proc/mdstat",
        expected_commands = ["cat /proc/mdstat"],
        hint_text    = "cat /proc/mdstat zeigt alle Software-RAID-Setups",
        quiz_questions = [
            QuizQuestion(
                question = "Wie viele Disks können bei RAID 5 ausfallen ohne Datenverlust?",
                options  = ["1", "2", "0", "3"],
                correct  = 0,
                explanation = "RAID 5: 1 Disk Fehlertoleranz. RAID 6: 2. RAID 1: 1 (bei 2 Disks). RAID 0: 0.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "RAID0=kein Schutz | RAID1=Spiegel | RAID5=Parity(min3) | RAID6=2Fehler | RAID10=1+0",
        memory_tip   = "RAID 5: N-1 Kapazität. N=Anzahl Disks, 1=Parity. Mindestens 3 Disks.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 20),
    ),

    Mission(
        mission_id   = "22.02",
        chapter      = 22,
        title        = "mdadm: Software RAID erstellen",
        mtype        = "CONSTRUCT",
        xp           = 95,
        speaker      = "RUST",
        story        = (
            "RUST: 'Hardware-RAID ist teuer. Software-RAID ist gratis.\n"
            " mdadm. Drei Befehle. Array erstellen.\n"
            " Performance kaum schlechter. Flexibilität: viel besser.'"
        ),
        why_important = (
            "mdadm ist das Standard-Tool für Software-RAID auf Linux.\n"
            "LPIC-1 Topic 104.3 testet mdadm-Grundbefehle."
        ),
        explanation  = (
            "MDADM — MULTIPLE DEVICE ADMIN:\n\n"
            "RAID-ARRAY ERSTELLEN:\n"
            "  mdadm --create /dev/md0 \\\n"
            "    --level=1 --raid-devices=2 \\\n"
            "    /dev/sdb1 /dev/sdc1\n\n"
            "DATEISYSTEM & MOUNT:\n"
            "  mkfs.ext4 /dev/md0\n"
            "  mount /dev/md0 /mnt/raid\n\n"
            "MDADM.CONF ERSTELLEN:\n"
            "  mdadm --detail --scan >> /etc/mdadm/mdadm.conf\n"
            "  update-initramfs -u  (damit RAID beim Boot verfügbar)\n\n"
            "STATUS:\n"
            "  cat /proc/mdstat             Schnell-Status\n"
            "  mdadm --detail /dev/md0      Details\n"
            "  mdadm --query /dev/sdb1      Disk-Info\n\n"
            "RAID VERWALTEN:\n"
            "  mdadm --add /dev/md0 /dev/sdd1      Disk hinzufügen\n"
            "  mdadm --fail /dev/md0 /dev/sdb1     Disk als fehlerhaft\n"
            "  mdadm --remove /dev/md0 /dev/sdb1   Disk entfernen\n\n"
            "ARRAY STOPPEN:\n"
            "  mdadm --stop /dev/md0\n"
            "  mdadm --zero-superblock /dev/sdb1"
        ),
        syntax       = "mdadm --create /dev/md0 --level=LEVEL --raid-devices=N /dev/sdX...",
        example      = "mdadm --detail /dev/md0 && cat /proc/mdstat",
        task_description = "Zeige RAID-Details mit cat /proc/mdstat",
        expected_commands = ["cat /proc/mdstat"],
        hint_text    = "cat /proc/mdstat gibt einen Überblick über alle Software-RAID-Arrays",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Datei muss nach `mdadm --create` aktualisiert werden für persistentes RAID?",
                options  = [
                    "/etc/mdadm/mdadm.conf",
                    "/etc/fstab",
                    "/etc/raid.conf",
                    "/proc/mdstat",
                ],
                correct  = 0,
                explanation = "/etc/mdadm/mdadm.conf speichert RAID-Konfiguration dauerhaft. mdadm --detail --scan >> mdadm.conf",
                xp_value = 15,
            ),
        ],
        exam_tip     = "mdadm --create → --detail → --scan >> mdadm.conf. /proc/mdstat = Live-Status.",
        memory_tip   = "mdadm: create=erstellen, detail=inspizieren, add=hinzufügen, fail=kaputt-markieren.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 20),
    ),

    Mission(
        mission_id   = "22.03",
        chapter      = 22,
        title        = "mdadm: RAID-Wiederherstellung",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "RUST: 'Eine Disk ausgefallen. Alert.\n"
            " RAID 1. Noch läuft alles. Aber degraded.\n"
            " Neue Disk. Einbauen. Resync. Das Prozedere.'"
        ),
        why_important = (
            "RAID-Wiederherstellung ist kritisches Wissen für Systemadministratoren.\n"
            "mdadm --fail, --remove, --add ist der Standard-Prozess."
        ),
        explanation  = (
            "RAID WIEDERHERSTELLUNG:\n\n"
            "DEGRADED ARRAY ERKENNEN:\n"
            "  cat /proc/mdstat         [UU] = OK, [_U] = degraded\n"
            "  mdadm --detail /dev/md0  State: degraded\n\n"
            "DISK ERSETZEN:\n"
            "  1. Disk als fehlerhaft markieren:\n"
            "     mdadm --fail /dev/md0 /dev/sdb1\n"
            "  2. Disk entfernen:\n"
            "     mdadm --remove /dev/md0 /dev/sdb1\n"
            "  3. Neue Disk partitionieren (gleiches Schema)\n"
            "  4. Neue Disk hinzufügen:\n"
            "     mdadm --add /dev/md0 /dev/sdd1\n"
            "  → Automatischer Resync beginnt\n\n"
            "RESYNC BEOBACHTEN:\n"
            "  cat /proc/mdstat\n"
            "  → recovery = 45.3% (78.5K/min) finish=5.0min\n\n"
            "HOT SPARE:\n"
            "  mdadm --create /dev/md0 --level=5 --raid-devices=3 \\\n"
            "    --spare-devices=1 /dev/sdb1 /dev/sdc1 /dev/sdd1 /dev/sde1\n"
            "  → Spare wird automatisch bei Ausfall aktiviert\n\n"
            "BENACHRICHTIGUNG:\n"
            "  mdadm --monitor --mail=admin@server --delay=300 /dev/md0 &"
        ),
        syntax       = "mdadm --fail /dev/md0 /dev/DISK && mdadm --remove /dev/md0 /dev/DISK && mdadm --add /dev/md0 /dev/NEWDISK",
        example      = "mdadm --detail /dev/md0 | grep -E 'State|Active|Failed'",
        task_description = "Zeige RAID-Konfigurationsdetails mit mdadm --detail /dev/md0 (falls vorhanden)",
        expected_commands = ["mdadm --detail"],
        hint_text    = "mdadm --detail /dev/md0 zeigt detaillierte RAID-Informationen",
        quiz_questions = [
            QuizQuestion(
                question = "Was bedeutet `[_U]` in der /proc/mdstat Ausgabe?",
                options  = [
                    "RAID ist degraded: eine Disk fehlt oder ist ausgefallen",
                    "RAID ist deaktiviert",
                    "RAID wird gerade erstellt",
                    "RAID ist gesund",
                ],
                correct  = 0,
                explanation = "[UU]=gesund, [_U]=eine Disk fehlt/fehlerhaft (degraded). Muss dringend ersetzt werden.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "fail→remove→add = Disk-Tausch. Hot Spare = automatisches Failover. Monitor für Alerts.",
        memory_tip   = "[UU]=gut, [_U]=kaputt. Erst fail, dann remove, dann neue Disk add.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.04",
        chapter      = 22,
        title        = "Disk Quotas: Speicher begrenzen",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "RUST: 'Ghost füllt /home mit 50GB Logs.\n"
            " Quotas. Soft limit. Hard limit. Grace period.\n"
            " Kein User beansprucht mehr als sein Anteil.'"
        ),
        why_important = (
            "Disk Quotas begrenzen den Speicher pro User/Gruppe.\n"
            "LPIC-1 Topic 104.3 testet quota-Grundbefehle."
        ),
        explanation  = (
            "DISK QUOTAS:\n\n"
            "VORAUSSETZUNG (in /etc/fstab):\n"
            "  /dev/sdb1  /home  ext4  defaults,usrquota,grpquota  0 2\n"
            "  → usrquota = User-Quotas, grpquota = Gruppen-Quotas\n\n"
            "QUOTA-DATENBANK ERSTELLEN:\n"
            "  quotacheck -cug /home\n"
            "  → Erstellt aquota.user und aquota.group in /home\n"
            "  -c = create, -u = user, -g = group, -m = kein Remount\n\n"
            "QUOTAS AKTIVIEREN:\n"
            "  quotaon -v /home\n"
            "  quotaon -a     Alle Filesysteme mit Quota-Option\n\n"
            "QUOTA SETZEN:\n"
            "  edquota -u ghost\n"
            "  → Öffnet Editor mit Quota-Tabelle\n"
            "  Filesystem  blocks  soft  hard  inodes  soft  hard\n"
            "  /dev/sdb1   512000  800000  1000000   0   0   0\n"
            "  (Werte in KB)\n\n"
            "QUOTA ANZEIGEN:\n"
            "  quota ghost          User-Quota\n"
            "  repquota /home       Alle User auf /home\n"
            "  repquota -a          Alle\n\n"
            "GRACE PERIOD:\n"
            "  edquota -t           Grace-Period setzen\n"
            "  Soft limit = Warnung (Grace period)\n"
            "  Hard limit = Absolutes Maximum"
        ),
        syntax       = "quotacheck -cug /home && quotaon /home && edquota -u USER",
        example      = "repquota -a && quota ghost",
        task_description = "Zeige Quota-Status mit repquota -a (falls Quotas aktiv)",
        expected_commands = ["repquota -a"],
        hint_text    = "repquota -a zeigt Quota-Nutzung aller User auf allen Filesystemen",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Unterschied zwischen Soft Limit und Hard Limit bei Quotas?",
                options  = [
                    "Soft Limit: Warnung + Grace Period erlaubt. Hard Limit: Absolut, keine Überschreitung",
                    "Soft Limit ist kleiner, Hard Limit ist größer",
                    "Soft Limit gilt für User, Hard Limit für Gruppen",
                    "Soft Limit kann der User selbst ändern",
                ],
                correct  = 0,
                explanation = "Soft: Warnung, Überschreitung für Grace Period erlaubt (z.B. 7 Tage). Hard: nie überschreitbar.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "quotacheck -cug. quotaon. edquota. repquota -a. Soft=Warnung, Hard=Maximum.",
        memory_tip   = "Soft=weich (Warnung), Hard=hart (Mauer). Grace Period = Gnadenfrist.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.05",
        chapter      = 22,
        title        = "LVM Snapshots: Konsistente Backups",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "RUST: 'Backup eines live Systems. Problem?\n"
            " LVM Snapshot. Einfrieren des Zustands.\n"
            " Backup. Snapshot löschen. Null Ausfallzeit.'"
        ),
        why_important = (
            "LVM Snapshots ermöglichen konsistente Backups ohne Downtime.\n"
            "Wichtiges Feature für Produktionssysteme."
        ),
        explanation  = (
            "LVM SNAPSHOTS:\n\n"
            "SNAPSHOT ERSTELLEN:\n"
            "  lvcreate -L 1G -s -n data_snap /dev/vg0/data\n"
            "  -L 1G  = Snapshot-Größe (COW-Bereich)\n"
            "  -s     = Snapshot\n"
            "  -n     = Name\n"
            "  Letzter Parameter = Quell-LV\n\n"
            "SNAPSHOT MOUNTEN:\n"
            "  mount -o ro /dev/vg0/data_snap /mnt/snap\n"
            "  → Konsistenter Zustand zum Zeitpunkt des Snapshots\n\n"
            "BACKUP:\n"
            "  tar czf /backup/data.tar.gz /mnt/snap\n"
            "  rsync -av /mnt/snap/ /backup/data/\n\n"
            "SNAPSHOT ENTFERNEN:\n"
            "  umount /mnt/snap\n"
            "  lvremove /dev/vg0/data_snap\n\n"
            "SNAPSHOT-GRÖSSE:\n"
            "  Snapshot wächst mit CoW-Operationen\n"
            "  Zu klein → overflow → Snapshot invalid!\n"
            "  Überwachen: lvs -o +data_percent\n\n"
            "RESTORE (Rollback):\n"
            "  lvconvert --merge /dev/vg0/data_snap\n"
            "  → Stellt data auf Snapshot-Zustand zurück"
        ),
        syntax       = "lvcreate -L SIZE -s -n SNAPNAME /dev/VG/LV",
        example      = "lvcreate -L 2G -s -n home_snap /dev/vg0/home && lvs",
        task_description = "Zeige LVM Volumes mit lvs",
        expected_commands = ["lvs"],
        hint_text    = "lvs zeigt alle Logical Volumes inkl. Snapshots",
        quiz_questions = [
            QuizQuestion(
                question = "Was passiert wenn ein LVM-Snapshot zu klein wird?",
                options  = [
                    "Der Snapshot wird invalid und unbrauchbar",
                    "Der Snapshot wächst automatisch",
                    "Das Original-Volume wird beschädigt",
                    "Der Snapshot wird auf die Disk-Größe erweitert",
                ],
                correct  = 0,
                explanation = "Snapshot overflow: Snapshot wird als invalid markiert und kann nicht mehr gemountet werden.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "lvcreate -s = Snapshot. lvconvert --merge = Rollback. lvs -o +data_percent = Füllstand.",
        memory_tip   = "Snapshot = Foto des Volumes. CoW = nur geänderte Blöcke werden gespeichert.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.06",
        chapter      = 22,
        title        = "LVM Thin Provisioning",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "RUST: '100 VMs. Jede mit 50GB Platte.\n"
            " Aber real genutzt: je 5GB.\n"
            " Thin Provisioning. Nur reservieren was genutzt wird.'"
        ),
        why_important = (
            "LVM Thin Provisioning ermöglicht Over-Provisioning und\n"
            "effiziente Speichernutzung in Virtualisierungsumgebungen."
        ),
        explanation  = (
            "LVM THIN PROVISIONING:\n\n"
            "KONZEPT:\n"
            "  Thin Pool = Pool of blocks (Reserve)\n"
            "  Thin Volume = LV das aus dem Pool nimmt (on-demand)\n"
            "  Over-provisioning: Summe aller LVs > Pool-Größe erlaubt\n\n"
            "THIN POOL ERSTELLEN:\n"
            "  lvcreate -L 100G -T vg0/thinpool\n\n"
            "THIN VOLUME ERSTELLEN:\n"
            "  lvcreate -V 20G -T -n vm1 vg0/thinpool\n"
            "  → vm1 hat 20GB Adressraum, aber nutzt nur tatsächlich verwendete Blöcke\n\n"
            "STATUS:\n"
            "  lvs -a -o+data_percent,metadata_percent\n"
            "  → Data%: wie voll ist der Pool?\n\n"
            "THIN SNAPSHOT:\n"
            "  lvcreate -s -n vm1_snap vg0/vm1\n"
            "  → Thin Volumes haben automatisch effizienten Snapshot\n\n"
            "AUTOEXTEND:\n"
            "  /etc/lvm/lvm.conf:\n"
            "    thin_pool_autoextend_threshold = 80\n"
            "    thin_pool_autoextend_percent = 20\n"
            "  → Pool wächst automatisch wenn 80% voll"
        ),
        syntax       = "lvcreate -L 100G -T vg0/thinpool && lvcreate -V 20G -T -n vm1 vg0/thinpool",
        example      = "lvs -a -o+data_percent,metadata_percent | grep thin",
        task_description = "Zeige alle LVs mit lvs -a",
        expected_commands = ["lvs -a"],
        hint_text    = "lvs -a zeigt alle Logical Volumes inkl. interne Thin-Pool-Volumes",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist Over-Provisioning bei LVM Thin?",
                options  = [
                    "Thin Volumes zusammen größer als der Pool — erlaubt wenn nicht alles genutzt wird",
                    "Pool hat mehr Platz als die VG",
                    "Automatische Erweiterung des Pools",
                    "Backup-Speicher für Notfälle",
                ],
                correct  = 0,
                explanation = "Over-provisioning: Summe der Thin Volume Größen > Pool. OK solange Nutzung < Pool-Größe.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "lvcreate -T = thin pool. lvcreate -V = thin volume. Data% überwachen!",
        memory_tip   = "Thin = schmal/sparsam. Nur wirklich genutzte Blöcke werden reserviert.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.07",
        chapter      = 22,
        title        = "LVM PV/VG/LV Management",
        mtype        = "CONSTRUCT",
        xp           = 90,
        speaker      = "RUST",
        story        = (
            "RUST: 'Physical Volume. Volume Group. Logical Volume.\n"
            " Drei Schichten. Volle Kontrolle.\n"
            " Resize, Extend, Reduce. Das LVM-Trifecta.'"
        ),
        why_important = (
            "LVM-Management ist fundamentales LPIC-1 Thema (Topic 104.1).\n"
            "pvcreate, vgcreate, lvcreate und Resize-Befehle."
        ),
        explanation  = (
            "LVM KOMPLETT:\n\n"
            "PHYSICAL VOLUME (PV):\n"
            "  pvcreate /dev/sdb           PV erstellen\n"
            "  pvs                         Alle PVs\n"
            "  pvdisplay /dev/sdb          Details\n"
            "  pvmove /dev/sdb /dev/sdc    Daten migrieren\n"
            "  pvremove /dev/sdb           PV entfernen\n\n"
            "VOLUME GROUP (VG):\n"
            "  vgcreate vg0 /dev/sdb /dev/sdc  VG aus 2 PVs\n"
            "  vgs                         Alle VGs\n"
            "  vgdisplay vg0               Details\n"
            "  vgextend vg0 /dev/sdd       PV zu VG hinzufügen\n"
            "  vgreduce vg0 /dev/sdb       PV aus VG entfernen\n"
            "  vgrename vg0 vgdata         VG umbenennen\n\n"
            "LOGICAL VOLUME (LV):\n"
            "  lvcreate -L 10G -n data vg0\n"
            "  lvs                         Alle LVs\n"
            "  lvdisplay /dev/vg0/data     Details\n"
            "  lvextend -L +5G /dev/vg0/data  Erweitern\n"
            "  lvreduce -L -2G /dev/vg0/data  Verkleinern (Vorsicht!)\n"
            "  lvrename vg0 data archive   LV umbenennen\n"
            "  lvremove /dev/vg0/data      LV löschen\n\n"
            "FILESYSTEM NACH LVEXTEND:\n"
            "  resize2fs /dev/vg0/data     ext4 (online!)\n"
            "  xfs_growfs /mnt/data        xfs (nur wachsen)"
        ),
        syntax       = "pvcreate → vgcreate → lvcreate",
        example      = "pvs && vgs && lvs",
        task_description = "Zeige Volume Groups mit vgs",
        expected_commands = ["vgs"],
        hint_text    = "vgs zeigt alle Volume Groups und ihren freien Speicher",
        quiz_questions = [
            QuizQuestion(
                question = "Was muss nach `lvextend` für ein ext4-Filesystem gemacht werden?",
                options  = [
                    "resize2fs /dev/vg0/LV  (ext4 Filesystem vergrößern)",
                    "mkfs.ext4 /dev/vg0/LV (neu formatieren)",
                    "mount -o remount /dev/vg0/LV",
                    "Nichts — ext4 erkennt die neue Größe automatisch",
                ],
                correct  = 0,
                explanation = "lvextend vergrößert das LV. resize2fs vergrößert das ext4 Filesystem im LV. Online-Resize möglich!",
                xp_value = 15,
            ),
        ],
        exam_tip     = "PV→VG→LV. lvextend + resize2fs/xfs_growfs. pvmove = Daten auf neue Disk migrieren.",
        memory_tip   = "Drei Schichten: Physical(Hardware)→Group(Pool)→Logical(nutzbar). Wie Schachteln.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.08",
        chapter      = 22,
        title        = "btrfs: Modernes Copy-on-Write Dateisystem",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'ext4 ist solide. btrfs ist die Zukunft.\n"
            " Eingebauter RAID. Snapshots. Checksums.\n"
            " Keine separaten Tools — alles im Dateisystem.'"
        ),
        why_important = (
            "btrfs ist ein modernes Dateisystem mit RAID, Snapshots und CoW.\n"
            "Wird in modernen Distributionen zunehmend genutzt (openSUSE, Fedora)."
        ),
        explanation  = (
            "BTRFS — B-TREE FILESYSTEM:\n\n"
            "ERSTELLEN:\n"
            "  mkfs.btrfs /dev/sdb\n"
            "  mkfs.btrfs -L DataPool /dev/sdb\n"
            "  mkfs.btrfs -d raid1 /dev/sdb /dev/sdc  RAID 1\n\n"
            "SUBVOLUMES:\n"
            "  btrfs subvolume create /mnt/data/@home\n"
            "  btrfs subvolume list /mnt/data\n"
            "  btrfs subvolume delete /mnt/data/@home\n\n"
            "SNAPSHOTS:\n"
            "  btrfs subvolume snapshot /mnt/data/@home /mnt/data/@home_snap\n"
            "  btrfs subvolume snapshot -r /mnt/data/@home /mnt/data/@home_snap  (ro)\n\n"
            "DISK HINZUFÜGEN (RAID erweitern):\n"
            "  btrfs device add /dev/sdd /mnt/data\n"
            "  btrfs balance start /mnt/data\n\n"
            "STATUS & HEALTH:\n"
            "  btrfs filesystem df /mnt/data\n"
            "  btrfs filesystem show /mnt/data\n"
            "  btrfs device stats /mnt/data\n"
            "  btrfs scrub start /mnt/data  (Checksummen prüfen)\n\n"
            "COMPRESS:\n"
            "  mount -o compress=zstd /dev/sdb /mnt/data\n"
            "  btrfs property set /mnt/data/file compression zstd"
        ),
        syntax       = "btrfs subvolume create|list|delete|snapshot",
        example      = "btrfs filesystem show /mnt && btrfs subvolume list /mnt",
        task_description = "Zeige btrfs-Befehlsübersicht mit btrfs --help",
        expected_commands = ["btrfs --help"],
        hint_text    = "btrfs --help zeigt alle btrfs-Unterbefehle",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Vorteil von btrfs-Snapshots gegenüber LVM-Snapshots?",
                options  = [
                    "btrfs-Snapshots sind im Dateisystem integriert und benötigen kein separates LVM-Setup",
                    "btrfs-Snapshots sind schneller",
                    "btrfs-Snapshots benötigen keine extra Speicherplatz",
                    "btrfs-Snapshots funktionieren ohne Root-Rechte",
                ],
                correct  = 0,
                explanation = "btrfs hat Snapshots nativ. LVM braucht separaten CoW-Bereich. btrfs: direkt auf Subvolume.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "btrfs subvolume create/list/snapshot. mkfs.btrfs -d raid1. btrfs scrub = Checksummen.",
        memory_tip   = "btrfs = Batterie inklusive: RAID, Snapshots, Checksums — alles eingebaut.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.09",
        chapter      = 22,
        title        = "iSCSI: Block-Storage über Netzwerk",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "RUST: 'Storage-Server. Disks über IP-Netz.\n"
            " iSCSI. Block-Device remote. Als wäre es lokal.\n"
            " SAN ohne teures Fibre Channel.'"
        ),
        why_important = (
            "iSCSI ermöglicht Block-Storage über Ethernet.\n"
            "Standard in modernen Rechenzentren. LPIC-1 Grundkenntnisse."
        ),
        explanation  = (
            "ISCSI — INTERNET SMALL COMPUTER SYSTEM INTERFACE:\n\n"
            "KONZEPT:\n"
            "  iSCSI Target = Storage-Server (stellt Disks bereit)\n"
            "  iSCSI Initiator = Client (nutzt Remote-Disk)\n"
            "  IQN = iSCSI Qualified Name (eindeutige ID)\n"
            "  Format: iqn.2024-01.com.example:storage1\n\n"
            "CLIENT (INITIATOR) KONFIGURATION:\n"
            "  apt install open-iscsi\n"
            "  systemctl start iscsid\n\n"
            "TARGET ENTDECKEN:\n"
            "  iscsiadm -m discovery -t sendtargets -p 192.168.1.50\n"
            "  → Zeigt verfügbare Targets\n\n"
            "TARGET VERBINDEN:\n"
            "  iscsiadm -m node --login\n"
            "  iscsiadm -m node -T iqn.2024-01.com.example:lun1 \\\n"
            "    -p 192.168.1.50 --login\n\n"
            "SESSIONS:\n"
            "  iscsiadm -m session        Aktive Sessions\n"
            "  iscsiadm -m session -P 3   Details\n\n"
            "VERWENDUNG:\n"
            "  lsblk                       Neue Disk sehen (/dev/sdb)\n"
            "  fdisk /dev/sdb              Partitionieren\n"
            "  mkfs.ext4 /dev/sdb1\n\n"
            "TRENNEN:\n"
            "  iscsiadm -m node --logout"
        ),
        syntax       = "iscsiadm -m discovery -t sendtargets -p ISCSI_SERVER",
        example      = "iscsiadm -m session && lsblk | grep -v loop",
        task_description = "Zeige iscsiadm-Optionen mit iscsiadm --help | head -20",
        expected_commands = ["iscsiadm --help"],
        hint_text    = "iscsiadm --help zeigt alle iSCSI-Verwaltungsoptionen",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Unterschied zwischen iSCSI Target und iSCSI Initiator?",
                options  = [
                    "Target = Server (stellt Storage bereit), Initiator = Client (verbindet sich)",
                    "Target = Client, Initiator = Server",
                    "Beide sind dasselbe — nur verschiedene Namen",
                    "Target = Hardware, Initiator = Software",
                ],
                correct  = 0,
                explanation = "Target = Storage-Server. Initiator = Client der den Storage nutzt. Standard-Client-Server.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "iscsiadm -m discovery = Target finden. -m node --login = verbinden. -m session = aktiv.",
        memory_tip   = "iSCSI = SCSI über IP. Target = Ziel(Server). Initiator = Initiiert Verbindung(Client).",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.10",
        chapter      = 22,
        title        = "SMART: Festplatten-Gesundheit überwachen",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "RUST: 'Festplatten sterben ohne Vorwarnung — meistens.\n"
            " SMART erkennt schlechte Sektoren, Fehler, Temperatur.\n"
            " smartctl. Der Vorbote des Disk-Tods.'"
        ),
        why_important = (
            "SMART (Self-Monitoring Analysis and Reporting Technology)\n"
            "ermöglicht vorausschauendes Disk-Monitoring."
        ),
        explanation  = (
            "SMARTMONTOOLS:\n\n"
            "INSTALLATION:\n"
            "  apt install smartmontools\n\n"
            "STATUS PRÜFEN:\n"
            "  smartctl -a /dev/sda       Vollständiger Report\n"
            "  smartctl -H /dev/sda       Nur Health-Status\n"
            "  smartctl -i /dev/sda       Geräteinformationen\n\n"
            "TESTS:\n"
            "  smartctl -t short /dev/sda   Kurzer Test (~2 Min)\n"
            "  smartctl -t long /dev/sda    Ausführlicher Test (~2 Std)\n"
            "  smartctl -l selftest /dev/sda  Test-Ergebnisse\n\n"
            "WICHTIGE ATTRIBUTE:\n"
            "  5  Reallocated_Sector_Ct  (schlechte Sektoren!)\n"
            "  187 Reported_Uncorrect    (nicht korrigierbare Fehler)\n"
            "  197 Current_Pending_Sector (instabile Sektoren)\n"
            "  198 Offline_Uncorrectable\n"
            "  194 Temperature_Celsius\n\n"
            "SMARTD (DAEMON):\n"
            "  /etc/smartd.conf\n"
            "  DEVICESCAN -a -o on -S on -t -m root\n"
            "  systemctl enable smartd\n\n"
            "NVMe:\n"
            "  smartctl -a /dev/nvme0\n"
            "  nvme smart-log /dev/nvme0"
        ),
        syntax       = "smartctl -a /dev/sda",
        example      = "smartctl -H /dev/sda && smartctl -a /dev/sda | grep -E 'FAILING|Reallocated|Temperature'",
        task_description = "Zeige Disk-Health mit smartctl -H /dev/sda",
        expected_commands = ["smartctl -H /dev/sda"],
        hint_text    = "smartctl -H /dev/sda zeigt den SMART-Gesundheitsstatus der Disk",
        quiz_questions = [
            QuizQuestion(
                question = "Welches SMART-Attribut zeigt umgelagerte (schlechte) Sektoren?",
                options  = [
                    "Reallocated_Sector_Ct (Attribut 5)",
                    "Temperature_Celsius (Attribut 194)",
                    "Power_On_Hours (Attribut 9)",
                    "Load_Cycle_Count (Attribut 193)",
                ],
                correct  = 0,
                explanation = "Reallocated_Sector_Ct: Anzahl schlechter Sektoren die umgelagert wurden. > 0 = Warnsignal.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "smartctl -a = alles | -H = Health | -t short/long = Test. smartd = Daemon für Monitoring.",
        memory_tip   = "SMART = vorausschauend. Reallocated Sectors = schlechte Blöcke. Null = gut.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.11",
        chapter      = 22,
        title        = "Dateisystem-Wartung: e2fsck, xfs_repair",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "RUST: 'Stromausfall. Filesystem-Fehler.\n"
            " e2fsck. fsck. Ungemountetes Filesystem reparieren.\n"
            " Vorsicht: niemals auf gemountetes FS anwenden!'"
        ),
        why_important = (
            "Filesystem-Reparatur ist kritisches Sysadmin-Wissen.\n"
            "LPIC-1 Topic 104.2 testet fsck und e2fsck."
        ),
        explanation  = (
            "FILESYSTEM-PRÜFUNG & REPARATUR:\n\n"
            "GRUNDREGEL: NIEMALS auf gemountetes FS anwenden!\n\n"
            "FSCK (generisch):\n"
            "  fsck /dev/sdb1           Auto-Erkennung des FS-Typs\n"
            "  fsck -a /dev/sdb1        Automatisch reparieren\n"
            "  fsck -n /dev/sdb1        Nur prüfen, nicht reparieren\n"
            "  fsck -t ext4 /dev/sdb1   Expliziter Typ\n\n"
            "E2FSCK (ext2/3/4):\n"
            "  e2fsck -f /dev/sdb1      Force check\n"
            "  e2fsck -y /dev/sdb1      Alle Fragen mit 'y' beantworten\n"
            "  e2fsck -p /dev/sdb1      Automatisch (wie fsck -a)\n\n"
            "TUNE2FS:\n"
            "  tune2fs -c 20 /dev/sdb1   Nach 20 Mounts prüfen\n"
            "  tune2fs -i 30d /dev/sdb1  Nach 30 Tagen prüfen\n"
            "  tune2fs -l /dev/sdb1      Label, UUID, Optionen lesen\n\n"
            "XFS:\n"
            "  xfs_repair /dev/sdc1      XFS reparieren\n"
            "  xfs_check /dev/sdc1       Prüfen (veraltet)\n"
            "  xfs_db -r /dev/sdc1       XFS Debugging\n\n"
            "AUTOMATISCH BEIM BOOT:\n"
            "  /etc/fstab 6. Feld: 0=nie, 1=root, 2=andere"
        ),
        syntax       = "e2fsck -f /dev/DEVICE  (ungemountet!)",
        example      = "umount /dev/sdb1 && e2fsck -f /dev/sdb1 && mount /dev/sdb1 /mnt",
        task_description = "Zeige e2fsck-Optionen mit e2fsck --help",
        expected_commands = ["e2fsck --help"],
        hint_text    = "e2fsck --help zeigt alle Optionen für ext2/3/4 Filesystem-Check",
        quiz_questions = [
            QuizQuestion(
                question = "Was bedeutet das 6. Feld (pass) in /etc/fstab?",
                options  = [
                    "0=kein fsck, 1=root (fsck zuerst), 2=andere FS (nach root)",
                    "Priorität beim Mounten",
                    "Anzahl der Backup-Kopien",
                    "Mount-Flags Nummer",
                ],
                correct  = 0,
                explanation = "Feld 6 (pass): 0=nie automatisch prüfen, 1=root wird zuerst geprüft, 2=danach.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "e2fsck -f = force | -y = auto-yes | -p = automatisch. NIEMALS auf gemountetes FS!",
        memory_tip   = "fsck = Filesystem Check. -y = autoматisch reparieren. Immer erst umounten!",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.12",
        chapter      = 22,
        title        = "Disk-Partitionierung: gdisk & parted",
        mtype        = "CONSTRUCT",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "RUST: 'fdisk für MBR. gdisk für GPT.\n"
            " parted für beide. 2TB+ Disks brauchen GPT.\n"
            " Kenn alle drei Tools — das Examen fragt alle.'"
        ),
        why_important = (
            "Partitionierung mit gdisk und parted ist LPIC-1 Topic 104.1.\n"
            "GPT ist der moderne Standard, MBR für Legacy."
        ),
        explanation  = (
            "PARTITIONIERUNGS-TOOLS:\n\n"
            "FDISK (MBR, < 2TB):\n"
            "  fdisk /dev/sdb      Interaktiv\n"
            "  fdisk -l /dev/sdb   Partitionen anzeigen\n"
            "  Befehle: n=new p=print d=delete t=type w=write q=quit\n\n"
            "GDISK (GPT, > 2TB):\n"
            "  gdisk /dev/sdb      Interaktiv (wie fdisk)\n"
            "  gdisk -l /dev/sdb   Anzeigen\n"
            "  Befehle: n=new p=print d=delete t=type w=write\n"
            "  Partition Types: 8300=Linux, 8200=swap, ef00=EFI\n\n"
            "PARTED (MBR + GPT):\n"
            "  parted /dev/sdb print\n"
            "  parted /dev/sdb mklabel gpt\n"
            "  parted /dev/sdb mkpart primary 0% 10GB\n"
            "  parted /dev/sdb rm 1\n"
            "  parted -s /dev/sdb mkpart primary ext4 10GB 100%\n\n"
            "PARTPROBE / UDEVADM:\n"
            "  partprobe /dev/sdb    Kernel über neue Partitionen informieren\n"
            "  udevadm settle        Warten bis udev fertig ist\n\n"
            "GPT VS MBR:\n"
            "  MBR: max 4 Primär, 2TB, BIOS\n"
            "  GPT: 128 Partitionen, > 2TB, UEFI (auch BIOS-kompatibel)"
        ),
        syntax       = "gdisk /dev/sdb  |  parted /dev/sdb print",
        example      = "parted -l && gdisk -l /dev/sda",
        task_description = "Zeige Partitionstabelle mit parted -l",
        expected_commands = ["parted -l"],
        hint_text    = "parted -l zeigt alle Partitionstabellen aller Disks",
        quiz_questions = [
            QuizQuestion(
                question = "Welches Partitionierungs-Tool sollte für Disks > 2TB verwendet werden?",
                options  = [
                    "gdisk oder parted (GPT-fähig)",
                    "fdisk (unterstützt beliebige Größen)",
                    "cfdisk (beste Unterstützung)",
                    "diskutil (Linux-Standard)",
                ],
                correct  = 0,
                explanation = "fdisk ist MBR-only (max 2TB). gdisk und parted können GPT erstellen (> 2TB, 128 Partitionen).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "fdisk=MBR(max2TB) | gdisk=GPT | parted=beides. GPT: 128 Partitionen, > 2TB, UEFI.",
        memory_tip   = "g in gdisk = GPT. parted = partition editor (GPT + MBR). MBR = Max Bigger Relief (2TB).",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.13",
        chapter      = 22,
        title        = "Swap: Auslagerungsspeicher verwalten",
        mtype        = "CONSTRUCT",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "RUST: 'RAM voll. OOM Killer droht.\n"
            " Swap. Auslagerungsspeicher. Disk statt RAM.\n"
            " Partition oder Swapfile. mkswap. swapon.'"
        ),
        why_important = (
            "Swap-Verwaltung ist LPIC-1 Grundwissen.\n"
            "mkswap, swapon/swapoff und /etc/fstab-Einträge."
        ),
        explanation  = (
            "SWAP VERWALTUNG:\n\n"
            "SWAP-PARTITION:\n"
            "  mkswap /dev/sdb2          Swap-Partition formatieren\n"
            "  swapon /dev/sdb2          Aktivieren\n"
            "  swapoff /dev/sdb2         Deaktivieren\n"
            "  swapon --show             Aktiver Swap anzeigen\n"
            "  free -h                   RAM + Swap gesamt\n\n"
            "/ETC/FSTAB:\n"
            "  UUID=xxx  none  swap  sw  0 0\n\n"
            "SWAPFILE (keine Partition nötig):\n"
            "  fallocate -l 4G /swapfile   4GB Datei\n"
            "  chmod 600 /swapfile\n"
            "  mkswap /swapfile\n"
            "  swapon /swapfile\n"
            "  echo '/swapfile none swap sw 0 0' >> /etc/fstab\n\n"
            "SWAPPINESS:\n"
            "  sysctl vm.swappiness         Aktueller Wert (0-100)\n"
            "  sysctl -w vm.swappiness=10   Weniger Swap nutzen\n"
            "  0 = Swap nur im Notfall\n"
            "  60 = Standard\n"
            "  100 = Aggressiv auslagern\n\n"
            "OOM KILLER:\n"
            "  /proc/PID/oom_score         OOM-Priorität\n"
            "  echo -17 > /proc/PID/oom_adj  Prozess schützen"
        ),
        syntax       = "mkswap DEVICE && swapon DEVICE",
        example      = "swapon --show && free -h",
        task_description = "Zeige aktiven Swap mit swapon --show",
        expected_commands = ["swapon --show"],
        hint_text    = "swapon --show zeigt alle aktiven Swap-Bereiche",
        quiz_questions = [
            QuizQuestion(
                question = "Welche Berechtigungen muss eine Swapfile haben?",
                options  = [
                    "chmod 600 (nur root darf lesen/schreiben)",
                    "chmod 644 (alle dürfen lesen)",
                    "chmod 755 (ausführbar)",
                    "chmod 700 (nur root, alle Operationen)",
                ],
                correct  = 0,
                explanation = "Swapfile mit chmod 600: nur root. Ohne korrekte Rechte: swapon verweigert.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "mkswap = formatieren | swapon/swapoff = aktivieren/deaktivieren | vm.swappiness=0-100",
        memory_tip   = "Swapfile: fallocate → chmod 600 → mkswap → swapon. Dann in fstab für Boot.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.14",
        chapter      = 22,
        title        = "Device Mapper: dm-crypt & dm-multipath",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "PHANTOM",
        story        = (
            "PHANTOM: 'Alles was zwischen Block-Device und Filesystem liegt.\n"
            " Device Mapper. dm-crypt = LUKS. dm-multipath = Pfade.\n"
            " Das Fundament von LUKS, LVM und iSCSI-Multipath.'"
        ),
        why_important = (
            "Device Mapper ist das Framework unter LUKS, LVM und Multipath.\n"
            "Verständnis hilft beim Debugging von Storage-Problemen."
        ),
        explanation  = (
            "DEVICE MAPPER:\n\n"
            "KONZEPT:\n"
            "  Device Mapper = Kernel-Framework für virtuelle Block-Devices\n"
            "  Basiert auf Mappings: Input-Block → Output-Block(s)\n\n"
            "DM-CRYPT (LUKS):\n"
            "  /dev/sdb → dm-crypt → /dev/mapper/secret_vol\n"
            "  cryptsetup luksOpen /dev/sdb secret_vol\n"
            "  → /dev/mapper/secret_vol = entschlüsseltes Device\n\n"
            "DM-MULTIPATH:\n"
            "  Mehrere Pfade zu einem Storage (Redundanz + Load Balancing)\n"
            "  Typisch für SAN/iSCSI\n"
            "  multipath -ll       Alle Multipfade anzeigen\n"
            "  /dev/mapper/mpathX  Multipath-Device\n\n"
            "DMSETUP:\n"
            "  dmsetup ls          Alle Device-Mapper-Devices\n"
            "  dmsetup info /dev/mapper/mpathX\n"
            "  dmsetup table       Mapping-Tabelle anzeigen\n\n"
            "DEVICE-MAPPER DEVICES:\n"
            "  /dev/mapper/  = Alle DM-Devices\n"
            "  ls /dev/mapper/\n"
            "  → vg0-lv0  (LVM-LVs)\n"
            "  → luks-xxx  (LUKS)\n"
            "  → mpathX    (Multipath)"
        ),
        syntax       = "dmsetup ls  /  ls /dev/mapper/",
        example      = "dmsetup ls && ls /dev/mapper/",
        task_description = "Zeige Device-Mapper-Devices mit dmsetup ls",
        expected_commands = ["dmsetup ls"],
        hint_text    = "dmsetup ls zeigt alle aktiven Device-Mapper-Devices",
        quiz_questions = [
            QuizQuestion(
                question = "Wo erscheinen Device-Mapper-Devices im Dateisystem?",
                options  = [
                    "/dev/mapper/",
                    "/dev/dm/",
                    "/dev/devmap/",
                    "/sys/mapper/",
                ],
                correct  = 0,
                explanation = "/dev/mapper/ enthält alle DM-Devices (LVM-LVs, LUKS, Multipath).",
                xp_value = 15,
            ),
        ],
        exam_tip     = "Device Mapper = Framework. /dev/mapper/ = DM-Devices. dmsetup ls = anzeigen.",
        memory_tip   = "Device Mapper = Vermittler zwischen physisch und logisch. LUKS/LVM nutzen ihn.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.15",
        chapter      = 22,
        title        = "Dateisystem-Typen: Vergleich & Wahl",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "RUST: 'ext4, xfs, btrfs, vfat, ntfs.\n"
            " Welches wofür?\n"
            " Das Examen fragt. Kenne die Eigenschaften.'"
        ),
        why_important = (
            "Kenntnis der Linux-Dateisysteme und ihrer Eigenschaften ist\n"
            "fundamentales LPIC-1 Wissen (Topic 104.2)."
        ),
        explanation  = (
            "DATEISYSTEM-VERGLEICH:\n\n"
            "EXT4:\n"
            "  Standard auf Debian/Ubuntu\n"
            "  Journaling, robust, gut getestet\n"
            "  Max Dateigröße: 16TB | Max FS: 1EiB\n"
            "  mkfs.ext4 /dev/sdb1\n\n"
            "XFS:\n"
            "  Standard auf Red Hat/CentOS\n"
            "  Sehr gut für große Dateien und parallele I/O\n"
            "  Nur vergrößern (nicht verkleinern!)\n"
            "  mkfs.xfs /dev/sdb1 | xfs_growfs /mountpoint\n\n"
            "BTRFS:\n"
            "  Modern, integriertes RAID/Snapshots/Checksums\n"
            "  Standard auf openSUSE, Fedora\n"
            "  mkfs.btrfs /dev/sdb1\n\n"
            "VFAT/FAT32:\n"
            "  Kompatibel mit Windows, USB-Sticks\n"
            "  Keine Berechtigungen, kein Journaling\n"
            "  mkfs.vfat /dev/sdb1\n\n"
            "NTFS:\n"
            "  Windows-Dateisystem\n"
            "  Lesen/Schreiben mit ntfs-3g (Linux)\n"
            "  mount -t ntfs-3g /dev/sdb1 /mnt\n\n"
            "TMPFS (RAM):\n"
            "  /tmp ist oft tmpfs (im RAM)\n"
            "  mount -t tmpfs tmpfs /mnt/ram -o size=1G"
        ),
        syntax       = "mkfs.ext4|xfs|vfat|btrfs DEVICE",
        example      = "df -T && lsblk -f",
        task_description = "Zeige Dateisystem-Typen aller Mounts mit df -T",
        expected_commands = ["df -T"],
        hint_text    = "df -T zeigt den Typ jedes gemounteten Dateisystems",
        quiz_questions = [
            QuizQuestion(
                question = "Welches Dateisystem kann NUR vergrößert, aber NICHT verkleinert werden?",
                options  = [
                    "XFS",
                    "ext4",
                    "btrfs",
                    "vfat",
                ],
                correct  = 0,
                explanation = "XFS kann mit xfs_growfs wachsen. Verkleinern ist nicht möglich — wichtig für die Planung!",
                xp_value = 15,
            ),
        ],
        exam_tip     = "ext4=Standard Debian | xfs=Standard RHEL | btrfs=Modern | vfat=Windows-kompatibel",
        memory_tip   = "XFS = eXtreme File System. Wächst nur. ext4 = Extended 4. Kann schrumpfen.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.16",
        chapter      = 22,
        title        = "UUID & Labels: Geräte-Identifizierung",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "RUST: 'Gerätename /dev/sdb kann sich ändern.\n"
            " UUID nicht. Label nicht.\n"
            " Nutze UUID in /etc/fstab — nicht /dev/sdb.'"
        ),
        why_important = (
            "UUIDs identifizieren Partitionen stabiler als Gerätenamen.\n"
            "LPIC-1 testet blkid und die Nutzung von UUIDs in fstab."
        ),
        explanation  = (
            "UUID & LABELS:\n\n"
            "UUID ANZEIGEN:\n"
            "  blkid                     Alle UUIDs\n"
            "  blkid /dev/sdb1           Für ein Device\n"
            "  lsblk -f                  Tree mit UUIDs\n"
            "  ls -la /dev/disk/by-uuid/ Symlinks\n\n"
            "LABEL SETZEN:\n"
            "  e2label /dev/sdb1 data    ext2/3/4 Label\n"
            "  xfs_admin -L data /dev/sdb1  xfs Label\n"
            "  mkfs.ext4 -L data /dev/sdb1  Beim Erstellen\n\n"
            "/ETC/FSTAB MIT UUID:\n"
            "  UUID=6f1b4a8c-xxxx-xxxx-xxxx  /mnt/data  ext4  defaults  0 2\n\n"
            "/ETC/FSTAB MIT LABEL:\n"
            "  LABEL=data  /mnt/data  ext4  defaults  0 2\n\n"
            "WARUM UUID STATT GERÄTENAME?\n"
            "  /dev/sdb kann sich nach Reboot zu /dev/sda ändern\n"
            "  UUID ändert sich nur bei Neuformatierung\n"
            "  LABEL kann von Admin gesetzt werden\n\n"
            "SYMLINKS:\n"
            "  /dev/disk/by-uuid/xxx → ../../sdb1\n"
            "  /dev/disk/by-label/data → ../../sdb1\n"
            "  /dev/disk/by-id/xxx → ../../sdb1"
        ),
        syntax       = "blkid /dev/sdb1  (UUID anzeigen)",
        example      = "blkid && lsblk -f | head -20",
        task_description = "Zeige alle Partitions-UUIDs mit blkid",
        expected_commands = ["blkid"],
        hint_text    = "blkid zeigt UUID, TYPE und LABEL aller Block-Devices",
        quiz_questions = [
            QuizQuestion(
                question = "Warum sollte man UUIDs statt Gerätenamen in /etc/fstab verwenden?",
                options  = [
                    "UUIDs sind stabil — Gerätenamen können sich nach Reboot ändern",
                    "UUIDs sind kürzer als Gerätenamen",
                    "Gerätenamen werden von systemd nicht unterstützt",
                    "UUIDs mounten schneller",
                ],
                correct  = 0,
                explanation = "Gerätenamen (sda/sdb) können sich nach Boot ändern. UUID bleibt bis zur Neuformatierung stabil.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "blkid = UUID/Label/Type. e2label = ext Label. lsblk -f = Übersicht. UUID in fstab = stabil.",
        memory_tip   = "UUID = Universally Unique ID. Wie Personalausweis — ändert sich nicht.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.17",
        chapter      = 22,
        title        = "Backup-Strategien: tar, rsync, dd",
        mtype        = "SCAN",
        xp           = 85,
        speaker      = "RUST",
        story        = (
            "RUST: 'Backup ist keine Option. Es ist Pflicht.\n"
            " tar für Archive. rsync für inkrementell.\n"
            " dd für Block-Level. Kenne alle drei.'"
        ),
        why_important = (
            "Backup-Tools sind fundamentales Sysadmin-Wissen.\n"
            "LPIC-1 testet tar, rsync und dd für verschiedene Backup-Szenarien."
        ),
        explanation  = (
            "BACKUP TOOLS:\n\n"
            "TAR (TAPE ARCHIVE):\n"
            "  tar czf backup.tar.gz /home\n"
            "  tar xzf backup.tar.gz -C /restore\n"
            "  tar cjf backup.tar.bz2 /home   (bzip2)\n"
            "  tar cJf backup.tar.xz /home    (xz, beste Kompression)\n"
            "  tar --listed-incremental=snap.snar -czf incr.tar.gz /home\n\n"
            "RSYNC (INKREMENTELL):\n"
            "  rsync -av /source/ /dest/          Lokal\n"
            "  rsync -avz /source/ user@host:/dest/  Remote\n"
            "  rsync -av --delete /source/ /dest/    Spiegel (löscht extra Dateien)\n"
            "  rsync -av --backup /source/ /dest/    Backup alter Dateien\n"
            "  rsync -av -n /source/ /dest/          Dry run\n\n"
            "DD (BLOCK-LEVEL):\n"
            "  dd if=/dev/sda of=/backup/sda.img    Disk-Image\n"
            "  dd if=/dev/sda of=/dev/sdb            Disk klonen\n"
            "  dd if=/dev/sda of=- | gzip > sda.img.gz\n"
            "  dd if=/dev/zero of=/dev/sdb bs=4M     Disk löschen\n\n"
            "BACKUP PRINZIPIEN:\n"
            "  3-2-1 Regel: 3 Kopien, 2 Medien, 1 extern\n"
            "  Vollbackup → Differentiell → Inkrementell"
        ),
        syntax       = "tar czf backup.tar.gz /pfad  /  rsync -av /src/ /dst/",
        example      = "tar czf /backup/home-$(date +%F).tar.gz /home && ls -lh /backup/",
        task_description = "Zeige tar-Version und Hilfe mit tar --version",
        expected_commands = ["tar --version"],
        hint_text    = "tar --version zeigt die installierte tar-Version",
        quiz_questions = [
            QuizQuestion(
                question = "Was bedeutet die Option `--delete` bei rsync?",
                options  = [
                    "Löscht im Ziel Dateien die in der Quelle nicht mehr existieren",
                    "Löscht Quelldateien nach dem Sync",
                    "Löscht das Ziel vor dem Sync",
                    "Löscht temporäre Dateien während des Sync",
                ],
                correct  = 0,
                explanation = "--delete: Ziel = perfekter Spiegel der Quelle. Dateien nur im Ziel werden gelöscht.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "tar czf=Erstellen xzf=Extrahieren. rsync -av=verbose --delete=Mirror. dd if=of=",
        memory_tip   = "tar = Archiv (Zip). rsync = Spiegel (Delta). dd = Block-Klon.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 15),
    ),

    Mission(
        mission_id   = "22.18",
        chapter      = 22,
        title        = "Dateisystem-Monitoring: df, du, iostat",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "RUST",
        story        = (
            "RUST: 'Disk voll. System reagiert nicht.\n"
            " df, du, iostat. Monitoring.\n"
            " Sehe es kommen bevor es passiert.'"
        ),
        why_important = (
            "Disk-Monitoring ist Grundlage jeder Systemverwaltung.\n"
            "LPIC-1 testet df, du und grundlegendes iostat."
        ),
        explanation  = (
            "DISK MONITORING:\n\n"
            "DF (DISK FREE):\n"
            "  df -h              Human-readable, alle FS\n"
            "  df -T              Mit Dateisystem-Typ\n"
            "  df -ih             Inodes (wichtig!)\n"
            "  df -h /home        Nur /home\n\n"
            "DU (DISK USAGE):\n"
            "  du -sh /var/*      Größe jedes Unterverzeichnisses\n"
            "  du -sh /var/log    Spezifisches Verzeichnis\n"
            "  du -ah /home | sort -rh | head -20  Größte Dateien\n"
            "  du --max-depth=1 /home\n\n"
            "NCDU (INTERAKTIV):\n"
            "  ncdu /home         Interaktiver Disk-Browser\n\n"
            "IOSTAT (I/O STATISTIKEN):\n"
            "  iostat             Basis I/O-Statistiken\n"
            "  iostat -x          Extended (await, util%)\n"
            "  iostat 2 5         Alle 2 Sek, 5 Mal\n"
            "  iostat -h          Human-readable\n\n"
            "IOTOP (PROZESS I/O):\n"
            "  iotop              Interaktiv\n"
            "  iotop -o           Nur aktive Prozesse\n\n"
            "LSBLK:\n"
            "  lsblk              Block-Device-Baum\n"
            "  lsblk -f           Mit Dateisystem-Info"
        ),
        syntax       = "df -h | du -sh /pfad/* | iostat -x",
        example      = "df -h && df -ih && du -sh /var/log/* 2>/dev/null | sort -rh | head -10",
        task_description = "Zeige Disk-Nutzung mit df -h",
        expected_commands = ["df -h"],
        hint_text    = "df -h zeigt Disk-Nutzung aller Dateisysteme in menschenlesbarem Format",
        quiz_questions = [
            QuizQuestion(
                question = "Was zeigt `df -ih`?",
                options  = [
                    "Inode-Nutzung aller Dateisysteme (human-readable)",
                    "Disk-Nutzung in Hexadezimal",
                    "Inode-Hexadezimal-IDs",
                    "Hidden-File-Nutzung",
                ],
                correct  = 0,
                explanation = "df -i = Inodes statt Blöcke. -h = human-readable. 100% Inodes = kein neuer File (auch wenn Platz!)",
                xp_value = 15,
            ),
        ],
        exam_tip     = "df -h = Platz | df -ih = Inodes | du -sh = Verzeichnis-Größe | iostat = I/O.",
        memory_tip   = "df = Disk Free (Gesamt). du = Disk Usage (Detail). iostat = I/O Statistik.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.19",
        chapter      = 22,
        title        = "Verschlüsselte Container: VeraCrypt & ecryptfs",
        mtype        = "SCAN",
        xp           = 80,
        speaker      = "CIPHER",
        story        = (
            "CIPHER: 'LUKS für Partitionen. VeraCrypt für portable Container.\n"
            " ecryptfs für Home-Verzeichnisse.\n"
            " Verschiedene Tools für verschiedene Anwendungsfälle.'"
        ),
        why_important = (
            "Dateisystem-Verschlüsselung über LUKS hinaus.\n"
            "Portable Container und Home-Verschlüsselung."
        ),
        explanation  = (
            "VERSCHLÜSSELUNGS-TOOLS:\n\n"
            "VERACRYPT (portable Container):\n"
            "  Erstellt verschlüsselte Dateien die als Volumes gemountet werden\n"
            "  veracrypt --create container.vc\n"
            "  veracrypt container.vc /mnt/vc\n"
            "  veracrypt -d container.vc\n"
            "  Plausible Deniability (versteckte Volumes)\n\n"
            "ECRYPTFS (Home-Verschlüsselung):\n"
            "  ecryptfs-setup-private   Privates Verzeichnis einrichten\n"
            "  ecryptfs-mount-private   Mounten\n"
            "  ~/.Private/              Verschlüsseltes Verzeichnis\n"
            "  ~/Private/               Entschlüsselter Mountpunkt\n"
            "  ecryptfs-migrate-home -u USER  Ganzes Home verschlüsseln\n\n"
            "LOOP-DEVICE MIT LUKS:\n"
            "  dd if=/dev/zero of=container.img bs=1M count=100\n"
            "  cryptsetup luksFormat container.img\n"
            "  losetup /dev/loop0 container.img\n"
            "  cryptsetup luksOpen /dev/loop0 mycontainer\n"
            "  mkfs.ext4 /dev/mapper/mycontainer\n"
            "  mount /dev/mapper/mycontainer /mnt/secure"
        ),
        syntax       = "ecryptfs-setup-private  /  veracrypt --create FILE",
        example      = "ls ~/.Private/ && mount | grep ecryptfs",
        task_description = "Zeige ecryptfs-Tools mit ecryptfs-setup-private --help",
        expected_commands = ["ecryptfs-setup-private --help"],
        hint_text    = "ecryptfs-setup-private --help zeigt Optionen für Home-Verschlüsselung",
        quiz_questions = [
            QuizQuestion(
                question = "Was ist der Vorteil von VeraCrypt gegenüber LUKS?",
                options  = [
                    "Portable Container-Dateien die auf jedem OS geöffnet werden können",
                    "Schnellere Verschlüsselung",
                    "Besser für ganze Disks",
                    "Kein Passwort nötig",
                ],
                correct  = 0,
                explanation = "VeraCrypt erstellt portable verschlüsselte Dateien — nutzbar auf Linux/Windows/macOS.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "LUKS=Partition | VeraCrypt=portable Container | ecryptfs=Home-Verzeichnis.",
        memory_tip   = "ecrypt = encrypt home. VeraCrypt = portables Schloss für Dateien.",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.20",
        chapter      = 22,
        title        = "Storage Performance: fio & bonnie++",
        mtype        = "SCAN",
        xp           = 75,
        speaker      = "RUST",
        story        = (
            "RUST: 'IOPS. Throughput. Latency.\n"
            " fio testet Disk-Performance.\n"
            " Kenn deine Disk — bevor die Applikation leidet.'"
        ),
        why_important = (
            "Disk-Performance-Testing ist wichtig für Sizing und Debugging.\n"
            "fio ist der Standard für Block-Device-Benchmarks."
        ),
        explanation  = (
            "STORAGE PERFORMANCE TESTING:\n\n"
            "FIO (FLEXIBLE I/O TESTER):\n"
            "  fio --name=randread --ioengine=libaio \\\n"
            "    --iodepth=1 --rw=randread --bs=4k \\\n"
            "    --direct=1 --size=1G --filename=/dev/sdb\n\n"
            "EINFACHE TESTS:\n"
            "  fio --name=seq_write --rw=write --bs=1M --size=4G --filename=/tmp/test\n"
            "  fio --name=rand_read --rw=randread --bs=4K --size=1G --filename=/dev/sdb\n\n"
            "WICHTIGE METRIKEN:\n"
            "  IOPS = I/O Operations Per Second (zufälliger Zugriff)\n"
            "  Throughput = MB/s (sequentieller Transfer)\n"
            "  Latency = ms/µs pro Operation\n\n"
            "DD FÜR SIMPLE TESTS:\n"
            "  dd if=/dev/zero of=/tmp/test bs=1M count=1000 oflag=direct\n"
            "  dd if=/tmp/test of=/dev/null bs=1M iflag=direct\n\n"
            "IOSTAT WÄHREND TEST:\n"
            "  iostat -x 1  (in separatem Terminal)\n"
            "  util% > 90 = gesättigte Disk"
        ),
        syntax       = "fio --name=test --rw=read|write|randread|randwrite --bs=4k --size=1G",
        example      = "dd if=/dev/zero of=/tmp/speedtest bs=1M count=500 oflag=direct && rm /tmp/speedtest",
        task_description = "Zeige Disk-Performance mit dd if=/dev/zero of=/tmp/test bs=1M count=100 oflag=direct",
        expected_commands = ["dd if=/dev/zero of=/tmp/test"],
        hint_text    = "dd if=/dev/zero schreibt Nullbytes — misst Schreib-Throughput",
        quiz_questions = [
            QuizQuestion(
                question = "Was misst IOPS (I/O Operations Per Second)?",
                options  = [
                    "Anzahl zufälliger Ein-/Ausgabe-Operationen pro Sekunde",
                    "Megabytes pro Sekunde",
                    "CPU-Zyklen pro Sekunde",
                    "Netzwerk-Pakete pro Sekunde",
                ],
                correct  = 0,
                explanation = "IOPS = wichtig für Datenbanken (zufälliger Zugriff). Throughput (MB/s) = wichtig für sequentielle I/O.",
                xp_value = 15,
            ),
        ],
        exam_tip     = "fio = flexibler Benchmark. dd = simpler Speed-Test. iostat = Live-Monitoring.",
        memory_tip   = "IOPS = zufälliger Zugriff (Datenbank). Throughput = sequentiell (Backup/Video).",
        gear_reward  = None,
        faction_reward = ("Root Collective", 10),
    ),

    Mission(
        mission_id   = "22.quiz",
        chapter      = 22,
        title        = "QUIZ — Storage Advanced Wissenstest",
        mtype        = "QUIZ",
        xp           = 200,
        speaker      = "SYSTEM",
        story        = (
            "SYSTEM: 'Storage Advanced Quiz initialisiert.\n"
            " RAID, LVM, Quotas, iSCSI, btrfs.\n"
            " Beweise dein Storage-Wissen.'"
        ),
        why_important = "Prüfungsvorbereitung: Storage, Dateisysteme und Backup.",
        explanation  = "Quiz über alle Storage-Themen.",
        syntax       = "",
        example      = "",
        task_description = "Beantworte alle Storage-Fragen.",
        expected_commands = [],
        hint_text    = "RAID Level, mdadm, Quotas, LVM-Snapshots, btrfs, UUID",
        quiz_questions = [
            QuizQuestion(
                question = "Welches RAID-Level bietet sowohl hohe Performance als auch Redundanz, benötigt aber 4 Disks?",
                options  = [
                    "RAID 10 (Mirror + Stripe)",
                    "RAID 5",
                    "RAID 6",
                    "RAID 0",
                ],
                correct  = 0,
                explanation = "RAID 10: Erst mirrorn (RAID 1), dann stripen (RAID 0). Min. 4 Disks. 50% Kapazität.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Was passiert wenn der LVM-Snapshot überläuft (overflow)?",
                options  = [
                    "Der Snapshot wird invalid und unbrauchbar",
                    "Das Original-Volume wird beschädigt",
                    "Der Snapshot wächst automatisch",
                    "Der Snapshot wird auf Disk gespeichert",
                ],
                correct  = 0,
                explanation = "Snapshot overflow: Snapshot-Device wird als invalid markiert. Nicht mehr mountbar.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Welcher Befehl zeigt die aktuelle Disk-Quota-Nutzung aller User?",
                options  = [
                    "repquota -a",
                    "quotacheck -a",
                    "quotaon -a",
                    "quota --all",
                ],
                correct  = 0,
                explanation = "repquota -a zeigt Report aller User auf allen Filesystemen mit Quotas.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Welches Kommando-Paar erstellt und aktiviert eine Swapfile?",
                options  = [
                    "mkswap /swapfile && swapon /swapfile",
                    "format /swapfile && activateswap /swapfile",
                    "dd /swapfile && mount /swapfile",
                    "newswap /swapfile && startswap /swapfile",
                ],
                correct  = 0,
                explanation = "mkswap initialisiert die Datei als Swap. swapon aktiviert sie für das System.",
                xp_value = 25,
            ),
        ],
        exam_tip     = "RAID 5 min 3 Disks, 1 Fehler tolerant. LVM Snapshot: lvcreate -s. Quotas: repquota.",
        memory_tip   = "Storage = RAID(Sicherheit) + LVM(Flexibilität) + Quotas(Kontrolle).",
        gear_reward  = "storage_master_badge",
        faction_reward = ("Root Collective", 30),
    ),

    Mission(
        mission_id   = "22.boss",
        chapter      = 22,
        title        = "BOSS: STORAGE DAEMON v22.0",
        mtype        = "BOSS",
        xp           = 725,
        speaker      = "RUST",
        story        = (
            "RUST: 'Ich bin STORAGE DAEMON. Wächter der Daten.\n"
            " RAID-Arrays. LVM-Volumes. Quota-Tabellen.\n"
            " Kein Byte entkommt meiner Kontrolle!\n"
            " Beweise dass du die Daten des Systems schützen kannst!'"
        ),
        why_important = "Abschluss-Boss für Storage — testet alle Disk-Management-Kenntnisse.",
        explanation  = (
            "STORAGE ADVANCED — ABSCHLUSS:\n\n"
            "Du solltest jetzt können:\n"
            "  ✓ RAID Level 0,1,5,6,10 erklären und erstellen\n"
            "  ✓ mdadm für Software-RAID nutzen\n"
            "  ✓ LVM vollständig verwalten (PV/VG/LV)\n"
            "  ✓ LVM Snapshots erstellen und nutzen\n"
            "  ✓ Disk Quotas mit edquota konfigurieren\n"
            "  ✓ btrfs Subvolumes und Snapshots\n"
            "  ✓ iSCSI Client konfigurieren\n"
            "  ✓ SMART für Disk-Health nutzen\n"
            "  ✓ UUID in fstab korrekt einsetzen\n"
            "  ✓ Backup mit tar, rsync, dd\n\n"
            "FINALE PRÜFUNG:\n"
            "  cat /proc/mdstat\n"
            "  vgs && lvs\n"
            "  repquota -a\n"
            "  df -h && df -ih\n"
            "  blkid"
        ),
        ascii_art    = """
  ███████╗████████╗ ██████╗ ██████╗  █████╗  ██████╗ ███████╗
  ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝
  ███████╗   ██║   ██║   ██║██████╔╝███████║██║  ███╗█████╗
  ╚════██║   ██║   ██║   ██║██╔══██╗██╔══██║██║   ██║██╔══╝
  ███████║   ██║   ╚██████╔╝██║  ██║██║  ██║╚██████╔╝███████╗
  ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
      ██████╗  █████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗
      ██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║
      ██║  ██║███████║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
      ██║  ██║██╔══██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
      ██████╔╝██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

  ┌─ STORAGE STATUS ─────────────────────────────┐
  │  RAID-5: DEGRADED    ::  LVM: VOLUME FULL    │
  │  Quota: EXCEEDED     ::  btrfs: SNAPSHOT ERR │
  │  mdadm: DRIVE FAIL   ::  iSCSI: DISCONNECT   │
  └──────────────────────────────────────────────┘

  ⚡ CHAOSWERK FACTION :: CHAPTER 22 BOSS ⚡""",
        story_transitions = [
            "STORAGE DAEMON lässt RAID-5 degradieren. /proc/mdstat zeigt FAILED.",
            "mdadm --add fügt neue Disk ein. Rebuild läuft. Er versucht zu stoppen.",
            "LVM-Volume voll. lvextend rettet die Daten. Er verliert die Kontrolle.",
            "Finaler Scan: df -h, blkid, /proc/mdstat — alles grün. Rust fällt.",
        ],
        syntax       = "cat /proc/mdstat && vgs && lvs && df -h && blkid",
        example      = "cat /proc/mdstat && vgs && lvs -a && df -h",
        task_description = "Führe finalen Storage-Audit durch: df -h && blkid",
        expected_commands = ["df -h"],
        hint_text    = "df -h zeigt den Speicher-Status aller Dateisysteme",
        quiz_questions = [
            QuizQuestion(
                question = "Ein RAID-5-Array mit 4 Laufwerken (je 1 TB) hat welche nutzbare Kapazität und Fehlertoleranz?",
                options  = [
                    "3 TB nutzbar, toleriert 1 Laufwerksausfall",
                    "4 TB nutzbar, toleriert 1 Laufwerksausfall",
                    "2 TB nutzbar, toleriert 2 Laufwerksausfälle",
                    "3 TB nutzbar, toleriert 2 Laufwerksausfälle",
                ],
                correct  = 0,
                explanation = "RAID-5 verwendet (N-1) Laufwerke für Daten, 1 für Parität (verteilt). Bei 4×1 TB = 3 TB nutzbar. Toleranz: 1 Ausfall. Für 2 Ausfälle wäre RAID-6 nötig.",
                xp_value = 25,
            ),
            QuizQuestion(
                question = "Du willst einem bestehenden LVM-Volume-Group (vg_data) ein neues Physical Volume hinzufügen. Was ist die korrekte Reihenfolge?",
                options  = [
                    "pvcreate /dev/sdb → vgextend vg_data /dev/sdb",
                    "vgextend vg_data /dev/sdb → pvcreate /dev/sdb",
                    "lvcreate vg_data /dev/sdb → vgextend vg_data /dev/sdb",
                    "vgcreate vg_data /dev/sdb → vgextend vg_data /dev/sdb",
                ],
                correct  = 0,
                explanation = "Zuerst muss das Gerät mit pvcreate als Physical Volume initialisiert werden, dann kann es mit vgextend zur VG hinzugefügt werden. Ohne pvcreate schlägt vgextend fehl.",
                xp_value = 30,
            ),
            QuizQuestion(
                question = "Was passiert, wenn du 'lvextend -L +10G /dev/vg_data/lv_home' ausführst?",
                options  = [
                    "Das Logical Volume wird um 10G erweitert, aber das Dateisystem bleibt unverändert",
                    "Das Logical Volume UND das Dateisystem werden um 10G erweitert",
                    "Das Logical Volume wird auf genau 10G gesetzt",
                    "Der Befehl schlägt fehl, weil kein Dateisystem-Typ angegeben wurde",
                ],
                correct  = 0,
                explanation = "lvextend ändert nur die LV-Größe. Das Dateisystem muss separat mit 'resize2fs' (ext4) oder 'xfs_growfs' (xfs) erweitert werden — außer man nutzt 'lvextend -r' (--resizefs).",
                xp_value = 35,
            ),
            QuizQuestion(
                question = "Welcher Befehl aktiviert Disk-Quotas für einen Benutzer 'alice' auf /dev/sda1 (usrquota gemountet)?",
                options  = [
                    "edquota -u alice",
                    "quota -u alice",
                    "setquota alice /dev/sda1",
                    "quotaon -u alice /dev/sda1",
                ],
                correct  = 0,
                explanation = "edquota -u alice öffnet den Quota-Editor für Benutzer alice zum Setzen von Soft/Hard Limits. quota -u alice zeigt nur aktuelle Nutzung. quotaon aktiviert das Quota-System generell.",
                xp_value = 30,
            ),
            QuizQuestion(
                question = "Was ist der Hauptvorteil von btrfs gegenüber ext4 für einen LPIC-1-Kandidaten?",
                options  = [
                    "Eingebaute Snapshots, Copy-on-Write und Online-Resize ohne Unmount",
                    "Schnelleres fsck durch Journal",
                    "Bessere Kompatibilität mit Windows-Systemen",
                    "Kleinere Metadaten-Overhead als ext4",
                ],
                correct  = 0,
                explanation = "btrfs bietet nativen CoW (Copy-on-Write), Snapshots mit btrfs subvolume snapshot, und kann online vergrößert werden. ext4 hat fsck-Journal, aber keine nativen Snapshots.",
                xp_value = 30,
            ),
        ],
        exam_tip     = "Storage Advanced ABGESCHLOSSEN. RAID/LVM/Quota/iSCSI/btrfs = LPIC-1 104.x komplett.",
        memory_tip   = "Daten schützen: RAID(Redundanz) + LVM(Flexibilität) + Quotas(Fairness).",
        gear_reward  = "storage_master_badge",
        faction_reward = ("Root Collective", 60),
    ),
]
