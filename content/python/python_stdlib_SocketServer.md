Title: Python SocketServer
Date: 2014-10-05 20:20
Modified: 2014-10-05 20:20
Tags: python, SocketServer
Slug: python-stdlib-socketserver
Authors: Joey Huang
Summary: 本文介绍Python标准库SocketServer

Python SocketServer
===================

## 摘要

本文介绍Python标准库SocketServer。SocketServer标准库简化了编写一个网络服务器的工作。阅读本文需要基本的网络编程知识以及线程和进程的概念。

**注意：**`SocketServer`在Python 3之后被重命名为`socketserver`

## SocketServer概述

### 网络服务种类
SocketServer包里最常用的两个基础服务类：

* `TCPServer`：提供TCP服务的网络服务可以从这个类继承
* `UDPServer`：提供UDP服务的网络服务可以从这个类继承

另外两个不常用，且只在类UNIX系统里可以使用的是`UnixStreamServer`和`UnixDatagramServer`，他们分别提供TCP和UDP的本地服务，一般用来实现进程间通信。

### 网络服务处理请求的方式
这四个类都只能串行地处理请求。即一个请求处理完成之前，新来的请求只能在排队，而无法得到及时处理。这在网络服务器中是不可接受的。解决方案是创建一个单独的进程或线程来处理每个请求。所幸SocketServer包里提供了另外两个工具类来实现请求的并行处理，他们是`ForkingMixIn`和`ThreadingMixIn`，分别实现**进程**和**线程**的并行方案。

### 创建网络服务
创建一个服务需要以下几个步骤：

1. 继承`BaseRequestHandler`类，并重载其`handle()`方法来实现一个请求处理器。
2. 创建一个服务器实例(`TCPServer` or `UDBPServer` etc.)，指定其提供服务的地址和端口，指定请求处理器。
3. 调用服务器实例的`serve_forever()`启动服务。当请求到来时，就会把请求派发给请求处理器处理。

### 多线程并发的注意事项

当使用`ThreadingMixIn`来实现多线程并发处理请求时，需要特别注意，当处理请求的线程意外终止时，网络服务进程需要作何反应。这个类提供了一个属性`daemon_threads`来定义网络服务进程的行为。当`daemon_threads`设置为False（默认）时，表示当处理请求的线程意外终止时，网络服务进程不会退出。而当`daemon_threads`设置为True的时候，如果处理请求的线程意外终止，网络服务进程会退出。

一个并发的UDP网络服务可以简单地通过下面的代码实现：
```python
class ThreadingUDPServer(ThreadingMixIn, UDPServer): pass
```
这里需要注意的是，`ThreadingMixIn`需要写在`UDPServer`之前，因为`ThreadingMixIn`重写了`UDPServer`类里的一些方法。具体原因可阅读Python多继承机制相关资料。

请求处理类`BaseRequestHandler`有两个子类，他们是`StreamRequestHandler`和`DatagramRequestHandler`，分别用来处理TCP请求和UDP请求。在使用时可以直接使用子类以便提供更大的方便性。

如何决定使用**多线程**还是**多进程**来实现并发请求处理？这个没有优劣之分。但需要注意**线程**和**进程**的本质区别，线程间是共享内存的，而进程是运行在独立的地址空间的。假如一个网络服务把状态信息保存在内存里，并且根据内存里的状态信息对请求做出不同的处理，这个时候就需要使用多线程。因为只有多线程才能及时地读到内存中最新的服务状态。如果实现的是HTTP服务器，它的状态信息都保存在文件里，那么多线程或多进程都可以满足要求。

有些时候，实现网络服务并发时，一个更灵活的方式是分部处理，即计算速度快的直接并行处理，而需要的计算量比较大的通过子进程来处理。这个方式就不能通过继承`ThreadingMixIn`来实现，而应该在请求处理器的`handle()`函数里，显式地通过`fork()`来创建一个子进程来实现。

线程和进程毕竟是比较昂贵的系统资源，在系统中线程和进程的数量往往都是有限制的。特别是针对那些TCP服务，一个连接可能持续保持很长时间，导致线程或进程长时间被占用。所以，另外一个方案是，维护一张数组，用来记录那些部分完成的请求，然后使用`select()`函数选择那些已经准备就绪的请求进入下一步处理的流程。具体可参考Python标准库`asyncore`，它提供用这种方式实现并发处理的一些基础设施。

## 类和接口介绍

### BaseServer介绍

`BaseServer`是`TCPServer`和`UDPServer`等服务类的共同父类。它定义了下面的接口，但大部分没有实现。而是由其子类实现。

* BaseServer.fileno()
  返回一个int型的文件描述符，这个文件代表当前服务正在监听的socket接口。当一个进程里有多个网络服务时，就可以使用这个返回值传给`select()`函数用来监测哪个服务已经有请求进来。
* BaseServer.handle_request()
  处理一个请求。这是个阻塞的函数。当服务进入事件循环开始提供服务时，这个接口被调用。当没有请求到来时，这个函数会阻塞在这等待请求的到来或者超时了返回。这个函数依次调用下面函数：`get_request()`，`verify_request()`，`process_request()`，如果用户提供的请求处理器的`handle()`函数抛出异常，服务的`handle_error()`函数将被调用。如果在`self.timeout`秒内没有收到请求，则调用`handle_timeout()`之后，这个函数就返回。
* BaseServer.serve_forever(poll_interval=0.5)
  进入事件循环，开始提供服务，直到`shutdown()`被调用为止。检查`shutdown()`是否被调用的时间间隔默认是0.5秒。
* BaseServer.shutdown()
  停止提供服务。此函数是阻塞函数，会一直等到服务停止后才返回。这个函数必须在`serve_forever()`函数运行的不同线程调用，否则会引起死锁。这个函数是Python 2.6版本新加的。
* BaseServer.RequestHandlerClass
  用户提供的请求处理器类。在处理新的请求时，会创建一个新的类实例给这个请求使用。
* BaseServer.server_address
  服务监听的地址。地址的格式和所使用的协议(TCP/IP or UNIX domain socket)有极大的相关性，具体参阅`socket`模块。如果是IPV4的地址，则其格式是一个包含地址和端口的元组，如`("127.0.0.1", "80")`。
* BaseServer.socket
  服务监听请求的socket实例。
* BaseServer.request_queue_size
  请求队列长度。当服务在处理一个请求时，新来的请求将在这里排除。如果队列长度己满时收到新的请求，则直接会返回一个错误给客户端。默认值是5，子类可以改写这个值。
* BaseServer.timeout
  当服务进入事件循环，开始等待请求到来时，如果超出`timeout`秒还没有请求到来，则会调用`handle_timeout()`。如果这个值是`None`则表示没有超时限制。

### RequestHandler介绍

* RequestHandler.setup()
  在`handle()`调用之前被调用。可以用来做一些初始化工作。默认是空实现。
* RequestHandler.finish()
  在`handle()`返回后被调用。可以用来做一些清理工作。默认是空实现。需要注意的是，如果`setup()`抛出异常，这个函数不会被调用。
* RequestHandler.handle()
  这个函数用来处理请求。默认空实现。一些上下文信息在这个函数里可以使用，`self.request`是请求信息；`self.client_address`是请求的客户端地址；`self.server`是服务实例。`self.request`的类型对TCP和UDP服务是不一样的，对TCP它是socket对象，对UDP是一对字符串和socket对象。可以使用`StreamRequestHandler`和`DatagramRequestHandler`来隐藏这个差异。这两个子类重载了`setup()`和`finish()`方法，然后提供`request.rfile`和`request.wfile`的类文件对象，用来读写数据。读即获取请求数据；写即返回应答数据。

## 例子

一个简单的回显服务。

下面是服务端代码。保存为EchoTCPServer.py。

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    import SocketServer

    class EchoRequestHandler(SocketServer.StreamRequestHandler):
        """ demo request handler """

        def handle(self):
            self.data = self.rfile.readline().strip()
            print("%s write: %s" % (self.client_address, self.data))
            self.wfile.write(self.data.upper())

    if __name__ == "__main__":
        HOST, PORT = 'localhost', 5639

        server = SocketServer.TCPServer((HOST, PORT), EchoRequestHandler)
        print("ECHO TCP server is running ...")
        server.serve_forever()


客户端代码。保存为EchoTCPClient.py

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    import socket
    import sys

    HOST, PORT = 'localhost', 5639
    data = " ".join(sys.argv[1:])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        sock.sendall(data + '\n')

        received = sock.recv(1024)
    finally:
        sock.close()

    print("Send:     %s" % (data))
    print("received: %s" % (received))

先执行服务端`python EchoTCPServer.py`，再执行客户端`python EchoTCPClient.py hello SocketServer`。

服务端输出如下：
```text
D:\lab\python>python DemoTCPServer.py
Echo TCP server is running ...
('127.0.0.1', 51245) write: hello SocketServer
```
客户端输出如下：
```text
D:\lab\python>python EchoTCPClient.py hello SocketServer
Send:     hello SocketServer
received: HELLO SOCKETSERVER
```

## 参考文档

Python官方标准库关于[SocketServer][1]的文档。

[1]: https://docs.python.org/2/library/socketserver.html
