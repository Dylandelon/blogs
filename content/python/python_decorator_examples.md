Title: Python装饰器实例
Date: 2014-10-03 20:20
Modified: 2014-10-03 20:20
Tags: python, decorator
Slug: python-decorator-example
Authors: Joey Huang
Summary: 本文介绍Flask里用到的一些Python装饰器实例，进而了解装饰器在产品级代码里的使用。

[TOC]

## Python装饰器入门

如果还不知道Python装饰器是什么东西，可以阅读[这篇文章][1]。它深入浅出地用实例介绍了装饰器，并且还介绍内置装饰器和functools包。另外，[这篇文章][2]对装饰器支持参数传递有一些简单的示例。也可以作为一个入门的参考。

## Flask里使用装饰器的几个例子

### setupmethod

#### 需求

如果web应用程序从运行起处理过一个HTTP请求，这个时候再向Flask添加route规则，则Flask在调试模式下，可以检查出一个APP的错误。为什么这是个错误呢？想像一下，如果一个web应用程序已经上线提供服务了，这个时候由于某些条件触发，向Flask又添加了一个route规则，则说明在添加这个route规则之前，向这个route发送的请求是没有接口可以处理的。

#### 解决方案

Flask定义了`setupmethod`装饰器来确保所有的初始化函数必须在web应用程序开始提供服务之前被调用。如果在已经提供服务之后被调用，则报错。

#### 源码分析

`setupmethod`装饰器源码定义在[app.py][3]里：

    #!python
    def setupmethod(f):
        """Wraps a method so that it performs a check in debug mode if the
        first request was already handled.
        """
        def wrapper_func(self, *args, **kwargs):
            if self.debug and self._got_first_request:
                raise AssertionError('A setup function was called after the '
                    'first request was handled.  This usually indicates a bug '
                    'in the application where a module was not imported '
                    'and decorators or other functionality was called too late.\n'
                    'To fix this make sure to import all your view modules, '
                    'database models and everything related at a central place '
                    'before the application starts serving requests.')
            return f(self, *args, **kwargs)
        return update_wrapper(wrapper_func, f)


* Line 6：这里确保用`setupmethod`装饰的函数在被实际调用之前，都会去检查`self._got_first_request`
* Line 14：这里的`f(self, *args, **kwargs)`确保`setupmethod`装饰器可以装饰任何参数形式的函数
* Line 15: update_wrapper是functools包提供的一个函数。用来确保被装饰的函数依然可以支持Python的反射机制

### locked_cached_property

#### 需求

有些属性的计算比较昂贵，如果这个属性又是非常经常被调用。那么把这个属性计算一次后，缓存起来，以确保下次访问时直接访问计算过的值。这个对性能的优化是比较有帮助的。

#### 解决方案

Flask定义了`locked_cached_property`装饰器来实现上述的需求。同时还提供了锁以保存并发线程访问的安全性。

#### 源码分析

`locked_cached_property`装饰器源码定义在[helpers.py][4]里：

    #!python
    class locked_cached_property(object):
        """A decorator that converts a function into a lazy property.  The
        function wrapped is called the first time to retrieve the result
        and then that calculated result is used the next time you access
        the value.  Works like the one in Werkzeug but has a lock for
        thread safety.
        """

        def __init__(self, func, name=None, doc=None):
            self.__name__ = name or func.__name__
            self.__module__ = func.__module__
            self.__doc__ = doc or func.__doc__
            self.func = func
            self.lock = RLock()

        def __get__(self, obj, type=None):
            if obj is None:
                return self
            with self.lock:
                value = obj.__dict__.get(self.__name__, _missing)
                if value is _missing:
                    value = self.func(obj)
                    obj.__dict__[self.__name__] = value
                return value

Line 1: 注意这里使用类来实现装饰器，而不是我们常见的函数。
Line 14: 这里用RLock来实现并发线程访问安全性。
Line 16: 这里实现了`__get__`，即`locked_cached_property`是一个non-data descriptor类。

我们看一下[app.py][3]里的`name`方法对这个装饰器是怎么使用的：

    :::python
    @locked_cached_property
    def name(self):
        ...

根据python decorator原理，上述代码实际上相当于下面的python代码：

    #!python
    def name(self):
        ...
    name = locked_cached_property(name)


根据python descriptor协议，Line 3的代码实际上就是定义了一个类的只读属性。即访问`app.name`时，实际上执行的是`locked_cached_property.__get__`方法。

这样就实现了`app.name`属性只计算一次，且并发访问安全的需求。当然，实现这一需求的方案有很多种，Flask里使用的这种实现方法优雅且pythonic。更重要的是，它使用了AOP(Aspect-Orient Program)编程思想，提高了代码的可复用性。

!!! Note "专业术语"
    如果你对本文使用的很多专业术语感到困惑，可阅读另外一篇[介绍Python特性]({filename}/python/python_features.md)的文章。它是一个网络上一些优秀文章的资源集合。

[1]: http://www.cnblogs.com/huxi/archive/2011/03/01/1967600.html
[2]: http://www.cnblogs.com/rhcad/archive/2011/12/21/2295507.html
[3]: https://github.com/mitsuhiko/flask/blob/0.10-maintenance/flask/app.py
[4]: https://github.com/mitsuhiko/flask/blob/0.10-maintenance/flask/helpers.py

