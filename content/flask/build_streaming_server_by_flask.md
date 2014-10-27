Title: 使用Flask搭建一个流媒体服务器
Date: 2014-10-28 01:00
Modified: 2014-10-28 01:00
Tags: python, flask
Slug: build-streaming-server-by-flask
Authors: Joey Huang
Summary: 本文介绍了使用Flask来搭建一个流媒体服务器的方法
Status: draft

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
            frame = camera.get_next_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

    

[1]: http://www.pythonweekly.com/
[2]: http://blog.miguelgrinberg.com/
[3]: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
[4]: http://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
[5]: http://baike.baidu.com/view/4875263.htm


