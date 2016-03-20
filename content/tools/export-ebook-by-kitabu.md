Title: 用 kitabu/princexml 制作高颜值的电子书
Date: 2016-03-20 21:15
Modified: 2016-03-20 21:15
Tags: markdown, ebook
Slug: export-ebook-by-kitabu
Authors: Joey Huang
Summary: 辛辛苦苦用 markdown 写就了一系列文章，怎么样导出制作成一本高颜值的电子书呢？本文有你需要的答案。

辛辛苦苦用 markdown 写就了一系列文章，怎么样导出制作成一本高颜值的电子书呢？本文介绍一种在 Mac 下使用 kitabu + princexml 导出高颜值电子书的方法。

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

## 配置

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

## 可能遇到的问题

另外，我自己写作过程中，直接把图片放在本地目录，然后使用相对路径在 markdown 里生成图片，比如：

```markdown
![正弦曲线](images/ch02.01.png)
```

否则就得找图床，生成电子书时还会从图床下载图片。所以直接放在本地，用相对路径引用是个相对经济的方案。默认情况下，kitabu 是不认本地相对路径的图片的。这时需要 hack 一下 kitabu，因为默认情况下，kitabu 启用了安全链接的功能，我们可以把这个功能关闭掉。

首先找到 kitabu 包的安装目录，可以使用 `gem help install` 命令，然后在输出中找 `--install-dir` 字段，比如我的机器上有这样的输出：

```
bogon:mybook kamidox$ gem help install
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

## 结语

差不多就这些。奋力写作吧，只为自己成为自己的出版商。
