# -*- coding: utf-8 -*-

import logging
from zope.publisher.browser import BrowserView
from AccessControl import getSecurityManager
from Products.CMFCore import permissions
import transaction

from plone import api

from iuem.usersandgroups.utils import getGroupByGID
from iuem.usersandgroups.utils import getUserByUID
from iuem.usersandgroups.utils import getIuemGroups
from iuem.usersandgroups.utils import getGroupByCN

from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class manageUsers(BrowserView):

    def __call__(self):
        # iuem_groups = getIuemGroups()
        # self.create_group_and_users('iuem')
        self.delete_group_and_users('iuem')
        # self.create_group_and_users('comiuem')
        # self.create_group_and_users('feiri')
        self.create_group_and_users('ecofluxweb')
        # self.delete_group_and_users('feiri')
        self.update_users_password()
        # import pdb;pdb.set_trace()
        

    def create_group_and_users(self, group_cn):
        """
        :param iuem_group: le groupe d'où sont tirés les noms des users
        :type iuem_group: objet ``iuemGroup``
        :returns: ``True`` si pas de problème, ``False`` sinon.
        """
        portal = api.portal.get()
        pwds = portal.acl_users.source_users._user_passwords
        group = api.group.get(groupname=group_cn)
        iuem_group = getGroupByCN(group_cn)
        if not group:
            plone_group = self.createGroup(iuem_group)
        for u in iuem_group.members:
            iuem_user = getUserByUID(u)
            try:
                dn = iuem_user.dn
                if not api.user.get(username=iuem_user.uid):
                    props = dict(fullname=iuem_user.cn)
                    user = api.user.create(
                        username=iuem_user.uid,
                        email=iuem_user.mail,
                        properties=props)
                    # transaction.commit()
                    pwds[iuem_user.uid] = iuem_user.pw
                    # transaction.commit()
                api.group.add_user(groupname=group_cn, username=iuem_user.uid)
            except Exception:
                logger.info('error: %s' % u)
        try:
            transaction.commit()
            return True
        except Exception:
            return False

    def delete_group_and_users(self, group_cn):
        """
        Supprime les utilisateurs d'un groupe donné. Si un utilisateur ne fait
        pas partie d'un autre groupe, il est supprimé aussi. Supprime aussi le
        le groupe. On prend aussi en compte qu'il peut y avoir un groupe local
        qui a été créé, indépendant des groupes LDAP. Donc, si un utilisateur
        fait partie de l'un de ces groupes locaux (autre
        que ``AuthenticatedUsers``), on ne supprime pas l'utilisateur

        :param iuem_group: le groupe d'où sont tirés les noms des users
        :type iuem_group: objet ``iuemGroup``
        :returns: ``True`` si pas de problème, ``False`` sinon.
        """
        portal = api.portal.get()
        plone_group = api.group.get(groupname=group_cn)
        # on commence par supprimer les utilisateurs qui ne font pas partie
        # d'un autre groupe
        # group = getGroupByCN(group_cn)
        if not plone_group:
            logger.info("Group %s doesn't exist" % group_cn)
            return False
        members = api.user.get_users(groupname=group_cn)
        for member in members:
            uid = member.id
            plone_groups = api.group.get_groups(username=uid)
            # si seulement 2 groupes, AuthenticatedUsers et group_cn
            # on supprime
            if len(plone_groups) == 2:
                api.user.delete(username=uid)
            else:
                logger.info('GARDER %s ' % uid)
        api.group.delete(groupname=group_cn)
        try:
            transaction.commit()
            return True
        except Exception:
            return False

    def createGroup(self, iuem_group):
        """
        :param iuem_group: le groupe à créer
        :type iuem_group: ``iuemGroup``
        :returns: l'objet ``group`` de plone
        """
        group = api.group.create(
            groupname=iuem_group.cn,
            title=iuem_group.cn,
            description=iuem_group.description,
            roles=['Member', ],
            )
        return group

    def update_users_password(self):
        users = api.user.get_users()
        portal = api.portal.get()
        pwds = portal.acl_users.source_users._user_passwords
        for user in users:
            uid = user.id
            iuem_user = getUserByUID(uid)
            pwds[uid] = iuem_user.pw
