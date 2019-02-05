# Install openwrt to Xiaomi R3G

## OpenWrt device page

https://openwrt.org/toh/xiaomi/mir3g

https://openwrt.org/toh/hwdata/xiaomi/xiaomi_miwifi_3g

## OpenWrt quick start

https://openwrt.org/docs/guide-quick-start/start

## OpenWrt user guide

https://openwrt.org/docs/guide-user/start

## OpenWrt 刷机教程

https://www.right.com.cn/FORUM/forum.php?mod=viewthread&tid=262215

## BREED + Netcap 中文教程

https://blog.skk.moe/post/miwifi-r3g-mwan/

## BREED + OpenWrt 中文教程

https://blog.csdn.net/z619193774/article/details/81507917

## OpenWrt GIT 描述的升级步骤及分区信息

https://git.openwrt.org/?p=openwrt/openwrt.git;a=commit;h=f2107fc328ff7f9817fe9ca64f84bba9e32abfc6

ramips: improve Xiaomi Mi Router 3G support

This commit improves support for the Xiaomi Mi Router 3G originally
added in commit 6e283cdc0da25928f8148805ebef7f8f2b769ee8

Improvements:

- Remove software watchdog as hardware watchdog now working as per
  commit 3fbf3ab44f5cebb22e30a4c8681b13341feed6a6 for all mt7621
  devices.

- Reset button polarity corrected - length of press determines reboot
  (short press) vs. reset to defaults (long press) behaviour.

- Enable GPIO amber switch port LEDs on board rear - lit indicates 1Gbit
  link and blink on activity.  Green LEDs driven directly by switch
  indicating any link speed and tx activity.

- USB port power on/off GPIO exposed as 'usbpower'

- Add access to uboot environment settings for checking/setting uboot
  boot order preference from user space.

Changes:

- Front LED indicator is physically made of independent Yellow/Amber,
  Red & Blue LEDs combined via a plastic 'lightpipe' to a front panel
  indicator, hence the colour behaviour is similar to an RGB LED. RGB
  LEDs are not supported at this time because they produce colour results
  that do not then match colour labels, e.g. enabling 'mir3g:red' and
  'mir3g:blue' would result in a purple indicator and we have no such
  label for purple.
  The yellow, red & blue LEDs have been split out as individual yellow,
  red & blue status LEDs, with yellow being the default status LED as
  before and with red's WAN and blue's USB default associations removed.

- Swapped order of vlan interfaces (eth0.1 & eth0.2) to match stock vlan
  layout. eth0.1 is LAN, eth0.2 is WAN

- Add 'lwlll' vlan layout to mt7530 switch driver to prevent packet
  leakage between kernel switch init and uci swconfig

uboot behaviour & system 'recovery'

uboot expects to find bootable kernels at nand addresses 0x200000 &
0x600000 known by uboot as "system 1" and "system 2" respectively.
uboot chooses which system to hand control to based on 3 environment
variables: flag_last_success, flag_try_sys1_failed & flag_try_sys2_failed

last_success represents a preference for a particular system and is set
to 0 for system 1, set to 1 for system 2.  last_success is considered *if*
and only if both try_sys'n'_failed flags are 0 (ie. unset) If *either*
failed flags are set then uboot will attempt to hand control to the
non failed system. If both failed flags are set then uboot will check
the uImage CRC of system 1 and hand control to it if ok.  If the uImage
CRC of system is not ok, uboot will hand control to system 2
irrespective of system 2's uImage CRC.

NOTE: uboot only ever sets failed flags, it *never* clears them. uboot
sets a system's failed flag if that system's was selected for boot but
the uImage CRC is incorrect.

Fortunately with serial console access, uboot provides the ability to
boot an initramfs image transferred via tftp, similarly an image may
be flashed to nand however it will flash to *both* kernels so a backup
of stock kernel image is suggested. Note that the suggested install
procedure below set's system 1's failed flag (stock) thus uboot ignores
the last_success preference and boots LEDE located in system 2.

Considerable thought has gone into whether LEDE should replace both
kernels, only one (and which one) etc. LEDE kernels do not include a
minimal rootfs and thus unlike the stock kernel cannot include a
method of controlling uboot environment variables in the event of
rootfs mount failure. Similarly uboot fails to provide an external
mechanism for indicating boot system failure.

Installation - from stock.

Installation through telnet/ssh:
- copy lede-ramips-mt7621-mir3g-squashfs-kernel1.bin and
  lede-ramips-mt7621-mir3g-squashfs-rootfs0.bin to usb disk or wget it
  from LEDE download site to /tmp
- switch to /extdisks/sda1/ (if copied to USB drive) or to /tmp if
  wgetted from LEDE download site
- run: mtd write lede-ramips-mt7621-mir3g-squashfs-kernel1.bin kernel1
- run: mtd write lede-ramips-mt7621-mir3g-squashfs-rootfs0.bin rootfs0
- run: nvram set flag_try_sys1_failed=1
- run: nvram commit
- run: reboot

Recovery - to stock.

Assuming you used the above installation instructions you will have a
stock kernel image in system 1. If it can be booted then it may be used
to perform a stock firmware recovery, thus erasing LEDE completely. From
a 'working' LEDE state (even failsafe)

Failsafe only:
- run: mount_root
- run: sh /etc/uci-defaults/30_uboot-envtools
Then do the steps for 'All'

All:
- run: fw_setenv flag_try_sys2_failed 1
- run: reboot

The board will reboot into system 1 (stock basic kernel) and wait with
system red light slowly blinking for a FAT formatted usb stick with a
recovery image to be inserted.  Press and hold the reset button for
around 1 second. Status LED will turn yellow during recovery and blue
when recovery complete.

## 研发讨论

https://forum.openwrt.org/t/xiaomi-wifi-router-3g/5377


I’ve updated @hammer instructions with recent findings, @r43k3n could you put these instructions into 1st post?

This is how I got LEDE installed. Some of the steps can be done differently. I used this for inspiration https://www.youtube.com/watch?v=CSHNyo5QxaQ 74

Unbox router
Connect to the router using WiFi
Goto http://192.168.31.1 3

Go through the wizard to set passwords for the router + wifi
Reconnect to the router using WiFi
Goto http://192.168.31.1 3

Logon and find the page where you can upgrade the firmware look for a big yellow dot with an “i” inside. You will see the version number of the router and there is a button below where you can browse for a file. Flash miwifi_r3g_firmware_c2175_2.25.122.bin (developer firmware) and wait a few minutes.
Download https://play.google.com/store/apps/details?id=com.xiaomi.router 11 to your phone/tablet (there is also an iOS app)
Open “Mi Wi-Fi” app (and sign-up) and sign-in to your account. Router will be detected and added to your account (assuming you are connected to the WiFi on the router and the routers WAN port is connected to Internet).
On a PC, visit http://d.miwifi.com/rom/ssh 68 and sign-in to you account. You will get to a page that should display your router, the root password and a download button. Hit the button to get miwifi_ssh.bin
Format USB drive using FAT32 and copy miwifi_ssh.bin, lede-ramips-mt7621-mir3g-squashfs-kernel1.bin and lede-ramips-mt7621-mir3g-squashfs-rootfs0.bin to the USB drive
Cut the power the router, put the USB drive in the router, press and hold “reset” button (with a paper-clip), power on the router (while holding reset). When the router starts flashing yellow release the reset button. Wait until router has rebooted and you should (finally…) have SSH access.
Login to the router using SSH using the “root” as username and the (root) “password” from http://d.miwifi.com/rom/ssh 68

In SSH console

cd /extdisks/sda1 (can be different if you remove and reinsert the usb stick)

mtd write lede-ramips-mt7621-mir3g-squashfs-kernel1.bin kernel1

mtd write lede-ramips-mt7621-mir3g-squashfs-rootfs0.bin rootfs0

nvram set flag_try_sys1_failed=1

nvram commit

reboot
LEDE should be installed and available at 192.168.1.1 (with WiFi disabled I assume)
Upgrading to a newer snapshot can be done using the regular methods (from the command-line using sysupgrade or through LuCI) using lede-ramips-mt7621-mir3g-squashfs-sysupgrade.tar

## 变砖后恢复

https://openwrt.org/toh/xiaomi/mir3g#debricking

https://forum.freifunk.net/t/router-recovery-tftp-pushbutton-und-ttl-serial-recovery/8691

变砖后通过breed恢复

https://forum.openwrt.org/t/xiaomi-3g-mir3g-breed-bootloader-configure-dual-boot-openwrt-pandorabox-padvan/22309/5

## breed

https://forum.openwrt.org/t/xiaomi-wifi-router-3g-18-06-x-feedback-and-help/19840/22

Follow the standard steps till you get SSH in the router.
By default, the router LAN IP should be 192.168.31.1

BACKUP the firmware, if you wish.
It's too long to write here, I assume you know how to do it.

Download the BREED firmware, I got it from
https://breed.hackpascal.net/breed-mt7621-xiaomi-r3g.bin 43
This one is Chinese version, I do't know if there is an English version.

SCP the file breed-mt7621-xiaomi-r3g.bin to the router, I put it into /tmp.

SSH to the router, and execute the command
mtd -r write /tmp/breed-mt7621-xiaomi-r3g.bin Bootloader
After it's done,
reboot

Before the power on, press and hold the reset buttom untill the light blinks stable.
If you didn't do it in time, never mind, just power off, and do it again.
Now you should able to access the BREED interface though browser 192.168.1.1

## Pandorabox and breed

https://forum.openwrt.org/t/xiaomi-wifi-router-3g-18-06-x-wifi-issues-2-4ghz-5ghz/20169/26

I suggest always to go to Stock before chaning to Padvan/OpenWrt/Pandora.
OpenWrt -> Stock -> Pandora

When i was on OpenWrt i first updated the "bootloader" to "breed". This then makes it easy to go to Padvan/OpenWrt/Pandora/Stock. Search the Web for instrunctions on Breed

To update "bootloader" while i was on "OpenWrt" i did as below.
Connect via ssh to the router:

cd /tmp
mtd_write unlock Bootloader
wget --no-check-certificate https://breed.hackpascal.net/breed-mt7621-xiaomi-r3g.bin
mtd_write write breed-mt7621-xiaomi-r3g.bin Bootloader
mtd_write verify breed-mt7621-xiaomi-r3g.bin Bootloader
reboot
If you miss mtd_write then you can:
SSH to the router, and execute the command:

opkg update
opkg install kmod-mtd-rw
insmod mtd-rw i_want_a_brick=1
mtd unlock /dev/mtd0
mtd -r write /tmp/breed-mt7621-xiaomi-r3g.bin Bootloader
reboot
To flash with "Breed":
Before the power on, press and hold the reset buttom until the light blinks stable.
Now you should able to access the BREED interface though browser 192.168.1.1

https://downloads.pangubox.com/pandorabox/18.10/targets/ralink/mt7621/packages/ 90

https://downloads.pangubox.com/pandorabox/18.12/targets/ralink/mt7621/
Ciao
Attaros

dd if=/dev/mtd0 of=/extdisks/sda/miwifi/backup/ALL.bin
dd if=/dev/mtd1 of=/extdisks/sda/miwifi/backup/Bootloader.bin
dd if=/dev/mtd2 of=/extdisks/sda/miwifi/backup/Config.bin
dd if=/dev/mtd3 of=/extdisks/sda/miwifi/backup/Bdata.bin
dd if=/dev/mtd4 of=/extdisks/sda/miwifi/backup/Factory.bin
dd if=/dev/mtd5 of=/extdisks/sda/miwifi/backup/crash.bin
dd if=/dev/mtd6 of=/extdisks/sda/miwifi/backup/crash_syslog.bin
dd if=/dev/mtd7 of=/extdisks/sda/miwifi/backup/reserved0.bin
dd if=/dev/mtd8 of=/extdisks/sda/miwifi/backup/kernel0.bin
dd if=/dev/mtd9 of=/extdisks/sda/miwifi/backup/kernel1.bin
dd if=/dev/mtd10 of=/extdisks/sda/miwifi/backup/rootfs0.bin
dd if=/dev/mtd11 of=/extdisks/sda/miwifi/backup/rootfs1.bin
dd if=/dev/mtd12 of=/extdisks/sda/miwifi/backup/overlay.bin
dd if=/dev/mtd13 of=/extdisks/sda/miwifi/backup/ubi_rootfs.bin
dd if=/dev/mtd14 of=/extdisks/sda/miwifi/backup/data.bin

## 安装 opkg

http://bbs.xiaomi.cn/t-34275260

前提：
1、安装开发者ROM
2、安装SSH
这两步小米路由器都是通用的，这里不讲

一、安装opkg
mkdir -p /userdisk/local/opt
mount -o bind /userdisk/local/opt /opt

cd /userdisk/local
wget http://pkg.entware.net/binaries/mipsel/installer/installer.sh
chmod +x installer.sh
./installer.sh
xxx可以换成自己喜欢的文件夹名。
运行：
export PATH=/opt/sbin:/opt/bin:$PATH
opkg update
opkg install xxxx

二、开机自动mount
不开机自动mount的话，重启后用opkg安装的软件不能正常执行
编辑/etc/rc.local，  vi /etc/rc.local
在exit 0之前加入：
mount -o bind /userdisk/local/opt /opt

三、设置环境变量
不设置环境变量，重启后运行时找不到软件
编辑/etc/profile，  vi /etc/profile
加入：
export PATH=/opt/sbin:/opt/bin:$PATH


## 安装 Transmission

通过 entware 来安装 Transmission

https://github.com/RMerl/asuswrt-merlin/wiki/Installing-Transmission-through-Entware

一些注意事项：

/opt/etc/transmission/settings.json 文件里的 rpc 端口改为 9191，因为 9091 和现有端口冲突，

然后在 rc.local 里添加如下内容，实现自动启动

```
/opt/etc/init.d/S88transmission start
```

修改 S88transmission 加上如下内容实现自动防火墙设置：

```
PRECMD=/opt/bin/firewall-start
```

其中 firewall-start 的内容如下：

```
#!/bin/sh
iptables -I INPUT -p tcp --destination-port 51413 -j ACCEPT
iptables -I INPUT -p udp --destination-port 51413 -j ACCEPT
iptables -I INPUT -p tcp --destination-port 9191 -j ACCEPT
```
