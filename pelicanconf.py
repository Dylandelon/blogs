#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Joey Huang'
SITENAME = u"kamidox.com"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh_CN'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d(%A) %H:%M')

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

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
        "codehilite(guess_lang=False,pygments_style=emacs,noclasses=True)"]

#THEME = "/home/kamidox/pelican/pelican-themes/foundation-default-colours"
THEME = "/home/kamidox/pelican/pelican-themes/tuxlite_tbs"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
