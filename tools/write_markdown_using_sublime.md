用sublime来撰写markdown文档
==========================

[TOC]

##什么是markdown
markdown的目标是 __易读易写__。点击这个[例子](https://github.com/revolunet/sublimetext-markdown-preview)查看由markdown撰写的内容在浏览器里的样式。

##sublime的markdown插件
只需要安装markdown preview即可。默认安装的markdown preview生成的网页是45em宽度的。这个在宽屏电脑上显示效果很不好，只有中间一小截。如果要定制这个属性，可以打开markdown preview安装目录下的markdown.css。找到如下内容：
```css
    body {
      width: 45em;
      border: 1px solid #ddd;
      outline: 1300px solid #fff;
      margin: 16px auto;
    }
```
把里面的 __45em__ 修改为 __80%__ 即可。

##常用语法
* 标题
* 列表

##支持的扩展

* 缩略语

The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium

* 定义列表

Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

* 代码片段

```python
import sublime

print('hello sublime')
```

* 角注
Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".

* 表格

First Header  | Second Header
--------------|--------------
Content Cell  | Content Cell
Content Cell  | Content Cell

* 警告

!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph.

* 黑体
This is __out of__ admonition!!!

* 代码片段

```python
    #!python
    # -*- coding: utf-8 -*-
    import hashlib, time
    import xml.etree.ElementTree as ET
    from flask import Flask, request, render_template
    from private_const import *
    import view

    app = Flask(__name__)
    app.debug = APP_DEBUG

    #homepage just for fun
    @app.route('/')
    def home():
        return render_template('index.html')
```

[1]: https://pythonhosted.org/Markdown/extensions/index.html
