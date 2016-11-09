Title: React 最佳实践示例项目
Date: 2016-11-09 22:52
Modified: 2016-11-09 22:52
Tags: react
Slug: react-best-practise-demo
Authors: Joey Huang
Summary: Github 上已经有一堆基于 React 的 HackerNews 客户端，为什么还需要写一个新的？

这一个是用 React 实现的 HackerNews 客户端，项目地址在这 [react-hacker-news](https://github.com/kamidox/react-hacker-news)。

## 写在前面

GitHub 上已经有一堆基于 React 的 HackerNews 客户端，为什么还需要写一个新的？

原因是前端技术发展太快了。如果你看过[《2016年里做前端是怎样一种体验》](https://segmentfault.com/a/1190000007083024)，除了一笑而过之外，还想了解文章里的那些把人搞晕的名词和术语，那么这篇文章会有一些有用的信息。

另外一个原因是，GitHub 上很多项目代码都有点过时，比如广为传播且 star 数最多的 [insin/react-hn](https://github.com/insin/react-hn) 使用 ES5 编写，且没有单元测试。

最后，我决定厚着脸皮，抛个砖，引个玉。这个 demo 项目是我学习 React 框架时做的第一个较完整的项目。我决定献丑写出来，可能对一些初学者有帮助。如果有幸遇到牛人指点一二，纠正我的错误观念，那就更好了。

正式开始之前，可以体验一下项目的成果：[react-hacker-news](https://kamidox.github.io/react-hacker-news/)。

## 最佳实践

哪些可以算得上 React 开发的最佳实践？我们展开看看。

* ES6: 绝大部分代码使用 ES6 代码编写。特别是 React Component 相关的代码也使用 ES6 语法。除了少敲点字外，最大的好处是整洁。
* eslint-config-airbnb: 这是一个 eslint 扩展。用完这个插件，真正体会到站在巨人的肩膀上的感觉。这个插件可能会帮助你纠正很多你平时根本没意识到的不良编码习惯。
* webpack/babel: 使用 babel 把 ES6/React 代码编译成浏览器广泛支持的 ES5 代码，使用 webpack 打包以及开发环境/生产环境管理。
* 持续集成：使用 `ghooks` 实现提交前的代码静态分析，以及 git commit msg 的格式检查。当然，这里还可以配置，在提交前自动执行单元测试。
* 提交记录规范: 有的人会在 git commit message 里骂人，有的会在里面写微型小说，程序员这个群体总是不缺创意。但这里，我们借助 [AngularJS 的规范](https://github.com/angular/angular.js/blob/master/CONTRIBUTING.md#-git-commit-guidelines)。如果没有按照规范写 commit message 提交前无法通过自动检查。还有一个好处是，可以直接使用一个命令生成 change log。
* 单元测试：使用 Mocha/Enzyme/chai/sinon 来做 React 的单元测试。国情因素，单元测试往往得不到重视。但从工程的角度，单元测试是质量保证的最重要工具之一。单元测试可以让代码取得别人天然的信任。
* Log 系统: 使用轻量级的 `loglevel` 来打印应用的调试信息。如果你还在使用 `console.log()` 来打印 Log，是时候规范一点了。
* 一键部署到 GitHub Pages：辛辛苦苦开发的应用，想和小伙伴们分享一下。没问题，一键即可部署到 GitHub Pages 上。要使用这个功能，你需要有 Python 环境，并且使用 `pip install ghp-import` 安装一个 `ghp-import`。

## 总结

荣耀属于阮一峰，只要你没有恐高症，站在巨人的肩膀上是个很好的提高效率的方式。这个项目以 [ruanyf/react-babel-webpack-boilerplate](https://github.com/ruanyf/react-babel-webpack-boilerplate) 作为起点开发的。远不止于此，阮一峰还在他博客上写下[React 技术栈系列教程](http://www.ruanyifeng.com/blog/2016/09/react-technology-stack.html)，推荐初学者阅读。

我 Fork 阮一峰的 boilerplate 项目，增加了几个 Feature:

* 把静态文件移到 `public` 目录下
* 增加单元测试工具集
* 增加一键部署到 GitHub Pages 功能

项目地址是 [kamidox/react-babel-webpack-boilerplate](https://github.com/kamidox/react-babel-webpack-boilerplate)，如果你认同这里阐述的开发理念，可以作为 React 项目的开发起点。


