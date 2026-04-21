"""
NeonGrid-9 :: Terminal Simulator
Simuliert Linux-Befehlsausgaben für Lernzwecke.
Spieler tippt Befehle — das System liefert realistische Ausgaben.
"""

import re
import time
from engine.display import C, show_code, slow_print

# ── Simulierte Ausgaben ────────────────────────────────────────────────────────
SIMULATED_OUTPUTS = {

    # ── Kapitel 1: Hardware ───────────────────────────────────────────────────
    "lspci": """\
00:00.0 Host bridge: Intel Corporation 8th Gen Core Processor Host Bridge/DRAM (rev 07)
00:02.0 VGA compatible controller: Intel Corporation UHD Graphics 620 (rev 07)
00:14.0 USB controller: Intel Corporation Sunrise Point-LP USB 3.0 xHCI Controller (rev 21)
00:1f.2 Memory controller: Intel Corporation Sunrise Point-LP PMC (rev 21)
00:1f.3 Audio device: Intel Corporation Sunrise Point-LP HD Audio (rev 21)
01:00.0 Network controller: Intel Corporation Wireless 8265 / 8275 (rev 78)
02:00.0 Non-Volatile memory controller: Samsung Electronics Co Ltd NVMe SSD Controller SM981""",

    "lspci -v": """\
00:02.0 VGA compatible controller: Intel Corporation UHD Graphics 620 (rev 07) (prog-if 00 [VGA controller])
\tSubsystem: Lenovo UHD Graphics 620
\tFlags: bus master, fast devsel, latency 0, IRQ 133
\tMemory at ec000000 (64-bit, non-prefetchable) [size=16M]
\tMemory at c0000000 (64-bit, prefetchable) [size=256M]
\tI/O ports at f000 [size=64]
\tExpansion ROM at 000c0000 [virtual] [disabled] [size=128K]
\tCapabilities: <access denied>
\tKernel driver in use: i915
\tKernel modules: i915""",

    "lspci -k": """\
00:02.0 VGA compatible controller: Intel Corporation UHD Graphics 620 (rev 07)
\tKernel driver in use: i915
\tKernel modules: i915
01:00.0 Network controller: Intel Corporation Wireless 8265 / 8275 (rev 78)
\tKernel driver in use: iwlwifi
\tKernel modules: iwlwifi""",

    "lsusb": """\
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 005: ID 04f2:b604 Chicony Electronics Co., Ltd Integrated Camera
Bus 001 Device 004: ID 8087:0a2b Intel Corp. Bluetooth wireless interface
Bus 001 Device 003: ID 0461:4d65 Primax Electronics, Ltd
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub""",

    "lsusb -v": """\
Bus 001 Device 005: ID 04f2:b604 Chicony Electronics Co., Ltd Integrated Camera
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               2.00
  bDeviceClass          239 Miscellaneous Device
  bDeviceSubClass         2
  bDeviceProtocol         1
  bMaxPacketSize0        64
  idVendor           0x04f2 Chicony Electronics Co., Ltd
  idProduct          0xb604 Integrated Camera
  bcdDevice            0.13
  iManufacturer           3 Chicony Electronics Co.,Ltd
  iProduct                1 Integrated Camera""",

    "lsusb -t": """\
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/6p, 10000M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/12p, 480M
    |__ Port 4: Dev 3, If 0, Class=Human Interface Device, Driver=usbhid, 1.5M
    |__ Port 6: Dev 4, If 0, Class=Wireless, Driver=btusb, 12M
    |__ Port 8: Dev 5, If 0, Class=Video, Driver=uvcvideo, 480M""",

    "lshw": """\
neongrid9
    description: Notebook
    product: ThinkPad X1 Carbon
    vendor: LENOVO
    version: ThinkPad X1 Carbon 6th
    serial: PF12AB34
    width: 64 bits
    capabilities: smp vsyscall32
  *-core
       description: Motherboard
       product: 20KH002DGE
       vendor: LENOVO
     *-cpu
          description: CPU
          product: Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
          vendor: Intel Corp.
          size: 3966MHz
          capacity: 4GHz
     *-memory
          description: System Memory
          size: 16GiB""",

    "lshw -short": """\
H/W path        Device     Class          Description
==============================================================
                           system         ThinkPad X1 Carbon
/0                         bus            20KH002DGE
/0/0                       memory         128KiB BIOS
/0/4                       processor      Intel Core i7-8550U
/0/4/5                     memory         256KiB L1 Cache
/0/4/8                     memory         8MiB L3 Cache
/0/1f                      memory         16GiB System Memory
/0/100/2       /dev/fb0    display        UHD Graphics 620
/0/100/1f.3                multimedia     Sunrise Point-LP HD Audio
/1             enp0s20f0u4 network        USB Ethernet""",

    "dmidecode": """\
# dmidecode 3.3
Getting SMBIOS data from sysfs.
SMBIOS 3.0.0 present.

Handle 0x0000, DMI type 0, 26 bytes
BIOS Information
\tVendor: LENOVO
\tVersion: N23ET68W (1.44 )
\tRelease Date: 11/08/2021
\tAddress: 0xE0000
\tRuntime Size: 128 kB
\tROM Size: 32 MB

Handle 0x0001, DMI type 1, 27 bytes
System Information
\tManufacturer: LENOVO
\tProduct Name: 20KH002DGE
\tVersion: ThinkPad X1 Carbon 6th
\tSerial Number: PF12AB34
\tUUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890""",

    "lsblk": """\
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
nvme0n1     259:0    0 476.9G  0 disk
├─nvme0n1p1 259:1    0   512M  0 part /boot/efi
├─nvme0n1p2 259:2    0     1G  0 part /boot
└─nvme0n1p3 259:3    0 475.4G  0 part /
sda           8:0    1  14.9G  0 disk
└─sda1        8:1    1  14.9G  0 part /media/usb""",

    "blkid": """\
/dev/nvme0n1p1: UUID="A1B2-C3D4" TYPE="vfat" PARTLABEL="EFI System Partition"
/dev/nvme0n1p2: UUID="a1b2c3d4-0001-0002-0003-000000000001" TYPE="ext4" LABEL="boot"
/dev/nvme0n1p3: UUID="a1b2c3d4-0001-0002-0003-000000000002" TYPE="ext4" LABEL="root"
/dev/sda1: UUID="a1b2c3d4-0001-0002-0003-000000000003" TYPE="ext4" LABEL="backup" """,

    "dmesg": """\
[    0.000000] Linux version 6.1.0-17-amd64 (debian-kernel@lists.debian.org)
[    0.000000] BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009efff] usable
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x000000009fffffff] usable
[    0.293114] ACPI: IRQ0 used by override.
[    0.458223] PCI: Using ACPI for IRQ routing
[    1.234567] usb 1-6: new high-speed USB device number 4 using xhci_hcd
[    1.456789] input: PC Speaker as /devices/platform/pcspkr/input/input4
[    2.111111] e1000e 0000:00:1f.6 eth0: NIC Link is Up 1000 Mbps Full Duplex
[    2.345678] EXT4-fs (nvme0n1p3): mounted filesystem with ordered data mode""",

    "dmesg | grep -i usb": """\
[    1.234567] usb 1-6: new high-speed USB device number 4 using xhci_hcd
[    1.235001] usb 1-6: New USB device found, idVendor=8087, idProduct=0a2b
[    1.235002] usb 1-6: New USB device strings: Mfr=0, Product=0, SerialNumber=0
[    1.235890] hub 1-6:1.0: USB hub found
[    1.456789] input: PC Speaker as /devices/platform/pcspkr/input/input4""",

    "dmesg | grep -i error": (
"[    0.299456] ACPI Error: AE_NOT_FOUND, While evaluating Sleep State [\\_S1_]\n"
"[    3.456789] EXT4-fs error (device nvme0n1p2): ext4_validate_block_bitmap:376: comm kworker/u4:2\n"
"Note: 2 errors found in kernel log."),

    "lsmod": """\
Module                  Size  Used by
snd_hda_intel          61440  0
snd_hda_codec         176128  1 snd_hda_intel
i915                 2850816  4
intel_agp              24576  1 i915
drm_kms_helper        245760  1 i915
drm                   622592  5 drm_kms_helper,i915
iwlwifi               454656  1 iwlmvm
iwlmvm                540672  0
mac80211              876544  1 iwlmvm
cfg80211             1073152  3 iwlmvm,iwlwifi,mac80211
usbcore               319488  7
xhci_hcd              290816  1
xhci_pci               24576  0
nvme                   45056  4
nvme_core             122880  8 nvme""",

    "modinfo i915": """\
filename:       /lib/modules/6.1.0-17-amd64/kernel/drivers/gpu/drm/i915/i915.ko
description:    Intel Graphics
license:        GPL and additional rights
author:         Intel Corporation
firmware:       i915/skl_dmc_ver1_27.bin
firmware:       i915/kbl_dmc_ver1_04.bin
depends:        drm_kms_helper,drm,intel_agp
retpoline:      Y
name:           i915
vermagic:       6.1.0-17-amd64 SMP preempt mod_unload modversions""",

    "cat /proc/cpuinfo": """\
processor\t: 0
vendor_id\t: GenuineIntel
cpu family\t: 6
model\t\t: 142
model name\t: Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
stepping\t: 10
microcode\t: 0xf4
cpu MHz\t\t: 1992.000
cache size\t: 8192 KB
physical id\t: 0
siblings\t: 8
core id\t\t: 0
cpu cores\t: 4
apicid\t\t: 0
flags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
bogomips\t: 3984.00
cache_alignment\t: 64
address sizes\t: 39 bits physical, 48 bits virtual""",

    "cat /proc/meminfo": """\
MemTotal:       16252928 kB
MemFree:         2341256 kB
MemAvailable:    8934512 kB
Buffers:          456789 kB
Cached:          5678901 kB
SwapCached:            0 kB
Active:          4567890 kB
Inactive:        3456789 kB
SwapTotal:       2097148 kB
SwapFree:        2097148 kB
Dirty:               256 kB
Writeback:             0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
Hugepagesize:       2048 kB""",

    "cat /proc/interrupts": """\
           CPU0       CPU1       CPU2       CPU3
  0:         16          0          0          0  IR-IO-APIC   2-edge      timer
  1:          0          0       3765          0  IR-IO-APIC   1-edge      i8042
  8:          0          1          0          0  IR-IO-APIC   8-edge      rtc0
  9:          0          0          0        283  IR-IO-APIC   9-fasteoi   acpi
 14:          0          0          0          0  IR-IO-APIC  14-fasteoi   INT344B:00
 16:          0          0          0        125  IR-IO-APIC  16-fasteoi   i801_smbus
133:       2345       1234        987        654  PCI-MSI 458752-edge      i915
142:        123         89         45         23  PCI-MSI 32768-edge       iwlwifi""",

    "cat /proc/ioports": """\
0000-0cf7 : PCI Bus 0000:00
  0000-001f : dma1
  0020-0021 : PIC
  0040-0043 : timer0
  0050-0053 : timer1
  0060-0060 : keyboard
  0064-0064 : keyboard
  0070-0077 : rtc0
  0080-008f : dma page reg
  00a0-00a1 : PIC
  00c0-00df : dma2
  00f0-00ff : fpu
f000-f03f : 0000:00:1f.4""",

    "cat /proc/iomem": """\
00000000-00000fff : Reserved
00001000-0009efff : System RAM
0009f000-0009ffff : Reserved
000a0000-000bffff : PCI Bus 0000:00
000c0000-000c7fff : Video ROM
000f0000-000fffff : System ROM
00100000-9fffffff : System RAM
  01000000-01c11c9f : Kernel code
  01c11ca0-0209167f : Kernel data
fd000000-fe7fffff : PCI Bus 0000:00
  ec000000-ecffffff : 0000:00:02.0""",

    "uname -a": """\
Linux neongrid9 6.1.0-17-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.69-1 (2023-12-30) x86_64 GNU/Linux""",

    "uname -r": "6.1.0-17-amd64",

    "journalctl -k": """\
Jan 15 08:00:01 neongrid9 kernel: Linux version 6.1.0-17-amd64
Jan 15 08:00:01 neongrid9 kernel: BIOS-e820: [mem 0x0000000000000000-0x9fffffff] usable
Jan 15 08:00:02 neongrid9 kernel: PCI: Using ACPI for IRQ routing
Jan 15 08:00:02 neongrid9 kernel: usb 1-6: new high-speed USB device number 4
Jan 15 08:00:03 neongrid9 kernel: EXT4-fs (nvme0n1p3): mounted filesystem
Jan 15 08:00:04 neongrid9 kernel: iwlwifi 0000:01:00.0: loaded firmware version 36.77d01142.0""",

    "ls /sys": "block  bus  class  dev  devices  firmware  fs  hypervisor  kernel  module  power",

    "ls /dev": """\
autofs  block  bsg  btrfs-control  bus  char  console  core  cpu  cpu_dma_latency
disk  dri  fd  full  fuse  hidraw0  hugepages  hwrng  input  kmsg  kvm  log
loop-control  mapper  mem  mqueue  net  null  nvme0  nvme0n1  nvme0n1p1  nvme0n1p2
nvme0n1p3  port  ppp  psaux  ptmx  pts  random  rfkill  rtc  rtc0  sda  sda1
shm  snapshot  snd  sr0  stderr  stdin  stdout  tty  tty0  tty1  urandom  vcs
vcsa  video0  zero""",

    "modprobe -l": "Use: modprobe <module_name>  or  lsmod  to list loaded modules",
    "modprobe usbcore": "(usbcore already loaded — no output on success)",
    "rmmod usbcore": "rmmod: ERROR: Module usbcore is in use by: usbhid xhci_hcd",
    "insmod": "Usage: insmod <module.ko>  — use modprobe for automatic dependency handling",

    "udevadm info /dev/sda": """\
P: /devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1:1.0/host0/target0:0:0/0:0:0:0/block/sda
N: sda
S: disk/by-id/usb-SanDisk_Cruzer_Glide_4C530001151016117503-0:0
S: disk/by-path/pci-0000:00:1d.0-usb-0:1:1.0-scsi-0:0:0:0
E: DEVLINKS=/dev/disk/by-id/usb-SanDisk_... /dev/disk/by-path/pci-...
E: DEVNAME=/dev/sda
E: DEVTYPE=disk
E: ID_BUS=usb
E: ID_MODEL=Cruzer_Glide
E: ID_VENDOR=SanDisk
E: SUBSYSTEM=block""",

    # ── Kapitel 2: Boot / GRUB2 ──────────────────────────────────────────────

    "fdisk -l": """\
Disk /dev/nvme0n1: 476.94 GiB, 512110190592 bytes, 1000215216 sectors
Disk model: Samsung SSD 970 EVO Plus 512GB
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: A1B2C3D4-E5F6-7890-ABCD-EF1234567890

Device             Start        End   Sectors   Size Type
/dev/nvme0n1p1      2048    1050623   1048576   512M EFI System
/dev/nvme0n1p2   1050624    3147775   2097152     1G Linux filesystem
/dev/nvme0n1p3   3147776 1000215182 997067407 475.4G Linux filesystem""",

    "cat /boot/grub/grub.cfg": """\
#
# DO NOT EDIT THIS FILE
#
# It is automatically generated by grub-mkconfig using templates
# from /etc/grub.d and settings from /etc/default/grub
#

### BEGIN /etc/grub.d/00_header ###
if [ -s $prefix/grubenv ]; then
  load_env
fi
set default="0"
set timeout=5

### BEGIN /etc/grub.d/10_linux ###
menuentry 'Debian GNU/Linux' --class debian --class gnu-linux {
        load_video
        insmod gzio
        insmod part_gpt
        insmod ext2
        set root='hd0,gpt2'
        linux   /vmlinuz-6.1.0-17-amd64 root=/dev/nvme0n1p3 ro quiet
        initrd  /initrd.img-6.1.0-17-amd64
}
menuentry 'Debian GNU/Linux (recovery mode)' {
        linux   /vmlinuz-6.1.0-17-amd64 root=/dev/nvme0n1p3 ro single
        initrd  /initrd.img-6.1.0-17-amd64
}""",

    "cat /etc/default/grub": """\
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.

GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""

# Uncomment to enable BadRAM filtering
#GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xfefefefe"

# Uncomment to disable graphical terminal
#GRUB_TERMINAL=console

# The resolution used on graphical terminal
#GRUB_GFXMODE=640x480

# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
#GRUB_DISABLE_LINUX_UUID=true""",

    "update-grub": """\
Sourcing file `/etc/default/grub'
Sourcing file `/etc/default/grub.d/init-select.cfg'
Generating grub configuration file ...
Found linux image: /boot/vmlinuz-6.1.0-17-amd64
Found initrd image: /boot/initrd.img-6.1.0-17-amd64
Found linux image: /boot/vmlinuz-6.1.0-16-amd64
Found initrd image: /boot/initrd.img-6.1.0-16-amd64
done""",

    "grub-install /dev/nvme0n1": """\
Installing for x86_64-efi platform.
Installation finished. No error reported.""",

    "grub-install /dev/sda": """\
Installing for i386-pc platform.
Installation finished. No error reported.""",

    "cat /proc/cmdline": "BOOT_IMAGE=/vmlinuz-6.1.0-17-amd64 root=/dev/nvme0n1p3 ro quiet splash",

    "ls /boot": """\
config-6.1.0-17-amd64  grub  initrd.img  initrd.img-6.1.0-17-amd64
initrd.img-6.1.0-16-amd64  System.map-6.1.0-17-amd64
vmlinuz  vmlinuz-6.1.0-17-amd64  vmlinuz-6.1.0-16-amd64""",

    "ls /boot/grub": "fonts  grub.cfg  grubenv  i386-pc  locale  unicode.pf2",

    "efibootmgr": """\
BootCurrent: 0001
Timeout: 1 seconds
BootOrder: 0001,0002,0000
Boot0000* Windows Boot Manager
Boot0001* debian
Boot0002* UEFI: SanDisk, Partition 1""",

    "efibootmgr -v": """\
BootCurrent: 0001
Timeout: 1 seconds
BootOrder: 0001,0002,0000
Boot0000* Windows Boot Manager	HD(1,GPT,abcd1234,0x800,0x82000)/File(\\EFI\\Microsoft\\Boot\\bootmgfw.efi)
Boot0001* debian	HD(1,GPT,abcd1234,0x800,0x82000)/File(\\EFI\\debian\\grubx64.efi)
Boot0002* UEFI: SanDisk, Partition 1	PciRoot(0x0)/Pci(0x14,0x0)/USB(1,0)""",

    "update-initramfs -u": """\
update-initramfs: Generating /boot/initrd.img-6.1.0-17-amd64""",

    "mkinitramfs -o /boot/initrd.img-test 6.1.0-17-amd64": """\
mkinitramfs: writing to /boot/initrd.img-test""",

    "ls -la /sys/firmware/efi": """\
total 0
drwxr-xr-x  7 root root 0 Jan 15 08:00 .
drwxr-xr-x 10 root root 0 Jan 15 08:00 ..
drwxr-xr-x  2 root root 0 Jan 15 08:00 efivars
drwxr-xr-x  2 root root 0 Jan 15 08:00 vars
-r--r--r--  1 root root 0 Jan 15 08:00 fw_platform_size
-r--r--r--  1 root root 0 Jan 15 08:00 fw_vendor""",

    # ── Kapitel 3: Init / systemd / SysVinit ─────────────────────────────────

    "runlevel": "N 5",

    "who -r": "         run-level 5  2089-01-15 08:00",

    "telinit 3": "(switching to runlevel 3 — graphical login disabled)",
    "telinit 6": "(rebooting system...)",

    "cat /etc/inittab": """\
# /etc/inittab -- init(8) configuration.
# Default runlevel.
id:5:initdefault:

# System initialization
si::sysinit:/etc/init.d/rcS

l0:0:wait:/etc/init.d/rc 0
l1:1:wait:/etc/init.d/rc 1
l2:2:wait:/etc/init.d/rc 2
l3:3:wait:/etc/init.d/rc 3
l4:4:wait:/etc/init.d/rc 4
l5:5:wait:/etc/init.d/rc 5
l6:6:wait:/etc/init.d/rc 6

# Ctrl-Alt-Delete
ca:12345:ctrlaltdel:/sbin/shutdown -t1 -a -r now

# Terminals
1:2345:respawn:/sbin/getty 38400 tty1
2:23:respawn:/sbin/getty 38400 tty2""",

    "ls /etc/init.d/": """\
README        cron          networking    rsyslog       udev
apache2       dbus          nfs-common    ssh           ufw
bluetooth     hostname.sh   procps        sudo          x11-common""",

    "ls /etc/rc3.d/": """\
K01apache2  S01cron  S01dbus  S01networking  S01rsyslog  S02ssh""",

    "service ssh status": """\
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2089-01-15 08:00:01 UTC; 5min ago
   Main PID: 1337 (sshd)
      Tasks: 1 (limit: 4915)
     Memory: 2.3M
        CPU: 89ms
     CGroup: /system.slice/ssh.service
             └─1337 sshd: /usr/sbin/sshd -D""",

    "service ssh start": "Starting OpenBSD Secure Shell server: sshd.",
    "service ssh stop": "Stopping OpenBSD Secure Shell server: sshd.",
    "service ssh restart": """\
Stopping OpenBSD Secure Shell server: sshd.
Starting OpenBSD Secure Shell server: sshd.""",

    "systemctl status ssh": """\
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2089-01-15 08:00:01 UTC; 5min ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 1337 (sshd)
      Tasks: 1 (limit: 4915)
     Memory: 2.3M
        CPU: 89ms
     CGroup: /system.slice/ssh.service
             └─1337 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups

Jan 15 08:00:01 neongrid9 systemd[1]: Starting OpenBSD Secure Shell server...
Jan 15 08:00:01 neongrid9 sshd[1337]: Server listening on 0.0.0.0 port 22.
Jan 15 08:00:01 neongrid9 systemd[1]: Started OpenBSD Secure Shell server.""",

    "systemctl status nginx": """\
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; disabled; vendor preset: enabled)
     Active: inactive (dead)""",

    "systemctl start ssh": "(no output — success is silence in systemd)",
    "systemctl stop ssh": "(ssh.service stopped)",
    "systemctl restart ssh": "(ssh.service restarted)",
    "systemctl reload ssh": "(ssh.service reloaded — config re-read, connections kept)",

    "systemctl enable ssh": """\
Created symlink /etc/systemd/system/multi-user.target.wants/ssh.service → /lib/systemd/system/ssh.service.""",

    "systemctl disable ssh": """\
Removed /etc/systemd/system/multi-user.target.wants/ssh.service.""",

    "systemctl is-active ssh": "active",
    "systemctl is-active nginx": "inactive",
    "systemctl is-enabled ssh": "enabled",
    "systemctl is-enabled nginx": "disabled",

    "systemctl list-units": """\
  UNIT                          LOAD   ACTIVE SUB     DESCRIPTION
  cron.service                  loaded active running Regular background program processing daemon
  dbus.service                  loaded active running D-Bus System Message Bus
  networking.service            loaded active exited  Raise network interfaces
  rsyslog.service               loaded active running System Logging Service
  ssh.service                   loaded active running OpenBSD Secure Shell server
  systemd-journald.service      loaded active running Journal Service
  systemd-logind.service        loaded active running Login Service
  systemd-udevd.service         loaded active running udev Kernel Device Manager
  graphical.target              loaded active active  Graphical Interface
  multi-user.target             loaded active active  Multi-User System
  network.target                loaded active active  Network

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state.
SUB    = The low-level unit activation state.
11 loaded units listed.""",

    "systemctl list-units --type=service": """\
  UNIT                          LOAD   ACTIVE SUB     DESCRIPTION
  cron.service                  loaded active running Regular background processing
  dbus.service                  loaded active running D-Bus System Message Bus
  rsyslog.service               loaded active running System Logging Service
  ssh.service                   loaded active running OpenBSD Secure Shell server
  systemd-journald.service      loaded active running Journal Service

LOAD   = Reflects whether the unit definition was properly loaded.
5 loaded units listed.""",

    "systemctl list-units --type=target": """\
  UNIT                   LOAD   ACTIVE SUB    DESCRIPTION
  basic.target           loaded active active Basic System
  graphical.target       loaded active active Graphical Interface
  multi-user.target      loaded active active Multi-User System
  network.target         loaded active active Network
  sysinit.target         loaded active active System Initialization

5 loaded units listed.""",

    "systemctl get-default": "graphical.target",

    "systemctl set-default multi-user.target": """\
Created symlink /etc/systemd/system/default.target → /lib/systemd/system/multi-user.target.""",

    "systemctl set-default graphical.target": """\
Created symlink /etc/systemd/system/default.target → /lib/systemd/system/graphical.target.""",

    "systemctl isolate rescue.target": """\
(switching to rescue.target — single-user mode, most services stopped)""",

    "systemctl isolate multi-user.target": """\
(switching to multi-user.target — text login, no GUI)""",

    "systemctl mask ssh": """\
Created symlink /etc/systemd/system/ssh.service → /dev/null.""",

    "systemctl unmask ssh": """\
Removed /etc/systemd/system/ssh.service.""",

    "systemctl cat ssh": """\
# /lib/systemd/system/ssh.service
[Unit]
Description=OpenBSD Secure Shell server
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target auditd.service
ConditionPathExists=!/etc/ssh/sshd_not_to_be_run

[Service]
EnvironmentFile=-/etc/default/ssh
ExecStartPre=/usr/sbin/sshd -t
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
ExecReload=/usr/sbin/sshd -t
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255
Type=notify
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
Alias=sshd.service""",

    "journalctl -u ssh": """\
-- Journal begins at Wed 2089-01-15 07:59:00 UTC, ends at Wed 2089-01-15 08:05:01 UTC. --
Jan 15 08:00:00 neongrid9 systemd[1]: Starting OpenBSD Secure Shell server...
Jan 15 08:00:01 neongrid9 sshd[1337]: Server listening on 0.0.0.0 port 22.
Jan 15 08:00:01 neongrid9 sshd[1337]: Server listening on :: port 22.
Jan 15 08:00:01 neongrid9 systemd[1]: Started OpenBSD Secure Shell server.""",

    "journalctl -f": """\
-- Logs begin at Wed 2089-01-15 07:59:00 UTC. --
Jan 15 08:05:00 neongrid9 systemd[1]: Starting Daily apt upgrade...
Jan 15 08:05:01 neongrid9 cron[2345]: (root) CMD (test -x /usr/sbin/anacron || ...)
Jan 15 08:05:01 neongrid9 kernel: audit: type=1400 audit(1705312301.123:45)
(Ctrl-C to stop following)""",

    "journalctl -n 20": """\
-- Logs begin at Wed 2089-01-15 07:59:00 UTC. --
Jan 15 08:04:50 neongrid9 sshd[1337]: Accepted publickey for root
Jan 15 08:04:51 neongrid9 systemd-logind[987]: New session 2 of user root.
Jan 15 08:05:00 neongrid9 systemd[1]: Starting Daily apt upgrade...
Jan 15 08:05:01 neongrid9 kernel: audit: type=1400""",

    "journalctl --since today": """\
-- Logs begin at Wed 2089-01-15 00:00:00 UTC. --
Jan 15 08:00:00 neongrid9 kernel: Linux version 6.1.0-17-amd64
Jan 15 08:00:01 neongrid9 systemd[1]: Started OpenBSD Secure Shell server.
Jan 15 08:00:02 neongrid9 systemd[1]: Reached target graphical.target""",

    "journalctl --since \"1 hour ago\"": """\
-- Logs begin at Wed 2089-01-15 07:05:00 UTC. --
Jan 15 08:00:00 neongrid9 kernel: Linux version 6.1.0-17-amd64
Jan 15 08:00:01 neongrid9 systemd[1]: Started OpenBSD Secure Shell server.""",

    "journalctl -p err": """\
-- Logs begin at Wed 2089-01-15 07:59:00 UTC. --
Jan 15 08:00:01 neongrid9 kernel: [    0.299456] ACPI Error: AE_NOT_FOUND
Jan 15 08:00:03 neongrid9 kernel: EXT4-fs error: ext4_validate_block_bitmap""",

    "journalctl -b": """\
-- Boot 7a3f2b1c4d5e6f8a (Wed 2089-01-15 07:59:58 UTC) --
Jan 15 07:59:58 neongrid9 kernel: Linux version 6.1.0-17-amd64
Jan 15 07:59:59 neongrid9 kernel: [    0.000000] BIOS-e820: usable memory regions
Jan 15 08:00:01 neongrid9 systemd[1]: Reached target basic.target
Jan 15 08:00:02 neongrid9 systemd[1]: Reached target multi-user.target
Jan 15 08:00:03 neongrid9 systemd[1]: Reached target graphical.target
Jan 15 08:00:03 neongrid9 systemd[1]: Startup finished in 2.891s (kernel) + 1.234s (userspace) = 4.125s""",

    "systemd-analyze": "Startup finished in 2.891s (kernel) + 1.234s (userspace) = 4.125s",

    "systemd-analyze blame": """\
          1.234s NetworkManager-wait-online.service
           890ms plymouth-quit-wait.service
           543ms dev-nvme0n1p3.device
           432ms systemd-journal-flush.service
           345ms accounts-daemon.service
           234ms udisks2.service
           198ms avahi-daemon.service
           178ms ssh.service
           134ms rsyslog.service
            98ms cron.service""",

    "systemd-analyze critical-chain": """\
graphical.target @4.125s
└─multi-user.target @4.124s
  └─ssh.service @3.946s +178ms
    └─network.target @3.944s
      └─NetworkManager.service @1.234s +2.710s
        └─dbus.service @1.100s +134ms
          └─basic.target @1.099s""",

    "ps -p 1": """\
    PID TTY          TIME CMD
      1 ?        00:00:03 systemd""",

    "cat /proc/1/comm": "systemd",

    "ps aux | grep systemd": """\
root           1  0.0  0.0 168932 14256 ?        Ss   08:00   0:03 /sbin/init
root         567  0.0  0.0  17304  8192 ?        Ss   08:00   0:00 /lib/systemd/systemd-journald
root         601  0.0  0.0  21908  7168 ?        Ss   08:00   0:00 /lib/systemd/systemd-udevd""",

    "shutdown -h now": "(Broadcast message from root: The system is going down for power off NOW!)",
    "shutdown -r now": "(Broadcast message from root: The system is going down for reboot NOW!)",
    "shutdown -h +5": "(Broadcast message: System will shut down in 5 minutes)",
    "halt": "(System halted)",
    "reboot": "(Rebooting...)",
    "poweroff": "(Powering off...)",

    "ls /lib/systemd/system/": """\
basic.target           multi-user.target      ssh.service
cron.service           network.target         sysinit.target
dbus.service           poweroff.target        systemd-journald.service
getty@.service         reboot.target          systemd-logind.service
graphical.target       rescue.target          systemd-udevd.service""",

    "cat /lib/systemd/system/cron.service": """\
[Unit]
Description=Regular background program processing daemon
Documentation=man:cron(8)
After=remote-fs.target nss-user-lookup.target

[Service]
EnvironmentFile=-/etc/default/cron
ExecStart=/usr/sbin/cron -f $EXTRA_OPTS
IgnoreSIGPIPE=false
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target""",

    "systemctl daemon-reload": "(systemd configuration reloaded — no output on success)",

    # ── Kapitel 5: Rechte, Links, FHS ────────────────────────────────────

    "ls -l": """\
total 64
drwxr-xr-x  2 root root  4096 Jan 15 08:00 bin
drwxr-xr-x  4 root root  4096 Jan 15 08:00 boot
drwxr-xr-x 17 root root  3780 Jan 15 08:00 dev
drwxr-xr-x 87 root root  4096 Jan 15 08:01 etc
drwxr-xr-x  3 root root  4096 Jan 14 10:00 home
lrwxrwxrwx  1 root root     7 Jan 10 00:00 lib -> usr/lib
drwxr-xr-x  2 root root  4096 Jan 10 00:00 media
drwxr-xr-x  2 root root  4096 Jan 10 00:00 mnt
drwxr-xr-x  2 root root  4096 Jan 10 00:00 opt
dr-xr-xr-x 13 root root     0 Jan 15 08:00 proc
drwx------  5 root root  4096 Jan 14 22:00 root
drwxr-xr-x 26 root root   820 Jan 15 08:01 run
lrwxrwxrwx  1 root root     8 Jan 10 00:00 sbin -> usr/sbin
drwxr-xr-x  2 root root  4096 Jan 10 00:00 srv
dr-xr-xr-x 13 root root     0 Jan 15 08:00 sys
drwxrwxrwt 18 root root  4096 Jan 15 08:05 tmp
drwxr-xr-x 11 root root  4096 Jan 10 00:00 usr
drwxr-xr-x 13 root root  4096 Jan 10 00:00 var""",

    "ls -la": """\
total 68
drwxr-xr-x  19 root  root  4096 Jan 15 08:00 .
drwxr-xr-x  19 root  root  4096 Jan 15 08:00 ..
drwxr-xr-x   2 root  root  4096 Jan 15 08:00 bin
drwxr-xr-x   4 root  root  4096 Jan 15 08:00 boot
drwxr-xr-x  17 root  root  3780 Jan 15 08:00 dev
drwxr-xr-x  87 root  root  4096 Jan 15 08:01 etc
drwxrwxrwt  18 root  root  4096 Jan 15 08:05 tmp
drwxr-xr-x  11 root  root  4096 Jan 10 00:00 usr
drwxr-xr-x  13 root  root  4096 Jan 10 00:00 var""",

    "ls /": "bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var",

    "ls -la /home/ghost": """\
total 44
drwxr-xr-x  5 ghost ghost 4096 Jan 15 08:00 .
drwxr-xr-x  3 root  root  4096 Jan 14 10:00 ..
-rw-r--r--  1 ghost ghost  220 Jan 14 10:00 .bash_logout
-rw-r--r--  1 ghost ghost 3526 Jan 14 10:00 .bashrc
-rw-r--r--  1 ghost ghost  807 Jan 14 10:00 .profile
drwxr-xr-x  2 ghost ghost 4096 Jan 15 07:00 .ssh
-rwxr-xr-x  1 ghost ghost 8192 Jan 15 08:00 scan.sh
-rw-rw-r--  1 ghost hackers 512 Jan 15 08:01 notes.txt
lrwxrwxrwx  1 ghost ghost   17 Jan 15 08:00 config -> /etc/neongrid.conf""",

    "ls -l /usr/bin/passwd": "-rwsr-xr-x 1 root root 59976 Mar 22 2023 /usr/bin/passwd",
    "ls -l /tmp": "drwxrwxrwt 18 root root 4096 Jan 15 08:05 /tmp",
    "ls -ld /tmp": "drwxrwxrwt 18 root root 4096 Jan 15 08:05 /tmp",

    "ls -li": """\
131073 -rw-r--r-- 2 root  root   2456 Jan 15 08:00 /etc/hosts
131073 -rw-r--r-- 2 root  root   2456 Jan 15 08:00 /tmp/hosts_hard
789012 lrwxrwxrwx 1 ghost ghost    10 Jan 15 08:01 /tmp/hosts_sym -> /etc/hosts""",

    "stat /etc/passwd": """\
  File: /etc/passwd
  Size: 2456            Blocks: 8          IO Block: 4096   regular file
Device: fd01h/64769d    Inode: 131073       Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2089-01-15 07:59:58.123456789 +0000
Modify: 2089-01-14 12:00:01.987654321 +0000
Change: 2089-01-14 12:00:01.987654321 +0000
 Birth: 2089-01-10 00:00:00.000000000 +0000""",

    "file /etc/passwd": "/etc/passwd: ASCII text",
    "file /bin/ls":     "/bin/ls: ELF 64-bit LSB pie executable, x86-64, dynamically linked",
    "file /tmp":        "/tmp: sticky, directory",

    "umask":    "0022",
    "umask -S": "u=rwx,g=rx,o=rx",

    "id":           "uid=1000(ghost) gid=1000(ghost) groups=1000(ghost),27(sudo),1001(hackers)",
    "id ghost":     "uid=1000(ghost) gid=1000(ghost) groups=1000(ghost),27(sudo),1001(hackers)",
    "groups":       "ghost sudo hackers",

    "which ls":     "/bin/ls",
    "which python3":"/usr/bin/python3",
    "which bash":   "/bin/bash",
    "whereis bash": "bash: /bin/bash /etc/bash.bashrc /usr/share/man/man1/bash.1.gz",
    "whereis ls":   "ls: /bin/ls /usr/share/man/man1/ls.1.gz",
    "type ls":      "ls is /bin/ls",
    "type cd":      "cd is a shell builtin",

    "find /etc -name '*.conf'": """\
/etc/ldap/ldap.conf
/etc/nginx/nginx.conf
/etc/ssh/sshd_config
/etc/rsyslog.conf
/etc/logrotate.conf
/etc/nsswitch.conf""",

    "find / -perm -4000 2>/dev/null": """\
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/su
/usr/bin/newgrp
/usr/lib/openssh/ssh-keysign
/usr/sbin/pam_extrausers_chkpwd""",

    "find /var/log -name '*.log'": """\
/var/log/syslog
/var/log/auth.log
/var/log/kern.log
/var/log/dpkg.log
/var/log/nginx/access.log
/var/log/nginx/error.log""",

    "readlink /tmp/hosts_sym": "/etc/hosts",
    "readlink -f /tmp/hosts_sym": "/etc/hosts",

    # ── Kapitel 7: Prozesse, Signale & Prioritäten ───────────────────────────
    "ps aux": """\
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1 168228 13240 ?        Ss   08:00   0:03 /sbin/init
root           2  0.0  0.0      0     0 ?        S    08:00   0:00 [kthreadd]
root          10  0.0  0.0      0     0 ?        I<   08:00   0:00 [rcu_sched]
root         512  0.0  0.1  17276  7532 ?        Ss   08:00   0:01 /lib/systemd/systemd-journald
root         789  0.0  0.1  14968  5120 ?        Ss   08:00   0:00 /usr/sbin/sshd -D
root        1234  0.0  0.0  28324  4096 ?        Ss   08:01   0:00 cron
ghost       2001  0.2  0.5 754832 42100 pts/0    Sl+  09:15   0:04 python3 main.py
ghost       2099  0.0  0.0  16892  3416 pts/0    S+   09:20   0:00 bash
root        2100  0.0  0.0  16384  1024 ?        R    09:20   0:00 ps aux""",

    "ps -ef": """\
UID          PID  PPID  C STIME TTY          TIME CMD
root           1     0  0 08:00 ?        00:00:03 /sbin/init
root           2     1  0 08:00 ?        00:00:00 [kthreadd]
root         512     1  0 08:00 ?        00:00:01 /lib/systemd/systemd-journald
root         789     1  0 08:00 ?        00:00:00 /usr/sbin/sshd -D
ghost       2001  2099  0 09:15 pts/0    00:00:04 python3 main.py
ghost       2099  2098  0 09:20 pts/0    00:00:00 bash
root        2101     1  0 09:20 ?        00:00:00 ps -ef""",

    "ps -aux": """\
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.1 168228 13240 ?        Ss   08:00   0:03 /sbin/init
ghost       2001  0.2  0.5 754832 42100 pts/0    Sl+  09:15   0:04 python3 main.py
ghost       2099  0.0  0.0  16892  3416 pts/0    S+   09:20   0:00 bash""",

    "pstree": """\
systemd─┬─cron
        ├─sshd───sshd───bash───python3
        ├─systemd-journal
        ├─systemd-logind
        └─2*[kworker/u8:1]""",

    "pstree -p": """\
systemd(1)─┬─cron(1234)
           ├─sshd(789)───sshd(2098)───bash(2099)───python3(2001)
           ├─systemd-journal(512)
           └─kthreadd(2)""",

    "pgrep sshd": """\
789
2098""",

    "pgrep -l sshd": """\
789 sshd
2098 sshd""",

    "top": """\
top - 09:25:01 up 1:25,  2 users,  load average: 0.15, 0.22, 0.18
Tasks: 142 total,   1 running, 141 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.3 us,  0.8 sy,  0.0 ni, 96.5 id,  0.2 wa,  0.0 hi,  0.2 si
MiB Mem : 15987.2 total,  8421.3 free,  4532.1 used,  3033.8 buff/cache
MiB Swap:  4096.0 total,  4096.0 free,     0.0 used. 10912.4 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 2001 ghost     20   0  754832  42100  18432 S   2.3   0.3   0:04.12 python3
  789 root      20   0   14968   5120   4096 S   0.0   0.0   0:00.23 sshd
    1 root      20   0  168228  13240   9216 S   0.0   0.1   0:03.15 systemd""",

    "uptime": """\
 09:25:01 up 1:25,  2 users,  load average: 0.15, 0.22, 0.18""",

    "uptime -p": "up 1 hour, 25 minutes",

    "kill -15 2001": "(SIGTERM gesendet an PID 2001)",
    "kill -9 2001":  "(SIGKILL gesendet an PID 2001 — Prozess sofort beendet)",
    "kill 2001":     "(SIGTERM gesendet an PID 2001)",
    "kill -SIGTERM 2001": "(SIGTERM gesendet an PID 2001)",
    "kill -SIGKILL 2001": "(SIGKILL gesendet an PID 2001 — nicht blockierbar)",
    "kill -l": """\
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL
 5) SIGTRAP      6) SIGABRT      7) SIGBUS       8) SIGFPE
 9) SIGKILL     10) SIGUSR1     11) SIGSEGV     12) SIGUSR2
13) SIGPIPE     14) SIGALRM     15) SIGTERM     16) SIGSTKFLT
17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP""",

    "killall python3": "(SIGTERM an alle python3-Prozesse gesendet)",
    "pkill python3":   "(Prozesse mit Name 'python3' beendet)",
    "pkill -9 python3": "(SIGKILL an alle python3-Prozesse)",

    "jobs": """\
[1]  Running    sleep 100 &
[2]- Stopped   vim notes.txt
[3]+ Running   python3 monitor.py &""",

    "fg": "(Vordergrundprozess: python3 monitor.py)",
    "fg 1": "(sleep 100 in den Vordergrund geholt)",
    "bg": "(sleep 100 läuft jetzt im Hintergrund weiter)",
    "bg 2": "(vim notes.txt wird im Hintergrund fortgesetzt)",

    "nohup python3 server.py &": """\
nohup: ignoring input and appending output to 'nohup.out'
[1] 3042""",

    "nice -n 10 python3 cpu_task.py": "(python3 cpu_task.py mit nice=10 gestartet)",
    "nice --adjustment=10 python3 cpu_task.py": "(python3 mit niceness 10 gestartet)",

    "renice -n 5 -p 2001": "2001 (process priority) old priority 0, new priority 5",
    "renice 5 2001":        "2001 (process priority) old priority 0, new priority 5",

    "free": """\
               total        used        free      shared  buff/cache   available
Mem:        16370688     4641792     8623104      483328     3105792    11175936
Swap:        4194304           0     4194304""",

    "free -h": """\
               total        used        free      shared  buff/cache   available
Mem:            15Gi       4.4Gi       8.2Gi       472Mi       3.0Gi        10Gi
Swap:          4.0Gi          0B       4.0Gi""",

    "free -m": """\
               total        used        free      shared  buff/cache   available
Mem:           15987        4533        8420         472        3033       10913
Swap:           4095           0        4095""",

    "vmstat": """\
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 8420480 524288 2582528    0    0    12     8  312  521  3  1 96  0  0""",

    "vmstat 1 5": """\
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 8420480 524288 2582528    0    0    12     8  312  521  3  1 96  0  0
 0  0      0 8419200 524288 2582528    0    0     0     0  289  498  2  0 98  0  0
 0  0      0 8419200 524288 2582528    0    0     0     4  301  512  1  0 99  0  0""",

    "iostat": """\
Linux 6.1.0-neongrid9  09/25/2089  _x86_64_

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.34    0.00    0.82    0.18    0.00   96.66

Device             tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
nvme0n1           8.23       102.4        45.2     1024568     452134
sda               0.12         1.2         0.4       12345       4234""",

    "lsof": """\
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
systemd     1   root  cwd    DIR    8,1     4096    2 /
systemd     1   root  txt    REG    8,1  1621544   1234 /lib/systemd/systemd
python3  2001  ghost  cwd    DIR    8,1     4096  5678 /home/ghost/neongrid9
python3  2001  ghost    0u   CHR  136,0      0t0     3 /dev/pts/0
python3  2001  ghost    1u   CHR  136,0      0t0     3 /dev/pts/0
sshd      789   root    3u  IPv4  15234      0t0   TCP *:ssh (LISTEN)
sshd      789   root    4u  IPv6  15235      0t0   TCP *:ssh (LISTEN)""",

    "lsof -i": """\
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd      789   root    3u  IPv4  15234      0t0   TCP *:ssh (LISTEN)
sshd      789   root    4u  IPv6  15235      0t0   TCP *:ssh (LISTEN)
sshd     2098   root    3u  IPv4  19823      0t0   TCP neongrid9:ssh->client:51234 (ESTABLISHED)
nginx     1500   root    6u  IPv4  20012      0t0   TCP *:http (LISTEN)
nginx     1500   root    7u  IPv4  20013      0t0   TCP *:https (LISTEN)""",

    "lsof -i :22": """\
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd     789 root    3u  IPv4  15234      0t0   TCP *:ssh (LISTEN)
sshd     789 root    4u  IPv6  15235      0t0   TCP *:ssh (LISTEN)
sshd    2098 root    3u  IPv4  19823      0t0   TCP neongrid9:ssh->client:51234 (ESTABLISHED)""",

    "lsof -p 2001": """\
COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3  2001 ghost  cwd    DIR    8,1     4096  5678 /home/ghost/neongrid9
python3  2001 ghost  txt    REG    8,1  5242880  9012 /usr/bin/python3.11
python3  2001 ghost    0u   CHR  136,0      0t0     3 /dev/pts/0
python3  2001 ghost    1u   CHR  136,0      0t0     3 /dev/pts/0
python3  2001 ghost    2u   CHR  136,0      0t0     3 /dev/pts/0""",

    "fuser /dev/sda1": "/dev/sda1:            1234  5678m",
    "fuser -v /dev/sda1": """\
                     USER        PID ACCESS COMMAND
/dev/sda1:           root       1234 f....  systemd
                     root       5678 F....  udisksd""",
    "fuser -k /mnt/usb": "(SIGTERM an alle Prozesse gesendet die /mnt/usb nutzen)",

    "screen": "(GNU Screen gestartet — Strg+A D zum Trennen)",
    "screen -ls": """\
There are screens on:
\t12345.pts-0.neongrid9\t(09/25/2089 09:00:00)\t(Detached)
\t12346.pts-1.neongrid9\t(09/25/2089 09:10:00)\t(Attached)
2 Sockets in /run/screen/S-ghost.""",

    "screen -r": "(Screen-Session wiederhergestellt)",
    "screen -r 12345": "(Screen 12345 wiederhergestellt)",
    "screen -d -r": "(Screen forcefully detached und reconnected)",

    "tmux": "(neue tmux-Session gestartet)",
    "tmux ls": """\
0: 2 windows (created Mon Sep 25 09:00:00 2089) [220x50]
1: 1 windows (created Mon Sep 25 09:10:00 2089) [220x50]""",
    "tmux new-session -s main": "(tmux-Session 'main' erstellt)",
    "tmux attach -t main": "(tmux-Session 'main' wiederhergestellt)",
    "tmux attach": "(tmux-Session 0 wiederhergestellt)",

    "cat /proc/loadavg": "0.15 0.22 0.18 2/142 2101",
    "cat /proc/cpuinfo": """\
processor\t: 0
vendor_id\t: GenuineIntel
cpu family\t: 6
model name\t: Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz
cpu MHz\t\t: 1800.000
cache size\t: 8192 KB
physical id\t: 0
core id\t\t: 0""",

    "cat /proc/meminfo": """\
MemTotal:       16370688 kB
MemFree:         8623104 kB
MemAvailable:   11175936 kB
Buffers:          524288 kB
Cached:          2581504 kB
SwapTotal:       4194304 kB
SwapFree:        4194304 kB""",

    "watch ps aux": "(ps aux wird alle 2 Sekunden aktualisiert — Strg+C zum Beenden)",
    "watch -n 1 ps aux": "(ps aux wird jede Sekunde aktualisiert — Strg+C zum Beenden)",

    # ── Kapitel 8: Regex & vi ─────────────────────────────────────────────────
    "grep '^root' /etc/passwd": "root:x:0:0:root:/root:/bin/bash",

    "grep -E 'error|warning' /var/log/syslog": """\
Sep 25 09:01:23 neongrid9 kernel: [1234.567] warning: CPU thermal throttling
Sep 25 09:03:41 neongrid9 sshd[789]: error: PAM: Authentication failure
Sep 25 09:05:12 neongrid9 systemd[1]: warning: Unit cron.service entered degraded state
Sep 25 09:07:55 neongrid9 kernel: [2345.678] error: EXT4-fs: I/O error""",

    "grep -n 'error' /var/log/syslog": """\
42:Sep 25 09:03:41 neongrid9 sshd[789]: error: PAM: Authentication failure
87:Sep 25 09:07:55 neongrid9 kernel: [2345.678] error: EXT4-fs: I/O error
103:Sep 25 09:12:01 neongrid9 nginx[1500]: error: connect() failed (111)""",

    "grep -c 'error' /var/log/syslog": "3",

    "grep -i 'ERROR' /var/log/syslog": """\
Sep 25 09:03:41 neongrid9 sshd[789]: error: PAM: Authentication failure
Sep 25 09:07:55 neongrid9 kernel: [2345.678] Error: EXT4-fs: I/O error
Sep 25 09:12:01 neongrid9 nginx[1500]: ERROR: connect() failed (111)""",

    "grep -v '^#' /etc/hosts": """\
127.0.0.1   localhost
127.0.1.1   neongrid9
::1         localhost ip6-localhost ip6-loopback""",

    "grep '[[:digit:]]' /etc/passwd": """\
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash
zara:x:1001:1001:Zara Z3R0:/home/zara:/bin/bash""",

    "sed 's/error/ERROR/g' /var/log/test.log": """\
Sep 25 09:03:41 neongrid9 sshd[789]: ERROR: PAM: Authentication failure
Sep 25 09:07:55 neongrid9 kernel: [2345.678] ERROR: EXT4-fs: I/O error""",

    "sed '/^#/d' /etc/hosts": """\
127.0.0.1   localhost
127.0.1.1   neongrid9
::1         localhost ip6-localhost ip6-loopback""",

    "sed -n '1,5p' /etc/passwd": """\
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync""",

    "awk -F: '{print $1}' /etc/passwd": """\
root
daemon
bin
sys
sync
games
man
ghost
zara""",

    "awk -F: '$3 >= 1000 {print $1}' /etc/passwd": """\
ghost
zara""",

    "awk '/ERROR/ {print NR, $0}' /var/log/syslog": """\
42 Sep 25 09:03:41 neongrid9 sshd[789]: ERROR: PAM: Authentication failure
87 Sep 25 09:07:55 neongrid9 kernel: ERROR: EXT4-fs: I/O error""",

    "awk -F: '{print $1, $3}' /etc/passwd": """\
root 0
daemon 1
bin 2
ghost 1000
zara 1001""",

    "vi /etc/hosts": "(vi Editor geöffnet — :q! zum Beenden ohne Speichern)",
    "vi /etc/passwd": "(vi Editor geöffnet — :q! zum Beenden ohne Speichern)",
    "vi /etc/ssh/sshd_config": "(vi Editor geöffnet — :q! zum Beenden ohne Speichern)",
    "vim /etc/hosts": "(vim Editor geöffnet — :q! zum Beenden ohne Speichern)",

    ":%s/http/https/g": "(vi: alle 'http' durch 'https' ersetzt — :wq zum Speichern)",
    "dd": "(vi Normal-Modus: aktuelle Zeile in Puffer gelöscht)",
    "yy": "(vi Normal-Modus: aktuelle Zeile in Puffer kopiert)",

    # ── Kapitel 9: Netzwerk ───────────────────────────────────────────────────
    "ip addr show": """\
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:ab:cd:ef brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86391sec preferred_lft 86391sec
    inet6 fe80::5054:ff:feab:cdef/64 scope link
       valid_lft forever preferred_lft forever""",

    "ip a": """\
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 state UNKNOWN
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 state UP
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::5054:ff:feab:cdef/64 scope link""",

    "ip route show": """\
default via 192.168.1.1 dev eth0 proto dhcp src 192.168.1.100 metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100""",

    "ip r": """\
default via 192.168.1.1 dev eth0 proto dhcp
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100""",

    "ip link show": """\
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 52:54:00:ab:cd:ef brd ff:ff:ff:ff:ff:ff""",

    "ip link set eth0 up":   "(eth0 aktiviert)",
    "ip link set eth0 down": "(eth0 deaktiviert — Verbindung unterbrochen!)",

    "ifconfig": """\
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::5054:ff:feab:cdef  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:ab:cd:ef  txqueuelen 1000  (Ethernet)
        RX packets 12453  bytes 9871234 (9.8 MB)
        TX packets 8921   bytes 2345678 (2.3 MB)

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>""",

    "route -n": """\
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 eth0""",

    "ss -tulpn": """\
Netid  State   Recv-Q  Send-Q   Local Address:Port    Peer Address:Port  Process
udp    UNCONN  0       0              0.0.0.0:68           0.0.0.0:*      users:(("dhclient",pid=987,fd=6))
udp    UNCONN  0       0              0.0.0.0:5353         0.0.0.0:*
tcp    LISTEN  0       128            0.0.0.0:22           0.0.0.0:*      users:(("sshd",pid=789,fd=3))
tcp    LISTEN  0       511            0.0.0.0:80           0.0.0.0:*      users:(("nginx",pid=1500,fd=6))
tcp    LISTEN  0       511            0.0.0.0:443          0.0.0.0:*      users:(("nginx",pid=1500,fd=7))
tcp    LISTEN  0       128               [::]:22              [::]:*      users:(("sshd",pid=789,fd=4))""",

    "ss -tlnp": """\
State    Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN   0       128           0.0.0.0:22        0.0.0.0:*      users:(("sshd",pid=789,fd=3))
LISTEN   0       511           0.0.0.0:80        0.0.0.0:*      users:(("nginx",pid=1500,fd=6))
LISTEN   0       511           0.0.0.0:443       0.0.0.0:*      users:(("nginx",pid=1500,fd=7))""",

    "ss -tnp": """\
State        Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
ESTABLISHED  0       0       192.168.1.100:22    192.168.1.5:51234  users:(("sshd",pid=2098,fd=3))""",

    "ss -s": """\
Total: 142
TCP:   8 (estab 1, closed 0, orphaned 0, timewait 0)

Transport Total     IP        IPv6
RAW       0         0         0
UDP       3         2         1
TCP       8         5         3
INET      11        7         4
FRAG      0         0         0""",

    "netstat -tulpn": """\
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address    Foreign Address  State    PID/Program
tcp        0      0 0.0.0.0:22       0.0.0.0:*        LISTEN   789/sshd
tcp        0      0 0.0.0.0:80       0.0.0.0:*        LISTEN   1500/nginx
tcp        0      0 0.0.0.0:443      0.0.0.0:*        LISTEN   1500/nginx
udp        0      0 0.0.0.0:68       0.0.0.0:*                 987/dhclient""",

    "netstat -an": """\
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address     Foreign Address   State
tcp        0      0 0.0.0.0:22        0.0.0.0:*         LISTEN
tcp        0      0 192.168.1.100:22  192.168.1.5:51234 ESTABLISHED
tcp        0      0 0.0.0.0:80        0.0.0.0:*         LISTEN
tcp        0      0 0.0.0.0:443       0.0.0.0:*         LISTEN""",

    "netstat -r": """\
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         _gateway        0.0.0.0         UG        0 0          0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U         0 0          0 eth0""",

    "ping -c 4 8.8.8.8": """\
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=12.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=117 time=12.5 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 11.8/12.175/12.5/0.261 ms""",

    "ping -c 4 localhost": """\
PING localhost (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.041 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.048 ms
64 bytes from localhost (127.0.0.1): icmp_seq=3 ttl=64 time=0.044 ms
64 bytes from localhost (127.0.0.1): icmp_seq=4 ttl=64 time=0.042 ms

--- localhost ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 0.041/0.044/0.048/0.003 ms""",

    "traceroute 8.8.8.8": """\
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1)  0.412 ms  0.398 ms  0.389 ms
 2  10.0.0.1 (10.0.0.1)  1.823 ms  1.802 ms  1.798 ms
 3  172.16.5.1 (172.16.5.1)  5.234 ms  5.187 ms  5.203 ms
 4  * * *
 5  72.14.234.1 (72.14.234.1)  8.921 ms  8.897 ms  8.912 ms
 6  8.8.8.8 (8.8.8.8)  12.345 ms  12.312 ms  12.298 ms""",

    "tracepath 8.8.8.8": """\
 1?: [LOCALHOST]                      pmtu 1500
 1:  _gateway (192.168.1.1)           0.412ms
 2:  10.0.0.1 (10.0.0.1)              1.823ms
 3:  172.16.5.1 (172.16.5.1)          5.234ms
 4:  no reply
 5:  8.8.8.8 (8.8.8.8)               12.345ms reached
     Resume: pmtu 1500 hops 5 back 5""",

    "dig google.com": """\
; <<>> DiG 9.16.1 <<>> google.com
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             300     IN      A       142.250.185.46

;; Query time: 12 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Sep 25 09:25:00 UTC 2089
;; MSG SIZE  rcvd: 55""",

    "dig google.com MX": """\
; <<>> DiG 9.16.1 <<>> google.com MX
;; ANSWER SECTION:
google.com.             600     IN      MX      10 smtp.google.com.
google.com.             600     IN      MX      20 alt1.aspmx.l.google.com.

;; Query time: 15 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)""",

    "dig -x 8.8.8.8": """\
; <<>> DiG 9.16.1 <<>> -x 8.8.8.8
;; ANSWER SECTION:
8.8.8.8.in-addr.arpa.  21599   IN      PTR     dns.google.

;; SERVER: 8.8.8.8#53(8.8.8.8)""",

    "dig +short google.com": "142.250.185.46",

    "dig @8.8.8.8 google.com": """\
; <<>> DiG 9.16.1 <<>> @8.8.8.8 google.com
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; ANSWER SECTION:
google.com.             300     IN      A       142.250.185.46""",

    "host google.com": """\
google.com has address 142.250.185.46
google.com has IPv6 address 2a00:1450:4001:808::200e
google.com mail is handled by 10 smtp.google.com.""",

    "host -t MX google.com": """\
google.com mail is handled by 10 smtp.google.com.
google.com mail is handled by 20 alt1.aspmx.l.google.com.""",

    "nslookup google.com": """\
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
Name:   google.com
Address: 142.250.185.46""",

    "cat /etc/resolv.conf": """\
# Generated by NetworkManager
nameserver 8.8.8.8
nameserver 8.8.4.4
search neongrid9.local""",

    "cat /etc/hosts": """\
127.0.0.1   localhost
127.0.1.1   neongrid9
::1         localhost ip6-localhost ip6-loopback
192.168.1.1 gateway
192.168.1.100 neongrid9""",

    "cat /etc/nsswitch.conf": """\
passwd:         files systemd
group:          files systemd
shadow:         files
hosts:          files mdns4_minimal [NOTFOUND=return] dns
networks:       files
protocols:      db files
services:       db files""",

    "hostname": "neongrid9",
    "hostnamectl": """\
   Static hostname: neongrid9
         Icon name: computer-vm
           Chassis: vm
        Machine ID: a1b2c3d4e5f6789012345678901234ab
           Boot ID: b2c3d4e5f6789012345678901234abcd
    Virtualization: kvm
  Operating System: Ubuntu 22.04.3 LTS
            Kernel: Linux 6.1.0-neongrid9
      Architecture: x86-64""",

    "hostnamectl set-hostname neongrid9": "(Hostname dauerhaft auf 'neongrid9' gesetzt)",

    "nmcli device status": """\
DEVICE  TYPE      STATE      CONNECTION
eth0    ethernet  connected  Wired connection 1
lo      loopback  unmanaged  --""",

    "nmcli connection show": """\
NAME                UUID                                  TYPE      DEVICE
Wired connection 1  a1b2c3d4-e5f6-7890-abcd-ef1234567890  ethernet  eth0""",

    "ssh-keygen -t ed25519": """\
Generating public/private ed25519 key pair.
Enter file in which to save the key (/root/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_ed25519
Your public key has been saved in /root/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:xK2M8n3pQ4rT5sU6vW7xY8zA9bC0dE1fG2hI3jK4 ghost@neongrid9
The key's randomart image is:
+--[ED25519 256]--+
|        ..o.     |
|       . +.o     |
|      . o.o .    |
|     . oo+ +     |
|      oSo+= .    |
|     . .+o=+     |
|      ..oB+.E    |
|      .=oX+o     |
|      o+=oB+.    |
+----[SHA256]-----+""",

    "ssh-keygen -t rsa -b 4096": """\
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Your identification has been saved in /root/.ssh/id_rsa
Your public key has been saved in /root/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:xK2M8n3pQ4rT5sU6vW7xY8zA9bC0dE1fG RSA 4096""",

    "ssh-copy-id ghost@192.168.1.100": """\
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_ed25519.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s)
Number of key(s) added: 1

Now try logging into the machine: 'ssh ghost@192.168.1.100'""",

    "iptables -L": """\
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:ssh
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:http
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:https
ACCEPT     all  --  anywhere             anywhere             state RELATED,ESTABLISHED

Chain FORWARD (policy DROP)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination""",

    "iptables -L -n -v": """\
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target  prot opt in  out  source    destination
 1234  98K  ACCEPT  tcp  --  *   *    0.0.0.0/0 0.0.0.0/0  tcp dpt:22
  891  82K  ACCEPT  tcp  --  *   *    0.0.0.0/0 0.0.0.0/0  tcp dpt:80
  445  41K  ACCEPT  tcp  --  *   *    0.0.0.0/0 0.0.0.0/0  tcp dpt:443
  201  12K  DROP    all  --  *   *    0.0.0.0/0 0.0.0.0/0""",

    "ufw status": """\
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)""",

    "ufw allow 22":     "Rule added\nRule added (v6)",
    "ufw allow ssh":    "Rule added\nRule added (v6)",
    "ufw allow 80/tcp": "Rule added",
    "ufw deny 23":      "Rule added\nRule added (v6)",
    "ufw enable":       "Firewall is active and enabled on system startup",
    "ufw disable":      "Firewall stopped and disabled on system startup",

    "cat /etc/network/interfaces": """\
# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4""",

    "cat /etc/hostname": "neongrid9",

    # ── Kapitel 10: Benutzer, Gruppen, sudo, PAM ──────────────────────────────
    "cat /etc/passwd": """\
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash
zara:x:1001:1001:Zara Z3R0:/home/zara:/bin/bash""",

    "getent passwd ghost": "ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash",
    "getent passwd root":  "root:x:0:0:root:/root:/bin/bash",
    "getent passwd zara":  "zara:x:1001:1001:Zara Z3R0:/home/zara:/bin/bash",

    "id": "uid=1000(ghost) gid=1000(ghost) groups=1000(ghost),27(sudo),999(docker)",
    "id ghost": "uid=1000(ghost) gid=1000(ghost) groups=1000(ghost),27(sudo),999(docker)",
    "id root": "uid=0(root) gid=0(root) groups=0(root)",
    "whoami": "ghost",

    "chage -l ghost": """\
Last password change\t\t\t\t: Sep 01, 2089
Password expires\t\t\t\t: Nov 30, 2089
Password inactive\t\t\t\t: never
Account expires\t\t\t\t\t: never
Minimum number of days between password change\t: 7
Maximum number of days between password change\t: 90
Number of days of warning before password expires\t: 14""",

    "chage -M 90 ghost":        "(Max-Passwort-Alter auf 90 Tage gesetzt für ghost)",
    "chage -m 7 ghost":         "(Min-Passwort-Alter auf 7 Tage gesetzt für ghost)",
    "chage -W 14 ghost":        "(Passwort-Warnzeitraum auf 14 Tage gesetzt für ghost)",
    "chage -M 90 -m 7 -W 14 ghost": "(Passwort-Aging für ghost konfiguriert: max=90, min=7, warn=14)",
    "chage -d 0 ghost":         "(ghost muss Passwort beim nächsten Login ändern)",

    "passwd ghost":              "(Passwort für ghost wird gesetzt — Eingabe erforderlich)",
    "passwd -l ghost":           "passwd: password expiry information changed.",
    "passwd -u ghost":           "passwd: password expiry information changed.",
    "passwd -e ghost":           "passwd: password expiry information changed.",

    "useradd -m -s /bin/bash operator": "(Benutzer 'operator' erstellt mit Home-Verzeichnis und bash-Shell)",
    "useradd -m -s /bin/bash agent":    "(Benutzer 'agent' erstellt mit Home-Verzeichnis und bash-Shell)",
    "useradd -m operator":              "(Benutzer 'operator' erstellt mit Home-Verzeichnis)",
    "useradd -r svcuser":               "(System-Account 'svcuser' erstellt, UID < 1000)",

    "usermod -aG sudo ghost":    "(ghost zur Gruppe 'sudo' hinzugefügt)",
    "usermod -aG sudo agent":    "(agent zur Gruppe 'sudo' hinzugefügt)",
    "usermod -aG docker ghost":  "(ghost zur Gruppe 'docker' hinzugefügt)",
    "usermod -s /bin/zsh ghost": "(Shell für ghost auf /bin/zsh geändert)",
    "usermod -L ghost":          "(Account ghost gesperrt)",
    "usermod -U ghost":          "(Account ghost entsperrt)",

    "userdel -r ghost":          "(Account ghost + Home-Verzeichnis gelöscht)",
    "userdel ghost":             "(Account ghost gelöscht, Home-Verzeichnis bleibt)",

    "groupadd hackers":          "(Gruppe 'hackers' erstellt)",
    "groupadd -g 2000 hackers":  "(Gruppe 'hackers' mit GID 2000 erstellt)",
    "groupdel hackers":          "(Gruppe 'hackers' gelöscht)",

    "gpasswd -a ghost sudo":     "(ghost zur Gruppe 'sudo' hinzugefügt)",
    "gpasswd -a ghost hackers":  "(ghost zur Gruppe 'hackers' hinzugefügt)",
    "gpasswd -d ghost hackers":  "(ghost aus Gruppe 'hackers' entfernt)",

    "groups": "ghost sudo docker audio video plugdev",
    "groups ghost": "ghost : ghost sudo docker audio",

    "cat /etc/group": """\
root:x:0:
daemon:x:1:
bin:x:2:
sudo:x:27:ghost,zara
docker:x:999:ghost
audio:x:29:ghost
video:x:44:ghost
ghost:x:1000:
zara:x:1001:""",

    "cat /etc/shadow": """\
root:$6$rounds=656000$salty$hash...ROOTHASHHEXADEC:19601:0:99999:7:::
ghost:$6$rounds=656000$ghostsalt$ghosthash...LONGHASH:19601:7:90:14:::
zara:$6$rounds=656000$zarasalt$zarahash...LONGHASH:19601:0:99999:7:::
nobody:*:19601:0:99999:7:::""",

    "sudo -l": """\
Matching Defaults entries for ghost on neongrid9:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\\:/usr/local/bin

User ghost may run the following commands on neongrid9:
    (ALL : ALL) ALL""",

    "sudo -i": "(root Login-Shell gestartet — 'exit' zum Verlassen)",
    "sudo -s": "(root Shell gestartet — 'exit' zum Verlassen)",

    "visudo":  "(visudo geöffnet — /etc/sudoers sicher bearbeiten)",

    "su -":          "(root Login-Shell — 'exit' zum Verlassen)",
    "su - ghost":    "(ghost Login-Shell gestartet)",
    "su ghost":      "(zu ghost gewechselt, keine Login-Shell)",

    "ls /etc/pam.d/": """\
atd        common-account  common-session         login    runuser-l  sudo
chfn       common-auth     common-session-noninteractive  newusers  sshd
chpasswd   common-password  cron                   other    su         useradd
chsh       cron             lightdm                passwd   su-l""",

    "cat /etc/pam.d/sshd": """\
# PAM configuration for the Secure Shell daemon
@include common-auth
account    required     pam_nologin.so
@include common-account
session [success=ok ignore=ignore module_unknown=ignore default=bad] pam_selinux.so close
session    required     pam_loginuid.so
@include common-session
session    optional     pam_motd.so motd=/run/motd.dynamic
session    optional     pam_motd.so noupdate
session    optional     pam_mail.so standard noenv
session    required     pam_limits.so
session    required     pam_env.so user_readenv=1 envfile=/etc/default/locale""",

    "cat /etc/pam.d/sudo": """\
# PAM configuration for sudo
@include common-auth
session    required   pam_limits.so
session    required   pam_env.so readenv=1 user_readenv=0""",

    "cat /etc/security/limits.conf": """\
# /etc/security/limits.conf
#
# Each line describes a limit for a user in the form:
# <domain> <type> <item> <value>
#
#*               soft    core            0
#root            hard    core            100000
#*               hard    rss             10000
ghost           soft    nofile          1024
ghost           hard    nofile          4096
@docker         soft    nproc           100""",

    "cat /etc/profile": """\
# /etc/profile: system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

if [ "${PS1-}" ]; then
  if [ "${BASH-}" ] && [ "$BASH" != "/bin/sh" ]; then
    if [ -f /etc/bash.bashrc ]; then
      . /etc/bash.bashrc
    fi
  fi
fi

if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
  unset i
fi""",

    "cat ~/.bashrc": """\
# ~/.bashrc: executed by bash(1) for non-login shells.

# don't put duplicate lines or lines starting with space in the history
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command
shopt -s checkwinsize

# enable color support of ls
if [ -x /usr/bin/dircolors ]; then
    eval "$(dircolors -b)"
    alias ls='ls --color=auto'
fi

# some aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

PS1='\\u@\\h:\\w\\$ '""",

    "cat ~/.bash_profile": """\
# ~/.bash_profile: executed by bash for login shells.

# include .bashrc if it exists
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ]; then
    PATH="$HOME/bin:$PATH"
fi""",

    "ls /etc/profile.d/": """\
bash_completion.sh  locale.sh  vte-2.91.sh  z.sh
color-prompt.sh     01-locale-fix.sh""",

    "ls /etc/skel/": ".bash_logout  .bash_profile  .bashrc",
    "ls -la /etc/skel/": """\
total 28
drwxr-xr-x   2 root root 4096 Jan  1  2089 .
drwxr-xr-x 142 root root 4096 Jan  1  2089 ..
-rw-r--r--   1 root root  220 Jan  1  2089 .bash_logout
-rw-r--r--   1 root root 3526 Jan  1  2089 .bash_profile
-rw-r--r--   1 root root 3526 Jan  1  2089 .bashrc""",

    # ── Kapitel 11: Logging, Zeit, Cron ──────────────────────────────────────
    "tail -n 20 /var/log/syslog": """\
Sep 25 09:20:01 neongrid9 CRON[3042]: (root) CMD (/usr/bin/check_updates.sh)
Sep 25 09:20:05 neongrid9 systemd[1]: Started Daily apt download activities.
Sep 25 09:21:33 neongrid9 sshd[2098]: Accepted publickey for ghost from 192.168.1.5
Sep 25 09:22:01 neongrid9 kernel: [5432.123] EXT4-fs (nvme0n1p2): mounted filesystem
Sep 25 09:23:15 neongrid9 rsyslogd: [origin software="rsyslogd" swVersion="8.2001.0"]
Sep 25 09:24:02 neongrid9 sudo[2201]: ghost : TTY=pts/0 ; USER=root ; COMMAND=/bin/systemctl
Sep 25 09:24:10 neongrid9 systemd[1]: Starting Cleanup of Temporary Directories...
Sep 25 09:24:11 neongrid9 systemd[1]: Finished Cleanup of Temporary Directories.
Sep 25 09:25:00 neongrid9 CRON[3099]: (ghost) CMD (/home/ghost/monitor.sh)
Sep 25 09:25:01 neongrid9 sshd[789]: Received signal 1; restarting.""",

    "tail -f /var/log/syslog": "(Live-Ansicht von /var/log/syslog — Strg+C zum Beenden)",
    "tail -f /var/log/auth.log": "(Live-Ansicht von /var/log/auth.log — Strg+C zum Beenden)",

    "tail -n 50 /var/log/auth.log": """\
Sep 25 08:01:12 neongrid9 sshd[789]: Server listening on 0.0.0.0 port 22.
Sep 25 09:21:33 neongrid9 sshd[2098]: Accepted publickey for ghost from 192.168.1.5
Sep 25 09:21:33 neongrid9 sshd[2098]: pam_unix(sshd:session): session opened for user ghost
Sep 25 09:24:02 neongrid9 sudo[2201]: ghost : TTY=pts/0 ; USER=root ; COMMAND=/bin/systemctl status nginx
Sep 25 09:24:02 neongrid9 sudo[2201]: pam_unix(sudo:session): session opened for user root""",

    "grep 'Failed password' /var/log/auth.log": """\
Sep 25 07:14:23 neongrid9 sshd[1891]: Failed password for invalid user admin from 203.0.113.42
Sep 25 07:14:45 neongrid9 sshd[1892]: Failed password for root from 203.0.113.42
Sep 25 07:15:01 neongrid9 sshd[1893]: Failed password for invalid user pi from 203.0.113.42""",

    "cat /var/log/kern.log": """\
Sep 25 08:00:01 neongrid9 kernel: [    0.000000] Linux version 6.1.0-neongrid9
Sep 25 08:00:01 neongrid9 kernel: [    0.456789] Detected 8 CPU cores
Sep 25 08:00:02 neongrid9 kernel: [    1.234567] EXT4-fs (nvme0n1p2): mounted filesystem
Sep 25 08:00:03 neongrid9 kernel: [    2.345678] IPv6: ADDRCONF(NETDEV_UP): eth0: link is not ready""",

    "cat /etc/rsyslog.conf": """\
#  /etc/rsyslog.conf  -- rsyslog v8 default configuration

$ModLoad imuxsock  # local system logging
$ModLoad imklog    # kernel logging

$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
$FileOwner root
$FileGroup adm
$FileCreateMode 0640
$DirCreateMode 0755

#
# Include all config files in /etc/rsyslog.d/
#
$IncludeConfig /etc/rsyslog.d/*.conf

#
# Log all kernel messages to the console.
#
kern.*                          /dev/console

# Log anything (except mail) of level info or higher.
*.info;mail.none;authpriv.none;cron.none  /var/log/messages

# The authpriv file has restricted access.
authpriv.*                      /var/log/secure

# Log all the mail messages in one place.
mail.*                          -/var/log/maillog

# Log cron stuff
cron.*                          /var/log/cron

# Everybody gets emergency messages
*.emerg                         :omusrmsg:*""",

    "journalctl -p err --since today": """\
Sep 25 09:03:41 neongrid9 sshd[789]: error: PAM: Authentication failure for illegal user admin
Sep 25 09:07:55 neongrid9 kernel: error: EXT4-fs: I/O error on /dev/nvme0n1p2
Sep 25 09:12:01 neongrid9 nginx[1500]: error: connect() to unix:/run/php/php8.1-fpm.sock failed""",

    "journalctl -b": "(Logs seit aktuellem Boot-Zeitpunkt — Q zum Beenden)",
    "journalctl -b -1": "(Logs des vorherigen Boots — Q zum Beenden)",
    "journalctl --list-boots": """\
-3 abc123def456 Mon 2089-09-22 08:00:01 UTC—Mon 2089-09-22 22:15:33 UTC
-2 def456abc789 Tue 2089-09-23 08:00:03 UTC—Tue 2089-09-23 23:45:12 UTC
-1 789abcdef012 Wed 2089-09-24 08:00:01 UTC—Wed 2089-09-24 22:30:44 UTC
 0 012def789abc Thu 2089-09-25 08:00:01 UTC—Thu 2089-09-25 09:25:01 UTC""",

    "journalctl --disk-usage": "Archived and active journals take up 124.0M in the file system.",
    "journalctl --vacuum-size=500M": "(Journal auf 500MB reduziert)",
    "journalctl --vacuum-time=30d":  "(Logs älter als 30 Tage gelöscht)",

    "ls /etc/logrotate.d/": """\
alternatives  apt  btmp  dpkg  nginx  rsyslog  ufw  wtmp""",

    "cat /etc/logrotate.conf": """\
# see "man logrotate" for details
# rotate log files weekly
weekly

# use the adm group for log file permissions
su root adm

# keep 4 weeks worth of backlogs
rotate 4

# create new (empty) log files after rotating old ones
create

# use date as a suffix of the rotated file
dateext

# uncomment this if you want your log files compressed
#compress

# packages drop log rotation information into this directory
include /etc/logrotate.d

/var/log/wtmp {
    missingok
    monthly
    create 0664 root utmp
    rotate 1
}""",

    "cat /etc/logrotate.d/rsyslog": """\
/var/log/syslog
/var/log/mail.info
/var/log/mail.warn
/var/log/mail.err
/var/log/mail.log
/var/log/daemon.log
/var/log/kern.log
/var/log/auth.log
/var/log/user.log
/var/log/lpr.log
/var/log/cron.log
/var/log/debug
/var/log/messages
{
\trotate 4
\tweekly
\tmissingok
\tnotifempty
\tcompress
\tdelaycompress
\tsharedscripts
\tpostrotate
\t\t/usr/lib/rsyslog/rsyslog-rotate
\tendscript
}""",

    "logrotate -d /etc/logrotate.conf": """\
reading config file /etc/logrotate.conf
including /etc/logrotate.d/apt
including /etc/logrotate.d/nginx
including /etc/logrotate.d/rsyslog
Handling 8 logs

rotating pattern: /var/log/syslog  weekly (4 rotations)
empty log files are not rotated, old logs are removed
considering log /var/log/syslog
  log does not need rotating (log has been rotated at 2089-9-22; that is not weekly enough)""",

    "timedatectl": """\
               Local time: Thu 2089-09-25 09:25:01 UTC
           Universal time: Thu 2089-09-25 09:25:01 UTC
                 RTC time: Thu 2089-09-25 09:25:00
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no""",

    "timedatectl set-ntp true":                  "(NTP-Synchronisation aktiviert)",
    "timedatectl set-ntp false":                 "(NTP-Synchronisation deaktiviert)",
    "timedatectl set-timezone Europe/Berlin":    "(Zeitzone auf Europe/Berlin gesetzt)",
    "timedatectl list-timezones": """\
Africa/Abidjan
Africa/Accra
...
Europe/Berlin
Europe/London
...
UTC
(516 Zeitzonen verfügbar)""",

    "date": "Thu Sep 25 09:25:01 UTC 2089",
    "date '+%Y-%m-%d %H:%M:%S'": "2089-09-25 09:25:01",
    "date -u": "Thu Sep 25 09:25:01 UTC 2089",

    "hwclock": "2089-09-25 09:25:00.234521+00:00",
    "hwclock -w": "(Hardware-Uhr mit Systemzeit synchronisiert)",
    "hwclock -s": "(Systemzeit von Hardware-Uhr übernommen)",

    "crontab -l": """\
# Crontab für ghost
0 2 * * * /home/ghost/backup.sh >> /var/log/backup.log 2>&1
*/5 * * * * /usr/bin/check_disk.sh
@reboot /home/ghost/start_monitor.sh
0 9 * * 1 /home/ghost/weekly_report.sh""",

    "crontab -e": "(Crontab im Editor öffnen — speichern und schließen zum Aktivieren)",
    "crontab -r": "(Crontab gelöscht — VORSICHT: nicht rückgängig machbar!)",

    "cat /etc/crontab": """\
# /etc/crontab: system-wide crontab
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )""",

    "ls /etc/cron.d/": "e2scrub_all  php  popularity-contest  sysstat",
    "ls /etc/cron.daily/": "apt-compat  dpkg  logrotate  man-db  passwd",
    "ls /etc/cron.weekly/": "man-db  update-notifier-common",
    "ls /etc/cron.hourly/": "(leer oder nicht vorhanden)",

    "atq": """\
3\tThu Sep 25 03:00:00 2089 a ghost
5\tFri Sep 26 02:00:00 2089 a root""",

    "at -l": """\
3\tThu Sep 25 03:00:00 2089 a ghost
5\tFri Sep 26 02:00:00 2089 a root""",

    "atrm 3": "(at-Job 3 gelöscht)",
    "at -d 3": "(at-Job 3 gelöscht)",

    "systemctl list-timers": """\
NEXT                         LEFT          LAST                         PASSED       UNIT                         ACTIVATES
Thu 2089-09-25 10:00:00 UTC  34min left    Thu 2089-09-25 09:00:00 UTC  25min ago    apt-daily.timer              apt-daily.service
Thu 2089-09-25 12:00:00 UTC  2h 34min left Thu 2089-09-24 12:00:00 UTC  21h ago      apt-daily-upgrade.timer      apt-daily-upgrade.service
Fri 2089-09-26 00:00:00 UTC  14h left      Thu 2089-09-25 00:00:00 UTC  9h ago       logrotate.timer              logrotate.service
Fri 2089-09-26 00:00:00 UTC  14h left      Thu 2089-09-25 00:00:00 UTC  9h ago       man-db.timer                 man-db.service

4 timers listed.""",

    "systemctl list-timers --all": """\
NEXT                         LEFT     LAST                         PASSED  UNIT                    ACTIVATES
Thu 2089-09-25 10:00:00 UTC  34min    Thu 2089-09-25 09:00:00 UTC  25min   apt-daily.timer         apt-daily.service
n/a                          n/a      n/a                          n/a     backup.timer            backup.service
Fri 2089-09-26 00:00:00 UTC  14h      Thu 2089-09-25 00:00:00 UTC  9h      logrotate.timer         logrotate.service

3 timers listed.""",

    # ── Kapitel 12: Paketverwaltung ───────────────────────────────────────────
    "dpkg -l": """\
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                       Version                    Architecture Description
+++-==========================-==========================-============-=================================
ii  apt                        2.6.1                      amd64        commandline package manager
ii  bash                       5.2.15-2+b2                amd64        GNU Bourne Again SHell
ii  curl                       7.88.1-10+deb12u5          amd64        command line tool for transferring data
ii  nginx                      1.22.1-9                   amd64        small, powerful, scalable web/proxy server
ii  openssh-server             1:9.2p1-2+deb12u2          amd64        secure shell (SSH) server
ii  python3                    3.11.2-1+b1                amd64        interactive high-level object-oriented language
ii  vim                        2:9.0.1378-2               amd64        Vi IMproved - enhanced vi editor""",

    "dpkg -s nginx": """\
Package: nginx
Status: install ok installed
Priority: optional
Section: httpd
Installed-Size: 1500
Maintainer: Debian Nginx Maintainers <pkg-nginx-maintainers@alioth-lists.debian.net>
Architecture: amd64
Version: 1.22.1-9
Depends: nginx-common (= 1.22.1-9)
Description: small, powerful, scalable web/proxy server
 Nginx ("engine X") is a high-performance web and reverse proxy server.""",

    "dpkg -L nginx": """\
/.
/etc
/etc/nginx
/etc/nginx/nginx.conf
/etc/nginx/sites-available
/etc/nginx/sites-enabled
/usr/sbin/nginx
/usr/share/doc/nginx
/var/log/nginx""",

    "dpkg -S /usr/bin/python3": "python3-minimal: /usr/bin/python3",
    "dpkg -S /usr/sbin/sshd":   "openssh-server: /usr/sbin/sshd",
    "dpkg -S /usr/bin/curl":    "curl: /usr/bin/curl",

    "dpkg -c ./custom-tool_1.0_amd64.deb": """\
drwxr-xr-x root/root         0 2089-09-01 ./
drwxr-xr-x root/root         0 2089-09-01 ./usr/
drwxr-xr-x root/root         0 2089-09-01 ./usr/bin/
-rwxr-xr-x root/root     45123 2089-09-01 ./usr/bin/custom-tool
drwxr-xr-x root/root         0 2089-09-01 ./etc/
-rw-r--r-- root/root       512 2089-09-01 ./etc/custom-tool.conf""",

    "apt update": """\
Hit:1 http://deb.debian.org/debian bookworm InRelease
Hit:2 http://deb.debian.org/debian bookworm-updates InRelease
Hit:3 http://security.debian.org/debian-security bookworm-security InRelease
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
3 packages can be upgraded. Run 'apt list --upgradable' to see them.""",

    "apt upgrade": """\
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Calculating upgrade... Done
The following packages will be upgraded:
  curl libcurl4 openssh-client
3 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
Need to get 1,234 kB of archives.
After this operation, 4,096 B of additional disk space will be used.
Do you want to continue? [Y/n]""",

    "apt install -y curl wget git": """\
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  curl wget git
0 upgraded, 3 newly installed, 0 to remove and 0 not upgraded.
Need to get 4,321 kB of archives.
Get:1 http://deb.debian.org/debian bookworm/main amd64 curl 7.88.1-10+deb12u5
Get:2 http://deb.debian.org/debian bookworm/main amd64 wget 1.21.3-1+b2
Get:3 http://deb.debian.org/debian bookworm/main amd64 git 1:2.39.2-1.1
Selecting previously unselected package curl.
Setting up curl (7.88.1-10+deb12u5) ...""",

    "apt search python3": """\
Sorting... Done
Full Text Search... Done
python3/stable,now 3.11.2-1+b1 amd64  [installed]
  interactive high-level object-oriented language (default python3 version)

python3-pip/stable 23.0.1+dfsg-1 all
  Python package installer

python3-venv/stable 3.11.2-1+b1 amd64
  Python venv module (python3 version)""",

    "apt show nginx": """\
Package: nginx
Version: 1.22.1-9
Priority: optional
Section: httpd
Maintainer: Debian Nginx Maintainers <pkg-nginx-maintainers@alioth-lists.debian.net>
Installed-Size: 1,500 kB
Depends: nginx-common (= 1.22.1-9), libnginx-mod-http-gzip-static (= 1.22.1-9)
Homepage: https://nginx.org
Download-Size: 598 kB
APT-Sources: http://deb.debian.org/debian bookworm/main amd64 Packages
Description: small, powerful, scalable web/proxy server""",

    "apt list --installed": """\
Listing... Done
apt/stable,now 2.6.1 amd64 [installed]
bash/stable,now 5.2.15-2+b2 amd64 [installed]
curl/stable,now 7.88.1-10+deb12u5 amd64 [installed]
nginx/stable,now 1.22.1-9 amd64 [installed]
python3/stable,now 3.11.2-1+b1 amd64 [installed]""",

    "apt-cache search nginx": """\
nginx - small, powerful, scalable web/proxy server
nginx-common - small, powerful, scalable web/proxy server (common files)
nginx-full - nginx web/proxy server (standard version)
nginx-light - nginx web/proxy server (basic version)
libnginx-mod-http-lua - Nginx HTTP Lua module""",

    "apt-cache show nginx": """\
Package: nginx
Version: 1.22.1-9
Architecture: amd64
Section: httpd
Installed-Size: 1500
Depends: nginx-common (= 1.22.1-9)
Filename: pool/main/n/nginx/nginx_1.22.1-9_amd64.deb
Size: 598324
SHA256: a1b2c3d4e5f6789012345678901234abcdef1234567890abcdef1234567890ab""",

    "apt-cache depends nginx": """\
nginx
  Depends: nginx-common
  Depends: libnginx-mod-http-gzip-static
    libnginx-mod-http-gzip-static
  Recommends: nginx-common""",

    "apt-cache policy nginx": """\
nginx:
  Installed: 1.22.1-9
  Candidate: 1.22.1-9
  Version table:
 *** 1.22.1-9 500
        500 http://deb.debian.org/debian bookworm/main amd64 Packages
        100 /var/lib/dpkg/status""",

    "cat /etc/apt/sources.list": """\
# Debian Bookworm
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian bookworm main

# Security updates
deb http://security.debian.org/debian-security bookworm-security main contrib non-free
deb-src http://security.debian.org/debian-security bookworm-security main

# Bookworm updates
deb http://deb.debian.org/debian bookworm-updates main contrib non-free""",

    "ls /etc/apt/sources.list.d/": "nginx.list  nodesource.list",

    "rpm -qa": """\
bash-5.1.8-6.el9.x86_64
coreutils-8.32-34.el9.x86_64
openssh-8.7p1-38.el9.x86_64
openssh-server-8.7p1-38.el9.x86_64
python3-3.9.18-3.el9.x86_64
nginx-1.20.1-14.el9.x86_64
systemd-252-18.el9.x86_64""",

    "rpm -qi openssh": """\
Name        : openssh
Version     : 8.7p1
Release     : 38.el9
Architecture: x86_64
Install Date: Mon Sep 25 08:00:00 2089
Group       : Applications/Internet
Size        : 1819428
License     : BSD
Signature   : RSA/SHA256, Mon Sep 25 07:00:00 2089, Key ID 199e2f91fd431d51
Source RPM  : openssh-8.7p1-38.el9.src.rpm
Summary     : An open source implementation of SSH protocol version 2
Description :
SSH (Secure SHell) is a program for logging into and executing commands on a
remote machine. SSH is intended to replace rlogin and rsh.""",

    "rpm -ql openssh": """\
/etc/ssh
/etc/ssh/moduli
/usr/bin/ssh-keygen
/usr/bin/ssh-keyscan
/usr/lib/systemd/system/sshd-keygen.target
/usr/share/man/man1/ssh-keygen.1.gz""",

    "rpm -qf /usr/bin/python3": "python3-3.9.18-3.el9.x86_64",
    "rpm -qf /usr/sbin/sshd":   "openssh-server-8.7p1-38.el9.x86_64",

    "rpm -ivh ./nginx-1.20.1-9.el8.x86_64.rpm": """\
Verifying...                          ################################# [100%]
Preparing...                          ################################# [100%]
Updating / installing...
   1:nginx-1:1.20.1-9.el8             ################################# [100%]""",

    "yum search httpd": """\
Last metadata expiration check: 0:05:23 ago on Thu Sep 25 09:00:00 2089.
========================= Name & Summary Matched: httpd ==========================
httpd.x86_64 : Apache HTTP Server
httpd-devel.x86_64 : Development interfaces for the Apache HTTP server
httpd-manual.noarch : Documentation for the Apache HTTP server
httpd-tools.x86_64 : Tools for use with the Apache HTTP Server""",

    "yum info httpd": """\
Last metadata expiration check: 0:05:23 ago.
Available Packages
Name         : httpd
Version      : 2.4.57
Release      : 5.el9
Architecture : x86_64
Size         : 1.5 M
Source       : httpd-2.4.57-5.el9.src.rpm
Repository   : appstream
Summary      : Apache HTTP Server
License      : ASL 2.0
Description  : The Apache HTTP Server is a powerful web server.""",

    "yum list installed": """\
Installed Packages
bash.x86_64             5.1.8-6.el9            @anaconda
coreutils.x86_64        8.32-34.el9            @anaconda
nginx.x86_64            1.20.1-14.el9          @appstream
openssh-server.x86_64   8.7p1-38.el9           @anaconda
python3.x86_64          3.9.18-3.el9           @anaconda""",

    "yum provides /usr/sbin/httpd": """\
Last metadata expiration check: 0:05:23 ago.
httpd-2.4.57-5.el9.x86_64 : Apache HTTP Server
Repo        : appstream
Matched from:
Filename    : /usr/sbin/httpd""",

    "dnf repolist": """\
repo id                   repo name
appstream                 AlmaLinux 9 - AppStream
baseos                    AlmaLinux 9 - BaseOS
extras                    AlmaLinux 9 - Extras""",

    "zypper repos": """\
# | Alias              | Name                    | Enabled | GPG Check | Refresh
--+--------------------+-------------------------+---------+-----------+--------
1 | openSUSE-Leap-15.5 | Main Repository         | Yes     | ( r ) Yes | Yes
2 | openSUSE-security  | Security Updates        | Yes     | ( r ) Yes | Yes
3 | packman            | Packman                 | Yes     | ( r ) Yes | No""",

    "zypper search nginx": """\
Loading repository data...
Reading installed packages...

S  | Name              | Summary                      | Type
---+-------------------+------------------------------+--------
i+ | nginx             | A HTTP server and mail proxy | package
   | nginx-mainline    | Mainline version of nginx    | package""",

    "ldd /usr/bin/python3": """\
        linux-vdso.so.1 (0x00007ffd12345000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f1234567000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1234200000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f1234100000)
        libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007f1234080000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f1234060000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f1234600000)""",

    "ldd /usr/bin/ssh": """\
        linux-vdso.so.1 (0x00007ffd98765000)
        libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x00007f9876543000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f9876520000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f9876200000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f9876600000)""",

    "ldconfig -p": """\
2089 libs found in cache `/etc/ld.so.cache'
        libz.so.1 (libc6,x86-64) => /lib/x86_64-linux-gnu/libz.so.1
        libssl.so.3 (libc6,x86-64) => /lib/x86_64-linux-gnu/libssl.so.3
        libcrypto.so.3 (libc6,x86-64) => /lib/x86_64-linux-gnu/libcrypto.so.3
        libc.so.6 (libc6,x86-64) => /lib/x86_64-linux-gnu/libc.so.6
        libpthread.so.0 (libc6,x86-64) => /lib/x86_64-linux-gnu/libpthread.so.0""",

    "ldconfig":    "(Shared-Library-Cache aktualisiert)",
    "cat /etc/ld.so.conf": """\
include /etc/ld.so.conf.d/*.conf""",

    "apt purge backdoor-agent":  "(backdoor-agent + alle Konfigurationsdateien entfernt)",
    "apt purge nginx":           "(nginx + alle Konfigurationsdateien entfernt)",
    "apt autoremove":            "(Nicht mehr benötigte Pakete entfernt)",
    "apt-key list": """\
/etc/apt/trusted.gpg.d/debian-archive-bookworm-automatic.gpg
--------------------------------------------------------------
pub   rsa4096 2023-01-01 [SC] [expires: 2031-01-01]
      1F89 983E 0081 FDE0 18F3  CC96 73A4 F27B 8DD4 7936
uid           [ unknown] Debian Archive Automatic Signing Key (12/bookworm)""",

    # ── Kapitel 13: Kernel, Module, sysctl, udev ──────────────────────────────
    "lsmod": """\
Module                  Size  Used by
e1000                 163840  0
snd_hda_intel          53248  2
snd_hda_codec_hdmi     65536  1 snd_hda_intel
snd_hda_codec          143360  2 snd_hda_codec_hdmi,snd_hda_intel
snd_hda_core           94208  3 snd_hda_codec_hdmi,snd_hda_codec,snd_hda_intel
i915                 2285568  3
drm_kms_helper        196608  1 i915
drm                   557056  4 drm_kms_helper,i915
dm_crypt               45056  0
dm_mod                155648  2 dm_crypt""",

    "modinfo e1000": """\
filename:       /lib/modules/6.1.0-neongrid9/kernel/drivers/net/ethernet/intel/e1000/e1000.ko
version:        7.3.21-k8-NAPI
license:        GPL v2
description:    Intel(R) PRO/1000 Network Driver
author:         Intel Corporation, <linux.nics@intel.com>
srcversion:     5D19B56A5C5C4BA8F31F0AD
alias:          pci:v00008086d00001076sv*sd*bc*sc*i*
depends:
retpoline:      Y
intree:         Y
name:           e1000
vermagic:       6.1.0-neongrid9 SMP preempt mod_unload modversions""",

    "modinfo -F description e1000": "Intel(R) PRO/1000 Network Driver",

    "modprobe e1000":    "(Modul e1000 + Abhängigkeiten geladen)",
    "modprobe -r e1000": "(Modul e1000 + Abhängigkeiten entladen)",
    "modprobe -v e1000": """\
insmod /lib/modules/6.1.0-neongrid9/kernel/drivers/net/ethernet/intel/e1000/e1000.ko""",

    "rmmod e1000":    "(Modul e1000 entladen)",
    "rmmod -f e1000": "(Modul e1000 force-entladen — VORSICHT!)",

    "cat /etc/modules": """\
# /etc/modules: kernel modules to load at boot time.
# Each line contains the name of a module.
e1000
dm_crypt
# i2c support
i2c_dev""",

    "ls /etc/modprobe.d/": "blacklist.conf  blacklist-framebuffer.conf  nvidia.conf",

    "cat /etc/modprobe.d/blacklist.conf": """\
# /etc/modprobe.d/blacklist.conf
# Automatically generated by the system
blacklist nouveau
blacklist pcspkr
blacklist snd_pcsp
# Uncomment to blacklist Intel AMT:
#blacklist mei_me""",

    "cat /proc/version": "Linux version 6.1.0-neongrid9 (ghost@neongrid9) (gcc version 12.2.0) #1 SMP PREEMPT Thu Sep 25 08:00:00 UTC 2089",

    "uname -r": "6.1.0-neongrid9",
    "uname -a": "Linux neongrid9 6.1.0-neongrid9 #1 SMP PREEMPT Thu Sep 25 08:00:00 UTC 2089 x86_64 GNU/Linux",
    "uname -m": "x86_64",
    "uname -s": "Linux",
    "uname -n": "neongrid9",

    "cat /proc/cmdline": "BOOT_IMAGE=/boot/vmlinuz-6.1.0-neongrid9 root=/dev/nvme0n1p2 ro quiet splash",
    "cat /proc/modules": """\
e1000 163840 0 - Live 0xffffffffc08a0000
snd_hda_intel 53248 2 - Live 0xffffffffc0880000
i915 2285568 3 - Live 0xffffffffc0400000
dm_crypt 45056 0 - Live 0xffffffffc03f0000
dm_mod 155648 2 dm_crypt - Live 0xffffffffc03b0000""",

    "cat /proc/uptime": "5125.23 40121.45",

    "cat /proc/filesystems": """\
nodev   sysfs
nodev   tmpfs
nodev   bdev
nodev   proc
nodev   cgroup
nodev   devtmpfs
nodev   devpts
        ext3
        ext4
        xfs
        vfat
nodev   nfs""",

    "sysctl net.ipv4.ip_forward": "net.ipv4.ip_forward = 0",
    "sysctl -w net.ipv4.ip_forward=1": "net.ipv4.ip_forward = 1",
    "sysctl -w net.ipv4.ip_forward=0": "net.ipv4.ip_forward = 0",
    "sysctl vm.swappiness": "vm.swappiness = 60",
    "sysctl -w vm.swappiness=10": "vm.swappiness = 10",

    "sysctl -a": """\
kernel.hostname = neongrid9
kernel.ostype = Linux
kernel.osrelease = 6.1.0-neongrid9
net.ipv4.ip_forward = 0
net.ipv4.icmp_echo_ignore_all = 0
vm.swappiness = 60
vm.dirty_ratio = 20
fs.file-max = 9223372036854775807
(... weitere Parameter ...)""",

    "sysctl -p": """\
net.ipv4.ip_forward = 1
vm.swappiness = 10
net.core.rmem_max = 134217728""",

    "cat /etc/sysctl.conf": """\
# /etc/sysctl.conf - Configuration for sysctl
#
# See /etc/sysctl.d/ for additional system variables.

# Uncomment the next line to enable packet forwarding for IPv4
#net.ipv4.ip_forward=1

# Uncomment the next line to enable packet forwarding for IPv6
#net.ipv6.conf.all.forwarding=1

# Do not accept ICMP redirects (prevent MITM attacks)
#net.ipv4.conf.all.accept_redirects = 0

# Decrease the time default value for tcp_fin_timeout connection
#net.ipv4.tcp_fin_timeout = 30""",

    "cat /proc/sys/net/ipv4/ip_forward": "0",
    "echo 1 > /proc/sys/net/ipv4/ip_forward": "(IP-Forwarding aktiviert)",

    "udevadm info /dev/sda": """\
P: /devices/pci0000:00/0000:00:1f.2/host0/target0:0:0/0:0:0:0/block/sda
N: sda
L: 0
S: disk/by-id/ata-Samsung_SSD_860_EVO_500GB_S3ETNX0K123456
S: disk/by-path/pci-0000:00:1f.2-ata-1
E: DEVNAME=/dev/sda
E: DEVTYPE=disk
E: SUBSYSTEM=block
E: MAJOR=8
E: MINOR=0
E: ID_VENDOR=ATA
E: ID_MODEL=Samsung_SSD_860_EVO
E: ID_FS_TYPE=""",

    "udevadm monitor": "(Echtzeit udev-Ereignisse — Strg+C zum Beenden)",
    "udevadm control --reload-rules": "(udev-Regeln neu geladen)",
    "udevadm trigger": "(udev-Regeln auf vorhandene Geräte angewendet)",

    "ls /etc/udev/rules.d/": "70-persistent-net.rules  80-net-setup-link.rules  99-custom.rules",

    "ls -l /dev/sda": "brw-rw---- 1 root disk 8, 0 Sep 25 08:00 /dev/sda",
    "ls -l /dev/": """\
total 0
crw-r--r-- 1 root root  10, 235 Sep 25 08:00 autofs
drwxr-xr-x 2 root root       60 Sep 25 08:00 block
drwxr-xr-x 2 root root       80 Sep 25 08:00 bus
crw------- 1 root root   5,   1 Sep 25 08:00 console
lrwxrwxrwx 1 root root       11 Sep 25 08:00 core -> /proc/kcore
crw-rw-rw- 1 root root   1,   7 Sep 25 08:00 full
crw-rw-rw- 1 root root  10, 229 Sep 25 08:00 fuse
crw-rw-rw- 1 root root   1,   3 Sep 25 08:00 null
brw-rw---- 1 root disk   8,   0 Sep 25 08:00 sda
brw-rw---- 1 root disk   8,   1 Sep 25 08:00 sda1
brw-rw---- 1 root disk   8,   2 Sep 25 08:00 sda2
crw-rw-rw- 1 root tty    5,   0 Sep 25 08:00 tty
crw-rw-rw- 1 root root   1,   9 Sep 25 08:00 urandom
crw-rw-rw- 1 root root   1,   5 Sep 25 08:00 zero""",

    "dmesg -T": """\
[Thu Sep 25 08:00:00 2089] Linux version 6.1.0-neongrid9 (gcc 12.2.0)
[Thu Sep 25 08:00:00 2089] BIOS-provided physical RAM map
[Thu Sep 25 08:00:01 2089] ACPI: IRQ0 used by override.
[Thu Sep 25 08:00:01 2089] PCI: Using configuration type 1 for base access
[Thu Sep 25 08:00:02 2089] e1000: Intel(R) PRO/1000 Network Driver
[Thu Sep 25 08:00:02 2089] e1000: Copyright (c) 1999-2006 Intel Corporation.
[Thu Sep 25 08:00:02 2089] EXT4-fs (nvme0n1p2): mounted filesystem with ordered data mode
[Thu Sep 25 08:00:03 2089] systemd[1]: systemd 252 running in system mode""",

    "dmesg -l err": """\
[Thu Sep 25 09:07:55 2089] kernel: error: EXT4-fs: I/O error on journal device
[Thu Sep 25 09:12:01 2089] kernel: error: iwlwifi: Failed to start RT ucode""",

    "dmesg | grep -i usb": """\
[    2.456789] usbcore: registered new interface driver usbfs
[    2.567890] usbcore: registered new interface driver hub
[    3.678901] usb 1-1: new high-speed USB device number 2 using xhci_hcd
[    3.789012] usb 1-1: New USB device found, idVendor=04f2, idProduct=b604""",

    "ls /boot/": """\
config-6.1.0-neongrid9
grub
initrd.img-6.1.0-neongrid9
System.map-6.1.0-neongrid9
vmlinuz-6.1.0-neongrid9""",

    "ls -la /boot/": """\
total 89456
drwxr-xr-x  4 root root     4096 Sep 25 08:00 .
drwxr-xr-x 20 root root     4096 Sep 25 08:00 ..
-rw-r--r--  1 root root   236545 Sep  1 00:00 config-6.1.0-neongrid9
drwxr-xr-x  6 root root     4096 Sep 25 08:00 grub
-rw-r--r--  1 root root 38912347 Sep  1 00:00 initrd.img-6.1.0-neongrid9
-rw-r--r--  1 root root  5234567 Sep  1 00:00 System.map-6.1.0-neongrid9
-rwxr-xr-x  1 root root 11543488 Sep  1 00:00 vmlinuz-6.1.0-neongrid9""",

    "ls /boot/vmlinuz*": "/boot/vmlinuz-6.1.0-neongrid9",

    "update-initramfs -u": """\
update-initramfs: Generating /boot/initrd.img-6.1.0-neongrid9
W: Possible missing firmware /lib/firmware/i915/tgl_dmc_ver2_12.bin for module i915""",

    "depmod -a": "(Modul-Abhängigkeitsdatenbank aktualisiert)",

    # ── Fehlende Befehle: 104.2 / 104.3 / 108.3 ───────────────────────────────

    # 104.2 Dateisystem-Integrität
    "fsck /dev/sdb1": """\
fsck from util-linux 2.36.1
e2fsck 1.46.5 (30-Dec-2021)
/dev/sdb1: clean, 42/131072 files, 28451/524288 blocks""",

    "fsck -f /dev/sdb1": """\
fsck from util-linux 2.36.1
e2fsck 1.46.5 (30-Dec-2021)
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
/dev/sdb1: 42/131072 files (0.0% non-contiguous), 28451/524288 blocks""",

    "tune2fs -l /dev/sda1": """\
tune2fs 1.46.5 (30-Dec-2021)
Filesystem volume name:   <none>
Last mounted on:          /boot
Filesystem UUID:          a1b2c3d4-e5f6-7890-abcd-ef1234567890
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery extent 64bit flex_bg sparse_super large_file huge_file dir_nlink extra_isize metadata_csum
Filesystem flags:         signed_directory_hash
Default mount options:    user_xattr acl
Filesystem state:         clean
Errors behavior:          Continue
Filesystem OS type:       Linux
Inode count:              131072
Block count:              524288
Reserved block count:     26214
Free blocks:              495837
Free inodes:              131030
First block:              0
Block size:               4096
Fragment size:            4096
Group descriptor size:    64
Reserved GDT blocks:      255
Blocks per group:         32768
Fragments per group:      32768
Inodes per group:         8192
Inode blocks per group:   512
Flex block group size:    16
Filesystem created:       Mon Jan 15 09:00:00 2024
Last mount time:          Mon Jan 15 09:23:11 2024
Last write time:          Mon Jan 15 09:23:11 2024
Mount count:              3
Maximum mount count:      -1
Last checked:             Mon Jan 15 09:00:00 2024
Check interval:           0 (<none>)
Lifetime writes:          94 MB
Reserved blocks uid:      0 (user root)
Reserved blocks gid:      0 (group root)
First inode:              11
Inode size:               256
Required extra isize:     32
Desired extra isize:      32
Journal inode:            8
First orphan inode:       0
Journal backup:           inode blocks""",

    "tune2fs -l /dev/sdb1": "(tune2fs: Gerät /dev/sdb1 nicht gemountet — tune2fs -l für Details)",
    "tune2fs -c 30 /dev/sda1": "(Max. Mount-Anzahl auf 30 gesetzt)",
    "tune2fs -L 'DataDisk' /dev/sdb1": "(Label 'DataDisk' auf /dev/sdb1 gesetzt)",

    "mount -a": "(Alle Einträge aus /etc/fstab gemountet)",
    "mount -o remount,rw /": "(/ neu gemountet mit rw-Optionen)",
    "mount -t tmpfs tmpfs /mnt/ramdisk": "(tmpfs auf /mnt/ramdisk gemountet)",
    "umount -l /mnt": "(Lazy unmount: /mnt wird freigegeben sobald nicht mehr genutzt)",

    "autofs --version": "Linux automount version 5.1.8",
    "systemctl status autofs": """\
● autofs.service - Automounts filesystems on demand
     Loaded: loaded (/lib/systemd/system/autofs.service; enabled)
     Active: active (running) since Mon 2024-01-15 09:00:00 UTC; 2h ago
   Main PID: 456 (automount)
      Tasks: 5 (limit: 4915)
     Memory: 1.8M""",
    "cat /etc/auto.master": """\
/misc   /etc/auto.misc
/net    -hosts
+dir:/etc/auto.master.d
+auto.master""",
    "cat /etc/auto.misc": """\
#
# This is an automounter map and it has the following format
# key [ -mount-options-separated-by-comma ] location
# Details may be found in the autofs(5) manpage

cd      -fstype=iso9660,ro,nosuid,nodev :/dev/cdrom
# the following entries are samples to pique your imagination
#linux          -ro,soft,intr           ftp.example.org:/pub/linux""",

    # 108.3 MTA — Mail Transfer Agent
    "mailq": """\
-Queue ID-  --Size-- ----Arrival Time---- -Sender/Recipient-------
Mail queue is empty""",

    "mailq -q": "(Postfix Mail-Queue-Flush gestartet)",

    "sendmail -V": "Postfix sendmail-compatibles tool 3.7.3",
    "sendmail -bp": "(Mail queue ist leer)",
    "sendmail -q": "(Mail-Queue wird verarbeitet)",

    "newaliases": "(aliases Database aktualisiert: /etc/aliases)",

    "cat /etc/aliases": """\
# See man 5 aliases for format
# Postmaster must be defined
postmaster:    root

# General redirections for pseudo accounts
nobody:        root
daemon:        root
bin:           root
mail:          root
ftp:           root

# Person who should get root's mail
#root:          marc""",

    "postfix status": """\
postfix/postfix-script: the Postfix mail system is running: PID: 789""",

    "postfix reload": "(Postfix Konfiguration neu geladen)",
    "postfix check": "(Postfix Konfiguration OK — keine Fehler)",
    "postfix start": "(Postfix Mail-System gestartet)",
    "postfix stop": "(Postfix Mail-System gestoppt)",

    "postconf -n": """\
alias_database = hash:/etc/aliases
alias_maps = hash:/etc/aliases
append_dot_mydomain = no
biff = no
compatibility_level = 3.6
inet_interfaces = loopback-only
inet_protocols = all
mailbox_size_limit = 0
mydestination = $myhostname, neongrid-9, localhost.localdomain, , localhost
myhostname = neongrid-9
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
myorigin = /etc/mailname
readme_directory = no
recipient_delimiter = +
relayhost =
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
smtp_tls_security_level = may
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated defer_unauth_destination
smtpd_tls_cert_file = /etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file = /etc/ssl/private/ssl-cert-snakeoil.key
smtpd_tls_security_level = may
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache""",

    "cat /etc/postfix/main.cf": """\
# See /usr/share/postfix/main.cf.dist for a commented version

smtpd_banner = $myhostname ESMTP $mail_name (Debian/GNU Linux)
biff = no
append_dot_mydomain = no
readme_directory = no
compatibility_level = 3.6

# TLS parameters
smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
smtpd_tls_security_level=may
smtp_tls_CAfile=/etc/ssl/certs/ca-certificates.crt
smtp_tls_security_level=may

myhostname = neongrid-9
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
myorigin = /etc/mailname
mydestination = $myhostname, neongrid-9, localhost.localdomain, , localhost
relayhost =
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = loopback-only
inet_protocols = all""",

    "cat ~/.forward": "ghost@external.net",
    "echo 'ghost@external.net' > ~/.forward": "(Mail für ghost wird an ghost@external.net weitergeleitet)",
    "cat /var/mail/ghost": """\
From root@neongrid-9 Mon Jan 15 09:00:00 2024
Return-Path: <root@neongrid-9>
X-Original-To: ghost
Delivered-To: ghost@neongrid-9
Received: by neongrid-9 (Postfix, from userid 0)
        id A1B2C3D4; Mon, 15 Jan 2024 09:00:00 +0000 (UTC)
To: ghost@neongrid-9
Subject: System Alert
Message-Id: <20240115090000.A1B2C3D4@neongrid-9>
Date: Mon, 15 Jan 2024 09:00:00 +0000 (UTC)
From: root@neongrid-9 (root)

NeonGrid-9 system message: disk usage 85% on /dev/sda1""",

    # ── Kapitel 14: Bash-Scripting ─────────────────────────────────────────────
    "chmod +x script.sh": "(Datei script.sh ist jetzt ausführbar)",
    "chmod +x deploy.sh": "(Datei deploy.sh ist jetzt ausführbar)",
    "chmod +x backup.sh": "(Datei backup.sh ist jetzt ausführbar)",
    "bash -n script.sh": "(Syntax-Check: keine Fehler gefunden)",
    "bash -n deploy.sh": "(Syntax-Check: keine Fehler gefunden)",
    "bash -x script.sh": """\
+ source /etc/os-release
+ echo Ubuntu
Ubuntu
+ DATE=2024-01-15
+ echo 'Backup gestartet: 2024-01-15'
Backup gestartet: 2024-01-15
+ tar -czf /backup/home-2024-01-15.tar.gz /home/ghost
+ echo 'Backup abgeschlossen'
Backup abgeschlossen""",
    "bash -x deploy.sh": """\
+ set -euo pipefail
+ APP_NAME=neongrid
+ VERSION=1.0.42
+ echo 'Deploying neongrid v1.0.42'
Deploying neongrid v1.0.42
+ systemctl stop neongrid
+ cp /tmp/neongrid-1.0.42 /usr/local/bin/neongrid
+ systemctl start neongrid
+ echo 'Deploy erfolgreich'
Deploy erfolgreich""",
    "echo $?": "0",
    "echo $0": "/bin/bash",
    "echo $#": "3",
    "echo $@": "arg1 arg2 arg3",
    "echo $$": "31337",
    "echo ${VAR:-default}": "default",
    "echo ${#PATH}": "47",
    "test -f /etc/passwd": "(Exit-Code 0 — Datei existiert)",
    "test -d /etc/": "(Exit-Code 0 — Verzeichnis existiert)",
    "test -z \"\"": "(Exit-Code 0 — String ist leer)",
    "test -n \"hello\"": "(Exit-Code 0 — String ist nicht leer)",
    "[ -f /etc/passwd ]": "(Exit-Code 0 — Bedingung wahr)",
    "[ -d /tmp ]": "(Exit-Code 0 — Bedingung wahr)",
    "[[ -f /etc/passwd && -r /etc/passwd ]]": "(Exit-Code 0 — beide Bedingungen wahr)",
    "for i in 1 2 3; do echo $i; done": """\
1
2
3""",
    "for f in /etc/*.conf; do echo $f; done": """\
/etc/adduser.conf
/etc/ca-certificates.conf
/etc/debconf.conf
/etc/deluser.conf
/etc/gai.conf
/etc/hdparm.conf
/etc/host.conf
/etc/kernel-img.conf
/etc/ldap.conf
/etc/logrotate.conf
/etc/nsswitch.conf
/etc/pam.conf
/etc/resolv.conf
/etc/rsyslog.conf
/etc/sysctl.conf""",
    "while read -r line; do echo \"$line\"; done < /etc/hostname": "neongrid-9",
    "until false; do echo loop; break; done": "loop",
    "break": "(Schleife verlassen)",
    "continue": "(Nächste Iteration)",
    "declare -a arr=(a b c)": "(Array 'arr' deklariert mit 3 Elementen)",
    "echo ${arr[0]}": "a",
    "echo ${arr[@]}": "a b c",
    "echo ${#arr[@]}": "3",
    "echo $(( 2 + 3 ))": "5",
    "echo $(( 10 % 3 ))": "1",
    "echo $(( 2 ** 8 ))": "256",
    "let x=5+3": "(x=8)",
    "expr 10 + 5": "15",
    "expr length \"hello\"": "5",
    "echo '5.5 * 2' | bc": "11.0",
    "echo 'scale=2; 22/7' | bc": "3.14",
    "echo ${PATH#*/}": "usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "echo ${PATH##*/}": "bin",
    "echo ${PATH%:*}": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin",
    "echo ${VAR/old/new}": "(Ersetzt erstes 'old' durch 'new')",
    "getopts 'hvf:' OPT": "(Option geparst — $OPT enthält Buchstaben, $OPTARG den Wert)",
    "read -p 'Name: ' NAME": "Name: (wartet auf Eingabe)",
    "read -s -p 'Passwort: ' PASS": "Passwort: (Eingabe versteckt)",
    "read -t 5 -p 'Eingabe: ' ANS": "Eingabe: (5 Sekunden Timeout)",
    "read -n 1 -p 'Weiter? [j/n]: ' CHOICE": "Weiter? [j/n]: (liest 1 Zeichen)",
    "type bash": "bash is /bin/bash",
    "which bash": "/bin/bash",
    "bash --version": """\
GNU bash, version 5.2.15(1)-release (x86_64-pc-linux-gnu)
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>""",
    "set -e": "(Shell beendet sich bei erstem Fehler — exit on error aktiv)",
    "set -u": "(Undefinierte Variablen verursachen Fehler — unset var = error)",
    "set -euo pipefail": "(Kombination: exit on error + unset = error + pipe-Fehler)",
    "set -x": "(Debug-Modus: Befehle werden vor Ausführung ausgegeben)",
    "set +x": "(Debug-Modus deaktiviert)",
    "exit 0": "(Skript beendet mit Exit-Code 0 — Erfolg)",
    "exit 1": "(Skript beendet mit Exit-Code 1 — Fehler)",
    "source script.sh": "(Skript in aktuelle Shell-Umgebung eingebunden)",
    ". script.sh": "(Skript in aktuelle Shell-Umgebung eingebunden — . ist Alias für source)",
    "declare -f myfunc": """\
myfunc ()
{
    local NAME=$1
    echo "Hallo, $NAME"
    return 0
}""",
    "local VAR=wert": "(lokale Variable in Funktion deklariert — nur in Funktion sichtbar)",
    "return 0": "(Funktion gibt Exit-Code 0 zurück)",
    # ── Kapitel 17: Shell-Umgebung ────────────────────────────────────────────
    "cat ~/.bashrc": """\
# ~/.bashrc: executed by bash(1) for non-login shells.

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# History
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000
shopt -s histappend

# Prompt
PS1='\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ '

# Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'
alias update='sudo apt update && sudo apt upgrade'

# Functions
mkcd() { mkdir -p "$1" && cd "$1"; }""",

    "cat ~/.profile": """\
# ~/.profile: executed by the command interpreter for login shells.

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

# Editor
export EDITOR=vim
export VISUAL=vim""",

    "cat ~/.bash_profile": """\
# .bash_profile — Login-Shell
# Lädt .profile und .bashrc
[[ -f ~/.profile ]] && source ~/.profile
[[ -f ~/.bashrc ]] && source ~/.bashrc""",

    "cat /etc/profile": """\
# /etc/profile: system-wide .profile file for the Bourne shell (sh(1))
# and Bourne compatible shells (bash(1), ksh(1), ash(1), ...).

if [ "${PS1-}" ]; then
  if [ "${BASH-}" ] && [ "$BASH" != "/bin/sh" ]; then
    if [ -f /etc/bash.bashrc ]; then
      . /etc/bash.bashrc
    fi
  fi
fi

if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
  unset i
fi""",

    "ls /etc/profile.d/": """\
01-locale-fix.sh  apps-bin-path.sh  bash_completion.sh
color_prompt.sh   dir_colors.sh     gawk.sh
im-config_wayland.sh  java_env.sh   vte-2.91.sh""",

    "env": """\
SHELL=/bin/bash
HOME=/home/ghost
USER=ghost
LOGNAME=ghost
PATH=/home/ghost/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=de_DE.UTF-8
TERM=xterm-256color
DISPLAY=:0
EDITOR=vim
VISUAL=vim
HISTSIZE=1000
HISTFILESIZE=2000
XDG_SESSION_TYPE=x11
XDG_SESSION_ID=1
XDG_RUNTIME_DIR=/run/user/1000
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01
LESSCLOSE=/usr/bin/lesspipe %s %s
LESSOPEN=| /usr/bin/lesspipe %s
_=/usr/bin/env""",

    "printenv": """\
SHELL=/bin/bash
HOME=/home/ghost
USER=ghost
PATH=/home/ghost/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=de_DE.UTF-8
TERM=xterm-256color
EDITOR=vim""",

    "printenv PATH": "/home/ghost/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",

    "printenv EDITOR": "vim",
    "printenv HOME": "/home/ghost",
    "printenv USER": "ghost",
    "printenv SHELL": "/bin/bash",
    "printenv TERM": "xterm-256color",

    "set": """\
BASH=/bin/bash
BASH_ARGC=()
BASH_ARGV=()
BASH_LINENO=()
COLUMNS=220
COMP_WORDBREAKS=$' \\t\\n"\\'\\><=;|&(:'
DIRSTACK=()
EDITOR=vim
GROUPS=()
HISTCONTROL=ignoreboth
HISTFILE=/home/ghost/.bash_history
HISTFILESIZE=2000
HISTSIZE=1000
HOME=/home/ghost
HOSTNAME=neongrid-9
IFS=$' \\t\\n'
LANG=de_DE.UTF-8
LINES=50
LOGNAME=ghost
MACHTYPE=x86_64-pc-linux-gnu
OLDPWD=/home/ghost
OPTERR=1
OPTIND=1
OSTYPE=linux-gnu
PATH=/home/ghost/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PIPESTATUS=([0]="0")
PPID=1234
PS1='\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ '
PS2='> '
PS4='+ '
PWD=/home/ghost
SHELL=/bin/bash
TERM=xterm-256color
UID=1000
USER=ghost
_=set
mkcd ()
{
    mkdir -p "$1" && cd "$1"
}""",

    "declare -x": """\
declare -x DISPLAY=":0"
declare -x EDITOR="vim"
declare -x HOME="/home/ghost"
declare -x LANG="de_DE.UTF-8"
declare -x LOGNAME="ghost"
declare -x PATH="/home/ghost/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
declare -x SHELL="/bin/bash"
declare -x TERM="xterm-256color"
declare -x USER="ghost"
declare -x VISUAL="vim"
declare -x XDG_SESSION_TYPE="x11" """,

    "export PATH=$PATH:~/bin": "(~/bin wurde zu PATH hinzugefügt)",
    'export PATH="$HOME/bin:$PATH"': "($HOME/bin wurde am Anfang von PATH eingefügt)",

    "which python3": "/usr/bin/python3",
    "which bash": "/bin/bash",
    "which ls": "/bin/ls",

    "type ls": "ls is aliased to `ls --color=auto'",
    "type cd": "cd is a shell builtin",
    "type python3": "python3 is /usr/bin/python3",
    "type mkcd": """\
mkcd is a function
mkcd ()
{
    mkdir -p "$1" && cd "$1"
}""",
    "type -a ls": """\
ls is aliased to `ls --color=auto'
ls is /bin/ls
ls is /usr/bin/ls""",

    "command -v ls": "/bin/ls",
    "command -v cd": "cd",

    "hash -r": "(Command-Hash-Tabelle geleert)",
    "hash": """\
hits\tcommand
   5\t/usr/bin/python3
   3\t/usr/bin/vim
  12\t/bin/ls
   1\t/usr/bin/git""",

    "unset EDITOR": "(EDITOR-Variable gelöscht)",
    "readonly PI=3.14159": "(PI als read-only Variable gesetzt)",
    "declare -r": """\
declare -r BASHOPTS="checkwinsize:cmdhist:complete_fullquote:extquote:force_fignore:globasciiranges:hostcomplete:interactive_comments:progcomp:promptvars:sourcepath"
declare -r BASH_VERSINFO=([0]="5" [1]="2" [2]="15" [3]="1" [4]="release" [5]="x86_64-pc-linux-gnu")
declare -ir EUID="1000"
declare -ir PPID="1234"
declare -ir UID="1000" """,

    "alias": """\
alias grep='grep --color=auto'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
alias update='sudo apt update && sudo apt upgrade'""",

    "unalias ll": "(Alias 'll' gelöscht)",
    "unalias -a": "(Alle Aliases gelöscht)",

    "declare -f": """\
mkcd ()
{
    mkdir -p "$1" && cd "$1"
}
backup ()
{
    cp "$1" "$1.bak.$(date +%Y%m%d)"
}""",

    "declare -f mkcd": """\
mkcd ()
{
    mkdir -p "$1" && cd "$1"
}""",

    "history": """\
  491  ls -la
  492  cd ~/neongrid9
  493  python3 main.py
  494  git status
  495  git add .
  496  git commit -m 'Add ch17'
  497  cat ~/.bashrc
  498  echo $PATH
  499  alias
  500  history""",

    "history 20": """\
  481  ssh ghost@10.0.0.5
  482  scp report.pdf ghost@10.0.0.5:~/
  483  ls -la /etc/
  484  cat /etc/passwd | grep ghost
  485  sudo systemctl restart nginx
  486  tail -f /var/log/nginx/error.log
  487  grep 'ERROR' /var/log/nginx/error.log
  488  vim /etc/nginx/nginx.conf
  489  sudo nginx -t
  490  sudo systemctl reload nginx
  491  ls -la
  492  cd ~/neongrid9
  493  python3 main.py
  494  git status
  495  git add .
  496  git commit -m 'Add ch17'
  497  cat ~/.bashrc
  498  echo $PATH
  499  alias
  500  history 20""",

    "history -c": "(History aus Memory gelöscht)",

    "echo $PS1": "\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ ",
    "echo $PS2": "> ",
    "echo $PS4": "+ ",

    "echo $HISTSIZE": "1000",
    "echo $HISTFILESIZE": "2000",
    "echo $HISTCONTROL": "ignoreboth",
    "echo $HISTFILE": "/home/ghost/.bash_history",

    "echo $TERM": "xterm-256color",
    "tput colors": "256",
    "tput clear": "(Terminal wird geleert)",

    "echo $EDITOR": "vim",
    "echo $VISUAL": "vim",
    "echo $HOME": "/home/ghost",
    "echo $USER": "ghost",
    "echo $SHELL": "/bin/bash",
    "echo $HOSTNAME": "neongrid-9",

    # ── Kapitel 16: Locale, X11, CUPS ────────────────────────────────────────
    "locale": """\
LANG=de_DE.UTF-8
LANGUAGE=de_DE:de
LC_CTYPE="de_DE.UTF-8"
LC_NUMERIC="de_DE.UTF-8"
LC_TIME="de_DE.UTF-8"
LC_COLLATE="de_DE.UTF-8"
LC_MONETARY="de_DE.UTF-8"
LC_MESSAGES="de_DE.UTF-8"
LC_PAPER="de_DE.UTF-8"
LC_NAME="de_DE.UTF-8"
LC_ADDRESS="de_DE.UTF-8"
LC_TELEPHONE="de_DE.UTF-8"
LC_MEASUREMENT="de_DE.UTF-8"
LC_IDENTIFICATION="de_DE.UTF-8"
LC_ALL=""",

    "locale -a": """\
C
C.UTF-8
de_DE.utf8
en_GB.utf8
en_US.utf8
POSIX""",

    "locale -a | grep de_DE": "de_DE.utf8",

    "localectl": """\
   System Locale: LANG=de_DE.UTF-8
       VC Keymap: de
      X11 Layout: de
       X11 Model: pc105""",

    "localectl list-locales": """\
C.UTF-8
de_DE.UTF-8
en_GB.UTF-8
en_US.UTF-8""",

    "localectl set-locale LANG=de_DE.UTF-8": "(Systemlocale auf de_DE.UTF-8 gesetzt — wirkt nach Neuanmeldung)",

    "iconv -l": """\
The following list contains all the coded character sets known.  This does
not necessarily mean that all combinations of these names can be used for
the FROM and TO command line parameters.  One coded character set can be
listed with several different names (aliases).

  437, 500, 500V1, 850, 851, 852, 855, 856, 857, 860, 861, 862, 863, 864,
  865, 866, 866NAV, 869, 874, 904, 1026, 1046, 1047, 8859_1, 8859_2,
  ...
  ISO-8859-1, ISO-8859-2, ISO-8859-3, ISO-8859-4, ISO-8859-5,
  UTF-8, UTF-16, UTF-16BE, UTF-16LE, UTF-32, UTF-32BE, UTF-32LE""",

    "iconv -f ISO-8859-1 -t UTF-8 datei.txt": "(Konvertierung erfolgreich — Ausgabe auf stdout)",

    "timedatectl list-timezones": """\
Africa/Abidjan
Africa/Accra
...
Europe/Berlin
Europe/Brussels
Europe/Bucharest
Europe/Budapest
...
UTC""",

    "timedatectl list-timezones | grep Europe": """\
Europe/Amsterdam
Europe/Andorra
Europe/Athens
Europe/Belgrade
Europe/Berlin
Europe/Brussels
Europe/Bucharest
Europe/Budapest
Europe/Chisinau
Europe/Copenhagen
Europe/Dublin
Europe/Gibraltar
Europe/Helsinki
Europe/Istanbul
Europe/Kiev
Europe/Lisbon
Europe/Ljubljana
Europe/London
Europe/Luxembourg
Europe/Madrid
Europe/Malta
Europe/Minsk
Europe/Monaco
Europe/Moscow
Europe/Nicosia
Europe/Oslo
Europe/Paris
Europe/Prague
Europe/Riga
Europe/Rome
Europe/Samara
Europe/Sofia
Europe/Stockholm
Europe/Tallinn
Europe/Tirane
Europe/Uzhgorod
Europe/Vaduz
Europe/Vienna
Europe/Vilnius
Europe/Warsaw
Europe/Zurich""",

    "timedatectl set-timezone Europe/Berlin": "(Zeitzone auf Europe/Berlin gesetzt)",
    "timedatectl set-timezone UTC": "(Zeitzone auf UTC gesetzt)",

    "ls /usr/share/zoneinfo/": """\
Africa      America    Antarctica  Arctic  Asia    Atlantic
Australia   Brazil     Canada      Chile   Etc     Europe
Indian      Mexico     Pacific     US      UTC     posix""",

    "ls /usr/share/zoneinfo/Europe/": """\
Amsterdam   Andorra   Athens    Belgrade   Berlin    Brussels
Bucharest   Budapest  Dublin    Gibraltar  Helsinki  Istanbul
Kiev        Lisbon    Ljubljana London     Madrid    Malta
Monaco      Moscow    Oslo      Paris      Prague    Rome
Stockholm   Vienna    Warsaw    Zurich""",

    "echo $DISPLAY": ":0",

    "xdpyinfo": """\
name of display:    :0
version number:    11.0
vendor string:    The X.Org Foundation
vendor release number:    12013000
X.Org version: 1.20.13
maximum request size:  16777212 bytes
image byte order:    LSBFirst
bitmap unit, bit order, padding:    32, LSBFirst, 32
image byte order:    LSBFirst
number of supported pixmap formats:    7
keycode range:    minimum 8, maximum 255
focus:  window 0x2400001, revert to Parent
number of extensions:    28
default screen number:    0
number of screens:    1

screen #0:
  dimensions:    1920x1080 pixels (527x296 millimeters)
  resolution:    93x93 dots per inch
  depths (7):    24, 1, 4, 8, 15, 16, 32
  root window id:    0x533
  depth of root window:    24 planes
  number of colormaps:    min 1, max 1
  default colormap:    0x20
  default number of colormap cells:    256
  preallocated pixels:    black 0, white 16777215
  options:    backing-store WHEN MAPPED, save-unders NO
  largest cursor:    256x256
  current input event mask:    0xda0035""",

    "xrandr": """\
Screen 0: minimum 320 x 200, current 1920 x 1080, maximum 16384 x 16384
HDMI-1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 527mm x 296mm
   1920x1080     60.00*+  50.00    59.94
   1280x720      60.00    50.00    59.94
   1024x768      60.00
   800x600       60.32    56.25
   640x480       59.94    60.00""",

    "echo $XDG_SESSION_TYPE": "x11",

    "echo $XDG_CONFIG_HOME": "/home/ghost/.config",

    "ls ~/.config/": """\
bash  dconf  fontconfig  gtk-3.0  gtk-4.0  ibus
nautilus  pulse  systemd  user-dirs.dirs  user-dirs.locale""",

    "xauth list": """\
neongrid-9/unix:0  MIT-MAGIC-COOKIE-1  4a7b8c2d9e1f3a5b6c7d8e9f0a1b2c3d
neongrid-9/unix:1  MIT-MAGIC-COOKIE-1  1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e""",

    "systemctl status cups": """\
● cups.service - CUPS Scheduler
     Loaded: loaded (/lib/systemd/system/cups.service; enabled)
     Active: active (running) since Mon 2024-01-15 09:00:00 UTC; 3h 12min ago
       Docs: man:cupsd(8)
   Main PID: 789 (cupsd)
     Status: "Scheduler is running..."
      Tasks: 1 (limit: 4915)
     Memory: 3.6M
        CPU: 156ms""",

    "lpstat -p": """\
printer HP_LaserJet_Pro is idle.  enabled since Mon 15 Jan 2024 09:00:00 UTC
printer Brother_MFC is idle.  enabled since Sun 14 Jan 2024 12:00:00 UTC
printer PDF is idle.  enabled since Mon 15 Jan 2024 09:00:00 UTC""",

    "lpstat -a": """\
HP_LaserJet_Pro accepting requests since Mon 15 Jan 2024 09:00:00 UTC
Brother_MFC accepting requests since Sun 14 Jan 2024 12:00:00 UTC
PDF accepting requests since Mon 15 Jan 2024 09:00:00 UTC""",

    "lpstat -d": "system default destination: HP_LaserJet_Pro",

    "lpstat -t": """\
scheduler is running
system default destination: HP_LaserJet_Pro
device for HP_LaserJet_Pro: socket://192.168.1.20:9100
device for Brother_MFC: usb://Brother/MFC-L2710DW
printer HP_LaserJet_Pro is idle.  enabled since Mon 15 Jan 2024 09:00:00 UTC
printer Brother_MFC is idle.  enabled since Sun 14 Jan 2024 12:00:00 UTC
HP_LaserJet_Pro accepting requests since Mon 15 Jan 2024 09:00:00 UTC
Brother_MFC accepting requests since Sun 14 Jan 2024 12:00:00 UTC""",

    "lpq": """\
HP_LaserJet_Pro is ready
no entries""",

    "lpq -P HP_LaserJet_Pro": """\
HP_LaserJet_Pro is ready
no entries""",

    "lpr datei.txt": "(Datei datei.txt an Standarddrucker HP_LaserJet_Pro gesendet — Job-ID: 42)",
    "lpr report.pdf": "(Datei report.pdf an Standarddrucker gesendet — Job-ID: 43)",
    "lp datei.txt": "request id is HP_LaserJet_Pro-42 (1 file(s))",

    "lprm -": "(Alle eigenen Druckjobs aus der Warteschlange entfernt)",
    "cancel": "(Druckjob abgebrochen)",

    "cupsenable HP_LaserJet_Pro": "(Drucker HP_LaserJet_Pro aktiviert)",
    "cupsdisable HP_LaserJet_Pro": "(Drucker HP_LaserJet_Pro deaktiviert)",

    "locale-gen de_DE.UTF-8": """\
Generating locales (this might take a while)...
  de_DE.UTF-8... done
Generation complete.""",

    "locale-gen": """\
Generating locales (this might take a while)...
  de_DE.UTF-8... done
  en_US.UTF-8... done
Generation complete.""",

    "update-locale LANG=de_DE.UTF-8": "(Systemlocale in /etc/default/locale auf de_DE.UTF-8 gesetzt)",

    "dpkg-reconfigure tzdata": """\
(Interaktive Zeitzonen-Auswahl gestartet)
Current default time zone: 'Europe/Berlin'
Local time is now:      Mon Jan 15 10:00:00 CET 2024.
Universal Time is now:  Mon Jan 15 09:00:00 UTC 2024.""",

    # ── Kapitel 15: Sicherheit / Security ────────────────────────────────────
    "find / -perm -4000 -type f 2>/dev/null": """\
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/su
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/umount
/usr/bin/mount
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper""",

    "find / -perm -2000 -type f 2>/dev/null": """\
/usr/bin/write
/usr/bin/wall
/usr/bin/ssh-agent
/var/local
/var/mail
/var/spool/mail""",

    "find / -perm /6000 -type f 2>/dev/null": """\
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/su
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/write
/usr/bin/wall""",

    "find / -mtime -1 -type f 2>/dev/null": """\
/var/log/auth.log
/var/log/syslog
/home/ghost/.bash_history
/tmp/tmpXk3j9f
/run/systemd/sessions/1.ref""",

    "cat /etc/ssh/sshd_config": """\
# This is the sshd server system-wide configuration file.
# See sshd_config(5) for more information.

Port 22
AddressFamily any
ListenAddress 0.0.0.0

HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

SyslogFacility AUTH
LogLevel INFO

LoginGraceTime 2m
PermitRootLogin prohibit-password
StrictModes yes
MaxAuthTries 6
MaxSessions 10

PubkeyAuthentication yes
AuthorizedKeysFile     .ssh/authorized_keys

PasswordAuthentication yes
PermitEmptyPasswords no

ChallengeResponseAuthentication no

UsePAM yes

X11Forwarding yes
PrintMotd no

AcceptEnv LANG LC_*

Subsystem sftp /usr/lib/openssh/sftp-server""",

    "sshd -t": "(SSH-Daemon Syntax-Check: keine Fehler gefunden)",
    "systemctl restart sshd": "(sshd neu gestartet)",
    "systemctl status sshd": """\
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled)
     Active: active (running) since Mon 2024-01-15 09:23:11 UTC; 2h 14min ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 1337 (sshd)
      Tasks: 1 (limit: 4915)
     Memory: 2.8M
        CPU: 89ms""",

    "gpg --list-keys": """\
/home/ghost/.gnupg/pubring.kbx
------------------------------
pub   rsa4096 2024-01-15 [SC]
      4A7B8C2D9E1F3A5B6C7D8E9F0A1B2C3D4E5F6A7B
uid           [ultimate] Ghost <ghost@neongrid.net>
sub   rsa4096 2024-01-15 [E]

pub   rsa2048 2023-06-01 [SC]
      1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0C
uid           [  full  ] Zara Z3R0 <zara@neongrid.net>
sub   rsa2048 2023-06-01 [E]""",

    "gpg --list-secret-keys": """\
/home/ghost/.gnupg/pubring.kbx
------------------------------
sec   rsa4096 2024-01-15 [SC]
      4A7B8C2D9E1F3A5B6C7D8E9F0A1B2C3D4E5F6A7B
uid           [ultimate] Ghost <ghost@neongrid.net>
ssb   rsa4096 2024-01-15 [E]""",

    "gpg --fingerprint": """\
pub   rsa4096 2024-01-15 [SC]
      4A7B 8C2D 9E1F 3A5B 6C7D  8E9F 0A1B 2C3D 4E5F 6A7B
uid           [ultimate] Ghost <ghost@neongrid.net>
sub   rsa4096 2024-01-15 [E]""",

    "gpg --gen-key": """\
gpg (GnuPG) 2.2.40; Copyright (C) 2022 g10 Code GmbH
gpg: Schlüsselpaar wird erzeugt...
gpg: Schlüssel 0A1B2C3D4E5F6A7B wurde erzeugt
gpg: Widerrufs-Zertifikat gespeichert als '/home/ghost/.gnupg/openpgp-revocs.d/...'
Öffentlichen und geheimen Schlüssel erzeugt und signiert.""",

    "fail2ban-client status": """\
Status
|- Number of jail:      2
`- Jail list:   sshd, apache-auth""",

    "fail2ban-client status sshd": """\
Status for the jail: sshd
|- Filter
|  |- Currently failed: 3
|  |- Total failed:     1847
|  `- File list:        /var/log/auth.log
`- Actions
   |- Currently banned: 2
   |- Total banned:     89
   `- Banned IP list:   47.101.12.33 185.220.101.47""",

    "cat /etc/fail2ban/jail.local": """\
[DEFAULT]
bantime  = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port    = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s""",

    "sudo -l": """\
Matching Defaults entries for ghost on neongrid:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\\:/usr/local/bin\\:/usr/sbin\\:/usr/bin\\:/sbin\\:/bin

User ghost may run the following commands on neongrid:
    (ALL : ALL) ALL""",

    "sudo -l -U ghost": """\
Matching Defaults entries for ghost on neongrid:
    env_reset, mail_badpass

User ghost may run the following commands on neongrid:
    (ALL : ALL) ALL""",

    "visudo": "(Öffnet /etc/sudoers im sicheren Editor mit Syntax-Prüfung)",

    "openssl dgst -sha256 /etc/passwd": """\
SHA256(/etc/passwd)= a3f8b2c1d4e5f6789012345678901234567890abcdef1234567890abcdef12345""",

    "openssl dgst -md5 /etc/passwd": """\
MD5(/etc/passwd)= d41d8cd98f00b204e9800998ecf8427e""",

    "openssl enc -aes-256-cbc -in datei.txt -out datei.enc": """\
enter AES-256-CBC encryption password:
Verifying - enter AES-256-CBC encryption password:
(Datei datei.txt wurde verschlüsselt → datei.enc)""",

    "openssl enc -d -aes-256-cbc -in datei.enc -out datei.txt": """\
enter AES-256-CBC decryption password:
(Datei datei.enc wurde entschlüsselt → datei.txt)""",

    "openssl rand -base64 32": "K3xN9mP7qR2sT5vW8yZ1aB4cD6eF0gH+J/L=",

    "cryptsetup luksFormat /dev/sdb1": """\
WARNING!
========
This will overwrite data on /dev/sdb1 irrevocably.

Are you sure? (Type 'yes' in capital letters): YES
Enter passphrase for /dev/sdb1:
Verify passphrase:
(LUKS-Container auf /dev/sdb1 erstellt)""",

    "cryptsetup luksDump /dev/sdb1": """\
LUKS header information
Version:        2
Epoch:          3
Metadata area:  16384 [bytes]
Keyslots area:  16744448 [bytes]
UUID:           a1b2c3d4-e5f6-7890-abcd-ef1234567890
Label:          (no label)
Subsystem:      (no subsystem)
Flags:          (no flags)

Data segments:
  0: crypt
\toffset: 16777216 [bytes]
\tlength: (whole device)
\tcipher: aes-xts-plain64
\tcipher_key: 512 bits""",

    "iptables -L -n -v": """\
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
 1234  98K  ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:22
  567  45K  ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:80
  234  18K  ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:443
    0     0 DROP       all  --  *      *       47.101.12.33         0.0.0.0/0
   89  7200 DROP       all  --  *      *       185.220.101.47       0.0.0.0/0
  456  36K  ACCEPT     all  --  lo     *       0.0.0.0/0            0.0.0.0/0

Chain FORWARD (policy DROP 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 3456 packets, 456K bytes)
 pkts bytes target     prot opt in     out     source               destination""",

    "iptables-save": """\
# Generated by iptables-save v1.8.7
*filter
:INPUT ACCEPT [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -s 47.101.12.33/32 -j DROP
COMMIT""",

    "last": """\
ghost    pts/0        192.168.1.10     Mon Jan 15 09:23   still logged in
ghost    pts/1        10.0.0.5         Mon Jan 15 08:15 - 09:00  (00:45)
root     tty1                          Sun Jan 14 23:59 - 00:02  (00:02)
ghost    pts/0        192.168.1.10     Sun Jan 14 18:30 - 22:45  (04:15)
reboot   system boot  6.1.0-neongrid9  Sun Jan 14 18:28
ghost    pts/0        192.168.1.10     Sat Jan 13 10:00 - 17:30  (07:30)

wtmp begins Sat Jan 13 10:00:00 2024""",

    "last -F": """\
ghost    pts/0        192.168.1.10     Mon Jan 15 09:23:11 2024   still logged in
ghost    pts/1        10.0.0.5         Mon Jan 15 08:15:30 2024 - Mon Jan 15 09:00:45 2024  (00:45)
root     tty1                          Sun Jan 14 23:59:01 2024 - Mon Jan 15 00:02:15 2024  (00:02)

wtmp begins Sat Jan 13 10:00:00 2024""",

    "lastb": """\
root     ssh:notty    47.101.12.33     Mon Jan 15 09:20 - 09:20  (00:00)
root     ssh:notty    47.101.12.33     Mon Jan 15 09:20 - 09:20  (00:00)
admin    ssh:notty    185.220.101.47   Mon Jan 15 09:18 - 09:18  (00:00)
root     ssh:notty    185.220.101.47   Mon Jan 15 09:18 - 09:18  (00:00)
ghost    ssh:notty    47.101.12.33     Mon Jan 15 09:15 - 09:15  (00:00)

btmp begins Mon Jan 15 08:00:00 2024""",

    "lastb | head -20": """\
root     ssh:notty    47.101.12.33     Mon Jan 15 09:20 - 09:20  (00:00)
root     ssh:notty    47.101.12.33     Mon Jan 15 09:20 - 09:20  (00:00)
admin    ssh:notty    185.220.101.47   Mon Jan 15 09:18 - 09:18  (00:00)""",

    "w": """\
 09:45:23 up  2:17,  2 users,  load average: 0.15, 0.22, 0.18
USER     TTY      FROM             LOGIN@   IDLE JCPU   PCPU WHAT
ghost    pts/0    192.168.1.10     09:23    0.00s  0.05s  0.01s w
ghost    pts/1    10.0.0.5         08:15   22:00m  0.03s  0.03s bash""",

    "nmap -sV localhost": """\
Starting Nmap 7.93 ( https://nmap.org )
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000088s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    nginx 1.22.0
5432/tcp open  pgsql   PostgreSQL DB 9.6.0 or later

Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/
Nmap done: 1 IP address (1 host scanned) in 1.23 seconds""",

    "cat /proc/self/status": """\
Name:\tbash
Umask:\t0022
State:\tS (sleeping)
Tgid:\t31337
Ngid:\t0
Pid:\t31337
PPid:\t31336
TracerPid:\t0
Uid:\t1000\t1000\t1000\t1000
Gid:\t1000\t1000\t1000\t1000
VmPeak:\t   13372 kB
VmSize:\t   13372 kB
VmRSS:\t    5248 kB
Threads:\t1""",

    # ── Topic 101: System Architecture ───────────────────────────────────────────
    "init": """\
init: Wechselt in Runlevel. Unter systemd: Weiterleitung an systemctl isolate.
Beispiel: init 3  →  systemctl isolate multi-user.target""",

    "init 0": "Fährt das System herunter (Runlevel 0).",
    "init 6": "Startet das System neu (Runlevel 6).",

    "wall": """\
Broadcast message from root@neongrid9 (pts/0) (Sun Apr 20 12:00:00 2026):

Achtung: System wird in 5 Minuten neu gestartet.""",

    "wall test": """\
Broadcast message from root@neongrid9 (pts/0) (Sun Apr 20 12:00:00 2026):

test""",

    # ── Topic 102: Paketverwaltung ────────────────────────────────────────────────
    "apt-get update": """\
Hit:1 http://deb.debian.org/debian bookworm InRelease
Get:2 http://security.debian.org bookworm-security InRelease [55.4 kB]
Get:3 http://deb.debian.org/debian bookworm-updates InRelease [52.1 kB]
Fetched 107 kB in 2s (53.5 kB/s)
Reading package lists... Done""",

    "apt-get install vim": """\
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  vim vim-runtime
0 upgraded, 2 newly installed, 0 to remove and 0 not upgraded.
Need to get 1,734 kB of archives.
After this operation, 8,152 kB of additional disk space will be used.
Get:1 http://deb.debian.org/debian bookworm/main amd64 vim 2:9.0.1378-2 [1,368 kB]
Get:2 http://deb.debian.org/debian bookworm/main amd64 vim-runtime 2:9.0.1378-2 [366 kB]
Setting up vim-runtime (2:9.0.1378-2) ...
Setting up vim (2:9.0.1378-2) ...
update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/vi""",

    "apt-get remove vim": """\
Reading package lists... Done
Building dependency tree... Done
The following packages will be REMOVED:
  vim
0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
After this operation, 3,756 kB disk space will be freed.
(Reading database ... 185432 files and directories currently installed.)
Removing vim (2:9.0.1378-2) ...""",

    "apt-get upgrade": """\
Reading package lists... Done
Building dependency tree... Done
Calculating upgrade... Done
The following packages will be upgraded:
  bash curl libssl3 openssl
4 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
Need to get 2.3 MB of archives.""",

    "rpm2cpio": """\
rpm2cpio: Konvertiert ein RPM-Archiv in ein cpio-Archiv.
Verwendung: rpm2cpio paket.rpm | cpio -idmv
Extrahiert Dateien aus einem RPM ohne Installation.""",

    "rpm2cpio package.rpm": """\
Extrahiere Inhalt von package.rpm als cpio-Stream...
(Ausgabe in cpio-Format — leite weiter an: cpio -idmv)""",

    # ── Topic 103: GNU und Unix-Befehle ──────────────────────────────────────────
    "cp file.txt backup.txt": "(Datei file.txt nach backup.txt kopiert)",

    "cp -r /etc/network /tmp/network_backup": """\
(Verzeichnis /etc/network rekursiv nach /tmp/network_backup kopiert)""",

    "cp -p /etc/hosts /tmp/hosts.bak": """\
(Datei mit Metadaten — Berechtigungen, Zeitstempel — kopiert)""",

    "mv file.txt newname.txt": "(Datei file.txt nach newname.txt umbenannt)",

    "mv /tmp/data /var/data": "(Verzeichnis /tmp/data nach /var/data verschoben)",

    "rm file.txt": "(Datei file.txt gelöscht)",

    "rm -rf /tmp/testdir": "(Verzeichnis /tmp/testdir rekursiv gelöscht)",

    "rm -i file.txt": """\
rm: remove regular file 'file.txt'? y
(Datei gelöscht)""",

    "mkdir testdir": "(Verzeichnis testdir erstellt)",

    "mkdir -p /tmp/a/b/c": """\
(Verzeichnisbaum /tmp/a/b/c erstellt — intermediate dirs angelegt)""",

    "rmdir testdir": "(Leeres Verzeichnis testdir entfernt)",

    "rmdir -p /tmp/a/b/c": """\
(Verzeichnisbaum /tmp/a/b/c entfernt — alle leeren Eltern auch gelöscht)""",

    "pwd": "/home/ghost",

    "less /etc/passwd": """\
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash
(Press q to quit, Space für nächste Seite)""",

    "ln -s /etc/hosts /tmp/hosts_link": """\
(Symbolischer Link /tmp/hosts_link → /etc/hosts erstellt)""",

    "ln /etc/hosts /tmp/hosts_hard": """\
(Harter Link /tmp/hosts_hard → /etc/hosts erstellt)""",

    "touch newfile.txt": """\
(Datei newfile.txt erstellt bzw. Zeitstempel aktualisiert)""",

    "touch -t 202601010000 file.txt": """\
(Zeitstempel von file.txt auf 2026-01-01 00:00 gesetzt)""",

    "nl /etc/passwd": """\
     1\troot:x:0:0:root:/root:/bin/bash
     2\tdaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
     3\tbin:x:2:2:bin:/bin:/usr/sbin/nologin
     4\tghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash""",

    "od -c /etc/hostname": """\
0000000   n   e   o   n   g   r   i   d   9  \\n
0000012""",

    "od -x /etc/hostname": """\
0000000 656e 676f 7264 3969 0a
0000011""",

    "cut -d: -f1 /etc/passwd": """\
root
daemon
bin
sys
ghost""",

    "cut -d: -f1,3 /etc/passwd": """\
root:0
daemon:1
bin:2
ghost:1000""",

    "paste file1.txt file2.txt": """\
zeile1_links\tzeile1_rechts
zeile2_links\tzeile2_rechts
zeile3_links\tzeile3_rechts""",

    "sort /etc/passwd": """\
bin:x:2:2:bin:/bin:/usr/sbin/nologin
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash
root:x:0:0:root:/root:/bin/bash""",

    "sort -n numbers.txt": """\
1
2
5
10
42
100""",

    "sort -r /etc/passwd": """\
root:x:0:0:root:/root:/bin/bash
ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin""",

    "uniq duplicates.txt": """\
alpha
beta
gamma
delta""",

    "uniq -c duplicates.txt": """\
      1 alpha
      3 beta
      2 gamma
      1 delta""",

    "uniq -d duplicates.txt": """\
beta
gamma""",

    "split -l 100 bigfile.txt part_": """\
(bigfile.txt aufgeteilt: part_aa, part_ab, part_ac ... je 100 Zeilen)""",

    "split -b 1M bigfile.bin chunk_": """\
(bigfile.bin aufgeteilt: chunk_aa, chunk_ab ... je 1 MiB)""",

    "tee output.txt": """\
(Liest stdin, schreibt gleichzeitig auf stdout und in output.txt)""",

    "tee -a logfile.txt": """\
(Hängt stdin an logfile.txt an, gibt gleichzeitig auf stdout aus)""",

    "xargs": """\
(Liest Argumente von stdin und übergibt sie an einen Befehl)
Beispiel: find /tmp -name '*.tmp' | xargs rm""",

    "xargs rm": "(Löscht alle von stdin übergebenen Dateien)",

    "xargs -I {} cp {} /backup/": """\
(Kopiert jede Datei von stdin nach /backup/ — {} als Platzhalter)""",

    "md5sum /etc/passwd": "a3b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6  /etc/passwd",

    "md5sum -c checksums.md5": """\
/etc/passwd: OK
/etc/hostname: OK
/etc/hosts: FAILED
md5sum: WARNING: 1 computed checksum did NOT match""",

    "sha256sum /etc/passwd": """\
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /etc/passwd""",

    "sha256sum -c hashes.sha256": """\
/etc/passwd: OK
/etc/hostname: OK""",

    "sha512sum /etc/passwd": """\
cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e  /etc/passwd""",

    "gzip file.txt": "(file.txt → file.txt.gz komprimiert, Original gelöscht)",

    "gzip -k file.txt": "(file.txt → file.txt.gz komprimiert, Original behalten)",

    "gzip -d file.txt.gz": "(file.txt.gz → file.txt dekomprimiert)",

    "gzip -l file.txt.gz": """\
         compressed        uncompressed  ratio uncompressed_name
                428                1024  58.2% file.txt""",

    "gunzip file.txt.gz": "(file.txt.gz → file.txt dekomprimiert, Archiv gelöscht)",

    "zcat file.txt.gz": """\
Inhalt der komprimierten Datei:
Zeile 1: NeonGrid-9
Zeile 2: Linux Training
Zeile 3: Ghost Mode Active""",

    "bzip2 file.txt": "(file.txt → file.txt.bz2 komprimiert)",

    "bzip2 -d file.txt.bz2": "(file.txt.bz2 → file.txt dekomprimiert)",

    "bunzip2 file.txt.bz2": "(file.txt.bz2 → file.txt dekomprimiert)",

    "bzcat file.txt.bz2": """\
Inhalt der bzip2-komprimierten Datei:
Zeile 1: NeonGrid-9
Zeile 2: Linux Training""",

    "xz file.txt": "(file.txt → file.txt.xz komprimiert — stärkste Kompression)",

    "xz -d file.txt.xz": "(file.txt.xz → file.txt dekomprimiert)",

    "unxz file.txt.xz": "(file.txt.xz → file.txt dekomprimiert)",

    "xzcat file.txt.xz": """\
Inhalt der xz-komprimierten Datei:
Zeile 1: NeonGrid-9
Zeile 2: Linux Training""",

    "tar -czf archive.tar.gz /etc/network": """\
(Erstellt archive.tar.gz aus /etc/network)""",

    "tar -xzf archive.tar.gz": """\
etc/network/
etc/network/interfaces
etc/network/if-up.d/
etc/network/if-down.d/""",

    "tar -cjf archive.tar.bz2 /home/ghost": """\
(Erstellt archive.tar.bz2 aus /home/ghost mit bzip2-Kompression)""",

    "tar -tvf archive.tar.gz": """\
drwxr-xr-x root/root         0 2026-01-01 etc/network/
-rw-r--r-- root/root       623 2026-01-01 etc/network/interfaces
drwxr-xr-x root/root         0 2026-01-01 etc/network/if-up.d/""",

    "cpio -idmv": """\
(Extrahiert cpio-Archiv aus stdin — typisch: rpm2cpio pkg.rpm | cpio -idmv)
usr/bin/example
usr/share/doc/example/README""",

    "cpio -o": """\
(Erstellt cpio-Archiv aus stdin-Dateiliste — typisch: find . | cpio -o > archiv.cpio)""",

    "egrep root /etc/passwd": "root:x:0:0:root:/root:/bin/bash",

    "egrep 'root|ghost' /etc/passwd": """\
root:x:0:0:root:/root:/bin/bash
ghost:x:1000:1000:Ghost User:/home/ghost:/bin/bash""",

    "fgrep root /etc/passwd": "root:x:0:0:root:/root:/bin/bash",

    "exec bash": """\
(Aktueller Prozess wird durch bash ersetzt — kein Fork)
root@neongrid9:~#""",

    # ── Topic 104: Dateisysteme ───────────────────────────────────────────────────
    "chown ghost:ghost file.txt": """\
(Eigentümer und Gruppe von file.txt auf ghost:ghost gesetzt)""",

    "chown -R root:root /var/www": """\
(Rekursiv: alle Dateien in /var/www gehören jetzt root:root)""",

    "chgrp staff /var/project": "(Gruppe von /var/project auf staff gesetzt)",

    "chgrp -R developers /srv/app": """\
(Rekursiv: Gruppe aller Dateien in /srv/app auf developers gesetzt)""",

    "du -sh /home/ghost": "1.2G\t/home/ghost",

    "du -sh /*": """\
0\t/bin
103M\t/boot
0\t/dev
14M\t/etc
1.2G\t/home
456K\t/lib
0\t/proc
44M\t/root
1.9M\t/run
0\t/sbin
3.5G\t/usr
472M\t/var""",

    "du -h --max-depth=1 /var": """\
56K\t/var/backups
48M\t/var/cache
412M\t/var/log
4.0K\t/var/mail
4.0K\t/var/spool
472M\t/var""",

    "e2fsck /dev/sda1": """\
e2fsck 1.47.0 (5-Feb-2023)
/dev/sda1: clean, 45821/1310720 files, 891234/5242880 blocks""",

    "e2fsck -f /dev/sdb1": """\
e2fsck 1.47.0 (5-Feb-2023)
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
/dev/sdb1: 128/131072 files (0.0% non-contiguous), 23456/524288 blocks""",

    "mke2fs /dev/sdc1": """\
mke2fs 1.47.0 (5-Feb-2023)
Creating filesystem with 524288 4k blocks and 131072 inodes
Filesystem UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Superblock backups stored on blocks: 32768, 98304, 163840, 229376, 294912
Allocating group tables: done
Writing inode tables: done
Writing superblocks and filesystem accounting information: done""",

    "mke2fs -t ext4 /dev/sdc1": """\
mke2fs 1.47.0 (5-Feb-2023)
Creating filesystem with 524288 4k blocks and 131072 inodes
Filesystem UUID: b2c3d4e5-f6a7-8901-bcde-f12345678901
Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done""",

    "mkfs /dev/sdc1": """\
mke2fs 1.47.0 (5-Feb-2023)
/dev/sdc1: 2048 MiB, 2147483648 bytes, 4194304 sectors
Creating filesystem with 524288 4k blocks and 131072 inodes""",

    "mkfs.ext4 /dev/sdc1": """\
mke2fs 1.47.0 (5-Feb-2023)
Creating filesystem with 524288 4k blocks and 131072 inodes
Filesystem UUID: c3d4e5f6-a7b8-9012-cdef-012345678912
Writing superblocks and filesystem accounting information: done""",

    "mkfs.xfs /dev/sdd1": """\
meta-data=/dev/sdd1              isize=512    agcount=4, agsize=131072 blks
data     =                       bsize=4096   blocks=524288, imaxpct=25
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
realtime =none                   extsz=4096   blocks=0, rtextents=0""",

    "mkswap /dev/sde1": """\
Setting up swapspace version 1, size = 2 GiB (2147479552 bytes)
no label, UUID=d4e5f6a7-b8c9-0123-def0-123456789012""",

    "gdisk /dev/sdb": """\
GPT fdisk (gdisk) version 1.0.9
Partition table scan:
  MBR: protective
  GPT: present
Found valid GPT with protective MBR; using GPT.
Command (? for help): """,

    "gdisk -l /dev/sdb": """\
GPT fdisk (gdisk) version 1.0.9
Disk /dev/sdb: 41943040 sectors, 20.0 GiB
Disk identifier (GUID): E5F6A7B8-C9D0-1234-EF01-234567890123
Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048         2099199   1024.0 MiB  8300  Linux filesystem
   2         2099200        41943006   19.0 GiB    8300  Linux filesystem""",

    "parted /dev/sdb": """\
GNU Parted 3.5
Using /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) """,

    "parted /dev/sdb print": """\
Model: ATA QEMU HARDDISK (scsi)
Disk /dev/sdb: 21.5GB
Partition Table: gpt
Number  Start   End     Size    File system  Name
 1      1049kB  1075MB  1074MB  ext4         Linux filesystem
 2      1075MB  21.5GB  20.4GB  ext4         Linux filesystem""",

    "parted -l": """\
Model: ATA QEMU HARDDISK (scsi)
Disk /dev/sda: 21.5GB
Partition Table: msdos
Number  Start   End     Size    Type     File system  Flags
 1      1049kB  538MB   537MB   primary  fat32        boot
 2      538MB   21.5GB  21.0GB  primary  ext4""",

    "locate passwd": """\
/etc/passwd
/etc/passwd-
/usr/share/doc/passwd/copyright
/usr/share/man/man5/passwd.5.gz
/usr/bin/passwd""",

    "locate -i readme": """\
/home/ghost/README.md
/usr/share/doc/bash/README
/usr/share/doc/coreutils/README""",

    "xfs_repair /dev/sdd1": """\
Phase 1 - find and verify superblock...
Phase 2 - using internal log
        - zero log...
        - scan filesystem freespace and inode maps...
Phase 3 - for each AG...
        - process known inodes...
Phase 7 - verify and correct link counts...
done""",

    "xfs_db /dev/sdd1": """\
xfs_db - XFS Debugger, Version 6.7.0
xfs_db>""",

    "xfs_fsr /dev/sdd1": """\
xfs_fsr: /dev/sdd1 start inode=0
extents before:5 after:3 DONE ino=131074
extents before:3 after:1 DONE ino=131075""",

    # ── Topic 105: Shell & Scripting ──────────────────────────────────────────────
    "seq 5": """\
1
2
3
4
5""",

    "seq 1 2 10": """\
1
3
5
7
9""",

    "seq -w 1 10": """\
01
02
03
04
05
06
07
08
09
10""",

    # ── Topic 107: Administrative Tasks ──────────────────────────────────────────
    "groupmod -n newname oldname": """\
(Gruppe oldname wurde in newname umbenannt)""",

    "groupmod -g 1500 developers": """\
(GID der Gruppe developers wurde auf 1500 geändert)""",

    "systemd-run --unit=test sleep 30": """\
Running as unit: test.service
Root   : /
Service: test.service""",

    "systemd-run --on-active=1h /usr/bin/backup.sh": """\
Running as unit: run-r1234abcd.service
Scheduled to run in 1h""",

    "tzselect": """\
Please identify a location so that time zone rules can be set correctly.
 1) Africa
 2) Americas
 3) Antarctica
 4) Asia
 5) Atlantic Ocean
 6) Australia
 7) Europe
 8) Indian Ocean
 9) Pacific Ocean
10) coord - I want to use geographical coordinates.
11) TZ - I want to specify the time zone using the Posix TZ format.
#?""",

    # ── Topic 108: Systemdienste ──────────────────────────────────────────────────
    "logger -t myapp 'Test-Meldung'": """\
(Nachricht in Syslog geschrieben: myapp: Test-Meldung)""",

    "logger": """\
(Schreibt eine Nachricht in das System-Log via syslog)
Verwendung: logger [-t TAG] [-p FACILITY.PRIORITY] Nachricht""",

    "logger -p auth.info 'Login erfolgreich'": """\
(Syslog-Eintrag: auth.info: Login erfolgreich)""",

    "systemd-cat echo 'Test'": """\
(Ausgabe von 'echo Test' wird ins Journal geschrieben)""",

    "systemd-cat -t myapp -p info": """\
(stdin/stdout wird ins Journal als myapp mit Priorität info geschrieben)""",

    "mail ghost@localhost": """\
Subject: Test
Hallo Ghost
.
EOT""",

    "mail -s 'Subject' ghost@localhost": """\
Cc:
(Wartet auf Nachrichtentext — Abschluss mit . auf eigener Zeile)""",

    "mail": """\
Mail version 8.1.2 01/15/2001.  Type ? for help.
"/var/mail/ghost": 2 messages 1 new 1 unread
>N  1 root@neongrid9   Mon Apr 20 12:00  18/624  Systembenachrichtigung
 U  2 cron@neongrid9   Mon Apr 20 06:00  12/456  Daily backup complete""",

    "chronyc tracking": """\
Reference ID    : C0000201 (192.0.2.1)
Stratum         : 2
Ref time (UTC)  : Sun Apr 20 10:00:00 2026
System time     : 0.000000001 seconds fast of NTP time
Last offset     : +0.000000023 seconds
Frequency       : 0.000 ppm slow
Root delay      : 0.001 seconds
Leap status     : Normal""",

    "chronyc sources": """\
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^* ntp1.example.com              2   6   377    31    +23us[  +45us] +/-  456us
^- ntp2.example.com              2   6   377    30   -450us[ -428us] +/-  870us""",

    "chronyc makestep": "200 OK",

    "ntpd -q": "ntpd: time set +0.000002s",

    "ntpdate ntp.ubuntu.com": """\
20 Apr 09:00:00 ntpdate[1234]: adjust time server 162.159.200.1 offset +0.002345 sec""",

    # ── Topic 109: Netzwerk ───────────────────────────────────────────────────────
    "ping6 ::1": """\
PING ::1(::1) 56 data bytes
64 bytes from ::1: icmp_seq=1 ttl=64 time=0.042 ms
64 bytes from ::1: icmp_seq=2 ttl=64 time=0.038 ms
--- ::1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss""",

    "ping6 fe80::1": """\
PING fe80::1(fe80::1) 56 data bytes
64 bytes from fe80::1%eth0: icmp_seq=1 ttl=64 time=0.215 ms""",

    "tracepath6 ::1": """\
 1?: [LOCALHOST]                      pmtu 65536
 1:  ::1                                             0.038ms reached
     Resume: pmtu 65536 hops 1 back 1""",

    "tracepath6 2001:db8::1": """\
 1?: [LOCALHOST]                      pmtu 1500
 1:  fe80::1                                         0.512ms
 2:  2001:db8::1                                     1.234ms reached
     Resume: pmtu 1500 hops 2 back 2""",

    "traceroute6 ::1": """\
traceroute to ::1 (::1), 30 hops max, 80 byte packets
 1  ::1  0.036 ms  0.028 ms  0.027 ms""",

    "netcat -l -p 1234": """\
(netcat wartet auf eingehende Verbindung auf Port 1234)""",

    "netcat localhost 1234": """\
(Verbindet zu localhost auf Port 1234)
Hallo, Verbindung hergestellt!""",

    "nc -z -v localhost 22": """\
Connection to localhost 22 port [tcp/ssh] succeeded!""",

    "nc -z -v localhost 1-100": """\
Connection to localhost 22 port [tcp/ssh] succeeded!
Connection to localhost 80 port [tcp/http] succeeded!""",

    # ── Topic 110: Sicherheit ─────────────────────────────────────────────────────
    "ssh ghost@localhost": """\
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ED25519 key fingerprint is SHA256:abc123def456ghi789.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'localhost' to the list of known hosts.
ghost@localhost's password:
Welcome to NeonGrid-9!
Last login: Sun Apr 20 09:00:00 2026""",

    "ssh -i ~/.ssh/id_rsa ghost@remotehost": """\
Welcome to NeonGrid-9 Remote!
Last login: Sun Apr 20 08:30:00 2026""",

    "ssh -p 2222 ghost@localhost": """\
ghost@localhost's password:
Welcome to NeonGrid-9 (Port 2222)!""",

    "ssh -L 8080:localhost:80 ghost@server": """\
(SSH-Tunnel: lokaler Port 8080 → server:80 weitergeleitet)""",

    "ssh-keygen -t ed25519": """\
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/ghost/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Your identification has been saved in /home/ghost/.ssh/id_ed25519
Your public key has been saved in /home/ghost/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:abc123def456ghi789jkl012mno345pqr678stu901 ghost@neongrid9""",

    "ssh-keygen -t rsa -b 4096": """\
Generating public/private rsa key pair.
Enter file in which to save the key (/home/ghost/.ssh/id_rsa):
Your identification has been saved in /home/ghost/.ssh/id_rsa
Your public key has been saved in /home/ghost/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:xyz789abc123def456ghi789jkl012mno345 ghost@neongrid9""",

    "ssh-copy-id ghost@remotehost": """\
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed
ghost@remotehost's password:
Number of key(s) added: 1
Now try logging into the machine, with: "ssh 'ghost@remotehost'"
and check to make sure that only the key(s) you wanted were added.""",

    "ssh-add ~/.ssh/id_ed25519": """\
Identity added: /home/ghost/.ssh/id_ed25519 (ghost@neongrid9)""",

    "ssh-add -l": """\
256 SHA256:abc123def456ghi789jkl012mno345pqr678stu901 ghost@neongrid9 (ED25519)""",

    "ssh-add -D": "All identities removed.",

    "ssh-agent bash": """\
(Startet SSH-Agent und öffnet neue Shell in dessen Umgebung)
SSH_AUTH_SOCK=/tmp/ssh-XXXXXX/agent.1234; export SSH_AUTH_SOCK;
SSH_AGENT_PID=1234; export SSH_AGENT_PID;""",

    "eval $(ssh-agent)": "Agent pid 1234",

    "gpg-agent --daemon": """\
GPG_AGENT_INFO=/run/user/1000/gnupg/S.gpg-agent:1234:1; export GPG_AGENT_INFO;""",

    "gpg-agent --version": """\
gpg-agent (GnuPG) 2.2.27
libgcrypt 1.8.8
Copyright (C) 2021 Free Software Foundation, Inc.""",

    "ulimit -a": """\
core file size              (blocks, -c) 0
data seg size               (kbytes, -d) unlimited
file size                   (blocks, -f) unlimited
max locked memory           (kbytes, -l) 8192
open files                          (-n) 1024
pipe size                (512 bytes, -p) 8
stack size                  (kbytes, -s) 8192
cpu time                   (seconds, -t) unlimited
max user processes                  (-u) 31220
virtual memory              (kbytes, -v) unlimited""",

    "ulimit -n 4096": """\
(Datei-Deskriptor-Limit auf 4096 erhöht — gilt nur für aktuelle Shell-Session)""",

    "ulimit -n": "1024",
}

# ── Platzhalter für unbekannte Befehle ─────────────────────────────────────────
UNKNOWN_CMD_RESPONSES = [
    "command not found",
    "No such file or directory",
    "Permission denied",
    "bash: {cmd}: command not found",
]


def normalize_cmd(cmd: str) -> str:
    """Normalisiert einen Befehl für den Lookup."""
    return cmd.strip().lower()


def get_output(cmd: str) -> tuple[bool, str]:
    """
    Gibt (gefunden, ausgabe) zurück.
    Sucht exakt, dann prefix-basiert.
    """
    cmd_stripped = cmd.strip()
    cmd_lower    = cmd_stripped.lower()

    # Exakte Übereinstimmung
    if cmd_stripped in SIMULATED_OUTPUTS:
        return True, SIMULATED_OUTPUTS[cmd_stripped]

    # Case-insensitive exakt
    for key, val in SIMULATED_OUTPUTS.items():
        if key.lower() == cmd_lower:
            return True, val

    # Prefix-Matching (z.B. "lspci -vv" → "lspci -v")
    for key, val in SIMULATED_OUTPUTS.items():
        if cmd_lower.startswith(key.lower()) and len(cmd_lower) > len(key):
            return True, val + f"\n(Ausgabe für '{key}' — Flags simuliert)"

    # Nur der Basis-Befehl
    base = cmd_stripped.split()[0] if cmd_stripped.split() else ""
    for key, val in SIMULATED_OUTPUTS.items():
        if key.split()[0].lower() == base.lower():
            return True, val + f"\n('{cmd_stripped}' → Basis-Ausgabe)"

    return False, f"bash: {cmd_stripped}: command not found"


def run_terminal(
    expected: list[str],
    task_description: str,
    hint_available: bool = False,
    hint_text: str = "",
    max_attempts: int = 5
) -> tuple[bool, int, str]:
    """
    Interaktives Terminal-Simulationsfenster.
    Returns: (success, attempts_used, final_command)
    """
    from engine.display import C, prompt_input, show_code, show_error, show_success

    attempts = 0
    last_cmd = ""

    print(C.GRAY + "\n  ╔═[ TERMINAL SIMULATION ]═══════════════════════════════╗" + C.RESET)
    print(C.GRAY + f"  ║  Aufgabe: " + C.WHITE + task_description[:54].ljust(54) + C.GRAY + "║" + C.RESET)
    print(C.GRAY + "  ║  Tippe einen Linux-Befehl. 'hint' für Hinweis.        ║" + C.RESET)
    print(C.GRAY + "  ╚══════════════════════════════════════════════════════╝" + C.RESET)
    print()

    while attempts < max_attempts:
        cmd = prompt_input("root@neongrid9")
        last_cmd = cmd

        if not cmd:
            continue

        if cmd.lower() in ("quit", "exit", "q"):
            return False, attempts, last_cmd

        if cmd.lower() == "hint":
            if hint_available and hint_text:
                print(C.YELLOW + f"\n  HINT: {hint_text}\n" + C.RESET)
            else:
                print(C.YELLOW + "\n  HINT: Nicht verfügbar — check die Erklärung nochmal.\n" + C.RESET)
            continue

        if cmd.lower() == "help":
            print(C.CYAN + f"\n  Erwartete Befehle: {', '.join(expected)}\n" + C.RESET)
            continue

        # Ausgabe simulieren
        found, output = get_output(cmd)
        if found:
            print()
            for line in output.split('\n')[:20]:  # max 20 Zeilen
                print(C.GREEN + "  " + line + C.RESET)
            if output.count('\n') > 20:
                print(C.GRAY + "  ... (Ausgabe gekürzt)" + C.RESET)
            print()

        # Prüfen ob richtige Antwort
        cmd_base = cmd.strip().split()[0].lower() if cmd.strip() else ""
        for exp in expected:
            exp_base = exp.strip().split()[0].lower()
            # Exakter Match oder Base-Match wenn expected nur Basis
            if cmd.strip().lower() == exp.strip().lower():
                return True, attempts + 1, cmd
            # Teilweise richtig: richtiger Basis-Befehl mit irgendwelchen Flags
            if cmd_base == exp_base and len(expected) == 1:
                return True, attempts + 1, cmd

        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0 and not found:
            print(C.WARN + f"  ✗  Befehl nicht erkannt. Noch {remaining} Versuche." + C.RESET)
        elif remaining > 0 and found:
            print(C.WARN + f"  ✗  Befehl ausgeführt, aber nicht der gesuchte. Noch {remaining} Versuche." + C.RESET)

    return False, attempts, last_cmd
