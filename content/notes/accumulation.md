Title: 日积月累
Date: 2015-04-13 00:19
Modified: 2015-04-13 00:19
Slug: accumulation
Authors: Joey Huang
Summary: 日积月累
Status: draft

[TOC]

## 20160406

### Pelican 代码阅读

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

## 20150423

#### 做成一件事情

* 选择一个方向：Android 进阶社区
* 持续输入价值：入门，进阶，疑难问题案例分析
* 持续运营：把文章/视频发到热闹的社区引流
* 想像空间：证明团队价值；与更大的世界发生交集；

**注意点**：专注；持续；快乐。忌朝三暮四，左顾右盼。

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


## 20160615

最高效的深度拷贝库: https://github.com/ivolovikov/fastest-clone

* javascript 元编程：利用 `new Function('params', 'function body')` 或 `eval('code')` 来进行实现函数
* javascript 元编程：利用 `Function.prototype.call()` 或 `Function.prototype.apply()` 来对函数进行调用
* 判断是否在 node.js 环境： `if (typeof module == 'object' && typeof module.exports == 'object')`
* 递归获取 Object 实例的所有属性以及属性的属性：`_getKeyMap: function (source, deep, baseKey, arrIndex)`

Node.js Design Patterns: Chapeter 1 Node.js Design Fundamentals

### The reactor pattern

* I/O is slow: 与内存访问速度在 GB/s 数量级；磁盘的访问速度在 MB/s 数量级。
* Blocking I/O:　阻塞式访问 I/O ，需要用多线程机制来处理并发。需要增加线程锁和线程数据同步，增加了复杂性。
* Non-blocking I/O: 使用非阻塞式 I/O 的一个方案是忙等待 (Busy Wait)，即不停地调用 I/O 函数，直到读出数据或出错为止。这种方案较浪费 CPU 。
* Event demultiplexing: 多路事件分解器来提高使用非阻塞 I/O 的效率。把所有待监控的资源都放在一个数组里，交给事件分解器来监视，当资源上有事件发生（比如有数据可供读取）时，监视动作返回，再去读取数据。当没有事件发生时，监控函数会进入睡眠状态，把 CPU 让给别的程序。这一编程模式类似用 `select` 函数实现异步 Socket 编程。
* The reactor pattern: 反应堆模式。比 Event demultiplexing 更进一步。直接给资源的操作提供一个 Handler 作为回调函数。当资源可用时，直接调用回调函数。实现完整的异步 I/O 编程模式。
* libuv: The non-blocking I/O engine of Node.js。不同的操作系统有各种的 Event demultiplexing 机制，比如 Linux 下的 `epoll`，Mac OS X 下的 `kqueue`，Windows 下的 I/O Completion Port API (IOCP)。不同平台的事件分发机制不同，且同一个平台下不同的资源的异步模式也不同。比如 Unix 下 socket 支持异步 I/O，而普通的文件系统 API 则不支持异步 I/O，这个时候就需要用单独的线程来模拟异步文件读写操作。libuv 库就是为了解决这些问题而产生的。它向 javascript 提供了不同操作系统，不同资源的异步 I/O 的抽像封装和实现。
* The recipe for Node.js: Node.js 包含以下几部分
  * 操作系统底层接口的封装，并暴露给 javascript 调用，如 libuv 等
  * V8, 这是 Google 给 Chrome 开发的高性能的 javascript 引擎
  * node.js 核心库 (node-core)，实现 Node.js 的高层 API


## 20160616

Node.js Design Patterns: Chapeter 1 Node.js Design Fundamentals

### The callback pattern

* The continuation-passing style: CPS 把函数作为参数传递，完成回调
  * Synchronous continuation-passing style：同步回调，即函数返回后，回调也己调用了。
  * Asynchronous continuation-passing style：异步回调，即函数返回后，回调还没被调用，回调会被推送到 event queue 里，在下一轮的 event loop 里调用回调。比如使用 `setTimeout()`， `process.nextTick()` 来实现。
  * Non continuation-passing style callbacks：非 CPS 方式的回调。比如 `Array.map()` 的回调函数，通过回调函数的返回值直接交互。
* Synchronous or asynchronous?：同步还是异步？
  * An unpredictable function：同步和异步不可预见性，即[有时是同步回调，有时是异步回调](#an_unpredictable_function)。这种问题会引入非常难查的 bug 。
  * Using synchronous APIs：改装成同步 API，比如通过 `fs.readFileSync()` 函数来实现。不推荐使用这种方式，会破坏 Node.js 的异步 I/O 模式。一个判断标准是：Use blocking API only when they don't affect the ability of the application to serve concurrent requests.
  * Deferred execution：延后执行，把 API 改装成异步回调。通过 `process.nextTick()` 实现。需要注意在 event loop 里的优先级。
* Node.js callback conventions: Node.js 的回调惯例
  * Callbacks come last: 把回调放在最后一个参数，这样在使用的时候，可以直接用匿名函数或箭头函数实现。如 `fs.readFile(filename, [options], callback)` 。
  * Error comes first: 把错误放在第一个参数。在 Node.js 里，CPS 风格的回调的第一个参数通常是错误信息，数据结果在第二个及之后的参数提供。如果没有出错，第一个参数的值为 `null` 或 `undefined` 。如 `fs.readFile('foo.txt', 'utf8', function(err, data) {}` 。
  * Propagating errors: 错误传递机制。同步调用时，错误传递机制通过 `throw` 来抛出异常，这样可以使错误在调用栈里往上跳，直到它被处理为止。而在异常调用里，异常处理的机制是，在 CPS 回调链里，通过回调函数一层层往上传递。可参阅[示例代码](#propagating_errors)。
  * Uncaught exceptions: 未处理的异常可以通过 `process.on('uncaughtException', function(err){}` 来捕获到。系统默认是直接退出程序。一般的处理是在这里记录异步 Log ，然后退出程序。针对网络服务而言，退出程序重启总是保证持续服务可用的一个折衷策略。

<a name="an_unpredictable_function"></a>**同步或异步不可预测的函数**

```javascript
var fs = require('fs');
var cache = {};
function inconsistentRead(filename, callback) {
  if(cache[filename]) {
    //invoked synchronously
    callback(cache[filename]);
  } else {
    //asynchronous function
    fs.readFile(filename, 'utf8', function(err, data) {
      cache[filename] = data;
      callback(data);
    });
  }
}
```

<a name="propagating_errors"></a>**异步回调的异常处理**

```javascript
var fs = require('fs');
function readJSON(filename, callback) {
  fs.readFile(filename, 'utf8', function(err, data) {
    var parsed;
    if(err)
      //propagate the error and exit the current function
      return callback(err);
    try {
      //parse the file contents
      parsed = JSON.parse(data);
    } catch(err) {
      //catch parsing errors
      return callback(err);
    }
    //no errors, propagate just the data
    callback(null, parsed);
  });
};
```

## 20160620

Node.js Design Patterns: Chapeter 1 Node.js Design Fundamentals

### The module system and its patterns

模块系统是 Node.js 的代码结构化的基础，实现信息隐藏和接口实现的功能。

* The revealing module pattern: 模块系统的本质是利用函数来创建具有信息隐藏功能的代码块。函数内的嵌套函数及变量对模块外部不可见，只有函数返回的属性和方法才对外可见。
* Node.js modules explained: 官方文档 [Node.js 模块系统](https://nodejs.org/api/modules.html) 是最权威且最清晰的资料。
* module.exports vs exports: The variable exports is just a reference to the initial value of module. exports。
* require is synchronous
* The resolving algorithm
  * File modules: 以 `/` 或 `./` 或 `../` 开头的参数，解释为文件模块
  * Core modules: 如果没有以路径开头，则解释为 Node.js 核心内置模块，如 `var fs = require(fs);` 。
  * Package modules: 如果没有核心模块与之匹配，则查找当前目录下的 `node_modules` 目录下查找匹配的模块，如果找不到，则查找从父目录的 `node_modules` 目录下查找，直至根目录下的 `node_modules` 。
  * 文件模块/包模块匹配策略
    * `moduleName.js`
    * `moduleName/index.js`
    * The `main` property of `moduleName/package.json`
* Solution for **Dependency Hell**: 按照上述模块搜索算法，每个模块都可以通过自己的 `node_modules` 子目录指定其依赖的子模块。这样即使同一个应用程序里不同模块引用了相同的子模块，他们各自独立，可以是不同的版本。
* The module cache: 模块缓存可以解决几个问题
  * 循环引用问题
  * 确保引用的一致性
  * 加快效率
* Cycles: 模块循环引用问题，A require B, B require A
* Module de nition patterns
  * Named exports: `exports.info = function(message) { ... }`
  * Exporting a function: `module.exports = function(message) { ... }`
  * Exporting a constructor: [示例代码](#exporting_a_constructor)
  * Exporting an instance: [示例代码](#exporting_an_instance)。巧妙地利用模块的缓存功能，使每个引用此模块的模块都引用了同一个实例。这样就实现了单例 (Singleton) 模式。
* Modifying other modules or the global scope: 不是好的实践，但在自动测试领域有其应用场景，我们称之为猴子补丁 (Monkey Patching) 。[示例代码](#monkey_patching) 。

<a name="exporting_a_constructor"></a>**模块返回构造函数**

```javascript
//file logger.js
function Logger(name) {
 this.name = name;
};
Logger.prototype.log = function(message) {
 console.log('[' + this.name + '] ' + message);
};
Logger.prototype.info = function(message) {
 this.log('info: ' + message);
};
Logger.prototype.verbose = function(message) {
 this.log('verbose: ' + message);
};
module.exports = Logger;
```

<a name="exporting_an_instance"></a>**模块返回一个实例/单例**

```javascript
// file logger.js
function Logger(name) {
  this.count = 0;
  this.name = name;
};

Logger.prototype.log = function(message) {
  this.count++;
  console.log('[' + this.name + '] ' + message);
};
module.exports = new Logger('DEFAULT');
```

<a name="monkey_patching"></a>**猴子补丁**

```javascript
// file patcher.js
// ./logger is another module
require('./logger').customMessage = function() {
  console.log('This is a new functionality');
};

// Using our new patcher module would be as easy as writing the following code:
// file main.js
require('./patcher');
var logger = require('./logger');
logger.customMessage();
```

## 20160621

### rethinkdb

提供在线数据库，提供数据的增删改查。一大亮眼特性是 changefeed。它能够把数据库中某个查询结果集的改变 publish 出来，供其他人 subscribe。这个特性对 realtime collaboration 的 app 来说非常有用。可以实现数据实时同步。

什么样的场景适合使用 rethinkdb ?

* Collaborative web and mobile apps
* Streaming analytics apps
* Multiplayer games
* Realtime marketplaces
* Connected devices

### leancloud

提供在线非结构化数据库，提供数据的增删改查。辅助类，提供实时聊天及推送，流量分析等功能。

### wilddog

国内的 BaaS (Backend as a Service) 平台。提供两大功能：

* 实时同步: 提供毫秒级实时数据同步。使用 TLS + websocket 保障通信安全。不支持 websocket 的环境使用 long-polling 模拟长连接。保障通信实时性。即一个数据修改后，另外一个订阅者可以马上得到同步。
* 在线 Json 数据库：提供数据的增删改查功能。

### 带网关的 IoT 系统通信需求

* 安全性：通信安全 (TLS) 及访问授权 (Auth)
* 实时性：控制命令和状态能及时送达，达到毫秒级实时性
* 双向通信：不同于 request/response 响应模型。App 与 Gateway，App 与 Server 之间必须支持双向实时通信。
* 一致性：App 与 Gateway 之间；App 与 Server 之间需要实现一致的通信协议和通信模型，减少系统复杂度和开发工作量。

### websocket & long-polling

* [RFC 6455 - The WebSocket Protocol](http://tools.ietf.org/html/rfc6455)
* [WebSocket API Specification](http://www.w3.org/TR/websockets/)
* [socket.io](http://socket.io): A powerful cross-platform WebSocket API for Node.js

### XaaS

> 传统云服务公司的定义：SaaS、PaaS、IaaS。越往下自由度越高，越往上使用起来越简单。
> SaaS解决的是开箱即用的问题，不用写代码，直接用。PaaS解决的是运维的问题，写完代码往云端一扔，搞定。而IaaS解决的是硬件资源弹性扩容的问题，像个水龙头，用多少拧多少。
> 目前PaaS代表的产品比如HeroKu，Google App Engine、国内SAE等，几乎全线已挂或半死不活。PaaS挂掉的原因是没有解决根本问题，半吊子。又不简单，又不自由。
> 广义BaaS是指用户需要通过远程API获得服务的云服务产品。比如类似统计服务MixPanel、友盟等。狭义的BaaS是指通过远程API提供计算和存储资源的产品，比如Parse、Firebase、Twilio、Pusher，Apple Cloud Kit这样的产品。

REF: http://www.leiphone.com/news/201605/UQ4LxnsXfxqv2r39.html

## 20160622

Node.js Design Patterns: Chapeter 1 Node.js Design Fundamentals

### The observer pattern

The observer pattern is already built into the Node.js core and is available through the `EventEmitter` class.

* EventEmitter 类的用法，可以手动创建一个 `EventEmitter` 实例来使用。
* 错误处理：不能直接抛出异常，因为事件回调一般在单独的消息循环里处理，抛出的异常会丢失。一个通用的做法是定义一个独立的 `error` 事件，然后 `emmit` 这个事件。
* Make any object observable：通过继承 `EventMitter` 来实现。ES5 可以通过 `util.inherits()` 实现，ES6 可以直接用 `inherit` 关键字实现。
* Synchronous and asynchronous events: 同步事件和异常事件
* EventEmitter vs Callbacks: 应该用哪个呢？
  * semantic: callbacks should be used when a result must be returned in an asynchronous way; events should instead be used when there is a need to communicate that something has just happened.
  * 如果一个事件可能发生多次，或者可能根本不会发生，使用 EventEmitter 是较好的选择
  * 使用 EventEmitter 可以让多个监听者同时监听到事件。而 callback 是一对一的结果返回。
* Combine callbacks and EventEmitter: 结合两者的优势。

```javascript
var glob = require('glob');
glob('data/*.txt', function(error, files) {
  console.log('All files found: ' + JSON.stringify(files));
}).on('match', function(match) {
  console.log('Match found: ' + match);
});
```

关于 `EventEmitter` 可参阅[官方资料](https://nodejs.org/dist/latest-v6.x/docs/api/events.html) 。

## 20160624

Node.js Design Patterns: Chapeter 2 Asynchronous Control Flow Patterns

### The difficulties of asynchronous programming

**The callback hell**: 使用 `request` 和 `mkdirp` 实现的一个简单的爬虫程序，可以明显地看到异步流程控制代码很容易陷入 callback hell 的陷阱。如[示例程序](#callback_hell)。callback hell 的代码有如下问题：

* 可读性差：很难界定回调函数的起始位置和结束位置
* 变量名重叠：比如回调函数里的错误码 `err` 在每个回调函数里都有，容易引起误解
* 闭包函数会引起少量的内存和性能问题，比如内存泄露

<a name="callback_hell"></a>**爬虫程序：callback hell**

```javascript
function spider(url, callback) {
    var filename = utilities.urlToFilename(url);
    fs.exists(filename, function(exists) {                              //[1]
        if(!exists) {
            console.log("Downloading " + url);
            request(url, function(err, response, body) {                //[2]
                if(err) {
                    callback(err);
                } else {
                    mkdirp(path.dirname(filename), function(err) {      //[3]
                        if(err) {
                            callback(err);
                        } else {
                            fs.writeFile(filename, body, function(err) { //[4]
                                if(err) {
                                    callback(err);
                                } else {
                                    callback(null, filename, true);
                                } });
                        } });
                } });
        } else {
            callback(null, filename, false);
        } });
}
```

### Using plain JavaScript

使用 JavaScript 的一些通用规则可以避免 callback hell 问题。

**Callback discipline**: 编写回调函数的一些原则

* You must exit as soon as possible. 尽早返回。即先处理错误。
* You need to create named functions for callbacks. 给回调创建命名函数。
* You need to modularize the code. Split the code into smaller, reusable functions whenever it's possible.

下面是按照编写回调函数的原则执行后的改进版本：

```javascript
function saveFile(filename, contents, callback) {
    mkdirp(path.dirname(filename), function(err) {
        if(err) {
            return callback(err);
        }
        fs.writeFile(filename, contents, callback);
    });
}

function download(url, filename, callback) {
    console.log('Downloading ' + url);
    request(url, function(err, response, body) {
        if(err) {
            return callback(err);
        }
        saveFile(filename, body, function(err) {
            console.log('Downloaded and saved: ' + url);
            if(err) {
                return callback(err);
            }
            callback(null, body);
        });
    });
}

function spider(url, callback) {
    var filename = utilities.urlToFilename(url);
    fs.exists(filename, function(exists) {
        if(exists) {
            return callback(null, filename, false);
        }
        download(url, filename, function(err) {
            if(err) {
                return callback(err);
            }
            callback(null, filename, true);
        })
    });
}
```

**Sequential execution**: 顺序执行

爬虫程序就是一个典型的顺序执行的程序。文件是否存在 -> 从网络下载 -> 新建文件夹 -> 写文件。对己知的顺序执行的异步任务，可以使用下面的代码模板：

```javascript
function task1(callback) {
    asyncOperation(function() {
        Start Task 1 Task 2 Task 3 End
        task2(callback);
    });
}

function task2(callback) {
    asyncOperation(function(result) {
        task3(callback);
    });
}

function task3(callback) {
    asyncOperation(function() {
        callback();
    });
}

task1(function() {
    //task1, task2, task3 completed
});
```

**Sequential iteration**: 异步遍历序列数据

* `task()` 函数最好是异步函数，如果是同步函数，可能造成深度递归，从而使栈溢出

```javascript
function iterate(index) {
    if(index === tasks.length)  {
        return finish();
    }
    var task = tasks[index];
    task(function() {
        iterate(index + 1);
    });
}

function finish() {
    //iteration completed
}

iterate(0);   // start iterate sequence asynchronize
```

**思考**

* 使用异步遍历序列数据的方法，实现爬虫的另外一个版本：递归下载网页和网页里的所有链接。注意，只下载相同域名下的链接。
* 更一般化地抽你异步遍历模型，可以实现如下函数签名的异步遍历函数 `iterateSeries(collection, iteratorCallback, finalCallback)` 。

## 20160627

Node.js Design Patterns: Chapeter 2 Asynchronous Control Flow Patterns

### Parallel execution

如果多个任务没有先后顺序上的依赖，那么可以使用并行执行的模型来实现。当任务全部完成后，通过回调函数通知调用者。

```javascript
var tasks = [...];
var completed = 0;

tasks.forEach(function(task) {
    task(function() {
        if(++completed === tasks.length) {
            finish(); }
    });
});

function finish() {
    //all the tasks completed
}
```






