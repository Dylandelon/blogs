Title: Global IP 技术方案汇总
Date: 2016-11-04 15:36
Modified: 2016-11-04 15:36
Slug: global-ip-solution
Tags: des
Authors: Joey Huang
Summary: Global IP 方案汇总
Status: draft

[TOC]

## App

使用 Welcome App 3.0 作为基线来开发。变更的技术方案如下：

### 推送方案

原方案：通过 SIP Server 发送推送通知，通过 SIP Message 来实现。
新方案：通过 Portal 服务器，通过 websocket/socket 发送 JSON 消息来实现。

变更原因：我们想把推送方案从 SIP 服务器切换到 Portal 服务器。与 Free@Home 方案保持一致。

适用场景：门铃/重复振铃/报警信息

### 双向通信机制

原方案：通过 SIP Message 来实现。
新方案：通过 Portal 服务器，通过 websocket/socket 发送 JSON 消息来实现。

变更原因：之前双向通信和推送都是用 SIP Message，这样会导致双向通信时，IPGW 回复的应答消息被当成推送发给所有的 App。最终导致最终用户会看到奇怪的推送消息。

适用场景：开灯/开锁/抓拍/SOS/切换门口机摄像头/获取通话时长

### 远程和本地的通信机制

当 DesAP 检测到需要发送推送消息时（门铃/重复振铃/报警信息），下面几个信息需要考虑：

1. 通过 websocket 发送推送请求给 portal 服务器。Portal 服务器判断 App 是否在线，如果在线，则直接通过 websocket 发送实时的 JSON 消息给 App。如果不在线，则通过 APNs/GCM 发送推送给 App。
2. 给工作在本地模式的 App ，通过 socket 长连接直接发送 JSON 消息。
3. 当 App 和 DesAP 通过局域网工作在本地模式时，App 需要向 Portal 服务器发送注销消息，这样确保不会收到 Portal 的推送以及实时消息。

当 App 和 DesAP 进行双向通信时（开灯/开锁/抓拍/SOS/切换门口机摄像头/获取通话时长），App 和 DesAP 直接通过 websocket/socket 的长连接上交互 JSON 数据包实现实时双向通信。

### 变更对其他设备的影响

#### DesAP

1. 需要实现基于 tcp 的长连接服务器。用来和 App 在本地时进行双向通信。
2. 原来通过 SIP Message 的双向交互需要替换为基于 tcp 长连接的 JSON 消息双向交互。
3. 原来通过 SIP Message 发起推送的机制需要变更为通过 websocket 发送 JSON 消息来发起推送。

#### Portal Server

1. 提供基于 websocket 长连接的推送接口
2. 提供基于 websocket 的双向通信接口

### 需要澄清的问题

1. Portal Server 只提供基于 websocket 的长连接，还是也有提供基于 tcp 的长连接？
2. 维护长连接的心跳包频率是多长？

## DesAP

* 平台基于 I.MX6
* 基于 IPGW DM365 平台，很多基础功能从 IPGW 上移植过来 -> Nancy

### PLC 配置以及两线组网

* PLC 直接贴在主板上，留出 SPI FLASH 接口，用顶针顶上去烧写软件
* PLC 接口设计：设置频段，工作模式设置，组网，退网。接口方式是 MII。AR7420。

通过人为按一下 OS 上组网按钮，然后再按一下 DesAP 上的组网按钮，即可实现组网。DesAP 上的组网按钮只有在安全按钮拨向关闭状态时才允许 PLC 设备组网。

#### 需要澄清的问题

1. PLC 设备上我们需要开发代码么？
A: 不需要开发代码

2. OS 和 DesAP 上和有一个 PLC 芯片，我们是直接用芯片还是用第三方生产的模块？
A: 直接使用芯片

3. 软件计划上的各个任务具体内容是什么？
A: 己沟通

### Wi-Fi 驱动以及组网

确保驱动正确运行后，通过 hostapd 实现 SoftAP。通过 wpa_supplicant 实现 Station。

#### SoftAP 功能

通过配置 hostapd.conf ，并在开机时自动运行 hostapd 来实现。需要关注的几个配置项：

1. SSID 名称，如 ssid=DesAP-XXXX，其中 XXXX 为 MAC 地址后四位
2. 工作模式，如 hw_mode=a 表示 5G，hw_mode=g 表示 2.4G
3. 国家码，如 country_code=CN 表示中国。国家码如何设置需要讨论具体方案
4. 工作频段，如 channel=0 表示自动选择频段，也可以人为设置特定的频段，如 channel=11
5. 80211n，我们需要打开 802.11n 以便让 AP 获得更大的带宽吞吐量
    * ht_capab=[HT40-][SHORT-GI-20][SHORT-GI-40]
    * ieee80211n=1
    * hw_mode=a
    * 设置 channel=64（这个不能乱设，频段有规定）; 或设置成 0 自动选择
6. 开启 DFS 功能，ieee80211d=1；ieee80211h=1

#### Station 功能

通过 wpa_supplicant 来连接家庭 WiFi 热点。

#### Bandwidth 自动测试及频段自动选择

前提：用户先进行配置，让 IS 连接到 DesAP 上。

通过交叉编译 iperf 并集成在 DesAP 和 IS 上实现带宽的自动测试。先让用户配置 DesAP 连接到家庭网络，从而确认家庭网络的频段 (2.4G or 5G)。然后启用 DesAP 的 SoftAP，让 IS 连接到 DesAP 上。开始测试带宽。测试完成后，DesAP 更换一个频段，继续测试带宽。然后建议用户选择最佳带宽的 DesAP SoftAP 配置。

#### WPS

通过配置 hostapd 来实现。具体方案需要研究 hostapd.conf 来实现。

DesAP 上有两个 WPS 按键：

* 实体按键：给 AP 模式使用，让 IS 连接上来
* 软按键：作为 Station 去连接家庭网络。需要打开 DesAP Web 页面操作。
* IS 上的 WPS 按键: IS 上也使用 WPS 软按键实现。
* DesAP: 提供自适应的 Web 配置页面，App 通过 WebView 直接访问并设置 DesAP

### DHCP

DesAP 有三个网口，一个作为 Station 连接到家里的 WiFi 热点。另外一个作为 AP 连接所有的 IS 设备；还有一个作为 PLC 网络接口连接 OS 设备。除了作为 Station 的网络接口外，其他两个网络接口 DesAP 都需要有一个 DHCP 服务器。主要需要实现如下功能：

1. 给 IS 设备分配 IP 地址
2. 给 OS 设备分配 IP 地址
3. 监控 Station 端的 IP 地址，确保这三个网段网络地址不冲突

DHCP 需要实现以下功能：

1. DHCP 地址池更改方案（当检测到地址冲突时，如何修改 DHCP 地址池，以及如何通知现有设备重新获取 IP 地址）
2. IP 数据包转发策略，通过设置每个网口的路由表来实现。这样可以让 DesAP 三个不同网口上的设备可以直接通信。

具体方案 Hack 有详细的文档描述。

### DNS

DesAP 需要实现 DNS 服务，以便可以通过一个简单易记的短网址，访问到 DesAP 的 web 配置界面。

### SIP 服务器

大部分沿用 IPGW 上的 flexsip 服务器方案。需要评估三个网口以及 IP Camera 发现及视频转发机制的影响。

### 视频转发以及码流控制

增加的功能点是码流控制，通过 RTCP 监控视频和音频的时延情况，根据时延情况动态调整 OS 设备的帧率以及码率。

这个工作应该在 IS 和 OS 两个设备上开发，如果多台 IS ，有些信号好，有些信号不好。则会全部变成低质量的视频传输。

### 手机，远程控制，远程通话相关功能

与原来的 IPGW 相比，需要增加的功能包含：

1. 实现 websocket 客户端，和 portal 服务器对接
2. 实现 tcp 服务器，实现与 App 在本地同局域网时的交互

这个工作的具体信息可参阅 App 的变更。

### XMPP client

需要在 DesAP 上实现 XMPP 客户端，以便与 Free@Home 对接。BJE 已经发了 Free@Home 的相差接口文档和 SDK 库。可以直接参考使用。

### Salto

需求及技术方案如何？

* 与Salto application的接口设计
* GSM接口
* 与cloud server的接口设计
* Salto appliation的移植

### RISCO

需求及技术方案如何？

* 与RISCO的接口设计
* 与cloud server的接口设计

### Onvif IPCAM

* 前期方案：onvif 先由 DesAP 模块成主机设备，发 I 帧来实现监控
* 正式方案：使用 P2P + onvif 方案 -> 和 Tobias 达成方案可行性的一致

* 设备搜索
* 设备管理
* 本地监视以及IP转发方案
* 远程监视方案

### Web server

基于 TLS/SSL 安全机制

* CGI 接口设计 -> 配置，给 Browser (App/Desktop)
* RESTFUL 接口设计 -> 给 IS 用的配置接口
* Native Socket (TCP/UDP?) Server -> 本地双向通信

计划重新排一下，目前的计划时间太短

### Web前端设计

外包来完成。但需要实现 PC 端和 Mobile 端兼容的前端设计和开发。

### 设备管理

* 设备搜索
* 设备注册
* 设备认证绑定
* 设备解绑

Frank 的设备发现，组网与安全的设计文档里有详细的方案。

### 用户管理

暂时先不做，沿用 IPGW 的方案。

### 自动测试以及软件测试模式

白盒 + 老化测试 的自动测试系统。

### 固件升级

通过上传到 Web 界面完成固件升级。沿用 IPGW 功能。
