# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView

from plone import api

from iuem.usersandgroups import utils

# from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups:modal')


class manageUsersModal(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
