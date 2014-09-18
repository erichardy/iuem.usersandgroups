# -*- coding: utf-8 -*-

import logging
from five import grok
from plone import api
# from plone.directives import dexterity, form
from plone.directives import form

from plone.supermodel import model
from plone.dexterity.content import Container, Item
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider
from collective import dexteritytextindexer

from zope import schema
from zope.interface import Invalid

from plone.namedfile.field import NamedBlobFile

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from iuem.usersandgroups import MessageFactory as _

logger = logging.getLogger('iuem.usersandgroups')


class IldapDirectory(form.Schema):
    LDAPUserFolderName = schema.TextLine(
            title=_(u"LDAPUserFolder name"),
            description=_("The name of the LDAP directory to which this \
                          folder is associated"),
            default=u'annuaire-ldap-iuem',
            required=True,
            )


class ldapDirectory(Container):
    grok.implements(IldapDirectory)

    def getAclUser(self):
        try:
            acl_users = self.acl_users[self.LDAPUserFolderName].acl_users
        except:
            return None
        return acl_users


class View(grok.View):
    grok.context(IldapDirectory)
    grok.require('zope2.View')
    grok.template('view')
