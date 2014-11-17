Title: FlaskBB阅读笔记（三）
Date: 2014-11-08 23:00
Modified: 2014-11-08 23:00
Tags: python, flask
Slug: flaskbb-notes-3
Authors: Joey Huang
Summary: FlaskBB是用Flask实现的一个轻量级论坛社区软件。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架以及在一个产品级的Flask应用里的一些最佳实践规则。本文介绍ORM基础知识，分析Flask-SQLAlchemy及sqlalchemy ORM引擎的一些常用方法，进而介绍FlaskBB用户管理模块的数据库设计。
Status: draft

[TOC]

## 开篇

[FlaskBB][1]是用Flask框架实现的一个轻量级的论坛社区软件，代码托管在GitHub上。本系列文章通过阅读FlaskBB的源代码来深入学习Flask框架，以及在一个产品级的Flask应用里的一些最佳实践规则。

本文是本系列文章的第三篇，将介绍ORM基础知识，分析Flask-SQLAlchemy及sqlalchemy ORM引擎的一些常用方法，进而介绍FlaskBB用户管理模块的数据库设计。


