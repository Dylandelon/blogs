Title: LeakCanary - Android 内存泄漏检查
Date: 2015-05-10 23:57
Modified: 2015-05-10 23:57
Tags: android
Slug: leakcanary
Authors: Joey Huang
Summary: 你被概率性的 OOM 困扰么？有时候，OOM 像幽灵一样，挥之不去，可真想把它揪出来时，又捉之不着。或许，是时候用 LeakCanary 来诊断一下了。LeakCanary 是一个用来检查 Android 下内存泄漏的开源库。这篇文章主要介绍 LeakCanary 的用法及其架构和其背后的实现原理。
Status: draft

### 前言

你被概率性的 OOM 困扰么？有时候，OOM 像幽灵一样，挥之不去，可真想把它揪出来时，又捉之不着。或许，是时候用 [LeakCanary][1] 来诊断一下了。它是一个用来检查 Android 下内存泄漏的开源库，这篇文章主要介绍其用法、架构和其背后的实现原理。

Square [有篇文章][2]介绍了开发这个库的原因。他们的一个付款流程里，需要用到用户的签名，他们直接用 Bitmap 来画签名，Bitmap 大小和屏幕分辨率是一样的。问题来了，在试图创建这个 Bitmap 对象时，概率性 OOM 如幽灵般相随。他们试了几个方法：

* 使用 `Bitmap.Config.ALPHA_8` 来节省内存
* 捕获 `OutOfMemoryError` 异常，调用 gc 清理内存，然后重试几次

最终这些都不起作用。最终他们发现他们在错误的方向上走得太远了。当存在**内存泄漏**时，可用内存越来越少，这个时候 OOM 可以发生在任何地方，特别是试图创建一些大内存对象，如 Bitmap 的时候。

我们在上一篇文章[《Android 内存与性能》][3]里介绍了使用 [MAT][4] 来分析内存泄漏的方法。概括起来核心步骤是：

* 发生 OOM 或做一些可能存在内存泄漏的操作后，导出 HPROF 文件
* 利用 MAT 结合代码分析，来发现一些引用异常，比如哪些对象本来应该被回收的，却还在系统堆中，那么它就是内存泄漏

如果有一个工具能自动完成这些事情，甚至在发生 OOM 之前，就把内存泄漏报告给你，那是多么美好的一件事情啊。LeakCanary 就是用来干这个事情的。

!!! notes "启发"
    LeakCanary 产生的背后有几个有意思的启发。一是像 Square 这样公司一样会被 OOM 这种问题困扰；二是他们也会犯错，试了几种方法都不起作用；三是他们最终用一个优雅的方式解决了这个问题，并且通过开源库的方式让所有人共享他们的工作成果。

### 用法

#### 监控 Activity 泄露

我们经常把 Activity 当作为 Context 对象使用，在不同场合由各种对象引用 Activity。所以，Activity 泄漏是一个重要的需要检查的内存泄漏之一。

```java
public class ExampleApplication extends Application {

	public static RefWatcher getRefWatcher(Context context) {
		ExampleApplication application = (ExampleApplication) context.getApplicationContext();
		return application.refWatcher;
	}

	private RefWatcher refWatcher;

	@Override public void onCreate() {
		super.onCreate();
		refWatcher = LeakCanary.install(this);
	}
}
```

`LeakCanary.install()` 返回一个配置好了的 `RefWatcher` 实例。它同时安装了 `ActivityRefWatcher` 来监控 Activity 泄漏。即当 `Activity.onDestroy()` 被调用之后，如果这个 Activity 没有被销毁，logcat 就会打印出如下信息告诉你内存泄漏发生了。

```shell
    * com.example.leakcanary.MainActivity has leaked:
    * GC ROOT thread java.lang.Thread.<Java Local> (named 'AsyncTask #1')
    * references com.example.leakcanary.MainActivity$2.this$0 (anonymous class extends android.os.AsyncTask)
    * leaks com.example.leakcanary.MainActivity instance
    * Reference Key: c4d32914-618d-4caf-993b-4b835c255873
    * Device: Genymotion generic Google Galaxy Nexus - 4.2.2 - API 17 - 720x1280 vbox86p
    * Android Version: 4.2.2 API: 17
    * Durations: watch=5100ms, gc=104ms, heap dump=82ms, analysis=3008ms
``` 

!!! notes
    LeakCanary 自动检测 Activity 泄漏只支持 Android ICS 以上版本。因为 `Application.registerActivityLifecycleCallbacks()` 是在 API 14 引入的。如果要在 ICS 之前监测 Activity 泄漏，可以重载 `Activity.onDestroy()` 方法，然后在这个方法里调用 `RefWatcher.watch(this)` 来实现。

#### 监控 Fragment 泄漏

```java
public abstract class BaseFragment extends Fragment {

	@Override 
	public void onDestroy() {
		super.onDestroy();
		RefWatcher refWatcher = ExampleApplication.getRefWatcher(getActivity());
		refWatcher.watch(this);
	}
}
```

当 `Fragment.onDestroy()` 被调用之后，如果这个 fragment 实例没有被销毁，那么就会从 logcat 里看到相应的泄漏信息。

#### 监控其他泄漏

```java
	...
	RefWatcher refWatcher = ExampleApplication.getRefWatcher(getActivity());
	refWatcher.watch(someObjNeedGced);
```

当 `someObjNeedGced` 还在内存中时，就会在 logcat 里看到内存泄漏的提示。

#### 集成 LeakCanary 库

```gradle
dependencies {
	debugCompile 'com.squareup.leakcanary:leakcanary-android:1.3'
	releaseCompile 'com.squareup.leakcanary:leakcanary-android-no-op:1.3'
}
```

在 debug 版本上，集成 LeakCanary 库，并执行内存泄漏监测，而在 release 版本上，集成一个无操作的 wrapper ，这样对程序性能就不会有影响。

### 原理

#### LeakCanary 流程图

![leakcanary](https://raw.githubusercontent.com/kamidox/blogs/master/images/leakcanary.png)

LeakCanary 的机制如下：

1. `RefWatcher.watch()` 会以监控对象来创建一个 `KeyedWeakReference` 弱引用对象
2. 在 `AndroidWatchExecutor` 的后台线程里，来检查弱引用已经被清除了，如果没被清除，则执行一次 GC
3. 如果弱引用对象仍然没有被清除，说明内存泄漏了，系统就导出 hprof 文件，保存在 app 的文件系统目录下
4. `HeapAnalyzerService` 启动一个单独的进程，使用 `HeapAnalyzer` 来分析 hprof 文件。它使用另外一个开源库 [HAHA][7]。
5. `HeapAnalyzer` 通过查找 `KeyedWeakReference` 弱引用对象来查找内在泄漏
6. `HeapAnalyzer` 计算 `KeyedWeakReference` 所引用对象的最短强引用路径，来分析内存泄漏，并且构建出对象引用链出来。
7. 内存泄漏信息送回给 `DisplayLeakService`，它是运行在 app 进程里的一个服务。然后在设备通知栏显示内存泄漏信息。

#### 几个有意思的代码

**如何导出 hprof 文件**

```java
File heapDumpFile = new File("heapdump.hprof");
Debug.dumpHprofData(heapDumpFile.getAbsolutePath());
```
可以参阅 [AndroidHeapDumper.java][8] 的代码。

**如何分析 hprof 文件**

这是个比较大的话题，感兴趣的可以称步另外一个开源库 [HAHA][7]，它的祖先是 [MAT][4]。

**如何使用 HandlerThread 实现后台处理**

可以参阅 [AndroidWatchExecutor.java][9]的代码，特别是关于 Handler, Loop 的使用，虽然是老话题。

**怎么样知道某个变量已经被 GC 回收**

可以参阅 [RefWatcher.java][10]的 `ensureGone()` 函数。最主要是利用 `WeakReference` 和 `ReferenceQueue` 机制。简单地讲，就是当弱引用 `WeakReference` 所引用的对象被回收后，这个 `WeakReference` 对象就会被添加到 `ReferenceQueue` 队列里，我们可以通过其 `poll()` 方法获取到这个被回收的对象的 `WeakReference`实例，进而知道需要监控的对象是否被回收了。

### 关于内存泄漏

内存泄漏可能很容易发现，比如 Cursor 没关闭；比如在 `Activity.onResume()` 里 register 了某个需要监听的事件，但在 `Activity.onPause()` 里忘记 unregister 了；内存泄漏也可能很难发现，比如 [LeakCanary 示例代码][5]，隐含地引用，并且只有在旋转屏幕时才会发生。还有更难发现，甚至无能为力的内存泄漏，比如 Android SDK 本身的 BUG 导致内存泄漏。[AndroidExcludedRefs.java][6] 里就记录了一些己知的 AOSP 版本的以及其 OEM 实现版本里存在的内存泄漏。

### 今日推荐

推荐一个画图工具 planUML，其最大的特色是使用脚本来画图。


[1]: https://github.com/square/leakcanary
[2]: https://corner.squareup.com/2015/05/leak-canary.html
[3]: http://kamidox.com/android-memory-guide.html
[4]: http://www.eclipse.org/mat/downloads.php
[5]: https://github.com/square/leakcanary/blob/master/library/leakcanary-sample/src/main/java/com/example/leakcanary/MainActivity.java
[6]: https://github.com/square/leakcanary/blob/master/library/leakcanary-android/src/main/java/com/squareup/leakcanary/AndroidExcludedRefs.java
[7]: https://github.com/square/haha
[8]: https://github.com/square/leakcanary/blob/master/library/leakcanary-android/src/main/java/com/squareup/leakcanary/AndroidHeapDumper.java
[9]: https://github.com/square/leakcanary/blob/master/library/leakcanary-android/src/main/java/com/squareup/leakcanary/AndroidWatchExecutor.java
