Title: macOS Sierra 上安装 mysqlclient 问题
Date: 2016-12-22 23:23
Modified: 2016-12-22 23:23
Tags: python
Slug: mysqlclient
Authors: Joey Huang
Summary: macOS Sieria 上安装 mysqlclient 遇到的坑

## 写在前面

好久没有写这种类型的文章了，记录遇到的具体问题。

随着搜索水平的提高，特别是英文搜索水平的提高，这种类型的文章感觉越来越没有价值，因为一搜索就找到了答案。难怪大家说，现在的程序员 = 搜索引擎 + Ctrl+C + Ctrl+V 。

今天写这个文章是因为花了吃奶的力气仍然搜索不到答案，最后还是靠经验和基础知识解决。问题是这样，在 macOS Sierra 上使用 pip 安装 mysqlclient 时遇到错误，无法链接到 libssl 库，系统上明明安装了 openssl 可是就是链接不到。

看到这里，99% 的读者可以关掉这个页面走人了。

## 问题现象

系统安装了 mysql ，使用 `pip install mysqlclient` 时出错，错误信息如下：

```
building '_mysql' extension
creating build/temp.macosx-10.6-intel-3.5
/usr/bin/clang -fno-strict-aliasing -Wsign-compare -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -arch i386 -arch x86_64 -g -Dversion_info=(1,3,9,'final',1) -D__version__=1.3.9 -I/usr/local/Cellar/mysql/5.7.16/include/mysql -I/Library/Frameworks/Python.framework/Versions/3.5/include/python3.5m -c _mysql.c -o build/temp.macosx-10.6-intel-3.5/_mysql.o -fno-omit-frame-pointer
/usr/bin/clang -bundle -undefined dynamic_lookup -arch i386 -arch x86_64 -g build/temp.macosx-10.6-intel-3.5/_mysql.o -L/usr/local/Cellar/mysql/5.7.16/lib -lmysqlclient -lssl -lcrypto -o build/lib.macosx-10.6-intel-3.5/_mysql.cpython-35m-darwin.so
ld: library not found for -lssl
clang: error: linker command failed with exit code 1 (use -v to see invocation)
error: command '/usr/bin/clang' failed with exit status 1
```

错误出现的系统是 macOS Sierra, 在 EI Capitan 上安装没有遇到这个问题。

## 问题分析

系统上明明装了 openssl 库，可是为什么找不到 libssl 呢？找了一堆答案都是教大家用 `brew link --force openssl` ，可是这个方法对 macOS Sierra 无效。原因是苹果现在不用 openssl 了，而是使用自己维护的加密算法库。为什么要这样做，不得而知，或许是被 openssl 经常爆出的滴血漏洞伤透了心吧。

所以，要在 mac 上链接 ssl 库，需要指定库的路径，即加上 `-L/usr/local/opt/openssl`，把这个目录加进库的搜索路径即可。

细心的人在用 `brew install openssl` 时会注意到下面的信息：

```
This formula is keg-only, which means it was not symlinked into /usr/local.

Apple has deprecated use of OpenSSL in favor of its own TLS and crypto libraries

Generally there are no consequences of this for you. If you build your
own software and it requires this formula, you’ll need to add to your
build variables:

LDFLAGS: -L/usr/local/opt/openssl/lib
CPPFLAGS: -I/usr/local/opt/openssl/include
PKG_CONFIG_PATH: /usr/local/opt/openssl/lib/pkgconfig
```

## 解决方案

1. 从 Github 上下载 [mysqlclient 源码](https://github.com/PyMySQL/mysqlclient-python/archive/1.3.9.tar.gz)
2. 进入项目的 virtualenv 环境。为什么要这一步，因为我们希望把 mysqlclient 安装到项目所在的 python 运行环境中
3. 运行 `python setup.py install`，这个时候肯定还是报错的
4. 拷贝命令台上的最后一个报错的命令，在 `-L/usr/local/Cellar/mysql/5.7.16/lib` 后面增加如下内容 `-L/usr/local/opt/openssl`，然后回车再执行一遍这个命令
5. 再次运行 `python setup.py install` 即可成功安装

当然，这个做法是偷懒的做法。真正优雅一点的是修改 mysqlclient 的编译脚本，直接把 ssl 库增加进去。或许还可以向开发者提个 PR 来解决这个问题。




