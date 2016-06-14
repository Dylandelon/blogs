Title: 日积月累
Date: 2015-04-13 00:19
Modified: 2015-04-13 00:19
Slug: accumulation
Authors: Joey Huang
Summary: 日积月累
Status: draft

[TOC]

## 20160614

Node.js Design Patterns: Chapeter 1 Node.js Design Fundamentals

异步和回调；模块系统；观察者模式等等

### The Node.js philosophy

* Small Core: 微内核
* Small Module: 小模块。解决了 dependency hell 问题，每个模块可以有自己独立的依赖模块列表。即一个软件可以依赖同一个模块的不同版本。
  * Small is beautiful.
  * Make each program do one thing well.
  * Easier to understand and use
  * Simpler to test and maintain
  * Perfect to share with the browser
* Small surface area: 小接口。暴露出最小的，最重要的接口。次要的放在模块的属性，方法里。
  * 暴露尽量少的接口 -> 易于使用
  * 模块设计的目的是为了被使用，而不是被扩展
* Simplicity and pragmatism: 简单实用原则


## 20160406

Pelican 代码阅读

* 命令行参数解析: python std lib -> argparse
* Log 系统: python std lib -> logging
* 导入 pelicanconf.py 中的设置信息
  使用 `imp.load_source()` 或 `SourceFileLoader().load_module()` 把 `pelicanconf.py` 作为模块导入，再使用 `inspect.getmembers()` 来获取模块里的变量，所有的全大写的变量作为设置信息读取进来。导入模块时，也可以使用 `__import__()` 函数，但参数的形式是不一样的。
* 给定一个字符串 `pelican.Pelican`，怎么样用这个字符串所代表的类创建对象？
  使用 `__import__` 和 `getattr()` 实现

```python
    cls = settings['PELICAN_CLASS']     # default class: 'pelican.Pelican'
    if isinstance(cls, six.string_types):
        module, cls_name = cls.rsplit('.', 1)
        module = __import__(module)
        cls = getattr(module, cls_name)

    return cls(settings), settings
```

* 如何把某个目录加入当前的模块搜索目录？
  把目录添加进 `sys.path` 列表即可
* 进程内信号/事件: 使用 [blinker](https://github.com/jek/blinker) 实现
* 插件系统
  * 使用进程内信号 `blinker` 来实现与插件的通信
  * 插件需要实现 `register()` 函数，这个函数由 Pelican 在初始化时调用
  * 插件需要注册 Pelican 系统的信号，根据不同的信号做相应的处理，具体参阅 `docs/plugins.rst` 以及 `pelican/signals.py`。
* 如何处理可选的依赖包？
  比如 Pelican 支持多种文档格式 markdown, rst, etc. 怎么样确保只使用 markdown 的人没安装 rst 转码库 `docutils` 也能正常运行呢？这里的方法是处理 `ImportError`，并且当发生 `ImportError` 时禁用这个转换器。
* TODO: Reader/Writer/Generator 源码阅读

## 20150607

####《持续的幸福》阅读笔记

* 幸福 1.0 vs 幸福 2.0
  幸福 1.0 主要关注生活满意度，由积极情绪，投入和意义构成。而幸福 2.0 则由 PERMA 指标构成，具体就是积极情绪，投入，意义，成就，积极的人际关系。Seligman 教授认为，要让人生蓬勃发展，可以提高这五项指标来获得。
* 三件好事练习
  从进化的角度来看，人是悲观偏好的，那些过分乐观的人活不过冰河世纪。如何克服悲观偏好，可以从三个好事练习着手。即每天记录三个好事，可以是大事（如获得升职），也可以是生活的小事（如发现一个好吃的饭馆）。然后写上这个事对你的影响或产生的原因。这样来引导自己多关注积极的事情。
* 突出优势练习
  通过 www.authentichappiness.org 来测量自己的性格优势，通过发挥自己的性格优势来增加幸福感。
* 积极主动式回应 vs 消极主动式回应
  女儿告诉我她在学校运动会上获得了一个奖牌。
  积极主动：太棒了，你拿到奖牌时是什么感受？你的同学是什么反应？这个运动挺难的，平时没见你练啊，你怎么拿到奖牌的？
  积极被动：哦，真厉害。
  消极被动：我今天上班很累。
  消极主动：不好好读书，拿个运动会奖牌干什么用，把时间花在学习上。
* 洛萨达比例
  职场洛萨达比例在 3:1 以上时，公司的业务是蓬勃发展的。要获得良好的家庭生活，洛萨达比例需要达到 5:1。
  洛萨达比例 (以其发现者 Marcel Losada 命名) 是指对所有的语言按照积极和消极进行编码，积极和消极的比例即洛萨达比例。
* 成就公式
  成就 = 技能 x 努力。成就是一个矢量，而不是绝对距离。成就是朝一个特定的方向持续努力的结果。
  **速度**: 自动化的东西越多，速度越快，我们对该任务的知识就越多。
  **缓慢**: 成就中举足轻重，有意识的过程（如规划，精细化，检查错误和创造）。速度越快，知识越多，留给这些执行功能的时间就越多。
  **学习速度**: 新的信息能以多快的速度变为自动知识，以留给缓慢的执行过程更多的时间。
* 学习的速度
  技能的学习是让我们获得一种自动化处理的能力。比如打字，刚开始的时候需要先想我们打什么字，这个字由哪几个字根组成，这些字根在哪个按键上，然后手指再按下这些按键。这是技能，当这项技能经过足够多的练习，变成一个自动化的过程后，打字就快很多了。因为头脑在想打哪个字的时候，手指已经直接按下能打出这个字所在的键盘了。这就是自动化处理能力。自动化处理能力可以大大提高效率。这也是一万小时天才理论的基础。学习的快，是指你能以多快的速度培养一项技能的自动化处理能力。
* 创伤后成长的五要素
  1. 认识到创伤后信念崩塌是正常的反应；
  2. 减少焦虑和强迫性的想法；
  3. 讲出创作经历；
  4. 描述创伤后积极的改变；
  5. 总结因为创伤而产生的更加坚强，更加无惧挑战的人生原则和立场。
  **那些杀不死我的，必将使我强大。**---尼采
* ABCDE 模式
  情感的后果不是由不好的事情导致的，而是由你对这个事情的解读导致的。
  Adversity -> Belief -> Consequence。Disputation 代表反驳，Energization 代表你成功进行反驳后受到的启发。
* 习得性无助
  经历过束手无策的逆境，再遇到逆境时，就会变得消极被动，容易放弃。
  **实验第一部份**
  掌握组：老鼠经历 64 次可避免的电击。
  无助组：老鼠经历 64 次无法避免电击。
  对照组：没有受到电击。
  **实验第二部分**：注射有 50% 概率到死的癌细胞
  掌握组：25% 死亡率
  无助组：75% 死亡率
  对照组：50% 死亡率

## 20150423

#### 做成一件事情

* 选择一个方向：Android 进阶社区
* 持续输入价值：入门，进阶，疑难问题案例分析
* 持续运营：把文章/视频发到热闹的社区引流
* 想像空间：证明团队价值；与更大的世界发生交集；

**注意点：**专注；持续；快乐。忌朝三暮四，左顾右盼。

## 20150419

#### Android Performance Training

* udacity.com 上来自 google 官方的原始资料
  https://www.udacity.com/course/viewer#!/c-ud825/l-3729268966/m-3785788694
* ChinaGDG from youku.com
  整理出几个专题：主要是内存专题和电池专题。同归复习渲染和运算专题。
  http://www.youku.com/playlist_show/id_23494296.html
* 通过示例现场演示几个工具的使用
  Memory Monitor, Heap Viewer, Allocation Tracker
* 可参考的文章
  hukai.me
  http://hukai.me/android-performance-memory


## 20150416

#### wallsplash-android MainActivity.java

* Enum for Java
  definitin of MainActivity.Category
* materialdrawer
  https://github.com/mikepenz/MaterialDrawer
* OpenLibra-Material
  https://github.com/saulmm/OpenLibra-Material
* aboutlibraries
  https://github.com/mikepenz/AboutLibraries
* iconics
  https://github.com/mikepenz/Android-Iconics

#### wallsplash-android ImagesFragment.java

* RecyclerView -> fragment_images.xml
  A flexible view for providing a limited window into a large data set.
  REF: GridLayoutManager, RecyclerView.Adapter
* ActivityOptionsCompat
  Helper for accessing features in android.app.ActivityOptions introduced in API level 16 in a backwards compatible fashion.
* errorview
  https://github.com/xiprox/ErrorView
  A custom view that displays an error image, a title, and a subtitle given an HTTP status code.

#### wallsplash-android UnsplashApi.java

* RxAndroid
  https://github.com/ReactiveX/RxAndroid
  Android specific bindings for RxJava
* RxJava
  https://github.com/ReactiveX/RxJava
  RxJava – Reactive Extensions for the JVM – a library for composing asynchronous and event-based programs using observable sequences for the Java VM
* retrofit
  https://github.com/square/retrofit
  Type-safe REST client for Android and Java by Square, Inc.
* okhttp
  https://github.com/square/okhttp
  An HTTP+SPDY client for Android and Java applications.
* Gson
  https://github.com/google/gson
  Gson is a Java library that can be used to convert Java Objects into their JSON representation. It can also be used to convert a JSON string to an equivalent Java object. Gson can work with arbitrary Java objects including pre-existing objects that you do not have source-code of.
* API
  http://wallsplash.lanora.io/pictures
  http://wallsplash.lanora.io/random

## 20150413

#### 配置 Alfred 来搜索 StackOverflow 和 Github

* StackOverflow
  http://stackoverflow.com/search?q={query}
* Github
  https://github.com/search?q={query}

#### unsplash api

http://tumblr.unsplash.com/api/read?num=10

#### 壁纸应用，图片来自 unsplash

https://github.com/kamidox/wallsplash-android
