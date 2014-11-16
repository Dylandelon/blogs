Title: FlaskBB阅读笔记（四）
Date: 2014-11-17 23:00
Modified: 2014-11-17 23:00
Tags: python, flask
Slug: flaskbb-notes-4
Authors: Joey Huang
Summary: FlaskBB是用Flask实现的一个轻量级论坛社区软件。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架以及在一个产品级的Flask应用里的一些最佳实践规则。本文通过分析FlaskBB的自动测试代码，进而介绍Python下的自动化测试工具pytest。

## 开篇

[FlaskBB][1]是用Flask框架实现的一个轻量级的论坛社区软件，代码托管在GitHub上。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架，以及在一个产品级的Flask应用里的一些最佳实践规则。

本文是本系列文章的第四篇，通过分析FlaskBB的自动测试代码，进而介绍Python下的自动化测试工具pytest。自动化测试在开发和重构过程中有着非常重要的地位。甚至还流行一种测试优先的编程方法，即针对一个功能模块，先写测试例，再去实现功能模块。




