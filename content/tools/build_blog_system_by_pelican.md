Title: 使用Pelican搭建博客系统
Date: 2014-10-26 23:20
Modified: 2014-10-26 23:20
Tags: python, pelican
Slug: build-blog-system-by-pelican
Authors: Joey Huang
Summary: 本文介绍了Pelican的特性；选择Pelican的理由以及从头安装配置，搭建出一个可运行的独立博客系统。最后给出我自己的最佳实践描述。

[TOC]

## 摘要

经过几天的折腾，用Pelican搭建的独立博客系统终于上线运行了。可以打开[kamidox.com][17]看一下效果图。由于选用了响应式网页设计的主题，所以在手机上的浏览效果也相当赞。本文介绍了Pelican的特性；选择Pelican的理由以及从头安装配置，搭建出一个可运行的独立博客系统。最后给出我自己的最佳实践描述。

## Pelican介绍

### 什么是Pelican

[Perlican][3]是用Python实现的一个静态网站生成器，支持[reStructuredText][1]或[Markdown][2]。它支持以下功能：

* 博客文章和静态网页
* 支持评论。评论是通过第三方服务[Disqus][9]支持的。即评论数据保存在第三方服务器上
* 主题支持
* 把博客文章生成PDF格式文档
* 多语言博客支持，如可以用英文和中文写同一篇博客。不同语言访问者访问相应语言的博文
* 支持Atom/RSS订阅
* 博文中代码高亮支持
* 博客搬家支持(WordPress, Dotclear, 或RSS feeds)
* 支持插件，如Twiter, Google Analytics等

### 为什么选择Pelican

首先排除掉WordPress之类的CMS系统。因为我不想要数据库，我只需要一个轻量级的静态网站生成器。我的博客使用Markdown编写，且保存在GitHub上。我想要的，只是用Markdown写完博客之后，git commit + git push即可直接发布到博客网站上。

[这篇文章][4]介绍了32个各种语言实现的博客引擎，而[这篇文章][5]介绍了５个最轻量级的静态网站生成器。最终选择Pelican是基于如下原因：

* 使用Python实现。由于最近在学习Python，我可以阅读源码并按照我的需求来改造Pelican使之完全符合我的需求。下次学习Ruby，用[jekyll][11]再折腾一遍。因为Jekyll是用Ruby实现的。且GitHub Pages的后台就是用Jekyll，到时可直接用GitHub Pages实现个人博客。
* 足够轻量级。总的代码量才1MB多。安装也方便。
* 有一堆现成的主题可以使用。这对我这种非专业前端的开发者来说，省了不少事。
* 文档齐全。
* 开发活动活跃。GitHub上代码提交活跃。上面文章里介绍的很多博客系统基本上都2+年前就停止更新了。

最后两点对使用任何开源工具来说都是很重要的，只有开发活跃，社区资源多，文档齐全，遇到问题的时候才能较快地得到解决。

## Pelican安装与配置

### 安装Pelican并创建项目

详细的信息可以参阅[Pelican官方文档][10]。假设电脑上已经安装Python和pip。首先，通过pip安装pelican和markdown：

    :::shell
    pip install pelican markdown

然后创建你的博客项目：

    :::shell
    mkdir ~/blogs
    cd ~/blogs
    pelican-quickstart

在运行pelican-quickstart时，系统会问一系列问题，比如你的博客网址啊，作者名字啊之类的，根据真实情况填写即可，这些问题只是用来生成配置文件的，我们后面都可以通过修改配置文件来手动修改这些设置。我填写的内容如下：

    #!shell
    kamidox@kamidox-laptop:~/lab/blogs$ pelican-quickstart
    Welcome to pelican-quickstart v3.4.0.

    This script will help you create a new Pelican-based website.

    Please answer the following questions so this script can generate the files
    needed by Pelican.

    > Where do you want to create your new web site? [.]
    > What will be the title of this web site? kamidox
    > Who will be the author of this web site? Joey Huang
    > What will be the default language of this web site? [en]
    > Do you want to specify a URL prefix? e.g., http://example.com   (Y/n)
    > What is your URL prefix? (see above example; no trailing slash) http://kamidox.com
    > Do you want to enable article pagination? (Y/n) Y
    > How many articles per page do you want? [10]
    > Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) Y
    > Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n)
    > Do you want to upload your website using FTP? (y/N) N
    > Do you want to upload your website using SSH? (y/N) y
    > What is the hostname of your SSH server? [localhost] kamidox.com
    > What is the port of your SSH server? [22]
    > What is your username on that server? [root] ubuntu
    > Where do you want to put your web site on that server? [/var/www] /home/ubuntu/blogs
    > Do you want to upload your website using Dropbox? (y/N) N
    > Do you want to upload your website using S3? (y/N) N
    > Do you want to upload your website using Rackspace Cloud Files? (y/N) N
    > Do you want to upload your website using GitHub Pages? (y/N) N
    Done. Your new project is available at /home/kamidox/lab/blogs

其中第14行的`http://kamidox.com`以及第21行的`kamidox.com`是我的域名，如果你只是在本机试验，可以填localhost。创建完项目后，目录下看起来象这样。

    :::shell
    kamidox@kamidox-laptop:~/lab/blogs$ tree
    .
    ├── content     # 这个就是放博客内容目录，这个目录及子目录下的所有md和rst文件将会被转成html文件
    ├── develop_server.sh   #这个是用来在本地运行一个服务器来实时查看生成的html文档的脚本
    ├── fabfile.py  # 这个是使用Python的fabric来实现文件上传的工具，即Deploy工具
    ├── Makefile    # 这个是使用是用来生成网站内容并上传的工具。后文详细解释
    ├── output      # 这个是从content目录生成的html目标文件的存放目录
    ├── pelicanconf.py      # 这个是本地开发时的配置文件
    └── publishconf.py      # 这个是发布时的配置文件

    2 directories, 5 files

### 配置pelicanconf.py和publishconf.py

Pelican的配置文件是直接用Python写的，我本地开发配置文件`pelicanconf.py`内容如下：

    #!/usr/bin/env python
    # -*- coding: utf-8 -*- #
    from __future__ import unicode_literals

    AUTHOR = u'Joey Huang'
    SITENAME = u"kamidox.com"
    SITEURL = 'http://localhost'
    DISQUS_SITENAME = 'kamidox'

    PATH = 'content'

    TIMEZONE = 'Asia/Shanghai'

    DEFAULT_LANG = u'zh_CN'
    DEFAULT_DATE_FORMAT = ('%Y-%m-%d(%A) %H:%M')

    USE_FOLDER_AS_CATEGORY = True
    DEFAULT_CATEGORY = 'hide'

    # Feed generation is usually not desired when developing
    FEED_ATOM = 'feeds/atom.xml'
    FEED_RSS = 'feeds/rss.xml'
    FEED_ALL_ATOM = None
    FEED_ALL_RSS = None
    CATEGORY_FEED_ATOM = None
    TRANSLATION_FEED_ATOM = None

    # menu items
    MENUITEMS = [('Home', SITEURL),
                ('About', 'about.html'),]

    DEFAULT_PAGINATION = 10
    MD_EXTENSIONS = [
            "extra",
            "toc",
            "headerid",
            "meta",
            "sane_lists",
            "smarty",
            "wikilinks",
            "admonition",
            "codehilite(guess_lang=False,pygments_style=emacs,noclasses=True)"]

    CNZZ_ANALYTICS = True
    MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'
    THEME = "themes/foundation-default-colours"

1. 第6行的SITENAME是博客网站的名称，可以是任何字符；第7行是博客网站的网址，这个字段在本地开发和发布版本是不一样的，本地直接填localhost即可，发布版本里需要填博客网址。
2. 第8行：我使用了Disqus作为我的评论系统，Disqus也是[YC][13]毕业生。启用Disqus评论系统非常简单，在官网上注册一个Disqus帐户，然后把帐户名填在`DISQUS_SITENAME`值里即可启用。我的Disqus帐号刚好也是`kamidox`。
3. 第33－42行：这里是配置Markdown扩展，用来支持代码高亮。并且使用Emacs风格的代码高亮。
4. 第44行：由于GFW的存在，我把Google Analize换成了国内的CNZZ统计。
5. 第46行：我的博客使用了`foundation-default-colours`这套主题。关于主题，后文详解。

开发环境和发布环境的配置差不多，除SITEURL不一样外，还多了两个配置：

    :::python
    SITEURL = 'http://kamidox.com'
    # usful setting for publish
    RELATIVE_URLS = False   # 禁用相对路径引用
    DELETE_OUTPUT_DIRECTORY = True      # 编译之前删除output目录，这样保证output下生成的内容是干净的

其它的配置项，可以参阅[Pelican设置文档][12]。

### 配置Makefile

撰写完博客，并在本地预览后，需要发布到服务器上。我使用Makefile的形式来生成文档并发布。我的Makefile核心代码如下：

    #!/makefile
    SSH_HOST=kamidox.com
    SSH_PORT=22
    SSH_USER=ubuntu
    SSH_TARGET_DIR=/home/ubuntu/blogs/
    SSH_KEY=/home/kamidox/work/aws/kamidox-key-tokyo.pem

    rsync_upload: publish
	    rsync -e "ssh -p $(SSH_PORT) -i $(SSH_KEY)" -P -rvzc --delete $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

1. 第2－4行：指定了要上传内容的目的服务器的地址，端口以及用户名
2. 第5行：指定了远程服务器上保存博客内容的目录
3. 第6行：我添加的SSH Identity文件路径。这是因为Amazon EC2登录时我是用SSH Identity文件登录的，而不是使用用户名和密码
4. 第8-9行：我使用rsync来进行上传操作。rsync可以在本地和远程服务器之间同步文件。同步过程中只同步那些改变了的文件，且传输过程中会压缩数据，它比scp要所需要的带宽要小。这里要注意的是，我在默认生成的Makefile上增加了`-i $(SSH_KEY)`，这个就是指定SSH Identity文件登录远程SSH的方法。

### 配置主题

Pelican支持大量的开源主题，GitHub上的[pelican-themes][14]项目有几十套主题，大部分都带了效果预览图。可以从里面挑一个你喜欢的主题样式来使用。还有一个更方便的挑选主题的方式，直接打开[www.pelicanthemes.com][15]挑选吧。一个网页里就列出了几乎所有的主题。我的博客是使用`foundation-default-colours`主题，并在这套主题的基础上进行了一些定制。选定好喜欢的主题后，从GitHub上下载下来所有的主题：

    :::shell
    mkdir ~/pelican
    cd ~/pelican
    git clone https://github.com/getpelican/pelican-themes.git

从里面拷贝一份你选中的主题到项目根目录的`themes`目录下，在本文的例子中是`~/lab/blogs/themes`。然后在`pelicanconf.py`和`publishconf.py`里通过下面代码指定博客主题：

    :::python
    THEME = "themes/foundation-default-colours"

通常的做法是，选中一个自己喜欢的主题后，会进行一些定制。Pelican使用[Jinja2][16]来配置主题。一个主题的典型结构如下：

    :::text
    ├── static
    │   ├── css
    │   └── images
    └── templates
        ├── analytics_cnzz.html // 这个是我添加的使用cnzz的统计服务的代码
        ├── analytics.html      // 这是Google Analytics的代码
        ├── archives.html       // 这个是博客归档页面的模板
        ├── article.html        // 这个是博客正文的显示模板
        ├── base.html           //　这个是所有页面的父类模板，即所有页面都引用这个页面。比如网页导航栏啊之类的，都定义在这里
        ├── categories.html     //　所有博客文章的分类列表
        ├── category.html       // 某个博客分类的文章列表模板
        ├── index.html          // 主页
        ├── page.html           // 分页显示的模板
        ├── tag.html            // 某类标签下的文章列表
        └── tags.html           // 所有的标签列表页面模板

稍微有点Jinja的知识加上一些HTML和CSS的知识，就可以自己定义主题了。

### 异常

**为什么博客主页打开半天都不显示出来**

因为GFW封锁了几乎所有和Google相关的网站，这些主题里又用了Google的字体，所以下载这些字体时会导致无法下载成功而半天不显示网页。解决方案很简单，直接修改css文件，不去下载Google字体即可。比如针对`foundation-default-colours`主题，打开主题根目录下的`static/css/foundation.css`和`static/css/foundation.min.css`文件，删除掉`@import url("//fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,700italic,400,300,700");`内容即可。当然，如果你和你的读者都是翻墙高手，那就不会遇到这个问题了。

**No module named html_parser**

运行 pelican 命令可能出现下面的错误：

```python
    Traceback (most recent call last):
  File "/usr/local/bin/pelican", line 7, in <module>
    from pelican import main
  File "/Library/Python/2.7/site-packages/pelican/__init__.py", line 20, in <module>
    from pelican.generators import (ArticlesGenerator, PagesGenerator,
  File "/Library/Python/2.7/site-packages/pelican/generators.py", line 22, in <module>
    from pelican.readers import Readers
  File "/Library/Python/2.7/site-packages/pelican/readers.py", line 24, in <module>
    from six.moves.html_parser import HTMLParser
ImportError: No module named html_parser
```

这种情况是由于 `six` 模块的 bug 引起的。可以修改 pelican 安装目录下的 `/Library/Python/2.7/site-packages/pelican/readers.py` 文件。

```python
# from six.moves.html_parser import HTMLParser
from HTMLParser import HTMLParser       # 如果你在 Python 2.7 版本下运行，可直接按照这个方式修改
```

## 撰写博客

### 撰写博客

在`content`目录下新建一个xxx.md，使用Makedown语法直接撰写文档即可。我在ubuntu下使用的是gedit，代码高亮效果很好。撰写博客的时候需要注意，Pelican支持一些元数据。比如，本文的元数据如下：

    #!text
    Title: 使用Pelican搭建博客系统
    Date: 2014-10-07 22:20
    Modified: 2014-10-07 23:04
    Tags: python, pelican
    Slug: build-blog-system-by-pelican
    Authors: Joey Huang
    Summary: 本文介绍了Pelican的特性；选择Pelican的理由以及从头安装配置，搭建出一个可运行的独立博客系统。
    Status: draft

1. 第5行：Slug是文档的唯一标识，生成html时，会直接使用这个值当html的文件名。所以，不同博客文章这个值需要保证唯一性，否则生成html时会报错。
2. 第8行：这个表示本文是草稿。比如我们一篇博客经常不是一次性写完的，写了一半暂不想让读者看到，或者写完想让别人帮忙审查一下，就可以加这一行标识。这样Pelican在处理时，这篇文章也会生成html，但不会放在博客的主页及分类索引里，这样普通的读者一般看不到这个文章。有这个标识的文章生成时放在`output/drafts`目录下，你就可以通过分享url的方式让你的co-worker帮你review你的文章。

我们可以在`content`目录下任意建子目录来组织管理博客文章。由于我们在设置文件里指定这个值`USE_FOLDER_AS_CATEGORY = True`，这样这些目录名称就自动变成博文分类的目录了。

### 预览博客文章

撰写文章的过程中，可以随时在浏览器里预览博客文章。方法是先在博客项目的根目录下执行下面命令来启动预览服务器：

    :::shell
    make devserver

这条命令会自动使用`pelicanconf.py`的配置文件来生成html网页，同时在本地的8000端口上启动一个http服务器，供你预览文章。这样，直接打开浏览器，输入`localhost:8000`即可打开本地服务器上的你的博客主页。比如，撰写本文时，我就直接在gedit里码字，然后在浏览器里输入`http://localhost:8000/drafts/build-blog-system-by-pelican.html`来实时预览效果。需要注意的是，上述命令会在后台持续监听`content`目录下的内容，如果这个目录下的内容发生变化，会自动重新生成html页面。所以，在gedit里写完一段内容，切换到浏览器，直接刷新一下就可以看到最新的结果了。

当文章写完后，需要在博客项目根目录上运行`make stopserver`来停止这个预览服务以及数据监控功能。

!!! Note "文章在主页上没看到？"
    撰写完文章，需要发布时，需要把`Status: draft`这行元数据去掉。否则文章不会出现在博客主页。只会在drafts下看得到。

## 发布博客

写完博客，我们想发布到网上。这个时候我们就需要一个主机和一个域名，我的独立博客系统用到的下面资源：

* Amazon EC2主机。一个帐户可以免费使用一年。可以点击[这里][6]注册。
* 申请独立域名。我是通过[阿里云][8]直接在[万网][7]上注册的。一年45元。

我的博客运行的软件环境：

* Ubuntu 14.04 Server版，运行在Anazon EC2主机上
* Nginx

### 配置Nginx

Ubuntu下安装Nginx：

    :::shell
    sudo apt-get install nginx-full

安装完成后，编辑配置文件：

    :::shell
    sudo vim /etc/nginx/sites-enabled/default

将配置文件替换成如下的内容：

    #!text
    server {
      listen 80 default_server;
      server_name localhost;
      root /home/kamidox/lab/blogs/output;

      location / {
        index index.html;
      }
    }

1. 第3行：这个是服务器地址。这里使用本机作为测试服务器就填localhost，如果是配置服务器，就要填服务器的域名。比如我的服务器上，这行是配置成kamidox.com。
2. 第4行：这个设置成博客文章的根目录。这个使用本机作为测试服务器，所以直接填博客项目的`output`目录。如果是在服务器上，我是直接配置成`/home/ubuntu/blogs`。

配置完成后，重启一下Nginx服务：

    :::shell
    sudo service nginx resart

然后在浏览器里输入`localhost`就可以看到博客首页。在本机验证成功Nginx配置后，就可以用SSH登录服务器去配置服务器了。

### 上传博客到服务器

直接在项目根目录下运行下面的命令即可把文章上传到博客服务器:

    :::shell
    make rsync_upload

因为我们在前文已经配置了Makefile文件。所以运行这个命令之后，就会使用 `publishconf.py` 来生成html，并且通过rsync上传到服务器Amazon EC2服务器的 `/home/ubuntu/blogs/` 目录下。

!!! Hint "配置Amazon EC2主机"
    发布博客到服务器上，需要先完成Amazon EC2主机的配置。具体可参阅[Amazon官网上的文档][6]。如果还没有主机，也可以把自己的电脑配置成服务器来作试验，所要做的，就是修改Makefile里的SSH_HOST的值为localhost即可。

## 最佳实践

我的博客内容托管在 GitHub 上。当我需要写一篇文章时，直接打开gedit/sublime开始用Markdown语法码字。想预览时，直接运行 `make devserver`，然后在浏览器里输入文章的URL就可以直接查看了。如果文章写了一半，还不想发布，直接加一条元数据 `Status: draft` 。然后 git commit + git push 提交到服务器。等到文章写完，想发布了，删除掉草稿标识；然后 git commit + git push 先提交到 GitHub 上；接着运行 `make rsync_upload` 即可把博客内容上传到 Amazon EC2 主机上。打开 [blog.kamidox.com][17] 确认一下即完成了一篇博文的发布。

[1]: http://docutils.sourceforge.net/rst.html
[2]: http://daringfireball.net/projects/markdown/
[3]: https://github.com/getpelican/pelican
[4]: http://blog.iwantmyname.com/2014/05/the-updated-big-list-of-static-website-generators-for-your-site-blog-or-wiki.html
[5]: http://siliconangle.com/blog/2012/03/20/5-minimalist-static-html-blog-generators-to-check-out/
[6]: https://aws.amazon.com
[7]: http://www.net.cn/
[8]: http://www.aliyun.com/
[9]: https://disqus.com/
[10]: http://docs.getpelican.com/en/3.4.0/
[11]: https://github.com/jekyll/jekyll
[12]: http://docs.getpelican.com/en/3.4.0/settings.html
[13]: https://www.ycombinator.com/
[14]: https://github.com/getpelican/pelican-themes
[15]: http://www.pelicanthemes.com/
[16]: http://jinja.pocoo.org/
[17]: http://blog.kamidox.com

