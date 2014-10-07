Title: Python特性汇总
Date: 2014-10-04 20:20
Modified: 2014-10-04 20:20
Tags: python
Slug: python-features
Authors: Joey Huang
Summary: 本文汇总了Python一些重要的特性，并收集了网络上介绍这些特性的优秀的文章

Python特性汇总
==============

## 摘要

本文汇总了Python一些重要的特性，并收集了网络上介绍这些特性的优秀的文章。

## Python Decorator

如果你对代码中出现的`@classmethod`感到很困惑，则需要了解一下Python装饰器。

* 入门文章
  [这篇文章][1]是不可多得的装饰器的入门文章，它对内置装饰器和functools包做详细的介绍。
  [这篇文章][2]里对装饰器支持参数传递有一些简单的示例。
* 深入阅读
  如果你对Python Decorator以及开源语言的演进感兴趣，可以深入阅读一些英文的资料。
  [PEP318][4]对Python Decorator进行了官方定义。
  [Python Decorator Wiki][5]更详细地描述了Python Decorator演进的历史。看完这篇文章，对开源语言的演进进程会有个相当直观的了解。

## with语句

`with`语句是从 Python 2.5 开始引入的一种与异常处理相关的功能。它让我们能更加优雅地编写异常处理代码。

* 入门文章
  [这篇文章][3]深入浅出地介绍了with语句产生的背景以及用法。来自IBM developerWorks。
* 深入阅读
  [PEP343][6]对`with`语句进行了官方描述。

## Python Descriptor

如果你对`__get__`，`__set__`，`__del__`等函数的工作机制不了解。那么需要学习一下Python Descriptor协议。

* 入门文章
  [这篇文章][7]对新式类和经典类以及类对象模式进行了较深入全面的介绍。
  [这篇文章][8]是上一篇文章的续集，正式介绍Python Descriptor。
* 深入阅读
  Python官网关于[Descriptor的教程][10]也是一篇非常不错的文章。不过是英文的。
  [另外一篇][9]非常不错的英文文章来自向来质量很高的IBM developerWorks。

[1]: http://www.cnblogs.com/huxi/archive/2011/03/01/1967600.html
[2]: http://www.cnblogs.com/rhcad/archive/2011/12/21/2295507.html
[3]: http://www.ibm.com/developerworks/cn/opensource/os-cn-pythonwith/
[4]: http://legacy.python.org/dev/peps/pep-0318/
[5]: https://wiki.python.org/moin/PythonDecorators
[6]: http://legacy.python.org/dev/peps/pep-0343/
[7]: http://www.cnblogs.com/btchenguang/archive/2012/09/17/2689146.html
[8]: http://www.cnblogs.com/btchenguang/archive/2012/09/18/2690802.html
[9]: http://www.ibm.com/developerworks/library/os-pythondescriptors/
[10]: https://docs.python.org/2/howto/descriptor.html
