Title: Android应用程序性能优化工具介绍及调试实例
Date: 2014-11-18 23:30
Modified: 2014-11-18 23:30
Tags: android
Slug: android-performance-debug-tools
Authors: Joey Huang
Summary: 本文介绍了android平台上的性能优化工具的使用，然后通过一个实例来介绍这些工具的使用以及一些常用的性能优化的方法。

[TOC]

## 开篇

关于Android性能方面，不能不读[这篇文章][1]。作者是GOOGLE员工，同时也是个摄影爱好者。本文就是通过阅读这篇文章，结合Android 4.4平台和自身实践总结出来的，个人认为对Android应用程序性能优化较有帮助的一些工具及使用示例。不足之处欢迎指正。

## 性能问题汇总

性能问题总的来说，就是反映慢。实际上，从图形学意义来讲，就是帧率低。性能问题最终可以归纳成两类问题：

1. 布局不合理导致过度绘制。
   重绘(Over Draw)是指屏幕上的一个象素点被画了多次，比如一个图片按钮(ImageButton)要先按出背景，再画出按钮上的图片，这就是重绘的概念。过度重绘是指有由于布局不合理导致一些不必要的重绘，比如一个窗口多有层背景，那么在渲染的时候，就会一层一层地画上去，上面的背景覆盖掉下而把背景。这个时候我们可以把下面的背景去掉。只画上层的背景，从而提高刷新速度。
2. 函数调用不合理导致每帧的刷新之间CPU花了太长的时间。
   比如每次刷新时，或者处理点击事件时，都去大量地读写文件。对于这种问题，要么使用缓存减少文件读取次数。如果不得不读，可能就要考虑使用异步加载的方式来确保界面刷新，数据加载完填充数据的方式来优化性能和用户体验。

## 性能调试工具

Android的开发者选项里以及ADT/monitor提供了大量性能调试工具来调试上述性能问题。本文重点介绍三个工具：

1. GPU呈现模式分析 -> 在adb shell dumpsys gfxinfo中
   这个在开发者选项的**监控**里面。可以从GPU刷新的角度分析我们的刷新帧率问题。
2. 调试GPU过度绘制 -> 显示过度重绘区域
   这个在开发者选项的**硬件加速渲染**里面。这个可以查看一些界面的布局不合理导致的过度绘制的性能问题。
3. Method Profiling工具
   这个在DDMS/monitor里可以找到，这个工具可以从虚拟机层面抓取每个函数及其调用的函数的运行时间，统计运行次数等功能。是分析性能问题的绝佳工具。

## GPU呈现模式分析

GPU呈现模式分析可以从GPU层面上分析我们的刷新效率。使用这个工具可以用来发现有没有刷新帧率过低的问题。

首先，在开发者模式里打开**GPU呈现模式分析**菜单，在弹出式菜单里选择**在adb shell dumpsys gfxinfo中**选项。打开这个选项后，系统会为每个窗口记录最近128帧的刷新时间。

接着，手机连接电脑，确保adb可用。然后运行你要调试的应用程序做一些必要的操作之后，运行下面的命令在抓取GPU刷新的LOG：

    :::shell
    adb shell dumpsys gfxinfo com.android.soundrecorder > soundrecorder_gfxinfo_1.log

其中*com.android.soundrecorder*是要分析的应用的包名称；*soundrecorder_gfxinfo_1.log*是抓取出来的LOG保存位置。

接着，打开LOG文件*soundrecorder_gfxinfo_1.log*，找到**Profile data in ms:**那节，可以看到类似下面的数据：

    :::text
    com.android.soundrecorder/com.android.soundrecorder.SoundRecorder/android.view.ViewRootImpl@41db6d18
    Draw    Process Execute
    4.38    6.49    0.87
    0.65    5.69    0.84
    4.40    7.82    3.10
    2.64    4.62    0.92
    ...     ...     ...

其中有三种类型的数据数据：

* Draw是在java里构建显示列表所花的时间，这个表示花在`View.onDraw(Canvas canvas)`里的时间
* Process是android的2D渲染器执行Draw所构建出来的显示列表所花的时间，一个View的结构层次越复杂，就有越多的渲染命令需要被执行，就会花越多的时间
* Execute是发送一帧显示数据给GPU的合成器所花的时间，这部分时间一般较短且较固定

上述的描述比较抽象，我们从代码层面来看这三个数据的含义：

`android.view.HardwareRender$GlRenderer.draw()`函数抛开无关代码后，只剩下两行：

    #!java
    @Override
    void draw(View view, View.AttachInfo attachInfo, HardwareDrawCallbacks callbacks, Rect dirty) {
        
        ...

        DisplayList displayList = buildDisplayList(view, canvas);
    
        ...

        status |= drawDisplayList(attachInfo, canvas, displayList, status);
        
        ...
    }

Line 6: 这个就是Draw的时间，`buildDisplayList()`最终会调用`View.getDisplayList()`，而后者就是从View树里从根部开始遍历所有的子View，并且依次调用每个View的`View.onDraw()`方法把控件都画在画布上。这里，每个View都独立地画在一个Canvas上。
Line 10: 这个就是Process的时间，`drawDisplayList()`会调用`android.view.GLE20Canvas.drawDisplayList()`函数来把DisplayList合并起来。即Draw的结果是一个DisplayList，Process要做的就是把这个DisplayList合并起来。

有了上面的分析，我们就清楚了这三个数据的含义，要减少Draw的时间，就要去减少控件层次结构和个数，同时优化每个控件的onDraw函数。要减少Process时间，就去减少控件层次结构和个数以及一些复杂的效果，如半透明之类的。而Execute的时间基本不受软件控制，可以排除在优化对象之外。

接下来，回到我们抓到的LOG数据*soundrecorder_gfxinfo_1.log*里面。我们把这三个数据拷贝到excel里，做一个柱状图(Stacked Column)来直观地观察一下GPU的刷新时间。

![IMAGE](http://kamidox-blogs.qiniudn.com/soundrecorder_gfxinfo_1_stacked_column.jpg)

从上图可以看出来，一帧的刷新时间大部分都小于16ms，部分帧超过16ms。除了这个数据外，我们也可以算一下Draw和Process的平均时间，计算这个时间是为了量化对比优化前后的性能指标。我们可以精确地计算出性能提升了多少个百分点。针对本次抓到的LOG，我们计算出来的平均时间如下：

* Draw平均时间：3.926ms
* Process平均时间：7.262ms

!!! Note "16ms的含义"
    一般情况下，如果能保证60fps的刷新帧率，那么人眼看起来就会觉得很流畅。这样1000 / 60大概就是16ms。所以需要保证一帧的刷新时间小于16ms就能保证流畅度。

## 调试GPU过度绘制

GPU呈现模式分析让我们了解GPU刷新，并且能知道帧率能不能达到60fps。还能算出Draw和Process平均时间供对比分析，但对怎么样优化就不明确了。这样我们就需要GPU过度绘制工具来帮忙。

首先，在开发者模式里关闭之前打开的**GPU呈现模式分析**，然后打开**调试GPU过度绘制**，选择**显示过度重绘区域**。这样就会看到界面会画出花花绿绿的背景。这些不同颜色的背景就是用来指示出过度重绘的程度的。

背景颜色   | 表示的含义
-----------|--------------------------------------------
无颜色     | 表示没有重绘，即一个象素点只被绘制了1次。
蓝色       | 表示重绘了1次，即一个象素点被绘制了2次。屏幕上如果有大块的的蓝色区域是可以接受的，但如果整个屏幕都是蓝色的，那就需要优化了，可以去掉一层。
绿色       | 表示重绘了2次，即一个象素点被绘制了3次。中等面积的绿色区域是可以接受的，不过最好引起警惕，去看一下能不能优化。
淡红色     | 表示重绘了3次，即一个象素绘制了4次。很小的淡红色区域是可以接受的，其他情况就需要去优化。
深红色     |表示重绘了4次以上。这个不正确的，必须进行优化。

我们可以打开录音机模块，看一下录音机这个模块在优化之前的GPU过度绘制显示图片：

![IMAGE](http://kamidox-blogs.qiniudn.com/profile_recorder_1.png) ![IMAGE](http://kamidox-blogs.qiniudn.com/profile_recorder_list_1.png)

录音主界面可以看出两个明显的问题：

1. 整个背景都蓝色的。这个应该可以优化，去掉一层。
2. 底部区域是绿色的，需要分析一下是否可以优化。

录音列表界面也可以看出一个问题：底部区域是蓝色的，重绘了2次，可以想办法优化。

我们以录音主界面为例，看一下它的布局文件：

    #!xml
    <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:background="@drawable/main_bg">

        <RelativeLayout android:id="@+id/timerViewLayout"
            android:layout_width="match_parent"
            android:layout_height="123dip">

            <ImageButton android:id="@+id/listButtons"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_alignParentTop="true"
                    android:layout_alignParentRight="true"
                    android:src="@drawable/record_ic_recordlist"
                    android:background="@null"/>

            <TextView android:id="@+id/stateMessage1"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_toLeftOf="@+id/listButtons"
                android:layout_alignParentTop="true"
                android:layout_alignParentLeft="true"
                android:layout_marginTop="15dip"
                android:layout_marginLeft="45dip"
                android:gravity="center"
                style="@android:style/TextAppearance.Small.Inverse" /> 
                
            <TextView android:id="@+id/timerView"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:textSize="60sp"
                android:layout_centerHorizontal="true"
                android:layout_alignParentBottom="true"
                style="@android:style/TextAppearance.Large.Inverse" />

        </RelativeLayout>
        
        <com.android.soundrecorder.VUMeter android:id="@+id/uvMeter"
            android:layout_width="match_parent"
            android:layout_height="0dip"
            android:layout_weight="1" />
        
        <RelativeLayout
            android:layout_width="match_parent"
            android:layout_height="150dip"
            android:background="@drawable/op_bar_bg">
            
            <ImageButton android:id="@+id/recordButton"
                android:layout_height="wrap_content" 
                android:layout_width="wrap_content"
                android:layout_centerInParent="true"
                android:src="@drawable/record_btn_record"
                android:background="@null"/>
            
            <TextView android:id="@+id/stopButton"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:textSize="14sp"
                android:textColor="#CCCCCC"
                android:text="@string/accept"
                android:layout_alignParentRight="true"
                android:layout_centerVertical="true"
                android:singleLine="true"
                android:gravity="center"
                android:layout_marginRight="25dip"
                android:clickable="true"
                android:background="@drawable/record_btn_complete"
                 />
        </RelativeLayout>
    </LinearLayout>

LINE 5：主界面有个主背景图片`@drawable/main_bg`，这是个全屏的背景图片。加上窗口背景图片，这块实际上有完全叠加起来的两层背景。我们可以优化去掉一层背景。
LINE 48：底部区域也有个背景图片`@drawable/op_bar_bg`。这个实际上是多余的，可以去掉。

优化措施：

1. 去掉LINE 5及LINE 48的背景图片
2. 在录音Activity的`onCreate()`方法设置窗口的背景图片`getWindow().setBackgroundDrawableResource(R.drawable.main_bg);`

!!! Note "窗口背景图片"
    定义在Theme里的窗口背景，在Activity启动的时候由系统创建并应用在Activity窗口里。所以在上面第2个优化步骤里。我们是直接把背景图片从布局文件里删除，移到Activity的窗口里。这样就省去了一层背景图片。

再来看一下录音列表这个activity的布局文件：

    #!xml
    <?xml version="1.0" encoding="utf-8"?>
    <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
        android:orientation="vertical" 
        android:layout_width="fill_parent"
        android:layout_height="fill_parent">
        
        <FrameLayout android:layout_width="fill_parent"
            android:layout_height="0dip"
            android:layout_weight="1">
                
            <TextView android:id="@android:id/empty"
                android:layout_width="fill_parent" 
                android:layout_height="fill_parent"
                android:gravity="center|center" 
                android:textSize="18sp"
                android:text="@string/list_empty" />
                
            <ListView android:id="@android:id/list" 
                android:layout_width="fill_parent"
                android:layout_height="wrap_content" 
                android:gravity="left|top" />
                
        </FrameLayout>
        
        <View android:id="@+id/menuAnchor"
            android:layout_width="1dip"
            android:layout_height="5dip"
            android:layout_gravity="right"
            android:visibility="invisible"/>"
        
        <RelativeLayout
            android:id="@+id/bottomBarLayout"
            android:layout_width="match_parent"
            android:layout_height="150dip"
            android:background="@drawable/op_bar_bg">
            
            <ImageButton android:id="@+id/recordButton"
                android:layout_height="wrap_content" 
                android:layout_width="wrap_content"
                android:layout_centerInParent="true"
                android:src="@drawable/record_btn_record"
                android:background="@null" />

            <ImageButton android:id="@+id/optionButton"
                android:layout_height="wrap_content" 
                android:layout_width="wrap_content"
                android:layout_alignParentRight="true"
                android:layout_centerVertical="true"
                android:layout_marginRight="25dip"
                android:src="@drawable/recordlist_btn_more"
                android:background="@null"/>

        </RelativeLayout>
    </LinearLayout>

LINE 35：底部区域有个背景图片`android:background="@drawable/op_bar_bg`，加上我们上面提到的窗口背景图片，所以底部区域这块实际上覆盖了两层背景。就是说这块背景会绘制2次，所以呈现了蓝色。

优化措施：

1. LINE 7的FrameLayout我们给它加上一个白色的背景色。
2. 在录音列表Activity的`onCreate()`方法里去掉窗口背景图片。`getWindow().setBackgroundDrawable(null)`

优化之后，我们再看一下这两个窗口在优化前后的样子：

![IMAGE](http://kamidox-blogs.qiniudn.com/profile_recorder_1.png) ![IMAGE](http://kamidox-blogs.qiniudn.com/profile_recorder_2.png) 

对比可以看得出来，录音主界面从原来是全屏蓝色，底部绿色变成背景全部无色。这样我们就省去了一层背景图片。

![IMAGE](http://kamidox-blogs.qiniudn.com/profile_recorder_list_1.png) ![IMAGE](http://kamidox-blogs.qiniudn.com/profile_recorder_list_2.png)

而录音列表界面背景也变成无色的，即背景只画一次。

优化之后，我们通过上面介绍的**GPU呈现模式分析**再抓一次LOG，计算Draw和Process的平均时间分别是：

* Draw平均时间：3.566ms；优化之前是3.926ms
* Process平均时间：7.200ms；优化之前是7.262ms

从上面定量来看，Draw性能大概提高了9.17%。而Process性能没有明显提高。这也是符合我们的预期的，因为我们只优化了画图部分，并没有优化布局的层次结构，所以Process不会提高。

## Method Profiling工具

上面介绍的工具用来调试布局不合理导致过度绘制，而Method Profiling工具则可以调试刷新之外的性能，比如响应用户点击事件时花了大量的时间读写文件之类的问题。

首先，手机连接电脑，确保adb可用。打开ADT/monitor，打开**device**窗口，选择要调试的应用程序，然后点击**Start Method Profiling**开始抓取LOG。

![IMAGE](http://kamidox-blogs.qiniudn.com/soundrecorder_start_method_profiling.jpg)

接着，操作手机运行你要优化性能的程序，在里面做适当的操作。操作完成后，点击**Stop Method Profiling**按钮，会自动在临时目录保存一个trace文件，打开后大概如下图所示：

![IMAGE](http://kamidox-blogs.qiniudn.com/soundrecorder_main_method_profiling.jpg)

一些关键数据的含义如下：

字段名称                    | 含义
----------------------------|---------------
Incl Cpu Time %             | 函数自己及其调用的函数总共所占用CPU的时间占总时间的百分比
Incl Cpu Time               | 函数自己及其调用的函数总共所占用CPU的时间，单位为ms
Excl CPU Time %             | 函数自己(不包含其调用的函数)运行时占用的CPU时间的百分比
Excl CPU Time               | 函数自己(不包含其调用的函数)运行时占用的CPU时间
Incl Real Time              | 函数自己及其调用的函数总共所用的时间
Excl Real Time              | 函数自己(不包含其调用的函数)运行时所用的时间
Calls + RecurCalls/Total    | 在抓LOG这段时间内函数的调用的总次数，包含递归调用的次数
Cpu Time/Call               | 函数调用一次所用的CPU时间
Real Time/Call              | 函数调用一次所用的时间

!!! Note "CPU Time vs Real Time"
    这两个时间有什么区别呢？简单地讲，CPU Time就是CPU真正在运行这个函数的代码所花的时间；而Real time是Wall time，即这个函数从开始进入到真正退出所花的时间。这两个时间为什么会不同呢？举个例子，假如一个函数读取文件，并处理文件里的文本内容。读取文件涉及到IO操作，比如打开文件，实际上打开文件时调用打开文件的这个函数所在线程会短时间进入SLEEP状态，即不占用CPU，但也不返回，而是等待底层真正文件打开成功后，退出SLEEP状态再返回。这个短时间的SLEEP状态是不计处CPU Time的，因为它不占用CPU。但是计入Real time，因为函数还没返回。所以两者必定满足下面的条件：CPU Time <= Real Time。

Method Profiling的信息量很大，可以挖掘很多很有意思的信息。下面列举一些信息来抛砖引玉。

### 刷新时间

我们可以用Method Profiling抓一个录音过程中的LOG文件。在ADT/monitor里可以看到上文我们提到Draw和Process的概念：

![IMAGE](http://kamidox-blogs.qiniudn.com/soundrecorder_GlRenderer.draw.jpg)

在ADT/monitor里的信息可以看出，`android.view.HardwareRender$GlRenderer.draw()`的**Incl Cpu Time**总共占用CPU 3012.359ms，占总CPU时间的88.8%，在抓LOG的这段时间里，总共调用了85次，每次调用的CPU时间是35.440ms，Real time是45.637ms。而其Children里面，`GlRenderer.buildDisplayList()`占用74.1%，这个实际上就是`View.onDraw()`占用的时间总和。`GlRenderer.drawDisplayList()`占用19.7%，这个就是合成DisplayList占用的时间。

通过这些信息，我们知道我们抓的这段LOG里，CPU主要花费在界面刷新上（占了88.8%）。我们需要优化控件的`onDraw()`方法来优化性能。

继续往下看，我们可以看到录音控件里的`UVMeter.onDraw()`方法占用了整个的CPU时间的61.8%。

![IMAGE](http://kamidox-blogs.qiniudn.com/soundrecorder_VUMeter.onDraw.jpg)

我们可以看出来`drawLine()`函数CPU时间占用了44.8%，总共用时940.858ms，调用了15046次，每次调用需要用时0.063ms；从这些数据来看，我们优化的方向应该想办法减少`UVMeter.onDraw()`里对`drawLine()`的调用次数。`String.format()`函数CPU时间占用了35.4%。可以用类似的方法来分析。

接下来，就是深入`UVMeter.onDraw()`方法的代码里，去看有没有办法减少`drawLine()`和`String.format()`函数的调用次数了。

### ListView的ViewHolder

在优化ListView的滚动效率时，我们经常会给每个Item一个ViewHolder避免重复创建View。我们抓一个打开录音列表Activity的Method Profiling LOG文件，从LOG文件里可以定量地看出来这个优化能节省多少时间。

![IMAGE](http://kamidox-blogs.qiniudn.com/soundrecorder_getView.jpg)

从trace里可以看到，`getView()`函数占总CPU时间的45.5%，每次调用平均CPU用时31.052ms。而其Children里的`LayoutInflater.inflate()`占用CPU时间72.7%，总共调用11次，每次CPU用时52.971ms。ViewHolder就是为了避免重复调用`inflate()`函数来创建View的。这样就可以为每个Item节省52.971ms。这是一个非常值得的优化项目。

我们可以再录音列表里上下滚动来抓一个LOG来对比：

![IMAGE](http://kamidox-blogs.qiniudn.com/soundrecorder_scroll_getView.jpg)

从对比可知，`getView()`占总CPU时间为12.8%，每次调用平均CPU时间为10.369ms。由此可见尽量减少调用`inflate()`是优化性能的一个重要方法。同时要减少`inflate()`函数的用时，可以通过简化View的布局层次结构来达到目的。

### 一些技巧

Method Profiling能看到的信息远不止这些。可以通过重点关注需要优化的性能瓶颈，有针对性地从Method Profiling Log里找到可优化的线索，一些有用的技巧总结如下：

1. 针对需要优化的性能问题抓取LOG
   比如需要优化滚动慢的问题，就只抓滚动的LOG，如果需要优化启动慢的问题，就只抓启动的LOG。这样才能有针对性地从LOG里找出可优化的线索。
2. 阅读LOG的时候，可以从上往下，按照CPU占用时间倒序来发现线索。针对framework里的一些函数如果不清楚其功能可以跳过。当看到应用里面的函数调用时，就需要深入去对比LOG和代码，来发现可优化的线索。

## 结束语

性能问题是个复杂的问题。单靠这些调试工具不能完全解决问题，而应该在设计阶段就考虑性能问题。在优化阶段利用这些调试工具来优化细节，同时发现一些设计阶段没有发现的性能瓶颈问题。

本文将录音机应用作为例子描述的一些log文件可以在[这里][2]下载到。里面的文件说明如下：

* sound_record_list_start.trace：启动录音列表的trace文件
* sound_record_list.trace：在录音列表里上下滚动的trace文件
* sound_recorder.trace：录音过程中的trace文件
* soundrecorder_gfxinfo_1.log：优化前的gfxinfo文件
* soundrecorder_gfxinfo_1.xlsx：优化前的gfxinfo文件制作出来的excel文件
* soundrecorder_gfxinfo_2.log：优化后的gfxinfo文件
* soundrecorder_gfxinfo_2.xlsx：优化后的gfxinfo文件制作出来的excel文件

[1]: http://www.curious-creature.org/docs/android-performance-case-study-1.html
[2]: http://pan.baidu.com/s/1Gp5Xc
