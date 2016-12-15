# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView

from plone import api

from iuem.usersandgroups import utils

# from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class manageUsers(BrowserView):

    def _nothing(self):
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

    def getAccessKey(self):
        return utils.getSettingValue('updates_key')

    def getGroups(self):
        """
        :returns: une liste de tuples. Chaque tuple est composé d'un
            objet ``iuemGroup`` et d'un booléen qui indique si le
            groupe ``LDAP`` est installé comme plone groupe.
        """
        xiuem_groups = utils.getIuemGroups()
        iuem_groups = sorted(xiuem_groups, key=lambda g: g.cn.lower())
        plone_groups = api.group.get_groups()
        plone_groupsIDs = [g.id for g in plone_groups
                           if utils.getGroupByCN(g.id) is not None]
        all_groups = []
        for iuem_group in iuem_groups:
            if iuem_group.cn in plone_groupsIDs:
                element = (iuem_group, True)
            else:
                element = (iuem_group, False)
            all_groups.append(element)
        # import pdb;pdb.set_trace()
        return all_groups

    def getMembers(self, members_list):
        if isinstance(members_list, list):
            return ','.join(members_list)
        else:
            return members_list
