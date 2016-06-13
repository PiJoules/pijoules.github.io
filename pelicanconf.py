#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

import os

AUTHOR = u'Leonard Chan'
SITENAME = u'Stuff I worked on'
ROOT = "/"

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ["images"]

PLUGINS = [
    'pelican_githubprojects',
]
GITHUB_USER = 'pijoules'
GITHUB_SORT_BY = "created"

# Choose THEME
theme = "backdrop"
if theme == "backdrop":
    theme_path = "themes/backdrop"
    expanded_theme_path = os.path.expanduser(theme_path)
    THEME = expanded_theme_path
    PAGINATED_DIRECT_TEMPLATES = ('categories', 'archives')
    SITESUBTITLE = "Sample SITESUBTITLE"
    PROFILE_IMAGE = "/images/soldier_uber.jpg"
    BACKDROP_IMAGE = "/images/process.jpeg"
    #FAVICON = None
    SITE_DESCRIPTION = """
    Greetings! I am a student at Drexel University studying Computer and Electrical
    Engineering. This website will primarily serve as a blog/personal notebook.
    My hobbies include Python, TF2, and memes.
    """
    SOCIAL = [
        ("github", "https://github.com/PiJoules"),
    ]
    EMAIL = "lchan1994@yahoo.com"
    BLOGKEYWORDS = ["Python"]
    #LICENSE = "Unlicense"

