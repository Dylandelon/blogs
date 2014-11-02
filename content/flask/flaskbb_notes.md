Title: FlaskBB阅读笔记
Date: 2014-11-28 23:25
Modified: 2014-11-02 23:25
Tags: python, flask
Slug: flaskbb-notes
Authors: Joey Huang
Summary: FlaskBB是用Flask实现的一个轻量级论坛社区软件。通过阅读FlaskBB源码来学习Flask构架，本文主要记录阅读源码过程中的一些笔记。
Status: draft

## FlaskBB的配置

FlaskBB使用下面典型的配置代码了加载应用程序的配置信息。

    #!python
    # Use the default config and override it afterwards
    app.config.from_object('flaskbb.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)
    # try to update the config via the environment variable
    app.config.from_envvar("FLASKBB_SETTINGS", silent=True)

`Flask.config`类是专门用来处理应用程序全局配置信息的。它类似python的`dict`类，增加了一些导入配置的函数而已。其中`Flask.config.from_object()`用来从一个python类里导入配置信息，需要注意的是，这个函数**只导入大写的类成员变量**，小写的类成员函数是不导入的。

`Flask.config.from_envvar()`用来从环境变量指定的文件中导入设置信息，比如上例中，可以设置`FLASKBB_SETTINGS`的环境变量指向`/path/to/python/config/file.py`，这样程序就会从这个文件里导入配置信息。

需要注意的是，最后导入的配置信息可覆盖前面导入的信息。所以，一般会有三个层次：一是默认配置；二是应用程序创建时传入的参数；最后再从环境变量里导入。

FlaskBB提供了不少配置信息，比如`SEND_LOGS`表示是不是要把错误信息发送给网站管理员邮箱；`SQLALCHEMY_DATABASE_URI`表示ORM数据库路径等等。具体参阅`flaskbb.configs.default.DefaultConfig`类。

## FlaskBB的Blueprint

Blueprint是Flask提供的模块化设计组件。FlaskBB主要由四个Blueprint组成：

1. forum
  论坛主模块，由`flaskbb.forum.views.forum`Blueprint实现
2. user
  用户管理模块，由`flaskbb.user.views.user`Blueprint实现
3. auth
  鉴权模块，由`flaskbb.auth.views.auth`Blueprint实现
4. management
  后台管理模块，由`flaskbb.management.views.management`Blueprint实现

## FlaskBB用到的Flask扩展

有大量的第三方开发者为Flask构架开发扩展，在[这里][1]可以找到官方收录的所有Flask扩展。FlaskBB用到了如下扩展：

1. [Flask-SQLAlchemy][3]
  这是[sqlalchemy][2]的Flask扩展，提供SQL数据库和ORM访问。
2. [Flask-Login][4]
  这个扩展提供了用户会话管理。实现了一些通用的会话管理任务，如登录，登出，以及记录用户会话期间的状态数据等。
3. [Flask-Mail][5]
  这个扩展让Flask应用很容易地发送电子邮件，而且支持单元测试。
4. [Flask-Cache][6]
  给Flask程序提供Cache支持。
5. [Flask-DebugToolbar][7]
  从Django移植过来的适用于Flask的调试器。主要用来调试Flask程序及性能。
6. [Flask-Redis][9]
  给Flask程序添加[Redis][8]的扩展。Redis是一个开源的使用ANSI C语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。
7. [Flask-Migrate][10]
  给Flask用的SQLAlchemy数据库迁移工具。比如，Flask应用的1.3版本在1.2版本的数据库的某个表里添加了一个字段，那么使用这个工具可以自动生成数据库迁移脚本，帮助使用1.2版本的用户把数据库从1.2版本升级到1.3版本。
8. [Flask-Theme2][11]
  给Flask应用添加主题支持。
9. [Flask-Plugins][12]
  和FlaskBB的作者是同一个人。提供更简单的插件管理。
10. [Flask-WhooshAlchemy][14]
  这个扩展帮助Flask程序实现基于SQLAlchemy数据库内容的文本搜索和索引服务。正如扩展的名字，它是使用[whoosh][13]和SQLAlchemy的ORM结合起来实现广西内容的搜索和索引功能。
11. [Flask-WTF][15]
  当你必须处理浏览器提交的表单数据时，视图代码很快会变得难以阅读。有一些库可以简化这个工作，其中之一便是WTForms。这个扩展让Flask使用更简单地集成WTForms，同时处理了CSRF(Cross-Site Rrequest Forgery，跨站请求伪造)，提供更好的安全性。还提供文件上传等功能。
12. [Flask-Script][16]
  给Flask应用程序提供外部脚本支持。比如运行开发服务器，初始化数据库，等命令行相关的任务。对FlaskBB而言，`python manage.py runserver`和`python manage.py createall`等命令就是通过这个扩展实现的。

[1]: http://flask.pocoo.org/extensions/
[2]: http://www.sqlalchemy.org/
[3]: http://github.com/mitsuhiko/flask-sqlalchemy/
[4]: http://github.com/maxcountryman/flask-login/
[5]:　http://github.com/mattupstate/flask-mail/
[6]: http://github.com/thadeusb/flask-cache/
[7]: http://github.com/mgood/flask-debugtoolbar/
[8]: http://www.redis.cn/
[9]: https://github.com/rhyselsmore/flask-redis/
[10]: https://github.com/miguelgrinberg/Flask-Migrate
[11]: https://github.com/sysr-q/flask-themes2
[12]: https://github.com/sh4nks/flask-plugins
[13]: https://bitbucket.org/mchaput/whoosh/wiki/Home
[14]: https://github.com/gyllstromk/Flask-WhooshAlchemy
[15]: https://github.com/lepture/flask-wtf
[16]: http://github.com/techniq/flask-script/




