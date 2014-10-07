Title: 使用Pelican搭建博客系统
Date: 2014-10-07 22:20
Modified: 2014-10-07 23:04
Tags: python, pelican
Slug: build-blog-system-by-pelican
Authors: Joey Huang
Summary: 本文介绍了Pelican的特性；选择Pelican的理由以及从头安装配置，搭建出一个可运行的独立博客系统。最后给出个人的一个最佳实践流程。

### 什么是Pelican

[Perlican][3]是用Python实现的一个静态网站生成器，支持[reStructuredText][1]或[Markdown][2]。它支持以下功能：

* 博客文章和静态网页
* 支持评论。评论是通过第三方服务Disqus支持的。即评论数据保存在第三方服务器上
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

* 使用Python实现。由于最近在学习Python，我可以阅读源码并按照我的需求来改造Pelican使之完全符合我的需求。
* 足够轻量级。总的代码量才1MB多。安装也方便。
* 有一堆现成的主题可以使用。这对我这种非专业前端的开发者来说，省了不少事。
* 文档齐全。
* 开发活动活跃。GitHub上代码提交活跃。上面文章里介绍的很多博客系统基本上都2+年前就停止更新了。

最后两点对使用任何开源工具来说都是很重要的，只有开发活跃，社区资源多，文档齐全，遇到问题的时候才能较快地得到解决。

### 安装

### 配置

#### 基本配置步骤

#### 主题选择

#### 代码高亮

#### Nginx配置多个应用

### 最佳实践

### TIPS

* 打开markdown风格的代码高亮：https://github.com/getpelican/pelican/issues/1238
* 主题及预览效果: http://www.pelicanthemes.com/。感觉foundation-default-colours风格不错。
* 这个介绍了5个轻量级静态博客引擎：http://siliconangle.com/blog/2012/03/20/5-minimalist-static-html-blog-generators-to-check-out/
* 这个介绍了32个博客引擎：http://blog.iwantmyname.com/2014/05/the-updated-big-list-of-static-website-generators-for-your-site-blog-or-wiki.html
*

[1]: http://docutils.sourceforge.net/rst.html
[2]: http://daringfireball.net/projects/markdown/
[3]: https://github.com/getpelican/pelican
[4]: http://blog.iwantmyname.com/2014/05/the-updated-big-list-of-static-website-generators-for-your-site-blog-or-wiki.html
[5]: http://siliconangle.com/blog/2012/03/20/5-minimalist-static-html-blog-generators-to-check-out/


