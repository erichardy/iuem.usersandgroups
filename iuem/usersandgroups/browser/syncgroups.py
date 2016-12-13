# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView

# from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups.browser.syncgroups')


class syncGroups(BrowserView):
    def __call__(self):
        context = self.context
        acl = context.aq_parent.getAclUser()
        groups = acl.getGroups()
        # import pdb;pdb.set_trace()
        groupIds = context.keys()
        for group in groups:
            groupId = group[0]
            if groupId not in groupIds:
                logger.info('must create ' + groupId)
