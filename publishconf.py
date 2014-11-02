#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

AUTHOR = u'Joey Huang'
SITENAME = u"kamidox.com"
SITEURL = 'http://kamidox.com'
DISQUS_SITENAME = 'kamidox'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh_CN'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d(%A) %H:%M')

USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = 'hide'

# Feed generation is usually not desired when developing
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# menu items
MENUITEMS = [('Home', SITEURL),
            ('About', 'about.html'),]

# Blogroll
# LINKS = (('GitHub', 'https://github.com/kamidox'),)

# Social widget
# SOCIAL = (('微博', 'http://weibo.com/kamidox'),)

DEFAULT_PAGINATION = 10

MD_EXTENSIONS = [
        "extra",
        "toc",
        "headerid",
        "meta",
        "sane_lists",
        "smarty",
        "wikilinks",
        "admonition",
        "nl2br",
        "codehilite(guess_lang=False,pygments_style=emacs,noclasses=True)"]

CNZZ_ANALYTICS = True

MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/index.html'

THEME = "themes/foundation-default-colours"
#THEME = "/home/kamidox/pelican/pelican-themes/foundation-default-colours"
#THEME = "themes/tuxlite_tbs"

# usful setting for publish
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True


