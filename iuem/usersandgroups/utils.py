# -*- coding: utf-8 -*-

from pdb import set_trace
# from dialog import Dialog
import os
import ldap
import logging
import stat
import sys

from plone import api

logger = logging.getLogger('iuem.usersandgroups.tebl:utils')


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

LDAP_SERVER = getSettingValue('ldap_uri')
LDAP_GROUPS_BASE = getSettingValue('groups_base')

class iuemGroup(object):
    def __init__(self):
        """
        Un objet de la classe ``ldapGroup`` a trois attributs:
        ``dn`` : le *dn* LDAP (ie : 'dn')
        ``cn`` : le *cn* LDAP (ie : 'cn=ums,ou=group,dc=univ-brest,dc=fr')
        ``gid`` : le gidNumber (ie : 600)
        ``members`` : une liste des identifiants des membres du groupe
        """
        self.dn = ''
        self.cn = ''
        self.gid = 0
        self.members = []

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

def getGroupByGID(gidNumber):
    """
    :param gidNumber: le GID d'un groupe LDAP
    :type gidNumber: integer
    :returns: un objet de la classe ``ldapGroup`` ou None s'il n'y a pas de
        groupe qui correspond au GID.
    """
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    l = ldap.initialize(LDAP_SERVER)
    search_filter = 'gidNumber=%s' % gidNumber
    try:
        results = l.search_s(LDAP_GROUPS_BASE,
                             ldap.SCOPE_SUBTREE,
                             search_filter,
                             ['cn', 'memberUid'])
        xgroup = iuemGroup()
        xgroup.gid = gidNumber
        xgroup.dn = results[0][0]
        xgroup.cn = results[0][1]['cn'][0]
        if len(results) != 0:
            try:
                xgroup.members = results[0][1]['memberUid']
            except Exception:
                xgroup.members = []
        return xgroup
    except Exception:
        # Exception LDAP !!!! : on est dans les groupes locaux
        try:
            localGroup = getLocalGroup(gidNumber)
            xgroup = belougaGroup()
            xgroup.gid = gidNumber
            xgroup.dn = xgroup.cn = localGroup[0]
            xgroup.members = localGroup[2]
            return xgroup
        except Exception:
            return None
        return None
