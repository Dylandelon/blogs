Title: 使用Flask搭建一个流媒体服务器
Date: 2014-10-28 23:25
Modified: 2014-10-28 23:25
Tags: python, flask
Slug: build-streaming-server-by-flask
Authors: Joey Huang
Summary: 本文翻译自PythonWeekly上的一篇文章，介绍了使用Flask来搭建一个流媒体服务器的方法。

[TOC]

## 摘要

收到前不久订阅的[PythonWeekly][1]发过来的一个邮件通知，由[Miguel][2]写的一篇介绍如何使用Flask搭建一个流媒体服务器的文章，思路很新颖也很有意思。你可以点击[这里][3]阅读英文原文。或者跟随本文跟我一起体验一把搭建一个流媒体服务器的过程吧。

## 理论基础

流媒体有两大特点，一是数据量大。二是有实时性要求。针对这两个特点，我们必须把应答数据分块传输给客户端来实现流媒体服务器。这里我们用到了两个关键技术来实现流媒体服务器，我们使用生成器函数来把数据分块传送，Flask的`Response`类本身对生成器函数有良好的支持。接着，我们使用**Multipart**来组装一个HTTP应答。

### 生成器函数

生成器函数是可被打断和恢复的函数。其关键字是`yield`，来看一个例子：

    :::python
    def gen():
        yield 1
        yield 2
        yield 3

上面的代码我们就定义了一个生成器函数，当生成器函数被调用时，它返回一个生成器迭代器，或直接叫生成器。通过不断地调用生成器的`next()`方法来执行生成器函数体的代码，直到遇到异常为止。

    :::python
    >>> g = gen()
    >>> g
    <generator object gen at 0xb72330a4>
    >>> g.next()
    1
    >>> g.next()
    2
    >>> g.next()
    3
    >>> g.next()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration

从上面的例子可以看到一个生成器函数可以返回多个结果。每当程序执行到`yield`语句时，函数现场会被保留，同时返回一个值。Flask就是利用这个特性把应答数据通过生成器分块发送给客户端。

### Multipart应答

Multipart应答包含一个*multipart*媒体类型，后面跟着多块独立的数据，每块数据有自己的*Content-Type*，每块数据之间通过*boundary*分隔。下面是一个例子：

    :::text
    HTTP/1.1 200 OK
    Content-Type: multipart/x-mixed-replace; boundary=frame

    --frame
    Content-Type: image/jpeg

    <jpeg data here>
    --frame
    Content-Type: image/jpeg

    <jpeg data here>
    ...

Multipart有多种不同的类型，针对流媒体，我们使用`multipart/x-mixed-replace`。浏览器处理这种Multipart类型时，会使用当前的块数据替换之前的块数据。这刚好就是我们想要的流媒体的效果。我们可以把媒体的一帧数据打包为一个数据块，每块数据有自己的*Content-Type*和可选的*Content-Length*。浏览器逐帧替换，就实现了视频的播放功能。[RFC1341][4]对Multipart媒体类型进行了详细的描述，有兴趣的朋友可移步参考。

## 实现流媒体服务器

上面介绍了实现流媒体服务器的理论知识。接下来我们使用这些知识来用Flask搭建一个流媒体服务器。

有多种方法可以在浏览器里实现流媒体播放，和Flask配合较好的是使用[Motion JPEG][5]的方法。简单地讲，就是把视频画面通过JPEG图片的方式，一帧一帧地发送给浏览器。这也是很多IP Camera使用的流媒体播放方式，它实时性很好，但视频效果不是很理想。因为Motion JPEG对视频的压缩效率太低了。

    #!/usr/bin/env python
    from flask import Flask, render_template, Response
    from camera import Camera

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

这个Flask应用程序导入了一个`Camera`类，这个类是为了持续不断地提供视频的帧数据的类。这个程序提供了两个服务路径，`/`路径由`index.html`模板提供服务，下面是它的内容：

    :::html
    <html>
      <head>
        <title>Video Streaming Demonstration</title>
      </head>
      <body>
        <h1>Video Streaming Demonstration</h1>
        <img src="{{ url_for('video_feed') }}">
      </body>
    </html>

这是一个非常简单的HTML网页。其中关键的是`img`这个标签，它定义了一张图片元素，其URL是`/video_feed`。从Flask应用程序代码的Line17-20可以知道，`/video_feed`是由一个`video_feed()`方法提供服务的，它返回的是一个multipart应答。这个应答的内容是由生成器函数`gen()`提供的。而`gen()`函数就是不停地从camera里获取一帧一帧的图片，并通过生成器返回给客户端。客户端浏览器在收到这个流媒体时，会在`img`标签定义的图片里，逐帧地显示图片，这样一个视频就播放出来的。目前市面上绝大部分浏览器都支持这个功能。

## 模拟视频帧数据

现在只要实现`Camera`类，并提供源源不断的视频帧数据即可运行上面的程序了。由于连接摄像头涉及到硬件，我们使用一个简单的模拟器来源源不断地返回数据：

    #!/usr/bin/env python
    from time import time

    class Camera(object):
        def __init__(self):
            self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

        def get_frame(self):
            return self.frames[int(time()) % 3]

这个代码很简单，它从本地读取三个图片，并根据当前时间，每秒返回不同的图片来模拟提供源源不断的视频帧数据。

大家可以从原作者的GitHub上下载程序的代码来运行。

    :::shell
    $ git clone https://github.com/miguelgrinberg/flask-video-streaming.git

或者直接下载[ZIP][6]包来运行。

下载完代码，进入代码根目录，执行`python app.py`。然后在浏览器里打开`http://localhost:5000`即可以看到模拟的视频了。

!!! Note "安装Flask"
    要运行上述代码，需要先安装Flask。[官网][9]上有教程，简单易懂。

## 连接硬件摄像头

下载代码的同学应该可以看到代码里还有一个`camera_pi.py`的文件，这个是用来实现真正的连接硬件摄像头的代码。原文作者使用的摄像头是[Raspberry Pi][7]，这是个类似Arduino的开源的硬件项目。

## 一些限制

当客户端浏览器打开上述流媒体服务的网址时，它就独占了这个线程。在把Flask应用Deploy到Nginx+uwsgi服务器上时，它能服务的最大客户端数目为应用程序的线程数，一般就是几个到几十个。而如果是在本机使用`python app.py`运行的测试服务器，则只能服务一个客户端。

针对这个问题，原文作者提供了一个解决方案。使用[gevent][8]来解决。

> gevent is a coroutine-based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libev event loop.

有兴趣的同学可以在原代码的基础上，引入gevent来支持多客户端。


[1]: http://www.pythonweekly.com/
[2]: http://blog.miguelgrinberg.com/
[3]: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
[4]: http://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
[5]: http://baike.baidu.com/view/4875263.htm
[6]: https://github.com/miguelgrinberg/flask-video-streaming/archive/master.zip
[7]: http://baike.baidu.com/view/5730914.htm
[8]: http://www.gevent.org/
[9]: http://flask.pocoo.org/


