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
            description=_("The name of the LDAP directory this \
                          folder is associated to"),
            default=u'annuaire-ldap-iuem',
            required=True,
            )
    otherLDAP = schema.Text(
            title=_(u'Other LDAP directories involved'),
            description=_(u"used to avoid duplicates (one per line)"),
            required=False
            )
    UseETCFiles = schema.Bool(
            title=_(u"Enable import/export to Users and Group files"),
            description=_(u"If enabled, users and groups folders \
                            must be present or created later..."),
            )


class ldapDirectory(Container):
    grok.implements(IldapDirectory)

    def getAclUser(self):
        try:
            aclUsers = self.acl_users[self.LDAPUserFolderName].acl_users
        except:
            return None
        return aclUsers


class View(grok.View):
    grok.context(IldapDirectory)
    grok.require('zope2.View')
    grok.template('view')
