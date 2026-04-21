# NeonGrid-9 to LPIC-1 Exam Topic Mapping

This guide shows how NeonGrid-9 chapters align with official LPIC-1 exam objectives. Use this to study for the real certification exam (101 & 102).

---

## 📋 LPIC-1 Exam Structure

**LPIC-1** consists of two exams:
- **101-500:** System Architecture & Linux Installation (4 topics)
- **102-500:** Linux Administration (6 topics)

Each exam:
- 60 questions
- 90 minutes
- 500+ passing score
- Valid for 5 years

---

## 🎮 Topic Breakdown

### ✅ LPIC-1 Exam 101-500: System Architecture & Installation

---

#### **101.1: Determine and configure hardware settings**
*Weight: 2 | Estimated Study Time: 2-3 hours*

**What You Need to Know:**
- Identify different types of hardware (CPUs, RAM, storage devices)
- Use tools to detect and configure hardware
- Understand BIOS vs UEFI
- Work with device drivers and kernel modules

**NeonGrid-9 Chapter:**
- **Chapter 1: Hardware Basics** ⭐⭐⭐ (Best coverage)
- **Chapter 13: Kernel & Modules** (For driver/module concepts)
- **Chapter 19: Ghost Processors** (Advanced process management)

**Key Missions:**
- Ch01.M1: "Erste Signale — Was ist Hardware?" (Mission intro)
- Ch01.M2: "BIOS Whisper — BIOS vs UEFI"
- Ch01.Boss: "Silicon Guardian — The Motherboard Oracle"
- Ch13.M1-5: "Module Mysteries" (Device drivers)

**Commands to Master:**
```bash
lspci          # List PCI devices
lsusb          # List USB devices
lsblk          # List block devices
cat /proc/cpuinfo  # CPU information
dmidecode      # BIOS/hardware info
modprobe       # Load/unload kernel modules
insmod, rmmod  # Kernel module management
```

---

#### **101.2: Boot the system**
*Weight: 3 | Estimated Study Time: 3-4 hours*

**What You Need to Know:**
- Boot process from power-on to login
- GRUB/LILO bootloader configuration
- Kernel parameters and boot options
- Rescue/recovery boot modes
- Recovery and single-user mode

**NeonGrid-9 Chapter:**
- **Chapter 2: Boot Process** ⭐⭐⭐ (Comprehensive)
- **Chapter 18: Exam Block 1** (Comprehensive review)

**Key Missions:**
- Ch02.M1: "Awakening — Power-On Self-Test"
- Ch02.M3: "GRUB Grimoire — Bootloader Secrets"
- Ch02.M5: "Recovery Ritual — Rescue Mode"
- Ch02.Boss: "Daemon Rising — The Bootstrap King"

**Commands to Master:**
```bash
grub-mkconfig  # Update GRUB configuration
grub-install   # Install GRUB bootloader
/etc/default/grub  # GRUB config file
init, systemd  # Init system
dmesg          # Kernel messages during boot
journalctl     # Boot messages from systemd
```

---

#### **101.3: Change runlevels, boot targets, and shutdown or reboot**
*Weight: 3 | Estimated Study Time: 2-3 hours*

**What You Need to Know:**
- Runlevels (0-6, S) vs systemd targets
- systemd services and unit files
- shutdown, halt, reboot commands
- Process signals and service management

**NeonGrid-9 Chapters:**
- **Chapter 2: Boot Process** (Runlevels/targets overview)
- **Chapter 7: Processes & Signals** ⭐⭐ (Process signals)
- **Chapter 21: Network Services** ⭐⭐⭐ (systemd deep dive)

**Key Missions:**
- Ch02.M4: "Runaway Levels — Init Systems Explained"
- Ch07.M2: "Signal Cascade — Process Signals"
- Ch21.M1-10: "Service Mastery" (systemd units)
- Ch21.Boss: "Daemon Wars — The Service Controller"

**Commands to Master:**
```bash
systemctl      # Control systemd services
systemctl list-units  # List active units
systemctl enable/disable  # Enable/disable at boot
systemctl set-default  # Change default target
journalctl -xe # System journal
init <runlevel>  # Change runlevel (legacy)
shutdown -h, -r  # Shutdown/reboot
```

---

#### **101.4: Design hard disk layout**
*Weight: 4 | Estimated Study Time: 4-5 hours*

**What You Need to Know:**
- Partitioning schemes and tools
- Filesystem selection and creation
- Mount points and /etc/fstab
- LVM (Logical Volume Manager) basics
- RAID concepts

**NeonGrid-9 Chapters:**
- **Chapter 3: Filesystems** ⭐⭐⭐ (Filesystems & mounting)
- **Chapter 4: Partitions & Disks** ⭐⭐⭐ (Partitioning focus)
- **Chapter 22: Storage Advanced** ⭐⭐⭐ (RAID, LVM, advanced)

**Key Missions:**
- Ch04.M1: "Partition Protocol — fdisk & parted"
- Ch04.M5: "LVM Labyrinth — Logical Volumes"
- Ch03.M1: "Mount Quest — Understanding Filesystems"
- Ch03.M3: "Inode Intrigue — Filesystem Internals"
- Ch22.M1-10: "Storage Mastery" (RAID, snapshots, backup)
- Ch22.Boss: "The Storage Architect — Data Sovereignty"

**Commands to Master:**
```bash
fdisk, parted  # Partition tools
mkfs.ext4, mkfs.btrfs  # Create filesystems
mount, umount  # Mount filesystems
/etc/fstab    # Permanent mount configuration
lsblk         # List block devices
lvdisplay, vgdisplay  # LVM commands
mdadm         # RAID management
```

---

### ✅ LPIC-1 Exam 102-500: Linux Administration

---

#### **102.1: Operate the system**
*Weight: 4 | Estimated Study Time: 3-4 hours*

**What You Need to Know:**
- Boot into different targets
- Use rescue/recovery modes
- Account for user limits (ulimit)
- Priority and nice values
- Identify resource exhaustion
- Locate and interpret system logs

**NeonGrid-9 Chapters:**
- **Chapter 2: Boot Process** (Targets & rescue modes)
- **Chapter 7: Processes & Signals** ⭐⭐ (Priority, nice)
- **Chapter 14: Logging & Monitoring** ⭐⭐⭐ (System logs)
- **Chapter 19: Ghost Processors** (Process management)

**Key Missions:**
- Ch07.M4: "Priority Pyramid — nice and renice"
- Ch14.M1: "Log Archaeology — Finding System Information"
- Ch14.M5: "Monitor Mastery — System Monitoring"
- Ch14.Boss: "The Chronicler — Log Analysis Expert"

**Commands to Master:**
```bash
nice, renice   # Set process priority
ps, top, htop  # Process monitoring
ulimit         # User resource limits
systemctl status  # Service status
journalctl, dmesg  # System logs
df, du, free   # Resource usage
lsof           # Open file descriptors
strace         # System call tracing
```

---

#### **102.2: Setup user and group accounts and related system files**
*Weight: 3 | Estimated Study Time: 3-4 hours*

**What You Need to Know:**
- User and group management
- /etc/passwd, /etc/shadow, /etc/group
- sudo and sudoers configuration
- User account creation/deletion
- Password policies
- User login behavior (/etc/profile, .bashrc)

**NeonGrid-9 Chapters:**
- **Chapter 6: Users & Groups** ⭐⭐⭐ (Complete coverage)
- **Chapter 17: Shell Environment** ⭐⭐ (User configuration files)
- **Chapter 15: Security Hardening** ⭐⭐ (sudo, authentication)

**Key Missions:**
- Ch06.M1: "User Creation Ceremony — useradd & userdel"
- Ch06.M3: "Group Governance — Group Management"
- Ch06.M5: "Sudoers Summit — Privilege Escalation"
- Ch06.Boss: "The User Master — Access Control"
- Ch17.M1: "Environment Engineering — Shell Configuration"
- Ch15.M4: "Sudo Summit — Sudoers Configuration"

**Commands to Master:**
```bash
useradd, userdel, usermod  # User management
groupadd, groupdel, groupmod  # Group management
passwd, chpasswd  # Password management
id, groups, whoami  # User information
su, sudo       # Privilege escalation
visudo         # Edit sudoers safely
/etc/passwd, /etc/shadow, /etc/group  # Key files
```

---

#### **102.3: Manage packages**
*Weight: 3 | Estimated Study Time: 3-4 hours*

**What You Need to Know:**
- Package management tools (apt, yum, rpm)
- Install, upgrade, remove packages
- Repository configuration
- Dependency resolution
- Package searching and querying
- Compiling from source (basic)

**NeonGrid-9 Chapters:**
- **Chapter 12: Packages & Repos** ⭐⭐⭐ (Primary topic)
- **Chapter 18: Exam Block 1** (Comprehensive review)

**Key Missions:**
- Ch12.M1: "APT Adventure — Debian Package Management"
- Ch12.M3: "Repository Riddle — Adding Repositories"
- Ch12.M5: "Dependency Dilemma — Resolving Package Issues"
- Ch12.Boss: "Package Overlord — Installation Mastery"

**Commands to Master:**
```bash
apt-get, apt   # Debian/Ubuntu package management
dpkg           # Low-level Debian package tool
yum, dnf       # RedHat/CentOS package management
rpm            # Low-level RPM tool
./configure, make, make install  # Build from source
/etc/apt/sources.list  # Repository configuration
apt-cache, yum search  # Search packages
```

---

#### **102.4: Manage services**
*Weight: 4 | Estimated Study Time: 3-4 hours*

**What You Need to Know:**
- systemd service management
- Service startup/stop/restart
- Service enable/disable
- Service dependencies
- Custom service unit files
- Troubleshoot service issues

**NeonGrid-9 Chapters:**
- **Chapter 21: Network Services** ⭐⭐⭐ (systemd deep dive)
- **Chapter 2: Boot Process** ⭐⭐ (Init systems overview)
- **Chapter 13: Kernel & Modules** (systemd as PID 1)

**Key Missions:**
- Ch21.M1: "Service Sanctuary — systemd Basics"
- Ch21.M3: "Unit Unveiled — Custom Unit Files"
- Ch21.M5: "Dependency Chains — Service Dependencies"
- Ch21.Boss: "Daemon Wars — The Service Controller"

**Commands to Master:**
```bash
systemctl start, stop, restart, status  # Service control
systemctl enable, disable, is-enabled   # Boot behavior
systemctl list-units, list-dependencies  # View services
/etc/systemd/system  # Custom unit files
journalctl -u <service>  # Service logs
systemd-analyze  # Performance analysis
```

---

#### **102.5: Create and manage access to filesystems**
*Weight: 4 | Estimated Study Time: 3-4 hours*

**What You Need to Know:**
- File permissions (rwx, chmod, chown)
- Special permissions (setuid, setgid, sticky bit)
- ACLs (Access Control Lists)
- Umask and default permissions
- File attributes (immutable, append-only)
- Disk quotas

**NeonGrid-9 Chapters:**
- **Chapter 5: Permissions & Owners** ⭐⭐⭐ (Complete coverage)
- **Chapter 3: Filesystems** ⭐⭐ (Permission context)
- **Chapter 15: Security Hardening** ⭐⭐ (Security implications)

**Key Missions:**
- Ch05.M1: "Permission Protocol — Understanding rwx"
- Ch05.M3: "Mode Magic — chmod & chown"
- Ch05.M5: "ACL Adventure — Advanced Access Control"
- Ch05.M7: "Umask Universe — Default Permissions"
- Ch05.Boss: "The Permission Master — Access Control Master"

**Commands to Master:**
```bash
chmod, chown, chgrp  # Permission management
ls -l, stat      # View permissions
umask           # Default permission mask
setfacl, getfacl  # ACL management
chattr, lsattr  # File attributes
quota, setquota  # Disk quotas
find -perm     # Find by permissions
```

---

#### **102.6: Manage network connectivity**
*Weight: 4 | Estimated Study Time: 4-5 hours*

**What You Need to Know:**
- Network interfaces and IP addressing
- Static vs DHCP configuration
- DNS configuration
- Network utilities (ping, traceroute, netstat)
- Firewall basics
- VPN basics

**NeonGrid-9 Chapters:**
- **Chapter 9: Network** ⭐⭐⭐ (TCP/IP, DNS)
- **Chapter 11: Logging & Monitoring** ⭐⭐ (Network monitoring)
- **Chapter 15: Security Hardening** ⭐⭐ (Firewall basics)
- **Chapter 20: Firewall Dominion** ⭐⭐⭐ (iptables, nftables)
- **Chapter 21: Network Services** ⭐⭐⭐ (Network daemons)

**Key Missions:**
- Ch09.M1: "IP Initiative — TCP/IP Basics"
- Ch09.M3: "DNS Dynasty — Domain Name System"
- Ch09.M5: "Routing Realm — Network Routing"
- Ch09.Boss: "Network Navigator — Connectivity Master"
- Ch15.M6: "Firewall Foundations — iptables Introduction"
- Ch20.M1-10: "Firewall Mastery" (iptables, nftables)
- Ch20.Boss: "Firewall Dominion — Packet Filter Expert"

**Commands to Master:**
```bash
ip addr, ip route  # IP configuration (modern)
ifconfig, route    # Network config (legacy)
ping, traceroute, mtr  # Network testing
netstat, ss, nstat  # Connection monitoring
cat /etc/resolv.conf  # DNS configuration
iptables, nftables  # Firewall rules
hostnamectl  # Hostname configuration
nmtui, nmcli  # Network Manager (modern systems)
```

---

## 📊 Chapter-to-Exam Mapping Table

| NeonGrid Chapter | Exam 101 Topic | Exam 102 Topic | Weight | Best For |
|-----------------|---|---|---|---|
| Ch01: Hardware | 101.1 ✅ | — | 2 | Hardware identification |
| Ch02: Boot | 101.2 ✅ | 102.1 ⭐ | 3-4 | Boot process, runlevels |
| Ch03: Filesystems | 101.4 ⭐ | 102.5 ⭐ | 4 | Filesystems, permissions |
| Ch04: Partitions | 101.4 ✅ | — | 4 | Partitioning, LVM |
| Ch05: Permissions | — | 102.5 ✅ | 4 | File permissions, ACLs |
| Ch06: Users | — | 102.2 ✅ | 3 | User/group management |
| Ch07: Processes | — | 102.1 ⭐ | 4 | Process management |
| Ch08-09: I/O, Shell | — | — | — | Scripting support |
| Ch10: System | — | 102.1 ⭐ | 4 | System limits, monitoring |
| Ch11: Network | — | 102.6 ✅ | 4 | Network concepts |
| Ch12: Packages | — | 102.3 ✅ | 3 | Package management |
| Ch13: Kernel | 101.1 ⭐ | 102.1 ⭐ | 4 | Kernel, modules |
| Ch14: Logging | — | 102.1 ✅ | 4 | System logs, monitoring |
| Ch15: Security | — | 102.5, 102.6 ⭐ | 4 | Firewall, security basics |
| Ch16-17: Locale, Env | — | — | — | Configuration mastery |
| Ch18: Exam Block | All 101/102 | All 101/102 | ⭐⭐⭐ | Comprehensive review |
| Ch19: Processors | 101.1, 102.1 ⭐ | — | 2-3 | Advanced process mgmt |
| Ch20: Firewall | — | 102.6 ✅ | 4 | Firewall deep-dive |
| Ch21: Services | 101.3, 102.4 ✅ | — | 3-4 | systemd expertise |
| Ch22: Storage | 101.4 ⭐ | — | 4 | Advanced storage |

**Key:** ✅ = Covers topic, ⭐ = Strong coverage, ⭐⭐⭐ = Best source

---

## 🎯 Study Strategy

### For LPIC-1 101-500 (System Architecture)

**Week 1-2: Hardware & Boot (Topics 101.1-101.3)**
- Play Ch01 (Hardware Basics)
- Play Ch02 (Boot Process)
- Focus on understanding concepts
- Complete all missions before moving on

**Week 3-4: Disk & Filesystems (Topics 101.4, 102.5)**
- Play Ch03 (Filesystems)
- Play Ch04 (Partitions & Disks)
- Play Ch05 (Permissions & Owners)
- Practice partition and filesystem commands

**Exam Prep:**
- Review Ch01-05 + Ch18 (Exam Block)
- Take practice exam (official LPIC resources)
- Get 70%+ on all mission types

---

### For LPIC-1 102-500 (Linux Administration)

**Week 1-2: User Management & Services (Topics 102.2, 102.3, 102.4)**
- Play Ch06 (Users & Groups)
- Play Ch12 (Packages & Repos)
- Play Ch21 (Network Services)
- Focus on practical command mastery

**Week 3-4: Network & Logging (Topics 102.1, 102.6)**
- Play Ch09 (Network)
- Play Ch11 (Logging)
- Play Ch14 (Logging & Monitoring)
- Play Ch20 (Firewall)
- Understand monitoring and troubleshooting

**Exam Prep:**
- Review Ch06-20 + Ch18 (Exam Block)
- Take practice exam (official LPIC resources)
- Get 70%+ on all mission types

---

## 📚 External Resources

**Official LPIC Resources:**
- [Linux Professional Institute](https://www.lpi.org/)
- [LPIC-1 Exam Details](https://www.lpi.org/our-certifications/lpic-1-overview)
- [Exam objectives PDF](https://www.lpi.org/en/our-certifications/lpic-1-exam-102-500-overview)

**Supplementary Study:**
- Linux Academy / A Cloud Guru LPIC-1 courses
- CompTIA Linux+ (similar scope)
- Linux man pages (`man` command in Linux)
- Official distro documentation (Debian, CentOS, Ubuntu)

---

## ✅ Exam Day Tips

1. **Study all chapters first** — Get foundation from NeonGrid-9
2. **Practice with real commands** — Use your own Linux system
3. **Review weak areas** — Revisit chapters you struggled with
4. **Take practice exams** — Identify problem topics
5. **Time management** — 60 questions in 90 minutes ≈ 1.5 min/question
6. **Read carefully** — Some questions have subtle tricks
7. **Process of elimination** — Mark hard questions, come back
8. **Don't overthink** — If you studied, you know this

---

**Good luck on your LPIC-1 journey! NeonGrid-9 provides the foundation. The rest is practice.** 🚀

*— Certification Path Unlocked*
