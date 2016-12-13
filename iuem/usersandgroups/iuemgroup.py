# -*- coding: utf-8 -*-

import logging
from zope.interface import implements

from plone import api

from iuem.usersandgroups.interfaces import IiuemGroup
from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups:iuemGroup')


class iuemGroup(object):
    implements(IiuemGroup)

    def includesMembers(self, membersList):
        """
        :type membersList: list
        :param membersList: les identifiants des membres d'un groupe
        :returns: True si les membres de ``membersList`` font partie du groupe
        """
        # print membersList
        if not isinstance(membersList, list):
            return False
        # on traite tout de suite le cas où la liste membersList est
        # plus grande que self.members
        if len(membersList) > len(self.members):
            return False
        # on traite le cas special ou le proprietaire est root
        if membersList == ['root']:
            return True
        result = [member for member in membersList if member in self.members]
        if len(result) > 0:
            return True
        return False
