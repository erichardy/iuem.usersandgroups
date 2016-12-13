# -*- coding: utf-8 -*-

import logging
import transaction

from node.ext.ldap import LDAPProps
from node.ext.ldap import LDAPConnector
from node.ext.ldap import LDAPCommunicator
from node.ext.ldap import SUBTREE

from plone import api

from iuem.usersandgroups.iuemuser import iuemUser
from iuem.usersandgroups.iuemgroup import iuemGroup

logger = logging.getLogger('iuem.usersandgroups.tebl:utils')

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


def update_users_password():
    users = api.user.get_users()
    portal = api.portal.get()
    pwds = portal.acl_users.source_users._user_passwords
    for user in users:
        uid = user.id
        iuem_user = getUserByUID(uid)
        pwds[uid] = iuem_user.pw


"""
conn = LDAPConnector(props=props)

conn.bind()

comm = LDAPCommunicator(conn)
comm.baseDN = 'dc=univ-brest,dc=fr'
comm.bind()
filter = '(objectClass=uboPersonne)'
filter = 'ou=people'
filter = 'uid=hardy'
filter = 'uid=ext_hardy'
res = comm.search(filter , SUBTREE)
"""

"""
[~]> ldapsearch  -H ldap://annuaire-iuem.univ-brest.fr \
-b ou=people,dc=univ-brest,dc=fr -LLL -D "cn=admin,dc=univ-brest,dc=fr" \
-W uid=hardy
Enter LDAP Password:
dn: uid=hardy,ou=people,dc=univ-brest,dc=fr
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: sambaSamAccount
objectClass: eduPerson
objectClass: supannPerson
objectClass: radiusprofile
objectClass: inetLocalMailRecipient
objectClass: uboPersonne
objectClass: shadowAccount
sn: Hardy
givenName: Eric
displayName: Eric Hardy
cn: Hardy Eric
uid: hardy
uboDateNaissance: 06/03/1955
uboMailRejet: REJECT
uboVerrou: OFF
preferredLanguage: fr
loginShell: /bin/tcsh
gecos: Eric Hardy
sambaAcctFlags: [U          ]
sambaPwdCanChange: 1126081548
sambaPwdMustChange: 2147483647
sambaPwdLastSet: 1126081548
sambaPrimaryGroupSID: S-1-5-21-3412794192-174867775-3059846230-51341
supannAliasLogin: hardy
supannCivilite: M.
supannListeRouge: FALSE
telephoneNumber: 0298498716
uboMdpInit: {crypt}gQqKAyM6vIgyM
radiusTunnelType: VLAN
radiusTunnelMediumType: IEEE-802
radiusTunnelPrivateGroupId: 132
mailHost: mailhost.univ-brest.fr
uboDateCreation: 20050830
mailLocalAddress: feiri@univ-brest.fr
mailLocalAddress: hardy@univ-brest.fr
mailLocalAddress: eric.hardy@univ-brest.fr
initials: Eric.Hardy@univ-brest.fr
mailRoutingAddress: hardy@univ-brest.fr
homeDirectory: /home/h/hardy
uidNumber: 200459
departmentNumber: ICH1
supannAffectation: UMS 3113
supannEntiteAffectation: UMS 3113
uboAffectPrincAnt: IRE2
gidNumber: 51341
uboCmp: I
uboLibelleCmp: IUEM
supannRole: heberge
supannRoleGenerique: heberge
uboListGroup: I
uboListGroup: ICH
uboListGroup: ICH1
postalAddress:: ICAgICRDT0FUTEFFUk9VTiQyOTI5MCRNSUxJWkFDJEZSQU5DRQ==
mail: Eric.Hardy@univ-brest.fr
mailForwardingAddress: hardy@univ-brest.fr
shadowMax: 99999
supannAutreMail: feiri@univ-brest.fr
supannAutreMail: hardy@univ-brest.fr
supannAutreMail: eric.hardy@univ-brest.fr
sambaSID: S-1-5-21-3412794192-174867775-3059846230-401919
eduPersonPrincipalName: hardy@univ-brest.fr
uboDateFinCompte: 20991231
supannMailPerso: hardy@univ-brest.fr
l: MILIZAC
uboTypeIndividu: H
supannEmpId: 459
supannRefId: {HARPEGE}459
eduPersonPrimaryAffiliation: employee
eduPersonAffiliation: employee
eduPersonOrgDN: dc=univ-brest,dc=fr
supannOrganisme: {CNRS}UMS 3113 - OSU
supannEtablissement: {CNRS}UMS 3113 - OSU
uboDateModif: 20130927
sambaPasswordHistory: {SSHA}AdYxS7WYG58Tu67VPxtqh2WsLjStADAsIBno/w==
sambaPasswordHistory: {SSHA}z4sU3af7f2JFVpjYm6YITJfxScHW1+YGzkKnnQ==
sambaPasswordHistory: {SSHA}ujuugevZRnEoUN4JKie7vJ1FY3Nl/dSNZMlPPg==
shadowLastChange: 20161212
userPassword:: e1NTSEF9MEhQTlk3VzNET3RzVG82WjJocDJHRGFQMVRjbTBqVk94TGtrVEE9PQ=
 =
sambaLMPassword: 00000000000000
sambaNTPassword: 7226FB1E87861BD6609574B31F531242
"""
