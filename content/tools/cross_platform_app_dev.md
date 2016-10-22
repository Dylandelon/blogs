Title: 跨平台 App 开发技术方案汇总
Date: 2016-10-23 01:13
Modified: 2016-10-23 01:13
Tags: tools
Slug: cross-platform-app-dev
Authors: Joey Huang
Summary: 跨平台 App 开发有哪些技术方案，各有哪些优缺点？是否需要从原生 App 开发切换到这些跨平台的方案上来？切换过去能节省多少工作量？

## Hybrid 技术

这类技术，使用 HTML/CSS/JavaScript 等前端技术来构建 App。利用 JSBridge 获取部分访问原生 API 的能力。最有代表性的是 [PhoneGap](http://phonegap.com)，它是 Adobe 收购一家开源创业公司后推出的平台。[这个链接](http://blog.ionic.io/what-is-cordova-phonegap/)有 PhoneGap 的一些历史信息。

这类平台的目标是保持大部分代码跨平台共用，涉及到平台不共用的 API （比如 GPS 接口，iOS 和 Android 肯定是不一样的），则由 PhoneGap 平台通过 JSBridge 提供。除此之外，还有一些明显的优点：

* 开发效率较高：使用 HTML/CSS/JavaScript 构建界面的效率要比原生 App 速度快很多。而且前端开发有一堆现成的框架和开源库可以直接使用。
* 即时更新：有 Bug 可以快速更新，不需要发布新 App，只需要更新服务器上更新相关的 HTML/CSS/JavaScript 即可。可以绕过 AppStore 的上架认证时间。
* 开发门槛低：对于前端开发工程师，可以快速转岗，开发出可用的 App，不需要对 iOS 平台和 Android 平台有太深入的了解。

这类平台的硬伤是：

* 单线程：JavaScript 在 WebView 里执行时是单线程的。对系统并发能力有较大的影响。
* 性能低：大概只能达到原生 App 70% 的流畅度。

[这篇文章](http://blog.csdn.net/pzhtpf/article/details/25326397)对几个热门的 Hybrid 平台进行了对比和介绍。

为了克服 Hybrid 的缺点，目前工程应用上典型的做法是，以原生 App 为主，把易变的逻辑，以及界面，不涉及性能瓶颈的部分使用基于 WebView 的 Hybrid 技术来开发。

## 准原生平台

为了解决 Hybrid 的问题，一些其他的方案逐步流行起来，最火的要算 [React-Native](https://facebook.github.io/react-native/)，它是 Facebook 基于其前端框架 [React](https://facebook.github.io/react/index.html) 之上构建的跨平台 App 开发构架。

这类平台的特点是，只使用 JavaScript 来构建界面，但实际上构建出来的所有界面都是系统原生控件。这是和 Hybrid 平台最大的区别。在 Hybrid 平台，一个按钮就是 HTML 构建出来的，但在 React-Native 平台，一个按钮是在各自的平台 (Android/iOS) 上以原生控件的形式渲染出来的。

这类平台最大的优势是：

* 跨平台开发界面及业务逻辑：以前端工程师熟悉的构架和技术，以一致的方式构建界面和业务逻辑。
* 即时更新：可以把业务逻辑放在 JavaScript 里，这样就可以直接在线更新功能。
* 性能较高：比 Hybrid 性能高，大概能达到原生 App 90% 的流畅度。
* 开发效率较高：可以使用前端技术快速构建界面。比如，熟悉 React 框架的人，可以无障碍地在 React-Native 下构建界面和业务逻辑。

这类平台和 Hybrid 相比，跟原生平台靠得更近一些，更多地依赖原生平台的一些知识。比如，很多机制，其实还是要分 iOS 平台和 Android 平台的。即无法做到真正的跨平台开发，在利用 React-Native 这类构架时，还是需要对目标平台有较深入的理解。

除了 React-Native 之外，比较著名的还有 [Weex](http://alibaba.github.io/weex/) 这是 alibaba 出品的一个构架，它是基于最近火热的前端构架 Vue.js 的。另外一个是 [NativeScript](https://www.nativescript.org/)，这是基于老牌的前端构架 Angular
之上构建的。

大家注意到，这些热门平台都是基于一个热门的前端构架来构建的。从这一点也可以看到这种类型的构架的目标，就是**让前端开发人员可以在其原有知识体系里，快速开发 App ，并且使用自己熟悉的语言 JavaScript 来处理业务逻辑**。至于核心的代码以及性能相关的代码，还是需要使用原生编程语言 (OC for iOS, Java for Android) 来编写，不同的平台最终向上层提供一致接口。这样，上面界面部分代码，甚至一些逻辑代码就可以跨平台共用了。

原理上，JavaScript 怎么样和原生平台交互呢？

JavaScript 是脚本语言，可以在运行时解释并执行。这类平台上写出来的 JavaScript 代码最终是由原生平台里面的 JavaScript 引擎来负责执行的。那么 JavaScript 如何调用原生代码呢？答案是利用语言的元编程能力，OC 和 Java 都具备一定的元编程能力，这样 JavaScript 只要知道原生平台的类名称，函数名称，就可以调用到原生平台的这个函数了。

关于这个课题，[这里有篇文章](http://www.jianshu.com/p/978c4bd3a759)写得深入浅出。想要理解原理的同学，推荐阅读。

关于这几类平台的性能对比，[这篇文章](https://my.oschina.net/vczero/blog/597980?fromerr=FY2e0zCC)有非常详细的数据。

## 总结

Hybrid 技术的愿景是真正达到一次开发，跨平台运行，但其性能是其最大的瓶颈。准原生平台的目标是让前端开发人员，基于其熟悉的前端框架，快速开发 App 的**界面和业务逻辑**，且其性能和原生 App 很接近。当使用准原生平台开发 App 时，除非你是全栈工程师，或者大体了解 iOS/Android 平台的一些开发知识，否则很大概率需要 iOS/Android 原生平台的开发人员配合。

以下几个场景可以考虑使用 React-Native 之类的准原生架构来开发：

* 熟悉前端技术构架：比如熟悉 React ，则可以考虑使用 React-Native 来进行开发。如果熟悉 Vue.js ，可以考虑选择 Weex 来进行开发。
* 对开发效率有较高的要求：特别是那些互联网创业公司，如果刚好又是个全栈工程师，可以考虑用这种技术来来提高整体开发效率，有可能一个人把 iOS/Android App 全包圆了。
* 应用非常频繁地更新：不管是修复严重 Bug 的 HotFix ，还是业务场景快速变化，我们在等待 AppStore 审核的时候，感觉是度日如年。如果这个痛点让你痛不欲生，不仿考虑一下准原生平台方案。

反过来，如果你对前端开发和构架不熟，切换到任何类型的跨平台技术方案上来，成本都将是巨大的。从头学习和适应全新的开发模式，虽然最后可能提高了效率，但学习时间成本可能会是不可承受这重。至少短期来看，性价比不高。

