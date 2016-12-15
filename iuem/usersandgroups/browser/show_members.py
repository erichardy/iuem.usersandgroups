# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView

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

    def getMembers(self, n):
        """
        :param n: le nombre d'éléments par ligne
        :type n: int
        :returns: une liste de listes, les listes "secondaires" contiennent
            n éléments
        """
        members = self.request.get('members').split(',')
        lmembers = len(members)
        if members:
            members.sort()
            comp = []
            for nb in range(0, lmembers, n):
                l1 = []
                for lnb in range(nb, nb + n):
                    if lnb < lmembers:
                        l1.append(members[lnb])
                comp.append(l1)
                nb = lnb + 1
            return comp
        else:
            return []
