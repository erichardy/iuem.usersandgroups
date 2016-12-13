# -*- coding: utf-8 -*-

from pdb import set_trace
# from dialog import Dialog
import os
import ldap

import logging
import stat
import sys
from node.ext.ldap import LDAPProps
from node.ext.ldap import LDAPConnector
from node.ext.ldap import LDAPCommunicator
from node.ext.ldap import SUBTREE

from plone import api

from iuem.usersandgroups.iuemgroup import iuemGroup
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

def getLdapProps():
    uri = getSettingValue('ldap_uri')
    admin =  getSettingValue('manager_dn')
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

def getUserByUID(uidNumber):
    """
    :param gidNumber: le GID d'un groupe LDAP
    :type gidNumber: integer
    :returns: un objet de la classe ``ldapGroup`` ou None s'il n'y a pas de
        groupe qui correspond au GID.
    """
    LDAP_SERVER = getSettingValue('ldap_uri')
    LDAP_USERS_BASE = getSettingValue('users_base')
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    l = ldap.initialize(LDAP_SERVER)
    search_filter = 'uid=%s' % uidNumber
    #
    # Cas special : root
    if uidNumber == 0:
        return 'root'

    try:
        results = l.search_s(LDAP_USERS_BASE,
                             ldap.SCOPE_SUBTREE,
                             search_filter,
                             ['cn', 'uid'])
        return results[0][1]['uid'][0]
    except Exception:
        return None


def getGroupByGID(gidNumber):
    """
    :param gidNumber: le GID d'un groupe LDAP
    :type gidNumber: integer
    :returns: un objet de la classe ``iuemGroup`` ou None s'il n'y a pas de
        groupe qui correspond au GID.
    """
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    LDAP_SERVER = getSettingValue('ldap_uri')
    LDAP_GROUPS_BASE = getSettingValue('groups_base')
    conn = ldap.initialize(LDAP_SERVER)
    search_filter = 'gidNumber=%s' % gidNumber
    results = conn.search_s(LDAP_GROUPS_BASE,
                            ldap.SCOPE_SUBTREE,
                            search_filter,
                            ['cn', 'memberUid'])
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
