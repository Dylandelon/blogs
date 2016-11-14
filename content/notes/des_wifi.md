Title: DES WiFi
Date: 2016-09-23 15:36
Modified: 2016-09-23 15:36
Slug: des-wifi
Authors: Joey Huang
Summary: DES WiFi 所有信息
Status: draft

## Wi-Fi Extender

### 配置方式

1. WPS 配置方式
2. 网页配置方式

### 配置后的 SSID 名称

1. 与原 Router 一致，包括 SSID 和密码 (TP-Link)
2. 名称为原 Router 的 SSID 加上后缀 "_EXT" 组成，密码一致 (TP-Link/NETGEAR)
3. 用户可以自己修改方案 (NETGEAR)

### 技术方案

#### WISP 方案

WISP

#### WDS 方案

WDS 的兼容性无法保证。

> WDS may be incompatible between different products (even occasionally from the same vendor) since the IEEE 802.11-1999 standard does not define how to construct any such implementations or how stations interact to arrange for exchanging frames of this format. The IEEE 802.11-1999 standard merely defines the 4-address frame format that makes it possible. - https://en.wikipedia.org/wiki/Wireless_distribution_system

WDS 网域中的设备处于同一个局域网。WDS 中转设备需要关闭 DHCP 功能。

### 杂项

#### 国家/地区设置

[TP-Link N300 Wi-Fi Range Extender - TL-WA850RE](https://www.amazon.com/TP-Link-Wi-Fi-Range-Extender-TL-WA850RE/dp/B00E98O7GC/ref=sr_1_5?s=pc&ie=UTF8&qid=1474618374&sr=1-5&keywords=WiFi+extender) 的 [user manual](https://images-na.ssl-images-amazon.com/images/I/A1dnoE9DPcS.pdf) 里写着可以设置国家？

#### UPNP

DesAP 各个网口上都会实现 UNPN 协议，通过广播让别的设备发现 DesAP 设备。

#### DHCP

当监测到家庭网络的网口 IP 地址改变，则检查 IS 网络和 PLC 网络的地址，如果有冲突，则需要改变 DHCP 地址池，然后通过一定的机制让 IS 和 PLC 网络里的设备来重新获取 IP 地址。

通知的机制可选如下：

1) 应用层私有协议 -> 通过广播发送。问题：Repeater 不会转发这个广播，且也不会重新发 DHCP 命令重新申请 IP 地址。
2) 利用 DHCP 续租时长，来周期性地继租 IP 地址，比如设置为 10 分钟。
3) 断网。 ifconfig wlan0 down / ifconfig wlan0 up 。在应用层实现，发现断网后，重新发送 DHCP 请求。

如何解决 WiFi Repeater 子网里的设备？

## WiFi DFS

### 给 WiFi 使用的有哪些 5G 频道？

CHANNEL | FREQUENCY | EUROPE (ETSI) | US (FCC) | JAPAN
--------|-----------|---------------|----------|---------------------
36  | 5180  |  Indoors                    | OK                  | OK
40  | 5200  |  Indoors                    | OK                  | OK
44  | 5220  |  Indoors                    | OK                  | OK
48  | 5240  |  Indoors                    | OK                  | OK
52  | 5260  |  Indoors / DFS / TPC        | DFS                 | DFS / TPC
56  | 5280  |  Indoors / DFS / TPC        | DFS                 | DFS / TPC
60  | 5300  |  Indoors / DFS / TPC        | DFS                 | DFS / TPC
64  | 5320  |  Indoors / DFS / TPC        | DFS                 | DFS / TPC
100 | 5500  |  DFS / TPC                  | DFS                 | DFS / TPC
104 | 5520  |  DFS / TPC                  | DFS                 | DFS / TPC
108 | 5540  |  DFS / TPC                  | DFS                 | DFS / TPC
112 | 5560  |  DFS / TPC                  | DFS                 | DFS / TPC
116 | 5580  |  DFS / TPC                  | DFS                 | DFS / TPC
120 | 5600  |  DFS / TPC                  | No Access           | DFS / TPC
124 | 5620  |  DFS / TPC                  | No Access           | DFS / TPC
128 | 5640  |  DFS / TPC                  | No Access           | DFS / TPC
132 | 5660  |  DFS / TPC                  | DFS                 | DFS / TPC
136 | 5680  |  DFS / TPC                  | DFS                 | DFS / TPC
140 | 5700  |  DFS / TPC                  | DFS                 | DFS / TPC
149 | 5745  |  SRD                        | OK                  | No Access
153 | 5765  |  SRD                        | OK                  | No Access
157 | 5785  |  SRD                        | OK                  | No Access
161 | 5805  |  SRD                        | OK                  | No Access
165 | 5825  |  SRD                        | OK                  | No Access

以欧洲为例，非 DFS 与 DFS 频道数大概是 9: 15。这个数字每个国家会有稍微不同。

来源：http://www.radio-electronics.com/info/wireless/wi-fi/80211-channels-number-frequencies-bandwidth.php

![5G Channels](../../images/wifi_5G_bands.png)

### 启用 DFS 的影响

* 需要做 DFS 认证
* 设备开机时**有可能**在 10 分钟的时间客户端无法扫描到 AP ，因为这段时间 AP 需要进行雷达频道扫描
* 使用 DFS 频道的过程中，AP 会持续检测雷达信号，如果检测到雷达信号，会进行频道切换，这会造成客户端连接中断一小段时间，之后客户端会自动连接上。

来源：http://www.tp-link.com/en/faq-763.html

禁用 DFS 频道是个较普遍的现象。不少厂商会决定不使用 DFS 频道。

来源：http://superuser.com/questions/692835/which-5ghz-channel-to-use/692837

### 禁用 DFS 的影响

* 可用频道变少
* 如果启用自动选择频道，则在 802.11n 下可用频道将变得更少

以德国为例，自动选择的可选频道为：36, 40, 44, 48, 52, 56, 60, 64 ，其中 52, 56, 60, 64 为 DFS 频道。如果禁用 DFS ，则只剩下 36, 40, 44, 48 四个自动可选频道，以及 149, 153, 157, 161, 165 五个手动选择的频道。

关于配置 802.11n 工作模式的自动可选频道相关的 `hostapd.conf` 配置项如下：

```text
# ht_capab: HT capabilities (list of flags)
# LDPC coding capability: [LDPC] = supported
# Supported channel width set: [HT40-] = both 20 MHz and 40 MHz with secondary
#   channel below the primary channel; [HT40+] = both 20 MHz and 40 MHz
#   with secondary channel above the primary channel
#   (20 MHz only if neither is set)
#   Note: There are limits on which channels can be used with HT40- and
#   HT40+. Following table shows the channels that may be available for
#   HT40- and HT40+ use per IEEE 802.11n Annex J:
#   freq        HT40-       HT40+
#   2.4 GHz     5-13        1-7 (1-9 in Europe/Japan)
#   5 GHz       40,48,56,64 36,44,52,60
#   (depending on the location, not all of these channels may be available
#   for use)
#   Please note that 40 MHz channels may switch their primary and secondary
#   channels if needed or creation of 40 MHz channel maybe rejected based
#   on overlapping BSSes. These changes are done automatically when hostapd
#   is setting up the 40 MHz channel.
# Spatial Multiplexing (SM) Power Save: [SMPS-STATIC] or [SMPS-DYNAMIC]
#   (SMPS disabled if neither is set)
# HT-greenfield: [GF] (disabled if not set)
# Short GI for 20 MHz: [SHORT-GI-20] (disabled if not set)
# Short GI for 40 MHz: [SHORT-GI-40] (disabled if not set)
# Tx STBC: [TX-STBC] (disabled if not set)
# Rx STBC: [RX-STBC1] (one spatial stream), [RX-STBC12] (one or two spatial
#   streams), or [RX-STBC123] (one, two, or three spatial streams); Rx STBC
#   disabled if none of these set
# HT-delayed Block Ack: [DELAYED-BA] (disabled if not set)
# Maximum A-MSDU length: [MAX-AMSDU-7935] for 7935 octets (3839 octets if not
#   set)
# DSSS/CCK Mode in 40 MHz: [DSSS_CCK-40] = allowed (not allowed if not set)
# 40 MHz intolerant [40-INTOLERANT] (not advertised if not set)
# L-SIG TXOP protection support: [LSIG-TXOP-PROT] (disabled if not set)
#ht_capab=[HT40-][SHORT-GI-20][SHORT-GI-40]
```

### 如何自动选择非 DFS 频道

可以通过配置 `hostapd.conf` 来实现。

* 需要开启自动选择频道的功能
* 设置 `acs_whitelist` 变量，标识出允许选择的频道列表
* 可以通过配置 ACS 算法来优先选择某些频道

下面是从 `hostapd.conf` 里摘抄出来涉及到的设置项。

```text
# Automatic channel selection (ACS) whitelist
# (default: not set)
# Allow only these channels in automatic channel selection
acs_whitelist=1 2 3 4 5 6 7 8 9 10 11 36 40 44 48 149 153 157 161 165
```

### 把需要手动选择的频道加入自动选择频道列表

可以通过配置黑白名单的方式把 149 153 157 161 165 频道配置进频道列表白名单，针对欧洲国家，可以按照下面的方式来配置。

```text
# Automatic channel selection (ACS) whitelist
# (default: not set)
# Allow only these channels in automatic channel selection
acs_whitelist=1 2 3 4 5 6 7 8 9 10 11 36 40 44 48 149 153 157 161 165
```
