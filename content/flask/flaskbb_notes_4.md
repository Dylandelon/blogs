Title: FlaskBB阅读笔记（四）
Date: 2014-11-17 23:00
Modified: 2014-11-17 23:00
Tags: python, flask
Slug: flaskbb-notes-4
Authors: Joey Huang
Summary: FlaskBB是用Flask实现的一个轻量级论坛社区软件。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架以及在一个产品级的Flask应用里的一些最佳实践规则。本文通过分析FlaskBB的自动测试代码，进而介绍Python下的自动化测试工具pytest。
Status: draft

[TOC]

## 开篇

[FlaskBB][1]是用Flask框架实现的一个轻量级的论坛社区软件，代码托管在GitHub上。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架，以及在一个产品级的Flask应用里的一些最佳实践规则。

本文是本系列文章的第四篇，通过分析FlaskBB的自动测试代码，进而介绍Python下的自动化测试工具pytest。自动化测试在开发和重构过程中有着非常重要的地位。甚至还流行一种测试优先的编程方法，即针对一个功能模块，先写测试例，再去实现功能模块。

## FlaskBB的测试代码

FlaskBB的测试代码在tests目录下：

    :::shell
    tests/
    ├── conftest.py
    ├── fixtures
    │   ├── app.py
    │   ├── forum.py
    │   ├── __init__.py
    │   └── user.py
    ├── __init__.py
    └── unit
        ├── __init__.py
        ├── __pycache__
        ├── test_forum_models.py
        └── utils
            ├── __init__.py
            ├── __pycache__
            ├── test_helpers.py
            ├── test_permissions.py
            ├── test_populate.py
            └── test_widgets.py

在FlaskBB项目目录下执行`py.test tests`输出以下测试结果：

    :::shell
    (.venv)kamidox@kamidox-laptop:~/code/flaskbb$ py.test tests 
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.25 -- pytest-2.6.3 -- /home/kamidox/co
    de/flaskbb/.venv/bin/python
    Tests are shuffled using seed number 362536085265.
    plugins: cov, random
    collecting ... collected 42 items

    tests/unit/test_forum_models.py::test_topic_save PASSED
    tests/unit/test_forum_models.py::test_topic_move PASSED
    tests/unit/utils/test_permissions.py::test_super_moderator_permissions PASSED
    tests/unit/test_forum_models.py::test_topic_url PASSED
    tests/unit/utils/test_permissions.py::test_can_moderate_without_permission PASSED
    tests/unit/test_forum_models.py::test_topic_merge PASSED
    tests/unit/test_forum_models.py::test_forum_update_read PASSED
    tests/unit/test_forum_models.py::test_forum_url PASSED
    tests/unit/utils/test_helpers.py::test_slugify PASSED
    tests/unit/test_forum_models.py::test_forum_save PASSED
    tests/unit/test_forum_models.py::test_forum_get_topics PASSED
    tests/unit/test_forum_models.py::test_forum_slugify PASSED
    tests/unit/test_forum_models.py::test_forum_delete PASSED
    tests/unit/utils/test_helpers.py::test_forum_is_unread PASSED
    tests/unit/utils/test_permissions.py::test_moderator_permissions_without_forum PASSED
    tests/unit/test_forum_models.py::test_category_delete_with_forum PASSED
    tests/unit/test_forum_models.py::test_topic_merge_other_forum PASSED
    tests/unit/test_forum_models.py::test_category_get_forums PASSED
    tests/unit/test_forum_models.py::test_topic_slug PASSED
    tests/unit/utils/test_permissions.py::test_normal_permissions PASSED
    tests/unit/utils/test_widgets.py::test_select_date_widget PASSED
    tests/unit/test_forum_models.py::test_forumsread PASSED
    tests/unit/test_forum_models.py::test_topic_tracker_needs_update_cleared PASSED
    tests/unit/test_forum_models.py::test_category_save PASSED
    tests/unit/test_forum_models.py::test_category_get_all PASSED
    tests/unit/utils/test_permissions.py::test_moderator_permissions_in_forum PASSED
    tests/unit/test_forum_models.py::test_forum_update_read_two_topics PASSED
    tests/unit/test_forum_models.py::test_category_delete PASSED
    tests/unit/utils/test_permissions.py::test_admin_permissions PASSED
    tests/unit/test_forum_models.py::test_topicsread PASSED
    tests/unit/test_forum_models.py::test_forum_delete_with_user_and_topic PASSED
    tests/unit/test_forum_models.py::test_post_save PASSED
    tests/unit/test_forum_models.py::test_category_delete_with_user PASSED
    tests/unit/test_forum_models.py::test_topic_delete PASSED
    tests/unit/test_forum_models.py::test_post_delete PASSED
    tests/unit/test_forum_models.py::test_topic_update_read PASSED
    tests/unit/test_forum_models.py::test_topic_move_same_forum PASSED
    tests/unit/utils/test_populate.py::test_create_default_groups PASSED
    tests/unit/test_forum_models.py::test_forum_get_forum PASSED
    tests/unit/test_forum_models.py::test_topic_tracker_needs_update PASSED
    tests/unit/test_forum_models.py::test_report PASSED
    tests/unit/test_forum_models.py::test_forum_update_last_post PASSED

    ========================== 42 passed in 20.21 seconds ==========================

我们可以看到总共有42个测试例，全部测试通过了。

## 通过实例来看pytest的运行机制

`tests/unit/test_forum_modules.py`里有个删除讨论区版块的单元测试函数：

    #!python
    def test_forum_delete(forum):
        """Test the delete forum method."""
        forum.delete()

        forum = Forum.query.filter_by(id=forum.id).first()

        assert forum is None

代码很简单，先调用`forum.delete()`来删除一个讨论区版块，接着从`Forum`里查询这个讨论区版块，应该是查询不到的，因为这个版块已经被删除了。

问题来了：

1. 单元测试函数`test_forum_delete(forum)`运行时的上下文环境是什么？
2. 单元测试函数的参数`forum`是哪里来的？
3. pytest怎么发现`test_forum_delete(forum)`单元测试函数并执行它的？

要回答这些问题，必须介绍pytest的fixtures的概念。

## 什么是fixtures

fixtures是指测试的上下文，单元测试函数在运行之前，必须为其创建有效的运行时上下文信息。在xUnit测试框架里，每个测试例运行时都有setup/teardown方法与之匹配，pytest不但支持经典的setup/teardown方法，借助python强大的自省功能，它支持通过测试函数的参数为单元测试函数创建运行时的上下文信息。在上例中，函数参数`forum`就是一个fixtures，它定义在`tests/fixtures/forum.py`里：

    #!python
    @pytest.fixture
    def forum(category, default_settings):
        """A single forum in a category."""
        forum = Forum(title="Test Forum", category_id=category.id)
        forum.save()
        return forum

`@pytest.fixture`装饰器告诉pytest，这是一个fixture。函数体很简单，就是创建一个forum，并保存在数据库里，最后返回这个forum实例。我们可以简单地理解成，在执行`test_forum_delete(forum)`之前，单元测试例的函数参数`forum`就是通过调用定义在`tests/fixtures/forum.py`里的fixture函数`forum()`创建出来并返回的。而作为fixture函数的`forum()`本身也引用了名字叫`category`和`default_settings`的fixtures。

到此我们可以总结一下fixtures的特点：

1. fixtures有明确的名字，并且通过在单元测试函数，测试类等的声明来调用。
2. fixtures使用模块化来实现，一个fixture函数可以引用别的fixture。
3. fixtures可以支持简单的单元测试以及复杂的功能测试，还可以配置在不同的测试例之间共用fixture。

FlaskBB的自动测试程序里，其所有的fixtures都定义在`tests/fixtures`目录下的三个文件里`app.py`，`forum.py`和`user.py`，其他的fixture都很好理解，定义在`app.py`里的`application`代码有点特殊：

    #!python
    @pytest.yield_fixture(autouse=True)
    def application():
        """application with context."""
        app = create_app(Config)

        ctx = app.app_context()
        ctx.push()

        yield app

        ctx.pop()

这里使用`@pytest.yield_fixture`来定义一个生成器fixture。其次注意到使用了`autouse=True`的参数，这个参数表示这个fixture在运行任何一个单元测试函数之前都必须先调用。即所有的单元测试函数都信赖这个fixture。从函数内容来看，它创建一个Flask APP的实例，以这个实例作为单元测试的上下文。

## pytest标准的测试例收集流程

pytest在运行测试例前，必须通过一套规则来收集所有的测试例。默认情况下，pytest的测试例收集流程如下：

1. 在运行`py.test`命令的当前目录或其后第一个参数（可以上目录，或模块名）所指定的位置开始收集测试例
2. 从起始目录递归查找所有的文件及子文件夹（包含在`norecursedirs`配置参数里的文件夹不会被搜索）
3. `test_*.py`或`*_test.py`将会按照python包结构被import进测试的上下文
4. 以`Test`开头的类将作为测试类被收集起来
5. 以`test_`开头的函数将作为单元测试函数被收集起来

当然，这个测试例收集规则是可以定制的，具体可参阅pytest的[官方文档][1]。

FlaskBB的单元测试代码都放在`tests/unit`目录下。所有以`test_`打头的文件都会被import进测试的上下文。同时所有python文件里以`test_`打头的函数都被作为单元测试函数被收集起来测试。这样我们前文提到的`test_forum_delete(forum)`函数就被作为一个单元测试函数收集起来了。

## conftest.py

pytest在执行任何一个单元测试的时候，最靠近执行目录下的那个`conftest.py`将被自动执行。针对FlaskBB，其内容为：

    #!python
    from tests.fixtures.app import *
    from tests.fixtures.forum import *
    from tests.fixtures.user import *

从代码来看，它import了我们定义的所有的fixtures。除了自定义的fixtures之外，系统也有一些内置的fixtures，可以运行`py.test --fixtures`来查阅所有的可用fixtures。

## pytest.ini

pytest在执行时，会读取命令运行目录下的pytest.ini文件，通过这个文件可以定制py.test命令的一些行为。FlaskBB的里pytest.ini的内容为：

    :::ini
    [pytest]
    norecursedirs = docs flaskbb logs migrations whoosh_index
    addopts = --strict --random -vvl

其中`norecursedirs`表示在递归查找测试例时，忽略docs flaskbb等目录。`addopts`为py.test命令添加一些自定义的选项。

!!! Note "py.test运行方式"
    笔者在第一次运行FlaskBB测试程序时，使用`py.test`直接运行，结果发现执行花了很长的时间，而且很多失败项。经查，原来在笔者的环境里，通过virtualenv把`.venv`目录放在了项目的根目录下，所以默认情况下pytest会从`.venv`里收集其他包的测试例来测试。所以，虽然可以定义`norecursedirs`目录，但还是推荐使用`py.test tests`这种后面直接跟着测试代码目录的方式来运行测试例。


## 结束语

通过上文的分析，可以轻松理解FlaskBB里的自动测试代码。在Quara上看到过一篇介绍Quara的continuous development的文章，Quara的网站每天会更新上百次，这是怎么做到的呢？如果没有自动化测试和自动化布署的工具，这是不可想象的。如果做黑盒测试，光回归测试就要累死人。有兴趣的同学可以[点击这里][2]看一下高大上的互联网公司是怎么做自动化测试和布署的。

[1]: http://pytest.org/latest/contents.html#toc
[2]: http://engineering.quora.com/Continuous-Deployment-at-Quora

