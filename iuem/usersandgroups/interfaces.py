# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
import logging

from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups.tebl:interfaces')
#


class IIUEMUsersAndGroupsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IIUEMUsersAndGroupsSettings(Interface):
    """Settings"""
    ldap_uri = schema.TextLine(
        title=_(u"ldap uri"),
        description=_(u"in the form of : ldap://...."),
        required=True,
        default=u"ldap://annuaire-iuem.univ-brest.fr",
        )
    manager_dn = schema.TextLine(
        title=_(u"manager dn"),
        required=True,
        default=u"cn=admin,dc=univ-brest,dc=fr"
        )
    manager_pw = schema.Password(
        title=_(u"manager password"),
        required=True
        )
    users_base = schema.TextLine(
        title=_(u"users branch base"),
        description=_(u"in the form of : ou=people,dc=univ-brest,dc=fr"),
        required=True,
        default=u"ou=people,dc=univ-brest,dc=fr",
        )
    groups_base = schema.TextLine(
        title=_(u"groups branch base"),
        description=_(u"in the form of : ou=group,dc=univ-brest,dc=fr"),
        required=True,
        default=u"ou=group,dc=univ-brest,dc=fr",
        )
    min_gid = schema.Int(
        title=_(u"minimum GID number"),
        description=_(u"not uset yet"),
        required=True,
        default=600,
        )
    max_gid = schema.Int(
        title=_(u"maximum GID number"),
        description=_(u"not uset yet"),
        required=True,
        default=999,
        )
    updates_key = schema.TextLine(
        title=_(u"key for updates by crontab"),
        description=_(u"a string without spaces for easier usage"),
        required=True,
        default=u"abcdef"
        )


class IiuemUser(Interface):
    """Interface of IUEM user object
    """

    dn = Attribute("dn")
    uid = Attribute("uid")
    cn = Attribute("cn")
    mail = Attribute("mail")
    pw = Attribute("userPassword")
    uidNumber = Attribute("uidNumber")
    gidNumber = Attribute("gidNumber")


class IiuemGroup(Interface):
    """Interface of IUEM group object
    """

    dn = Attribute("dn")
    cn = Attribute("cn")
    gidNumber = Attribute("gidNumber")
    description = Attribute("description")
    members = Attribute("members list")

    def includesMembers(membersList):
        """returns True if membersList is included in members
        """
