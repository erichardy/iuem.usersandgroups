# -*- coding: utf-8 -*-

import logging
import datetime
from zope.publisher.browser import BrowserView

from iuem.usersandgroups.utils import updateUsersPassword
from iuem.usersandgroups.utils import removeLDAPOrphanUsers
from iuem.usersandgroups.utils import getSettingValue

logger = logging.getLogger('iuem.usersandgroups:passwords_update')


class pwUpdate(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        wget http://myplone:8080/Plone/@@pw-update?key=abcdef -O -

        Voir les logs...
        """
        request = self.request
        required_key = getSettingValue('updates_key')
        key = request.get('key')
        if key != required_key:
            msg = "Access key doesn't match required key !!!!"
            logger.info(msg)
            return msg
        removeLDAPOrphanUsers()
        updateUsersPassword()
        now = datetime.datetime.now()
        return 'passwords updated at ' + str(now)
