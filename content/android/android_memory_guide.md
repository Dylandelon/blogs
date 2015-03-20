Title: Android应用内存使用指南
Date: 2015-03-22 23:30
Modified: 2015-03-22 23:30
Tags: android
Slug: android-memory-guide
Authors: Joey Huang
Summary: 本文介绍了android平台上内存管理机制以及开发过程中关于内存使用的注意事项以及内存相关问题的调试方法和调试工具。

### 内存和性能

**GC 的工作机制**
当 GC 工作时，虚拟机停止其他工作。频繁地触发 GC 进行内存回收，会导致系统性能严重下降。

**内存抖动**
在极短的时间内，分配大量的内存，然后又释放它，这种现象就会造成内存抖动。典型地，在 View 控件的 onDraw 方法里分配大量内存，又释放大量内存，这种做法极易引起内存抖动，从而导致性能下降。因为 onDraw 里的大量内存分配和释放会给系统堆空间造成压力，触发 GC 工作去释放更多可用内存，而 GC 工作起来时，又会吃掉宝贵的帧时间 (帧时间是 16ms) ，最终导致性能问题。

**调试工具**

* Memory Monitor Tool: 可以查阅 GC 被触发起来的时间序列，以便观察 GC 是否影响性能。
* Allocation Tracker Tool: 从 Android Studio 的这个工具里查看一个函数调用栈里，是否有大量的相同类型的 Object 被分配和释放。如果有，则其可能引起性能问题。

**几个原则**

* 别在循环里分配内存 (创建新对象)
* 尽量别在 View 的 onDraw 函数里分配内存
* 实在无法避免在这些场景里分配内存时，考虑使用对象池 (Object Pool)

**实例**

通过实例来演示内存抖动以及内存分配工具的使用。最后通过对象池来改善问题。

**八卦**

GC 是在 1959 年由 John McCarthy 发明的，此发明是为了解决 Lisp 编程语言里的内存问题的。《黑客和画家》作者，硅谷最有影响力的孵化器公司 YC 创立者 Paul Graham 高度评价 Lisp 语言，认为编程语言发展到现在，还是没有跳出 Lisp 语言在上世纪 60 年代所倡导的那些理念。并且，他还把自己当初创业，实现财务自由的项目 Viaweb 的成功归功于 Lisp 语言。详细可阅读 Paul Graham 的[这篇博客][1]和[这篇博客][2]。


[1]: http://www.paulgraham.com/hundred.html
[2]: http://www.paulgraham.com/diff.html





