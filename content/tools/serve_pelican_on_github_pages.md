Title: 使用 Github Pages 来托管 Pelican 生成的博客
Date: 2015-08-22 23:52
Modified: 2015-08-22 23:52
Tags: github, pelican
Slug: serve-pelican-on-github-pages
Authors: Joey Huang
Summary: 本文介绍如何把 Pelican 生成的博客托管在 github 上

## 关于 Github Pages

Github Pages 是 Github 提供的免费的空间来展现静态网页。

> Websites for you and your projects. Hosted directly from your GitHub repository. Just edit, push, and your changes are live.

依照[官方文档][1]很容易做出一个 Github Pages 网页。使用 Github Pages 来写博客的主流方法是使用 [Jekyll][2] 来作为 SSG (Static Site Generator)。

## 把 Pelican 生成的博客托管在 Github Pages 上

由于历史原因使用了 Pelican 作为 SSG 并托管在 AWS 主机上。切换到 Github Pages + Jekyll 意味着更换 SSG ，这样必须把所有符合 Pelican 规则的 markdown 文件转换为符合 Jekyll 规则的 markdown 文件。于是想到了一个更偷懒的方法：直接用 Pelican 生成的静态网页放在 Github 上作为 Github Pages。最后再绑定我们自己的域名。这样就完成了迁移工作。

[ghp-import][3] 是做这个事情的最佳工具。 

发布博客时，输入下面的命令即可：`ghp-import -p output`。这个命令做以下几件事情：

1. 把 Pelican 生成的静态网页所在目录 `output` 下的所有文件写入 Git 的 `gh-pages` 分支
2. 带 `-p` 选项会把 `gh-pages` 分支上的内容 push 到 Github 上

打开 `YourUserName.github.io/YourRepoName` 就可以看到最新的博客内容了。比如 [kamidox.github.io/blogs][4] 就是我使用 Github Pages 的托管的博客了。

关于如何使用 Pelican 来写博客，可以参阅[这篇文章][5]。

## 定制域名

关于 Github Pages 定制域名可以参阅[官方教程][6]。我们使用 Github 强烈推荐的子域名的形式来寶域名，就是在 `gh-pages` 分支根目录提交一个 `CNAME` 文件，而 ghp-import 又会完全覆盖掉 gh-pages 分支。如何解决这个矛盾呢？阳光下没有新鲜事，具体可以参阅 [Pelican 的 Tips][7]。归纳起来，就是先在 `content/extra` 目录下新建一个叫 `CNAME` 的文件，其内容就是自定义域名的内容，如 `blog.kamidox.com`。然后在 Pelican 的配置文件 `publishconf.py` 下添加如下内容：


```python
STATIC_PATHS = ['extra']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},	# 这是个路径映射，即会把 `content/extra/CNAME` 文件拷贝到 `output/CNAME`
    }
```

!!! notes "注意"
    1. 留意一下上面的路径映射。如果没有这个映射，则 Pelican 会把 `content/extra` 目录下的内容原封不动的拷贝到 `output/extra` 目录下。
    2. 另外一个需要注意的是，我们提交 CNAME 子域名文件后后，不需要在域名供应商那边手动添加解析，这个过程中 Github 自动替我们完成的。


[1]: https://pages.github.com
[2]: http://jekyllrb.com
[3]: https://github.com/davisp/ghp-import
[4]: http://kamidox.github.io/blogs
[5]: http://kamidox.com/build-blog-system-by-pelican.html
[6]: https://help.github.com/articles/adding-a-cname-file-to-your-repository/
[7]: http://docs.getpelican.com/en/latest/tips.html#extra-tips

