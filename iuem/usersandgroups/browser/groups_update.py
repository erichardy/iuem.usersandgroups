# -*- coding: utf-8 -*-

import logging
import transaction
import datetime
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import (
    newSecurityManager, setSecurityManager)

from zope.publisher.browser import BrowserView

from plone import api
from iuem.usersandgroups.utils import UnrestrictedUser
from iuem.usersandgroups.utils import getGroupByCN
from iuem.usersandgroups.utils import createUser
from iuem.usersandgroups.utils import removeUserFromGroup
from iuem.usersandgroups.utils import getSettingValue

logger = logging.getLogger('iuem.usersandgroups:groups_update')


class groupsUpdate(BrowserView):

    def __call__(self):
        """
        wget http://myplone:8080/Plone/@@groups-update?key=abcdef -O -

        Voir les logs...
        """
        portal = api.portal.get()
        request = self.request
        required_key = getSettingValue('updates_key')
        key = request.get('key')
        if key != required_key:
            msg = "Access key doesn't match required key !!!!"
            logger.info(msg)
            return msg
            portal = api.portal.get()
        sm = getSecurityManager()
        try:
            # go Admin, even in anymomous mode !
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', ['Manager'], '')
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)
            plone_groups = api.group.get_groups()
            for plone_group in plone_groups:
                self.update_group(plone_group)
            transaction.commit()
        finally:
                # Restore the old security manager
                setSecurityManager(sm)
        now = datetime.datetime.now()
        # self.request.response.redirect(portal.absolute_url())
        return 'groups updated at ' + str(now)

    def update_group(self, plone_group):
        """
        Met à jour les utilisateurs du groupe plone en fonction des
        groupes ``LDAP``.

        Si un utilisateur ne fait plus partie d'aucun groupe, le compte
        plone est supprimé.
        :param group: le groupe à mettre à jour
        :type group: un objet ``group`` de plone
        :returns: ``True`` si OK, ``False`` sinon
        """
        iuem_group = getGroupByCN(plone_group)
        if not iuem_group:
            logger.info('Local group not updated : %s' % plone_group)
            return None
        # import pdb;pdb.set_trace()
        plone_members = api.user.get_users(groupname=iuem_group.cn)
        plone_uids = [m.id for m in plone_members]
        # premier passage: on verifie que les membres du groupe LDAP
        # soient membres du groupe plone.
        # si ce n'est pas le cas, on crée l'utilisateur et on
        # l'ajoute au groupe  plone
        for iuem_member in iuem_group.members:
            if iuem_member not in plone_uids:
                plone_user = createUser(iuem_member)
                if plone_user:
                    api.group.add_user(
                        groupname=plone_group.id,
                        username=plone_user.id
                        )
        # second passage, inverse celui-ci : on supprime, si nécessaire
        # un utilisateur plone d'un groupe s'il n'est plus dans un groupe ldap
        for plone_uid in plone_uids:
            if plone_uid not in iuem_group.members:
                removeUserFromGroup(plone_uid, iuem_group.cn)
