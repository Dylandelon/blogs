Title: Werkzeug简介
Date: 2014-10-02 20:20
Modified: 2014-10-02 20:20
Tags: python, wekzeug
Slug: werkzeug-overview
Authors: Joey Huang
Summary: 本文简单介绍了Werkzeug开源项目，然后挖了一个大坑。准备慢慢把这个坑填上。


## 什么是Werkzeug

官网的描述是
> Werkzeug is a WSGI utility library for Python. It's widely used and BSD licensed. -- [Zerkzeug][1]

什么又是WSGI呢？WSGI的全称是Web Server Gateway Interface，它是用来定义web服务器接口的一个规范。简单地讲，就是定义http服务器应该长什么样子，能处理哪些事情。[PEP333][2]就是对这个规范的详细描述。

Werkzeug就是用python对WSGI的实现一个通用库。它是[Flask][3]所使用的底层WSGI库。

[Werkzeug的源码][4]在托管在GitHub，目前的开发还是很活跃的状态。

## Werkzeug包含哪些内容的实现

* HTTP头的解析
* 易用使用的request和response对象
* 基于交互风格的JavaScript脚本语言的浏览器调试器
* 与 WSGI 1.0 规范100%兼容
* 支持Python 2.6, 2.7和3.3
* Unicode支持
* HTTP Session和签名Cookie支持
* URI和IRI处理函数，包含对Unicode的支持
* 内置兼容一些非标准的WSGI服务器和浏览器
* 集成了URLs路由功能

## 关于Werkzeug作者

Werkzeug的作者是[Armin Ronacher][5]，它是个高产的程序员。从Werkzeug，到Flask，再到Jinja2几乎一个人包圆了。它的[博客][6]上也经常分享一些很有价值文章，对Python编程感兴趣的朋友可以读一读。

看到过一个对Werkzeug和Flask源码的评价：
> Most pythonic code and write for human being

## What's next?

挖个大坑：阅读Werkzeug源码，总结一些有价值的信息，写成博文。

[1]: http://werkzeug.pocoo.org/
[2]: http://legacy.python.org/dev/peps/pep-3333/
[3]: http://flask.pocoo.org/
[4]: https://github.com/mitsuhiko/werkzeug
[5]: https://github.com/mitsuhiko
[6]: http://lucumr.pocoo.org/

