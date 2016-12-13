# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView
from AccessControl import getSecurityManager
from Products.CMFCore import permissions

from iuem.usersandgroups.utils import getGroupByGID
from iuem.usersandgroups.utils import getUserByUID

from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class manageUsers(BrowserView):

    def __call__(self):
        gr = getGroupByGID(605)
        ldapUser = getUserByUID('hardy')
        import pdb;pdb.set_trace()

