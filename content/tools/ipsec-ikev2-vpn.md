Title: step-by-step 构建 IPSec/IKEv2 VPN
Date: 2016-11-01 23:22
Modified: 2016-11-01 23:22
Tags: tools
Slug: ipsec-ikev2-vpn
Authors: Joey Huang
Summary: 升级到 iOS 10 和 macOS Sierra 后，安全性较差的 pptp vpn 服务器不能再使用了。那就搭个 IPSec/IKEv2 VPN 服务器吧。

> 升级到 iOS 10 和 macOS Sierra 后，发现原来的 pptp vpn 没了。那是因为 Apple 因为安全原因，禁用的 pptp vpn ，这里可以查阅到 [Apple 官方声明](https://support.apple.com/en-us/HT206844)。你需要搭建一个支持 IPSec/IKEv2 的 VPN 服务器。本文使用 AWS 的 Ubuntu 服务器搭建一个支持 IPSec/IKEv2 的 VPN 服务器。

## 写在前面

你需要一个 AWS Ubuntu 服务器。国内访问的话，建议申请日本的服务器，速度最快。如果不知道怎么申请 AWS 服务器，请用 Baidu Google 一下。

搭建支持 IPSec/IKEv2 的 VPN 服务器总共分几步：

* 你需要有一台运行 ubuntu 的海外主机，本文使用 aws ubuntu 主机
* 在 AWS ubuntu 主机上运行一个脚本安装并配置 VPN 服务器
* 启动 VPN 服务
* 客户端配置 VPN

本文重点描述后面三个步骤。

## 安装并配置 VPN 服务器

这本来是一个很繁琐的步骤，具体可参阅 [使用 Strongswan 搭建 IPSec/IKEv2 VPN](https://hjc.im/shi-yong-strongswanda-jian-ipsecikev2-vpn/)。有心人把文章里描述的步骤写了个 [shell 脚本](https://github.com/magic282/One-Key-L2TP-IKEV2-Setup)并放在了 github 上。这样我们执行脚本即可完成软件安装以及配置工作。

### STEP 1 下载脚本

使用 ssh 登录 aws ubuntu 主机，执行下面命令下载脚本：

```shell
$ wget https://raw.githubusercontent.com/magic282/One-Key-L2TP-IKEV2-Setup/master/l2tp_setup.sh
```

### STEP 2 添加可执行权限

```shell
$ chmod a+x l2tp_setup.sh
```

### STEP 3 安装软件

运行脚本，需要注意，需要使用 root 用户运行这个脚本。

```shell
$ sudo ./l2tp_setup.sh
```

出现下面的提示时，输入 1

```
"#################################"
"What do you want to do:"
"1) Install l2tp"
"2) Add an account"
"#################################"
```

出现下面的提示时，输入 PSK 密码，**这个密码后面客户端登录时要用到**，注意保管好：

```shell
Please set the secretkey(Pre Shared Key):
```

出现下面提示时，输入 2

```
"##################"
"What type is your VPS?"
"1) OpenVZ"
"2) others"
##################"
```

**特别注意**：这里需要确认一下你的主机是 OpenVZ 还是其他，如 xen 。然后做出相应的选择。一个简单的方法是运行 `ls /proc | grep vz` ，如果输出 `vz` 就选择 1，否则就选择 2。针对 AWS 上的 ubuntu 选择 2 即可。

接下来，脚本会下载 Strongswan 软件包，并编译安装。过程可能要几分钟时间。如果没有错误的话，脚本接着会输出如下内容：

```shell
##################
Please set a password to export the key
##################
Enter Export Password:
Verifying - Enter Export Password:
```

可以直接按两个回车，即使用空的密钥导出密码。不出意外的话，最终会安装成功，并输出下面的成功信息：

```shell
################################################
Success!
Use this to connect your L2TP service.
IP: xxx.xxx.xxx.xxx (你的虚拟主机的 IP 地址)
Secretkey: xxxxxx (你的 PSK 密码)
CA cert: /root/l2tpInstall/ca.cert.pem
Don't forget to add a new user later, LOL.
################################################
```

### STEP 4 添加用户

运行脚本

```shell
$ sudo ./l2tp_setup.sh
```

出现下面的提示时，输入 2

```
"#################################"
"What do you want to do:"
"1) Install l2tp"
"2) Add an account"
"#################################"
```

接着在相应的提示下输入用户名和密码：

```shell
Please input an new username:
<在这里输入用户名>
Please input the password:
<在这里输入密码>
```

这样就成功添加了一个用户。我们可以在客户端使用这个用户和密码以及 PSK 来登录了。

### STEP 5 配置数据包转发

编辑 `/etc/sysctl.conf`，将 `net.ipv4.ip_forward=1` 一行前面的 `#` 号去掉，保存后执行 `sysctl -p`。

## 启动 VPN 服务

这一步不注意就会漏掉，如果漏掉这一步，不会有出错信息，但客户端就是连接不上。即，我们需要手动启动 VPN 服务：

```shell
sudo ipsec start
```

可以使用 `ps` 命令确认服务是否正常运行起来了

```shell
$ ps -ax | grep ipsec
 1861 ?        Ss     0:00 /usr/local/libexec/ipsec/starter --daemon charon
 1862 ?        Ssl    0:00 /usr/local/libexec/ipsec/charon --use-syslog
```

## 客户端配置 VPN

在 macOS 上，新建一个 VPN，`VPN Type` 选择 `Cisco IPSec`。输入 VPN 服务器地址或域名，以及用户名和密码 (STEP 4 里添加的用户名和密码)。点击 `Authentication Settings ...` ，在弹出的窗口里的 `Shared Secret` 里输出 PSK (STEP 3 里设置的密码)。这样就可以上网了。

在 iOS 上，进入 `设置 -> 通用 -> VPN -> 添加 VPN 配置...`，类型选择 `IPSec`，输入用户名密码以及 PSK 即可完成配置。

## 尽情冲浪吧~~~
