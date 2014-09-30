用sublime来撰写markdown文档
============================

[TOC]

##摘要

本文包含两部分内容：

1. 在sublime里安装Markdown Preview插件来实现markdown文件的预览
2. 介绍markdown常用的语法，让初次接触markdown的人可以在短时间内掌握常用的语法和句法

##什么是markdown

> Markdown 是一种轻量级标记语言，它允许人们使用**易读易写**的**纯文本格式**编写文档，然后转换成**格式丰富的HTML页面**。    —— [维基百科](https://zh.wikipedia.org/wiki/Markdown)

##安装Markdown Preview插件

推荐的安装方法是通过[Package Control][2]来安装：
1. 如果你的sublime还没有安装[Package Control][2]，需要先点击[这里][2]查看安装方法
2. 使用 `ctrl + shift + P` 来打开命令窗口，输入并选择 `Package Control: Install Package`
3. 在弹出的窗口里，输入 `Markdown Preview`并按回车来完成安装

##配置Markdown Preview插件

###配置快捷键

通过 `Preferences -> Key Bindings - User`打开sublime的快捷键配置文件，把下面内容复制到这个设置文件里保存。
```json
{ "keys": ["alt+m"], "command": "markdown_preview", "args": {"target": "browser", "parser":"markdown"} }
```
配置完成后，按下`alt + m`即可直接在浏览器里预览markdown的写作效果。

###配置css文件

Markdown Preview生成的HTML文件，在浏览器里查看时其默认的宽度为45em，如果你觉得生成的网页太窄，可以修改一下css文件。
打开Markdown Preview的安装目录，找到markdown.css和github.css文件，查找下面的内容：
```json
    body {
      width: 45em;
      border: 1px solid #ddd;
      outline: 1300px solid #fff;
      margin: 16px auto;
    }
```

把里面的 __45em__ 修改为 __80%__ 或者你认为合适的尺寸即可。

!!! Note
    * Linux环境：通过 `Package Control: List Packages` ，在己安装的Packages里选择 `Markdown Preview` 会直接打开Markdown Preview的安装目录，在打开的目录中直接可以找到markdown.css和github.css。
    * Windows环境：在sublime安装目录下，找到 `Data\Installed Packages` 目录，这个目录就是安装包的目录。如果已经安装好Markdown Preview，可以看到文件 `Markdown Preview.sublime-package` 。这个其实是一个zip包。直接用系统里的压缩工具打开，然后在压缩包的根目录下查找markdown.css和github.css，按照上述方法修改即可。**修改完成需要保存回压缩包**。在打开压缩包修改的时候，必须关闭sublime，否则无法修改成功。

##几个常用的markdown语法

###标题

```markdown
标题1
=====

#标题1

##标题2

###标题3
```

###列表

```markdown
* 列表1
* 列表2
* 列表3

- 列表1
- **列表2**
- 列表3

1 列表1
2 列表2
3 列表3
```

###弹出式注释

```markdown
把鼠标停留在**HTML**和**W3C**上看会发生什么。

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium
```

###定义列表

```markdown
Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.
```

###代码片段

```markdown
    ```python
        #!python
        # -*- coding: utf-8 -*-
        from flask import Flask, render_template

        app = Flask(__name__)
        app.debug = APP_DEBUG

        #homepage just for fun
        @app.route('/')
        def home():
            return render_template('index.html')
    ```
```

###角注

```markdown
Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".
```

###表格

```markdown
First Header  | Second Header
--------------|--------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```

###警告

```markdown
!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph.
```

###强调

```markdown
这是**黑体**写法
这是*斜体*的写法
```

###超链接

```markdown
这是一个[链接](https://github.com/kamidox/blogs)
这是另外一种[链接][1]的形式

[1]: https://pythonhosted.org/Markdown/extensions/index.html
```

###引用

```markdown
> 引用的文字内容
> 这是另外的引用内容
```

###图片

```markdown
![图片描述](https://raw.githubusercontent.com/karan/Hook/master/logo.png)
```

###目录

```markdown
[TOC]
```

##练习
1. 直接在配置好的sublime里新建一个readme.md，把上面的markdown语法拷贝进去练习一下。
2. 推荐一个做得相当不错的markdown在线编辑器[马克飞象](http://maxiang.info/)。
3. 本文就是用markdown编写的。右键点击[这里][3]，另存到本地即可。


[1]: https://pythonhosted.org/Markdown/extensions/index.html
[2]: https://sublime.wbond.net/
[3]: https://raw.githubusercontent.com/kamidox/blogs/master/tools/write_markdown_using_sublime.md
