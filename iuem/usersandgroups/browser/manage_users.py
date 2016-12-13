# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView
import transaction

from plone import api

from iuem.usersandgroups import utils

# from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class manageUsers(BrowserView):

    def __call__(self):
        # iuem_groups = getIuemGroups()
        # utils.create_group_and_users('iuem')
        # utils.delete_group_and_users('iuem')
        # utils.create_group_and_users('comiuem')
        # utils.create_group_and_users('feiri')
        # utils.create_group_and_users('ecofluxweb')
        # utils.delete_group_and_users('feiri')
        utils.update_users_password()
        # import pdb;pdb.set_trace()

