# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView

from iuem.usersandgroups import utils

# from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class manageUsers(BrowserView):

    def __call__(self):
        # iuem_groups = getIuemGroups()
        # utils.createGroupAndUsers('iuem')
        # utils.deleteGroupAndUsers('iuem')
        # utils.createGroupAndUsers('comiuem')
        # utils.createGroupAndUsers('feiri')
        utils.createGroupAndUsers('ecofluxweb')
        # utils.deleteGroupAndUsers('ecofluxweb')
        # utils.deleteGroupAndUsers('feiri')
        # utils.updateUsersPassword()
        # import pdb;pdb.set_trace()
