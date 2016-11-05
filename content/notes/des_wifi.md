Title: DES WiFi
Date: 2016-09-23 15:36
Modified: 2016-09-23 15:36
Slug: des-wifi
Authors: Joey Huang
Summary: 流媒体质量控制协议
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