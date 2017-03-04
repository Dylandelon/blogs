Title: 用 kitabu 制作高颜值的电子书
Date: 2016-03-20 21:15
Modified: 2017-02-26 23:15
Tags: markdown, ebook
Slug: export-ebook-by-kitabu
Authors: Joey Huang
Summary: 辛辛苦苦用 markdown 写就了一系列文章，怎么样导出制作成一本高颜值的电子书呢？本文有你需要的答案。

辛辛苦苦用 markdown 写就了一系列文章，怎么样导出制作成一本高颜值的电子书呢？本文介绍一种在 Mac 下使用 kitabu + princexml 导出高颜值电子书的方法。

本文还介绍了字体定制，排版定制，代码高亮，使用 MathJax 渲染 LaTex 数学公式等方法。

## 安装软件

首先安装 [kitabu](https://github.com/fnando/kitabu)

```shell
gem install kitabu
```

这是个开源的 Ruby 包，主要提供电子书模板和制作过程自动化的功能。如果你没使用过 ruby ，可能在使用 `gem install kitabu` 时报错 `Errno::ECONNRESET: Connection reset by peer`，可以试试切换 taobao 的 [RubyGems 镜像](https://ruby.taobao.org)：

```
$ gem sources --add https://ruby.taobao.org/ --remove https://rubygems.org/
$ gem sources -l
*** CURRENT SOURCES ***

https://ruby.taobao.org
```

如果发现无法编译 kitabu extension：

```
ERROR: Failed to build gem native extension.
```

可以试试安装命令行的 xcode 工具：`xcode-select --install`，安装完成后，再用 `gem install kitabu` 来安装 kitabu。需要注意的事，当升级 ruby 版本时，需要重新安装 kitabu 工具。或者切换到旧版本的 ruby 运行环境中运行。

接着安装 [princexml](http://princexml.com)，可以从官网 princexml.com 下载免费的安装包。princexml 会完成从 html 转为为 pdf 功能。安装完这两个工具后，可以用 `kitabu check` 命令检查一下是否安装成功：

```shell
bogon:~ kamidox$ kitabu check

Prince XML: Converts HTML files into PDF files.
Installed.

KindleGen: Converts ePub e-books into .mobi files.
Installed.

html2text: Converts HTML documents into plain text.
Not installed.
```

我的环境里多安装了 KindleGen ，如果你需要制作 .mobi 格式的电子书，可以使用 `brew install kindlegen` 来安装。不过这一步不是必须的。

## 制作电子书

接着在工作目录执行 `kitabu new mybook` 即可创建 kitabu 电子书的模板：

```
mybook/
├── Gemfile
├── Guardfile
├── config
│   ├── helper.rb
│   └── kitabu.yml
├── fonts
├── images
│   ├── kitabu-icon.png
│   ├── kitabu-icon.svg
│   ├── kitabu-word.png
│   ├── kitabu-word.svg
│   ├── kitabu.png
│   └── kitabu.svg
├── output
├── templates
│   ├── epub
│   │   ├── cover.erb
│   │   ├── cover.png
│   │   └── page.erb
│   ├── html
│   │   └── layout.erb
│   └── styles
│       ├── epub.scss
│       ├── files
│       │   └── _normalize.scss
│       ├── html.scss
│       ├── pdf.scss
│       └── print.scss
└── text
    ├── 01_Getting_Started.md
    ├── 02_Creating_Chapters.md
    ├── 03_Syntax_Highlighting.erb
    ├── 04_Dynamic_Content.erb
    └── 05_Exporting_Files.md
```

然后在 `mybook` 目录运行 `kitabu export` 即可在 `output` 目录下生成电子书了。默认情况下，会生成 [kitabu 使用说明文档](https://github.com/fnando/kitabu/raw/master/attachments/kitabu.pdf)。

## 基础配置

要制作自己的电子书，需要做些简单的配置。先把 kitabu 模板的 `text` 目录清空，然后把自己的 markdown 文件拷贝到这个目录下，需要注意的是 kitabu 是使用文件名排序生成电子书，并且会自动把 2-6 级标题自动生成书籍的目录。如果你的 markdown 文件是以 1 级标题开始，则需要把所有的标题降一个等级。

接着修改 `config/kitabu.yml` 把书箱的作者，版权声明，出版商的信息补充完整。然后修改 `templates` 目录下的 css 文件，让生成的电子书更漂亮。

我自己主要修改两处。一是修改 `templates/styles/pdf.scss`，在所有的 `font-family` 字段里添加 `PingFang SC`，以便使用 Mac 的苹方字体来显示中文，默认字体中文效果比较差。比如：

```
body {
  font-family: Caslon, serif;
  font-size: 14px;
  line-height: 1.5;
}
```

改成

```
body {
  font-family: PingFang SC, Caslon, serif;
  font-size: 14px;
  line-height: 1.5;
}
```

二是修改图片的宽度，以便电子书里的图片能自动缩放，避免大图片显示不全的问题。这个主要是修改 `templates/styles/files/_normalize.scss`：

```
img {
  border: 0;
}
```

改成：

```
img {
  border: 0;
  width: 100%;
}
```

这样生成的电子书颜值就很高了。如果你是前端工程师，折腾一下 css 可以做出更精美的电子书。

## 在电子书中插入图片

另外，我自己写作过程中，直接把图片放在本地目录，然后使用相对路径在 markdown 里生成图片，比如：

```markdown
![正弦曲线](images/ch02.01.png)
```

否则就得找图床，生成电子书时还会从图床下载图片。所以直接放在本地，用相对路径引用是个相对经济的方案。默认情况下，kitabu 是不认本地相对路径的图片的。这时需要 hack 一下 kitabu，因为默认情况下，kitabu 启用了安全链接的功能，我们可以把这个功能关闭掉。

首先找到 kitabu 包的安装目录，可以使用 `gem help install` 命令，然后在输出中找 `--install-dir` 字段，比如我的机器上有这样的输出：

```
$ gem help install
  ... ...
  Defaults:
    --both --version '>= 0' --document --no-force
    --install-dir /usr/local/lib/ruby/gems/2.3.0 --lock
```

然后进入 `/usr/local/lib/ruby/gems/2.3.0/gems/kitabu-2.0.4/` 目录，打开 `lib/kitabu/markdown.rb` 文件，把

```ruby
renderer = Renderer.new(hard_wrap: true, safe_links_only: true)
```

修改为

```ruby
renderer = Renderer.new(hard_wrap: true, safe_links_only: false)
```

## 支持 LaTex 公式

[MathJax](http://www.mathjax.org/) 是一个 JavaScript 库，用来渲染 LaTex 格式的数学公式。如果你想了解怎么样在 Markdown 里书写数学公式，可以参考我之前的一篇博客 [《使用 Markdown + MathJax 在博客里插入数学公式》](http://blog.kamidox.com/write-math-formula-with-mathjax.html)。

默认情况下，kitabu 无法在渲染使用 MathJax 在 markdown 里书写的数学公式。其原因是 princexml 不支持 Window 等对象，所以 MathJax 的 JavaScript 脚本无法执行。

解决这个问题的思路是，使用 [Phantomjs](http://phantomjs.org) 来渲染包含 LaTex 数学公式的 html 页面，由于 Phantomjs 可以正确地执行 MathJax 的 JavaScript 脚本，所以能正确地渲染出数学公式。接着再使用 princexml 来生成 PDF 格式的电子书就可以正确地渲染出数学公式了。思路很简单，操作起来还是有点麻烦。

**首先**，安装 Phantomjs 工具，可以在[官网下载](http://phantomjs.org/download.html)安装适合你的操作系统的版本。在 macOS 上，下载下来的是一个绿色安装包，我把它放在硬盘的合适位置后，把 `/bin/phantomjs` 加入到 PATH 变量里，以便在命令行中能直接执行这个命令。

```shell
$ tree ~/tools/phantomjs/
~/tools/phantomjs/
├── ChangeLog
├── LICENSE.BSD
├── README.md
├── bin
│   └── phantomjs
├── examples
```

**接着**，安装 MathJax ，方法是把 [MathJax](https://github.com/mathjax/MathJax/archive/2.7.0.zip) 下载到电子书的目录。比如，你使用 `kitabu new mybook` 时，则把 MathJax 下载后解压到 `mybook` 目录下，我使用的是 MathJax 2.7.0 版本。

**接着**，再把 [MathJaxRender.js](https://raw.githubusercontent.com/kamidox/blogs/master/images/MathJaxRender.js) 和 [MathJaxConfig.js](https://raw.githubusercontent.com/kamidox/blogs/master/images/MathJaxConfig.js) 也下载到 `mybook` 目录下。这两个分别是 phantomjs 渲染脚本和 MathJax 配置文件。需要**特别注意**，MathJaxConfig.js 不要修改文件名，如果修改了文件名，很多引用的地方也要跟着同步修改。

**接着**，还要 hack 一下 kitabu，其目的是配置 Redcarpet (这是把 markdown 转成 html 的 ruby 库)，关闭智能脚本渲染，即把 `superscript` 改为 `false` ，否则会和 MathJax 冲突。

方法是进入 `/usr/local/lib/ruby/gems/2.3.0/gems/kitabu-2.0.4/` 目录，打开 `lib/kitabu/markdown.rb` 文件，把

```ruby
    self.processor = Redcarpet::Markdown.new(renderer, {
      tables: true,
      footnotes: true,
      space_after_headers: true,
      superscript: true,
      highlight: true,
      strikethrough: true,
      autolink: true,
      fenced_code_blocks: true,
      no_intra_emphasis: true
    })
```

修改为

```ruby
    self.processor = Redcarpet::Markdown.new(renderer, {
      tables: true,
      footnotes: true,
      space_after_headers: true,
      superscript: false,
      highlight: true,
      strikethrough: true,
      autolink: true,
      fenced_code_blocks: true,
      no_intra_emphasis: true
    })
```

**最后**，修改 `mybook/templates/html/layout.erb` 文件，以便在模板里引入 MathJax 及其配置文件，方法是在其 `head` 标签下插入如下内容，

```html
    <!-- add LaTeX support by MathJax -->
    <script type="text/javascript" src="../MathJax/MathJax.js"></script>
    <script type="text/javascript" src="../MathJaxConfig.js"></script>
```

即，把

```html
  <head>
    <title><%= title %></title>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <link name="stylesheet" rel="stylesheet" type="text/css" href="styles/html.css" />
    <meta name="author" content="<%= authors.join(', ') %>" />
    <meta name="subject" content="<%= subject %>" />
    <meta name="keywords" content="<%= keywords %>" />
    <meta name="date" content="<%= published_at %>" />

    <%= highlight_theme %>
  </head>
```

改成

```html
  <head>
    <title><%= title %></title>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <link name="stylesheet" rel="stylesheet" type="text/css" href="styles/html.css" />
    <meta name="author" content="<%= authors.join(', ') %>" />
    <meta name="subject" content="<%= subject %>" />
    <meta name="keywords" content="<%= keywords %>" />
    <meta name="date" content="<%= published_at %>" />
    <!-- add LaTeX support by MathJax -->
    <script type="text/javascript" src="../MathJax/MathJax.js"></script>
    <script type="text/javascript" src="../MathJaxConfig.js"></script>

    <%= highlight_theme %>
  </head>
```

完成这些步骤后，我的电子书目录看起来像这样：

```shell
mybook/
├── Gemfile
├── Guardfile
├── MathJax
│   └── MathJax.js
├── MathJaxConfig.js
├── MathJaxRender.js
├── build-ebook.sh
├── config
├── fonts
├── images
├── output
├── templates
└── text
```

`build-ebook.sh` 的内容是这样的：

```shell
kitabu export --only=pdf
cd output
phantomjs ../MathJaxRender.js kitabu-ebook.pdf.html | prince --javascript -o ml-scikit-learn.pdf -
cd ..
```

其中调用 `phantomjs` 的那行命令就是用来生成带数学公式的电子书的。不要忘记了这个命令最后还有一个 `-` 字符，意思是从 stdin 里读取输入来转换为 PDF。

参考文档： [Using MathJax with PrinceXML](http://www.princexml.com/forum/topic/2971/using-mathjax-with-princexml)

## 结语

差不多就这些。奋力写作吧，只为自己成为自己的出版商。
