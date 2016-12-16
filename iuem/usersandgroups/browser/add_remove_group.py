# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView

from iuem.usersandgroups import utils

# from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups:manageGroup')


class addRemoveGroup(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # iuem_groups = getIuemGroups()
        # utils.createGroupAndUsers('iuem')
        # utils.deleteGroupAndUsers('iuem')
        # utils.createGroupAndUsers('comiuem')
        # utils.createGroupAndUsers('feiri')
        # utils.createGroupAndUsers('ecofluxweb')
        # utils.deleteGroupAndUsers('ecofluxweb')
        # utils.deleteGroupAndUsers('feiri')
        # utils.updateUsersPassword()
        pass

    def __call__(self, group, operation):
        logger.info(group)
        logger.info(operation)
        if operation == 'install':
            utils.createGroupAndUsers(group)
            return group + ' installed'
        if operation == 'uninstall':
            utils.deleteGroupAndUsers(group)
            return group + ' uninstalled'
        return 'nothing to do'
