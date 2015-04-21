Title: Android应用内存与性能
Date: 2015-04-22 23:30
Modified: 2015-04-22 23:30
Tags: android
Slug: android-memory-guide
Authors: Joey Huang
Summary: 本文介绍了android平台上内存管理机制以及开发过程中关于内存使用的注意事项以及内存相关问题的调试方法和调试工具。
Status: draft

### 官方教程

1. [Android Performance][6] 是 GOOGLE 近期发布在 Udacity 上的官方教程
   不方便科学上网的同学可以从我的[百度网盘][7]里下载。
2. [Android Performance Patterns][8] 是 GOOGLE 在 2015 年发布在 Facebook 上的专题课程
   这部分内容 CDGChina 加了中文字幕，并放在 [Youku][8] 上了。

### 关于内存的几个结论

**GC 的工作机制**
当 GC 工作时，虚拟机停止其他工作。频繁地触发 GC 进行内存回收，会导致系统性能严重下降。

**内存抖动**
在极短的时间内，分配大量的内存，然后又释放它，这种现象就会造成内存抖动。典型地，在 View 控件的 onDraw 方法里分配大量内存，又释放大量内存，这种做法极易引起内存抖动，从而导致性能下降。因为 onDraw 里的大量内存分配和释放会给系统堆空间造成压力，触发 GC 工作去释放更多可用内存，而 GC 工作起来时，又会吃掉宝贵的帧时间 (帧时间是 16ms) ，最终导致性能问题。

**内存泄漏**
Java 语言的内存泄漏概念和 C/C++ 不太一样，在 Java 里是指不正确地引用导致某个对象无法被 GC 释放，从而导致可用内存越来越少。比如，一个图片查看程序，使用一个静态 Map 实例来缓存解码出来的 Bitmap 实例来加快加载进度。这个时候就可能存在内存泄漏。

内存泄漏会导致可用内存越来越少，从而导致频繁触发 GC 回收内存，进而导致性能下降。

**调试工具**

* Memory Monitor Tool: 可以查阅 GC 被触发起来的时间序列，以便观察 GC 是否影响性能。
* Allocation Tracker Tool: 从 Android Studio 的这个工具里查看一个函数调用栈里，是否有大量的相同类型的 Object 被分配和释放。如果有，则其可能引起性能问题。
* MAT: 这是 Eclipse 的一个插件，也有 [stand alone][9] 的工具可以下载使用。

**几个原则**

* 别在循环里分配内存 (创建新对象)
* 尽量别在 View 的 onDraw 函数里分配内存
* 实在无法避免在这些场景里分配内存时，考虑使用对象池 (Object Pool)

**实例**

通过实例来演示内存抖动。

**延伸阅读**

关于 Android 性能优化，网络上有几篇比较好的文章，基本按照 GOOGLE 的官方教程翻译过来的，质量比较高。可以参考一下。

1. [Android 性能优化内存篇][3]－[胡凯的博客][4]
2. [Android性能优化典范][5]－[胡凯的博客][4]

**历史**

GC 是在 1959 年由 John McCarthy 发明的，此发明是为了解决 Lisp 编程语言里的内存问题的。《黑客和画家》作者，硅谷最有影响力的孵化器公司 YC 创立者 Paul Graham 高度评价 Lisp 语言，认为编程语言发展到现在，还是没有跳出 Lisp 语言在上世纪 60 年代所倡导的那些理念。并且，他还把自己当初创业，实现财务自由的项目 Viaweb 的成功归功于 Lisp 语言。详细可阅读 Paul Graham 的[这篇博客][1]和[这篇博客][2]。


[1]: http://www.paulgraham.com/hundred.html
[2]: http://www.paulgraham.com/diff.html
[3]: http://hukai.me/android-performance-memory/
[4]: http://hukai.me
[5]: http://hukai.me/android-performance-patterns/
[6]: https://www.udacity.com/course/ud825
[7]: http://pan.baidu.com/
[8]: http://www.youku.com/playlist_show/id_23494296.html
[9]: http://www.eclipse.org/mat/downloads.php
