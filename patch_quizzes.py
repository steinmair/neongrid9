#!/usr/bin/env python3
"""
NeonGrid-9 Quiz Patch Script
Adds quiz_questions to all missions that are missing them.
"""

import re
import sys
import os

# ── Quiz content per mission ID ───────────────────────────────────────────────
# Each entry: list of (question, [options], correct_letter, explanation, xp)

QUIZ_DATA = {

    # ── CH04: Partitions ──────────────────────────────────────────────────────
    "4.01": [
        ("Welche maximale Festplattengröße unterstützt MBR?",
         ["A) 4 TB", "B) 2 TB", "C) 8 TB", "D) 1 TB"],
         "B", "MBR nutzt 32-bit LBA → max 2 TB. GPT nutzt 64-bit → praktisch unbegrenzt.", 20),
        ("Wie viele primäre Partitionen erlaubt MBR maximal?",
         ["A) 8", "B) 16", "C) 4", "D) 128"],
         "C", "MBR: max 4 primäre Partitionen. Mehr geht nur mit Extended+Logical.", 20),
    ],
    "4.02": [
        ("Welcher fdisk-Befehl schreibt Änderungen permanent auf die Platte?",
         ["A) s", "B) w", "C) q", "D) p"],
         "B", "'w' in fdisk = Write. Ohne 'w' werden keine Änderungen gespeichert.", 20),
        ("Was ist der Hex-Code für eine Linux-Partition in fdisk?",
         ["A) ef", "B) 82", "C) 83", "D) 8e"],
         "C", "83 = Linux, 82 = Linux Swap, 8e = Linux LVM, ef = EFI System.", 20),
    ],
    "4.03": [
        ("Was ist der gdisk-Typcode für eine EFI System Partition?",
         ["A) 8300", "B) 8200", "C) ef00", "D) fd00"],
         "C", "ef00 = EFI System, 8300 = Linux filesystem, 8200 = Linux swap.", 20),
        ("Welches Tool ist nativ für GPT-Partitionierung optimiert?",
         ["A) fdisk", "B) cfdisk", "C) parted", "D) gdisk"],
         "D", "gdisk = GPT disk, nativ für GUID Partition Table. fdisk kann GPT lesen, aber gdisk versteht es vollständig.", 20),
    ],
    "4.04": [
        ("Was bedeutet 'mklabel msdos' in parted?",
         ["A) Erstellt MS-DOS-Partition", "B) Erstellt MBR-Partitionstabelle", "C) Erstellt ext2-Dateisystem", "D) Fehler: ungültiger Befehl"],
         "B", "In parted heißt MBR 'msdos'. 'mklabel gpt' für GPT, 'mklabel msdos' für MBR.", 20),
        ("Wann schreibt parted Änderungen auf die Festplatte?",
         ["A) Erst nach 'w'", "B) Erst nach 'commit'", "C) Sofort bei jedem Befehl", "D) Erst nach 'quit'"],
         "C", "parted schreibt SOFORT! Kein 'w' wie bei fdisk. Das ist die kritische Falle.", 20),
    ],
    "4.05": [
        ("Welcher Befehl erstellt ein ext4-Dateisystem auf /dev/sda1?",
         ["A) mkfs /dev/sda1", "B) format -t ext4 /dev/sda1", "C) mkfs.ext4 /dev/sda1", "D) newfs ext4 /dev/sda1"],
         "C", "mkfs.ext4 /dev/sda1 oder mkfs -t ext4 /dev/sda1 sind gleichwertig.", 20),
        ("Was bedeutet 'mkfs ohne Typ-Suffix' (nur mkfs /dev/sda1)?",
         ["A) Erstellt ext4", "B) Erstellt ext2 (kein Journaling)", "C) Fehler", "D) Erstellt XFS"],
         "B", "mkfs ohne Suffix = mkfs.ext2 — veraltet und ohne Journaling!", 20),
    ],
    "4.07": [
        ("Welcher Befehl vergrößert ein XFS-Dateisystem?",
         ["A) xfs_growfs /dev/sda2", "B) xfs_growfs /mountpoint", "C) resize2fs /dev/sda2", "D) xfs_resize /data"],
         "B", "xfs_growfs braucht den MOUNTPOINT, nicht das Device! Das ist die XFS-Falle im Examen.", 20),
        ("XFS kann...",
         ["A) vergrößert und verkleinert werden", "B) nur vergrößert, nicht verkleinert werden", "C) nur verkleinert werden", "D) nicht geändert werden ohne Neuformat"],
         "B", "XFS kann NUR vergrößert werden. Verkleinern ist nicht möglich — Datenverlust!", 20),
    ],
    "4.08": [
        ("Was ist die korrekte Reihenfolge zum Einrichten von Swap?",
         ["A) swapon → mkswap → fstab", "B) mkswap → fstab → swapon", "C) mkswap → swapon → fstab", "D) fstab → mkswap → swapon"],
         "C", "Erst mkswap (formatieren), dann swapon (aktivieren), dann fstab (permanent).", 20),
        ("Welcher fstab-Eintrag aktiviert eine Swap-Partition permanent?",
         ["A) /dev/sda2  /swap  swap  defaults  0  0", "B) /dev/sda2  none  swap  sw  0  0", "C) /dev/sda2  swap  ext4  defaults  0  0", "D) /dev/sda2  none  none  swap  0  0"],
         "B", "Swap-fstab: Gerät, 'none' als Mountpunkt, 'swap' als Typ, 'sw' als Option.", 20),
    ],
    "4.10": [
        ("Was tust du, wenn umount 'device is busy' meldet?",
         ["A) Reboot", "B) umount -f", "C) lsof /mountpoint", "D) mount -r"],
         "C", "lsof /mountpoint oder fuser -m /mountpoint zeigt, welche Prozesse das FS belegen.", 20),
        ("Welcher Befehl mountet alle Dateisysteme aus /etc/fstab?",
         ["A) mount /all", "B) mount --fstab", "C) mount -a", "D) fstab-mount"],
         "C", "mount -a = alle aus fstab mounten. Gut zum Testen nach fstab-Änderungen.", 20),
    ],
    "4.12": [
        ("Wann darf fsck auf einer Partition laufen?",
         ["A) Immer, auch während des Betriebs", "B) Nur auf unmounted Partitionen", "C) Nur bei Reboot", "D) Nur auf Read-Only-Partitionen"],
         "B", "fsck NIEMALS auf gemounteten Partitionen! Nur unmounted oder Read-Only.", 20),
        ("Was macht fsck -n?",
         ["A) Kein Backup erstellen", "B) Nur prüfen ohne Reparieren (Dry Run)", "C) Nicht interaktiv", "D) Nein zu allen Fragen"],
         "B", "fsck -n = nur prüfen, nichts reparieren. Sicher für erste Diagnose.", 20),
    ],
    "4.13": [
        ("Was zeigt 'lsblk -f'?",
         ["A) Nur Festplattengrößen", "B) Dateisystem-Typ, UUID und Mountpoint", "C) Nur Partitionstypen", "D) Festplatten-Fehler"],
         "B", "lsblk -f = kombiniert Gerätebaum mit FSTYPE, UUID und MOUNTPOINTS.", 20),
        ("Warum nutzt man UUID statt /dev/sda1 in /etc/fstab?",
         ["A) UUID ist kürzer", "B) UUID ist stabiler bei Geräteänderungen", "C) /dev/sda1 funktioniert nicht", "D) UUID ist schneller"],
         "B", "/dev/sdX kann sich ändern (neue USB-Geräte). UUID bleibt immer gleich — stabiler!", 20),
    ],

    # ── CH05: Permissions ─────────────────────────────────────────────────────
    "5.03": [
        ("Was macht 'chown :gruppe datei' (nur Doppelpunkt + Gruppe)?",
         ["A) Setzt Owner und Gruppe", "B) Setzt nur die Gruppe", "C) Fehler", "D) Löscht den Owner"],
         "B", "chown :gruppe = nur Gruppe setzen (wie chgrp). chown user:gruppe = beides.", 20),
        ("Welcher Befehl ändert Besitzer rekursiv für ein ganzes Verzeichnis?",
         ["A) chown user /verz", "B) chown -R user:group /verz", "C) chgrp -r user /verz", "D) chmod -R user /verz"],
         "B", "chown -R = rekursiv. Ändert Owner und Gruppe aller Dateien im Verzeichnis.", 20),
    ],
    "5.08": [
        ("Was ist der Unterschied zwischen locate und find?",
         ["A) locate sucht in Echtzeit, find aus Datenbank", "B) locate nutzt Datenbank (schnell), find sucht aktuell (langsam)", "C) Kein Unterschied", "D) locate nur für Verzeichnisse"],
         "B", "locate = schnell via Datenbank (kann veraltet sein). find = langsam aber immer aktuell.", 20),
        ("Welcher Befehl aktualisiert die locate-Datenbank?",
         ["A) locate -update", "B) updatedb", "C) find -update", "D) locate --refresh"],
         "B", "updatedb aktualisiert die mlocate-Datenbank. Ohne updatedb zeigt locate veraltete Ergebnisse.", 20),
    ],
    "5.10": [
        ("Was bedeutet ctime bei einer Datei?",
         ["A) Creation time (Erstellungszeit)", "B) Change time (Metadaten geändert)", "C) Current time", "D) Copy time"],
         "B", "ctime ≠ Creation! ctime = change time (Metadaten wie Rechte, Owner geändert). mtime = Inhalt geändert.", 20),
        ("Welcher Befehl zeigt den tatsächlichen Typ einer Datei (z.B. ob sie wirklich eine Textdatei ist)?",
         ["A) stat datei", "B) ls -l datei", "C) file datei", "D) type datei"],
         "C", "file erkennt Dateitype am Inhalt (Magic Bytes), nicht an der Endung.", 20),
    ],

    # ── CH06: Shell ───────────────────────────────────────────────────────────
    "6.01": [
        ("Was ist der Unterschied zwischen 'VAR=wert' und 'export VAR=wert'?",
         ["A) Kein Unterschied", "B) export macht die Variable für Kind-Prozesse verfügbar", "C) VAR=wert ist sicherer", "D) export ist permanenter"],
         "B", "export = Umgebungsvariable (an Kinder vererbt). VAR=wert = lokal in aktueller Shell.", 20),
        ("Was enthält $?",
         ["A) Den Dateinamen des aktuellen Skripts", "B) Den Exit-Code des letzten Befehls", "C) Die Prozess-ID der Shell", "D) Den aktuellen Pfad"],
         "B", "$? = Exit-Code. 0 = Erfolg, 1-255 = Fehler. Wichtig nach jedem Befehl prüfen!", 20),
    ],
    "6.02": [
        ("Was macht '!!' in der Bash?",
         ["A) Führt letzten Befehl als Root aus", "B) Wiederholt den letzten Befehl", "C) Zeigt Befehlshistorie", "D) Löscht History"],
         "B", "!! = letzten Befehl wiederholen. 'sudo !!' = letzten Befehl als root — sehr praktisch!", 20),
        ("Was ist HISTSIZE?",
         ["A) Maximale Größe von ~/.bash_history auf Disk", "B) Anzahl der History-Einträge im RAM", "C) Maximale Befehlslänge", "D) Anzahl der History-Dateien"],
         "B", "HISTSIZE = Einträge im RAM (aktuelle Session). HISTFILESIZE = Einträge in ~/.bash_history.", 20),
    ],
    "6.04": [
        ("Was macht 'tee' in einer Pipeline?",
         ["A) Leitet stdout in /dev/null", "B) Schreibt auf stdout UND in eine Datei gleichzeitig", "C) Dupliziert stderr", "D) Verbindet zwei Pipes"],
         "B", "tee = T-Stück: Ausgabe geht sowohl auf Terminal als auch in Datei. tee -a = append.", 20),
        ("Was passiert bei 'cmd1 | cmd2'?",
         ["A) cmd2 liest aus einer Datei", "B) stdout von cmd1 wird stdin von cmd2", "C) Beide Befehle laufen nacheinander", "D) Fehler bei Leerzeichen"],
         "B", "Pipe | verbindet stdout des ersten Befehls mit stdin des zweiten.", 20),
    ],
    "6.07": [
        ("Was macht 'tail -f /var/log/syslog'?",
         ["A) Zeigt letzten Fehler", "B) Zeigt Log-Datei live/in Echtzeit", "C) Zeigt nur Fehler", "D) Filtert Log"],
         "B", "tail -f = follow = Live-Monitoring. Neue Zeilen werden sofort angezeigt.", 20),
        ("Was ist der Unterschied zwischen tail -f und tail -F?",
         ["A) Kein Unterschied", "B) -F funktioniert auch nach Log-Rotation (öffnet neue Datei)", "C) -f ist schneller", "D) -F zeigt mehr Zeilen"],
         "B", "tail -F = --follow=name, öffnet die Datei neu nach Log-Rotation. Wichtig für Produktions-Logs.", 20),
    ],
    "6.09": [
        ("Was bedeutet $NF in awk?",
         ["A) Kein Feld gefunden", "B) Letzte Spalte (Number of Fields)", "C) Neue Funktion", "D) Null-Feld"],
         "B", "$NF = letzte Spalte. $1 = erste, $2 = zweite. NR = aktuelle Zeilennummer.", 20),
        ("Welcher awk-Befehl nutzt Doppelpunkt als Feldtrenner?",
         ["A) awk '$:' /etc/passwd", "B) awk -F: '{print $1}' /etc/passwd", "C) awk --sep: /etc/passwd", "D) awk ':' /etc/passwd"],
         "B", "awk -F: = Feldtrenner Doppelpunkt. Klassisch für /etc/passwd.", 20),
    ],
    "6.10": [
        ("Was ist der Unterschied zwischen 'cp -a' und 'cp -p'?",
         ["A) Kein Unterschied", "B) -a = archive (Rechte+Zeit+Symlinks), -p = nur Rechte+Zeit", "C) -p ist komplett, -a nur Rechte", "D) -a für Verzeichnisse, -p für Dateien"],
         "B", "cp -a = archive, erhält alles inkl. Symlinks. cp -p = preserve (Rechte+Zeitstempel).", 20),
        ("Was passiert bei 'rm -rf /verzeichnis/'?",
         ["A) Nur leere Verzeichnisse werden gelöscht", "B) Alle Dateien und Verzeichnisse werden sofort gelöscht (kein Undo!)", "C) Fragt nach Bestätigung", "D) Verschiebt in Trash"],
         "B", "rm -rf = rekursiv force = sofort gelöscht, kein Undo, kein Papierkorb!", 20),
    ],

    # ── CH07: Processes ───────────────────────────────────────────────────────
    "7.01": [
        ("Was ist PID 1 bei einem modernen Linux-System?",
         ["A) bash", "B) kernel", "C) systemd (oder init)", "D) cron"],
         "C", "PID 1 = systemd (oder init bei alten Systemen). Alle anderen Prozesse sind Kinder davon.", 20),
        ("Was ist ein Zombie-Prozess?",
         ["A) Prozess ohne CPU-Zeit", "B) Beendeter Prozess, dessen Exit-Status noch nicht vom Elternprozess abgerufen wurde", "C) Prozess mit negativer Priorität", "D) Daemon ohne Terminal"],
         "B", "Zombie (Z-State): Prozess fertig, aber Eltern hat wait() noch nicht aufgerufen. Zeigt Z in ps.", 20),
    ],
    "7.03": [
        ("Was bedeuten die drei Load-Average-Werte in top/uptime?",
         ["A) RAM, CPU, Disk", "B) Letzte 1, 5 und 15 Minuten", "C) Min, Avg, Max CPU", "D) 3 CPU-Kerne"],
         "B", "Load Average: 3 Werte für 1/5/15 Minuten. Load 1.0 auf 1-Core = 100% ausgelastet.", 20),
        ("Mit welcher Taste sortiert man 'top' nach RAM-Nutzung?",
         ["A) R", "B) P", "C) M", "D) S"],
         "C", "top: M = nach Memory, P = nach CPU, N = nach PID. 'k' = kill.", 20),
    ],
    "7.05": [
        ("Was macht 'Ctrl+Z' bei einem laufenden Prozess?",
         ["A) Beendet den Prozess", "B) Pausiert den Prozess (SIGSTOP) und schickt ihn in den Hintergrund", "C) Wechselt in den Hintergrund ohne Pause", "D) Öffnet neues Terminal"],
         "B", "Ctrl+Z = SIGSTOP = Prozess pausieren. Dann 'bg' zum Weiterlaufen im Hintergrund.", 20),
        ("Was macht nohup?",
         ["A) Kein Hang-Up: Prozess läuft weiter auch nach SSH-Logout", "B) Höhere Priorität", "C) Keine CPU-Nutzung", "D) Nur für Hintergrundprozesse"],
         "A", "nohup = no hangup. Prozess ignoriert SIGHUP beim SSH-Logout. Ausgabe → nohup.out.", 20),
    ],
    "7.07": [
        ("Was bedeutet si/so > 0 in vmstat?",
         ["A) System-Idle > 0", "B) Das System lagert Speicher aus (swap in/out) — RAM-Problem!", "C) I/O-Operationen", "D) System-Interrupts"],
         "B", "vmstat si=swap in, so=swap out. Beide > 0 = System swappt = RAM knapp!", 20),
        ("Was zeigt 'free -h' im Feld 'available'?",
         ["A) Freier RAM (physisch leer)", "B) Tatsächlich verfügbarer RAM (inkl. Cache der freigegeben werden kann)", "C) Swap-Größe", "D) Shared Memory"],
         "B", "'available' ist wichtiger als 'free'! Enthält freien + freigebbaren Cache.", 20),
    ],
    "7.08": [
        ("Wie findest du, welcher Prozess Port 80 belegt?",
         ["A) ps -p 80", "B) lsof -i :80", "C) top --port 80", "D) netstat -pid 80"],
         "B", "lsof -i :80 zeigt Prozess auf Port 80. ss -tulpn | grep :80 geht auch.", 20),
        ("Was tust du, wenn umount 'device is busy' meldet?",
         ["A) Reboot sofort", "B) lsof /mnt oder fuser -m /mnt", "C) umount --ignore-busy", "D) rm -rf /mnt/*"],
         "B", "lsof /mountpoint zeigt welche Prozesse das Dateisystem offen halten.", 20),
    ],
    "7.09": [
        ("Was macht 'Ctrl+A d' in screen?",
         ["A) Alle Sessions löschen", "B) Session detachen (läuft im Hintergrund weiter)", "C) Neues Fenster öffnen", "D) Screen beenden"],
         "B", "Ctrl+A d = detach. Session läuft weiter. 'screen -r' zum Wiederverbinden.", 20),
        ("Welcher Befehl listet alle laufenden screen-Sessions auf?",
         ["A) screen -list", "B) screen -ls", "C) screen --show", "D) sessions -screen"],
         "B", "screen -ls zeigt alle Sessions. screen -r SESSION zum Verbinden.", 20),
    ],

    # ── CH08: Regex/Vi ────────────────────────────────────────────────────────
    "8.01": [
        ("Was ist der Unterschied zwischen BRE und ERE in grep?",
         ["A) BRE unterstützt mehr Sonderzeichen", "B) ERE nutzt + ? | ohne Backslash, BRE braucht \\+", "C) Kein Unterschied", "D) BRE = für Dateien, ERE = für Stdin"],
         "B", "ERE (Extended): + ? | ( ) ohne Backslash. BRE (Basic): braucht \\+ \\? usw.", 20),
        ("Welcher Flag aktiviert Extended Regular Expressions in grep?",
         ["A) grep -B", "B) grep -E (oder egrep)", "C) grep -X", "D) grep -r"],
         "B", "grep -E oder egrep = Extended Regex. LPIC-1 prüft: 'Wie ERE aktivieren?'", 20),
    ],
    "8.02": [
        ("Was macht 'grep -v ^$' mit einer Datei?",
         ["A) Zeigt nur leere Zeilen", "B) Entfernt/filtert Leerzeilen heraus", "C) Zählt Zeilen", "D) Fehler: ungültiger Ausdruck"],
         "B", "grep -v = invertieren. ^$ = leere Zeile (Anfang direkt Zeilenende). Also: alle nicht-leeren Zeilen.", 20),
        ("Was gibt 'grep -c MUSTER datei' zurück?",
         ["A) Die gefundenen Zeilen mit Zeilennummern", "B) Nur die Anzahl der Treffer (keine Zeilen)", "C) Alle Dateien mit Treffern", "D) Kontext-Zeilen"],
         "B", "grep -c = count = gibt nur die Anzahl der Treffer-Zeilen zurück.", 20),
    ],
    "8.03": [
        ("Was macht 'sed s/alt/neu/' ohne /g-Flag?",
         ["A) Ersetzt alle Vorkommen", "B) Ersetzt nur das ERSTE Vorkommen in jeder Zeile", "C) Fehler", "D) Ersetzt letztes Vorkommen"],
         "B", "Ohne /g: nur erstes Vorkommen pro Zeile. Mit /g: alle. PRÜFUNGS-FALLE!", 20),
        ("Was macht sed -i?",
         ["A) Ignoriert Fehler", "B) Ändert die Datei direkt (In-Place)", "C) Interaktiver Modus", "D) Case-insensitive"],
         "B", "sed -i = In-Place, ändert die Datei direkt. Ohne -i: nur Ausgabe auf stdout.", 20),
    ],
    "8.04": [
        ("Was druckt 'awk '{print $NF}' datei'?",
         ["A) Erste Spalte", "B) Letzte Spalte jeder Zeile", "C) Anzahl der Felder", "D) Fehler"],
         "B", "$NF = letztes Feld (Number of Fields). NR = aktuelle Zeilennummer.", 20),
        ("Welcher awk-Befehl filtert Zeilen, die 'root' enthalten?",
         ["A) awk 'root' datei", "B) awk '/root/ {print}' datei", "C) awk -g 'root' datei", "D) awk --match root datei"],
         "B", "awk '/MUSTER/' = filtert Zeilen mit Muster. Ohne Aktion = print (Standard).", 20),
    ],
    "8.05": [
        ("Welche vi-Taste bringt dich IMMER in den Normal-Modus?",
         ["A) Enter", "B) q", "C) ESC", "D) Ctrl+C"],
         "C", "ESC = immer Normal-Modus. Mehrfach drücken schadet nicht. Essenziell für vi!", 20),
        ("Wie speicherst und beendest du vi?",
         ["A) :save", "B) :wq oder ZZ", "C) Ctrl+S", "D) :exit!"],
         "B", ":wq = write+quit. ZZ = Kurzform. :q! = quit ohne Speichern.", 20),
    ],
    "8.06": [
        ("Was macht 'dd' in vi (im Normal-Modus)?",
         ["A) Löscht ein Zeichen", "B) Löscht die aktuelle Zeile (in Puffer)", "C) Öffnet neues Dokument", "D) Dupliziert die Zeile"],
         "B", "dd = delete line. Der Inhalt ist im Puffer! dd + p = Zeile verschieben.", 20),
        ("Wie kopiert man 3 Zeilen in vi?",
         ["A) 3yy", "B) copy 3", "C) yank 3", "D) c3"],
         "A", "3yy = yank (kopieren) 3 Zeilen. Dann 'p' zum Einfügen nach dem Cursor.", 20),
    ],
    "8.07": [
        ("Wie ersetzt man in vi ALLE Vorkommen von 'alt' durch 'neu' in der ganzen Datei?",
         ["A) :s/alt/neu/", "B) :%s/alt/neu/g", "C) :replace alt neu", "D) /alt → :change/neu"],
         "B", ":%s/alt/neu/g = % (ganze Datei) s (substitute) /g (global). :s ohne % = nur aktuelle Zeile.", 20),
        ("Was bedeutet ':q!' in vi?",
         ["A) Speichern und beenden", "B) Beenden OHNE zu speichern (force quit)", "C) Quit interaktiv", "D) Fehler: ungültiger Befehl"],
         "B", ":q! = force quit ohne Speichern. Das ! überschreibt die Änderungs-Warnung.", 20),
    ],
    "8.08": [
        ("Wie schreibt man 'eine oder mehrere Ziffern' als POSIX-Klasse in grep?",
         ["A) grep '[digit]+' datei", "B) grep '[[:digit:]]\\+' datei", "C) grep '\\d+' datei", "D) grep '[0-9]+' datei"],
         "B", "POSIX: [[:digit:]] in doppelten Klammern. Mit BRE braucht + einen Backslash: \\+", 20),
        ("Was ist der Unterschied zwischen [[:alpha:]] und [a-z]?",
         ["A) Kein Unterschied", "B) [[:alpha:]] ist POSIX-konform und locale-aware", "C) [a-z] ist korrekter", "D) [[:alpha:]] nur für Großbuchstaben"],
         "B", "[[:alpha:]] ist POSIX-offiziell und berücksichtigt Locale (Umlaute etc.). Beide funktionieren aber POSIX ist korrekter.", 20),
    ],
    "8.boss": [
        ("Was macht 'grep -E'?",
         ["A) Erweiterte Ausgabe", "B) Aktiviert Extended Regular Expressions", "C) Ergebnis in Datei", "D) Rekursive Suche"],
         "B", "grep -E = Extended Regex. Ermöglicht + ? | ohne Backslash.", 20),
    ],

    # ── CH09: Network ─────────────────────────────────────────────────────────
    "9.01": [
        ("Wie viele nutzbare Hosts hat ein /24-Netz?",
         ["A) 256", "B) 255", "C) 254", "D) 253"],
         "C", "256 Adressen - 2 (Netz + Broadcast) = 254 nutzbare Hosts.", 20),
        ("Welcher Adressbereich ist ein privates Klasse-C-Netz?",
         ["A) 10.0.0.0/8", "B) 172.16.0.0/12", "C) 192.168.0.0/16", "D) 169.254.0.0/16"],
         "C", "Private Bereiche: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 (RFC 1918).", 20),
    ],
    "9.02": [
        ("Was zeigt 'ip route show'?",
         ["A) Routing-Tabelle des Kernels", "B) Netzwerk-Interfaces", "C) Offene Verbindungen", "D) DNS-Server"],
         "A", "ip route show = Routing-Tabelle. ip addr show = Interfaces+IPs. ip link show = Layer-2.", 20),
        ("Wie deaktiviert man ein Netzwerk-Interface mit ip?",
         ["A) ip link off eth0", "B) ip link set eth0 down", "C) ip addr remove eth0", "D) ifdown eth0"],
         "B", "ip link set DEV down/up. Das moderne Tool ersetzt ifconfig.", 20),
    ],
    "9.03": [
        ("Was zeigt 'ss -tulpn'?",
         ["A) TCP/UDP Listening Ports mit Prozessnamen", "B) Netzwerk-Statistiken", "C) Alle Netzwerk-Geräte", "D) DNS-Anfragen"],
         "A", "ss -tulpn: t=TCP, u=UDP, l=listening, p=Prozess, n=numerisch (keine Namen auflösen).", 20),
        ("Was ist der Unterschied zwischen ss und netstat?",
         ["A) Kein Unterschied", "B) ss ist modern/schneller, netstat ist deprecated", "C) netstat ist moderner", "D) ss nur für UDP"],
         "B", "ss ersetzt netstat. Aber LPIC-1 prüft noch netstat! Beide kennen.", 20),
    ],
    "9.04": [
        ("Wie stoppst du ping nach genau 5 Paketen?",
         ["A) ping --count=5", "B) ping -c 5 HOST", "C) ping -n 5 HOST", "D) ping -p 5 HOST"],
         "B", "ping -c COUNT = Anzahl der Pakete. ping -c 5 host → stoppt nach 5.", 20),
        ("Was ist tracepath im Vergleich zu traceroute?",
         ["A) Identisch", "B) tracepath braucht keine Root-Rechte, traceroute schon", "C) tracepath ist schneller", "D) traceroute ist deprecated"],
         "B", "tracepath: kein Root nötig. traceroute: braucht oft root. Beide zeigen Routing-Pfade.", 20),
    ],
    "9.05": [
        ("Welcher dig-Befehl macht einen Reverse-Lookup (IP → Name)?",
         ["A) dig HOST reverse", "B) dig -x IP", "C) dig PTR IP", "D) dig --reverse IP"],
         "B", "dig -x IP = Reverse DNS Lookup (PTR-Record). host IP funktioniert auch.", 20),
        ("Welche Datei definiert die Reihenfolge von DNS vs. /etc/hosts?",
         ["A) /etc/dns.conf", "B) /etc/nsswitch.conf", "C) /etc/resolv.conf", "D) /etc/hosts.conf"],
         "B", "/etc/nsswitch.conf: hosts: files dns = erst /etc/hosts dann DNS.", 20),
    ],
    "9.06": [
        ("Was ist der sichere SSH-Schlüsseltyp für neue Systeme?",
         ["A) rsa 1024", "B) dsa", "C) ed25519", "D) ecdsa 256"],
         "C", "ed25519 ist modern, sicher und schnell. RSA 4096 geht auch. DSA = veraltet!", 20),
        ("Was macht 'PermitRootLogin no' in sshd_config?",
         ["A) SSH deaktivieren", "B) Root-Login über SSH verbieten", "C) Passwort-Login für root deaktivieren", "D) Root-Befehle blockieren"],
         "B", "PermitRootLogin no = kein direkter Root-SSH. Erst als User, dann sudo.", 20),
    ],
    "9.07": [
        ("Wo wird der Hostname dauerhaft gespeichert?",
         ["A) /etc/sysconfig/network", "B) /etc/hostname", "C) /proc/hostname", "D) /etc/hosts"],
         "B", "/etc/hostname = dauerhafter Hostname. hostnamectl set-hostname NAME schreibt dorthin.", 20),
        ("Was macht nmcli device status?",
         ["A) Startet NetworkManager", "B) Zeigt Status aller Netzwerkgeräte", "C) Konfiguriert DNS", "D) Zeigt Routing-Tabelle"],
         "B", "nmcli device status = Übersicht aller Netzwerkgeräte und deren Verbindungsstatus.", 20),
    ],

    # ── CH10: Users ───────────────────────────────────────────────────────────
    "10.01": [
        ("Welche Datei enthält verschlüsselte Passwörter?",
         ["A) /etc/passwd", "B) /etc/shadow", "C) /etc/password", "D) /etc/login"],
         "B", "/etc/shadow enthält gehashte Passwörter (nur root lesbar). /etc/passwd ist world-readable.", 20),
    ],
    "10.02": [
        ("Was macht 'useradd -m username'?",
         ["A) Erstellt Benutzer ohne Homeverzeichnis", "B) Erstellt Benutzer MIT Homeverzeichnis (/home/username)", "C) Modifiziert bestehenden Benutzer", "D) Erstellt System-Benutzer"],
         "B", "useradd -m = create home directory. Ohne -m: kein /home/username erstellt.", 20),
        ("Welcher Befehl ändert das Passwort eines Benutzers als Root?",
         ["A) useradd --password user", "B) passwd username", "C) chpasswd username", "D) usermod --password user"],
         "B", "passwd USERNAME als root ändert das Passwort für jeden Benutzer.", 20),
    ],
    "10.03": [
        ("Was macht 'groupadd entwickler'?",
         ["A) Benutzer zu Gruppe hinzufügen", "B) Neue Gruppe 'entwickler' erstellen", "C) Gruppenpasswort setzen", "D) Gruppenmitglieder anzeigen"],
         "B", "groupadd GRUPPENNAME erstellt eine neue Gruppe in /etc/group.", 20),
        ("Wie fügt man einen Benutzer zu einer Gruppe hinzu ohne andere Gruppen zu entfernen?",
         ["A) usermod -g gruppe user", "B) usermod -aG gruppe user", "C) groupadd -u user gruppe", "D) gpasswd gruppe user"],
         "B", "usermod -aG = append to Group. Ohne -a würde -G alle anderen Gruppen entfernen!", 20),
    ],
    "10.04": [
        ("Was enthält /etc/passwd pro Zeile (7 Felder)?",
         ["A) user:pass:uid:gid:comment:home:shell", "B) user:uid:gid:home:shell:pass:groups", "C) user:pass:home:shell:uid:gid:comment", "D) uid:user:pass:gid:home:shell:comment"],
         "A", "/etc/passwd: username:password(x):UID:GID:GECOS:Homedir:Shell", 20),
    ],
    "10.05": [
        ("Was macht chage -l username?",
         ["A) Ändert Passwort-Ablauf", "B) Zeigt Passwort-Ablauf-Informationen", "C) Sperrt das Konto", "D) Löscht Ablauf-Daten"],
         "B", "chage -l = list. Zeigt Passwort-Ablauf, letztes Änderungsdatum, etc.", 20),
        ("Wie sperrt man ein Benutzerkonto (kein Login möglich)?",
         ["A) usermod -L username", "B) usermod -d /bin/false username", "C) passwd --lock username", "D) A oder C"],
         "D", "usermod -L = lock (! vor Passwort in shadow). passwd --lock macht dasselbe.", 20),
    ],
    "10.06": [
        ("Wo werden Sudo-Rechte konfiguriert?",
         ["A) /etc/sudoers und /etc/sudoers.d/", "B) /etc/sudo.conf", "C) ~/.sudorc", "D) /etc/pam.d/sudo"],
         "A", "/etc/sudoers (bearbeiten NUR mit visudo!). /etc/sudoers.d/ für zusätzliche Dateien.", 20),
        ("Was macht visudo besonders sicher?",
         ["A) Verschlüsselt die sudoers-Datei", "B) Prüft Syntax vor dem Speichern (verhindert kaputte sudo-Config)", "C) Erstellt Backup automatisch", "D) Setzt Rechte automatisch"],
         "B", "visudo prüft Syntax vor Speicherung. Kaputte sudoers = kein sudo mehr = gesperrt!", 20),
    ],
    "10.07": [
        ("Was ist getent?",
         ["A) Holt Einträge aus Datenbanken (passwd, group, hosts) inkl. LDAP/NIS", "B) Gibt Umgebungsvariablen aus", "C) Zeigt Netzwerk-Entitäten", "D) Listet Benutzer-Entitlements"],
         "A", "getent = get entries. getent passwd username zeigt Benutzerinfos aus allen konfigurierten Quellen (lokal + LDAP).", 20),
    ],
    "10.boss": [
        ("Welcher Befehl zeigt alle Mitglieder einer Gruppe?",
         ["A) groups GRUPPE", "B) getent group GRUPPE", "C) groupmembers GRUPPE", "D) cat /etc/group | grep GRUPPE"],
         "B", "getent group GRUPPE zeigt alle Mitglieder. grep funktioniert auch.", 20),
    ],

    # ── CH11: Logging ─────────────────────────────────────────────────────────
    "11.01": [
        ("Was ist die Syntax einer rsyslog-Regel?",
         ["A) facility.severity  Ziel", "B) severity:facility  Ziel", "C) Ziel  facility.severity", "D) facility → severity → Ziel"],
         "A", "rsyslog: FACILITY.SEVERITY  Ziel. z.B. kern.err /var/log/kernel.log", 20),
        ("Welche Syslog-Facility ist für den Kernel?",
         ["A) system", "B) kern", "C) daemon", "D) local0"],
         "B", "kern = Kernel-Messages. daemon = System-Daemons. mail = Mail-System.", 20),
    ],
    "11.02": [
        ("Welcher journalctl-Befehl zeigt Logs seit heute Morgen?",
         ["A) journalctl --since today", "B) journalctl --since '00:00'", "C) journalctl -today", "D) A oder B"],
         "D", "journalctl --since today oder --since '00:00'. Auch: --since '2024-01-01 08:00'.", 20),
        ("Was macht journalctl -p err?",
         ["A) Zeigt Fehler-Prioritäts-Logs (error und höher)", "B) Zeigt nur exakte 'err'-Meldungen", "C) Prüft Journal-Integrität", "D) Persistenz aktivieren"],
         "A", "-p err = priority filter: zeigt err, crit, alert, emerg (alle schwerwiegenden).", 20),
    ],
    "11.03": [
        ("Was macht logrotate mit dem 'rotate 4'-Parameter?",
         ["A) Log alle 4 Stunden rotieren", "B) Maximal 4 alte Log-Versionen behalten", "C) 4 Log-Dateien pro Verzeichnis", "D) Alle 4 KB rotieren"],
         "B", "rotate N = behalte N alte Versionen. Ältere werden gelöscht.", 20),
        ("Was bedeutet 'compress' in einer logrotate-Konfiguration?",
         ["A) Neue Logs komprimieren", "B) Rotierte Logs mit gzip komprimieren", "C) Log-Kompressionsrate erhöhen", "D) Space-Limit setzen"],
         "B", "compress = rotierte Logs mit gzip packen (.gz). 'delaycompress' = erst beim nächsten Durchlauf.", 20),
    ],
    "11.04": [
        ("Was macht timedatectl set-ntp true?",
         ["A) NTP manuell konfigurieren", "B) Automatische Zeitsynchronisation über NTP aktivieren", "C) Zeitzone setzen", "D) NTP-Server anzeigen"],
         "B", "timedatectl set-ntp true = NTP aktivieren (systemd-timesyncd). False = deaktivieren.", 20),
        ("Was ist hwclock?",
         ["A) Hardware-Clock (BIOS/UEFI-Uhr) lesen und setzen", "B) Software-Clock", "C) NTP-Client", "D) Zeitzone-Tool"],
         "A", "hwclock = Hardware Clock (RTC). hwclock -s = Systemzeit aus HW-Uhr setzen.", 20),
    ],
    "11.05": [
        ("Was ist der crontab-Eintrag für 'jeden Tag um 03:30'?",
         ["A) 3 30 * * *", "B) 30 3 * * *", "C) * * 30 3 *", "D) 0 3 30 * *"],
         "B", "crontab: MIN STD TAG MON WOT. 30 3 * * * = 03:30 jeden Tag.", 20),
        ("Welcher Befehl bearbeitet den crontab des aktuellen Benutzers?",
         ["A) crontab -l", "B) crontab -e", "C) cron -edit", "D) vi /etc/crontab"],
         "B", "crontab -e = edit (öffnet Editor). crontab -l = list (anzeigen). crontab -r = remove!", 20),
    ],
    "11.06": [
        ("Wie plant man einen Job mit at für 'morgen um 14:00'?",
         ["A) at 14:00+1", "B) at 14:00 tomorrow", "C) at --time 14:00 --day tomorrow", "D) at next 14:00"],
         "B", "at 14:00 tomorrow. Weitere: 'at now + 2 hours', 'at midnight'. Befehle per stdin eingeben.", 20),
        ("Welcher Befehl zeigt alle ausstehenden at-Jobs?",
         ["A) at -list", "B) atq", "C) at --queue", "D) jobs --at"],
         "B", "atq = at queue. Zeigt alle geplanten Jobs. atrm JOBNR = löschen.", 20),
    ],
    "11.07": [
        ("Was ist ein systemd-Timer im Vergleich zu cron?",
         ["A) Langsamer als cron", "B) Besser in systemd integriert, mit Abhängigkeiten und Logging", "C) Nur für root", "D) Nur für einmalige Jobs"],
         "B", "systemd Timer: Logging via journalctl, Abhängigkeiten, präzise Zeitsteuerung. Cron: einfacher.", 20),
        ("Was macht OnCalendar=daily in einem systemd-Timer?",
         ["A) Täglich um Mitternacht ausführen", "B) Täglich zur aktuellen Zeit", "C) Alle 24 Stunden ab Start", "D) Einmal pro Kalender"],
         "A", "OnCalendar=daily = täglich um Mitternacht. OnCalendar=weekly = montags 00:00.", 20),
    ],
    "11.08": [
        ("Was macht 'logrotate -d /etc/logrotate.conf'?",
         ["A) Debug: Dry-run ohne Änderungen", "B) Löscht Log-Dateien", "C) Deaktiviert logrotate", "D) Zeigt Log-Statistiken"],
         "A", "logrotate -d = debug/dry-run. Zeigt was passieren würde ohne etwas zu ändern.", 20),
        ("Wo liegen anwendungsspezifische logrotate-Konfigurationen?",
         ["A) /etc/logrotate.conf", "B) /etc/logrotate.d/", "C) /var/log/rotate.d/", "D) ~/.logrotate/"],
         "B", "/etc/logrotate.d/ = Drop-in-Verzeichnis. Jede Anwendung hat eigene Datei dort.", 20),
    ],
    "11.09": [
        ("Wie prüft man die Größe des systemd-Journals?",
         ["A) du -sh /var/log/journal", "B) journalctl --disk-usage", "C) systemctl status journald", "D) ls -lh /var/log/journal"],
         "B", "journalctl --disk-usage zeigt belegten Speicher. journalctl --vacuum-size=500M bereinigt.", 20),
        ("Was ist der Unterschied zwischen persistentem und flüchtigem Journal?",
         ["A) Kein Unterschied nach Reboot", "B) Persistent: /var/log/journal (überlebt Reboot), flüchtig: /run/log/journal", "C) Persistent ist komprimiert", "D) Flüchtig ist schneller"],
         "B", "Storage=persistent in journald.conf → /var/log/journal. Storage=volatile → /run (weg nach Reboot).", 20),
    ],
    "11.10": [
        ("Was macht 'systemctl list-timers'?",
         ["A) Zeigt alle aktiven crontabs", "B) Zeigt alle systemd-Timer mit nächster Ausführung", "C) Listet Timer-Dateien", "D) Startet alle Timer"],
         "B", "systemctl list-timers zeigt Timer, letzten und nächsten Ausführungszeitpunkt.", 20),
        ("Wie aktiviert man einen systemd-Timer dauerhaft?",
         ["A) crontab -e", "B) systemctl enable --now NAME.timer", "C) systemctl start NAME.timer", "D) timerctl enable NAME"],
         "B", "systemctl enable --now NAME.timer = aktivieren + sofort starten.", 20),
    ],
    "11.11": [
        ("Was ist 'batch' im Vergleich zu 'at'?",
         ["A) batch ist interaktiver", "B) batch führt Jobs aus wenn System-Load niedrig genug", "C) batch ist für root", "D) batch läuft täglich"],
         "B", "batch = last-abhängige at-Variante. Führt Job aus wenn Load < 1.5 (konfigurierbar).", 20),
        ("Wie zeigt man den Inhalt eines at-Jobs an?",
         ["A) at -view JOBNR", "B) at -c JOBNR", "C) atq -show JOBNR", "D) cat /var/spool/at/JOBNR"],
         "B", "at -c JOBNR = cat job. Zeigt das vollständige Skript inkl. Umgebungsvariablen.", 20),
    ],
    "11.12": [
        ("Was passiert wenn cron.allow existiert?",
         ["A) Alle außer gelisteten dürfen crontab nutzen", "B) Nur gelistete Benutzer dürfen crontab nutzen", "C) Root kann crontab für alle bearbeiten", "D) cron läuft im allow-only Modus"],
         "B", "cron.allow: nur gelistete Benutzer dürfen crontab. Existiert cron.deny: alle außer gelisteten.", 20),
        ("Was wenn cron.allow existiert aber leer ist?",
         ["A) Alle dürfen cron nutzen", "B) Niemand außer root darf crontab nutzen", "C) Cron-Dienst startet nicht", "D) Nur root-Gruppe"],
         "B", "cron.allow leer = niemand (außer root) darf crontab. Root ist immer erlaubt.", 20),
    ],
    "11.boss": [
        ("Was macht 'journalctl -b -1'?",
         ["A) Letzter Boot-Zyklus", "B) Logs vom vorletzten Boot", "C) Boot-Statistiken", "D) Letzten 1 Eintrag"],
         "B", "journalctl -b 0 = aktueller Boot. -b -1 = vorletzter Boot. Nützlich nach Abstürzen.", 20),
    ],

    # ── CH12: Packages ────────────────────────────────────────────────────────
    "12.01": [
        ("Was macht 'dpkg -l'?",
         ["A) Installiert Paket", "B) Listet alle installierten Pakete", "C) Zeigt Paket-Log", "D) Löscht Paket"],
         "B", "dpkg -l = list all installed packages. dpkg -L PKG = listet Dateien eines Pakets.", 20),
        ("Welcher Befehl zeigt, zu welchem Paket eine Datei gehört?",
         ["A) dpkg -s /pfad", "B) dpkg -S /pfad/zur/datei", "C) dpkg -q datei", "D) apt-file datei"],
         "B", "dpkg -S = search. Zeigt welches Paket die Datei installiert hat.", 20),
    ],
    "12.02": [
        ("Was macht 'apt upgrade' im Vergleich zu 'apt full-upgrade'?",
         ["A) Kein Unterschied", "B) apt upgrade entfernt keine Pakete, full-upgrade schon (bei Konflikten)", "C) full-upgrade ist sicherer", "D) apt upgrade ist für Kernel"],
         "B", "apt upgrade: keine Pakete entfernt. full-upgrade (dist-upgrade): entfernt bei Bedarf.", 20),
        ("Warum muss man 'apt update' vor 'apt install' ausführen?",
         ["A) Lädt Paket herunter", "B) Aktualisiert die lokale Paketliste (Metadaten) vom Repository", "C) Prüft Abhängigkeiten", "D) Authentifiziert Repository"],
         "B", "apt update = Paketliste aktualisieren (keine Installation!). Ohne update: veraltete Infos.", 20),
    ],
    "12.03": [
        ("Was steht in /etc/apt/sources.list?",
         ["A) Installierte Pakete", "B) Repository-URLs und Komponenten (main, contrib, etc.)", "C) GPG-Schlüssel", "D) Paket-Cache"],
         "B", "/etc/apt/sources.list: Repository-Quellen. /etc/apt/sources.list.d/: Drop-in Dateien.", 20),
        ("Was macht 'apt-key add -'?",
         ["A) Fügt leeren Schlüssel hinzu", "B) Fügt GPG-Schlüssel aus Stdin zum apt-Keyring hinzu", "C) Erstellt neuen Schlüssel", "D) Zeigt alle Schlüssel"],
         "B", "apt-key add KEY = GPG-Signaturschlüssel für Repository-Verifikation hinzufügen.", 20),
    ],
    "12.04": [
        ("Welcher rpm-Befehl zeigt, zu welchem Paket eine Datei gehört?",
         ["A) rpm -qi /pfad", "B) rpm -qf /pfad/zur/datei", "C) rpm -ql datei", "D) rpm -qs datei"],
         "B", "rpm -qf = query file. rpm -qi = query info. rpm -ql = query list (Dateien des Pakets).", 20),
        ("Was macht 'rpm -ivh paket.rpm'?",
         ["A) Informationen anzeigen", "B) Installieren mit verbose + Fortschrittsbalken", "C) Auf Updates prüfen", "D) Verify Hashsumme"],
         "B", "rpm -ivh: i=install, v=verbose, h=hash (Fortschrittsbalken #####).", 20),
    ],
    "12.05": [
        ("Was ist der Unterschied zwischen yum und dnf?",
         ["A) yum ist moderner", "B) dnf ist der moderne Nachfolger von yum (schneller, bessere Abhängigkeiten)", "C) Kein Unterschied", "D) yum ist für RHEL, dnf für Fedora"],
         "B", "dnf = Dandified YUM, moderner Ersatz. RHEL8+ nutzt dnf. yum ist oft ein Alias.", 20),
        ("Was macht 'yum/dnf provides /pfad/zur/datei'?",
         ["A) Zeigt Abhängigkeiten", "B) Zeigt welches Paket diese Datei bereitstellt", "C) Überprüft Datei-Integrität", "D) Installiert Datei"],
         "B", "provides = Gegenstück zu dpkg -S. Sucht Paket das eine bestimmte Datei enthält.", 20),
    ],
    "12.06": [
        ("Was macht 'zypper search PKG'?",
         ["A) Installiert Paket", "B) Sucht nach Paket in Repositories", "C) Zeigt Paket-Details", "D) Entfernt Paket"],
         "B", "zypper search (oder se) sucht. zypper install (in), zypper remove (rm).", 20),
        ("Zypper ist der Paketmanager für welche Distributionen?",
         ["A) Debian/Ubuntu", "B) RHEL/CentOS", "C) SUSE/openSUSE", "D) Arch Linux"],
         "C", "zypper = SUSE/openSUSE. apt/dpkg = Debian/Ubuntu. yum/dnf/rpm = RHEL.", 20),
    ],
    "12.07": [
        ("Was zeigt 'ldd /pfad/zum/programm'?",
         ["A) Dateiformat des Programms", "B) Benötigte Shared Libraries (dynamische Abhängigkeiten)", "C) Debug-Symbole", "D) Programmversion"],
         "B", "ldd = list dynamic dependencies. Zeigt alle .so-Dateien die das Programm braucht.", 20),
        ("Was macht ldconfig?",
         ["A) Library konfigurieren (kompilieren)", "B) Shared Library Cache aktualisieren (nach Installation neuer .so-Dateien)", "C) Alle Libraries auflisten", "D) Library-Pfade in .bashrc setzen"],
         "B", "ldconfig aktualisiert den ld.so-Cache. Nach neuer Library: ldconfig ausführen!", 20),
    ],
    "12.boss": [
        ("Was ist der Unterschied zwischen 'dpkg -r' und 'dpkg -P'?",
         ["A) Kein Unterschied", "B) -r entfernt Paket (Konfig bleibt), -P purge (Konfig auch gelöscht)", "C) -r ist für RHEL, -P für Debian", "D) -P ist sicherer"],
         "B", "dpkg -r = remove (Konfigurationsdateien bleiben). dpkg -P = purge (alles weg).", 20),
    ],

    # ── CH13: Kernel ──────────────────────────────────────────────────────────
    "13.01": [
        ("Welcher Befehl lädt ein Kernel-Modul mit allen Abhängigkeiten?",
         ["A) insmod modul", "B) modprobe modul", "C) lsmod modul", "D) modload modul"],
         "B", "modprobe = lädt Modul + alle Abhängigkeiten automatisch. insmod = nur das Modul selbst.", 20),
        ("Was zeigt 'lsmod'?",
         ["A) Verfügbare Module auf Disk", "B) Aktuell geladene Kernel-Module", "C) Module-Konfiguration", "D) Modul-Fehler"],
         "B", "lsmod = list modules. Zeigt geladene Module + Größe + Verwendungen.", 20),
    ],
    "13.02": [
        ("Wo konfiguriert man Module die beim Boot automatisch geladen werden?",
         ["A) /etc/modules-load.d/ oder /etc/modules", "B) /boot/grub/modules", "C) /lib/modules/", "D) /etc/modprobe.conf"],
         "A", "/etc/modules (Debian) oder /etc/modules-load.d/*.conf (systemd) = automatisches Laden.", 20),
        ("Wie blockiert man ein Kernel-Modul dauerhaft?",
         ["A) rmmod --permanent modul", "B) blacklist modul in /etc/modprobe.d/", "C) modprobe -b modul", "D) touch /etc/modules.blacklist"],
         "B", "blacklist MODUL in /etc/modprobe.d/blacklist.conf. Dann: update-initramfs -u", 20),
    ],
    "13.03": [
        ("Was zeigt cat /proc/cpuinfo?",
         ["A) CPU-Auslastung", "B) CPU-Modell, Kerne, Flags und Taktrate", "C) CPU-Temperatur", "D) Prozess-Liste"],
         "B", "/proc/cpuinfo = CPU-Details vom Kernel. /proc/meminfo = RAM-Details.", 20),
        ("Was macht 'uname -r'?",
         ["A) Zeigt alle Kernel-Infos", "B) Zeigt die laufende Kernel-Version", "C) Zeigt Release-Datum", "D) Root-Prüfung"],
         "B", "uname -r = release (Kernel-Version). uname -a = alle Infos.", 20),
    ],
    "13.04": [
        ("Wie setzt man einen sysctl-Parameter dauerhaft?",
         ["A) sysctl -w param=wert (dauerhaft)", "B) Eintrag in /etc/sysctl.conf oder /etc/sysctl.d/", "C) Kernel-Recompile", "D) Nur via Reboot"],
         "B", "sysctl -w = temporär (bis Reboot). Dauerhaft: /etc/sysctl.conf, dann sysctl -p.", 20),
        ("Was macht 'sysctl -p'?",
         ["A) Listet alle Parameter", "B) Lädt Konfiguration aus /etc/sysctl.conf neu", "C) Persistenz prüfen", "D) Setzt Default-Werte"],
         "B", "sysctl -p = apply persistent settings. Liest /etc/sysctl.conf und aktiviert.", 20),
    ],
    "13.05": [
        ("Was ist udev?",
         ["A) UDP Event Daemon", "B) Kernel-Geräteverwaltungs-Daemon (erstellt /dev-Einträge dynamisch)", "C) User Device Manager", "D) USB Detector"],
         "B", "udev = Userspace Device Manager. Erstellt /dev-Einträge dynamisch bei Hardware-Erkennung.", 20),
        ("Welcher Befehl zeigt udev-Informationen zu einem Gerät?",
         ["A) udev-info /dev/sda", "B) udevadm info /dev/sda", "C) udev list /dev/sda", "D) devinfo /dev/sda"],
         "B", "udevadm info = udev admin info. udevadm monitor = Live-Events beobachten.", 20),
    ],
    "13.06": [
        ("Was macht 'dmesg -T'?",
         ["A) Teste Kernel-Fehler", "B) Zeigt Kernel-Nachrichten mit menschenlesbarem Timestamp", "C) Nur Fehler-Level", "D) Tail-Modus"],
         "B", "dmesg -T = human-readable timestamps (statt Sekunden seit Boot).", 20),
        ("Was ist der Unterschied zwischen dmesg und journalctl -k?",
         ["A) Kein Unterschied", "B) dmesg zeigt Kernel-Ringpuffer, journalctl -k zeigt Kernel-Logs aus systemd-Journal", "C) dmesg ist moderner", "D) journalctl -k ist schneller"],
         "B", "Beide zeigen Kernel-Messages. journalctl -k (--dmesg) aus persistentem Journal.", 20),
    ],
    "13.07": [
        ("Welche Dateien liegen typischerweise in /boot/?",
         ["A) Nur GRUB-Dateien", "B) Kernel-Image (vmlinuz), initrd/initramfs, GRUB-Konfiguration", "C) Nur initramfs", "D) Boot-Logs"],
         "B", "/boot/: vmlinuz-* (Kernel), initrd.img-* (initramfs), grub/ (Bootloader-Konfig).", 20),
        ("Was macht update-initramfs -u?",
         ["A) Updates den Kernel", "B) Aktualisiert das initramfs-Image für den aktuellen Kernel", "C) GRUB updaten", "D) Boot-Parameter setzen"],
         "B", "update-initramfs -u = update. Nötig nach Kernelmodul-Änderungen, die beim Boot benötigt werden.", 20),
    ],
    "13.boss": [
        ("Welcher Befehl lädt ein Modul inkl. Abhängigkeiten?",
         ["A) insmod", "B) modprobe", "C) modload", "D) lsmod"],
         "B", "modprobe = loads module + dependencies. insmod = low-level, no dependencies.", 20),
    ],

    # ── CH14: Scripting ───────────────────────────────────────────────────────
    "14.01": [
        ("Was ist die Shebang-Zeile und warum wichtig?",
         ["A) Kommentar-Zeile", "B) Erste Zeile: #!/bin/bash — definiert den Interpreter für das Skript", "C) Sicherheits-Header", "D) Encoding-Deklaration"],
         "B", "#!/bin/bash = Shebang. Ohne Shebang: Skript wird als aktuelle Shell interpretiert.", 20),
        ("Welche Rechte braucht ein Skript zum Ausführen?",
         ["A) Read + Execute", "B) Write + Execute", "C) Nur Execute", "D) Alle Rechte (777)"],
         "A", "chmod +x oder chmod 755. Read+Execute reicht zum Ausführen.", 20),
    ],
    "14.02": [
        ("Was enthält $#?",
         ["A) Exit-Code des letzten Befehls", "B) Anzahl der Skript-Argumente", "C) Letztes Argument", "D) Skriptname"],
         "B", "$# = Anzahl der Parameter. $1 $2 ... = einzelne Parameter. $@ = alle als Array.", 20),
        ("Was ist der Unterschied zwischen $@ und $*?",
         ["A) Kein Unterschied", "B) \"$@\" bewahrt einzelne Argumente (gequotet), \"$*\" macht einen String", "C) $* ist veraltet", "D) $@ nur in Funktionen"],
         "B", "\"$@\" = jedes Argument separat gequotet. \"$*\" = alle als ein String. $@ fast immer bevorzugt.", 20),
    ],
    "14.03": [
        ("Welche test-Bedingung prüft ob eine Datei existiert?",
         ["A) [ -e DATEI ]", "B) [ -x DATEI ]", "C) [ -f DATEI ]", "D) [ -d DATEI ]"],
         "A", "-e = exists. -f = regular file. -d = directory. -x = executable. -r = readable.", 20),
        ("Was macht '[ -z $VAR ]'?",
         ["A) Prüft ob Variable zero ist (Zahl)", "B) Prüft ob Variable leer (zero length) ist", "C) Prüft ob Variable gesetzt ist", "D) Prüft Datei-Größe"],
         "B", "-z = zero length (leer). -n = not empty. Immer quoten: [ -z \"$VAR\" ]!", 20),
    ],
    "14.04": [
        ("Was ist der Unterschied zwischen for und while in Bash?",
         ["A) Kein Unterschied", "B) for iteriert über Liste, while läuft solange Bedingung wahr", "C) while ist schneller", "D) for nur für Zahlen"],
         "B", "for VAR in LISTE: iteriert. while BEDINGUNG: läuft solange Bedingung 0 (true).", 20),
        ("Wie iteriert man über alle Argumente in einer for-Schleife?",
         ["A) for arg in $@; do", "B) for arg in \"$@\"; do", "C) for arg; do (implizit $@)", "D) B oder C"],
         "D", "for arg in \"$@\"; do ODER kurz: for arg; do (iteriert implizit über \"$@\").", 20),
    ],
    "14.05": [
        ("Wie ruft man eine Funktion 'myfunc' in Bash auf?",
         ["A) call myfunc", "B) myfunc [argumente]", "C) function myfunc", "D) invoke myfunc"],
         "B", "Funktionen einfach wie Befehle aufrufen: myfunc arg1 arg2. Definition: myfunc() { ... }", 20),
        ("Was macht case $VAR in bei Bash?",
         ["A) Prüft jeden Buchstaben", "B) Switch/Case: prüft Variable gegen Muster, führt passenden Block aus", "C) Iteriert über Variable", "D) Nur für Zahlen"],
         "B", "case $VAR in MUSTER) Befehle ;; esac. Muster: a|b = oder, * = default.", 20),
    ],
    "14.06": [
        ("Wie berechnet man 2+3 in Bash?",
         ["A) expr 2 + 3", "B) echo $((2+3))", "C) let result=2+3", "D) A, B oder C"],
         "D", "Alle drei sind gültig! $(( )) = arithmetic expansion. let und expr auch möglich.", 20),
        ("Wie greift man auf alle Elemente eines Bash-Arrays zu?",
         ["A) $ARRAY", "B) ${ARRAY[@]}", "C) $ARRAY[*]", "D) ${ARRAY[all]}"],
         "B", "${ARRAY[@]} = alle Elemente (gequotet). ${#ARRAY[@]} = Anzahl der Elemente.", 20),
    ],
    "14.07": [
        ("Was ist 'getopts' in Bash?",
         ["A) Paket-Manager", "B) Verarbeitet Kommandozeilen-Optionen (-v, -f, etc.)", "C) Debugger", "D) Eingabe-Validator"],
         "B", "getopts 'hv:f:' = parsed -h (kein Arg), -v (mit Arg :), -f (mit Arg :). $OPTARG = Argument.", 20),
        ("Was macht 'read -p \"Eingabe: \" VAR'?",
         ["A) Liest Variable aus Datei", "B) Zeigt Prompt und liest Eingabe in Variable", "C) Passwort-Eingabe", "D) Liest Prozess-ID"],
         "B", "read -p PROMPT VAR = Benutzereingabe mit Prompt. read -s = silent (für Passwörter).", 20),
    ],
    "14.boss": [
        ("Was ist $? in Bash?",
         ["A) Anzahl der Parameter", "B) Exit-Code des letzten Befehls (0=Erfolg)", "C) Prozess-ID", "D) Letztes Argument"],
         "B", "$? = Exit-Code. 0 = Erfolg. 1-255 = Fehler. Immer nach kritischen Befehlen prüfen!", 20),
    ],

    # ── CH15: Security ────────────────────────────────────────────────────────
    "15.01": [
        ("Was findet 'find / -perm -4000 -type f'?",
         ["A) Alle Dateien größer als 4000 Bytes", "B) Alle Dateien mit SUID-Bit gesetzt", "C) Alle ausführbaren Dateien", "D) Alle root-Dateien"],
         "B", "-perm -4000 = SUID-Bit gesetzt. -perm -2000 = SGID. -perm /6000 = SUID oder SGID.", 20),
        ("Was ist das SUID-Bit?",
         ["A) Set-User-ID: Programm läuft mit Rechten des Datei-Owners", "B) Secure-User-ID: Authentifizierungs-Bit", "C) Super-User-ID: nur für root", "D) System-User-ID: für Daemons"],
         "A", "SUID: Programm läuft als Datei-Owner (z.B. passwd läuft als root). Sicherheitsrisiko!", 20),
    ],
    "15.02": [
        ("Was aktiviert SSH-Schlüssel-Authentifizierung und deaktiviert Passwort-Login?",
         ["A) PubkeyAuthentication yes + PasswordAuthentication no", "B) KeyAuth yes + PassAuth no", "C) UsePublicKey yes + NoPassword yes", "D) AuthMethod key"],
         "A", "In sshd_config: PubkeyAuthentication yes (Standard) + PasswordAuthentication no.", 20),
        ("Was bedeutet 'PermitRootLogin prohibit-password'?",
         ["A) Root kann gar nicht einloggen", "B) Root kann nur mit SSH-Key einloggen, kein Passwort", "C) Root-Passwort ist deaktiviert", "D) Temporäres Verbot"],
         "B", "prohibit-password = without-password: Root-Login nur via SSH-Key möglich.", 20),
    ],
    "15.03": [
        ("Was macht 'gpg --verify datei.asc datei'?",
         ["A) Verschlüsselt Datei", "B) Prüft GPG-Signatur der Datei", "C) Entschlüsselt Signatur", "D) Erstellt Signatur"],
         "B", "gpg --verify = Signatur prüfen. gpg -d = decrypt. gpg -e = encrypt. gpg --sign = signieren.", 20),
        ("Welcher Befehl exportiert einen öffentlichen GPG-Schlüssel?",
         ["A) gpg --export-public KEYID", "B) gpg --export KEYID", "C) gpg -e KEYID", "D) gpg --pub KEYID"],
         "B", "gpg --export KEYID > schluessel.asc. --export-secret-keys für privaten Schlüssel.", 20),
    ],
    "15.04": [
        ("Was macht fail2ban?",
         ["A) Firewall-Regelwerk", "B) Sperrt IPs nach zu vielen fehlgeschlagenen Login-Versuchen", "C) SSL-Zertifikat-Manager", "D) Netzwerk-Monitor"],
         "B", "fail2ban liest Logs, erkennt Brute-Force-Versuche und sperrt IPs via iptables/nftables.", 20),
        ("Wo konfiguriert man fail2ban anwendungsspezifisch?",
         ["A) /etc/fail2ban/jail.conf", "B) /etc/fail2ban/jail.local", "C) /etc/fail2ban/rules/", "D) ~/.fail2ban"],
         "B", "jail.local überschreibt jail.conf. Eigene Konfiguration IMMER in jail.local!", 20),
    ],
    "15.05": [
        ("Was macht 'visudo' im Vergleich zum direkten Bearbeiten von /etc/sudoers?",
         ["A) Kein Unterschied", "B) visudo prüft Syntax vor Speicherung (verhindert kaputte sudo-Config)", "C) visudo verschlüsselt die Datei", "D) visudo erstellt Backup"],
         "B", "visudo = safe editor for sudoers. Syntaxfehler = kein sudo. Immer visudo verwenden!", 20),
        ("Was bedeutet '%gruppe ALL=(ALL) NOPASSWD: ALL' in sudoers?",
         ["A) Gruppe kann alles ohne Passwort sudo machen", "B) Gruppe hat kein Passwort", "C) Alle Gruppen dürfen sudo", "D) Fehler: % ungültig"],
         "A", "% = Gruppe. NOPASSWD: = kein Passwort nötig. ALL=(ALL) = überall als jeder User.", 20),
    ],
    "15.06": [
        ("Was ist LUKS?",
         ["A) Linux User Key System", "B) Linux Unified Key Setup — Festplatten-Verschlüsselung", "C) Lightweight Unix Kerberos System", "D) Linux USB Key Service"],
         "B", "LUKS = Linux Unified Key Setup. Standard für dm-crypt Festplatten-Verschlüsselung.", 20),
        ("Was ist die korrekte LUKS-Workflow-Reihenfolge?",
         ["A) luksOpen → luksFormat → mkfs → mount", "B) luksFormat → luksOpen → mkfs → mount", "C) mkfs → luksFormat → mount", "D) luksFormat → mkfs → luksOpen"],
         "B", "cryptsetup luksFormat → luksOpen (mapper erstellen) → mkfs → mount.", 20),
    ],
    "15.07": [
        ("Was zeigt 'iptables -L -n -v'?",
         ["A) Alle Netzwerkverbindungen", "B) Alle Firewall-Regeln mit Paket-Countern", "C) Netzwerk-Statistiken", "D) Open Ports"],
         "B", "iptables -L = list. -n = numerisch (kein DNS). -v = verbose (Counters).", 20),
        ("Was ist die INPUT-Chain in iptables?",
         ["A) Ausgehender Traffic", "B) Eingehender Traffic (zum lokalen System)", "C) Weitergeleiteier Traffic", "D) Alle Chains"],
         "B", "INPUT = eingehend. OUTPUT = ausgehend. FORWARD = weitergeleitet (Router).", 20),
    ],
    "15.boss": [
        ("Was findet 'find / -perm /6000 -type f'?",
         ["A) Dateien größer 6000 Bytes", "B) Dateien mit SUID ODER SGID Bit", "C) Nur SUID-Dateien", "D) Nur SGID-Dateien"],
         "B", "-perm /6000 = SUID (4000) ODER SGID (2000). -perm -6000 = beides gesetzt.", 20),
    ],

    # ── CH16: Locale ──────────────────────────────────────────────────────────
    "16.01": [
        ("Was macht 'iconv -f UTF-8 -t ISO-8859-1 datei.txt'?",
         ["A) Datei von ISO-8859-1 nach UTF-8 konvertieren", "B) Datei von UTF-8 nach ISO-8859-1 konvertieren", "C) Datei-Encoding anzeigen", "D) Fehler"],
         "B", "-f = from (Quelle), -t = to (Ziel). iconv konvertiert Zeichensätze.", 20),
        ("Was überschreibt LC_ALL?",
         ["A) Nur LANG", "B) Alle LC_*-Variablen und LANG (höchste Priorität)", "C) Nur spezifische LC_*", "D) Nichts"],
         "B", "LC_ALL überschreibt alle anderen Locale-Einstellungen. Höchste Priorität.", 20),
    ],
    "16.02": [
        ("Wie setzt man die Zeitzone dauerhaft mit timedatectl?",
         ["A) timedatectl --timezone Europe/Berlin", "B) timedatectl set-timezone Europe/Berlin", "C) export TZ=Europe/Berlin", "D) ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/timezone"],
         "B", "timedatectl set-timezone NAME = dauerhaft. Symbolischer Link nach /etc/localtime wird automatisch gesetzt.", 20),
        ("Wo sind die Zeitzonendaten gespeichert?",
         ["A) /etc/timezone/", "B) /usr/share/zoneinfo/", "C) /var/lib/timezone/", "D) /etc/timedate/"],
         "B", "/usr/share/zoneinfo/ = Zeitzonendaten. /etc/localtime = aktuell gesetzter Link.", 20),
    ],
    "16.03": [
        ("Was ist die DISPLAY-Variable?",
         ["A) Monitor-Auflösung", "B) X-Server-Adresse (HOST:DISPLAY.SCREEN), benötigt für GUI-Anwendungen", "C) Desktop-Hintergrund", "D) Bildschirm-Helligkeit"],
         "B", "DISPLAY=:0 = lokaler Display. DISPLAY=host:0 = Remote-Display. Nötig für GUI-Apps via SSH.", 20),
        ("Was macht 'ssh -X remote' im Vergleich zu 'ssh -Y remote'?",
         ["A) Kein Unterschied", "B) -X = mit Sicherheitsfilter, -Y = trusted (weniger sicher aber kompatibler)", "C) -X für TCP, -Y für UDP", "D) -Y ist veraltet"],
         "B", "ssh -X = X11 Forwarding mit Sicherheitsfilter. -Y = trusted (mehr Rechte, weniger sicher).", 20),
    ],
    "16.04": [
        ("Was ist graphical.target in systemd?",
         ["A) Nur für Grafik-Karten", "B) Das Boot-Target das GUI startet (entspricht Runlevel 5)", "C) GPU-Treiber-Target", "D) Display-Server-Target"],
         "B", "graphical.target = GUI-Boot (Runlevel 5). multi-user.target = CLI-Boot (Runlevel 3).", 20),
        ("Was ist ein Display Manager?",
         ["A) Grafik-Kartentreiber", "B) Login-Screen-Programm (GDM, SDDM, LightDM)", "C) Fenster-Manager", "D) X-Server-Konfiguration"],
         "B", "Display Manager = grafischer Login-Screen. GDM=GNOME, SDDM=KDE, LightDM=leichtgewichtig.", 20),
    ],
    "16.05": [
        ("Was macht 'lpr datei.txt'?",
         ["A) Listet Drucker-Ressourcen", "B) Druckt die Datei auf dem Standard-Drucker", "C) Zeigt Drucker-Status", "D) Konfiguriert Drucker"],
         "B", "lpr = line print. Druckt auf Standard-Drucker. lpr -P DRUCKER datei = spezifischer Drucker.", 20),
        ("Wie zeigt man die Druckwarteschlange an?",
         ["A) lpr -q", "B) lpq oder lpstat", "C) cups -list", "D) print --queue"],
         "B", "lpq = Warteschlange anzeigen. lpstat -p = Drucker-Status. lprm JOBNR = Job löschen.", 20),
    ],
    "16.06": [
        ("Was ist AT-SPI2?",
         ["A) Netzwerk-Protokoll", "B) Accessibility-Framework für barrierefreie Linux-Anwendungen", "C) Audio-Interface", "D) Dateiformat"],
         "B", "AT-SPI2 = Assistive Technology Service Provider Interface. Basis für Screenreader etc.", 20),
        ("Was ist Orca?",
         ["A) Dateimanager", "B) Screen Reader für visuelle Beeinträchtigungen unter GNOME", "C) Terminal-Emulator", "D) Datenbankmanager"],
         "B", "Orca = GNOME Screen Reader. Liest UI-Elemente vor. Teil der GNOME Accessibility Suite.", 20),
    ],
    "16.boss": [
        ("Was macht 'locale-gen de_DE.UTF-8'?",
         ["A) Setzt Standard-Locale", "B) Generiert/kompiliert die Locale-Daten für de_DE.UTF-8", "C) Installiert Sprachpaket", "D) Zeigt Locale-Info"],
         "B", "locale-gen = Locale-Daten kompilieren. Dann update-locale LANG=de_DE.UTF-8.", 20),
    ],

    # ── CH17: Shell Environment ───────────────────────────────────────────────
    "17.01": [
        ("Was ist der Unterschied zwischen Login-Shell und Non-Login-Shell?",
         ["A) Kein Unterschied", "B) Login-Shell liest /etc/profile + ~/.bash_profile, Non-Login nur ~/.bashrc", "C) Login-Shell hat mehr Rechte", "D) Non-Login ist interaktiv"],
         "B", "Login: /etc/profile → ~/.bash_profile (einmal). Non-Login: ~/.bashrc (jedes neue Terminal).", 20),
        ("Welche Datei konfiguriert die Bash für alle Benutzer systemweit?",
         ["A) /etc/bashrc", "B) /etc/profile", "C) ~/.bashrc", "D) /etc/bash.bashrc"],
         "B", "/etc/profile = systemweit für Login-Shells. ~/.bash_profile = benutzerspezifisch.", 20),
    ],
    "17.02": [
        ("Was ist der Unterschied zwischen 'env' und 'set'?",
         ["A) Kein Unterschied", "B) env = nur Umgebungsvariablen. set = alle Shell-Vars + Funktionen", "C) set ist moderner", "D) env ist für Root"],
         "B", "env = exportierte Umgebungsvariablen. set = alle Variablen inkl. Shell-Funktionen.", 20),
        ("Was macht 'export VAR'?",
         ["A) Löscht Variable", "B) Macht Variable zu Umgebungsvariable (an Kind-Prozesse vererbt)", "C) Setzt Variable dauerhaft", "D) Exportiert in Datei"],
         "B", "export = Umgebungsvariable. Kind-Prozesse erben sie. In ~/.bashrc für Dauerhaftigkeit.", 20),
    ],
    "17.03": [
        ("Wie fügt man /opt/bin dauerhaft zu PATH hinzu?",
         ["A) PATH=/opt/bin (überschreibt alten PATH)", "B) export PATH=\"$PATH:/opt/bin\" in ~/.bashrc", "C) add-path /opt/bin", "D) PATH+=:/opt/bin"],
         "B", "export PATH=\"$PATH:/opt/bin\" = anhängen. Punkt wichtig: /opt/bin am Ende.", 20),
        ("Warum soll '.' (current directory) NICHT in PATH stehen?",
         ["A) Zu langsam", "B) Sicherheitsrisiko: böswillige Programme im cwd könnten ausgeführt werden", "C) Funktioniert nicht", "D) Nur Windows-Problem"],
         "B", "'.' in PATH = Sicherheitslücke! Angreifer könnte 'ls' im aktuellen Verzeichnis platzieren.", 20),
    ],
    "17.04": [
        ("Wie umgeht man einen Alias für einen Befehl?",
         ["A) alias-off befehl", "B) \\befehl (Backslash) oder 'command befehl'", "C) unalias befehl; befehl", "D) befehl --no-alias"],
         "B", "\\ls oder command ls umgeht den ls-Alias. \\befehl = Original-Befehl direkt.", 20),
        ("Was zeigt 'type ls'?",
         ["A) ls-Handbuch", "B) Was 'ls' ist: Alias, Built-in, Funktion oder externer Befehl", "C) Dateityp", "D) ls-Version"],
         "B", "type zeigt ob Befehl ein Alias, Shell-Built-in, Funktion oder externes Programm ist.", 20),
    ],
    "17.05": [
        ("Was macht 'Ctrl+R' in Bash?",
         ["A) Reverse-Sort der History", "B) Rückwärts-Suche in der Befehlshistorie", "C) Run-Modus aktivieren", "D) Resets Terminal"],
         "B", "Ctrl+R = reverse-i-search. Inkrementelle Rückwärts-Suche in ~/.bash_history.", 20),
        ("Was ist HISTCONTROL=ignoreboth?",
         ["A) Ignoriert alle History-Einträge", "B) Ignoriert Duplikate UND Befehle mit Leerzeichen davor", "C) Ignoriert beide History-Dateien", "D) Deaktiviert History"],
         "B", "ignoreboth = ignoredups + ignorespace. Sinnvoll zum Vermeiden von Doppeleinträgen.", 20),
    ],
    "17.06": [
        ("Was bedeutet '\\u@\\h:\\w\\$' im PS1-Prompt?",
         ["A) Ungültige Sequenz", "B) User@Hostname:Pfad$ ($ für User, # für Root)", "C) User-ID@Host:Windows$", "D) Uhrzeit@Hostname:Pfad"],
         "B", "\\u=Username, \\h=Hostname, \\w=Pfad, \\$=$ für User / # für Root.", 20),
        ("Was ist PS2?",
         ["A) PlayStation 2", "B) Fortsetzungs-Prompt (erscheint bei mehrzeiligen Befehlen)", "C) Zweiter Shell-Prompt", "D) Passwort-Prompt"],
         "B", "PS2 = Secondary Prompt. Erscheint bei unvollständigen Befehlen (nach Enter mitten in Befehl).", 20),
    ],
    "17.boss": [
        ("Was macht 'unalias -a'?",
         ["A) Einen Alias löschen", "B) Alle Aliases löschen", "C) Alias-Datei leeren", "D) Aliases deaktivieren"],
         "B", "unalias -a = alle Aliases der aktuellen Session löschen.", 20),
    ],

    # ── CH18: Exam ────────────────────────────────────────────────────────────
    "18.boss": [
        ("Was ist der LPIC-1-Prüfungsformat?",
         ["A) Nur Multiple-Choice", "B) Multiple-Choice + Freitexteingabe (Commands)", "C) Nur Kommandozeilen-Aufgaben", "D) Nur Essay"],
         "B", "LPIC-1: Multiple Choice + Fill-in-the-blank (Befehle eingeben). 60 Minuten, 60 Fragen.", 20),
    ],
}


def get_quiz_python(mission_id):
    """Returns Python code for quiz_questions for a given mission_id."""
    data = QUIZ_DATA.get(mission_id)
    if not data:
        return None

    lines = ["        quiz_questions    = [\n"]
    for q, opts, correct, explanation, xp in data:
        lines.append("            QuizQuestion(\n")
        lines.append(f"                question    = {repr(q)},\n")
        lines.append(f"                options     = {repr(opts)},\n")
        lines.append(f"                correct     = {repr(correct)},\n")
        lines.append(f"                explanation = {repr(explanation)},\n")
        lines.append(f"                xp_value    = {xp},\n")
        lines.append("            ),\n")
    lines.append("        ],\n")
    return "".join(lines)


def patch_file(filepath, mission_map):
    """
    Patches a chapter file to add quiz_questions to missions that need them.
    mission_map: {mission_id: quiz_python_code}
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    patches_applied = 0

    for mission_id, quiz_code in sorted(mission_map.items()):
        # Find the mission by mission_id (files use double quotes)
        found = False
        for spacing in ['   ', '  ', ' ']:
            for quote in ['"', "'"]:
                id_pattern = f'mission_id{spacing}= {quote}{mission_id}{quote}'
                id_pos = content.find(id_pattern)
                if id_pos != -1:
                    found = True
                    break
            if found:
                break
        if not found:
            print(f"  WARNING: Could not find mission_id {mission_id!r} in {filepath}")
            continue

        # Find the next Mission( start (to limit search scope)
        next_mission_pos = content.find('\n    Mission(', id_pos + 1)
        if next_mission_pos == -1:
            next_mission_pos = len(content)

        # In this mission's block, find exam_tip or memory_tip (whichever comes first after hint_text)
        block = content[id_pos:next_mission_pos]

        # Check if quiz_questions already present
        if 'quiz_questions' in block:
            print(f"  SKIP: {mission_id} already has quiz_questions")
            continue

        # Find hint_text in block
        hint_pos = block.find('hint_text')
        if hint_pos == -1:
            # Find where to insert before exam_tip or memory_tip
            for target in ['exam_tip', 'memory_tip', 'gear_reward', 'faction_reward']:
                target_pos = block.find(f'        {target}')
                if target_pos != -1:
                    insert_before = content[id_pos:][target_pos]
                    break
            else:
                print(f"  WARNING: No insertion point for {mission_id}")
                continue

        # Find end of hint_text line(s)
        hint_start = id_pos + hint_pos
        # Find the comma+newline that ends the hint_text field
        # hint_text can be multi-line (quoted strings concatenated)
        # Look for the pattern: ",\n        " after hint_text value
        after_hint = content[hint_start:]

        # Find first occurrence of "\n        " that's followed by a known field
        for next_field in ['exam_tip', 'memory_tip', 'quiz_questions', 'gear_reward', 'faction_reward', 'simulated_commands']:
            next_pos = after_hint.find(f'\n        {next_field}')
            if next_pos != -1:
                # Insert quiz_questions before this next field
                abs_insert = hint_start + next_pos + 1  # after the \n
                content = content[:abs_insert] + quiz_code + content[abs_insert:]
                patches_applied += 1
                print(f"  PATCHED: {mission_id}")
                break
        else:
            print(f"  WARNING: Could not find insertion point for {mission_id}")

    if patches_applied > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  => Wrote {patches_applied} patches to {os.path.basename(filepath)}")
    else:
        print(f"  => No changes needed for {os.path.basename(filepath)}")

    return patches_applied


# ── Chapter file mapping ───────────────────────────────────────────────────────
CHAPTER_FILES = {
    4:  ('missions/ch04_partitions.py',    ["4.01","4.02","4.03","4.04","4.05","4.07","4.08","4.10","4.12","4.13"]),
    5:  ('missions/ch05_permissions.py',   ["5.03","5.08","5.10"]),
    6:  ('missions/ch06_shell.py',         ["6.01","6.02","6.04","6.07","6.09","6.10"]),
    7:  ('missions/ch07_processes.py',     ["7.01","7.03","7.05","7.07","7.08","7.09"]),
    8:  ('missions/ch08_regex_vi.py',      ["8.01","8.02","8.03","8.04","8.05","8.06","8.07","8.08","8.boss"]),
    9:  ('missions/ch09_network.py',       ["9.01","9.02","9.03","9.04","9.05","9.06","9.07"]),
    10: ('missions/ch10_users.py',         ["10.01","10.02","10.03","10.04","10.05","10.06","10.07","10.boss"]),
    11: ('missions/ch11_logging.py',       ["11.01","11.02","11.03","11.04","11.05","11.06","11.07","11.08","11.09","11.10","11.11","11.12","11.boss"]),
    12: ('missions/ch12_packages.py',      ["12.01","12.02","12.03","12.04","12.05","12.06","12.07","12.boss"]),
    13: ('missions/ch13_kernel.py',        ["13.01","13.02","13.03","13.04","13.05","13.06","13.07","13.boss"]),
    14: ('missions/ch14_scripting.py',     ["14.01","14.02","14.03","14.04","14.05","14.06","14.07","14.boss"]),
    15: ('missions/ch15_security.py',      ["15.01","15.02","15.03","15.04","15.05","15.06","15.07","15.boss"]),
    16: ('missions/ch16_locale.py',        ["16.01","16.02","16.03","16.04","16.05","16.06","16.boss"]),
    17: ('missions/ch17_shellenv.py',      ["17.01","17.02","17.03","17.04","17.05","17.06","17.boss"]),
    18: ('missions/ch18_exam.py',          ["18.boss"]),
}


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    total_patches = 0

    for ch, (filepath, mission_ids) in sorted(CHAPTER_FILES.items()):
        print(f"\n=== Patching CH{ch:02d}: {filepath} ===")
        mission_map = {}
        for mid in mission_ids:
            code = get_quiz_python(mid)
            if code:
                mission_map[mid] = code
            else:
                print(f"  WARNING: No quiz data for {mid}")
        total_patches += patch_file(filepath, mission_map)

    print(f"\n{'='*60}")
    print(f"Total patches applied: {total_patches}")


if __name__ == '__main__':
    main()
