# -*- coding: utf-8 -*-

import logging
import datetime
import transaction
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import (
    newSecurityManager, setSecurityManager)
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser

from node.ext.ldap import LDAPProps
from node.ext.ldap import LDAPConnector
from node.ext.ldap import LDAPCommunicator
from node.ext.ldap import SUBTREE

from plone import api

from iuem.usersandgroups.iuemuser import iuemUser
from iuem.usersandgroups.iuemgroup import iuemGroup

logger = logging.getLogger('iuem.usersandgroups:utils')

# Misc utilities


def getSettingValue(record):
    """
    :param record: une clé du registre de configuration
    :type record: str
    :return: la valeur enregistrée par le control panel
    """
    prefix = "iuem.usersandgroups.interfaces.IIUEMUsersAndGroupsSettings."
    prefix += record
    try:
        reg = api.portal.get_registry_record(prefix)
        return reg
    except Exception:
        logger.info("Cannot get Registry record: " + record)
        return u""

# Ldap utilities


def getLdapProps():
    uri = getSettingValue('ldap_uri')
    admin = getSettingValue('manager_dn')
    pw = getSettingValue('manager_pw')
    props = LDAPProps(uri=uri,
                      user=admin,
                      password=pw,
                      cache=False)
    return props


def getLdapCommunicator(base):
    """
    :param base: soit "users" soit "groups"
    :type base: str
    :returns: un communicateur de node.ext.ldap qui permet de réaliser
        des requêtes au serveur LDAP
    """
    props = getLdapProps()
    conn = LDAPConnector(props=props)
    comm = LDAPCommunicator(conn)
    if base in ['u', 'U', 'users']:
        comm.baseDN = getSettingValue('users_base')
    else:
        comm.baseDN = getSettingValue('groups_base')
    comm.bind()
    return comm


def getUserByUID(uid):
    """
    :param gidNumber: le GID d'un groupe LDAP
    :type gidNumber: integer
    :returns: un objet de la classe ``ldapGroup`` ou None s'il n'y a pas de
        groupe qui correspond au GID.
    """
    comm = getLdapCommunicator("u")
    search_filter = 'uid=%s' % uid
    try:
        results = comm.search(search_filter, SUBTREE)
        # return results[0][1]['uid'][0]
        result = results[0][1]
        user = iuemUser()
        user.dn = results[0][0]
        user.cn = result.get('cn')[0]
        user.uid = result.get('uid')[0]
        user.mail = result.get('mail')[0]
        user.pw = result.get('userPassword')[0]
        user.uidNumber = result.get('uidNumber')[0]
        user.gidNumber = result.get('gidNumber')[0]
        return user
    except Exception:
        return None


def getIuemGroups():
    """
    :returns: liste d'objets de type iuemGroup
    """
    comm = getLdapCommunicator("group")
    search_filter = 'objectClass=posixGroup'
    results = comm.search(search_filter, SUBTREE)
    groups = []
    for result in results:
        g = iuemGroup()
        g.dn = result[0]
        attrs = result[1]
        g.cn = attrs.get('cn')[0]
        g.gidNumber = attrs.get('gidNumber')[0]
        g.description = attrs.get('description')[0]
        g.members = attrs.get('memberUid')
        groups.append(g)
    return groups


def getGroupByGID(gidNumber):
    """
    :param gidNumber: le GID d'un groupe LDAP
    :type gidNumber: integer
    :returns: un objet de la classe ``iuemGroup`` ou None s'il n'y a pas de
        groupe qui correspond au GID.
    """
    comm = getLdapCommunicator("group")
    search_filter = 'gidNumber=%s' % gidNumber
    results = comm.search(search_filter, SUBTREE)
    group = iuemGroup()
    group.gid = gidNumber
    group.dn = results[0][0]
    group.cn = results[0][1]['cn'][0]
    if len(results) != 0:
        try:
            group.members = results[0][1]['memberUid']
        except Exception:
            group.members = []
    return group


def getGroupByCN(cn):
    """
    :param cn: le cn d'un groupe LDAP
    :type cn: str
    :returns: un objet de la classe ``iuemGroup`` ou None s'il n'y a pas de
        groupe qui correspond au GID.
    """
    comm = getLdapCommunicator("group")
    search_filter = 'cn=%s' % cn
    results = comm.search(search_filter, SUBTREE)
    group = iuemGroup()
    group.dn = results[0][0]
    result = results[0][1]
    group.cn = result.get('cn')[0]
    group.gidNumber = result.get('gidNumber')[0]
    group.description = result.get('description')[0]
    group.members = result.get('memberUid')
    return group

# Plone utilities


def create_group_and_users(group_cn):
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
        createGroup(iuem_group)
    for u in iuem_group.members:
        iuem_user = getUserByUID(u)
        try:
            if not api.user.get(username=iuem_user.uid):
                props = dict(fullname=iuem_user.cn)
                api.user.create(
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


def createGroup(iuem_group):
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


def delete_group_and_users(group_cn):
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
    plone_group = api.group.get(groupname=group_cn)
    # on commence par supprimer les utilisateurs qui ne font pas partie
    # d'un autre groupe
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


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return "AnonymousUser"


def update_users_password():
    """
    Met à jour les mots de passe des utilisateurs d'``acl_users``
    de plone à partir des mots de passe de l'annuaire ``LDAP``.
    """
    now = datetime.datetime.now()
    logger.info('Starting update passwords at ' + str(now))
    portal = api.portal.get()
    sm = getSecurityManager()
    try:
        # go Admin, even in anymomous mode !
        tmp_user = UnrestrictedUser(
            sm.getUser().getId(), '', ['Manager'], '')
        tmp_user = tmp_user.__of__(portal.acl_users)
        newSecurityManager(None, tmp_user)
        users = api.user.get_users()
        portal = api.portal.get()
        pwds = portal.acl_users.source_users._user_passwords
        for user in users:
            uid = user.id
            try:
                iuem_user = getUserByUID(uid)
                pwds[uid] = iuem_user.pw
            except Exception:
                logger.info('Cannot update password for %s' % uid)
        transaction.commit()
    finally:
            # Restore the old security manager
            setSecurityManager(sm)
    now = datetime.datetime.now()
    logger.info('Update passwords finished at ' + str(now))
