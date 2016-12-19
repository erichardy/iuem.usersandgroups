# -*- coding: utf-8 -*-

# sphinx configuration

project = u'iuem.usersandgroups'
copyright = u'2016, FEIRI / IUEM'

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]
master_doc = 'index'
exclude_patterns = ['links.rst', ]
html_domain_indices = True

locale_dirs = ["translated/"]
language = 'en'
# html_theme = "classic"

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual])
# This enables PDF generation.
latex_documents = [(
    'index',
    'ploneapi.tex',
    u'plone.api Documentation',
    u'', 'manual'
), ]

from pkg_resources import get_distribution
# version = release = get_distribution(project).version

import sys


class Mock(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()

MOCK_MODULES = ['lxml']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()

