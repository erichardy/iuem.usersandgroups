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
        # import pdb;pdb.set_trace()
        user = iuemUser()
        user.dn = results[0][0]
        user.cn = result.get('cn')[0]
        user.uid = result.get('uid')[0]
        user.mail = result.get('mail')[0]
        userPassword = result.get('userPassword')
        if userPassword:
            user.pw = result.get('userPassword')[0]
        else:
            userPassword = 'xyz'
        user.uidNumber = result.get('uidNumber')[0]
        user.gidNumber = result.get('gidNumber')[0]
        return user
    except Exception:
        return None


def createUser(uid):
    """
    Crée un utilisateur Plone à partir de son compte
    dans l'annuaire ``LDAP``. Si l'``UID`` existe déjà,
    rien n'est fait, on retourne l'utilisateur.
    :param uid: uid ``ldap`` d'un utilisateur
    :type uid: str
    :returns: l'utilisateur créé ou déjà existant,
        ``None`` si pas d'utilisateur
    """
    iuem_user = getUserByUID(uid)
    if not iuem_user:
        logger.info('user %s cannot be updated' % uid)
        return None
    plone_user = api.user.get(username=iuem_user.uid)
    if plone_user:
        return plone_user
    try:
        portal = api.portal.get()
        pwds = portal.acl_users.source_users._user_passwords
        props = dict(fullname=iuem_user.cn)
        plone_user = api.user.create(
            username=iuem_user.uid,
            email=iuem_user.mail,
            properties=props)
        # transaction.commit()
        pwds[iuem_user.uid] = iuem_user.pw
        transaction.commit()
        return plone_user
    except Exception:
        return None


def removeUserFromGroup(uid, gid):
    """
    On n'opère ici que sur les groupes de Plone. Cette
    fonction est utilisée pour la synchronisation entre
    les groupes LDAP et les groupes Plone.

    Si l'utilisateur ne fait pas partir d'autres groupes,
    le compte est supprimé.
    :param uid: user ID ou cn d'un utilisateur
    :type uid: str
    :param gid: nom d'un groupe
    :type gid: str
    :returns: le groupe plone mis à jour, ou ``None``
        si opération pas possible
    """
    api.group.remove_user(groupname=gid, username=uid)
    try:
        user_groups = api.group.get_groups(username=uid)
    except Exception:
        return None
    # si seulement le groupe AuthenticatedUsers, on supprime
    if len(user_groups) == 1:
        try:
            api.user.delete(username=uid)
        except Exception:
            return None
    plone_group = api.group.get(groupname=gid)
    return plone_group


def removeLDAPOrphanUsers():
    """
    Vérifie que les utilisateurs qui ont un ``uid`` LDAP
    soient bien dans un groupe autre que AuthenticatedUsers.
    Si ce n'est pas le cas, on supprime les comptes concernés

    Cela permet, par exemple, de "nettoyer" les comptes si
    on a supprimé, sous le control panel de gestion des utilisateurs
    et groupe, un groupe qui a été créé à partir de l'annuaire LDAP
    """
    users = api.user.get_users()
    for user in users:
        uid = user.id
        if getUserByUID(uid):
            plone_groups = api.group.get_groups(username=uid)
            if len(plone_groups) <= 1:
                api.user.delete(username=uid)
                logger.info('delete %s ' % uid)


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
    try:
        group.dn = results[0][0]
        result = results[0][1]
        group.cn = result.get('cn')[0]
        group.gidNumber = result.get('gidNumber')[0]
        group.description = result.get('description')[0]
        group.members = result.get('memberUid')
        return group
    except Exception:
        return None

# Plone utilities


def createGroupAndUsers(group_cn):
    """
    :param iuem_group: le groupe d'où sont tirés les noms des users
    :type iuem_group: objet ``iuemGroup``
    :returns: ``True`` si pas de problème, ``False`` sinon.
    """
    plone_group = api.group.get(groupname=group_cn)
    iuem_group = getGroupByCN(group_cn)
    if not plone_group:
        createGroup(iuem_group)
    for u in iuem_group.members:
        plone_user = createUser(u)
        api.group.add_user(groupname=group_cn, username=plone_user.id)
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


def deleteGroupAndUsers(group_cn):
    """
    Supprime les utilisateurs d'un groupe donné. Si un utilisateur ne fait
    pas partie d'un autre groupe, il est supprimé aussi. Supprime aussi le
    le groupe. On prend aussi en compte qu'il peut y avoir un groupe local
    qui a été créé, indépendant des groupes LDAP. Donc, si un utilisateur
    fait partie de l'un de ces groupes locaux (autre
    que ``AuthenticatedUsers``), on ne supprime pas l'utilisateur

    :param iuem_group: le groupe d'où sont tirés les ``uid``
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
            logger.info('Keep : %s ' % uid)
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


def updateUsersPassword():
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
