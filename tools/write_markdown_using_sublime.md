用sublime来撰写markdown文档
==========================

[TOC]

##什么是markdown
markdown的目标是 __易读易写__。用markdown可以非常容易地写出图文并茂，排版优美的文档。可以点击下面这个[例子](https://github.com/revolunet/sublimetext-markdown-preview)查看由markdown撰写的内容在浏览器里的样式。

##安装Markdown Preview插件
推荐的安装方法是通过[Package Control][2]来安装：
1. 如果你的sublime还没有安装[Package Control][2]，需要先[点击这里][2]查看安装方法
2. 使用 `ctrl + shift + P` 来打开命令窗口，输入并选择 `Package Control: Install Package`
3. 在弹出的窗口里，输入 `Markdown Preview`并按回车来安装

##配置Markdown Preview插件

* 配置快捷键
通过 `Preferences -> Key Bindings - User`打开sublime的快捷键配置文件，把下面内容加到这个设置文件里，保存

```json
{"keys": ["alt+m"], "command": "markdown_preview", "args": {"target": "browser", "parser":"markdown"}}
```

配置完成后，直接在markdown编辑的时候，按下alt + m即可直接在浏览器里预览写作效果。

* 配置css文件
Markdown Preview生成的HTML文件，在浏览器里查看时其默认的宽度为45em，如果你觉得生成的网页太窄，可以修改一下css文件。

打开Markdown Preview的安装目录，找到markdown.css和github.css文件，分别查找下面的内容：

```css
    body {
      width: 45em;
      border: 1px solid #ddd;
      outline: 1300px solid #fff;
      margin: 16px auto;
    }
```
把里面的 __45em__ 修改为 __80%__ 或者你认为合适的尺寸即可。

* Linux环境

通过 `Package Control: List Packages` ，在己安装的Packages里选择 `Markdown Preview` 会直接打开Markdown Preview的安装目录，在打开的目录中直接可以找到markdown.css和github.css。

* Windows环境

在sublime安装目录下，找到 `Data\Installed Packages` 目录，这个目录就是安装包的目录。如果已经安装好Markdown Preview，可以看到文件 `Markdown Preview.sublime-package` 。这个其实是一个zip包。直接用系统里的压缩工具打开，然后在压缩包的根目录下查找markdown.css和github.css，按照上述方法修改即可。 __修改完成直接保存回压缩包即可__ 。需要注意，在打开压缩包修改的时候，必须关闭sublime，否则无法修改成功。

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
[2]: https://sublime.wbond.net/