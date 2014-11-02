Title: FlaskBB阅读笔记（一）
Date: 2014-11-28 23:25
Modified: 2014-11-02 23:25
Tags: python, flask
Slug: flaskbb-notes-1
Authors: Joey Huang
Summary: FlaskBB是用Flask实现的一个轻量级论坛社区软件。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架以及在一个产品级的Flask应用里的一些最佳实践规则。

## 开篇

[FlaskBB][19]是用Flask框架实现的一个轻量级的论坛社区软件，代码托管在[GitHub][19]上。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架以及在一个产品级的Flask应用里的一些最佳实践规则。本文是这系列文章的第一遍。

本文分析FlaskBB的主程序`app.py`的源码。我们从`create_app()`函数入手，分析FlaskBB的软件结构。

    #!python
    def create_app(config=None):
        """
        Creates the app.
        """
        # Initialize the app
        app = Flask("flaskbb")

        # Use the default config and override it afterwards
        app.config.from_object('flaskbb.configs.default.DefaultConfig')
        # Update the config
        app.config.from_object(config)
        # try to update the config via the environment variable
        app.config.from_envvar("FLASKBB_SETTINGS", silent=True)

        configure_blueprints(app)
        configure_extensions(app)
        configure_template_filters(app)
        configure_context_processors(app)
        configure_before_handlers(app)
        configure_errorhandlers(app)
        configure_logging(app)

        return app
    
## 配置

FlaskBB使用下面典型的配置代码了加载应用程序的配置信息。

    #!python
    # Use the default config and override it afterwards
    app.config.from_object('flaskbb.configs.default.DefaultConfig')
    # Update the config
    app.config.from_object(config)
    # try to update the config via the environment variable
    app.config.from_envvar("FLASKBB_SETTINGS", silent=True)

`Flask.config`类是专门用来处理应用程序全局配置信息的。它类似python的`dict`类，增加了一些导入配置的函数而已。其中`Flask.config.from_object()`用来从一个python类里导入配置信息，需要注意的是，这个函数**只导入大写的类成员变量**，小写的类成员函数是不导入的。

`Flask.config.from_envvar()`用来从环境变量指定的文件中导入设置信息，比如上例中，可以设置`FLASKBB_SETTINGS`的环境变量指向*/path/to/python/config/file.py*，这样程序就会从这个文件里导入配置信息。

需要注意的是，最后导入的配置信息可覆盖前面导入的信息。所以，一般会有三个层次：一是默认配置；二是应用程序创建时传入的参数；最后再从环境变量里导入。

FlaskBB提供了不少配置信息，比如`SEND_LOGS`表示是不是要把错误信息发送给网站管理员邮箱；`SQLALCHEMY_DATABASE_URI`表示ORM数据库路径等等。具体参阅`flaskbb.configs.default.DefaultConfig`类。

## Blueprint

Blueprint是Flask提供的模块化设计组件。FlaskBB通过`configure_blueprints()`来初始化Blueprint

    #!python
    def configure_blueprints(app):
        app.register_blueprint(forum, url_prefix=app.config["FORUM_URL_PREFIX"])
        app.register_blueprint(user, url_prefix=app.config["USER_URL_PREFIX"])
        app.register_blueprint(auth, url_prefix=app.config["AUTH_URL_PREFIX"])
        app.register_blueprint(management, url_prefix=app.config["ADMIN_URL_PREFIX"])

主要由四个Blueprint组成：

1. forum
  论坛主模块，由`flaskbb.forum.views.forum`Blueprint实现，默认其挂载的URL是`/`
2. user
  用户管理模块，由`flaskbb.user.views.user`Blueprint实现，默认其挂载的URL是`/user`
3. auth
  鉴权模块，由`flaskbb.auth.views.auth`Blueprint实现，默认其挂载的URL是`/auth`
4. management
  后台管理模块，由`flaskbb.management.views.management`Blueprint实现，默认其挂载的URL是`/admin`

## FlaskBB用到的Flask扩展

有大量的第三方开发者为Flask构架开发扩展，在[这里][1]可以找到官方收录的所有Flask扩展。FlaskBB通过`configure_extensions()`函数来初始化用到的扩展。这些扩展的简要信息汇总如下：

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

## 自定义的Jinja2过滤器

Jinja2提供了[自定义过滤器][17]的功能，可以在Jinja2模板里灵活使用。FlaskBB通过函数`configure_template_filters()`定义了一系列过滤器，其中`is_online`过滤器是这样定义的：

    :::python
    app.jinja_env.filters['is_online'] = is_online

过滤器就是一个简单的python函数，`is_online()`函数定义在*flaskbb/utils/helper.py*里：
    
    #!python
    def is_online(user):
        """A simple check to see if the user was online within a specified
        time range

        :param user: The user who needs to be checked
        """
        return user.lastseen >= time_diff()

这样，在Jinaja2模板*flaskbb/templates/user/profile.html*里，就可以使用下面的代码来判断用户是否在线：

    :::html
    {% if user|is_online %}
    <tr><td><span class="label label-success">Online</span></td></tr>
    {% else %}
    <tr><td><span class="label label-default">Offline</span></td></tr>
    {% endif %}

上面Jinja2模板里`user|is_online`脚本会导致`is_online(user)`被调用来判断用户是否在线。

## 向模板注入设置信息

FlaskBB通过调用`configure_context_processors()`向模板注入设置信息。代码如下：

    #!python
    def configure_context_processors(app):
    """
    Configures the context processors
    """
    @app.context_processor
    def inject_flaskbb_config():
        """
        Injects the ``flaskbb_config`` config variable into the templates.
        """
        return dict(flaskbb_config=flaskbb_config)

使用`context_processor`装饰器来装饰`inject_flaskbb_config()`函数，这样这个函数会被Flask记录起来，每次要渲染模板时，会先调用这个函数更新一下模板上下文信息。这样，在模板里就可以访问这里注入的上下文信息。上下文处理器函数必须返回一个`dict`实例。Flask官方文档对[context_processor][18]有详细的描述。

例如，返回的`dict`里包含'name: kamidox'这样的值，则在Jinja2模板里可以直接用`{% name %}`来访问`name`变量，其值为`kamidox`。

## 更新用户在线信息

FlaskBB通过`configure_before_handlers()`函数来注册每个请求之前的动作，以记录用户的在线信息。

    #!python
    def configure_before_handlers(app):
    """
    Configures the before request handlers
    """

    @app.before_request
    def update_lastseen():
        """
        Updates `lastseen` before every reguest if the user is authenticated
        """
        if current_user.is_authenticated():
            current_user.lastseen = datetime.datetime.utcnow()
            db.session.add(current_user)
            db.session.commit()

这里，`before_request`装饰器将把`update_lastseen()`函数注册进Flask，Flask在处理请求之前都会调用这个函数。FlaskBB使用这个机制来记录最后一次看到用户的时间。结合会话的超时机制，就可以判断用户是否在线。

## 自定义错误处理

通过`configure_errorhandlers()`来实现自定义错误处理。其中，HTTP 403, 404及500的错误处理定义如下

    #!python
    def configure_errorhandlers(app):
    """
    Configures the error handlers
    """

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500

这样当发生这些http错误时，错误网页将从服务器返回自定义的错误网页，而不是浏览器客户端默认的错误页面。

## LOG配置

通过`configure_logging()`来配置系统的LOG。FlaskBB的LOG主要保存在应用程序根目录下的*logs*目录里，分两个文件保存，一个是INFO级别的LOG，另外一个是ERROR级别的LOG。同时还支持把ERROR级别的LOG通过邮件的方式发送给网站管理员。

下面代码配置了INFO级别的LOG：

    #!python
    logs_folder = os.path.join(app.root_path, os.pardir, "logs")
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    info_log = os.path.join(logs_folder, app.config['INFO_LOG'])

    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

下面代码配置了通过邮件发送错误LOG给网站管理员：

    #!python
    from logging.handlers import SMTPHandler
    if app.config["SEND_LOGS"]:
        mail_handler = \
            SMTPHandler(app.config['MAIL_SERVER'],
                        app.config['MAIL_DEFAULT_SENDER'],
                        app.config['ADMINS'],
                        'application error, no admins specified',
                        (
                            app.config['MAIL_USERNAME'],
                            app.config['MAIL_PASSWORD'],
                        ))

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        app.logger.addHandler(mail_handler)

## 结束语

通过对主程序`app.py`的代码分析，我们基本上知道了FlaskBB的主体框架，模块划分，用到的外部扩展等信息。下一篇将分模块深入阅读各个Blueprint模块的实现以及数据库设计方面的内容。


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
[17]: http://jinja.pocoo.org/docs/dev/api/#custom-filters
[18]: http://flask.pocoo.org/docs/0.10/templating/#context-processors
[19]: https://github.com/sh4nks/flaskbb


