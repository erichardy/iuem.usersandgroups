# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView

from plone import api

from iuem.usersandgroups import utils

# from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class showMembers(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # import pdb;pdb.set_trace()

    def getGroupName(self):
        group_name = self.request.get('name')
        if group_name:
            return group_name
        else:
            return None

    def getMembers(self):
        members = self.request.get('members')
        if members:
            return members.split(',')
        else:
            return []
