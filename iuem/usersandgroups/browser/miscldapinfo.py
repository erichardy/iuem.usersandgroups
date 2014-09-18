# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView
from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class miscLdapInfo(BrowserView):
    pass

