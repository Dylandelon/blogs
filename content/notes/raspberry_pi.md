Title: Raspberry Pi
Date: 2018-12-29 14:36
Modified: 2018-12-29 14:36
Slug: raspberry
Authors: Joey Huang
Summary: Raspberry Pi Notes
Status: draft

# Raspberry Pi 笔记

## 软件源镜像

https://blog.csdn.net/nobmr/article/details/52607666

Raspbian http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/

编辑/etc/apt/sources.list文件。删除原文件所有内容，用以下内容取代：

deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ wheezy main non-free contrib

deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ wheezy main non-free contrib

编辑此文件后，请使用sudo apt-get update命令，更新软件列表。

## Transmission

https://www.jianshu.com/p/9dac4772cc72

修改配置文件：

```
sudo vim /etc/transmission-daemon/settings.json
```

重启服务：

```
sudo service transmission-daemon reload
```

## Samba

https://oshlab.com/setting-samba-raspberry-pi/

修改完 `/etc/samba/smb.conf` 后，重启 samba：

```
sudo update-rc.d smbd enable
sudo update-rc.d nmbd enable
sudo service smbd restart
```

## VNC

开启：https://baijiahao.baidu.com/s?id=1606207693709103859&wfr=spider&for=pc
分辨率：https://softsolder.com/2016/12/23/raspberry-pi-forcing-vnc-display-resolution/

开启 VNC 服务，只需要开启一次即可。远程配置树莓派的指令为 `sudo raspi-config`，在终端/运行中键入以上指令后选择5 Interfacing Options。然后启用 VNC 即可。

然后，每次要访问之前，需要用 ssh 登录 raspberry pi 设备，输入 `vncserver` 启动 VNC 服务。

## 虚拟键盘

使用 `sudo apt-get install matchbox-keyboard` 安装虚拟键盘。安装完如果 `keyboard` 没有出现在 `Accessories` 菜单里，试试下面的命令：

`sudo cp /usr/share/applications/inputmethods/matchbox-keyboard.desktop /usr/share/applications/`

然后，在图形界面下打开 Terminal，输出如下命令 `lxpanelctl restart`。再来检查 `Accessories` 是否出现 `keyboard` 菜单项。如果此时出现了 2 个 `keyboard` 菜单项，则使用 `sudo rm /usr/share/applications/matchbox-keyboard.desktop` 删除掉拷贝的文件，再次运行 `lxpanelctl restart` 即可。

## 开机自动执行脚本

```
sudo vim /etc/rc.local
sudo chmod +x /etc/rc.local
```

## WiFi 配置

https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
https://www.digikey.com/en/maker/blogs/raspberry-pi-3---how-to-connect-wi-fi-and-bluetooth

Open the wpa-supplicant configuration file in nano:

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

Go to the bottom of the file and add the following:

```
network={
    ssid="testing"
    psk="testingPassword"
}
```

## 启用 WebGL

https://www.raspberrypi.org/forums/viewtopic.php?t=191087

要在浏览器下运行诸如 Scratch 3.0 这样的程序时，需要启用 WebGL 才行。方法如下：

1. use raspi-config to enable OpenGL (Full KMS)
2. remove "--disable-gpu-compositing'' from /etc/chromium-browser/customizations/00-rpi-var

这样，打开 Chromium 浏览器，打开 `get.webgl.org` ，如果出现一个转动的正方形，则说明 WebGL 已经正确打开。

打开 WebGL 有几个注意事项：

1. 一定要在外接显示器上操作，不要用 vnc 之类的远程桌面上操作。因为远程桌面上操作时，用的 glx 版本过低，导致 Chromium 无法打开 WebGL。方法是，在远程桌面上打开命令行，输入 `glxinfo` 命令即可看到 glx 的版本。
2. 打开 WebGL 后，要用 raspi-config 里，推荐给 GPU 分配 256MB 的内存
3. 可以在 Chromium 浏览器里输入 `chrome://gpu/` 查看 gpu 信息

## Todo

1. 启用 dotfile ，让 bash 更友好


## Know Issues

1. volume was not unmounted cleanly
2. 移动硬盘会自动挂载到 /media/pi 目录？
    * https://retroresolution.com/2016/06/10/automatically-mounting-an-external-usb-hard-disk-on-the-raspberry-pi/#li_background

