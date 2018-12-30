Title: Raspberry Pi
Date: 2018-12-29 14:36
Modified: 2018-12-29 14:36
Slug: raspberry
Authors: Joey Huang
Summary: Raspberry Pi Notes
Status: draft

# Raspberry Pi 笔记

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

## 虚拟键盘

使用 `sudo apt-get install matchbox-keyboard` 安装虚拟键盘。安装完如果 `keyboard` 没有出现在 `Accessories` 菜单里，试试下面的命令：

`sudo cp /usr/share/applications/inputmethods/matchbox-keyboard.desktop /usr/share/applications/`

然后，在图形界面下打开 Terminal，输出如下命令 `lxpanelctl restart`。再来检查 `Accessories` 是否出现 `keyboard` 菜单项。如果此时出现了 2 个 `keyboard` 菜单项，则使用 `sudo rm /usr/share/applications/matchbox-keyboard.desktop` 删除掉拷贝的文件，再次运行 `lxpanelctl restart` 即可。

## 开机自动执行脚本

```
sudo vim /etc/rc.local
sudo chmod +x /etc/rc.local
```

## Todo

1. 启用 dotfile ，让 bash 更友好


## Know Issues

1. volume was not unmounted cleanly
2. 移动硬盘会自动挂载到 /media/pi 目录？
    * https://retroresolution.com/2016/06/10/automatically-mounting-an-external-usb-hard-disk-on-the-raspberry-pi/#li_background

