Title: 流媒体质量控制协议
Date: 2016-09-08 15:36
Modified: 2016-09-08 15:36
Slug: stream-qos
Authors: Joey Huang
Summary: 流媒体质量控制协议
Status: draft

## 为什么需要质量控制

在实时视频流媒体领域，要求带宽充足且稳定。带宽的波动可能造成视频卡顿。

## RTCP 控制方案

[RTCP](https://en.wikipedia.org/wiki/RTP_Control_Protocol) 是在 [RFC3550](https://tools.ietf.org/html/rfc3550) 里随着 RTP 协议里引入的。其目的是把接收端 QoS 信息发送给发送端，发送端根据接收端报告的 QoS 调整输出的 bitrate 。

### RTCP 包含的信息

* 丢包率
* jitter

接收端根据这些信息调整编码器的输出。

### RTCP 发送间隔

根据带宽进行动态计算。简单地讲，就是 session bandwidth 的 5% 用来当 RTCP 。同时还建议了最小值，5s, 2.5s 等。实际上这个规则很复杂，因为要考虑到增大 RTCP 的包频率会占用带宽。ietf 上有个[官方邮件](https://www.ietf.org/mail-archive/web/avt/current/msg15644.html)讨论这个问题。

### RTCP 的不足

RTCP 方案的最大缺点是，**无法分辨出带宽限制和随机丢包**。比如，在 30 fps 情况下，RTCP 报告的丢包率和在 15 fps 情况下报告的差别不大。这个时候输出端就无法做有有效的输出控制。

## SVP

为了解决 RTCP 的问题，[RFC4585](https://tools.ietf.org/html/rfc4585) 定义了一套扩展的方案。

### PLI - Picture Loss Indication

基于 intra-picture/inter-picture 模型。当帧预测链被破坏 (如 i-frame 丢失) ，接收方可以发送 PLI 命令给发送方，发送方重新发上一个 i-frame 给接收方来修复。

#### PLI 命令的发送时机

可以在检测到 i-frame 丢失时发送，也可以待到常规的 RTCP 命令发送时间窗口发送。具体权衡要看整体的性能。

### SLI - Slice Loss Indication

当接收端检测到丢失一个或多个连续的 microblock 时，向发送端发送 SLI 反馈。收到 SLI 反馈后接收端如何处理不在 RFC4585 里讨论，这个是和具体的视频压缩算法相关的。比如，典型地重新发送一个 i-frame 给接收端。

### RPSI - Reference Picture Selection Indication

现代解码算法允许使用更老的帧来作为预测的引用帧，而不仅仅依赖上一帧作为预测基础帧。RPSI 可以让解码码发送预测帧序列中的丢失帧给编码端，从而实现同步。

#### RPSI 命令的发送时机

越老的 RPSI ，编码器构建的代价越大。所以 RPSI 应该尽快发送出去，而不必等到 RTCP 的时间窗口。

## 背景知识

### RTP 协议

RTP 是由 RFC3550 定义的用来做实时流媒体传输的协议。它的特点是：

* 在包头里带有流媒体的格式，时间以及帧序号
* 一个包传输一个流媒体片段，比如 20ms 语音，接收者可以直接播放

[RFC3551](https://tools.ietf.org/html/rfc3551) 定义了不同的音频视频格式使用 RTP 传输数据时的帧格式。这个文档有点老，如果想找新一点的视频格式，比如 H264, V8 等，比如可以搜索 “RTP payload H264”，"rtp payload  V8" 等来找到对应的 RFC 文档。

### IP 多播

RTP 可以使用 [IP 多播](https://en.wikipedia.org/wiki/IP_multicast) 来传输数据。发送端把数据发出去，不管接收者。接收者使用 IGMP 协议向网络说明自己对哪个多播的数据包感兴趣，路由器根据 IGMP 登记的信息进行数据复制和转发。

### microblock

[microblock](https://en.wikipedia.org/wiki/Macroblock) 是视频压缩处理单元。典型地 microblock 包含 16x16 个采样，这些采样可以进一步拆分成传输块 (transform blocks) 或预测块 (prediction blocks)。

### YUV

* Y 代表亮度，指明图片的黑白部分内容。
* U 代表输入信号中红色部分与亮度值的差异。
* V 代表输入信号中蓝色部分与亮度值的差异。

[WikiPedia](https://en.wikipedia.org/wiki/YUV) 上有解释及示例图片。

### Interlaced Video

一种不增加带宽占用的前提下，提高用户帧率感知的技术。其原理是对不同时间的数据进行采样，利用 [Phi phenomenon](https://en.wikipedia.org/wiki/Phi_phenomenon) 原理来增强用户感知的帧率。