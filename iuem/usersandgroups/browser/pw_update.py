# -*- coding: utf-8 -*-

import logging
import datetime
from zope.publisher.browser import BrowserView

from iuem.usersandgroups.utils import update_users_password
from iuem.usersandgroups.utils import getSettingValue

logger = logging.getLogger('iuem.usersandgroups:passwords_update')


class pwUpdate(BrowserView):

    def __call__(self):
        """
        wget http://myplone:8080/Plone/@@pw-update?key=abcdef -O -
        """
        request = self.request
        required_key = getSettingValue('pw_update_key')
        key = request.get('key')
        if key != required_key:
            msg = "Access key doesn't match required key !!!!"
            logger.info(msg)
            return msg
        update_users_password()
        now = datetime.datetime.now()
        return 'passwords updated at ' + str(now)
