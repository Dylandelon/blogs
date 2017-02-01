Title: 微信小程序离线开发文档
Date: 2017-2-1 14:52
Modified: 2017-2-1 14:52
Tags: weapp
Slug: weapp-doc
Authors: Joey Huang
Summary: 边开发微信小程序边打开腾讯的微信小程序开发文档的网站，跳转慢，搜索渣？这里有一个更优雅的解决方法。

## 写在前面

程序员开发过程中离不开开发文档，微信小程序也不例外。开发微信小程序的常规姿势是边写代码，边开着微信小程序开发文档的网页，来回切换。这里有一个更优雅的解决方案。

## 微信小程序离线开发文档

* 安装 [Dash](https://kapeli.com/dash)。如果你不知道 Dash，是时候了解一下了，绝对会有相见恨晚的感觉。
* 下载 [minapp-docset](https://github.com/kamidox/html2Dash/releases/download/minapp-docset-V0.1/minapp.docset.v0.1.tar.gz)，导入 Dash 即可。

Windows 用户可以使用 [velocity](http://velocity.silverlakesoftware.com/)，Linux 用户可以使用 [Zeal](http://zealdocs.org/) 作为 Dash 的替代品。

最后的效果图长这样：

![Dash 效果图](http://upload-images.jianshu.io/upload_images/184896-d08314fbc56d99f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 背后的原理

知其然知其所以然。背后的原理其实不复杂。先使用 wget 把整个微信小程序的开发文档全部下载下来，再用一个 Python 脚本生成 Dash 格式的 docset。感兴趣的同学可以看看 [html2Dash](https://github.com/kamidox/html2Dash)，我分享到 Github 上了。

话说 wget 简直逆天，一个命令可以把一个网站全下载下来。

```shell
$ wget -r -p -k -np http://www.jianshu.com
```

**不要乱试哦，小心你的硬盘撑破肚子。**


