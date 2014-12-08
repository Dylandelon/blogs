Title: FlaskBB阅读笔记（三）
Date: 2014-12-07 23:00
Modified: 2014-12-07 23:00
Tags: python, flask
Slug: flaskbb-notes-3
Authors: Joey Huang
Summary: FlaskBB 是用 Flask 实现的一个轻量级论坛社区软件。本系列文章通过阅读 FlaskBB 的源代码来深入学习 Flask 框架以及在一个产品级的 Flask 应用里的一些最佳实践规则。本文介绍 ORM 基础知识，分析 Flask-SQLAlchemy 及 sqlalchemy ORM 引擎的一些常用方法，进而介绍 FlaskBB MVC 代码结构。
Status: draft

[TOC]

## 开篇

[FlaskBB][1]是用Flask框架实现的一个轻量级的论坛社区软件，代码托管在GitHub上。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架，以及在一个产品级的Flask应用里的一些最佳实践规则。

本文是本系列文章的第三篇，将介绍ORM基础知识，分析Flask-SQLAlchemy及sqlalchemy ORM引擎的一些常用方法，进而介绍FlaskBB用户管理模块的数据库设计。

## 什么是 ORM

> 对象关系映射（英语：Object Relational Mapping，简称ORM，或O/RM，或O/R mapping），是一种程序技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。从效果上说，它其实是创建了一个可在编程语言里使用的“虚拟对象数据库”。-百度百科

简单地说，使用 ORM 来操作数据库，我们基本上不用跟 SQL 打交道了。直接用程序语言的对象来打交道即可。Flask-SQLAlchemy 是 ORM 引擎 sqlalchemy 针对 Flask 的扩展。

## 定义表

定义一个表只需要继承自 `db.Model` 即可。

    #!python
    class User(db.Model, UserMixin):
        __tablename__ = "users"
        __searchable__ = ['username', 'email']

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(200), unique=True, nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)
        _password = db.Column('password', db.String(120), nullable=False)

这样我们就定义了一个叫 `users` 的表格，表格的名称由 `__tablename__` 指定。这样任何对表格的操作，都可以转化为对 `User` 类的操作。代码里的 `db` 对象是什么呢？在 extensions.py 里创建了 db 对象 `db = SQLAlchemy()`。然后在 app.py 里初始化这个 db 对象 `db.init_app(app)`。

## 定义一对多关系

一个论坛用户会对应多个论坛主题。论坛主题由类 `Topic` 表达。

    #!python
    class Topic(db.Model):
        __tablename__ = "topics"
        __searchable__ = ['title', 'username']

        id = db.Column(db.Integer, primary_key=True)
        forum_id = db.Column(db.Integer,
                             db.ForeignKey("forums.id",
                                           use_alter=True,
                                           name="fk_topic_forum_id"),
                             nullable=False)
        title = db.Column(db.String(255), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
        username = db.Column(db.String(200), nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow())
        last_updated = db.Column(db.DateTime, default=datetime.utcnow())
        locked = db.Column(db.Boolean, default=False)
        important = db.Column(db.Boolean, default=False)
        views = db.Column(db.Integer, default=0)
        post_count = db.Column(db.Integer, default=0)

User 类通过 `db.relationship` 来定义表 User 和 Topic 的一对多关系。

    #!python
    class User(db.Model, UserMixin):
        __tablename__ = "users"
        __searchable__ = ['username', 'email']

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(200), unique=True, nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)
        _password = db.Column('password', db.String(120), nullable=False)
        ...
        topics = db.relationship("Topic", backref="user", lazy="dynamic")

关键代码在 LINE 10 。这一行代码会在 `users` 表里创建一个列叫 `topics`，这个列就保存了这个用户发起的所有论坛主题。然后在 `topics` 表里创建一个列叫 `user`，这是通过 `backref` 这个参数实现的，所以我们可以通过 `Topic.user` 来引用论坛主题的发起用户。最后一个参数 `lazy` 可以有四个值：

* `select`
  这是默认值，表示 SQLAlchemy 会在必要的时候一次性把所有的数据从数据库里通过 SQL SELECT 语句读取出来。当一对多的数据量比较小时可以用这个值，当数据量比较大时，用这个值会降低程序的性能。
* `joined`
  告诉 SQLAlchemy 使用 JOIN 子句一次性地把关系数据从数据库里导出来。关于 JOIN 可参阅[这篇文章][1]。
* `subquery`
  类似 `joined`，但 SQLAlchemy 会使用子查询来读取数据库。关于子查询可参阅[这篇文章][2]。
* `dynamic`
  针对一对多关系里，数据量比较大时，这是个特殊且有用的类型。它不会一次性把所有的关系数据都从数据库里读出来，相反它会返回一个查询对象，在需要数据时，从这个查询对象时进行二次查询，才能获得需要的数据。这种类型可以提高程序性能。

## 定义多对多关系

一个用户可以属于多个组，而一个组里也会有多个用户。针对这种多对多的关系，我们需要第三个表来保存这种多对多关系。

    #!python
    groups_users = db.Table(
        'groups_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('group_id', db.Integer(), db.ForeignKey('groups.id')))

首先直接使用 `db.Table` 定义一个多对多的关系表 `groups_users`。这里要注意不要使用继承 `db.Model` 来定义这个多对多关系表。然后，在 User 类里使用 `db.relationship` 来定义多对多关系：

    #!python
    class User(db.Model, UserMixin):
        __tablename__ = "users"
        __searchable__ = ['username', 'email']

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(200), unique=True, nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)
        _password = db.Column('password', db.String(120), nullable=False)
        ...
        secondary_groups = \
            db.relationship('Group',
                        secondary=groups_users,
                        primaryjoin=(groups_users.c.user_id == id),
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')

其中 LINE 10 - 15 使用 `db.relationship` 来定义多对多关系。第一个参数表示多对多关系的类为 Group，第二个参数 `secondary=groups_users` 表示需要从第三个叫 `groups_users` 的表里获取多对多关系，第三个参数 `primaryjoin=(groups_users.c.user_id == id)` 表示连接查询时的条件。第四个参数 `backref=db.backref('users', lazy='dynamic')` 会在 Group 类里创建一个成员叫 users，其中 `db.backref` 的 `lazy` 参数为 `dynamic` 表示 Group.users 为一个查询对象。第五个参数 `lazy='dynamic'` 表示 User.secondary_groups 为一个查询对象，其实这里可以不要使用 `dynamic`，因为一个用户所属的组是很有限的，不可能很多，可以一次性全部加载进来。

## 插入及修改记录

插入记录时，不用再写 SQL 语句了，直接使用类对象来操作即可。用户注册成功后，需要向 users 表插入一条记录。在 `flaskbb.auth.RegisterForm.save()` 里实现：

    #!python
    def save(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data,
                    date_joined=datetime.utcnow(),
                    primary_group_id=4)
        return user.save()

创建一个 User 对象，然后调用对象的 `save()` 方法：

    #!python
    def save(self, groups=None):
        """Saves a user. If a list with groups is provided, it will add those
        to the secondary groups from the user.

        :param groups: A list with groups that should be added to the
                       secondary groups from user.
        """

        if groups:
            # TODO: Only remove/add groups that are selected
            secondary_groups = self.secondary_groups.all()
            for group in secondary_groups:
                self.remove_from_group(group)
            db.session.commit()

            for group in groups:
                # Do not add the primary group to the secondary groups
                if group.id == self.primary_group_id:
                    continue
                self.add_to_group(group)

            self.invalidate_cache()

        db.session.add(self)
        db.session.commit()
        return self

其关键代码是 LINE 24 - 25。其中 `db.session` 对象是 Flask-SQLAlchemy 扩展为我们创建的一个事务对象，使用 `db.session.add()` 来插入记录，使用 `db.session.commit()` 来提交事务，使操作生效。LINE 9 - LINE 22是当需要改变一个用户所属的组时的操作代码，这里就不展开讨论。

需要说明的是，修改记录时也是使用 `db.session.add()` 方法。SQLAlchemy 会自动根据主键的值来判断这是一个新加的记录还是要修改的记录。

!!! Note "关于db.session.commit()"
    User.save() 方法里，当 groups 参数不为空时，会有两个 db.session.commit() 的调用。把一个操作分成两个事务，就达不到保证数据一致性的目的了。这里的代码写法应该可以再考量一下。

## 删除记录

当我们需要从 users 表里删除记录里，调用 `User.delete()` 方法即可，它的代码是这样的：

    #!python
    def delete(self):
        """Deletes the User."""

        # This isn't done automatically...
        PrivateMessage.query.filter_by(user_id=self.id).delete()
        ForumsRead.query.filter_by(user_id=self.id).delete()
        TopicsRead.query.filter_by(user_id=self.id).delete()

        db.session.delete(self)
        db.session.commit()

        return self

LINE 9 - 10 是用来从 users 表里删除一条记录。LINE 5-7 是用来在删除用户之前，把一些用户相关的数据也一并删除掉。

## 查询记录

继承自 `db.Model` 的类会引入 `query` 属性，这是个可查询对象 `Query` 的实例。其常用的方法有 `query.filter()`，`query.filter_by()`，`query.order_by()`，`query.limit()`，`query.get()`等等。这些函数只是指定了查询的条件，查询真正开始是在调用 `query.first()`，`query.all()` 等方法后才发生的。

例如，获取用户的主题个数 `User.topic_count()`：

    #!python
    @property
    def topic_count(self):
        """Returns the thread count"""
        return Topic.query.filter(Topic.user_id == self.id).count()

再如 `User.delete()` 的代码里删除用户相关的数据的代码：
    
    #!python
    PrivateMessage.query.filter_by(user_id=self.id).delete()
    ForumsRead.query.filter_by(user_id=self.id).delete()
    TopicsRead.query.filter_by(user_id=self.id).delete()

再如 `User.save()` 的代码里关于群组的相关操作代码：

    #!python
    secondary_groups = self.secondary_groups.all()
    for group in secondary_groups:
        self.remove_from_group(group)
    db.session.commit()

通过 `self.secondary_groups.all()` 获取所有的群组，然后在这些群组里把用户移除。
        
!!! Note "filter() vs filter_by()"
    `filter(*criterion)` 使用 SQL 表达式，而 `filter_by(**kwargs)` 使用关键字表达式。从函数声明可以看出来 `filter()` 接受的参数是一个元组表达式，而 `filter_by()` 接受的是一个 dict 表达式。所以，`Topic.query.filter(Topic.user_id == self.id).count()` 等价于 `Topic.query.filter_by(user_id = self.id).count()`。关于这个区别，还可以进一步查阅 [StackOverFlow][3] 及 [SegmentFault][4] 上的文章，还有[官方的文档][5]。顺便吐槽一下，从这个对比可以看出来 StackOverFlow 和国内 SegmentFault 质量差异，顺便再感慨一下，学 IT 的人英文不好你就等着受苦吧，永远接触不到第一手的权威资料。
    
关于查询还需要说明的一点，Flask-SQLAlchemy 提供了便利的函数 `get_or_404()` 及 `first_or_404()` 来替代 `get()` 和 `first()` 方法。这两个方法在 view 里特别有用，如找不到这个用户时，直接抛出 404 异常。而不是返回一个 None。

    #!python
    @user.route("/<username>")
    def profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        return render_template("user/profile.html", user=user)

## MVC 代码结构

介绍完 ORM，我们可以看一下 FlaskBB 项目 `flaskbb/flaskbb` 目录下的核心代码的 MVC 代码结构。它把每个模块封装成一个独立的 bluepoint，每个模块又分为 model，view，form 三个模块。这样整体代码结构非常清晰。

    :::shell
    flaskbb
    ├── __init__.py
    ├── _compat.py
    ├── app.py
    ├── email.py
    ├── extensions.py
    ├── auth
    │   ├── __init__.py
    │   ├── forms.py
    │   └── views.py
    ├── configs
    │   ├── __init__.py
    │   ├── default.py
    │   ├── development.py
    │   ├── development.py.example
    │   ├── production.py.example
    │   └── testing.py
    ├── fixtures
    │   ├── __init__.py
    │   ├── groups.py
    │   └── settings.py
    ├── forum
    │   ├── __init__.py
    │   ├── forms.py
    │   ├── models.py
    │   └── views.py
    ├── management
    │   ├── __init__.py
    │   ├── forms.py
    │   ├── models.py
    │   └── views.py
    ├── user
    │   ├── __init__.py
    │   ├── forms.py
    │   ├── models.py
    │   └── views.py
    └── utils
        ├── __init__.py
        ├── decorators.py
        ├── helpers.py
        ├── permissions.py
        ├── populate.py
        ├── settings.py
        └── widgets.py

## 结束语

本文简单介绍了 ORM 操作数据库的概念和一些基本的用法。可参考的资料很多，这里强烈推荐官方文档，深入浅出。关于入门资料，可参阅 [Flask-SQLAlchemy 官方文档][6]。深入阅读可以参考 [sqlalchemy 官方文档][7]。

[1]: http://www.w3school.com.cn/sql/sql_join.asp
[2]: http://www.360doc.com/content/11/0407/17/5789627_107867377.shtml
[3]: http://stackoverflow.com/questions/2128505/whats-the-difference-between-filter-and-filter-by-in-sqlalchemy
[4]: http://segmentfault.com/q/1010000000140472
[5]: http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=filter_by#sqlalchemy.orm.query.Query.filter
[6]: http://flask-sqlalchemy.pocoo.org/2.0
[7]: http://docs.sqlalchemy.org/en/latest/orm





























