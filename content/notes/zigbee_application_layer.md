Title: ZigBee 应用层详解
Date: 2015-11-14 09:36
Modified: 2015-11-14 09:36
Slug: zigbee-application-layer
Tags: zigbee
Authors: Joey Huang
Summary: ZigBee 应用层详解
Status: draft

# ZigBee 应用层详解

[TOC]

## 发送和接收数据

无线网络的主要目的是为了在网络节点之间可靠地传输数据。Zigbee 网络可以很简便地实现这个目的。在很多平台上，只需要简单地指定节点的地址的要发送的数据，就可以直接发送到目的节点了，中间的过程 ZigBee 网络会自动搞定，比如路由发现之类的。

```c
AF_DataRequest( & addrInfo, iDataSize, pPtrToData, NULL);
```

ZigBee 网络有三种数据相关的操作：

* 数据请求 - 即发送数据，由应用层发起。
* 数据确认 - 即针对发送数据的请求的确认，每一个数据请求都会对应一个唯一的确认信息。
* 数据到达 - 即接收数据，由网络层通知应用层收到其他节点发送过来的数据。

数据请求有几种方式：

* 单播确认 - 目的节点只有一个，且要求有数据确认
* 单播不确认 - 目的节点只有一个，但不要求端到端的数据确认
* 广播 - 发送数据给网络中的所有节点，有三种方式 0xffff 表示所有节点，0xfffd 表示所有没有睡眠的节点，0xfffc 表示所有的路由器
* 组播/多播 - 发送给网络中的一组设备。组播在网络层也是使用广播的机制，只是在应用层会进行过滤，即任何不属于这个组的节点 (endpoint) 会丢弃数据。

ZigBee 是个异步网络，数据在节点传输是有延迟的。一个常用的计算规则是一跳的传输为 10 ms 。比如节点 A 到节点 D 要经过 3 跳，那么可以大概估计需要 30 ms 才能把数据送达，又经过 30 ms 才会有数据确认。但实际情况要比这个复杂，有时网络会会进行重发，这里的延时就跟环境有关系，还有的时候需要发现路由，这时的延时时间就更不确定了。在最后的情况下，网络层会进行 3 次重发，每次间隔 1.5s ，所以在最坏的情况下，需要经过 5s 才能把数据送达。ZigBee 应用层需要支持最坏情况下的网络延时。

ZigBee 应用层实现时，需要注意：

* 在设计基于 ZigBee 的应用层协议时，需要尽量减少数据包的大小。这样可以减少网络传输的时间。但如果是分包传输，比如 ZC 要发送固件对 ZR/ZED 进行在线升级，这个时候需要用尽量大的数据包，以便减小数据包的个数。IEEE 802.15.4 的 MTU 是 127 bytes。
* 尽量减少广播和组播的使用。因为它可能会导致网络风暴，导致网络瘫痪。如果不得己使用，设置好 radius 属性，以便广播在小范围内传输，而不是整个网络。
* ZigBee 空中包的传输是用 Little-Endian 格式的，即权重小的字节在低地址。

## 通用 API

很不幸的是，ZigBee 并没有通用 API。ZigBee 有协议，但协议主要集中在空中包。ZigBee 联盟在测试设备的兼容性时，也只看空中包的兼容性。

目前主流的 ZigBee 芯片厂商有：

* TI：如 CC2530 等。实际上 TI 是在 2006 年收购 ChipCon 公司才进入 ZigBee 行业的。TI 的协议栈名称叫 Z-Stack。
* Ember：是美国 Boston 的一家创业公司。在 2012 年被 Silicon Labs 收购。Silicon Labs 在 2008 年还收购了 Integration Associates ，这也是一家做 ZigBee 的技术公司。
* Freescale：这是另外一家做 ZigBee 的公司。协议栈名称民 BeeStack。

## ZigBee 网络

ZigBee 网络又称为 ZigBee Personal Area Network (PAN)。本节讨论 ZigBee PAN 的几个属性，PAN IDs, extended PAN IDs, 信道。ZigBee 网络只能由 ZC 设备创建，ZR/ZED 只能加入网络。



