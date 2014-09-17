# -*- coding: utf-8 -*-

import logging
from five import grok
from plone import api
# from plone.directives import dexterity, form
from plone.directives import form

from plone.supermodel import model
from plone.dexterity.content import Item
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


class IGroup(form.Schema):
    title = schema.TextLine(
            title=_(u"group id"),
            required=True,
            )
    gid = schema.Int(
          title=_(u'group number'),
          required=True
          )
    more_users = schema.TextLine(
            title=_(u"additional users in group"),
            description=_(u"users list, separated by comma ','"),
            required=False,
            )


class Group(Item):
    grok.implements(IGroup)
