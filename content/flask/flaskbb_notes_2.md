Title: FlaskBB阅读笔记（二）
Date: 2014-11-04 23:00
Modified: 2014-11-04 23:00
Tags: python, flask
Slug: flaskbb-notes-2
Authors: Joey Huang
Summary: FlaskBB是用Flask实现的一个轻量级论坛社区软件。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架以及在一个产品级的Flask应用里的一些最佳实践规则。本文分析了管理模块manage.py的实现，通过它学习Flask-Script扩展模块的用法。
Status: draft

## 开篇

[FlaskBB][1]是用Flask框架实现的一个轻量级的论坛社区软件，代码托管在GitHub上。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架，以及在一个产品级的Flask应用里的一些最佳实践规则。

本文是这系列文章的第二遍。本文分析FlaskBB的脚本管理程序`manage.py`的源码。基本上每个Flask程序都需要一个`manage.py`，用户可以通过它来创建数据库，运行开发服务器的任务。在FlaskBB的`README.md`里有下面一段话：

    :::markdown
    * Create a virtualenv
    * Install the dependencies
        * `pip install -r requirements.txt`
    * Configuration (_adjust them accordingly to your needs_)
        * For development copy `flaskbb/configs/development.py.example` to `flaskbb/configs/development.py`
    * Database creation
        * `python manage.py createall`
    * Run the development server
        * `python manage.py runserver`
    * Visit [localhost:8080](http://localhost:8080)

这些指令是指导用户安装/运行FlaskBB论坛程序的。其中`python manage.py createall`和`python manage.py runserver`就是本文要介绍的主角，其中第一条命令用来创建一个测试数据库，第二条命令用来运行开发服务器。

有了这些神器，从GitHub下载代码：

    :::shell
    cd ~
    git clone https://github.com/sh4nks/flaskbb.git
    
然后创建virtualenv：

    :::shell
    cd ~/flaskbb
    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    
拷贝配置文件：

    :::shell
    cp flaskbb/configs/development.py.example flaskbb/configs/development.py
    
创建数据库，并运行开发服务器：

    :::shell
    python manage.py createall
    python manage.py runserver

这样打开[localhost:8080](http://localhost:8080)即可看到FlaskBB运行出来的论坛网站了。

## Flask-Script用法

要了解`manage.py`的工作原理，必须先了解Flask-Script扩展模块的用法。在本系列第一篇文章中，我们简要介绍了Flask-Script的作用。其官方文档这样描述自己：

> The Flask-Script extension provides support for writing external scripts in Flask. This includes running a development server, a customised Python shell, scripts to set up your database, cronjobs, and other command-line tasks that belong outside the web application itself.

### 创建命令

使用`@command`装饰器创建命令：

    #!python
    from flask.ext.script import Manager

    app = Flask(__name__)
    # configure your app

    manager = Manager(app)

    @manager.command
    def hello():
        "Just say hello"
        print "hello"
    
    if __name__ == "__main__":
        manager.run()

这样就创建了一个`hello`的命令，假设上述文件保存为`manage.py`，则可以运行这个添加的命令：

    :::shell
    $ python manage.py hello
    > hello world
    
用`@option`装饰器创建带参数的命令：

    :::python
    @manager.option('-n', '--name', dest='name', default='joe')
    @manager.option('-u', '--url', dest='url', default=None)
    def hello(name, url):
        if url is None:
            print "hello", name
        else:
            print "hello", name, "from", url

上述命令可以这样调用：

    :::shell
    $ python manage.py hello -n Joe -u reddit.com
    > hello Joe from reddit.com
    $ python manage.py hello -n Joe
    > hello Joe
    $ python manage.py hello --name Joey --url kamidox.com
    > hello Joey from kamidox.com

实际上，使用`@command`装饰器也可以实现上述相同的带参数的命令，只是使用`@option`可读性更好一点。

### 获取用户输入

在创建数据库时，需要和用户交互，输入数据库用户名密码等信息。我们可以借助prompt系列函数来获取用户的输入：

    #!python
    from flask.ext.script import Manager, prompt_bool

    from myapp import app
    from myapp.models import db

    manager = Manager(app)

    @manager.command
    def dropdb():
        if prompt_bool("Are you sure you want to lose all your data"):
            db.drop_all()

这个命令可以这样调用：

    :::shell
    $ python manage.py dropdb
    > Are you sure you want to lose all your data ? [N]

Flask-Script还提供了`prompt_pass()`，`prompt_choices()`等不同形态的函数来获取用户输入信息。

### 其它技巧

不带任何参数运行`python manage.py`会输出可用的命令列表：

    :::shell
    (.venv)kamidox@kamidox-laptop:~/code/flaskbb$ python manage.py
    usage: manage.py [-?]
                     {shell,create_admin,db,createall,runserver,initflaskbb,initdb,dropdb}
                     ...

    positional arguments:
      {shell,create_admin,db,createall,runserver,initflaskbb,initdb,dropdb}
        shell               Runs a Python shell inside Flask application context.
        create_admin        Creates the admin user
        db                  Perform database migrations
        createall           Creates the database with some testing content. If you
                            do not want to drop or create the db add '-c' (to not
                            create the db) and '-d' (to not drop the db)
        runserver           Runs the Flask development server i.e. app.run()
        initflaskbb         Initializes FlaskBB with all necessary data
        initdb              Creates the database.
        dropdb              Deletes the database

    optional arguments:
      -?, --help            show this help message and exit

也可以针对特定命令获取其帮助信息：

    :::shell
    (.venv)kamidox@kamidox-laptop:~/code/flaskbb$ python manage.py runserver --help
    usage: manage.py runserver [-?] [-h HOST] [-p PORT] [--threaded]
                               [--processes PROCESSES] [--passthrough-errors] [-d]
                               [-D] [-r] [-R]

    Runs the Flask development server i.e. app.run()

    optional arguments:
      -?, --help            show this help message and exit
      -h HOST, --host HOST
      -p PORT, --port PORT
      --threaded
      --processes PROCESSES
      --passthrough-errors
      -d, --debug           enable the Werkzeug debugger (DO NOT use in production
                            code)
      -D, --no-debug        disable the Werkzeug debugger
      -r, --reload          monitor Python files for changes (not 100{'const':
                            True, 'help': 'monitor Python files for changes (not
                            100% safe for production use)', 'option_strings':
                            ['-r', '--reload'], 'dest': 'use_reloader',
                            'required': False, 'nargs': 0, 'choices': None,
                            'default': None, 'prog': 'manage.py runserver',
                            'container': <argparse._ArgumentGroup object at
                            0xb609cd6c>, 'type': None, 'metavar': None}afe for
                            production use)
      -R, --no-reload       do not monitor Python files for changes

更多详细的用法可参阅[Flask-Script官方文档][2]，如果翻墙不便，也可以从GitHub上下载Flask-Script源码，然后在docs自己编译生成html文档。

    :::shell
    cd ~/code
    git clone https://github.com/smurfix/flask-script.git
    cd docs
    make html

编译完成后，打开`docs/_build/html/index.html`即可查阅Flask-Script文档了。

!!! Note "Sphinx"
    如果编译提示出错，检查一下是否安装了[Sphinx][3]。这是个用来生成优美的html文档的引擎。IBM DeveloperWorks有[一篇文章][4]介绍了Sphinx的作用。感兴趣的朋友可以参考一下。

## manage.py源码分析

有了上面的背景知识，阅读`manage.py`就很轻松了。



[1]: https://github.com/sh4nks/flaskbb
[2]: http://flask-script.readthedocs.org/
[3]: http://sphinx.pocoo.org/
[4]: http://www.ibm.com/developerworks/cn/opensource/os-sphinx-documentation/


